"""Open Area 1: fold Deniliquin in behind a 5 km road-routed boundary.

Deniliquin sits 34.9 km north of the Victorian border — nearly 20 km outside the
15 km strip — and has been an open question in every handover since the rule was
cut from 50 km to 15 km. It is now inside, on the same terms as Casino: the
routed boundary detours around the town and rejoins the corridor east and west,
so Open Area 1 stays a single continuous area rather than gaining a bolt-on ring.

One thing is different from Casino, and it is a fact about the town rather than a
choice. Deniliquin has no orbital road. Its roads are dead-end radials off the
centre, so with the town core excluded from the graph there is no connected path
at all around the west and north side — not a long one, none. No radius fixes it
either; 8 km is the best available anywhere and still only closes 9 of 12 arcs.
So the boundary follows roads where roads exist (the Cobb Highway in from
Mathoura, the Riverina Highway and Tocumwal Road out to the east) and holds a
true 5 km arc across the west and north, which is exactly what this project
already does in the Sunraysia mallee and the Snowy high country.
"""
import json, math, pathlib
from shapely.geometry import LineString, Point, shape, mapping
from shapely.ops import transform, split, unary_union
from shapely.validation import make_valid, explain_validity
import pyproj

ROOT = pathlib.Path(__file__).resolve().parent.parent
fwd = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3112", always_xy=True).transform
inv = pyproj.Transformer.from_crs("EPSG:3112", "EPSG:4326", always_xy=True).transform
P = lambda g: transform(fwd, g)
W = lambda g: transform(inv, g)

DENI     = Point(144.95658, -35.52824)   # town centre, as classified in towns.json
DEN_RAD  = 5000                           # the 5 km rule
NECK_PAD = 5000                           # neck window = gap to the band + this

def rd(p):
    pts = [tuple(map(float, s.split())) for s in p.read_text().strip().split(';')]
    return LineString([(lo, la) for la, lo in pts])

detour = rd(ROOT / 'data/oa1_deniliquin_route.txt')

fc = json.load(open(ROOT / 'data/pma.geojson'))
by = {f['properties']['id']: shape(f['geometry']) for f in fc['features']}
line = by['line_snap']

# ---- splice the detour into the routed boundary ---------------------------
c = list(line.coords)
A, B = detour.coords[0], detour.coords[-1]
ia = min(range(len(c)), key=lambda i: (c[i][0]-A[0])**2 + (c[i][1]-A[1])**2)
ib = min(range(len(c)), key=lambda i: (c[i][0]-B[0])**2 + (c[i][1]-B[1])**2)
assert ia < ib, "attachment points out of order"
line2 = LineString(c[:ia] + list(detour.coords) + c[ib+1:])
(ROOT / 'data/oa1_route_deniliquin.txt').write_text(
    ';'.join(f"{la:.4f} {lo:.4f}" for lo, la in line2.coords))
print(f"Open Area 1 routed boundary {P(line).length/1000:,.0f} km -> {P(line2).length/1000:,.0f} km "
      f"(detour {P(detour).length/1000:.1f} km replaces {P(LineString(c[ia:ib+1])).length/1000:.1f} km)")

S = json.load(open(ROOT / 'work/states.geojson'))
G = {f['properties']['STATE_NAME']: shape(f['geometry']).buffer(0) for f in S['features']}
nsw = G['New South Wales']
nswP = P(nsw)
lp = P(line2)

def ext(l, f=400_000):
    """Push both ends well outside NSW so the line cuts the state cleanly."""
    cs = list(l.coords)
    (x0, y0), (x1, y1) = cs[0], cs[1]
    a = math.hypot(x1-x0, y1-y0)
    s = (x0-(x1-x0)/a*f, y0-(y1-y0)/a*f)
    (x0, y0), (x1, y1) = cs[-1], cs[-2]
    a = math.hypot(x1-x0, y1-y0)
    e = (x0-(x1-x0)/a*f, y0-(y1-y0)/a*f)
    return LineString([s] + cs + [e])

parts = list(split(nswP, ext(lp)).geoms)
bp = P(by['border'])
cand = [g for g in parts if 1e7 < g.area < 6e10 and g.distance(bp) < 3000]
open_road = make_valid(unary_union(cand).buffer(0))
assert open_road.is_valid, explain_validity(open_road)
print(f"split into {len(parts)}; kept {[round(g.area/1e6) for g in cand]} km2")
print(f"Open Area 1 (road, Deniliquin in) {open_road.area/1e6:,.0f} km2 "
      f"(was {P(by['open_road']).area/1e6:,.0f})")

# ---- geometric: the 15 km band + a 5 km disc + the neck joining them -------
band = P(by['open_exact'])
disc = P(DENI).buffer(DEN_RAD, resolution=64)
gap  = band.distance(disc)
win  = gap + NECK_PAD
neck = unary_union([disc, band.intersection(disc.buffer(win))]).convex_hull
open_exact = make_valid(unary_union([band, disc, neck]).buffer(0))
print(f"disc edge to the 15 km band {gap/1000:.1f} km; neck window {win/1000:.1f} km")
print(f"Open Area 1 (geometric, Deniliquin in) {open_exact.area/1e6:,.0f} km2 "
      f"(band was {band.area/1e6:,.0f})")
assert len(getattr(open_road, 'geoms', [open_road])) >= 1
for nm, g in (("road", open_road), ("geometric", open_exact)):
    print(f"   Deniliquin inside ({nm}): {g.contains(P(DENI))}   "
          f"closest approach of the boundary to the town centre "
          f"{g.boundary.distance(P(DENI))/1000:.2f} km")

def F(g, p):
    w = W(g)
    if w.geom_type in ('Polygon', 'MultiPolygon') and not w.is_valid:
        w = make_valid(w)
        if w.geom_type == 'GeometryCollection':
            w = unary_union([q for q in w.geoms
                             if q.geom_type in ('Polygon', 'MultiPolygon')])
    return {"type": "Feature", "properties": p,
            "geometry": json.loads(json.dumps(mapping(w)))}

drop = {'open_road', 'open_exact', 'line_snap', 'line_deniliquin'}
feats = [f for f in fc['features'] if f['properties']['id'] not in drop]
feats += [
  F(open_exact, {"id": "open_exact", "area_km2": round(open_exact.area/1e6)}),
  F(open_road,  {"id": "open_road",  "area_km2": round(open_road.area/1e6)}),
  F(lp,         {"id": "line_snap"}),
  F(P(detour),  {"id": "line_deniliquin"}),
]
json.dump({"type": "FeatureCollection", "features": feats},
          open(ROOT / 'data/pma.geojson', 'w'))
print("\nActive PMA and town classification are recomputed downstream by "
      "build_oa2_casino_border.py.")

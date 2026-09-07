"""Open Area 2: fold Casino in behind a 5 km road-routed boundary, and hold
every PMA polygon 500 m south of the real NSW/Queensland border.

Casino sits 43.6 km from the coast — 8 km outside the 35 km strip. Rather than a
detached ring, the western boundary of Open Area 2 detours around the town and
rejoins the Summerland Way corridor north and south, so Open Area 2 stays a
single continuous area. The detour is routed the same way as every other
boundary here, with one addition: road nodes within 4.2 km of the centre of
Casino are removed from the graph before routing, so shortest paths cannot cut
back through the town.

The Queensland border used for the setback is no longer the ~1:250k state
outline the rest of the build is drawn from. It is the administrative boundary
as published in OpenStreetMap — the ways shared by the NSW and QLD
admin_level=4 relations, the same line consumer maps render. The 1:250k outline
runs a median 109 m and up to 6 km away from it, so a setback measured against
the old line would not have meant what it says.
"""
import json, pathlib
from shapely.geometry import LineString, Point, box, shape, mapping
from shapely.ops import transform, split, unary_union, linemerge
from shapely.validation import make_valid, explain_validity
import pyproj

ROOT = pathlib.Path(__file__).resolve().parent.parent
fwd = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3112", always_xy=True).transform
inv = pyproj.Transformer.from_crs("EPSG:3112", "EPSG:4326", always_xy=True).transform
P = lambda g: transform(fwd, g)
W = lambda g: transform(inv, g)

CASINO    = Point(153.048, -28.861)     # town centre used throughout the project
CAS_RAD   = 5000                         # the 5 km rule
NECK_PAD  = 5000                         # neck window = gap to the band + this
SETBACK   = 500                          # metres clear of the Queensland border
MIN_PART  = 50_000                       # drop fragments below 5 ha
SOUTH_LAT = -29.8073

def rd(p):
    pts = [tuple(map(float, s.split())) for s in p.read_text().strip().split(';')]
    return LineString([(lo, la) for la, lo in pts])

inland = rd(ROOT / 'data/oa2_route.txt')
south  = rd(ROOT / 'data/oa2_south_route.txt')
casino = rd(ROOT / 'data/oa2_casino_route.txt')

# ---- splice the Casino detour into the western boundary -------------------
c = list(inland.coords)
A, B = casino.coords[0], casino.coords[-1]
ia = min(range(len(c)), key=lambda i: (c[i][0]-A[0])**2 + (c[i][1]-A[1])**2)
ib = min(range(len(c)), key=lambda i: (c[i][0]-B[0])**2 + (c[i][1]-B[1])**2)
assert ia < ib, "attachment points out of order"
inland2 = LineString(c[:ia] + list(casino.coords) + c[ib+1:])
(ROOT / 'data/oa2_route_casino.txt').write_text(
    ';'.join(f"{la:.4f} {lo:.4f}" for lo, la in inland2.coords))
print(f"western boundary {P(inland).length/1000:.0f} km -> {P(inland2).length/1000:.0f} km "
      f"(detour {P(casino).length/1000:.1f} km replaces {P(LineString(c[ia:ib+1])).length/1000:.1f} km)")

S = json.load(open(ROOT / 'work/states.geojson'))
G = {f['properties']['STATE_NAME']: shape(f['geometry']).buffer(0) for f in S['features']}
nsw, qld, act = G['New South Wales'], G['Queensland'], G['Australian Capital Territory']
nswP, qldP, actP = P(nsw), P(qld), P(act)

# ---- the real Queensland border, from OpenStreetMap ------------------------
qb = shape(json.load(open(ROOT / 'data/qld_border.geojson'))['geometry'])
# trim the 5 km maritime tail east of Point Danger — the PMA ends at the coast
land = unary_union([nsw, qld]).buffer(0.002)
onland = qb.intersection(land)
segs = [g for g in getattr(onland, 'geoms', [onland]) if 'Line' in g.geom_type]
qb = max(segs, key=lambda g: g.length)
qbP = P(qb)
old = nsw.boundary.intersection(qld.buffer(0.0005))
oldP = P(linemerge(unary_union([g for g in getattr(old, 'geoms', [old]) if 'Line' in g.geom_type])))
print(f"NSW/QLD border: OSM {qbP.length/1000:,.0f} km / {len(qb.coords):,} vertices  "
      f"vs 1:250k outline {oldP.length/1000:,.0f} km / 313 vertices")

# everything south of that line, so no polygon can survive north of it
cut = LineString([(140.5, qb.coords[-1][1] + 0.02)] + list(qb.coords)[::-1] + [(154.6, qb.coords[0][1] - 0.02)])
whole = unary_union([nswP, actP])
pieces = list(split(whole, P(cut)).geoms)
southern = unary_union([g for g in pieces if g.difference(qldP).area > g.area * 0.5])
print(f"split NSW+ACT on the border into {len(pieces)} "
      f"({[round(g.area/1e6) for g in pieces]} km2); keeping {southern.area/1e6:,.0f} km2 south of it")
setback = qbP.buffer(SETBACK)
print(f"holding every polygon {SETBACK} m clear of it")

def clip(g):
    """Inside NSW/ACT, south of the real border, and SETBACK clear of it."""
    g = g.intersection(southern).difference(qldP).difference(setback)
    g = make_valid(g.buffer(0))
    parts = [p for p in getattr(g, 'geoms', [g])
             if p.geom_type == 'Polygon' and p.area >= MIN_PART]
    g = make_valid(unary_union(parts))
    assert g.is_valid, explain_validity(g)
    return g

# ---- Open Area 2, road-routed --------------------------------------------
region = nswP.intersection(P(box(151.0, -30.10, 154.3, -27.5)))
region = max(getattr(region, 'geoms', [region]), key=lambda g: g.area)
cut2 = LineString(
    [(153.46, south.coords[-1][1])] +
    list(south.coords)[::-1] +
    list(inland2.coords)[1:] +
    [(inland2.coords[-1][0] - 0.05, -27.60)])
parts = list(split(region, P(cut2)).geoms)
yamba = P(Point(153.34, -29.44))
oa2_road = clip(unary_union([g for g in parts if g.contains(yamba)]))
print(f"Open Area 2 (road, Casino in) {oa2_road.area/1e6:,.0f} km2")

# ---- Open Area 2, geometric: 35 km band + a 5 km disc round Casino + neck --
fc = json.load(open(ROOT / 'data/pma.geojson'))
by = {f['properties']['id']: shape(f['geometry']) for f in fc['features']}
band = P(by['open2_exact'])
disc = P(CASINO).buffer(CAS_RAD, resolution=64)
win  = band.distance(disc) + NECK_PAD      # same neck rule as Deniliquin
neck = unary_union([disc, band.intersection(disc.buffer(win))]).convex_hull
oa2_exact = clip(unary_union([band, disc, neck]))
print(f"Open Area 2 (geometric, Casino in) {oa2_exact.area/1e6:,.0f} km2 "
      f"(band was {band.area/1e6:,.0f}; neck window {win/1000:.1f} km)")

# ---- Active PMA -----------------------------------------------------------
o1e, o1r = P(by['open_exact']), P(by['open_road'])
act_exact = clip(whole.difference(o1e).difference(oa2_exact))
act_road  = clip(whole.difference(o1r).difference(oa2_road))
print(f"Active PMA road {act_road.area/1e6:,.0f} km2   exact {act_exact.area/1e6:,.0f} km2")
for nm, g in (("Open Area 2 road", oa2_road), ("Open Area 2 exact", oa2_exact),
              ("Active road", act_road), ("Active exact", act_exact)):
    print(f"   {nm:<18} into QLD {g.intersection(qldP).area:>8,.0f} m2   "
          f"clearance from the border {g.boundary.distance(qbP):,.1f} m")

def F(g, p):
    w = W(g)
    if w.geom_type in ('Polygon', 'MultiPolygon') and not w.is_valid:
        w = make_valid(w)
        if w.geom_type == 'GeometryCollection':
            w = unary_union([q for q in w.geoms
                             if q.geom_type in ('Polygon', 'MultiPolygon')])
    assert w.geom_type in ('Polygon', 'MultiPolygon', 'LineString',
                           'MultiLineString'), w.geom_type
    return {"type": "Feature", "properties": p,
            "geometry": json.loads(json.dumps(mapping(w)))}

drop = {'open2_road', 'open2_exact', 'open2_line_snap', 'active_exact', 'active_road',
        'qld_border', 'open2_line_casino'}
feats = [f for f in fc['features'] if f['properties']['id'] not in drop]
feats += [
  F(oa2_exact,  {"id": "open2_exact", "area_km2": round(oa2_exact.area/1e6)}),
  F(oa2_road,   {"id": "open2_road",  "area_km2": round(oa2_road.area/1e6)}),
  F(P(inland2), {"id": "open2_line_snap"}),
  F(P(casino),  {"id": "open2_line_casino"}),
  F(qbP,        {"id": "qld_border", "source": "OpenStreetMap admin_level=4",
                 "length_km": round(qbP.length/1000), "setback_m": SETBACK}),
  F(act_exact,  {"id": "active_exact", "area_km2": round(act_exact.area/1e6)}),
  F(act_road,   {"id": "active_road",  "area_km2": round(act_road.area/1e6)}),
]
json.dump({"type": "FeatureCollection", "features": feats},
          open(ROOT / 'data/pma.geojson', 'w'))

towns = json.load(open(ROOT / 'data/towns.json'))
moved = []
for t in towns:
    if t['s'] == 'VIC':
        continue
    pp = P(Point(t['lon'], t['lat']))
    z  = 'open' if o1e.contains(pp) else ('open2' if oa2_exact.contains(pp) else 'active')
    zr = 'open' if o1r.contains(pp) else ('open2' if oa2_road.contains(pp) else 'active')
    if (z, zr) != (t['z'], t['zr']):
        moved.append((t['n'], f"{t['z']}/{t['zr']}", f"{z}/{zr}"))
    t['z'], t['zr'] = z, zr
json.dump(towns, open(ROOT / 'data/towns.json', 'w'))
print(f"\n{len(moved)} localities changed zone (geometric/routed):")
for n, a, b_ in sorted(moved): print(f"   {n:<24} {a} -> {b_}")

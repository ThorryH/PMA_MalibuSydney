"""Open Area 2 with a road-routed southern edge (Grafton area -> coast).

Replaces the straight 29.8073 S line with a boundary that follows road
centrelines, assembled the same way as the rest of the PMA boundaries:
the geometric line is sampled every 4 km, anchors snap to the nearest OSM
road node within 12 km, and consecutive anchors are joined by Dijkstra
shortest paths.  Legs longer than 2.6x direct + 8 km keep the geometric line.
"""
import json, pickle, pathlib
from shapely.geometry import LineString, Point, box, shape, mapping
from shapely.ops import transform, split, unary_union
import pyproj

ROOT = pathlib.Path(__file__).resolve().parent.parent
fwd = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3112", always_xy=True).transform
inv = pyproj.Transformer.from_crs("EPSG:3112", "EPSG:4326", always_xy=True).transform
P = lambda g: transform(fwd, g)
W = lambda g: transform(inv, g)

def rd(p):
    pts = [tuple(map(float, s.split())) for s in p.read_text().strip().split(';')]
    return LineString([(lo, la) for la, lo in pts])

inland = rd(ROOT / 'data/oa2_route.txt')          # west edge, south -> north
south  = rd(ROOT / 'data/oa2_south_route.txt')    # south edge, west -> east
SOUTH_LAT = -29.8073
assert abs(inland.coords[0][0] - south.coords[0][0]) < 1e-6, "termini must match"

S = json.load(open(ROOT / 'work/states.geojson'))
G = {f['properties']['STATE_NAME']: shape(f['geometry']).buffer(0) for f in S['features']}
nsw, act = G['New South Wales'], G['Australian Capital Territory']
nswP = P(nsw)

# region: NSW north of -30.10 (comfortably south of the routed edge's -29.853 dip)
region = nswP.intersection(P(box(151.0, -30.10, 154.3, -27.5)))
region = max(getattr(region, 'geoms', [region]), key=lambda g: g.area)

# one continuous cut: sea -> south edge (E->W) -> inland edge (S->N) -> into QLD
cut = LineString(
    [(153.46, south.coords[-1][1])] +
    list(south.coords)[::-1] +
    list(inland.coords)[1:] +
    [(inland.coords[-1][0] - 0.05, -27.60)])
cutP = P(cut)
print("cut simple:", cutP.is_simple)

parts = list(split(region, cutP).geoms)
yamba = P(Point(153.34, -29.44))
oa2_road = unary_union([g for g in parts if g.contains(yamba)])
print(f"split into {len(parts)}: {[round(g.area/1e6) for g in parts]}")
print(f"Open Area 2 (road, routed south edge) {oa2_road.area/1e6:,.0f} km2")

fc = json.load(open(ROOT / 'data/pma.geojson'))
by = {f['properties']['id']: shape(f['geometry']) for f in fc['features']}
oa2_exact = P(by['open2_exact'])
o1e, o1r = P(by['open_exact']), P(by['open_road'])
whole = unary_union([nswP, P(act)])
act_exact = whole.difference(o1e).difference(oa2_exact)
act_road  = whole.difference(o1r).difference(oa2_road)
print(f"Active PMA road {act_road.area/1e6:,.0f} km2   exact {act_exact.area/1e6:,.0f} km2")
print(f"southern edge: routed {P(south).length/1000:.1f} km "
      f"vs straight {P(LineString([(152.8899,SOUTH_LAT),(153.2902,SOUTH_LAT)])).length/1000:.1f} km")

F = lambda g, p: {"type": "Feature", "properties": p,
                  "geometry": json.loads(json.dumps(mapping(W(g))))}
drop = {'open2_road', 'open2_line_south', 'open2_line_south_exact',
        'active_exact', 'active_road'}
feats = [f for f in fc['features'] if f['properties']['id'] not in drop]
feats += [
  F(oa2_road,  {"id": "open2_road", "area_km2": round(oa2_road.area/1e6)}),
  F(P(south),  {"id": "open2_line_south"}),
  F(P(LineString([(152.8899, SOUTH_LAT), (153.36, SOUTH_LAT)])),
               {"id": "open2_line_south_exact"}),
  F(act_exact, {"id": "active_exact", "area_km2": round(act_exact.area/1e6)}),
  F(act_road,  {"id": "active_road",  "area_km2": round(act_road.area/1e6)}),
]
json.dump({"type": "FeatureCollection", "features": feats},
          open(ROOT / 'data/pma.geojson', 'w'))

# reclassify the routed zone for every locality
towns = json.load(open(ROOT / 'data/towns.json'))
moved = []
for t in towns:
    if t['s'] == 'VIC':
        continue
    pp = P(Point(t['lon'], t['lat']))
    zr = 'open' if o1r.contains(pp) else ('open2' if oa2_road.contains(pp) else 'active')
    if zr != t['zr']:
        moved.append((t['n'], t['zr'], zr))
    t['zr'] = zr
json.dump(towns, open(ROOT / 'data/towns.json', 'w'))
print(f"\n{len(moved)} localities changed routed zone:")
for n, a, b in sorted(moved): print(f"   {n:<22} {a} -> {b}")

print("\nspot checks (routed):")
for nm, lo, la in [("Grafton",152.9336,-29.6876),("South Grafton",152.9255,-29.7047),
  ("Clarenza",152.955,-29.723),("Bom Bom",152.93713,-29.76173),("Braunstone",152.96667,-29.8),
  ("Mcphersons Crossing",152.917,-29.8107),("Coutts Crossing",152.88333,-29.81667),
  ("Glenugie",153.02139,-29.81954),("Pillar Valley",153.14946,-29.77799),
  ("Minnie Water",153.2982,-29.77651),("Diggers Camp",153.28808,-29.81476),
  ("Lake Hiawatha",153.25919,-29.80389),("Wooli",153.26239,-29.85296),
  ("Copmanhurst",152.792,-29.605)]:
    p = P(Point(lo, la))
    print(f"   {nm:<20} road={'IN ' if oa2_road.contains(p) else 'out'}  "
          f"exact={'IN ' if oa2_exact.contains(p) else 'out'}")

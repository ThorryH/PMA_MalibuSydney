import json, math, pickle
from shapely.geometry import LineString, Polygon, box, shape, Point
from shapely.ops import transform, split, unary_union
import pyproj
fwd=pyproj.Transformer.from_crs("EPSG:4326","EPSG:3112",always_xy=True).transform
inv=pyproj.Transformer.from_crs("EPSG:3112","EPSG:4326",always_xy=True).transform
P=lambda g: transform(fwd,g); W=lambda g: transform(inv,g)

pts=[tuple(map(float,s.split())) for s in open('oa2_route.txt').read().strip().split(';')]
route=LineString([(lo,la) for la,lo in pts])
rp=P(route)
SOUTH=pts[0][0]                                     # southern terminus latitude
print(f"OA2 routed boundary {rp.length/1000:.0f} km, southern edge at lat {SOUTH}")

G={f['properties']['STATE_NAME']:shape(f['geometry']).buffer(0) for f in json.load(open('states.geojson'))['features']}
nsw,act=G['New South Wales'],G['Australian Capital Territory']
nswP=P(nsw)
north=P(box(151.0,SOUTH,154.3,-27.5))
region=nswP.intersection(north)
region=max(getattr(region,'geoms',[region]),key=lambda g:g.area) if region.geom_type=='MultiPolygon' else region

def ext(l):
    # exit the region through its southern edge and through the QLD border
    c=list(l.coords)
    s=P(Point(pts[0][1]-0.05, SOUTH-0.5))
    e=P(Point(pts[-1][1]-0.05, -27.6))
    return LineString([(s.x,s.y)]+c+[(e.x,e.y)])

parts=list(split(region,ext(rp)).geoms)
print("split areas:",[round(g.area/1e6) for g in parts])
mid=rp.interpolate(0.5,normalized=True)
east=unary_union([g for g in parts if g.representative_point().x > mid.x])
oa2_road=unary_union([g for g in getattr(east,'geoms',[east]) if g.area>1e7])
print(f"Open Area 2 (road) {oa2_road.area/1e6:,.0f} km2")

d=pickle.load(open('oa2.pkl','rb'))
coastP=d['coastP']; D=d['D']
oa2_exact=nswP.intersection(coastP.buffer(D,resolution=48)).intersection(north)
oa2_exact=max(getattr(oa2_exact,'geoms',[oa2_exact]),key=lambda g:g.area) if oa2_exact.geom_type=='MultiPolygon' else oa2_exact
print(f"Open Area 2 (exact 35 km) {oa2_exact.area/1e6:,.0f} km2")

south_line=P(LineString([(pts[0][1],SOUTH),(153.36,SOUTH)]))

fc=json.load(open('pma.geojson'))
drop={'open2_exact','open2_road','open2_line_snap','open2_line_south','grafton_ring','active_exact','active_road'}
feats=[f for f in fc['features'] if f['properties']['id'] not in drop]
by={f['properties']['id']:shape(f['geometry']) for f in feats}
whole=unary_union([nswP,P(act)])
o1e,o1r=P(by['open_exact']),P(by['open_road'])
act_exact=whole.difference(o1e).difference(oa2_exact)
act_road =whole.difference(o1r).difference(oa2_road)
def F(g,p): return {"type":"Feature","properties":p,
  "geometry":json.loads(json.dumps(__import__('shapely').geometry.mapping(W(g))))}
feats += [F(oa2_exact,{"id":"open2_exact","area_km2":round(oa2_exact.area/1e6)}),
          F(oa2_road ,{"id":"open2_road","area_km2":round(oa2_road.area/1e6)}),
          F(rp,{"id":"open2_line_snap"}),
          F(south_line,{"id":"open2_line_south"}),
          F(act_exact,{"id":"active_exact","area_km2":round(act_exact.area/1e6)}),
          F(act_road ,{"id":"active_road","area_km2":round(act_road.area/1e6)})]
json.dump({"type":"FeatureCollection","features":feats},open('pma.geojson','w'))
print("active exact",round(act_exact.area/1e6),"active road",round(act_road.area/1e6))
for nm,lo,la in [("Grafton",152.9336,-29.6876),("South Grafton",152.9255,-29.7047),
  ("Clarenza",152.955,-29.723),("Junction Hill",152.947,-29.629),("Waterview Hts",152.870,-29.706),
  ("Ulmarra",153.038,-29.615),("Copmanhurst",152.792,-29.605),("Coutts Crossing",152.892,-29.836),
  ("Casino",153.048,-28.861),("Lismore",153.276,-28.813),("Kyogle",152.985,-28.618)]:
    p=P(Point(lo,la)); print(f"  {nm:<16} road={'IN ' if oa2_road.contains(p) else 'out'}  exact={'IN ' if oa2_exact.contains(p) else 'out'}")

import json, math
from shapely.geometry import LineString, MultiLineString, shape, Point
from shapely.ops import transform, split, unary_union
import pyproj
fwd=pyproj.Transformer.from_crs("EPSG:4326","EPSG:3112",always_xy=True).transform
inv=pyproj.Transformer.from_crs("EPSG:3112","EPSG:4326",always_xy=True).transform
P=lambda g: transform(fwd,g); W=lambda g: transform(inv,g)

def rd(f): return [tuple(map(float,s.split())) for s in open(f).read().strip().split(';')]
pts=[]
for f in ['oa1_route0.txt','oa1_route1a.txt','oa1_route1b.txt','oa1_route2a.txt']:
    pts += rd(f)
pts += [(la,lo) for la,lo in json.load(open('s2b.json'))]

# drop out-and-back spurs and keep a west->east progression
clean=[]
for p in pts:
    if clean and abs(p[0]-clean[-1][0])<1e-6 and abs(p[1]-clean[-1][1])<1e-6: continue
    clean.append(p)
line=LineString([(lo,la) for la,lo in clean])
lp=P(line)
print(f"assembled road boundary: {lp.length/1000:.0f} km, {len(clean)} pts")

G={f['properties']['STATE_NAME']:shape(f['geometry']).buffer(0) for f in json.load(open('states.geojson'))['features']}
nsw,act=G['New South Wales'],G['Australian Capital Territory']
nswP=P(nsw)

def ext(l,f=400_000):
    c=list(l.coords)
    (x0,y0),(x1,y1)=c[0],c[1];  a=math.hypot(x1-x0,y1-y0)
    s=(x0-(x1-x0)/a*f, y0-(y1-y0)/a*f)
    (x0,y0),(x1,y1)=c[-1],c[-2]; a=math.hypot(x1-x0,y1-y0)
    e=(x0-(x1-x0)/a*f, y0-(y1-y0)/a*f)
    return LineString([s]+c+[e])

parts=list(split(nswP,ext(lp)).geoms)
print("split areas km2:",[round(g.area/1e6) for g in parts])
fcx=json.load(open('pma.geojson'))
bp=P(shape([f for f in fcx['features'] if f['properties']['id']=='border'][0]['geometry']))
cand=[g for g in parts if g.area>1e7 and g.area<2e11 and g.distance(bp)<3000 and g.area<1.5e11]
cand=[g for g in cand if g.area < 6e10]
strip=unary_union(cand)
print("kept pieces:",[round(g.area/1e6) for g in cand])
print(f"Open Area 1 (road) {strip.area/1e6:,.0f} km2")

fc=json.load(open('pma.geojson'))
feats=[f for f in fc['features'] if f['properties']['id'] not in ('open_road','line_snap','active_road')]
by={f['properties']['id']:shape(f['geometry']) for f in feats}
whole=unary_union([nswP,P(act)])
o2r=P(by['open2_road'])
act_road=whole.difference(strip).difference(o2r)
def F(g,p): return {"type":"Feature","properties":p,
    "geometry":json.loads(json.dumps(__import__('shapely').geometry.mapping(W(g))))}
feats += [F(strip,{"id":"open_road","area_km2":round(strip.area/1e6)}),
          F(lp,{"id":"line_snap"}),
          F(act_road,{"id":"active_road","area_km2":round(act_road.area/1e6)})]
json.dump({"type":"FeatureCollection","features":feats},open('pma.geojson','w'))
print("active (road)",round(act_road.area/1e6))
print("ids:",[f['properties']['id'] for f in feats])

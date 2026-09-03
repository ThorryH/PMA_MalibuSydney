import json, math, pickle
from shapely.geometry import shape, Point, LineString, box, MultiLineString
from shapely.ops import unary_union, transform, linemerge, split
import pyproj
fwd=pyproj.Transformer.from_crs("EPSG:4326","EPSG:3112",always_xy=True).transform
inv=pyproj.Transformer.from_crs("EPSG:3112","EPSG:4326",always_xy=True).transform
P=lambda g: transform(fwd,g); W=lambda g: transform(inv,g)

d=pickle.load(open('oa2.pkl','rb'))
nswP, inland, D = d['nswP'], d['inland'], d['D']
GRAF_LAT=-29.6876; GRAF=Point(152.9336,GRAF_LAT)
north=P(box(151.0,GRAF_LAT,154.3,-27.5))

G={f['properties']['STATE_NAME']:shape(f['geometry']).buffer(0) for f in json.load(open('states.geojson'))['features']}
nsw,act=G['New South Wales'],G['Australian Capital Territory']

# ---------- exact ----------
oa2_exact = d['oa2']
print(f"OA2 exact      {oa2_exact.area/1e6:,.0f} km2")

# ---------- road-snapped ----------
snap=json.load(open('snap2.json'))
LIMIT=8.0
exact_pts=[inland.interpolate(min(i*4000,inland.length)) for i in range(len(snap))]
pts=[]
for (lat,lon,dd,nm,cls),ep in zip(snap,exact_pts):
    if dd is not None and dd<=LIMIT: pts.append((P(Point(lon,lat)),nm,dd))
    else: pts.append((ep,'(50 km line)',None))
# order south -> north, drop backtracks
pts.sort(key=lambda t:t[0].y)
keep=[]
for p,nm,dd in pts:
    if keep and p.y<=keep[-1][0].y+800: continue
    keep.append((p,nm,dd))
line=LineString([(p.x,p.y) for p,_,_ in keep]).simplify(900)
print(f"road line: {line.length/1000:.0f} km, {len(line.coords)} verts; "
      f"{sum(1 for _,_,dd in keep if dd is not None)}/{len(keep)} on a road")

def extend(l,f=400_000):
    c=list(l.coords)
    (x0,y0),(x1,y1)=c[0],c[1];  a=math.hypot(x1-x0,y1-y0)
    s=(x0-(x1-x0)/a*f, y0-(y1-y0)/a*f)
    (x0,y0),(x1,y1)=c[-1],c[-2]; a=math.hypot(x1-x0,y1-y0)
    e=(x0-(x1-x0)/a*f, y0-(y1-y0)/a*f)
    return LineString([s]+c+[e])

region=nswP.intersection(north)
region=max(getattr(region,'geoms',[region]),key=lambda g:g.area) if region.geom_type=='MultiPolygon' else region
parts=list(split(region,extend(line,120_000)).geoms)
print('split parts',[round(g.area/1e6) for g in parts])
east=unary_union([g for g in parts if g.representative_point().x>line.interpolate(0.5,normalized=True).x])
oa2_road=unary_union([g for g in getattr(east,'geoms',[east]) if g.area>1e7])
print(f"OA2 road-snap  {oa2_road.area/1e6:,.0f} km2")

# southern edge line (Grafton straight to the coast)
south_line=P(LineString([(GRAF.x,GRAF_LAT),(153.3248,GRAF_LAT)]))

# ---------- rebuild everything ----------
fc=json.load(open('pma.geojson'))
by={f['properties']['id']:shape(f['geometry']) for f in fc['features']}
o1e,o1r = P(by['open_exact']), P(by['open_road'])
whole = unary_union([nswP,P(act)])
act_exact = whole.difference(o1e).difference(oa2_exact)
act_road  = whole.difference(o1r).difference(oa2_road)
print(f"active exact   {act_exact.area/1e6:,.0f} km2")
print(f"active road    {act_road.area/1e6:,.0f} km2")

def F(g,props): return {"type":"Feature","properties":props,"geometry":json.loads(json.dumps(
    __import__('shapely').geometry.mapping(W(g))))}
feats=[]
for f in fc['features']:
    i=f['properties']['id']
    if i in ('active_exact','active_road','open2_exact','open2_road','open2_line_exact',
             'open2_line_snap','open2_line_south','coast'): continue
    feats.append(f)
feats += [
  F(act_exact ,{"id":"active_exact","area_km2":round(act_exact.area/1e6)}),
  F(act_road  ,{"id":"active_road","area_km2":round(act_road.area/1e6)}),
  F(oa2_exact ,{"id":"open2_exact","area_km2":round(oa2_exact.area/1e6)}),
  F(oa2_road  ,{"id":"open2_road","area_km2":round(oa2_road.area/1e6)}),
  F(inland    ,{"id":"open2_line_exact"}),
  F(line      ,{"id":"open2_line_snap"}),
  F(south_line,{"id":"open2_line_south"}),
  F(d['coastP'],{"id":"coast"}),
]
json.dump({"type":"FeatureCollection","features":feats},open('pma.geojson','w'))
pickle.dump({'oa2_exact':oa2_exact,'oa2_road':oa2_road},open('oa2b.pkl','wb'))
print("written")

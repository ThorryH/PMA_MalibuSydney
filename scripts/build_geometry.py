import json, math, csv
import numpy as np
from shapely.geometry import shape, mapping, LineString, Point, box
from shapely.ops import unary_union, linemerge, transform, split, nearest_points
from shapely.strtree import STRtree
import pyproj

fwd=pyproj.Transformer.from_crs("EPSG:4326","EPSG:3112",always_xy=True).transform
inv=pyproj.Transformer.from_crs("EPSG:3112","EPSG:4326",always_xy=True).transform
P=lambda g: transform(fwd,g); W=lambda g: transform(inv,g)

G={f['properties']['STATE_NAME']:shape(f['geometry']).buffer(0)
   for f in json.load(open('states.geojson'))['features']}
nsw,vic,act=G['New South Wales'],G['Victoria'],G['Australian Capital Territory']

raw=nsw.boundary.intersection(vic.buffer(0.0035))
lines=[g for g in getattr(raw,'geoms',[raw]) if 'Line' in g.geom_type]
m=linemerge(unary_union(lines))
segs=[g for g in getattr(m,'geoms',[m]) if g.length>0.02]
from shapely.geometry import MultiLineString
border=MultiLineString(segs)
print('border segments',len(segs))
nswP,actP,borderP=P(nsw),P(act),P(border)
BL=borderP.length
print(f"border {BL/1000:.0f} km")

D=50_000.0
buf=borderP.buffer(D,resolution=48)
print('buffer type',buf.geom_type)
if buf.geom_type=='MultiPolygon': buf=max(buf.geoms,key=lambda g:g.area)
strip_exact=buf.intersection(nswP)
strip_exact=max(getattr(strip_exact,'geoms',[strip_exact]),key=lambda g:g.area) if strip_exact.geom_type=='MultiPolygon' else strip_exact
print(f"exact strip {strip_exact.area/1e6:,.0f} km2  mean width {strip_exact.area/BL/1000:.1f} km")

off=buf.exterior.intersection(nswP.buffer(800))
offline=max([g for g in getattr(off,'geoms',[off]) if 'Line' in g.geom_type],key=lambda g:g.length)
c=list(offline.coords)
if c[0][0]>c[-1][0]: c=c[::-1]
offline=LineString(c)
print(f"offset line {offline.length/1000:.0f} km, {len(c)} verts")

# roads (Natural Earth 10m) ------------------------------------------------
bb=box(139.5,-38.6,151.6,-32.4)
rgeo=[]
for f in json.load(open('ne_roads.geojson'))['features']:
    if f['properties'].get('type') not in ('Major Highway','Secondary Highway','Road'): continue
    g=shape(f['geometry'])
    if g.intersects(bb): rgeo.append(g.intersection(bb))
roadsP=P(unary_union(rgeo))
roadparts=list(getattr(roadsP,'geoms',[roadsP]))
print("road parts",len(roadparts))

# localities ---------------------------------------------------------------
towns=[]
seen=set()
with open('auspost.csv',newline='',encoding='utf-8',errors='replace') as fh:
    for r in csv.DictReader(fh):
        if r['state'] not in ('NSW','VIC'): continue
        try: lo,la=float(r['long']),float(r['lat'])
        except: continue
        if not(140.5<lo<151.0 and -38.5<la<-32.5): continue
        k=(r['locality'].title(),r['state'])
        if k in seen: continue
        seen.add(k); towns.append((k[0],k[1],lo,la))
tp=[P(Point(lo,la)) for _,_,lo,la in towns]
ttree=STRtree(tp)
print("localities",len(towns))

# snap ---------------------------------------------------------------------
SEARCH=25_000.0; STEP=10_000.0
L=offline.length; n=int(L//STEP)
samples=[offline.interpolate(min(i*STEP,L)) for i in range(n+1)]
snap=[];  hits=0; dists=[]
for p in samples:
    q=nearest_points(p,roadsP)[1]; dd=p.distance(q); dists.append(dd)
    if dd<=SEARCH: snap.append(q); hits+=1
    else: snap.append(p)
print(f"snapped {hits}/{len(samples)}  median dist to road {np.median(dists)/1000:.1f} km")

sn=[]
for pt in snap:
    if sn and pt.x<=sn[-1].x+2000: continue
    sn.append(pt)
line_snap=LineString([(p.x,p.y) for p in sn]).simplify(2000)

def ext(l,f=500_000):
    cs=list(l.coords)
    (x0,y0),(x1,y1)=cs[0],cs[1]; a=math.hypot(x1-x0,y1-y0)
    s=(x0-(x1-x0)/a*f, y0-(y1-y0)/a*f)
    (x0,y0),(x1,y1)=cs[-1],cs[-2]; a=math.hypot(x1-x0,y1-y0)
    e=(x0-(x1-x0)/a*f, y0-(y1-y0)/a*f)
    return LineString([s]+cs+[e])

parts=list(split(nswP,ext(line_snap)).geoms)
strip_road=unary_union([g for g in parts if g.distance(borderP)<2000 and g.representative_point().y<nswP.centroid.y])
print(f"road strip {strip_road.area/1e6:,.0f} km2  mean width {strip_road.area/BL/1000:.1f} km")

whole=unary_union([nswP,actP])
active_exact=whole.difference(strip_exact)
active_road=whole.difference(strip_road)

# control towns: localities within 12 km of the exact 50 km line
ctrl=[]
for i,(nm,st,lo,la) in enumerate(towns):
    if st!='NSW': continue
    dd=tp[i].distance(offline)
    if dd<12_000:
        ctrl.append({"name":nm,"lon":lo,"lat":la,
                     "d_border_km":round(tp[i].distance(borderP)/1000,1),
                     "d_line_km":round(dd/1000,1)})
ctrl.sort(key=lambda t:t['lon'])
print("control towns on the line:",len(ctrl))
for t in ctrl[:60]: print(" ",t['name'],t['d_border_km'])

def F(g,props): return {"type":"Feature","properties":props,"geometry":mapping(W(g))}
fc={"type":"FeatureCollection","features":[
 F(borderP,{"id":"border"}),
 F(strip_exact,{"id":"open_exact","area_km2":round(strip_exact.area/1e6)}),
 F(strip_road ,{"id":"open_road","area_km2":round(strip_road.area/1e6)}),
 F(active_exact,{"id":"active_exact","area_km2":round(active_exact.area/1e6)}),
 F(active_road ,{"id":"active_road","area_km2":round(active_road.area/1e6)}),
 F(offline,{"id":"line_exact"}),
 F(line_snap,{"id":"line_snap"}),
]}
json.dump(fc,open('pma.geojson','w'))
json.dump(ctrl,open('towns.json','w'))
print("written")

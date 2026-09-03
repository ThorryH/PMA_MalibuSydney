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

D=15_000.0
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

# Open Area 1 road boundary is produced separately from OSM data by
# build_oa1_route.py; geo2.py emits the exact geometry only.
strip_road=strip_exact
line_snap=offline

whole=unary_union([nswP,actP])
active_exact=whole.difference(strip_exact)
active_road=whole.difference(strip_road)

def F(g,props): return {"type":"Feature","properties":props,"geometry":mapping(W(g))}
fc={"type":"FeatureCollection","features":[
 F(borderP,{"id":"border"}),
 F(strip_exact,{"id":"open_exact","area_km2":round(strip_exact.area/1e6)}),
 F(active_exact,{"id":"active_exact","area_km2":round(active_exact.area/1e6)}),
 F(active_road ,{"id":"active_road","area_km2":round(active_road.area/1e6)}),
 F(offline,{"id":"line_exact"}),
]}
json.dump(fc,open('pma.geojson','w'))
print("written")

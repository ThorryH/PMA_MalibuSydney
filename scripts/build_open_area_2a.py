import json, math
from shapely.geometry import shape, Point, LineString, box, MultiLineString
from shapely.ops import unary_union, transform, linemerge, nearest_points, split
import pyproj
fwd=pyproj.Transformer.from_crs("EPSG:4326","EPSG:3112",always_xy=True).transform
inv=pyproj.Transformer.from_crs("EPSG:3112","EPSG:4326",always_xy=True).transform
P=lambda g: transform(fwd,g); W=lambda g: transform(inv,g)

G={f['properties']['STATE_NAME']:shape(f['geometry']).buffer(0) for f in json.load(open('states.geojson'))['features']}
nsw,qld,act=G['New South Wales'],G['Queensland'],G['Australian Capital Territory']

REG=box(151.4,-30.6,153.95,-27.9)
bnd=nsw.boundary.intersection(REG)
parts=[]
for g in getattr(bnd,'geoms',[bnd]):
    if 'Line' not in g.geom_type: continue
    d=g.difference(qld.buffer(0.02))
    for h in getattr(d,'geoms',[d]):
        if 'Line' in h.geom_type and h.length>0.05: parts.append(h)
coast=max(getattr(linemerge(unary_union(parts)),'geoms',[linemerge(unary_union(parts))]),key=lambda g:g.length)
coastP=P(coast)

GRAF=Point(152.9336,-29.6876)          # Grafton
grafP=P(GRAF)
cp=nearest_points(grafP,coastP)[1]
D=grafP.distance(cp)
print(f"Grafton -> nearest coast: {D/1000:.1f} km at {[round(v,4) for v in transform(inv,cp).coords[0]]}")

# southern edge: due east from Grafton to the coast (constant latitude)
east=LineString([(GRAF.x,GRAF.y),(154.2,GRAF.y)])
hit=east.intersection(nsw.boundary)
pts=[p for p in getattr(hit,'geoms',[hit]) if p.geom_type=='Point']
xend=max(p.x for p in pts) if pts else 153.4
south=LineString([(GRAF.x-0.6,GRAF.y),(xend+0.15,GRAF.y)])
print("due-east line hits coast at lon",round(xend,4),
      "=> ",round(P(LineString([(GRAF.x,GRAF.y),(xend,GRAF.y)])).length/1000,1),"km due east")

# exact Open Area 2: within D of the coast, north of Grafton's latitude, inside NSW
band=coastP.buffer(D,resolution=48)
nswP=P(nsw)
north=P(box(151.0,GRAF.y,154.3,-27.5))
oa2=nswP.intersection(band).intersection(north)
oa2=max(getattr(oa2,'geoms',[oa2]),key=lambda g:g.area) if oa2.geom_type=='MultiPolygon' else oa2
print(f"Open Area 2 (exact): {oa2.area/1e6:,.0f} km2")

# inland boundary line = the western edge of the band inside NSW, north of Grafton
inland=band.exterior.intersection(nswP.buffer(600)).intersection(north.buffer(600))
il=[g for g in getattr(inland,'geoms',[inland]) if 'Line' in g.geom_type]
inland=max(il,key=lambda g:g.length)
c=list(inland.coords)
if c[0][1]>c[-1][1]: c=c[::-1]     # south -> north
inland=LineString(c)
print(f"inland boundary line: {inland.length/1000:.0f} km, {len(c)} verts")

json.dump({"D":D,"graf":[GRAF.x,GRAF.y],"xend":xend}, open('oa2_params.json','w'))
import pickle
pickle.dump({'coastP':coastP,'oa2':oa2,'inland':inland,'south':P(south),'nswP':nswP,'north':north,'D':D},
            open('oa2.pkl','wb'))

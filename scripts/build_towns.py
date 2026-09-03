import json,csv
from shapely.geometry import shape, Point
from shapely.ops import transform
import pyproj
fwd=pyproj.Transformer.from_crs("EPSG:4326","EPSG:3112",always_xy=True).transform
P=lambda g: transform(fwd,g)
fc=json.load(open('pma.geojson'))
by={f['properties']['id']:shape(f['geometry']) for f in fc['features']}
borderP=P(by['border']); openE=P(by['open_exact']); openR=P(by['open_road'])
nsw=shape([f for f in json.load(open('states.geojson'))['features'] if f['properties']['STATE_NAME']=='New South Wales'][0]['geometry']).buffer(0)
vic=shape([f for f in json.load(open('states.geojson'))['features'] if f['properties']['STATE_NAME']=='Victoria'][0]['geometry']).buffer(0)

KEY={'DENILIQUIN','MOAMA','ALBURY','CULCAIRN','JERILDERIE','FINLEY','COROWA','TOCUMWAL','BAROOGA','MULWALA','HOWLONG','HOLBROOK','HENTY','URANA','BERRIGAN','MOULAMEIN','BALRANALD','WENTWORTH','BURONGA','DARETON','EUSTON','HAY','NARRANDERA','WAGGA WAGGA','GRIFFITH','LEETON','TUMBARUMBA','KHANCOBAN','JINDABYNE','BOMBALA','DELEGATE','EDEN','MERIMBULA','BEGA','COOMA','BARHAM','TOOLEYBUC','WAKOOL','CONARGO','MATHOURA','WANGANELLA','OAKLANDS','WALLA WALLA','LOCKHART','THE ROCK','TUMUT','BATLOW','QUEANBEYAN','NIMMITABEL','PAMBULA','CANBERRA','GUNDAGAI','COOTAMUNDRA','TEMORA','YOUNG','COROWA','WENTWORTH','HILLSTON','IVANHOE','MENINDEE','BROKEN HILL','POONCARIE','SYDNEY','NEWCASTLE','WOLLONGONG','DUBBO','ORANGE','BATHURST','NOWRA','BATEMANS BAY','ULLADULLA','GOULBURN','MOAMA','ECHUCA','SWAN HILL','MILDURA','SHEPPARTON','WODONGA','WANGARATTA'}
seen={}; out=[]
for r in csv.DictReader(open('auspost.csv',newline='',encoding='utf-8',errors='replace')):
    if r['state'] not in ('NSW','VIC','ACT'): continue
    if r.get('type')!='Delivery Area': continue
    try: lo=float(r['Long_precise']); la=float(r['Lat_precise'])
    except: continue
    nm=r['locality'].title()
    k=(nm,r['state'])
    if k in seen: continue
    if not(140.7<lo<151.5 and -38.4<la<-32.6): continue
    seen[k]=1
    p=Point(lo,la); pp=P(p)
    if r['state']=='NSW' and not nsw.buffer(0.02).contains(p): continue
    if r['state']=='VIC' and not vic.buffer(0.02).contains(p): continue
    db=pp.distance(borderP)/1000
    if db>200: continue
    zone='vic' if r['state']=='VIC' else ('open' if openE.contains(pp) else 'active')
    zr  = 'vic' if r['state']=='VIC' else ('open' if openR.contains(pp) else 'active')
    out.append({"n":nm,"s":r['state'],"lon":round(lo,5),"lat":round(la,5),
                "d":round(db,1),"z":zone,"zr":zr,"k":1 if r['locality'].upper() in KEY else 0})
out.sort(key=lambda t:(-t['k'],t['n']))
json.dump(out,open('towns.json','w'))
print(len(out),'towns;',sum(t['k'] for t in out),'key')
for t in out:
    if t['k'] and t['s']=='NSW': print(f"  {t['n']:<14} {t['d']:>6.1f} km  exact={t['z']:<6} road={t['zr']}")

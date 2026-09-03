import json,csv
from shapely.geometry import shape, Point
from shapely.ops import transform
import pyproj
fwd=pyproj.Transformer.from_crs("EPSG:4326","EPSG:3112",always_xy=True).transform
P=lambda g: transform(fwd,g)
fc=json.load(open('pma.geojson'))
by={f['properties']['id']:shape(f['geometry']) for f in fc['features']}
borderP=P(by['border']); openE=P(by['open_exact']); openR=P(by['open_road'])
o2E=P(by['open2_exact']); o2R=P(by['open2_road'])
import pickle
coastP=pickle.load(open('oa2.pkl','rb'))['coastP']
S={f['properties']['STATE_NAME']:shape(f['geometry']).buffer(0) for f in json.load(open('states.geojson'))['features']}
nsw,vic=S['New South Wales'],S['Victoria']

KEY=set("""DENILIQUIN MOAMA ALBURY CULCAIRN JERILDERIE FINLEY COROWA TOCUMWAL BAROOGA MULWALA HOWLONG HOLBROOK
HENTY URANA BERRIGAN MOULAMEIN BALRANALD WENTWORTH BURONGA DARETON EUSTON HAY NARRANDERA WAGGA WAGGA GRIFFITH
LEETON TUMBARUMBA KHANCOBAN JINDABYNE BOMBALA DELEGATE EDEN MERIMBULA BEGA COOMA BARHAM TOOLEYBUC WAKOOL
CONARGO MATHOURA WANGANELLA OAKLANDS WALLA WALLA LOCKHART THE ROCK TUMUT BATLOW QUEANBEYAN NIMMITABEL PAMBULA
GUNDAGAI COOTAMUNDRA TEMORA YOUNG HILLSTON IVANHOE MENINDEE BROKEN HILL POONCARIE SYDNEY NEWCASTLE WOLLONGONG
DUBBO ORANGE BATHURST NOWRA BATEMANS BAY ULLADULLA GOULBURN ECHUCA SWAN HILL MILDURA SHEPPARTON WODONGA
WANGARATTA GRAFTON SOUTH GRAFTON MACLEAN YAMBA ILUKA EVANS HEAD BALLINA LENNOX HEAD BYRON BAY BANGALOW
MULLUMBIMBY BRUNSWICK HEADS OCEAN SHORES MURWILLUMBAH TWEED HEADS KINGSCLIFF LISMORE ALSTONVILLE WARDELL
WOODBURN CORAKI CASINO KYOGLE NIMBIN BONALBO ULMARRA WOOLI COPMANHURST GLEN INNES TENTERFIELD ARMIDALE
COFFS HARBOUR WOOLGOOLGA PORT MACQUARIE TAMWORTH LISMORE BALLINA""".split("\n"))
KEY=set(w.strip() for line in KEY for w in [line] if w.strip())
KEY=set()
for line in """DENILIQUIN|MOAMA|ALBURY|CULCAIRN|JERILDERIE|FINLEY|COROWA|TOCUMWAL|BAROOGA|MULWALA|HOWLONG|HOLBROOK|HENTY|URANA|BERRIGAN|MOULAMEIN|BALRANALD|WENTWORTH|BURONGA|DARETON|EUSTON|HAY|NARRANDERA|WAGGA WAGGA|GRIFFITH|LEETON|TUMBARUMBA|KHANCOBAN|JINDABYNE|BOMBALA|DELEGATE|EDEN|MERIMBULA|BEGA|COOMA|BARHAM|TOOLEYBUC|WAKOOL|CONARGO|MATHOURA|WANGANELLA|OAKLANDS|WALLA WALLA|LOCKHART|THE ROCK|TUMUT|BATLOW|QUEANBEYAN|NIMMITABEL|PAMBULA|GUNDAGAI|COOTAMUNDRA|TEMORA|YOUNG|HILLSTON|IVANHOE|MENINDEE|BROKEN HILL|POONCARIE|SYDNEY|NEWCASTLE|WOLLONGONG|DUBBO|ORANGE|BATHURST|NOWRA|BATEMANS BAY|ULLADULLA|GOULBURN|ECHUCA|SWAN HILL|MILDURA|SHEPPARTON|WODONGA|WANGARATTA|GRAFTON|SOUTH GRAFTON|MACLEAN|YAMBA|ILUKA|EVANS HEAD|BALLINA|LENNOX HEAD|BYRON BAY|BANGALOW|MULLUMBIMBY|BRUNSWICK HEADS|OCEAN SHORES|MURWILLUMBAH|TWEED HEADS|KINGSCLIFF|LISMORE|ALSTONVILLE|WARDELL|WOODBURN|CORAKI|CASINO|KYOGLE|NIMBIN|BONALBO|ULMARRA|WOOLI|COPMANHURST|GLEN INNES|TENTERFIELD|ARMIDALE|COFFS HARBOUR|WOOLGOOLGA|PORT MACQUARIE|TAMWORTH""".split("\n"):
    KEY|=set(line.split("|"))

seen=set(); out=[]
for r in csv.DictReader(open('auspost.csv',newline='',encoding='utf-8',errors='replace')):
    if r['state'] not in ('NSW','VIC','ACT'): continue
    if r.get('type')!='Delivery Area': continue
    try: lo=float(r['Long_precise']); la=float(r['Lat_precise'])
    except: continue
    nm=r['locality'].title(); k=(nm,r['state'])
    if k in seen: continue
    p=Point(lo,la); pp=P(p)
    db=pp.distance(borderP)/1000
    south = db<=200 and -38.4<la<-32.6
    north = (-30.6<la<-27.9 and lo>151.4)
    if not(south or north): continue
    if r['state']=='NSW' and not nsw.buffer(0.02).contains(p): continue
    if r['state']=='VIC' and not vic.buffer(0.02).contains(p): continue
    seen.add(k)
    if r['state']=='VIC': z=zr='vic'
    else:
        z  = 'open'  if openE.contains(pp) else ('open2' if o2E.contains(pp) else 'active')
        zr = 'open'  if openR.contains(pp) else ('open2' if o2R.contains(pp) else 'active')
    rec={"n":nm,"s":r['state'],"lon":round(lo,5),"lat":round(la,5),"z":z,"zr":zr,
         "k":1 if r['locality'].upper() in KEY else 0}
    if south:
        rec["d"]=round(db,1); rec["r"]="border"
    else:
        rec["d"]=round(pp.distance(coastP)/1000,1); rec["r"]="coast" 
    out.append(rec)
out.sort(key=lambda t:(-t['k'],t['n']))
json.dump(out,open('towns.json','w'))
from collections import Counter
print(len(out),'towns',Counter(t['z'] for t in out))
print('\nOpen Area 2 key towns:')
for t in out:
    if t['k'] and t['z']=='open2': print('  ',t['n'],'| road-variant:',t['zr'])
print('\nJust outside (active) in the north:')
for t in out:
    if t['k'] and t['z']=='active' and t['lat']>-30.4 and t['lon']>151.4: print('  ',t['n'],'| road-variant:',t['zr'])

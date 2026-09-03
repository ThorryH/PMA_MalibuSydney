import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from shapely.geometry import shape
import numpy as np

fc=json.load(open('pma.geojson'))
by={f['properties']['id']:shape(f['geometry']) for f in fc['features']}
states={f['properties']['STATE_NAME']:shape(f['geometry']) for f in json.load(open('states.geojson'))['features']}
towns=json.load(open('towns.json'))

BG='#0d1117'; INK='#e8eef5'
fig,ax=plt.subplots(figsize=(15,10.5),dpi=170)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

def poly(g,**kw):
    z=kw.get('zorder',1)
    for p in getattr(g,'geoms',[g]):
        x,y=p.exterior.xy; ax.fill(x,y,**kw)
        for i in p.interiors:
            xi,yi=i.xy; ax.fill(xi,yi,color=BG,zorder=z+0.01)
def outline(g,**kw):
    for p in getattr(g,'geoms',[g]):
        x,y=p.exterior.xy; ax.plot(x,y,**kw)
def line(g,**kw):
    for p in getattr(g,'geoms',[g]):
        x,y=p.xy; ax.plot(x,y,**kw)

for nm in ['Victoria','South Australia','Queensland']:
    poly(states[nm],color='#232c36',zorder=1)
    outline(states[nm],color='#3a4756',lw=.8,zorder=1.3)

poly(by['active_exact'],color='#1d4ed8',alpha=.62,zorder=2)
poly(by['open_exact'],color='#f59e0b',alpha=.92,zorder=3)
outline(by['active_exact'],color='#7dd3fc',lw=1.0,zorder=3.6)
line(by['border'],color='#ef4444',lw=2.2,zorder=5)
line(by['line_exact'],color='#ffffff',lw=1.3,ls=(0,(5,3)),zorder=5)

EXTRA={'Sydney':(151.209,-33.868),'Newcastle':(151.784,-32.927),'Wollongong':(150.894,-34.425),
       'Dubbo':(148.601,-32.243),'Orange':(149.100,-33.284),'Bathurst':(149.580,-33.420),
       'Goulburn':(149.717,-34.755),'Nowra':(150.600,-34.865),'Batemans Bay':(150.176,-35.708),
       'Canberra':(149.128,-35.283),'Broken Hill':(141.467,-31.958),'Port Macquarie':(152.909,-31.431),
       'Coffs Harbour':(153.114,-30.296),'Tamworth':(150.930,-31.092),'Wagga Wagga':(147.368,-35.117),
       'Griffith':(146.052,-34.289),'Bega':(149.842,-36.689),'Cooma':(149.130,-36.235)}
VICCTX={'Melbourne':(144.963,-37.814),'Echuca':(144.751,-36.133),'Shepparton':(145.400,-36.380),
        'Wangaratta':(146.320,-36.358),'Wodonga':(146.888,-36.122),'Swan Hill':(143.554,-35.338),
        'Mildura':(142.150,-34.187),'Bendigo':(144.278,-36.758)}
NSWSHOW={'Deniliquin','Balranald','Moulamein','Barham','Tocumwal','Corowa','Albury','Holbrook',
         'Culcairn','Finley','Jerilderie','Hay','Narrandera','Wentworth','Jindabyne','Bombala',
         'Eden','Moama','Khancoban','Berrigan','Tumbarumba','Buronga','Euston'}
tl={t['n']:t for t in towns if t['s']=='NSW'}
for n in NSWSHOW:
    t=tl.get(n)
    if not t: continue
    c='#fde68a' if t['z']=='open' else '#bfdbfe'
    ax.plot(t['lon'],t['lat'],'o',ms=3.4,color=c,zorder=6,mec=BG,mew=.7)
    ax.annotate(n,(t['lon'],t['lat']),textcoords='offset points',xytext=(4.5,3),fontsize=6.6,color=c,zorder=6.5)
for n,(lo,la) in EXTRA.items():
    if n in tl and n in NSWSHOW: continue
    ax.plot(lo,la,'o',ms=3.4,color='#bfdbfe',zorder=6,mec=BG,mew=.7)
    ax.annotate(n,(lo,la),textcoords='offset points',xytext=(4.5,3),fontsize=6.6,color='#bfdbfe',zorder=6.5)
for n,(lo,la) in VICCTX.items():
    ax.plot(lo,la,'o',ms=2.6,color='#8a97a6',zorder=6,mec=BG,mew=.6)
    ax.annotate(n,(lo,la),textcoords='offset points',xytext=(4,2.5),fontsize=6.0,color='#8a97a6',zorder=6.5)

# new dealership marker
ax.plot(151.209,-33.868,marker='*',ms=17,color='#facc15',mec='#0d1117',mew=1.0,zorder=8)
ax.annotate('NEW DEALERSHIP',(151.209,-33.868),textcoords='offset points',xytext=(-14,-15),
            fontsize=7.2,color='#facc15',fontweight='bold',ha='right',zorder=8)

# 50 km callout
ax.annotate('50 km', xy=(144.55,-35.35), xytext=(144.55,-34.55), fontsize=8.4, color='#ffffff',
            ha='center', zorder=8, arrowprops=dict(arrowstyle='<->',color='#ffffff',lw=1.1))

ax.set_xlim(140.6,154.2); ax.set_ylim(-38.4,-28.0)
ax.set_aspect(1/np.cos(np.radians(34))); ax.axis('off')
ax.text(.012,.978,'MALIBU BOATS — NEW SOUTH WALES PMA',transform=ax.transAxes,color=INK,
        fontsize=17,fontweight='bold',va='top')
ax.text(.012,.944,'State overview · Open Area 1 = 50 km strip north of the Victorian border · balance = NSW dealer active territory',
        transform=ax.transAxes,color='#93a3b3',fontsize=8.6,va='top')
h=[Patch(fc='#f59e0b',alpha=.92,label='Open Area 1 — 50 km north of the VIC border   53,600 km²'),
   Patch(fc='#1d4ed8',alpha=.62,label='NSW dealer active territory — rest of NSW + ACT   734,100 km²'),
   Patch(fc='#232c36',ec='#3a4756',label='Outside the PMA — VIC / SA / QLD'),
   Line2D([],[],color='#ef4444',lw=2.2,label='NSW / VIC border (River Murray → Cape Howe)'),
   Line2D([],[],color='#fff',lw=1.3,ls='--',label='50 km boundary line')]
lg=ax.legend(handles=h,loc='lower left',bbox_to_anchor=(.012,.012),frameon=True,fontsize=8.2)
lg.get_frame().set_facecolor('#151c24'); lg.get_frame().set_edgecolor('#33404e')
for t in lg.get_texts(): t.set_color(INK)
ax.text(.988,.016,'Open Area 2 — still to be defined',transform=ax.transAxes,color='#f59e0b',
        fontsize=8.2,ha='right',alpha=.9)
ax.text(.988,.905,'Concept only — boundaries indicative',transform=ax.transAxes,color='#5c6b7a',
        fontsize=7,ha='right',va='top')
plt.savefig('pma_state_overview.png',facecolor=BG,bbox_inches='tight',pad_inches=.25)
print('ok')

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
poly(by['open2_exact'],color='#10b981',alpha=.92,zorder=3)
outline(by['open2_exact'],color='#6ee7b7',lw=1.0,zorder=3.7)
line(by['open2_line_south'],color='#facc15',lw=2.0,zorder=5)
line(by['open2_line_exact'],color='#ffffff',lw=1.3,ls=(0,(5,3)),zorder=5)
outline(by['active_exact'],color='#7dd3fc',lw=1.0,zorder=3.6)
line(by['border'],color='#ef4444',lw=2.2,zorder=5)
line(by['line_exact'],color='#ffffff',lw=1.3,ls=(0,(5,3)),zorder=5)

EXTRA={'Grafton':(152.9336,-29.6876),'Sydney':(151.209,-33.868),'Newcastle':(151.784,-32.927),'Wollongong':(150.894,-34.425),
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
ax.plot(152.9336,-29.6876,marker='D',ms=6.5,color='#facc15',mec='#0d1117',mew=1.0,zorder=8)
ax.annotate('GRAFTON — Open Area 2 anchor',(152.9336,-29.6876),textcoords='offset points',
            xytext=(-11,-11),fontsize=7.0,color='#facc15',fontweight='bold',ha='right',va='center',zorder=8)
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
ax.text(.012,.944,'State overview · Open Area 1 = 50 km north of the Victorian border · Open Area 2 = Grafton to the Queensland border, 35 km inland',
        transform=ax.transAxes,color='#93a3b3',fontsize=8.6,va='top')
h=[Patch(fc='#f59e0b',alpha=.92,label='Open Area 1 — 50 km north of the VIC border   53,600 km²'),
   Patch(fc='#10b981',alpha=.92,label='Open Area 2 — Grafton to QLD, 35 km inland   6,070 km²'),
   Patch(fc='#1d4ed8',alpha=.62,label='NSW dealer active territory — the balance   728,000 km²'),
   Patch(fc='#232c36',ec='#3a4756',label='Outside the PMA — VIC / SA / QLD'),
   Line2D([],[],color='#ef4444',lw=2.2,label='NSW / VIC border (River Murray → Cape Howe)'),
   Line2D([],[],color='#fff',lw=1.3,ls='--',label='50 km boundary line')]
lg=ax.legend(handles=h,loc='lower left',bbox_to_anchor=(.012,.012),frameon=True,fontsize=8.2)
lg.get_frame().set_facecolor('#151c24'); lg.get_frame().set_edgecolor('#33404e')
for t in lg.get_texts(): t.set_color(INK)

ax.text(.988,.016,'Concept only — boundaries indicative · Open Areas 1 and 2 defined',
        transform=ax.transAxes,color='#5c6b7a',fontsize=7.4,ha='right',va='bottom')

# ---- inset: Northern Rivers / Open Area 2 ----
iax=fig.add_axes([0.105,0.375,0.275,0.365]); iax.set_facecolor('#141b23')
for sp in iax.spines.values(): sp.set_color('#3a4756'); sp.set_linewidth(1.0)
def ipoly(g,**kw):
    for p in getattr(g,'geoms',[g]):
        x,y=p.exterior.xy; iax.fill(x,y,**kw)
def iline(g,**kw):
    for p in getattr(g,'geoms',[g]):
        x,y=p.xy; iax.plot(x,y,**kw)
ipoly(states['Queensland'],color='#232c36',zorder=1)
ipoly(by['active_exact'],color='#1d4ed8',alpha=.62,zorder=2)
ipoly(by['open2_exact'],color='#10b981',alpha=.92,zorder=3)
iline(by['open2_line_exact'],color='#ffffff',lw=1.4,ls=(0,(5,3)),zorder=5)
iline(by['open2_line_snap'],color='#a3e635',lw=1.6,ls=(0,(2,3)),zorder=5.2)
iline(by['open2_line_south'],color='#facc15',lw=2.2,zorder=5.4)
INSET={'Grafton':(152.9336,-29.6876,'#facc15'),'Maclean':(153.196,-29.457,'#a7f3d0'),
       'Yamba':(153.360,-29.437,'#a7f3d0'),'Evans Head':(153.430,-29.115,'#a7f3d0'),
       'Woodburn':(153.343,-29.068,'#a7f3d0'),'Coraki':(153.290,-28.994,'#a7f3d0'),
       'Ballina':(153.565,-28.866,'#a7f3d0'),'Lismore':(153.276,-28.813,'#a7f3d0'),
       'Alstonville':(153.443,-28.844,'#a7f3d0'),'Byron Bay':(153.616,-28.643,'#a7f3d0'),
       'Mullumbimby':(153.500,-28.553,'#a7f3d0'),'Nimbin':(153.223,-28.596,'#a7f3d0'),
       'Murwillumbah':(153.394,-28.328,'#a7f3d0'),'Tweed Heads':(153.545,-28.176,'#a7f3d0'),
       'Kingscliff':(153.577,-28.253,'#a7f3d0'),
       'Casino':(153.048,-28.861,'#bfdbfe'),'Kyogle':(152.985,-28.618,'#bfdbfe'),
       'Bonalbo':(152.628,-28.740,'#bfdbfe'),'Copmanhurst':(152.792,-29.605,'#bfdbfe'),
       'Wooli':(153.262,-29.874,'#bfdbfe'),'Coffs Harbour':(153.114,-30.296,'#bfdbfe')}
for n,(lo,la,c) in INSET.items():
    iax.plot(lo,la,'D' if n=='Grafton' else 'o',ms=5.5 if n=='Grafton' else 3.0,color=c,
             zorder=6,mec='#0d1117',mew=.7)
    iax.annotate(n,(lo,la),textcoords='offset points',xytext=(4.5,3),fontsize=6.8,color=c,zorder=6.5)
iax.set_xlim(152.45,153.80); iax.set_ylim(-30.05,-27.86)
iax.set_aspect(1/np.cos(np.radians(29))); iax.set_xticks([]); iax.set_yticks([])
iax.text(.03,.975,'OPEN AREA 2 — NORTHERN RIVERS',transform=iax.transAxes,color='#6ee7b7',
         fontsize=8.4,fontweight='bold',va='top')
iax.text(.03,.932,'Grafton → QLD border · 35 km inland · 6,070 km²',transform=iax.transAxes,
         color='#93a3b3',fontsize=6.8,va='top')
iax.text(.03,.038,'— — 35 km line     · · · road-snapped     — Grafton line',transform=iax.transAxes,
         color='#93a3b3',fontsize=6.2,va='bottom')

plt.savefig('pma_state_overview.png',facecolor=BG,bbox_inches='tight',pad_inches=.25)
print('ok')

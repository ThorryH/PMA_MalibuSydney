from playwright.sync_api import sync_playwright
errs=[];reqs=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1500,'height':940})
    pg.on('pageerror',lambda e: errs.append(str(e)[:200]))
    pg.on('console',lambda m: errs.append('CONSOLE '+m.text[:160]) if m.type=='error' else None)
    pg.on('request',lambda r: reqs.append(r.url))
    pg.goto('file:///home/claude/Malibu_NSW_PMA_interactive_map.html'); pg.wait_for_timeout(12000)
    info=pg.evaluate("({loaded: !!(window.map && map.isStyleLoaded && map.isStyleLoaded()), layers: (window.map&&map.getStyle&&map.getStyle().layers)?map.getStyle().layers.filter(l=>l.id.startsWith('pma_')||l.id.startsWith('ln_')||l.id.startsWith('towns')).map(l=>l.id):[]})")
    print('style loaded:',info['loaded']); print('custom layers:',info['layers'])
    pg.screenshot(path='/home/claude/vec_state.png')
    pg.click('#mode button[data-m="detail"]'); pg.wait_for_timeout(2500)
    pg.evaluate("void map.jumpTo({center:[146.9,-36.0],zoom:9})"); pg.wait_for_timeout(2500)
    pg.evaluate("void map.fire('click',{lngLat:new maplibregl.LngLat(146.92,-36.02),point:{x:1,y:1}})"); pg.wait_for_timeout(600)
    pg.screenshot(path='/home/claude/vec_detail.png')
    hosts=set()
    for u in reqs:
        if u.startswith('http'): hosts.add(u.split('/')[2])
    print('external hosts:',sorted(hosts))
    print('errors:',errs[:6]); b.close()

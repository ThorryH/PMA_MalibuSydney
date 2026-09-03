from playwright.sync_api import sync_playwright
urls=[];errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']); pg=b.new_page(viewport={'width':1500,'height':940})
    pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('request',lambda r: urls.append(r.url) if ('cartocdn' in r.url or 'arcgisonline' in r.url) else None)
    pg.goto('file:///home/claude/Malibu_NSW_PMA_interactive_map.html'); pg.wait_for_timeout(2500)
    pg.screenshot(path='/home/claude/v_state.png')
    pg.click('#mode button[data-m="detail"]'); pg.wait_for_timeout(1200)
    pg.evaluate("void map.setView([-29.69,152.94],10)"); pg.wait_for_timeout(1500)
    pg.evaluate("void map.fire('click',{latlng:L.latLng(-29.705,152.926)})"); pg.wait_for_timeout(500)
    pg.screenshot(path='/home/claude/v_graf.png')
    print('carto reqs:',sum(1 for u in urls if 'cartocdn' in u),' esri reqs:',sum(1 for u in urls if 'arcgisonline' in u))
    print('ERRORS:',errs[:5]); b.close()

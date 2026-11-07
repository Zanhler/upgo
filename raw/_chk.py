# confere reels (toca, avança, loop) e os prints finais
import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}); e = []
    pg.on("pageerror", lambda x: e.append(str(x)))
    pg.goto("http://localhost:4200/"); time.sleep(4)
    pg.evaluate("document.getElementById('reels').scrollIntoView({behavior:'instant'})"); time.sleep(2)
    st = lambda: pg.evaluate("(()=>{const r=[...document.querySelectorAll('.rl')];const i=r.findIndex(x=>x.classList.contains('on'));const v=r[i].querySelector('video');return [i,+v.currentTime.toFixed(1),v.paused,v.readyState]})()")
    print("reel", st()); pg.screenshot(path="raw/_reels_d.png")
    for _ in range(5):
        pg.click('[data-rl="1"]'); time.sleep(1.0); print("next", st())
    time.sleep(1); print("depois do salto", st())
    for _ in range(9):
        pg.click('[data-rl="-1"]'); time.sleep(.2)
    time.sleep(1.2); print("volta", st())
    pg.evaluate("document.getElementById('contato').scrollIntoView({behavior:'instant'})"); time.sleep(4); pg.screenshot(path="raw/_contato_d.png")
    pg.evaluate("document.getElementById('desafios').scrollIntoView({behavior:'instant'})"); pg.mouse.move(5, 5); time.sleep(1); pg.screenshot(path="raw/_desafios_d.png")
    pg.evaluate("window.scrollTo({top:0,behavior:'instant'})"); time.sleep(1); pg.screenshot(path="raw/_capa_d.png")
    print("erros", e); pg.close()
    pg = b.new_page(viewport={"width": 390, "height": 844}); e = []
    pg.on("pageerror", lambda x: e.append(str(x)))
    pg.goto("http://localhost:4200/"); time.sleep(4)
    h = pg.evaluate("document.body.scrollHeight")
    for y in range(0, h, 350):
        pg.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})"); time.sleep(.1)
    for s in ["essencia", "reels", "larissa", "agendar", "avaliacoes", "contato"]:
        pg.evaluate(f"document.getElementById('{s}').scrollIntoView({{behavior:'instant'}})"); time.sleep(1); pg.screenshot(path=f"raw/_{s}_m.png")
    print("m", h, pg.evaluate("document.documentElement.scrollWidth"), e); b.close()

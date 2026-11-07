# confere a bolinha (y muda sem parar, degrau avança) e o carrossel (anda, hover para e toca, sair retoma)
import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}); e = []
    pg.on("pageerror", lambda x: e.append(str(x)))
    pg.goto("http://localhost:4200/"); time.sleep(4)
    pg.evaluate("document.getElementById('desafios').scrollIntoView({behavior:'instant'})"); pg.mouse.move(700, 400)
    seq = []
    for _ in range(16):
        d = pg.evaluate("(()=>{const m=new DOMMatrix(getComputedStyle(document.querySelector('[data-pto]')).transform);return [[...document.querySelectorAll('.dg')].findIndex(x=>x.classList.contains('on')),Math.round(m.m41),Math.round(m.m42)]})()")
        seq.append(d); time.sleep(.2)
    print("bolinha", seq)
    time.sleep(.5); pg.screenshot(path="raw/_desafios_d.png")
    d = [pg.evaluate("(()=>[...document.querySelectorAll('.dg')].findIndex(x=>x.classList.contains('on')))()")]
    for _ in range(7):
        time.sleep(2.6); d.append(pg.evaluate("(()=>[...document.querySelectorAll('.dg')].findIndex(x=>x.classList.contains('on')))()"))
    print("degraus", d)
    pg.evaluate("document.getElementById('reels').scrollIntoView({behavior:'instant'})"); pg.mouse.move(5, 5); time.sleep(1)
    tx = lambda: pg.evaluate("Math.round(new DOMMatrix(getComputedStyle(document.querySelector('.rl-trilho')).transform).m41)")
    a = tx(); time.sleep(1); c = tx(); print("anda sozinho", a, c, "ativos:", pg.evaluate("document.querySelectorAll('.rl.on').length"))
    pg.screenshot(path="raw/_reels_d.png")
    pg.mouse.move(720, 450); time.sleep(1.5)
    st = pg.evaluate("(()=>{const r=document.querySelector('.rl.on');if(!r)return null;const v=r.querySelector('video');return [+v.currentTime.toFixed(1),v.paused]})()")
    a = tx(); time.sleep(.8); c = tx(); print("hover", st, "parado", a, c); pg.screenshot(path="raw/_reels_h.png")
    pg.mouse.move(5, 5); time.sleep(.6); a = tx(); time.sleep(.8); c = tx(); print("saiu", a, c, "ativos:", pg.evaluate("document.querySelectorAll('.rl.on').length"))
    print("erros", e, pg.evaluate("document.getElementById('reels').offsetHeight")); pg.close()
    pg = b.new_page(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True); e = []
    pg.on("pageerror", lambda x: e.append(str(x)))
    pg.goto("http://localhost:4200/"); time.sleep(4)
    pg.evaluate("document.getElementById('reels').scrollIntoView({behavior:'instant'})"); time.sleep(1)
    pg.touchscreen.tap(195, 500); time.sleep(1); print("toque", pg.evaluate("document.querySelectorAll('.rl.on').length")); pg.screenshot(path="raw/_reels_m.png")
    print("m", pg.evaluate("document.documentElement.scrollWidth"), e); b.close()

# giro: dispara mouseenter durante a rotação e amostra o ângulo; quadros da linha 2 durante a entrada
import time
from playwright.sync_api import sync_playwright
ANG = "(()=>{const m=new DOMMatrix(getComputedStyle(document.querySelector('[data-vira]')).transform);return Math.round(Math.atan2(m.m12,m.m11)*180/Math.PI)})()"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}); e = []
    pg.on("pageerror", lambda x: e.append(str(x)))
    pg.goto("http://localhost:4200/"); time.sleep(5.5)
    pg.evaluate("document.querySelector('[data-vira]').dispatchEvent(new MouseEvent('mouseenter'))")
    v = []
    for i in range(10):
        v.append(pg.evaluate(ANG))
        pg.evaluate("document.querySelector('[data-vira]').dispatchEvent(new MouseEvent('mouseenter'))"); time.sleep(.1)
    print("ângulos com mouseenter repetido", v); pg.close()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("http://localhost:4200/"); t0 = time.time(); n = 0
    time.sleep(2.5)
    while time.time() - t0 < 5:
        pg.screenshot(path=f"raw/_q{n}.png", clip={"x": 150, "y": 160, "width": 600, "height": 200}); n += 1
    print("quadros", n, "erros", e); b.close()

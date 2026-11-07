# confere a seção nova, os degraus com as fotos novas e imagens quebradas
import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    for n, vp in [("d", {"width": 1440, "height": 900}), ("m", {"width": 390, "height": 844})]:
        pg = b.new_page(viewport=vp); e = []
        pg.on("pageerror", lambda x: e.append(str(x)))
        pg.on("response", lambda r: r.status >= 400 and "localhost" in r.url and e.append(f"{r.status} {r.url}"))
        pg.goto("http://localhost:4200/"); time.sleep(5)
        h = pg.evaluate("document.body.scrollHeight")
        for y in range(0, h, 300):
            pg.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})"); time.sleep(.12)
        pg.evaluate("document.getElementById('espaco').scrollIntoView({behavior:'instant'})"); time.sleep(1.5); pg.screenshot(path=f"raw/_espaco_{n}.png")
        g = lambda: pg.evaluate("[...document.querySelectorAll('.esp-grande img')].findIndex(x=>x.classList.contains('on'))")
        a = g(); time.sleep(4.2); c = g()
        pg.evaluate("document.getElementById('espaco').scrollIntoView({behavior:'instant'})"); time.sleep(1.2); pg.screenshot(path=f"raw/_espaco2_{n}.png")
        pg.evaluate("document.getElementById('desafios').scrollIntoView({behavior:'instant'})"); time.sleep(.6); pg.screenshot(path=f"raw/_desafios_{n}.png")
        time.sleep(2.7); pg.screenshot(path=f"raw/_desafios2_{n}.png")
        ruins = pg.evaluate("[...document.images].filter(i=>i.complete&&i.src&&!i.naturalWidth).map(i=>i.src)")
        print(n, "altura", h, "scrollW", pg.evaluate("document.documentElement.scrollWidth"), "seção", pg.evaluate("document.getElementById('espaco').offsetHeight"), "troca", a, c, "quebradas", ruins, "erros", e)
        pg.close()
    b.close()

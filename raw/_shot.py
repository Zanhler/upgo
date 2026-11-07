# prints (desktop/celular), erros de console e teste do agendar
import time
from playwright.sync_api import sync_playwright
R = "raw/"
with sync_playwright() as p:
    b = p.chromium.launch()
    for nome, vp in [("d", {"width": 1440, "height": 900}), ("m", {"width": 390, "height": 844})]:
        pg = b.new_page(viewport=vp); erros = []
        pg.on("pageerror", lambda e: erros.append(str(e))); pg.on("console", lambda m: m.type == "error" and erros.append(m.text))
        pg.goto("http://localhost:4200/", wait_until="domcontentloaded")
        time.sleep(1.5); pg.screenshot(path=f"{R}_abre_{nome}.png"); time.sleep(3.2); pg.screenshot(path=f"{R}_capa_{nome}.png")
        h = pg.evaluate("document.body.scrollHeight")
        for y in range(0, h, 350): pg.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})"); time.sleep(.1)
        for k, v in [("motivo", "ganhar força"), ("exp", "nunca fiz Pilates"), ("dia", "sábado")]:
            pg.click(f'[data-g="{k}"] button[data-v="{v}"]')
        print(nome, "altura", h, "scrollW", pg.evaluate("document.documentElement.scrollWidth"), "|", pg.inner_text("[data-bolha]"), "| tarde desabilitada:", pg.is_disabled('[data-g="per"] button[data-v="à tarde"]'))
        print(" alturas", {s: pg.evaluate(f"document.getElementById('{s}').offsetHeight") for s in ["inicio","desafios","essencia","reels","larissa","agendar","avaliacoes","contato"]})
        for s in ["desafios", "essencia", "reels", "larissa", "agendar", "avaliacoes", "contato"]:
            pg.evaluate(f"document.getElementById('{s}').scrollIntoView({{behavior:'instant'}})"); time.sleep(1.3); pg.screenshot(path=f"{R}_{s}_{nome}.png")
        print(nome, "erros", erros); pg.close()
    b.close()

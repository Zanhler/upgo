# degraus parados até a seção aparecer, 6º -> 1º; agendar com múltipla escolha e altura
import time
from playwright.sync_api import sync_playwright
ativo = "[...document.querySelectorAll('.dg')].findIndex(x=>x.classList.contains('on'))"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}); e = []
    pg.on("pageerror", lambda x: e.append(str(x)))
    pg.goto("http://localhost:4200/"); time.sleep(4)
    print("antes de chegar", pg.evaluate(ativo)); time.sleep(3); print("ainda", pg.evaluate(ativo))
    pg.evaluate("document.getElementById('desafios').scrollIntoView({behavior:'instant'})"); pg.mouse.move(5, 5)
    seq = [pg.evaluate(ativo)]
    for _ in range(7):
        time.sleep(2.6); seq.append(pg.evaluate(ativo))
    print("subindo", seq)
    pg.evaluate("document.getElementById('agendar').scrollIntoView({behavior:'instant'})"); time.sleep(1)
    print("ao sair", pg.evaluate(ativo), "altura agendar", pg.evaluate("document.getElementById('agendar').offsetHeight"))
    for k, v in [("motivo", "ganhar força"), ("motivo", "aliviar uma dor"), ("exp", "já fiz Pilates"), ("dia", "terça"), ("dia", "quinta"), ("dia", "sábado"), ("per", "à noite")]:
        pg.click(f'[data-g="{k}"] button[data-v="{v}"]')
    print(pg.inner_text("[data-bolha]"), "| noite ok:", not pg.is_disabled('[data-g="per"] button[data-v="à noite"]'))
    pg.click('[data-g="dia"] button[data-v="terça"]'); pg.click('[data-g="dia"] button[data-v="quinta"]')
    print(pg.inner_text("[data-bolha]"), "| só sáb, noite off:", pg.is_disabled('[data-g="per"] button[data-v="à noite"]'))
    time.sleep(.5); pg.screenshot(path="raw/_agendar_d.png"); print("erros", e); pg.close()
    pg = b.new_page(viewport={"width": 390, "height": 844}); e = []
    pg.on("pageerror", lambda x: e.append(str(x)))
    pg.goto("http://localhost:4200/"); time.sleep(4)
    pg.evaluate("document.getElementById('agendar').scrollIntoView({behavior:'instant'})"); time.sleep(1); pg.screenshot(path="raw/_agendar_m.png")
    print("m", pg.evaluate("document.getElementById('agendar').offsetHeight"), pg.evaluate("document.documentElement.scrollWidth"), e); b.close()

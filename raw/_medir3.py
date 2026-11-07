# registra, desde o início, o ângulo da linha 2, a saída do painel e a suavidade do giro
import time
from playwright.sync_api import sync_playwright
INI = """
window.__a=[];
(function f(){const el=document.querySelector('[data-vira]');if(el){const m=new DOMMatrix(getComputedStyle(el).transform);const p=document.querySelector('[data-abertura]');window.__a.push([Math.round(performance.now()),Math.round(Math.atan2(m.m12,m.m11)*180/Math.PI),p?1:0])}requestAnimationFrame(f)})();
"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}); pg.add_init_script(INI)
    pg.goto("http://localhost:4200/"); time.sleep(6)
    a = pg.evaluate("window.__a")
    gira = [x for x in a if x[1] != 0]
    saiu = next((x[0] for x in a if x[2] == 0), None)
    print("painel saiu em", saiu, "ms | giro de", gira[0][0] if gira else None, "a", gira[-1][0] if gira else None, "ms | quadros no giro", len(gira))
    if gira:
        d = [gira[i + 1][0] - gira[i][0] for i in range(len(gira) - 1)]
        print("maior intervalo no giro", max(d), "ms | sequência", [x[1] for x in gira][::6])
    b.close()

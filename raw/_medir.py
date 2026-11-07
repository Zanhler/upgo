# mede a entrada do título: quadros longos, tarefas longas e quantas vezes o giro reinicia com o mouse parado em cima
import time
from playwright.sync_api import sync_playwright
INI = """
window.__q=[];window.__lt=[];
new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push([Math.round(e.startTime),Math.round(e.duration)]))).observe({type:'longtask',buffered:true});
let u=performance.now();(function f(t){window.__q.push([Math.round(t),Math.round(t-u)]);u=t;requestAnimationFrame(f)})(u);
"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}); pg.add_init_script(INI); e = []
    pg.on("pageerror", lambda x: e.append(str(x)))
    pg.goto("http://localhost:4200/")
    pg.mouse.move(400, 300)
    time.sleep(3.4)
    # varre o mouse sobre "Não por aqui!" enquanto o título entra e gira
    giros = pg.evaluate("window.__g=0;new MutationObserver(()=>{const m=new DOMMatrix(getComputedStyle(document.querySelector('[data-vira]')).transform);const a=Math.atan2(m.m12,m.m11);if(window.__a!==undefined&&window.__a>1&&a<.2&&a>=0)window.__g++;window.__a=a}).observe(document.querySelector('[data-vira]'),{attributes:true,attributeFilter:['style']});0")
    for i in range(30):
        pg.mouse.move(250 + (i % 10) * 25, 295 + (i % 3) * 8); time.sleep(.06)
    time.sleep(1.5)
    r = pg.evaluate("({q:window.__q,lt:window.__lt,g:window.__g})")
    janela = [x for x in r["q"] if 2500 < x[0] < 6000]
    print("quadros", len(janela), "maiores", sorted(x[1] for x in janela)[-6:], ">50ms:", sum(1 for x in janela if x[1] > 50))
    print("tarefas longas", r["lt"]); print("reinícios do giro", r["g"]); print("erros", e)
    b.close()

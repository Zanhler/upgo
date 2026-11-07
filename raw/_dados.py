# horário da semana, avaliações completas, whatsapp da bio, perfil da fundadora, legendas inteiras
import json, os, re, time, urllib.request
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
out = open(R + "/_dados.txt", "w", encoding="utf-8")
def P(*a): print(*a, file=out)
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(locale="pt-BR", viewport={"width": 1400, "height": 1000}, user_agent=UA)
    pg = c.new_page()
    pg.goto("https://www.google.com/maps/search/UP+GO+PILATES+CALISTENIA+Rio+Claro?hl=pt-BR", wait_until="domcontentloaded"); time.sleep(7)
    try: pg.click('button:has-text("Dispensar")', timeout=2000)
    except Exception: pass
    P("HORAS", pg.eval_on_selector_all('[aria-label*="feira" i],[aria-label*="sábado" i],[aria-label*="domingo" i]', "a=>[...new Set(a.map(x=>x.getAttribute('aria-label')))]"))
    pg.click('button[role="tab"]:has-text("Avaliações")', timeout=5000); time.sleep(3)
    for _ in range(14):
        pg.evaluate("""()=>{const r=document.querySelector('[data-review-id]'); let e=r; while(e&&e.scrollHeight<=e.clientHeight+5) e=e.parentElement; if(e) e.scrollTop=e.scrollHeight;}"""); time.sleep(1)
    for bt in pg.query_selector_all('button[aria-label*="Ver mais"],button:has-text("Mais")'):
        try: bt.click(timeout=300)
        except Exception: pass
    time.sleep(1)
    revs = pg.evaluate("""()=>[...document.querySelectorAll('div[data-review-id][aria-label]')].map(d=>[d.getAttribute('aria-label'),(d.querySelector('.wiI7pd')||{}).innerText||'',(d.querySelector('.rsqaWe')||{}).innerText||''])""")
    P("REVS", len(revs))
    for r in revs: P(r)
    pg.close()
    pg = c.new_page()
    pg.goto("https://wa.me/message/XDX7RQMJZUSEC1", wait_until="domcontentloaded"); time.sleep(5)
    P("WA", pg.url); P(pg.inner_text("body")[:300])
    pg.close()
    pg = c.new_page()
    pg.goto("https://www.instagram.com/laris_bueno_/", wait_until="domcontentloaded"); time.sleep(6)
    P("LARIS", pg.title()); 
    try: pg.click('svg[aria-label="Fechar"]', timeout=1500)
    except Exception: pass
    P(pg.inner_text("main")[:500] if pg.query_selector("main") else "")
    imgs = pg.eval_on_selector_all("img", "a=>a.map(i=>[i.src,i.naturalWidth,i.alt.slice(0,120)])")
    for i, (s, w, a) in enumerate(imgs[:1]): open(R + "/ig/laris.jpg", "wb").write(urllib.request.urlopen(urllib.request.Request(s, headers={"User-Agent": UA})).read())
    pg.screenshot(path=R + "/ig/_laris.png"); pg.close()
    for code in ["DfVBRclodb9", "DejxSDUxdzR"]:
        pg = c.new_page(); pg.goto("https://www.instagram.com/upgo.pilatesefuncional/p/" + code + "/", wait_until="domcontentloaded"); time.sleep(5)
        P("CAP", code, pg.eval_on_selector_all('meta[property="og:description"],meta[name="description"]', "a=>a.map(m=>m.content)")); P(pg.eval_on_selector_all("h1", "a=>a.map(x=>x.innerText)")); pg.close()
    b.close()
out.close()

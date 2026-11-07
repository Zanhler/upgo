# Maps: nota, horários, avaliações e fotos
import os, re, time, json, urllib.request
from playwright.sync_api import sync_playwright
OUT = os.path.dirname(os.path.abspath(__file__)) + "/maps"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(locale="pt-BR", viewport={"width": 1400, "height": 1000}, user_agent=UA).new_page()
    pg.goto("https://www.google.com/maps/search/UP+GO+PILATES+CALISTENIA+Rio+Claro?hl=pt-BR", wait_until="domcontentloaded"); time.sleep(7)
    try: pg.click('button:has-text("Dispensar")', timeout=2000)
    except Exception: pass
    time.sleep(1)
    print(pg.title()); print(pg.inner_text("body")[:1500])
    for h in pg.eval_on_selector_all('[aria-label*="horário" i],[aria-label*="segunda" i]', "a=>a.map(x=>x.getAttribute('aria-label'))")[:5]: print("H:", h)
    pg.screenshot(path=OUT + "/_m.png")
    try:
        pg.click('button:has-text("Avaliações")', timeout=4000); time.sleep(3)
        for _ in range(3):
            try: pg.mouse.move(300, 600); pg.mouse.wheel(0, 1500)
            except Exception: pass
            time.sleep(1.2)
        for bt in pg.query_selector_all('button:has-text("Mais")')[:10]:
            try: bt.click(timeout=500)
            except Exception: pass
        print("REV:", pg.eval_on_selector_all('[data-review-id]', "a=>[...new Set(a.map(x=>x.innerText.slice(0,350)))]")[:12])
    except Exception as e: print("sem aval", e)
    try:
        pg.click('button:has-text("Visão geral")', timeout=2000); time.sleep(1)
        pg.click('button:has-text("Ver fotos")', timeout=4000); time.sleep(5)
    except Exception as e: print("foto", e)
    srcs = set(re.findall(r'https://lh3\.googleusercontent\.com/[^"\')\s&]+', pg.content()))
    n = 0
    for s in srcs:
        u = re.sub(r"=[^=]*$", "", s) + "=s1600-k-no"
        try:
            d = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=20).read()
            if len(d) > 25000: open(f"{OUT}/f_{n:02d}.jpg", "wb").write(d); n += 1
        except Exception: pass
    print("fotos", n)
    b.close()

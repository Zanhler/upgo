# abre o perfil sem login: bio, links e posts visíveis
import json, os, re, time, urllib.request
from playwright.sync_api import sync_playwright
OUT = os.path.dirname(os.path.abspath(__file__)) + "/ig"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
def get(u, n):
    open(OUT + "/" + n, "wb").write(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30).read())
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(locale="pt-BR", viewport={"width": 1300, "height": 1000}, user_agent=UA).new_page()
    pg.goto("https://www.instagram.com/upgo.pilatesefuncional/", wait_until="domcontentloaded"); time.sleep(8)
    print(pg.title())
    try: pg.click('svg[aria-label="Fechar"]', timeout=2000)
    except Exception: pass
    for t in ["mais", "more"]:
        try: pg.click(f'span:has-text("{t}")', timeout=1000)
        except Exception: pass
    time.sleep(1)
    print(pg.inner_text("main")[:900] if pg.query_selector("main") else pg.inner_text("body")[:900])
    pg.screenshot(path=OUT + "/_top.png")
    for _ in range(4): pg.mouse.wheel(0, 900); time.sleep(1.5)
    imgs = pg.eval_on_selector_all("img", "a=>a.map(i=>[i.src,i.naturalWidth,i.alt.slice(0,300)])")
    links = pg.eval_on_selector_all("a", "a=>a.map(x=>x.href)")
    print([l for l in links if "/p/" in l or "/reel/" in l or "l.instagram" in l or "linktr" in l or "wa.me" in l][:40])
    n = 0
    for src, w, alt in imgs:
        if w >= 300:
            try: get(src, f"p{n:02d}.jpg"); print(f"p{n:02d}", w, alt[:170]); n += 1
            except Exception as e: print("x", e)
    if imgs: get(imgs[0][0], "avatar.jpg"); print("avatar", imgs[0][1])
    json.dump({"imgs": imgs, "links": links}, open(OUT + "/_page.json", "w", encoding="utf-8"), ensure_ascii=False)
    b.close()

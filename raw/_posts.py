# posts em alta (só imagens do carrossel >= 700px), legenda e url de vídeo dos reels
import json, os, re, time, urllib.request
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
B = "https://www.instagram.com/upgo.pilatesefuncional/"
POSTS = ["DfVBRclodb9","DfCJrakkSTi","De1pm49RUIG","Dez7OriuxNl","Dec8eZixXeV","Detmvz6RG9b".replace("Detmvz","DetmvZ"),"DejxSDUxdzR","Deg0p6Rxlrq","DePJPkbx491","DeSHXghOZnc","DeM5NpYx3S9","DeeMiU3RQDP"]
REELS = ["DfZ1rtKuXjj","DfF2319OWDh","De_492HRib_","Dej_1z9xC5z","DeZYz_0RAz5","DeNTygVOdkJ"]
def get(u, f):
    open(f, "wb").write(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=60).read())
txt = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(locale="pt-BR", viewport={"width": 1300, "height": 1000}, user_agent=UA)
    for code in POSTS:
        pg = c.new_page()
        pg.goto(B + "p/" + code + "/", wait_until="domcontentloaded"); time.sleep(5)
        seen, n = set(), 0
        for pas in range(8):
            for src, w in pg.eval_on_selector_all("img", "a=>a.map(i=>[i.src,i.naturalWidth])"):
                base = src.split("?")[0]
                if w >= 700 and base not in seen:
                    seen.add(base); get(src, f"{R}/hi/{code}_{n}.jpg"); n += 1
            nx = pg.query_selector('button[aria-label="Avançar"],button[aria-label="Next"]')
            if not nx: break
            try: nx.click(timeout=1500); time.sleep(1)
            except Exception: break
        cap = pg.eval_on_selector_all('meta[property="og:description"],meta[name="description"]', "a=>a.map(m=>m.content)")
        h1 = pg.eval_on_selector_all("h1", "a=>a.map(x=>x.innerText)")
        txt[code] = (h1 or cap or [""])[0][:700]; print(code, n, txt[code][:220].replace("\n", " ")); pg.close()
    for code in REELS:
        pg = c.new_page(); vids = []
        pg.on("response", lambda r: vids.append(r.url) if ".mp4" in r.url else None)
        pg.goto(B + "reel/" + code + "/", wait_until="domcontentloaded"); time.sleep(7)
        html = pg.content()
        m = re.findall(r'"video_url":"([^"]+)"', html) or re.findall(r'video_versions[^\]]*?"url":"([^"]+)"', html)
        vsrc = pg.eval_on_selector_all("video", "a=>a.map(v=>v.src)")
        u = m[0].encode().decode("unicode_escape").replace("\/", "/") if m else None
        if not u:
            lim = [re.sub(r"&?bytestart=\d+|&?byteend=\d+", "", x) for x in vids]
            u = lim[0] if lim else None
        print(code, "json" if m else "net", len(vids), vsrc[:1], (u or "")[:90])
        if u:
            try: get(u, f"{R}/video/{code}.mp4"); print(" ok", os.path.getsize(f"{R}/video/{code}.mp4"))
            except Exception as e: print(" x", e)
        pg.close()
    b.close()
json.dump(txt, open(f"{R}/ig/_legendas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

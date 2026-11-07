# rodada 5: fotos novas do espaço (HEIC do dev) nos degraus + seção "O cuidado começa antes da aula"
import os, shutil
from PIL import Image
os.makedirs("raw/_v4", exist_ok=True)
for a in ["index.html", "css/style.css", "js/script.js"]:
    shutil.copy(a, "raw/_v4/" + os.path.basename(a))
def rep(s, a, b):
    assert a in s, a[:60]; return s.replace(a, b)

mapa = {"IMG_0283": "espaco-salao", "IMG_0280": "espaco-mandala", "IMG_0281": "espaco-logo", "IMG_0279": "espaco-aparelhos",
        "IMG_0277": "det-aroma", "IMG_0278": "det-som", "IMG_0282": "det-temperatura", "IMG_0284": "det-luz"}
for o, n in mapa.items():
    im = Image.open(f"raw/novas/{o}.jpg"); im.thumbnail((1400, 1400)); im.save(f"img/{n}.webp", quality=82)

f = "js/script.js"; s = open(f, encoding="utf-8").read()
s = rep(s, '{ n: "Primeiro passo", img: "estudio",', '{ n: "Primeiro passo", img: "espaco-salao",')
s = rep(s, 'alt: "Estúdio com reformers e aparelhos"', 'alt: "Salão do estúdio com barrel, cadillac e o logo UP.GO na parede"')
s = rep(s, '{ n: "Aula em grupo", img: "mandala",', '{ n: "Aula em grupo", img: "espaco-mandala",')
s = rep(s, 'alt: "Turma no tapete, em frente à parede de mandala azul"', 'alt: "Sala com tapetes azuis e a parede de mandala"')
s = rep(s, '/* ---------- avaliações: uma por vez ---------- */', '''/* ---------- o espaço: a foto grande troca sozinha ---------- */
const espImgs = $$(".esp-grande img");
let ei = 0;
setInterval(() => { ei = (ei + 1) % espImgs.length; espImgs.forEach((im, j) => im.classList.toggle("on", j === ei)); }, 4000);

/* ---------- avaliações: uma por vez ---------- */''')
s = rep(s, 'gsap.from(".chat", {', 'gsap.from(".esp-t", { y: 24, opacity: 0, duration: .7, stagger: .08, ease: "power3.out", scrollTrigger: { trigger: ".esp", start: "top 80%", once: true } });\ngsap.from(".chat", {')
open(f, "w", encoding="utf-8").write(s)

f = "index.html"; s = open(f, encoding="utf-8").read()
s = rep(s, '<!-- AGENDAR -->', '''<!-- O ESPAÇO -->
<section class="sec" id="espaco">
  <div class="wrap">
    <h2 data-e>O cuidado começa antes da aula.</h2>
    <p class="sub esp-sub" data-e>Antes de você chegar, já existe planejamento. E o espaço também é preparado para receber você.</p>
    <div class="esp">
      <div class="esp-grande">
        <img class="on" src="img/espaco-logo.webp" alt="Salão com aparelhos, tecido azul suspenso e o logo UP.GO na parede" loading="lazy">
        <img src="img/espaco-aparelhos.webp" alt="Ladder barrel, espaldar e cadillac no salão do estúdio" loading="lazy">
      </div>
      <div class="esp-tiles">
        <figure class="esp-t"><img src="img/det-aroma.webp" alt="Mão segurando o aromatizador de chá branco" loading="lazy"><figcaption><b>Aroma</b><span>Chá branco no ambiente e nos tecidos.</span></figcaption></figure>
        <figure class="esp-t"><img src="img/det-som.webp" alt="Caixa de som azul tocando a playlist Alongamento" loading="lazy"><figcaption><b>Som</b><span>Música no ritmo da aula.</span></figcaption></figure>
        <figure class="esp-t"><img src="img/det-temperatura.webp" alt="Mão segurando o controle do ar-condicionado" loading="lazy"><figcaption><b>Temperatura</b><span>Ambiente climatizado.</span></figcaption></figure>
        <figure class="esp-t"><img src="img/det-luz.webp" alt="Abajur azul aceso ao lado da parede de mandala" loading="lazy"><figcaption><b>Luz</b><span>Luz suave na sala da mandala.</span></figcaption></figure>
      </div>
    </div>
  </div>
</section>

<!-- AGENDAR -->''')
s = rep(s, '<a href="#larissa">Larissa</a>', '<a href="#larissa">Larissa</a>\n    <a href="#espaco">O espaço</a>')
s = s.replace('css/style.css?v=1', 'css/style.css?v=5').replace('js/script.js?v=1', 'js/script.js?v=5')
open(f, "w", encoding="utf-8").write(s)

f = "css/style.css"; s = open(f, encoding="utf-8").read()
s = rep(s, '/* agendar */', '''/* o espaço */
.esp-sub{margin-bottom:24px}
.esp{display:grid;grid-template-columns:1.1fr 1fr;gap:12px;height:440px}
.esp-grande{position:relative;border-radius:var(--r);overflow:hidden;background:var(--gelo)}
.esp-grande img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.04);transition:opacity .9s,transform 4.5s linear}
.esp-grande img.on{opacity:1;transform:none}
.esp-tiles{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:12px;min-height:0}
.esp-t{position:relative;border-radius:var(--r);overflow:hidden;min-height:0}
.esp-t img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .9s var(--mola)}
.esp-t:hover img{transform:scale(1.06)}
.esp-t figcaption{position:absolute;inset:auto 0 0;padding:30px 12px 10px;color:#fff;background:linear-gradient(transparent,rgba(11,40,85,.85));display:grid;line-height:1.3}
.esp-t b{font-size:.92rem;font-weight:600}
.esp-t span{font-size:.76rem}

/* agendar */''')
s = rep(s, "  .lar-foto{height:340px}\n", "  .lar-foto{height:340px}\n  .esp{grid-template-columns:1fr;height:auto}\n  .esp-grande{height:320px}\n  .esp-tiles{grid-template-rows:none}\n  .esp-t{aspect-ratio:1}\n")
open(f, "w", encoding="utf-8").write(s)

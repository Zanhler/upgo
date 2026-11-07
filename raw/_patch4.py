# rodada 4: botões da capa e entrada do título sem trava
import os, shutil
os.makedirs("raw/_v3", exist_ok=True)
for a in ["index.html", "css/style.css", "js/script.js"]:
    shutil.copy(a, "raw/_v3/" + os.path.basename(a))
def rep(s, a, b):
    assert a in s, a[:60]; return s.replace(a, b)

f = "index.html"; s = open(f, encoding="utf-8").read()
s = rep(s, '''<a class="bt bt-azul" href="#agendar">Agendar minha aula</a>
        <a class="bt bt-linha" href="#desafios">Qual é o seu desafio?</a>''',
'''<a class="bt bt-azul" href="https://wa.me/5519981261106?text=Ol%C3%A1%2C%20gostaria%20de%20agendar%20uma%20aula!" target="_blank" rel="noopener"><svg><use href="#zap"/></svg>Agendar minha aula</a>
        <a class="bt bt-linha bt-ig" href="https://www.instagram.com/upgo.pilatesefuncional/" target="_blank" rel="noopener" aria-label="Instagram da UP.GO"><svg><use href="#ig"/></svg></a>''')
s = rep(s, '  <symbol id="zap" viewBox="0 0 24 24">', '''  <symbol id="ig" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.9"><rect x="3" y="3" width="18" height="18" rx="5.2"/><circle cx="12" cy="12" r="4.2"/></g><circle cx="17.3" cy="6.7" r="1.25" fill="currentColor"/></symbol>
  <symbol id="zap" viewBox="0 0 24 24">''')
# o vídeo da capa só começa depois da abertura
s = rep(s, 'muted loop playsinline autoplay preload="metadata"', 'muted loop playsinline preload="metadata"')
open(f, "w", encoding="utf-8").write(s)

f = "css/style.css"; s = open(f, encoding="utf-8").read()
s = rep(s, ".bt-sm{height:38px;", ".bt-ig{width:46px;padding:0;color:var(--azul-forte)}\n.bt-ig svg{width:22px;height:22px}\n.bt-sm{height:38px;")
s = rep(s, "  .capa-bt .bt{flex:1 1 100%}\n", "  .capa-bt .bt{flex:1 1 0}\n  .capa-bt .bt-ig{flex:none}\n")
# o desfoque do cabeçalho repinta a cada quadro enquanto a capa se mexe
s = rep(s, "background:rgba(255,255,255,.94);backdrop-filter:blur(10px);transition:box-shadow .3s}", "background:#fff;transition:box-shadow .3s}")
s = rep(s, ".l2{display:inline-block !important;", ".l2{display:inline-block !important;will-change:transform;")
open(f, "w", encoding="utf-8").write(s)

f = "js/script.js"; s = open(f, encoding="utf-8").read()
# Goooo: calcula quantos "o" cabem uma vez por volta, em vez de medir a cada letra; só começa depois da abertura
i = s.index("let nO = 1;"); j = s.index("/* ---------- desafios")
s = s[:i] + '''let nO = 1, maxO = 0;
function medeGo() {
  go.textContent = "Go"; const a = go.offsetWidth;
  go.textContent = "Goo"; const o = go.offsetWidth - a;
  maxO = Math.max(4, Math.floor((go.parentElement.clientWidth - 40 - a) / o) + 1);
}
function esticaGo() {
  if (nO === 1) medeGo();
  go.textContent = "G" + "o".repeat(nO);
  if (nO < maxO) { nO++; setTimeout(esticaGo, 70); return; }
  go.textContent += "!";
  setTimeout(() => { nO = 1; esticaGo(); }, 2200);
}
if (calmo) go.textContent = "Goooooooo!";

''' + s[j:]
# carrossel: não mede o layout a cada quadro
s = rep(s, "const volta = () => rls[N].offsetLeft - rls[0].offsetLeft;", "let rlVolta = 0;\nconst medeVolta = () => { rlVolta = rls[N].offsetLeft - rls[0].offsetLeft; };\nmedeVolta(); addEventListener(\"resize\", medeVolta);")
s = rep(s, "const v = volta(); if (v && -rlX >= v) rlX += v;", "if (rlVolta && -rlX >= rlVolta) rlX += rlVolta;")
# vídeo da capa e faixa só depois da abertura
s = rep(s, 'new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { const p = vCapa.play(); if (p && p.catch) p.catch(() => {}); } else vCapa.pause(); })).observe(vCapa);',
 'const tocaCapa = () => { const p = vCapa.play(); if (p && p.catch) p.catch(() => {}); };\nnew IntersectionObserver(es => es.forEach(e => { if (!e.isIntersecting) vCapa.pause(); else if (!document.body.classList.contains("abrindo")) tocaCapa(); })).observe(vCapa);')
s = rep(s, 'const fim = () => { abertura.remove(); document.body.classList.remove("abrindo"); };',
 'const fim = () => { abertura.remove(); document.body.classList.remove("abrindo"); tocaCapa(); if (!calmo) esticaGo(); };')
# cambalhota: nunca reinicia no meio, sem recuo no começo, e só depois que o painel saiu
s = rep(s, 'const viraL2 = () => gsap.fromTo(l2, { rotation: 0 }, { rotation: 360, duration: 1.05, ease: "back.inOut(1.3)" });',
 'const viraL2 = () => { if (!gsap.isTweening(l2)) gsap.fromTo(l2, { rotation: 0 }, { rotation: 360, duration: .9, ease: "power2.inOut", force3D: true }); };')
s = rep(s, 'const ab = gsap.timeline({ onComplete: () => { fim(); }, defaults: { ease: "power2.inOut" } });',
 'const ab = gsap.timeline({ onComplete: () => { fim(); setTimeout(viraL2, 500); }, defaults: { ease: "power2.inOut" } });')
s = rep(s, '.add(() => { entra.play(); setTimeout(viraL2, 650); }, 2.55)', '.add(() => entra.play(), 2.55)')
open(f, "w", encoding="utf-8").write(s)

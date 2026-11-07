# rodada 2: bolinha pingando de degrau em degrau; reels em carrossel contínuo, selecionado só no hover
import os, shutil
os.makedirs("raw/_v1", exist_ok=True)
for a in ["index.html", "css/style.css", "js/script.js"]:
    shutil.copy(a, "raw/_v1/" + os.path.basename(a))
def rep(s, a, b):
    assert a in s, a[:60]; return s.replace(a, b)

f = "js/script.js"; s = open(f, encoding="utf-8").read()
s = rep(s, 'b.addEventListener("click", () => { paraDg(); vaiDg(i); });', 'b.addEventListener("click", () => { paraDg(); vaiDg(i); dgT = setTimeout(tocaDg, 6000); });')
i = s.index("function vaiDg(i) {"); j = s.index("/* ---------- sanfona dos pilares")
s = s[:i] + '''// a bolinha (o ponto azul do logo) não para: pinga no degrau e salta para o próximo
let pulo, pinga, sentido = 1;
function pingaNoDegrau() {
  const y = posPto(di).y;
  pinga = gsap.timeline({ repeat: -1 })
    .to(dPto, { y: y - 26, duration: .25, ease: "power2.out" })
    .to(dPto, { y, duration: .25, ease: "power2.in" })
    .to(dPto, { scaleX: 1.22, scaleY: .78, transformOrigin: "50% 100%", duration: .06, yoyo: true, repeat: 1 });
}
function vaiDg(i) {
  const prev = di; di = i;
  dgs.forEach((b, j) => { b.classList.toggle("on", j === i); b.setAttribute("aria-selected", j === i); });
  dgImgs.forEach((im, j) => im.classList.toggle("on", j === i));
  $("[data-d-tit]").textContent = DEGRAUS[i].n; $("[data-d-txt]").textContent = DEGRAUS[i].t;
  const p = posPto(i);
  if (!anima) { if (typeof gsap !== "undefined") gsap.set(dPto, { x: p.x, y: p.y }); else dPto.style.transform = `translate(${p.x}px,${p.y}px)`; return; }
  if (pinga) pinga.kill();
  if (pulo) pulo.kill();
  if (prev < 0) { gsap.set(dPto, { x: p.x, y: p.y }); pingaNoDegrau(); return; }
  const topo = Math.min(posPto(prev).y, p.y) - 36;
  gsap.set(dPto, { scaleX: 1, scaleY: 1 });
  pulo = gsap.timeline({ onComplete: pingaNoDegrau })
    .to(dPto, { x: p.x, duration: .5, ease: "none" }, 0)
    .to(dPto, { y: topo, duration: .25, ease: "power2.out" }, 0)
    .to(dPto, { y: p.y, duration: .25, ease: "power2.in" }, .25)
    .to(dPto, { scaleX: 1.28, scaleY: .72, transformOrigin: "50% 100%", duration: .07, yoyo: true, repeat: 1 }, .5)
    .fromTo($("i", dgs[i]), { y: 5 }, { y: 0, duration: .28, ease: "back.out(3)", clearProps: "y" }, .5);
}
// sobe até o último degrau e desce de volta, sempre de um em um
function proximoDg() {
  if (di + sentido < 0 || di + sentido >= DEGRAUS.length) sentido = -sentido;
  vaiDg(di + sentido);
}
const paraDg = () => { clearInterval(dgT); clearTimeout(dgT); };
const tocaDg = () => { paraDg(); dgT = setInterval(proximoDg, 2600); };
vaiDg(0); tocaDg();
addEventListener("resize", () => {
  const p = posPto(di); if (typeof gsap === "undefined") return;
  if (pinga) pinga.kill(); if (pulo) pulo.kill();
  gsap.set(dPto, { x: p.x, y: p.y }); if (anima) pingaNoDegrau();
});

''' + s[j:]
i = s.index('const trilho = $("[data-trilho]");'); j = s.index('const vCapa = $(".ca-2 video");')
s = s[:i] + '''const trilho = $("[data-trilho]");
const umaVolta = REELS.map(r => `<div class="rl"><img src="img/reel-${r}.webp" alt="" loading="lazy"><video muted loop playsinline preload="none" src="video/${r}.mp4"></video><span class="rl-barra"><i></i></span></div>`).join("");
trilho.innerHTML = umaVolta + umaVolta + umaVolta;
const rls = $$(".rl", trilho), N = REELS.length;
let rlX = 0, rlSel = null, rlVis = false, rlT0 = 0, rlRaf;
const volta = () => rls[N].offsetLeft - rls[0].offsetLeft;
function selRl(c) {
  if (rlSel === c) return;
  if (rlSel) { const v0 = $("video", rlSel); v0.pause(); v0.currentTime = 0; rlSel.classList.remove("on"); $(".rl-barra i", rlSel).style.width = "0"; }
  rlSel = c;
  trilho.classList.toggle("tem-sel", !!c);
  if (c) { c.classList.add("on"); const pr = $("video", c).play(); if (pr && pr.catch) pr.catch(() => {}); }
}
// gira sozinho o tempo todo; só para enquanto um vídeo está selecionado
(function gira(t) {
  const dt = Math.min(50, t - rlT0); rlT0 = t;
  if (rlVis && !rlSel && !calmo) {
    rlX -= dt * .045;
    const v = volta(); if (v && -rlX >= v) rlX += v;
    trilho.style.transform = `translate3d(${rlX}px,0,0)`;
  }
  if (rlSel) { const v = $("video", rlSel); if (v.duration) $(".rl-barra i", rlSel).style.width = `${v.currentTime / v.duration * 100}%`; }
  rlRaf = requestAnimationFrame(gira);
})(0);
rls.forEach(r => {
  r.addEventListener("pointerenter", e => { if (e.pointerType === "mouse") selRl(r); });
  r.addEventListener("click", e => { if (matchMedia("(hover: none)").matches) { e.stopPropagation(); selRl(rlSel === r ? null : r); } });
});
trilho.addEventListener("pointerleave", e => { if (e.pointerType === "mouse") selRl(null); });
document.addEventListener("click", () => { if (matchMedia("(hover: none)").matches) selRl(null); });
new IntersectionObserver(es => es.forEach(e => { rlVis = e.isIntersecting; if (!rlVis) selRl(null); }), { threshold: .1 }).observe(trilho);
''' + s[j:]
open(f, "w", encoding="utf-8").write(s)

f = "index.html"; s = open(f, encoding="utf-8").read()
s = rep(s, '    <div class="setas"><button type="button" data-rl="-1" aria-label="Vídeo anterior">←</button><button type="button" data-rl="1" aria-label="Próximo vídeo">→</button></div>\n', '')
open(f, "w", encoding="utf-8").write(s)

f = "css/style.css"; s = open(f, encoding="utf-8").read()
i = s.index(".rl-vp{"); j = s.index("/* larissa */")
s = s[:i] + '''.rl-vp{overflow:hidden;padding:36px 0}
.rl-trilho{display:flex;gap:14px;width:max-content;will-change:transform}
.rl{position:relative;width:220px;aspect-ratio:9/16;border-radius:var(--r);overflow:hidden;background:var(--gelo);cursor:pointer;flex:none;transition:transform .5s var(--mola),opacity .35s,box-shadow .35s}
.rl-trilho.tem-sel .rl{opacity:.55}
.rl-trilho .rl.on{opacity:1;transform:scale(1.15);z-index:2;box-shadow:0 22px 44px -18px rgba(11,78,166,.6)}
.rl img,.rl video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.rl video{opacity:0;transition:opacity .35s}
.rl.on video{opacity:1}
.rl-barra{position:absolute;left:10px;right:10px;top:10px;height:3px;border-radius:2px;background:rgba(255,255,255,.4);overflow:hidden;opacity:0;z-index:1;transition:opacity .3s}
.rl.on .rl-barra{opacity:1}
.rl-barra i{display:block;height:100%;width:0;background:#fff}

''' + s[j:]
s = rep(s, "  .rl{width:140px}\n  .rl.on{width:210px}\n", "  .rl{width:160px}\n")
s = rep(s, ".rl-vp{overflow:hidden;padding:36px 0}", ".rl-vp{overflow:hidden;padding:36px 0 30px}")
s = rep(s, ".reels-top{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;margin-bottom:26px}", ".reels-top{margin-bottom:0}")
s = rep(s, "  .reels-top{align-items:flex-end}\n", "")
s = rep(s, ".setas{display:flex;gap:8px;flex:none}\n.setas button,.rev-nav button{", ".rev-nav button{")
s = rep(s, ".setas button:hover,.rev-nav button:hover{", ".rev-nav button:hover{")
open(f, "w", encoding="utf-8").write(s)

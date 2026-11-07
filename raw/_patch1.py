def rep(s, a, b):
    assert a in s, a[:60]; return s.replace(a, b)
f = "js/script.js"; s = open(f, encoding="utf-8").read()
# degraus: altura como fração
s = rep(s, 'b.style.setProperty("--h", `${22 + i * 13}%`);', 'b.style.setProperty("--k", (.24 + i * .152).toFixed(3));')
# reels: 3 cópias do trilho, começa no meio e salta sem transição ao passar das bordas
i = s.index('const trilho = $("[data-trilho]");'); j = s.index('const vCapa = $(".ca-2 video");')
s = s[:i] + '''const trilho = $("[data-trilho]");
const umaVolta = REELS.map(r => `<div class="rl"><img src="img/reel-${r}.webp" alt="" loading="lazy"><video muted playsinline preload="none" src="video/${r}.mp4"></video><span class="rl-barra"><i></i></span></div>`).join("");
trilho.innerHTML = umaVolta + umaVolta + umaVolta;
const rls = $$(".rl", trilho), N = REELS.length, LIM = 9;
let ri = N, rlVis = false, rlRaf, saltoT;
function centraRl() {
  const w = innerWidth <= 520 ? [140, 210] : [190, 262], gap = 14;
  trilho.style.transform = `translateX(${trilho.parentElement.clientWidth / 2 - (ri * (w[0] + gap) + w[1] / 2)}px)`;
}
function marcaRl() { rls.forEach((r, j) => r.classList.toggle("on", j === ri)); centraRl(); }
function vaiRl(i) {
  $("video", rls[ri]).pause(); cancelAnimationFrame(rlRaf); clearTimeout(saltoT);
  ri = i; marcaRl();
  if (rlVis) tocaRl();
  // passou da volta do meio: volta para ela sem o olho perceber
  saltoT = setTimeout(() => {
    if (ri >= N && ri < 2 * N) return;
    const v = $("video", rls[ri]), t = v.currentTime, novo = ri >= 2 * N ? ri - N : ri + N;
    trilho.classList.add("salto"); v.pause(); ri = novo; marcaRl();
    trilho.getBoundingClientRect(); trilho.classList.remove("salto");
    if (rlVis) tocaRl(t);
  }, 850);
}
function tocaRl(de = 0) {
  const c = rls[ri], v = $("video", c), barra = $(".rl-barra i", c);
  try { v.currentTime = de; } catch (e) {}
  const pr = v.play(); if (pr && pr.catch) pr.catch(() => {});
  cancelAnimationFrame(rlRaf);
  (function passo() {
    const dur = Math.min(LIM, v.duration || LIM), p = Math.min(1, v.currentTime / dur);
    barra.style.width = `${p * 100}%`;
    if (p >= 1 || v.ended) { vaiRl(ri + 1); return; }
    rlRaf = requestAnimationFrame(passo);
  })();
}
rls.forEach((r, i) => r.addEventListener("click", () => { if (i !== ri) vaiRl(i); }));
$$("[data-rl]").forEach(b => b.addEventListener("click", () => vaiRl(ri + +b.dataset.rl)));
marcaRl();
addEventListener("resize", centraRl);
new IntersectionObserver(es => es.forEach(e => {
  rlVis = e.isIntersecting;
  if (rlVis) tocaRl($("video", rls[ri]).currentTime); else { cancelAnimationFrame(rlRaf); $("video", rls[ri]).pause(); }
}), { threshold: .3 }).observe(trilho);
''' + s[j:]
open(f, "w", encoding="utf-8").write(s)

f = "css/style.css"; s = open(f, encoding="utf-8").read()
s = rep(s, ".dg i{display:block;border-radius:10px 10px 4px 4px;background:var(--gelo);height:var(--h);transition:background .35s}", ".dg i{display:block;border-radius:10px 10px 4px 4px;background:var(--gelo);height:calc((100% - 2.6em) * var(--k));transition:background .35s}")
s = rep(s, ".dg span{font-size:.72rem;font-weight:500;color:var(--cinza);line-height:1.2;height:2.4em;", ".dg span{font-size:.72rem;font-weight:500;color:var(--cinza);line-height:1.2;height:2.6em;flex:none;")
s = rep(s, ".ca-2{right:0;bottom:30px;width:34%;aspect-ratio:9/15;", ".ca-2{right:0;bottom:30px;width:34%;aspect-ratio:1/1.32;")
s = rep(s, ".ca img,.ca video{width:100%;height:100%;object-fit:cover}", ".ca img,.ca video{width:100%;height:100%;object-fit:cover}\n.ca-2 video{object-position:50% 100%}")
s = rep(s, ".rl-trilho{display:flex;gap:14px;align-items:center;width:max-content;transition:transform .8s var(--mola)}", ".rl-trilho{display:flex;gap:14px;align-items:center;width:max-content;transition:transform .8s var(--mola)}\n.rl-trilho.salto,.rl-trilho.salto .rl{transition:none}")
s = rep(s, ".rev-cards{position:relative;min-height:160px}", ".rev-cards{display:grid}")
s = rep(s, ".rc{position:absolute;inset:0;padding:24px 28px;", ".rc{grid-area:1/1;padding:24px 28px;")
s = rep(s, ".rc.on{position:relative;opacity:1;", ".rc.on{opacity:1;")
open(f, "w", encoding="utf-8").write(s)

f = "index.html"; s = open(f, encoding="utf-8").read()
s = rep(s, "https://maps.google.com/maps?q=Avenida%204%2C%20Av.%20Cidade%20Claret%2C%201546%2C%20Rio%20Claro%20-%20SP&z=16&output=embed", "https://maps.google.com/maps?q=UP%20GO%20PILATES%20CALISTENIA%2C%20Rio%20Claro%20-%20SP&z=16&output=embed")
open(f, "w", encoding="utf-8").write(s)

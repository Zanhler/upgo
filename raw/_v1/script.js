// UP.GO — interações e movimento
(() => {
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const ZAP = "5519981261106";
const calmo = matchMedia("(prefers-reduced-motion: reduce)").matches;
const anima = typeof gsap !== "undefined" && !calmo;

/* ---------- aberto agora (Google: seg–sex 6h–21h, sáb 7h–12h) ---------- */
const HORAS = { 1: [360, 1260], 2: [360, 1260], 3: [360, 1260], 4: [360, 1260], 5: [360, 1260], 6: [420, 720] };
const DIAS = ["dom.", "seg.", "ter.", "qua.", "qui.", "sex.", "sáb."];
const fmt = m => `${Math.floor(m / 60)}h`;
function status() {
  const n = new Date(), d = n.getDay(), m = n.getHours() * 60 + n.getMinutes(), h = HORAS[d], el = $("[data-status]");
  $$("[data-horas] [data-d]").forEach(li => li.classList.toggle("hoje", li.dataset.d.split(" ").includes(String(d))));
  if (h && m >= h[0] && m < h[1]) { el.className = "status aberto"; $("b", el).textContent = `Aberto · até ${fmt(h[1])}`; return; }
  for (let i = 0; i < 8; i++) {
    const dd = (d + i) % 7, hh = HORAS[dd];
    if (!hh || (i === 0 && m >= hh[0])) continue;
    el.className = "status fechado";
    $("b", el).textContent = `Fechado · abre ${i === 0 ? "hoje" : i === 1 ? "amanhã" : DIAS[dd]} às ${fmt(hh[0])}`;
    return;
  }
}
status(); setInterval(status, 60000);

const cab = $("#cab");
const solid = () => cab.classList.toggle("solid", scrollY > 20);
addEventListener("scroll", solid, { passive: true }); solid();

/* ---------- Goooooooo! a faixa estica sozinha ---------- */
const go = $("[data-go]");
let nO = 1;
function esticaGo() {
  const caixa = go.parentElement;
  go.textContent = "G" + "o".repeat(nO);
  if (go.offsetWidth < caixa.clientWidth - 40) { nO++; setTimeout(esticaGo, 70); return; }
  go.textContent += "!";
  setTimeout(() => { nO = 1; esticaGo(); }, 2200);
}
if (!calmo) esticaGo(); else go.textContent = "Goooooooo!";

/* ---------- desafios: degraus que sobem sozinhos ---------- */
const DEGRAUS = [
  { n: "Primeiro passo", img: "estudio", t: "Antes do primeiro exercício, ouvimos sua história e entendemos de onde você está partindo.", alt: "Estúdio com reformers e aparelhos" },
  { n: "Aula em grupo", img: "mandala", t: "A energia é coletiva. A atenção é individual. As turmas são reduzidas por escolha.", alt: "Turma no tapete, em frente à parede de mandala azul" },
  { n: "Aparelhos", img: "reformer", t: "Pilates nos aparelhos, com acompanhamento e progressões que respeitam o seu momento.", alt: "Aluna no reformer" },
  { n: "Calistenia", img: "parada-parede", t: "Usar o próprio corpo como resistência: aprender a sustentar, movimentar e dominar o próprio corpo.", alt: "Aluna em parada de mão na parede" },
  { n: "Invertidas", img: "invertida-cadillac", t: "Cada invertida tem orientação, cuidado e uma progressão pensada para você.", alt: "Invertida no cadillac" },
  { n: "Tecido e arco", img: "arco", t: "As primeiras invertidas suspensas: movimentos que você talvez nunca imaginou fazer.", alt: "Aluna invertida no arco suspenso" },
];
const dgBox = $("[data-degraus]"), dgFotos = $("[data-d-fotos]"), dPto = $("[data-pto]");
DEGRAUS.forEach((d, i) => {
  const b = document.createElement("button");
  b.type = "button"; b.className = "dg"; b.setAttribute("role", "tab"); b.style.setProperty("--k", (.24 + i * .152).toFixed(3));
  b.innerHTML = `<i></i><span>${d.n}</span>`;
  b.addEventListener("click", () => { paraDg(); vaiDg(i); });
  dgBox.appendChild(b);
  dgFotos.insertAdjacentHTML("beforeend", `<img src="img/${d.img}.webp" alt="${d.alt}" loading="${i ? "lazy" : "eager"}">`);
});
const dgs = $$(".dg", dgBox), dgImgs = $$("img", dgFotos);
let di = -1, dgT;
function posPto(i) {
  const b = dgs[i], barra = $("i", b), cx = dgBox.getBoundingClientRect(), r = barra.getBoundingClientRect();
  return { x: r.left - cx.left + r.width / 2 - 9, y: r.top - cx.top - 24 };
}
function vaiDg(i) {
  const prev = di; di = i;
  dgs.forEach((b, j) => { b.classList.toggle("on", j === i); b.setAttribute("aria-selected", j === i); });
  dgImgs.forEach((im, j) => im.classList.toggle("on", j === i));
  $("[data-d-tit]").textContent = DEGRAUS[i].n; $("[data-d-txt]").textContent = DEGRAUS[i].t;
  const p = posPto(i);
  if (anima && prev >= 0) {
    // o ponto azul do logo pula de um degrau para o outro
    const de = posPto(prev);
    gsap.killTweensOf(dPto);
    gsap.timeline()
      .to(dPto, { x: p.x, duration: .55, ease: "none" }, 0)
      .to(dPto, { y: Math.min(de.y, p.y) - 30, duration: .27, ease: "power2.out" }, 0)
      .to(dPto, { y: p.y, duration: .28, ease: "power2.in" }, .27)
      .to(dPto, { scaleX: 1.25, scaleY: .75, duration: .08, yoyo: true, repeat: 1 }, .55);
  } else if (typeof gsap !== "undefined") gsap.set(dPto, { x: p.x, y: p.y });
  else dPto.style.transform = `translate(${p.x}px,${p.y}px)`;
}
const paraDg = () => clearInterval(dgT);
const tocaDg = () => { paraDg(); dgT = setInterval(() => vaiDg((di + 1) % DEGRAUS.length), 3400); };
vaiDg(0); tocaDg();
const desBox = $(".des");
desBox.addEventListener("mouseenter", paraDg);
desBox.addEventListener("mouseleave", tocaDg);
addEventListener("resize", () => { const p = posPto(di); if (typeof gsap !== "undefined") gsap.set(dPto, { x: p.x, y: p.y }); });

/* ---------- sanfona dos pilares: troca sozinha, hover assume ---------- */
const sfs = $$("[data-sanfona] .sf");
let si = 0, sfT;
const abreSf = i => { si = i; sfs.forEach((s, j) => s.classList.toggle("on", j === i)); };
const tocaSf = () => { clearInterval(sfT); sfT = setInterval(() => abreSf((si + 1) % sfs.length), 4200); };
sfs.forEach((s, i) => {
  s.addEventListener("mouseenter", () => { clearInterval(sfT); abreSf(i); });
  s.addEventListener("focus", () => { clearInterval(sfT); abreSf(i); });
  s.addEventListener("click", () => { clearInterval(sfT); abreSf(i); });
});
$("[data-sanfona]").addEventListener("mouseleave", tocaSf);
tocaSf();
$$(".gr").forEach(g => g.addEventListener("click", () => {
  if (anima) gsap.fromTo(".grego strong", { scale: 1 }, { scale: 1.18, duration: .18, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "left center" });
}));

/* ---------- reels: o vídeo do meio toca, e passa para o próximo sozinho ---------- */
const REELS = ["desafios", "reformer", "bola", "turma", "temos-desafio", "hollywood"];
const trilho = $("[data-trilho]");
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
const vCapa = $(".ca-2 video");
new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { const p = vCapa.play(); if (p && p.catch) p.catch(() => {}); } else vCapa.pause(); })).observe(vCapa);

/* ---------- agendar: as escolhas viram a mensagem ---------- */
const esc = {};
const bolha = $("[data-bolha]"), enviar = $("[data-enviar]");
function mensagem() {
  let m = "Olá, gostaria de agendar uma aula!";
  if (esc.exp) m += ` ${esc.exp[0].toUpperCase()}${esc.exp.slice(1)}`;
  if (esc.motivo) m += `${esc.exp ? " e" : " Quero"} ${esc.exp ? "quero " : ""}${esc.motivo}`;
  if (esc.exp || esc.motivo) m += ".";
  if (esc.dia || esc.per) m += ` Fica melhor ${[esc.dia ? (esc.dia === "sábado" ? "no sábado" : `na ${esc.dia}`) : "", esc.per || ""].filter(Boolean).join(" ")}.`;
  return m;
}
function atualiza() {
  const m = mensagem();
  bolha.textContent = m;
  enviar.href = `https://wa.me/${ZAP}?text=${encodeURIComponent(m)}`;
  if (anima) gsap.fromTo(bolha, { scale: .96, transformOrigin: "right bottom" }, { scale: 1, duration: .35, ease: "back.out(2.4)" });
}
$$("[data-g]").forEach(g => g.addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b || b.disabled) return;
  const k = g.dataset.g, on = b.classList.contains("on");
  $$("button", g).forEach(x => x.classList.remove("on"));
  if (on) delete esc[k]; else { b.classList.add("on"); esc[k] = b.dataset.v; }
  // sábado só abre de manhã
  if (k === "dia") {
    const sab = esc.dia === "sábado";
    $$('[data-g="per"] button').forEach(x => { x.disabled = sab && x.dataset.v !== "de manhã"; });
    if (sab && esc.per && esc.per !== "de manhã") { delete esc.per; $$('[data-g="per"] button').forEach(x => x.classList.remove("on")); }
  }
  atualiza();
}));
atualiza();

// mandala da parede do estúdio: anéis de pétalas gerados
const mand = $("[data-mandala]");
const petala = (r, l, w) => `M0 ${-r} C${w} ${-r - l * .35} ${w * .75} ${-r - l * .8} 0 ${-r - l} C${-w * .75} ${-r - l * .8} ${-w} ${-r - l * .35} 0 ${-r}Z`;
let mHtml = "";
[[40, 46, 16, 10], [78, 60, 22, 14], [128, 78, 28, 18], [196, 92, 34, 24]].forEach(([r, l, w, n]) => {
  for (let i = 0; i < n; i++) {
    const a = 360 / n * i + (n % 4 ? 9 : 0);
    mHtml += `<g transform="rotate(${a})"><path d="${petala(r, l, w)}"/><path d="${petala(r + l * .18, l * .62, w * .55)}"/><circle cy="${-r - l - 8}" r="3"/></g>`;
  }
});
mand.innerHTML = mHtml + `<circle r="24"/><circle r="36"/>`;

/* ---------- avaliações: uma por vez ---------- */
const cards = $$(".rc"), pts = $("[data-pts]");
pts.innerHTML = cards.map(() => "<i></i>").join("");
let ci = 0, ct;
const vaiRv = i => { ci = (i + cards.length) % cards.length; cards.forEach((c, k) => c.classList.toggle("on", k === ci)); $$("i", pts).forEach((q, k) => q.classList.toggle("on", k === ci)); };
const autoRv = () => { clearInterval(ct); ct = setInterval(() => vaiRv(ci + 1), 4500); };
$$("[data-rv]").forEach(b => b.addEventListener("click", () => { vaiRv(ci + +b.dataset.rv); autoRv(); }));
$$("i", pts).forEach((q, k) => q.addEventListener("click", () => { vaiRv(k); autoRv(); }));
const rvBox = $("[data-reviews]");
rvBox.addEventListener("mouseenter", () => clearInterval(ct));
rvBox.addEventListener("mouseleave", autoRv);
vaiRv(0); autoRv();

/* ---------- movimento ---------- */
const abertura = $("[data-abertura]");
const fim = () => { abertura.remove(); document.body.classList.remove("abrindo"); };
const l2 = $("[data-vira]");

if (!anima) { fim(); return; }
gsap.registerPlugin(ScrollTrigger);

// abertura: a figura em um traço só, depois as letras; o triângulo sobe e o ponto cai
const entra = gsap.timeline({ paused: true });
entra.from(".capa-txt > *", { y: 22, opacity: 0, duration: .7, stagger: .08, ease: "power3.out" })
     .from(".ca", { y: 50, opacity: 0, duration: .9, stagger: .1, ease: "power3.out" }, 0)
     .from(".ca-frase", { scale: .7, opacity: 0, duration: .5, ease: "back.out(2)", transformOrigin: "left bottom" }, .5);
const viraL2 = () => gsap.fromTo(l2, { rotation: 0 }, { rotation: 360, duration: 1.05, ease: "back.inOut(1.3)" });

const ab = gsap.timeline({ onComplete: () => { fim(); }, defaults: { ease: "power2.inOut" } });
ab.set(".ab-t", { opacity: 1 })
  .to(".ab-lotus", { strokeDashoffset: 0, duration: 1.05 }, .05)
  .to(".ab-arco", { strokeDashoffset: 0, duration: .35 }, 1)
  .fromTo(".ab-cab", { scale: 0, opacity: 1 }, { scale: 1, duration: .4, ease: "back.out(3)" }, 1.12)
  .to(".ab-l", { strokeDashoffset: 0, duration: .42, stagger: .13 }, 1.15)
  .fromTo(".ab-tri", { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: .35, ease: "back.out(2.6)" }, 1.6)
  .fromTo(".ab-pto", { y: -70, opacity: 1 }, { y: 0, duration: .6, ease: "bounce.out" }, 1.6)
  .to(".ab-sub", { opacity: 1, duration: .35 }, 1.9)
  .add(() => { entra.play(); setTimeout(viraL2, 650); }, 2.55)
  .to(abertura, { yPercent: -100, duration: .75, ease: "power3.inOut" }, 2.5);
abertura.addEventListener("click", () => ab.progress(1));

// "Não por aqui!" dá uma cambalhota: sozinha de tempos em tempos e ao passar o mouse
l2.addEventListener("mouseenter", viraL2);
l2.addEventListener("click", viraL2);
setInterval(() => { if (scrollY < 500 && !document.hidden) viraL2(); }, 7000);

// colagem da capa responde ao mouse
const arte = $("[data-arte]");
arte.addEventListener("mousemove", e => {
  const r = arte.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
  $$("[data-p]", arte).forEach(el => gsap.to(el, { x: x * 22 * +el.dataset.p, y: y * 18 * +el.dataset.p, duration: .8, overwrite: "auto" }));
});

// mandala gira devagar
gsap.to(mand, { rotation: 360, duration: 120, repeat: -1, ease: "none", transformOrigin: "50% 50%" });

// entradas discretas
$$("[data-e]").forEach(el => gsap.from(el, { y: 20, opacity: 0, duration: .7, ease: "power3.out", scrollTrigger: { trigger: el, start: "top 90%", once: true } }));
gsap.from(".lar-foto", { x: -40, opacity: 0, duration: .9, ease: "power3.out", scrollTrigger: { trigger: ".lar", start: "top 80%", once: true } });
gsap.from(".chat", { y: 40, opacity: 0, duration: .8, ease: "power3.out", scrollTrigger: { trigger: ".chat", start: "top 88%", once: true } });

// nota sobe até 5,0 quando aparece
const nota = $("[data-conta]");
ScrollTrigger.create({ trigger: nota, start: "top 90%", once: true, onEnter: () => {
  const o = { v: 0 };
  gsap.to(o, { v: +nota.dataset.conta, duration: 1.2, ease: "power2.out", onUpdate: () => { nota.textContent = o.v.toFixed(1).replace(".", ","); } });
} });
})();

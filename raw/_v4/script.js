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
let nO = 1, maxO = 0;
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
  b.addEventListener("click", () => { paraDg(); vaiDg(i); dgT = setTimeout(tocaDg, 6000); });
  dgBox.appendChild(b);
  dgFotos.insertAdjacentHTML("beforeend", `<img src="img/${d.img}.webp" alt="${d.alt}" loading="${i ? "lazy" : "eager"}">`);
});
const dgs = $$(".dg", dgBox), dgImgs = $$("img", dgFotos);
let di = -1, dgT;
function posPto(i) {
  const b = dgs[i], barra = $("i", b), cx = dgBox.getBoundingClientRect(), r = barra.getBoundingClientRect();
  return { x: r.left - cx.left + r.width / 2 - 9, y: r.top - cx.top - 24 };
}
// a bolinha (o ponto azul do logo) não para: pinga no degrau e salta para o próximo
let pulo, pinga, dgVis = false;
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
  const topo = Math.min(posPto(prev).y, p.y) - 36, d = Math.abs(i - prev) > 1 ? .4 : .25;
  gsap.set(dPto, { scaleX: 1, scaleY: 1 });
  pulo = gsap.timeline({ onComplete: pingaNoDegrau })
    .to(dPto, { x: p.x, duration: d * 2, ease: "none" }, 0)
    .to(dPto, { y: topo, duration: d, ease: "power2.out" }, 0)
    .to(dPto, { y: p.y, duration: d, ease: "power2.in" }, d)
    .to(dPto, { scaleX: 1.28, scaleY: .72, transformOrigin: "50% 100%", duration: .07, yoyo: true, repeat: 1 }, d * 2)
    .fromTo($("i", dgs[i]), { y: 5 }, { y: 0, duration: .28, ease: "back.out(3)", clearProps: "y" }, d * 2);
}
// sobe de um em um e, do último, volta para o primeiro
const paraDg = () => { clearInterval(dgT); clearTimeout(dgT); };
const tocaDg = () => { paraDg(); if (dgVis) dgT = setInterval(() => vaiDg((di + 1) % DEGRAUS.length), 2600); };
vaiDg(0);
// só começa a subir quando a pessoa chega na seção; ao sair, volta para o primeiro degrau
new IntersectionObserver(es => es.forEach(e => {
  dgVis = e.isIntersecting;
  if (dgVis) tocaDg(); else { paraDg(); if (di) vaiDg(0); }
}), { threshold: .6 }).observe(dgBox);
addEventListener("resize", () => {
  const p = posPto(di); if (typeof gsap === "undefined") return;
  if (pinga) pinga.kill(); if (pulo) pulo.kill();
  gsap.set(dPto, { x: p.x, y: p.y }); if (anima) pingaNoDegrau();
});

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
const umaVolta = REELS.map(r => `<div class="rl"><img src="img/reel-${r}.webp" alt="" loading="lazy"><video muted loop playsinline preload="none" src="video/${r}.mp4"></video><span class="rl-barra"><i></i></span></div>`).join("");
trilho.innerHTML = umaVolta + umaVolta + umaVolta;
const rls = $$(".rl", trilho), N = REELS.length;
let rlX = 0, rlSel = null, rlVis = false, rlT0 = 0, rlRaf;
let rlVolta = 0;
const medeVolta = () => { rlVolta = rls[N].offsetLeft - rls[0].offsetLeft; };
medeVolta(); addEventListener("resize", medeVolta);
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
    if (rlVolta && -rlX >= rlVolta) rlX += rlVolta;
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
const vCapa = $(".ca-2 video");
const tocaCapa = () => { const p = vCapa.play(); if (p && p.catch) p.catch(() => {}); };
new IntersectionObserver(es => es.forEach(e => { if (!e.isIntersecting) vCapa.pause(); else if (!document.body.classList.contains("abrindo")) tocaCapa(); })).observe(vCapa);

/* ---------- agendar: as escolhas viram a mensagem ---------- */
const esc = {}; // motivo e dia são listas
const bolha = $("[data-bolha]"), enviar = $("[data-enviar]");
const lista = (a, liga = "e") => a.length < 2 ? a[0] : `${a.slice(0, -1).join(", ")} ${liga} ${a[a.length - 1]}`;
const noDia = d => d === "sábado" ? "no sábado" : `na ${d}`;
function mensagem() {
  let m = "Olá, gostaria de agendar uma aula!";
  const mot = esc.motivo || [], dias = esc.dia || [];
  if (esc.exp) m += ` ${esc.exp[0].toUpperCase()}${esc.exp.slice(1)}`;
  if (mot.length) m += `${esc.exp ? " e quero" : " Quero"} ${lista(mot)}`;
  if (esc.exp || mot.length) m += ".";
  if (dias.length || esc.per) m += ` Fica melhor ${[dias.length ? lista(dias.map(noDia), "ou") : "", esc.per || ""].filter(Boolean).join(" ")}.`;
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
  const k = g.dataset.g;
  if (g.hasAttribute("data-multi")) {
    b.classList.toggle("on");
    const v = $$("button.on", g).map(x => x.dataset.v);
    if (v.length) esc[k] = v; else delete esc[k];
  } else {
    const on = b.classList.contains("on");
    $$("button", g).forEach(x => x.classList.remove("on"));
    if (on) delete esc[k]; else { b.classList.add("on"); esc[k] = b.dataset.v; }
  }
  // só sábado marcado: o estúdio fecha às 12h, então só cabe a manhã
  if (k === "dia") {
    const soSab = (esc.dia || []).length === 1 && esc.dia[0] === "sábado";
    $$('[data-g="per"] button').forEach(x => { x.disabled = soSab && x.dataset.v !== "de manhã"; });
    if (soSab && esc.per && esc.per !== "de manhã") { delete esc.per; $$('[data-g="per"] button').forEach(x => x.classList.remove("on")); }
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
const fim = () => { abertura.remove(); document.body.classList.remove("abrindo"); tocaCapa(); if (!calmo) esticaGo(); };
const l2 = $("[data-vira]");

if (!anima) { fim(); return; }
gsap.registerPlugin(ScrollTrigger);

// abertura: a figura em um traço só, depois as letras; o triângulo sobe e o ponto cai
const entra = gsap.timeline({ paused: true });
entra.from(".capa-txt > *", { y: 22, opacity: 0, duration: .7, stagger: .08, ease: "power3.out" })
     .from(".ca", { y: 50, opacity: 0, duration: .9, stagger: .1, ease: "power3.out" }, 0)
     .from(".ca-frase", { scale: .7, opacity: 0, duration: .5, ease: "back.out(2)", transformOrigin: "left bottom" }, .5);
const viraL2 = () => { if (!gsap.isTweening(l2)) gsap.fromTo(l2, { rotation: 0 }, { rotation: 360, duration: .9, ease: "power2.inOut", force3D: true }); };

const ab = gsap.timeline({ onComplete: () => { fim(); setTimeout(viraL2, 500); setInterval(() => { if (scrollY < 500 && !document.hidden) viraL2(); }, 7000); }, defaults: { ease: "power2.inOut" } });
ab.set(".ab-t", { opacity: 1 })
  .to(".ab-lotus", { strokeDashoffset: 0, duration: 1.05 }, .05)
  .to(".ab-arco", { strokeDashoffset: 0, duration: .35 }, 1)
  .fromTo(".ab-cab", { scale: 0, opacity: 1 }, { scale: 1, duration: .4, ease: "back.out(3)" }, 1.12)
  .to(".ab-l", { strokeDashoffset: 0, duration: .42, stagger: .13 }, 1.15)
  .fromTo(".ab-tri", { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: .35, ease: "back.out(2.6)" }, 1.6)
  .fromTo(".ab-pto", { y: -70, opacity: 1 }, { y: 0, duration: .6, ease: "bounce.out" }, 1.6)
  .to(".ab-sub", { opacity: 1, duration: .35 }, 1.9)
  .add(() => entra.play(), 2.55)
  .to(abertura, { yPercent: -100, duration: .75, ease: "power3.inOut" }, 2.5);
abertura.addEventListener("click", () => ab.progress(1));

// "Não por aqui!" dá uma cambalhota: sozinha de tempos em tempos e ao passar o mouse
l2.addEventListener("mouseenter", viraL2);
l2.addEventListener("click", viraL2);


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

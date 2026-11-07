# rodada 3: degraus só começam ao chegar na seção e voltam do último ao primeiro; "date" mais baixo e com múltipla escolha
import os, shutil
os.makedirs("raw/_v2", exist_ok=True)
for a in ["index.html", "css/style.css", "js/script.js"]:
    shutil.copy(a, "raw/_v2/" + os.path.basename(a))
def rep(s, a, b):
    assert a in s, a[:60]; return s.replace(a, b)

f = "js/script.js"; s = open(f, encoding="utf-8").read()
s = rep(s, "let pulo, pinga, sentido = 1;", "let pulo, pinga, dgVis = false;")
# pulo de volta ao primeiro é mais longo
s = rep(s, '''  const topo = Math.min(posPto(prev).y, p.y) - 36;
''', '''  const topo = Math.min(posPto(prev).y, p.y) - 36, d = Math.abs(i - prev) > 1 ? .4 : .25;
''')
s = rep(s, '''    .to(dPto, { x: p.x, duration: .5, ease: "none" }, 0)
    .to(dPto, { y: topo, duration: .25, ease: "power2.out" }, 0)
    .to(dPto, { y: p.y, duration: .25, ease: "power2.in" }, .25)
    .to(dPto, { scaleX: 1.28, scaleY: .72, transformOrigin: "50% 100%", duration: .07, yoyo: true, repeat: 1 }, .5)
    .fromTo($("i", dgs[i]), { y: 5 }, { y: 0, duration: .28, ease: "back.out(3)", clearProps: "y" }, .5);''',
'''    .to(dPto, { x: p.x, duration: d * 2, ease: "none" }, 0)
    .to(dPto, { y: topo, duration: d, ease: "power2.out" }, 0)
    .to(dPto, { y: p.y, duration: d, ease: "power2.in" }, d)
    .to(dPto, { scaleX: 1.28, scaleY: .72, transformOrigin: "50% 100%", duration: .07, yoyo: true, repeat: 1 }, d * 2)
    .fromTo($("i", dgs[i]), { y: 5 }, { y: 0, duration: .28, ease: "back.out(3)", clearProps: "y" }, d * 2);''')
i = s.index("// sobe até o último degrau e desce de volta"); j = s.index('addEventListener("resize", () => {\n  const p = posPto(di)')
s = s[:i] + '''// sobe de um em um e, do último, volta para o primeiro
const paraDg = () => { clearInterval(dgT); clearTimeout(dgT); };
const tocaDg = () => { paraDg(); if (dgVis) dgT = setInterval(() => vaiDg((di + 1) % DEGRAUS.length), 2600); };
vaiDg(0);
// só começa a subir quando a pessoa chega na seção; ao sair, volta para o primeiro degrau
new IntersectionObserver(es => es.forEach(e => {
  dgVis = e.isIntersecting;
  if (dgVis) tocaDg(); else { paraDg(); if (di) vaiDg(0); }
}), { threshold: .6 }).observe(dgBox);
''' + s[j:]

# agendar: motivo e dia aceitam mais de um
i = s.index("function mensagem() {"); j = s.index("function atualiza() {")
s = s[:i] + '''const lista = (a, liga = "e") => a.length < 2 ? a[0] : `${a.slice(0, -1).join(", ")} ${liga} ${a[a.length - 1]}`;
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
''' + s[j:]
i = s.index('$$("[data-g]").forEach(g => g.addEventListener("click", e => {'); j = s.index("atualiza();\n\n// mandala")
s = s[:i] + '''$$("[data-g]").forEach(g => g.addEventListener("click", e => {
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
''' + s[j:]
s = rep(s, "const esc = {};", "const esc = {}; // motivo e dia são listas")
open(f, "w", encoding="utf-8").write(s)

f = "index.html"; s = open(f, encoding="utf-8").read()
s = rep(s, '<div class="ag-g" data-g="motivo"><p>', '<div class="ag-g" data-g="motivo" data-multi><p>')
s = rep(s, '<div class="ag-g" data-g="dia"><p>Melhor dia</p>', '<div class="ag-g" data-g="dia" data-multi><p>Melhores dias</p>')
s = rep(s, "Não desmarque da sua agenda. Escolha abaixo e a conversa vai pronta para o WhatsApp.", "Não desmarque da sua agenda. Marque o que quiser, mais de um motivo e mais de um dia, e a conversa vai pronta para o WhatsApp.")
open(f, "w", encoding="utf-8").write(s)

f = "css/style.css"; s = open(f, encoding="utf-8").read()
s = rep(s, ".ag-g{margin-top:16px}", ".sec-azul{padding:44px 0}\n.ag-g{display:grid;grid-template-columns:104px 1fr;align-items:center;gap:8px;margin-top:8px}\n.ag-esq .sub{max-width:600px;margin-bottom:16px}")
s = rep(s, ".ag-g p{font-size:.8rem;font-weight:500;color:rgba(255,255,255,.75);margin-bottom:6px}", ".ag-g p{font-size:.8rem;font-weight:500;color:rgba(255,255,255,.75)}\n.ag-g div{display:flex;flex-wrap:wrap;gap:6px}")
s = rep(s, ".ag-g button{height:36px;padding:0 14px;margin:0 6px 6px 0;", ".ag-g button{height:34px;padding:0 13px;")
s = rep(s, ".mandala{position:absolute;right:-170px;top:50%;width:760px;height:760px;margin-top:-380px;", ".mandala{position:absolute;right:-150px;top:50%;width:640px;height:640px;margin-top:-320px;")
s = rep(s, ".chat-c{background:var(--gelo);min-height:190px;padding:18px 16px;", ".chat-c{background:var(--gelo);min-height:128px;padding:14px 16px;")
s = rep(s, ".chat .bt{width:calc(100% - 32px);margin:14px 16px 16px}", ".chat .bt{width:calc(100% - 32px);margin:12px 16px 14px}")
s = rep(s, "  .mandala{right:-300px;width:640px;height:640px;margin-top:-320px}\n", "  .mandala{right:-300px}\n  .sec-azul{padding:40px 0}\n  .ag-g{grid-template-columns:1fr;gap:5px;margin-top:12px}\n")
open(f, "w", encoding="utf-8").write(s)

# agrupa os botões de cada grupo numa div, para a linha "rótulo + botões"
f = "index.html"; s = open(f, encoding="utf-8").read()
import re
def agrupa(m):
    return f'{m.group(1)}\n        <div>{m.group(2).strip()}</div>\n      </div>'
s, n = re.subn(r'(<div class="ag-g"[^>]*><p>[^<]*</p>)\s*((?:<button[^\n]*</button>))\s*</div>', agrupa, s)
assert n == 4, n
open(f, "w", encoding="utf-8").write(s)

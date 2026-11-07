# UP.GO Pilates & Calistenia — landing

`start.bat` sobe `serve.py` (sem cache e com Range, por causa dos vídeos) na porta **4200** e abre http://localhost:4200.
HTML/CSS/JS puro. Tudo em `js/script.js`; GSAP + ScrollTrigger em `js/vendor`.

## De onde veio cada coisa
- **Google Maps** (`raw/_maps.py`, `raw/_dados.py`): Avenida 4, Av. Cidade Claret, 1546, Rio Claro/SP, 13503-230; (19) 98126-1106; seg–sex 6h–21h, sáb 7h–12h, dom fechado; 5,0 com 30 avaliações; avaliações citadas. Fotos do Maps: estúdio, reformer, barrel, cadillac, parada na parede.
- **Instagram @upgo.pilatesefuncional** (`raw/_ig.py`, `raw/_posts.py`): bio, destaques ("Só alongamento? Não por aqui!", "Goooooooo!"), legendas (pilares, kállos + sthénos, "Posso tentar de novo?", "date"), fotos em alta e 6 reels em `video/`. Abre sem login.
- **@laris_bueno_**: Larissa Bueno, profissional de educação física, pós-graduada pela Unicamp. A legenda "Eu aprendi a gostar de exercício..." saiu na conta do estúdio, em 1ª pessoa, sem assinatura.
- **Logo**: redesenhado em SVG por cima do avatar (150px), em traços, para a abertura poder desenhá-lo (`raw/_logo_test.html` compara com o original).
- **Paleta**: azul do logo `#1c8fd6`, azul dos posts `#0d5cc0`, azul da faixa `#0b4ea6`, gelo `#f1f7fc`, preto `#17191c`. Só Poppins.
- **Fotos do tecido**: vinham com texto queimado; removido com inpaint em `raw/_imgs.py`.

## O que tem
Abertura (a figura do logo se desenha num traço só, letras em seguida, triângulo sobe, ponto cai quicando) · capa com "Não por aqui!" dando cambalhota e colagem com vídeo · faixa "Goooooo!" que estica sozinha · **Qual é o seu desafio?**: 6 degraus que sobem sozinhos, com o ponto azul do logo pulando · pilares em sanfona + kállos/sthénos · reels: o do meio toca, passa sozinho e dá a volta · depoimento da Larissa · **"date"**: escolhas viram a mensagem do WhatsApp, com a mandala da parede do estúdio girando no fundo · avaliações uma por vez (estrutura da Corpo Lounge) · mapa largo com cartão.

## A confirmar com o cliente
- Se (19) 98126-1106 é o WhatsApp: a bio usa link `wa.me/message/...`, que não mostra o número.
- Se a foto do tecido na seção da Larissa é ela: nada no post diz quem é.
- Se querem "Pilates com Jesus" no rodapé (está na bio).

## Fotos novas (07/11)
8 HEIC enviadas pelo dev: `raw/_heic.py` converte (pillow-heif num ambiente temporário) para `raw/novas/`; `raw/_patch5.py` gera `img/espaco-*.webp` e `img/det-*.webp`. Salão e sala da mandala entraram nos degraus 1 e 2; o resto na seção "O cuidado começa antes da aula". `img/estudio.webp` e `img/mandala.webp` ficaram sem uso. Legendas de Aroma, Som, Temperatura e Luz foram escritas a partir das fotos: confirmar com o cliente.

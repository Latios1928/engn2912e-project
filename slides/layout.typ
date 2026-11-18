// Repo layout diagram. Compile with:
//   typst compile layout.typ layout.png --ppi 220
// Uses the fletcher package (downloaded automatically on first compile).
#import "@preview/fletcher:0.5.8": diagram, edge, node

#set page(width: auto, height: auto, margin: 12pt, fill: white)
#set text(size: 14pt)
#show raw: set text(size: 14pt)

#let blue = rgb("#2f6fb0")
#let orange = rgb("#d9822b")
#let gray = rgb("#6b7280")
#let pwr = rgb("#b83a3a")
#let purple = rgb("#7c4dbd")

// A labelled box: bold title, optional gray subtitle.
#let card(pos, title, sub: none, color: black, fill: white, w: 150pt, name: none) = node(
  pos,
  box(width: w, align(center)[
    #text(weight: "bold", fill: color)[#title]
    #if sub != none [ \ #text(size: 14pt, fill: gray)[#sub] ]
  ]),
  stroke: 1.5pt + color,
  fill: fill,
  corner-radius: 6pt,
  inset: 10pt,
  name: name,
)

#diagram(
  spacing: (40pt, 100pt),
  edge-stroke: 1.5pt,

  card((1, 0), `snn_top.v`, fill: luma(245), name: <top>),

  node((0, 0), align(left)[`clk, rst, in[1:0],` \ `data[3:0], addr[3:0]`], stroke: none, name: <inpad>),
  node((2, 0), [`out[4:0]`], stroke: none, name: <outpad>),
  edge(<inpad>, <top>, "-|>"),
  edge(<top>, <outpad>, "-|>"),

  card(
    (0, 1),
    `snn_digital`,
    color: blue,
    fill: blue.lighten(88%),
    w: 170pt,
    name: <dig>,
  ),
  card(
    (2, 1),
    `snn_analog`,
    color: orange,
    fill: orange.lighten(88%),
    w: 170pt,
    name: <slot>,
  ),

  node((0, 1.7), align(center)[`vdd`#sub[`d`]], stroke: none, name: <dsup>),
  node((2, 1.7), align(center)[`vdd`#sub[`a`]`, VT, Iref`], stroke: none, name: <asup>),
  node((1, 1.7), [`gnd`], stroke: none, name: <gnd>),
  edge(<gnd>, (1, 1.35), (0.3, 1.35), (0.3, 1), "-|>", stroke: pwr + 1.5pt),
  edge(<gnd>, (1, 1.35), (1.7, 1.35), (1.7, 1), "-|>", stroke: pwr + 1.5pt),
  edge(<dsup>, <dig>, "-|>", stroke: pwr + 1.5pt),
  edge(<asup>, <slot>, "-|>", stroke: pwr + 1.5pt),

  edge(
    (0.75, 0),
    (0.75, 0.5),
    (0, 0.5),
    <dig>,
    "-|>",
    label: text(size: 14pt)[`clk, rst, data,` \ `addr, in`],
    label-side: center,
    label-pos: 0.5,
  ),
  edge(<dig>, <slot>, "-|>", label: text(size: 14pt)[`w, s, pulse`], label-side: center),
  edge(
    <slot>,
    (2, 0.5),
    (1.25, 0.5),
    (1.25, 0),
    "-|>",
    label: text(size: 14pt)[`spike`],
    label-side: center,
    label-pos: 0.5,
  ),
)

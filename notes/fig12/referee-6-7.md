# Referee report · Fig. 12, §6.7 "Rough roads, the tyre's grip, and shaking from below ★"

Read blind, as rendered, by its target reader: an undergraduate who knows Fourier series and the damped oscillator, plus a
school student good at maths. Page `public/simulations/beer-slosh.html`, built with `npm run build`, served from `public/`
with `notes/fig12/serve.cjs`, opened in headless Chromium at 1280 × 900 and 390 × 900 (DPR 2) with every fold open.
6 November 2026. No plan or check file was read.

Measured: no KaTeX errors on the page; no sideways page scroll at 390 px; every display box in §6.7 reports
scrollWidth = clientWidth (297 px at 390), so the overflow test passes, and yet (R1) loses glyphs on the phone (item 1).

## Severity-ordered findings

1. **(R1) is cut on a phone (390 px).** KaTeX breaks the display into three lines. The first line ends "cos(2" and the next
   starts "φ_i)", so the glyphs "πn_ix +" are missing. The scroll-width test does not catch this: the box reports 297/297
   while the line is cut inside it. The reader sees an equation with a hole in it, and it is the defining equation of the
   section. (R4) also breaks at 390 px, into "A > 4ζg = 4 × 0.0053 × / 9.81 m/s² / = 0.21 m/s² at / 2f₁₁ = 6.84 Hz". It
   is readable, but "at" is left alone on a line. (R2) and (R3) break cleanly.
2. **The Key-result box disagrees with the measurements below it.** The box says "a cobbled street at walking pace sits on
   the parametric resonance". But the setts as built are 150 mm stones plus 20 mm joints, so their pitch is 0.17 m and at
   1 m/s they shake at 5.9 Hz, not 6.84 Hz (they would match at 1.16 m/s). The next paragraph measures 0.034–0.090 m/s² rms
   for the setts in the 6.5–7.2 Hz band, which is ×√2 ≈ 0.05–0.13 m/s², below the 0.21 m/s² threshold. It then says that
   only class D and the washboard come close. So the box's main claim is overstated by the section's own numbers. The
   reader leaves with the wrong lesson.
3. **The Faraday analysis has no ending.** The section derives a threshold, finds that two roads come near it, and then
   Table 2a and the last paragraph explain the washboard by a different mechanism: horizontal pushing at f₁₁ (direct
   resonance). The reader is never told whether the parametric pumping happens in the simulation at all. Is the a_z term
   of (R3) in the live model? Does any row of Table 2a show it? A run with horizontal forcing off would settle it. As
   written, the reader cannot tell which mechanism causes which spill.
4. **Silent step in the ★ derivation: "keep the terms at ω".** The target reader knows the damped oscillator but probably
   not averaging or two-timing. The missing steps are these. Impose the gauge ċ cos ωt + ṡ sin ωt = 0. Use
   cos 2ωt cos ωt = ½(cos ωt + cos 3ωt) and cos 2ωt sin ωt = ½(sin 3ωt − sin ωt). Drop the 3ω terms, which is valid when ε
   and ζ are ≪ 1 (never stated). Then match the coefficients. Without these the equations for ċ and ṡ look pulled from a
   hat. The algebra itself checks: (c − s)˙ = (ε/4 − ζ)ω(c − s), so the threshold ε = 4ζ is right. It matches Landau and
   Lifshitz, *Mechanics* §27, which the section neither cites nor uses. The "Key result" also has no source (e.g. Benjamin
   and Ursell 1954 for Faraday sloshing).
5. **The section uses symbols defined only in later sections.** The section uses "b i" ("the motor's push b i", (R2)), but
   b and i are defined in section 7, *The DC gear motor*, which comes after §6.7. The Table 2a columns "PI speed" and
   "Slosh feedback" are defined in sections 8.2 and 8.4. The section also points ahead to "section 11.9" for the breaking
   limit and "section 13" for the 1.24 m/s². A reader going in order meets these as undefined. One clause each would fix
   it: "the motor force b i (section 7)", "the controllers of section 8".
6. **The physical picture of driving over a spectrum is missing.** Two ideas carry the whole section, and neither is
   stated:
   (a) At speed v, spatial frequency n becomes time frequency f = v n. The section uses this three times (14.6 cm ↔
   6.84 Hz, 0.30 m ↔ 3.3 Hz, v = λf₁₁) but never writes it down.
   (b) With w = 2, the height spectrum falls as n⁻². So the quoted rms heights (3.8 … 30.5 mm) come almost entirely from
   the longest waves near 0.011 cycles/m: gentle hills 90 m long, which do nothing to the pint. The acceleration spectrum
   ∝ (2πvn)⁴ G_d rises as n². The short waves shake the glass even though they are tiny in height.
   Without (b), the reader thinks "class D = 29 mm bumps", which is the wrong picture. (R1) is also simply a Fourier series
   on period L with random phases, and saying so would anchor it for this reader.
7. **Numbers and choices with no reason given.**
   - The lower limit 0.011 cycles/m is not a multiple of Δn = 1/126 m⁻¹. Why 0.011, and why L = 126 m?
   - The band 6.5–7.2 Hz is not linked to the width of the instability tongue. At threshold the tongue has zero width, so
     the band needs a reason.
   - Comparing a band rms ×√2 with a threshold derived for a coherent sine is fair only as an order of magnitude. The text
     half-says this ("the threshold's order"). Random parametric forcing has its own threshold.
   - "setts 0.034–0.090, washboard 0.13–0.15": a range over what? Seeds, speeds or controllers?
   - "The roughness ramps in" (linearly? cosine taper?) and "shifted to pass through zero at 1 m" (vertically?) are vague.
   - "more than the PI loop asks then": give the number.
   - "μ = 0.8 … of the order of rubber on a dry road": no source.
   - "a quarter of itself": 105.7 g is a quarter only of the 427 g stout, which is not stated here. A reader thinking of a
     568 ml pint gets about a fifth.
8. **The reader cannot follow the evidence trail, and some table entries are unexplained.**
   - "(checked: `node tools/fig12/study.cjs 25 speed 0` still gives 29.9 mm)": the reader does not know what 29.9 mm is,
     or which run it belongs to.
   - "(`notes/fig12/phase1.md` §6)": `notes/` is not under `public/`, so the site does not serve it. This is a dead
     reference for every reader.
   - Table 2a, washboard row: the PI lean (81.4 mm) is larger than the open-loop lean (66.7 mm), yet the PI spill is
     smaller (60.1 g against 105.7 g). The text does not mention it. The later remark about the breaking-limit clip half
     explains it.
   - Table 2a: spill is shown in some cells, and in one cell as "0 g", but left out of others. Does blank mean zero?
   - At 390 px every number in the table wraps from its unit ("7.6 / mm"). It is still readable.
   - The 6.5–7.2 Hz rms values are said to come from "Table 2a", but Table 2a holds leans and spills, not accelerations.

## Smaller points (lost-reader sentences)

- "m³" as the unit of G_d is unexplained: m² per (cycle/m). One clause would help the school student.
- "the wheel's envelope (section 6.1) does that here too": fine for an in-order reader.
- "its spin is not modelled (the motor stays tied to the cart's speed)": the section never says what this means on screen
  or for energy when the clip acts. When the wheel leaves the road, N = 0, so F_m = 0, and the cart coasts. Say so.
- (R3) writes ω and ζ, while (16) defines ω₁₁ and f₁₁, and (R4) switches to f₁₁. Name the mode once: ω = ω₁₁ = 2πf₁₁.
- The "heavier while it falls toward the middle, lighter while it rises" picture is correct. Energy gain
  dE/dt = −ω²(a_z/g) q q̇ is positive when a_z > 0 while q q̇ < 0. It is the best sentence in the section. Pair it with the
  playground swing pumped by standing at the bottom.
- Suspension check, offered free: transmissibility at r = 6.84/2.8 ≈ 2.4 is about 1/(r² − 1) ≈ 0.2. That predicts the
  measured road-to-glass ratio (0.72 → 0.142, a factor of 0.20). Stating it would be the "small number worked" that
  STANDARD §4.4 asks for.

## Verdict per part, against `notes/STANDARD.md` §4

| Part | Verdict | Reason |
|---|---|---|
| Opening paragraph | **Clear, leave it.** | Good everyday picture (hills to cobbles). |
| A road from its spectrum | **Needs work.** | (R1) cut at 390 px (item 1). Missing f = vn and the "height from long waves, shaking from short waves" picture (item 6). Unexplained 0.011 and 126 m (item 7). ISO numbers and rms heights check out: G₀n₀²(1/0.011 − 1/10) gives 3.81 mm for A. |
| The grip | **Needs work (small).** | b i used before section 7 defines it (item 5). The check command and "29.9 mm" are opaque (item 8). μ unsourced. The physics is sound: 0.8 × 4.4 N = 3.5 N. |
| Shaking from below: (R3)–(R4) | **Needs work.** | The averaging step is silent (item 4). Small-ε, small-ζ assumption not stated. No source for the threshold. The pumping picture and the arithmetic are right (4 × 0.0053 × 9.81 = 0.208). |
| Key-result box | **Needs work.** | The cobbles claim is contradicted by the sett pitch (0.17 m → 5.9 Hz) and by the measured band accelerations (item 2). |
| "Does the cart let that much through?" | **Needs work.** | Band and rms-vs-sine comparison not justified. Ranges not explained. Dead link to `notes/` (items 7, 8). Transmissibility check missing. |
| Table 2a | **Needs work (small).** | Columns refer forward to sections 8.2/8.4. Blank versus "0 g". The PI lean exceeds the open-loop lean without comment (item 8). |
| Washboard paragraph | **Clear, with one gap.** | The direct-resonance explanation and v = λf₁₁ = 1.03 m/s are clear and correct. It should say plainly that this is horizontal forcing, not the Faraday mechanism just derived (item 3). |

STANDARD items most missed: §4.3 (silent step), §4.4 (no check worked: the transmissibility check is there for the taking),
§4.6 (is a_z in the live model?), §4.8 (threshold unsourced; a dead `notes/` reference).

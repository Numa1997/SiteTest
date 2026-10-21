# Fig. 3 · Double-slit lecture note: judgment and plan

Page: `public/simulations/Interactive Double-Slit Experiment Visualization.html`, note on lines 129–536.
Rule: Numa's verdicts in `notes/STANDARD.md`. Judge first; a clear section is not touched; the smallest change that fixes a real gap.
Every number in the note was recomputed with the page's own formulas (`notes/fig03/check.cjs`, a copy of `compute()`, `storeDerived()`
and `drawPattern()` at page:620–634, 708–772) before judging; the results are listed under "Numbers checked".

## Verdicts

| § | Title | Verdict |
|---|---|---|
| 1 | Bright and dark from one source | Clear, leave it. Loudspeakers, soap film, CD, Young, photons: a physical picture before any symbol. Young's card (1/30 inch = 0.85 mm, middle always white, fringes gone when one edge is blocked) agrees with his paper, which I read (Phil. Trans. 94, 1804, Section I). |
| 2 | The model | Clear, leave it. Coordinates (1), assumptions, k, slider ranges; Figure 1 checked point by point (arc radius 223.2 = \|PS₁\|, Q on S₂P). |
| 3 | The exact path difference | Clear, leave it. (2)→(3) shown step by step; numbers match the page. |
| 4 | The far field, 4.1 ★, Figure 2, Exercise 4.1 | Clear, leave it. (4) and the geometric argument; (5) re-derived (odd powers of ε, third order) and correct; all numbers match. |
| 5 | Adding the two waves | **Needs work, two items.** (a) The box says "In the far field δs = b sin θ": θ appears here for the first time and is never defined; until now the note has only α, the direction of P. (b) "the cos Δφ term averages to zero": no cos Δφ has been written yet; (7) has cos²(Δφ/2), and the identity 2cos²(Δφ/2) = 1 + cos Δφ is a silent step. Section 7 then leans on "the cross term cos Δφ". Everything else (6)–(9), Figure 3, Exercise 5.1 is clear. |
| 6 | Slits with a width ★ | Clear, leave it. (10) integral checked; envelope numbers match. (β also names b²/4r² in 4.1; each is defined where it is used, both in ★ parts: taste, not a gap.) |
| 7 | One particle at a time | **Needs work, two items.** (c) "Close one slit, or place a detector …: the dots then pile up as the sum of two single-slit patterns": wrong for the closed slit, which gives one single-slit pattern (Feynman III-1, P₁ with hole 2 blocked; P′₁₂ = P′₁ + P′₂ only when watched). (d) "The animation shows how a fringe pattern builds up dot by dot": the page has no such animation; Figure 5 is a still. Rest clear. |
| 8 | How the page computes | Clear, leave it. Matches the code line by line (verdict thresholds, 301 samples, 57 samples per fringe, phase 0.8 Δt). The clock caps Δt at 0.05 s (sim.js:178); that only matters after a pause or a hidden tab: not a gap. |
| 9 | From lengths to pixels | Clear, leave it. All layout numbers match drawShapes()/drawWaves()/drawPattern(). |
| 10 | What the model leaves out | **Needs work, one item.** (e) "Polarisation … ignored. For small angles this changes nothing." The small quantity is the wrong one: what matters is the angle γ between the two paths at P, not the direction θ. At the page's own distances P is only 5 slit separations away and γ ≈ 11° at the default dark fringe; for light polarised in the plane of the drawing that dark fringe keeps sin²(γ/2) ≈ 0.9 % of I₀, more than a hundred times the 7×10⁻⁵ of the amplitude item above it. For light polarised along the slits nothing changes. Rest of § 10 clear. |
| 10.1 | Further reading | **Needs work.** (f) None of the three items has a link. Add a link to a page I opened for each; add Young's 1804 paper, the primary source of the numbers in § 1. |

## Planned changes (all inside existing lines, so no page line number moves)

(a) § 5 box, page line 345: before "In the far field …" add one sentence defining θ: any direction from the normal to the wall, as the
    plot under the figure uses it; α is the one direction that points at P.
(b) § 5, line 350: write (7) as E₀² + E₀² cos Δφ (from 2cos²(Δφ/2) = 1 + cos Δφ), name it the sum of the two intensities plus a
    cross term, then let the two lamps average the cross term away. Same sentence count plus one.
(c) § 7, line 491: "the dots then pile up as one single-slit pattern, or, with the detector, as the sum of two, without fringes".
(d) § 7, line 491: "The animation shows" → "Figure 5 shows".
(e) § 10, line 522: replace the second sentence with: light polarised along the slits: nothing changes; the other polarisation: each
    field points across its own path, the two meet tilted by γ, 11° at the default dark fringe; two equal arrows nearly opposed leave
    2E₀ sin(γ/2), so that dark fringe keeps sin²(γ/2) = 0.9 % of I₀; far away the paths are parallel and γ → 0.
(f) § 10.1, lines 529–531: links on the three titles (Pearson, Wiley, feynmanlectures.caltech.edu chapters I-29, I-30, III-1);
    Young 1804 appended on line 531 (same physical line, to keep every page line number fixed for the docs that link them).

No equation is renumbered or added. No figure, box or section is added.

## Numbers to measure for the changes, and how

- γ, the angle at P between S₁P and S₂P, and sin²(γ/2): in headless Chromium, set d = 200, b = 40, λ = 13.5 and α = 10.0° (the
  slider step nearest the dark fringe, verdict "Destructive"), read the stored points `pt_x`, `pt_y` and `L1`, `L2`, and compute the
  angle there; cross-check with the exact dark fringe α = 9.7613° found by bisection on the page's formula (3) (check.cjs).
- Also read back at the defaults: `ds`, `b_sin_a`, `m_x[1]`, the verdicts at 9.5°, 10°, 19.5°, 20° (Exercise 5.1), and Exercise 4.1
  at (b, d, α) = (80, 100, 30°) and (80, 300, 30°), to show the existing numbers hold in the browser too.

## Numbers checked (check.cjs, before any edit)

Defaults: L₁ = 206.8507, L₂ = 220.4784, δs = 13.627725, b sin α = 13.680806 (+0.390 %, 0.00393 λ), (5) gives 13.627469.
Figure 2: within 1 % from d = 124.73 px (r = 3.32 b); 1.554 % at d = 100. Exercise 4.1: 38.2685 / 40.0000 (4.52 %), 39.8008,
errors 1.7315 → 0.1992, drop 8.69, b/r = 0.693. Exercise 5.1: δs/λ = 0.4867, 0.5121, 0.9852, 1.0095 at 9.5°, 10°, 19.5°, 20°;
far field 9.715°, 19.725°; exact at d = 200: 9.761°, 19.805°; at d = 100: 20.044°. (9): 67.5 px; HeNe 2.532 mm.
§ 6: envelope 0.743 (30°), 0.265 (90°), 0.875 (θ₁) for w = 8; 0.405 for w = 20; θ₂ = 42.454°.
§ 7: (12) expects 130.9 and 2.25 dots; the 2000 dots drawn in Figure 5 (read from its SVG, x = 395 + 10.1 θ) give 139 strictly
within 1°, two more exactly on the boundary at the SVG's 0.1-unit rounding, and 3 near ±9.715°: consistent with the note's 140 and 3.
de Broglie 0.1226 nm at 100 V, 4485 × shorter than 550 nm. § 8: 57.4 samples per fringe at b = 80, λ = 8.
§ 9: b/λ = 2.963, 1.876 µm, 394.9 λ, 0.1451°, slow-down 6.8×10¹⁴. § 10: dark fringe α = 9.7613°, L₁ = 200.518, L₂ = 207.268,
amplitudes differ 1.64 %, I_min = 6.85×10⁻⁵; γ = 11.098°, sin²(γ/2) = 0.00935. Max |δs − (L₂ − L₁)| over all sliders 1.35×10⁻¹³ px.

## Done (20 October 2026)

Changes (a)–(f) made as planned, all within page lines 345, 350, 491, 522, 529–531; the page still has 948 lines, so no line
link anywhere moves. Walkthrough untouched. Doc `docs/simulations/fig03-double-slit.md`: header size (173 421 bytes, 62 long lines,
56 in the note) and the § 10 row of the note table.

Measured in headless Chromium on the build (`node notes/fig03/measure.cjs`, output `measure-out.json`), from the page's store:
- α = 10.0° (d = 200, b = 40, λ = 13.5; verdict "Destructive", δs/λ = 0.5121): γ = 11.082°, sin²(γ/2) = 0.00932.
  Exact dark fringe α = 9.7613° (check.cjs, the page's formula (3)): γ = 11.098°, sin²(γ/2) = 0.00935. Note: 11°, 0.9 %.
- Defaults: δs = 13.627724988366344, b sin α = 13.680805733026748, γ = 10.103°; Exercise 5.1 readouts 0.49, 0.51, 0.99, 1.01 with
  the verdicts the note names; Exercise 4.1 38.2685, 40.0000, 39.8008. γ over the sliders' corners: 2.9° to 43.6°.
- 1440 × 900 and 390 × 844: 0 console errors, 0 `.katex-error` (354 KaTeX nodes in the note), 0 px sideways scroll; all 13 folds
  closed by Collapse all and each reopened by its own toggle. The only boxes past the right edge at 390 px are KaTeX's visually hidden
  MathML copies (clipped, no scroll). Screenshots: `shot-*-1440.png`, `shot-*-390.png`.
- References: four items, each linked to a page opened on 20 October 2026 (Pearson and Wiley product pages with the chapter lists;
  feynmanlectures.caltech.edu I-29, I-30, III-1, read through Firecrawl because direct fetches get Cloudflare's 403; Young's paper,
  read as the Royal Society PDF through Firecrawl, Section I).

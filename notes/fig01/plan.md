# Fig. 1 · Wave Interference · plan

Page: `public/simulations/Circular Wave Interference Visualization.html`, note L98–L495. Walkthrough `circles` (not edited).
Doc: `docs/simulations/fig01-wave-sources.md`. Judged against notes/STANDARD.md §4 and Numa's verdicts: a clear section is not touched.

Constraint found while judging: other docs (`docs/scripts/dataset.md`, `datalog.md`, `sim.md`, `walk.md`) link to this page's
code by line number (L497, L505–L508, L526, L547, L572, L798, L893, L904). Every edit therefore stays inside existing lines:
the page keeps 907 lines and no line link anywhere moves.

## Verdicts

| § | Section | Verdict |
|---|---|---|
| Abstract, contents | | clear, leave it |
| 1 | Pebbles in a row | clear, leave it. Pond, harbour, line arrays, Huygens 1690, Figure 1; up to 24 sources matches `MAX_SOURCES`. |
| 2 | The model | clear, leave it. Wave equation, linearity, coordinates; 360.5 px field height, 770 × 347 canvas, 10 px lift, sliders and presets all match the code (measured). |
| 3 | One source, one ring ★ | clear, leave it. Hankel far field and the 1/(8kr) phase lag checked with mpmath: lag 0.00992 rad at kr = 4π (two wavelengths), height error 3.9 × 10⁻⁴. §3.1 matches `precompute()`; e^−0.15 = 0.861. |
| 4 | Adding the rings | **needs work.** "The pattern moves as one ring does: a crest keeps kr_i − ωt fixed and travels at v". True of each ring, not of the pattern: where rings cross at an angle the crests of the sum move faster and lie further apart. Straight up the middle between the two Reset sources, at the centre of the wide screen, they climb at 1.55 v and are 46 px apart (measured below). The Speed readout invites the reader to compare. |
| 5 | Two sources: calm hyperbolae | clear, leave it. (9), (10), 26 and 14 calm lines, residue 0.071 / 0.162 all recomputed. |
| 6 | A row ★ | **needs work.** "The damping factors are then all the same" is false for γ > 0: far away the factors differ from source to source by e^{γ s sinθ/R}, which does not shrink with distance (a factor 1.25 across the row at 42° at the default γ). The eqnote already says the check used γ = 0. Everything else (11)–(14), 0.220 side lobe, 42.0°, 63.2°, 79.2°, Figure 3 caption numbers: recomputed, correct. |
| 7 | Near the row ★ in 7.1 | clear, leave it. D²/λ = 15 053 px = 18.8 widths; every amplitude in the text and the Figure 4 caption recomputed (0.009–0.829, 0.036–0.765, 0.119–0.168, 0.050, 0.013–0.387, peaks every ≈ 44 px, 104.0 px, 0.142, 0.141, 0.140, 0.076 … 0.173). "Usual form" of the Fraunhofer condition: a matter of taste, the conclusion holds with or without the 8. |
| 8 | Two maps and a turning phase | clear, leave it. Matches `precompute()`, `render()`, `Sim.clock` (Δt cap 0.05 s), grid formula; grids re-measured. Build time on this machine 32–57 ms (note: 59–98 ms, "depend on the machine"); not a gap. |
| 9 | From numbers to colours | clear, leave it. LUT colours, 0.158, 2/255 match the builder. |
| 10 | What the model leaves out | clear, leave it. |
| 10.1 | Further reading | **needs work.** None of the four items has a link. Each needs a link to a page I opened; the list also lacks one open text a school student can actually read. |

## Changes (smallest that fix the gap)

1. §4, L285 and L287. "The pattern moves as one ring does" → "Each ring runs outward as if it were alone: a crest of ring i keeps
   kr_i − ωt fixed …". After the readout sentence, two sentences: this is the speed of each ring; where two rings cross at an angle
   the crests of their sum slide along faster, like the crossing point of a closing pair of scissors; straight up the middle between
   the two Reset sources, at the centre of a wide screen, they climb at 1.55 v = 51 px/s and lie 46 px apart.
   Measure: in Chromium, Reset, pause, read the stored C and S maps at the centre cell, crest speed = ω/|∇ arg U|; and follow one
   crest of the stored ψ up the column next to x = 400 px while the page plays.
2. §6, L308. "The damping factors are then all the same, and …" → "Set the damping aside for the moment, γ = 0: all the arrows in (7)
   are then equally long, and …", plus one parenthesis: with damping the nearer sources' arrows are a little longer; that moves no
   beam, and at the default γ it changes (12) by at most 0.03.
   Measure: in Chromium, Line of 16 at λ = 30 px, the exact sum from the stored x_s, y_s, k, g at 10⁶ px, normalised by the sum of
   the arrow lengths, against (12), every 0.1° from −90° to 90°.
3. §10.1, L487–L490. Link each title to a page I opened (Pearson, archive.org lending copy of Crawford, Wiley, Cambridge Core), house
   style `<a href><em>Title</em></a>` as in the other notes. Add Feynman Vol. I ch. 29–30 (Caltech's online edition), on the same line
   as the Born and Wolf item so no line moves.
4. Doc: page byte count; "four references" → five, linked.

No new section, figure, box or equation. Equation numbers untouched.

## Done and measured (20 October 2026)

- Build `APPDEPLOY_VITE_OUT_DIR=/tmp/fig01-dist npm run build`, served by `serve.cjs`, Chromium 1194 headless.
- `measure.cjs` → `measure-out.json`: grids 360 × 162 (1280–1600 px), 360 × 360 (880 px), 324 × 324 (390 px); worldH 360.519,
  y_s 350.519, centre row y 181.372 on 1280/1440. Crest speed at the centre cell after Reset, from the stored C and S:
  ω/|∇ arg U| = 51.10 px/s = 1.5486 v, local wavelength 46.46 px; following one crest of the stored ψ up the column at x = 398.9 px
  while playing: 1.60, 1.50, 1.43 v as it climbs through y ≈ 190, 172, 155 px (r/h falls with height; 1.55 at the centre row).
  Far field of Line of 16 from the stored x_s, y_s, k, g at 10⁶ px: (12) against the exact sum, γ = 0: 2.2 × 10⁻³ (as the eqnote);
  with the page's damping, normalised by the sum of arrow lengths: 0.031 at γ = 0.15 (0.149 at γ = 0.6). Rebuild for Line of 16:
  1 866 240 cos + sin, 32–57 ms here; frame 0.9–2.0 ms.
- `check.py` → `check-out.txt`: every other number of the note recomputed from the page's formulas in float64 (all agree).
- `render-check.cjs`: 1440 × 900 and 390 × 844, no console or page errors, 0 `.katex-error`, 304 KaTeX nodes, no raw delimiters,
  no sideways scroll, 14 of 14 folds open, 5 references with 6 links; each fold also closed and reopened by its own toggle.
- Page still 907 lines; changed lines L285, L287, L308, L487–L490 only. Sources opened: Pearson page (contents: ch. 4, 7, 9, 10),
  archive.org lending copy of Crawford (full-text search: Chapter 9 Interference and Diffraction p. 451, 9.6 Diffraction and
  Huygens' Principle p. 478), Wiley page (contents: ch. 6 Arrays), Cambridge Core page (contents: VIII Elements of the theory of
  diffraction), Feynman Vol. I ch. 29 and 30 (read through Firecrawl; the site refuses WebFetch and curl with 403). Hecht 5th ed.
  section 4.4.2 was not in the opened page; the 3rd edition scan at archive.org has "4.4.2 Huygens's Principle" in chapter 4.

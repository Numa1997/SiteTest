# Fig. 8 · Draw & Decompose · plan for the lecture note

Page `public/simulations/draw-decompose.html`, note L136–608. Judged against notes/STANDARD.md §4, under "Numa's verdicts":
judge first, touch only what needs it, smallest change. Every number in the note was re-measured before judging (scripts in
this folder; results in `measure-out.json`, `analyse-out.json`, `analyse2-out.json`, `overshoot-out.json`).

## Verdicts

| § | Section | Verdict |
|---|---|---|
| Abstract, contents | | clear, leave it |
| 1 | A drawing made of circles | clear, leave it. Picture first (online animations, equaliser, JPEG/MP3, bead on a wire, Ptolemy); Figure 1 caption checked: k = 1, −2, 4 are all 1 mod 3, so z(t + 2π/3) = e^{2πi/3} z(t). |
| 2 | The model | needs work, one pointer: "its resampling repeats the endpoint, so the equivalence is not exact" uses the repeated start point before anything explains it (that is section 7.1). The rest is clear. |
| 3 | Each circle is an average | clear, leave it. |
| 4 ★ | From an integral to 256 samples | needs work, one step: in 4.1, "So keeping all N coefficients … reproduces every sample exactly, z_n = Σ c_k e^{2πikn/N}" is asserted. It is the inverse DFT, and Parseval (8) is built on it. The missing step is one line: put (4) in for c_k, and the sum over the N frequencies is the geometric series (5) again with k and n swapped. 4.2 and 4.3 are clear; their numbers check (see below). |
| 5 | Parseval's theorem and the error | needs work, one phrase, in the Figure 3 caption: "Beyond K ≈ 80 both curves flatten near 10⁻³ because all the computed circles are in use". At K = 80 only 80 of the 120 are in use. Measured: for the heart, half of e_K² at K = 80 (2.6 × 10⁻⁷ of 5.0 × 10⁻⁷) is in computed circles not yet used, and going from K = 80 to K = 120 lowers the error only from 9.9 × 10⁻⁴ to 6.8 × 10⁻⁴. For the square the circles left after K ≈ 95 are numerically zero (about 10⁻¹⁶). So the curves flatten because the circles still to be added are tiny. Text, box and Exercise 5.1 are clear; numbers check. |
| 6 ★ | Corners cost circles | needs work, two items. (a) 6.1: "For k = 1 − 4m the four terms of (12) point the same way and add; for every other k they cancel" gives the result without the reason. Missing: the corners sit at t_j = jπ/2 and each jump is the one before turned by a right angle, Δż_j = i^j Δż_0, so term j is Δż_0 (i e^{−ikπ/2})^j. (b) 6.1, figure eight: "1.2 × 10⁻⁶ at 40" should be 1.3 × 10⁻⁶: measured 1.2605 × 10⁻⁶ two ways (exact curve by quadrature; page dft() on 65 536 samples at spacing L/N). Eqs. (11)–(13) were checked by hand (signs, factors); the rest is clear. |
| 7 | What the page computes | clear, leave it. Steps match `resamp()`, `decompose()`, `dft()`, `rebuild()`, the clock (dt capped at 0.05 s in `Sim.clock`, sim.js L178); 7.1 numbers check. |
| 8 | From units to pixels | clear, leave it. 0.46, 0.006, R and the 256-instant scan, eq. (16), 0.4 s, 1×–63×, 24 segments with opacity 0.12 + 0.88 (c+1)/24 from 0.157 to 1, colours: all match the code. |
| 9 | What the model leaves out | list clear, leave it. |
| 9.1 | Further reading | needs work: none of the four references has a link. Opened: Boas, Wiley page (chapter list) and the CERN library copy of the 3rd-edition contents (ch. 7 §11 "Parseval's Theorem"); Kreyszig, Wiley page of the 10th edition (ch. 11 "Fourier Analysis"); Stein & Shakarchi, Princeton University Press page (ch. 2, 3, 7 as cited; curl got 403, opened with WebFetch); Numerical Recipes, numerical.recipes/book.html (the 3rd edition free to read online; ch. 12 "Fast Fourier Transform", ch. 13 "Fourier and Spectral Applications"). Chapter numbers in the note are right. |

## Changes (in place, on the same lines, so no line number of the page moves and the doc's links stay valid)

1. §2 (L216): add "(section 7.1)" after "its resampling repeats the endpoint".
2. §4.1 (L309): after the inverse-DFT formula, one sentence: put (4) in for c_k; the sum over the N frequencies is the
   geometric series (5) again with k and n trading places; it vanishes for every sample but z_n itself.
3. §5, Figure 3 caption (L379): "because all the computed circles are in use" → the circles still left to add are tiny,
   and what is missing lies beyond |k| = 60, where the page computes nothing.
4. §6.1 (L489): replace "For k = 1 − 4m the four terms of (12) point the same way and add; for every other k they cancel."
   by the reason (t_j = jπ/2, Δż_j = i^j Δż_0, ratio i e^{−ikπ/2}, which is 1 for k = 1 − 4m and −1 or ±i otherwise, so the
   four terms add or close up like the arrows of (5)). Inline maths only; no new display equation, no renumbering.
5. §6.1 (L492): 1.2 × 10⁻⁶ → 1.3 × 10⁻⁶.
6. §9.1 (L597–600): link each title to the page opened. Numerical Recipes gets "(readable online)".

## Numbers re-measured (all agree with the note unless listed above)

Headless Chromium 1440 × 900, the page's own store `Sim.data.ds` after clicking presets and moving the K slider
(`measure.cjs`): heart ⟨|z|²⟩ = 0.515044672459522, e_24 = 0.005405966670666 (errP 0.005405966670687), readouts 99.99 %,
0.00541; K = 1: 94.30 %, k = −1, relative error 23.9 %; relative error 2.87 % (K = 10), 0.753 % (24), 0.234 % (50), 0.0685 %
(120); worst |err − errP|/err over K = 1…120: 2.2 × 10⁻¹⁰ (at K = 119), inside "3 parts in 10¹⁰"; k²|c_k| = 0.550, 0.552,
0.544 (k = 10, 20, 30). Square: ⟨|z|²⟩ = 0.6546, K = 1 readouts 98.52 % and 0.09831; first four ranks k = 1, −3, 5, −7;
radii 0.803, 0.0903, 0.0317 (k = 1, −3, 5), 2.47 × 10⁻³ (k = 2 and −1). Open wave: 10|c_10| = 0.271; relative error 20.5 %,
14.2 %, 8.41 % (K = 24, 50, 120). Figure eight: Δs = 0.02032, |c_60| = 5.90 × 10⁻⁵ (estimate Δs/(2π·60) = 5.39 × 10⁻⁵),
relative error at K = 120: 8.41 × 10⁻⁴. Timing: dft() alone median 1.0 ms; one decomposition (preset click) 7–9 ms on the
first click after load, 3–6 ms after (`timing.cjs`), so "about 1 ms" and "about 8 ms" stand.

Page code run in Node (functions extracted verbatim from the page by `pagecode.cjs`): aliasing alone (both transforms
sampled at spacing L/N) changes the heart's three largest radii by 7 × 10⁻⁷, 2.9 × 10⁻⁴, 5 × 10⁻⁶, under 0.1 %; near
|k| = 60 by 17–21 % (heart, even k) and 8–10 % (open wave). Periodic sampling (no repeated start point): figure eight
relative error at K = 120 = 1.48 × 10⁻⁶; square radii within 0.13 % of (14). Figure eight from the exact curve: 0.397,
5.82 × 10⁻⁴, 8.08 × 10⁻⁵, 1.03 × 10⁻⁵, 1.26 × 10⁻⁶ (k = 1, 10, 20, 30, 40). Corners and overshoot (`overshoot.cjs`, at the
page's 601 points and at 60 001): square K = 10 passes 0.019–0.022 inside the corners and crosses a side by 0.0104;
K = 50 by 0.0038; open wave overshoot 5.86 %, 7.93 %, 9.52 % of 1.7 at K = 24, 50, 120 (0.162 units).

## Doc

`docs/simulations/fig08-draw-decompose.md`: only the byte count of the page changes; no line moves.

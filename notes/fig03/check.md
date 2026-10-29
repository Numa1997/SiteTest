# Figure 3 · derivation check of the lecture note

Page: `public/simulations/Interactive Double-Slit Experiment Visualization.html`, the note between
`<article class="paper" id="paper">` and `</article>` (lines 129–536), state of the working tree on 20 October 2026,
including the uncommitted edit shown by `git diff HEAD` (Section 5 cross-term sentence, the θ/α sentence in the box after (8),
the closing-one-slit sentence in Section 7, the polarisation bullet in Section 10, and the reference links).

How it was checked

- Build: `OUT_DIR=/tmp/fig03-check-dist npm run build`; the built page is byte-identical to the source file.
  Served by a small Node static server on localhost; loaded in headless Chromium
  (`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, Playwright from `npm root -g`). No console errors; KaTeX rendered 354
  formulas, 0 `.katex-error`, tags (1)…(13) in order.
- Numbers from the page's own code, three roads: (a) the page's store `Sim.data.ds` after moving the real sliders with
  `input` events; (b) the visible readouts and SVG attributes; (c) for values the 0.5° slider cannot reach (fringe positions,
  the dark fringe of Section 10, the full slider sweep, the Figure 2 curve) the page's own `compute()` source, extracted verbatim from
  the inline script and run in the same Chromium with stub sliders.
- Equations: re-derived in SymPy 1.14 (identities, series, integrals, limits, units with `sympy.physics.units`).
- Static figures 2, 4, 5: every path point parsed from the SVG and compared with the formula; Figure 5 regenerated exactly
  (see N50).
- Links: curl first; where curl got 403, the response was Cloudflare's "Attention Required" bot page (Feynman) or a
  publisher block (Royal Society), not a dead link, so the second road was Firecrawl scrape, which returned HTTP 200 and the page.

Verdicts: "verified", "wrong, because …", "unverifiable, because …". A "remark" inside a verified row is a wording
point that does not make the statement false.

## 1. Numbered equations

| # | Equation in the note | Re-derivation (SymPy), units, limits | Verdict |
|---|---|---|---|
| (1) | S₁ = (−b/2, 0), S₂ = (b/2, 0), P = (−d tan α, d) = (−r sin α, r cos α), r = d/cos α | Identity checked symbolically. Units: lengths. Limit α = 0: P = (0, d), r = d. Matches the code `P = {x: X0 − d·tan(a), y: Y0 − d}` (y flipped, shifted). | verified |
| (2) | L₁,₂ = √((d tan α ∓ b/2)² + d²) | |P − S₁|², |P − S₂|² from (1) equal the stated forms. Limits: b → 0 gives L₁ = L₂ = r; α = 0 gives L₁ = L₂. | verified |
| (3) | δs = (L₂² − L₁²)/(L₁ + L₂) = 2bd tan α/(L₁ + L₂) | `expand(L2² − L1² − 2bd tan α) = 0`; (L₂ − L₁) − (L₂² − L₁²)/(L₁+L₂) = 0. Units: length. Limits: α → 0: 0; b → 0: 0; d → 0: 0 (caption of Fig. 2); d → ∞: b sin α. | verified |
| (4) | δs ≈ 2bd tan α cos α/(2d) = b sin α | Identity exact once L₁ + L₂ = 2r. Limit α = 0: 0; small α: bα. | verified |
| (5) | δs = b sin α [1 − b² cos² α/(8r²) + O(b⁴/r⁴)] | `series(L2 − L1, b, 0, 5)` with L₁,₂² = r² ∓ br sin α + b²/4 equals b sin α − b³ sin α cos² α/(8r²) exactly. Next term: + b⁵ sin α cos² α (7 cos² α − 4)/(128 r⁴), so the bracket's remainder is indeed O(b⁴/r⁴). Limits: r → ∞ gives (4); α = 90°: exact δs = b for r > b/2 and the correction vanishes, consistent. | verified |
| (6) | E = 2E₀ cos(Δφ/2) cos(kL̄ − ωt), Δφ = kδs = 2πδs/λ | Sum-to-product identity checked (difference expands to 0). Units: Δφ dimensionless. Limits: Δφ = 0 gives 2E₀cos(kL − ωt); Δφ = π gives 0. | verified |
| (7) | ⟨E²⟩ = 2E₀² cos²(Δφ/2), I/I₀ = cos²(πδs/λ) | Time average over one period integrated symbolically: 2E₀² cos²(Δφ/2). One slit: E₀²/2, so I₀ is 4×, as stated. Limits: δs = 0 → 1, δs = λ/2 → 0. | verified |
| (8) | δs = mλ bright, δs = (m + ½)λ dark | cos²(πm) = 1, cos²(π(m + ½)) = 0 for integer m. | verified |
| (9) | Δy = λD/b | y_m = D tan(asin(mλ/b)) = mλD/b + m³λ³D/(2b³) + …; leading term gives (9). Units: length. HeNe example correction (mλ/b)²/2 ≈ 3×10⁻⁶. | verified |
| (10) | ∫ e^{−ikx′ sin θ} dx′ over (−w/2, w/2) = w sin β/β, β = πw sin θ/λ | Integral done symbolically, equal after k = 2π/λ. Limits: θ → 0 gives w; w → 0 gives the point source. Remark: with P on the S₁ side (Section 2) a source at +x′ is farther, so "shorter by x′ sin θ" holds for θ counted towards +x; the sign drops out of the symmetric integral. | verified |
| (11) | I/I₀ = cos²(πb sin θ/λ)(sin β/β)² | |E|² of two slits each carrying (10), normalised at θ = 0, equals the product (SymPy, real form). Limit w → 0 gives (7) in the far field. | verified |
| (12) | p(θ)dθ ∝ cos²(πb sin θ/λ) dθ | Far-field (7) used as probability density; normalisable on (−30°, 30°). Used for N50–N51. | verified |
| (13) | λ = h/√(2mₑeV); V = 100 V: λ = 0.123 nm | CODATA 2018: 0.122643 nm (relativistic correction 0.122637 nm, negligible at 100 eV ≪ 511 keV). Units via `sympy.physics.units`: 0.12264 nm. | verified |

## 2. Unnumbered derivations in the text

| # | Statement | Check | Verdict |
|---|---|---|---|
| D1 | (changed line, §5) 2cos²(Δφ/2) = 1 + cos Δφ, so ⟨E²⟩ = E₀² + E₀² cos Δφ: sum of intensities (½E₀² + ½E₀²) plus a cross term | Identity verified in SymPy; 2E₀²cos²(Δφ/2) = E₀²(1 + cos Δφ). | verified |
| D2 | |1 + e^{iΔφ}|² = 2 + 2 cos Δφ = 4 cos²(Δφ/2), "the same result" | Both identities verified; with ⟨E²⟩ = ½|Ẽ|² it reproduces (7). | verified |
| D3 | §4.1: L₁,₂² = r² ∓ br sin α + b²/4 | From (1), verified. | verified |
| D4 | §4.1: √(1+u) = 1 + u/2 − u²/8 + u³/16 − …; odd part to third order r(ε − ½εβ + ⅛ε³) | Series verified; odd part computed with ε ~ O(1), β ~ O(2) bookkeeping: r(ε − εβ/2 + ε³/8). | verified |
| D5 | §5: I₀ is four times one slit (2E₀² vs ½E₀²); averaged over a fringe two slits give twice one | ⟨2E₀²cos²(Δφ/2)⟩ over Δφ = E₀² = 2 × ½E₀². | verified |
| D6 | §7: dy = D sec²θ dθ, density per length p(θ)/(D sec²θ) | d(D tan θ)/dθ = D/cos²θ verified. | verified |
| D7 | (changed line, §10) two equal fields in opposite phase tilted by γ leave 2E₀ sin(γ/2); dark fringe keeps sin²(γ/2) of I₀; γ → 0 far away | |ê₁ − ê₂|² = 4 sin²(γ/2) verified. Exact angle: (P − S₁) × (P − S₂) = bd, so sin γ = bd/(L₁L₂); series in b gives γ ≈ b cos α/r → 0 as r → ∞. Measured against the peak with tilted fields the ratio would be tan²(γ/2); both round to 0.9 %. | verified |

## 3. Numbers in the note

Defaults: d = 200 px, α = 20°, b = 40 px, λ = 13.5 px. "Store" means `Sim.data.ds` after the sliders were moved in Chromium;
"compute()" means the page's own function run with stub sliders.

### Section 1

| # | Claim | Recomputed | Verdict |
|---|---|---|---|
| N1 | Sound at 20 °C ≈ 343 m/s | 331.3·√(1 + 20/273.15) = 343.2 m/s | verified |
| N2 | 343 Hz has a wavelength of 1 m | 343/343 = 1.00 m | verified |
| N3 | Light: "more than a million times finer" | 1 m / (0.4–0.7 µm) = 1.4–2.5 × 10⁶ | verified |
| N4 | CD tracks 1.6 µm apart | Standard CD track pitch 1.6 µm (Red Book / IEC 60908 value) | verified |
| N5 | Young argued in lectures to the Royal Society between 1801 and 1803 | Bakerian Lecture "On the theory of light and colours", Phil. Trans. 92 (1802) 12–48 (DOI 10.1098/rstl.1802.0004, opened via Firecrawl); Bakerian Lecture read 24 Nov 1803 (primary source, R6) | verified |
| N6 | Slip of card about 0.85 mm wide | Young, Exper. 1: "about one-thirtieth of an inch in breadth" = 0.847 mm (PDF read) | verified |
| N7 | Middle of the shadow always bright; blocking one edge removed the bands | Young: "leaving the middle of the shadow always white"; with a screen at one edge "all the fringes … immediately disappeared" (PDF read) | verified |

### Section 2

| # | Claim | Recomputed | Verdict |
|---|---|---|---|
| N8 | Sliders: d 100–300 px, b 20–80 px, λ 8–40 px, α 0°–30° | `<input>` attributes: d 100–300 step 1, b 20–80 step 1, λ 8–40 step 0.5, α 0–30 step 0.5 | verified |
| N9 | "as on the page, we take P on the side of S₁" | code: P.x = 300 − d tan α, S₁.x = 300 − b/2; default P drawn at (227.21, 170.00), S₁ at 280 | verified |

### Section 3

| # | Claim | Recomputed | Verdict |
|---|---|---|---|
| N10 | L₁ = 206.85 px | store L1 = 206.850698 | verified |
| N11 | L₂ = 220.48 px | store L2 = 220.478423 | verified |
| N12 | δs = 13.6277 px | store ds = 13.6277250 | verified |
| N13 | Readouts show these rounded | readouts "206.9 px", "220.5 px", "13.63 px" | verified |
| N14 | (3) and L₂ − L₁ differ by at most 1.4 × 10⁻¹³ px over every slider combination | compute() over all 201 × 61 × 61 = 747 921 (d, α, b): max 1.350 × 10⁻¹³ px at d = 298, α = 14°, b = 29 | verified |
| N15 | (3) has an exact zero at α = 0 | α = 0 on the page: ds = 0 exactly (and ds_direct = 0) | verified |

### Section 4 and Figure 2

| # | Claim | Recomputed | Verdict |
|---|---|---|---|
| N16 | Shortcut b sin α = 13.6808 px | store b_sin_a = 13.6808057 | verified |
| N17 | 0.39 % more than exact | (13.6808057 − 13.6277250)/13.6277250 = 0.3895 % | verified |
| N18 | Corrected form (5) gives 13.6275 px | 13.6274692 | verified |
| N19 | Error of the shortcut 0.0039 λ | 0.0530807/13.5 = 0.00393 | verified |
| N20 | Shortcut "always a little too long" | L₁ + L₂ > 2r (median of triangle S₁PS₂, strict for α < 90°), so δs < b sin α; no counterexample in the sweep of N14 | verified |
| N21 | Fig. 2 computed at every whole pixel of d, 0–300 px | SVG: 301 points; solid curve vs compute() max deviation 0.05 SVG units, dashed b sin α 0.014 units (both = rounding to 0.1) | verified |
| N22 | Dotted correction (5) drawn from d = 25 px | first point x = 116.8 → d = 24.98; 276 points; matches (5) within 0.05 units | verified |
| N23 | Shortcut within 1 % of exact beyond d = 125 px | relative error 1.012 % at d = 124, 0.996 % at d = 125 (relative to b sin α the switch is also between 124 and 125) | verified |
| N24 | About 3.3 slit separations from M | r = 125/cos 20° = 133.0 px = 3.33 b | verified |
| N25 | Still 1.6 % too long at d = 100 px | 1.554 % | verified |
| N26 | Fig. 2 label: b sin α = 13.68 px; corrected curve close to exact beyond about 40 px | 13.68; (5) vs exact: −1.2 % at d = 40, −0.48 % at 50, −0.23 % at 60 | verified |
| N27 | Ex. 4.1: δs exact = 38.27 px (b = 80, d = 100, α = 30°) | sliders moved; store 38.268470, readout "38.27 px" | verified |
| N28 | Ex. 4.1: b sin α = 40.00 px | readout "40.00 px" | verified |
| N29 | Ex. 4.1: shortcut 4.5 % too long | 1.73153/38.26847 = 4.52 % | verified |
| N30 | Ex. 4.1: at d = 300, exact 39.80 px | store 39.800835, readout "39.80 px" | verified |
| N31 | Ex. 4.1: error falls from 1.73 px to 0.20 px | 1.731530 → 0.199165 | verified |
| N32 | Ex. 4.1: an 8.7-fold drop | 1.731530/0.199165 = 8.694 | verified |
| N33 | Ex. 4.1: (5) predicts nine-fold; the difference is the b⁴/r⁴ terms; b/r = 0.69 | (5) error ∝ r⁻² → 9; b/r = 80/115.47 = 0.6928; the next term of the series (row (5)) moves (5)'s 1.80 px to 1.73 px at d = 100 | verified |

### Section 5, Figure 3 and Exercise 5.1

| # | Claim | Recomputed | Verdict |
|---|---|---|---|
| N34 | Light oscillates about 5 × 10¹⁴ times a second | c/600 nm = 5.0 × 10¹⁴ Hz | verified |
| N35 | HeNe 633 nm, b = 0.25 mm, D = 1 m: Δy = 2.53 mm | 2.532 mm | verified |
| N36 | At the defaults λd/b = 67.5 px | store fringe_px = 67.5 | verified |
| N37 | Fig. 3 arrows: in step 2E₀; 2π/3 apart E₀ and a quarter of the peak; π apart 0 | SVG: arrows of 80 units; sum 160; second arrow at 120.0°, sum length 80.0 (¼ of peak intensity); at π the sum is a dot | verified |
| N38 | Ex. 5.1: between 9.5° and 10.0° readout 0.49 → 0.51, verdict Destructive | slider steps on the page: 9.5° "0.49" Destructive, 10.0° "0.51" Destructive (Destructive from 8.5° to 11.0°) | verified |
| N39 | Ex. 5.1: between 19.5° and 20.0° readout 0.99 → 1.01, verdict "Constructive · bright fringe, m = 1" | 19.5° "0.99", 20.0° "1.01", both "Constructive · bright fringe, m = 1" | verified |
| N40 | Far field puts these fringes at 9.72° and 19.72° | asin(λ/2b) = 9.7151°, asin(λ/b) = 19.7246° (store m_theta[1] = 19.72463) | verified |
| N41 | Exact δs at d = 200 puts them at 9.76° and 19.81° | compute() bisection: 9.7613°, 19.8051° | verified |
| N42 | At d = 100 the bright fringe moves to 20.04° | compute() bisection: 20.0438° | verified |

### Section 6 and Figure 4

| # | Claim | Recomputed | Verdict |
|---|---|---|---|
| N43 | w = 20 px: λ/w = 0.675 = 2λ/b, at θ = 42.45° | 0.675, 0.675, asin 0.675 = 42.454° | verified |
| N44 | Page draws each slit as an 8 px gap | wall segments in the live SVG end at 276 and restart at 284 (S₁ = 280); code `gap = 4` each side | verified |
| N45 | 8 px gap: envelope 0.74 at 30°, 0.26 at 90°, first fringe 1 → 0.88 | 0.7426, 0.2648, 0.8751 | verified |
| N46 | 8 px gap narrower than λ has no envelope zero | zero needs sin θ = λ/w = 1.69 > 1 | verified |
| N47 | Fig. 4 computed every 0.2° from 0° to 90° | 451 points per curve; point slits, 20 px slits and envelope match (7), (11) and (sin β/β)² within 0.06 SVG units (rounding) | verified |
| N48 | First bright fringe 19.72° cut to 0.41 | β = π/2 there, (2/π)² = 0.4053 | verified |
| N49 | Faint line at 30°; "m = 2 missing" at 42.45° | line x = 275.3 = 64 + 30·634/90; label x = 363.0 → 42.44° | verified |

### Section 7 and Figure 5

| # | Claim | Recomputed | Verdict |
|---|---|---|---|
| N50 | 2000 dots: 140 within 1° of the centre, 3 within 1° of ±9.72° | Regenerated: `numpy.random.default_rng(1)`, one draw at a time θ = uniform(−30, 30), accept if random() < (12); after each strip y = top + 4 + 56·random(n). Reproduces all 2220 SVG dots (max |Δθ| 0.005°, the SVG rounding). Unrounded counts: 140 and 3. (From the SVG alone 139–141, two dots lie at ±1.00° after rounding.) | verified |
| N51 | Rule (12) expects 131 and 2.2 | 2000 × ∫ p over |θ| < 1° = 130.9; over |θ ∓ 9.715°| < 1° = 2.25 | verified |
| N52 | Fig. 5: 20, 200, 2000 dots, rejection sampling, NumPy generator, seed 1 | strip counts 20/200/2000; generator reproduced (N50) | verified |
| N53 | Bright bands at 0° and ±19.72°, dark at ±9.72° | far-field values as N40 | verified |
| N54 | Per unit length smaller than straight ahead by a factor 3/4 at 30° | cos²30° = 3/4 | verified |
| N55 | (changed line) Close one slit → one single-slit pattern; which-path detector → sum of two; no fringes; cross term gone | One open slit: only |ψ₁|², no cross term; detector: |ψ₁|² + |ψ₂|². Both correct (for the page's point slits the single-slit pattern is flat). Matches Feynman III-1 (R5) | verified |
| N56 | h = 6.626 × 10⁻³⁴ J s | 6.62607015 × 10⁻³⁴ | verified |
| N57 | de Broglie proposed λ = h/p in 1924 | 1924 thesis | verified |
| N58 | 100 V electrons: 0.123 nm | 0.12264 nm (row (13)) | verified |
| N59 | About 4500 times shorter than 550 nm | 550/0.12264 = 4485 | verified |
| N60 | Electrons, neutrons, atoms and C₆₀ molecules show the fringes | standard record (electron double slit 1961, neutrons 1988, atoms 1991, C₆₀ 1999) | verified |

### Section 8 (method) and Section 9 (drawing)

| # | Claim | Recomputed | Verdict |
|---|---|---|---|
| N61 | Verdict tolerance 0.08: Constructive covers 0.94–1, Destructive 0–0.06 | cos²(0.08π) = 0.938, sin²(0.08π) = 0.062 | verified |
| N62 | Plot samples 301 directions, one every 0.1° | store theta: 301 values, step 0.1° | verified |
| N63 | Finest fringes (b = 80, λ = 8): one fringe spans 57 samples | page at b = 80, λ = 8: far-field maxima at samples 0, 57, 115, 175, 236, 300; smallest spacing 57 (asin 0.1 = 5.739°) | verified |
| N64 | Double precision, about 16 significant digits | 53-bit mantissa = 15.95 digits | verified |
| N65 | Phase advances 0.8 Δt periods per frame | code line 811; measured 1.653 periods in 2.067 s of clock time = 0.800/s. Remark: `sim.js` line 179 caps Δt at 0.05 s, so below 20 frames per second the wavelets run slower than stated | verified |
| N66 | Store holds L₂ − L₁ and the bar length S₂Q, "at the line that computes it" | store ds_direct = 13.627724988366339, S2Q = 13.627724988366323 vs ds = …344. Remark: the five points and S2Q are written in `storeDerived()`, called at the end of `compute()`, from the same variables (no recomputation); S2Q is |Q − S₂| from unrounded points, the drawn bar carries 2 decimals (13.6278) | verified |
| N67 | Figure 600 × 440 units; positions to two decimals | viewBox 0 0 600 440; `n(v) = v.toFixed(2)`; e.g. Q at (314.26, 357.64) | verified |
| N68 | Wall at y = 370, midpoint x = 300; P at (300 − d tan α, 370 − d) | X0 = 300, Y0 = 370; default P drawn at (227.21, 170.00) = (300 − 200 tan 20°, 170) | verified |
| N69 | Wall 5 units thick, 8-unit gap per slit | stroke-width 5; gaps 276–284, 316–324 | verified |
| N70 | Arc and bar only when δs > 0.05 px; α arc only when α > 0.2° | code lines 651, 657, 677; at α = 0 no paths drawn, at α = 0.5° (δs = 0.347) both arcs drawn | verified |
| N71 | Wavelets r_n = (n + φ)λ to 430 px, opacity 0.55(1 − r/430) | live: phase 0.50656, first r = 6.8386 = 0.50656 × 13.5, step 13.5; opacity "0.541" = 0.55(1 − 6.84/430) | verified |
| N72 | Plane wave and arcs move at 0.8λ per second = 10.8 px/s | store ring_speed 10.8; plane lines at y = 370 + (1 − φ)λ + nλ (376.66, 390.16, …) | verified |
| N73 | Green light 5.5 × 10¹⁴ Hz | c/550 nm = 5.45 × 10¹⁴ | verified |
| N74 | Animation slowed by about 7 × 10¹⁴ | 5.45 × 10¹⁴/0.8 = 6.8 × 10¹⁴ | verified |
| N75 | b = 40 px, λ = 13.5 px: 2.96 wavelengths | 2.963 | verified |
| N76 | For 633 nm: slits 1.88 µm apart | 2.963 × 0.633 = 1.876 µm | verified |
| N77 | 0.25 mm = 395 wavelengths | 394.9 | verified |
| N78 | First bright fringe 0.145° from the centre | asin(633 nm/0.25 mm) = 0.1451° | verified |
| N79 | Plot: θ over 500 units, I/I₀ over 118 units; dot at the exact intensity at α; m labels at far-field directions | x0 = 56, x1 = 556, yb = 142, yt = 24; dot cy = 24.10 → 0.99915 vs store I = 0.99912; "m = 1" at x = 384.74 = X(19.7246°) | verified |

### Section 10

| # | Claim | Recomputed | Verdict |
|---|---|---|---|
| N80 | Dark fringe at the defaults: L₁ = 200.52 px, L₂ = 207.27 px | compute() at α = 9.7613° (δs = λ/2 = 6.75): L₁ = 200.5182, L₂ = 207.2682 | verified |
| N81 | Amplitudes (1/√L) differ by 1.6 % | 1 − √(L₁/L₂) = 1.64 % (other way round 1.67 %) | verified |
| N82 | Dark fringe keeps 7 × 10⁻⁵ of the peak | ((1 − q)/(1 + q))², q = √(L₁/L₂): 6.85 × 10⁻⁵ | verified |
| N83 | (changed line) Angle γ between the two paths at that dark fringe: 11° | compute() points: angle S₁PS₂ = 11.098° (sin γ = bd/(L₁L₂) = 0.19249; small-angle b cos α/r = 11.13°). At α = 20° it would be 10.10°, so the value is for the dark fringe as stated | verified |
| N84 | (changed line) Remainder keeps sin²(γ/2) = 0.9 % of I₀ | sin²(5.549°) = 0.935 % → 0.9 % (tan²(γ/2) = 0.944 % if referred to the tilted peak) | verified |
| N85 | (changed line) Light polarised along the slits: nothing changes; far away γ → 0 | both fields along the slit axis, parallel: scalar sum exact; γ ≈ b cos α/r (D7): 22.0° at d = 100, 11.1° at 200, 7.4° at 300 for the first dark fringe | verified |

## 4. Description of the numerical method against the code

| § | Note says | Code | Verdict |
|---|---|---|---|
| 8 | Slits and P placed by (1); L₁, L₂ distances; δs from (3), not as L₂ − L₁ | `compute()` lines 621–627: S₁, S₂ = X0 ∓ b/2; P = (X0 − d tan a, Y0 − d); `dist` = Math.hypot; `deltaS = 2*b*d*Math.tan(a)/(L1+L2)` | verified |
| 8 | Q = P + L₁û, û unit vector from P to S₂ | lines 628–629: `ux = (S2.x − P.x)/L2`, `Q = P + u·L1` | verified |
| 8 | Readouts: L₁, L₂, exact δs, b sin α, δs/λ, Δφ in units of π | `readouts()` lines 775–780 | verified |
| 8 | Verdict from fractional part f; Constructive f < 0.08 or f > 0.92; Destructive |f − ½| < 0.08; else Partial with I/I₀ from (7) | `storeDerived()` lines 757–760 | verified |
| 8 | Plot: 301 directions 0–30° every 0.1°; burgundy far-field cos²(πb sin θ/λ); dashed exact δs at x = d tan θ | `drawPattern()` lines 712–730 (accent #7a1f2b solid, ink dashed "5 4") | verified |
| 8 | Only the wavelets move; phase += 0.8Δt each frame; geometry and readouts unchanged | clock callback lines 809–815 calls only `drawWaves()`; remark on the Δt cap in N65 | verified |
| 8 | Data panel stores every number at the line that computes it, incl. L₂ − L₁ and S₂Q | see N66 | verified |
| 9 | Drawing geometry, two decimals, wall, gaps, thresholds, wavelets, plane wave | see N67–N72; lines 614, 642, 651, 657, 687–704 | verified |

## 5. References and links

| # | Reference | Link check (road) | Cited chapter/section | Verdict |
|---|---|---|---|---|
| R1 | Hecht, Optics, 5th ed., Pearson, 2017, ch. 9, 10 | curl: 200 | Pearson page TOC: "9: Interference 10: Diffraction"; page lists hardcover ISBN 9780133977226, © 2017 (published Sept 2016). Remark: the page's top offer is the 2021 Pearson+ eTextbook, © 2022 | verified |
| R2 | Halliday, Resnick, Walker, Fundamentals of Physics, 10th ed., Wiley, 2014, ch. 35, 36 | curl: 200 | Wiley page "Fundamentals of Physics, Extended, 10th Edition", ISBN 978-1-118-54787-8, July 2014; TOC "Chapter 35 Interference", "Chapter 36 Diffraction". Remark: the link is the Extended edition; chapter numbers are the same | verified |
| R3 | Feynman Lectures I, ch. 29 (interference) | curl: 403 = Cloudflare "Attention Required" bot page, not a dead link; Firecrawl: 200 | title "Vol. I Ch. 29: Interference" | verified |
| R4 | Feynman Lectures I, ch. 30 (diffraction) | curl 403 (Cloudflare); Firecrawl: 200 | title "Vol. I Ch. 30: Diffraction" | verified |
| R5 | Feynman Lectures III, ch. 1 (quantum behaviour) | curl 403 (Cloudflare); Firecrawl: 200 | title "Vol. III Ch. 1: Quantum Behavior"; content includes the which-way experiment that kills the interference | verified |
| R6 | Young, Bakerian Lecture, Phil. Trans. 94, 1–16 (1804), read 24 Nov 1803; Section I is the slip-of-card experiment | curl: DOI redirects to royalsocietypublishing.org, which answers 403 to curl; Firecrawl: 200 on the DOI and on the PDF | Page: "I. The Bakerian Lecture. Experiments and calculations relative to physical optics", (94): 1–16, 1804. PDF read: "Read November 24, 1803"; "I. Experimental demonstration of the general law of the interference of light", Exper. 1 is the slip of card | verified |

## Summary

Equations 13, derivations 7, numbers 85, method rows 8, references 6: 119 rows.

**119 verified / 0 wrong / 0 unverifiable.**

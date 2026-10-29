# Fig. 1 · derivation check

Page: `public/simulations/Circular Wave Interference Visualization.html`, the lecture note between
`<article class="paper" id="paper">` and `</article>` (lines 98–495). Branch `claude/physics-notes-rewrite-cwctkk`, HEAD `468c139`.
The file checked is byte-identical to HEAD (md5 `fad90877…`). Its changes against base `db1a24b` are the seven lines in
sections 4 and 6 and the reference list. Those lines got extra care.

How the check was made:

- **Build.** `OUT_DIR=/tmp/fig01-check-dist npm run build`. The built page is byte-identical to the source page,
  and `sim.js`, `dataset.js` and the style sheets in the build match `public/`.
- **Browser.** A Node static server of my own on 127.0.0.1. Playwright 1.56.1 from `npm root -g` (`/opt/node22/lib/node_modules`),
  Chromium `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, headless, file name URL-encoded. No page errors at any width.
  Numbers were read from the page's own store (`Sim.data.ds`) while the page ran. Where the note samples differently from the grid
  (1 px, 0.1°, far field), the sum (6) was recomputed in the page in float64, from the page's stored source positions and `y_s`.
- **Algebra.** SymPy 1.14 and mpmath for every numbered equation, with a SymPy dimension check (`sympy.physics.units`).
  numpy was used for the angle sweeps.
- **Scripts.** All in `/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/fig01/`:
  `lib.cjs` (server and browser), `grid.cjs`, `main.cjs`, `extra.cjs`, `residue.cjs` (browser), and `derive.py`, `units.py`,
  `hankel.py`, `damp12*.py`, `svgcheck.py` (Python).
- **Not read.** `notes/fig01/plan.md` and the other reports and scripts in `notes/fig01/`.

Default "wide screen" below means a 1440 × 900 window. There the canvas is 770 × 347 css px and the grid 360 × 162. The field
height is `worldH` = 360.519 px, the source line is at `y_s` = 350.519 px, and the centre cell is j = 81, i = 180, at
y = 181.372 px, h = 169.147 px above the sources.

## 1 · Numbered equations

| # | Equation | Re-derivation (SymPy) | Units | Limiting cases | Verdict |
|---|---|---|---|---|---|
| (1) | ψ_tt = v²(ψ_xx + ψ_yy) | Linear in ψ, so the sum of two solutions is a solution. ψ = Re[u(r)e^{−iωt}] with u = H₀⁽¹⁾(kr) satisfies it (via (3)). | s⁻² both sides | v → 0: no propagation | verified |
| (2) | r_i = √((x−x_i)² + (y−y_s)²) | Same as the code: page lines 641–644, `r = Math.sqrt(x*x + y2)` with x, y measured from the source | px | P on the source: r = 0 | verified |
| (3) | u'' + u'/r + k²u = 0, k = ω/v = 2π/λ | SymPy: ∇²u(√(x²+y²)) − (u'' + u'/r) = 0. Putting u e^{−iωt} into (1) gives u'' + u'/r + (ω/v)²u = 0. 2πf/(fλ) = 2π/λ. H₀⁽¹⁾(kr) put into the equation gives 0 (mpmath residual 6 × 10⁻¹⁷ at kr = 7.3). | px⁻² each term | k → 0: Laplace's equation | verified |
| (4) | H₀⁽¹⁾ ≈ √(2/πkr) e^{i(kr−π/4)}; ψ ≈ √(2/πkr) cos(kr − ωt − π/4) | mpmath: \|H₀/asymptote\| − 1 = 1.2 × 10⁻², 1.3 × 10⁻³, 1.3 × 10⁻⁴ at kr = 10, 100, 1000. SymPy: Re[√(2/πkr) e^{i(kr−π/4)} e^{−iωt}] − √(2/πkr) cos(kr−ωt−π/4) = 0. | kr, ωt dimensionless | kr → ∞: the error falls as 1/kr | verified |
| (5) | ψ_i = a_i cos(kr_i − ωt), a_i = e^{−γr_i/R}, R = 300 px | Same as the code: `g = damp.value / R` (line 628), `a = Math.exp(-g*r)*norm`, `ph = k*r` (line 645), R = 300 (line 512) | γr/R dimensionless | γ = 0: a = 1, no fall-off | verified |
| (6) | ψ = (1/N) Σ a_i cos(kr_i − ωt) | Same as the code: `norm = 1/max(1,N)` (629); C, S summed (647–648); ψ = C cos ωt + S sin ωt (664) = (1/N) Σ a cos(kr − ωt) by (18) | dimensionless | N = 1: one ring; \|ψ\| ≤ 1 because a ≤ 1 | verified |
| (7) | ψ = Re[U e^{−iωt}], U = (1/N) Σ a_i e^{ikr_i} = C + iS, A = \|U\| | SymPy: Re[a e^{ikr} e^{−iωt}] − a cos(kr − ωt) = 0. With C = A cos δ, S = A sin δ: C cos φ + S sin φ = A cos(φ − δ), so the amplitude is √(C²+S²). Code line 652 stores A = √(C²+S²). | dimensionless | all arrows aligned: A = mean a_i | verified |
| (8) | v = ω/k = fλ | SymPy: d/dt(kr − ωt) = 0 gives ṙ = ω/k. ω/k = 2πf/(2π/λ) = fλ. | px/s | — | verified |
| (9) | ψ = a cos(kΔr/2) cos(k r̄ − ωt) | SymPy: [a cos(kr₁−ωt) + a cos(kr₂−ωt)]/2 − a cos(k(r₂−r₁)/2) cos(k(r₁+r₂)/2 − ωt) = 0. The 1/N = 1/2 of (6) is included. | dimensionless | Δr = 0: ψ = a cos(k r̄ − ωt) | verified |
| (10) | Δr = (m + ½)λ | SymPy: kΔr/2 = (m+½)π gives Δr = λ(2m+1)/2. Maxima at Δr = mλ. | px | — | verified |
| (11) | r_n ≈ r₀ − n s sin θ | SymPy: r_n = r₀ − n s sin θ + n²s²cos²θ/(2r₀) + O(r₀⁻²). The neglected term is the curvature the eqnote names. | px | r₀ → ∞: exact | verified |
| (12) | (1/N)Σe^{−inβ} = (1/N)(1−e^{−iNβ})/(1−e^{−iβ}); \|F\| = \|sin(Nβ/2)/(N sin(β/2))\| | SymPy summation; the note's form minus SymPy's form = 0. \|1−e^{−iφ}\|² − 4sin²(φ/2) = 0. Numerically equal to 10⁻¹² for N = 1, 2, 5, 16. | dimensionless | β → 0: 1 (SymPy limit); N = 1: 1 | verified |
| (13) | sin θ_edge = ±λ/(Ns), sin θ_m = mλ/s | Nβ/2 = π gives sin θ = λ/(Ns). β = 2πm gives sin θ = mλ/s. | dimensionless | N → ∞: beam width → 0 | verified |
| (14) | sin θ₀ = vτ/s | SymPy: the phase k(r₀ − n s sin θ) − ω(t − nτ) has n-coefficient −ks sin θ + ωτ, which is 0 at sin θ = ωτ/(ks) = vτ/s. Beam towards larger n, the later sources. | dimensionless | τ = 0: θ₀ = 0 | verified |
| (15) | r ≫ D²/λ | SymPy: √(r² + (D/2)²) − r → D²/(8r). Requiring this ≪ λ gives r ≫ D²/(8λ); D²/λ is the conventional stricter form (antenna texts often use 2D²/λ). | px | D → 0: no condition | verified |
| (16) | r ≈ h + u²/(2h) | SymPy series of √(h²+u²) in u | px | u = 0: r = h | verified |
| (17) | U ≈ (√(λh)/D) e^{−γh/R} e^{i(kh+π/4)} | SymPy: ∫e^{iau²}du = (−1)^{1/4}√(π/a) = √(π/a)e^{iπ/4}. With a = k/2h, √(π/a) = √(λh). Damping taken at r ≈ h inside the Fresnel zone. | √(λh)/D dimensionless | With the true 1/√(kr) factor, √(λh)/√(kh) = λ/√(2π), independent of h, as the note says | verified |
| (18) | ψ = C cos ωt + S sin ωt | SymPy: cos(kr−ωt) − (cos kr cos ωt + sin kr sin ωt) = 0. Exact. | dimensionless | — | verified |
| (19) | c = c₀ + (c± − c₀)\|ψ\|^0.8 | Same as the code (lines 586–590): `mid + (end − mid)·|a|^0.8` with a = n/127.5 − 1, rounded. All 768 table entries match (19) at ψ = n/127.5 − 1. | 0–255 per channel | ψ = ±1: the end colours; ψ → 0: cream | verified |

## 2 · Numbers in the note

| # | Section | Claim | Recomputed (from the page, in headless Chromium unless stated) | Verdict |
|---|---|---|---|---|
| N1 | 1, 9 | up to 24 sources; the list keeps the newest 24 | 30 clicks leave N = 24, readout "24 (max)", first kept u = 0.209 (the 7th click) | verified |
| N2 | 1 | Huygens, *Treatise on Light*, 1690 | *Traité de la lumière*, Leiden, Pieter van der Aa, 1690 (first-edition listings found through Firecrawl search) | verified |
| N3 | 2 | the field is 800 px wide on every screen | `WORLD_W` = 800; dx·cols = 800 at every width tried | verified |
| N4 | 2 | height 360.5 px on a wide screen, canvas 770 × 347 css px | canvas 770 × 347 and worldH = 360.519 at 1200, 1280, 1366, 1440 and 1920 px windows. At 1500–1600 px the canvas is smaller (530 × 239 to 630 × 284) and worldH is 360.42–360.75; the grid is still 360 × 162. | verified |
| N5 | 2 | 800 px on a phone, where it is square | 390 px phone: canvas 356 × 356, worldH = 800; 880 px: 814 × 814, worldH = 800 | verified |
| N6 | 2 | sources 10 px above the bottom edge | y_s = worldH − 10 = 350.519 (stored) | verified |
| N7 | 2 | λ 16–64 px (30), f 0.2–2 Hz (1.1), γ 0–0.6 (0.15) | `<input>` min/max/value attributes and stored defaults λ = 30, f = 1.1, γ = 0.15 | verified |
| N8 | 2, 5 | Reset: x = 200 and 600 px, s = 400 px | stored x_s = [200, 600] | verified |
| N9 | 2, 6 | Line of 16: 64 to 736 px, x_n = 64 + 44.8n, s = 44.8, D = 672 | stored x_s = 64, 108.8, …, 736; spacing 44.8; D = 672 | verified |
| N10 | 3 | kr = 1 at r = λ/2π = 4.77 px (λ = 30) | 30/2π = 4.775 | verified |
| N11 | 3 | first correction to (4): 1/(8kr) rad, 0.01 rad two wavelengths from a source | mpmath: arg H₀⁽¹⁾(z) − (z − π/4) = −0.009915 at z = 4π; 1/(8·4π) = 0.00995 | verified |
| N12 | 3 | the first correction is a phase **lag** | wrong, because the sign is reversed: arg H₀⁽¹⁾(kr) = kr − π/4 − 1/(8kr) + …, so the exact phase is *smaller* than in (4) (mpmath: −0.0997, −0.0197, −0.0099 at kr = 1, 2π, 4π). With ψ ∝ cos(phase − ωt), the true wave reaches each phase 1/(8kr)/ω earlier, and its crests sit 1/(8k²r) further out. The correct statement is "a phase **lead** (advance) of 1/(8kr) rad". The size, 0.01 rad, is right. | wrong |
| N13 | 3 | a still smaller error in the height | mpmath: \|H₀\|/√(2/πkr) − 1 = −3.9 × 10⁻⁴ at kr = 4π | verified |
| N14 | 3 | e^{−0.15} = 0.861 after 300 px | 0.8607 | verified |
| N15 | 4 | \|ψ\| ≤ 1 | a ≤ 1 and the 1/N factor give \|U\| ≤ 1; the clip (line 665) never acts except through rounding | verified |
| N16 | 4 | Speed readout 1.1 Hz × 30 px = 33 px/s | stored v = 33; readout text "33 px/s"; at f = 1.5 it reads "45 px/s" | verified |
| N17 | 4 | T = 1/f = 0.909 s | stored T = 0.90909 | verified |
| N18 | 4 (changed) | up the middle between the Reset sources, centre of a wide screen: crests climb at 1.55 v = 51 px/s | On the bisector r = √(200² + h²) and the crest speed is v·r/h (SymPy: (ω/k)/(dr/dh)). At h = 169.147: r/h = 1.5486, so 51.10 px/s. From the page's stored C, S at columns i = 179, 180 (x = 398.9, 401.1): ω/(dφ/dh) = 51.10 px/s. Crests tracked in the stored ψ over 181 frames while playing: median 51.16 px/s (49–54 frame to frame). At the geometric centre (h = 170.26) r/h = 1.543; at the 1500–1600 px layouts r/h = 1.548. h → ∞ gives v; h → 0 gives ∞ (the scissors). | verified |
| N19 | 4 (changed) | and lie 46 px apart instead of 30 | local spacing λ·r/h = 46.46 px. From the stored C, S: 2π/(dφ/dh) = 46.46 px. Gap between the two tracked crests straddling the centre row: median 46.6 px (46.1–47.0). | verified |
| N20 | 5 | λ = 30: m = −13 … 12, 26 calm lines, 2s/λ = 26.7 | \|m + ½\|·30 < 400 for m = −13 … 12: 26; 800/30 = 26.67 | verified |
| N21 | 5 | λ = 60: 14 calm lines | m = −7 … 6: 14 | verified |
| N22 | 5 | residue \|a₁ − a₂\|/2 on the centre row: 0.071 at γ = 0.15, largest out to the sides | at the exact calm crossings on y = 181.372, with the page's g: 0.07107, at the outermost crossings (x = 64.0 and 736.0). The stored A at the outermost grid minima is 0.0739 (0.0243 at γ = 0, the grid offset of a 2.2 px cell). | verified |
| N23 | 5 | 0.162 at γ = 0.6 | exact crossings: 0.1624 (second-outermost crossing; 0.1615 at the outermost); stored A at the outer grid minima 0.1618–0.1627 | verified |
| N24 | 5 | at γ = 0 the calm lines are perfectly still | residue \|a₁ − a₂\|/2 = 0 at γ = 0 | verified |
| N25 | 6 (changed) | with damping the arrows of the nearer sources are a little longer; that moves no beam | a_n ∝ e^{+γ n s sin θ/R} (larger for the nearer sources). Normalised by the total arrow length, the damped pattern still equals 1 exactly at β = 2πm. Peaks found at 0.0°, ±42.0° for λ = 30. | verified |
| N26 | 6 (changed) | at the default γ, damping changes (12) by at most 0.03 | wrong, because the largest change at γ = 0.15 is 0.041 at the default λ = 30 px, and up to 0.057 over the slider's range of λ. Method: \|Σ a_n e^{ikr_n}\| / Σ a_n against (12); normalising by N times the middle arrow gives the same. At λ = 30 the maximum is 0.0407 at θ = ±45.36°, where damping fills the nulls beside the side beams ((12) gives 0.0001 there, the damped sum 0.0408). The page's own sum (6) at r = 10⁶ px from the row centre gives the same 0.0408. Only on Figure 3's coarse 0.1° grid does it shrink to 0.031–0.032. Across the λ slider the change is 0.041–0.057 for λ = 16–23 and 26–47 px, largest 0.057 at λ = 42 px (θ ≈ −84.9°) and at λ = 23 px. It falls to 0.013 at λ = 64 px. Correct statement: "at the default γ it changes (12) by at most 0.04 at λ = 30 px, and by up to 0.06 over the range of the slider". | wrong |
| N27 | 6 | eqnote: (12) against the page's sum (6), γ = 0, at 10⁶ px: largest difference 2.2 × 10⁻³ | 2.207 × 10⁻³ (at ±2.4°, the first zeros), λ = 30, measured from the row centre (400, y_s), same on 0.1° and 0.01° grids. Measured from source 0 instead it would be 1.1 × 10⁻². The note does not say which point; the centre gives its number. | verified |
| N28 | 6 | 6.3 × 10⁻⁵ at 10⁷ px | 6.262 × 10⁻⁵ (from the centre) | verified |
| N29 | 6 | N − 2 side lobes between full beams; for N = 16 the strongest reaches 0.220 | 15 zeros in 0 < β < 2π, so 14 side lobes; peak 0.22012 at β = 0.5624 | verified |
| N30 | 6 | sin θ₁ = 30/44.8 = 0.670, θ₁ = ±42.0° | 0.6696; 42.040° | verified |
| N31 | 6 | λ = 40: 63.2°; λ = 44: 79.2°; from 45 px λ/s > 1 | 63.23°, 79.16°; 45/44.8 = 1.0045 (slider steps are 1 px, so 45 is the first) | verified |
| N32 | 6, Fig. 3 | computed every 0.1° from −90° to 90°; main beam 2.40° to the first zero; side beams at ±42.04°; λ = 64: 5.12° | 1801 points per curve; 2.399°, 42.040°, 5.123°. The plotted SVG curves equal (12) at λ = 30 and 64 to 0.00036 (0.1 px plotting resolution = 0.0004). | verified |
| N33 | 7 | D²/λ = 15 053 px, 18.8 field widths | 672²/30 = 15 052.8; ÷ 800 = 18.82 | verified |
| N34 | 7, Fig. 4 | centre row y = 181.4 px, 169.1 px above the sources | stored y[j_c] = 181.372, h = 169.147 | verified |
| N35 | 7 | N = 2 (64, 736 px), λ = 64, γ = 0.15, x = 200–600: A from 0.009 to 0.829 | 0.00897 to 0.82854 (1 px samples, float64 sum (7) in the page) | verified |
| N36 | 7 | N = 4: 0.036 to 0.765 | 0.03601 to 0.76517 | verified |
| N37 | 7 | N = 16: 0.119 to 0.168, never more than 0.050 from the continuous row | 0.11851 to 0.16805. Largest gap to the continuous row in 200–600: 0.0503 (0.072 if the whole row 0–800 is taken). The stored grid A for Line of 16 at λ = 64 equals the float64 sum to 4.6 × 10⁻⁸ (float32) and gives 0.1185–0.1679. | verified |
| N38 | Fig. 4 | continuous row = 67 201 sources between 64 and 736 px; sampled every 1 px | 672/0.01 + 1 = 67 201. The four plotted curves equal the recomputed N = 2, 4, 16 and continuous rows to 0.0009, 0.0006, 0.0003, 0.0002 (plot units). | verified |
| N39 | 7 | λ = 30, N = 16: amplitude from 0.013 to 0.387, tall peaks about every 44 px | 0.01307 to 0.38670. Tall peaks (A > 0.25) at x = 175 … 625; gaps 43–48 px, mean 45.0 px, against s = 44.8 px. | verified |
| N40 | 7 | repeat length λ/sin θ₁ = s | λ/(λ/s) = s | verified |
| N41 | 7.1 | λ = 64, h = 169.1: Fresnel zone √(λh) = 104.0 px | √(64 × 169.147) = 104.05 | verified |
| N42 | 7.1 | (17) gives A = 0.142, against an average of 0.141 (continuous) and 0.140 (16 sources) over x = 200–600 | 0.14227; continuous 0.14082; 16 sources 0.14021 (stored grid: 0.14024) | verified |
| N43 | 7.1 | 16 sources, λ = 64: average A 0.076, 0.110, 0.140, 0.157, 0.173 at 50, 100, 169, 250, 340 px above the row | 0.07595, 0.10978, 0.14020, 0.15678, 0.17283 (x = 200–600, 1 px) | verified |
| N44 | 8 | 360 × 162 = 58 320 points in 1280–1600 px windows | 360 × 162 = 58 320 at 1200, 1280, 1366, 1440, 1500, 1536, 1600 and 1920 | verified |
| N45 | 8 | 360 × 360 = 129 600 at 880 px | 360 × 360 = 129 600 | verified |
| N46 | 8 | 324 × 324 = 104 976 on a 390 px phone | 324 × 324 = 104 976 (canvas 356 css px, dpr 2) | verified |
| N47 | 8 | at λ = 16 px: 7.2 points per wavelength (wide), 6.48 (phone) | 16/(800/360) = 7.2; 16/(800/324) = 6.48 | verified |
| N48 | 8 | 2 × 16 × 58 320 = 1 866 240 cosines and sines | stored `trig_calls` = 1 866 240 | verified |
| N49 | 8 | one rebuild took 59–98 ms in three runs; a frame 0.9–1.6 ms | unverifiable, because the times depend on the machine and its load; the note says so itself. Here, three fresh page loads gave 77, 84 and 65 ms per rebuild and 44 ms for warm rebuilds. Frames took 0.7–6.3 ms (medians 1.1–1.4 ms). Same order as the note. | unverifiable |
| N50 | 8 | C, S and ψ stored as 32-bit floats | `Float32Array` for C, S, ψ and A (store dtypes) | verified |
| N51 | 9 | λ = 30 px is one 26.7th of the width | 800/30 = 26.67 | verified |
| N52 | 9 | row n = round(127.5ψ + 127.5) of 256 colours | line 667; table length 768 = 256 × 3; 0 of 768 entries differ from (19) | verified |
| N53 | 9 | c₀ = (255, 250, 243), c₊ = (122, 31, 43), c₋ = (58, 50, 46) | table rows 0 and 255 = (58, 50, 46) and (122, 31, 43); `mid` = (255, 250, 243) | verified |
| N54 | 9 | ψ = 0.1 drawn 0.1^0.8 = 0.158 of the way from cream | 0.1585 | verified |
| N55 | 9 | one step Δψ = 2/255 = 0.0078 | 0.00784 | verified |
| N56 | 9 | a calm line stays cream in every frame | exact at γ = 0. At the default γ the outermost calm crossings on the centre row move with amplitude 0.071, which the table draws about 0.12 of the way from cream. Section 5 already says so. | verified |
| N57 | 9 | dot of radius 5.5 css px, cream rim, soft glow, on y_s | lines 681–693: arc radius 5.5, `T.accent` #7a1f2b fill, `T.card` #fffaf3 2 px rim, cream radial glow of radius 20, at y = box.h − 10·box.w/800. Screen pixel at both Reset dots: rgb(122, 31, 43), alpha > 0. | verified |
| N58 | 9 | Add 5 random: between 133.3 and 666.7 px | line 727: u = 1/6 + random·4/6, times 800 = 133.33 … 666.67 | verified |
| N59 | 10 | Kirchhoff's obliquity factor (1 + cos χ)/2 | standard result (Born & Wolf §8.3.2; Hecht §10.4, both ToCs read below) | verified |
| N60 | Ex. 5.1, 6.1 | 26 and 14 calm lines; side crests at about 42°; no side beams from 45 px | same as N20, N21, N30 and N31 | verified |

## 3 · The numerical method against the code

Line numbers are in the page file. `sim.js` is `public/scripts/sim.js`.

| # | Note (section 8 or 9) | Code | Verdict |
|---|---|---|---|
| M1 | (18) splits space from time; C and S do not depend on time | `precompute()` (627–657) sums `a·cos(ph)` and `a·sin(ph)` into C, S (647–648); `render()` uses them with cos ωt and sin ωt (660, 664) | verified |
| M2 | C and S are recomputed when sources are added, cleared or reset, or λ or γ moves, but not for f | λ and γ sliders call `changed()`, which sets `dirty` (594, 596, 598); `setSources()` calls `changed()` (701–704); f calls only `readouts()` (595). Measured: f change → 0 rebuilds, λ change → 1. (A resize also rebuilds, line 624; the note does not mention it. That is an omission, not an error.) | verified |
| M3 | 2NP cosines and sines per rebuild | one `Math.cos` and one `Math.sin` per source per cell (647–648); stored `trig_calls` = 2NP (655) | verified |
| M4 | each frame ωt ← ωt + 2πfΔt, Δt the real frame time capped at 0.05 s | `sim.js` 179: `dt = min((ts − last)/1000, 0.05)`; 181: dt = 0 while paused; page 762: `omegaT += 2π·freq·dt` | verified |
| M5 | then two multiplications and an addition per point, whatever N | line 664: `v = sumC[p]*c + sumS[p]*s` (plus the clip and table lookup, 665–671) | verified |
| M6 | columns min(360, max(60, round(w/1.1))), rows in proportion | line 602 exactly; line 603 `rows = max(30, round(cols·h/w))` (proportional, floored at 30) | verified |
| M7 | each value computed at the centre of its cell | 641, 643: `(j + 0.5)·dy − sy`, `(i + 0.5)·dx − sx`; coordinates 619–620 | verified |
| M8 | C, S, ψ in 32-bit floats | `ds.var(..., Float32Array)` for C, S, ψ, A (549–552) | verified |
| M9 | one grid point = one pixel of a small image, stretched with smoothing | `off` canvas cols × rows, `putImageData` (673), `imageSmoothingEnabled = true`, quality "high", `drawImage(off, 0, 0, box.w, box.h)` (674–676). 200 random cells: drawn image pixel = table row of stored ψ in 200 of 200. | verified |
| M10 | ψ clipped to [−1, 1] before the lookup; row round(127.5ψ + 127.5) | 665, 667 | verified |
| M11 | a_i = e^{−γr_i/R}, divided by N; phase k r_i; distances exact (2) | 628–629, 640–645 | verified |
| M12 | readouts give the number of sources and the speed (8) | `readouts()` 706–714: `r-n`, `r-v` = round(f·λ) px/s | verified |

## 4 · References and links

| # | Reference | Link (road) | Chapter claim | Verdict |
|---|---|---|---|---|
| R1 | Hecht, *Optics*, 5th ed., Pearson, 2017: ch. 4, 7, 9, 10 | pearson.com/…/P200000006793: curl 200. The page is *Optics*, 5th edition, Eugene Hecht. It lists the current eTextbook as "Published 14 July 2021, © 2022". The print 5th edition is © 2017 (ISBN 9780133977226, from the copyright page of the Global Edition). | Pearson ToC on that page: 4 The Propagation of Light, 7 The Superposition of Waves, 9 Interference, 10 Diffraction. Huygens's principle is §4.4.2 inside 4.4 Refraction. Firecrawl read the ToC from a library copy of the Global Edition (lib.ysu.am); the §4.4.2 number comes from a search excerpt. | verified |
| R2 | Crawford, *Waves*, Berkeley Physics Course vol. 3, McGraw-Hill, 1968: ch. 9; §9.6 Huygens' principle; link is a lending copy | archive.org/details/bwb_Y0-EAO-918_3: curl 200. Item "Waves", Frank S. Crawford Jr., 1968, volume 3. It is in the in-library and print-disabled collections, access-restricted with Borrow; its text files answer 401 without a login. | ToC from a copy on Scribd (Firecrawl): "9 Interference and Diffraction 451 … 9.5 Angular Width of a Beam of Waves 473, 9.6 Diffraction and Huygens' Principle 478, 9.7 Geometrical Optics 498". The archive.org item itself could not be opened past the login. | verified |
| R3 | Balanis, *Antenna Theory*, 4th ed., Wiley, 2016: ch. 6 | wiley.com/…-p-9781118642061: curl 200. 4th Edition, ISBN 978-1-118-64206-1, February 2016. | Wiley's ToC excerpt PDF (media.wiley.com/…1118642066-6.pdf, pdftotext): "6 Arrays: Linear, Planar, and Circular 285", with 6.3 N-Element Linear Array: Uniform Amplitude and Spacing. The index puts the phased (scanning) array at pp. 302–304, inside ch. 6. | verified |
| R4 | Born and Wolf, *Principles of Optics*, 7th ed., CUP, 1999: ch. 8 | doi.org/10.1017/CBO9781139644181: curl 200, redirects to cambridge.org/core/books/principles-of-optics. Page: 7th edition, print 13 October 1999, online 2013. Chapter "VIII Elements of the theory of diffraction, pp 412–516". | CERN library ToC PDF of the seventh (expanded) edition, read with Firecrawl (cds.cern.ch returned HTML to curl): "8.2 The Huygens–Fresnel principle 413; 8.3 Kirchhoff's diffraction theory 417" | verified |
| R5 | Feynman, Leighton, Sands, vol. I ch. 29 and 30, Caltech online edition | feynmanlectures.caltech.edu/I_29.html and I_30.html: curl 403. The 403 comes from Cloudflare's bot screen on that site; the agent proxy is fine. Firecrawl live fetch (maxAge 0): status 200 for both. | Titles "Vol. I Ch. 29: Interference" with 29–4 Two dipole radiators and 29–5 The mathematics of interference; "Vol. I Ch. 30: Diffraction" with 30–1 The resultant amplitude due to n equal oscillators and 30–2 The diffraction grating. Matches "two sources and the adding of arrows" and "the row of n equal sources, its beams and side beams". | verified |

All six URLs open.

## Summary

114 rows: 19 equations, 60 numbers, 12 method lines, 5 references. Two rows are wrong (N12, N26) and one is unverifiable (N49).

**verified 111 / wrong 2 / unverifiable 1**

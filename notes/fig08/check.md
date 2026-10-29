# Fig. 8 · derivation check

Note checked: `public/simulations/draw-decompose.html`, the lecture note inside `<article class="paper" id="paper">`, at HEAD `468c139`
(file sha256 starts `d7b4ae7a0289b509`). Changes against the base `db1a24b` were read line by line: the pointer to section 7.1 in
section 2, the inversion sentence after (5), the new opening of section 5, the Figure 3 caption, the square argument before (14),
`1.3e-6` for the figure eight at k = 40, and the reference links. The rest of the note was checked too.

How the checks were made:

- **Build.** `OUT_DIR=/tmp/fig08-check-dist npm run build`, run twice: before and after the section 5 edit. The built
  page is byte-identical to the source. The page script and `sim.js`, `dataset.js`, `datalog.js` and `fold.js` did not change between
  the two builds, and the store values from the two runs are identical.
- **Browser.** A small Node static server on port 8738, and Playwright with
  `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, at 1440 × 900 (canvas 770 × 601) and 390 × 844 (canvas 356 × 356). No
  console errors.
- **Page numbers.** Read from the page's own store (`Sim.data.ds`) and panel readouts, for six presets and every K from 1 to 120.
- **Code variants.** The page's own `resamp`, `dft`, `chainAt`, `param`, `poly` and `SHAPES` were cut out of the built HTML and run
  in the page with one change at a time: NS = 65 536, step `L/N` (no repeated endpoint), or M = 100 000.
- **Independent checks.** SymPy 1.14 for the algebra. numpy and mpmath for a Python transcription of the page, an FFT of the stored
  samples, and the figure eight's coefficients computed from the smooth curve. The note's SVG paths were parsed and compared with the
  store.
- **Scripts.** All the scripts are in my scratchpad (`/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/f8/scripts`).
  None of them went into the repository.

## 1. Numbered equations

| # | Statement | Check | Verdict |
|---|---|---|---|
| (1) | \(z(t)=\sum_k c_k e^{ikt}\), \(z(t+2\pi)=z(t)\), mean-square convergence for finite average of \(\|z\|^2\) | Correct statement of the L² theory (Riesz–Fischer / Parseval). SymPy: (3) applied to \(2e^{it}+(1-3i)e^{-2it}+\tfrac i2 e^{4it}\) returns exactly 2, 1−3i, i/2, and 0 for absent k. Units: \(c_k\) carries the units of z. | verified |
| (2) | \(\frac1{2\pi}\int_0^{2\pi}e^{ijt}e^{-ikt}dt=\delta_{jk}\) | SymPy: \(\int_0^{2\pi}e^{idt}dt=0\) for any integer \(d\ne0\); pairs (3,3), (−4,−4) → 1; (3,−2), (1,5), (0,7) → 0. | verified |
| (3) | \(c_k=\frac1{2\pi}\int z e^{-ikt}dt\) | Follows from (1) and (2); SymPy test as in (1). Limit k = 0: the mean, the centroid of the uniform wire. | verified |
| (4) | \(c_k\approx\frac1N\sum z_n e^{-2\pi ikn/N}\) | Same as `dft()`: the sum over n = 0..N−1 of the products (7), then `/= N`. | verified |
| (5) | \(\frac1N\sum_n w^n=\frac1N\frac{1-w^N}{1-w}=0\), \(w^N=1\), \(w\ne1\) | SymPy: \(\sum_{n=0}^{N-1}w^n-(1-w^N)/(1-w)=0\) for \(w\ne1\). Numerically ≤ 3 × 10⁻¹⁴⁷ (N = 8, 16) and 0.0 (N = 256) for j − k = 1, 2, 3, 5, N−1, N+3. The condition "j − k not a multiple of N" is stated. | verified |
| (5′) | After (5), new text: all N coefficients of N neighbouring frequencies give \(z_n=\sum_k c_k e^{2\pi ikn/N}\); substituting (4) turns it into the series (5) "with k and n trading places" | Substituting gives \(\sum_m z_m\,\frac1N\sum_k e^{2\pi ik(n-m)/N}=\sum_m z_m\delta_{nm}=z_n\). The index summed is now k, and the integer n − m takes the place of j − k. Numerically (N = 8, k = −3..4, random z): 5.7 × 10⁻¹⁶. | verified |
| (6) | \(\frac1N\sum z_n e^{-2\pi ikn/N}=\sum_m c_{k+mN}\) | For samples \(z_n=z(2\pi n/N)\) exactly. Test series with \(c_1, c_9, c_{-7}, c_3, c_{11}\), N = 8: both sides 2.3 + 0.7i (k = 1) and 0.55 (k = 3). (The page's samples are not exactly \(z(2\pi n/N)\); see M2.) | verified |
| (7) | Re and Im of (4) | SymPy: \((x+iy)(\cos a-i\sin a)\) has real part \(x\cos a+y\sin a\) and imaginary part \(y\cos a-x\sin a\). These are the code lines `re += z[n].x*c + z[n].y*s; im += z[n].y*c - z[n].x*s`. | verified |
| (8) | Parseval, \(\langle\|z\|^2\rangle=\sum_k\|c_k\|^2\) over N neighbouring frequencies | Random N = 16: 1.3218255733077346 and …44. FFT of the page's stored heart samples: mean \(\|z_n\|^2\) = Σ over the 256 bins of \(\|c_k\|^2\) to 2.2 × 10⁻¹⁶ relative; square, eight and wave to 0. Units: length². | verified |
| (9) | \(e_K^2=\sum_{k\notin S}\|c_k\|^2=\langle\|z\|^2\rangle-\sum_{k\in S}\|c_k\|^2\) | Random N = 16, S of 4 bins: 0.6146469669676126 and …27. Brute force over all 1820 four-bin subsets: the minimum is the 4 largest. Limits: S empty → \(\langle\|z\|^2\rangle\); all N → 0. | verified |
| (10) | relative error \(=\sqrt{1-\sum_S\|c_k\|^2/\langle\|z\|^2\rangle}\) | Algebra from (9). Numerically 0.6819080172339125 and …26. Lies between 0 and 1. | verified |
| (11) | \(c_k=\frac1{ik}\frac1{2\pi}\int\dot z e^{-ikt}dt\) | Integration by parts; the boundary term cancels by periodicity, which needs z continuous (a jump gives (13)). SymPy on a smooth periodic test curve, k = 1, 2, 3, 5: difference 0. Units: ż is length per radian and 1/k is a pure number, so length. | verified |
| (12) | \(c_k\approx-\frac1{2\pi k^2}\sum_j\Delta\dot z_j e^{-ikt_j}\), equal for a polygon | A second integration by parts gives \(-\frac1{2\pi k^2}[\sum_j\Delta\dot z_j e^{-ikt_j}+\int\ddot z e^{-ikt}dt]\) with \(\Delta\dot z=\dot z(t_j^+)-\dot z(t_j^-)\). SymPy, side-1.4 square: the exact piecewise-linear integrals equal (12) to 0 for k = 1, −3, 5, −7 (0.80242284, 0.089158093, 0.032096913, 0.016375976), and both are 0 for k = 2, −1, 3, 4. | verified |
| (13) | \(\|c_k\|\approx\|\Delta z\|/(2\pi\|k\|)\) | SymPy, sawtooth \(z=t\) on (0, 2π) (jump 2π): \(c_k=i/k\), so \(\|c_k\|=1/\|k\|=\|\Delta z\|/(2\pi\|k\|)\) exactly for k = 1, 2, 5, −3. Limit: no jump, so no 1/k term. | verified |
| (14) | \(\|c_k\|=\frac{4\sqrt2v}{2\pi k^2}=\frac{\sqrt2L}{\pi^2k^2}=\frac{0.802}{k^2}\) | SymPy with v = L/2π: the difference is 0. √2 · 5.6/π² = 0.802423. Exact for k = 1, since the square is a polygon (see (12)). Units: length. | verified |
| (15) | \(t\leftarrow t+2\pi\Delta t/T_\text{loop}\); \(z(t)=\sum_{\text{rank}<K}\|c_k\|e^{i(kt+\arg c_k)}\) | Code: `t += TAU*dt/loop.value`, with `dt = min(gap, 0.05)` and 0 while paused (`Sim.clock`); `chainAt()` is the closed-form sum. Dimensionless. | verified |
| (16) | px per unit \(=0.46\min(w,h)/\max(1,R_\text{view})\times\)zoom | Code: `viewScale()`. Measured in Chromium for 6 presets × K = 1, 24, 120 at both viewports: the stored `scale` minus the formula is 0 exactly. Units: px per unit, with the 1 in \(\max(1,R)\) read as 1 unit. | verified |

## 2. Numbers and stated results, in note order

| # | Where · claim | Recomputed | Verdict |
|---|---|---|---|
| N1 | Fig. 1 · k = 1, −2, 4: after a third of a loop the chain is turned by 120°, three-fold symmetry | \(e^{ik2\pi/3}=e^{2\pi i/3}\) for all three k. The drawn path (721 points) fits \(\sum c_je^{ik_jt}\) with k = 1, −2, 4 (y up) to 0.07 px, with radii 108.0, 45.4 and 27.0 px, the same as the drawn circles. The ±k fit fails (160 px). A 120° rotation maps the path onto itself to 0.12 px. | verified |
| N2 | §2 · Time per loop 12 s by default | Slider `value="12"`, readout "12 s". | verified |
| N3 | §2 · the centred sample mean is zero | The stored centred heart samples have \(\|c_0\|\) = 1.7 × 10⁻¹⁶. | verified |
| N4 | Fig. 2 · N = 16 points made by the page's own resampling; the cross is the mean | The page's `resamp()` run on the 31 drawn raw points (+340 px) reproduces the 16 drawn samples to 0.09 px. Mean (511.86, 171.42); drawn cross (511.9, 171.4). Equal chords 36.9–38.6 px; closing step 43.2 px. | verified |
| N5 | §4 · N = 256 | `NS = 256`; store N = 256. | verified |
| N6 | §4.2 · \(-60\le k\le60\), below N/2 = 128 | `KMAX = 60`. | verified |
| N7 | §4.2 · against 65 536 samples, the aliases change the radii of the heart's three largest circles by less than 0.1 % | **Aliases alone** (page code at NS = 256 and 65 536, both without the repeated endpoint): k = −1, 2, −3 change by 1 × 10⁻⁶, 2.9 × 10⁻⁴ and 5 × 10⁻⁶, so at most 0.029 %. **Caveat:** with the page's own resampling at both N, the changes are 0.31 %, 0.17 % and 3.0 %. That difference is the repeated endpoint (section 7.1), not aliasing. The comparison has to keep the endpoint treatment fixed. | verified |
| N8 | §4.2 · near \(\|k\|\)=60 the aliases change the heart's radii by about 20 % and the open wave's by 10 % | Aliases alone, heart: 18–21 % at even \(\|k\|\) = 56–60 (the larger radii) and about 4 % at odd. Page resampling: 8–22 %. Open wave: 9.0–10.1 % both ways. | verified |
| N9 | §4.3 · 30 720 complex products | 120 × 256 = 30 720. | verified |
| N10 | §4.3 · `dft()` about 1 ms | 200 runs on the heart in Chromium: median 0.80 ms, minimum 0.60, 90th percentile 1.9. | verified |
| N11 | §4.3 · whole decomposition about 8 ms | Preset click (shape, decompose, rebuild, readouts, spectrum), 60 runs per preset: first click 7.9–17 ms, warm median 2.9–3.5 ms, 90th percentile 4.6–7.8 ms, maximum 35 ms. Right order of magnitude; it depends on the machine and on JIT warm-up. | verified |
| N12 | §5 (new) · "the computed circles redraw the N samples exactly, \(z_n=\sum_k c_k e^{2\pi ikn/N}\)" | | wrong, because the identity needs **all N = 256** coefficients (4), over N neighbouring frequencies (section 4.1). The page computes only 120 of them (\(\|k\|\le60\), k ≠ 0), and they do not redraw the samples exactly. At K = 120 the measured RMS error is 4.91 × 10⁻⁴ for the heart (0.068 %, as section 9 says), 7.12 × 10⁻⁴ for the square and 0.0444 for the open wave. Correct: "all N coefficients (4) of N neighbouring frequencies redraw the samples exactly; the page computes 120 of them". |
| N13 | §5 (new) · "\(\tfrac1N\sum_n e^{2\pi i(j-k)n/N}=0\) for \(j\ne k\), which is equation (5)" | | wrong, because (5) holds only when j − k is not a multiple of N. For j = k ± 256 the average is 1: that is the aliasing of section 4.2. Correct: "for \(j\ne k\) among N neighbouring frequencies", which is how Parseval (8) then uses it. One phrase fixes this row and N12. |
| N14 | §5 · the two error readouts agree to within 3 parts in 10¹⁰ for the default heart, K = 1..120 | Measured in the page: largest \(\|e_K-e_K^{\text{Parseval}}\|/e_K\) = 2.2 × 10⁻¹⁰. | verified |
| N15 | §5 · the gap comes from subtracting two nearly equal numbers in (9) | Measured error against \(\sqrt{\sum_{\text{dropped}}\|c_k\|^2}\) (FFT of the stored samples): agree to 7 × 10⁻¹⁴. The page's \(\langle\|z\|^2\rangle-\)kept route: 2.2 × 10⁻¹⁰. | verified |
| N16 | §5 · heart, one circle: k = −1 (traced clockwise), 94.3 % kept, \(\sqrt{0.057}\) = 24 % | Readout "−1"; cap 94.303 %; \(\sqrt{0.057}\) = 0.239; measured relative error 0.2387. The parametrisation runs clockwise (x = 0.85 sin³u is positive just after the notch while y falls). | verified |
| N17 | §5 · K = 24: 99.99 % kept, RMS 0.00541, 0.75 % of \(\sqrt{0.5150}\) = 0.718 | Readouts "99.99 %" and "0.00541" (0.0054060). ⟨\|z\|²⟩ = 0.515045, root 0.71767. Ratio 0.753 %. | verified |
| N18 | §5 box · among the 120 computed components, the K largest are least-squares optimal | Follows from (9). Brute-force test in (9). | verified |
| N19 | Fig. 3 · heart 24 %, 2.9 %, 0.75 %, 0.23 % at K = 1, 10, 24, 50 | Page: 23.87 %, 2.866 %, 0.753 %, 0.234 %. | verified |
| N20 | Fig. 3 · roughly \(K^{-3/2}\) in the middle | Log–log slope from K = 10 to 50: −1.56. | verified |
| N21 | Fig. 3 (edited) · beyond K ≈ 80 both curves flatten near 10⁻³; the circles left are tiny; what is missing lies beyond \(\|k\|\)=60 | Heart 9.87 × 10⁻⁴ → 6.85 × 10⁻⁴ and square 9.05 × 10⁻⁴ → 8.80 × 10⁻⁴ from K = 80 to 120. Rank-80 radii: 1.6 × 10⁻⁴ (heart), 6.6 × 10⁻⁵ (square). At K = 120 the Parseval residual is exactly the energy outside \(\|k\|\le60\): 4.7 × 10⁻⁷ of ⟨\|z\|²⟩ for the heart. | verified |
| N22 | Fig. 4 · K = 3, 10, 50; 601 points; at K = 50 the curve covers the samples at this scale | The plotted curves are the page's stored 601-point curves (F4). At K = 50 the largest gap to a sample is 0.0075 units = 1.05 px for the heart and 0.81 px for the square, against a 1.8 px line. With K = 3 the notch is a 0.048-unit dip; with K = 10 it is 0.30 deep. | verified |
| N23 | Fig. 4 · the square "reaches a given error with fewer circles than the heart (Figure 3)" | | wrong, because it holds only down to an error of about 9 × 10⁻⁴. The two curves of Figure 3 cross at K = 84 (heart 8.93 × 10⁻⁴, square 8.93 × 10⁻⁴). After that the square stays at its floor of 8.80 × 10⁻⁴, while the heart reaches 6.85 × 10⁻⁴ at K = 120. An error below 8.8 × 10⁻⁴ is reached by the heart and never by the square. Correct: "reaches a given error down to about 10⁻³ with fewer circles than the heart". |
| N24 | Fig. 4 · square at K = 10 passes 0.019–0.022 units inside each corner | Smallest corner-to-curve distances 0.0193, 0.0209, 0.0221, 0.0209 (dense curve; the 601-point curve gives the same to ±0.0003). | verified |
| N25 | Ex. 5.1 · square, K = 1: 98.52 % kept, RMS 0.09831 | Readouts "98.52 %" and "0.09831". | verified |
| N26 | Ex. 5.1 · \(\sqrt{0.6546}\) = 0.8091; the check gives back 0.9852 | ⟨\|z\|²⟩ = 0.654599, root 0.80907. 1 − (0.09831/0.8091)² = 0.98524. | verified |
| N27 | Ex. 5.1 · K = 4 keeps k = 1, −3, 5, −7; \(z(t+\pi/2)=iz(t)\) leaves only k = 1 − 4m | Ranks 0–3 are k = 1, −3, 5, −7. By (3), \(c_k(1-ie^{-ik\pi/2})=0\), so \(c_k\ne0\) needs \(e^{ik\pi/2}=i\), that is k ≡ 1 (mod 4). The preset runs anticlockwise from the corner (0.7, 0.7). | verified |
| N28 | §6 · v = L/2π per unit of t | From t = 2πs/L. | verified |
| N29 | §6.1 · side 1.4, L = 5.6, \(\|\Delta\dot z\|=\sqrt2v\) | Vertices ±0.7; store L = 5.600000000000028. \(\|v(i-1)\|=\sqrt2v\) (SymPy). | verified |
| N30 | §6.1 (new) · \(t_j=j\pi/2\), \(\Delta\dot z_j=i^j\Delta\dot z_0\), the term is \(\Delta\dot z_0(ie^{-ik\pi/2})^j\), the bracket is 1 for k = 1 − 4m and −1 or ±i otherwise, and these cancel | Equal sides, start at a corner, anticlockwise. SymPy bracket: k ≡ 1 → 1; 0 → i; 2 → −i; 3 → −1. A fourth root of unity other than 1 sums to 0 over j = 0..3. | verified |
| N31 | §6.1 · (14) gives 0.802, 0.0892, 0.0321; exact even for k = 1 | 0.802423, 0.0891581, 0.0320969. Exact polygon coefficients equal (14) (row (12)). | verified |
| N32 | §6.1 · the page finds 0.803, 0.0903, 0.0317; scatter about 1 % | Store 0.803078, 0.090312, 0.031708. Off by +0.08 %, +1.29 %, −1.21 %. | verified |
| N33 | §6.1 · heart: both derivatives vanish at the notch and the point; a cusp, in moving down and out moving up; velocity jump 2v | SymPy: x′ = y′ = 0 at u = 0 and π. y″ = 697/320 and 527/320 (both > 0), x‴ = ±5.1. So the tangent is vertical and the bead goes down, then up. Δż = 2vi at both. | verified |
| N34 | §6.1 · cusps at t = 0 and π; they add for even k and cancel for odd k | The mirror x → −x splits the length in halves, so t = π at the point. \(1+e^{-ik\pi}\) = 2, 0, 2, 0 for k = 2, 1, 4, 3. | verified |
| N35 | §6.1 · \(L/(\pi^2k^2)=0.550/k^2\) with L = 5.428 | SymPy: 4v/(2πk²) − L/(π²k²) = 0. Page L = 5.42763 (smooth curve 5.42765); L/π² = 0.54993. | verified |
| N36 | §6.1 · \(k^2\|c_k\|\) = 0.550, 0.552, 0.544 at k = 10, 20, 30 | Page at +k: 0.5505, 0.5520, 0.5440. At −k: 0.507, 0.542, 0.536 (Fig. 5 plots the larger). | verified |
| N37 | §6.1 · a \(1/k^2\) tail gives \(\sum\|c_k\|^2\sim K^{-3}\), so \(e_K\propto K^{-3/2}\) | mpmath: \(K^3\sum_{k>K/2}k^{-4}\) = 2.29, 2.47, 2.57, 2.62 for K = 20, 40, 80, 160, tending to 8/3. | verified |
| N38 | §6.1 · open wave ends 1.7 apart; 1.7/(2π) = 0.271; the page finds 0.271 at k = 10 | x from −0.85 to 0.85 with y = 0 at both ends; stored \(\|z_{255}-z_0\|\) = 1.7. 1.7/2π = 0.27056. Page \(10\|c_{10}\|\) = 0.27096. | verified |
| N39 | §6.1 · \(K^{-1/2}\): 20 %, 14 %, 8.4 % at K = 24, 50, 120 | Page 20.48 %, 14.18 %, 8.41 %. Slope from K = 24 to 120: −0.55. | verified |
| N40 | §6.1 (edited) · figure eight from the smooth shape: 0.40 at ±1; 5.8 × 10⁻⁴, 8.1 × 10⁻⁵, 1.0 × 10⁻⁵, **1.3 × 10⁻⁶** at k = 10, 20, 30, 40; 7–9 times smaller per ten steps | Spectral arc-length integral (numpy, M = 2¹⁴ and 2¹⁶ agree): 0.39700, 5.8236 × 10⁻⁴, 8.0813 × 10⁻⁵, 1.0345 × 10⁻⁵, 1.2605 × 10⁻⁶. The page's own code with M = 100 000, N = 262 144 and no repeated endpoint gives the same five digits. Ratios 7.21, 7.81, 8.21. The old value 1.2 × 10⁻⁶ was wrong; 1.3 is right. | verified |
| N41 | Fig. 5 · heart even k, square k = 1 − 4m, dotted (13) and (14); figure-eight floor near 10⁻⁴ from the sampling | Plotted sets as stated (F5). The dotted lines are 0.271/\|k\| and 0.803/k² read back. Page radii for the eight: 1.26 × 10⁻⁴ (k = 20), 1.17 × 10⁻⁴ (30), 8.4 × 10⁻⁵ (40), 5.9 × 10⁻⁵ (60). Without the repeated endpoint they are 1.3 × 10⁻⁸ at 60. | verified |
| N42 | §6.2 · square crosses a side line by at most 0.010 near a corner at K = 10, and by 0.0038 at K = 50 | Largest overshoot past a side line: 0.0104 at 0.09 from a corner (K = 10); 0.0038 at 0.013 from a corner (K = 50). | verified |
| N43 | §6.2 · open wave overshoots each end by 5.9 %, 7.9 %, 9.5 % of 1.7 at K = 24, 50, 120; the Gibbs limit is about 9 % | Dense curve: 5.86 %, 7.93 %, 9.52 % at both ends; the 601-point curve gives 5.85–9.52 %. Si(π)/π − ½ = 8.95 %. | verified |
| N44 | Ex. 6.1 · the overshoot grows to about 0.16 units | 0.1619 at K = 120. | verified |
| N45 | §7 · 120 coefficients, 601 points, Δt at most 0.05 s | `K.max` = 120; `i <= 600`; `Math.min(…, 0.05)` in `Sim.clock`. | verified |
| N46 | §7.1 · ⟨\|z\|²⟩ = 0.515044672459522 and \(e_{24}\) = 0.005405966670666, in the page and in Python | Page 0.5150446724595221 and 0.005405966670666055. My own Python transcription: 0.515044672459522 (−2.2 × 10⁻¹⁶) and 0.005405966670666 (+4.5 × 10⁻¹⁷); coefficients to 4.4 × 10⁻¹⁶, same order. | verified |
| N47 | §7.1 · \(z_{255}\) lands on \(z_0\); the pause adds about \(\Delta s/(2\pi\|k\|)\); figure eight Δs = 0.0203 gives 5.4 × 10⁻⁵ at \(\|k\|\)=60; the page finds 5.9 × 10⁻⁵ | Stored \(\|r_{255}-r_0\|\) = 0 (heart, square) and 3 × 10⁻¹⁶ (eight). The estimate comes from the phase sawtooth (jump 2π/256) times the speed L/2π, which is about Δs. Δs = 0.020324; 0.020324/(120π) = 5.39 × 10⁻⁵; page 5.905 × 10⁻⁵ at ±60. | verified |
| N48 | §7.1 · the pause gives the square's k = 2 and k = −1 radii of 2.5 × 10⁻³ and causes the 1 % scatter of (14) | Page 2.4717 × 10⁻³ for both. Without the repeated endpoint they are ≤ 3 × 10⁻¹⁵, and the radii become 0.80246, 0.089198 and 0.032137, within 0.13 % of (14). | verified |
| N49 | §7.1 · a gap g adds about \(g/(2\pi\|k\|)\) | (13). | verified |
| N50 | §7.1 · figure eight at K = 120: relative error 1.5 × 10⁻⁶ with step L/N, against 8.4 × 10⁻⁴ | Page 8.414 × 10⁻⁴. Page code with step `tot / N`: 1.484 × 10⁻⁶, measured and by Parseval. | verified |
| N51 | §8 · 1 unit = 0.46 of the shorter side; y up; a pointer step under 0.006 units is skipped | `S()`, `world()`, and `> 0.006` in `pointermove`. | verified |
| N52 | §8 · R is the joint distance plus radius at 256 instants, or the furthest sample | `rebuild()` loop over `i < 256`, and `samples.forEach`. | verified |
| N53 | §8 · R_view jumps up at once and relaxes down with time constant 0.4 s | Code `1 - exp(-real/0.4)`. Measured (open wave, K 120 → 1): fitted τ = 0.400 s; half-way at 0.282 s (0.4 ln 2 = 0.277). | verified |
| N54 | §8 · at zoom 1× nothing leaves the figure; zoom 1× to \(10^{1.8}\) ≈ 63× | Largest extent / half the short side = 0.92 (6 presets, K = 1, 24, 120, both viewports, no pan). \(10^{1.8}\) = 63.1; slider max 1.8; `setZoom` clamps to [1, 10^1.8]. | verified |
| N55 | §8 · trail in 24 segments, opacity 0.16 to 1, over the last loop | `nseg = 24`; 0.12 + 0.88·(c+1)/24 runs from 0.157 to 1.000; the trail keeps 0.98 of a loop. | verified |
| N56 | §8 · four arm colours, first twelve numbered by rank; 601-point pink curve; stems \(\|c_k\|\)/largest at −60..60, burgundy if kept, tan if not | `VEC[i % 4]`; `i < 12`; `'#c9707e'`; `spectrum()` with `T.accent` / `T.tanInk`. | verified |
| N57 | §9 · heart at K = 120: relative error still 0.068 % | 0.06847 %. | verified |
| N58 | §9 · corners cut by at most Δs = L/255; 0.021 for the heart | Store `step` = L/255 = 0.021285. | verified |
| N59 | §9 · "the page's choice makes ⟨\|z\|²⟩ the moment of inertia of a uniform wire" | | wrong, because the units do not match. ⟨\|z\|²⟩ is a length squared and a moment of inertia is mass × length squared. Section 5 has it right: ⟨\|z\|²⟩ is I/m, exact for the 256 point masses and only approximate for the wire because of the repeated endpoint. Correct: "makes ⟨\|z\|²⟩ (nearly) the moment of inertia per unit mass of a uniform wire". |
| N60 | §5 · for equal point masses at the centred samples, ⟨\|z\|²⟩ is exactly I/m | Polar moment about the centroid: \(I=\sum m r_n^2\), so \(I/(Nm)\) is the mean of \(r_n^2\). | verified |

## 3. Description of the numerical method against the code

| # | Note | Code | Verdict |
|---|---|---|---|
| M1 | §2, §7: resample at equal arc length so that t ∝ distance | `resamp()` | verified |
| M2 | §4: "takes N = 256 samples \(z_n=z(t_n)\) at equal steps \(t_n=2\pi n/N\)" | `step = tot / (N - 1)`: sample n sits at arc length nL/255, that is at t = 2πn/255. For closed shapes sample 255 repeats sample 0 (stored: \(\|r_{255}-r_0\|\) = 0; step × 255/L = 1). | wrong, because the code samples at \(t=2\pi n/(N-1)\), not \(2\pi n/N\). The DFT then treats the samples as if they were at \(2\pi n/N\). Sections 7 and 7.1 describe this correctly, and section 2 now points there, but section 4 states the ideal as what the page does. Correct: "at (almost) equal steps, \(z_n\) at arc length \(nL/(N-1)\), so that \(z_{N-1}\) repeats \(z_0\) (section 7.1)". |
| M3 | §7: \(s_i=\sum_{j\le i}\|p_j-p_{j-1}\|\), \(\Delta s=L/(N-1)\), sample n at \(n\Delta s\) by linear interpolation, n = 0..255 | `arcDistances`, `tgt = i*step`, `f = min(1, …)`, first sample = stroke start | verified |
| M4 | §7: subtract the mean so \(c_0=0\); store ⟨\|z\|²⟩ here | `decompose()`: `meanX/meanY` over NS, `samples`, `meanZ2`, `ds.set('E', …)` | verified |
| M5 | §7: sums (7) for k = −60..60 except 0 | `dft()`: `k === 0` skipped, `/N`, `amp = hypot`, `phase = atan2` | verified |
| M6 | §7: sort by \(\|c_k\|\), first K used, largest circle at the base of the chain | `out.sort(b.amp - a.amp)`; `chainAt` starts at the origin with rank 0 | verified |
| M7 | §7: rebuild on every K change: kept share, error by Parseval (9), error at the 256 samples, 601 curve points | `Sim.slider('K', {onInput: rebuild})`; `errP = sqrt(max(0, meanZ2 - kept))`; `err` over `NS`; `i <= 600` (also `extR` and `spectrum()`) | verified |
| M8 | §7: per frame (15), no integration, joints are partial sums, the last one is the pen | `Sim.clock` callback and `chainAt`; `draw()` cumulates `p.vx`, `p.vy` | verified |
| M9 | §5: readouts "⟨\|z\|²⟩ kept" = share, "RMS error" measured, "… by Parseval" = right side of (9) | `readouts()`: `100*kept/meanZ2`, `err`, `errP` | verified |
| M10 | §8: units, R, R_view, zoom, Follow the pen | `S()`, `world()`, `rebuild()` extR, clock relaxation, `setZoom`, `draw()` view centre | verified |
| M11 | §8: what is drawn and in which colours | `draw()`, `spectrum()`. (Component circles are drawn only when the radius exceeds 1.5 px; the note leaves this out.) | verified |

## 4. Figure data against the page's numbers

| # | Figure | Check | Verdict |
|---|---|---|---|
| F3 | Fig. 3 curves (120 + 120 points) | Read back with x = 64 + K·634/120 and y = 284 − 66.5(log₁₀e + 4). Both curves equal the page's stored relative error at every K to 7.5 × 10⁻⁴ decades (0.05 px, the 1-decimal SVG rounding). | verified |
| F4 | Fig. 4 samples and K = 3, 10, 50 curves (257 + 3 × 601 points) | They equal the page's stored centred samples and `full_x/full_y` to 0.08 px. (Remark: the axes use 139.1 px per unit in x and 140.0 in y, a 0.6 % horizontal squash; not a number in the note.) | verified |
| F5 | Fig. 5 curves (60, 30, 30, 60 points) and the two dotted laws | Every point equals the page's larger of \(\|c_{\pm k}\|\) to 0.0011 decades (0.05 px). Dotted lines \(k\|c\|\) = 0.271 and \(k^2\|c\|\) = 0.803. | verified |

## 5. References

| # | Reference · link · cited part | Road taken and result | Verdict |
|---|---|---|---|
| R1 | Boas, 3rd ed., Wiley, 2006 · wiley.com …p-9780471198260 · ch. 7 Fourier series and transforms, incl. Parseval | curl (browser user-agent): HTTP 200, title "Mathematical Methods in the Physical Sciences, 3rd Edition \| Wiley", ISBN 978-0-471-19826-0 (hardcover listed July 2005; the book's copyright page says © 2006). Wiley's contents tab is empty in the static HTML. I read the front matter and contents PDF found through Firecrawl search (sites.evergreen.edu, Boas-Preface-ToC.pdf): "7 FOURIER SERIES AND TRANSFORMS 340 … 11. Parseval's Theorem 375 · 12. Fourier Transforms 378"; "Copyright 2006 John Wiley & Sons". | verified |
| R2 | Kreyszig, 10th ed., Wiley, 2011 · wiley.com …p-9781119455929 · ch. 11 Fourier analysis | curl: HTTP 200, "Advanced Engineering Mathematics, 10th Edition", ISBN 978-1-119-45592-9 (a later loose-leaf printing of the 10th edition, July 2020; e-book January 2018; the 2011 hardcover has another ISBN). Wiley's contents excerpt PDF (media.wiley.com/…/1119455928-14.pdf): "PART C Fourier Analysis. PDEs 473 · CHAPTER 11 Fourier Analysis 474". | verified |
| R3 | Stein & Shakarchi, PUP, 2003 · press.princeton.edu …/9780691113845/fourier-analysis · ch. 2, 3, 7 | curl got HTTP 403 twice (the hardcover URL and the paperback variant, browser user-agent). That is a bot block, not proof of a dead link. I took another road, WebFetch: the page opens and shows Stein and Shakarchi, hardcover ISBN 9780691113845, published 6 April 2003. Contents: ch. 2 "Basic Properties of Fourier Series", ch. 3 "Convergence of Fourier Series", ch. 7 "Finite Fourier Analysis". | verified |
| R4 | Press et al., 3rd ed., CUP, 2007, readable online · numerical.recipes/book.html · ch. 12, 13 | curl: HTTP 200. The online reader's contents: "12 Fast Fourier Transform 600", "13 Fourier and Spectral Applications 640". Its chapters 16 "Classification and Inference" and 22 "Less-Numerical Algorithms" belong to the 3rd edition. The home page says "Read the newest Third Edition book in C++ online for free, with nags". | verified |

## Remarks (not counted)

- N7: anyone who repeats the 65 536-sample comparison with the page's own resampling will see 3.0 % at k = −3, not < 0.1 %. To
  show aliasing alone, the comparison has to keep the endpoint treatment the same at both N.
- §8, "at zoom 1× nothing leaves the figure": this holds for the unpanned view. Dragging, or Follow the pen, can move parts out.
- The heart's quoted \(k^2|c_k|\) values are at +k. At −k they are 4–8 % lower (0.507 at k = −10).

**Summary: 95 rows (17 equations, 60 numbers, 11 method rows, 3 figure-data rows, 4 references): 90 verified, 5 wrong, 0 unverifiable.**

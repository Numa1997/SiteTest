# Fig. 7 · derivation check of the lecture note

Page checked: `public/simulations/phasor-sums.html`, the note between `<article class="paper" id="paper">` and `</article>`,
as committed in 468c139 (file md5 `81106e1f8a87ed3da3028f1a6940d5d1`; unchanged in 6df11fb). The shared scripts
(`sim.js`, `dataset.js`, `datalog.js`) are unchanged since db1a24b.

How it was checked.

- Equations re-derived in SymPy 1.x (identities, `dsolve`, `rsolve`, series, symbolic averages); units and limits by hand.
- Every number recomputed from the page's own code: the page was built with
  `APPDEPLOY_VITE_OUT_DIR=/tmp/fig07-check-dist npm run build` (built file identical to the source), served by a small
  Node static server, and driven in headless Chromium 1194 through Playwright (`npm root -g` → `/opt/node22/lib/node_modules`).
  Values were read from the page's store `Sim.data.ds` and from the readout text, after clicking the real buttons and
  sliders. Figure data were checked by parsing the SVG paths in the note and comparing them with (6).
- The method sections (7, 7.1, 8, 8.1) were read against the script line by line (page lines 799–1351, `sim.js` clock).
- Links: curl first; where curl got a 403 or an empty 202, headless Chromium, then Firecrawl `scrape`. The road taken is
  given in each row.
- Scripts and raw output are in the session scratchpad (temporary): `svgcheck.py`, `derive.py`, `closure.js`,
  `layout.cjs`, `exercises.cjs`, `record.cjs`, `record2.cjs`, `dance.cjs`, `dance2.cjs`, `morph.cjs`, `refs*.cjs`.
  I did not read `plan.md`, `referee.md`, `walk.md` or the other agents' scripts in this folder.

## Numbered equations

| Eq. | Statement | Check | Verdict |
|---|---|---|---|
| (1) | \(i(x+iy) = -y + ix\) | SymPy: difference expands to 0. A quarter turn: \((x,y)\mapsto(-y,x)\). | verified |
| (2) | \(\mathrm{d}z/\mathrm{d}\theta = iz,\ z(0)=1\) | `dsolve` gives \(z = e^{i\theta}\). \(\mathrm{d}\lvert z\rvert^2/\mathrm{d}\theta = 2\,\mathrm{Re}(\bar z\, i z) = 0\) for any \(z\) (SymPy), so "no closer, no further"; speed \(\lvert iz\rvert = \lvert z\rvert = 1\). | verified |
| (3) | \(e^{i\theta} = \cos\theta + i\sin\theta\) | SymPy `expand_complex`: 0. | verified |
| (4) | power series split into cos and sin series | Series of \(e^{i\theta}\) to order 12: real part minus cos series = 0, imaginary part minus sin series = 0; signs \(1, -\theta^2/2!, +\theta^4/4!\) and \(\theta, -\theta^3/3!, +\theta^5/5!\) as printed. | verified |
| (5) | \(A e^{i(\omega t+\varphi)} = A\cos + iA\sin\) | SymPy 0. Units: \(\omega t\) in rad/s · s = rad. One turn \(2\pi/\lvert\omega\rvert\). | verified |
| (6) | \(z(t) = \sum_k A_k e^{i(\omega_k t+\varphi_k)}\) | Definition; it is exactly `sumAt()` (page l. 813–825): \(x=\sum A\cos(\omega t+\varphi)\), \(y=\sum A\sin(\ldots)\). | verified |
| (7) | \(\dot z = \sum i\omega_k A_k e^{i(\ldots)}\) | SymPy: \(\mathrm{d}(6)/\mathrm{d}t - (7) = 0\) (N = 3). Each term has \(\lvert\cdot\rvert^2 = A^2\omega^2\) and is perpendicular to its arm (\(\mathrm{Re}(\bar a\,\dot a)=0\)). Units: length/s. | verified |
| (8) | \(A(e^{i\omega_1 t}+e^{i\omega_2 t}) = A e^{i\bar\omega t}(\ldots) = 2A\cos(\Delta\omega t/2)e^{i\bar\omega t}\) | Both steps reduce to 0 in SymPy. Limit \(\Delta\omega\to0\): \(2Ae^{i\omega t}\), one arm of length \(2A\). | verified |
| (9) | \(r = 2A\cos(n\theta)\), \(n = \Delta\omega/(2\bar\omega) = (\omega_1-\omega_2)/(\omega_1+\omega_2)\) | Substituting \(t=\theta/\bar\omega\) into \(r = 2A\cos(\Delta\omega t/2)\): identical; SymPy simplifies \(n\) to the printed fraction. | verified |
| (10) | \(\lvert z\rvert = 2A\lvert\cos((\Delta\omega t+\varphi_1-\varphi_2)/2)\rvert = 2.2\lvert\cos(t/2+0.05)\rvert\) | SymPy: \(\lvert z\rvert^2 - 4A^2\cos^2(\ldots) = 0\). Beating pair: \(((5-6)t - 0.1)/2 = -(t/2 + 0.05)\), cosine even. Limit \(\Delta\omega=0\): constant \(2A\lvert\cos(\Delta\varphi/2)\rvert\), as Exercise 4.1 uses. | verified |
| (11) | \(\lvert z\rvert^2 = A_1^2 + A_2^2 + 2A_1A_2\cos((\omega_1-\omega_2)t+\varphi_1-\varphi_2)\) | SymPy 0. New sign argument checked: in the triangle O, \(z_1\), \(z\) the angle at the joint is \(\pi\) minus the angle between the arms (numerical example: 1.44159 = 1.44159), and \(\cos(\pi-\alpha) = -\cos\alpha\) (SymPy). Limit \(A_2\to0\): \(\lvert z\rvert = A_1\). | verified |
| (12) | \(T = 2\pi/g,\ g = \gcd(\omega_k)\) | \(e^{i\omega_k T}=1\ \forall k\) with \(\omega_k = g m_k\), \(\gcd(m_k)=1\) ⇔ \(T\in(2\pi/g)\mathbb Z\) (Bézout). Units: rad / (rad/s) = s. For distinct frequencies with \(A_k\neq0\), linear independence of the \(e^{i\omega_k t}\) makes every period of the pen a common period of all arms, so only cancellation (equal frequencies summing to 0) can shorten it, as the new paragraph says. | verified |
| (13) | \(z(t+\tau) = \sum A_k e^{i(\omega_k t+\varphi_k)}e^{i\omega_k\tau}\) | SymPy 0 (N = 3). | verified |
| (14) | \(\lvert z\rvert^2 = \sum A_k^2 + 2\sum_{j<k}A_jA_k\cos((\omega_j-\omega_k)t+\varphi_j-\varphi_k)\) | SymPy 0 (N = 3, all symbols free). | verified |
| (15) | \(\langle\lvert z\rvert^2\rangle_t = \sum A_k^2\) (all \(\omega_k\) different) | Integrated over one period in SymPy for \(\omega = (1,-4,6), (4,-2,7), (1,5,-9)\): \(A_1^2+A_2^2+A_3^2\). With equal frequencies the average is \(A_1^2+A_2^2+2A_1A_2\cos(\varphi_1-\varphi_2)\), so the condition is needed. | verified |
| (16) | \(p\leftarrow p+\alpha(q-p) \Rightarrow p^{(m)}-q = (1-\alpha)^m(p^{(0)}-q) \approx e^{-\alpha m}(\ldots)\) | `rsolve`: \(q + (1-\alpha)^m(p_0-q)\). \(\ln(1-\alpha) = -\alpha - \alpha^2/2 - \ldots\), so the ≈ holds for small α. Code `morphStep()` (l. 863–869) is this recurrence. Limit α = 1: immediate. | verified |
| (17) | \(s = 0.44\min(w,h)/\max(R,0.05)\times\text{zoom}\) | Code `baseScale()·zoom` and `finalScale()` (l. 1060–1065). Units px per plane unit. Triangle inequality: every joint and circle edge lies within \(\sum_m A'_m\) of 0, so with \(R\ge\sum A'\) everything sits within \(0.44\min(w,h)\) of the centre. Floor 0.05 avoids \(R\to0\). Measured: scale 132.22 px at 1440 px. | verified |

## Numbers, section by section

| § | Number in the note | Recomputed / measured | Verdict |
|---|---|---|---|
| 1 | Ptolemy about 150 CE, Kepler's ellipses 1609, "about fourteen centuries" | Almagest c. 150 CE, *Astronomia nova* 1609; the span is 1459 years, about 14½ centuries. | verified |
| 1 | Socket arrow 325 V, fifty turns a second | \(230\sqrt2 = 325.3\) V; 50 Hz mains. | verified |
| 1 | Three phases a third of a turn apart sum to zero | \(1 + e^{2\pi i/3} + e^{4\pi i/3} = 0\). | verified |
| 2.1 | Speed equals distance, 1 | \(\lvert\mathrm{d}z/\mathrm{d}\theta\rvert = \lvert z\rvert = 1\). | verified |
| Fig. 1 | θ = 50°; arrow, arc, sine and cosine curves | SVG: tip (229.3, 73.4) = centre + 100(cos 50°, −sin 50°); arc end (184.3, 127.0); dashed carry-over at x = 404.4 = 360 + 320·50/360; sine and cosine paths within 0.11 px of \(150-100\sin\), \(150-100\cos\). Cosine "a quarter turn earlier": \(\cos\theta = \sin(\theta+\pi/2)\). | verified |
| 3 | Radius 0 to 2, ω −32 to 32 rad/s, phase 0 to 6.28 rad, steps 0.01 | `ctl('amp',…,0,2)`, `ctl('freq',…,-32,32)`, `ctl('phase',…,0,6.28)`, `step="0.01"` (l. 971, 978–980). | verified |
| Fig. 2 | Spirograph, t = 0.30 s, A = 1, 0.62, 0.34, ω = 1, 7, −13, φ = 0, 0, 0.5, period 2π s | Preset l. 677 matches. SVG at 84 px/unit: \(z_1\) (300.2, 155.2), \(z_2\) (274.0, 110.2), pen (246.3, 102.9), radii 52.1 and 28.6 px, θ-arcs, all equal to (6) at t = 0.30 s within 0.05 px; the 801-point curve lies within 0.07 px of the true curve. gcd(1, 7, 13) = 1 → 2π s. Legend "7 times as fast", "13 times as fast, backwards". | verified |
| 3.1 | Arm velocity size \(A_k\lvert\omega_k\rvert\) at right angles | From (7), SymPy. | verified |
| 3.1 | \(e^{it}+e^{-it} = 2\cos t\) stops at its ends | SymPy; \(\dot z = -2\sin t = 0\) at \(t = k\pi\), where \(z=\pm2\). | verified |
| 3.1 | Opposite velocities come round once per \(2\pi\) change of the angle between arms | Angle between the two velocity vectors is \((\omega_1-\omega_2)t\) + constant. | verified |
| 3.1 | Trefoil A = 1, 0.5; ω = 1, −2; tip speeds 1; angle grows at 3 rad/s; three stops \(2\pi/3\) s apart; deltoid | Preset l. 674. \(1\cdot1 = 0.5\cdot2 = 1\). \(\dot z = 0\) exactly at \(t = \pi/6 + 2\pi k/3\) (SymPy, k = 0, 1, 2). Deltoid = hypocycloid with R = 3r: \(2r e^{it} + r e^{-2it}\), r = 0.5. | verified |
| 4 | Length rises and falls at the full difference rate (new) | \(\lvert\cos(\Delta\omega t/2)\rvert\) has period \(2\pi/\lvert\Delta\omega\rvert\) (numerically \(2\times10^{-15}\)), the cosine itself \(4\pi/\lvert\Delta\omega\rvert\). | verified |
| 4.1 | n petals for odd n, 2n for even n; \(\cos n(\theta+\pi) = (-1)^n\cos n\theta\); odd n retraces, even n adds n new (new) | Identity: SymPy 0 for n = 1…6. Counting distinct petal tips over \(0\le\theta<2\pi\): 1, 4, 3, 8, 5, 12 for n = 1…6. | verified |
| 4.1 | 3-petal ω = 4, −2 → \(\bar\omega=1\), \(\Delta\omega=6\), n = 3; 4-petal ω = 3, −1 → n = 2, 4 petals; 8-petal ω = 5, −3 → n = 4, 8 petals | Presets l. 670–672; arithmetic. | verified |
| 4.1 | Phases −π/2, +π/2 turn the cosine into a sine, rotating the rose by \(\pi/(2n)\) | SymPy: \(z = 2A\sin(\Delta\omega t/2)e^{i\bar\omega t}\); \(\sin n\theta = \cos n(\theta - \pi/(2n))\). | verified |
| 4.1 | The pen passes through the centre once per petal | Zeros of \(r\) per period of the trace: n (odd) and 2n (even). | verified |
| 4.2 | Beating pair A = 1.1, ω = 5, 6, φ = 0, 0.1 | Preset l. 673. | verified |
| 4.2 | \(\bar\omega = 5.5\) rad/s, once every 1.14 s | \(2\pi/5.5 = 1.1424\) s. | verified |
| 4.2 | Envelope period \(2\pi/\lvert\Delta\omega\rvert = 6.28\) s | 6.2832 s. | verified |
| 4.2 | Forks at 440 and 442 Hz beat twice a second | 2 Hz. | verified |
| Fig. 3 | 0 ≤ t ≤ 20 s in steps of 0.025 s | 801 points per path, x step 31.7 px per s × 0.025 s; at \(t_i = 0.025\,i\) the three paths are within 0.09 px of Re z and ±\lvert z\rvert from (6). | verified |
| Fig. 3 | ±\lvert z\rvert agrees with (10) to \(2\times10^{-14}\) | Max over the 801 times in float64: \(1.92\times10^{-14}\). | verified |
| Fig. 3 | Fast period 1.14 s, envelope 6.28 s, centre passes at t = 3.04, 9.32, 15.61 s | \(t/2+0.05 = \pi/2 + k\pi\) → \(t = \pi - 0.1 + 2\pi k\) = 3.0416, 9.3248, 15.6080. Dashed lines at x = 160.4, 359.6, 558.8 px → 3.04, 9.32, 15.61 s. | verified |
| 4.2 | \(\lvert z\rvert\) between \(\lvert A_1-A_2\rvert\) and \(A_1+A_2\); Trefoil 0.5 to 1.5 | From (11). | verified |
| Ex. 4.1 | Speed 1.00×; \(\lvert z(t)\rvert\) readout starts at 2.197 | Default speed 1. Chromium: first readout "2.197"; \(2.2\cos 0.05 = 2.19725\). | verified |
| Ex. 4.1 | Falls to zero near t = 3.04 s | Chromium, store `absz` per frame: minimum 0.0091 at t = 3.033 s (frame spacing 0.017 s); readout "0.009" at "t = 3.03 s". | verified |
| Ex. 4.1 | Back near 2.2 at 6.18 s | Store maximum 2.19999 at t = 6.183 s; \(2\pi - 0.1 = 6.183\). | verified |
| Ex. 4.1 | Circle 2 at 5.50 → beat period 12.57 s | \(2\pi/0.5 = 12.566\); the Period readout also shows "12.57 s". | verified |
| Ex. 4.1 | Circle 2 at 5.00 → \(\lvert z\rvert\) stays 2.197 | Chromium: \(\lvert z\rvert\) min = max = 2.1972506 over 1.5 s; readout "2.197". | verified |
| 5 | 3-petal rose g = gcd(4, 2) = 2 rad/s, closes after π s = 3.14 s | `structure()`: G = gcd(400, 200) = 200; readout "3.14 s". | verified |
| 5 | Every other preset g = 1 rad/s, 6.28 s | Chromium, all ten presets: rose4, rose8, beat, trefoil, star, epicycle, spirograph, galaxy, flower all "6.28 s". | verified |
| 5 | Irrational ratio (1 and √2): never closes, dense in the ring \(\lvert A_1-A_2\rvert\) to \(A_1+A_2\) | Kronecker: \((t, \sqrt2 t)\) mod \(2\pi\) is dense on the torus, and the torus maps onto the ring by (11). | verified |
| 5 | \(e^{it}-e^{it}+e^{2it} = e^{2it}\) repeats after π s; listed frequencies 1 and 2 rad/s give \(T = 2\pi\) s; the readout uses every arm with A > 0 (new) | Identity trivial; gcd(1, 2) = 1. Code `if (p.amp > 0)` (l. 830). Chromium, three arms (1, 1, 0), (1, 1, 3.14), (1, 2, 0): Period readout "6.28 s". | verified |
| 5 | Steps of 0.01 rad/s, Euclid on \(100\,\omega_k\) | `Math.round(p.freq * 100)`, `gcd()` (l. 806–810, 830). | verified |
| 5 | −2.1 → g = 0.1 rad/s, T = 62.83 s; −2.01 → g = 0.01 rad/s, T = 628.32 s | gcd(400, 210) = 10; gcd(400, 201) = 1. Readouts "62.83 s" and "628.32 s". | verified |
| 5 | Petals \(\lvert\omega_1-\omega_2\rvert/g\): 3 and 61 | 6/2 = 3; 6.1/0.1 = 61. | verified |
| 5.1 | τ = 2π/M, β = 2π ω₁/M, q-fold for ω₁/M = p/q | Each factor \(e^{i\omega_k\tau}\) equal ⇔ \((\omega_j-\omega_k)\tau \in 2\pi\mathbb Z\); first at 2π/M; gcd(p, q) = 1 makes the multiples of p cover all residues mod q. Code `q = M / gcd(w[0], M)` is the same reduction. | verified |
| 5.1 | Star ω = 1, −4, 6: differences −5, 5, M = 5, 1/5, five-fold | Readout "5-fold". | verified |
| 5.1 | 3-petal rose M = 6, 4/6 = 2/3, three-fold | Readout "3-fold". | verified |
| Fig. 4 | \(t_i = iT/n\), n = 1500; T = π s and 2π s; 3-fold and 5-fold | 1501 points per path; at these \(t_i\) the paths lie within 0.08 px (rose) and 0.13 px (star) of (6). | verified |
| Fig. 4 | \(z(T)\) lands on \(z(0)\) to within \(3\times10^{-15}\) | Float64 with the page's wrapped phases: \(2.5\times10^{-15}\) (rose), \(2\times10^{-17}\) (star). | verified |
| Ex. 5.1 | 3.14 s and 3-fold; ten left-arrow presses → −2.10 | Chromium: keyboard ArrowLeft ×10 on Circle 2's slider → value "−2.1", store −2.1. | verified |
| Ex. 5.1 | 61 petals, 62.83 s, 7000 samples | Readouts "62.83 s", "61-fold"; Final view caption "final shape · 7000 samples"; round(10 · 700) = 7000. | verified |
| Ex. 5.1 | −2.50: 13 petals in 12.57 s; −3.00: 7 petals in 6.28 s | Readouts "12.57 s"/"13-fold" and "6.28 s"/"7-fold"; 6.5/0.5 = 13, 7/1 = 7. | verified |
| 6 | Star \(1^2+0.5^2+0.18^2 = 1.2824\); \(\lvert z\rvert^2 = 1.2824 + 1.36\cos5t + 0.18\cos10t\) | SymPy difference 0. Readout "1.282". | verified |
| 6 | Readout ⟨\lvert z\rvert²⟩ = ΣA² "at the foot of the controls" (new) | Chromium, 1440 px: the readout block is the last block of the controls column (x 958–1278), y 1991–2188, above only the three-line legend; the ⟨\lvert z\rvert²⟩ row is its last row. 390 px: same order, at y 3431–3486, below the figure and the circle cards. | verified |
| Fig. 5 | \(\lvert z\rvert^2\) between 0.1024 and 2.8224 | As a polynomial in \(c=\cos5t\): \(689/625 + 34c/25 + 9c^2/25\), stationary point \(c = -17/9\) outside [−1, 1]; ends 64/625 = 0.1024 and 1764/625 = 2.8224. SVG path within 0.08 px of (6). | verified |
| Fig. 5 | ΣA² = 1.2824; running average on 1.2824 at every multiple of \(2\pi/5 = 1.26\) s | Dashed level at y = 165.0 ↔ 1.2824; running average at m·2π/5, m = 1…5: 1.28240000000 (10⁶-step trapezoid). Grey SVG path within 0.16 px. | verified |
| Fig. 5 | "computed from (6) on \(10^6\) equal steps" | — | unverifiable, because the figure keeps only 1001 rounded points; they match a 10⁶-step computation to 0.16 px, but any grid finer than about 10³ steps would draw the same picture |
| 6 | Equal frequencies: readout 2.42, pen at 2.197, square 4.828 | \(2\cdot1.1^2 = 2.42\) (readout "2.420"); \(\lvert z\rvert^2 = 2.42(1+\cos0.1) = 4.8279\), \(\lvert z\rvert = 2.19725\). | verified |
| 7 | Δt capped at 50 ms; speed 0 to 4 | `Math.min((ts-last)/1000, 0.05)` in `Sim.clock`; slider `min="0" max="4"`. | verified |
| 7 | Angle rounding below \(10^{-11}\) rad for ω = 32 rad/s after 1000 s | Exact rational error of `w*t + phi` in float64 for 200 000 random t ≤ 1000, φ ≤ 6.28: max \(3.63\times10^{-12}\) rad, one ulp of 32 000. | verified |
| 7 | Trail length 100 to 6000, default 2400 = 40 s at 60 fps | Slider l. 120; store `trail_max` 2400; 2400/60 = 40 s. | verified |
| 7 | 3-petal rose chords stray at most 0.0007 (0.035 % of radius 2) at 1.00×; 0.011, sixteen times more, at 4.00× | Max distance from arc to chord over all segments of length 1/60 s and 4/60 s: 0.000694 (0.0347 %) and 0.01110; ratio 15.98; bound \(a_\perp h^2/8 = 20h^2/8\). | verified |
| 7 | Final shape: 700 samples per 2π s, clamped 1500 to 12 000; span at most 60 × 2π = 377 s; 628 s drawn in part; slider 1 to 24 × 2π s | `refinal()` l. 846, `spanNow()` l. 840. −2.01: store span 376.99 s, n = 12 000. | verified |
| 7 | Every preset gets n = 1500 | Chromium store `n_path` = 1500 for all ten presets. | verified |
| 7.1 | α from 0.02 to 0.35, default 0.08 | Slider l. 136. | verified |
| 7.1 | Time constant 12.0 frames = 0.20 s; below 1 % after 56 frames | \(-1/\ln0.92 = 11.993\); /60 = 0.1999 s; \(0.92^{55} = 0.0102\), \(0.92^{56} = 0.0094\). | verified |
| 8 | Canvas 770 × 601 at 1440 px; 132 px per unit for R = 2 | Chromium: box 770 × 601 (600.59), store `scale` 132.22, `fitR` 2. | verified |
| 8 | Chords miss the curve by 0.09 px at 1.00× and 1.5 px at 4.00× | 0.000694 × 132.22 = 0.092 px; 0.01110 × 132.22 = 1.47 px. | verified |
| 8 | Phone 390 px: canvas 356 × 356 | Chromium: 356 × 356. | verified |
| 8 | R relaxes with time constant 0.6 s; Zoom 1× to 0.3× | `fit()`: `(1 - Math.exp(-dt / 0.6))`; slider `min="0.3" max="1"`. | verified |
| 8 | Curve 1.8 px; twelve pieces, opacity 0.25 → 1; arm dot radius 3 px; pen radius 5.5 px; final view 1.8 px over 6 px band | `lineWidth = 1.8`; `chunks = 12`, `globalAlpha = 0.18 + 0.82(c+1)/12` = 0.248 … 1; `arc(nx, ny, 3)`; `arc(…, 5.5)`; `lineWidth = 6` with rgba(226,162,170,0.45) then 1.8. | verified |
| 8.1 | FFT 2048, 1024 bins, 21.5 Hz at 44.1 kHz; smoothing 0.8 | `fftSize = 2048`, `smoothingTimeConstant = 0.8`; 44100/2048 = 21.53 Hz (headless Chromium's default rate is 44 100 Hz). | verified |
| 8.1 | Bands 20–150, 150–4000, 4000–16 000 Hz; bass bins 1 to 7; /255; \(e \leftarrow e + 0.15(e_\text{raw}-e)\) | `band()` l. 908: max(1, ⌊20/21.53⌋) = 1, ⌈150/21.53⌉ = 7; `/ 255`; `* 0.15`. | verified |
| 8.1 | Bass arms: \(A' = A[1 + \text{ease}(\text{bass})d_\text{bass}(1-0.7\lvert\omega\rvert/\lvert\omega\rvert_\max)]\) for \(\lvert\omega\rvert\) ≤ median; treble arms \(A(1+\text{high}\,d_\text{high})\); mid multiplies Δt by \(1+\text{mid}\,d_\text{speed}\) | `buildLive()` l. 945–947, `speedFactor()` l. 957. Measured with the CSP bypassed (see the method table): mul of Star's arms 1.0156, 1.0094, 1.0000 before a beat. | verified |
| 8.1 | Beat: raw bass > 1.35 × previous frame, > 0.22, and at least 280 ms since the last beat | `rb > prevBass * 1.35 && rb > 0.22 && now - lastBeat > 280` (strictly more than 280 ms; no practical difference). | verified |
| 8.1 | On a beat all radii are multiplied by \(1 + d_\text{burst}\), falling back linearly to 1 over 10 frames | — | wrong, because `analyse()` sets `burst = 1 + dBurst.value` and `burstFrames = 10`, and a few lines later, in the same call and before `buildLive()` reads it, decrements `burstFrames` to 9 and overwrites `burst = 1 + dBurst.value · 9/10`. Measured in Chromium (CSP bypassed, default d_burst = 0.60, a 60 Hz beat every 500 ms): the beat frame carries 1.5400 on all 16 beats, then 1.48, 1.42, …, 1.06, and 1.0000 on the tenth frame; 9 frames above 1. Correct: "multiplied by \(1 + 0.9\,d_\text{burst}\), falling by \(0.1\,d_\text{burst}\) each frame, back to 1 on the tenth frame" (or change the code so the beat frame keeps \(1 + d_\text{burst}\)) |
| 8.1 | Tempo = 60 000 / median of the last 8 intervals in ms | l. 919–922. Measured (CSP bypassed): beats 500 ms apart → "120 BPM". | verified |
| 8.1 | Record: first frame at least 50 ms after the last snapshot; every third or fourth frame at 60 fps; 58 ms apart on average (new) | `recAcc += real; if (recAcc >= 0.05) { recAcc = 0; push }`. Chromium, three 15 s recordings: 3.50, 3.52, 3.54 frames per snapshot; mean 58.9, 59.3, 59.1 ms (rAF mean 16.9 ms); intervals of 3 frames 112–124 times, 4 frames 126–142 times, 5–6 frames 1–5 times. At exactly 16.67 ms per frame, 3.5 frames = 58.3 ms. | verified |
| 8.1 | Replay moves each value, every frame, the fraction \(\Delta t/(50\ \mathrm{ms})\) toward the stored list (new) | `al = Math.min(1, dt / 0.05)` with `dt = real` ≤ 0.05 s. Chromium: Circle 1 radius 2 → stored 1; ratio of successive gaps 0.640–0.674 against \(1 - \Delta t/0.05\) = 0.666–0.668. | verified |
| 9 | Period readout assumes ω in multiples of 0.01 rad/s | `Math.round(100 ω)`. | verified |
| 9 | All active circles at one ω → Symmetry "0-fold" | Chromium: 3-petal rose with Circle 2 set to 4 → "0-fold" (M = 0, q = 0). With only one active circle the readout shows "∞ (circle)" instead, and when equal-ω arms cancel the curve is a point, not a circle (that case measured \(\lvert z\rvert\) = 0.000). | verified (for two or more active circles) |
| 9 | Meters respond twice as fast at 120 Hz as at 60 Hz | Per-frame factor 0.15: time constant \(-1/\ln0.85 = 6.15\) frames = 0.10 s at 60 Hz, 0.05 s at 120 Hz. | verified |

## The numerical method, against the code

| Note says | Code | Verdict |
|---|---|---|
| §7: nothing is integrated; each frame t advances by Δt·s, then (6) is evaluated | Clock callback l. 1325–1327: `t += dt * lastSpeed; sumAt(t, live)`. Only in the Live view (`mode === 'live'`); in the Final shape view t stands still, which the note does not say. | verified |
| §7: live trail = pen position at the end of each frame, newest *Trail length* points, joined by straight segments | l. 1328–1330, `polyline()`. | verified |
| §7: Final shape samples \(t_i = i\,T_\text{span}/n\), n + 1 points | `refinal()` l. 846–851. | verified |
| §7: period and symmetry from integer gcds of round(100 ω), A = 0 left out | `structure()` l. 828–836. Also recomputed every 0.1 s in `readouts()`. | verified |
| §7.1: new exact samples at once, drawn points move the fraction α per frame; a change of sample count snaps; Smooth morphing off → α = 1 | `edited()` → `refinal(false)`; `morphStep()`; snap when `morphPath.length !== finalPath.length` or the switch is off. | verified |
| §7.1: "The curves drawn in between are point-by-point blends of the old and the new curve, not the curves of the in-between slider settings." (new) | (6) is linear in each \(A_k\). | wrong, because for the *Radius* slider the point-by-point blend **is** the curve of an in-between setting: \((1-\lambda)z_\text{old} + \lambda z_\text{new}\) is (6) with \(A_k\) replaced by \(A_k^\text{old} + \lambda(A_k^\text{new} - A_k^\text{old})\), \(\lambda = 1-(1-\alpha)^m\). Measured in Chromium: Star, Circle 2 radius 0.50 → 1.00 in the Final view; after 10 frames the drawn path equals the exact curve with \(A_2 = 0.5 + 0.5(1-0.92^{10}) = 0.78281\) to \(6.7\times10^{-16}\). For ω (−4 → −3.5) and φ (0 → 1.5) the best in-between value misses by 1.25 and 0.13 units, so the sentence holds only for those sliders. Correct: "For a change of radius the in-between curves are those of in-between radii; for a change of frequency or phase they are blends that no in-between setting draws." |
| §8: pixel = \((c_x + s x, c_y - s y)\); R in Live = max(ΣA′, farthest trail point), grows at once, relaxes over 0.6 s; Final R = largest \lvert z\rvert as drawn | `polyline()`, `reach()`, `fit()`, `finalScale()`. | verified |
| §8.1: music rescales only copies \(A'_k\); stored A, ω, φ untouched | `buildLive()` builds `live` from `phasors` with `amp * mul`; nothing writes back. (Replay, not the music, does change the stored values.) | verified |
| §8.1: "An audio file you choose stays in your browser and is played through the Web Audio analyser", and Record times snapshots "against the audio time" | `loadAudio()` sets `audio.el.src = URL.createObjectURL(file)`, a `blob:` URL. The page's own CSP meta tag (l. 5) is `default-src 'self'` with no `media-src`, so `blob:` media is refused. | wrong, because the browser never plays the file. Measured in Chromium on the local build and on https://phyeinusul.com/simulations/phasor-sums: console "Refused to load media from 'blob:…' because it violates the following Content Security Policy directive: "default-src 'self'"", and over 8 s with Auto Dance on, bass, mid and high stay 0.000, burst 1, BPM 0. So Auto Dance does nothing, and `recTime()` always falls back to the wall clock since Record was pressed (the audio is never "playing"). The description matches the JavaScript (it works with the CSP bypassed, rows above), so the fault is the page's CSP, which needs `media-src 'self' blob:`; until then the note describes a feature the page does not have. The CSP is the same in db1a24b, so this is not from the latest edit |

## References and links

| Reference | Link and road | Cited chapter | Verdict |
|---|---|---|---|
| Feynman, Leighton, Sands, *FLP* Vol. I, ch. 22 and 48 | `I_22.html`, `I_48.html`: curl 403 (Cloudflare "Attention Required"), headless Chromium 403 too; Firecrawl scrape: status 200, titles "Vol. I Ch. 22: Algebra" and "Vol. I Ch. 48: Beats". | Ch. 22 "Algebra", last section 22–6 "Imaginary exponents" ends with \(e^{i\theta} = \cos\theta + i\sin\theta\), "our jewel". Ch. 48 "Beats". | verified |
| Needham, *Visual Complex Analysis*, OUP 1997; 25th anniversary edition 2023 | OUP page: curl 202 with an empty body; headless Chromium: page opens, "Visual Complex Analysis 25th Anniversary Edition", paperback published 28 February 2023, ISBN 9780192868923. | Table of contents on that page: "1. Geometry and Complex Arithmetic". | verified |
| Hecht, *Optics*, 5th ed., Pearson 2017 | Pearson page: curl 200, "Optics, 5th edition … © 2017 Eugene Hecht". | Same page lists "7: The Superposition of Waves". Sections from Pearson's own table of contents (pearson.de PDF for the 5th Global Edition, via Firecrawl after curl was reset): "7.1. The Addition of Waves of the Same Frequency", "7.2. The Addition of Waves of Different Frequency". | verified |
| Kuhn, *The Copernican Revolution*, Harvard 1957 | HUP page: curl 200, title "The Copernican Revolution — Harvard University Press", ISBN 9780674171039. | The HUP page has no contents list; the contents in several catalogue listings (Perlego, eBay, course PDFs, found by Firecrawl search) give "Chapter 2: The Problem of the Planets", and its text treats the epicycle–deferent system. | verified |

## Summary

Rows: 17 equations, 74 numbers, 9 method statements, 4 references (104 rows).

**100 verified / 3 wrong / 1 unverifiable.**

Wrong: the beat-burst multiplier in §8.1 (1 + 0.9 d_burst, back to 1 on the tenth frame, not 1 + d_burst over 10 frames);
the new §7.1 sentence on in-between curves (false for the Radius slider); and Auto Dance as served (the page's CSP blocks the
`blob:` audio, so no file plays and Record never uses audio time; a page bug, not a fault in the note's description of the code).
Unverifiable: the 10⁶ steps behind Figure 5.

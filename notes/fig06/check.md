# Fig. 6 lecture note: independent check

Page: `public/simulations/wave-interference.html`, the note between `<article class="paper" id="paper">` and `</article>`, as of the working tree on
branch `claude/physics-notes-rewrite-cwctkk`, 20 October 2026, with the uncommitted edit (`git diff HEAD`) included. I did not read `plan.md`
or any other file in `notes/fig06/` except this one.

How it was checked:

- **Equations.** Re-derived in SymPy 1.14 (`derive.py`), with numbers from NumPy/mpmath (`numerics.py`). The figure curves were parsed out of the SVG
  and compared with the formulas (`svgcheck.py`).
- **Page numbers.** Measured in headless Chromium 1194 (Playwright) on my own build: `APPDEPLOY_VITE_OUT_DIR=/tmp/fig06-check-dist npm run build`.
  The built page and `sim.js` are byte-identical to the sources. They were served by a small Node static server on `localhost:8766` (`measure.cjs`).
  Windows used: 1440 × 900 at DPR 1, and 390 × 844 at DPR 3. Values were read from the page's store `Sim.data.ds`, from its own `Sim.data.check`
  functions, and from the visible readouts.
- **Links.** Opened with curl first. Where curl got a Cloudflare challenge, I opened the page with Firecrawl scrape (`maxAge: 0`).
- **Where the scripts are.** All the scripts and their outputs are in
  `/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/f6/`. The browser output is in `js/m1.json` there.

## Equations

| # | Equation | Verdict | How checked |
|---|---|---|---|
| E1 | (1) \(y_i = A_i\sin(2\pi f_i(X/200 - s_i t)+\varphi_i)\) | verified | Same expression as the code: `y()` is `w.A*Math.sin(2*Math.PI*w.f*(X/200 - w.s*simT) + w.phi)`. It also matches the Fig. 6 caption. Units hold when X is read in px and t in s, as the text says. |
| E2 | (2) \(k_i=2\pi f_i/200\), \(\lambda_i=200/f_i\), \(\omega_i=2\pi f_is_i\), \(\nu_i=f_is_i\), \(v_i=200s_i\) | verified | SymPy: the phase equals \(k_iX-\omega_it+\varphi_i\) identically. The code's `kw`, `lamw`, `omw`, `nuw` and `vw` lines use the same formulas. Units: rad/px, px, rad/s, Hz, px/s. |
| E3 | (3) wave equation, \(v_i=\omega_i/k_i\), and the changed sentence before it ("comes back as minus itself, times \(\omega_i^2\) … \(k_i^2\)") | verified | SymPy: \(y_{tt}=-\omega^2y\), \(y_{XX}=-k^2y\), and \(y_{tt}-v^2y_{XX}=0\). Limit s = 0: v = 0 and \(y_{tt}=0\), a wave that stands still. Units px/s² on both sides. |
| E4 | (4) linearity of \(\mathcal L=\partial_t^2-v^2\partial_X^2\) | verified | SymPy, with arbitrary functions \(y_1, y_2\). |
| E5 | (5) phasor sum \(C e^{i\psi}=A_1e^{i\varphi_1}+A_2e^{i\varphi_2}\) | verified | SymPy: \(\operatorname{Im}[e^{i\theta}(\dots)]\) equals the sum of the two sines identically. |
| E6 | (6) \(C^2=A_1^2+A_2^2+2A_1A_2\cos(\varphi_1-\varphi_2)\) | verified | SymPy (\(|Z|^2\)). Limits: in step gives \(A_1+A_2\); half a turn apart gives \(|A_1-A_2|\). |
| E7 | (7) sum-to-product | verified | SymPy `expand_trig`. Limit a = b gives \(2A\sin a\). |
| E8 | (8) \(\lambda_\text{beat}=2\pi/|\Delta k|=200/|f_1-f_2|\), \(T_\text{beat}=1/|\nu_1-\nu_2|\) | verified | SymPy. \(|\cos|\) has period π, so \(a-b\) must grow by 2π. Limit \(f_1\to f_2\) gives \(\to\infty\): the beat stops, which the page shows (stored `bl` becomes NaN). |
| E9 | (9) \(v_\text{env}=200\frac{f_1s_1-f_2s_2}{f_1-f_2}\), \(v_\text{carrier}=200\frac{f_1s_1+f_2s_2}{f_1+f_2}\) | verified | SymPy from (2). A point of fixed envelope moves at Δω/Δk (solved). Limit \(s_1=s_2\): both become 200 s. The formula matches the code's `venv` line. |
| E10 | (10) square-wave series | verified | SymPy, the full integral over (−π, π): \(b_{1..7}=4/\pi,0,4/3\pi,0,4/5\pi,0,4/7\pi\), and every \(a_n=0\). The half-period-shift argument for missing even harmonics was checked for n ≤ 9. |
| E11 | (11) \(\sum 30/n\,\sin nx\approx H\operatorname{sq}(x)\), \(H=23.56\) px | verified | \(H=30\pi/4=23.5619\). The page's wave of Frequency 0.4n is exactly \(\sin nx\) with \(x=2\pi\cdot0.4(X/200-t)\) (SymPy). |
| E12 | (12) orthogonality | verified | SymPy, general integers: Piecewise(0 for m ≠ n, π for m = n). The sin·cos integral is 0 (checked for m, n ≤ 8). The product-to-sum identity in the text was checked too. |
| E13 | (13) \(b_m=\frac1\pi\int F\sin mx\,dx\) | verified | SymPy on a general series with \(a_0..a_5\) and \(b_1..b_5\). |
| E14 | (14) \(b_n=2(1-\cos n\pi)/(n\pi)\) | verified | SymPy: \(2(1-(-1)^n)/(\pi n)\), so 4/(nπ) for odd n and 0 for even n. |
| E15 | (15) \(dS_N/dx=\frac4\pi\sum\cos(2k-1)x=\frac2\pi\frac{\sin2Nx}{\sin x}\) | verified | SymPy: the telescoping identity \(2\sin x\cos(2k-1)x=\sin2kx-\sin(2k-2)x\) holds, and the closed form holds for N = 1…7. Limit x → 0 gives 4N/π, which equals (4/π)·N. |
| E16 | (16) \(S_N(\pi/2N)\to\frac2\pi\mathrm{Si}(\pi)=1.17898\) | verified | mpmath: \(1.1789797\). The exact integral gives 1.273240 (N = 1), 1.200422 (N = 2), 1.184225 (N = 4), 1.179814 (N = 10), 1.178988 (N = 100) and 1.178980 (N = 1000). N drops out in the limit. |
| E17 | (17) \(C_\nu=|\sum_{\nu_i=\nu}A_ie^{i\varphi_i}|\) | verified | SymPy: the waves of one ν at X = 0 sum to \(\operatorname{Im}[e^{-i\omega t}\sum A e^{i\varphi}]\). `lines()` implements this with `Math.hypot(re, im)`, and with \(|\sum A\sin\varphi|\) at ν = 0, as the text says. |
| E18 | (18) \(\overline{y^2}=\frac12\sum C_\nu^2\) (no stem at ν = 0) | verified | SymPy: the mean over one common period of three sines with distinct ν is \((C_1^2+C_2^2+C_3^2)/2\). Units px². |
| E19 | (19) triangle inequality | verified | Standard. Equality only when all the crests coincide. The page's `r-sum` readout is `sum_A`. |
| E20 | (20) \(R\), \(R_c\), \(y_\text{screen}=y_\text{mid}-\frac yR\frac h2\) | verified | Same as `nice()`, `sumRange`, `compRange` and the `py` lines of `draw()`. Measured R = 60 and R_c = 30 for the preset. Limit y = ±R lands on the panel edges. |
| E21 | Unnumbered energy derivation (changed lines): string KE \(\frac12\mu y_t^2\), PE \(\frac12Ty_X^2\); one-way wave gives KE = PE; mean KE of one harmonic \(\frac14\mu\omega_n^2A_n^2\), total \(\frac12\mu\omega_n^2A_n^2\); \(\overline e=\frac12\mu\sum\omega_n^2A_n^2\) | verified | SymPy: for \(y=F(X-vt)\), \(y_t=-vy_X\), and with \(T=\mu v^2\) KE = PE identically. One harmonic, averaged over a period: KE = \(\mu\omega^2A^2/4\) and KE + PE = \(\mu\omega^2A^2/2\). Three harmonics (1, 3, 5) with arbitrary phases: \(\overline e=\frac12\mu\omega_0^2(B_1^2+9B_2^2+25B_3^2)\), so the cross terms vanish. Units: kg/m · s⁻² · m² = J/m (sympy.physics.units). |

## Numbers, in the order they appear

| # | Where | Claim | Verdict | How checked |
|---|---|---|---|---|
| N1 | §1 | 110 and 111 vibrations a second give one swell per second | verified | Equation (8). |
| N2 | §1 | up to six waves | verified | `MAX_WAVES = 6`. The Add button is disabled at 6. |
| N3 | §2 | 800 px in view, so \(4f_i\) wavelengths; four at the default Frequency 1 | verified | `WORLD_W = 800`, and 800/(200/f) = 4f. The default wave has f = 1. |
| N4 | §2 | the Phase slider covers 0 to about 2π | verified | min 0, max 6.28, step 0.05. In Chromium the highest reachable value is 6.25 rad = 0.995 × 2π. |
| N5 | Fig. 1 | curve, \(A_i\), \(\lambda_i\), \(A_i\sin\varphi_i\), shifted copy | verified | Least-squares fit to the SVG paths: A = 70.00, φ = 0.600 rad, λ = 240 units (residual 0.05). The marker sits at the height \(A\sin\varphi\) (120.5) and the arrow at the crest (x = 147.1). The pale copy is the same sine moved 36 units to the right. |
| N6 | §3.1 | One wave, then Add wave +: a copy at 20 px, 1.00, 1×; the sum doubles to 40 px; one stem of 40 px | verified | Measured: A = [20, 20], f = [1, 1], s = [1, 1], `nu_line` = [1], `A_line` = [40]. Readouts: "40.0 px" sum, "40.0 px" peak. |
| N7 | §3.1 | phase step 0.05 rad; nearest step to π is 3.15 rad; it misses by 0.0084 rad | verified | Setting 3.14159 snaps to 3.15, labelled "1.00 π". 3.15 − π = 0.00841. |
| N8 | §3.1 | the sum is then 0.17 px; Peak reads 0.2 px | verified | (6): 40·\|cos(1.575)\| = 0.16815. Measured `A_line` = 0.168146, peak 0.168146, readout "0.2 px". |
| N9 | Fig. 2 | phasor diagram | verified | From the SVG: \(A_1=150\) at 25.0°, \(A_2=100\) at 80.0°, C drawn as 222.96 at 46.6°. (6) gives C = 222.95. The heights at the right are \(A_1\sin\varphi_1=63.4\) and \(C\sin\psi=161.9\). |
| N10 | §4 | Beats preset: Amplitude 18 px, Speed 1×, Frequencies 1.00 and 1.25 | verified | Stored A = [18, 18], s = [1, 1], f = [1, 1.25]. |
| N11 | §4 | \(\lambda_\text{beat}\) = 800 px (one beat across the view); 4 s at a fixed point | verified | Stored `bl` = 800. The page's own repeat time `Sim.data.round.length()` = 4 s. |
| N12 | §4 | carrier 1.125 Hz; nine carrier oscillations in two beats | verified | 8 s × 1.125 Hz = 9. |
| N13 | Fig. 3 | sum at X = 400 px every 0.01 s from 0 to 8 s; envelope \(\pm36\|\cos(\pi(t-2)/4)\|\); zero at 0, 4 and 8 s; 36 px halfway | verified | SymPy: at X = 400, \((a-b)/2=\pi(t-2)/4\). From the SVG: 801 points spaced 0.01 s. The sum curve deviates from the formula by at most 0.025 px, the envelope by 0.027 px; both are within the SVG's 0.1-unit rounding. The envelope encloses the sum at every sample, with zeros at exactly 0, 4 and 8 s. |
| N14 | Ex. 4.1 | Frequency 1.10: one beat every 10 s, 2000 px, 2.5 views; at 1.00 it stops | verified | Measured `bl` = 2000.0 and round = 10 s. At 1.00, `bl` and `venv` are undefined (NaN). |
| N15 | Ex. 4.1 | Speed 0.50×: waves at 200 and 100 px/s; envelope 300 px/s to the left; carrier 144 px/s to the right; Data panel symbol \(v_\text{env}\) | verified | Measured v = [200, 100] and `venv` = −300. (9) gives a carrier of 144.44. The store's symbol for `venv` is `v_env`. |
| N16 | §4.1 | deep water: \(\omega=\sqrt{gk}\) gives \(v_g=v_p/2\); crests run forward through the group | verified | SymPy: \(\frac{d\omega/dk}{\omega/k}=\frac12\). Since \(v_p>v_g\), crests appear at the back and die at the front. |
| N17 | §4.1, changed lines | "On this bench, though, you set each speed by hand, so the envelope is only the place where crests happen to fall into step. Nothing travels with it, which is why it is free to run backwards faster than either wave." | wrong, because the reason given does not hold. Running backwards faster than either wave is not a sign that nothing travels. The exercise's two waves, \((k,\omega)=(2\pi/200,\,2\pi)\) and \((2\pi\cdot1.25/200,\,2\pi\cdot0.625)\), lie on a chord of slope −300 px/s. A lossless medium whose \(\omega(k)\) falls with k there, a backward-wave medium such as the optical branch of a two-atom chain, has exactly this negative group velocity, and its energy really does run backwards with the envelope. Group speeds above the phase speed also occur in real media (capillary waves, \(v_g=1.5\,v_p\)). Correct statement: the bench has no medium, so nothing carries energy, and the envelope speed follows only from the two (k, ω) pairs you choose. In a real medium the same envelope would need a dispersion relation that falls with k there, and the energy would go with it. | Physics argument; the numbers are from (9). The previous sentence ("for waves that lose no energy … any slow signal, travels") is verified. |
| N18 | §5 | Square preset: Frequencies 0.4, 1.2, 2.0, 2.8; Amplitudes 30, 10, 6, 4.3 (30/7 = 4.29); Phase 0; Speed 1× | verified | Stored values match. The code is `Math.round(30/n*10)/10` and `n*2/5`. |
| N19 | §5 | \(H=\frac\pi4\times30=23.56\) px | verified | 23.5619. |
| N20 | §5 | wavelength 500 px; 1.6 of them in view; repeats every 2.5 s | verified | 200/0.4, 800/500, 1/0.4. |
| N21 | §5 | n = 9 would need Frequency 3.6, above the slider's top value of 3 | verified | `FMAX = 3`. |
| N22 | §5 | one term rises 27 % above the plateau | verified | (30 − H)/H = 27.32 %. Note: the table's 13.66 % is the same overshoot measured against the jump 2H. |
| N23 | §5, §5.2 | overshoot 8.95 % of the jump, 4.22 px above the plateau, limit 27.78 px | verified | (1.178980 − 1)/2 = 8.949 %; 0.178980·H = 4.217 px; 1.178980·H = 27.779 px. |
| N24 | Fig. 4 | partial sums at t = 0, every 1 px over 0–500 px; 1 term, the preset (30, 10, 6, 4.3), 10 terms (30/n, n ≤ 19); dashed H = 23.56; dotted ±27.78; label "27.8 px" | verified | From the SVG: 501 points each. The largest deviation from the formula is 0.023, 0.021 and 0.021 px (the axis ticks themselves are rounded to 0.1 unit). The dashed levels are ±23.56; the dotted lines sit at ±27.78. |
| N25 | §5.1 eqnote | trapezoid rule on 2 000 001 points: \(b_1=1.273240\), \(b_3=0.424413\), \(b_5=0.254648\), \(b_2=b_4=0\) | verified | NumPy `trapezoid`: 1.273240, 0.424413, 0.254648, 0.000000, 0.000000, equal to the exact values to six decimals. |
| N26 | §5.2 | first crest at \(x=\pi/2N\), i.e. \(X=125/N\) px | verified | SymPy solve. On a 0.01 px grid the peaks sit at 125.00, 41.67 (3 terms), 31.25 (4), 12.50 (10) and 1.25 px (100), or at their mirror images. |
| N27 | §5.2 | 1.17898 | verified | See E16. |
| N28 | table, row 1 | 1 term: 30.00 px, 13.66 % | verified | 0.01 px grid: 30.0000 and 13.662 %. |
| N29 | table, row 2 | 3 terms (n ≤ 5): 28.00 px, 9.42 % | verified | 28.0000 and 9.418 %. |
| N30 | table, row 3 | 4 terms (preset): 27.91 px, 9.22 % | verified | 27.9081 and 9.223 %, with the preset's 4.3 px. With the exact 30/7 of (11) it would be 27.90 and 9.21; the row is labelled "preset", so the preset values are right. |
| N31 | table, row 4 | 10 terms: 27.80 px, 8.99 % | verified | 27.7987 and 8.991 %. |
| N32 | table, row 5 | 100 terms: 27.78 px, 8.95 % | verified | 27.7793 and 8.949 %. |
| N33 | table, row 6 | limit: 27.78 px, 8.95 %; jump 2H = 47.12 px | verified | 27.7791, 8.949 %, 47.1239. |
| N34 | §6 | Parseval for the preset: \(\frac12(30^2+10^2+6^2+4.3^2)=527.2\) px²; \(H^2=555.2\) px²; about 95 % | verified | 527.245; 555.165; ratio 0.94971. |
| N35 | §6 eqnote | the mean of \(y^2\) at X = 0 over 2.5 s on 250 000 points is 527.2450 px² | verified | Run in Chromium with the page's own `Sim.data.check.y_comp` (its `yAt`) on the stored preset, t = j·2.5/250 000: 527.245000000002. |
| N36 | §6, changed lines | every odd harmonic carries the same energy; in the preset to within 0.7 % | verified | \((\omega_nA_n)^2 \propto (0.4n\,A_n)^2\) = 144, 144, 144, 144.96. The largest difference is 0.668 % (Wave 4, from 4.3 instead of 4.2857). |
| N37 | §6, changed lines | "the endless sum diverges: a string bent into true corners would hold infinite energy, though its mean square is only \(H^2\)" | wrong, because the divergence comes from the square wave's jumps (vertical steps of infinite slope), not from corners. A corner (a kink) costs finite energy. A triangle wave has \(A_n\propto1/n^2\), so \(\omega_n^2A_n^2\propto1/n^2\) and the sum converges. A plucked guitar string starts with such a corner and holds the finite energy the finger gave it. Correct statement: "a string with true vertical steps would hold infinite energy in this small-slope model" (with the exact stretching energy, T times the extra length, each step would cost only T·2H). The divergence of the square-wave sum and "mean square only \(H^2\)" are both right. | Fourier amplitudes of the triangle and square waves; the energy formula E21. |
| N38 | §6 | peak 27.9 px, ceiling 50.3 px; \(\sin3x=-1\) wherever \(\sin x=1\) | verified | Measured over 180 frames: peak 27.9069–27.9081, readout "27.9 px" (also "27.9 px" on the 390 px phone). Readout "50.3 px". The continuous maximum is 27.9081. |
| N39 | Ex. 6.1 | without Wave 4 the peak is 28.0 px = 30·½ + 10 + 6·½ at x = π/6 | verified | Measured 27.9995–28.0000, readout "28.0 px". On a 0.01 px grid the maximum is 28.0000. The slope at π/6 is 0 analytically. |
| N40 | Ex. 6.1 | Wave 2 at Phase 1.00 π: the peak jumps to 41.7 px; no stem moves | verified | Measured φ₂ = 3.15 ("1.00 π"), peak 41.6998–41.7002, readout "41.7 px". `A_line` stays [30, 10, 6, 4.3]. |
| N41 | §7 | Δt capped at 0.05 s; below 20 frames a second the motion slows; Pause stops the clock | verified | `sim.js`: `dt = Math.min((ts-last)/1000, 0.05)` and `if (!playing) dt = 0`. |
| N42 | §7 | M + 1 samples at \(X_j=800j/M\); M = plot width − 58 | verified | `samples = Math.max(2, Math.round(right-left))` with right = w − 14 and left = 44; X = i/samples·800. "Screen pixel" here means CSS pixel: on the DPR-3 phone each sample spans 3 device pixels. |
| N43 | §7 | 1440 × 900: plot 770 wide, M = 712, 1.12 px per sample; phone 390 wide: M = 298, 2.68 px | verified | Measured box_w = 770, M = 712, ΔX = 1.1236; phone box_w = 356, M = 298, ΔX = 2.6846. |
| N44 | §7 | three sine calls per wave and sample, \(3N(M+1)\) = 8 556 per frame (preset, wide window) | verified | Code: two `y()` calls per sample in the component loop and one in the sum loop. 3·4·713 = 8 556. |
| N45 | §7 | "… plus one per wave for the stored values at the centre of the view" (the per-frame sine count) | wrong, because `lines()`, called by `drawSpectrum()` every frame, also calls `Math.sin(wv.phi)` once per wave (with one `Math.cos`) for the spectrum's phasor sum. Wrapping `Math.sin` in Chromium counts 8 564 calls per frame in two successive frames, and `Math.cos` 4: that is \(3N(M+1)+2N\) = 8 556 + 4 + 4. Correct: "plus two per wave: one for the stored values at the centre of the view, one for the spectrum". | Headless Chromium count. |
| N46 | §7 | the peak is the largest \(|y|\) among this frame's samples; readouts rewritten every 8th frame, 7.5 times a second at 60 fps | verified | `pk = Math.max(pk, Math.abs(v))` in the sum loop. A MutationObserver on `r-peak` saw writes at frames 241, 249, 257, … (every 8th) at 60.0 fps. |
| N47 | §7 | values exact to double precision, about 16 significant digits | verified | Direct evaluation of (1) in float64. The phase argument grows with t, so the absolute phase error grows slowly (about 1e−11 rad after an hour), which is still negligible. |
| N48 | §7 | chord sag \(Ak^2\Delta X^2/8\); shortest wave at Frequency 3, λ = 66.7 px, A = 40 px: 0.06 px wide window, 0.32 px phone; about 25 samples per wavelength | verified | 0.0561 and 0.3201 px (the exact sag \(A(1-\cos(k\Delta X/2))\) is 0.0561 and 0.3197); 66.67/2.6846 = 24.8 samples. |
| N49 | §7 | the spectrum is computed from the slider values with (17), not from the curve | verified | `lines()` reads `waves` only. |
| N50 | §7 | t, Δt, M, ΔX and the peak are written to the store where they are computed | verified | `ds.set('t'/'dt')` is in the clock callback; `ds.set('M'/'dX'/'peak')` is in `draw()`. |
| N51 | §8 | upper panel 56 % of the height left after the margins; burgundy fill; sample j in column 44 + j | verified | `hSum = (h-30-44-14)*0.56`, fill `rgba(122,31,43,0.09)`, `lineTo(left + i, …)`. |
| N52 | §8 | preset in the wide window: R = 60 px, h = 220.1, 1 px drawn 1.83 px tall and 0.89 px wide, about twice as steep | verified | Measured R = 60 and hSum = 220.08. 110.04/60 = 1.834, 712/800 = 0.890, ratio 2.06. |
| N53 | §8 | stem at \(44+(\nu/6)(w-58)\); height scaled to max(40, tallest); axis 0–6 Hz because 3 × 2 = 6 | verified | Code `X(nu)` and `amax`. Measured `x_line` = 91.467 for ν = 0.4 at w = 770 (formula 91.467). `FMAX` = 3, Speed max = 2, `NUMAX` = 6; the caption reads "ν from 0 to 6 Hz". |
| N54 | §8 | one colour per wave; a shared stem in ink | verified | `colour: g.n > 1 ? T.ink : g.colour`. |
| N55 | §8 | Wave 4's 4.3 px shows as "4 px" on its card; the wave, the 50.3 px sum and the store keep 4.3 | verified | Measured card output "4 px" and input value 4. Stored A[3] = 4.3; readout "50.3 px". |
| N56 | §9 | the spectrum merges equal-ν waves with their relative phase at X = 0 | verified | `lines()` uses only φᵢ, which is the phase at X = 0. |

## Reference list

| # | Reference | Verdict | Road taken |
|---|---|---|---|
| R1 | Feynman, Vol. I ch. 48 "Beats", `feynmanlectures.caltech.edu/I_48.html` | verified | curl got 403, which is a Cloudflare "Attention Required" challenge, not a dead link. Firecrawl scrape with `maxAge: 0` returned status 200, title "The Feynman Lectures on Physics Vol. I Ch. 48: Beats". |
| R2 | Feynman, Vol. I ch. 50 "Harmonics", `…/I_50.html` | verified | Same: curl 403 (Cloudflare challenge); Firecrawl `maxAge: 0` returned 200, title "… Vol. I Ch. 50: Harmonics". Addison-Wesley 1963 is the standard imprint. |
| R3 | French, *Vibrations and Waves*, Norton 1971, ch. 2 and 6, `archive.org/details/vibrationswaves0000fren` | verified | curl 200. The record gives 1971, New York: Norton, and the contents "… The superposition of periodic motions [ch. 2] … Normal modes of continuous systems. Fourier analysis [ch. 6] …". The publisher's preview (pageplace.de, M.I.T. Introductory Physics Series) lists "Superposed vibrations of different frequency; beats, 22" in chapter 2. |
| R4 | Hecht, *Optics*, 5th ed., Pearson 2017, ch. 7, Pearson product page | verified | curl 200. The page's table of contents lists "7: The Superposition of Waves". Year: Pearson's catalogue data says copyright 2016 (print released Dec 2015), but the book's own copyright line, quoted in the Global Edition, reads "Optics, Fifth Edition, ISBN 9780133977226 … Pearson Education © 2017". |
| R5 | Boas, *Mathematical Methods in the Physical Sciences*, 3rd ed., Wiley 2006, ch. 7, Section 7.11 Parseval, Wiley product page | verified | curl 200. Wiley's contents list "Chapter 7 Fourier Series and Transforms" (release July 2005). The copyright page (PDF of the 3rd edition, via Firecrawl) reads "Copyright 2006 John Wiley & Sons, Inc.". "7.11 Parseval's Theorem" is confirmed by bartleby's section list for ISBN 9780471198260 and by a UT Dallas syllabus on the 3rd edition. |

**Summary: 79 verified / 3 wrong / 0 unverifiable.** That is 21 equation rows, 56 number rows and 5 reference rows; N17, N37 and N45 are wrong.

# Fig. 4 lecture note: derivation and number check

Page: `public/simulations/Transverse and longitudinal waves.html`, the note between `<article class="paper" id="paper">` and `</article>`.
Version checked: HEAD `468c139` (the working tree equals HEAD for this file). Every change against `db1a24b` was read, the new §2 caveat,
"same phase", the Exercise 3.1 sentence on a new medium, the three-sentence ⁴⁄₃G explanation and the named \(y_\mathrm{T}\) included.
The page script (lines 735–1082) and `scripts/sim.js` are unchanged against `db1a24b`; only prose changed.

How the checks were made:
- **Equations.** Re-derived in SymPy 1.14: 58 symbolic checks, all pass. Units were checked with `sympy.physics.units`, and limiting cases are listed per row.
- **Numbers.** The site was built with `APPDEPLOY_VITE_OUT_DIR=/tmp/fig04-check-dist npm run build` (the built page is byte-identical to the source) and served by a small Node static server.
  - Each number was read from the page's own store (`Sim.data.ds`) and readouts in headless Chromium 1194 through Playwright, at 1440 × 900, 390 × 844, 1280 × 800 and 1600 × 900.
  - Reduced motion was set, so the first frame, \(\omega t = 0\), holds still. One `draw()` was recorded by wrapping the canvas 2D methods.
  - Sliders were moved by input events, and the clock was played for the Exercise 5.1 minimum gap and for the 0.05 s cap, which was tested with a 300 ms stall.
  - The run was repeated on the final HEAD. Its results are identical, apart from the frame-timing entries.
- **Figures.** Figures 1–4 were parsed from the SVG and compared point by point with (1) and (10) on the stated sampling grids. Every residual is within the 0.05 rounding of the SVG coordinates once the axis scales are fitted.
- **Links.** Each link was opened with curl. The Feynman page returns 403 to curl, so it was read through Firecrawl. Chapters were checked against first-party tables of contents.

Lengths without a unit qualifier are pixels of the 640 px medium, as the note defines them.

## 1. Numbered equations

| # | Statement | Re-derivation (SymPy), units, limits | Verdict |
|---|---|---|---|
| (1) | \(\xi = A\sin(kX-\omega t)\), \(k=2\pi/\lambda\), \(\omega=2\pi f\) | Spatial period \(2\pi/k=\lambda\), temporal period \(2\pi/\omega=1/f\); ξ px, k rad/px, ω rad/s. A → 0: no wave. Matches code lines 885–886, 928. | verified |
| (2) | \(v=\mathrm dX/\mathrm dt=\omega/k=f\lambda\) | d/dt(kX(t) − ωt) = 0 gives dX/dt = ω/k = fλ; px/s. f → 0: pattern stands still. | verified |
| (3) | \(u=-A\omega\cos\), \(\partial\xi/\partial X=Ak\cos\), \(u=-v\,\partial\xi/\partial X\) | All three identities hold; \(u=-v\,g'\) also holds for any \(g(X-vt)\), as the text claims. u px/s, slope dimensionless. | verified |
| (4) | \(\mu\,\mathrm dX\,\xi_{tt}=F[\xi_X(X+\mathrm dX)-\xi_X(X)]=F\xi_{XX}\mathrm dX\) | The slope difference is \(\xi_{XX}\mathrm dX+O(\mathrm dX^2)\) (generic quintic test), and \(F\sin(\arctan s)=Fs+O(s^3)\). Both sides are in N. A straight string (\(\xi_{XX}=0\)) feels no net force. | verified |
| (5) | \(\xi_{tt}=v^2\xi_{XX}\), \(v=\sqrt{F/\mu}\) | The sine solves it iff v = ω/k, and \(\sqrt{\mathrm{N}/(\mathrm{kg/m})}\) = m/s. F → ∞ gives v → ∞; μ → ∞ gives v → 0. | verified |
| (6) | \(\rho\xi_{tt}=\partial\sigma/\partial X=E\xi_{XX}\), \(v=\sqrt{E/\rho}\) | ∂(Eξ_X)/∂X = Eξ_XX for uniform E; \(\sqrt{\mathrm{Pa}/(\mathrm{kg/m^3})}\) = m/s. | verified |
| text before (7) | \(pV^\gamma\) fixed, \(\mathrm dp=-\gamma p\,\mathrm dV/V\), so \(B=\gamma p\); \(\delta p=-B\,\partial\xi/\partial X\) | \(p=CV^{-\gamma}\) gives \(-V\,\mathrm dp/\mathrm dV=\gamma p\) and \(\mathrm dp=-\gamma p\,\mathrm dV/V\). In 1-D, dV/V = ∂ξ/∂X, and −∂(δp)/∂X = Bξ_XX, so v = √(B/ρ). | verified |
| (7) | \(v=\sqrt{\gamma p/\rho}=343\ \mathrm{m/s}\) | √(1.40 × 101 325 / 1.204) = 343.249 m/s; with the unrounded ρ = 1.204318 it is 343.204 m/s. Limit γ → 1 gives Newton’s isothermal 290.1 m/s. | verified |
| text after (8) | ⁴⁄₃G decomposition (now three sentences) | With Lamé λ = K − 2G/3, uniaxial strain ε gives σ_xx = (K + 4G/3)ε. The split is isotropic ε/3 each (trace ε, stress Kε) plus deviatoric (2ε/3, −ε/3, −ε/3), with zero trace and stress 2G·2ε/3 = 4Gε/3. | verified |
| (8) | \(v_\mathrm P=\sqrt{(K+\tfrac43G)/\rho}\), \(v_\mathrm S=\sqrt{G/\rho}\) | See the row above. \(v_\mathrm P^2-v_\mathrm S^2=(K+G/3)/\rho>0\), so P is always faster. G → 0 gives v_S = 0 and v_P = √(K/ρ), as in (7). At ν = 0 (K = 2G/3), K + 4G/3 = E = 2G: no bulging to prevent. In general K + 4G/3 − E = (3K − 2G)²/(3(3K + G)) ≥ 0. | verified |
| (9) | \(\xi=g(X-vt)+h(X+vt)\) | Solves (5) identically. \(A\sin k(X-vt)=A\sin(kX-\omega t)\) iff ω = vk. | verified |
| (10) | \(\rho/\rho_0=1/(1+A_\mathrm Lk\cos)\approx1-A_\mathrm Lk\cos\) | The spacing is ∂(X + ξ)/∂X, and the first-order series is 1 − a cos. A_L k → 0 gives 1; A_L k → 1 diverges at phase π. At phase π, ξ = 0 and u = +A_L ω. | verified |
| (11) | \(X_\mathrm p-X_\mathrm c=(\pi-\pi/2)/k=\lambda/4\) | Exact. The strain equals −u/v, and A_L k < 1 ⇔ A_L ω < v, as the text says. | verified |
| (12) | \(A_\mathrm L=\min(A,0.8/k)=\min(A,0.8\lambda/2\pi)\) | 0.8/k = 0.8λ/2π; a px value. Same as code line 799, `Math.min(amp.value, 0.8 * lambda.value / (2 * Math.PI))`. | verified |
| (13) | \(e=\tfrac12\mu\xi_t^2+\tfrac12F\xi_X^2\), with the new tilt step | \(\sqrt{1+s^2}=1+s^2/2+O(s^4)\), so F times the extra length is ½Fξ_X² per unit length (constant tension). Both terms are in J/m. | verified |
| (14) | \(\partial_te+\partial_XP=0\), \(P=-F\xi_X\xi_t\) | ∂e/∂t + ∂P/∂X = ξ_t(μξ_tt − Fξ_XX) = 0. For g(X − vt), P = μvu² and the kinetic term equals the potential term. N·m/s = W. | verified |
| (15) | \(\langle e\rangle=\tfrac12\mu\omega^2A^2\), \(\langle P\rangle=v\langle e\rangle\) | ⟨u²⟩ = A²ω²/2 (exact integral), so ⟨e⟩ = 2·½μ⟨u²⟩ and ⟨P⟩ = μv⟨u²⟩ = v⟨e⟩. Doubling ω at fixed A and v gives 4×. The rod substitution ρS, ES keeps v² = E/ρ. | verified |
| (16) | \(\omega t\leftarrow\omega t+2\pi f\Delta t\) | Same as code line 978. A clock-based phase would jump by 2πΔf·t. The phase at X = 0 is −ωt, independent of k. Measured: ωt = 2πft to 1 × 10⁻¹⁴ at constant f. | verified |
| (17) | \(s=(W-44)/640\), \(x_\text{upper}=22+sX\), \(x_\text{lower}=22+s(X+\xi)\) | Code lines 835, 884/902, 927. X = 0 → 22 and X = 640 → W − 22. Recorded arcs match the formula to 0.0 px. | verified |

## 2. Numbers

| § | Number in the note | Recomputed / measured | Verdict |
|---|---|---|---|
| 2 | \(A_\mathrm Lk\approx0.743\) at defaults; A_L equals A | Store: AL = 26, ALk = 0.742558, cap = false | verified |
| 2 | Neighbours close to “about a quarter” of rest spacing | Continuum 1 − 0.7426 = 0.257. Particles: closest pair 7.012/25.6 = 0.274 at the first frame, minimum over time 7.011 | verified |
| 2 | Medium 640 px | `LENGTH = 640` | verified |
| 2 | Defaults A = 26 px, f = 0.50 Hz, λ = 220 px, 26 particles | Slider `value` attributes and store A, f, lambda, N | verified |
| 2 | Spacing 640/25 = 25.6 px | Store X[1] − X[0] = 25.6 | verified |
| 2 | Followed particle no. 12, X = 307.2 px | Store follow = floor(25/2) = 12, X[12] = 307.2 | verified |
| Fig. 1 | Crests λ = 220 px apart; first frame ωt = 0 | Store crests 55, 275, 495 at ωt = 0; SVG crest tips at X = 55, 275, 495 | verified |
| Fig. 1 | Burgundy particle rising | u = −Aω cos(kX) = +64.97 px/s, ξ = 15.76 px at X = 307.2 | verified |
| Fig. 1 | Compression λ/4 = 55 px ahead of crest | Store comp0 = 110 vs crest 55; SVG triangles at X = 110, 330, 550 | verified |
| Fig. 1 | Drawing to scale, one unit per medium pixel | Upper curve (321 points), 26 upper and 26 lower particles and 65 tint stops all match y = 124 − ξ, x = 40 + X(+ξ); max residual 0.05 (rounding) | verified |
| Fig. 2 | Snapshots at t = 0 and 0.5 s (a quarter period); curve moved 55 px | T/4 = 0.5 s; v·0.5 s = 55 px; SVG crest moves from X = 55.1 to 109.9 (rounded grid) | verified |
| Fig. 2 | Sampled every 2.5 px; histories over 4 s in steps of 0.025 s | 257 and 161 points; both curves and the dots match (1) within rounding (0.05 after axis fit) | verified |
| Fig. 2 | X = 307.2 and 358.4 px, two places apart | i = 12 and 14 | verified |
| Fig. 2 | T = 2 s; lag 51.2/110 = 0.47 s | 1/f = 2; 51.2/110 = 0.4655 | verified |
| 3 | v = 0.50 × 220 = 110 px/s; Speed readout and caption | Store v = 110; readout “110 px/s”; caption “v = 110 px/s” | verified |
| 3 | Aω = 81.7 px/s | 26π = 81.681 | verified |
| 3 | Aω/v = Ak = 0.743 | 0.742558 | verified |
| Ex. 3.1 | Period readout 2 s | “2.00 s” | verified |
| Ex. 3.1 | 640/110 = 5.8 s | 5.818 | verified |
| Ex. 3.1 | f = 1.00 Hz: period halves, Speed 220 px/s | Readouts “1.00 s”, “220 px/s” | verified |
| Ex. 3.1 | New sentence: a new medium; in a real medium doubling f halves λ (Section 4.4) | Non-dispersive medium: λ = v/f with v fixed, so 2f gives λ/2. Consistent with §4.4 | verified |
| Ex. 3.1 | λ = 110 px: Speed back to 110 px/s; still once a second | Readouts “110 px/s”, “1.00 s” | verified |
| Ex. 3.1 | Upper-row period and top speed independent of λ | T = 1/f and Aω contain no λ | verified |
| Ex. 3.1 | Lower row capped to 14 px at λ = 110 | 0.8 × 110/2π = 14.006; readout “14 px (cap)” | verified |
| 4.2 | ρ = 1.2043 kg/m³ (28.97 g/mol, 293.15 K, 101 325 Pa) | pM/(RT) = 1.204318 with R = 8.314462618 | verified |
| 4.2 | √(1.40 × 101 325 / 1.204) = 343.2 m/s; (7) 343 m/s | 343.249 | verified |
| 5 | Triangles of the lower row 55 px right of the upper ones | comp0 − crest = 110 − 55 = 55 = λ/4 | verified |
| 5 | Cap: tightest spacing 20 %, densest point 5× | 1 − 0.8 = 0.2, 1/0.2 = 5 when the cap acts (see remark 6) | verified |
| 5 | Default cap 28.0 px, above A = 26 px | 0.8 × 220/2π = 28.011; Longit. A readout “26 px” without “(cap)” | verified |
| 5 | A_L k = 0.743 | 0.742558 | verified |
| 5 | Figure 3: 26 particles, two periods | 26 paths, 0 ≤ t ≤ 4 s | verified |
| 5 | Compression density 1/(1 − 0.743) = 3.88 | 1/(1 − 0.742558) = 3.884 (see remark 1 on the rounded operand) | verified |
| 5 | Rarefaction density 1/(1 + 0.743) = 0.574 | 0.5739 | verified |
| 5 | Linear values 1.74 and 0.26 | 1.7426 and 0.2574 | verified |
| 5 | Denser half fills 1/2 − A_L k/π = 26 % | 0.26364 | verified |
| 5 | Denser half: phases π/2 to 3π/2, rearmost pushed forward and foremost pulled back by A_L, so they fit into λ/2 − 2A_L | ρ > 1 ⇔ cos < 0. ξ(π/2) = +A_L, ξ(3π/2) = −A_L. Span = λ/2 − 2A_L, so the fraction is 1/2 − 2A_L/λ = 1/2 − A_L k/π (SymPy) | verified |
| 5 | First-frame gaps 7.0 to 44.1 px | Store xL at ωt = 0: min 7.0123, max 44.1453 | verified |
| Fig. 3 | x = X + A_L sin(kX − ωt), 0–4 s in steps of 0.025 s | 26 × 161 points; max deviation 0.05 (rounding); followed path burgundy | verified |
| Fig. 3 | Dashed lines x = (π + ωt)/k + nλ advance 110 px/s | Six lines at x(0) = 110 + 220n; slopes 109.98–110.01 from rounded endpoints | verified |
| Fig. 4 | Sampled every 1 px, exact and linearised curves | 641 points each; residual 0.055 after axis fit (rounding) | verified |
| Fig. 4 | Exact peak 3.88, trough 0.574; linear 1.74 and 0.26 | Curve values 3.8844 at X = 110, 0.5739 at X = 0; linear 1.7426, 0.2574 | verified |
| Fig. 4 | Both cross 1 at the same places | Both cross where cos = 0: X = 55, 165, 275, 385, 495, 605 | verified |
| Fig. 4 | Dots at the 26 particles | Match 1/(1 + A_L k cos kX_i) within rounding | verified |
| Ex. 5.1 | Longit. A follows up to 28 px; at 29 reads “28 px (cap)” | Readouts at A = 27, 28, 29: “27 px”, “28 px”, “28 px (cap)” | verified |
| Ex. 5.1 | λ = 100: cap 0.8 × 100/2π = 12.7 px, readout “13 px (cap)” | 12.732; readout “13 px (cap)” | verified |
| Ex. 5.1 | Bars crowd but never cross | Store ALk = 0.800 < 1 | verified |
| Ex. 5.1 | N = 40: closest two within 3.9 px; rest spacing 16.4 px | Played 4.2 s: min neighbour gap 3.8559 (214 frames). Analytic d − 2A_L sin(kd/2) = 3.8559; d = 640/39 = 16.410 (medium px, see remark 4) | verified |
| Ex. 5.1 | Ak = 29 × 2π/100 = 1.82 | 1.8221 (store Ak) | verified |
| 6 | Double f, same A: four times the power | ⟨P⟩ ∝ ω² at fixed v (row (15)) | verified |
| 7 | Frame step capped at 0.05 s | sim.js line 179; measured Δt = 0.05 after a 300 ms stall | verified |
| 7 | Top frequency 2 Hz; 2π × 2 × 0.05 = 0.63 rad | Slider max 2; 0.6283 | verified |
| 8 | Margins 22 px, W − 44 | `LEFT = 22`, right − left = w − 44 | verified |
| 8 | 770 × 481 at 1440 px wide, s = 1.134 | Measured box 770 × 481; s_px = 1.134375 (also 770 at 1280) | verified |
| 8 | 356 × 374 at 390 px wide, s = 0.4875 | Measured box 356 × 374; s_px = 0.4875 | verified |
| 8 | y_T at 30 %, lower row at 77 % (y_T now named) | Line 837; yT = 144.3 = 0.3 × 481, yL = 370.37 | verified |
| 8 | Upper discs 4.5 px, followed 6.5 px | Recorded arcs: 25 at 4.5, 1 at 6.5 | verified |
| 8 | Curve through 215 points, every 3 px, last at X = 640 | Recorded path: 215 vertices, X = 0, 3, …, 639, then 640 | verified |
| 8 | Crest triangles 8 px above the highest point sA | Recorded tips 8.000 css px above y_T − sA | verified |
| 8 | Lower discs 4 px on bars 56 px tall | Recorded arcs 4 px (6.5 px followed, see remark 2); bars 56.0 px | verified |
| 8 | Band 68 px | Recorded fillRect height 68 (BAND = 34, ×2) | verified |
| 8 | Opacity 0.03 + 0.2 max(0, −cos) at 65 points every 10 px, linear blend | 65 gradient stops, step 1/64 of the medium; opacities 0.030–0.230 | verified |
| 8 | Compression triangles above the band | Tips 6 px above the band top | verified |
| 8 | Tint stops at 0.23; stored density 3.88 and 0.574 | 0.03 + 0.2 = 0.23. For the density see remark 3 | verified |
| 9 | Ak = 0.743 is 36.6° | arctan 0.742558 = 36.596° | verified |
| 9 | Chain with a = 25.6 px, λ = 220 px: 2.2 % slower | sin(ka/2)/(ka/2) = 0.97788, so 2.21 % slower | verified |
| 9 | Fig. 5 is water waves | Nav link 5 → `water-wave.html` | verified |

## 3. Numerical method against the code

| Note says | Code | Verdict |
|---|---|---|
| §2: “The page simply draws formula (1)” | Upper row: line 885 (A sin). Lower row: line 927 (A_L sin), equal to A at defaults, as the sentence says | verified |
| §2: both rows carry the same phase kX − ωt | Lines 885 and 927 both use `k * X - omegaT` with the same k and omegaT | verified |
| §7: nothing integrated; the formula is evaluated afresh per particle each frame; double precision | Loops at lines 882–886 and 925–929 inside `draw()`, called each frame (line 981); JS doubles, Float64Array store | verified |
| §7: only the phase is carried, ωt ← ωt + 2πfΔt | Line 978 | verified |
| §7: Δt is the real time since the last frame, 0 while paused, capped at 0.05 s | sim.js lines 179–181 | verified |
| §7: the f slider changes only the rate; the λ slider changes k at once, stretching about X = 0 | freq is read inside the accumulation (978); lambda is read at the start of each `draw()` (836) | verified |
| §7: per particle X_i = i·640/(N − 1), phase, ξ and u (upper); displacement, position, velocity, density, shading (lower); each stored where computed | Lines 883, 886, 928, 929 | verified |
| §7: the Data panel reads the store and recomputes nothing | `Sim.live` (964–976) reads the store; for the Check column see remark 5 | verified |
| §7: reduced motion starts paused | sim.js line 177; measured `playing = false` with reduced motion, true without | verified |
| §8: (17) and y_T − sξ | Lines 835, 902, 927; arcs equal the formula to 0.0 px | verified |
| §8: rose lines and pale ticks (upper) when Equilibrium positions is on | Rose lines 887–892 always; ticks 893–896 only when `eqBox.checked` | verified |
| §8: curve loop | Lines 868–872 | verified |
| §8: crest markers | Lines 874–875; marker tip at y_T − As − 8 | verified |
| §8: lower discs, bars, rose line when Follow and Equilibrium are both on | Lines 938–942 and 949–955 | verified |
| §8: band, gradient, compression markers | Lines 909–918 | verified |
| §8: tint laid out by X, particles by X + ξ; curve and tint samples not stored; particles drawn at stored screen positions | Gradient stop at X/LENGTH (913). The arc uses `px`, stored as xl_px (929, 942); the arc y equals the stored yi_px | verified |
| §3/§5: crest and compression positions | Lines 874 and 917 ((π/2 + ωt)/k and (π + ωt)/k, mod λ) | verified |
| Readouts used in the exercises | Lines 801–808: `Math.round(v)`, `(1/f).toFixed(2)`, `al.toFixed(0)` + “(cap)” when al < A | verified |

## 4. Further reading: links and chapters

| Ref. | Link (road) | Chapter / details | Verdict |
|---|---|---|---|
| 1 Young & Freedman | Pearson page: curl 200; H1 “University Physics with Modern Physics, 15th edition” | Publisher TOC numbered in order: 14 Periodic Motion, **15 Mechanical Waves, 16 Sound and Hearing**. The page lists this ISBN as published 15 July 2020; the 15th edition carries copyright 2020 | verified |
| 2 French | Routledge page: curl 200, “Vibrations and Waves – 1st Edition – A.P. French”, Copyright 1971, by CRC Press, M.I.T. Introductory Physics Series. Internet Archive: curl 200, New York: Norton, 1971, access-restricted (lending) | Routledge TOC: “6 Normal modes of continuous systems… **7 Progressive Waves** 8 Boundary effects and interference”; the IA contents list has the same order | verified |
| 3 Stein & Wysession | Wiley page: curl 200, title matches | Wiley TOC: **2 Basic Seismological Theory, 3 Seismology and Earth Structure**. The authors’ companion site levee.wustl.edu/seismology/book reads “Wiley-Blackwell Publishing, 2003”. Its chapter 2 figures begin with Figure 2.2-1, “Tensions on a string segment”, so the chapter opens (after 2.1 Introduction) with waves on a string. The IA catalogue gives Malden, MA: Blackwell Pub., 2003. Wiley’s own page shows “January 1991”, a catalogue error, not the note’s | verified |
| 4 Feynman I-47 | curl: 403 (Cloudflare “Attention Required”), not proof of a dead link. Firecrawl scrape: 200, page title “The Feynman Lectures on Physics Vol. I Ch. 47: Sound. The wave equation” | §47-3 derives the wave equation for sound from Newton’s laws; §47-5 explains why the changes are adiabatic (Laplace against Newton’s isothermal guess) | verified |

## Remarks (not errors)

1. §5 writes 1/(1 − 0.743) = 3.88. With the rounded operand the quotient is 3.891. The value 3.88 is right because it comes from A_L k = 0.7426. Writing 1/(1 − 0.7426) = 3.88 would make the line reproducible by hand.
2. In the §8 lower-row item, the followed particle is a 6.5 px burgundy disc on a 2.6 px wide burgundy bar (lines 936, 942). The note gives only the 4 px disc.
3. §8 says the stored density is 3.88 at the compression centres. The store holds the density only at particles. At the first frame no particle sits at X = 110, so the largest stored value is 3.849. The value 3.884 is reached when a particle passes a centre. Figure 4, which the sentence cites, is the continuum.
4. The Exercise 5.1 gap of 3.9 px and the §5 gaps are medium pixels. On a 1440 px window they are s = 1.134 times larger: 3.9 becomes 4.4 css px.
5. §7 says the Data panel “recomputes nothing”. That is true of what the panel displays. Its Check column recomputes each formula from stored inputs when asked; this is deliberate, as the pipeline test.
6. “Caps the amplitude … so that the tightest spacing is 20 %” holds when the cap acts. At the defaults the tightest spacing is 25.7 %.

**Summary: 107 rows: 107 verified / 0 wrong / 0 unverifiable** (19 equation rows, the 17 numbered equations plus the B = γp and ⁴⁄₃G text derivations; 66 number rows; 18 method rows; 4 reference rows).

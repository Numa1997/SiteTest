# Fig. 15 lecture note: derivation and number check, round 2

What was checked: `public/scripts/resonant-note.js` at commit 333915d (02:25:50 UTC, clean tree). The note was being edited while
I worked: snapshots at 02:22 and 02:23 were reviewed too, and every change up to 333915d was checked again.
The page was rendered with headless Chrome from `public/` served on 127.0.0.1:9847. There were 816 KaTeX blocks and 0 katex-error;
the note text contains no NaN, undefined or null. Every number below was read from that rendered text.

How:
- Equations: re-derived in SymPy 1.14. Script: `sym.py` in this folder.
- Numbers: recomputed by my own code, which is independent of `gen2_numbers.py`. Scripts: `num.py`, `num2.py`, `num3.py`, `num4.py`, `prof.py`.
  - The 1D exact numbers use an analytic single-barrier `w`, `gamma` and my own `P^N`, cross-checked against `tm.py`.
  - The diode numbers use `iv.py` with `iv.V0 = 2`, `nper` 200 against the note's 60.
  - The data numbers come from `index.json`.
  - `gen2_numbers.py` was re-run. Its output equals the NUM block key for key, with no difference.
- Method text: compared line by line with `rt3d2.py`, `rt3d2_run.py`, `file_rt3d2.py`, `rt3d-worker.js` and `resonant-tunnelling.html`.

## Concrete errors, ranked by severity

1. **Section 1, "Reading the figures" (and the page's own gain note): "on one scale for the whole run, so that the start packet's peak is height 1" is wrong.**
   - `buildSheet()` divides by `S = run.peakMax = max(head.peaks)`. `rt3d-worker.js` decodes |psi| in units of the start peak (`peaks = p/pk[0]` in `rt3d2_run.py`).
   - So the *largest* peak of the run is height 1, and the start packet sits at `1/S` (or `1/S^2` in the |psi|^2 view).
   - The reflected wave interferes with the incoming one, so `S > 1` in most runs. In the generation-1 files stored in the repository:
     - running example E = 0.735: S = 1.239. The start peak sits at 0.81 (Re psi view) and 0.65 (|psi|^2 view).
     - E = 1.2: S = 1.39.
     - up to S = 2.32 in other runs.
   - The generation-2 run files cannot be fetched: `phyeinusul.com/r2/...` returned HTTP 404 for three files. They are written by the same code.
   - Correct form: "one scale for the whole run, set by the largest value the run reaches, which is height 1". Or change the code to `S = head.peaks[0]`, but then clipping at 1.25 matters at gain 1.

2. **Section 10, run length: "Each run lasts until the packet has passed and the trapped wave has drained, or as long as the box allows" misdescribes `t_end_of()`.**
   - The code takes the time for the packet's trailing edge to reach 20 a past the last face, plus 3 x `tau_est`.
   - `tau_est` is the longest 1D lifetime in the packet's window, **capped at 60 (sigma_x <= 4) or 150 (long packets)**. Shells use a fixed 30.
   - Nothing in the code depends on the box.
   - Correct form: "...plus three lifetimes of the longest-lived resonance the packet holds, with the lifetime capped at 60 (150 for long packets): from 30 to 517 time units." The 30 and 517 are correct.

3. **Section 11, "by 3–4 % of the peak during the collision, and by up to 10 % late in the run": not reproduced.**
   - I compared the stored 1D twin of `dflat_R0_E0.735.bin` (generation 1) with an exact packet built from `tm.psi_x` stationary states, over |x| < 38.5. At t = 0 the difference is 0.
   - Measured against each frame's own peak:
     - collision (t = 10–35): up to 5.8 %
     - t = 35–45: up to 12 %
     - after t = 45: up to 66 %
   - Measured against the run's overall peak: at most 3.0 % throughout, and about 2 % late.
   - Neither measure gives "3–4 %, then up to 10 %". The note should name the measure. The likely statement is "up to 6 % of the frame's peak during the collision, and much more late in the run, when what remains is small", or "under 3 % of the run's largest value at all times".

4. **Eq. (10), the amplitude phase (modulus correct).**
   - With t and r taken at each barrier's own centre and a common origin (`tm.py`'s convention), the pair's transmitted amplitude is `t^2/(1 - r^2 e^{2iks})`.
   - The note's `t^2 e^{iks}/(1 - r^2 e^{2iks})` is larger by exactly `e^{iks}`. Checked at E = 0.5, 0.735, 1.1: the ratio equals `e^{iks}` to 1e-15.
   - That form is the amplitude at the second centre divided by the amplitude at the first centre. |t_2|^2 and everything after it are unaffected.
   - Fix: say which reference points the amplitude uses, or drop `e^{iks}`.

5. **Section 3 Key-result box: arithmetic.** The printed sum `1 + 4(2.351)^2/(4·0.735·1.265)` equals 6.945, not 6.947. The 6.947 comes from the unrounded sinh = 2.35144. T = 0.144 is unaffected. Write 6.945, or sinh(1.591) = 2.3514.

6. **Section 5, "to within 0.0003" (FP_theta_mod).**
   - `gen2_numbers.py` evaluates theta at the *rounded* E = 0.735. At the exact E_r = 0.734935, theta mod 2 pi = 1.4e-8.
   - As written the sentence is true, but it makes the resonance condition look approximate.
   - Fix: compute at the unrounded E_r and quote "to 1e-8", or say that 0.0003 comes from rounding E_r.

7. **Section 5, "Midway between resonances T_2 ≈ T^2/4R".** This is an approximation. The exact value at sin^2 = 1 is `T^2/(1+R)^2`, from SymPy: 0.00600 against 0.00605 for the running example. The exact form is just as short.

8. **Section 10 box: "|psi| is stored in 256 steps".** These are 256 levels, 255 steps (`round(255·|psi|/peak)`). The "0.2 %" (0.5/255) is right.

9. **Not an equation, but it blocks the page.** The live site serves no generation-2 run. `https://phyeinusul.com/r2/resonant-tunnelling/2026-11-14/runs/flat_N2_V2_D1_P2.5_R0_B0_s3_E0.650.bin` (the page's default run), `..._E0.700.bin` and `flat_N2_V2_D2_P3.5_..._E0.700.bin` all return HTTP 404. The note's page then shows "could not load".

Everything else I checked is right; see the tables.

## Equations

| Eq. | Verdict |
|---|---|
| (1) TDSE | verified (standard; units consistent) |
| (2) separation | verified: product ansatz splits into three brackets; SymPy confirms the quoted free Gaussian `g` solves `i g_t = -g_yy/2` (residual 0) |
| (3) sigma_perp(t) | verified: SymPy variance of |g|^2 = sigma^2 (1 + (t/2sigma^2)^2); units: hbar t/(m sigma^2) dimensionless; t→0 gives sigma |
| (4) k, kappa | verified |
| (5) edge matrix | verified (SymPy solve of continuity of chi, chi'); identical to `tm.edge` |
| (6) M form, w, gamma, |w|^2−|gamma|^2 = 1 | verified: SymPy product edge·flight·edge, shifted to the barrier centre, gives exactly the quoted w and gamma = +i(kappa^2+k^2)/(2k kappa) sinh(kappa d); M21 = M12*, M22 = M11*; det = 1. Conjugation argument and current conservation (j = v(|A|^2−|B|^2)) checked |
| (7) |w|^2 | verified (SymPy, exact) |
| (8) T, R | verified; limits d→0: T→1, V0→∞: T→0 (SymPy) |
| (9) thick barrier | verified: lim_{d→∞} T(8)/T(9) = 1 (SymPy) |
| (10) two-barrier sum | |t_2|^2 verified against `tm.py` to 1e-15; amplitude carries an extra e^{iks} (error 4) |
| (11) unequal pair peak | verified: leading order in T_a, T_b of T_aT_b/(1−sqrt(R_aR_b))^2 is 4T_aT_b/(T_a+T_b)^2 (SymPy) |
| (12) theta | verified (round-trip factor r^2 e^{2iks} = R e^{i theta}) |
| (13) Airy form | verified: |1−Re^{i theta}|^2 = (1−R)^2+4R sin^2(theta/2), T_2 = 1/(1+4R sin^2/T^2) (SymPy). Midway approximation: see error 7 |
| (14) resonance | verified; the "n depends on how rho is counted" remark is right (here theta ≈ 0, rho ≈ −pi + 0.11) |
| (15) Lorentzian, Gamma = 2T/(sqrt R theta') | verified (SymPy); units: theta' is 1/energy, so Gamma is an energy |
| step phase, rate 2/kappa | verified: d/dk[−2 arctan(kappa/k)] = 2/kappa with kappa^2 = 2V0−k^2 (SymPy) |
| −2 ln R vs 2T/sqrt R to O(T^3) | verified: 2T + T^2 + 2T^3/3 vs 2T + T^2 + 3T^3/4 |
| (16) tau = hbar/Gamma | verified |
| (17) Gamma ≈ hbar v T/L_eff | verified (from (15) with t_rt = 2L_eff/v, sqrt R → 1); units energy; limits T→0 and R→0 hold |
| phase average 1/sqrt(1+F) = T/(2−T) | verified (SymPy integral; equals the incoherent sum T^2/(1−R^2)) |
| (18) packet average | verified (definition; sigma_k = 1/(2 sigma_x) for exp(−x^2/4 sigma_x^2)) |
| (19) sqrt(pi/8) Gamma/sigma_E | verified (SymPy: area pi Gamma/2 × 1/(sqrt(2 pi) sigma_E)) |
| (20) finite well | verified (even/odd log-derivative matching) |
| (21) hard-wall estimate | verified |
| (22) xi = Re(w e^{−iks}) = cos(ks+phi)/sqrt T | verified (trace of M·diag; numerically via my own P) |
| Cayley–Hamilton, P^N = U_{N−1}P − U_{N−2}I | verified (recursion = SymPy `chebyshevu` up to n = 5) |
| (23) T_N | verified: my independent product agrees; the 1e-12 check is reproduced by gen2 (2.3e-12) |
| (24) Kronig–Penney | verified |
| (25) Strang split | verified; matches `rt3d2.run` (halfV · ifft(kin · fft) · halfV, then mask) |
| (26) interpolation | verified: identical to `interp()` in the page (cr, ci = e^{iE dt}; cp, sp = e^{−iE tau}) |
| (27) rates add | verified |
| (28) tau_side ~ mR^2/hbar | verified as an order of magnitude; units kg m^2/(J s) = s |
| (29) ramp | verified; same as `iv.T_biased` and `rt3d2.vbias` (outer faces x_l, x_r) |
| (30) transverse sum | verified: SymPy integral = kT ln(1+e^{(E_F−E)/kT}); 2 d^2k/(2pi)^2 = (m/pi hbar^2) dE_perp |
| (31) Tsu–Esaki | verified: e × dE/(2 pi hbar) × (m kT/pi hbar^2) ln(...) = e m kT/(2 pi^2 hbar^3); matches `iv.supply`/`iv_curve` |
| (32) trapezoid | verified: identical to `file_rt3d2.py` (`np.trapezoid(T*supply(E,V), E)`, E_F = 1, kT = 0.05; walls use twin T, discs use T_far) |

## Numbers (my recomputation → verdict)

| Where | Number | Verdict |
|---|---|---|
| Abstract, §3 | 14 in a hundred, T = 0.144, 14.4 % | verified (0.14395) |
| §1 | glass 4 % | verified ((0.5/2.5)^2) |
| Fig. 1 | E/V0 true 0.37, drawn near 0.5 | verified (0.3675; SVG 57/115 = 0.50) |
| Fig. 1, §10 | 47 energies 0.30…2.60, 25 diode energies 0.10…1.30 | verified (`EGRID`, `EBIAS`) |
| §2 | sigma_perp(40) = 7.3 | verified (7.31) |
| §2 | "packet has long passed" at t = 40 | verified (centre at x ≈ +32) |
| §2 box | k = 1.212, 2pi/k = 5.18, kappa = 1.591, e^{−kappa d} = 0.204 | verified |
| §3 box | sinh(1.591) = 2.351, |w|^2 = 6.947, |r| = 0.925 | 2.351, 0.925 verified; 6.947 see error 5 |
| Ex. 3.1 | sinh(3.18) = 12.0, T = 6.4e-3, 22 times | verified (12.02, 6.40e-3, 22.5) |
| §3 | (9) gives 0.154 | verified (0.1545) |
| Ex. 4.1 | 2.1, 7.1, 13.9, 36.8, 67.1, 92.5, 99.9 % | verified (all seven) |
| §4 box | |t_2|^2 = 1.000 at 0.735 | verified (0.9999965) |
| §5 | theta within 0.0003 | see error 6 |
| §5 | 2.76 effective width, half-wavelength 2.59 | verified (2.757, 2.591) |
| §5 | hbar theta' = 4.45, 2L_eff/v = 4.55 | verified (4.4536, 4.5487) |
| §5 | 0.3109, 0.3112, 0.2879 | verified |
| §5 box | Gamma(15) = 0.0699, exact 0.0704, tau 14.2, "about three round trips", v = 1.21, L_eff = 2.76, Gest 0.0633 | verified (14.2/4.45 = 3.2) |
| §5 | 0.144/1.856 = 0.078 | verified (0.0776) |
| §6 | sigma_E = 0.202, (19) 0.218, exact 0.196, one barrier 0.149 | verified (0.2021, 0.218, 0.1959, 0.1494) |
| §6 | box 2.67×, sigma_E long 0.051, FWHM 0.119, Tbar12 0.538 | verified (my k-space average 0.540; the index's 0.01-grid interpolation gives 0.538) |
| §6 | long run 0.51 at E = 0.713 vs exact 0.499; 5 runs | 0.499 verified (0.4997); 0.51 and n = 5 from index (gen2 = NUM) |
| §6 | d = 2: 0.0225 at 0.7215 vs exact 0.0318; (19) 0.0359; exact 0.035 | verified (0.0319, 0.0359, 0.0351) |
| §7 | (21) gives 0.649 | verified |
| §7 table | resonances 0.735 / 0.388, 1.486 / 0.238, 0.931 / 0.16, 0.633, 1.397 | verified |
| §7 table | finite well 0.744 / 0.395, 1.445 / 0.241, 0.933, 1.878 / 0.162, 0.638, 1.377 | verified |
| §7 table | hard box 2.193, 0.79, 0.403, 0.244 | verified |
| §7 table | Gamma 0.0704, 0.0172, 0.00606, 0.00267; tau 14.2, 58.3, 165, 375 | verified |
| §7 | "few thousandths", "few hundredths" | verified (0.002–0.009; 0.02–0.04) |
| §7 | 3D run P = 3.5 at E = 0.35: tau 65.2, "12 % longer" | 65.2 from index (gen2 = NUM); 12 % verified |
| §7 | first resonances 0.238, 0.16 below 0.30 | verified |
| §8 table | E_r 0.64, 0.735, 0.877, 0.742, 0.744 | verified |
| §8 table | kappa d 1.31, 1.59, 2.06, 2.38, 3.17 | verified |
| §8 table | T1 0.248, 0.144, 0.0526, 0.0316, 0.00657 | verified |
| §8 table | Gamma 0.116, 0.0704, 0.0291, 0.0142, 0.00291 | verified |
| §8 table | (17) 0.093, 0.0633, 0.0282, 0.0139, 0.0029 | verified |
| §8 table | tau 8.6, 14.2, 34.4, 70.4, 344 | verified |
| §8 box | 22× more opaque, 24× narrower, "within a quarter" | verified (21.9, 24.2; worst case 20 % at V0 = 1.5) |
| §8 | run d = 2: t_end 213, t0 91, tau 210 ("lower bound") | from index (gen2 = NUM); 213 < 344 verified; 213 = flight + 3×60 (cap) consistent with code |
| §9 | band 0.59–0.955, width 0.365, gap 1.126, second band 2.082 | verified (my independent xi) |
| §9 | peaks N = 3: 0.657, 0.83; N = 5: 0.614, 0.685, 0.791, 0.902; N = 10: nine values | verified; T_N = 1 to 1e-12 at each |
| §9 | xi = 0 at 0.735, band midpoint 0.773 | verified (xi(0.735) = −3.8e-4; 0.7725) |
| §9 | TN check 2.3e-12 | verified (gen2 re-run) |
| §9 | peaks 0.02–0.17 apart, spread 0.2 | verified (0.018–0.173; 0.202) |
| §9 | N = 10 band 0.129 (exact 0.158), gap 0.0218 (exact 0.032) | exact verified (0.1580, 0.0320); run means from index (gen2 = NUM) |
| §10 | 192×128×128, 96 a × 64 a; 256 for N = 10; 512 for long | verified (`jobs()`, `setup`) |
| §10 | faces halfway between grid points, D = 1 is two points | verified (`centres()`: faces on odd multiples of 0.25) |
| §10 | outer tenth, factor 1 → 0 | verified (`sin^(1/8)`, W = n//10, 0 at the edge) |
| §10 | diagonal mode 0.59 rad/step | verified (3(2pi)^2·0.005 = 0.592) |
| §10 | ~1 ns per point per step; ≥3 million points | verified (median 0.95 ns, 0.87–1.12 over 1237 runs; 3.15 M) |
| §10 | 3739 runs; A 1128, B 188, C 564, D 376, E 423, F 1000, G 60 | verified by running `jobs()` (G = 4 structures × 1 resonance × 15) |
| §10 | start share at most 2.1e-5 | verified (max over index; 20 long d = 2 runs are above 1e-5) |
| §10 | runs last 30–517 | verified (index); the "box" wording: error 2 |
| §10 | six parts on 2 T4 each; 1237 filed from 2 parts; 5.9 h | verified (index notebooks: shard 1 and 2 of 6, Tesla T4 × 2, sum sweep_s 5.9 h) |
| §10 | 200 frames; z = 0 half plane; 8-bit levels; peaks stored; p(x,t); region probabilities; twin on same grid and step; SHA-256 + notebook/version/commit; page checks SHA | verified against `rt3d2.run`, `run1d`, `file_rt3d2.py`, `rt3d-worker.js` (crypto.subtle.digest) |
| §10 box | 0.2 % amplitude, 2pi/255 phase, ±0.012 rad, below 3 levels drawn −pi | verified (`qp[qa<3] = 0` → −pi in the worker); "256 steps" see error 8 |
| §10 box | colour table 1025 steps, clip ±1.25 | verified (`rt3d-view.js` LUT 1025; `buildSheet` clip) |
| §11 | 115 runs; 3D vs twin 1.8e-4 | verified (generation-1 index, `sep_check_max` at 0.735) |
| §11 | twin 0.186, exact 0.196, 5 % | verified (0.1861, 0.1959) |
| §11 | +22 % at 0.4; −20 %, 0.056 vs 0.071 at 1.2 | verified (1.223; 0.0564 vs 0.0706) |
| §11 | 3–4 % / up to 10 % profile difference | not reproduced, see error 3 |
| §11 | tau 15.1 (3D), 15.3 (twin), 14.2 exact, 6–8 % | verified (15.112, 15.33; +6.4 %, +7.9 %) |
| §11 | fit window 60 % → 5 % (or to the end) | verified (`fit_tau`) |
| §11 | T_far rule; 0.179 vs 0.186, 4 % | verified (`summary()`; 0.1793/0.1861 = 0.963) |
| §12 | walls at E = 0.65: tau 15.1, T 0.176; R = 2: tau 1.99, side 2.28, T 0.936; one disc R = 4: 0.678, R = 6: 0.415 | from index (gen2 = NUM); 2.28 arithmetic verified |
| §12 | R^2 column 144, 81, 36, 16, 4 | verified |
| §12 | R = 2 lifetime shorter than one round trip | verified (1.99 < 4.45) |
| §12 shells | 66.9 @0.30, 110 @0.35, 63.2 @0.40, 104 @0.45; 16 runs each; cut flags | from index (gen2 = NUM); "lowest energies of the grid" holds |
| §13 table | a = 2.75 nm, 4.13 nm, 300 meV, 110 meV, 10.6 meV, 62 fs | verified (2.7536 nm, 4.130 nm, 110.25 meV, 10.56 meV, 62.3 fs) |
| §13 | E_F = 150 meV, kT = 0.05 → 87 K | verified (87.03 K) |
| §13 | m* = 0.067 m_e; 0.30 eV for 35 % Al | unverifiable: I did not read Vurgaftman et al.; it is consistent with ~65 % of the Gamma-gap difference (≈0.28–0.30 eV) |
| §13 | peaks 0.735, 0.483, 0.226; heights 1, 0.877, 0.559 | verified (nper 200 gives the same to 4 digits) |
| §13 | level falls by about half the bias | verified (0.252 at 0.5, 0.509 at 1.0) |
| §13 | V_p 0.875 (131 mV), V_v 1.825 (274 mV), PVR 4.3 | verified (`iv_curve` re-run; a 0.01 grid gives 0.87, 1.82, 4.32) |
| §13 | supply 14.2 → 18.0; area 0.103 → 0.073 → 0.041 | verified (14.15, 18.04; 0.1030, 0.0730, 0.0405) |
| §13 | diode from runs: 170 of 500 walls filed | from index (gen2 = NUM); "about a third" verified (34 %) |
| Fig. 3 | to-scale energies (V0 = 2 → 88 px, V_b = 1 → 44 px; levels 0.735 at y = 132, 0.226 at y = 154; E_F = 1 at y = 120; collector filled to 0) | verified, coordinate by coordinate |
| §13 box | 1.92 THz (Maekawa 2016) | unverifiable: not read; it matches the cited title |
| §14 Problem 3 | (not stated) crossing time 5.4 fs, about 11 crossings | consistent |

# Chapter 2 "The source": independent check of equations, numbers and method

Page checked: `public/portfolios/electron-beam/index.html`, element `#ch02` (built 9 Nov 2026 20:16; its text matches `text/ch02.py` as built now).
Inputs read: `text/ch02.py`, `physics/ch02.js`, `physics/ch02_ui.js`, `ref/ch02.py`, `derive/ch02.py`, `data/ch02/derive_results.json`, `data/ch02/README.md`.

How the check was done:

- **Equations.** Each of the 34 numbered equations was re-derived in SymPy (1.13, Python 3.13), not by re-running `derive/ch02.py`. Integrals that SymPy cannot do in closed form were done in mpmath at 25 to 30 digits. This covers v(f) by direct quadrature of the barrier, the exact t(f), the Fermi-integral kernel of (2.21), and the order-exchange identity of (2.26).
- **Numbers.** Every number was recomputed in headless Chromium (Playwright, Chrome 153) from the page's own solver, `window.EB_CH02`, loaded from the built page. They were then compared with the rendered text (`#ch02.innerText`). The JS solver and the NumPy twin agree to ≤ 4×10⁻¹² relative on every quantity compared (I_e, d_v, J, B_r, FWHM, v, G …).
- **Sources.** Primary sources were opened where reachable: Allaham et al. 2022 (arXiv:2205.15042), Forbes 2013 (arXiv:1209.6611), Ayari et al. 2023 (arXiv:2301.13578), and the Hitachi page. Cho 2014 could not be fetched: doi.org and the KISTI PDF link both timed out, so its quoted values are marked unverifiable.

Scripts are in the scratchpad: `sym.py`, `sym2.py`, `sym3.py`, `js/run.cjs`, `js/reg.cjs`.

## 1. Numbered equations

| eq. | statement | verdict | units / limiting case checked |
|---|---|---|---|
| 2.1 | F = V/(k r) | verified (SymPy: point-charge potential gives surface field V/r, k = 1) | V/m; k = 1 is the isolated sphere |
| 2.2 | F_im = −e²/(4πε₀(2x)²) = −e²/(16πε₀x²) | verified | N; → 0 as x → ∞ |
| 2.3 | U_im = −∫ₓ^∞ e²/(16πε₀x′²)dx′ = −e²/(16πε₀x) | verified; −dU/dx = F_im; the aside (pair energy e²/(8πε₀x) is twice) also verified | J |
| 2.4 | U = φ − eFx − e²/(16πε₀x) | verified (sum of 2.3 and −eFx) | J; F = 0 gives the image-rounded step |
| 2.5 | x₁,₂ = φ(1 ∓ √(1−f))/(2eF), f = 4eFQ₀/φ² = e³F/(4πε₀φ²) | verified (both roots make U = 0; quadratic eFx² − φx + Q₀ = 0 checked); f = F/F_R with F_R = 4πε₀φ²/e³ | f dimensionless; f → 1 roots merge |
| 2.6 | Δφ = √(e³F/(4πε₀)) = φ√f; x_m = √(Q₀/(eF)) | verified (dU/dx = 0 at x_m; U(x_m) = φ − Δφ); constant 1.199985 eV (V/nm)^−½ matches Forbes 2013 table | J |
| 2.7 | −(ħ²/2m)ψ″ + Uψ = wψ | verified | J |
| 2.8 | ψ ≈ ψ(x₁)exp(−∫κdx) | verified (WKB without the κ^−½ prefactor, as the text says) | κ in m⁻¹ |
| 2.9 | D ≈ e^−G, G = (2/ħ)∫√(2m(U−w))dx | verified as the WKB/Gamow form. The code does not use it; see M1 | G dimensionless |
| 2.10 | G_△ = (2/ħ)∫₀^{φ/eF}√(2m(φ−eFx))dx = 4√(2m)φ^{3/2}/(3ħeF) | verified; b = 6.830 890 eV^−3/2 V nm⁻¹ (Forbes 2013: 6.830 890) | dimensionless |
| 2.11 | substitution x = x₁ + Δsin²ϑ; G = (2√(2m)/ħ)√(eF)∫2Δ²sin²cos²/√(x₁+Δsin²)dϑ | verified: (x−x₁)(x₂−x) = Δ²sin²cos², dx = 2Δ sin cos dϑ, U − w = eF(x−x₁)(x₂−x)/x all checked in SymPy. The integrand and prefactor in `barrierG` match line for line | v(0) = 1, v(1) = 0 by mpmath (v(10⁻⁶) = 0.999996, v(0.9999) = 8×10⁻⁵) |
| 2.12 | v ≈ 1 − f + (f/6)ln f | verified: max error on 199 points (0.005 to 0.995) is 0.0023772, and on 999 points 0.0023772 (mpmath); limits 1 and 0 | — |
| 2.13 | dJ_in = e(2/h³)𝓕 v_x d³p | verified | A m⁻² |
| 2.14 | J = e∫dw D (4πm/h³)∫𝓕(w+ε_t)dε_t | verified (v_x dp_x = dw; dp_y dp_z = 2πm dε_t) | A m⁻² |
| 2.15 | N(w) = (4πm kT/h³)ln(1+e^{−w/kT}) | verified (SymPy integral gives kT ln(e^{w/kT}+1) − w, the same thing); limit N → 4πm(−w)/h³ for T → 0, w < 0 verified | s kg⁻¹ m⁻⁴ = (m² s J)⁻¹ |
| 2.16 | G ≈ G_F − w/d, 1/d = −dG/dw | verified (definition; dG/dw = −∂G/∂φ because the image term is w-independent) | d in J |
| 2.17 | ∂G/∂φ = (3b√φ/2F) t(f), t = v − (4/3)f v′ | verified (SymPy with general v(f), f ∝ F/φ²) | J⁻¹ |
| 2.18 | t ≈ 1 + f/9 − (f/18)ln f | verified (from 2.12 and 2.17). Exact t(0.2844) = 1.04807 (mpmath), Forbes form 1.05147: 0.325 % apart, as the text says | t(0) = 1 |
| 2.19 | J₀ = (4πme/h³)d²e^{−G_F} | verified (∫₋∞⁰(−w)e^{w/d}dw = d²) | A m⁻² |
| 2.20 | J₀ = e³F²/(8πhφt²)·exp(−v bφ^{3/2}/F) | verified (SymPy with d = ħeF/(2√(2mφ)t), ħ = h/2π) | A m⁻²; a = e²/(8πh) = 1.541 434 µA eV V⁻² |
| 2.21 | J(T) = J₀(πkT/d)/sin(πkT/d) | verified: the by-parts step and the kernel ∫e^{au}/(1+e^u)du = π/sin πa (mpmath, 10⁻²⁰); the full ratio at kT = 0.025852, d = 0.17502 eV agrees to 2×10⁻²⁴ | → 1 as T → 0; diverges at kT → d |
| 2.22 | ln(I/V²) = ln(Aa/(φt²ζ²)) − bφ^{3/2}ζ v/V | verified (from I = A J₀(V/ζ)) | — |
| 2.23 | S_FN = −bφ^{3/2}ζ(1 − f/6) | verified (d[X v(c/X)]/dX = v − f v′ = 1 − f/6 exactly for Forbes' v). As usual, the slow V-dependence of t² in the intercept is neglected | V |
| 2.24 | J = A_R T² e^{−φ/kT}, A_R = 4πmek²/h³ | verified; A_R = 1.201 73×10⁶ A m⁻² K⁻² | A m⁻² |
| 2.25 | J = A_R T² exp(−(φ−Δφ)/kT) | verified (2.24 with φ → φ − Δφ) | F → 0 gives 2.24 |
| 2.26 | P(ε) = 𝓕(ε)∫₋∞^ε D dw, J = e(4πm/h³)∫P dε | verified (order exchange / by parts; mpmath on a smooth test D: agreement 7×10⁻²²) | — |
| 2.27 | P ∝ e^{ε/d}/(1+e^{ε/kT}) | verified; the peak ε* = kT ln[kT/(d−kT)] also verified (root of d ln P/dε). But see N-row "peak −0.046" and wording W2 | — |
| 2.28 | j(ε_t) = e(4πm/h³)∫D 𝓕(w+ε_t)dw | verified | A m⁻² J⁻¹ |
| 2.29 | B_r = (e/π) j(0) | verified (dΩ = π dε_t/(eV), B = j eV/π) | A m⁻² sr⁻¹ V⁻¹ |
| 2.30 | B_r = J/(π d[eV]) | verified (j = (J/d)e^{−ε_t/d}; ⟨ε_t⟩ = d) | as 2.29 |
| 2.31 | b = L/p∞ = r√(ε_t/(eV)) | verified, with "=" really "≈": p∞ = √(2m(eV + ε_t + E_n)); C17's numbers 0.70687 / 0.70686 / 0.70711 nm reproduced by hand | m |
| 2.32 | Φ = n√(kT/(2πm)) = p/√(2πm kT) | verified (MB normalised; three integrals in SymPy) | m⁻² s⁻¹ |
| 2.33 | dθ/dt = a(1−θ) − k_d θ | verified (Langmuir, first order; definition) | s⁻¹ |
| 2.34 | θ = θ∞ + (θ₀−θ∞)e^{−(a+k_d)t}, θ∞ = a/(a+k_d) | verified (satisfies the ODE and θ(0) = θ₀); t* = −ln(1−θ*/θ∞)/(a+k_d) verified; t* ≈ θ*/a holds to O(θ*²) (5 % at θ* = 0.1) | — |

## 2. Statements around the equations (wording and physics)

| where | statement | verdict |
|---|---|---|
| W1, §2.5.2 after (2.20) | "At about f≈0.8 the derivation fails, as Allaham et al. note, because electrons at the Fermi level can fly over the barrier top" | **wrong, because** at f = 0.8 the barrier top is φ(1−√f) = 0.106 φ = 0.475 eV above the Fermi level (page JS). Fermi-level electrons fly over only at f = 1, which is how Allaham et al. define F_R. Allaham et al. say separately that the MG derivation "breaks down at a f_C value around 0.8". Correct form: "At about f ≈ 0.8 the derivation fails (Allaham et al. 2022); the barrier top is then only ≈ 0.1 φ above the Fermi level, and Fermi-level electrons fly over it at f = 1." |
| W2, §2.7 | "The peak is at ε* = kT ln[kT/(d−kT)] when d > 2kT" | **wrong, because** the peak exists whenever d > kT. d > 2kT is the condition for ε* < 0 (peak below the Fermi level). Correct: "when d > kT; it lies below the Fermi level when d > 2kT". |
| W3, §2.5.1 | "For the triangular barrier v = 1, t = 1, and d = ħeF/(2√(2mφ)) … d is an energy, 0.175 eV at the working point" | **wrong, because** the triangular-barrier formula gives 0.184 eV at 4 V/nm and 4.5 eV. 0.175 eV is d with t(f) = 1.0515 (`d_tunnel`). Correct: "0.184 eV for the triangular barrier, 0.175 eV with the image term (d = ħeF/(2√(2mφ) t))". |
| W4, §2.11 | "\\(\ln J\\) varies as \\(F^{17}\\) locally" | **wrong, because** it is J, not ln J, that varies as F^17.5 (∂ln J/∂ln F = 17.46). Correct: "J varies as F^{17.5} locally". |
| W5, key box after (2.20) | FN equation "is exact within the model of sections 2.2 to 2.4, at T = 0 and for f away from 1" | **wrong, because** it rests on the linearisation (2.16) of G in w, and the page evaluates it with Forbes' approximate v and t (t is 0.32 % off, which gives about 0.65 % in J). Correct: "the leading-order (linearised-exponent) result of the model …". |
| W6, §2.5.2 limits | "for F → 0 the equation becomes the triangular-barrier form of Fowler and Nordheim (1928)" | **unverifiable, because** FN 1928 was not opened. For the record, the 1928 prefactor contains the factor √μ/(μ+φ) (Fermi energy μ), so the v = t = 1 form is usually called the "elementary FN-type equation" rather than the 1928 form. |
| W7, §2.3 | "(the exponent in Example 2.2 is 10.7)" | **wrong, because** G = 10.66 is first given in Example 2.3; Example 2.2 gives only the roots and the top. Correct: "Example 2.3". |
| W8, §2.9 | Dyke and Trolan X89 "which Forbes (2013) re-analysed, covers 0.20 < f < 0.34" | range verified (Forbes 2013, p. 16); attribution slightly off: Forbes 2013 states the re-analysis is Forbes 2008a. |
| W9, §2.10.1 | "at 10⁻⁴ Pa a clean surface is covered in a fraction of a second" | **wrong, because** the page's own table gives 0.93 s (H₂, shown as "1 s") and 3.5 s (CO) at unit sticking. Correct: "in about one second (H₂) to a few seconds (CO)". |
| W10, §2.6.1 | regime: "at the top, thermionic or Schottky" | verified with a nuance: the code labels thermionic when the peak is within 3 kT of the top or above it (`peak < top − 3kT` → thermal-field). |
| W11, §2.10.2 | "When k_d is negligible, t* ≈ θ*N_s/(κsΦ)" | verified as a small-θ* approximation (−ln(1−θ*) ≈ θ*; 5 % at θ* = 0.1). The Cho fit and Fig. 2.7 use this linear form; the flash table uses the exact t*. |

## 3. Every number in the text

Each number was recomputed with `EB_CH02` in Chromium and compared with the rendered text, unless the row says otherwise.

| § | quoted | recomputed | verdict |
|---|---|---|---|
| 2.1 | φ = 4.5 eV, "accepted average value" (Dolan & Dyke 1954) | — | unverifiable, because Dolan & Dyke was not opened (paywalled); 4.5 eV used as input |
| 2.1 | 1 eV = 1.602 176 634×10⁻¹⁹ J | exact SI | verified |
| 2.1 | k = 5 (Chapman 1971; Ayari 2023) | Ayari et al. use Gomer's β = 1/(5r) (arXiv p. 9) | verified for Ayari; Chapman unverifiable (not opened) |
| Ex 2.1 | F = 4.00×10⁹ V/m = 4.0 V/nm | 4.000×10⁹ | verified |
| Ex 2.1 | proton field at a₀: 5.14×10¹¹ V/m; 1/129 | 5.1422×10¹¹; 128.56 | verified |
| Ex 2.1 | φ/(eF) = 1.125 nm | 1.125 | verified |
| 2.2 | F_R = 14.06 V/nm | 14.0628 | verified |
| (2.6) | 1.2000 eV×√(F/(V/nm)) | 1.199985 | verified |
| Ex 2.2 | f = 0.2844; x₁ = 0.087 nm; x₂ = 1.038 nm; Δφ = 2.40 eV; top 2.10 eV; width 0.95 nm | 0.284437; 0.08668; 1.03832; 2.39997; 2.10003; 0.95165 | verified |
| 2.3 | G "of order 10", 10.7 | 10.658 | verified (but see W7 for the cross-reference) |
| 2.3 | 2κ_e = 10.246 eV^−½ nm⁻¹ | 10.24633 (Allaham et al. quote 10.24633) | verified |
| 2.3.1 | b = 6.8309 eV^−3/2 V nm⁻¹; Forbes 6.830 890 | 6.830 890 (Forbes 2013 table) | verified |
| 2.3.1 | G_△ = 16.30 | 16.3018 | verified |
| 2.3.2 | Forbes v good to 0.0024; ours 0.00238 on 199 values | 0.0023772 (JS, and mpmath on its own) | verified (Forbes 2006 itself not opened) |
| 2.3.2 | v = 0.6538 (quadrature), 0.6560 (Forbes) | 0.653793; 0.655961 | verified |
| Ex 2.3 | G = 16.30×0.6538 = 10.66; D = 2.35×10⁻⁵; ×283; 1 in 42 532 | 10.6580; 2.3512×10⁻⁵; 282.53; 42 532.3 | verified |
| 2.5.1 | d = 0.175 eV | 0.175020 | verified as d with t (see W3) |
| 2.5.1 | C8: agreement 2.5×10⁻¹¹; Forbes t 0.32 % off | t_exact 1.048068 vs 1.051471 → 0.325 % (mpmath) | verified |
| key, table | a = 1.5414 µA eV V⁻²; b = 6.8309 | 1.541434; 6.830890 | verified |
| table | J₀ = 1.13×10⁸ A/m² at 4 V/nm | 1.12504×10⁸ (jFN, Forbes v and t) | verified as the output of `jFN` |
| table | f 0.2844; v 0.6538; t 1.0515 | 0.284437; 0.653793 (quadrature); 1.051471 (Forbes t) | verified. Note that 1.0515 is Forbes' (2.18), not the exact v − (4/3)fv′ = 1.0481 that the "meaning" column names |
| Ex 2.4 | J₀ = (1.5414×10⁻⁶/4.5)×4²/1.051²×e^{−10.66} A/nm² "which is 1.13×10⁸ A/m²" | the arithmetic as written gives 1.165×10⁸ A/m² | **wrong, because** the printed exponent 10.66 uses the quadrature v = 0.6538, but 1.13×10⁸ comes from `jFN`, which uses Forbes' v = 0.6560, i.e. e^{−10.693}. Correct: either write e^{−10.69} (v = 0.6560) and keep 1.13×10⁸, or keep e^{−10.66} and give 1.16×10⁸ A/m² |
| Ex 2.4 | full integral 1.16×10⁸ A/m² at 300 K | 1.16160×10⁸ | verified |
| 2.5.3 | πkT/d = 0.464; factor 1.037; 3.7 % | 0.46404; 1.03681; 3.68 % | verified |
| 2.6 | A_R = "1.20173e+06" A m⁻² K⁻² | 1.201732×10⁶ | value verified; **wrong as typeset, because** the format `.5e` prints "1.20173e+06" inside KaTeX (visible on the page and in check row C10). Correct: 1.20173×10⁶ (format `tex5`) |
| 2.6 | Schottky preset φ = 2.9 eV, T = 1800 K, F = 0.5 V/nm | inputs (assumed, stated) | verified as stated inputs |
| 2.6 | kT = 0.155 eV; Δφ = 0.849 eV; gain 238 | 0.155112; 0.848518; 237.54 | verified |
| 2.6 | J_R 2.96×10⁴ → J_RS 7.02×10⁶ A/m²; full 8.14×10⁶, 16 % above | 2.9560×10⁴; 7.0219×10⁶; 8.1428×10⁶; 15.96 % | verified |
| 2.6.1 | C11: within 2.4 % at 4 and 5 V/nm; within 0.5 % at 2800 K, 0.1 V/nm | 0.9958, 0.9765 → 2.35 %; 1.00533 → 0.53 % | verified (3 V/nm, not quoted, is 2.1 %) |
| Fig 2.4 | 4 V/nm nearly T-independent up to ≈1000 K; 0.5 V/nm rises by orders of magnitude | 4 V/nm: 1.16×10⁸ (300 K) → 1.48×10⁸ (800 K) → 1.93×10⁸ (1100 K); 0.5 V/nm: 10⁻⁴⁰ → 8×10⁶ | verified |
| 2.7 | C12 ratio 1 + 2.3×10⁻⁵ | 1.0000230 | verified |
| 2.7 | peak "−0.046 eV" from ε* = kT ln[kT/(d−kT)] | formula: −0.04531 eV → −0.045; full-integral grid peak: −0.04616 | **wrong, because** the text attaches the full model's peak (−0.046) to the analytic formula, which gives −0.045 eV (`more_numbers` overwrites `peak_cfe_eV` from derive with `mC['peak']`). Correct: "−0.045 eV (the full integral puts it at −0.046 eV)" |
| 2.7 | d = 0.175 eV; kT = 0.0259 eV; FWHM 0.218 (linearised) and 0.215 eV (full) | 0.175020; 0.025852; 0.21794 (my root-finding: −0.19450 to +0.02343 eV); 0.214726 | verified |
| 2.7 | ΔE = 0.184, 0.215, 0.245 eV at 3, 4, 5 V/nm | 0.18394, 0.21473, 0.24493 | verified |
| 2.7 | Schottky ΔE = 0.43 eV; peak 0.15 eV above the top | 0.42510; 0.14766 | verified |
| 2.7 | Hitachi: 0.2–0.3 eV (CFE), 0.6–1.1 eV (Schottky) | Hitachi page fetched 9 Nov 2026: "typically around 0.2–0.3 eV", "around 0.6–1.1 eV" | verified |
| 2.7 | cold 0.21 eV, Schottky 0.43 eV | 0.2147; 0.4251 | verified |
| 2.8.1 | J/(πd) = 2.11×10⁸; full 2.17×10⁸ | 2.11260×10⁸; 2.17024×10⁸ | verified |
| 2.8.1 | ⟨ε_t⟩ 0.168 eV (cold), 0.155 eV (Schottky) | 0.167930; 0.155112 | verified |
| 2.8.1 | Schottky B_r 1.67×10⁷; factor 13; J 1.16×10⁸ vs 8.14×10⁶ | 1.67100×10⁷; 12.99; as above | verified |
| 2.8.1 | Hitachi "up to about 10⁹ A/cm²·sr" | quoted on the page | verified |
| 2.8.2 | C17: 0.70687 vs 0.70686 nm | reproduced: L/p∞ = 0.70686 nm; r√(ε_t/eV) = 0.70711 nm | verified |
| 2.8.2 | d_v = 1.30 nm (cold), 8.8 nm (Schottky) | 1.29588; 8.80659 | verified |
| 2.8.2 | Hitachi: 2.5–5 nm, 15–30 nm | quoted on the page | verified |
| 2.9 | Ayari setup: ⟨111⟩, 125 µm, 15 nm, 30 s at 1700 K, 3×10⁻¹⁰ Torr (4×10⁻⁸ Pa), 1300–1630 V | arXiv:2301.13578 §III; 3×10⁻¹⁰ Torr = 4.0×10⁻⁸ Pa | verified |
| 2.9 | 33 points | 33 (run 4 down, 1310–1630 V in 10 V steps) | verified (this sweep starts at 1310 V, not 1300 V) |
| 2.9 | slope −41 339 V, intercept 4.578; authors 41 339 ± 73, 4.57 ± 0.05 | −41 339.0; 4.5782; paper Fig. 2 caption | verified |
| 2.9 | φ = 4.5 eV "which the authors also assume" | arXiv p. 8: "If we assume that the work function φ = 4.5 eV" | verified |
| 2.9 | s(f) = 0.974; ζ = 651 nm from the slope | 0.97350; 651.22 | verified |
| 2.9 | fit ζ = 657.5 nm; A = 781 nm²; rms 1.8 %; max 5.8 %; r = 132 nm | 657.52; 780.68; 1.849 %; 5.84 %; 131.50 | verified (131.50 rounds to 132 under round-half-even; 131.5 is the value) |
| 2.9 | authors 653 nm and 131 nm (paramIV4d.txt) | paper text gives 1/β = 653 nm; 653/5 = 130.6 | 653 nm verified from the paper; paramIV4d.txt itself unverifiable (not in the repository) |
| 2.9.1 | rms 0.0185 for φ = 4.0–5.5 eV; ζ = 788, 658, 560, 484 nm | rms 0.018470–0.018506; ζ 787.7, 657.5, 559.7, 484.0 | verified |
| 2.9.1 | current range factor 752 | 751.6 | verified |
| 2.9.1 | drift 8 %/h; noise 1.8 % | paper: "in the order of 8 % per hour"; 1.82 % | verified |
| 2.9.1 | I(1470 V) list, ten sweeps | matches the CSV values to 3 s.f. | verified |
| 2.9.1 | "The fit gives a tip of 130 nm radius" | 131.5 nm (shown as 132 nm two paragraphs earlier) | **wrong, because** it is typed by hand and contradicts the 132 printed above (130 nm is the authors' rounded value). Correct: "about 130 nm (131.5 nm)" or read from `ayari/fits/4.5/r_nm` |
| 2.9.1 | f = 0.142–0.176; F = 1.99–2.48 V/nm | 0.14167–0.17628; 1.9923–2.4790 | verified |
| 2.9.1 | Forbes "reasonable" 0.15 ≤ f ≤ 0.45; "clearly unreasonable" 0.10 (Allaham Table 1) | Allaham Table 1, φ = 4.5 eV column: f₁ = 0.10, f₂ = 0.15, f₃ = 0.45 | verified |
| 2.9.1 | X89: 0.20 < f < 0.34; working point f = 0.28 inside | Forbes 2013 p. 16; 0.2844 | verified (see W8) |
| 2.10.1 | Φ(H₂, 10⁻⁹ Pa) = 1.07×10¹⁴; Φ(CO) = 2.87×10¹³ m⁻² s⁻¹ | 1.07137×10¹⁴; 2.87478×10¹³ | verified |
| 2.10.1 | 1/a² = 9.98×10¹⁸ m⁻² (a = 0.3165 nm) | 9.9828×10¹⁸ | verified |
| 2.10.1 | monolayer table (H₂/CO): 1 s/3 s, 93 s/6 min, 2.6 h/9.7 h, 25.9 h/4.0 days, 10.8 days/40.3 days | 0.93/3.48 s, 93.3/347.9 s, 2.593/9.663 h, 25.93 h/4.026 d, 10.80/40.26 d | verified (see W9 for the sentence below the table) |
| 2.10.1 | 10⁻¹¹ mbar = 10⁻⁹ Pa; 25.9 h | exact; 25.927 h | verified (the Applied Materials quote is unverifiable, because the press release was not opened in this check) |
| 2.10.3 | Δφ_ads = 1.0 eV → ρ = 0.0021 | 0.0021195 | verified |
| 2.10.3 | ∂ln J/∂ln F = 17.5; ∂ln J/∂ln φ = −26.6 | 17.461; −26.576 | verified |
| 2.10.3 | +0.1 eV (2.2 %) → ×0.55; +1 eV → ×0.0021; +10 % F → ×4.9 | 0.5526; 0.0021195; 4.9151 | verified |
| 2.10.4 | Cho: τ₉₀ = 15, 105, 450 min at 2×10⁻⁸, 2–3×10⁻⁹, 6–8×10⁻¹⁰ Pa; > 99 % H₂; C_CH = 1.93×10⁻⁷ Pa·min | — | unverifiable, because Cho 2014 could not be fetched (doi.org and KISTI PDF both timed out) |
| 2.10.4 | pτ = 3.00, 2.63, 3.15 ×10⁻⁷ Pa·min; ±9 %; factor 29 | 3.000, 2.625, 3.150; ±8.97 %; 28.6 | verified (arithmetic on the quoted inputs) |
| 2.10.4 | κs = 0.52, 0.59, 0.49, mean 0.54 | 0.5185, 0.5926, 0.4939; 0.5350 | verified |
| 2.10.4 | "one and a half decades" | log₁₀ 28.6 = 1.46 | verified |
| 2.10.5 | k_d = 1.2×10⁻¹⁹ (300 K), 0.21 (700 K), 2657 (1000 K), 1.6×10⁸ s⁻¹ (2000 K) | 1.206×10⁻¹⁹; 0.2092; 2657.2; 1.630×10⁸ | verified |
| 2.10.5 | 1/k_d(700 K) = 4.8 s | 4.780 | verified |
| 2.10.5 | flash after 104 min at 10⁻⁸ Pa; table 10 min, 104 min, 17.3 h, 7.2 days, 72.2 days | t* = 6238 s = 103.97 min; 623.8 s, 6238 s, 62 385 s, 623 849 s, 6.238×10⁶ s | verified |
| Fig 2.8 | flashes every 104 min, 5 s at 1000 K, threshold 0.7 | cycle(): flashes at 103.98, 208.05, 312.12 min | verified |
| 2.10.5 | "\\(\nu_0=10^{13}\\)" | page renders **"u₀ = 10¹³ s⁻¹"** | **wrong as typeset, because** `text/ch02.py` line 743–744 has a literal line break where the `\n` of `\nu` was, so KaTeX shows "u₀". Correct: `\(\nu_0=10^{13}\ \mathrm{s^{-1}}\)` on one line |
| 2.10.5 | 8201 sites; 820 nm²; one atom 1.2×10⁻⁴ | 8200.6; 820.06; 1.219×10⁻⁴ | verified |
| 2.11 | 4 V/nm; F^{17}; 820 nm², 5 %, 15 708 nm²; 0.17 eV | 4.0; 17.46; 820.06, 5.22 %, 15 707.96; 0.1679 | numbers verified; the "ln J varies as" wording is wrong (W4) |
| 2.11 | ∂ln J/∂ln φ = −27; 0.1 eV removes 45 %; 1 eV removes 99.8 % | −26.58; 44.74 %; 99.79 % | verified |
| 2.11 | 25.9 h; current falls 10 % "in a few hours" at 10⁻⁹ Pa | t(θ = 0.1, κs = 0.535) = 5.1 h | verified |
| 2.13.1 | JS and NumPy agree to 10⁻⁹ | ≤ 4×10⁻¹² relative here | verified |
| 2.13.1 | hand-over: F 4.00/0.50 V/nm; I_e 9.53×10⁻⁸/3.64×10⁻⁶ A; B_r 2.17×10⁸/1.67×10⁷; ΔE 0.215/0.425 eV; d_v 1.30/8.8 nm | 4/0.5; 9.5258×10⁻⁸/3.6445×10⁻⁶; 2.1702×10⁸/1.6710×10⁷; 0.21473/0.42510; 1.2959/8.8066 | verified |
| 2.13.3 | 19 of 19 checks pass | derive_results.json summary | verified; check C2's detail "= 1.1999 eV (V/nm)^−½" is a hand-typed rounding of 1.199985 (should read 1.2000) |
| Prob. 1 | F = 5.33 V/nm; f = 0.379; v = 0.559; J₀ = 9.23×10⁹ A/m² | 5.3333; 0.37925; 0.55947; 9.2326×10⁹ | verified |
| Prob. 2 | −(3/2)×16.30×1.051 = −25.7; full −26.6 | −25.711; −26.576 | verified (the identity ∂ln J/∂ln φ ≈ −(3/2)bφ^{3/2}t/F also verified from 2.17) |
| Prob. 3 | 3479 s (CO), 933 s (H₂) at 10⁻⁷ Pa | 3478.5; 933.39 | verified |

## 4. Description of the numerical method against the code

| item | the note says | the code does | verdict |
|---|---|---|---|
| M1 | Key result §2.4: "D = e^−G from (2.9) … the code of this page evaluates it numerically" | `emissionModel` (JS l.113–118, ref l.140–141): **D = 1/(1+e^G)** (Kemble form). Above the barrier top it uses G = −(w − top)·s_top, a linear continuation with slope s_top = G(top − 0.02 eV)/0.02 eV (the "parabolic-top (Kemble) continuation" in a code comment) | **wrong, because** the page never states the Kemble form or the continuation above the top. Every "full integral" number (J, ΔE, B_r, ⟨ε_t⟩, hand-over, the Schottky "16 % … tunnelling through the top", C11–C14) depends on it. Near the top, e^−G and 1/(1+e^G) differ by up to a factor 2. Correct: state D(w) = 1/(1+e^{G(w)}), and for w above the top D = 1/(1+e^{−(w−top)s_top}) |
| M2 | §2.3.2: Gauss–Legendre "48 points" | 48 in `barrierG` default (G_ex); **64** in `vExact` (v = 0.6538, Fig. 2.3, C7); **24** in `emissionModel` for every energy (all full-integral numbers) | **wrong, because** the full integral uses 24 points and v(f) uses 64. Correct: "48 points for G(0), 64 for v(f), 24 inside the energy integral" |
| M3 | energy integral "numerically, without limits" | trapezoid rule on w ∈ [−max(25d, 12kT), max(14kT, top + 14kT)], n = max(400, min(2400, ⌈range/(min(d,kT)/14)⌉)); 500 points inside the cap integral | consistent ("without limits" means no asymptotic limits), but the finite window and the 500-point cap grid are not stated |
| M4 | FN plot: "the full integral … over the apex cap, **21 voltages**" | `ch02_ui.js` l.71–76: **13 voltages** from 0.70 V to 1.15 V, cap integral with 16 Gauss nodes | **wrong, because** there are 13 points, not 21. Correct: "13 voltages from 0.70 V to 1.15 V" |
| M5 | FN plot "with the straight line of slope (2.23)" | the dashed line is a least-squares fit through the 13 clean-tip points (`drawFN`); (2.23) is used only to turn that slope into ζ, which is stored and not shown (260 nm against kr = 250 nm at the cold preset) | **wrong, because** the line's slope is fitted, not computed from (2.23). Correct: "the least-squares straight line through the clean tip; (2.23) turns its slope into ζ" |
| M6 | "radius of the drawn apex: slider; drawn to scale against the shank" (also printed on the canvas) | `drawTip`: rpx = 12 + 44·ln(r/10 nm)/ln 60, a **logarithmic** map from 10–600 nm to 12–56 px; the shank cone is built from rpx | **wrong, because** the drawn radius is on a log scale (50 nm → 29 px, 500 nm → 54 px), not to scale. Correct: "drawn on a logarithmic scale (12 px at 10 nm to 56 px at 600 nm)" |
| M7 | field-line and electron-dot density follow F and I | lines = round(2 + 1.6 F[V/nm]) clipped to 3–13; dots = 34·(log₁₀ I + 12)/9 | verified (the caption says "logarithm of the current") |
| M8 | dark dots ∝ θ | round(40 θ) | verified |
| M9 | P(ε) mixed with weights 1−θ, θ | `mixture()` | verified |
| M10 | θ(t) from (2.34), flashes below threshold; whole run computed at once and replayed | `cycle()` with exact `coverageStep`, dt = t_max/4000; playback only reads | verified; flash times are quantised to dt |
| M11 | patch model ρ = J(φ+Δφ_ads)/J(φ) at the same field (0.0021) | the simulation uses ρ = I_covered/I_clean from the cap integral of the full model (0.00168 at the cold preset); the text tables use the FN ratio | minor mismatch, not stated; effect on the flash time below 0.05 % |
| M12 | cap: F = F₀cos ϑ, J integrated over the hemisphere | I = 2πr²∫₀¹J(F₀u)du (24 nodes for the hand-over, 16 in the simulation) | verified |
| M13 | analytic J(T) used in fits | `jFN` returns NaN when πkT/d ≥ 1.5; `fit_tip` treats NaN as a bad ζ | not stated on the page; consistent with "poor description well before kT → d" |

## 5. Summary of errors

1. **(2.9) / key result §2.4, method:** the code uses D = 1/(1+e^G) with a linear-in-energy continuation of G above the barrier top, not D = e^−G. The page should say so.
2. **§2.3.2, method:** the Gauss–Legendre point counts are 24 for the full integral and 64 for v(f), not 48 throughout.
3. **Example 2.4:** e^{−10.66} (quadrature v) is inconsistent with the quoted 1.13×10⁸ A/m², which uses Forbes' v and e^{−10.69}. The printed arithmetic gives 1.16×10⁸.
4. **After (2.20):** at f ≈ 0.8 Fermi-level electrons do not fly over the barrier, whose top is still 0.475 eV above them. Fly-over happens at f = 1. Allaham et al. give the 0.8 breakdown without that reason.
5. **Key result after (2.20):** "exact within the model" is overstated. The equation is the linearised-exponent result.
6. **§2.5.1 near (2.17):** the triangular-barrier d is 0.184 eV; 0.175 eV includes t(f).
7. **§2.7 near (2.27):** the formula peak is −0.045 eV, and −0.046 is the full integral's peak. The peak exists for d > kT; d > 2kT puts it below the Fermi level.
8. **§2.11:** J, not ln J, varies as F^17.5.
9. **§2.10.1:** at 10⁻⁴ Pa a monolayer takes about 1 s (H₂) to 3.5 s (CO), not "a fraction of a second".
10. **§2.10.5, typesetting:** `\nu_0` lost its `\n` to a line break and renders as "u₀".
11. **§2.6, typesetting:** A_R renders as "1.20173e+06".
12. **§2.3:** "the exponent in Example 2.2" should be Example 2.3.
13. **§2.9.1:** the hand-typed "130 nm" contradicts the computed 132 nm (131.5) printed two paragraphs earlier.
14. **§2.12 "Equation to screen":** the FN sweep has 13 voltages, not 21. Its dashed line is a least-squares fit, not "of slope (2.23)". The apex radius is drawn on a log scale, not "to scale against the shank".

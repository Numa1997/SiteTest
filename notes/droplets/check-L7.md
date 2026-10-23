# Gate 2 check, L7 (chapter 8): equations (8.1) and (8.2)

Text: `portfolios-src/droplets/text/book-08.src.html` (current version). Scripts and printed outputs: `notes/droplets/gate2/`.
Route 1 = SymPy 1.14. Route 2 = Wolfram Language 15.0.1 plus NumPy/SciPy (pair-clock simulation, own evaluation of the law, the table of 8.3 from `data/cold.json`, read only).
Source of (8.2) read in this run: Sotiropoulou, Ickes, Nenes and Ekman (2021), Atmos. Chem. Phys. 21, 9741, Appendix B (open access; eq. B5 for F_BR and eq. B8 for graupel-graupel A, C and gamma; the page was fetched through a web-fetch connector). Phillips, Yano and Khain (2017) itself was not opened (the abstract page only), so the check of (8.2) against its source is through Sotiropoulou's Appendix B, which prints it.

| Eq. | Route 1 (SymPy) | Route 2 (Wolfram, and NumPy/SciPy) | Units / limit / sign | Verdict |
|---|---|---|---|---|
| (8.1) dN_new/dt = sum over pairs of K n1 n2 x F | Units: K n1 n2 is m^-3 s^-1 and F is a number, so dN_new/dt is m^-3 s^-1 (checked). Counting: N1 N2 pairs of two kinds, each meeting at K/V, give K n1 n2 events per volume; one kind has N(N-1)/2 pairs, so (1/2) K n^2 (limit K/2 per n^2). The sum over unordered pairs therefore needs the 1/2 for equal bins, which `tools/run_cold.cjs` has (`i === j ? 0.5 : 1`) | NumPy: 3625 independent pair clocks (40 x 60 pairs of two kinds, 50 of one kind) simulated 20 times: rate 2537.40 +- 0.23 against K n1 n2 + (1/2) K n3(n3-1) = 2537.50; a double sum over ordered pairs would give 3395.0. Table arithmetic from the model data: 2.80 x 1.7 = 4.76 ("0 to 4.8"), 0.14 x 12 = 1.68 ("1.7"), 2.6/1.6e-3 = 1625 and 2.6/0.050 = 52 (text "1600 times" and "52 times") | events per m^3 per second; F >= 0. F = 0 (rime splintering at -10 C) gives zero | right |
| (8.2) F = alpha A [1 - exp(-(C K0/(alpha A))^gamma)], gamma = 0.3 | Same form as eq. B5 of Sotiropoulou 2021 (alpha = pi D^2, D = size of the smaller particle; K0 = collision kinetic energy; A asperity density; C fragility); gamma = 0.3 for graupel-graupel (B8). Units: alpha A dimensionless, C K0/(alpha A) dimensionless (checked). With y = (C K0/(alpha A))^gamma: F = alpha A (1 - e^-y). Hard hit: F -> alpha A (limit 1). K0 -> 0: F -> 0. dF/dK0 = alpha A gamma y e^-y/K0 > 0 (monotone). Soft hit: 1 - e^-y = y - y^2/2 + y^3/6, so F = alpha A x^0.3 [1 - x^0.3/2 + ...] with x = C K0/(alpha A); local exponent d ln F/d ln K0 = gamma y e^-y/(1 - e^-y) -> gamma as y -> 0, i.e. the 0.3 power of the text (x = 1.8e-5: correction 1.9 %). Eight orders of energy lower give only 2.4 orders fewer fragments | Wolfram: same limits (1 and 0), same derivative, same local exponent and limit gamma. SciPy: F / (alpha A x^0.3) = 0.9999, 0.9980, 0.9844, 0.9396, 0.8843 for x = 1e-12, 1e-8, 1e-5, 1e-3, 1e-2; F / alpha A = 0.981, 1.00000, 1.00000 for x = 1e2, 1e4, 1e8; numerical local exponent at the worked example 0.2944 | units as left; sign: F >= 0, increasing in K0 and in C | right (as a transcription of the cited law; the law itself is a fit) |

## The worked example of 8.2, recomputed

40 um and 8 um ice spheres (900 kg/m^3) at -10 C, 600 hPa; fall speeds 0.1726 and 0.0076 m/s taken from the text: masses 2.413e-10 and 1.930e-12 kg, K0 = 2.607e-14 J (text 2.6e-14). Coefficients from Sotiropoulou B8: a0 = 3.78e4 (1 + 0.0079/D^1.5) at D = 0.5 mm gives 2.675e7; A = a0/3 + max(2 a0/3 - a0 |T - 258|/9, 0) at T = 263.15 K gives 1.144e7 m^-2 (temperature factor 0.4278); alpha = pi (16 um)^2 = 8.04e-10 m^2; alpha A = 9.202e-3 (text 9.2e-3); C K0 = 1.64e-7 (text 1.6e-7) with C = 6.3e6 J^-1; F = 3.398e-4 (text 3.4e-4), i.e. one fragment per 2943 collisions (text "one per three thousand"). Wolfram gives the same F = 0.000339783. With psi = 3.5e-3 (C = 2.2e4) F = 6.3e-5, ratio 5.37 (soft-limit scaling (1/3.5e-3)^0.3 = 5.45). The old study's rule gives 0.001 x 2.413e-10/4.712e-13 = 0.512 fragments (text 0.51). The thesis liquid fraction polynomial at -10 C is 44.55 %; 301 droplets per cm3 give 134.1 liquid and 166.9 ice (text).

## Table of 8.3 against `data/cold.json` (model output, not under test)

Ice-ice collisions 2.878 cm^-3 min^-1 (text 2.88); riming events with drop radius >= 25 um 2.803, of which the drop is the larger partner 2.799 (text "2.799 of 2.803"); shattering 0 to 4.76 (text 0 to 4.8); breakup 3.01e-4 (psi = 3.5e-3) to 1.61e-3 (psi = 1) (text 3.0e-4 to 1.6e-3); with the true D 0.050; old rule 2.61 (text 2.6); ratios 1623 and 52; event-weighted collision energies at 5 % and 95 %: 1.3e-14 and 2.3e-13 J.

## Notes (none changes a verdict)

1. "Eight to twelve orders of magnitude below the collisions (8.2) was fitted to": not reproduced. My own estimate for ice spheres of 0.5 to 5 mm with a size ratio of at least 2 (Schiller-Naumann drag balance for the fall speeds) gives collision energies of 1e-8 to 1e-4 J, i.e. 5.7 to 10.0 orders of magnitude above the cloud's 1.3e-14 to 2.3e-13 J. The energy range of the experiments behind the fit was not in the sources read, so the text's range is unverifiable here; "six to ten" is what my estimate supports.
2. Sotiropoulou's bulk implementation uses a corrected speed difference, dv = (1.7 (u1 - u2)^2 + 0.3 u1 u2)^(1/2) (after Mizuno 1990 and Reisner 1998), when two fall speeds are close. The text uses dv = |v1 - v2| (the chapter-4 CKE). For the worked example the correction would multiply K0 by 1.71 and F by 1.18. This does not change any conclusion (the correction is part of the source's collision bookkeeping, not of eq. B5), but a reader comparing with that paper should know. Maximum fragments per collision in the source is 100; not reached here.
3. The law is used far below its fitted range, as the text says in the same section. Using the true diameter of the smaller particle in A (16 um instead of 0.5 mm) gives F = 1.28e-2 for the worked example: 38 times more. The recommendation to clamp D to the fitted range is the source's (Sotiropoulou: "set to the nearest limit of the range").
4. Rime splintering "-2 to -16 C, peak near -5 C, stops below about -8 C" and Brownscombe and Thorndike's 14 % and 12 fragments are literature statements. Sotiropoulou's introduction confirms the -8 to -3 C window for rime splintering; the others were not checked.

## Commands run (from `notes/droplets/gate2/`)

```
timeout 250 python3 L7_route1_sympy.py > L7_route1_sympy.out.txt
python3 L7_route2_numeric.py     | tee L7_route2_numeric.out.txt
# Wolfram: code in L7_route2.wl, evaluated in the Wolfram Language evaluator, output transcribed in L7_route2_wolfram.out.txt
```

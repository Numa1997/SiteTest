# Gate 2 check, L6 (chapter 7): Kolmogorov time, Stokes numbers, and the epsilon -> 0 limit of the turbulence formula

Text: `portfolios-src/droplets/text/book-07.src.html` (current version). Chapter 7 has no numbered equation. Scripts and printed outputs: `notes/droplets/gate2/`.
Route 1 = SymPy 1.14. Route 2 = Wolfram Language 15.0.1 plus NumPy/SciPy: my own implementation of the formula, transcribed from the primary source and compared with `physics.cjs` `ayalaFactor`.
Primary source read: Ayala, Rosa and Wang (2008), New J. Phys. 10, 075016, Part 2, reprint text from the author's page (research.me.udel.edu/lwang/reprints/Ayala_etal_NJP_Theory.pdf): eq. (81) for the variance sigma^2 in the weak-inertia limit, eq. (26) for the acceleration variance a0 (v_k/tau_k)^2 with a0 = (11 + 7 R_lambda)/(205 + R_lambda), Table 2 (tau_k = (nu/eps)^(1/2), v_k = (nu eps)^(1/4), tau_p, v_p = tau_p abs(g)), eq. (3) and (4) (gravity-only reference abs(v_p2 - v_p1)/2 and enhancement ratio, g12 = 1 here), and the corrigendum of the same journal (2008, 10, 099802) which gives |w_r| = sqrt(2/pi) (sigma^2 + (pi/8)(tau_p1 - tau_p2)^2 g^2)^(1/2) as the recommended form. The IOP pages themselves are blocked from this environment; the text was read through a web-fetch connector.

| Statement | Route 1 (SymPy) | Route 2 (Wolfram, and NumPy/SciPy) | Units / limit / sign | Verdict |
|---|---|---|---|---|
| tau_K = sqrt(nu/eps) | Dimensional analysis: nu^a eps^b with the dimension of a time gives a = 1/2, b = -1/2 (the only combination); the Kolmogorov Reynolds number v_K eta/nu = 1 with eta = (nu^3/eps)^(1/4) | Wolfram `Solve` of the exponent equations: a = 1/2, b = -1/2. tau_K = 41.15 ms at nu = 1.6935e-5 m2/s (10 C, 850 hPa) and eps = 1e-2 m2/s3 (text 41 ms); 130.1 ms at 10 cm2/s3, 20.6 ms at 400 | s (checked). eps -> 0: tau_K -> infinity (smooth flow) | right |
| Response times and Stokes numbers: 8 um droplet 0.8 ms, 40 um collector 18 ms, St about 0.4 at eps = 1e-2 | tau_p = v/g (drag-corrected, as in chapter 3; the paper's Table 2 has v_p = tau_p abs(g) as well) | NumPy: tau_p(8 um) = 0.812 ms, tau_p(40 um) = 18.05 ms, St = tau_p/tau_K = 0.0197 (8 um) and 0.439 (40 um) at 100 cm2/s3 (text 0.8 ms, 18 ms, "about 0.4"); St(40 um) = 0.139 and 0.877 at 10 and 400 cm2/s3. The cut "every collector above 43 um at 400 cm2/s3 has St above 1": St(43 um) = 0.995, St passes 1 at 43.15 um (text 43) | dimensionless. St grows with radius | right |
| Weak-inertia relative speed reduces to gravity at eps -> 0 | Ratio R(eps) = <abs(w_r)>/(abs(v1-v2)/2) with sigma^2 = R^2 eps/(15 nu) + (tau1-tau2)^2 a0 (v_k/tau_k)^2 + (v1 tau1 - v2 tau2)^2 2 eps/(15 nu), closed form of the corrigendum: lim eps->0 R = 1 exactly (sigma^2 -> 0 and sqrt(2/pi) sqrt(pi/8) = 1/2). First order: (R - 1)/eps -> 4 (R^2 + 2 A^2)/(15 pi nu d^2 g^2), d = tau1 - tau2, A = v1 tau1 - v2 tau2; the acceleration term enters at eps^(3/2) | Wolfram: same limit 1 and same first-order coefficient. NumPy (own code from the paper) against `ayalaFactor`: identical to 9 digits at the 9 eps values from 1e-12 to 0.04 m2/s3 and for 11 of 12 other (pair, eps) cases; the two remaining cases (eps = 0.1 for 40 on 8 um, 4e-2 for 50 on 10 um) are ones where the collector's St exceeds 1, and the model returns 1.0 there as the text says (my own code, which has no switch, gives 1.77 and 1.40); (R-1)/eps = 3.56759 at eps = 1e-12 against the predicted 3.56761 | all four terms in m2 s-2 (checked). R >= 1: every term adds positively; d -> 0 makes the gravity reference vanish (hence the size-ratio cut) | right |
| "raises the kernel by 0.4 %, 5.6 % and 28 % at 10, 100 and 400 cm2/s3" (40 um on 8 um) | – | Own implementation: +0.43 %, +5.64 %, +28.14 % (model: +0.43 %, +5.64 %, +28.14 %) | – | right |
| New sentence: "two effects of similar size: accelerations ... and the coupling of settling to the shear; the second is larger at 10 and 100, the first at 400" | – | Each term alone raises the speed by: acceleration +0.07, +2.20, +16.5 %; coupling +0.36, +3.51, +13.4 %; plain shear +0.00 % at 10, 100, 400 cm2/s3. Coupling larger at 10 and 100, acceleration larger at 400: as stated, and the two are comparable | – | right |
| "formula is used inside its range (size ratio below 0.6, radii up to 60 um, St below 1)" | – | The St cut is enforced by the model (checked above). The range 10 to 60 um is the range of the paper's DNS comparison; the 0.6 ratio is the model's own choice (the paper warns that the theory needs gravity to dominate the relative motion) | – | unverifiable as a property of the paper (design choice of the model; no contradiction found) |

## Notes

1. The enhancement is for the geometric kernel with the radial distribution function set to 1 (paper eq. 4, g12 = 1), as the model does; the paper's own empirical RDF would add to it for St > 0.2 or so. The text says only the geometric part is raised ("a lower bound"), consistent.
2. The corrigendum's claim that the closed form is within about 2.5 % of the exact direction average: I find 2.62 % at b = 1.27 (SciPy and Wolfram agree, closed form larger). Not used in the text.
3. The 1.7 % shortening of t90 (-1.1 % at 400 cm2/s3 as an artefact of the cut), the factors of 2 and 7 from Wang et al. (2008), and Grabowski and Wang (2013) are model runs or literature statements, not re-derived here.
4. Firecrawl (the first search connector tried) was out of credits; the second road (Exa fetch of the author's reprint) worked.

## Commands run (from `notes/droplets/gate2/`)

```
python3 L6_route1_sympy.py       | tee L6_route1_sympy.out.txt
node L6_model_dump.cjs > L6_model_dump.json
python3 L6_route2_numeric.py     | tee L6_route2_numeric.out.txt
# Wolfram: code in L6_route2.wl, evaluated in the Wolfram Language evaluator, output transcribed in L6_route2_wolfram.out.txt
```

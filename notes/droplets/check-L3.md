# Gate 2 check, L3 (chapter 4): equations (4.1) and (4.2)

Text: `portfolios-src/droplets/text/book-04.src.html`. Scripts and printed outputs: `notes/droplets/gate2/`.
Route 1 = SymPy 1.14. Route 2 = Wolfram Language 15.0.1 plus NumPy (explicit perfectly inelastic collisions, example numbers with an independently coded surface tension). Fall speeds used in the example numbers are inputs from `vBeard`/`vStokes`.

| Eq. | Route 1 (SymPy) | Route 2 (Wolfram, and NumPy) | Units / limit / sign | Verdict |
|---|---|---|---|---|
| (4.1) KE = (1/2)(m1+m2) V^2 + (1/2) mu_red dv^2, mu_red = m1 m2/(m1+m2) | With V = (m1 v1 + m2 v2)/M the two decompositions printed in the text, v1 = V + (m2/M) dv and v2 = V - (m1/M) dv, hold identically (difference [0,0,0]); KE minus the right side = 0 for symbolic 3-D vectors; the cross term m1 V.(m2 dv/M) - m2 V.(m1 dv/M) = 0. Momentum is conserved, so V is the same before and after; a perfect merger ends with all the mass at V, and the energy lost KE - M V^2/2 equals mu_red dv^2/2 exactly (difference 0), so CKE is the most the collision can turn into deformation and heat | Wolfram: same three statements (0, {0,0,0}, 0). NumPy: 1e5 random masses and 3-D velocities, merger loss against CKE and KE against split: max relative deviation 1.1e-12. 1-D example m = (2,3), u = (4,-1): CKE 15.0, KE before 17.5, after merger 2.5, lost 15.0 | J on both sides (checked). m2 -> oo gives mu_red = m1, CKE = m1 dv^2/2 (wall); equal masses mu_red = m/2; dv = 0 gives CKE = 0; CKE >= 0 | right |
| (4.2) We = CKE/(pi sigma d_c^2), E_coal = exp(-1.15 We) | d_c = (d1^3 + d2^3)^(1/3) follows from volume conservation (equal densities); pi sigma d_c^2 is the surface energy of the merged sphere (area pi d^2); We is dimensionless (checked: J/(N/m . m^2)). E_coal(0) = 1, E_coal -> 0, dE/dWe < 0, E = 1/2 at We = 0.6027. The factor 1.15 and the exponential are a fit (thesis law, Straub et al. 2010 form): nothing to derive | Wolfram: same d_c, limits, derivative; We = 0.52 -> E = 0.54991; We = 61 -> 3.4e-31. NumPy example numbers with sigma = 0.07422 N/m (own IAPWS 2014 code, 10 C): 8 um on 40 um: dv = 0.1691 m/s, CKE = 3.04e-14 J, We = 2.03e-5, E = 0.999977 (text 3.0e-14, 2.0e-5, 0.99998; 1/We = 49 300, text "50 000 times stiffer"); 60 and 50 um: We = 2.86e-4 (text 2.9e-4); radii 500 and 250 um: dv = 2.123 m/s (text 2.1), We = 0.520, E = 0.5500 (text 0.52, 0.55); with Stokes speeds dv = 23.06 m/s, We = 61.3, E = 2e-31 (text 23 m/s, 61, "switched off") | We and E dimensionless; E in (0,1]. Sign: more collision energy, less coalescence | right as a formula; the numerical coefficient 1.15 is an empirical fit, unverifiable by derivation, and its source (Straub et al. 2010) could not be read in this run |

## Notes

1. The "500 um drop meeting a 250 um drop" are radii (diameter 1 mm and 0.5 mm), which is what the numbers need (dv = 2.1 m/s and 23 m/s for Stokes). The text says "a 500 um drop" without saying radius; elsewhere in the notes sizes are radii, so this is consistent, but a reader might take 500 um as a diameter (then dv = 1.16 m/s, We = 0.078 and E = 0.91, model functions `vBeard`, `weber`).
2. The text says the law "was made for drops of 0.35 mm and more" and is used here for cloud droplets where We is 1e-5; the check above shows it is then 1 to within 3e-5 for the 8/40 um pair, but this is extrapolation of a fit, stated as such in the text.
3. Straub et al. (2010) could not be opened (publisher pages are blocked from this environment and the web-search connector Firecrawl was out of credits), so the exponent 1.15 and the definition of We were not compared with the primary source. Marked "fit, unverifiable" rather than "right".

## Commands run (from `notes/droplets/gate2/`)

```
python3 L3_route1_sympy.py       | tee L3_route1_sympy.out.txt
node L3_model_dump.cjs > L3_model_dump.json
node L3_diameter_variant.cjs     | tee L3_diameter_variant.out.txt
python3 L3_route2_numeric.py     | tee L3_route2_numeric.out.txt
# Wolfram: code in L3_route2.wl, evaluated in the Wolfram Language evaluator, output transcribed in L3_route2_wolfram.out.txt
```

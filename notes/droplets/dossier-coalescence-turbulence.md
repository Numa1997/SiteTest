# Dossier: coalescence efficiency and turbulence, Droplet Collection study

Scout dossier, 23 October 2026. Case: 300 cm^-3 droplets of 8 um radius plus 1 cm^-3 collectors of 40 um, 10 C, 850 hPa.
Air constants used below (scout-derived, not from a source): rho_air = 1.046 kg/m^3, mu = 1.765e-5 Pa s (Sutherland), nu = 1.69e-5 m^2/s.
Units: 1 m^2/s^3 = 10^4 cm^2/s^3, so eps = 1e-3, 1e-2, 1e-1 m^2/s^3 is 10, 100, 1000 cm^2/s^3.

## 0. Bottom line

1. Coalescence efficiency. For 8 um droplets on 40-60 um collectors, and for 50-60 um collector pairs, every energy-based formula gives E_coal = 1 to better than 0.1 percent (Weber number We = 1e-5 to 3e-4). But no source I opened measured coalescence for drops this small. Low and List measured only drops of 0.395 mm diameter and larger. The Straub fit rests on simulations with diameters 0.35 mm and larger. Beard and Ochs (1995) is the only formula built for this size range, and I could not open it (see 1.2).
2. Turbulence, 40 um with 8 um. The geometric kernel changes by only a few percent at eps <= 100 cm^2/s^3: +0.4 percent at 10, +5.6 percent at 100 (my evaluation of Ayala et al.'s weak-inertia formula, Rlambda = 2e4). At 400 it is about +28 percent. At 1000 the formula is outside its validity. The pure Saffman-Turner shear kernel is under 1 percent of the gravity kernel up to 1000 cm^2/s^3. Not covered: turbulent change of the collision efficiency (Wang et al.: "overall enhancement typically falls below 2" for size ratios 0.2-0.8).
3. Turbulence, two ~50 um collectors. Different regime. Equal drops have zero gravitational kernel, so any collision is turbulent. For 50/60 um the differential fall speed is only 0.09 m/s (0.167 m/s for 40/8). The enhancement can be large: Wang et al. find total enhancement x2 (eps = 100) and x7 (eps = 400) for 18/20 um. Grabowski and Wang say "up to a factor of 5" for pairs with low gravitational rate. No opened source gives a number for 50-60 um.
4. Not obtained: Beard and Ochs 1995 (formula, scatter), Wang et al. 2008 table, Ayala et al. Part 1 table, Grabowski and Wang 2013 body text (ε for stratocumulus). See section 5.

## 1. Reading ledger (what I really opened)

| # | Source | What I read | Link opened | Status |
|---|---|---|---|---|
| 1 | Beard and Ochs 1984, JGR 89(D5) 7165-7169 | Abstract and reference list only | https://agupubs.onlinelibrary.wiley.com/doi/10.1029/JD089iD05p07165 | Paywalled. No formulas. |
| 2 | Beard and Ochs 1995, JAS 52, 3977-3996 | Not opened. AMS returned HTTP 405 / 403 on every route. | (tried) https://journals.ametsoc.org/view/journals/atsc/52/22/1520-0469_1995_052_3977_cbspii_2_0_co_2.xml | **Secondary only:** Jacobson (2011), JAS 68, 334-346, https://journals.ametsoc.org/view/journals/atsc/68/2/2010jas3605.1.xml (opened, text read, equation images not extracted) |
| 3 | Low and List 1982a, JAS 39, 1591-1606 | AMS abstract page | https://journals.ametsoc.org/view/journals/atsc/39/7/1520-0469_1982_039_1591_ccabor_2_0_co_2.xml | Full text not opened. Formula from Jacobson (2011) in words and constants, and from PySDM code (below). |
| 4 | Straub et al. 2010, JAS 67(3), 576-588 | AMS page: abstract and the start of the introduction and section 2 | https://journals.ametsoc.org/view/journals/atsc/67/3/2009jas3175.1.xml | Body (definition range of We, scatter) was fetched but **not read**; see section 5. |
| 5 | Saffman and Turner 1956, JFM 1, 16-30 | Full text, Caltech author copy (scan, OCR). | https://authors.library.caltech.edu/91043/1/on_the_collision_of_drops_in_turbulent_clouds.pdf | Equations garbled in places. Marked OCR. |
| 6 | Ayala, Rosa, Wang 2008, NJP 10, 075016 (Part 2) | Full text including the corrigendum | https://iopscience.iop.org/article/10.1088/1367-2630/10/7/075016/pdf | Complete. |
| 7 | Wang, Ayala, Rosa, Grabowski 2008, NJP 10, 075013 | Abstract only | https://iopscience.iop.org/article/10.1088/1367-2630/10/7/075013 | Table not obtained. |
| 8 | Grabowski and Wang 2013, Annu. Rev. Fluid Mech. 45, 293-324 | Abstract only | https://www.annualreviews.org/doi/10.1146/annurev-fluid-011212-140750 | Body paywalled. Secondary: Grabowski's 2013 slides, https://hogback.atmos.colostate.edu/cmmap/research/docs/aug13/Grabowski.pdf |
| 9 | Xue, Wang, Grabowski 2008, JAS 65, 331-356 | Abstract, introduction, start of section 2 (cut off at 2d) | https://journals.ametsoc.org/view/journals/atsc/65/2/2007jas2406.1.xml | Partial. |
| x | Ayala et al. 2008 Part 1, NJP 10, 075015 | Abstract only | https://iopscience.iop.org/article/10.1088/1367-2630/10/7/075015/pdf | Tables not obtained. |
| x | Secondary for formulas | Jacobson 2011 (above); PySDM source (raw GitHub: straub2010.py, lowlist1982.py in PySDM/dynamics/collisions/coalescence_efficiencies); de Jong et al. 2023, GMD 16, 4193, https://gmd.copernicus.org/articles/16/4193/2023/gmd-16-4193-2023.html; List, Fung, Nissen 2009, JAS 66, 2190, https://journals.ametsoc.org/view/journals/atsc/66/8/2009jas2863.1.xml | Read. |

Tool notes: Firecrawl was out of credits. Bash was refused. AMS blocks PDF routes.
Local copies of fetched text (outside the repository, readable by Read):
- `/root/.claude/projects/-home-user-SiteTest/de75440b-f270-5344-8ae7-923c4f178e24/tool-results/toolu_0157hUuZngf6pRwtZHxAvD3W.json` (Ayala Part 2)
- `.../toolu_01UuctdTXD6W3oWUKLqpCZzr.json` (Straub 2010 page, 56 kB, unread)
- `.../toolu_016zTin5nY3HvuvFq96B2Gs3.json` (Xue 2008 page, Annual Reviews abstract)
- `.../toolu_01JKeBpRFDMmBXetdnv5j87b.json` (Jacobson 2011, List et al. 2009)
- `.../toolu_01QtUaRvByBZZPX6LwbBMAGZ.json` (de Jong et al. 2023)

## 2. Part A, coalescence efficiency

### 2.0 Shared definitions (energy form)

For a collision of a large drop (diameter d_L, fall speed V_L) and a small drop (d_S, V_S), sigma = surface tension (0.0728 N/m for water at 20 C, List et al. 2009):

| Symbol | Meaning | Expression | Where it comes from |
|---|---|---|---|
| CKE | collision kinetic energy | (pi/12) rho_w d_L^3 d_S^3 / (d_L^3 + d_S^3) (V_L - V_S)^2 = (1/2) m_red dV^2 | PySDM code (secondary); Jacobson describes it in words |
| S_t | surface energy of the two drops | pi sigma (d_L^2 + d_S^2) | PySDM; Jacobson |
| d_c | diameter of the merged sphere | (d_L^3 + d_S^3)^(1/3) | Straub intro: D_c = (d_L^3 + d_S^3)^(1/3) |
| S_c | surface energy of the merged sphere | pi sigma d_c^2 | PySDM; Jacobson |
| dS | surface energy released | S_t - S_c | Jacobson |
| E_T | total coalescence energy | CKE + dS | Jacobson |
| We | Weber number (Straub form) | CKE / S_c | PySDM code; Jacobson calls it "another form of the dimensionless Weber number" |

### 2.1 Beard and Ochs 1984 (JGR)

- Establishes (abstract only): coalescence efficiency for accretion was taken to be governed by a collisional Weber number. With theoretical collision efficiencies, this was used to organise collection-efficiency data from several sources into one set. The paper says: "assumed to be governed by a collisional Weber number".
- Numbers in the abstract: maximum collection efficiency 71 percent for a collector of 115 um and a cloud droplet of 12 um radius (the abstract does not say whether 115 um is radius or diameter). Time-averaged collection efficiency for growth from 50 to 500 um by accreting 30 um droplets is 50 percent lower than the time-averaged collision efficiency. Maximum 65 percent time-averaged collection efficiency for 10 um droplets. Droplets smaller than 5 um contribute negligibly.
- Does not establish for us: no formula, no scatter, no value for 8 um droplets with 40-60 um collectors was readable.

### 2.2 Beard and Ochs 1995 (JAS), only through Jacobson 2011

Not opened. What Jacobson reports about it (secondary, from the text; his equation images were not extracted):
- Efficiencies are given for two ranges of the small-drop diameter d_s: 14 to 200 um, and 200 to 800 um. For d_s < 14 um the efficiency converges to 1.
- 14-200 um: found by Newton-Raphson iteration with coefficients A0 = 5.07, A1 = -5.94, A2 = 7.27, A3 = -5.29. r_s and r_b are small and big radii in um. Four iterations from a first guess of 0.5 suffice.
- 200-800 um: a form in q = r_s/r_b and a Weber number built from rho_w, sigma and the fall speeds.
- Seifert et al. (2005) use BO95 for d_s < 0.3 mm, Low and List for d_s > 0.5 mm, and an interpolation between.
- Our 8 um radius droplet has d_s = 16 um. It lies in the 14-200 um branch, just above the point where E = 1 is stated. I cannot give its value.
- Stated scatter: unknown.

### 2.3 Low and List 1982a (JAS)

- Measured (abstract): 761 collision experiments out of 14,000 attempts, at terminal velocity and 100 kPa. Six size pairs (diameters in cm): [0.18; 0.0395], [0.40; 0.0395], [0.44; 0.0395], [0.18; 0.0715], [0.18; 0.10], [0.30; 0.10]. Over 100 repeats per pair. Consistent with McTaggart-Cowan and List (1975b).
- Result in the abstract: significant coalescence only when drops smaller than 0.06 cm diameter are struck by larger ones. The empirical equation uses collision kinetic energy and surface-tension energy.
- Formula (from Jacobson's words and constants, PySDM code consistent; algebra not read from the paper):
  E_coal = a (1 + d_S/d_L)^-2 exp( - b sigma E_T^2 / S_c ), a = 0.778, b = 2.61e6 m^2 J^-2, sigma in J/m^2. Taken as zero "otherwise" (Jacobson); the condition itself I did not see.
- Valid range used by others: d_S > 0.5 mm (Jacobson). Measured range in the abstract: d_S from 0.395 mm, d_L 1.0-4.4 mm.
- Scatter: not in the abstract. Not obtained.
- Warning: PySDM's `lowlist1982.py` multiplies a "water mass" term by rho_w/2 when forming CKE. If that attribute is a mass this looks dimensionally off. I used the physical definition in 2.0 instead.

### 2.4 Straub et al. 2010 (JAS 67, 576-588)

- Result (abstract): E_c = exp(-1.15 We). The paper says coalescence efficiencies "can be described best by means of the Weber number". It contrasts this with Low and List.
- Basis: numerical simulations (not laboratory) of 32 drop pairs, 6 eccentricities each. Small-drop diameters 0.035-0.18 cm, large-drop diameters 0.06-0.46 cm (introduction).
- We (as PySDM implements it): CKE / (pi sigma d_c^2), see 2.0. Not checked against the paper body.
- Behaviour reported by de Jong et al. 2023 using it: E_c approaches 1 for colliding drops smaller than 1 mm diameter, and goes to 0 for drops larger than 6 mm.
- Scatter: not obtained (body unread).
- Does not establish: anything for drops under 0.35 mm diameter. Our cloud pairs are 20 times below that.

### 2.5 E_coal for our pairs (scout calculation, not from a source)

Method: Straub's exp(-1.15 We) with the energies of 2.0. Fall speeds: Stokes with the nonlinear factor f = 1 + 0.15 Re^0.687 (Ayala eq. 91) at 850 hPa, 10 C for cloud-size drops: V(8) = 0.008, V(40) = 0.175, V(50) = 0.257, V(60) = 0.348 m/s. Millimetre-drop speeds are Gunn-Kinzer values quoted from memory (1.0 mm 4.03, 0.5 mm 2.06, 0.25 mm about 0.95 m/s), not read in this session. Sizes (a) and (b) are radii.

| Pair | d_L, d_S (um) | dV (m/s) | CKE (J) | S_c (J) | We | E_c, Straub form (extrapolated far below its fit range) |
|---|---|---|---|---|---|---|
| (a) 40 um + 8 um | 80, 16 | 0.167 | 3.0e-14 | 1.47e-9 | 2.0e-5 | 0.99998 |
| (a) 60 um + 8 um | 120, 16 | 0.340 | 1.2e-13 | 3.30e-9 | 3.8e-5 | 0.99996 |
| (b) 50 um + 60 um | 100, 120 | 0.091 | 1.4e-12 | 4.46e-9 | 3.1e-4 | 0.9996 |
| (b) 50 um + 50 um | 100, 100 | 0 by gravity (turbulent 0.05 m/s gives We about 1e-4) | 0 | 3.6e-9 | 0 | 1.000 |
| (c) 500 + 250 um taken as radii | 1000, 500 | 1.97 | 1.13e-7 | 2.47e-7 | 0.456 | 0.59 (Straub). Low and List form: 0.778/(1.5)^2 x exp(-0.018) = 0.34 |
| (c) 500 + 250 um taken as diameters | 500, 250 | 1.11 | 4.5e-9 | 6.2e-8 | 0.072 | 0.92 (Straub). Low and List not applicable (d_S < 0.5 mm) |

Caveats:
- The Weber-number forms know nothing about gas-film bounce of tiny drops. Case (a) and (b) rows say only: the collision energy is 4 to 5 orders below the surface energy.
- Case (c) is ambiguous (radius or diameter). Both are shown. The two formulas disagree by 0.25 at 1.0/0.5 mm, a size where both claim validity.
- BO95, the formula meant for (a) and (b), could not be evaluated.

## 3. Part B, turbulence and collisions

### 3.1 Saffman and Turner 1956 (JFM 1, 16-30), full text, OCR

- Establishes (paraphrased): drops much smaller than the smallest eddies feel only the local velocity gradient, so the collision rate depends on eps and nu alone. Collision rate for drops that follow the air: N = 2 pi R^2 n1 n2 <|w_r|>, with w_r = R |du/dx|, <(du/dx)^2> = eps/(15 nu), du/dx Gaussian, so <|du/dx|> = (2 eps/(15 pi nu))^(1/2).
- Result: K_ST = 1.30 (r1 + r2)^3 (eps/nu)^(1/2), stated for r1/r2 between 1 and 2. Check: (8 pi/15)^(1/2) = 1.294, so 1.30 is that constant. Their approximate combined formula (their eq. 10) gives a different constant, about 1.67 (OCR).
- Assumptions: collision efficiency = 1 (argued from Manley and Mason glass-sphere and bubble experiments, ratio of radii below 2). The paper says it takes "the collision efficiency of nearly equal droplets as unity". Also: R much smaller than the dissipation length, relaxation time much smaller than the Kolmogorov time, isotropic small scales, high Reynolds number, no gravity in the shear term.
- Weak points flagged by Ayala et al.: their cylindrical shear term differs from the spherical one by an isotropy error, and their combined formula does not reduce to the correct gravity-only limit.
- Their ε estimates: 5 cm^2/s^3 mean for the lowest few km (Brunt, quoted), stratiform clouds lower, about 1000 cm^2/s^3 for vigorous cumulus (from u = 2 m/s, scale 50 m gives 1600). Turbulent acceleration equals gravity at about 2100 cm^2/s^3. Conclusion: effects small in layer clouds, 1000 cm^2/s^3 would be less effective than gravity.
- Their time for mean mass +50 percent (1.5 g/m^3, equal drops, shear only): 11 h at 5 cm^2/s^3, 2.8e3 s at 1000 cm^2/s^3.
- Does not establish: unequal-size or sedimenting pairs (the combined formula is rough), preferential concentration, collision-efficiency changes.

**Shear kernel for our pairs** (K = 1.294 R^3 (eps/nu)^(1/2), R = a1 + a2, nu = 1.69e-5 m^2/s; scout calculation):

| Pair | R (um) | (eps/nu)^(1/2) = 7.70 / 24.3 / 77.0 s^-1 for eps = 1e-3 / 1e-2 / 1e-1 | K at 1e-3 | K at 1e-2 | K at 1e-1 | Gravity kernel pi R^2 dV (E_coll = 1) | K_ST / gravity at 1e-3 / 1e-2 / 1e-1 |
|---|---|---|---|---|---|---|---|
| 40 + 8 um | 48 | | 1.10e-6 cm^3/s | 3.48e-6 | 1.10e-5 | 1.21e-3 cm^3/s | 0.09 / 0.29 / 0.91 percent |
| 50 + 50 um | 100 | | 9.96e-6 | 3.15e-5 | 9.96e-5 | 0 | not defined |
| 50 + 60 um | 110 | | 1.33e-5 | 4.19e-5 | 1.33e-4 | 3.46e-3 | 0.38 / 1.2 / 3.8 percent (larger by 1/E_coll once the real collision efficiency is used) |

### 3.2 Ayala, Rosa, Wang 2008, Part 2 (NJP 10, 075016), full text

Establishes: the geometric collision kernel of sedimenting droplets in turbulence is the product of two statistics: the mean radial relative velocity at contact and the radial distribution function (RDF) g12.
Quote: "turbulence could triple the geometric collision kernel" (10/20 um pair, Rlambda = 2e4, eps = 600 cm^2/s^3).

Equations we may use (symbols: R = a1 + a2; tau_p response time; v_p terminal velocity; v_k, tau_k, eta Kolmogorov scales; nu air viscosity; eps dissipation rate; Rlambda Taylor-microscale Reynolds number; the text extraction dropped every eps symbol, restored here):

1. Kernel: Gamma12 = 2 pi R^2 <|w_r|> g12. Gravity only: <|w_r|>^g = (1/2)|v_p2 - v_p1|, g12 = 1, Gamma^g = pi R^2 |v_p2 - v_p1|. Enhancement: Gamma12/Gamma^g = (<|w_r|>/<|w_r|>^g) x g12.
2. Radial relative velocity (recommended form per the corrigendum, error under 2.5 percent against the exact form): <|w_r|> = (2/pi)^(1/2) [ sigma^2 + (pi/8)(tau_p1 - tau_p2)^2 g^2 ]^(1/2), where sigma^2 is the variance of the turbulent part of the radial relative velocity.
3. Weak-inertia limit of sigma^2 (their eq. 81; eps restored from the statement under eq. 83 that the coupling ratio is independent of eps): sigma^2 = (1/15) R^2 eps/nu + (tau_p1 - tau_p2)^2 <(Du/Dt)^2> + (v_p1 tau_p1 - v_p2 tau_p2)^2 (2 eps/(15 nu)). The three terms are shear, fluid acceleration, and a new gravity-shear coupling.
4. Acceleration variance: <(Du/Dt)^2> = a0 (v_k/tau_k)^2, a0 = (11 + 7 Rlambda)/(205 + Rlambda) (Zaichik et al.), about 7 at cloud Reynolds numbers.
5. Derived scales: tau_k = (nu/eps)^(1/2), eta = (nu^3/eps)^(1/4), v_k = (nu eps)^(1/4), u' = Rlambda^(1/2) v_k / 15^(1/4).
6. RDF at contact: g12 = [(eta^2 + r_c^2)/(R^2 + r_c^2)]^(C1/2), C1 = y(St) / [ (g/(v_k/tau_k)) 0.1886 exp(20.306/Rlambda) ], y(St) = -0.1988 St^4 + 1.5275 St^3 - 4.2942 St^2 + 5.3406 St, St = max(St1, St2); (r_c/eta)^2 = |St2 - St1| 20.115 (a_og/Rlambda)^(1/2), a_og = a0 + (pi/8)(g/(v_k/tau_k))^2. Set y = 0 if it turns negative at large St.
7. Nonlinear drag for radius above 30 um: tau_p = 2 rho_w a^2 / (9 rho nu f(Re_p)), f = 1 + 0.15 Re_p^0.687, v_p = tau_p g.
8. Corrigendum: in the long equation (76) the term (v_p1 - v_p2/phi) must read (v_p1 - v_p2)/phi.

Conditions of validity (from the paper): droplet radius a much smaller than eta; rho_w much greater than rho; sedimentation parameter v_p/v_k above 1. Theory built for sedimentation dominating the relative motion, so it is weakest for near-equal sizes.

Stated scatter against DNS: <|w_r|> within 5 percent for bidisperse cases; 48 percent error for monodisperse pairs at 400 cm^2/s^3; the integrated kernel is underpredicted by up to 30 percent at high St and high eps (400 cm^2/s^3).

Numbers reported:
- Clustering (RDF) matters only for a1/a2 below 1.2. For ratios above 1.3, g12 is close to 1, even at eps = 400 cm^2/s^3 and Rlambda = 72.
- For 10/20 um at Rlambda about 1e4 and eps above 300 cm^2/s^3: kernel is 2 to 3 times the gravity kernel. Rlambda matters as much as eps for this pair.
- For 20 um self-collisions: kernel at eps = 600 cm^2/s^3 is about 9 times that at 100 cm^2/s^3.
- Typical cumulus dissipation 100-650 cm^2/s^3 (cites Rogers and Yau 1989; Pruppacher and Klett 1997). Cloud Rlambda about 1e4 to 2e4 (text uses 10,000 and 20,000). DNS Rlambda 43-72.
- For the 10-20 um pair at eps = 100 and Rlambda = 2e4, the acceleration term is 1.9e3 times the shear term and the coupling term is 140 times the shear term (950 times for 20-30 um). So Saffman-Turner shear alone is a poor guide for sedimenting pairs.

Does not establish: any value for 40/8 or 50-60 um pairs (no table); collision-efficiency changes (that is Wang et al.); a table of "enhancement for 10-60 um at eps = 100 and 400". That table is in Part 1, which I could only read as an abstract: the DNS covers eps 10-400 cm^2/s^3 and radii 10-60 um, and finds the geometric kernel up to 47 percent above the sedimentation-only kernel, with the enhancement rising with eps and Rlambda.

**Scout evaluation of the weak-inertia formula for 40 um + 8 um** (hand calculation, eq. 2-4 above, g12 = 1 because the size ratio is 5; Rlambda = 2e4, a0 = 6.9; the answer barely depends on Rlambda because a0 saturates at 7):
tau_p(40) = 0.0178 s, tau_p(8) = 8.2e-4 s, v_p1 tau_p1 - v_p2 tau_p2 = 3.12e-3 m, gravity-only <|w_r|> = 0.0835 m/s.

| eps (m^2/s^3) | eps (cm^2/s^3) | tau_k (s) | St of the 40 um drop | shear term in sigma^2 (m^2/s^2) | acceleration term | coupling term | <|w_r|> / <|w_r|>^g (kernel change) |
|---|---|---|---|---|---|---|---|
| 1e-3 | 10 | 0.130 | 0.14 | 9e-9 | 1.5e-5 | 7.7e-5 | 1.004 (+0.4 %) |
| 1e-2 | 100 | 0.041 | 0.43 | 9e-8 | 4.9e-4 | 7.7e-4 | 1.056 (+5.6 %) |
| 4e-2 | 400 | 0.021 | 0.87 | 4e-7 | 3.9e-3 | 3.1e-3 | 1.28 (+28 %) |
| 1e-1 | 1000 | 0.013 | 1.4 | 9e-7 | 1.5e-2 | 7.7e-3 | 1.76 (+76 %, outside validity, St > 1) |

The expansion is for small St. Rows with St above about 0.4 are less reliable. Rlambda and the collision efficiency are not part of this table.

### 3.3 Wang, Ayala, Rosa, Grabowski 2008 (NJP 10, 075013), abstract only

What the abstract says (hybrid DNS including aerodynamic interactions): turbulence raises the collision efficiency. For 18 and 20 um radius droplets: x4 at eps = 400 cm^2/s^3 and x1.6 at 100. Total enhancement (geometric times efficiency) for this pair: x7 at 400 and x2 at 100. For intermediate size ratios (0.2 < a2/a1 < 0.8) the overall enhancement "typically falls below 2". The enhancement peaks at a2/a1 -> 1 and at a2/a1 -> 0. Self-collision efficiency can exceed 1 in a bidisperse suspension, depending on volume concentration.
Table of enhancement factors: **not obtained**. Our 40/8 ratio (0.2) sits at the edge of "intermediate". The 50/60 ratio (0.83) sits in the near-equal branch; the 50/50 case is the limit a2/a1 = 1.
Conditions: DNS Rlambda is of order 50-70, not 1e4.

### 3.4 Grabowski and Wang 2013 (Annu. Rev. Fluid Mech. 45, 293-324), abstract plus slides

- Abstract: small-scale turbulence in cumulus makes a significant contribution to collision-coalescence, "enhancing the collection kernel up to a factor of 5", especially for droplet pairs with a low gravitational collision rate. That "moderate level of enhancement" has a significant impact on warm-rain initiation.
- Slides (secondary, Grabowski 2013, from a talk citing the review): cloud turbulence has Rlambda about 1e4 and outer scale about 100 m; a plot of the enhancement factor "including turbulent collision efficiency" at eps = 100 and 400 cm^2/s^3 (figure only, no numbers in the text); LES of BOMEX shallow cumulus with eps above 1 cm^2/s^3 in cloudy points; rain accumulation about 10 times larger with the turbulent kernel for one aerosol case (60 mg^-1).
- Typical ε for stratocumulus or cumulus with sources: **not obtained** from the review. The values I could cite come from Ayala (cumulus 100-650 cm^2/s^3), Saffman-Turner (5 cm^2/s^3 mean low atmosphere; 1000 for vigorous cumulus) and Xue (300 cm^2/s^3 with u' = 2.02 m/s; observed rms u' range 0.5-2.5 m/s).

### 3.5 Xue, Wang, Grabowski 2008 (JAS 65, 331-356), partly read

- Method: kinetic collection equation, bin integral method, with the Hall gravitational kernel as base case and four turbulent kernels, the Ayala kernel being the most realistic. Typical case: eps = 300 cm^2/s^3, u' = 202 cm/s.
- Result: "shorten the time for the formation of drizzle drops by about 40%" relative to the base case (both radar-reflectivity and mass-weighted-size measures). Moderate kernel enhancement still has a large effect on the autoconversion phase.
- From the introduction: gravity controls collisions above 50 um radius, turbulence can enhance the 10-30 um and 30-100 um ranges; the gravity-only 20 to 100 um growth needs about an hour, a factor 2 or more slower than observed rain onset in tropical cumulus (15-20 min).
- Does not establish: stratocumulus; the numbers for eps = 10 or 1000 cm^2/s^3; the section-2d comparison of kernels was cut off.

### 3.6 Taylor-microscale Reynolds number for our ε values

Relation (scout-derived from lambda^2 = 15 nu u'^2/eps and Rlambda = u' lambda/nu): Rlambda = u'^2 (15/(eps nu))^(1/2). It reproduces Xue's pair (eps = 300 cm^2/s^3, u' = 2.02 m/s gives about 2.2e4). With the outer-scale guess u' about (eps L)^(1/3), L = 100 m (the scale on Grabowski's slide):

| eps (m^2/s^3) | (15/(eps nu))^(1/2) (s/m^2... in SI) | u' = 1 m/s | u' = 2 m/s | u' = (eps x 100 m)^(1/3) | Rlambda for that u' |
|---|---|---|---|---|---|
| 1e-3 | 2.98e4 | 3.0e4 | 1.2e5 | 0.46 m/s | 6e3 |
| 1e-2 | 9.4e3 | 9.4e3 | 3.8e4 | 1.0 m/s | 9e3 |
| 1e-1 | 3.0e3 | 3.0e3 | 1.2e4 | 2.2 m/s | 1.4e4 |

DNS in the sources uses Rlambda = 43, 54, 72 (and 45-75 in earlier work), 100 times lower than cloud values. Every DNS enhancement number is therefore a lower-Rlambda number; Ayala's model suggests the Rlambda effect on the 10/20 um pair is as strong as the eps effect (not tested for the 40/8 pair).

## 4. Answers to the two questions as posed

- Coalescence: given a collision, assume E_coal = 1 for 8 um droplets on 40-60 um collectors, and for 50-60 um pairs, but say this is an extrapolation of energy-based forms, and that Beard and Ochs 1995 is the right reference to check it. At 500/250 um, E_coal drops to 0.3-0.9 depending on the interpretation of the sizes and the formula chosen.
- Turbulence: 40 um with 8 um, a few percent at eps = 100 cm^2/s^3 (geometric part), 28 percent at 400. Two ~50 um collectors: not a few percent. The question is ill-posed for equal sizes (zero gravitational kernel), and for 50/60 um the differential sedimentation is half that of the 40/8 pair, so the published enhancements for near-equal pairs (x2 at 100, x7 at 400 for 18/20 um; up to x5 in the review) are the relevant order of magnitude. No opened source gives the number for 50-60 um.

## 5. Open questions

1. Beard and Ochs 1995: the exact formulas, the Weber number definition, the stated scatter and measured range. Needs a PDF from a library.
2. Low and List 1982a: the exact printed formula, the condition that sets E = 0, and the scatter of the data. The version here is Jacobson's constants plus PySDM's code.
3. Straub 2010: the definition range of We, the figure of E_c against We, and any scatter statement. The page body is saved at `.../toolu_01UuctdTXD6W3oWUKLqpCZzr.json` and was not read (call budget).
4. Is there any measurement of coalescence efficiency for cloud droplets (8 um radius) with 40-60 um collectors, including bounce? Not in any source I opened.
5. Wang et al. 2008 table of collision-efficiency enhancement, and Ayala et al. Part 1 table of geometric enhancement. Needed to replace my formula-based +5.6 percent with a DNS number and to add the collision-efficiency enhancement for 40/8 and 50/60 um.
6. Hydrodynamic collision efficiency (Hall, or Beard-Grover) for 40/8 and 50/60 um in still air. Needed to convert the turbulent gain into a ratio to the real gravitational rate.
7. Typical eps and Rlambda for stratocumulus and cumulus from Grabowski and Wang 2013 (with sources). Not obtained.
8. Case (c): are 500 and 250 um radii or diameters? Also whether the study wants fall speeds at 850 hPa, which are a few percent higher than the sea-level Gunn-Kinzer values I used.
9. The PySDM Low-List CKE line (rho_w/2 times a water-mass term) looks dimensionally off; the formula should be read from the original paper before anyone codes it.

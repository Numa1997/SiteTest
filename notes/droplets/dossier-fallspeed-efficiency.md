# Dossier: fall speed and collision efficiency of water drops in air

Study: Droplet Collection (cloud droplets of about 8 um radius growing to rain by gravitational collection).
Written 2026-10-23 by a scout. No code was written. All numbers below were read in this session unless a line says otherwise.

How the sources were read. The AMS journal site blocks plain downloads (HTTP 403), but its PDF links for Gunn and Kinzer (1949),
Beard (1976), Langmuir (1948) and Hall (1980) were fetched through the Firecrawl PDF reader and read whole as machine-extracted text.
Scanned tables can carry misread digits. Every table below that was typed from such text is marked "OCR". Before any number goes into code,
check it against the page image. Pinsky et al. (2001) could not be fetched as a PDF (404); only parts of its full text came back through a search tool.

---------------------------------------------------------------------

## 0. Answer in brief

1. Fall speed. Use Beard (1976), regimes 1 and 2, for drops of equivalent diameter 0.5 um to 1.07 mm (radius 0.25 um to 0.535 mm).
   An 8 um radius droplet is 16 um in diameter, so it sits in regime 1 (Stokes law with slip correction). Collectors up to 300 um radius
   (0.6 mm diameter) sit in regime 2. For drops of 1.07 to 7 mm use regime 3, or the measured Gunn and Kinzer table.
2. Stated accuracy. Beard gives it as agreement with the formulas he fitted, not as an experiment: regime 2 has rms 0.09 % and maximum 0.6 %
   against the rigid-sphere drag formulas it was fitted to (20 um to 1 mm); regime 3 is within +-0.5 % of Gunn and Kinzer at sea level.
   Beard says the Gunn and Kinzer data are inaccurate for d below about 0.4 mm. Gunn and Kinzer state better than 0.7 % only for masses of
   10 to 100 000 micrograms (d about 0.27 to 5.8 mm).
3. Drag-law alternative. Schiller and Naumann (1933) was not opened in this session. See the unverified entry in section 3.
4. Collision efficiency. Hall (1980) Table 1 is the compiled table (section 6). It states no accuracy. Pinsky et al. (2001) use a single
   method over a wide range and add the dependence on pressure; their efficiency tables were not obtained. Langmuir (1948) is an analytic
   model for point droplets, good for the physics story, not for numbers near equal sizes.
5. Critical Stokes number, radius-based, point particle on a sphere: 1/12 = 0.0833 in potential flow (Langmuir and Blodgett 1946,
   restated by Langmuir 1948); 1.214 in Stokes flow (Langmuir 1948), refined to 1.21194 by Michael and Norey (1970, Canadian Journal of
   Physics), a value they warn is an approach criterion, not a true contact criterion. The diameter-based form is half: 1/24 and about 0.606.

---------------------------------------------------------------------

## 1. Gunn and Kinzer (1949)

Reference. Gunn, R. and Kinzer, G. D., 1949: The terminal velocity of fall for water droplets in stagnant air. J. Meteorol. 6(4), 243-248.
DOI 10.1175/1520-0469(1949)006<0243:TTVOFF>2.0.CO;2
Opened: https://journals.ametsoc.org/downloadpdf/journals/atsc/6/4/1520-0469_1949_006_0243_ttvoff_2_0_co_2.pdf (full text, OCR of a 6-page scan).
Abstract page: https://journals.ametsoc.org/view/journals/atsc/6/4/1520-0469_1949_006_0243_ttvoff_2_0_co_2.xml

What it establishes (paraphrase).
- More than 1500 distilled-water droplets, mass 0.2 to 100 000 micrograms, were timed between two induction rings about 1 m apart.
  Each drop carried a small charge; the charge was tested and did not change the speed.
- The drops fell about 12 m to reach terminal speed and a further 8 m before the timing section.
- Conditions of the tabulated values: pressure 760 mm Hg, temperature 20 C, relative humidity 50 %.
- The measurements were taken over days of changing pressure and temperature, so a density correction was applied. They say that with no
  correction the error would not exceed 1.5 %. Entrainment of air by many falling drops raised the measured speed by a few percent, so
  single-drop conditions were kept.
- Mass was found by weighing (drops above 5 mg) or from the diameter of the drop in an oil dish (diameter accurate to 2 % at 10 micrograms,
  0.5 % at 10 000 micrograms). Mass scatter of the dropper was 12 % for the smallest drops, about 2 % at 10 000 micrograms.
- Stated accuracy. Direct quote: "The over-all accuracy of the mass-terminal-velocity measurements is better than 0.7 per cent."
  In the body this statistical figure is claimed for masses 10 to 100 000 micrograms (diameter 0.267 mm to 5.76 mm), each point from at least
  50 events. For masses below 10 micrograms they did no statistical analysis; those points (Fig. 3) only approach Stokes law below about
  0.4 microgram. Above 100 000 micrograms (d 0.58 cm) drops are mechanically unstable.
- Equivalent diameter is the diameter of a sphere of the same mass, using density 1 g/cm3 (checked: 0.1 cm gives 524 micrograms).

Table 2 of the paper (OCR; diameters converted from cm to mm). Reynolds number is rho_air d V / eta; C_D is the drag coefficient the authors computed.

| d (mm) | V (cm/s) | mass (ug) | Re | C_D |
|---|---|---|---|---|
| 0.1 | 27 (footnote: Stokes law below 0.08 mm) | 0.524 | 1.80 | 15.0 |
| 0.2 | 72 | 4.19 | 9.61 | 4.2 |
| 0.3 | 117 | 14.14 | 23.4 | 2.4 |
| 0.4 | 162 | 33.5 | 43.2 | 1.66 |
| 0.5 | 206 | 65.5 | 68.7 | 1.28 |
| 0.6 | 247 | 113.1 | 98.9 (OCR; Kajikawa 1974 prints 98.7) | 1.07 |
| 0.7 | 287 | 179.6 | 134 | 0.926 |
| 0.8 | 327 | 268 | 175 | 0.815 |
| 0.9 | 367 | 382 | 220 | 0.729 |
| 1.0 | 403 | 524 | 269 | 0.671 |
| 1.2 | 464 | 905 | 372 | 0.607 |
| 1.4 | 517 | 1437 | 483 | 0.570 |
| 1.6 | 565 | 2140 | 603 | 0.545 |
| 1.8 | 609 | 3050 | 731 | 0.528 |
| 2.0 | 649 | 4190 | 866 | 0.517 |
| 2.2 | 690 | 5580 | 1013 | 0.504 |
| 2.4 | 727 | 7240 | 1164 | 0.495 |
| 2.6 | 757 | 9200 | 1313 | 0.494 |
| 2.8 | 782 | 11490 | 1461 | 0.498 |
| 3.0 | 806 | 14140 | 1613 | 0.503 |
| 3.2 | 826 | 17160 | 1764 | 0.511 |
| 3.4 | 844 | 20600 | 1915 | 0.520 |
| 3.6 | 860 | 24400 | 2066 | 0.529 |
| 3.8 | 872 | 28700 | 2211 | 0.544 |
| 4.0 | 883 | 33500 | 2357 | 0.559 |
| 4.2 | 892 | 38800 | 2500 | 0.575 |
| 4.4 | 898 | 44600 | 2636 | 0.594 |
| 4.6 | 903 | 51000 | 2772 | 0.615 |
| 4.8 | 907 | 57900 | 2905 | 0.635 |
| 5.0 | 909 | 65500 | 3033 | 0.660 |
| 5.2 | 912 | 73600 | 3164 | 0.681 |
| 5.4 | 914 | 82400 | 3293 | 0.700 |
| 5.6 | 916 | 92000 | 3423 | 0.727 |
| 5.8 | 917 | 102200 | 3549 | 0.751 |

Cross-check of the velocity column against a second source: Kajikawa (1974, Tenki 21(7), https://www.metsoc.jp/tenki/pdf/1974/1974_07_0317.pdf,
seen only as a search excerpt) reprints the same velocities from 0.2 mm to 5.8 mm. Every row I compared agrees. The same excerpt gives
25.6 cm/s at d = 0.10 mm, taken from Beard and Pruppacher (1969), against 27 cm/s from Gunn and Kinzer: a gap of about 5 %.

The paper also prints Table 1 (mass against speed in m/s, 20 samples from 0.25 to 100 000 micrograms) and Fig. 2/3. Three rows of Table 1
as a spot check (OCR): 1 ug, d 0.1241 mm... see the paper; 1000 ug, d 1.241 mm, 4.76 m/s; 10 000 ug, d 2.67 mm, 7.65 m/s. (The diameter column of
Table 1 is in cm in the paper: 0.1241 cm, 0.267 cm.)

What it does not establish.
- Nothing for droplets below about 0.1 mm diameter; the 8 um radius droplets of the study are out of range. At 0.1 mm Beard calls
  these data wrong (evaporation of the smallest drops); at diameters below about 0.4 mm he calls them inaccurate (see section 2).
- No pressure or temperature dependence (single condition).
- Isolated drops in still air, distilled water. Nothing on turbulence, charge fields or neighbours.

---------------------------------------------------------------------

## 2. Beard (1976)

Reference. Beard, K. V., 1976: Terminal velocity and shape of cloud and precipitation drops aloft. J. Atmos. Sci. 33(5), 851-864.
DOI 10.1175/1520-0469(1976)033<0851:TVASOC>2.0.CO;2
Opened: https://journals.ametsoc.org/downloadpdf/journals/atsc/33/5/1520-0469_1976_033_0851_tvasoc_2_0_co_2.pdf (full text, 14 pages, OCR).

What it establishes (paraphrase).
- Three flow regimes, each with its own formula, built so that they join smoothly at the crossover sizes (checked at 500 mb and -10 C).
- Regime 1, slip flow about a rigid sphere, Stokes drag with a Knudsen-number correction.
- Regime 2, continuum flow past a rigid sphere with a steady wake: Reynolds number as a polynomial in the Davies number.
- Regime 3, continuum flow around a non-circulating drop of equilibrium (flattened) shape: Reynolds number as a polynomial in the Bond number
  times a physical property number. Based on the wind-tunnel scaling of Garner and Lihou (1965) for the dependence on fluid properties
  and on Gunn and Kinzer at sea level for the numbers.

### 2.1 Regimes, equations, limits (Table 1 of the paper)

Symbols (paper's appendix): d0 equivalent spherical diameter; eta air viscosity; rho air density; Delta rho = rho_water - rho_air; sigma surface
tension; g = 9.8 m/s2 as printed; N_Re = rho V d0 / eta.

| regime | diameter | Reynolds number | velocity |
|---|---|---|---|
| 1 slip flow | 0.5 um to 19 um | about 1e-6 to 0.01 | V = C1 Csc d0^2, with C1 = Delta rho g / (18 eta) |
| 2 rigid sphere | 19 um to 1.07 mm | about 0.01 to 300 | V = eta N_Re / (rho d0), N_Re = Csc exp(Y), Y = b0 + b1 X + ... + b6 X^6, X = ln N_Da, N_Da = C2 d0^3, C2 = 4 rho Delta rho g / (3 eta^2) |
| 3 deformed drop | 1.07 mm to 7 mm | about 300 to 4000 | V = eta N_Re / (rho d0), N_Re = N_P^(1/6) exp(Y), Y = b0 + ... + b5 X^5, X = ln(Bo N_P^(1/6)), Bo = C3 d0^2, C3 = 4 Delta rho g / (3 sigma), N_P = sigma^3 rho^2 / (eta^4 Delta rho g) |

Note: Beard reuses the letters b0.. in regime 3; the c0..c5 of the request are his b0..b5 of regime 3. Beard's Bond number is the "modified"
one, Bo = (4/3) N_Bo with N_Bo = Delta rho g d0^2 / sigma. The Davies number is C_D N_Re^2 = N_Da (named by Beard after Davies 1945).
Crossover at 1.07 mm was chosen so the two formulas agree at three air states (20 C and 1.20 kg/m3; 20 C and 0.60 kg/m3; -10 C and 0.66 kg/m3);
crossover sizes came out within 1.07 +- 0.01 mm.

### 2.2 Slip correction (regime 1, and regime 2 up to about 30 um)

- General form (Davies 1945 constants): Csc = 1 + (2 l / d0) [1.257 + 0.400 exp(-1.10 d0 / (2 l))], with Csc = D_Stokes / D.
- For 0.5 um <= d0 <= 20 um the exponential term is below about 0.002 and Beard uses the first-order form Csc = 1 + 2.51 l / d0
  (the Stokes-Cunningham factor). 2.51 = 2 x 1.257.
- Mean free path: l = l0 (eta/eta0) (p0/p) (T/T0)^(1/2), with l0 = 6.62e-6 cm, eta0 = 1.818e-4 g cm-1 s-1, p0 = 1013.25 mb, T0 = 293.15 K.
  (In the extracted text one display line reads 10^-8 cm; the running text and Table 1 give 10^-6 cm. 6.62e-6 cm is the same as 6.62e-8 m.)
  Beard says Davies' own pressure formula for l is wrong by a factor of about 2^(3/4) and must not be paired with the Davies slip constants.
- Size of the correction: Csc = 1.01 at d0 = 20 um and 1.17 at d0 = 1 um. In regime 2 the factor Csc stays in N_Re = Csc exp(Y), but dropping
  it above about 30 um costs less than 0.5 % in V.

### 2.3 Coefficients (Table 1 of the paper, OCR, and independent cross-check)

Regime 2, Y = sum b_k X^k, k = 0..6, X = ln N_Da.

| k | Beard 1976, printed (OCR) | disdrodb / AMT 2026 table (excerpt) | St Andrews thesis (excerpt) | CARMApy (excerpt) | digit by digit |
|---|---|---|---|---|---|
| 0 | -0.318657E+1 | -3.18657 | -3.18657 | -3.18657 | identical (6 digits) |
| 1 | +0.992696 | 0.992696 | 0.992696 | +0.992696 | identical |
| 2 | -0.153193E-2 | -0.00153193 | -1.53193e-3 | -1.53193e-3 | identical |
| 3 | -0.987059E-3 | -0.000987059 | not in excerpt | -9.87059e-4 | identical |
| 4 | -0.578878E-3 | -0.000578878 | not in excerpt | -5.78878e-4 | identical |
| 5 | +0.855176E-4 | 0.0000855176 | not in excerpt | +8.55176e-5 | identical |
| 6 | -0.327815E-5 | not in excerpt | not in excerpt | cut off ("B6.") | NOT cross-checked |

Regime 3, Y = sum b_k X^k, k = 0..5, X = ln(Bo N_P^(1/6)).

| k | Beard 1976, printed (OCR) | disdrodb / AMT 2026 table (excerpt) | St Andrews thesis (excerpt) | digit by digit |
|---|---|---|---|---|
| 0 | -0.500015E+1 | -5.00015 | -5.00015 | identical |
| 1 | +0.523778E+1 | 5.23778 | 5.23778 | identical |
| 2 | -0.204914E+1 | -2.04914 | -2.04914 | identical |
| 3 | +0.475294 | 0.475294 | not in excerpt | identical |
| 4 | -0.542819E-1 | -0.0542819 | not in excerpt | identical |
| 5 | +0.238449E-2 | 0.00238449 | not in excerpt | identical |

Honest limits of this cross-check.
- The Beard coefficients I could read digit by digit (all of regime 3 and b0 to b5 of regime 2) match in every digit. b6 of regime 2
  (-3.27815e-6) is confirmed only against my own recollection and the single OCR reading; the excerpts I saw were cut before it.
- The OCR of Beard's Table 1 is damaged in places (one block shows b1 as "0.992090", another as "0.992696"; b4 appears once as
  "-0.5788785-3"). The cross-check settles these: b1 = 0.992696, b4 = -0.578878E-3.
- The other implementations are transcriptions of the same paper, so they test the digits, not the physics.
- The excerpts were search-engine snippets from: https://github.com/ltelab/disdrodb/blob/main/disdrodb/fall_velocity/rain.py,
  https://amt.copernicus.org/articles/19/4943/2026/amt-19-4943-2026.pdf, https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/6971/PeterSpeirsPhDThesis.pdf,
  https://arxiv.org/pdf/2606.30438 . None of them was opened whole. Pruppacher and Klett (1997) chapter 10 was not opened.

### 2.4 Accuracy Beard states

| regime | statement in the paper |
|---|---|
| 1 | No numerical accuracy given. It says the Stokes velocity of a 1 um droplet is wrong by as much as 17 % without slip, and that use of older mean-free-path formulas makes no significant difference for cloud droplets. The mean free path formula is argued from kinetic theory, not fitted. |
| 2 | Table 3: compared with the three rigid-sphere drag formulas it is fitted to (Table 2 of the paper: LeClair et al. 1970 for 0.01 <= Re <= 20, Beard and Pruppacher 1969 for 20 <= Re <= 258, Perry 1950 for 258 <= Re <= 5000), rms deviation 0.09 %, maximum 0.6 %, 25 points between 20 um and 1 mm, 20 C, 1 atm, 50 % RH. |
| 3 | The formula agrees within +-0.5 % of the Gunn and Kinzer velocities at sea level (the data it was fitted to). Pressure dependence rests on the Garner and Lihou scaling; Beard states there are no measurements of drops falling at reduced air density to test it. A fixed effect of turbulence is unknown: still-air values may be within a few percent of real rain (from the field data of Laws 1941). |

Table 3 also shows how other schemes behave against the same basic formulas (20 um to 1 mm). Gunn and Kinzer's measured data: rms 3.3 %, maximum 8.0 %
(0.1 to 1 mm, 10 points). Berry and Pranger (1974): 1.1 % and 3.2 %. Foote and du Toit (1969): 3.5 % and 13.7 %. Davies (1945): 2.4 % and 7.5 %.
Beard blames the Gunn and Kinzer scatter below about 0.4 mm (Re below about 40) on those data, not on his formula.

What it does not establish.
- No new measurement. Regimes 1 and 2 are fits to theory and to other authors' drag data. The "accuracy" is the closeness of the fit.
- Regime 1 is not tested against any droplet fall data in the paper.
- No data on the temperature and pressure variation of the viscosity, surface tension and density of water and air used in his scheme were
  extracted here; they are needed to run the formulas away from 20 C and 1 atm. Beard (1977, J. Atmos. Sci. 34, 1293-1298, "Terminal velocity adjustment
  for cloud and precipitation drops aloft") follows this paper and was not opened. Hall (1980) uses it for sea-level conditions.
- Beard's Fig. 7 table of velocities at five pressure levels came out of the OCR with numbers that do not match the Gunn and Kinzer sea-level
  table (for example 3.7 m/s at 1 mm, against 4.03 m/s measured); treat that extraction as unreliable and do not use it.

---------------------------------------------------------------------

## 3. A standard drag law for rigid spheres (alternative)

Schiller, L. and Naumann, A., 1933, Z. Ver. Dtsch. Ing. 77, 318; as given in Clift, R., Grace, J. R. and Weber, M. E., 1978, Bubbles, Drops and Particles,
Academic Press. NOT OPENED in this session. Entries below are from memory and must be checked before use.

- Form: C_D = (24 / Re) (1 + 0.15 Re^0.687). Quoted range Re below about 800, accuracy about 5 % (recollection of Clift et al.; unverified).
- It describes a rigid sphere, so it has no slip term and no drop deformation. It is meant for d below about 1 mm.

What I could check from the papers I did open. Langmuir (1948) Table 2 lists his rigid-sphere values C_D Re/24 against Re (from the data available in 1948).
Setting the Schiller and Naumann factor (1 + 0.15 Re^0.687) beside them, my own arithmetic gives: Re = 1: 1.150 against Langmuir 1.176 (-2.2 %);
Re = 10: 1.730 against 1.78 (-2.8 %); Re = 100: 4.55 against 4.59 (-0.9 %); Re = 300: 8.55 against 8.26 (+3.5 %); Re = 1000: 18.28 against 18.62 (-1.8 %).
So the two agree to a few percent, which is the level of the scatter that Beard (1976) finds among drag formulas of that time. Beard's own Table 2 is a
three-piece fit and Beard shows it matches Gunn and Kinzer well from Re about 100 to 400.

Not established: the stated accuracy and range of Schiller and Naumann from the primary text.

---------------------------------------------------------------------

## 4. Critical Stokes number for impaction on a sphere

Definitions found.
- Langmuir (1948) defines K = lambda_s / S, where lambda_s is the "range" of the droplet: the distance a droplet of radius r, thrown at speed U into still
  air, would travel if Stokes drag held at all speeds. Per his Table 4 footnote, K = 1297 r^2 U / S in cgs units, which equals (2/9) rho_water r^2 U / (eta S)
  with eta about 1.71e-4 poise. (Equation (8) as extracted reads "2/3"; the Table 4 footnote and the stopping-distance formula both give 2/9, so I read the "2/3" as an extraction slip.)
  So K is a Stokes number based on the collector RADIUS S: K = U tau_p / S with tau_p = (2/9) rho_water r^2 / eta.
- Diameter-based form (collector diameter 2S): St = K / 2.

Values and who gave them.

| flow | critical value, radius-based | diameter-based | source read |
|---|---|---|---|
| potential flow, sphere | K = 1/12 = 0.0833 (Langmuir's Table 1: E_A = 0 at K = 0.0833) | 1/24 | Langmuir 1948 (opened); the underlying 1945/1946 report by Langmuir and Blodgett (Army Air Forces Tech. Rep. 5418, not opened) |
| potential flow, cylinder | K = 1/8 | 1/16 | Langmuir 1948 (opened) |
| Stokes (creeping) flow, sphere | K_crit = 1.214 | 0.607 | Langmuir 1948 (opened): found in the second half of 1947 by "new calculations" with improved step-by-step methods; the 1945 report had given about 1.0 |
| Stokes flow, sphere, refined | 1.21194 ("correct to five decimal places") | 0.60597 | Michael and Norey 1970, Can. J. Phys. 48, "Slow motion of a sphere in a two-phase medium", DOI 10.1139/p70-202 (abstract only, via search tool) |
| Stokes flow, quoted by a later paper | about 0.605 for Re = 0, falling to 1/24 as Re goes to infinity; diameter-based St = tau_p U / d | | arXiv:1708.03198 (ar5iv HTML opened as a search excerpt), citing Phillips and Kaye (1999) |

Notes.
- Michael and Norey (1969), J. Fluid Mech. 37, 565-575, DOI 10.1017/S0022112069000723, is the POTENTIAL-flow paper (collision efficiencies, with and without
  gravity). Only its abstract was seen. The Stokes-flow value 1.21194 is in their 1970 Canadian Journal of Physics paper. The abstract of that paper says that
  Langmuir had given 1.214 and that the new value does not allow for the build-up of lubrication resistance as the particle nears the sphere, so it is the value
  at which a particle comes within about its own diameter of the sphere in finite time. So it is a limit for a point particle, not a contact value for a droplet of finite size.
- Phillips and Kaye (1999), J. Aerosol Sci. 30(7), "The influence of the viscous boundary layer on the critical Stokes number for particle impaction near a
  stagnation point", DOI 10.1016/S0021-8502(98)00766-6: only the listing was seen. The "0.605" and "1/24" in the table above come from the arXiv paper quoting it,
  not from Phillips and Kaye. 0.605 is not exactly half of 1.21194 (0.60597); the third digit is probably rounding in the quoting paper, but I could not check.
- Slinn (1983), as quoted in the same arXiv paper (diameter-based St): E about ((St - St_c)/(St - St_c + 2/3))^(3/2), with St_c about
  (0.6 + (1/24) ln(1 + Re/2)) / (1 + ln(1 + Re/2)). Secondary source, not verified.
- A lecture note (Clarkson University, Ahmadi, https://webspace.clarkson.edu/projects/crcd/public_html/me537/downloads/P_Impaction.pdf, excerpt) gives
  St_crit = 1/(4b) on the stagnation streamline with b = 2 for a cylinder and b = 3 for a sphere in inviscid flow (1/8 and 1/12), which agrees with Langmuir.
- Lesnic, Elliott and Ingham (1994, Mathematika, DOI 10.1112/S0025579300007385) give bounds on the critical Stokes number for potential and viscous flows
  (abstract only).
- Factor-2 trap: Langmuir's inviscid efficiency for a sphere is E = K^2 / (K + 1/2)^2 (his equation 9, valid for K above about 0.2). In terms of the diameter-based St the
  same curve reads St^2 / (St + 1/4)^2. That is my own algebra; one lecture note I saw prints the form with 1/4 and a radius in its definition, which I could not reconcile.
  Always state which length (collector radius or diameter) the Stokes number uses.

What this does not establish. Whether a droplet of the study (r about 8 um on a collector of 20 to 300 um radius) is a point particle: the critical value is for a point.
Finite size adds interception, which Langmuir's equations (9) and (16) do not contain.

---------------------------------------------------------------------

## 5. Langmuir (1948)

Reference. Langmuir, I., 1948: The production of rain by a chain reaction in cumulus clouds at temperatures above freezing. J. Meteorol. 5(5), 175-192.
DOI 10.1175/1520-0469(1948)005<0175:TPORBA>2.0.CO;2
Opened: https://journals.ametsoc.org/downloadpdf/journals/atsc/5/5/1520-0469_1948_005_0175_tporba_2_0_co_2.pdf (full text, 18 pages, OCR).

What it establishes (paraphrase).
- Collection efficiency E for a collector drop of radius S falling through droplets of radius r. Two limits for a sphere, both with Stokes drag on the cloud droplet
  (his Table 1, in terms of K defined in section 4):
  - E_A, "aerodynamic" = potential flow past the sphere: E_A = K^2 / (K + 1/2)^2 for K above about 0.2 (equation 9, from improved methods of summer 1947), critical K = 1/12.
  - E_V, viscous flow past the sphere: E_V = [1 + (3/4) ln(2K) / (K - 1.214)]^(-2) (equation 16), critical K = 1.214. Check: K = 10 gives 0.634, as he says.
- The interpolation. Which limit applies depends on the Reynolds number of the collector, R_s = 2 rho S U / eta (air density rho, collector radius S, fall speed U).
  The form is (his equation 23, stated as an empirical equation):
  E = [E_V + E_A (R_s / 60)] / [1 + (R_s / 60)].
  So E tends to E_V when R_s is small compared with 60 and to E_A when it is large.
- Its stated basis. He plotted the fall speed U(S) from his drag table (Table 2) on log axes and found two straight asymptotes: slope 2 where Stokes law holds (C_D R/24 = 1) and
  slope 1/2 where C_D is constant at C_0 = 0.40. They cross at R_s = 24 / 0.40 = 60. The efficiency equation copies that way of joining the two asymptotes. It is not derived from the equations of flow;
  it was applied with the R_s of Table 2. For K below about 2 he interpolated along straight lines radiating from K = 2.5 on the K axis (his equation 25 and Fig. 1), because the two limit curves are not parallel there.
  The critical K moves from the potential-flow value (for S very large) to 1.214 (for S going to zero).
  (The section 6 text as extracted gives 0.125 for the large-S limit, which is the cylinder value; his Table 1 gives 0.0833 for the sphere. I treat this as a slip in his text or in the extraction.)
- His Table 1 (limits, OCR):

| K | E_A | E_V |
|---|---|---|
| 0.0833 | 0 (critical) | 0 |
| 0.10 | 0.011 | 0 |
| 0.15 | 0.047 | 0 |
| 0.20 | 0.081 | 0 |
| 0.40 | 0.199 | 0 |
| 0.60 | 0.298 | 0 |
| 1.00 | 0.445 | 0 |
| 1.214 | 0.501 | 0 (critical) |
| 1.5 | 0.563 | 0.066 |
| 2.0 | 0.640 | 0.186 |
| 3.0 | 0.738 | 0.326 |
| 5 | 0.826 | 0.472 |
| 10 | 0.907 | 0.634 |
| 20 | 0.952 | 0.760 |
| 50 | 0.980 | 0.872 |
| 100 | 0.990 | 0.924 |
| 200 | 0.995 | 0.956 |

- His Table 4 (collection efficiency, interpolated, OCR). Rows: collector radius S in um; columns: droplet radius r in um. Built from Fig. 1 and his Table 2,
  which is for air at 785 mb and +2 C (about 2000 m), not sea level. For S above 1000 um he took U = 900 cm/s.

| S (um) | r = 2 | 3 | 4 | 6 | 8 | 10 | 15 | 20 |
|---|---|---|---|---|---|---|---|---|
| 15 | - | - | - | - | 0.092 | 0.269 | 0.500 | 0.643 |
| 25 | - | - | - | 0.050 | 0.277 | 0.411 | 0.613 | 0.724 |
| 40 | - | - | - | 0.205 | 0.394 | 0.510 | 0.690 | 0.782 |
| 70 | - | - | 0.035 | 0.340 | 0.500 | 0.608 | 0.750 | 0.834 |
| 100 | - | - | 0.133 | 0.418 | 0.564 | 0.660 | 0.793 | 0.862 |
| 150 | - | 0.010 | 0.245 | 0.498 | 0.631 | 0.713 | 0.829 | 0.887 |
| 200 | - | 0.085 | 0.326 | 0.564 | 0.684 | 0.756 | 0.859 | 0.908 |
| 300 | - | 0.213 | 0.425 | 0.643 | 0.749 | 0.810 | 0.892 | 0.929 |
| 400 | 0.040 | 0.303 | 0.500 | 0.698 | 0.793 | 0.849 | 0.919 | 0.950 |
| 600 | 0.121 | 0.355 | 0.530 | 0.731 | 0.827 | 0.876 | 0.939 | 0.963 |
| 1000 | 0.140 | 0.358 | 0.535 | 0.738 | 0.834 | 0.886 | 0.944 | 0.966 |
| 1400 | 0.168 | 0.360 | 0.534 | 0.735 | 0.840 | 0.890 | 0.950 | 0.970 |
| 1800 | 0.117 | 0.288 | 0.456 | 0.680 | 0.800 | 0.865 | 0.935 | 0.965 |
| 2400 | 0.075 | 0.220 | 0.372 | 0.606 | 0.743 | 0.823 | 0.920 | 0.950 |
| 3000 | 0.050 | 0.170 | 0.306 | 0.546 | 0.690 | 0.785 | 0.900 | 0.940 |

- His Table 5: smallest collector radius that collects anything, for droplet radius r: r = 1.5: 600 um; 2: 350; 3: 140; 4: 58; 5: 31; 6: 20; 7: 14 (all in um). Droplets above 8 um radius have no such limit.
  His own sample growth (collector 40 um growing to 3000 um in droplets of 8 um radius, 1 g/m3) takes 3860 s by his Tables 6 and 7.
- His Table 2 gives rigid-sphere C_D Re/24 against Re: 1.009 (0.05), 1.176 (1.0), 1.78 (10), 4.59 (100), 8.26 (300), 18.62 (1000) and so on, with the matching fall speeds for the collector at 785 mb and +2 C
  (for example S = 43 um: 19.9 cm/s; S = 106 um: 80 cm/s; S = 313 um: 272 cm/s).

What it does not establish.
- E is for point droplets obeying Stokes drag, with droplet inertia but no hydrodynamic interaction between the two bodies and no interception term. Langmuir himself says the real efficiency should be
  checked against experiment and later work did (Hall's table is the later reference).
- The numbers in his Table 4 are for 785 mb / +2 C, and the interpolation (equation 23) is empirical, not derived.
- The correct reading of "E" (which cross-section it is normalised to) should be checked against the page images; I read it as the fraction of droplets in the volume swept by the collector of radius S.

---------------------------------------------------------------------

## 6. Hall (1980)

Reference. Hall, W. D., 1980: A detailed microphysical model within a two-dimensional dynamic framework: model description and preliminary results. J. Atmos. Sci. 37(11), 2486-2507.
DOI 10.1175/1520-0469(1980)037<2486:ADMMWA>2.0.CO;2
Opened: https://journals.ametsoc.org/downloadpdf/journals/atsc/37/11/1520-0469_1980_037_2486_admmwa_2_0_co_2.pdf (full text, 22 pages, OCR). Free to read at AMS.

What it establishes (paraphrase).
- Table 1 of the paper is the model's collision-efficiency table for water drops, with collector radius (rows) against radius ratio r/R (columns), and it was taken from Schlamp et al. (1976).
  It is assembled from earlier calculations:
  - collectors of radius below 30 um: Davis (1972) and Jonas (1972), Stokes flow past two interacting droplets with gas-kinetic slip corrections;
  - collectors of 40 to 300 um, ratio r/R below 0.6: Schlamp et al. (1976), Lin and Lee (1975) and Shafrir and Gal-Chen (1971), all with the superposition approximation
    (each drop moves in the flow field of the other as if alone); Hall says this is not valid above ratio 0.6 because of nonlinear interaction and long interaction times;
  - collectors of 40 to 300 um, ratio above 0.6: Klett and Davis (1973), modified Oseen flow, the only treatment he found for that range;
  - collectors above 300 um: E = 1 assumed.
  Coalescence efficiency is taken as 1. The values are for laminar flow; he notes that de Almeida (1979) finds larger values in turbulence.
- The model uses Beard (1977) fall speeds for surface conditions and no altitude dependence of either the fall speed or the efficiency.
- Hall states no error bars on the table; the accuracy of each block is that of its source calculation (not stated in Hall).

Table 1 of the paper (OCR). Row label is the collector radius R in um (called "drop radius" in the extracted text); columns are the ratio r/R of the collected to the collector radius.
Values above 1 are as printed (wake capture, from the Klett and Davis block). The jump in the 30 to 40 um rows at small ratio is where the source method changes.

| R (um) \ r/R | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.45 | 0.50 | 0.55 | 0.60 | 0.65 | 0.70 | 0.75 | 0.80 | 0.85 | 0.90 | 0.95 | 1.00 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 300 | 0.97 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| 200 | 0.87 | 0.96 | 0.98 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| 150 | 0.77 | 0.93 | 0.97 | 0.97 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| 100 | 0.50 | 0.79 | 0.91 | 0.95 | 0.95 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| 70 | 0.20 | 0.58 | 0.75 | 0.84 | 0.88 | 0.90 | 0.92 | 0.94 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.97 | 1.0 | 1.02 | 1.04 | 2.3 | 4.0 |
| 60 | 0.05 | 0.43 | 0.64 | 0.77 | 0.84 | 0.87 | 0.89 | 0.90 | 0.91 | 0.91 | 0.91 | 0.91 | 0.91 | 0.92 | 0.93 | 0.95 | 1.0 | 1.03 | 1.7 | 3.0 |
| 50 | 0.005 | 0.40 | 0.60 | 0.70 | 0.78 | 0.83 | 0.86 | 0.88 | 0.90 | 0.90 | 0.90 | 0.90 | 0.89 | 0.88 | 0.88 | 0.89 | 0.92 | 1.01 | 1.3 | 2.3 |
| 40 | 0.001 | 0.07 | 0.28 | 0.50 | 0.62 | 0.68 | 0.74 | 0.78 | 0.80 | 0.80 | 0.80 | 0.78 | 0.77 | 0.76 | 0.77 | 0.77 | 0.78 | 0.79 | 0.95 | 1.4 |
| 30 | 0.0001 | 0.002 | 0.02 | 0.04 | 0.085 | 0.17 | 0.27 | 0.40 | 0.50 | 0.55 | 0.58 | 0.59 | 0.58 | 0.54 | 0.51 | 0.49 | 0.47 | 0.45 | 0.47 | 0.52 |
| 20 | 0.0001 | 0.0001 | 0.005 | 0.016 | 0.022 | 0.03 | 0.043 | 0.052 | 0.064 | 0.072 | 0.079 | 0.082 | 0.080 | 0.076 | 0.067 | 0.057 | 0.048 | 0.040 | 0.033 | 0.027 |
| 10 | 0.0001 | 0.0001 | 0.0001 | 0.014 | 0.017 | 0.019 | 0.022 | 0.027 | 0.030 | 0.033 | 0.035 | 0.037 | 0.038 | 0.038 | 0.037 | 0.036 | 0.035 | 0.032 | 0.029 | 0.027 |

For the study's pair (collector 40 um, collected droplets 8 and 10 um): r/R = 0.20 gives E = 0.50, r/R = 0.25 gives E = 0.62.
Langmuir's Table 4 gives 0.394 and 0.510 for S = 40 um with r = 8 and 10 um (at 785 mb, point droplets, so lower).

What it does not establish.
- No uncertainty. Entries are rounded to two significant figures, and some adjacent entries (the 0.95 to 0.97 plateaus, the row ends above 1) look like hand-merged blocks.
- Only sea-level conditions. Only the size-dependence; nothing on pressure (Pinsky et al. 2001 add that).
- The OCR may have misread digits; check the table against the page image before coding it. The ten rows asked for (20 um to 300 um) plus the 10 um row are all given above.

---------------------------------------------------------------------

## 7. Pinsky, Khain and Shapiro (2001)

Reference. Pinsky, M., Khain, A. and Shapiro, M., 2001: Collision efficiency of drops in a wide range of Reynolds numbers: effects of pressure on spectrum evolution.
J. Atmos. Sci. 58(7), 742-764. DOI 10.1175/1520-0469(2001)058<0742:CEODIA>2.0.CO;2
Partly opened: https://journals.ametsoc.org/view/journals/atsc/58/7/1520-0469_2001_058_0742_ceodia_2.0.co_2.xml (abstract, introduction, parts of sections 2 to 5 as search-tool excerpts).
The PDF link returned 404; the appendix tables of efficiencies (A1 to A9) were NOT seen.

What it establishes (paraphrase).
- Method. A superposition method (Pruppacher and Klett 1997): each drop moves in the flow field that its partner would make alone. This is not the full hydrodynamic-interaction method
  (no-slip conditions on both surfaces) used by Davis and Hocking for small droplets. The authors say the superposition method is least accurate near contact and most accurate for drops of dissimilar size,
  because dissimilar drops pass the close region quickly.
- The flow field is the Stokes solution for droplets below 30 um (Re below 0.4), the Hamielec and Johnson (1962) solution for 40 to 300 um, and an interpolation with weights between them.
  Reynolds numbers from 0 to 100, collectors up to 300 um radius, one method over the whole range (earlier work used a different method for each size range).
- Pressure dependence. Calculations at 1000, 750 and 500 mb, with T = 271 K at 750 mb and 251 K at 500 mb (surface 19 C, freezing level at 2.2 km). Efficiencies and kernels rise with height.
  The largest gain in efficiency is a factor 2.1 at 500 mb for the pair of radius 5 and 29 um. Droplets of 2 to 10 um with collectors of 17 to 30 um gain most.
  The collection kernel at 500 mb is up to 2.35 times the 1000 mb value (about twice for droplets of 5 to 10 um with collectors of 15 to 25 um). Of that increase, about 90 % is from the efficiency and
  about 10 % from the larger swept volume. For radii above 40 to 50 um the efficiency is already near 1, so the kernel there grows only through the swept volume (1.1 at 700 mb, 1.3 at 500 mb).
- A box-model run (initial droplets centred at 10 um, 1 g/m3) shows the early spectrum evolving much faster at 500 mb: raindrops of 300 um radius at 20 min, against none above 90 um at 1000 mb.
- They remark that earlier authors' efficiencies differ significantly from each other; this paper's tables are given at high resolution in size for small droplets.

What it does not establish, or what I could not find.
- Numbers for a 40 um collector with 8 to 10 um partners: not obtained (they are in the appendix tables I could not open). The difference from Hall's table: the passages that compare the two were not in the excerpts.
- The definition of the kernel is garbled in the excerpt (the symbols were lost); the standard form is K = pi (r1 + r2)^2 E |V1 - V2| but I did not see it written.
- The fall-speed law they use was not seen.

---------------------------------------------------------------------

## 8. Open questions

Not opened.
- Schiller and Naumann (1933); Clift, Grace and Weber (1978); Pruppacher and Klett (1997) chapter 10; Beard (1977); Langmuir and Blodgett (1946 report); Michael and Norey (1969 and 1970 full text); Phillips and Kaye (1999) full text; Davies (1945); Beard and Pruppacher (1969); Schlamp et al. (1976); Pinsky et al. appendix tables; Foote and du Toit (1969) (the PDF at atmos.albany.edu was listed, not read).

Secondary or snippet-only sources (named above): Kajikawa (1974) for the Gunn and Kinzer velocity column and for 25.6 cm/s at 0.10 mm; the disdrodb file and AMT paper, the St Andrews thesis and CARMApy for Beard's coefficients; arXiv:1708.03198 for 0.605 and 1/24; Slinn (1983) as quoted there; Clarkson lecture note.

Uncertain.
- Beard regime 2, coefficient b6 (-3.27815e-6) is not confirmed by an independent text.
- Beard's formulas for how the viscosity, surface tension and air and water density vary with temperature and pressure were not extracted; they are needed to use the scheme away from 20 C and 1 atm.
- Beard's agreement figures (0.09 % rms, 0.6 % maximum, +-0.5 %) measure how well the polynomials match the formulas or data they were fitted to. There is no independent experimental check of regimes 1 and 2 in this paper.
  Because the Gunn and Kinzer data differ from Beard's formula by 3.3 % rms between 0.1 and 1 mm, a choice must be made there; Beard's argument is that the data are the weaker side below 0.4 mm. No measurement below about 0.1 mm was in the sources.
- The 0.605 against 0.606 (diameter-based Stokes critical value) and the "Phillips and Kaye" origin of 0.605 rest on one secondary paper.
- Langmuir's section 6 gives 0.125 as the large-collector critical K where his Table 1 gives 0.0833; and his equation (8) was extracted with "2/3" where 2/9 is implied. Both look like slips (his or the OCR's); the page image should settle them.
- Hall's table and Langmuir's Table 4 were typed from OCR; any digit going into code needs a check against the page image. Hall's table has several block-merging features (flat 0.95 to 0.97 plateaus, jump between 30 and 40 um) whose origin I did not trace to the source papers.
- Pinsky et al. 2001: efficiency numbers for the study's pairs and the comparison with Hall are missing. Recommended next step: obtain the PDF (appendix tables A1 to A3 at 1000 mb) from a library or from the authors' pages.
- Which of Hall (1980), Pinsky et al. (2001) or a newer compilation is the right choice for droplets of 8 um radius with collectors near 20 um to 40 um is a physics decision for the study. In that corner (r/R about 0.2 to 0.4, R about 20 to 40 um) Hall, Langmuir and Pinsky are expected to differ most
  (the Hall rows for 20 um and 30 um differ from the 40 um row by factors of 10 to 100 at small ratios), and Pinsky et al. say that is where the pressure effect is largest.

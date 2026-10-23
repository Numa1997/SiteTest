# Contract L1: fall speed from a drag balance (round 3)

Gate 1. Round 1 failed (2 fatal, 8 must-fix), round 2 failed (0 fatal, 4 must-fix, 15 minor); round 2's objections are answered in
section 10. Every number in this contract is printed by `portfolios-src/droplets/derive/L1_r2.py` (which imports `L1_beard.py`),
except where a line names another file.

Sources and how they were read. Beard (1976): read whole by the scout (OCR, `dossier-fallspeed-efficiency.md` §2); coefficients
confirmed digit by digit in disdrodb `fall_velocity/rain.py` (read by the lead). Gunn and Kinzer (1949): table and body read by the
scout (OCR); abstract read. LeClair, Hamielec and Pruppacher (1970), Beard and Pruppacher (1969), Pruppacher and Beard (1970):
abstracts read by the lead on 23 October 2026 (journal pages via a search tool; the full texts are blocked to this session).
Langmuir (1948): read whole by the scout.

## 1. Question and observables

How fast does a drop of radius a fall in still air at the cloud's temperature and pressure, and how much does replacing Stokes'
law change the growth of L0? Observables: v(a) for diameters 1 µm to 5.8 mm (regime 3, above 1.07 mm, is carried for later rungs; no
L1 result depends on it); its agreement with measurements; L0's open-cloud time 40 → 100 µm and its closed-box t₅₀, t₉₀ recomputed
with the new speed. In the closed box F_c is the fraction of all water held by the collectors (collector water over collector plus
droplet water; 0.294 at t = 0), and t₅₀, t₉₀ are the times at which F_c reaches 0.5 and 0.9 (E = 1, coalescence = 1, finite r).

## 2. Picture and formal mechanism

Picture: draw a teaspoon slowly through honey. The honey closes in behind it at once, and doubling the speed doubles the push you
feel. Swish the same spoon through water: the water piles up in front and swirls away behind, and doubling the speed roughly
quadruples the push. In honey the fluid's viscosity sets the push (Re = 0.01–0.07 for a 1 cm spoon at 1 cm/s, honey of 2–14 Pa s);
in water the momentum of the fluid thrown aside sets it (Re ≈ 10⁴ at 1 m/s). A falling droplet lives in the honey world. A collector
leaves it gradually: by Beard's law, doubling the speed multiplies the drag by 2.13 at a = 40 µm (Re = 0.84) and by 2.44 at 100 µm
(Re = 8.6), a quarter of the way from the honey world's 2 to the water world's 4.

Mechanism: steady fall, weight less buoyancy equals drag:

  (4π/3) a³ (ρ_w − ρ_a) g = ½ ρ_a v² π a² C_D,          Re = 2aρ_a v/μ.                                       (L1.1)

For a rigid sphere the drag depends on a, v, ρ_a, μ only: five quantities with the force, three units, two groups, so C_D = C_D(Re).
Multiplying (L1.1) by Re² removes the unknown speed: the Davies number N_Da = C_D Re² = 4ρ_a(ρ_w − ρ_a) g d³/(3μ²) (d = 2a) holds
only the drop and the air, the drag law becomes Re(N_Da), and v = μ Re/(ρ_a d). A large drop also flattens and its water may
circulate; that brings in three more quantities (σ, Δρ g and μ_w) and with them more groups: Beard's regime 3 uses the Bond number
Bo = 4Δρ g d²/(3σ) and N_P = σ³ρ_a²/(μ⁴Δρ g); the viscosity ratio μ_w/μ_a, which governs internal circulation, is neglected everywhere
(row in section 5).

## 3. Model

State: none new (v is algebraic in a). Law: (L1.1). Closures, all of Beard (1976):
- Regime 1, d < 19 µm: Stokes' law C_D = 24/Re, derived in this study's textbook (chapter on fall speed, source in
  `portfolios-src/droplets/text/`, written after Gate 2; the same derivation is in the baseline, `notes/droplets/baseline/theory.html`,
  eqs. 13–15), times the slip factor C_sc = 1 + 2.51 ℓ/d (2.51 = 2 × 1.257, Davies' constant as Beard uses it), with Beard's mean free
  path ℓ = ℓ₀ (μ/μ₀)(p₀/p)(T/T₀)^½, ℓ₀ = 6.62 × 10⁻⁸ m, μ₀ = 1.818 × 10⁻⁵ Pa s, p₀ = 1013.25 hPa, T₀ = 293.15 K; ℓ = 0.0756 µm here.
  C_sc is kept as a first-order factor in regime 2 as well; it matters only below about 30 µm.
- Regime 2, 19 µm ≤ d < 1.07 mm: ln(Re/C_sc) = Σ_{k=0}^{6} b_k (ln N_Da)^k, fitted by Beard to three drag formulas for a rigid sphere:
  LeClair et al.'s (1970) numerical Navier–Stokes solutions (Re 0.01–20), Beard and Pruppacher's (1969) wind-tunnel measurements on
  water drops (Re 20–258), Perry's (1950) handbook curve above. The fit's rms 0.09 %, max 0.6 % is fit quality against those formulas.
  LeClair et al. report their computed drag "in close agreement" (abstract) with the measurements of Pruppacher and Steinberger (1968)
  and of Beard and Pruppacher over the whole range Re 0.01–400, and that as Re → 0 the drag approaches the Oseen drag, not the Stokes
  drag. In the study's collector range (a = 40–100 µm, Re = 0.84–8.6; Re = 20 at a = 146 µm) the speed is therefore LeClair's
  computation, checked by its authors against measurements of rigid spheres and of water drops. A rigid sphere's C_D(Re) is universal,
  so the regime carries over to 850 hPa through Re alone.
- Regime 3, 1.07 mm ≤ d < 7 mm: Re = N_P^{1/6} exp Σ_{k=0}^{5} c_k Y^k, Y = ln(Bo N_P^{1/6}), fitted by Beard to Gunn and Kinzer at sea
  level; its pressure dependence rests on Garner and Lihou's scaling, with no measurement aloft (Beard).
- Air: ideal gas; Sutherland's viscosity with the constants of N. Koudsie's thesis (2022, eq. 20, as quoted in the baseline:
  1.72 × 10⁻⁵ Pa s at 273 K, S = 120 K), 0.34 % above the standard constants (1.716 × 10⁻⁵ Pa s, S = 110.4 K) at 10 °C; σ from IAPWS (2014).

## 4. Rejected alternatives

1. Stokes' law for all sizes (the thesis): its own Re reaches 1 at a = 41.0 µm (Beard's at 42.7 µm), and the error grows smoothly:
   too fast by 1.5 % at 20 µm, 11 % at 40 µm, 27 % at 60 µm, 69 % at 100 µm.
2. A rigid-sphere law at all sizes: measured drops are spherical within error below a = 140 µm and slightly oblate from 140 to 500 µm
   (Pruppacher and Beard 1970, abstract); a 3 mm drop is flattened (Bo = 1.617 at 20 °C). A rigid sphere with Langmuir's (1948)
   large-Re drag C_D = 0.40 would fall √(0.503/0.40) = 1.12 times faster than Gunn and Kinzer measured at 3 mm (their C_D = 0.503);
   with Langmuir's own C_D at Re = 1000, 0.447, the excess is about 1.06; Beard's regime 3 carries the shape.
3. Solving the Navier–Stokes equations around the sphere ourselves: in the collector range this is what LeClair et al. did, and what
   the fit carries; repeating it would add cost and no physics. Rejected for cost.

## 5. Assumptions and their numbers (10 °C, 850 hPa)

| Assumption | Number | Fails where |
|---|---|---|
| Steady fall | τ_p = 20.08 ms at 40 µm; growth times are minutes | never here |
| Isolated drop in still air | spacing n^{−1/3} = 1.494 mm = 37 radii of a 40 µm collector (15 of a 100 µm drop); its Oseen length ν/v = 96 µm | crowded rain shafts |
| Continuum air with first-order slip | ℓ = 0.0756 µm; Knudsen 2ℓ/d = 0.0094 at d = 16 µm; C_sc − 1 = 1.19 % at d = 16 µm, 0.24 % at 80 µm | below d ≈ 1 µm |
| Rigid, non-circulating drop | measured drops do circulate (surface speed about 1/100 of the fall speed, Pruppacher and Beard 1970); Hadamard–Rybczynski gives +1/(2 + 3κ) = +0.45 % on the Stokes speed for κ = μ_w/μ_a = 73.7 (μ_w = 1.306 × 10⁻³ Pa s, a standard value not re-read) | negligible below regime 3 |
| Spherical below regime 3 | measured drops are spherical within error below a = 140 µm; Bo = 0.0070 at d = 200 µm, 0.20 at 1.07 mm | regime 3 |
| Dry air | saturated air is 0.55 % lighter: v changes +0.045 % at 40 µm, +0.124 % at 100 µm; its viscosity differs by a fraction of a percent (not computed here); both act on Stokes and Beard alike and cannot move the time ratios of section 7 | negligible |
| No charge | not quantified here; the thesis cloud is a fair-weather case, and electric forces are outside the study (stated on the page) | thunderstorms |
| No turbulence | deferred to L6, where its size is computed | strong convection |

One effect at this rung: what changes the L0 results is the inertial drag of regime 2. Slip changes Δv at 40 µm by +0.19 %; shape is
not modelled below 1.07 mm.

## 6. Comparison with measurement

- **In the study's range** (d = 80–200 µm, Re 0.84–8.6): Beard's regime 2 is LeClair's computed drag, which its authors found in close
  agreement with Pruppacher and Steinberger's (1968) measured drag on rigid spheres (Re 0.001–10) and Beard and Pruppacher's (1969)
  wind-tunnel measurements on water drops (radii 10–475 µm, Re 0.2–200, saturated air, speeds also given for 400–1013 mb). This study
  read those three papers only as abstracts, so the agreement is the authors' statement, not checked here. One number is known here,
  from a search excerpt of Kajikawa (1974): Beard and Pruppacher's 25.6 cm/s at d = 0.1 mm, 2.5 % above Beard's formula (24.96 cm/s in
  dry air, 24.98 cm/s in saturated air).
- **Gunn and Kinzer (1949)**, 20 °C, 760 mm Hg, 50 % relative humidity (their abstract: "better than 0.7 per cent"; the scout's OCR
  reading of the body limits this to masses of 10–100 000 µg, d = 0.27–5.8 mm), compared in their own humid air (density 0.44 % below
  dry air):
  - in sample, 1.2–5.8 mm (regime 3 was fitted to these data): |error| ≤ 0.49 %, inside Beard's ±0.5 %, by construction;
  - out of sample, 0.3–1.0 mm (regime 2): −1.94, −1.94, −1.90, −1.01, −0.34, −0.21, −0.56, −0.37 %, one-signed: the formula is up to
    1.9 % below the data at 0.3–0.5 mm, nearly three times their stated accuracy;
  - in the study's range, d = 0.1 and 0.2 mm: −7.5 % and −3.5 %.
  The sources disagree about these small drops: Beard (1976) judges Gunn and Kinzer's data below about 0.4 mm inaccurate (evaporation
  of the smallest drops), while Beard and Pruppacher (1969) say their own data "agreed quite closely" with Gunn and Kinzer's; yet at
  0.1 mm the one value known here differs from Gunn and Kinzer's 27 cm/s by 5 %. This study cannot resolve the conflict without the
  full papers and says so on the page. If the truth at d = 80–200 µm lies 2–4 % above Beard's formula, L1's growth times are 2–4 % too
  long, below every other uncertainty of observable 1.
- **Low end of the fit:** the polynomial has no small-N_Da limit (Re_fit/Re_Stokes = 0.996 at ln N_Da = −2, 0.83 at −4). At ln N_Da = 0
  it is 0.85 % below Stokes, and Oseen's inertial correction Re(1 + 3Re/16) = N_Da/24 (Oseen's law, cited; the approach to Oseen's drag
  as Re → 0 is LeClair et al.'s finding) gives 0.77 %; at −1.1 the two give 0.20 % and 0.26 %. The small gap from Stokes at the 19 µm
  joint is inertia, as it should be.
- **Joints:** −0.17 % at 19 µm and −0.02 % at 1.07 mm (10 °C, 850 hPa); −0.19 % and +0.003 % at 20 °C, 1013 hPa.
- **Coefficients:** all thirteen equal disdrodb's transcription digit by digit.

## 7. What the new speed does to growth, and the prediction

The time ratio is fixed between exact bounds. In both the open cloud and the closed box the time is t = ∫ f(R) dR/ΔV(R) with the same
f(R) > 0 for both speed laws and ΔV = v(R) − v(r) > 0 for R > r (each law with its own droplet speed: v_S(8 µm) = 0.00787 m/s without
slip, v_B = 0.00796 m/s with slip). Hence t_B/t_S = ∫ w (ΔV_S/ΔV_B) dR / ∫ w dR with the positive weight w = f/ΔV_S: a weighted mean of
ΔV_S/ΔV_B over the radii crossed, between its smallest and largest value there (the ratio rises monotonically with R, so the bounds
are its end values):

- open cloud, 40 → 100 µm: bound [1.117, 1.698]; computed 597.3 s (Stokes) → 781.1 s (Beard), ratio 1.308;
- closed box, F_c = 0.5 (R = 47.74 µm): bound [1.117, 1.174]; computed 175.6 → 201.0 s, ratio 1.145;
- closed box, F_c = 0.9 (R = 58.07 µm): bound [1.117, 1.262]; computed 551.5 → 661.8 s, ratio 1.200.

These are code tests, not physics tests: a result outside its bound would be a code error. The open-cloud growth rate
(R + r)²ΔV/R² has local exponent 1.47 (40–50 µm), 1.44 (40–60), 1.32 (60–80), 1.23 (80–100): above 1, so growth over the study's window
is still faster than exponential; exponential growth needs exponent 1, and only for v ∝ a^½ (constant C_D, Re above about 10³) does
R^{1/2} grow linearly in time. The L0 blow-up (1264.0 s from 40 µm with r ≪ R) lies outside the 40 → 100 µm window; the lengthening
comes from v_S/v_B = 1.11–1.69 across it.

**Prediction that could come out wrong.** In the full SCE of L4 (all pairs, lognormal modes, E = 1, the coalescence law), replacing
Stokes speeds by Beard speeds lengthens t₉₀ by a factor inside the closed box's bound [1.117, 1.262], although the SCE has channels the
box lacks (droplet–droplet and collector–collector mergers, a size spread, and a coalescence law that itself depends on the speed).
If the factor falls outside, those channels respond to the fall speed differently from collection, and the page's account of where
the drag law acts must change. Not computed before this contract was written.

L1 makes no new prediction against nature: in the study's range its drag law is LeClair's computation, and its test against nature
is the agreement LeClair, Beard and Pruppacher report with measurements (section 6), which this study takes from their abstracts.

## 8. Derived, cited, chosen, and the price

Derived: (L1.1), the Davies number, the exact time-ratio bounds, the self-consistency failure of Stokes' law, the drag exponents of the
picture. Cited: Beard's regimes and coefficients (a fit to LeClair et al.'s computed drag, Beard and Pruppacher's measurements and
Perry's curve), the slip constants, Oseen's law, Sutherland's law with the thesis's constants, IAPWS σ, Gunn and Kinzer's data, the
measurements named in section 6. Chosen: Beard's regime boundaries, ρ_w = 1000 kg/m³, dry air. Price: a fitted law has no physics
outside its range; its high-order terms are large and cancelling (seven terms at d = 0.2 mm, 10 °C, 850 hPa: −3.19, 5.81, −0.05,
−0.20, −0.68, 0.59, −0.13), so it must not be extrapolated; the small-drop data disagree among themselves by up to 5 % at 0.1 mm.

## 9. What L1 changes in the study

The thesis kernel and the extended kernel differ first in this rung: Stokes speeds overstate the collector's speed by 11–69 % between
40 and 100 µm. In growth this is a 14–31 % effect (section 7), smaller than the efficiency of L2 (contract L2 gives the bound for that).

## 10. Answers to round 2 (`skeptic-G1-L1-r2.md`)

| # | Objection | Answer |
|---|---|---|
| N1, #11 | Script does not print every number | `L1_r2.py` now prints every number of this contract (round-3 block), except the honey Re range (printed too) and Kajikawa's 25.6 cm/s (a search excerpt, stated). E values are no longer quoted here. |
| N2, #3 | Measurements in the study's range missed | §3 and §6 rewritten around LeClair et al., Pruppacher and Steinberger, Beard and Pruppacher (abstracts read by the lead), with the conflict about Gunn and Kinzer's small drops stated. |
| N3 | Prediction 2 cannot fail | Dropped. §7 says plainly that L1 makes no new prediction against nature, and why. |
| N4 | Prediction 1 cannot fail | Replaced by the SCE prediction of §7, not computed beforehand; the effect of E belongs to contract L2, with its bound. |
| N5 | "Halfway"; honey Re; wording; group count | Drag exponents 1.09 and 1.29 (×2.13, ×2.44): "a quarter of the way". Honey 2–14 Pa s, Re 0.01–0.07. Pressure/shear wording removed. Three quantities, the groups named. |
| N6, #21 | Dry vs 50 % RH | Gunn and Kinzer compared in their humid air: in sample 0.49 %, settled within Beard's ±0.5 %. |
| N7 | Moist viscosity | Stated qualitatively, not computed, and shown not to affect the time ratios. |
| N8 | Bound statement loose | Weight and both droplet speeds written; monotonicity stated. |
| N9 | F_c undefined | Defined in §1. |
| N10 | Seven terms' condition | Given at 10 °C, 850 hPa, printed. |
| N11, #16 | 1.12 from the asymptote | Both 1.12 (asymptote) and about 1.06 (Langmuir's C_D at Re = 1000) given; Pruppacher and Beard's measured shapes added. |
| N12 | Deformation statement | Replaced by the measured shapes. |
| N13 | No section 9 | Added. |
| N14 | Kajikawa a search excerpt | Said so. |
| N15 | Davies attribution, μ₀ | Moved to 2.51; μ₀, p₀, T₀ stated. |
| N16 | Spacing in droplet radii | Collector radii and the Oseen length added. |
| N17 | Charge, turbulence without numbers | Charge stated as outside the study; turbulence deferred to L6 where it is computed. |
| N18 | Rate exponent | Growth-rate exponents 1.47–1.23 given. |
| N19 | Oseen uncited | Cited, with LeClair's finding. |
| #12 | Textbook location | Given (planned source folder, and the baseline's existing derivation). |
| #13 | Gunn and Kinzer's body sentence | The mass limit stays attributed to the scout's OCR reading; the abstract's unqualified claim is quoted. |

## 11. After Gate 1 (passed in round 3, `skeptic-G1-L1-r3.md`): corrections and the prediction's outcome

- Moist air (§5): it does not act on both laws alike; it moves the time ratios by −0.07 % and +0.05 % (skeptic's computation), so the
  conclusion stands for a different reason: the change is too small to matter.
- Beard and Pruppacher (1969): their speeds at 400–1013 mb are calculated from their measured drag formula at assumed temperatures; the
  measurement is the drag at Re 0.2–200 in saturated air.
- The approach to the Oseen drag as Re → 0 is credited by LeClair et al. to Maxworthy and to Pruppacher and Steinberger; LeClair et al.
  confirm it. A rigid 3 mm sphere falls at Re ≈ 1700, where the excess over Gunn and Kinzer is about 1.1.
- §9's "14–31 %" holds for the box and the open cloud only.
- **The prediction of §7 failed** (computed in L4 after this contract, `status.md`; s = 8, Δt = 1 s, lognormal modes untruncated,
  thesis's coalescence law, E = 1, every pair): t₉₀ = 4.512 min with Stokes speeds and 7.963 min with Beard speeds, a factor 1.765, far
  outside the box bound [1.117, 1.262] (the skeptic's independent rough SCE gave 1.62–1.90). Reason: in the population, collectors also
  merge with each other and droplets with droplets, and those rates depend on the difference of fall speeds between similar drops,
  which Stokes' R² law exaggerates far more than it exaggerates one collector's speed. The drag law therefore matters more for the cloud
  than for a single collector; the lecture notes say so.

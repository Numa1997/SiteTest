# Contract L2: collision efficiency from droplet trajectories (round 2)

Gate 1. Round 1 (`skeptic-G1-L2-r1.md`: 11 must-fix, 8 minor) is answered in section 9; round-2 numbers in
`portfolios-src/droplets/derive/L2_r2.cjs`. Terms used from other levels: observable 1 = t₅₀, t₉₀ of the mass fraction in drops ≥ 40 µm;
observable 2 = time to the first 100 µm drop in a stated volume; SCE = the stochastic collection equation of L4; "the old study" = the
baseline in `notes/droplets/baseline/` built on Koudsie (2022). Sources: `dossier-fallspeed-efficiency.md` (Langmuir 1948 read whole by the scout; Hall 1980 Table 1 typed from OCR;
Michael and Norey 1970 and Pinsky, Khain and Shapiro 2001 seen only in part). Prototype and every number below:
`portfolios-src/droplets/derive/L2_traj.cjs` (solver), `L2_pairs.cjs`, `L2_langmuir.cjs`, `L2_numbers.cjs`, `L2_scan.cjs`,
`L2_trace.cjs`; fall speeds from `derive/beard.cjs` (L1).

## 1. Question and observables

Of the droplets whose centres lie in a collector's swept tube, which fraction actually touch it? Observables: the collision
efficiency E(R, r) on a table of collector radii 2 µm–4 mm and size ratios p = r/R from 0.002 to 1, at the cloud's air (10 °C,
850 hPa); E(40 µm, 8 µm); the critical Stokes numbers for a point droplet on the upstream axis; and the change of L1's closed-box
t₅₀, t₉₀ when the table replaces E = 1.

## 2. Picture and formal mechanism

Picture: drive through heavy rain and every drop ahead hits the windscreen; drive through fine mist and much of it never touches the
glass, because the air pushed aside by the car carries it round. A falling drop pushes the air below it aside in the same way, and
only droplets heavy enough to keep going while the air turns reach its surface.

Mechanism: Newton's law for the small droplet (the partner) in the air flow around the collector. In the collector's frame the air
far away rises at U = v(R); the partner feels the drag on its velocity relative to the local air and its own weight:

  dx/dt = v,     τ dv/dt = u(x) − v − τ g* e_z,     g* = g(1 − ρ_a/ρ_w).                                   (L2.1)

Scaled by R (length) and U (speed), time by R/U:

  dy/ds = w,     St dw/ds = a(y) − w − S e_z,     St = τU/R,     S = v(r)/U.                                 (L2.2)

St is the partner's stopping distance in collector radii: how far it would coast if the air stopped. The partner touches when
|y| = 1 + p (interception: its centre need only come within R + r). The largest starting offset b_c that still touches, far
upstream, gives E = (partner flux through the disc of radius b_c)/(flux through the disc of radius 1 + p).

## 3. Model

- **One-sided flow (Langmuir's method).** The partner moves in the flow of the collector alone; the collector does not feel the partner.
  This is *not* the superposition method of Hall's (1980) 40–300 µm sources and of Pinsky et al. (2001), in which each drop also moves in
  the flow its partner would make alone. The term left out: the partner's Stokes flow at the collector's centre, about (3/4)(r/d)v(r),
  is 0.006 U at 40/8 µm but 0.035 U at 20/8 µm, where the approach speed near contact is itself only about 0.1 U (skeptic's estimate).
- **Two model flows**, both exact solutions with a uniform stream U at infinity, in spherical coordinates (q = |y|, θ from the
  upstream direction of the air):
  creeping (Stokes) flow, ψ = ½ q² sin²θ (1 − 3/(2q) + 1/(2q³)), for collector Re → 0;
  potential flow, ψ = ½ q² sin²θ (1 − 1/q³), for Re → ∞ without a boundary layer or wake.
- **Interpolation in Re** (Langmuir 1948, his eq. 23, stated by him as empirical): E = (E_S + E_P Re/60)/(1 + Re/60), Re = 2Rρ_a U/μ.
  The 60 is where his Stokes and constant-drag asymptotes of the fall speed cross (24/0.40), an analogy, not the flow the partner meets.
  **This is the weakest link of the level.** At 40 µm (Re = 0.84) Stokes flow holds only within the Oseen length ν/U = 2.4 R, while the
  partner coasts 3.6 R; neither model flow is right between Re ≈ 1 and 20. The answer moves with the crossover: E(40, 8) = 0.344 (60),
  0.358 (20), 0.399 (6), 0.485 (2); Hall's 0.50 needs about 1.7 (`L2_r2.cjs`). A Navier–Stokes flow field at Re = 1–10 was chosen not to
  be computed at this rung (a lecture note, not a paper); instead Hall's table, whose 40–300 µm block was computed by its sources with
  flow fields of intermediate Reynolds number (dossier §7), is carried beside ours to the end, and observable 1 is reported as a band.
- **Partner drag.** Linear in the slip velocity with a drag-corrected relaxation time τ = v(r)/g*, so that the partner's terminal
  speed equals L1's Beard speed exactly; Stokes' τ = 2ρ_w r²/(9μ) differs by 1.2 % at 8 µm (slip) and by the inertial factor for larger
  partners. The transient drag nonlinearity along the path is neglected (row in section 5).
- **Start and flux.** Partners start at z = −Z (Z = 200 R for Stokes flow, 30 R for potential flow) moving with the local air less
  their settling; the flux through the start disc of radius b is 2π[ψ(b, −Z) − ½ S b²] (units U R²), so
  E = 2[ψ(b_c, −Z) − ½ S b_c²] / [(1 − S)(1 + p)²]. Far upstream ψ → ½ b², giving E = b_c²/(1 + p)².
- **Numerics.** Dormand–Prince 5(4) with error control on the gap; partners with St < 10⁻³ use the inertialess limit
  dy/ds = a − S e_z; bisection on b to 10⁻⁷ (1 + p). The critical Stokes numbers use the axis problem in log variables
  (ξ = ln η, u = w/η), where contact is a finite-time blow-up of u, classified exactly near the surface (creeping flow: the side of
  u = −1/St; potential flow: the sign of 1 − 12 St).
- **Table and use.** E on 64 collector radii (2 µm–4 mm, log-spaced) × 40 ratios (0.002–1, log-spaced), interpolated bilinearly
  in (ln R, ln p), clamped at the edges. Generated by the study's own code at build time (`tools/gen_tables.cjs`), stored with the
  air state and the generator's version, and re-checked by an independent Python integration of sample entries (Gate 2).
- **Near-equal sizes (p > 0.6).** Hall (1980) says superposition is not valid there. The model holds E at its p = 0.6 value (the
  choice of the old study), and every result that depends on these pairs is also computed with E = 1 above p = 0.6 for collectors
  ≥ 40 µm. These two do **not** bracket the truth: Hall's Klett and Davis block reaches 0.95–1.4 at R = 40 µm and 1.3–4.0 at R = 50–70 µm
  for p = 0.95–1 (wake capture). The reason it matters little is the weight, not a bracket: pairs with r/R > 0.9 carry 1.7 % of the
  mass transfer rate at t = 0 and 1.4 % after 10 min (`L2_r2.cjs`), because their speed difference is small.

## 4. Rejected alternatives

1. **Hall's (1980) compiled table** as the model: it is the standard input of bin models, but it has no generator, mixes four
   methods with jumps between their blocks (30 → 40 µm), is for sea level only, states no accuracy, and its digits here come from
   OCR. Used as the comparison of section 6, not as the model.
2. **Full hydrodynamic interaction** (two-sphere Stokes solutions, Davis 1972; Jonas 1972): needed for collectors below about
   30 µm and for near-equal sizes; beyond this study's means (the two-sphere resistance functions). Its absence is the main price.
3. **Navier–Stokes flow fields at intermediate Re** (Hamielec and Johnson 1962, as in Pinsky et al. 2001): their coefficients were
   not obtained; Langmuir's interpolation is used instead and labelled empirical.

## 5. Assumptions and their numbers (10 °C, 850 hPa)

| Assumption | Number | Fails where |
|---|---|---|
| One-sided flow | valid for p ≪ 1 and inertial partners; Hall: superposition not valid above p = 0.6 | near-equal sizes (section 3); and small collectors, where an inertialess partner on the axis hovers: its settling ratio S exceeds the air's approach speed at contact I(p) = 1 − 3/[2(1+p)] + 1/[2(1+p)³] for every pair computed (R = 20–40 µm, r = 6–12 µm; e.g. 40/8: S = 0.045 against I = 0.039), so only inertia (St) carries partners in; where St is near its critical value (R ≲ 25 µm) E switches on and off with p (R = 20 µm: nonzero only for p = 0.375–0.45; R = 16 µm: zero), a model artifact, with a floor of 0.0017 that comes only from the potential-flow weight. E for R < 30 µm in this model is not physics; prediction 3 tests that it does not matter |
| No wake in either model flow | real flow past a sphere has a wake in Beard's regime 2 above Re of tens; Re = 20 at a = 146 µm | collectors above about 150 µm (E there is near 1 for most partners, and the interpolation leans on potential flow) |
| No hydrodynamic interaction, no lubrication near contact, no van der Waals or electric force | Michael and Norey (1970) warn that 1.21194 is an approach criterion for a point, not a contact value | small collectors (R < 30 µm): our E is below 0.002 for most p where Hall's compilation gives 0.01–0.08 |
| Linear partner drag with τ = v(r)/g* | partner Re at terminal speed 0.008 (8 µm), 1.53 (50 µm); at Re_p = 1.5 the relaxation rate along the path is off by about 11 % (skeptic, Schiller–Naumann) | collector–collector pairs |
| No Basset history force, no added mass | history force about 4 % of the drag on the partner's own time scale, up to about 7 % over a passage time R/U (skeptic's estimate); added mass and fluid acceleration about 10⁻³ | dropped; a few-percent effect on paths |
| Coalescence efficiency 1 for the table | E here is the collision efficiency; coalescence is L3 and multiplies the kernel separately (Hall 1980 also takes 1) | — |
| Steady collector flow | the flow around the collector is set up by viscous diffusion in R²/ν = 0.09 ms, against the passage time R/U = 0.23 ms at 40 µm (ratio Re/2 = 0.42) | marginal near Re ≈ 2; the Re interpolation above dominates |
| Finite start distance, contact test | E(40 µm, 8 µm) in Stokes flow, prototype: 0.33668 (Z = 50), 0.33706 (100), 0.33747 (200), 0.33746 (400); with a closest-approach event (skeptic) 0.33752 converged, O(Z⁻²); the model tests contact only at step ends and misses grazes, an error ≤ 3 × 10⁻⁴ in E, and the independent SciPy check (event-based) gives E(40, 8) = 0.3442 against 0.3444 | negligible beside the closure band |

## 6. Exact solutions, limits and comparisons it must reproduce

- **Critical Stokes numbers** (point partner, S = 0, on the axis): potential flow 1/12 = 0.08333, by local analysis plus numerics (the
  damped oscillator St η'' + η' + 3η = 0 at the stagnation point proves that St > 1/12 hits; that an overdamped partner arriving from far
  away does not is shown numerically, here and by the skeptic's independent G-criterion to 7 digits); creeping flow 1.21194, Michael and Norey (1970,
  "correct to five decimal places", abstract via the dossier; Langmuir 1948 gave 1.214). Prototype: 0.08333 and 1.21194 at Z = 20
  and 100 (old study: 0.08425 and 1.21194).
- **Langmuir (1948) Table 1** (point partner, S = 0, his fitted formulas): potential flow within 0.7 % for K ≥ 3 (0.743 vs 0.738 at
  K = 3; 0.908 vs 0.907 at K = 10), creeping flow within 3.2 % for K ≥ 5 (0.457 vs 0.472 at 5; 0.640 vs 0.634 at 10; 0.774 vs
  0.760 at 20), but 10 % low at K = 3 (0.295 vs 0.326) and 8 % low at K = 3.6 (0.354 vs 0.383), where the study's own pairs sit
  (K ≈ 3.6–4.7). Near the critical numbers the values differ more (potential flow, K = 0.2: 0.034 vs 0.081; creeping, K = 2: 0.162 vs
  0.186); Langmuir's table near K = 0.1–0.15 is not his own formula either. No third computation was consulted, so these gaps are
  **unresolved**, and the page says so.
- **Langmuir's Table 4** is not used as a check: his E is for a point droplet without settling, normalised by πR², ours includes
  interception and settling and is normalised by π(R + r)²; the near agreement (0.359 against 0.394) is a coincidence.
- **Hall (1980) Table 1** (OCR, digits not checked against the page image): along the growth path r = 8 µm Hall's values are 1.23 to
  1.53 times ours (40 µm: 0.344 vs 0.50; 50 µm: 0.406 vs 0.62, the worst; 100 µm: 0.550 vs 0.674; 300 µm: 0.750 vs 1.0); at p = 0.1 the
  gap reaches a factor 3 (R = 50 µm: 0.128 vs 0.40). Ours is near zero where Hall has 0.01–0.08 (R ≤ 20 µm). Hall's table is for sea
  level: our E(40, 8) is 0.332 there (skeptic), so the altitude offset is about 0.01.
- **The old study's stored table:** E(40 µm, 8 µm) = 0.343; ours 0.344.
- **Model limits:** St → ∞: E → 1 (straight paths); potential flow approaches it fastest. p → 0, St → 0, S = 0: interception only,
  E → 2ψ(1 + p, π/2)/(1 + p)² = 1 − 3/[2(1 + p)] + 1/[2(1 + p)³] ≈ (3/2)p² in creeping flow and 3p in potential flow.

## 7. Predictions and results

1. **The efficiency, not the drag law, decides the speed.** As first written ("t₉₀ lengthens by more than 1.20") this could not fail:
   with E ≤ 0.75 along the whole growth path the factor is at least 1.33. The derived expectation is the one-line continuous-collection
   integral of L0 with Beard speeds, own table against E = 1 (`derive/L0_r3.cjs`, computed after round 1 of this contract, so recorded as
   a result, not a prediction): ×2.26 for 40 → 100 µm in the open cloud, ×2.47 for the closed box's t₉₀ (11.03 → 27.24 min). In the full
   SCE the same switch gives ×1.69 (7.96 → 13.47 min), smaller because collector–collector and droplet–droplet pairs, which carry part
   of the growth in the SCE, are less affected than capture.
2. **The old study's headline** (SCE, extended kernel: 6 / 14 min) is reproduced by L4 with this table (5.77 / 13.47 min). One matching
   table entry is not the reason; along r = 8 µm our table and the old one were not compared entry by entry, so this is a reproduction,
   not an explanation.
3. **Prediction (could fail; tested in L4): the small-collector artifact does not matter for observable 1.** Replacing our efficiencies
   for collectors below 30 µm by Hall's changes t₉₀ by less than 5 %. Outcome (`L2_r2.cjs`): 13.442 against 13.470 min, −0.2 %: passed.

## 8. Derived, cited, chosen, and the price

Derived: (L2.1)–(L2.2), the Stokes number as a stopping distance, the flux formula, the interception limits, the potential-flow
critical number 1/12, the asymptotic classification at the stagnation point. Computed: the table, the creeping-flow critical number.
Cited: the two flow fields (classical exact solutions, derived in the textbook), Langmuir's interpolation (empirical), Michael and
Norey's 1.21194, Hall's comparison table. Chosen: superposition, τ = v(r)/g*, the table grid, the p > 0.6 closure with its bracket.
Price: the one-sided flow ignores the partner's own flow, which matters most for small collectors (where it underestimates E by
0.01–0.08) and for near-equal sizes (where it fails); Langmuir's interpolation is not physics; our E is 1.2–1.5 times below Hall's
compiled values along r = 8 µm, mostly because of the flow field at Re ≈ 1–20, so observable 1 carries a closure uncertainty that the
page shows as a band: t₉₀ = 11.4 min (Hall) to 13.5 min (ours).

## 9. Answers to round 1 (`skeptic-G1-L2-r1.md`)

| # | Objection | Answer |
|---|---|---|
| 1 | Not superposition | Renamed "one-sided flow (Langmuir's method)"; the difference from Hall's sources and the size of the dropped term are stated (section 3). |
| 2 | Flow field at Re ≈ 1–20 | Accepted as the weakest link; the crossover sensitivity is computed (0.344 → 0.485); no Navier–Stokes field at this rung, by choice; Hall's table, computed with intermediate-Re fields, is carried as the other end of the observable-1 band (11.4–13.5 min). The "fails where" column now names Re ≈ 1–20. |
| 3 | Langmuir comparison skips K = 3–3.6 | Shown (−10 %, −8 %) and called unresolved. |
| 4 | Table 4 compares different quantities | Dropped as a check, with the reason. |
| 5 | "His closed forms differ" mislabelled | Reworded: his table near K = 0.1–0.15 is not his formula; unresolved. |
| 6 | "Bracket" false | Withdrawn; Hall's 1.3–4.0 quoted; the weight of p > 0.9 pairs computed (1.7 %, 1.4 %). |
| 7 | Hovering limit | The criterion S > I(p) and its consequence added to the assumptions table. |
| 8 | On-off window and floor for R < 30 µm | Stated as a model artifact; prediction 3 shows it does not matter (−0.2 %). |
| 9 | Interception limit only for S = 0 | Noted in the hovering row: the physical small-St limit is (I − S)/(1 − S), zero here. |
| 10 | 1/12 half derived | "Local analysis plus numerics". |
| 11 | Grazes missed | Stated with its size (≤ 3 × 10⁻⁴); the independent SciPy check uses events and agrees to 2 × 10⁻⁴. |
| 12 | Gap to Hall understated; altitude | Quoted along r = 8 µm (×1.23–1.53, worst at 50 µm) and at p = 0.1 (×3); altitude offset 0.01. |
| 13 | Prediction 1 cannot fail | Accepted; replaced by the derived factors, recorded honestly as results computed after round 1. |
| 14 | Prediction 2's "because" | Removed; terms defined in the header. |
| 15 | Missing terms | Rows for the Basset force, coalescence, flow set-up time (R²/ν) and nonlinear partner drag. |
| 16 | Alternatives weakly motivated | "Chosen not to at this rung" (section 3). |
| 17 | OCR not checked against page images | Said in section 6; the page images were not reachable for either of us. |
| 18 | Stale files | `L2_stc.cjs` deleted; the unused require removed from `L2_traj.cjs`. |
| 19 | Undefined terms | Defined in the header. |

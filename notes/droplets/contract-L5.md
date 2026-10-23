# Contract L5: the stochastic process itself

Gate 1. Sources: `dossier-stochastic.md` (Telford 1955, Gillespie 1972 and 1975 read whole by the scout from page images;
Kostinski and Shaw 2005, Shima et al. 2009 preprint, Alfonso et al. 2008/2015/2017, Dziekan and Pawlowska 2017, Wilkinson 2016 arXiv
read). Code: `portfolios-src/droplets/physics.cjs` (`gillespieRun`, `drawModes`, `tableMax`); quick engine test
`tools/test_gillespie.cjs`; SCE tail resolution `tools/tail_resolution.cjs`.

## 1. Question and observables

Rain begins with the luckiest drops, not the average one. How long until the first drop of radius 100 µm (and of 1 mm) appears in a
stated volume of cloud, how widely does that time scatter from one volume to the next, and when does the mean-field SCE of L4 stop
describing the cloud? Observables:
- **Observable 2**: T₁₀₀(V) and T₁ₘₘ(V), the times at which the first drop of r ≥ 100 µm (r ≥ 1 mm) appears in a well-mixed volume V,
  as distributions over ensembles of runs (mean, standard error, quantiles, seeds), for V = 1, 10, 100 and 1000 cm³; T₁ₘₘ in 1 m³ only through the Poisson bridge (section 3).
- **Observable 1 in finite volumes**: the ensemble mean of F₄₀(t) against the SCE, as a function of V.

## 2. Picture and formal mechanism

Picture: two identical collectors start side by side. One happens to meet a droplet early, grows a little, falls a little faster and
meets the next droplet sooner; the other waits. Like compound interest started a few days apart, the early lead never closes. Among
a million collectors, a few have such luck several times over, or meet another large drop, and they are the first drizzle.

Mechanism: in a well-mixed volume V each pair (i, j) merges in the next dt with probability K(r_i, r_j) dt/V, independently of the
past (a Markov jump process). The probability of the whole list of drop counts obeys a master equation (Gillespie 1972; Alfonso et
al. 2008, eq. 2). Its mean obeys the SCE only if ⟨n_i n_j⟩ = ⟨n_i⟩⟨n_j⟩, which holds as V → ∞ (Gillespie 1972). The first-drop time
is a property of single realisations and of the extreme tail, which the mean describes only through a further assumption (section 3).

## 3. Model

- **Exact sampling** (Gillespie 1975, his method B, generalised to classes): drops are grouped in size classes (4 per doubling of
  radius, 0.5 µm–8 mm); each class pair (a, b) has a majorant K*_ab ≥ K(r_i, r_j) for every i in a, j in b (from the extreme radii and
  speeds of the classes, and the efficiency table's maximum over the class pair, which is exact because the table is piecewise
  bilinear in ln R, ln p; the bound is checked at every proposal and any violation stops the run). Proposals arrive as a Poisson
  process of rate A* = Σ_{a<b} K*_ab n_a n_b/V + Σ_a K*_aa n_a²/(2V); a class pair is chosen in proportion to its share, two members at
  random, and the pair is accepted with probability K/K*. By thinning (Lewis and Shedler's construction; Gillespie 1975's rejection
  method), the accepted events form exactly the coalescence process of the master equation. Derivation of the same-class rate in the
  textbook.
- **Kernel**: the extended kernel (L1–L3: Beard speeds, this study's efficiency table, the coalescence law), and the near-equal bracket
  (E = 1 above r/R = 0.6 for collectors ≥ 40 µm, L2).
- **Initial drops**: fixed numbers N_d = 300 V and N_c = V (V in cm³), radii drawn independently from the lognormal modes. The modes
  are **truncated at 3σ_g** (no droplet above 15.6 µm or collector above 69.1 µm at t = 0) for observable 2, because the untruncated
  lognormal tail already holds 0.23 drops of r ≥ 100 µm and 82 drops ≥ 80 µm per m³ at t = 0 (computed on the SCE grid): in a large
  volume the first drizzle would then be decided by the initial tail, which comes from aerosol and condensation physics outside this
  study. Untruncated runs are shown beside them so the reader sees the effect. Fixed counts rather than Poisson-distributed counts: a
  stated choice; it removes the fluctuation of positions (Gillespie 1972's type ii) and keeps that of the process.
- **Ensembles**: 200 runs at 1 cm³, 100 at 10 cm³, 100 at 100 cm³, 30 at 1000 cm³ (scope kept to a lecture note); seeds 1000·V + run number; results
  reported as means with standard errors, quantiles and empirical distributions.
- **The large-volume limit.** In a volume V much larger than the volume in which one large drop forms, the number of drops ≥ 100 µm
  at time t is close to Poisson with mean V n₁₀₀(t), where n₁₀₀ is the SCE's concentration of such drops; since a drop above 100 µm
  stays above it, P(T₁₀₀ > t) = exp[−V n₁₀₀(t)], and the median is where V n₁₀₀ = ln 2. This is the bridge from the volumes that can
  be simulated exactly to 1 m³, and it is tested (prediction 7.2).

## 4. Rejected alternatives

1. **Super-droplets with multiplicities above 1** (Shima et al. 2009): right for the mean, but they inflate fluctuations unless the
   number of super-droplets is at least a ninth of the real drops (Dziekan and Pawlowska 2017), so they cannot answer a question about
   the first drop more cheaply than exact sampling.
2. **The master equation solved directly** (Alfonso 2015): exact, but limited to about 50 drops by the number of states.
3. **Telford's or Kostinski and Shaw's single collector**: exact for one collector in an unchanging sea of identical droplets, but
   without depletion, without a size spread and without collector–collector mergers, which section 5 shows are the route to 100 µm
   here. Kept as a limit and a check (section 6).

## 5. Assumptions and their numbers

| Assumption | Number | Fails where |
|---|---|---|
| Well-mixed volume V | a collector at 0.18–0.35 m/s crosses 1 cm in 0.03–0.06 s and 10 cm (1 L) in 0.3–0.6 s, while its next capture takes about 8 s (L0); turbulent mixing over 10 cm takes of order (0.1 m)^{2/3} ε^{−1/3} = 1.0 s at ε = 10⁻² m²/s³ | volumes above about a litre are well mixed only on minute time scales; Dziekan and Pawlowska estimate the strictly well-mixed volume at 1.5 × 10⁻² cm³ (their setting); the page states the well-mixed box as an idealisation |
| No sedimentation out of V, no condensation | closed box, as L0–L4 | real clouds |
| Fixed counts, independent radii | positional fluctuations excluded (above) | a real cloud's volumes differ in count by √N |
| Truncation at 3σ_g | removes 0.27 % of each mode's number and the tail that would otherwise decide T₁₀₀ in large V | shown against untruncated runs |
| The extended kernel's near-equal closure | E held at its r/R = 0.6 value; bracket E = 1 | collector–collector mergers: the bracket is computed |

## 6. Exact results and checks it must reproduce

- **One collector among identical droplets** (no droplet–droplet events because equal drops fall at equal speeds): the exact process
  is a pure birth chain with rates λ_n = K(R_n, r)(N − n)/V; the time to the n-th capture is a sum of independent exponentials. The
  ensemble mean and variance of that time must match Σ 1/λ_k and Σ 1/λ_k² within sampling error. This tests the engine's class
  choice and thinning exactly.
- **Majorant**: zero violations in every run; acceptance ratio reported.
- **Mass**: every run conserves Σ r³ to rounding.
- **Large V**: the ensemble mean of F₄₀(t) approaches the SCE as V grows (Gillespie 1972).
- **SCE tail resolution**: the SCE's V n₁₀₀(t) = ln 2 times converge with grid resolution (1 m³: 55 s at s = 8, 60 s at s = 16; 1 L:
  170 and 175 s; 100 cm³: 280 and 280 s; truncated modes).

## 7. Predictions that could come out wrong

1. **The gap.** The first 100 µm drop in 1 m³ appears about ten times earlier than the mean-field time, defined as the time at which
   half the water sits in drops ≥ 100 µm (590 s in the SCE, truncated modes). The factor ten is Kostinski and Shaw's luck factor for the
   fastest 10⁻⁶ of collectors (0.087–0.1 of the mean time; 10⁶ collectors per m³). If the exact process, through the tested Poisson
   bridge, shows no such gap, the luck argument does not apply to a cloud whose collectors are already large, and the reason must be
   found before going on.
2. **The Poisson bridge.** For truncated modes at V = 100 and 1000 cm³, the fraction of runs without a 100 µm drop by time t matches
   exp[−V n₁₀₀^SCE(t)] (Kolmogorov–Smirnov at the 5 % level). If it fails, correlations (depletion around a lucky drop, the finite
   number of large collectors) matter, and the 1 m³ value cannot be taken from the SCE.
3. **The route to 100 µm.** In at least 90 % of the runs at V ≥ 100 cm³, the first drop ≥ 100 µm has merged with at least one partner
   of radius ≥ 30 µm (a collector–collector merger), not grown by droplet capture alone.
4. **Small volumes.** For V ≤ 10 cm³ the ensemble-mean F₄₀ lags the SCE (as Dziekan and Pawlowska found for small cells: depletion and
   correlations slow growth); for V ≥ 1000 cm³ it agrees within two standard errors at every minute. A quick engine test (4–40 runs,
   untruncated) already showed a lag at 1 cm³ (0.505 against 0.752 at 10 min) and agreement at 100 cm³; the full ensembles set the
   numbers.

## 8. Derived, cited, chosen, and the price

Derived: the thinning construction with class majorants (and its exactness), the same-class rate, the Poisson bridge and its median,
the birth-chain check. Cited: the master equation and the SCE's assumptions (Gillespie 1972), the rejection method (Gillespie 1975),
the luck factor (Kostinski and Shaw 2005), the small-cell findings (Dziekan and Pawlowska 2017). Chosen: the volumes, the ensemble
sizes, the 3σ_g truncation, fixed counts, four classes per doubling of radius. Price: a well-mixed box larger than about a litre is an
idealisation; 1 m³ is reached only through the Poisson bridge, so its first-drop time is as good as the SCE's tail and the bridge's
test at 1000 cm³; and the near-equal efficiency, which drives collector–collector mergers, is the least known closure of the study.

## 9. Outcomes (computed after this contract; `tools/run_stochastic.cjs`, `tools/run_bridge.cjs`, `checks/check_physics.py`)

The contract file is dated 12:26, the stored ensembles 12:28–12:36 (23 Oct).

1. The gap: in 1 m³ the first 100 µm drop appears after about 60 s (bridge, s = 16); half the water is above 100 µm after 585 s:
   a factor of about 10: **passed** (but known before the contract; see §10.1).
2. Poisson bridge against exact runs (Kolmogorov–Smirnov): 1000 cm³, 30 runs, D = 0.156, p = 0.42; 100 cm³, 100 runs, D = 0.088,
   p = 0.40: **passed** at the 5 % level. Medians 175 s and 286 s against the bridge's 175 s and 280 s.
3. The route: 230 of 230 first drops ≥ 100 µm had merged with a partner ≥ 30 µm: **passed**.
4. Small volumes: F₄₀ at 10 min 0.520 ± 0.019 (1 cm³), 0.696 ± 0.009 (10), 0.730 ± 0.004 (100), 0.740 ± 0.002 (1000); the SCE with
   truncated modes gives 0.742 at 10 min: the lag at ≤ 10 cm³ **holds** (and is still 0.012 at 100 cm³, 7 standard errors at 20 min).
   At 1000 cm³ the ensemble agrees with the truncated SCE (s = 16) within 1.3 standard errors at every odd minute to 21 min (F₄₀ = 0.99);
   after that the runs exceed the SCE by 1–2 × 10⁻⁴, statistically significant (z up to 5) but invisible on the page; cause not
   investigated: **failed** as written after 22 min (see §10.4).
5. Engine test (added): one collector and 20 identical droplets, against the exact death chain, 4000 runs: mean 8.246 ± 0.036 against
   8.221, χ² p = 0.15: **passed**. Zero majorant violations in all 430 ensemble runs.

## 10. Answers to round 1 (`skeptic-G1-L4L5-r1.md`, L5: PASS with fixes)

| # | Answer |
|---|---|
| 1 | Accepted: the gap was computed before this contract, so it is a result, not a prediction. The open prediction was the Poisson bridge (2), which could have failed and did not at 100 and 1000 cm³. |
| 2 | Accepted, and it changes the teaching: the luck here is meeting another collector early, not lucky captures. Capture alone takes the largest starting collector (69 µm) to 100 µm in 560 s with 1312 captures, and its count varies by a few per cent. Chapter 6's picture and its paragraph on Telford, Kostinski and Shaw are rewritten. |
| 3 | Accepted and measured: 55 / 57 / 61 s at s = 8 / 16 / 32 (`derive/L5_tail.cjs`, 1 s records; the skeptic's 65 s used coarser records). 1000 cm³: 170 / 173 / 179 s against 175 s exact; 100 cm³: 278 / 279 / 284 s against 286 s exact. The page says "about a minute" and gives the three values. The gap is about nine to eleven. |
| 4 | Accepted: prediction 4 as written **failed** after 22 min at 1000 cm³ (the runs exceed the SCE by 1–2 × 10⁻⁴ in F₄₀, z up to 6–10). Cause not found. It is invisible on the page, and the page quotes nothing after 20 min from the comparison. |
| 5 | Added to chapter 6: 1 cm³ cannot make a 100 µm drop (it needs the water of 3.75 cm³); in 10 cm³ every run made one (median 605 s) while (6.1) allows at most 32 % of volumes, because in a small volume the first merged drop sweeps up the rest: (6.1) needs rare and independent large drops. The 1 mm time in 1 m³ (about 18 min) is labelled untested (a 1 mm drop needs 3.75 L of cloud). |
| 6 | 130 of 130 at V ≥ 100 cm³, and 100 of 100 at 10 cm³. |
| 7 | The bound is checked at every proposal; the code stops after more than 10 violations; zero occurred. |
| 8 | The test run is the stronger one: the full capture-count distribution against the matrix exponential (χ², p = 0.15). Same-class pairs with K > 0 are exercised by every ensemble run (0 violations in 430). |
| 9 | Acceptance 0.50 / 0.55 / 0.59 / 0.59 at 1 / 10 / 100 / 1000 cm³; chapter 6 says "50 to 59 %". |
| 10 | Mixing time about 5 s at 1 m against a first-drop time of about 60 s: the well-mixed cubic metre is an idealisation by a factor of about ten in time. |
| 11 | "Moves 0.27 % of each mode's drops from its tails into its body." |
| 12 | Continuous lognormal: 0.25 per m³ (chapter 6 now says 0.25). |
| 13 | Adopted in chapter 6: one collector in 1 cm³ cannot meet another; n(n − 1)/2 = 0 where the SCE uses n²/2. |
| 14 | With 30 runs the 5 % KS critical distance is 0.25, so the test excludes only large differences; the medians are the sharper evidence. |
| 15 | Noted. |

# Droplet Collection: status

Branch `claude/affectionate-maxwell-8ys77u`. Read this first every turn. `/goal` is a slash command only Numa can type; this session
runs on the fallback of physics-model-loop 1.1 (never end a turn with an actionable item; `send_later` if a turn must end with work left).

## The Fermi estimate (written before any model, 23 October 2026)

Air at 10 °C and 850 hPa: ρ_a = 1.0458 kg/m³ (ideal gas), μ = 1.771 × 10⁻⁵ Pa s (Sutherland), ν = 1.69 × 10⁻⁵ m²/s.
Stokes speed v = kR² with k = 2(ρ_w − ρ_a)g/(9μ) = 1.23 × 10⁸ m⁻¹ s⁻¹: 0.79 cm/s at 8 µm, 19.7 cm/s at 40 µm (Re = 0.93),
1.23 m/s at 100 µm (Re = 15). Stokes' own Reynolds number reaches 1 at R = 41.0 µm.

The thesis cloud, taken monodisperse: 300 cm⁻³ droplets of 8 µm hold 0.643 g/m³; 1 cm⁻³ collectors of 40 µm hold 0.268 g/m³
(29 % of the water). One collector is worth 125 droplets.

**Observable 1 (mean-field times to 50 / 90 % of the mass in r ≥ 40 µm).** The collectors sweep π R² v = 9.9 × 10⁻¹⁰ m³/s each; with
10⁶ of them per m³ the droplet water is cleared on an e-folding time of 17 min at fixed collector size and E = 1. Getting from 29 % to
50 % needs about 6 min (E = 1, Stokes), 17 min with E = 0.34 (an efficiency typical of 40 µm on 8 µm). Collector growth speeds this up
and the size spread of real modes moves half the collector mass across 40 µm at once, so expect t₅₀ of a few minutes (E = 1) to
about 10 min (E ≈ 0.3), and t₉₀ two to five times longer. The old study's 3 / 5 min (thesis kernel) and 6 / 14 min (extended kernel)
are inside this range.

**Observable 2 (first large drops).** Generic estimate: one collector in 0.3 g/m³ of droplets, E = 1, Stokes speed, no depletion,
dR/dt = kR²W/(4ρ_w), grows from 40 to 100 µm in 27 min (12.6 min in 0.64 g/m³) and its radius would blow up at 45 min (21 min):
that blow-up is the Stokes law's R² speed, stopped in reality by the drag law, depletion and E < 1.
In the thesis cloud each collector has only 300 droplets to share: if all collectors were identical, collecting all of them takes
each to 60 µm, and a 100 µm drop needs 1828 droplets. **Correction (skeptic-G1-L0-r1, objection 1, confirmed by my own runs):** I first
wrote that every drop above 60 µm must therefore come from collector–collector mergers. That is false. Collectors share one sweep
integral, so a collector that starts larger ends far larger (R(∞) = 1/(1/R₀ − Φ): 78 µm → 164 µm in the lognormal mode), and the
Poisson spread of captures alone puts 12 % of collector mass above 60 µm by t₉₀. The first 100 µm drops come from the large tail of
the collector mode, from luck in captures, and from collector–collector mergers; L4 and L5 must say which dominates.
A 1 mm drop holds 4.19 mg, the water of 4.6 L of this cloud.

**Observable 3 (ice).** No estimate yet; set from the dossier on measured splinter yields before L7.

Thermal noise: surface energy of a 10 µm drop 9.0 × 10⁻¹¹ J = 2.3 × 10¹⁰ kT: irrelevant. Kolmogorov time at ε = 10⁻² m²/s³ and this
ν: 41 ms; τ_p(10 µm) = 1.26 ms; Stokes number 0.030 (0.010 to 0.096 for ε = 10⁻³ to 10⁻¹).

## Queue (first open item is next)

1. [x] Gate 1: L0 PASS (r3), L1 PASS (r3), L2 PASS (r3), L3/L6/L7 PASS (fixes check), L4/L5 PASS (fixes check).
2. [x] Gate 2: `check-L0.md` … `check-L7.md`: all 24 numbered equations right by SymPy and Wolfram (+ SciPy); (4.2)'s 1.15 and
       (8.2)'s coefficients are fits, checked as transcriptions. Scripts in `gate2/`.
3. [~] Gate 3: round 1 failed honest/sourced/readable (32 objections, `skeptic-G3-r1.md`); all answered (`gate3-answers-r1.md`);
       round 2 running.
4. [ ] Remove the old app bundle `static/` (keep old `fig/` for the i18n pages) once Gate 3 passes.
5. [ ] Open the PR into main (NOT merged).

## Done, with evidence

- 23 Oct (after resume): `checks/check_numbers.cjs` 148/148 PASS; `checks/check_physics.py` 12/12 PASS; `checks/check_browser.py`
  PASS at 360/390/1024/1440 px; `python3 tools/inventory.py --check` OK; `npm run build` OK (root package-lock removed).
- Ice law corrected against Sotiropoulou et al. 2021 App. B (read): breakup 3.0e-4 to 1.6e-3 cm⁻³ min⁻¹ (clamped D), 0.050 (true D);
  old rule 2.6, so 1600× and 52× less. Shattering bracket from Korolev and Leisner Table 1 (read): 0–1.7 fragments per freezing drop.
- Efficiency band (L2 round 2, reproduced): t₉₀ = 13.47 / 12.60 / 11.48 / 10.49 min at crossover 60 / 20 / 6 / 2; Hall 11.38; E = 1
  below 30 µm: 12.68 (`derive/L2_cross.cjs`). Resolution (`derive/L4_conv.cjs`): s = 4/8/16 → 13.35/13.47/13.53; Δt → 0.005 min.
  Tail (`derive/L5_tail.cjs`): 1 m³ first-drop median 55/57/61 s at s = 8/16/32.
- Chapters 3, 4, 5, 6, 7, 8, 9, problems and checks corrected to computed values and rewritten where the physics lesson changed
  (luck = collector meets collector; 10 cm³ bridge failure; 1 cm³ one-collector argument; turbulence a lower bound).
- Portfolios article rewritten (four plates from the build, links #book/#sim/#checks/#fig-…); `docs/portfolios.md`, `docs/pages.md`,
  `portfolios-src/droplets/README.md`, `tools/inventory.py` rules, `docs/files.md` regenerated.

- `done.md` written (23 Oct). Fermi estimate above.
- Dossiers: `dossier-fallspeed-efficiency.md`, `dossier-stochastic.md`, `dossier-coalescence-turbulence.md`, `dossier-ice.md`.
- L0 derivations: SymPy (`derive/L0_sympy.py`), Wolfram (`derive/L0_wolfram.md`); numbers reproduced by the skeptic to every digit.
- Beard's b₆ = −3.27815 × 10⁻⁶ confirmed in disdrodb `fall_velocity/rain.py` (lead, 23 Oct).
- Old headline reproduced: Gunn–Kinzer largest error 2.07 % from 0.3 mm (`derive/L1_beard.py`); continuous GCE thesis kernel 3/7 min and
  F₄₀(0) = 0.2009 (`derive/L0_population.py`); critical Stokes numbers 0.08333 and 1.21194 (`derive/L2_traj.cjs`).

- Model code drafted in `portfolios-src/droplets/physics.cjs` for L0–L4 (awaiting Gate 1 verdicts for L1–L4):
  Beard speeds, trajectory efficiencies, coalescence law, kernel, SCE (two-bin, limiter, overflow), GCE, Golovin exact.
- `data/etab_warm.json`: 64 × 40 efficiency table, own generator (`tools/gen_tables.cjs`, 130 s).
- Golovin (`tools/run_golovin.cjs`): ε = 0.4279 / 0.1504 / 0.0511 / 0.0182 at s = 2/4/8/16, observed order 1.51, 1.56, 1.49;
  mass error −4.58 × 10⁻⁷ = initial truncation below 1 µm; scheme drift 1.8 × 10⁻¹³; number error −0.0018 (old values reproduced digit for digit).
- Warm cloud (`tools/run_warm.cjs`, s = 8, Δt = 1 s, 4 mm grid): SCE thesis 3/5 min, GCE thesis 3/7, SCE extended 6/14, GCE extended 7/19:
  all four old headlines reproduced; mass drift ≤ 3.4 × 10⁻¹³; limiter fixes 0.

- L5 ensembles (`tools/run_stochastic.cjs --json` → `data/stochastic.json`, truncated modes, seeds 1000·V + k, 0 majorant violations):
  F₄₀ at 10 min 0.520 ± 0.019 (1 cm³, 200 runs), 0.696 ± 0.009 (10, 100), 0.730 ± 0.004 (100, 100), 0.740 ± 0.002 (1000, 30);
  first r ≥ 100 µm: never in 1 cm³; median 605 s (10 cm³), 286 s (100 cm³), 175 s (1000 cm³); SCE Poisson bridge predicted 280 and 175 s;
  route: 230/230 first drops merged with a partner ≥ 30 µm. SCE: half the water above 100 µm at 590 s; 1 m³ bridge median 60 s.

- Interpolated SCE times (records every 5 s, s = 8, Δt = 1 s, untruncated modes): t₅₀/t₉₀ min: thesis 2.272/4.512; thesis kernel with Beard
  speeds 2.886/7.963; extended 5.767/13.470; coalescence = 1: 5.766/13.435; Hall efficiencies 4.570/11.382; near-equal E = 1 5.679/13.311;
  turbulence (Ayala, within its range) 100 cm²/s³ 5.513/13.242, 400 cm²/s³ 5.523/13.327.
  Predictions: L0 8.1 PASS (2.27 within ±0.5 of 2.50; 4.51 < 6.85). L1 §7 FAILED: Stokes→Beard ratio in the SCE 1.765, outside the box
  bound [1.117, 1.262] — speed differences between similar drops (collector–collector, droplet–droplet, E = 1) respond more strongly than
  capture; goes into the text. L2 1 PASS (×1.69 > 1.20), L2 2 PASS (6/14). L3 1 FAILED narrowly (t₉₀ changes 0.26 %, predicted < 0.1 %;
  still far below the closure band). L6: −1.7 % at 100 cm²/s³ → stated check (X = 10 % from Ayala's +5.6 %).

## Handoff notes

Nothing is running. Resume list, in order:
1. L0 Gate 1: round-3 fixes written (contract §12); skeptic was re-checking them when stopped (resume it or a fresh short check).
2. L2 Gate 1: contract round 2 written (§9 answers all 19 objections; `derive/L2_r2.cjs`); send to skeptic round 2.
3. L3/L6/L7: skeptic round 1 = PASS with fixes (`skeptic-G1-L3L6L7-r1.md`); apply the fixes, incl. the Phillips asperity term
   A = 1 + 0.0079/D^1.5 (D in m, clamped 0.5–5 mm) in `tools/run_cold.cjs`, collision energies 10⁻¹⁴–10⁻¹³ J, Hallett–Mossop wording,
   shattering geometry and bracket, the L6 lower-bound wording; rerun `run_cold.cjs --json`, update chapter 8 text.
4. L4, L5 contracts to a skeptic. 5. Gate 2 check files `check-L<k>.md`. 6. `checks/check_numbers.cjs`. 7. Gate 3 skeptic on the
   rendered pages. 8. README, Portfolios article, docs, inventory. 9. commit, push, PR (not merged).

Done since the last update: browser check PASS at 360/390/1024/1440 px (book-05 lognormal formula made a display equation);
`checks/check_physics.py` 12/12 PASS (incl. NumPy re-solve of the SCE 5.774/13.483 against 5.767/13.470, Gillespie against the exact
capture chain p = 0.15, Poisson bridge KS p = 0.42); L2 prediction 3 PASS (Hall below 30 µm: t₉₀ −0.2 %); `physics.cjs` kernel option
`hallBelow`; `derive/L2_stc.cjs` deleted. Nothing committed yet.

## For the i18n session (not this study's files)

- `public/de/portfolios.html` and `public/ar/portfolios.html` still show the old Droplet Collection article and its old `fig/` plates.
  After this branch merges, the English article's pieces need German and Arabic translations and `python3 tools/i18n/build.py`;
  then the old `public/portfolios/droplet-collection/fig/*.svg` (all but `plate-*.svg`) can go.

## Decisions for Numa

- Numa, 23 Oct (mid-run): "We are not writing a paper, we are writing a lecture note. Be careful how wacky or far you go; as long as
  it is readable and understandable, I am fine." Applied: L5 to four volumes (1, 10, 100, 1000 cm³), no 10 L or stochastic 1 mm runs;
  L6 one computed number and a stated check; L7 a short table of measured channels at −10 °C; skeptics judge as a student reader
  (correct and followable), sourcing nitpicks minor; text as lecture notes (picture, model, maths), no literature survey.
- Default (stated on the page): observable 2 uses lognormal modes truncated at 3σ_g; untruncated shown beside it.

## Provisional choices

(none yet)

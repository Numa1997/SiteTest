# Fig. 11 · status and handoff (4 November 2026, evening)

## Done this evening (branch `fig11-sampled`, PR into main)

- Browser tests rerun on the sampled-gain version (raw outputs in `study/runs-2026-11-04/`): 40/40 random, rolling and stopping; 8 machines × 6,
  48/48 rolling and 48/48 stopping; continuous gains at 40 ms 0/6, c* = 0; `t7.cjs` en/de/ar at 1280/390: 0 errors, 0 KaTeX errors, 0 pending.
- Lecture note: §7.2–7.5 with (16a)–(16h) and Table 1; §8 "The loop period" recomputed (`study/sec8b.js`: continuous gains rest to 34 ms,
  designed to 260 ms; doubled 58/342.5 ms, halved 19/195 ms); §9 rewritten with (19a) and the argument for maps; §11.2 (23) with Δ; §11.3 new
  tests; §11.4 "Arriving moving" with (25), (26) and the measured glide lean (`study/glide.js`); problems 12.5, 12.6; sources [9] Van Loan
  (report PDF read from eCommons, bitstream of TR 77-298), [10] Guo et al. (eq. (3), (4) read), [11] Wolfram documentation (read).
- Walkthrough 15 steps (walkcheck 65/65), German and Arabic (build.py --check clean), docs (fig11 doc, walk.md, inventory).

## Still to do

- Request 4, the swap (separate branch): this simulation to Projects, "Double Pendulum under Control" back to Simulations as Fig. 11, with DE/AR.

---

## Earlier handoff (4 November 2026, 09:00)

Page: `public/simulations/double-inverted-pendulum.html` (double inverted pendulum on a cart). Live version: PR #77 (merged, `b917f12`):
rescue after a fall (calm → planned swing-up → time-varying LQR → hand-over at W < 0.9 c*), lecture note §9–§11, walkthrough steps 10–12, DE/AR.

Work in progress is on branch **`fig11-sampled`** (pushed, NOT merged). Study scripts and their raw outputs: `notes/fig11/study/`.
Working notes with every Wolfram check of the model: `notes/fig11/checked.html`.

## Numa's requests this round (verbatim intent)

1. "Right then, if you're so sure of the solution, implement it": gains designed for the loop period T_s (discrete-time LQR) instead of the
   continuous gains used whatever the slider says.
2. "Note it??? … that's the most important part! Extensively elaborate, and work out a mathematical model for it!": the lecture note must
   carry the full sampled-data model (see "Note: to write" below), derived step by step, every term from where it comes, checked in Wolfram.
3. Moving equilibria: "a steady state where it moves at a constant velocity"; "every time you plan a trajectory where you … arrive at a
   non zero velocity …, you force yourself to decelerate later … needless velocity changes"; "from there you need a new stable point, with a
   completely new planned trajectory, in a new phase space". Implemented as: planner may arrive moving, balancer then holds the moving
   equilibrium, target buttons glide along the family of equilibria.
4. **Swap placement**: this simulation goes to **Projects**; the project **"Double Pendulum under Control"** (`public/portfolios/pendulum-control/index.html`,
   project 05, Fig. 11 until 3 Nov, see `docs/simulations/fig11-pendulum-control.md`) comes back to **Simulations as Fig. 11**. Numa: "that one is
   actually simpler". Every simulation page is EN/DE/AR, the pendulum-control page is English only (1550 lines): it needs DE/AR.
5. Numa wants to see every step: post raw test output, push each step, keep him informed in short messages.

## Done on `fig11-sampled` (code, tested, not yet in the note)

All in `public/simulations/double-inverted-pendulum.html`:

- `expm`, `sampledModel(A,B,R,T)`: exact zero-order-hold model Φ = e^{AT}, Γ = ∫₀ᵀ e^{Aτ}dτ B from one exponential of [[A,B],[0,0]]T;
  exact sampled cost Q_d, N_d, R_d of ∫(sᵀQs + ρu²)dt from exp([[−Āᵀ, Q̄],[0, Ā]]T) (Van Loan): integral = F22ᵀF12.
- `dlqr(A,B,R,T)`: discrete Riccati with cross term by the structure-preserving doubling algorithm (Guo, Chu, Liang, Lin, arXiv 2005.08288, formulas
  checked); K_d = (R_d + ΓᵀPΓ)⁻¹(ΓᵀPΦ + N_dᵀ).
  **Check:** identical to Wolfram `DiscreteLQRegulatorGains[ssm, {Q, {{1}}}, τ]` to every digit: 10 ms (5.322, −408.009, 493.663, 11.556, −13.147, 76.277),
  40 ms (2.528, −251.393, 279.000, 5.540, −10.590, 41.286); JS vs scipy 2e−13. T → 0 tends to the continuous K (0.1 ms: −502.88 vs −504.02).
- Switch **Gains designed for: The loop period | Continuous time** (`#gmode`, `gmode`), T_s slider now redesigns; readout **Largest factor per look |λ|**
  (`r-lam`, `specRad()` by repeated squaring); settling time −T_s/ln|λ|.
- Certificate for the sampled loop `catchGen()` (generator, run between frames by `think()`): largest c with W(F(s)) < W(s) for all 0 < W ≤ c,
  F = one loop period of the true equations with u = sat(−Ks) held; 1500 random directions on 4 shells, climbs from the 3 weakest linear directions
  (smallest eigenvectors of P − A_clᵀPA_cl in sphere coordinates, `jacobi()`) ± and from the worst 6; bisection 13 steps in [1, 1e4].
  Results: 1 ms 31.6 (continuous value 31.4), 10 ms 37.3 (full search 36.85), 40 ms 115.9 (full 113.8); continuous gains at 40 ms: 0. 0.2–0.35 s in Chromium.
  While computing, `cLevel = null` and the supervisor skips the W checks.
- Moving equilibria: `ref` = fixed | cruise (x₀ + v t) | glide (critically damped, ω = 0.5 s⁻¹, closed form in `refXV(t)`); `err(st,t)`, `Wof(st,t)`,
  `lqrU(st,t)`; `Wred()` (W with x and ẋ errors zero) for the hand-over when rolling. Switch **After a swing-up: Keep rolling | Stop the cart** (`#after`).
  Planner terminal speed weight `lim.vw` (0 when rolling, 0.3 when stopping). Target buttons: step when at rest, glide when moving.
- Tracking (23): stage cost now Q·Δ and ρ·Δ per 10 ms step (rectangle rule of (14)), terminal P = the balancer's P (consistent units).
- `_t('target')` on the canvas (was English in DE/AR). New `_t` strings: 'Balancing while rolling at {v} m/s, a moving equilibrium.', 'Balancing while gliding to the target.', 'target'.

**Tests run on the branch (headless Chromium, frame driver 1/60 s + 8 ms planning, `notes/fig11/study/t9.cjs`):**
T_s = 40 ms with designed gains, 6/6 random states balanced (before: 0/6). Other settings NOT yet rerun after these changes.

## Evidence (study, `notes/fig11/study/`)

- `hold.js`/`hold2.js`: 600 s hold at 10 ms: rests exactly; continuous gains at 40 ms: never rests, limit cycle ±4.9°, motor ±60 N; designed gains at 40 ms: rests exactly.
- `model.py`: ρ(Φ − ΓK_cont) crosses 1 at T_s = 34.40 ms through λ = −1 (flip, period 2T_s); designed gains stable at 120 ms (0.907). Table in `table.json`.
- One-mode model (Wolfram-checked): ż = σz + bu, u = −κz held: λ = e^{σT} − (γ/σ)(e^{σT} − 1), γ = bκ; λ < 1 ⇔ γ > σ; λ > −1 ⇔
  T < T* = (1/σ) ln((γ+σ)/(γ−σ)) = (2/σ) arcoth(γ/σ) → 2/γ as σ → 0. With σ = 10.39 s⁻¹ and the fastest closed-loop rate 42.62 s⁻¹ (γ = 53.0): T* ≈ 38 ms; full model 34.4 ms.
- Arrival experiment (`exp.js`, outputs `exp-{A,B}-{calm,raw}.txt`; A = must stop, B = free arrival speed):
  calmed starts (25): both 25/25; ∫u² 944 → 844 (−11 %), total speed change 22.1 → 19.4 m/s (−12 %), peak force same, arrival 0.3–0.5 m/s (9 hard cases ~4 m/s).
  raw random starts (40): both 15/40 plans; speed change 31.24 vs 31.23; ∫u² 1955 vs 2072. So it helps from rest-like starts only.

## To do, in order

1. Rerun browser tests on `fig11-sampled`: `t9.cjs random` (40 states) and `t9.cjs machines` (T_s 40, 60, m0 3, m1/m2 1/1.5, L 1/1.2, L 0.3/0.4, u_max 30, 120),
   both with rolling (default) and `STOP=1` (stop the cart); swing-up from hanging; flick and drag; `t7.cjs` en/de/ar at 1280/390 px. Post the raw output to Numa.
2. **Note: to write** (house style: Latin Modern, KaTeX, numbered equations; Taylor voice; every term derived; use (16a)–(16h) inside §7 so later numbers stay):
   §7.2 "A real controller samples" → subsections: the machine between two looks (16a) and one exponential (16b) with the derivation (variation of constants;
   augmented state with u̇ = 0); why the loop breaks: the one-mode model (16c)–(16d) with the shower picture, 34.4 ms through −1, the limit cycle ±4.9 °/±60 N;
   the exact sampled cost (16e)–(16f) with Van Loan's identity derived (F12 solves Ḟ12 = −ĀᵀF12 + Q̄e^{Āt}); the discrete Riccati equation (16g)–(16h) by
   completing the square on V(s) = sᵀPs, its T → 0 limit back to (15); the doubling algorithm; table of |λ| and gains vs T_s; Wolfram checks.
   §8 "The loop period" paragraph: recompute with designed gains (longest T_s held from the standard start, lengths doubled/halved).
   §9: certificate for the sampled loop, (19a) W(F(s)) < W(s), the argument for maps, the weakest-direction climbs, the numbers above.
   §11: (23) with Q·Δ, ρ·Δ; new §11.4 "Arriving moving": equations depend on ẍ not on x or ẋ (Galilean invariance) → family of equilibria (25);
   free terminal speed enlarges the terminal set; measured effect (numbers above, honestly: helps only from rest-like starts); hand-over with W_red;
   leaving by the glide (26) and lean ≈ a/g; price: the cart keeps rolling, a real rail is finite.
   Sources to cite (opened): Wolfram DiscreteLQRegulatorGains documentation; Guo–Chu–Liang–Lin arXiv 2005.08288 (SDA formulas); Van Loan 1977 report
   (only the eCommons record opened; the PDF was blocked three ways: derive the identity in the note).
3. Walkthrough `public/scripts/walk/dipc.js`: Riccati step → dlqr; new step for sampledModel; certificate step → catchGen; plan step (vw, ref). `node notes/walkcheck.cjs` must find every quote.
4. DE/AR: `python3 tools/i18n/build.py --todo de` / `ar`, translate (glossary in `docs/glossary.md`; earlier tables in `i18n/<lang>/`), `tools/i18n/ingest.py`, `build.py --check` clean.
5. Docs: `docs/simulations/fig11-double-inverted-pendulum.md`, `docs/scripts/walk.md` line links, `python3 tools/inventory.py`, `python3 tools/redirects.py`.
6. `npm run build` (delete `package-lock.json`), commit, PR into main via `gh api`, merge (Numa's standing rule: merge and publish once finished and tested), verify live
   with a sentence only the new version has.
7. Then the **swap** of request 4 (separate branch and PR): move files, catalog/Projects entries, home plate, redirects (`MOVED` in `tools/redirects.py`), docs,
   DE/AR of the pendulum-control page.

## Decisions for Numa

- None open. Defaults chosen: "Keep rolling" and "The loop period" are the defaults.

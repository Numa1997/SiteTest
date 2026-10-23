# Contract L4: the population, mean field

Gate 1. Sources: `dossier-stochastic.md` (Gillespie 1972 read whole by the scout: the SCE as the first moment of the master equation
with correlations dropped), the baseline's chapters 7–9 (checked against, not copied), Bott (1998) for the Golovin test parameters
(as used by the baseline; Bott's paper not opened here: the parameters are stated as the test's definition, not as his result).

## 1. Question and observables

When every particle may collect or be collected, how fast does the water move into large drops, and which ingredient, the kernel or
the bookkeeping, decides that speed? Observable 1: F₄₀(t), the fraction of the initial water in drops of radius r ≥ 40 µm (in-grid
particles; the overflow and any passive store are reported separately), and the first recorded minutes t₅₀, t₉₀ at which it reaches
0.5 and 0.9, for the thesis cloud: two lognormal modes, droplets 300 cm⁻³ with median radius 8 µm and geometric standard deviation
1.25, collectors 1 cm⁻³ with median 40 µm and 1.2, at 10 °C and 850 hPa (the old study's reference cloud; the thesis itself used
size ranges and normal distributions, so this is a stated replacement, not a rerun of the thesis's figures). Also: the mean-field
expected number of drops above 100 µm and above 1 mm per m³ (the input of L5's first-drop question), and the mass spectrum.

## 2. Picture and formal mechanism

Picture: a ledger with one line per size. A merger of a 10 µm and a 20 µm droplet crosses out one entry on each of their lines and
writes one entry on the line of 20.8 µm. Number falls by one per merger; mass is moved, never made.

Mechanism: binary events in a well-mixed volume. With n(m, t) dm the number of particles per m³ with mass in [m, m + dm] and the pair
rate K(m, m') (L0–L3: volume swept per second), the expected change is gains from all pairs that sum to m, minus losses of m in any
pair (Smoluchowski's coagulation equation, in cloud physics the stochastic collection equation, SCE):

  ∂n(m)/∂t = ½ ∫₀^m K(m', m − m') n(m') n(m − m') dm' − n(m) ∫₀^∞ K(m, m') n(m') dm'.                       (L4.1)

The ½ counts each unordered pair once. Its moments, ∫φ(m)·(L4.1): mass (φ = m) is conserved exactly; number (φ = 1) falls; the second
moment rises (derived in the textbook). (L4.1) is an equation for the mean: Gillespie (1972) derives it from the master equation of
the exact process by setting ⟨n_i n_j⟩ = ⟨n_i⟩⟨n_j⟩ (no correlations) and C(m, m) = 0 for exactly equal sizes. The page says so
plainly: the SCE does not describe one cloud, it describes the average of many, and it says nothing about the spread (L5).

The thesis's bookkeeping (the gravitational collection equation, GCE) is kept for comparison: two fixed groups, collectors that grow
smoothly by (L0.1) summed over all droplet sizes and never meet each other, and pool droplets that only deplete. The textbook derives
it from (L4.1) as a drift (first term of a jump expansion) restricted to collector–droplet pairs.

## 3. Model and numerics

- **Grid.** Bin masses x_k = x₀ 2^{k/s}, x₀ = mass of a 1 µm water sphere, s bins per doubling of mass, up to the first bin above a
  4 mm water sphere (radius; s = 8 gives 289 bins). Each bin stores the mass per unit ln r, G_k = 3 x_k² n(x_k), so the water is the
  plain sum Δ Σ G_k, Δ = ln 2/(3s).
- **One pair, one step.** For bins i ≤ j the events per m³ in Δt are C_ij = K_ij N_i N_j Δt (half that, with N_i(N_i − 1) → N_i², for
  i = j; K_ii = 0 by gravity alone). Each event removes one particle of mass x_i and one of x_j and makes one of x* = x_i + x_j.
- **Two-bin deposit.** x* lies between x_k and x_{k+1}; put the fraction f = (x* − x_k)/(x_{k+1} − x_k) of the products in bin k + 1
  and 1 − f in bin k. Two conditions (number and mass of the products), two unknowns: the lever rule. It keeps both exactly; it
  smears a product over two neighbours, which is the scheme's numerical diffusion, measured by the Golovin test.
- **Positivity.** Pairs are visited smaller bin first and updated in place; a step never takes from a bin more than it holds,
  counting what the product returns to the bin (the limiter of the baseline, derived again in the textbook). Rounding leftovers below
  zero are set to zero and counted.
- **Overflow.** Products heavier than the last bin go to an overflow store that keeps their mass and number and takes no further part.
  The mass inventory, in-grid + overflow, equals the initial mass to rounding.
- **Kernels** (each built from the levels below, at the cloud's air): (a) the thesis kernel: Stokes speeds, E = 1, the thesis's
  coalescence law exp(−1.15 W_E) with Stokes speeds; (b) the extended kernel: Beard speeds (L1), this study's efficiency table (L2),
  the same coalescence law with Beard speeds (L3); (c) for the closure band: (b) with Hall's (1980) efficiencies; (d) for the
  near-equal bracket: (b) with E = 1 above p = 0.6 for collectors ≥ 40 µm (L2).
- **Time step** Δt = 1 s, tested at 0.5 and 0.25 s; resolution s = 4, 8, 16. The reference runs use s = 8, Δt = 1 s, 60 min.
- **GCE**, for the kernel-versus-bookkeeping comparison: collector classes from the collector mode's bins, each with its own radius
  R_i(t) growing by Σ_j K(R_i, r_j) n_j x_j, pool bins from the droplet mode depleting by Σ_i N_i K(R_i, r_j); integrated with the same
  Δt. Same initial water, same kernels.

## 4. Rejected alternatives

1. **Bott's (1998) flux method**: the standard bin scheme; the baseline's stored comparison showed number errors up to +4.7 % at 2
   bins per doubling against the split's 0.2 %. The two-bin split keeps the number of products exactly; chosen.
2. **A bulk (moment) scheme**: two moments per mode cannot answer t₅₀/t₉₀ of a threshold fraction without assuming the spectrum's
   shape; rejected because the observable is a property of the spectrum.
3. **Particles (super-droplets) for the mean**: they converge to the same mean at a far higher cost for the tails; they are L5's
   tool for the spread, not L4's for the mean.

## 5. Assumptions and their numbers

| Assumption | Number | Fails where |
|---|---|---|
| Well-mixed box | collectors sweep 1.37 × 10⁻³ of the air per second (L0); turbulent remixing over a metre takes of order L^{2/3} ε^{−1/3} = 4.6 s at ε = 10⁻² m²/s³ (1 m scale; dimensional estimate) | small volumes and rare drops: L5 |
| No correlations (mean field) | exact as V → ∞ (Gillespie 1972); Dziekan and Pawlowska (2017) found the SCE right for the mean only with ≥ 10⁴ to ≥ 10⁷ droplets in the volume, depending on the spectrum | the tail and small volumes: L5 |
| Explicit step Δt = 1 s | a collector merges about 0.13 times per second at the start (L0); the fraction of a droplet bin removed per step is about 4 × 10⁻⁴ | tested by Δt = 0.5, 0.25 s |
| Grid resolution s = 8 | neighbour radius ratio 2^{1/24} = 1.029 | tested by s = 4, 16 and the Golovin solution |
| Closed box, no condensation, no sedimentation out, no break-up | L0 row: condensation supply comparable to the collection drain | a real cloud (stated on the page) |

## 6. Exact solutions and checks it must pass

- **Mass**: in-grid + overflow = initial to rounding (relative 10⁻¹³ or better over 60 min); the only mass error against an exact
  solution is the part of the initial spectrum below the grid's first bin, stated separately.
- **Golovin's exact solution** (sum kernel K = b(m + m'), exponential start; derived in the textbook by the Laplace transform and
  characteristics), with b = 1.5 m³ kg⁻¹ s⁻¹, mean radius 10 µm, L = 1 g/m³, 60 min: the spectrum error ε = (Δ/L) Σ |G_k − G_exact|
  at s = 2, 4, 8, 16, the observed order log₂(ε_s/ε_{2s}), the number error against N₀ e^{−bLt} (exact), the mass error.
- **Moment identities**: number decay e^{−bLt} for the sum kernel; for the constant kernel (K = K₀), N(t) = N₀/(1 + ½K₀N₀t).
- **Monodisperse, capture only** (from contract L0, prediction 8.2): the SCE restricted to collector–droplet pairs, started with
  identical collectors and droplets, puts 12 ± 2 % of collector mass above R_m = 60.15 µm at t₉₀ (master equation: 12.1 %).
- **Δt and s convergence** of t₅₀, t₉₀ (first recorded minutes) and of F₄₀(30 min).
- **Positivity** counter = 0 in the warm runs.

## 7. Predictions that could come out wrong

1. (From L0.) With the thesis kernel and the lognormal modes the SCE gives t₅₀ within ±0.5 min of 2.50 min and t₉₀ below 6.85 min
   (the capture-only mean field). Recorded once a minute, the old study had 3 / 5 min.
2. (From L2.) With the extended kernel the SCE gives 6 / 14 min within ±1 min (the old study's headline), because the efficiency at
   the governing pair matches the old table to 0.3 %.
3. (From the brief.) The kernel changes observable 1 more than the bookkeeping: |t₉₀(thesis kernel) − t₉₀(extended)| exceeds
   |t₉₀(SCE) − t₉₀(GCE)| for both kernels. (Old study: kernel 5 → 14 min; bookkeeping 7 → 5 and 19 → 14 min.)
4. (From L2.) The closure band: replacing this study's efficiencies by Hall's moves t₉₀ by less than the kernel change of
   prediction 3, but by more than the Δt and s errors; this band is the honest uncertainty of observable 1 within the model.
5. (Scheme.) Golovin's spectrum error falls with an observed order between 1 and 2 per doubling of s.

## 8. Derived, cited, chosen, and the price

Derived: (L4.1) from pair rates, its moments, the GCE as a restricted drift, the lever rule, the limiter, Golovin's solution.
Cited: Gillespie (1972) for the mean-field assumption; the test parameters of Golovin's case. Chosen: the lognormal modes, the grid,
the in-place pair order, Δt, the 4 mm top. Price: the SCE gives the mean only; its tail (the first large drops) is trustworthy only
in a large volume (L5 tests how large); the two-bin split smears the spectrum (Golovin measures by how much); the closed box has no
condensation, no sedimentation and no break-up.

## 9. Outcomes (computed after this contract; `tools/run_warm.cjs`, `tools/run_golovin.cjs`, `checks/check_physics.py`)

The contract file is dated 12:10, the stored runs 12:16–12:35 (23 Oct). Prediction 2 is a reproduction of the old study's published
numbers rather than a forecast about nature, and is labelled so on the page.

1. Thesis kernel, SCE: t₅₀ = 2.27, t₉₀ = 4.51 min (interpolated; 3 / 5 by the minute): **passed** (2.27 within ±0.5 of 2.50; 4.51 < 6.85).
   Why the runaway of L0 §8.1 does not happen here: the coalescence law with Stokes speeds switches off large pairs (chapter 4).
2. Extended kernel, SCE: 5.77 / 13.47 min (6 / 14 by the minute): **reproduced**.
3. Kernel against bookkeeping: kernel moves t₉₀ by 9.0 min (4.51 → 13.47); bookkeeping by 2.5 min (thesis, 4.51 → 7.0) and 5.2 min
   (extended, 13.47 → 18.67): **passed**.
4. Closure band: Hall's efficiencies give 4.57 / 11.38 min; the band 11.4–13.5 min is smaller than the kernel change (9.0 min) and far
   larger than the Δt and s errors (two independent codes agree to 0.013 min, `check_physics.py`): **passed**.
5. Golovin: spectrum error 0.428 / 0.150 / 0.051 / 0.018 at s = 2 / 4 / 8 / 16, observed order 1.51, 1.56, 1.49: **passed**.
   Mass error −4.58 × 10⁻⁷ (the water below the first bin); scheme drift 1.8 × 10⁻¹³.

Independent check (`checks/check_physics.py`): the SCE re-solved with different code and update order (NumPy, all pairs at once,
Δt = 0.5 s) gives 5.774 / 13.483 min. A limiter that counts gross instead of net losses (a large drop sweeping up a droplet mostly stays
in its own bin) slows the large drops and gives t₉₀ = 18.3 min; the model's limiter counts net losses, as it must.

## 10. Answers to round 1 (`skeptic-G1-L4L5-r1.md`, L4: PASS with fixes)

| # | Answer |
|---|---|
| 1 | The §6 checks, now reported. Golovin number error −0.0018 at s = 8 (`tools/run_golovin.cjs`). Constant kernel, monodisperse start, N/N₀ = 0.24993 against the exact 0.25000 after 6000 s (`derive/L4_conv.cjs`). The monodisperse 12 ± 2 % test was withdrawn in L0 round 3 (grid-dependent), and its grid-free replacement, the death-chain test of the stochastic engine, passed (`check_physics.py`). Positivity: 0 limiter corrections in every run. Δt and s convergence: next row. |
| 2 | Accepted: code agreement is not a resolution error. Measured (`derive/L4_conv.cjs`): t₉₀ = 13.352 / 13.470 / 13.527 min at s = 4 / 8 / 16, and 13.470 / 13.473 / 13.474 min at Δt = 1 / 0.5 / 0.25 s. The numerical answer is good to about 0.1 min, against a physical band of 3.0 min. Chapter 5 now teaches this. |
| 3 | Accepted: Golovin's ε measures the bulk of the spectrum, not the far tail. The skeptic measured the two-bin scheme over-filling the tail (×2.05 at s = 8 and ×1.31 at s = 16 at the 10⁻⁶ level). The consequence for L5 was measured directly: the 1 m³ first-drop median from (6.1) is 55 / 57 / 61 s at s = 8 / 16 / 32 (`derive/L5_tail.cjs`, 1 s records), so chapter 6 says "about a minute" and names the slow convergence. |
| 4 | GCE times corrected to the interpolated 6.86 and 18.57 min; bookkeeping gaps 2.3 and 5.1 min (chapters 5 and 9; `check_numbers.cjs`). |
| 5 | t₅₀, t₉₀ are interpolated between 5 s or 10 s records; the per-minute values appear only as the old study's comparison column. |
| 6 | "A few × 10⁻¹³" (3.4 × 10⁻¹³ is the largest, as chapter 5 says). |
| 7 | The notes say "it assumes that the numbers of drops in different size classes are uncorrelated" and, in chapter 6, give the n(n − 1) against n² example. The jump-expansion phrase is not on the page. |
| 8 | N(≥ 100 µm) = 3.64 × 10⁴, 4.12 × 10³, 9.96 × 10² per m³ at 10 / 20 / 30 min (extended, s = 8): falling, because the 100 µm drops merge into larger ones. The caption of figure 6.1 now says why (6.1) uses the largest n₁₀₀ reached. |
| 9 | Noted with thanks: the limiter acts only in the top bin and moves 5 × 10⁻²⁷ of the water. |
| 10 | "A mean drop mass equal to that of a 10 µm sphere." |
| 11 | Accepted: file times cannot be checked from git. The contract claims nothing about timing beyond labelling which outcomes were known. |

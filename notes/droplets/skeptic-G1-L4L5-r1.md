# Skeptic report, Gate 1, round 1: contracts L4 and L5

Blind review: I read only `contract-L4.md`, `contract-L5.md`, the code (`physics.cjs`, `tools/*.cjs`, `checks/check_physics.py`)
and the data files. I ran `tools/run_golovin.cjs`, `tools/run_warm.cjs` (s = 4, 8, 16; Δt = 1, 0.5, 0.25 s), `tools/tail_resolution.cjs 32`,
`checks/check_physics.py` (12/12 pass), and my own Python and instrumented copies in the scratchpad (`g1l45_*`). I edited no project
file except this report.

Overall: the physics is sound and the code does what the contracts say. The SCE scheme, the GCE, Golovin's solution, the exact
stochastic engine (class majorants + thinning) and the stored ensembles all check out. The problems are in how outcomes are labelled
(two "passes" that are not clean passes, one "prediction" whose answer was already in the contract), one wrong physical explanation
(Kostinski and Shaw's luck factor), and the far tail of the SCE, which the 1 m³ first-drop time depends on and which is not converged.

---

## L4: the SCE, two-bin scheme, GCE, Golovin, warm-cloud times

**Verdict: PASS with fixes.**

### Objections

| # | Severity | Claim (quoted) | Problem | Fix I would accept |
|---|---|---|---|---|
| 1 | must-fix | §6 lists checks: "the number error against N₀ e^{−bLt}", "for the constant kernel … N(t) = N₀/(1 + ½K₀N₀t)", "Monodisperse, capture only … 12 ± 2 %", "Δt and s convergence of t₅₀, t₉₀ … and of F₄₀(30 min)", "Positivity counter = 0" | §9 reports none of these. They are promised checks with no outcome. | Report each, or point to where it is reported. What I measured: Golovin number error −0.18 % (s = 8), −0.17 % (s = 16); positivity fixes 0 in all runs; Δt and s numbers in row 2. |
| 2 | must-fix | Outcome 4: "far larger than the Δt and s errors (two independent codes agree to 0.013 min, `check_physics.py`)" | Agreement between two codes is not a Δt or s error. The NumPy re-solve reads the model's own kernel matrix and grid (s = 8), so it cannot see grid error. The real grid error is about 10× the quoted 0.013 min: extended-kernel t₉₀ = 13.352 / 13.470 / 13.527 min at s = 4 / 8 / 16 (my runs, interpolated), so about 0.06–0.1 min at s = 8. Δt error is tiny: 13.470 / 13.473 / 13.474 min at Δt = 1 / 0.5 / 0.25 s. The conclusion stands (the band is 2.1 min). | Cite the s and Δt runs, not the code agreement. Report the code agreement as what it is: a check of the update code, same kernel, same grid. |
| 3 | must-fix | §1: "the mean-field expected number of drops above 100 µm and above 1 mm per m³ (the input of L5's first-drop question)"; §6/§9: Golovin's ε as the measure of the scheme's error | ε is an L1 error dominated by the bulk of the spectrum. It says nothing about the far tail, and the far tail is exactly what L5's Poisson bridge uses at 1 m³: about 0.7 drops ≥ 100 µm per m³ among 3 × 10⁸ drops. The two-bin split makes the far tail too fat (each event smears a product into the next bin up). In Golovin's test with the model's own `sceRun` at 60 min, the number of drops above the radius where the exact cumulative fraction is 10⁻⁶ is too large by ×4.2 / ×2.05 / ×1.31 at s = 4 / 8 / 16. At the 10⁻⁹ level it is ×71 / ×10 / ×2.4. At 10 min: ×1.74 (s = 8) and ×1.20 (s = 16) at 10⁻⁶. | Add one tail measure to the Golovin test (for example the ratio above at 10⁻⁶ and 10⁻⁹) and one sentence on the page: the scheme over-fills the far tail, so first drops taken from it come too early. Link the sentence to L5. |
| 4 | minor | Outcome 3: "bookkeeping by 2.5 min (thesis, 4.51 → 7.0) and 5.2 min (extended, 13.47 → 18.67)" | Mixed resolutions. The SCE numbers are interpolated, but 7.0 is the once-a-minute value. 18.67 matches neither the stored data nor my runs. Interpolated GCE t₉₀ from `data/warm.json` (and my rerun) is 6.86 and 18.57 min, so the gaps are 2.35 and 5.10 min. The verdict is unchanged. | Use interpolated values throughout: 2.35 and 5.10 min. |
| 5 | minor | §1: t₅₀, t₉₀ are "the first recorded minutes" | §9 reports interpolated values as the headline numbers. | Define the observable once (interpolated) and give the per-minute values beside it. |
| 6 | minor | §6: "relative 10⁻¹³ or better over 60 min" | Measured drift: 3.4 × 10⁻¹³ (thesis, s = 8), 3.1 × 10⁻¹³ (extended, s = 16). | "a few × 10⁻¹³". |
| 7 | minor | §2: "setting ⟨n_i n_j⟩ = ⟨n_i⟩⟨n_j⟩ (no correlations) and C(m, m) = 0 for exactly equal sizes"; "as a drift (first term of a jump expansion)" | A second-year student cannot decode either phrase. The first presumably means that equal drops fall at equal speeds, so N(N − 1) → N² costs nothing. The second is a Kramers–Moyal expansion. | Say it in words: "replace the random jumps of a collector's mass by their average rate", and "equal drops never meet under gravity, so the self-pair term vanishes". |
| 8 | minor | §1 observable: N(≥ 100 µm), N(≥ 1 mm) per m³ | Not reported in §9. The tool prints them: 3.64 × 10⁴, 4.12 × 10³, 9.96 × 10² m⁻³ at 10 / 20 / 30 min (extended, s = 8). | Report them. Note that N₁₀₀ falls after 10 min because the 100 µm drops merge into larger ones; students will ask. |
| 9 | minor | §3 "Positivity … a step never takes from a bin more than it holds" | Good news worth stating. I instrumented the limiter: in the 60 min extended run it binds 136 828 times, all in the top (4.1 mm) bin, and suppresses 5 × 10⁻²⁷ of the water. It never touches the physics. The "gross limiter gives 18.3 min" sentence is then clear: a gross cap would bind everywhere a big drop sweeps droplets. | One sentence: where and how much the limiter acts. |
| 10 | minor | Golovin "mean radius 10 µm" | It is the radius of the mean mass (x̄ = mass of a 10 µm sphere), not the mean radius. | Reword. |
| 11 | minor | "The contract file is dated 12:10, the stored runs 12:16–12:35" | This cannot be checked from the repository. The contract and the data first enter git together (commit efc3e42, 13:23), and the contract's file time is now 13:36. The data file times (12:16, 12:35) do match. | Commit the contract before the runs next time, or record its hash in the run output. No change needed to the page. |

### Numbers I recomputed

- **Golovin, independently (SciPy `ive`, my own quadrature):** at bLt = 5.4, N/N₀ = 0.004517 = e^{−5.4} (exact); mass = 1.00000000 L; M₂/M₂(0) =
  49 055 against e^{2bLt} = 49 021 (0.07 %, quadrature).
- **Golovin, my own two-bin SCE solver** (vectorised, all pairs at once, my net-loss limiter, Δt = 1 s): ε = 0.418 / 0.140 / 0.042 at s =
  2 / 4 / 8, observed order 1.58, 1.76. Number error −0.5 %; mass drift ≤ 3 × 10⁻¹⁵. Peak 470 µm against 456 exact at s = 8. These match
  the model's ε = 0.428 / 0.150 / 0.051 / 0.018 and orders 1.51 / 1.56 / 1.49 (rerun: identical to §9). The small differences come from
  the update order.
- **SCE moment property (constant kernel, my solver, s = 4):** N(t)/N₀ = 0.24978 against 1/(1 + ½K₀N₀t) = 0.25000. The second moment rises
  1.013 × the exact K₀M₁²t: the two-bin smearing adds 1.3 % to M₂ growth at s = 4.
- **Warm cloud** (model, interpolated at 5 s): thesis kernel 2.272 / 4.512 min; extended 5.767 / 13.470; Hall 4.570 / 11.382; GCE thesis
  2.499 / 6.860, GCE extended 6.570 / 18.567. All of §9 is reproduced except the GCE figures in objection 4. s = 4 / 8 / 16: thesis t₉₀
  4.370 / 4.512 / 4.570; extended 13.352 / 13.470 / 13.527.
- **NumPy re-solve** (`check_physics.py`): 5.774 / 13.483 min, as stated.

---

## L5: the exact stochastic process, first-drop times, Poisson bridge

**Verdict: PASS with fixes.** The engine is right: I checked the same-class rate by hand (an unordered pair is proposed with probability
2/n_a² at class rate K* n_a²/2V, then accepted with K/K*, which gives K/V). The majorant is a valid upper bound: the table's maximum is
taken over the bounding rectangle in (ln R, ln p), which contains the true pair set. The death-chain test passes (8.246 ± 0.036 against
8.221, p = 0.15). The fixes are about labels, one mechanism and the tail.

### Objections

| # | Severity | Claim (quoted) | Problem | Fix I would accept |
|---|---|---|---|---|
| 1 | must-fix | Prediction 1, "The gap … about ten times earlier than the mean-field time … (590 s in the SCE)"; outcome "**passed**" | This was not a prediction. §6 of the same contract already gives the answer: "1 m³: 55 s at s = 8, 60 s at s = 16". The 590 s was also computed beforehand. Only the bridge's validity was still open, and prediction 2 tests that. | Label it as L4 labels its prediction 2: "computed before the contract; not a forecast". Drop "passed". |
| 2 | must-fix | Prediction 1: "The factor ten is Kostinski and Shaw's luck factor for the fastest 10⁻⁶ of collectors"; §2 picture "One happens to meet a droplet early … the early lead never closes" | The wrong mechanism, and the contract's own outcome 3 shows it: every first 100 µm drop came from collector–collector mergers. Capture luck cannot do it here. From the largest collector the truncated modes allow (69.1 µm), reaching 100 µm by droplet capture alone takes about 1 300 captures and 450 s on average (mean field, no depletion, the model's kernel). Its spread is a sum of 1 300 exponentials: relative sd ≈ 3 %, so even the luckiest 10⁻⁶ is near 390 s, not 60 s. Kostinski and Shaw's factor applies to a collector that needs tens of captures. The agreement with "10" is a coincidence. | Rewrite the explanation: the first drizzle drop comes from the rare largest collectors meeting each other (three or more), not from luck in droplet captures. Give the two-line estimate above; it teaches more than the luck factor. Keep Kostinski and Shaw as the contrast: why luck matters for small collectors (few captures) and not here (many). |
| 3 | must-fix | §6: "the SCE's V n₁₀₀(t) = ln 2 times converge with grid resolution (1 m³: 55 s at s = 8, 60 s at s = 16 …)"; outcome 1 "after about 60 s (bridge, s = 16)" | Not converged. I ran `tools/tail_resolution.cjs 32`: 65 s at s = 32 (1 L: 180 s, 100 cm³: 285 s). The steps 55 → 60 → 65 s do not shrink. This fits L4 objection 3: the two-bin scheme over-fills the tail at the 10⁻⁶ to 10⁻⁹ level (×1.3–2.4 at s = 16 in Golovin's test), and here n₁₀₀ rises about 100× per minute near 60 s, so a factor 2 is about 9 s. | State the 1 m³ time as "at least 65 s, probably 65–75 s; still moving with resolution". The gap becomes about 9 (585/65), which is still "about ten". Remove "converge". |
| 4 | must-fix | Prediction 4: "for V ≥ 1000 cm³ it agrees within two standard errors at every minute"; outcome "**passed** for the range the page uses, with that note" | That rescopes the prediction after seeing the data. Against the truncated SCE at s = 16, the 1000 cm³ ensemble gives z = +1.5 at 23 min, +3.0 at 25, +6.4 at 30 and +10.6 at 40 min. The prediction failed as stated after about 23 min, though the gap is tiny (≤ 2 × 10⁻⁴). I ruled out two causes. The overflow (F₄₀ excludes it) is only 1.8 × 10⁻³¹ at 30 min. The grid is not it either: s = 8 and 16 give the same F₄₀ at 30 min, 0.99944. | Label it "held to 21 min; failed statistically after about 23 min, in the fourth decimal; cause unknown (not overflow, not grid)". The page can still use the early range. |
| 5 | must-fix | §1 Observable 2: T₁₀₀(V) and T₁ₘₘ(V) "for V = 1, 10, 100 and 1000 cm³"; T₁ₘₘ in 1 m³ through the bridge | §9 reports T₁₀₀ only at 100 and 1000 cm³, and T₁ₘₘ nowhere. The missing cases are the most instructive. (a) **1 cm³:** a 100 µm drop is impossible by mass. The truncated cloud holds 1.11 g/m³, so one 100 µm drop needs the water of 3.8 cm³; the largest possible drop in 1 cm³ is 64 µm. Indeed 0 of 200 runs made one. (b) **10 cm³:** every one of the 100 runs made one (median 605 s), but the bridge **fails completely**: the SCE never reaches V n₁₀₀ = ln 2 (n₁₀₀ peaks near 3.8 × 10⁴ m⁻³), so it predicts that most volumes never make one (KS D = 0.97). (c) **1 mm:** impossible in ≤ 1000 cm³ (it needs 3.8 L of cloud water). The bridge gives 1030 / 1075 s at s = 8 / 16 for 1 m³, entirely untested. | Report (a)–(c). (a) and (c) need one line each of mass budget. (b) is the honest lower limit of the bridge: it works at ≥ 100 cm³ and fails at 10 cm³. Give the 1 mm number as an untested extrapolation, or drop it. |
| 6 | minor | Outcome 3: "230 of 230 first drops ≥ 100 µm" | The prediction is for V ≥ 100 cm³, which is 130 runs. The 230 include the 100 runs at 10 cm³. All are 100 % either way. | "130 of 130 at V ≥ 100 cm³ (and 100 of 100 at 10 cm³)". |
| 7 | minor | §3: "any violation stops the run" | The code stops after more than 10 violations (`if (violations > 10) throw`). Zero occurred, so no result changes. | Make the code throw at the first violation, or reword. |
| 8 | minor | §6 engine check: "mean and variance of that time [to the n-th capture] must match Σ 1/λ_k and Σ 1/λ_k²" | The test actually run compares the capture-count distribution at 60 s with the matrix exponential (χ²). That is stronger, but it is a different test. It also never exercises the same-class rate with K > 0, because identical droplets have K = 0. Same-class collector–collector mergers are the route to 100 µm (objection 2). The formula is right (checked above), but it is tested only by derivation. | Describe the test that was run. Either add a same-class test (for example a constant kernel in one class) or say "same-class rate: derived, not separately tested". |
| 9 | minor | §6: "acceptance ratio reported" | Not in §9. Stored runs: 0.50 (1 cm³), 0.55, 0.59, 0.59 (1000 cm³). | Report it. |
| 10 | minor | §5: "volumes above about a litre are well mixed only on minute time scales" | This contradicts the row's own estimates: (0.1 m)^{2/3} ε^{−1/3} = 1.0 s at 10 cm, and 4.6 s at 1 m (L4). | Compare the mixing time (about 5 s at 1 m) with the first-drop time (about 60 s), and state the idealisation in those terms. |
| 11 | minor | §5: truncation "removes 0.27 % of each mode's number" | Both `lognormalBins` (rescale) and `drawModes` (redraw) keep the number. They move 0.27 % of the drops from the tails into the body. | Reword. |
| 12 | minor | §3: "the untruncated lognormal tail already holds 0.23 drops of r ≥ 100 µm and 82 drops ≥ 80 µm per m³" | The continuous lognormal gives 0.25 and 72 per m³. The grid values carry a binning effect (+14 % at 80 µm). | Quote the continuous values, or say "on the s = 8 grid". |
| 13 | minor | Prediction 4 explanation: "depletion and correlations slow growth" | With fixed counts, 1 cm³ holds exactly one collector, so a collector–collector merger is impossible (n(n − 1) = 0, where the SCE uses n²). Given objection 2, that is the main reason for the 1 cm³ lag, and a student can see it at once. | Say it in those words. |
| 14 | minor | Prediction 2 "**passed** at the 5 % level" | With 30 runs, the 5 % KS critical distance is 0.25, so the test excludes only large differences. The medians (174 s exact, 175 s bridge at s = 16, 180 s at s = 32) are the stronger evidence. | One sentence on the test's power. |
| 15 | minor | "The contract file is dated 12:26, the stored ensembles 12:28–12:36" | As for L4, this cannot be verified from git. `stochastic.json` was written at 12:28:13. If the 430-run ensemble took more than two minutes, it started before 12:26. | Note only. Objection 1 is the real issue. |

### Numbers I recomputed

- **Ensembles** (`data/stochastic.json`): F₄₀(10 min) = 0.5204 ± 0.0190, 0.6955 ± 0.0092, 0.7303 ± 0.0035, 0.7398 ± 0.0023 for 1 / 10 / 100 /
  1000 cm³. Truncated SCE (s = 16) 0.7418. At 20 min, 100 cm³: z = −7.1. These match §9.
- **First 100 µm drop:** 0/200 runs (1 cm³); 100/100, median 605 s (10 cm³); 100/100, median 286 s (100 cm³); 30/30, median 174 s
  (1000 cm³). Partner ≥ 30 µm in every run that made one. Violations 0.
- **KS, my own scipy** (bridge s = 16): 1000 cm³ D = 0.156, p = 0.42; 100 cm³ D = 0.088, p = 0.40 (as stated); 10 cm³ D = 0.97, p ≈ 0
  (not stated). With s = 8: D = 0.187 / 0.091.
- **Bridge medians from `data/bridge.json`:** 1 m³ 55 / 60 s, 1 L 170 / 175 s, 100 cm³ 280 / 280 s (s = 8 / 16). At s = 32 (my run): 65 / 180 /
  285 s. Half the water ≥ 100 µm at 585 s. First 1 mm drop in 1 m³: 1030 / 1075 s.
- **Mass budget:** truncated LWC 1.109 g/m³; a 100 µm drop needs 3.78 cm³ of cloud and a 1 mm drop 3.78 L. The largest possible drop is
  64 µm in 1 cm³ and 138 µm in 10 cm³.
- **Capture-only estimate:** a 69.1 µm collector in 8 µm droplets at 0.8 g/m³ (model kernel; E = 0.48, v = 0.43 m/s) needs 1 309
  captures and 449 s to reach 100 µm.
- **Engine checks** (`check_physics.py`, rerun, 12/12 pass): death chain 8.246 ± 0.036 against 8.221, χ² p = 0.15. Bridge as above.

---

## For the reader (both notes)

A strong second-year student can follow both notes if the textbook keeps the ledger picture (L4) and the "too-fast clock, then accept
with K/K*" picture of thinning (L5). Three places would lose them: the "jump expansion" wording, the unexplained "C(m, m) = 0", and
the luck story in L5 §2, which the results contradict. The two mass-budget lines (no 100 µm drop in 1 cm³, no 1 mm drop in a litre) are
the most teachable facts in L5 and are currently missing.

---

## Fixes check (round 1 answers, contracts §10, chapters 5–6, `tools/figs.cjs`)

I reran `derive/L4_conv.cjs` and `derive/L5_tail.cjs`, and both reproduce exactly:
- L4: t₉₀ = 13.352 / 13.470 / 13.527 min at s = 4 / 8 / 16 and 13.470 / 13.473 / 13.474 min at Δt = 1 / 0.5 / 0.25 s. The constant kernel gives N/N₀ = 0.24993 against 0.25000.
- L5: the bridge medians are 55 / 57 / 61 s (1 m³), 170 / 173 / 179 s (1000 cm³) and 278 / 279 / 284 s (100 cm³) at s = 8 / 16 / 32.

My earlier 65 s came from 5 s records, so 61 s is the right figure. The running maximum of n₁₀₀ in figure 6.1 is correct, because a volume that once held a 100 µm drop keeps one. It leaves the 100 cm³, 1000 cm³ and 1 m³ medians unchanged, since they fall before n₁₀₀ peaks at 580 s. In 10 cm³ it gives the plateau of 1 − e^{−0.39} = 32 %. The L4 answers 1–11 and L5 answers 1–4 and 6–15 are accepted.

**Remaining issues**

| # | Severity | Where | Problem | Fix |
|---|---|---|---|---|
| R1 | must-fix (one sentence) | Chapter 6, the 10 cm³ paragraph: "The collection equation describes a cloud so large that no single drop matters, and spreads the same water over many drops." | The direction is backwards. The mean field puts the water in *fewer, larger* drops than a 10 cm³ box can hold. At 605 s (truncated SCE, s = 16), 53 % of the water is above 100 µm. That is 1.4 drops' worth of 100 µm per 10 cm³, but packed into drops of mass-mean radius 153 µm, only 0.39 per 10 cm³. By 15 and 30 min that radius is 250 and 630 µm. The mean-field drops keep growing on water from far beyond 10 cm³. A closed 10 cm³ box caps its largest drop at its own water, about 140 µm: the stored runs reach median 135 µm at 20 min and 138 µm at 60 min, never above 144 µm. So every box ends with exactly one drop of 100–140 µm. The page's own "the water ends up in one drop" is right; only the contrast sentence is wrong. | Replace with something like: "The collection equation describes a cloud so large that its big drops keep growing past 140 µm on water from far beyond 10 cm³, so there are fewer than one of them per 10 cm³. A closed 10 cm³ volume cannot grow a drop beyond its own water, about 140 µm, so every such volume ends with one." |
| R2 | minor | Chapter 6 and L5 §10.2: "1312 captures and 560 s" | No script in the repository produces this. With the model's kernel and no droplet depletion I get 1 309 captures and 449 s for 8 µm droplets at 0.80 g/m³, and 906 captures and 387 s for the truncated droplet spectrum. 560 s may include depletion. The argument holds for any of these, since all are far above 60–175 s. | Name the assumptions (droplet size, depletion), or add a script line that prints the number. |
| R3 | minor | L4 §6 still lists "Monodisperse, capture only … 12 ± 2 %"; §10.1 says "0 limiter corrections" | The test is withdrawn but still listed. And `fixes` counts rounding corrections, not limiter actions: the limiter does act, but only in the top bin (§10.9). | Strike the withdrawn line. Say "0 rounding fixes". |
| R4 | minor | L5 §9.1 and §9.4 still read "**passed**" | §10 corrects both labels, but a reader of §9 alone would miss the corrections. | Add "(see §10)" to the two labels, or edit §9. |

### Final Gate 1 verdicts

- **L4: PASS.** R3 is cosmetic.
- **L5: PASS once R1 is applied.** It is a one-sentence change and needs no new review round. R2 and R4 are cosmetic.

Confirmed applied: R1 (the chapter 6 10 cm³ paragraph is now correct: 155 µm drops, 0.39 per 10 cm³, a box caps at 139 µm), R2 (448 s and 1312 captures for 8 µm droplets with no depletion; this matches my 449 s), R4 (§9.1 and §9.4 point to §10), and the R3 wording "0 rounding fixes". Still open: L4 §6 lists the withdrawn "Monodisperse, capture only … 12 ± 2 %" test with no withdrawn mark (cosmetic). Verdicts: L4 PASS, L5 PASS.

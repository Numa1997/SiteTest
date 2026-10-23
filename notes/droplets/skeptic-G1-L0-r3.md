# Skeptic review, Gate 1, contract L0, round 3

Reviewed: `notes/droplets/contract-L0.md` (round 3) against my round-2 report `skeptic-G1-L0-r2.md`, and the files it cites in
`portfolios-src/droplets/derive/` (`L0_r3.cjs` and `L0_population.py` part (c) are new; `L0_wolfram.md`, `L0_sympy.py`, `L2_numbers.cjs`),
plus `physics.cjs` (the SCE and coalescence code that `L0_r3.cjs` calls). I opened `text/book-02.src.html`, `text/book-05.src.html` and
`baseline/results.html` only to check the citations and one provenance claim. `status.md` was not read.

## Runs

- `node derive/L0_r3.cjs` (4 s here, not a minute) and `python3 derive/L0_population.py` (12 s). Both exit 0. Output saved in
  `/tmp/claude-0/-home-user-SiteTest/de75440b-f270-5344-8ae7-923c4f178e24/scratchpad/sk3_out_r3.txt` and `.../sk3_out_pop.txt`.
- **Every number the contract quotes from these two files is printed there.** The table in section 5 (5.31 / 9.96 / 2.93 / 9.19; 6.29 / 13.02 / 3.35 / 11.03;
  11.23 / 21.93 / 6.41 / 19.22; 15.95 / 29.49 / 9.07 / 27.24). The well-mixed row: 176.5 m and 1.95 sweeps. Section 1: +58.9 / +8.8 / +2.3 / +0.8 %.
  Section 8.1: 2.27 / 3.65 min, 90.5 % off the grid; with the coalescence law 2.27 / 4.51 min, 0.0 %, 0.1 %. The mean field: 2.50 / 6.85 min, 78.3 → 164.0 µm.
  Section 1: P(R ≥ 65 µm) = 4.77 × 10⁻³, P(R ≥ 68 µm) = 2.20 × 10⁻⁵. The quad route: 2.92704 / 9.19197 min. Section 8.2: 551.1 s, 58.022 µm, s.d. 1.694 µm.
  The script also prints a fifth correction row (Stokes speeds with this study's E table: 13.51 / 22.89 / 7.93 / 22.77). The contract leaves it out. That is fine,
  and it backs "most of it from E = 1": E alone gives ×2.3–2.7, Beard alone ×1.2–1.3.
- New scratch checks (in the same scratchpad, `sk3_*`):
  - `sk3_sceconv.cjs` and `sk3_sceconv_law.cjs`: the 8.1 SCE at other bin widths, time steps and grid tops.
  - `sk3_chain.py`: the exact death chain of 8.2; molecular slip; the mixing scales; t*.

## Round-2 objections

| # | Objection | Verdict | Evidence |
|---|---|---|---|
| N1 | 8.1 met for an unnamed reason (runaway) | **answered**, but see R3-1 | The runaway is computed (2.27 / 3.65 min, 90.5 % off the 4 mm grid by 5 min), named (kernel ∝ m^{4/3}, the population form of the (L0.3) blow-up) and turned into a requirement for L4. The ±0.5 min band is gone. Both numbers are printed by `L0_r3.cjs`. My probe shows that 3.65 depends on the grid (R3-2, minor). The replacement "prediction that could fail" is not a prediction (R3-1). |
| N2 | 8.2's band smaller than its open choices | **answered** | Replaced by a test with no grid: the Gillespie engine against the exact pure-death chain. I solved the chain (n = 20, V = 0.05 cm³, t = 60 s): mean 16.72 captures, s.d. 1.72, P(j) from 0.0095 at j = 12 to 0.232 at j = 17. So the test can fail and has power. The s.d. 1.694 µm at t₉₀ = 551.1 s is printed (my round-2 value: 1.70). Minor: the number of realisations and the χ² pooling rule are not stated (R3-5). |
| N3 | "2.928, 9.186 (quad)" in no file | **answered** | Part (c) runs `quad` and prints 2.92704 and 9.19197 min (error estimates 10⁻¹¹ s). These equal my round-2 quadrature and `solve_ivp`. The 9.186 is gone from the contract. The comment in `L0_sympy.py` (line 33) is now true. |
| N4 | Coalescence row selective | **answered** | Rewritten as I proposed (not measured; Straub 0.99998, Low and List 0.54; BO95 via Jacobson; uncertainty unknown). I rechecked We ≈ 2–2.5 × 10⁻⁵ for 40/8 µm, so E_coal = 0.99997–0.99998. Stale echo: the §10 row 5 answer still says "coalescence ≥ 0.9996" (R3-4). |
| N5 | Times without their errors | **answered** | The four-row table matches the script and reproduces my round-2 numbers. "Short by about 2 to 3, most of it from E = 1" is right (ratios 2.09–3.10). |
| N6 | L0 stops at 60 µm in the thesis cloud | **answered** | Said in bold in §1 and in the last line of §7, with the master-equation tail. The size names are corrected. |
| N7 | Picture shows half the mechanism | **answered** | §2 now has sweep R⁴ against mass R³, the faster heavier drop, and "a third to a half are hit". |
| N8 | Langmuir's equation not in the cited section | **answered** | "Usually attributed … not checked against the equation in his paper." |
| N9 | 0.344 without a file | **answered** | `derive/L2_numbers.cjs` prints 0.344 at R = 40 µm, r/R = 0.2 (I ran it). Nit: that script calls `L2_traj.cjs`, not `physics.cjs` pairEfficiency. `check_physics.py` compares the model's value with SciPy ("text 0.344"). |
| N10 | Still air against well mixed | **answered** | The scale argument is in the row. I checked (l²/ε)^{1/3} = 1.00 s and 0.46 s at l = 1 cm, ε = 10⁻⁴ and 10⁻³ m²/s³. 1 cm is a few Kolmogorov lengths (2.6 and 1.5 mm), so it is borderline inertial, but τ_η = 0.41 and 0.13 s gives the same conclusion: seconds against a 12 min depletion time. 176.5 m and 1.95 are printed. |
| N11 | "≪" not usable | **answered** | N_c ≤ 0.015 cm⁻³ ⇒ +2.3 %, with the computed series (my round-2 +67 % was at 0.154; the contract's +59 % is at 0.150). Stale echo: the §10 row 6 answer still says "N_c ≪ 0.154" (R3-4). |
| N12 | Wolfram checks its own antiderivative | **partly** | The contract answer is now honest, and no sentence in the contract leans on Wolfram for the printed G. But `L0_wolfram.md` item 4 still reads "differentiates back to the integrand, equation (L0.5)", and the printed G was not added to the saved Wolfram input. Minor; one word fixes it ("Wolfram's own antiderivative of …"). |
| N13 | Scales scattered; cloud type | **answered** | Scales are listed and the cloud type is stated (weakly turbulent layer or young cumulus, ε ≤ 10⁻² m²/s³; vigorous cumulus up to 6.5 × 10⁻²). t* = 21.1 min is right: 1/(cR₀) = 21.08 min, and 12.64 = 0.6 t*. The value t* = 17.77 min in my round-2 report was wrong. |
| r1 #10 | Thesis unnamed; "which textbook" | **answered** | N. Koudsie (2022), Bachelor thesis, Leipzig, named in the header. Stokes' drag points to chapter 2 (`text/book-02.src.html`, which derives (2.2) from the stream function) and to `derive/L1_stokes_sympy.py`; both exist. The equation numbers "eq. 20" and "(4.2)" are not checked against the thesis. The baseline quotes the law as exp(−1.15 W_E), which is what `physics.cjs` uses. |

Of the 13 round-2 objections and round-1 #10: 13 are answered and 1 is partly answered (N12, minor).

## New objections (round-3 text)

| # | Where | What is wrong | Evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| R3-1 | §8.1, "The prediction that could fail … (Outcome, computed after this prediction was written: 2.27 / 4.51 min …)" | This is labelled a prediction, but its outcome was already known. The old study's own row in the baseline reads "3 / 5 min SCE, thesis kernel", so t₉₀ lies in (4, 5] min. That is exactly the predicted "t₉₀ moves above 4 min" and "the runaway stops". The project's lecture notes already print the same kernel's result, 2.27 / 4.51 min: `text/book-05.src.html` (table "thesis | SCE | 2.27 | 4.51 | 3 / 5", file time 12:49) and `text/book-02.src.html` ("4.51 min … with Stokes speeds", 12:45). Both were written before this contract (13:14). Calling this a prediction, with a note that it was computed afterwards, presents a reproduction as a test. With it, §8 has no physical prediction left that could fail. 8.2 is a valid test, but of the code, not of nature. | baseline `results.html` line 23; the book-05 table; the file times | **must fix** (honesty; one sentence) | Relabel it: "Known result, reproduced: the old study recorded 5 min and chapter 5 gives 4.51 min; L0 supplies the reason (the runaway stops because E_coal → 0 at Weber numbers of tens)." Either rename §8 "Tests for later levels", or add one forward claim whose outcome is not yet known. An example: the share of the 40 → 100 µm time spent below 60 µm stays above 50 % with L1 + L2. `L0_r3.cjs` already gives 51 % (Hall) and 54 % (own table), so this would itself be a check, not a prediction; choose one that has not been run. |
| R3-2 | §8.1, "t₉₀ = 3.65 min … in line with the skeptic's 2.3 / 4.1"; "every run must count the mass that leaves the grid" | 3.65 is a property of this grid, not of the kernel. Counting the overflow mass is necessary but not enough: a drop parked in the overflow store stops collecting, so t₉₀ moves with the grid top. The gap to the grid-free super-droplet value (4.0–4.1) is 10 %, and it is not named. | Same code (`physics.cjs` sceRun), all pairs, Stokes, E = 1. t₉₀ = 3.51 / 3.65 / 3.72 min for s = 4 / 8 / 16 (4 mm top). 3.65 → 3.86 min when the top is 2 mm instead of 4 mm. Δt 1 → 0.25 s: 3.648 → 3.654. t₅₀ is stable (2.24–2.28). With the coalescence law nothing leaves the grid, and t₉₀ = 4.37 / 4.51 / 4.57 for s = 4 / 8 / 16, so "above 4 min" is robust there. | minor | Write "t₉₀ ≈ 3.5–3.9 min (bins and grid top; super-droplets 4.0–4.1)". Add to the L4 requirement: "and state the grid top, since parked mass stops collecting". |
| R3-3 | §5 Stokes row, "molecular slip raises … Δv(40/8 µm) by 0.05 %" | The sign and the scope are wrong. Slip on the 8 µm droplet alone *lowers* Δv by 0.049 %. Slip on both drops (Cunningham, λ = 0.0756 µm) raises Δv by 0.20 %. The 0.05 % came from my round-2 report, where I gave it without its sign. The error is mine, carried into the contract. Negligible either way. | `sk3_chain.py`: v(8 µm) +1.19 %, v(40 µm) +0.24 %, Δv +0.198 % | minor | "raises v(8 µm) by 1.2 % and Δv(40/8 µm) by 0.2 %". |
| R3-4 | §10 answer rows 1, 2, 5, 6 | They describe text that round 3 replaced. Row 1: "replaced by prediction 8.2 … (12.1 %)", but 8.2 is now the Gillespie test. Row 2: "the band is one-sided and argued", but 8.1 has no band. Row 5: "coalescence ≥ 0.9996", contradicted by §5. Row 6: "N_c ≪ 0.154". | — | minor | Mark them "superseded in round 3 (see N1, N2, N4, N11)". |
| R3-5 | §8.2 | The test has no sample size or χ² pooling rule. The exact reference distribution is not recorded. | Exact chain: mean 16.72, s.d. 1.72 captures; expected counts below j = 12 are under 1 % in total. | minor | Add "10⁴ realisations; pool classes with expected count < 5; exact mean 16.72 ± 1.72 captures". |

Checked and found correct in the rewritten parts:
- The m^{4/3} homogeneity and the gelling argument.
- R(∞) = 1/(1/R₀ − Φ): 78.3 → 164 µm implies 40 → 54.6 µm.
- The Weber number "of tens above 200 µm" with Stokes speeds: about 20 for 400 + 200 µm; 0.08 for 200 + 40 µm.
- The factors "2 to 3" in the corrections table.
- The depletion time, 12.2 min.
- The fall distance and the sweep integral; the script integrates both correctly.
- v ∝ R → exponential; v ∝ √R → R^{1/2} linear in t.

## The six thresholds

| Threshold | Verdict | Reason |
|---|---|---|
| Motivated | **pass** | Both of the study's questions get an L0 answer: "how fast" (times with their L1/L2 corrections; L0 is short by 2–3×) and "into rain?" (no: identical collectors stop at 60.15 µm). The bottleneck is kept. |
| Honest | **fail (narrow)** | R3-1: a known result is presented as a prediction with an outcome "computed after". Everything else is now traceable, and the earlier untraceable numbers (quad, 0.344) are fixed. |
| Derived | **pass (narrow)** | (L0.1)–(L0.5) hold. 8.2 is well posed and exactly computable. 8.1 now states its mechanism. But after R3-1, L0 has no open prediction about nature, only a code test. |
| Checked | **pass** | Every quoted number is printed by a cited file, and my independent routes agree. The only soft spot is the grid dependence of 3.65 (R3-2). |
| Sourced | **pass** | Thesis named; Langmuir hedged; Stokes derivation and its check exist; 0.344 has a file. Nits: `L2_numbers.cjs` uses `L2_traj.cjs`; thesis equation numbers unchecked. |
| Readable | **pass (narrow)** | Clear structure, scales listed, the picture is now complete. §8.1 is one dense paragraph doing five jobs (reference, runaway, L4 requirement, "prediction", outcome); split it. |

## Verdict

Gate 1 for L0, round 3: **not passed as written, by one sentence.**
- No fatal objection.
- One must-fix: R3-1, relabel the postdicted coalescence-law "prediction" in §8.1 and say where the result was already known.
- Four minor: R3-2 to R3-5, plus N12's one word in `L0_wolfram.md`.

All 13 round-2 objections and round-1 #10 are answered, except N12 (partly, minor). Once R3-1 is fixed, I see no reason for another full round: the gate can pass on a check of that one sentence.

## Round 3 fixes (checked only the changed text)

| # | Fix | Verdict | Evidence |
|---|---|---|---|
| R3-1 | §8.1 relabelled: "A known result that L0 explains, not a prediction". It cites the old study's 3 / 5 min and this study's 2.27 / 4.51 min, says both were computed before the paragraph, and says plainly that L0 holds no open prediction about nature, only the code test 8.2. | **answered** | It now matches the baseline row and `book-05`. The Weber-number reason is the one I checked (about 20 for 400 + 200 µm with Stokes speeds). Leftover wording, minor: the §8 heading still reads "Predictions that could come out wrong", and the runaway paragraph is still headed "Prediction for L4", although it is computed. The new last sentence of 8.1 makes the status clear, so I do not hold the gate on it. |
| R3-2 | Grid dependence stated: 3.51 / 3.65 / 3.72 / 3.86 min against the grid-free 4.0–4.1 min, with the reason. | **answered** | These are my numbers and my reason. |
| R3-3 | Slip: "applied to both drops it raises Δv(40/8 µm) by 0.20 %". | **answered** | Matches my +0.198 %. |
| R3-4 | §10 kept as the record of round 2; §11 and §12 supersede it. | **answered** | Acceptable for a contract's history. |
| R3-5 | 8.2 now gives 4000 runs (seeds 1–4000), pooling until each cell expects at least 5 runs, p > 0.01, and the mean within three standard errors. It now uses the extended kernel (Beard speeds, L2 table). Outcome: 8.246 ± 0.036 against the exact 8.221; χ² = 18.1 on 13 degrees of freedom, p = 0.15. | **answered** | The pooling rule in `checks/check_physics.py` (section 7) is the one stated. It builds the exact chain by matrix exponential from the engine's own rates, which is right for a test of thinning and bookkeeping. My independent exact chain with `physics.cjs` kernel (Beard, L2 table) gives mean 8.222 (s.d. 2.28), against the contract's 8.221. χ² = 18.1 on 13 d.o.f. gives p = 0.154, and \|8.246 − 8.221\| = 0.025 < 3 × 0.036. I did not see the 4000-run outcome line printed: my run of `check_physics.py` was stopped by the pause after its first checks, which passed (including E = 0.3444 at 40/8 µm). So the Monte Carlo outcome is consistent but not reproduced by me. |
| N12 | `L0_wolfram.md` item 4: "Wolfram's own antiderivative … differentiates back … the printed G of (L0.5) itself is checked by SymPy … not by this item." | **answered** | The file now says exactly what the Wolfram run shows. |

**Final Gate 1 verdict for L0: passed.**
- No fatal objection and no open must-fix: all of round 1, round 2 and round 3 are answered.
- Two cosmetic leftovers remain: the §8 heading and the "Prediction for L4" label.
- One item rests on the contract's report, not my rerun: the 4000-run outcome of 8.2.

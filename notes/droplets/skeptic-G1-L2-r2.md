# Skeptic, Gate 1, contract L2, round 2

Reviewed: `contract-L2.md` (round 2), `skeptic-G1-L2-r1.md`, `derive/L2_r2.cjs`, `derive/L0_r3.cjs`, `derive/L2_traj.cjs`, the kernel and
Hall-table code in `physics.cjs`, `data/hall1980.json`, and sections 6–7 of `dossier-fallspeed-efficiency.md`. I ran `L2_r2.cjs` (7 s) and
`L0_r3.cjs` (4 s). My own scripts are in `/tmp/claude-0/-home-user-SiteTest/de75440b-f270-5344-8ae7-923c4f178e24/scratchpad/`:
`sk3l_sce.cjs` (SCE with E = 1, own table, Hall's table), `sk3l_sce2.cjs` (droplet–droplet pairs), `sk3l_cross.cjs` (the whole table
regenerated at other crossover numbers, then the SCE), `sk3l_near.cjs` (near-equal weight with Hall's wake values).

## 1. Numbers the contract quotes, checked against the printouts

| Quoted in the contract | Printed? | Value |
|---|---|---|
| E(40, 8) = 0.344 / 0.358 / 0.399 / 0.485 at crossover 60 / 20 / 6 / 2 | yes, `L2_r2` | same |
| "Hall's 0.50 needs about 1.7" | **no** | my algebra from E_S = 0.33747, E_P = 0.83823, Re = 0.837: 1.74. Right, but not printed |
| Hall along r = 8 µm: "1.23 to 1.53 times ours" | **partly** | `L2_r2` prints 1.45, 1.53, 1.27, 1.28, 1.23, 1.25, **1.03** (200 µm), 1.33. The range is 1.03–1.53 (see N4) |
| 40/8: 0.344 vs 0.50; 50: 0.406 vs 0.62; 100: 0.550 vs 0.674; 300: 0.750 vs 1.0 | yes | same |
| p = 0.1, R = 50: 0.128 vs 0.40 | no (round-1 skeptic's number) | fine as a quote |
| Hovering: 40/8 S = 0.045, I = 0.039; all 12 pairs hover | yes | same |
| Near-equal weight 1.7 % / 1.4 % | yes | 1.66 % / 1.36 % |
| Prediction 3: 13.442 vs 13.470 min | yes | 13.442 / 13.470 |
| Prediction 2: 5.77 / 13.47 min | yes | 5.767 / 13.470 |
| Prediction 1: ×2.26 open cloud 40 → 100 µm | yes, `L0_r3` | 29.49 / 13.02 = 2.265 |
| ×2.47, closed box t₉₀ 11.03 → 27.24 min | yes, `L0_r3` | same |
| SCE ×1.69 (7.96 → 13.47 min) | 13.47 yes; **7.96 no** | 7.963 is in `contract-L1.md` (line 193); my `sk3l_sce.cjs` gives 7.963 |
| Band end t₉₀ = 11.4 min (Hall) | **no** cited script prints it | my `sk3l_sce.cjs`: 11.382 min. Right |
| "SciPy check gives E(40, 8) = 0.3442 against 0.3444" | **no** | round 1 reported 0.3444 against 0.3444. 0.3442 appears nowhere |

Every number that is quoted is right except 0.3442. Four of them (1.7, 7.96, 11.4, 0.3442) are not printed by the scripts the contract names.

## 2. Round-1 objections

| # | Verdict | Evidence |
|---|---|---|
| 1 Not superposition | **partly** | §3 is now right and clear. But §8 still says "Chosen: **superposition**". The code still labels the table `version: 'L2-superposition-1'` (`physics.cjs`, `makeTable`). The size of the dropped term is quoted with the sideways Stokeslet factor; on the axis it is twice that (N7). |
| 2 Flow field at Re ≈ 1–20 | **partly** | The crossover sensitivity is printed and called the weakest link. That is honest. Choosing not to compute a Navier–Stokes field is stated as a choice; that is acceptable here. But the band given for observable 1 (11.4–13.5 min) is narrower than the model's own sensitivity (N2). §9 says the "fails where" column now names Re ≈ 1–20. It does not: the no-wake row still says "collectors above about 150 µm". |
| 3 Langmuir K = 3–3.6 | answered | −10 % and −8 % shown, called unresolved. |
| 4 Table 4 | answered | Dropped as a check, with the reason. |
| 5 K = 0.2 label | answered | Reworded; unresolved. |
| 6 False bracket | answered in §3 | Withdrawn; Hall's 1.3–4.0 quoted; weight printed. I checked the weight with Hall's own wake-capture values in place of the clamp: 2.52 % at t = 0 and 1.56 % at 10 min (`sk3l_near.cjs`). The "small weight" argument holds. But §8 still lists "the p > 0.6 closure **with its bracket**" (N1). |
| 7 Hovering limit | answered | Criterion S > I(p) stated and printed for 12 pairs. |
| 8 On-off window and floor | answered | Called a model artifact; prediction 3 measures its effect (−0.2 %). |
| 9 Interception limit with S | **not answered** | §9 says the hovering row gives "(I − S)/(1 − S)". It does not; that formula appears only in §9 itself. §6 "Model limits" still gives only the S = 0 limit. The formula is right (I re-derived it from the stream function of a − S e_z). |
| 10 1/12 half derived | answered | "Local analysis plus numerics". |
| 11 Grazes missed | answered by statement | The code is unchanged; the error (≤ 3 × 10⁻⁴) is stated, which is enough at this size. The quoted SciPy value 0.3442 is wrong; it was 0.3444. |
| 12 Gap to Hall | **partly** | The quoted range leaves out the printed 1.03 at 200 µm. The "factor 3 at p = 0.1" understates R = 40 µm (0.009 against 0.07, a factor 8; small in absolute terms). Altitude offset stated. (N4) |
| 13 Prediction 1 cannot fail | **partly** | Replaced by derived factors, honestly labelled as results computed after round 1. Good. But the new "because" sentence is wrong for droplet–droplet pairs (N3). |
| 14 Prediction 2's "because" | answered | Removed; terms defined. |
| 15 Missing terms | answered, one row weak | Rows added for Basset, coalescence, set-up time and nonlinear drag. The steady-flow row's reasoning is off (N8); the conclusion stands. |
| 16 Alternatives | answered | "Chosen not to at this rung". |
| 17 OCR | answered | Stated. |
| 18 Stale files | answered | `L2_stc.cjs` gone; `L2_traj.cjs` no longer requires `physics.cjs`. |
| 19 Undefined terms | answered | Header defines them. |

Tally: 13 answered, 5 partly (1, 2, 12, 13, and 6 through the §8 leftover), 1 not answered (9, minor).

## 3. New problems in round 2

| # | Where | What is wrong | Evidence | Severity | Fix |
|---|---|---|---|---|---|
| N1 | §8 | §8 contradicts §3. It says "Chosen: superposition" and "the p > 0.6 closure with its bracket". Both were withdrawn in round 2. | Text, line 138. | must fix (two words) | "one-sided flow"; "the p > 0.6 closure (not a bracket)". Rename the table version string in `physics.cjs` when the code is next touched. |
| N2 | §3, §8 band | The band understates the model's own weakest link. §3 moves the crossover from 60 down to 2 at 40/8, but never carries that through to observable 1. §8 then gives the band as 11.4–13.5 min, which is only two runs: Hall's table and ours. | I regenerated the whole 64 × 40 table at each crossover. The stored table is reproduced to 5 × 10⁻⁷. SCE t₉₀: **13.47 (60), 12.60 (20), 11.48 (6), 10.49 (2) min** (`sk3l_cross.cjs`). Hall's 11.38 min sits at crossover ≈ 6. Crossover 2 matches Hall at 40/8, and it gives 10.5 min. Caveat: a low crossover also raises the small-collector floor (more potential-flow weight at Re ≈ 0.1), so some of the 10.5 is that artifact. | must fix (one sentence) | Print these four numbers from `L2_r2.cjs`. Then give the band as roughly 10.5–13.5 min, or keep 11.4–13.5 and say it is a two-model spread, not the full closure range. |
| N3 | §7 prediction 1 | "Smaller because collector–collector and droplet–droplet pairs … are less affected than capture." This is half wrong. Droplet–droplet pairs are the *most* affected: their E drops from 1 to about 0.001. | Table E at R = 10–20 µm: 0.0001–0.013. Put E = 1 back for collectors below 30 µm, keeping our table elsewhere: t₉₀ goes 13.47 → 12.69 min (`sk3l_sce2.cjs`). So they carry about 6 % of t₉₀, and they are slowed, not spared. Collector–collector pairs are less affected; that half is right (E(40, p ≥ 0.6) = 0.64 against 0.34 for capture). The likelier reason the SCE factor is smaller is the spread of collectors: the leading, larger collectors have E closer to 1. That is not tested. | must fix (one line) | Drop "and droplet–droplet", or drop the "because" and say the reason was not isolated. |
| N4 | §6 Hall comparison | The range "1.23 to 1.53" leaves out a printed ratio of 1.03 at 200 µm. The 200 µm value comes from a rule the contract never mentions. | At R = 200 µm, p = 0.04 lies below Hall's first column (0.05). `hallE` scales E linearly to 0 below p = 0.05, so Hall's 0.87 becomes 0.696. That rule is the code's choice, not Hall's, and it also enters the 11.4 min band end (every collector above 160 µm with an 8 µm partner). Hall's own values along r = 8 µm also jump about (0.62 at 50 µm, 0.57 at 60 µm) because the table steps sharply between p = 0.10 and 0.15. | should fix | Quote 1.03–1.53 and explain the 200 µm point, or stop at 150 µm. State the p < 0.05 rule as a choice in §3 or §8. At p = 0.1, say "up to a factor 8 at R = 40 µm (0.009 vs 0.07)". |
| N5 | §3, §5, §7, §8 | Some numbers are not printed by the scripts the contract cites, and one is wrong. | 1.7 (crossover), 7.96 (lives in contract L1), 11.4 (printed nowhere), 0.3442 (wrong; 0.3444). | minor | Add 1.7, 7.96 and 11.4 to `L2_r2.cjs`; correct 0.3442 → 0.3444. |
| N6 | §3 interpolation | "Hall's table, whose 40–300 µm block was computed by its sources with flow fields of intermediate Reynolds number (dossier §7)." Dossier §7 is Pinsky et al. Dossier §6, on Hall, names the sources (Schlamp et al., Lin and Lee, Shafrir and Gal-Chen) and says they used superposition, but not which flow field. | Dossier lines 352–357, 398–401. | minor (sourcing) | Point to where this is shown, or write "(by our reading; their flow fields were not opened)". My memory is that those authors used numerical Navier–Stokes fields of Le Clair et al. (1970); I did not check it. §8 leans on this claim ("mostly because of the flow field"). |
| N7 | §3 one-sided flow | The dropped term's size uses (3/4)(r/d)v(r). That is the sideways value of a moving sphere's far field. Straight ahead, on the line of motion, the factor is (3/2)(r/d) − ½(r/d)³. | 40/8: 0.011 U, not 0.006 U. 20/8: 0.068 U, not 0.035 U, against an approach speed of about 0.1 U. | minor | Quote "0.006–0.011 U at 40/8, 0.035–0.07 U at 20/8". It strengthens the contract's own verdict on R < 30 µm. |
| N8 | §5 steady-flow row | (R²/ν)/(R/U) = Re/2 is just the Reynolds number. It says whether inertia matters in the flow, not whether the flow is steady. A drop falling at constant speed has a steady flow in its own frame at any Re below wake shedding. "Marginal near Re ≈ 2" is therefore wrong. (Round 1 suggested this comparison; it was my predecessor's slip.) | The right test compares R²/ν with the time over which U changes: the collector's response time (about 20 ms) or its growth time (minutes). R²/ν = 0.09 ms, so the ratio is about 5 × 10⁻³ or less. | minor | Replace the row's argument with that comparison; the conclusion (steady flow) stands. |
| N9 | §5 interaction row | "Small collectors (R < 30 µm): our E is below 0.002 for most p." True only for R ≲ 16 µm. | Stored table: R = 20 µm, 0.001–0.013; R = 25 µm, 0.13–0.26 for p = 0.3–0.5, close to Hall interpolated between his 20 and 30 µm rows. | minor | "R ≲ 16 µm"; or describe 16–25 µm as the switching zone named in the hovering row. |
| N10 | §7 prediction 3 | It is labelled "could fail", but it was computed in the same round as the text. The contract does not say whether the 5 % threshold was fixed first. Prediction 1 is labelled honestly; this one should be too. | — | minor | One clause. |
| N11 | §5 hovering row | Readability. One table cell holds four ideas, and it says "fails where … hovers" while showing that 40/8 hovers too. That can mislead. The real separator is St close to its critical value, which the cell does say at its end. | — | minor | Move it into a short paragraph under §3. Put the separator first: hovering decides nothing where St is well above St_c. |

Downstream, not a contract fault, listed so it is not lost: the lecture text `text/book-03.src.html` still calls the method "superposition". It still says "0.1 to 0.2 below Hall's" and "doubling the distance changes E(40, 8) by less than 10⁻⁵" (with the event check it is 3 × 10⁻⁵). The `physics.cjs` comment still says "the near-equal bracket". These must follow the contract before the page is built.

Checks that came out right: the crossover numbers, the hovering numbers, the near-equal weight (and it stays small with Hall's wake values, 2.5 %), prediction 3, the L0_r3 factors, 7.963 and 11.38 min (recomputed), the (I − S)/(1 − S) limit (re-derived), and the dropped-term arithmetic as the contract defines it.

## 4. Thresholds

- **Motivated: pass.** The windscreen picture leads, and every ingredient is introduced for a reason.
- **Honest: fail, narrowly.** The round-1 honesty problems are fixed: the method's name, the false bracket, the skipped Langmuir points and the gap to Hall. Four new ones remain. §8 still says "superposition" and "bracket" (N1). The band is narrower than the model's own crossover sensitivity, by about 1 min of t₉₀ (N2). A printed ratio is left out of a quoted range (N4). §9 claims fixes that are not in the text (objections 2 and 9). Each is a one-line edit.
- **Derived: pass.** The new hovering criterion is derived and right. The prediction-1 factors come from a stated integral and are printed. 1/12 is labelled honestly.
- **Checked: pass, with one exception.** Every quoted number reproduces, apart from 0.3442. The exception is the "because" in prediction 1, which was never checked and is half wrong (N3).
- **Sourced: pass with minor fixes.** Hall's source flow fields are cited to the wrong dossier section (N6). Four numbers have no printout in the scripts the contract names (N5). OCR status is stated.
- **Readable: pass with minor fixes.** Short and plain. The hovering cell (N11) and the dense §3 interpolation paragraph are the hardest parts for a second-year student; a three-sentence paragraph each would fix them.

## 5. Gate 1 verdict

**Not passed in round 2, but close.** No new research computation is needed. Round 3 needs:

- text edits for N1, N3, N4 and N2;
- a few extra print lines in `L2_r2.cjs`: the four crossover t₉₀ values (my `sk3l_cross.cjs` takes about 2 min), Hall's 11.38 min, 7.963 min and the 1.74 crossover;
- the minor items (5, 6, 7, 8, 9, 10, 11 and objection 9's formula in §6), at the author's discretion.

A round-3 check should take minutes.

Not checked by me: Hall's and Langmuir's page images (not attempted again); the flow fields Hall's 40–300 µm sources used (my recollection only); E in a real Navier–Stokes field (out of scope by instruction).

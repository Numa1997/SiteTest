# Check of the step-by-step passages, round 3 (book-06 §6.3–6.4, book-09, book-10 §10.1–10.3)

Independent checker. Derivations in SymPy, numbers recomputed in Node from `physics.cjs` (air 283.15 K, 85 000 Pa) and from
`data/stochastic.json`, `data/bridge.json` (s16), `data/energy.json`. I also ran `checks/check_numbers.cjs`: 468/468 PASS. That
script only checks that the quoted strings appear; the verdicts below come from my own recomputation.
Scripts: scratchpad `c6.cjs`, `c2.cjs` and an inline SymPy session (not in the repository).

## 1. book-06 §6.3

| item | verdict |
|---|---|
| Method box "first drizzle drop", step 1 (fixed counts N V rounded) | CORRECT. `drawModes`: `n = Math.round(md.N*V*1e-6)` per mode. Measured: 301, 3010, 30100, 301000 drops. The cut is a redraw of z until \|z\| ≤ 3 (`do … while`). |
| step 1, seeds 1000 V + k | CORRECT. `run_stochastic.cjs`: `seed = 1000*V + k`. Stored seeds are 1001–1200, 10001–10100, 100001–100100, 1000001–1000030. |
| step 2, one hour | CORRECT. `tEnd: 3600`. |
| step 3, first passage after each merger | CORRECT. `gillespieRun` l.623 tests the merged drop `r[id2] >= th` after every accepted event and stores the event time once. There is also a t = 0 test (l.596); it never fires because the cut is 69 µm. |
| step 4, "The *median* is the time by which half the runs have had their first drop" | **WRONG (small)**. The code (`run_stochastic.cjs`, `check_numbers.cjs` `med`) takes `t[Math.floor(n/2)]`, the upper median: the time by which n/2 + 1 runs have had one. Recomputed: 10 cm³ gives 605.13 s (upper) against 604.85 s (true median). 100 cm³ gives 286.23 against 285.50. 1000 cm³ gives **174.63 against 174.33 s**, and 15 of 30 runs have had one by 174.03 s. So "175 s in 1000 cm³" should be 174 s under the stated definition. The "(6.1) 175 vs exact 175" match then becomes 175 vs 174. Fix: use the true median `(t[n/2-1]+t[n/2])/2`, or define the median as the code computes it. |
| Example 6.2 steps 1–5 (69.12 µm; W = 8.050e-4; E = 0.477; Δv = 0.4231 m/s; 3.035 and 5.556 µm/min; 448 s; 1312) | CORRECT. Recomputed: W = 8.0499e-4 (uncut droplet mode). E(69, 8/69) = 0.47709, Δv = 0.42306, rates 3.0351 and 5.5562 µm/min. Euler at 0.05 s gives 447.85 s, a fine midpoint step 447.81 s. (100³ − 69³)/8³ = 1312.0. dR/dt = (1.1)/(4πρ_wR²) matches (1.1) in book-01 and the code. Note: W is the uncut mode, about 1 % more than the cut mode holds; that is harmless for a best case. Step 4 starts at 69 µm, step 1 at 69.12 µm. |
| Example 6.2 step 6: "Captures arrive at random, independently, so their number in a given time is Poisson-distributed, and its relative spread is 1/√1312 = 2.8 %." | **WRONG (reasoning; conclusion survives)**. The capture rate grows with every capture (the collector grows), so this is a pure-birth process, not a Poisson process. The right quantity is the arrival time T = Σ τ_k with τ_k ~ Exp(λ_k) and λ_k = 4πR_k² (dR/dt)/v_8. Recomputed: mean 448.2 s, sd 13.3 s, **relative spread 2.97 %** (not 2.8 %). A 3σ-lucky collector arrives 8.9 % sooner. Taken as a 3σ excess in captures it is 4.6 % sooner. "About a tenth sooner" and "7.5 minutes" therefore stand. Corrected sentence: "Each capture waits an exponential time at a rate that grows as the collector grows; summing these waits, the arrival time scatters by 3.0 %." |
| "So capture alone … needs 7.5 minutes … The exact runs in 1000 cm³ make the first drizzle in three" | CORRECT (448 s = 7.47 min; 174–175 s). |
| Three steps to (6.1) | CORRECT. SymPy: lim (1 − x/J)^J = e^{−x}; e^{−x} = ½ ⇒ x = ln 2. Units: n_100 [m⁻³] × V [m³] is dimensionless. Limit V→0: P→1. |
| (6.1) "P(no 100 µm drop in V **by** t) = e^{−V n_100(t)}" | CORRECT with a gap. The steps give "at t". For a single volume "at t" equals "by t", because a drop ≥ 100 µm only grows. But the mean-field n_100(t) later falls (large drops merge), so e^{−Vn_100(t)} would rise again. The box's "largest value so far" is the patch, and it is not derived. Unjustified step (see list). |
| "Two assumptions … rare (step 1) … independent (step 2)" | Unjustified attribution. Step 1 needs only small enough pieces, which J→∞ supplies at any density. Rarity is not used. What is used is independence (no exclusion, no clustering). |
| Method box "the prediction (6.1)" step 1 | CORRECT. `run_bridge.cjs`: `makeGrid(16, 4e-3)`, `dt: 1`, `recordEvery: 5`, `trunc: 3`. `sceRun.record`: `N100 = Σ_{k≥k100} N[k] + over.N`, with k100 the first bin with r ≥ 100 µm. |
| step 2 (largest value so far) | CORRECT in effect. `run_bridge.cjs` and `check_numbers.cjs` `bridgeMed` use the first record with V·N100 ≥ ln 2 on the raw series. Example 6.3's check and `tailMed` use the running max. For a first crossing the two are identical, and I confirmed the same times (60/175/280 s). Note: the comment in `run_bridge.cjs` says "for 20 min" but tEnd = 3600. |
| step 3 | CORRECT (ln 2 = 0.693). |
| Example 6.3 | CORRECT. 0.693/1e-3 = 693.1. First record ≥ 693 is at 175 s with 744.485. Threshold 6931 is reached at 280 s (7107.95). Threshold 0.693 at 60 s (0.9732). |
| "the smooth-growth bookkeeping of the thesis (5.2)" (end of §6.3) | **WRONG reference**. (5.2) is the moment identity (book-05, and used as such in §10.1 step 3). The thesis bookkeeping is the collector/pool scheme of §5.x (`gceRun`). Fix: name that section, or drop "(5.2)". |

## 2. book-06 §6.4

| item | verdict |
|---|---|
| Step 1 ½Kc²V = (K/V)·½n² | CORRECT (c = n/V). |
| Step 2 ½n(n−1) | CORRECT. |
| Step 3 ratio (n−1)/n | CORRECT. |
| Step 4: Poisson ⇒ ⟨n(n−1)⟩ = n̄² | CORRECT. SymPy: Σ n(n−1) λⁿe^{−λ}/n! = λ². This is the second factorial moment. So ⟨½n(n−1)⟩ = ½n̄², exactly the equation's count. |
| Step 4: "Our volumes hold exactly V collectors each" | CORRECT. `drawModes` gives round(10⁶·V·10⁻⁶) = V collectors. Symbol clash: V here is the number of cm³, while in (6.1) V is in m³. |
| Pair table | CORRECT (0.5/0/0; 50/45/0.900; 5000/4950/0.990; 500 000/499 500/0.999). |
| F40 table | CORRECT. Recomputed means at t = 0: 0.1524, 0.1876, 0.1946, 0.1961; collection equation (bridge s16) 0.1969. At 10 min: 0.5204, 0.6955, 0.7303, 0.7398; collection equation 0.7418. |
| "From 100 cm³ upward the gap is a few thousandths, the size of the pair deficit." | **WRONG for 100 cm³ at 10 min**. The gap is 0.7418 − 0.7303 = **0.0115**, a hundredth, with standard error 0.0035. A 1 % pair deficit is 0.0074 of 0.742. Only 1000 cm³ (0.002 ± 0.002) is "a few thousandths". Correct form: "In 100 cm³ the gap after 10 min is 0.012, in 1000 cm³ 0.002." Also, the start gaps (0.009 in 10 cm³) cannot come from pair counts, because no merger has happened at t = 0. They are the averaging-of-ratios effect the method box names. |
| Method box "average growth" steps 1–3 | CORRECT. `recordEvery: 60`; F40 = Σ_{r≥40 µm} m / mass0 per run (`gillespieRun.record`); plain average over runs. 200/100/100/30 runs. Mean field from bridge.json s16 (same cut modes). |
| "equal weighting … why the 1 cm³ curve starts below" | CORRECT in part. Recomputed for 1 cm³ at t = 0: mean of ratios 0.152, ratio of sums 0.175. The remaining gap to 0.197 is sampling of 200 single collectors. |
| Fig. 6.2 caption: "starts lower (0.15) because its single collector … is smaller than 40 µm about half the time" | Unjustified. The mean field also has half its collectors below 40 µm. The real reason is that F40 = M_c/(M_c + M_d) is concave in M_c, so equal-weight averaging lowers it (the box's own explanation). |

## 3. book-09

| item | verdict |
|---|---|
| e_s = 1227.2 Pa (Bolton) | CORRECT (1227.17). It is the same formula as `growthG`. |
| q_s = εe_s/(p − e_s) = 9.111 g/kg, ε = 0.622 | CORRECT (9.1114). Note: this is a mixing ratio, per kg of *dry* air, not "per kilogram of air". |
| step 2 c_p dT + g dz + L dq_s = 0 | CORRECT. |
| g/c_p = 9.76 K/km | CORRECT (9.758). |
| Γ_m = g(1 + Lq_s/(R_dT))/(c_p + εL²q_s/(R_dT²)) = 4.98 K/km | CORRECT formula (the standard AMS saturated-adiabatic form) and value 4.980. SymPy: with dq_s = q_s[L dT/(R_vT²) − d ln p] and d ln p = −g dz/(R_dT), step 2 gives exactly this Γ_m (difference 0). The derivation as written is incomplete. "Differentiating q_s (Clausius–Clapeyron)" gives only the denominator's εL²q_s/(R_dT²). The numerator's Lq_s/(R_dT) comes from the falling pressure (hydrostatics plus ideal gas), which is not mentioned. It also uses q_s ≈ εe_s/p, while step 1 uses p − e_s. |
| step 4 dq_s/dz = (c_pΓ_m − g)/L = −1.939 g/kg/km; ×1.0458 = 2.028 g/m³/km | CORRECT (−1.9384 with L = 2.477e6; ρ_a = 1.04579). Sign checked. |
| step 5 0.061 and 0.243 g/m³ | CORRECT (0.0608, 0.2434). |
| step 6 collection 0.036 g/m³; "two to seven times" | CORRECT (energy.json warm recs, ≥ 20 µm water gained in 60 s). Ratios 1.7 and 6.8, so "two" is generous. |
| "a rising cloud condenses 0.06 to 0.25 g/m³ of new water per minute" (callout) | **WRONG (rounding)**. 0.243 rounds to 0.24. `check_numbers.cjs` deliberately rounds up (`Math.ceil`). Correct: "0.06 to 0.24 g/m³". |
| Table row 1 (t50, t90) | CORRECT: two-bin, 8 bins/doubling, 1 s (book-05). Tests: Golovin, NumPy solver, 4→8→16 bins, Δt halved twice (book-05, checks page). |
| Table row 1 spread | CORRECT. Crossover 60→2 and Hall's table (book-05). The runs are in chapter 5; "(chapter 3)" names only where the crossover is defined. SciPy E(40, 8) = 0.3442 vs 0.3444 (checks page). |
| Table row 2: "exact simulation by thinning, 230 runs" | **WRONG**. The ensemble is 430 runs (200 + 100 + 100 + 30; the checks page says "0 times in 430 runs"). 230 is the number that *made* a 100 µm drop. Correct: "430 runs (230 of them made a drizzle drop)". The tests (capture chain of 4000 runs, χ² p = 0.15; (6.1); Kolmogorov–Smirnov p = 0.42/0.40) exist on the checks page. |
| Table row 3 (ice) | CORRECT: all pairs summed once (`run_cold.cjs` double loop i ≤ j); collision energies against the fitted range (book-08). |
| Table row 4 (energy) | CORRECT: surface rose in 0 of 3600 steps (energy.json `rises` = 0); (10.9) stored vs summed; classes vs drawn drops (checks page). |
| Table row 5 (place) | CORRECT: 50 m cells (book-12); super-droplets vs collection equation (5.873/13.716 min); "evenly spread air stays even" (drift check). |

## 4. book-10 §10.1–10.3

| item | verdict |
|---|---|
| (10.1), 4π(3/4π)^{2/3} = (36π)^{1/3} | CORRECT (SymPy: cube = 36π). Units: J/m² × m²/kg^{2/3} × kg^{2/3} = J. |
| (10.2) and the sign argument | CORRECT (SymPy difference 0; x^{2/3} > x on (0,1)). |
| (10.3) | CORRECT. It is (5.2) with φ = σ(36π)^{1/3}ρ_w^{-2/3}m^{2/3}, and the factor ½ of (5.2) is carried. Units: J m⁻³ s⁻¹. Limit: K→0 or one drop gives dF/dt = 0. |
| Equal drops 1 − 2^{−1/3} = 20.6 % | CORRECT (0.20630). |
| (1 + p³)^{2/3} − 1 = ⅔p³ − ⅑p⁶ + … | CORRECT (next term +4/81 p⁹). |
| share destroyed 1 − ⅔p + ⅑p⁴ − … | CORRECT (SymPy: 1 − 2p/3 + p⁴/9 − 4p⁷/81). At p = 0.2: 0.866844, and the exact value is 0.866844. |
| Example 10.1 | CORRECT: 40.1064 µm; 2.011e-8, 8.042e-10, 2.021e-8 m²; 6.972e-10 m², 86.7 %, 86.68 %; σ = 0.074221 gives 5.174e-11 J. Ratio to 3.043e-14 J is 1700. |
| Example 10.2 | CORRECT: e^{2 ln²1.25} = 1.1047; 8.408 µm; 1.978e-2 and 1.595e-3 J/m³; 0.0214, 92.5 %; collector water 27.9 % ("28 %"). Uses uncut modes, as the chapter-5 run does (`run_energy.cjs` calls `lognormalBins` without trunc). |
| Method box "free energy in the run" step 1 | CORRECT. `sceRun` l.450–452 computes `surfaceSum` before and after each `sceStep`; `surfaceSum` = Σ N_k x_k^{2/3} + overS; the overflow adds C·x_s^{2/3} (`sceStep` l.400); SURF = (36π)^{1/3}ρ_w^{−2/3}. dt = 1 s, s = 8 (chapter 5's grid). The multiplication by σ·SURF is applied for the stored E_s (`ES*surfaceSum`); the rise test compares raw sums, which is equivalent. |
| step 2 | CORRECT (`ledger.rises`; energy.json rises = 0, maxRise 0). |
| step 3 | CORRECT (`ledgerAdd`: released += C(x_i^{2/3} + x_j^{2/3} − (x_i + x_j)^{2/3}) into channel (cls j, cls i)). |
| (10.4) and the entropy books | CORRECT: u_s|ΔA|/T + (dσ/dT)|ΔA| = σ|ΔA|/T. |
| Example 10.3 | CORRECT: dσ/dT = −1.4560e-4; 0.0412; 0.1154 J, 1.555; 8.048e-11 J; drop of 2.702e-10 kg; 7.105e-5 K; 2.842e-13, 1.015e-13, 1.827e-13 J/K; 1.324e10 k_B. Lamb r²/5ν at 40 µm = 2.45e-4 s. |
| §10.2 "In our cloud": 0.033 J, 7.5e-5 J/K, 1.8e10 k_B, 2.3 %, 28 s | CORRECT: totRel × 1.5554 = 0.03292; totRel/T = 7.48e-5; 1.80e10; maxRatio × u_s/σ = 2.32 % (the stored maxRatio, 1.49 %, is the free-energy ratio and the text correctly multiplies it); E_s0/P_g0 = 28.05 s. |
| Method box "three powers" step 1 | CORRECT. `figs.cjs` energyflow: `(Es[i−1] − Es[i])/Δt · u_s/σ` on records every 10 s (`recordEvery: 10`); u_s/σ = 1.5554. |
| step 2 | CORRECT: Σ N_k x_k g(1 − ρ_a/ρ_w) v_Beard(r_k) + overflow at the mean mass (`run_energy.cjs` onRecord). 7.620e-4 W/m³; collectors 87.79 %. |
| step 3 | CORRECT in value (ρ_aε = 1.04579e-2). Note: `figs.cjs` draws `E.warm.rhoEps \|\| 1.0458e-2`, and energy.json has no `rhoEps`, so the line is a typed constant, not computed from `A.rho`. |
| Sackur–Tetrode value; Example 10.4 | CORRECT: m = 2.145e-12 kg; 2πmk_BT = 5.268e-32; λ = 2.887e-18 m; 1/n = 3.322e-9 m³, cube 1492 µm; λ³ = 2.406e-53; ratio 1.381e44; ln = 101.64, +2.5 = 104.14; 1.324e10/104.14 = 1.27e8. "Some three hundred times smaller than a proton" holds for the proton's charge *radius* (0.84 fm / 2.887e-18 m = 291); against its diameter it is about 580. |
| Three-step origin of S, and the 5/2 | CORRECT in result; one step muddled. SymPy: with F = −k_BT ln[(V/λ³)^N/N!], S/Nk_B − ln(V/Nλ³) = 5/2 and U = (3/2)Nk_BT. So 1 comes from 1/N! via Stirling, and 3/2 is U/T, the "motion". The middle step says "each have V/N to themselves, and the number of arrangements is about (eV/Nλ³)^N". If each particle really had its own V/N, the count would be (V/Nλ³)^N with no e and no 1/N!. The e appears only when each particle ranges over all of V and the count is divided by N!. Correct form: "N identical particles each range over all of V: (V/λ³)^N arrangements, divided by the N! swaps, ≈ (eV/Nλ³)^N." Also, "S = k_B ln(arrangements)" with this count is ln Z, not S. The +3/2 is exactly S/k_B − ln Z = U/k_BT, which the text calls "the motion adds". Acceptable at this level. |
| "A merger destroys one drop's worth of it, 104 k_B" | Approximate. ∂S/∂N = k_B[ln(V/Nλ³) + 3/2] = 103.1 k_B (SymPy). This is irrelevant to the 10⁸ margin. |

## Unjustified steps
1. §6.3: the switch from n_100(t) to its running maximum in (6.1) is a patch for the failure of independence once large drops merge, not a consequence of the derivation.
2. §6.3: "rare" is attributed to step 1, but step 1 does not use it.
3. Example 6.2 step 6: Poisson statistics claimed for a self-accelerating capture chain.
4. Example 9.1 step 3: the pressure-change (hydrostatic) term that produces the numerator of Γ_m is not stated; q_s ≈ εe_s/p is used silently.
5. Fig. 6.2 caption: the reason given applies equally to the mean field.
6. §10.3: "each have V/N to themselves" contradicts the 1/N! count that produces the e.

## Symbol clashes
- ε: R_d/R_v (Example 9.1) vs dissipation rate (§10.2 method, ch. 7) vs spectrum error (ch. 11, checks page).
- V: volume in m³ in (6.1) vs a number of cm³ in "exactly V collectors" and the seed 1000 V + k.
- n: collector count (§6.4) vs n_100 concentration vs size distribution n(m) in (10.3) vs number density in Example 10.4.
- N: mode concentration vs bin numbers N_k vs particle number in Sackur–Tetrode.
- x: share m/(m + m') in (10.2) vs bin mass x_k in the method box right after it.
- σ: surface tension vs σ_g, and the velocity spread of ch. 12.
- (5.2): called "bookkeeping of the thesis" in §6.3, but it is the moment identity.

## WRONG items
1. book-06 method box §6.3 step 4: the code's "median" is the upper median, `t[floor(n/2)]`. Under the stated definition the 1000 cm³ median is 174 s, not 175 s; 10 cm³ is 605 s and 100 cm³ is 286 s (rounded).
2. book-06 Example 6.2 step 6: "Poisson-distributed … 1/√1312 = 2.8 %" is wrong. Captures form a pure-birth chain; the arrival-time spread is 2.97 %, and 3σ luck gives about 9 % sooner. The conclusion stands.
3. book-06 §6.3 end: "the smooth-growth bookkeeping of the thesis (5.2)" is the wrong reference, since (5.2) is the moment identity.
4. book-06 §6.4: "From 100 cm³ upward the gap is a few thousandths". At 100 cm³ after 10 min the gap is 0.012 ± 0.004.
5. book-09 callout: "0.06 to 0.25 g/m³" should be 0.06 to 0.24 (0.243).
6. book-09 table row 2: "230 runs" should be 430 runs, of which 230 made a drizzle drop.

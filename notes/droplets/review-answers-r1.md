# Answers to the round-1 reviews of Part IV (24 October 2026)

Reviews: `review-physics-ch10-11.md` (physics), `review-intent-ch10-11.md` (intent and teaching). Part IV is now three chapters:
10 Energy and entropy of merging, 11 Who eats whom, 12 A cloud with a shape. Numbers: `checks/check_numbers.cjs` 235/235,
`checks/check_physics.py` 14/14, browser check PASS at 360/390/1024/1440 px.

## Physics review
1. Ventilation missing (fatal): added, f_v from Pruppacher and Klett 13-60/61 (`physics.cjs` ventilation); (12.4) restated; times requoted
   (100 µm lasts 205 s; 150 µm vanishes on the way; 200 µm arrives with 41 %); the case without ventilation is reported (21.3 % against 13.6 %).
2. "More edge, less rain" confounded (fatal): the mean motion now comes from a stream function solved with psi = 0 on the outline (12.2), so
   it never crosses it (checked: zero wind at every sampled point outside four outlines). Shape is tested at fixed area with outlines drawn
   by chance (seven distinct outlines, 0.64 km², r = −0.91, −1.9 points per km/km²); the named shapes are shown but not used as the test.
   Exit routes are logged separately (below the base; through sides and top). The ladder rungs show which effect does what.
3. Drift (major): the full 2-D drift with the mean-flow term, derived with SymPy (`derive/L10_drift.py`, residual 0) and implemented;
   "exact" is now said only of the OU part. Mixing test: 4 seeds, two times, and a no-drift control (χ² 0.83–1.19 against 15.3).
4. Eddy strength set by the cell (major): σ² = (ε L_e)^(2/3) with L_e an explicit parameter; sensitivity runs L_e = 50/100/200 m (rain
   20.5 / 13.6 / 4.7 %); the text calls it the least certain number; C0 cited (Sawford 1991); crossing trajectories named as a price.
5. Convergence claim false (major): new box tests, 32 seeds each at 32/128/512 and 12 at 2048 per cell; our 128 result (+0.1 ± 2.1 %) quoted
   beside the reviewer's (+6.0 ± 1.6 %), "together about 4 %"; the γ > 1 share (44–46 %) disclosed; Δt independence stated.
6. Undisclosed turbulent kernel (major): separate rows, "ε peaked, stochastic element only" (11.2 %) and "+ turbulent collision factor" (11.4 %).
7. Free energy against energy (major): σA is the surface free energy; heat u_s = σ − T dσ/dT = 1.56 σ; warming 7.1e-5 K; (10.4) written
   ΔS = −ΔF/T with the sign right; heat/gravity ratio 2.3 %; (11.1) uses ΔF.
8. Overclaims (major): "never the reverse" replaced by "no thermal fluctuation splits a drop; breakup needs mechanical work, outside this
   box"; "one drop" restricted to the model.
9. Metropolis (major): 11.1 says the uniform proposal is an extra assumption, no splits are proposed so it is not equilibrium sampling, and
   the same acceptance with collision-weighted proposals reproduces the cloud; "one model" softened to "coincide".
10. Sources (major): Menon and Pego Theorem 5.1 and Remark 5.3 read (arXiv nlin/0306047), qualifiers added (collection equation, after
   rescaling, weak sense); Thomson's drift derived here; the other sources stay marked "not reread", per source.
11. Edge per area (major): Crofton perimeter (`physics.cjs` perimeter): cumulus 4.29, disc 4.43, box 5.00, tower 6.26 per km.
12–23 (minor): the born flag now means "contains collector water", propagated in both branches; merger counts taken before the split;
   cloud.json from one code version (all cases rerun); births weighted by water; variance, not "scatter"; true medians (6292, about 29 930);
   "rare by count, large in water" with both columns; standard errors and significance stated; the "counts stay whole" claim removed;
   vapour budget, base updraft and condensation named as prices; problem 6 kept at its physical point (splits need 10^12 K), splits not built.

## Intent review
1. Energy, entropy and place never meet (fatal): chapter 12 runs the ledger by region (core, flank, edge band, clear air, below the base):
   water by class, diet, free energy released, distance from greatest entropy, and the fate of water by starting place (fig. 12.6).
2. Energy idea not in its strongest form (major): chapter 10 writes F = E − TS with the drops' own entropy (104 k_B per drop against
   1e10 per merger) and builds the vapour channel, ripening, as an explicit gradient descent of the free energy (10.5–10.7), run for a day.
3. Outline crossed by the wind (major): fixed as physics 2.
4. Hidden change (major): fixed as physics 6.
5. Stochastic element not shown (major): figure 12.1 (paths with and without eddies), panel 4 "Follow one drop" trail, arrows only where the
   wind blows; the price (no puffs) stated.
6. Ladder (major): section 12.4, four rungs with their numbers and figure 12.2.
7. Mergers against water (major): the ledger table has both columns; figure 11.3 on a linear axis.
8. Chapter 10 too long (major): split into chapters 10 and 11; numbers rounded; the Jensen aside removed from the student text.
9. Panel 5 (major): volume choice and the three rules' size spectra; a note on splits (a temperature control is not built).
10. Phone canvas (major): drawn at its displayed size times devicePixelRatio; labels outside the canvas; dots at least 2 px.
11–18 (minor): 11.3 retitled; ε no longer names the spectrum error in Part IV, ζ for the random numbers; the status bullet removed; variance
   wording; fig. 11.5 runs left to right; one name per rule; problem 8 for chapter 12; a panel speed choice.

## Still open
- Picture data for the mean motion (L11) is not built; chapter 12 says so.
- Turbulence at contact scale (L9) is not built.
- Puffs (a stochastic field rather than per-drop eddies) are not built; stated as a price.

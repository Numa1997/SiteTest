# Independent physics review: chapters 10 and 11, problems 6 and 7 (Droplet Collection)

Reviewer: independent physics referee (Claude), 23 October 2026. Scope: `portfolios-src/droplets/text/book-10.src.html`,
`book-11.src.html`, problems 6–7 in `problems.src.html`, and the L8 and L10 code in `physics.cjs`, `tools/run_energy.cjs`,
`tools/run_cloud.cjs`, `tools/figs.cjs`, `checks/check_numbers.cjs` and `checks/check_physics.py`. I did not read `notes/droplets/`.
Scratch scripts and outputs are in
`/tmp/claude-0/-home-user-SiteTest/de75440b-f270-5344-8ae7-923c4f178e24/scratchpad/review_phys/`. They are `derive.py` (SymPy),
`mix.cjs`, `box.cjs`, `cloudrun.cjs`, `evsplit.cjs`, `orig_box.cjs`, `phys_mod.cjs` (an instrumented copy of the model with options for
the drift, ventilation and the exit route), plus the figure screenshots and the two primary sources I read (`src/mp.txt`, `src/shima.txt`).

## Verdict

| criterion | verdict | one-line reason |
|---|---|---|
| derived | **FAIL** | (11.2) as written is the 1-D Thomson drift and does not satisfy the well-mixed condition in 2-D (shown with SymPy). (11.3) has no ventilation. (10.4) has the wrong sign, and the heat is computed from the free energy. |
| checked | **FAIL** | The check scripts confirm that each number in the text matches the data files, but not the physics. The claim "128 super-droplets within 2 %" is false (+6.0 ± 1.6 % in t90, 64 seeds). "Edge per area" comes from a 25 m staircase count. cloud.json mixes outputs of two code versions. |
| honest | **FAIL** | The "eddies strongest in the core" case also switches on Ayala's turbulent kernel, and the text does not say so. The edge-loss mechanism is asserted, not measured. "The end state of a closed cloud is one drop" and "never the reverse" overclaim. The key sources are marked "not reread". |
| sourced | **FAIL** | Menon–Pego, Shima, Thomson, Rogers–Yau, Jaynes and Lamb are all cited "not reread". σ² = (εh)^{2/3} and C₀ = 6 have no source. Thomson is cited for a form that is not his 2-D solution. I checked Menon–Pego and Shima myself: the text's use of them is essentially right. |
| statistically sound | **FAIL** | The three-seed SEs are computed correctly and the main shape differences are significant within the model. But the SDM convergence claim rests on too few runs and is wrong. The well-mixed statistic is a single seed and a single time after a stratified start, with no null distribution. Confidence intervals ignore 2 degrees of freedom. |

The energy and entropy algebra of chapter 10 is mostly right, and its numbers reproduce. Chapter 11 is not ready. Its headline
interpretation, that edge per area sets the rain share, is not supported once the confounds are measured, and its rain shares carry a
systematic bias of about 10 percentage points from the missing ventilation. That bias is larger than every difference between shapes in
the table.

## Objections

### Fatal

**1. Ventilation is missing from the evaporation law. The rain at the ground is biased high by about 10 percentage points, more than any difference between shapes.**
Evidence: `growthG` and the evaporation step (physics.cjs:654–658 and 720–724) use dr²/dt = 2GS with no ventilation factor. A 100 µm drop
falls at 0.728 m/s (vBeard at 850 hPa) with Re = 8.6 and X = Sc^{1/3}Re^{1/2} = 2.50. Beard and Pruppacher (1971), as given in Pruppacher
and Klett eq. 13-61, then give f_v = 0.78 + 0.308X = 1.55. f_v is 1.12 at 50 µm and 1.00 at 10 µm. I integrated single drops falling the
300 m from the base:
- Without ventilation, a 150 µm drop reaches the ground with 33 % of its mass.
- With ventilation it evaporates completely.
- A 200 µm drop arrives with 74 % of its mass without ventilation and 41 % with it.

I reran the reference cumulus (seed 1001) with f_v added (`evsplit.cjs`, option `vent`). Rain fell from 33.0 % to 23.2 %. For the tower
it fell from 22.1 % to 14.4 %. The table's whole spread across shapes (22.3–32.6 %) is the same size as this bias.
The 257 s quoted for a 100 µm drop is therefore an upper bound, about 205 s with ventilation.

Fix: multiply 2GS by f_v(r) (Pruppacher and Klett 13-60/13-61) in makeCloud. Rerun all cases and restate (11.3) as dr²/dt = 2 G S f_v.
Requote 2.6/257/412 s, adding a sentence on ventilation, and rewrite the table.

**2. "The more edge a cloud has for its size, the more water it loses" is not what the runs show. Shape is confounded with cell geometry and cloud-base exits.**
Evidence:
- **(a) Without the stochastic element, rain does not follow edge per area at all.** It is tower 51.0 %, cumulus 46.5 %, disc 43.3 %
  (41.7 % with seed 1002) and box 39.0 % (38.8 %). The tower has the most edge and rains the most (`cloudrun.cjs`, `ns2.txt`). The
  baseline before eddies is set by the shape of the cell, which differs per shape:
  - cell width/height 1.07, 1.00, 1.00 and 0.41;
  - cloud top 1350, 1151, 1100 and 1400 m;
  - area 0.87, 0.64, 0.64 and 0.49 km².
- **(b) The mean flow crosses the cloud edge for two shapes and not for the others.** The cell fills the bounding box: 26.3 % of the
  cumulus cell and 21.0 % of the disc cell lie in clear air, and 0 % for the box and tower. So for the cumulus and disc the mean flow
  itself carries cloudy air across the fixed mask, where its droplets evaporate in seconds. The air then re-enters "saturated" with no
  drops. For the box and tower the streamlines close inside the cloud, and their strongest downdraft sits exactly on the cloud edge.
- **(c) A third or more of "evaporated" is loss below the cloud base, not loss through the edge.** I split the evaporated water by height
  (seed 1001). The box lost 35.7 % below z = 300 m and 35.3 % above. The cumulus lost 28.4 % below and 35.7 % above. So the box and the
  cumulus lose the same share through their sides and top. The box rains 8 points less because more of its rain evaporates below the
  base, not because it has more edge.
- **(d) The eddies cut rain by the same amount in three of the shapes.** From no eddies to eddies (seed 1001), rain falls by 13.4 points
  (cumulus), 13.6 (disc), 14.2 (box) and 28.9 (tower). Edge per area does not order the first three.

Fix: design a controlled comparison and measure the exits.
- Use one cell geometry, or none, for every shape. Or fit the cell to each shape, so that the streamlines never cross the mask.
- Hold area and depth fixed while varying the outline.
- Log the exit route (side or top versus base) and the evaporation below the base separately.
- Rewrite 11.3 to claim only what those runs show. Until then, remove "the more edge … the more water it loses that way" from 11.3 and
  from the chapter 9 summary.

### Major

**3. Equation (11.2) is the one-dimensional Thomson drift. In 2-D it violates the well-mixed condition, and it omits the mean-flow term.**
Evidence: SymPy (`derive.py`) puts p = N(u′; σ²(x,z)) into the stationary Fokker–Planck equation for (x, u′), with dx = (U + u′)dt and
steady, divergence-free U = (ψ_z, −ψ_x).
- The code's component-wise drift ½∂ᵢσ²(1 + uᵢ′²/σ²) leaves a nonzero residual. It contains u_x u_z²∂_xσ², u_x²u_z∂_zσ² and
  (U·∇σ²)(2σ² − |u′|²) terms.
- The correct drift is aᵢ = ½∂ᵢσ² + uᵢ′[(u′ + U)·∇σ²]/(2σ²), plus the −C₀ε u′/(2σ²) damping. Its residual is exactly 0.
- Dropping only the U·∇σ² term leaves −(U·∇σ²)(2σ² − |u′|²)/(2σ⁴), so the mean-flow coupling is not legitimate in general.

The coupling is small here. The ratio U·∇σ² / (σ²/T_L) is about 2 % for the peaked ε field. In my runs (`mix.cjs`) the code drift, the
full drift and the full drift with U agreed to within the test's noise: χ² per cell 0.79/1.11/0.82 at 30 min and 0.96/0.88/1.08 at
120 min, and the core density was 0.98–1.05 of the mean. With no drift at all, χ² was 2.09 at 30 min and 8.31 at 120 min. So the test
does detect the leading term, but it cannot detect the omitted ones.

Fix: print the correct 2-D drift in (11.2), which adds one term, and implement it in physics.cjs:705–706. State that it is first order
in time while the OU part is exact. Say "updated exactly" only of the homogeneous part.

**4. The stochastic element's strength is set by the arbitrary cell size h, and eddies between 50 m and the cloud scale are missing.**
Evidence: σ² = (εh)^{2/3} and T_L = 2σ²/(C₀ε) give a diffusivity K = σ²T_L = ⅓ε^{1/3}h^{4/3}.
- Doubling h to 100 m multiplies K by 2.5.
- This form is a sub-grid closure for Lagrangian dispersion inside an LES (Weil, Sullivan and Moeng 2004, J. Atmos. Sci. 61, 2877),
  where the resolved field carries the larger eddies. Here the only resolved motion is one laminar cell.
- Eddies of 100 m to 1 km carry most of the turbulent energy (σ² ∝ ℓ^{2/3}: 2.9 m²/s² at 500 m against 0.63 at 50 m) and most of the
  edge mixing. They are absent.

Yet the eddies are the largest single effect in the table (46.1 → 32.6 % rain). Calling σ² = (εh)^{2/3} "a standard choice … uncertain by
tens of percent" understates the problem. A K41 spectrum with C_K = 1.5 gives a sub-h variance per component of 0.44–1.05 (εh)^{2/3},
depending on whether the cutoff is π/h or 2π/h, and the missing scales are a factor of order h^{4/3} in K, not tens of percent.

Fix:
- State that K scales as h^{4/3} and that the larger eddies are absent.
- Run h = 25 and 100 m, or K at the cloud scale, and report the rain share's sensitivity.
- Cite a source for σ² and C₀: Sawford (1991, Phys. Fluids A 3, 1577) or Pope (2002) for C₀ ≈ 6, and Weil et al. (2004) for the closure.
- Add the crossing-trajectories effect (Csanady 1963). Drizzle falls at 0.7–1.5 m/s against σ = 0.79 m/s, which shortens its velocity
  memory. Add it, or state it as a caveat.

**5. The super-droplet convergence claim "with 128 within 2 %" is false: the runs are about 6 % slow.**
Evidence: my box test (`box.cjs`) reproduces run_cloud's boxTest with Δt = 1 s.

| super-droplets per cell | seeds | t50 bias | t90 bias |
|---|---|---|---|
| 32 | 64 | +6.8 ± 3.7 % | **+15.9 ± 2.9 %** |
| 128 (the runs) | 64 | +4.2 ± 2.3 % | **+6.0 ± 1.6 %** |
| 128 at Δt = 0.2 s | 32 | +3.9 ± 3.4 % | +6.3 ± 2.2 % |
| 2048 | 6 | +0.7 ± 1.5 % | +1.5 ± 1.2 % |
| 10 240 (text) | 4 | −1.1 % | −0.4 % |

Biases are against the SCE (5.873 / 13.716 min). "About 10 % slow" at 32 understates the t90 bias. The trend is a monotone
resolution bias, so the box test shows convergence with N, not that 128 is converged. The bias does not depend on Δt.

The scheme is also run far outside Shima's own criterion p ≪ 1. Shima et al. call γ > 1 "not consistent with the fundamental premise".
In the reference cloud p > 1 for 6 % of candidate pairs, p reaches about 470–680, and 36–45 % of collisions have γ > 1. My Δt = 0.2 s
test shows this does not shift the mean, so it is a disclosure point, not an error. The run tools contain no test at 32 or 128 at all:
the sentence cannot be reproduced from the repository.

Fix: add the 32/128/512/2048 box tests, with at least 32 seeds each, to run_cloud and check_physics. Quote the measured bias. Either
raise the resolution or state that t90 in the cloud runs is about 6 % slow. Disclose Δt and the share of collisions with γ > 1, and
mention γ in the text of (11.4): "each swallow γ of the first", not "one".

**6. The "cumulus, eddies strongest in the core" case changes two things at once, and only one is disclosed.**
Evidence: run_cloud.cjs:72 sets `kernelEps: true`, so the kernel gets Ayala's turbulent factor at the local ε (physics.cjs:731 and 257–267).
The text presents the case as a change of the ε field only. Two sentences contradict it:
- 11.2: "the speed at which two drops in a cell approach each other is still set by gravity";
- the caveat list: "the stochastic element … does not change how fast two drops in one cell approach each other".

Fix: either drop `kernelEps`, or add a row for each change separately and say in the table which kernel each row uses.

**7. Chapter 10 conflates surface free energy with energy.**
Evidence: σ is the surface Helmholtz free energy per area. The heat released isothermally is u_s = σ − T dσ/dT per m² of surface lost.
From the model's own IAPWS σ(T), dσ/dT = −1.456×10⁻⁴ J m⁻² K⁻¹ at 283.15 K, so u_s = 0.1154 J/m² = **1.555 σ**. Consequences:
- The 40 µm + 8 µm capture releases 8.05×10⁻¹¹ J of heat, not 5.17×10⁻¹¹.
- The drop warms by **7.1×10⁻⁵ K**, not 4.6×10⁻⁵.
- "At its largest 1.49 % of gravity's power" becomes 2.3 % as heat.

The entropy produced, σ|ΔA|/T = −ΔF/T, is numerically right: 1.32×10¹⁰ k_B and 7.48×10⁻⁵ J/K. But it is right for a reason the text does
not give: the surface loses its own entropy (−dσ/dT)|ΔA| while delivering the larger heat u_s|ΔA|. As written, "Heat ΔE delivered at
temperature T is entropy, ΔS = ΔE_s/T" also has the wrong sign, because ΔE_s < 0. The Metropolis weight (10.5) should be written with
ΔF, which is what the code effectively uses.

Fix:
- Call σA the surface free energy.
- Write (10.4) as ΔS_total = −ΔF_s/T = σ|ΔA|/T. Explain heat = (σ − T dσ/dT)|ΔA| and the surface's entropy loss in one paragraph.
- Requote the warming and the heat-to-gravity ratio.
- In (10.5) use ΔF.

**8. "It fixes the direction: fewer, larger drops, never the reverse" and "The end state of a closed cloud is one drop" overclaim.**
Evidence:
- The second-law argument covers only splitting by thermal fluctuation. Breakup driven by mechanical energy, which comes from gravity's
  work that is at least 67 times larger here (Fig. 10.1), does not violate it. It happens in real clouds: collisional breakup, and the
  spontaneous breakup of drops above about 3–4 mm. Problem 6 says so itself.
- The model also has kernel(a, a) = 0 (dv = 0) and E_coal → 0 at large Weber number. Merging lowers the energy but need not happen, so
  "one drop" is not guaranteed even within the model.
- One drop holding the water of 1 m³ would be about 6.4 mm, above the breakup limit.

Fix: restrict the claim to "no thermal fluctuation splits a drop. Breakup needs mechanical work, which the closed box here leaves out."
Remove "never the reverse" and qualify "the end state … is one drop" as "in this model, for the 100 cm³ box".

**9. "Metropolis = coalescence with a constant kernel" is exact only as a statement about the proposal distribution, and the text sells it as energy deciding.**
Evidence:
- Every proposed merger is accepted (ΔF ≤ −1.65×10⁹ k_BT for the smallest pair, two 4.1 µm drops), and no split is ever proposed. So the
  chain is not a Metropolis sampler of any Boltzmann distribution. There are no reverse moves, so detailed balance is not satisfied
  and there is no symmetric pair of moves.
- It is a pure absorbing coalescence chain whose dynamics come entirely from the proposal rule. With uniform pair proposals its jump
  chain is exactly the jump chain of the constant-kernel Marcus–Lushnikov process (verified in gillespieRun's class-pair rates:
  each unordered pair is proposed at rate K/V). The time correspondence to (10.7) holds only in the mean-field limit.
- The same "energy-only" rule with proposals weighted by the gravitational collision rate would reproduce the real cloud on the same
  landscape. So "the energy-only Monte Carlo spends almost all its mergers joining droplets to droplets" is a consequence of the uniform
  proposal, not of energy.
- Section 10.5's "the Monte Carlo that minimises energy and the distribution that maximises entropy are one model" overstates the link.
  Neither energy nor Jaynes entropy enters the dynamics. The exponential arises from the kinetics of the constant kernel.

Fix: say plainly that the uniform proposal is an extra assumption, the "uninformed lottery", and that energy only vetoes nothing. State
that there are no reverse moves, so this is not equilibrium Metropolis sampling. Soften "are one model" to "coincide for the constant
kernel".

**10. The primary sources for both chapters are cited "not reread", which the project's own method forbids.**
Evidence: book-99 lists Jaynes (1957), Lamb (1932), Menon and Pego (2004), Rogers and Yau (1989), Shima et al. (2009) and Thomson
(1987) as "not reread". There is no source for σ² = (εh)^{2/3}, C₀ = 6, the wall reflection or the ventilation omission.

I read the two most load-bearing sources myself:
- **Menon and Pego** (arXiv nlin/0306047, Theorem 5.1 and Remark 5.3): for K = 2 and a finite initial measure, every finite-mass start
  is attracted to the exponential under weak convergence of the rescaled size distribution. Finite mass is sufficient but not necessary;
  a slowly varying divergent mass also works. The text's statement is correct, but it should add "in the mean-field equation, weakly,
  after rescaling, as t → ∞". The L1 spectrum error of Fig. 10.6 is a stronger norm. Uniform convergence of densities needs extra
  regularity (Menon and Pego, arXiv nlin/0306048).
- **Shima et al.** (arXiv physics/0701103v2, section 5.1.3): the code's p, γ, γ̃ = min(γ, ⌊ξ_j/ξ_k⌋) and the equal-multiplicity split
  ξ_j′ = ⌊ξ_k/2⌋, ξ_k′ = ξ_k − ⌊ξ_k/2⌋ match the paper exactly.

Fix: read Thomson (1987) and Rogers and Yau chapter 7 (ventilation) and correct as in objections 1 and 3. Add sources for σ², C₀ and
the closure (objection 4). Add the qualifiers to the Menon–Pego sentence.

**11. "Edge per area" is computed by a 25 m staircase count that undercounts curved outlines by about 10 %.**
Evidence: check_numbers.cjs:407 counts boundary pixels × 25 m. A Crofton-formula perimeter on a 2 m grid gives a different set of
values; the text's numbers reproduce only the pixel method.

| shape | text (1/km) | true (1/km) |
|---|---|---|
| cumulus | 3.90 | 4.29 |
| disc | 3.92 | 4.44 |
| box | 4.84 | 4.99 (the analytic 5.00) |
| tower | 6.06 | 6.28 |

The bias differs by shape, 3 % for straight edges and 10–12 % for curved ones. The ranking survives, but the cumulus and disc are no
longer "about" equal: 4.29 against 4.44. The core share is 62.0 % of the area, not 61.0 %.

Fix: compute the perimeter analytically (box, disc, tower) or with a sub-metre contour, and requote.

### Minor

**12.** The "born" flag (physics.cjs:684) is described as the "radius class at start". On merging it is overwritten (`if (p1.born === 1)
p2.born = 1`), and in the equal-split branch (line 744) it is not propagated at all. In my seed-1001 run all passages of 100 µm came
from collector-born super-droplets. The flag is not used in any figure or number, so either define it ("contains collector-born water")
and propagate it in both branches, or delete it. `st.collisions` (line 745) is computed after p2.xi has been halved in the split
branch, so it undercounts. It is not used.

**13.** data/cloud.json mixes two code versions. The stored passage logs for box/disc/tower differ from the current code: box seed 1001
stores 176 passages, while the current code gives 2553 with identical rain 24.76 %. Tower stores 78 against 1376 (`orig_box.cjs`). Only
the reference case was regenerated (ONLY=reference). Fix: regenerate all cases with one code version.

**14.** "90.2 % of 11 508 passages" counts super-droplets, not drops or water. Weighted by multiplicity it is 88.0 % (seed 1001, my
instrumented run), so the conclusion survives. Chapter 9's "nine tenths of the drizzle is born in the updraft core" should say
"super-droplets", or quote the weighted share.

**15.** The well-mixed statistic "0.79 times the scatter of pure chance" mislabels a variance ratio as "scatter" (the standard-deviation
ratio is 0.89). It is one seed at one time after a stratified start (χ²₀ = 0, so a value below 1 is expected). Under Poisson the χ²/dof
on 149 dof has SD 0.12, and in my reruns it wanders between 0.75 and 1.18. Fix: report the time-averaged profile of parcel density
against ε, with error bars from several seeds, and show the no-drift control (χ² = 2.1 → 8.3), which demonstrates the test's power.

**16.** Medians of 20 are quoted as the upper middle value: 6365 rather than (6219 + 6365)/2 = 6292, and 29 933 rather than 29 932.5.

**17.** "Collector–collector mergers are rare, a third of a percent of all mergers" matches only t50 (0.36 %), not t90 or one hour
(0.18 %, 0.15 %). By water, collectors-eat-collectors is about 15 % of all water (Fig. 10.4), which is worth saying next to
"rare by count".

**18.** The SE "at most 0.4 percentage points" is correct (0.40, still air), but with 2 degrees of freedom the 95 % interval is ±4.3 SE ≈
±1.7 points. Quote that. Welch tests: reference against disc t = 8.1, significant; box against still air t = 3.6 on df 2 (p ≈ 0.07);
tower against still air t = −2.4 (p ≈ 0.09). The last two are not significant, so do not rank them. The first-drizzle column differences
(9.2–10.1 min) are within about 2 SE and should not be read.

**19.** In the box test the multiplicities are not integers (3.75×10¹³/8192 = 4.58×10⁹ is not whole), contrary to "the counts stay whole".
Water is still conserved. State it, or choose counts that divide evenly.

**20.** The fixed mask has no vapour budget and no evaporative cooling. The clear air never moistens, though the evaporated water (about
64 % of 1.1 g/m³ over 0.87 km²) is about 15 % of the domain's whole saturation deficit and far more near the edge. Add this to "What this
chapter does not do".

**21.** In 10.3, "by 10⁹ to 10¹² k_BT (section 10.1)": section 10.1 does not give the range. My numbers are 1.65×10⁹ for two 4.1 µm drops
and 5.3×10¹¹ for 0.28 mm + 0.05 mm. Cite the computation or the problem.

**22.** Problem 6: a split proposal in Metropolis–Hastings needs the Hastings ratio, because the merge and split proposals are not
symmetric. Problem 7 and Fig. 10.6: "approaches it from any start" should read "from any start with finite water (in the mean field)".

**23.** The text says "updated exactly by (11.2)". Only the OU part is exact. The drift and the advection are forward Euler with
Δt = 1 s. That is acceptable, since Euler spiral-out on the cell is about 3×10⁻⁶ per step, but say it.

## What I verified and found right

Derivations (SymPy, `derive.py`):
- (10.1): 4πr² = (36π)^{1/3}ρ_w^{−2/3}m^{2/3}, exactly.
- (10.2): the identity holds, the bracket is negative on (0, 1) and deepest at x = ½. Two equal drops lose 1 − 2^{−1/3} = 20.63 % of
  their joint surface.
- The small-partner expansion 1 − ⅔(r/R) + (1/9)(r/R)⁴ − (4/81)(r/R)⁷ is right.
- (10.3) follows from (5.2) with its ½ and is ≤ 0. It is a Lyapunov function both in the mean field and merger by merger. The data show
  0 rises in 3600 steps, 0 energy-raising events in 40 Monte Carlo runs, and 0 rises for the constant kernel.
- Jensen for the two-bin deposit is right: (1 − f)x_k^{2/3} + f x_{k+1}^{2/3} ≤ x*^{2/3}, so the scheme removes at least the exact
  release. Measured: 0.097 % more over the hour.
- Steepest descent: ∂/∂r₁[r₁² + r₂² − (r₁³ + r₂³)^{2/3}] > 0, so it always merges the two largest drops.
- (10.6) is the maximum of entropy at fixed N and M. (10.7) and the exponential solve (5.1) with constant K: the residual is exactly 0,
  M is conserved, and N = 2/(Kt + 2/N₀). Problem 7's algebra is right line by line.
- The (11.2) OU part keeps the stationary variance, and T_L = 2σ²/(C₀ε) gives velocity diffusion C₀ε. The cell (11.1) is divergence-free,
  rises at W₀ in the middle and sinks at the sides. Its normal velocity is continuous at the box; only the tangential velocity jumps.
- (11.4) and the Shima update match Shima et al. section 5.1.3. The expected number of real coalescences equals ξ_jξ_kKΔt/ΔV per pair.
- Reflecting walls with velocity reversal preserve a symmetric Gaussian, and the no-drift control shows the test can see a missing drift.

Numbers recomputed from the model or the data (each matches the text unless noted):

1. σ = 0.07422 N/m.
2. E_s(0) = 0.02138 J/m³.
3. 92.54 % of E_s is in droplets.
4. ΔF(40, 8 µm) = 5.174×10⁻¹¹ J.
5. The collision KE is 3.043×10⁻¹⁴ J, a ratio of 1700.
6. Lamb's damping time is 0.246 ms.
7. Warming 4.57×10⁻⁵ K (σ-based; 7.1×10⁻⁵ with u_s, objection 7).
8. 1.32×10¹⁰ k_B per capture.
9. 0.02117 J/m³ released over the hour, 99.0 % of the start.
10. 7.48×10⁻⁵ J/K.
11. 1.80×10¹⁰ k_B per merger (3.01×10⁸ mergers per m³).
12. The largest release ratio is 1.490 %, at t = 10 s.
13. E_s/P_g = 28.05 s.
14. t50 = 5.77 min and t90 = 13.47 min.
15. The ledger table: all 12 entries.
16. 69.52 % of drizzle water came from droplets.
17. 87.46 % of the release came from collectors or drizzle eating droplets.
18. The spectrum errors 1.32, 1.92, 1.38, 1.90, 0.170 and 0.018.
19. The three-rule table: 50.95 ± 0.15, 78.87 ± 0.02 and 33.94 %; 0.008 %, 99.05 % and 0.
20. Final drop 0.299 mm (LWC 1.116 g/m³).
21. Collectors peak at 5.0 min; drizzle overtakes at 8.3 min.
22. Problem 6: 12.60 µm, 3.848×10⁻¹¹ J, 9.84×10⁹ k_BT and 2.79×10¹² K.
23. σ = 0.794/0.368/1.260 m/s and T_L = 21.0/45.2/13.2 s.
24. K = 13.2 m²/s, which spreads a puff 126 m in 10 min.
25. G = 9.726×10⁻¹¹ m²/s, from F_k = 6.334×10⁹ and F_d = 3.948×10⁹ s/m² (e_s = 1227 Pa, D_v = 2.70×10⁻⁵ m²/s at 850 hPa).
26. 2.57 s and 257 s (without ventilation), and 412 s to fall 300 m at 0.728 m/s.
27. All rain and evaporation means of the table, and SE max 0.40.
28. 11 508 passages.
29. First drizzle super-droplet at 2.03/2.10/2.18 min.
30. 3.9×10¹¹ and 3.9×10⁹ drops per super-droplet.
31. About 1.3×10¹⁶ drops in the cumulus slice.
32. The box test numbers as stored.
33. Mass budget: air + rain + evaporated = 99.96 %.

Figures: I screenshotted Figs. 10.1–10.6 and 11.1–11.4 from the served page. Each shows what its caption says: the drizzle-on-drizzle
diet passes 1, the collector peak is near 5 min, the crossover near 8 min, and drizzle falls out of the base in the middle. Fig. 11.4
correctly says "super-droplets" in the caption, while its in-figure label says "drops".

Kept as right:
- the distinction between thermodynamic entropy and Jaynes's entropy of the size distribution, which the text makes explicitly;
- the radius-prior remark n ∝ m^{−2/3}e^{−βm};
- the honest caveats on condensation and super-droplet lumping.

## How to reproduce

```
S=/tmp/claude-0/-home-user-SiteTest/de75440b-f270-5344-8ae7-923c4f178e24/scratchpad/review_phys
python3 -I $S/derive.py                                   # SymPy: (10.1)-(10.7), problem 7, OU, Thomson residuals
S=$S node $S/mix.cjs code|none|full|fullU 7200            # well-mixed test with the drift variants
S=$S node $S/box.cjs 96,32 64                             # super-droplet box bias at 128 per cell
S=$S node $S/cloudrun.cjs '{"shape":"box","stochastic":false}' 1001 x   # shape baselines without eddies
S=$S node $S/evsplit.cjs '{"shape":"cumulus","vent":true}' 1001 x       # ventilation, and evaporation below/above the base
```

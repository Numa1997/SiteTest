# Check of note §11.10 "The 3D solver on your graphics chip ★", the "On the graphics chip" paragraph of §14, the §15 edits and the abstract

Checked 7 November 2026, 00:20–01:20 UTC, by a checker who did not write the note. **The text checked is the one in commit
12f2fc5** (`public/simulations/beer-slosh.html` sha256 3c80c32c…, `public/scripts/stout-cart.js` sha256 141e40ac…,
`public/scripts/stout-gpu.js` sha256 fb48b145…, `public/scripts/stout-gpu-view.js` sha256 80c474eb…). While the check ran,
another session edited `beer-slosh.html` and `stout-cart.js` in the working tree (joint motor + suspension controller,
suspension LQR limits). Those edits do not touch §11.10, §14, §15, the abstract, `World.advanceGpu` or the GPU files (checked with
`git diff HEAD`). `notes/fig12/runs/rest-gpu.txt` is **empty in the commit**. The run that backs the "left alone" sentence
(`rest-gpu.txt`/`.json`, 00:14 UTC) exists only in the working tree.

Verdicts: **verified**, **wrong, because …** (with the correct value and the command), **unverifiable, because …**.

## How it was checked

- **SymPy** (scratchpad `sym.py`): (9) from the thin tilted layer; G1, with the code's expression set against the note's for
  n = 1…6; G2 from dI = −κI dℓ; the integral of a sphere's chord over its projected disc.
- **Bookkeeping of G1 against `World.advance`** (scratchpad `bookkeeping.cjs`): 2000 random sequences of step impulses,
  random batch sizes 1–16 and step lengths 1–5 ms, with the impulse algebra of `advanceGpu` copied line by line.
- **Thickness scale** (scratchpad `thick.py`): Monte Carlo of the sum of sphere chords along 400 rays through particles on
  the jittered 2 mm lattice of `GpuFluid.seed` (radius 2.2 mm, as `stout-gpu-view.js`), times `thickScale`, against the true path.
- **GPU solver in headless Chromium** (Playwright, WebGPU on SwiftShader with the flags of the tools):
  `OUT=… node tools/fig12/gpu-linearity.cjs 6 0.3 0.5`, run twice; `SERIES=… node tools/fig12/gpu-study.cjs 25 off 4 0.7`, run twice;
  `gpu-study.cjs 10 off 4 0.3` twice and `10 off 1 0.3`; and scratchpad `gpu-tilt.cjs step|ramp`, a copy of the TILT branch of
  `gpu-linearity.cjs` that reads the centre of mass back every step (step push, 1–2 s) or every second step (the
  `check.cjs tilt` protocol: 1 − cos ramp over 2 s, mean over 2.5–5.5 s). Page errors: none. The only console error was the
  404 of the tools' blank `/none` page.
- **Processor's solver in Node** (scratchpad `cpu-rest.cjs`, `cpu-tilt-step.cjs`): the same rest and step-tilt runs on
  `Fluid` from `stout-cart.js`, to compare like with like.
- **Stored runs**: `linfit.cjs` was rerun on `linearity-gpu-a/b.json` and `linearity-3d-a/b/c.json`. The maxima during the push
  were read from the series.
- **Code against text**: every pass of `GpuFluid.steps` against the list "One step, as the chip does it", `World.advanceGpu`
  against G1, and `stout-gpu-view.js` against "The picture". `Fluid` (CPU) was read for the tolerances, the dilation and the inheritance rule.

## Equations

| Item | Verdict | Evidence |
|---|---|---|
| (G1) D = Σ_{i=0}^{n−1} J_i − n J_0 | verified | Index convention (the text never states it outright): J_0 is the impulse of the previous batch's last step, and J_1…J_n are this batch's steps. §10.2 hands J_{i−1} over during step i, so during the batch the cart is owed J_0…J_{n−1}. It received J_0/Δt in each of the n steps, i.e. n J_0. Code: `owed = J0 + Σ_{k<n−1} Jl_k − n J0`, where `Jl_k` are the batch's impulses 1…n−1. SymPy: code − note = 0 for n = 1…6. Units: N s. |
| (G1) F_ℓ = J_n/Δt + D/(nΔt) over the next batch | verified, one ambiguity | `advanceGpu` sets `Fx = J0/h + owed/(n h)` at the start of the next call, with that call's own n. Over n steps of h the cart receives n J_n + D, whatever h and n are. The n in D/(nΔt) is the **next** batch's n (write n′). The store's `F_lx_next` (end of `advanceGpu`, and the panel check `C2.F_lx_next`) uses the current batch's n. It is the force actually applied only when the next batch has the same n. Units: N. |
| "cart and stout exchange exactly the momentum they exchange in section 10.2" | verified (as bookkeeping) | `bookkeeping.cjs`: after every batch, delivered = (cumulative impulse `World.advance` would have handed over) − D, to 3 × 10⁻¹⁴ (round-off). The identity concerns impulses: the two couplings give different J sequences, because the cart's force history differs. That is why batch 4 leans 67.4 mm against 65.7 mm. |
| "late by at most one batch" | wrong, because the owed part arrives up to 2n − 2 steps late | J_i of step i (1 ≤ i ≤ n−1) is due during step i+1 but is paid uniformly over the next batch's steps n+1…2n. Its last part arrives 2n−1−i steps late (up to 2n−2 steps, 1.5 batches at n = 4, 1.9 at n = 16). Its centroid arrives (n+1)/2 to (3n−3)/2 steps late (2.5–4.5 steps at n = 4). Correct: "settled by the end of the next batch: on average about one batch late, at most just under two". |
| "with n = 1 nothing is owed and the steps are those of section 10.2" | verified | D = J_0 − J_0 = 0 (SymPy). `bookkeeping.cjs`: at n = 1 the per-step force equals `World.advance`'s J_{k−1}/h exactly (difference 0). Per step, `advanceGpu` also substeps the cart in the same way, hands over the same mean acceleration, uses the same spill accounting, and reads the probes and drops as `advance` does. One difference: when the CFL limit binds, `advanceGpu` takes round(dt/h_max) steps of h_max, while `advance` cuts dt into equal steps. The coupling is identical. |
| (G2) I = I_0 e^{−κℓ} from dI = −κI dℓ, κ = ln 2/(6 mm) | verified | SymPy `dsolve`: I = I_0 e^{−κℓ}. I/I_0 at 6 mm = 1/2. Code: `kappa = Math.log(2)/0.006` (m⁻¹, with ℓ in m: consistent), `T = exp(−κ·thick)`, colour = mix(dark, ruby, T): ruby where thin, black where thick, as stated. Units: κℓ dimensionless. Limits: ℓ = 0 gives T = 1 (ruby); ℓ → ∞ gives black. "A drawing constant, not a measured property": correct, it is a fixed number in the shader. |
| "the Beer–Lambert law" | verified | Exponential attenuation in a homogeneous absorber along a path, which is what G2 is. On the page it sets a colour mix along the line of sight, not a computed light transport. The note says so ("a drawing constant"). |
| Thickness ℓ: "the spheres' chords are added up, scaled by the ratio of a particle's volume to its sphere's" | verified | For particles of number density 1/s³, the expected chord sum per unit path is (4/3 π r_d³)/s³, because ∫ chord dA over the disc = sphere volume (SymPy: 4πr_d³/3). The factor is s³/(4/3 π r_d³) = (2 mm)³/(4/3 π (2.2 mm)³) = 0.1794 = `thickScale` (`stout-gpu-view.js` l. 170, s = dx/ppcSide = `Vseed`^{1/3}). Monte Carlo (`thick.py`): scaled sum / true path = 0.9998 mean, 0.046 s.d. per ray (lattice graininess), 0.84–1.11 range. Unbiased. |
| (9) used for the tilt: x̄ = −(a/g) π R(h)⁴/(4V) = −0.877 mm | verified | SymPy: I = πR⁴/4, x̄ = −πR⁴a/(4Vg), cylinder −R²a/(4gh). Tulip, page code: R(h) = 39.100 mm, V = 426.60 cm³, a = 2 m/s²: x̄ = −0.87728 mm. Units: m. |

## §11.10 "What is solved"

| Claim | Verdict | Evidence |
|---|---|---|
| Same equations (4)–(5) in the glass's frame, pressure from (45), "not a weakly compressible liquid" | verified | FORCES adds dt(−a_x) to u and dt(−g − a_z) to w on open faces (= g − a_g of (4)), then explicit viscosity. PRESSURE/CG solve the Poisson system for q = pΔt/ρ (46). PROJECT subtracts ∇q. No equation of state anywhere in `stout-gpu.js`. (4), (5), (45) are the right equation numbers (l. 230, 231, 585). |
| Tolerance 10⁻⁵ of the largest right-hand side (processor 10⁻⁷) | verified | GPU: `tol = o.tol \|\| 1e-5`, in the shader `tol = P_.tol * bm` with bm = max\|b\| and the residual's max norm. CPU (`Fluid`, l. 753): `tol = 1e-7 * bmax`, max norm. Both cap at 300 iterations. |
| 2 × 2 × 2 particles per 4 mm cell, APIC, cut-cell wall, level set, ghost fluid, step 5 ms | verified, one omission | `ppcSide 2`, `rpFactor 1.8`, `kernel 2`, `sliver 0.1`, `thetaMin 0.05`, `forcedPhi 0.05` as on the CPU. `dtMax: 1/200` in the page (l. 878) and the tools. Not said: the cut-cell "inherit" rule is two **Jacobi** passes on the chip (`copyF`/`inherit` twice) against two Gauss–Seidel sweeps from the top on the CPU (`inheritWallPhi`). On the CPU a wall cell can inherit from a cell that turned liquid earlier in the same sweep; on the chip it cannot. So "same cut-cell wall" is not exactly true. The header comment of `stout-gpu.js` lists this difference and says each difference is "stated in the lecture note"; this one is not. Effect: none visible at rest (below). |
| Whole glass, 51 332 particles, 20 × 20 × 45 cells | verified | `nx = ny = 2⌈R/dx⌉ = 2⌈39.299/4⌉ = 20`, `nz = ⌈177.5/4⌉ = 45`. `npStart` = 51 332 in every run = 2 × 25 666 (the CPU half: `Fluid` gives 25 666 particles on 20 × 10 × 45). `GpuFluid.seed` takes the CPU's half and its mirror image. |
| "the stout can now swirl" | verified (possibility only) | Nothing in the solver imposes symmetry. But the start is exactly mirror-symmetric and a_g has no y part, so a swirl can grow only from float32 round-off. No run in the note shows one. |
| Single precision, "about 7 digits" | verified | All shader arithmetic is f32 (24-bit significand, 7.2 decimal digits). The host adds the per-workgroup partial sums in float64. |
| Jacobi preconditioner instead of MIC(0); MIC(0)'s triangular sweeps are sequential | verified | `pcg`: z = r / A_d. CPU `precond`: forward and backward triangular sweeps over the liquid-cell list. |
| "about 70–100 iterations a step instead of about 33" | wrong, because the runs give 85–99, and 37 at rest | Mean CG iterations per step: 84.6 (A 0.5), 94.2 (1), 99.1 (2), 99.0 (4), 98.3 (6), 98 (steady tilt), 99.2 (A 6, rerun). At rest: 36.7 (`rest-gpu.txt`, working tree only). The CPU's 32 a step (§11.6) supports "about 33". Correct: "about 85–100 a step under a push (37 at rest) instead of about 32". |

## §11.10 "One step, as the chip does it"

| Pass in the note | Verdict | Code (`GpuFluid.steps`, order of `run(...)`) |
|---|---|---|
| (1) sort by cell: count, prefix sum, scatter, each cell's list in particle order | verified | `count` (atomic integer counts), `scan` (one workgroup), `scatter`, `sortCell` (insertion sort by particle index), then `permute` (not named in the note; it reorders the arrays). |
| (2) level set: "which cells are near the surface (masks dilated twice by two cells)", φ from particles within 2Δx with wall images | verified, wording imprecise | Two masks ("empty", and "occupied") are each dilated **once** by ±2 cells, separably along x, y, z (`dilate0`, `dilateX/Y/Z`), as on the CPU (l. 358–375). "Twice" reads as two dilations. Better: "two masks, each dilated by two cells". `phiCells`: Zhu–Bridson over the 5 × 5 × 5 block, R_k = 2Δx, wall images by `imgF`. |
| (3) liquid cells; cut cells inherit from an open neighbour | verified | `flags`, then `copyF`/`inherit` twice. See the Jacobi remark above. |
| (4) particle-to-grid by gathering, in sorted order | verified | `p2gU/V/W`: each face visits the cells overlapping [node − 1, node + 1) and sums w(u_p + C_p·(x_node − x_p)) and w in cell and particle order, then S/M. Same terms as `Fluid.transfer`. "On the processor each particle adds its share to the eight faces around it": verified (`transfer`, toGrid). |
| (5) gravity and fictitious force, then viscosity | verified | `force` ×3, then `copyT`/`visc` ×3. |
| (6) matrix and right-hand side, then CG "in one group of 256 workers" | verified | `assemble`, then `pcg` dispatched with one workgroup of WG = 256. |
| (7) pressure gradient and three layers of extrapolation | verified | `gradient`, then three `copyV`/`extend` passes, then `zeroInvalid`, per component. |
| (8) grid-to-particle, midpoint advection, wall, floor, spill | verified | `g2p`, `advect` (RK2 midpoint; wall projection along the normal of (6); floor; box top; spill above z_rim and outside R_rim). |
| (9) the sums the cart needs | verified | `momentum`: per-workgroup Σu, Σv, Σw and max\|v\|², plus integer column counts for the probes. |
| "a chip can add floating-point numbers that way only in an order that changes from run to run" | verified | WGSL has atomics only for i32/u32. Float accumulation needs CAS loops whose order is not fixed. |
| "Every sum on the chip is formed in a fixed order, and a run repeats exactly on one device" | verified | All float sums use fixed orders: gather in cell/particle order, fixed-tree workgroup reductions, partials added on the host in index order. Atomics are on integers only (counts, the spill index). Repeat runs: `gpu-linearity.cjs 6 0.3 0.5` twice (9.5 g spilled), series identical. `gpu-study.cjs 25 off 4 0.7` twice (cart coupled, 2.7 g spilled), series identical. `gpu-study.cjs 10 off 4 0.3` twice: identical files. Also the stored tilt (−0.922 mm) was reproduced to every printed digit by an independent script. One caveat: the order of the spilled particles in the spill list follows an atomic counter. The host adds their float32 velocities into `spillPx` in float64, which is exact in practice, but the order of the drops in the room varies. |

## §11.10 "The cart and the chip, in batches"

| Claim | Verdict | Evidence |
|---|---|---|
| A read-back waits for the chip, "of the order of a millisecond or more" | unverifiable, because this machine has no graphics chip | SwiftShader runs on the processor, so the wait cannot be measured here. Plausible. |
| A batch of n steps, "as many as the frame lasted (at most 16)", one read-back | verified | Page l. 1537: `want = min(dt, 0.08, nmax·dtMax)`, `n = round(want/h)`, capped at `MAXB = 16`. One `mapAsync` per chunk of ≤ 16 steps. Not said: n is also cut to ⌊60 ms / (ms per step)⌋ when the chip is slow. |
| The cart runs ahead, with the stout's push held at the last known force, and hands each step's acceleration to the chip | verified | `advanceGpu`: `c.forces(this.Fx, …)` once, then n cart steps building `list` of {dt, ax, az}, then `f.steps(list)`. |
| "Section 10.2 hands the cart the impulse of fluid step i … during step i + 1" | verified | §10.2 (l. 575) and `World.advance`. |
| "the stout's push on the cart is a ripple of about 0.08 m/s² (section 12)" | wrong, because the number is in Example 4.2 (§4), not §12, and belongs to the 10 mm bump | Example 4.2: 0.0834 m/s² predicted, 0.0829 m/s² fitted, 10 mm bump, open loop. §12 only refers to Example 4.2. On the 25 mm bump that §11.10 then quotes, the ripple scales with the swing: (estimate) about 0.2 m/s². |
| "at 50 frames a second a batch is 20 ms, a quarter of a radian of the 3.2 Hz swing" | wrong, because 20 ms is 0.40 rad | 2π × 3.2 Hz × 0.020 s = 0.402 rad (23°, 1/16 of a period). Correct: "about 0.4 rad (a sixteenth of a swing)". n = 4 steps at 50 Hz: verified. |
| 25 mm bump, open loop: batches of 1 and 4 lean 65.7 and 67.4 mm and spill 13.5 and 13.9 g | verified | `notes/fig12/runs/study-gpu.txt` lines 1–2 (`gpu-study.cjs 25 off 1`, `… 25 off 4`). Batch 4 against batch 1: +2.6 % lean, +3.0 % spill. A 0.7 s rerun with batch 4 reproduces the stored run's start (a_x 3.56, the stored value for batch 4). |
| Probes read once per batch; Kalman filter fuses a reading whenever a new one comes (section 8.5) | verified | `readProbes()` at the end of `advanceGpu` sets `probe.fresh`. `Cart.sample` (l. 1569) uses y_q only when fresh and then clears it. §8.5 is the Kalman section (l. 504). |

## Table 6 and the "Checks" paragraph

Commands: `node tools/fig12/linfit.cjs notes/fig12/runs/linearity-gpu-a.json notes/fig12/runs/linearity-gpu-b.json` and the
same for `linearity-3d-a/b/c.json`. The A = 6 row was rerun on the chip for 0.5 s (lean −69.0 mm at 0.205 s, identical).

| Entry | Page | Run files / rerun | Verdict |
|---|---|---|---|
| Largest lean, chip, A = 0.5/1/2/4/6 | 5.5 / 11.5 / 25.4 / 46 / 69 | 5.46 (1.325 s) / 11.48 / 25.40 / 46.02 / 69.00 | verified. "46" and "69" are 46.0 and 69.0: the tool's `+x.toFixed(1)` drops the zero. |
| Largest lean, processor | 5.9 / 11.5 / 25.4 / 45.3 / 69.3 | 5.89 (1.93 s) / 11.51 / 25.38 / 45.29 / 69.33 | verified |
| Free swing, chip | 2.0, 3.194; 5.0, 3.200; 15.2, 3.190; 32.6, 3.108; 38.9, 3.049 | identical (misfit 1.17, 2.13, 2.41, 3.72, 6.11 mm rms) | verified |
| Free swing, processor | 2.1, 3.160; 4.4, 3.202; 14.7, 3.194; 32.7, 3.109; 36.9, 3.056 | identical | verified |
| Spilled, chip / processor | 0, 0, 0, 1.6/1.6, 12.3/12.2 g | identical | verified |
| "The two solutions agree in the push" | — | During the push (t ≤ 0.3 s) the largest leans are 1.85/1.85, 11.48/11.51, 25.40/25.38, 46.02/45.29, 69.00/69.33 mm | verified. At A = 0.5 the table's 5.5/5.9 mm are late jumps in a noisy series (1.3 s, 1.9 s), not push responses. The caption's "largest lean" matches Table 5's corrected caption. |
| "in the free swing's frequency within 1 % at every amplitude" | wrong, because at A = 0.5 m/s² the gap is 1.1 % | 3.194 against 3.160 Hz: +1.08 %. The others: −0.06, −0.13, −0.03, −0.23 %. Correct: "within 0.25 % from 1 m/s² up, 1.1 % at 0.5 m/s², where the swing is 2 mm, half a cell". |
| "in its softening from 3.19 to 3.05 Hz as it grows (section 11.9)" | verified | Chip 3.194/3.200 → 3.049. Processor 3.202 → 3.056 (§11.9: "from 3.20 to 3.06"). The free-swing amplitudes differ more (5.0 against 4.4 mm, 38.9 against 36.9 mm). The note does not claim they agree. |
| "and in what spills" | verified | 1.6/1.6 g, 12.3/12.2 g. |
| Steady push 2 m/s²: centre of mass −0.922 mm on the chip, "the mean over the last second of 2 s"; command `TILT=2 node tools/fig12/gpu-linearity.cjs 0 0 2` | wrong, because −0.922 mm is a sampling artefact | `tilt-gpu.txt` holds −0.922 mm, and an independent rerun gives the same −0.9222 mm. But the push is a step from t = 0, so the stout still swings: over 1–2 s the centre of mass oscillates between −1.706 and −0.142 mm. The tool averages only **10 samples**, every 20th step (t = 1.005, 1.105, …, 1.905 s). Sampled every step over the same second, the chip's mean is **−0.9735 mm (+11.0 %)**. The processor under the same step protocol gives **−0.9766 mm (+11.3 %)**, sampled every step, or −1.006 mm with the tool's 10 samples. Under §12's own protocol (`check.cjs tilt`: 1 − cos ramp over 2 s, mean over 2.5–5.5 s) the chip gives **−0.9130 mm (+4.1 %)** and the processor −0.895 mm (+2.0 %). Commands: scratchpad `gpu-tilt.cjs step`, `gpu-tilt.cjs ramp`, `cpu-tilt-step.cjs`; `notes/fig12/runs/tilt_0.004.txt`. |
| "the exact quasi-static value, (9) evaluated for the tulip, is −0.877 mm" | verified | −0.87728 mm (above). |
| "so the chip is 5.1 % off, the processor on the same grid 2.0 % (section 12)" | wrong, because the two numbers come from different protocols | 0.922/0.877 − 1 = 5.1 % (arithmetic right). The 2.0 % (Table 1, §12) uses the ramp protocol. Like for like: chip +4.1 % against processor +2.0 % (ramp), or +11.0 % against +11.3 % (step, dense sampling). The conclusion that the chip is somewhat further off holds (4.1 against 2.0 %), but the number should be −0.913 mm, 4.1 %, and the command should be the ramp protocol. |
| 25 mm bump, open loop: chip 65.7 mm, 13.5 g; processor 60.7 mm, 11.9 g | verified | `study-gpu.txt` l. 1. Table 2 / `study_25_off_0_0.004.txt`. |
| Accelerations 3.58 and 7.62 against 3.58 and 7.63 m/s², "agree to the hundredth" | verified | `study-gpu.txt` (batch 1): 3.58, 7.62. Table 2: 3.58, 7.63. They differ by 0.01 in a_z: "to within 0.01 m/s²" is the exact wording. |
| Speed loop: leans 27.7 and 29.9 mm; commands `gpu-study.cjs 25 off 1`, `… 25 speed 4` | verified | `study-gpu.txt` l. 3 (batch 4). Table 2: 29.9 mm. |
| "Left alone … its fastest particle moves at up to 14 mm/s within 2 s (the processor's, 3.2 mm/s after 1 s)" | wrong, because it compares the chip's start-up peak with the processor's value at 1 s; the two solvers are the same | `rest-gpu.json` (working tree only): the chip's 14.31 mm/s is at **t = 0.05 s**. Afterwards: 5.52 (0.1 s), 3.18 (0.5 s), **3.20 (1 s)**, at most 3.49 after 1 s. The processor's `Fluid` from the same seed peaks at **14.31 mm/s at t = 0.05 s** too and reads 5.52, 4.54, 3.18, 3.20 mm/s at 0.1, 0.2, 0.5, 1 s (scratchpad `cpu-rest.cjs`). Every printed digit agrees up to 1 s. Correct: "at rest both solvers give the same start-up stir, 14 mm/s at 0.05 s, decaying to 3 mm/s by 1 s". |
| "and the lean it reads drifts by under 1 mm" | verified, with context | Chip: 0.56 mm at t = 0, 1.42 mm at 2 s (drift 0.86 mm). The processor drifts 0.56 → 0.95 mm in 2 s (0.39 mm). This is the one difference at rest: 0.47 mm by 2 s. |
| "The likely cause is single precision in the pressure solve; it is not established" | wrong, because it explains a difference that the speeds do not show | The fastest-particle history is identical to the processor's (row above), so there is nothing GPU-specific to explain there. Only the lean's extra drift of 0.47 mm in 2 s remains, and its cause was not tested (candidates: f32, the Jacobi-preconditioned 10⁻⁵ tolerance, the Jacobi inheritance). |

## §11.10 "The picture" and "Speed"

| Claim | Verdict | Evidence |
|---|---|---|
| Drawn without sending the particles back | verified | `GpuView.render` binds the solver's live position buffer (`f.side === 0 ? posA : posB`). Positions are read back only while paused (`posWatch`, for the store). |
| Spheres through the camera of section 14; nearest depth kept | verified | `vs`/`fsDepth`: `toScreen` with the page camera (`cam.d, r, u, Cp, f`), sphere radius 2.2 mm, `depthCompare: 'less'`. |
| Bilateral filter, edge kept sharp; normal from the smoothed depth | verified | `FILTER`: Gaussian in pixel distance and in depth difference (scale 1.5 r_d), separable, x and y applied 4 times. `SHADE`: the normal from the neighbours on the closer side. |
| Thickness from chords, scaled | verified | `fsThick`, additive blend into r16float at half size. Scale: see the Equations table. |
| Head: "the top 12 mm of the stout below the computed surface is painted cream" | verified | `headH = 0.012`; `inHead = smoothstep(top − headH ± 1.5 mm)`, with `top` from the column-height surface map `hs`. |
| "screen-space fluid rendering, as in the WebGPU fluids of [26]" | verified (reference number) | [26] is the 26th entry of §16 (matsuoka-601, Codrops 2025, Splash / WebGPU-Ocean). The source was not reread for this check. |
| A step takes "about 0.3 s, a hundred times slower than real time" on SwiftShader | wrong, because 0.3 s per 5 ms step is 60 times | Stored runs: 297–463 ms per step (60–93 times slower); this check, with two runs sharing the CPU: 470–570 ms. Correct: "0.3–0.5 s, 60–90 times slower than real time". |
| "Every number in this subsection was computed there" | verified | Every run file names `google/swiftshader`. |
| Rate measured and printed: "real time" or "slow motion" and the factor | verified | Page l. 963: `cap-rate` prints "real time (… measured on your graphics chip)" when simPerReal ≥ 0.95, else "slow motion ×…". |
| Without WebGPU: processor, half glass, about 0.3 s per s on four cores, said in the caption | verified | `NO_GPU_NOTE` → `capModel()`: "your browser offers no WebGPU, so the stout runs on the processor (half glass, slow motion)". 0.3 s per s matches §11.7. |

## §14 "On the graphics chip", §15, the abstract

| Claim | Verdict | Evidence |
|---|---|---|
| §14: GPU is the default where the browser offers WebGPU | verified | `WANT_GPU = !MODAL && !grid && !!navigator.gpu`. |
| §14: the surface is the smoothed envelope of the particles, so a curling crest or a thrown-up drop is shown | verified | Drawn from the particles' depth image, not from column heights. A particle that has spilled (w < 0) is not drawn by the GPU view; it becomes a drop drawn by the page's 2D view. |
| §14: colour follows the thickness along each line of sight, (G2) | verified | As above. |
| §14: head = top 12 mm, cream | verified | As above. |
| §14: probes, charts and data panel read the column heights, as with the processor | verified | `readProbes` → `GpuFluid.columnHeights` (integer counts per column, the CPU's 3 × 3 filter and volume tables) → `columnHeightAt`. |
| §15: "On the processor: swirl and any motion that breaks the mirror symmetry (section 3.4). The graphics chip's solver computes the whole glass" | verified | `Fluid` computes y ≥ 0 only. `GpuFluid.whole = true`. |
| §15: "The next model would resolve the wall layer …" (whole glass removed from the list) | verified | Consistent with the GPU solver. |
| Abstract: the 3D solution of the whole glass runs on the reader's chip through WebGPU, drawn by the chip from its particles; the rate is measured and printed; without WebGPU, half the glass on the processor in slow motion | verified | As above. |
| Abstract: the reduced model "is kept as a comparison and as the controller's own picture of the stout; it is not a fluid simulation" | verified | `?model=live` only. The button reads "Reduced model, not a fluid simulation". The Kalman filter and LQR are built on one sloshing mode (`World` constructor, `c.sloshMode`). |
| Abstract: the LQR "acts on the 3D fluid itself, in slow motion" | wrong, because on a real graphics chip the 3D fluid may run in real time | This sentence is left over from before the edit and now contradicts the preceding sentence of the abstract. Drop "in slow motion" or write "in real time where the chip keeps up". |

## Unedited text that the GPU default now contradicts (outside the brief, for the author)

- §3.4: "only the half y ≥ 0 need be computed. The page does exactly that … those motions are absent from the page by
  construction (section 15)". This is now true only on the processor.
- §10.1: "P = 2m_p Σ u_p (the factor 2 for the half glass not computed)". On the chip P = m_p Σ u_p (`this.P = [mp·sx, mp·sz]`).
- §14, last paragraph: "Spilled drops are drawn … with their mirror images". With the chip there are none (`dropsFrom`: `both = [1]` when `whole`).

## Code remarks (no note claim depends on them)

- `G2P.advect` writes a spilled particle into `spill[2n]` for n < 4096, but the buffer holds `SPILLCAP` = 1024 particles, and
  the host reads `min(1024, count)`. If more than 1024 particles spill in one step, WebGPU's robust access may discard or
  redirect the extra writes, `np` is overcounted, and their momentum is missing from P_spill. Not reached in any run here: the
  largest total loss is 1476 particles in 2 s.
- `gpu-linearity.cjs` steps `GpuFluid` directly at 5 ms, without the CFL limit (49), as `linearity.cjs` does on the CPU. At A = 6 m/s²
  the fastest particle reaches 785 mm/s, 0.98 cell a step. The comparison in Table 6 is like for like.

## Errors, in short

1. Tilt: −0.922 mm / 5.1 % is the mean of 10 samples of a ±0.8 mm swing. Like for like with §12's protocol the chip gives −0.913 mm, +4.1 % (processor +2.0 %). With the tool's step push and dense sampling, chip and processor agree: −0.974 against −0.977 mm (+11 %).
2. Rest: the chip's 14 mm/s is the start-up stir at 0.05 s, which the processor has identically (14.31 mm/s at 0.05 s, 3.20 mm/s at 1 s on both). The "single precision" explanation addresses a difference that does not exist. Only the lean's drift differs (0.86 against 0.39 mm in 2 s). The backing run file is empty in commit 12f2fc5.
3. "within 1 % at every amplitude": 1.1 % at 0.5 m/s² (3.194 against 3.160 Hz).
4. "a quarter of a radian": 20 ms of a 3.2 Hz swing is 0.40 rad.
5. "a ripple of about 0.08 m/s² (section 12)": the number is Example 4.2's (§4), for the 10 mm bump. The 25 mm bump gives roughly 0.2 m/s² (estimate).
6. "late by at most one batch": the owed impulse is settled by the end of the next batch, up to 2n − 2 steps (under two batches) late; on average about one batch.
7. "70–100 iterations": 85–99 under a push, 37 at rest.
8. "a hundred times slower than real time": 0.3–0.46 s per 5 ms step is 60–90 times.
9. Abstract: "in slow motion" for the LQR on the 3D fluid no longer holds on a real chip.
10. Wording and omissions: "masks dilated twice" (two masks, each dilated once by two cells); the Jacobi form of the wall-cell inheritance is a difference the note does not state ("same cut-cell wall"); in G1 the n of D/(nΔt) is the next batch's n′, and the stored `F_lx_next` uses the current n; J_0 is never defined as the previous batch's last impulse; "46"/"69" are 46.0/69.0.

Verified without reservation: G1's algebra and its momentum bookkeeping (exact to round-off), n = 1 ≡ §10.2's coupling, G2, the
Beer–Lambert reading, the thickness factor (0.1794, unbiased by Monte Carlo), (9) = −0.877 mm, every Table 6 entry against the run
files and `linfit.cjs`, the particle and cell counts, the 10⁻⁵/10⁻⁷ tolerances, the pass list against `GpuFluid.steps`, the exact
repeatability of runs (spill and cart included), the bump numbers, and the equation and section references (4)–(5), (45), (9), §8.5, §10.2, §11.9, [26].

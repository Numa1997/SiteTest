# Fig. 15 correction: brief for the correcting session

Written 14 November 2026 by the coordinating chat (session_01DGmqintkoYzahfGQQzdXYL), on the owner's order:
"direct and deploy a new session to correct everything from the resonant tunneling".
You are that session. Read this file whole, then the files it names, before any work. Never write the owner's name.

## 0. The owner's standing order on data (binding)

The owner, verbatim, 14 November 10:35 UTC:

> "absolutely not generate a single atom of data, of new data, if it's not needed. In other words, if you can use other data to
> generate corrected data, then use it already, for fuck's sake, rather than delete everything and delete all of our energy costs."

And today: "I'm not gonna fucking accept that we will have to recompute everything. [...] The corrections basically must use the
current data, unless it's absolutely not possible anymore."

So you work down this ladder, and you show with numbers that a rung is exhausted before you use the next:

1. **Keep what passes.** A stored run that passes the gate (section 3) against an exact or converged reference stays as it is.
   Nothing that passes is recomputed. No R2 object is ever deleted.
2. **Exact answers instead of simulations,** wherever the physics has one (walls: section 4).
3. **Exact reductions to fewer dimensions** (discs and shells are axisymmetric: section 5).
4. **Correction of stored data by other stored or exact data,** only after validation against converged references.
5. **New computation only for what is left,** and a GPU only with the owner's explicit yes on a bill. You launch nothing on Kaggle.

Where a rung cannot work, say why in physics terms, with a number. Example of such a reason: a stored frame is the solution of the
grid's Hamiltonian, not the true one; turning it into the true solution by first-order perturbation (Duhamel) needs the full 3D
complex field at every step, and only an 8-bit slice of one plane was stored.

## 1. What is wrong (each item checked by the coordinator; handles given)

**D1. The barriers are drawn on too coarse a grid.** `tools/kaggle/resonant-tunnelling/rt3d2.py` (branch
`claude/fig15-resonant-tunnelling`, line 117) sets V = V0 on grid points strictly inside each barrier, on a 0.5 a grid, with the
spectral free flight `exp(-0.5j*K2*dt)` (line 121). A barrier 1 a thick is two grid points. The free flight sees the band-limited
version of that staircase, so the phase a wave gains on each round trip between the barriers is wrong, and every resonance sits at
the wrong energy.
- Fact (coordinator's own transfer matrix, `notes/fig15/coordinator/mytm.py`, checked against the analytic single barrier to
  all printed digits; results in `my_unbiased.json`, `my_biased.json`): of the 1,088 wall runs, **917 fail** the gate
  |T_run − T_exact| ≤ max(0.005, 1 % of T_exact): 468 of 613 unbiased, 449 of 475 biased. Unbiased: median error 0.021,
  worst 0.435. Single walls fail too (33 of 47).
- Fact: the chat's audit (`notes/fig15/error_audit.json`) uses the same reference to within 1.2 × 10⁻⁴.
- Fact: the index's own `twin.T_exact` is sampled too coarsely (1201 points in k) for the narrowest peaks. It is off by up to
  0.0023. Do not use it as the reference. Use a converged packet average (it stops changing between 4001 and 80001 points).
- Fact (from the 1D twin, `notes/fig15/audit/twin_converge.py`): a time step 4 times smaller or a box twice as long change T by
  less than 0.0003. The barrier drawing is the cause.

**D2. The side border eats the wave in long runs.** The box is 64 a across, with an absorbing border on the outer tenth. A packet
3 a wide spreads across as σ(t) = 3 √(1 + (t/18)²): 17 a at t = 100 and 33 a at t = 200. Runs last up to t ≈ 540. For walls the
trapped share between the walls (region `well`, which spans the whole cross-section) therefore ends 6 %, 36 % and 36 % below the
exact twin's in the three cases the writer checked. Every fitted 3D lifetime of walls is too short.
- Inference: for discs the `well` region is limited to ρ < R ≤ 12 a, well inside the border, so D2 should barely touch the disc
  and shell trapped shares. Measure it; don't assume it.

**D3. Both defects were known and written into the note instead of being fixed.**
- Fact: the chat measured "3–4 % during the collision, trapped state 10 % longer" on 13 November at 17:55 UTC.
- Fact: the old coordinating chat then ordered that error to be described in the note.
- Fact: the live note's section 11 gives transmission off by factors of 0.30 to 1.80 for some structures.
- The correction removes the errors; the note then describes the corrected method.

**History you must know.** On 13 November at 20:09 UTC the chat proposed building the walls exactly from 1D, and the owner
answered "Yes, but walls in 3D too". The owner wanted 3D pictures. The exact wall rebuild of section 4 is a true 3D field
(ψ = χ(x,t) h(y,t) h(z,t)), not a 1D picture. Say that plainly in every report about walls.

## 2. What you have

- **Branch to start from:** `claude/fig15-resonant-tunnelling` (tip dddec29). It holds the solver, the runner, the filer
  `file_rt3d2.py`, `tm.py`, `iv.py`, the audit scripts `notes/fig15/audit/*.py`, `notes/fig15/error_audit.json`,
  `notes/fig15/STATE.md` and `notes/fig15/BRIEF.md`.
- **Work on a new branch** `claude/fig15-correction`. Push only there. Nothing goes to `main` without the coordinator's word.
- **This brief and the coordinator's checks:** branch `ccr-0bb034eb-nkmdd2`, files `notes/fig15/CORRECTION.md` and
  `notes/fig15/coordinator/` (`mytm.py`, `twin.py`, the JSON results). Get them with
  `git fetch origin ccr-0bb034eb-nkmdd2 && git checkout origin/ccr-0bb034eb-nkmdd2 -- notes/fig15/CORRECTION.md notes/fig15/coordinator`.
- **Stored runs:** 3,697 files in R2. Read them over plain HTTPS at `https://phyeinusul.com/r2/<runs_base><file>`, with `runs_base`
  and `file` from `public/data/resonant-tunnelling/2026-11-14/kaggle/index.json`. Check each file's SHA-256 against the index.
  No token is needed or allowed for reading. File format: `tools/kaggle/resonant-tunnelling/read_rt3d.py`.
- **The groups:** walls 1,088 (613 unbiased, 475 biased); discs 2,327; shells 282.
- **Coordinator's test of Richardson extrapolation** (`richardson_sample2.json`, 40 random unbiased walls). It combines the
  stored run with a new run at half the spacing along x: T ≈ (4 T(0.25) − T(0.5))/3.
  - The stored 3D run plus a 0.25 a twin passes 28 of 40, median error 0.0027. It fails at N = 5 and 10, and near narrow peaks.
  - A 0.25 and 0.125 twin pair passes 38 of 40.
  - Conclusion: reusing the stored run this way helps, but alone it does not pass the gate everywhere.

## 3. The gate (put it in the filer; a failing run is refused, not filed)

- **Transmission:** |T_run − T_ref| ≤ max(0.005, 1 % of T_ref). The owner has not yet confirmed this tolerance. Use it
  provisionally and name it as provisional in every report.
- **Walls, also the curves:** the trapped-share curve and the x-profile, against the exact solution at the stored frame times.
  Propose a tolerance with its reason. The coordinator takes it to the owner.
- **The reference** must be exact (walls) or converged and independent (discs, shells). A run checked only against another run with
  the same grid is not checked: the 3D runs and their 1D twins agree to 0.0017 and are both wrong.
- **Record** each run's reference value and error in the index. That is how the page's three-way proof shows it.

## 4. Walls (1,088): exact, no GPU

Separation: V depends on x only and the start is a product. So for all time ψ(x,y,z,t) = χ(x,t) h(y,t) h(z,t), where h is the free
Gaussian, h(y,t) ∝ (1 + it/2σ⊥²)^(−1/2) exp(−y²/(4σ⊥²(1 + it/2σ⊥²))), with σ⊥ = `sp`.

**χ by superposition of stationary states.** χ(x,t) = ∫ φ(k) ψ_k(x) e^(−ik²t/2) dk.
- ψ_k is the scattering state incident from the left. For unbiased walls it comes from the transfer matrix. For biased walls, slice
  the ramp finely with faces on slice edges; `mytm.py` shows the slicing converge, identical at 500, 2000 and 8000 slices.
- φ(k) is the start packet's spectrum. The expansion in left-incident states is exact to within the packet's share at k < 0 and
  inside the barriers: the index stores `start_in_barrier`, about 10⁻⁶. State the bound.
- No time grid and no barrier sampling are involved, so neither D1 nor D2 can arise.

**What each rebuilt file holds:** exactly what the page reads, in the same RT3C format and at the same frame times as the stored
file:
- |ψ| and arg ψ on z = 0, y ≥ 0, sampled on the stored 0.5 a output points, as 8-bit levels of each frame's peak;
- the x-profile |χ|²;
- the region curves;
- T, and τ refitted.

**Check your writer:** feed it the grid twin's χ (the solver's own `run1d` at 0.5 a) instead of the exact χ. It must reproduce a
stored wall file to within the 8-bit steps. That proves your files match what the page plays.

**Then report, without filing:**
- how many of the 171 passing walls also pass the curve gate (D2);
- the three-way proof for 5 runs: the stored value, the value recomputed from stored inputs, and the pixel read back.

Whether to keep or rebuild the walls that pass T but fail the curve gate is the owner's decision. Ask through the coordinator.

## 5. Discs (2,327) and shells (282): references first, then the cheapest correction that passes

The packet starts on the x axis and moves along it. Discs are centred on that axis; shells are centred at the origin, which lies on
it. So ψ = ψ(x, ρ, t) with no angle dependence (m = 0):

  i ∂ψ/∂t = −½ (∂²ψ/∂x² + ∂²ψ/∂ρ² + (1/ρ) ∂ψ/∂ρ) + V(x, ρ) ψ.

This is an exact 2D problem. A shell is not a 1D radial problem, because the packet comes from one side.

1. **Build an axisymmetric reference solver.**
   - Use spectral flight along x and a discrete Hankel transform of order 0 in ρ (quasi-discrete, Guizar-Sicairos & Gutiérrez-Vega
     2004), or finite differences in ρ.
   - Hold V as cell averages, with faces between grid points.
   - Make the ρ range wide enough that the border cannot eat what the regions measure.
2. **Validate it:**
   - (a) A disc wider than the ρ range must give the exact wall answer.
   - (b) It must converge in Δx, Δρ and Δt. Give the table.
   - (c) Run it with rt3d2's own drawing rules at 0.5 a on a few stored runs. It must agree with the stored 3D T and curves to about
     10⁻³. That proves the reduction is the same physics as the stored data.
3. **Measure the cost per run** on this container's CPU, and estimate it for a T4 from measured step times. Launch nothing.
4. **Compute references for a stratified sample** of 60–80 stored runs: every R, every (V0, D, P), N = 3, 5 and 10, both shell
   sizes, biased discs, long packets, and points near and away from resonances.
5. **Test each reuse rule on that sample** and give its pass rate:
   - keep as stored;
   - difference rule: T_disc + (T_wall,exact − T_wall,stored) at the same V0, D, P, N, E, bias;
   - Richardson with the stored run (it needs one new run at 0.25 a; give its cost);
   - any rule you find that uses stored data and passes.
6. **Classify all 2,609 disc and shell runs** as keep, correct by a validated rule, or recompute.
   - Cost the recompute set on CPU and on GPU.
   - Frames: a scalar rule corrects only T and the curves. Ask, through the coordinator, whether the page needs corrected frames for
     every run or corrected curves plus a smaller set of frames.

**STOP after step 6.** Write the numbers into your state file and report. No mass computation before the owner's yes.

## 6. Afterwards (only on the owner's yes, through the coordinator)

- File the corrected data as a new generation with its own date, gate in the filer. The old generation stays with its audit.
- Duplicates (21 specs filed once for groups A and F) are never computed twice.
- The page changes only to read the new generation and show each run's reference and error. The note is revised afterwards.

## 7. How you work

- **First,** write `notes/fig15/CORRECTION_STATE.md` on your branch (aim, steps, numbers, files, commits, these rules). Keep it
  current and push it.
- **Read first:** `CLAUDE.md`, `AGENTS.md`, `notes/fig15/STATE.md`, `notes/fig15/LESSONS.md`, `docs/kaggle-pipeline.md`.
- **The owner:** BSc in physics (computational and theoretical).
  - Define every term at first use, metric units.
  - Mark Fact (with a handle: file:line or a command), Inference and Opinion.
  - Give the mechanism of each result in one line, in physics terms.
- **Forbidden:**
  - No GPU, no Kaggle launch, no R2 write or delete.
  - No change to `main`, the live page or any Worker.
  - No messages to other sessions except the coordinator.
- **Report** to the coordinator (session_01DGmqintkoYzahfGQQzdXYL, send_message) at each STOP, in at most 12 lines:
  - what you measured;
  - the handle to the numbers;
  - what you propose next.
- **Never relay another chat's number as Fact** until you have reproduced it.

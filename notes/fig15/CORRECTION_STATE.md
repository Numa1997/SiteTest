# Fig. 15 correction: state of the correcting session

Started 14 November 2026 by the correcting session (started by the coordinator, session_01DGmqintkoYzahfGQQzdXYL).
A chat that has lost its context rereads this file, then `notes/fig15/CORRECTION.md` (the brief), and continues from "Next".

## Aim
Correct Fig. 15 (resonant tunnelling, generation 2, 3,697 stored 3D runs) using the data already stored and exact physics,
recomputing only what no exact or stored-data route can fix. Ladder (brief section 0): keep what passes; exact answers
(walls); exact reductions (discs, shells are axisymmetric, m = 0); correction of stored data by validated rules; new computation
last, GPU only with the owner's yes on a bill.

## Rules (binding)
- No GPU, no Kaggle launch, no R2 write or delete, no change to `main`, the live page or any Worker.
- Messages only to the coordinator (send_message), at each STOP, at most 12 lines: measured, handle, proposal.
- Gate (provisional, not yet confirmed by the owner): |T_run - T_ref| <= max(0.005, 1 % of T_ref).
- Mark Fact (with handle) / Inference / Opinion. Never relay another chat's number as Fact before reproducing it.
- Wall rebuild is a true 3D field psi = chi(x,t) h(y,t) h(z,t); say so in every report about walls.
- Never write the owner's name.
- Owner, 14 Nov: after each big chunk of work, review online sources (GitHub, Kaggle, papers, other simulations) and learn
  from their experience before the next chunk. Learn, never copy. Read primary sources whole; say which tools answered.
- Branch `claude/fig15-correction` (from `claude/fig15-resonant-tunnelling` tip dddec29); push only there.

## Steps
1. [ ] Section 4, walls (exact, CPU): stationary-state superposition chi(x,t); writer in RT3C; writer check against run1d;
   curve gate (D2) count among T-passing walls; three-way proof on 5 runs.  -> STOP 1, report.
2. [ ] Section 5, steps 1-6: axisymmetric reference solver; validation (wall limit, convergence table, rt3d2 rules vs stored 3D);
   cost per run (CPU, T4 estimate); stratified sample of 60-80 references; reuse rules and pass rates; classification of the
   2,609 disc and shell runs.  -> STOP 2, report.

## Live work (14 Nov)
- Walls: CPU batch (rebuild_walls_all.py) stopped by the owner at 488 of 1,088 (records: notes/fig15/correction/walls_rebuild.jsonl,
  files in scratchpad rebuilt/). The other 600 (correction/walls_left.json) run on Kaggle: numakoudsie/fig15-correction-walls-exact
  v1, kernel 144992045, launched ~12:40 UTC, commit 63fddef, exact_wall_jax.py (complex128, checked against the CPU code on one run:
  T to 6e-9, levels to 1, curves to 1e-7). Quota before launch: 48,167 s used of 108,000.
- Owner, 14 Nov: when everything is done, integrate ALL data into one new generation: kept stored runs + 1,088 exact walls
  (488 CPU + 600 GPU) + 2D discs and shells, one index.

## Run of the "complete brief" (14 Nov, ~13:00-13:15 UTC)
- Step 1: branch at 7e75d4b; Kaggle connector loaded; quota 48,167 s used of 108,000 s (resets 21 Nov 00:00 UTC); R2 check
  `curl -sS https://api.cloudflare.com/client/v4/accounts` returned "success" with one account.
- Step 2 (commit e5ba25a): wall_gpu_run.py rewritten: reads walls_all.json (all 1,088 walls, 475 biased, 13 geometry groups),
  START/STOP range, batches each group with jax.vmap (k padded with zero weights; adaptive batch <= 8 from a memory estimate),
  checks the first wall of each group against the verified single-wall path (dT <= 1e-9, levels <= 1) and falls back to it on any
  mismatch or error; pip-install fallbacks in wall_gpu_run.py and rt2d_run.py replaced by the GPU backend check; loaders
  (walls_gpu.ipynb.tmpl, build_rt2d.py) check the backend first. NOT run locally (brief: no computing in the container).
- Step 3: numakoudsie/fig15-correction-walls-gpu v1, kernel 144997790, walls 0-100, commit e5ba25a, saved ~13:09 UTC.
  get_notebook_session_status returned {} at ~1 min and at ~3 min (13:13 UTC): no session started (same symptom as
  fig15-correction-walls-exact v1). get_notebook_info shows the notebook saved, current_version_number 1, last_run_time
  "2026-11-11T13:13:11Z" (a date three days off). STOPPED per the brief; owner asked to open the notebook page.
- Not launched: walls-gpu-2, 2d-smoke, 2d shards, filing. Smoke loader built (scratchpad), not saved to Kaggle.

## Numbers (filled as measured)
### Walls, exact solver (`tools/kaggle/resonant-tunnelling/correction/exact_wall.py`)
- Method: chi = Int dk/2pi [c+ psi+ + (k/kR) c- psi-] e^{-iEt}; both scattering families (left- and right-incident), exact
  projections c+- = <psi+-|chi0> (closed form + numeric tail correction), flux integrals for left/right shares.
- Closure P_left + P_struct + P_right = 1 to 2.5e-6 .. 2.4e-5 (sx = 12). Share carried by the two families 0.99998-1.0000;
  the missing part is bounded by the start packet's share right of the first face (start_in_barrier).
- Convergence (scratchpad conv.py): dk 5e-4 -> 2.5e-4 changes T by <= 3e-6, P_well <= 1e-5, |chi|^2 <= 3.5e-5 (N = 10, t 221);
  bias slicing 2000 -> 8000 changes T by 8e-9; fine grid 0.01 -> 0.005: <= 2e-9.
- vs coordinator's mytm.packet_T: unbiased N=2 E=0.3: 0.0085371 vs 0.0085371 (|G|^2 weights) and 0.0085558 (true packet, tail
  included); biased B=2.125 E=0.5: 0.0390478 vs 0.0390475.
- Bug found and fixed in my own code: weight of right-incident states under bias was kR/k, must be k/kR (T came out 1.47).
### Writer check (`rebuild_wall.py twin`), flat_N2_V2_D1_P2.5_R0_B0_s3_E0.300
- The grid twin's chi equals the stored prof1d to 4.6e-8 (relative). Rebuilt |psi| levels: max diff 1 level (1.1 % of points);
  arg levels: max diff 1 where |psi| >= 10 levels (<= 3 where 3-10 levels).
- NEW finding (Fact, measured): the stored 3D run loses norm steadily from t = 0, before any wave reaches a border: 3D transverse
  share / exact discrete transverse share = 0.99981 at t 4.5, 0.99784 at t 45, 0.99536 at t 89.6. Cause NOT yet known. My first
  inference (float32 rounding of the kinetic factor) is ruled out by measurement: weighted over the packet's spectrum it removes
  3.6e-9 per step, 3.2e-5 over the run, 1/140 of the loss. Remaining suspects: the float32 FFT itself on the GPU. Effect: curves
  up to 2.4e-3 low. The 2D solver must show its own drift below 1e-3 (owner's rule).

### 2D solver, first measurements (`correction/axisym_jax.py`, CPU, complex128)
- Wall limit, N2 V2 D1 P2.5 E0.75 sx3, hx 0.0625, Nr 64, Rmax 40, t 100: exact T 0.196820.
  Box 96 a, dt 0.01: 0.200847 (+0.0040). Box 192 a, dt 0.01: 0.196889 (+7e-5). Box 96 a, dt 0.0025: 0.210937 (+0.014).
  Norm drift (|psi|^2 + absorbed - 1): 1.2e-12. CPU 3.7 ms per step at 98,304 cells (4 cores shared with the wall batch).
- Fact: the sin^(1/8) mask applied every step reflects part of the wave back; its strength grows as 1/dt (the mask is a CAP of
  imaginary height -ln(m)/dt). This explains the predecessor's "unexplained" +0.004 at dt 0.0025 (BRIEF 3). Inference: the stored
  3D runs carry the same reflection from their x and side borders. Rule for the references: box 2x the stored one (reflection
  returns after the read time), and measure it.

## Outside sources, part B (14 Nov, 20 min; WebSearch and WebFetch answered, pdftotext read the PDF)
1. Order-0 QDHT (Guizar-Sicairos & Gutierrez-Vega 2004) is the standard radial transform: pyhank (pyhank.readthedocs.io) uses it
   for radially symmetric beam propagation, replacing the 2D FFT across by one 1D transform; XMDS2 has a "bessel" dimension used
   for cylindrical Gross-Pitaevskii runs (testsuite bessel_cosine_evolution.xmds), grids 64x256 to 160x1024 (arXiv 2005.00368).
2. Both note the Bessel basis imposes psi = 0 at the outer radius: a wave reaching it reflects unless absorbed first.
3. Yu & Esry, arXiv 1710.04338 (read): judge an absorber by its reflection R(k) for stationary states, R <= Rc over [kmin, kmax].
   The absorber must be long enough to hold the longest wavelength: for an exponential CAP, kmin * beta >= 1.1 for Rc = 1e-3.
4. The rt3d2 border is the cos^(1/8) mask (their Table I, "cosine masking function"); they find optimised exponential CAPs
   need 3-4x less range for the same R. Inference: slow components (small k, e.g. transverse spreading) reflect off a 6 a mask.
5. For the 2D solver: make the rho absorber at least ~10 a and measure its reflection (Rmax 40 vs 60); count what it absorbs.
6. Float32 drift: no source measures it for split-step; NVIDIA forum report: accumulate sums in float64. My own test rules out the
   kinetic factor (above). The 2D solver runs complex128 on CPU; on the T4 measure the drift before trusting float32.

## Files and commits
- `notes/fig15/CORRECTION.md`, `notes/fig15/coordinator/*` (brief and coordinator's checks, from branch ccr-0bb034eb-nkmdd2)
- this file

## Next
Section 4: exact chi(x,t) for one wall run, compared with the stored file.

## 13:20-13:30 UTC, owner: "run the GPU scripts"
- create_notebook_session (slug fig15-correction-walls-gpu) at 13:20 started a run (search_notebooks: last_run_time 13:20:36;
  quota climbing ~1 s/s from 48,167 s). get_notebook_session_status keeps answering {} even while it runs: not a reliable signal.
- A save_notebook for version 2 was refused: "Maximum batch GPU session count of 2 reached" -> two batch sessions are held:
  walls-gpu v1 (13:20) and walls-exact v1 (12:28, the old 600-wall job). cancel_notebook_session is denied in this session.
- file_corrected.py (step 9) written: gate, statuses kept / rebuilt / recomputed / failed / missing, diode J(V) from T_ref.
- 13:29 UTC: owner stopped walls-gpu and walls-exact by hand. Tracker added (commit 54cf2c7): ETA lines, timing.json, CALIB mode.
  Launched numakoudsie/fig15-correction-walls-calib v1 (kernel 145000508, two batches per group, timeout 3600 s); started 13:29:55.
  Quota at 13:31: 48,930 s. Another session's notebook (fig-16-guinness-cart-with-control, 13:28) holds the second GPU slot.
  Live tracking: Kaggle shows logs only after a run ends; ntfy.sh relay was refused by this session's permission check.
- 14:19 UTC: owner allowed ntfy.sh for the live tracker, this use only. Commit c53a447: say() pushes progress lines (every 30 s,
  key events at once) to a private-name ntfy.sh topic given by the loader (topic kept out of the repository).
- walls-calib v1 (13:30, no tracker): never released output; quota froze at 51,863.9 s by 14:32-14:41 (no session running).
  sessionTimeoutSeconds 3600 did not show as a stop at 14:30 (output list stayed empty).
- 14:42 UTC: numakoudsie/fig15-correction-2d-smoke v1 launched (kernel 145008546, commit c53a447, tracker on).
  walls-calib v2 refused: "Maximum batch GPU session count of 2 reached" (second slot held).
- 2D smoke v1 (14:42): A1 c64 wall limit T 0.196539 (exact 0.196820), drift 2.7e-3, 1.068 ms/step at 786,432 cells;
  A1 c128 T 0.196889, drift 2.6e-12, 8.060 ms/step. Then crashed: TypeError in axisym_jax's fori_loop carry (float32 vs float64
  after the c128 run left x64 on). Fixed in 17ffd02 (explicit dtypes). Smoke v2 launched ~14:58 (tracker topic suffix -smoke2).
  Inference: c64 drift 2.7e-3 > 1e-3 fails the brief's gate -> c128 needed; bill ~ 28.7 M steps x 8.06 ms / 2 = ~116,000 s.

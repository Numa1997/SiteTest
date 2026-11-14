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
  share / exact discrete transverse share = 0.99981 at t 4.5, 0.99784 at t 45, 0.99536 at t 89.6. Inference: complex64 rounding of
  the kinetic phase factor on the GPU (|exp(-i K^2 dt/2)| != 1 in float32), about 4e-7 per step. Effect: curves up to 2.4e-3 low.

## Files and commits
- `notes/fig15/CORRECTION.md`, `notes/fig15/coordinator/*` (brief and coordinator's checks, from branch ccr-0bb034eb-nkmdd2)
- this file

## Next
Section 4: exact chi(x,t) for one wall run, compared with the stored file.

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
- Branch `claude/fig15-correction` (from `claude/fig15-resonant-tunnelling` tip dddec29); push only there.

## Steps
1. [ ] Section 4, walls (exact, CPU): stationary-state superposition chi(x,t); writer in RT3C; writer check against run1d;
   curve gate (D2) count among T-passing walls; three-way proof on 5 runs.  -> STOP 1, report.
2. [ ] Section 5, steps 1-6: axisymmetric reference solver; validation (wall limit, convergence table, rt3d2 rules vs stored 3D);
   cost per run (CPU, T4 estimate); stratified sample of 60-80 references; reuse rules and pass rates; classification of the
   2,609 disc and shell runs.  -> STOP 2, report.

## Numbers (filled as measured)
(none yet)

## Files and commits
- `notes/fig15/CORRECTION.md`, `notes/fig15/coordinator/*` (brief and coordinator's checks, from branch ccr-0bb034eb-nkmdd2)
- this file

## Next
Section 4: exact chi(x,t) for one wall run, compared with the stored file.

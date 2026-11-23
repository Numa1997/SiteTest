# 0004 report (final, after 0005): energy-closure audit of 4.5. (a) refuted; (b) partial only; (c) adjoint break PROVED, ratio 3.09, mostly interior foam, not rotation, not the mass floor; (d) books telescope exactly, projection adds energy

23 Nov 2026, 22:25 UTC. Final full run: Kaggle CPU, step4-energy-audit-cpu v4, 21:34:12-22:16:24 UTC, code 49839c5 (enable_ls_extend fix
of 0005 included). GPU used: 0 s. Outputs notes/spill/step4/audit_0004/full_v4/. Marks as fixed in da8f611, unchanged.
Default path (Fact, full_v4/default_path_identity.json): at 1.5 mm, 3 steps of the 4.5 set-up, every state array of the 5acb718 solver
equals the current solver's bit for bit (audit off), and the motion is identical with audit on. The fix and the logging change nothing.

## Step 4, the 3 mm instrumented slosh, window 0.2009-1.0015 s (Fact, full_v4/slosh_audit_full_summary.json; 653 steps, no particle lost)
Raw table (Neon section 5), mJ:
| -dKE 0.0370 | -dPE 1.2618 | -dU_el 0.0153 | -dE_mech 1.2988 | -dE_tot 1.3141 | PE(t_b) - PE(0) -0.148 |
| E_plastic 0.8711 | E_drop 0.9033 | E_wall_foam 0.5103 | E_wall_stout 0.0869 | E_visc_stout 0.0091 |
| W_stress_grid 0.2771 | W_constit 0.8558 | ratio 3.088 | E_num -0.1632 | closure on E_tot (all sinks) 1.124 |
E_plastic split: mass-floor particles 0.0960, within 1.5 dx of the wall 0.2345, interior 0.5406. Shadow cell-strain (no rotation)
E_plastic_cellD 0.9190 (E_plastic - cellD = -0.048). Grid work on mass-floor faces -0.041. U_el(0.2) 0.0186, U_el(1.0) 0.0033.
Ledger (window sums): dE_P2G +2.5058, dE_visc -0.0091, dE_wall -0.5971, dE_dev -0.2771, dE_grav_proj +0.0878, dE_G2P_coll -3.0091;
sum -1.29880 = dE_mech -1.29880.
| mark | number | result |
| (b) min(U_el) >= -1e-12 J | 0.0 | PASS |
| (b) U_el(0.2) > U_el(1.0) | 0.0186 > 0.0033 mJ | PASS |
| (b) alone explains: sinks/(-dE_mech) > 1.25 and r_tot <= 1.02 and abs(r_tot - 1) < 0.25 | 1.130, r_tot 1.117 | FAIL (b not the sole cause) |
| (b) r_tot > 1.05: partial contributor only | 1.117 | PASS (partial only) |
| (c) adjoint abs(W_constit / W_stress_grid - 1) < 0.05 | 3.088 | FAIL |
| (c) proved: W_constit / W_stress_grid > 1.15 | 3.088 | PASS (c proved) |
| (d) telescoping abs(sum - dE_mech) < 1e-7 J | 2.5e-16 J | PASS |
| (d) wall logger abs(-dE_wall / (E_wall_foam + E_wall_stout) - 1) < 0.02 | 1.0000000004 | PASS |
| (d) dE_grav_proj <= 0.02 (-dE_mech) = 0.026 mJ | +0.088 mJ | FAIL |
| (d) dE_G2P_coll <= 0.02 (-dE_mech) | -3.009 mJ | PASS |

## What the numbers prove or refute
- (a) factor bug in the e_plastic line: REFUTED (slab: E_plastic / W_grav 1.0019, / E_drop 0.9891).
- (b) missing elastic store: REAL but small: -dU_el 0.015 mJ at 3 mm; partial contributor only.
- (c) F_dev / C not adjoint: PROVED. The foam's constitutive work (0.856 mJ) is 3.09 times the work its stress force takes out of the grid
  (0.277 mJ). Where (Fact): 62 % of E_plastic is interior foam, 27 % near the wall, 11 % at mass-floor particles; the no-rotation shadow
  gives the same E_plastic within 5.5 % (0.919 vs 0.871), so the rotation term and the mass floor are not the main cause at this grid.
  Inference (not tested): the strain rate C read by G2P carries velocity differences that the stress force did not create (projection,
  friction, the P2G/G2P transfer), so the return map dissipates energy that the transfers also remove; the books then count it twice.
- (d) books: the six sub-steps telescope to round-off and the wall logger is exact. The pressure-plus-gravity step ADDS 0.088 mJ (6.8 % of
  -dE_mech) over the window: a second, smaller error in the projection (cut cells, Inference). P2G/G2P swing +2.51 / -3.01 mJ, net -0.50.
- Grid dependence (Fact): the overshoot is +13 % at 3 mm (sinks / -dE_mech 1.130) against +51 % at 1.5 mm (4.5 Part C). Not explained yet.

## Rotation check and slab (as before, unchanged in v4)
Rotation: max s 7.48 Pa, E_plastic 1.89 J/m^3, both FAIL as set by construction (yield after 108 steps at 30 rad/s). Slab marks: W_grav
PASS, E_drop PASS, W_stress_grid FAIL (badly defined: floor faces; 0.670 above them).

## Needs the owner
- The fix is decided after this report (0004). Candidates the numbers point to: make the stress force and the return map work-consistent
  (C from the same grid velocity the stress force acted on), and look at the projection's +0.088 mJ. No change made.

## Clean up
- Kept: notebook step4-energy-audit-cpu (the fix will need a rerun), all outputs. Scratch launch files deleted.

---
Earlier sections (before 0005), kept for the record:

# 0004 report: energy-closure audit. Test (a) refutes a factor bug in E_plastic; rotation check fails as predicted; the 3 mm slosh (b, c, d-ledger) is blocked by an old crash in enable_ls_extend (needs the owner)

23 Nov 2026, ~21:30 UTC. Branch claude/guinness-projection-fix. GPU used: 0 s. Every run on Kaggle CPU, notebook step4-energy-audit-cpu
(v1 smoke 20:59:32-21:00:39 UTC, code bdf2bbd; v2 full rot+slab 21:21:33-21:22:39 UTC, code d96331d). Outputs:
notes/spill/step4/audit_0004/smoke_v1/ and full_v2/. Marks were fixed before any run (STATE-projection-fix.md, "0004 step 5", da8f611).
Solver default path: unchanged (every added line runs only under Stout.audit, default False; step4_slab.py only under EAUDIT=1). The
bit-for-bit check against 5acb718 (block "ident") could not run: it hits the same enable_ls_extend crash at 3 mm (below).

## Step 1, Neon's numbers from the repo (Fact)
All found: h 0.018 m whole layers, tau_b 1.5 tau_y, +0.49 % (notes/spill/step4/README-4p3.md row C1, diag_4p3.json); s/G 0.0488;
4 266 mass-floor faces = n_floor_max of the 22 Nov pre-fix run (slosh_head_summary.json:34); the fixed run's maximum is 4 204.

## Step 2, test (d) on the committed 4.5 log (slosh_head_fix.jsonl)
| mark | number | result |
| window integrity abs(reported - cum diff) < 1e-9 J | 3.43e-8 J | FAIL as written |
| PE drift abs(PE(1.0) - PE(0)) / (-dE_mech) < 0.05 | 0.026 (PE fell 0.033 mJ) | PASS |
Window: the 3.43e-8 J is a sampling difference (steps at t 0.20015 and 1.00076 s), 5e-5 of the 0.65 mJ gap; the 0.379 mJ of plastic
work before 0.2 s is not in the window. No PE swelling. floor_w in 4.5 covers every closed w face, including vertical wall faces (Fact,
stout_jax.py:519-531 at 5acb718; Geometry body=F16 makes Stout.cont True).

## Step 3, test (a): 4.3 slab energy identity, window 1.0008-2.0 s (Fact, full_v2/step4_slab_energy_4.3_T2s_h18mm_jz0_full_summary.json)
E_plastic 1.4386e-6 J; W_grav 1.4359e-6 J; E_drop 1.4545e-6 J; W_stress_grid -1.5685e-5 J (all faces); above the floor faces 2.1486e-6 J;
energy wiped on the floor faces 1.7865e-5 J; dKE -3.4e-13 J; dU_el 4.4e-11 J.
| mark | number | result |
| abs(E_plastic / W_grav - 1) < 0.03 | +0.0019 | PASS |
| abs(E_plastic / E_drop - 1) < 0.02 | -0.0109 | PASS |
| abs(E_plastic / W_stress_grid - 1) < 0.03 | ratio -0.092 | FAIL |
Candidate (a), a factor 2 or sqrt 2 in the e_plastic line: REFUTED (E_plastic matches gravity's work to 0.19 % and the return map's
free-energy drop to 1.1 %).
The third mark is badly defined for this slab (kept, raw number reported): W_stress_grid is taken before the no-slip floor faces are set
to zero, and those faces carry 1.79e-5 J, twelve times the plastic work. Without them, E_plastic / W_stress_grid_above_floor = 0.670.
Inference (not tested): even in the slab the grid work of F_dev and the constitutive work do not match face by face; this bears on (c).

## Step 4, test (c) rotation check (Fact, full_v2/rotation_check.json): 1 000 steps, Omega 30 rad/s, dt 7.67e-4 s, from be = I
| mark | number | result |
| max_s_rot < 0.05 tau_y (0.27 Pa) | 7.48 Pa | FAIL |
| E_plastic_rot == 0 | 1.89 J/m^3 | FAIL |
Set to fail by construction (step 5 note): f = I + dt C gives s growing about 0.051 Pa per step (predicted 0.0509); yield is reached at
step 108 (0.083 s of pure rotation). Inference: wherever the foam spins at tens of rad/s, rotation alone makes stress and plastic work
that take no energy from the grid; it inflates E_plastic. Its size in 4.5 is not measured yet (needs the slosh run).

## Step 4, tests (b), (c) adjoint and split, (d) ledger: NOT RUN
The 3 mm slosh fails at set-up, in the 5acb718 solver and in the current one: enable_ls_extend, `idx[new, k] = (I[:, 0] * ny + I[:, 1]) * nz
+ I[:, 2]` (stout_jax.py:826) writes all rows into the rows not yet found; it works only on the first push pass. At 1.5 mm every solid
cell is found on the first pass, so it never failed; at 3 mm some need a further pass ("shape mismatch (3348,) vs (8,)"). The one-line
fix indexes the right side by [new], as the wts line below it already does. It is a solver change, forbidden by 0004 rule 6.

## Which candidates (so far)
- (a) factor bug in E_plastic: refuted.
- (d) window leak and PE swelling: refuted (step 2). The sub-step ledger is not run.
- (c) rotation term: proved to exist and to make plastic work from rotation alone; its share of the 0.65 mJ is not measured.
- (b) and the (c) adjoint ratio: not measured.

## Needs the owner
- Allow the one-line enable_ls_extend fix (`... [new]`), then the 3 mm slosh and the bit-for-bit identity check run (CPU, about 1 h).
  The identity check against 5acb718 at 1.5 mm would show the default path unchanged. Alternative without a solver change: run the slosh
  at 2 mm if the crash does not fire there (unknown, about 4-5 h CPU).

## Clean up
- Kept: notebook step4-energy-audit-cpu (the slosh run still needs it), all outputs committed. Scratch launch files in the session scratchpad
  deleted. The worker session (stopped on the owner's order) left only the committed marks and code, reviewed line by line before keeping.

# 0004: find why the 4.5 energy books do not close: Neon's four discriminating tests (from the coordinator, 23 Nov 2026)

The owner sent our 4.5 energy-closure problem to Neon (Gemini). Its full answer is in
`notes/coord/neon/2026-11-23-energy-closure-answer.md`; read it whole first. Summary of what it says:
- (a) Factor convention: s = sqrt(tau:tau/2) and gp = sqrt(2 Dp:Dp) ARE work-conjugate with factor 1, and backward Euler
  slightly UNDER-counts the step's free-energy drop. So a factor 2 or sqrt 2 can only be a typo in the e_plastic line.
- (b) U_el = sum V_p (G/2)(tr be - 3) is missing from the stores; it is released after the push and feeds E_plastic without
  lowering E_mech. Real, but estimated 0.06-0.24 mJ, too small alone for the 0.65 mJ gap.
- (c) Its top candidate: the stress force on the grid (F_dev) and the gradient C that drives the return map are not discrete
  adjoints: mass-floor attenuation alpha_f = M_f/max(M_f, m_floor) < 1 weakens F_dev while G2P feeds the unattenuated velocity
  into C; closed wall faces and extrapolated air faces; and f = I + dt C under pure rotation gives f f^T = I + dt^2 Omega Omega^T,
  i.e. stress from rotation alone. All of these make the logged E_plastic larger than the work the stress really took out.
- (d) Bookkeeping: E_plastic window leak from the push, PE swelling (0.15 mm rise = 0.67 mJ), projection or pushback energy injection.

## Do this, in this order. Every model run on Kaggle CPU (0 GPU-min); reading the committed 4.5 log needs no run.
0. Ack at once.
1. Check Neon's numbers that come from our repo before using them (test 4.3 slab: h, tau_b, s/G; the 4 266 mass-floor faces;
   4.3's 0.49 % match). Report each as found or not found, with file and line.
2. Test (d), log part, on the committed `notes/spill/step4/slosh_head_fix.jsonl`: window integrity of E_plastic over 0.2-1.0 s,
   PE(1.0) - PE(0.0) against -dE_mech, and whether floor_w was active on vertical wall faces in that run. Marks as in Neon's
   section 4 (d).
3. Test (a): the 4.3 slab energy identity (E_plastic vs W_grav, E_drop, W_stress_grid). Marks as in Neon's section 4 (a).
4. Tests (b), (c), (d)-ledger together in ONE instrumented coarse slosh on Kaggle CPU (dx = 3 mm, same push, to 1.0 s): log U_el,
   W_stress_grid, W_constit, the E_plastic split (mass-floor / wall / interior), the shadow cell-strain E_plastic_cellD, the
   sub-step energy ledger; plus the 1000-step rigid-rotation unit check. Marks as in Neon's section 4 (b), (c), (d).
5. Before any run: check that every pass mark is reachable by construction (handoff rule 6), and fix the marks in the report
   before the numbers exist. If a mark is badly defined, keep it, report the raw number, and say why.
6. Change nothing in the solver and tune nothing. This instruction only measures. Instrumentation goes behind flags that leave
   the default path bit for bit unchanged.
7. One notebook per purpose (new versions, not new notebooks). Clean-up rule as always; never delete old work before the new
   result is verified.

## Report
`notes/coord/to-coordinator/0004-report.md`: each test, each mark PASS/FAIL with its number, which candidate(s) the numbers
prove or refute, and the raw energy table Neon lists in its section 5. Stop there; the fix is decided after the report.

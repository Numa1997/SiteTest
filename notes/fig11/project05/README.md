# Project 05: the cart must reach its target, rods up, in a liquid

Diagnosis scripts from session_01DGmqipN2AgsvWVoWUUtBT6 (6 November 2026). Each is a Playwright script; serve `public/`
with `python3 -m http.server 8765 --directory public` and run `NODE_PATH=$(npm root -g) node <script>`.
They drive the page through the `window.DIPC` hook (page line ~1840): `ds`, `p`, `fluidQ`, `fieldV`, `fluidPar`, `mode`, `W()`, `cLevel`, `log`.

| Script | What it shows |
|---|---|
| why.cjs | medium set mid-run (MEDS=water,honey): t, x, θ1, θ2 (deg), mode, W, c* every 0.25 s, then the supervisor log |
| cstar.cjs | the certified level c* per medium |
| target.cjs | does the cart reach x = +1 m with the rods up, per medium |
| hold.cjs / stuck.cjs | balancer alone holding / where the cart stalls |
| plan.cjs | does the swing-up planner find a path when drag is in its model |
| lin.cjs | the drag linearisation checked against rhs / rhsF |
| kchk.cjs | the redesigned gain K with drag (lqDrag) |
| shoot.cjs | "did we shoot?": bang-bang energy pump u = −u_max sign 𝒫 for 20 s per medium and force limit; motor's work, heat of the cart's and the rods' drag, highest share of the lift reached (lecture note 13.7) |
| machine.cjs | the planner (drag in its model) for other machines: MACH="m0/m1/m2/L1/L2/F;…" |
| swing.cjs | the swing-up in the running page: MACH, MEDS, GO/GOAT (press "to +1 m" at second GOAT), SHOT (screenshots) |
| honeyhold.cjs | the balancer holding upright rods in honey (written while a test switch existed; the switch is gone, see below) |
| own_proof.cjs | the generalised force Q from a given field, per medium (field really pushes; still fluid gives 0) |

## What was done with it (6 November 2026, session 2)

Merged to main: the test switches (planDrag, lqDrag, pumpOn, superOn, rescueOn, CLO setters) are gone; drag in the planner and in
the balancer's design, the pump after a failed plan and the low start of the c* search are now fixed page behaviour. Scripts that
set a switch (plan.cjs, why.cjs with superOn, honeyhold.cjs, kchk.cjs) record how the diagnosis was made; with the switch gone the
assignment is ignored and they measure the page as it is.
Two changes in supervise(): in a medium the guard keeps the balancer while the model shows W lower by a tenth after 4 s; at a
catch in a medium the reference is fixed where the cart was caught (a cruise (25) needs a push against drag that (25) leaves out).
Measured: default machine, 60 N: the cart reaches +1 m upright in water and glycerol (16 s), honey 0.84 m after 24 s. Swing-up:
none in any liquid with the default machine at 60 or 200 N (shoot.cjs, plan.cjs); with rods 2 kg, 0.20/0.25 m and 200 N, the
page swings up in water, catches at 14 s and reaches +1 m (swing.cjs); still none in glycerol or honey.

## Later, not now

Numa's idea (6 November 2026): give the cart a sense of its surroundings, sound waves sent out and their reflections read back
(sonar), to sense the flow or obstacles. Not built.

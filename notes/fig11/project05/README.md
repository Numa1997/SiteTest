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
| own_proof.cjs | the generalised force Q from a given field, per medium (field really pushes; still fluid gives 0) |

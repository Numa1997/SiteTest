# Project 06: measurements of the liquid machine

Scripts of session_01DGmqimmNH2QUM3GJS4w2gK (7 November 2026). Serve `public/` with `python3 -m http.server 8765 --directory public` and run
`NODE_PATH=$(npm root -g) node <script>`; each drives `rods-in-liquid.html` through `window.DIPC` (PAGE=… for another page).
What they gave is in [docs/simulations/project06-rods-in-liquid.md](../../../docs/simulations/project06-rods-in-liquid.md) and the
lecture note's 13.7–13.8.

| Script | What it shows |
|---|---|
| paddle.cjs | (48): ω_need and the liquid's ω_t for project 05's outer rod, a 2 kg rod and project 06's, per liquid (plain Node) |
| plans.cjs | the swing-up planner from hanging, per machine (MACH) and liquid, horizons 3 and 4 s: found or not, steps, gap, force, time |
| swing.cjs | the swing-up in the running page, then "to +1 m" (GO, GOAT); t, x, angles, mode every second; screenshots with SHOT |
| drag.cjs | grab the cart with the mouse in a flow, drag, hold, let go; the flow's rest state, rescue or not, the page time of release and catch, and how close the rods come back |
| release.cjs | the same in still water, sampled every 0.2 s with unwrapped angles: the rods fall while held and are caught after |
| flick.cjs | which flick J the balancer catches, per liquid |
| challenge.cjs | the deep flows' starting strength U per liquid: the running page, supervisor included, for 120 s after the flow is chosen while balancing (STEP, TOP: the grid; honey in 0.01 m/s) |
| switchon.cjs | choose each deep flow while the rods balance and watch 60 s: held or knocked down, the largest gap to the rest state |
| samecode.py | the two pages' inline scripts, the settings block aside, compared character for character |
| i18n/validate.py | checks German and Arabic translations (tags, maths, markers, numbers) before `tools/i18n/fill.py` stores them |

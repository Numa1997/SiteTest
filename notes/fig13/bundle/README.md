# fig13-bundle: what is in here

Made on 8 November 2026 while identifying and reproducing the "spirographs in momentum space" picture from 2swap's "Double Pendulums are Chaoticn't" (https://www.youtube.com/watch?v=dtjb2OhEQcU, about 7:08–7:20). Start with `PROMPT.md`. The video frame and Numa's photo of it are not included (public repository, 2swap's frame): watch the video at 7:08–7:20.

| Path | What it is |
|---|---|
| `PROMPT.md` | The task for the Claude Code session: facts, theory to study, where it goes, build, checks, publish, skills |
| `prototype/simulations/momentum-spirographs.html` | Working prototype in the Phyein Usul design. Live RK4 in JS, 10 × 10 grid, fading trails, rods, chaos map, panel, schematic (Figure 1). Expects the repo's `../styles`, `../fonts`, `../images` next to it (symlink `public/` folders to test). |
| `prototype/simulations/fig13-map.png` | Chaos map 384 × 216, house palette (rose to wine, alpha by chaos), made by `compute/map2png.py` |
| `compute/sim.py` | NumPy: tip paths of the 10 × 10 grid at a step of 1/9000 s for 12 s (`python3 sim.py OUTDIR`), and the twin-pendulum chaos map (`python3 sim.py OUTDIR 384 216`, about 200 s on 2 cores) |
| `compute/map2png.py` | Map to RGBA PNG: log10 of the mean twin distance, 2 to 99.5 percentile stretch |
| `compute/shot.cjs` | Playwright: serves on :8813, advances the page to t = 6 s, takes screenshots, reads back inked pixels (alpha first), dumps JS tips |
| `data/paths.npz` | `tips[k, (x, y_up), cell]` every 10 steps (900 per second), plus p1, p2, E0, and the energy drift (max 1.56e-6) |
| `data/map.npz` | `mean_dist` (216 × 384), `E` at θ = 0, axes gx (p1) and gy (p2) |
| `data/js_tips.json` | Browser tips at t = 6 s. Agree with `paths.npz` to within 5.8e-8 m |
| `screenshots/` | Prototype page at 1440 × 1000 @2x, the figure alone, the schematic |
| `sources/swaptube/` | Files from github.com/2swap/swaptube (Unlicense, public domain; LICENSE included). The 2025-07-17 versions (commit d7f4d55) of PendulumScene, PendulumGridScene, PendulumFractal.cu and PendulumHelpers; current master PendulumHelpers.h (0cab4c0); and the deleted project file of the video (`DoublePendulum.oldproject`, momentum-space part at about lines 410–545) |

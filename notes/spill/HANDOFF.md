# Handoff: the continuous spill model (branch claude/continuous-spill), 18 Nov 2026, from session_01DGmqioyaYR5VnnZaKfpEhD

Stopped by the owner; all work passes to session_01DGmqipAnEdVvBLCf7CLGmT. Nothing here is merged or live. Branch from main e1a72d7;
`git merge-tree` against main 75343c8: no conflicts. Full history: notes/spill/STATE.md. Rule kept: nothing ran in a container.

## 1. Changes to tools/fig12/kaggle/stout_jax.py, by function (old model unchanged bit for bit when body=None: smoke check 1)
- Constants: RHO_AIR = 1.204 kg/m^3, MU_AIR = 1.81e-5 Pa s (air 20 C, 101.3 kPa; for air_drag).
- Geometry(R, dzp, fill, dx, body=None): new argument body = (hx, hy, z_top). With body: square grid n = ceil(2(max(hx,hy)+2dx)/dx),
  z0 = -(ceil(-z_top/dx)+4) dx (cavity floor z = 0 on a face), top 30 mm above the rim; open fractions from open() = not solid();
  a face is closed when the segment between its two cell centres crosses solid AND both centres are open (thin wall must not couple
  inside to outside; cut cells whose centre is in the wall keep their fractions, as in the old model); wallcut limited to the band
  |r - R| < dx/2; cavc = cavity(); lsdom = cav_inner inside the cavity, every open cell elsewhere; wall area by _wall_area_solid.
- Geometry.cavity(x,y,z): z > 0 and r < R(z). Geometry.solid(x,y,z): glass wall R(z)..R(max(z,8 mm))+2.5 mm for 0<z<rim, foot
  r < Rout for z_top<z<=0, body |x|<hx,|y|<hy for z<=z_top. Geometry.open = not solid. Geometry._wall_area_solid: solid surface area
  per cell from 4x4x4 sample crossings, |(Ax,Ay,Az)| x 4/3. Geometry.WALL = 2.5 mm. Old _wall_area kept for body=None.
- Stout.__init__: self.cont = body is not None; floor_w = all closed w faces when cont; self.gamma = GAMMA when cont, else 0;
  self.lsdom from Geometry.
- level_set: empty-cell mask uses lsdom (= cav_inner when old); mirror images only for particles inside the cavity when cont.
- tension(ph, hf, dt) NEW: Young-Laplace jump gamma kappa (kappa = div grad phi/|grad phi|, clipped to 2/dx), as the surface's
  pressure in solver units, where no head lies and |phi| < 2 dx. pressure(..., pst=None): pst added to the surface load ps3.
- air_drag(vel, mass, ph, liq, dt, wind) NEW: headwind = (-v_x, -v_z) of the glass on liquid outside the cavity; Schiller-Naumann
  C_D(Re), d = 4/|kappa| in [dx, 10 mm]; applied through a one-sided smoothed surface delta (06bd5ed, NOT yet checked).
- step(..., wind=None): calls tension (cont) and air_drag (cont and wind given). make_advance (ride branch) passes
  wind=(-cs["vx"], -cs["vzb"]) when S.cont.
- g2p: when cont, _g2p_cont NEW: no free flight; particles above the grid top move by the body force alone; contact with glass wall,
  foot and body puts a particle back on the side it came from (inside: up to the floor, then in to R(z) - dx/10; from outside: out to
  Rout + dx/10; from above: onto the rim), normal velocity into the solid removed; leaving the grid sideways or below = fallen off the
  cart (act False, landed True).
- observe: when cont, the stored "drops" are every particle outside the cavity plus the loose ones; nfly counts those outside.

## 2. Tests (Kaggle CPU only; scripts tools/spill/*.py)
| notebook (version) | commit | dx | result |
|---|---|---|---|
| continuous-spill-cpu v1 (smoke_cpu.py) | 214fd3d | 4 mm | rest FAIL (collapse: surface 23-28 mm), shove spills, books close |
| continuous-spill-cpu v2 (rest_diag.py) | 7f139ca | 4 mm | old geometry holds 124.6-124.9 mm; continuous collapses (mean z 72.7 -> 6.8 mm), tension not the cause |
| continuous-spill-smoke v1 | f885e96 | 4 mm | rest: 0 lost, 48 outside, surface 122.2-124.9; shove pass |
| continuous-spill-smoke v2 | c8fb967 | 4 mm | 48 outside = puddle on the body (floor-corner leak); shove pass |
| continuous-spill-smoke v3 | f315e4a | 4 mm | rest 0 outside 0 lost PASS; wall columns 1.4 mm low; shove: books 27624+23748=51372 |
| continuous-spill-smoke v4 | 6a41be3 | 4 mm | same (wall columns low at 4 mm) |
| continuous-spill-smoke-b v1 | 86bbb88 | 4 mm | rest 0/0 PASS; film check crashed (index bug, fixed 317057d) |
| continuous-spill-smoke-2mm v1 | c8fb967 | 2 mm | superseded, result not read |
| continuous-spill-smoke-2mm-b v1 | 6a41be3 | 2 mm | ALL PASS: rest 420216/420216, 0 outside, median 125.01 (124.86-125.09; old 124.85-125.08); shove books 214112+206104=420216, vmax 3.09 m/s |
| continuous-spill-smoke-2mm-c v1 | cc51c2c | 2 mm | launched 21:30, PENDING (face rule: cut cells keep fractions) |
| continuous-spill-drag v1 (drag_check.py) | 036b81d | 2 mm | FAIL: 8 mm drop, U 1.5 m/s: 0.0805 vs law 0.1197 m/s^2; still air PASS |

## 3. Open items
- Drag: fix 06bd5ed (one-sided smoothed delta, exact surface area) written, not run: run drag_check.py at 06bd5ed (gate 25 %).
- 2mm-c result: read continuous-spill-smoke-2mm-c output (smoke.log); gates: 0 outside, 0 lost, median within 0.5 mm of 125 mm,
  shove books exact, film check 0.
- Head stage 2: the head is still a sheet on cavity columns; its spill still makes ballistic lumps (head_spill) = still a
  discontinuity. Not designed.
- Splash: Riboux & Gordillo PRL 113, 024507 (2014) criterion in notes/spill/STATE.md (beta >= 0.14); wet deck Cossali 1997 (to read);
  not coded. Wetting angle, surface tension at 6 C, dissolved gas: no measured values found (STATE.md).

## 4. Launching a continuous ride on Kaggle GPU (NOT wired yet; changes needed)
- Fig. 12 (tools/fig12/kaggle/run_b.py, notebook numakoudsie/guinness-on-a-cart-stout-in-jax): line ~128
  `G = Geometry(R, DZP, FILL, dx)` -> `G = Geometry(R, DZP, FILL, dx, body=(BODY_HALF[0], BODY_HALF[1], BODY_TOP))` behind a task
  flag (e.g. task["cont"]); Stout(..., K_frac=1.0) (more particles near surfaces). Wind is passed by make_advance automatically.
- Fig. 16 (tools/fig16/kaggle/run16.py, notebook numakoudsie/fig-16-guinness-cart-with-control): its own advance; the same Geometry
  change with the deck: body = (0.155, 0.062, z_top) with z_top = the deck top below the glass's inner floor (FLOOR_ABOVE_DECK 30 mm:
  -0.030; check cart16 model), and pass wind=(-v_x, -v_z) of the deck to S.step; the rotating frame's forces apply to particles
  outside the glass too (frame_accel already per position).
- Grid at 1.5 mm: 151 x 151 x 132 = 3.0 M cells vs 0.37 M; estimate 4-8x the old T4 time (old: Fig. 12 ~45 s/simulated s; Fig. 16
  run 5 ~153 s/simulated s): Fig. 16 off rides (20 s) 204-408 T4-min, kerb_full 41-82, Fig. 12 sharp30 x 4 48-96; total 300-600.
  First a 0.5 s calibration (~5-10 T4-min). The owner decided: NO recompute (18 Nov 22:11).
- Outputs: the same npz/summary as today; H now on the 151 x 151 columns (only cavity columns finite); drops = all particles outside
  the cavity (up to M_drops; set M_drops >= 100000 for the off rides: 2 mm shove had 63405 outside).
- Packing: pack_ride.py / pack16.py should crop H to the cavity window (keeps the page format) and store the outside liquid as a new
  field (positions per frame, deflated Int16 like drops), plus "fallen off" mass per frame from nlanded x mp.

## 5. Data layout the pages would get
Per frame as today (H, hf on the cavity's columns; drops/lumps), plus: outside liquid positions (x, y, z in mm/10, Int16, per frame
offsets like nd), spilled-off mass per frame (g), on-deck mass per frame (g). Lumps of head unchanged until head stage 2.

## 6. Branch claude/guinness-realism (never merged; merges cleanly into main 75343c8)
- tools/realism/kaggle_shots.py (page screenshots on Kaggle CPU), render_pint.py + kaggle_render.py (Blender Cycles frame, the only GPU
  use: 6.5 T4-min, notebook guinness-realism-render v1), notes/realism/STATE.md (photos, run register).
- public/scripts/pint3d-view.js physically based (glass n 1.52 transmissive, stout Beer-Lambert from deLange's spectrum at SRM 40, foam,
  warm room, bar top), new public/scripts/cart3d.js (Fig. 16 cart and road in 3D), one hook in guinness16-play.js (setCart/setPose),
  and the deck_px_* lines in cart16-view.js for the data panel. The owner rejected the 3D look (18 Nov).

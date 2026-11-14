# Fig. 16 · A Pint of Guinness on a Cart Built to Carry It

Page: `public/simulations/guinness-cart-control.html` (English only, `ENGLISH_ONLY` in `tools/i18n/build.py`), served at
<https://phyeinusul.com/simulations/guinness-cart-control>. Added 14 November 2026. Fig. 12 (`guinness-kaggle.html`) is the "before"
and is not changed, apart from the "16" link in the figure navigation that every simulation page carries.

## What the page does

It plays, on one clock, Fig. 12's best stored ride on a road (left) and the new four-wheel cart's stored ride on the same road
(right). Nothing physical is computed in the browser. Each stored picture (30 a second, none interpolated) holds the stout's surface on
the solver's columns, the head's thickness, the drops and lumps in the air, the cart's pose and its control signals. Every file is
checked against the SHA-256 in its index before it is drawn (`crypto.subtle`, which needs https; elsewhere the page says it could not
check). The one value read in the browser from stored data is Fig. 12's tilt per picture (Fig. 12's files store only its largest
tilt): twice the cos θ part of the stored surface on the outer ring, exactly as `tools/fig12/kaggle/pack_ride.py` reads it.

- `public/scripts/guinness16-play.js`: the player. Reads `public/data/fig16/2026-11-14/index-16.json` and Fig. 12's
  `public/data/fig12/2026-11-14-run10/index-jax.json`; Fig. 12's best ride per road is fixed in `BEST12` (least head spilled, then least
  tilt: the kerb with the slosh LQR, the gentle roads with joint control); the comparison table is filled from the two indexes. Words are
  rewritten four times a second; nothing reacts to the pointer crossing the figure.
- `public/scripts/cart16-view.js`: `Cart16View`, which extends Fig. 12's `StoutView2` (not edited). The camera, the projection and
  `drawGlass` (the Guinness tulip, harp and lettering, stout and head from the stored fields) are Fig. 12's; the machine under the glass is
  new: deck, four wheels on swing arms hinged under the deck, coil springs over dampers, voice-coil actuators (wine) and load cells (gold)
  at the struts' tops, rear hub motors, the IMU, controller, battery and the road scanner on its boom. The deck's tilt reaches the glass
  by wrapping `project` while `drawGlass` runs. The pose comes from the stored axle heights, deck height and pitch, each measured from its
  first stored value.
- The lecture note (first version) is built into the page by `tools/fig16/build_page.py` from `notes/fig16/page/guinness-cart-control.src.html`:
  every number in it is filled from the stored data (the two indexes, the stored rides and the run's summary
  `notes/fig16/run16-v2-summary.json`); `--check` fails if the page differs from what its source and data give.

## The machine and its control system (`tools/fig16/kaggle/cart4.py`)

Planar, as Fig. 12 (both wheels of an axle meet the same road). A rigid deck (2.4 kg with glass, battery, controller and scanner, plus
the pint as a rigid load) heaves and pitches on two axles 0.22 m apart; per axle a spring of 700 N/m over a damper of 19 N s/m, a
voice-coil actuator of ±50 N (two struts), bump stops at ±30 mm, tyres of 16 kN/m. Two rear hub motors, 3 N/A each at the road, 8 A,
24 V, 0.6 Ω. The stout feels the uniform effective gravity of the point S where its first mode lives, 122 mm above the deck's centre,
turned into the glass's frame (note eq. 1); its push acts back on the deck at the same point. Left out: the rotating frame's forces that
vary across the glass.

Control, every 1 ms: LQR on the linear model of cart, deck, axles and the first sloshing mode (run 8's measured swing with the head:
2.915 Hz, ζ 0.425, β 1.241), with the optimal feed-forward of the road the scanner reads 0.25 s ahead (Tomizuka's preview, note eq. 4);
the swing estimated by a Kalman filter from the IMU's acceleration and Fig. 12's two wall probes. The weighting is chosen in the
notebook among five, on the kerb, with the few-mode stout of `tools/fig16/slosh_model.py`; run 2 chose q = 0.25 mm.

## How the data was made

1. **The design model, on the CPU.** `tools/fig16/rides.py` decodes Fig. 12's stored rides; `slosh_model.py` (three cos θ modes, the
   head's friction with a fitted power 0.667 of the speed, Cantat's 2/3) was fitted on run 8's speed-held rides only (`fit.py`,
   `fit.json`) and validated on run 10's five controlled rides (`validate.py`, `validation.json`, `notes/fig16/model.md`).
2. **On Kaggle** (the owner's rule: everything computed in the owner's notebooks). GPU notebook `numakoudsie/fig-16-guinness-cart-with-control`:
   version 1, the smoke test (6 mm grid, two pictures per task); version 2, the rides (1.5 mm grid, Tesla T4, 19 min): the rest guard,
   the design step, the kerb with control on and off, the five bumps and the 25 mm bump with control on. Code: `run16.py`, `cart4.py`,
   `modal4.py`, the notebook cell `nb_cell.py` (fetches the files at a pinned commit, here 2041127). CPU notebook
   `numakoudsie/fig-16-cart-diagnostics-cpu` (`diag16.py`): the diagnostics that showed the passive cart violent but stable.
3. **Packing** (`tools/fig16/kaggle/pack16.py`, format conversion only): Fig. 12's file format plus the cart's signals, into
   `public/data/fig16/2026-11-14/` with `index-16.json` (SHA-256, measured numbers, the design and the notebook's version).

## Stored results (index-16.json)

Kerb, 1.5 m/s: control on, tilt 2.64 mm, head spilled 0.004 mL, stout 0; control off, stopped at 0.77 s when its list of flying drops was
full, with 8.35 mL of head and 9.79 g of stout already spilled. Five bumps, 1.0 m/s: 0.65 mm, nothing spilled. One 25 mm bump, 1.0 m/s:
0.50 mm, nothing spilled. Books closed in every ride (0 particles; head within 1e-8 mL). Fig. 12's best on the same roads: 20.81 mm and
1.63 mL; 1.00 mm; 1.03 mm.

## Open

The full lecture note to the standard of `notes/STANDARD.md` (readers, derivation checker); the data panel with the three-way proof;
run-to-run scatter on the kerb; the rotating frame's non-uniform forces; the figure's Kaggle dataset `numakoudsie/fig16-...` (the layout
rule of `docs/kaggle-pipeline.md`).

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
  The wheels (14 November 2026): angle −x/R_w from the player's position between stored pictures (`pose.wheelAng`, kinematics), spokes
  smeared over the angle the wheel really turned since it was last drawn (`WheelBlur` in `stout-view.js`, 18 November 2026: right at any
  frame rate; before, a fixed 1/60 s let slow frames strobe the five spokes backwards), one gold valve mark with a streak behind it.
- The lecture note is built into the page by `tools/fig16/build_page.py` from `notes/fig16/page/guinness-cart-control.src.html`
  (the note sits between [`<article class="paper" id="paper">`](../../notes/fig16/page/guinness-cart-control.src.html#L89) and
  [`</article>`](../../notes/fig16/page/guinness-cart-control.src.html#L389)): every number in it is a `{{key}}` filled from stored data;
  `--check` fails if the page differs from what its source and data give. See "The lecture note" below.

## The machine and its control system (`tools/fig16/kaggle/cart4.py`)

Planar, as Fig. 12 (both wheels of an axle meet the same road). A rigid deck (2.4 kg with glass, battery, controller and scanner, plus
the pint as a rigid load) heaves and pitches on two axles 0.22 m apart; per axle a spring of 700 N/m over a damper of 19 N s/m, a
voice-coil actuator of ±50 N (two struts), bump stops at ±30 mm, tyres of 16 kN/m. Two rear hub motors, 3 N/A each at the road, 8 A,
24 V, 0.6 Ω. The stout feels the uniform effective gravity of the point S where its first mode lives, 122 mm above the deck's centre,
turned into the glass's frame (note eq. 4); its push acts back on the deck at the same point. Since run 3 the rotating frame's forces that
vary across the glass are in the fluid too (note eq. 8).

Control, every 1 ms: LQR on the linear model of cart, deck, axles and the first sloshing mode (run 8's measured swing with the head:
2.915 Hz, ζ 0.425, β 1.241), with the optimal feed-forward of the road the scanner reads 0.25 s ahead (note eq. 17);
the swing estimated by a Kalman filter from the IMU's acceleration and two wall probes. In the controlled kerb rides (run 6,
GPU notebook version 9) each probe is an area sensor, `Stout.probes_patch` in `tools/fig12/kaggle/stout_jax.py`: the median of
3 × 3 columns at the wall divided by the first mode's shape there (0.971); `run16.py` selects it with `PROBE=patch`. Fig. 12's
`probes()` is unchanged. The weighting is chosen in the
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

## The lecture note (rewritten 15 November 2026)

A chapter in the manner of a second-year textbook (`notes/STANDARD.md`, verdict of 21 October 2026), nine sections: 1 the kerb and the
hand; 2 the machine (Table 1 of every parameter, Example 2.1 the bounce); 3 what the stout feels on a tilting deck (effective gravity,
the acceleration of S on a pitching deck, eq. 3, the waiter's tilt, eq. 5, the linear sideways acceleration, eq. 6, the driven swing,
eq. 7, ★ the forces of a turning glass, eq. 8); 4 the cart's equations of motion (eqs. 9 to 11), its natural modes with the control off
(Table 2, from `modes16.json` and recomputed) and the wheelbase filter (eq. 13); 5 the control system (Bryson's rule, ★ LQR from
dynamic programming, eqs. 15 and 16, ★ preview, eq. 17, the Kalman filter, eq. 18, the hardware's limits, the design step, Table 3);
6 how the rides were computed (the solver, the cart's sub-steps, the three notebook versions, the volume correction, errors to
expect); 7 the results (Tables 4 and 5, sampling of peaks); 8 what is on the screen; 9 limits, Problems, further reading (only
sources opened: Tong, Åström and Murray, Boyd, Liu, Lessard and Seiler, Welch and Bishop, Kugelstadt et al., Fig. 12's note).

**Where its numbers come from.** `notes/fig16/note_numbers.py` measures every derived number from the code and the stored data and
writes `notes/fig16/note-numbers.json`; [`build_page.py`](../../tools/fig16/build_page.py#L53) only formats them
([the keys](../../tools/fig16/build_page.py#L77), [Table 3's rows](../../tools/fig16/build_page.py#L68) from the index's design step).
It uses [`statics`](../../tools/fig16/kaggle/cart4.py#L82), [`linear_model`](../../tools/fig16/kaggle/cart4.py#L97) and
[`design`](../../tools/fig16/kaggle/cart4.py#L133) of `cart4.py` (masses, modes, LQR gain, closed-loop poles, preview gains, Kalman
gain), the glass profile, Fig. 12's cart constants, and the stored rides (accelerations by central differences of the stored speed,
pitch rates, tilts every picture and every second picture, seed scatter, strokes, airborne pictures, the swelling check from the
stored surfaces). It also runs four checks printed in the note: eq. 4 and the rotating-frame formula of
[`Stout.frame_accel`](../../tools/fig12/kaggle/stout_jax.py#L273) on random states (agree to 10⁻¹⁵), eq. 6 against eq. 4, and the
preview law (17) against a direct solution of the optimality equations (agree to 10⁻¹⁵).

**Found while measuring, and fixed.**
- The centripetal term of the acceleration of S had the wrong sign in [`Cart4.forces`](../../tools/fig16/kaggle/cart4.py#L220)
  (fixed in commit 7bb19a7). The error, 2 h_g θ'² along the glass's axis, left the sideways push g_x exact. Runs 5 and 6 use the
  fixed code; the two gentle roads with control (run 2, version 2) predate it.
- In the linear model the stout feels the deck but does not push back on it, so Table 2's "pitch mode with the stout" is the deck's own
  pitch mode (4.08 Hz natural, 3.85 Hz ringing) whose eigenvector carries the driven swing; `modes16.json` lists ringing
  frequencies (|Im λ|/2π), not natural ones.
- The drive force is capped by the rear tyres' grip (μ N_r = 19 N at rest), below the motors' 48 N.
- Seed 1 of the controlled kerb (runs 3 and 5) showed a late actuator burst (up to 28-32 N after 3.3 s). Cause: single grid columns
  next to the wall spiking for one picture, magnified 2.67 times by the two-point probe's extrapolation (audit M3,
  `tools/fig16/kaggle/diag_burst.py`). With area probes (run 6) the actuators stay below 0.4 N after 3.3 s.

## Data panel (18 November 2026)

The page loads `scripts/dataset.js` after `sim.js` and `styles/data.css`; `guinness16-play.js` declares one store
(`Sim.dataset`, about 60 names) and appends `scripts/datalog.js` once the first ride is in it. The figure's two panes carry
`id="stage"`, so the panel's Read values switch (off by default) sits in the caption.
- What is stored, where it is set: the reader's choice and both files (road, control on or off, file names, SHA-256 as fetched,
  notebook version, pictures a second, frames, the head's volume at the start), copied in `fillRide()` when a ride is chosen; the right
  ride's arrays as stored (time, tilt, pitch, motor current, the two axles' actuator forces, speed, head in the glass, head and stout
  spilled) and Fig. 12's spilled head and stout; every frame in `tick()`, the values at the picture on screen, Fig. 12's tilt read from
  its stored surface (`tilt12`) and the residual of the head's book; `k_text16`/`k_text12`, the pictures whose numbers the readings show.
- Checks (`Sim.data.check`): each "now" value against the stored array at k; k against min(N − 1, round(t f)); the pitch against
  (θ_k − θ_0) 180/π; the playback length; Fig. 12's tilt written out again from the stored surface; the fingerprint against the index.
- Read back (`Sim.data.drawn`): the words of the readings under each figure must equal the stored value at k_text, formatted as the
  page formats it. Pixels of the deck: `Cart16View` records the deck top's front and rear edge in `deckStore` (not `ds`: with `ds`, the
  drawing it inherits from Fig. 12 would write names this store does not declare); until the drawing records them the check says "not
  recorded". The pixel test checks alpha first.
- Book: head in the glass + head spilled = the head at the start (`head_res`, stored by the page, added again by the panel).
- Read values pins a pane (the new cart, its pint, Fig. 12's cart or pint) and shows its stored values in the strip under the figure.
- Where the picture and the store differ is said in the panel's `about`: readings trail by up to 0.25 s; wheels turn by interpolated
  position (kinematics); the switch cross-fades over 0.45 s; Fig. 12's tilt per picture is read on the page; the 3D close-ups record no
  points of their own.
- Proof: `tools/fig16/kaggle/panel16_check.py`, run on Kaggle's CPU (headless Chromium, 1440 and 390 px, three rides).

## Kaggle dataset (18 November 2026)

`numakoudsie/fig16-guinness-cart-control` (private) holds every output file of the GPU notebook versions the page plays (2, 8, 9),
byte for byte, with a manifest; see `docs/kaggle-pipeline.md` and `notes/inventory/datasets/fig16-guinness-cart-control/`.

**Control switch and run 3 (15 November 2026).** The page offers three roads and one switch, "Control system on/off". The switch keeps
the ride time and cross-fades the last picture out over 0.45 s. `guinness16-play.js` reads both indexes,
`public/data/fig16/2026-11-14/` (run 2) and `2026-11-15/` (runs 3, 3b, 4: the turning deck's forces on the stout, 60 pictures a
second, control off on every road). Per road and setting it plays run 3's ride where one exists, else run 2's, seed 1. Page files
keep at most 2,048 drops per picture (an even subsample; the true count is `nd_true`). See `notes/guinness-rebuild/audit.md`.

**3D close-up (15 November 2026).** `public/scripts/pint3d-view.js` (an ES module on three.js 0.170, vendored) draws the same stored
picture of the pint in 3D under the cart's picture, with the camera riding with the glass:
- the stout's surface from the stored column heights, sampled on 24 rings and 96 angles as `StoutView2` samples them
  (`StoutRide.atInward`), with the outer ring meeting the glass at the surface's own height;
- the stout's side against the glass;
- the head as a second surface at the stored height plus the stored thickness, and its band against the glass;
- drops of stout (spheres of radius 0.8 mm, at most 4,096) and lumps of head (spheres of their stored volume).

It computes nothing physical. The lighting, the gloss and the glass's tint are drawing only.


**One geometry (15 November 2026).**
- The drawn cart takes its wheelbase, wheel radius and hinge depth from the ride's stored cart parameters
  (`Cart16View.fromCart`, from `cart4.py` CART4).
- The player hands the view the stored axle heights, the deck's centre-of-mass height and the pitch as stored. The earlier
  hand-set offset of +0.098 m and the subtraction of the first frame are gone.
- The glass's inner floor stands 30 mm above the deck's centre of mass in the drawing (seat 16 mm, foot 14 mm), as in the
  simulation (`FLOOR_ABOVE_DECK`).
- The deck's size, the track width and the parts' shapes are drawing only, because the simulated cart is planar.

**Check of the 3D close-up (15 November 2026).** `node tools/fig16/check_pint3d.cjs` runs in Chromium and checks three ways:
- the stored stout height and head thickness at the wall facing the camera, read with `StoutRide.atInward`, the same function the
  2D view uses;
- that point projected through the close-up's own camera;
- the pixel read back: drawn (alpha > 0) and dark just below the surface, drawn and light inside the head band.

Result on 15 November: 65 of 65 columns pass, in 5 pictures of 5 rides, including the uncontrolled kerb at 0.70 s (stored
height 130 mm at the front wall) and the uncontrolled 25 mm bump at 1.2 s (163 mm, stout over the rim).

## Frame times of the 3D close-up (18 November 2026)

`tools/fig16/kaggle/frames_check.py` ran on a Kaggle T4 machine (CPU notebook `fig-16-cart-diagnostics-cpu`, version 16, 3.3 GPU-minutes;
report `notes/guinness-rebuild/frames/frames16-report-v16.json`). Headless Chromium did not reach the T4 by any of the three routes tried
(ANGLE on Vulkan, ANGLE on EGL, the default): WebGL named SwiftShader or Mesa llvmpipe, both software. Whole-page frame intervals there
(250-1000 ms) measure a CPU standing in for a graphics card, not the page on a real device, and are not a result. What does carry over
is the close-up's own timer (`Pint3D.stats`): 5-7 ms of JavaScript and 1-2 ms of render call per stored picture, so the 3D close-up is a
small part of a frame; the 2D drawing of the carts and glasses takes the rest. A real frame rate needs a browser with a graphics card.

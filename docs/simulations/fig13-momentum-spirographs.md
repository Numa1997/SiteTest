# Fig. 13 · Spirographs in Momentum Space, the Flower Hunt, the dashboard and the films

Published 8 November 2026 at Numa's word. English only (`ENGLISH_ONLY` in `tools/i18n/build.py`). In the catalog
(`public/scripts/catalog.js`, entry `momentum-spirographs`, fig 13; its German and Arabic catalog strings are not translated, as Fig. 12's)
and in the Fig. links of every simulation page since 10 November 2026 (the two project pages, double-inverted-pendulum and rods-in-liquid,
carry no Fig. list).

## The physics, in one place

A compound double pendulum: two equal uniform rods (1 kg, 1 m, g = 9.8 m/s²), angles θ₁, θ₂ from straight down, conjugate
momenta p₁, p₂. Hamilton's equations for the general family (masses, lengths, rods or point masses) are in the head comment of
`public/simulations/momentum-spirographs.html` and in `tools/fig13/chaos_map.py` (`coefficients`, `deriv`).

- **Momentum space** is only where a pendulum is placed: each one hangs still and is kicked with the (p₁, p₂) of its place.
  What it draws is the real path of its lower rod's tip, as a long exposure.
- **The tip as a complex number.** With z = x + i h, x = l(sin θ₁ + sin θ₂), h = −l(cos θ₁ + cos θ₂), so
  z = −i l (e^{iθ₁} + e^{iθ₂}): the two rods are two rotating arrows. The plane of z is the wall the pendulum swings in.
- **The butterfly** is the periodic orbit kicked with p = (3.557312977, 12.211005484) kg·m²/s: its state returns after
  T = 2.659405 s to about 1e-11 (Newton's method, DOP853, `tools/fig13/butterfly.py`), θ₂ having gained exactly 24 turns.
  Trace of its return map 2.000385: weakly unstable, an error grows by about 2 % per lap. Energy 390.78 J, far above the
  ±19.6 J range of the potential, so the motion is close to the integrable g = 0 rotor.
- **Turning the paper.** Each instant is the point (x, h, τ), τ = k·(age). Turned by φ about the vertical axis through τ_c:
  screen x = τ_c + (τ − τ_c) cos φ + x sin φ, screen y = h. φ = 0 is the wave h(t); φ = 90° is the path (x, h).

## Pages (public/)

| File | What it is |
|---|---|
| `simulations/momentum-spirographs.html` | Fig. 13, the one page that holds everything (11 November 2026): the live grid over the chaos map with its controls and the pinned pendulum; a guide of six jumps at the top; the stations of section `#inside`, each opening in place in a frame (`#butterfly` the dashboard, `#hunt` the flower hunt, `#catch` the live catch, `#films` the eight films, each started by its own button); and one lecture note of four parts, 35 sections and 33 equations, written into the page by `tools/fig13/build_page.py`. |
| `simulations/flower-hunt.html` | The flower hunt: a garden of closed flowers and butterflies, a bench to test any kick, study notes. |
| `simulations/butterfly-dashboard.html` | The dashboard: complex plane, h(t) to the right joined by a horizontal line, x(t) below joined by a vertical line, both wave panels turned by φ (by itself or by hand). A wheel and the butterfly. Wide and tall (phone) layouts are chosen by the width of the figure. Test hook `window.__dash`. |
| `simulations/fig13/bell.html` | Film: the bell above the floor (3-D), r = 2l cos(Δ/2). |
| `simulations/fig13/turning.html?scene=wheel\|butterfly` | Film: turning the paper, with the deck of earlier pictures. |
| `simulations/fig13/together.html` | Film: six pictures on one clock; the phone layout on a portrait screen. |
| `simulations/fig13/dive.html` | Film, phone first: from momentum space into one cell, then the exposure grows from an eye's 0.1 s to one lap. |
| `simulations/fig13/reem.html` | The film player, written by `film_page.py`: the eight live parts in order (the gift For رِيمْ, the construction, the catch, the dive, six pictures, turning the paper twice, the bell). `?part=k` starts at part k; `?embed=1` (inside the Fig. 13 page) hides the back link and tells the page each part's shape. The gift film itself (`tools/fig13/gift/reem.html`) writes رِيمْ and فَرَاشَتُكِ (each traced from a plate Numa chose) with 640 arrows each, then the butterfly by two arrows, then its dashboard with the paper turning, then the exact strike and why it is not chaos. Labels and captions in Instrument Sans. No recorded video is on the site. |
| `simulations/fig13/construction.html` | The player with the construction film alone (`tools/fig13/gift/construction.html`): h(t) beside the plane, x(t) below, the two time axes joined by a 45-degree mitre; for each instant a level and an upright line cross at the tip of the pendulum; a wheel first, then the butterfly. |
| `simulations/fig13/catch.html` | The player with the catch film alone (`tools/fig13/gift/catch.html`, drawn live from `pendulum.js`): struck with p = (2, 4) (18 J), the pendulum swings in chaos for 8 s; a motor at the top pin (drawn as a direct-drive torque motor; torque constant 2.5 N·m/A, assumed) pumps and steers, waits, catches, holds four laps and lets go. When the catch happens is not a fixed number: 8 s of chaos amplify the last digit of the arithmetic (73 s in Chromium 153, 118 s in Node 22, 43 s in Python, measured 11 November 2026). |
| `simulations/butterfly-catch.html` | Catching the butterfly: the live catch (`fig13/live-catch.html` in a frame) with **Random chaos** (random angles and momenta) and **Choose a strike** (a tap on the Fig. 13 chaos map, p₁ ∈ [−12, 12], p₂ ∈ [−8, 16], strikes both rods from rest), each restarting the run computed live; then the lecture note on the theory and the method (13 sections, 15 numbered equations, the phase diagram, the checks). Body in `tools/fig13/catch_note_body.html`. English only. |
| `simulations/fig13/film.html` | The whole gift as one film, computed and drawn live in the browser, nothing recorded: the eight parts of `reem.html` (the same list), played in order; the page keeps the clock and asks each film for frame f. The motion comes from `pendulum.js`: the pendulum's Hamilton equations integrated by RK4 (the butterfly from its strike, matching `orbit24.json` to 4e-7 rad); for the catch, the orbit, its step maps and the motor's periodic-LQR gains are computed at start (about 0.1 s, gains equal to the Python ones to three decimals) and the controller of `butterfly_control.py` runs as the film plays (when it is caught depends on the device's arithmetic, see `catch.html` above); the catch film's clock follows the phases (chaos at half speed, the motor at a quarter, from a second after the catch at half). Play/pause, previous, next, from the start, Night/Paper, progress; loops. Written by `tools/fig13/gift/film_page.py`. The same film as one MP4 (about 60 MB) is too large for Cloudflare's 25 MiB per file; it is made from the three masters with ffmpeg and not committed. |

The four films are generated: edit `tools/fig13/gift/*.html` and run `python3 tools/fig13/gift/publish_films.py`, which rewrites the
asset paths, adds the two security meta tags and a link back to the dashboard. Opened without `?film=1` they loop live.

## Tools (tools/fig13/)

- `chaos_map.py` → `map_png.py` → `public/images/fig13/chaos-map-rods-P20.png` (1280 × 720 for p₁ ∈ ±35.6, p₂ ∈ ±20; row 0 is p₂ = +20).
- `hunt.py`, `hunt_inspect.py`, `hunt_export.py`, `butterfly.py`: the hunt for closed orbits; `hunt_export.py` writes `public/scripts/fig13-hunt-data.js`.
- `gift/orbit.py` → `gift/orbit24.json` (samples spaced T/(n−1), not exactly 1/3000 s; index by t/T·(n−1)).
- `gift/dive_data.py` → `gift/dive/dive.json` and `dive.bin` (not committed in tools/, about 47 s to regenerate; checks the butterfly cell against orbit24 to 3.6e-5 rad and every cell's energy to 1e-6).
- `gift/render.cjs THEME OUTDIR DSF [frames|all] [PAGE] [SCENE] [WxH]` renders a film to frames (local server on port 8766 in the repository root); ffmpeg makes the MP4. Videos are not committed.

## What makes the butterfly (checked on orbit24.json, 8 November 2026)

- At every petal the arm is straight (Δ = 2πn), and then tip = 2l·e^{iθ₁}: the petal points exactly along the upper rod.
- Over one lap the upper rod makes 0 net turns and swings between −156.7° and +156.7°, never over the top; the lower rod makes 24 turns
  (about 9 turns of the elbow per second). The butterfly is a slow pendulum (the upper rod, held by gravity) carrying a fast spinner
  (the lower rod); the wings are the turning points of the slow swing, where the petals pile up (±135.6° at the petals).
- Conditions: a hard kick mostly to the lower rod, so that the arm folds through (eq. 3 of the hunt note: 3p₁² − 114p₁p₂ + 75p₂² > 0)
  and the petals nearly do not creep without gravity (the one-petal resonance, δ/2π ≈ 0); gravity then holds the petal direction to a
  swing about straight down. If the upper rod went over the top, the petals would go all the way round: a flower, not a butterfly.
  It closes exactly when one swing takes a whole number N of petals (N = 24 at E = 390.8 J; the hunt found N = 12 to 32 on p₁ ≈ 3.556).

## The calligraphy of the gift (8-9 November 2026)

Tried and rejected by Numa, in order: a font drawn at random (Noto Nastaliq Urdu); my own reed-pen sketch (`qalam.py`); reed strokes over
Amiri composed as a mirror butterfly (`qalam2.py`); automatic re-inking of whole words (`qalam3.py`, worse than its model); ten more fonts.
Accepted: the reference plate Numa chose (a screenshot of an image made by Gemini), traced to vector outlines (`ref_trace.py`, `reem_ref.json`)
and set as gold on navy (`plate.py`). Its Arabic was checked by eye only: the third dot under the ya was wrong and removed; the vowel marks are
kept as drawn and have not been checked by a calligrapher.

**فَرَاشَتُكِ in the hand of رِيمْ (9 November 2026).** Measured on the traced name (stroke width against direction over 5282 skeleton samples): a flat
nib about 60 px wide held at 70 degrees (horizontal strokes 57-60 px, strokes at 60-75 degrees about 16 px); uprights about 40 px, as with the reed
turned to 45 degrees. `farashatuki.py` takes the plate's own ra, fathas, damma, kasra and the small hooked mark, and writes fa, alif, shin, ta, the
kaf and the dots with that nib, on the plate's habit of letters climbing from the upper right and the ra sweeping under what follows.

**فَرَاشَتُكِ, final (9 November 2026).** Numa rejected the composed versions (`farashatuki.py`: "just disconnected letters"; the three compositions
of `farashatuki_v2.py` were shown, not used) and chose the Diwani panel (03, top right) of a nine-style sheet of the word he sent, an image made by an
image generator. `farashatuki_trace.py` traces it like the name: gold ink brighter than the dark board, panel frame, labels and guide lines removed,
14 contours (letters, dots and the small Diwani marks), filled with the even-odd rule. As with the name, its vowel marks were not checked by a calligrapher.
Numa then sent the same panel full-screen (about 3.5 times sharper); the film uses that trace (`farashatuki_trace.py panel`, smoothed over the
phone zoom's JPEG blocks; the fa's head is solid there, as on the plate).

**Labels (9 November 2026).** At Numa's request ("old and scientific") the films' labels, readouts and captions are set in Instrument Sans
(SIL OFL; `tools/fig13/gift/fonts/`), with its tabular digits frozen into the font so that changing numbers do not jitter, and IBM Plex Sans
supplying Greek (φ, θ), which Instrument Sans lacks. This is the only place on the site with a font outside the house set; titles stay in
Instrument Serif. The player pages' buttons keep IBM Plex Mono.

## The butterfly physically (`tools/fig13/butterfly_physics.py`, 9 November 2026)

- The strike: both rods hanging still, the upper rod is set turning at −25.30 rad/s (4.0 turns a second, backwards), the lower at +74.59 rad/s
  (11.9 forwards); p = (3.557313, 12.211005) kg·m²/s, E = 390.78 J.
- Over a lap: the upper rod's speed swings between −32.7 and +33.1 rad/s, the lower rod never stops (44.7 to 74.6 rad/s, always forwards); the tip moves
  at 38 to 52 m/s; the top pin pulls with 905 N on average and up to 4.31 kN (220 times the pendulum's weight, 19.6 N; from the centre of mass's
  acceleration, sampled at 20 001 points).
- Stability from the exact variational equations (SymPy Jacobian, DOP853, rtol 1e-12; det of the lap map 1 to 2e-12): multipliers 1.01977 and 0.98062
  (plus the pair at 1 every periodic orbit has): unstable, an error grows ×1.0198 a lap. The finite-difference trace of `butterfly.py` (2.0004) could not
  tell this ('neutral'); this settles it.
- Twins struck 1e-6 apart in p₂: the butterfly pair stays within 0.32 mm (tip) after 40 laps (106 s); at 18 J (p = (2, 4)) a pair disagrees by 1 cm after
  6 s, at 65 J (p = (3, 6)) after 37 s.
- 1 500 laps (66 min) of butterflies struck 0, 1e-6 and 1e-3 off in p₂: the wing angle (largest petal direction) stays between 135.56° and 135.9°, the upper
  rod never goes over the top. The exact closed drawing is unstable; the butterfly shape is robust.
- Why it is not chaos, in one line: the motion carries 20 times the energy gravity can give or take (390.8 J against ±19.6 J), so gravity only steers.

## Catching the butterfly with a motor (`tools/fig13/butterfly_control.py`, 9 November 2026)

Method of the skill `phyein-usul-first-principles-control` (§8), applied to a periodic orbit instead of a resting point: a motor torque τ at the top pin
enters as a generalised force on θ₁ (dp₁/dt gains τ); the orbit is sampled at 2 400 points a lap and linearised step by step (variational equations);
controllability over one lap: all four Gramian eigenvalues positive (3.5e-8 to 4.0e-5, the smallest along the timing of the lap); periodic LQR
(Q = diag(1, 1, 0.05, 0.05), R = 1e-3 per (N·m)², |τ| ≤ 60 N·m): the closed-loop lap multipliers fall to 0.07 to 0.08. Verified on the nonlinear equations
(RK4 at the same step, torque held over a step), with the reference re-indexed to the nearest orbit point each step:
- nudged 0.1 rad off: back on the orbit within about 5 s, at most 8.3 N·m, then the torque falls to zero (holding the orbit costs nothing);
- pump, wait, catch: the motor pumps the energy to 390.8 J (τ = sat(0.02 (E* − E) θ̇₁)), switches off, and waits until the free motion passes within
  0.12 of the orbit, then catches. From p = (2, 4) (18 J, chaotic): pump 1.9 s, caught at 6.4 s, at most 2.2 N·m in the catch, then within 6e-4 of the orbit
  with zero holding torque. From p = (3, 6) (65 J): caught at 5.7 s. Not caught within 300 s from p = (5, −3), (−2, 5), (1, 8), (0, 0.5), (−4, 3): after the
  pump these sit on regular motions at the right energy that never come near the butterfly.
- Did not work: time-locked tracking (fights the lap's timing, the costliest direction); a transverse-only cost with saturated torque (drained the energy);
  steering a smoothed θ₁ (breaks when the upper rod goes over the top), the width or the average of P (the loops fight), braking going-round alone.

**Catch from anywhere (`catch_anywhere`, compiled with numba; settings `SETTINGS`).** P = p₁ + p₂ is the slow pendulum's momentum (dP/dt = τ − gravity's
torque), so one motor reaches both the energy and the swing:
1. pump and steer: τ = (kE (E* − E) + memory) θ̇₁ + (kA (P* − P_reach) + memory) P, where P_reach is the largest |P| over the last 3 s and P* = 15.77 its value
   on the butterfly (integral memories against steady errors, as in Fig. 9);
2. wait with the motor off until the free motion passes within 0.3 of the butterfly or of its mirror image (the same drawing flipped, held by the same gains
   with the torque reversed);
3. catch and hold with the periodic LQR;
4. a miss (steering not settled in 12 s, nothing near in 12 s, or a catch that slips past 1) drains the pendulum back to 60 J, into chaos, and tries again:
   each try is a fresh draw.
Integration: RK4 at four sub-steps per control step (2 400 steps a lap; at one sub-step the free orbit drifts about 1e-2 a lap and the motor
locked onto that drift: an earlier count of "30 of 30", made at one sub-step, was wrong and was withdrawn the same day); free motion by DOP853.
Result, |τ| ≤ 60 N·m, catch within 0.2: of 30 random strikes p ∈ [−8, 8]² kg·m²/s, 28 caught and held within 900 s (22 within 300 s; mean 163 s, slowest
794 s); 2 not caught in 900 s. Close in, the catch converges from 0.05 to 0.2 away to the exact orbit (error below 1e-4, energy 390.78 J).
Let go: released within 0.0003 of the orbit, the free pendulum stays within 0.1 of it for 275 laps (731 s), then wanders but stays within 0.13 for 1 500
laps (66 min), its wings 135.55° to 135.83° throughout, never over the top (DOP853).

**Interactive catch and new settings (9 November 2026, evening).** `pendulum.js` `Run` takes any start state. Settings `SET`: catch at
distance 0.6 (the catch's basin, measured: from 0.3 16/16, 0.4 13/16, 0.6 12/16, 0.8 9/16), settled at |E − E*| < 5 J and
|P_reach − 15.77| < 3, let go only after four laps and within 0.005. On 100 random starts (Node, the browser code): all caught and held,
median 16 s after the motor switches on, 82 within 60 s, 90 % within 87 s, slowest 188 s; released within 3e-4, at most 0.0034 four
laps later. The earlier settings (catch 0.2, settled at 1 J and 1) caught 29 of 40 within 400 s. A one-lap Gauss-Newton torque plan
(a "bridge", 12 segments) was tried and dropped: from 0.2 to 1.0 away it landed within 0.05 in 1 or 2 of 12 cases. `butterfly_control.py`
`SETTINGS` follow (its release is not distance-gated). The film's clock: a search after a miss runs at 4×, waiting at full speed.

**10 November 2026.** The gift player (`reem.html`, `film.html`) plays eight live parts: the gift, the construction, the catch, then the
dive, six pictures (phone layout), turning the paper (wheel, butterfly) and the bell; each part has its own stage size (portrait
1080 × 1920 or wide 1920 × 1080). Captions and subtitles of the gift, construction and catch films sit in fixed boxes and shrink their
type to fit (`fitBox`), so a browser's translation, longer than the English, never spills over the drawing.

**11 November 2026: the Fig. 13 page itself.** Until now `momentum-spirographs.html` was the bare figure: no axes, no legend for the
glow, no lecture note (the catalog's "Read the lecture note" led nowhere). Added:
- axes: the p₂ of each row along the left edge, the p₁ of each column along the bottom (`drawAxes`);
- **Explain the eye** (`drawAnatomy`): the ellipses K = 2U₂ (pupil) and K = 2(U₁ + U₂) from the strike's kinetic energy
  K = (B p₁² − 2C p₁p₂ + A p₂²)/(2(AB − C²)), and the two fold-through lines from K = (p₁ + p₂)²/(2(A + B − 2C)), all for the sliders' values;
- **Pinned pendulum**: a tap on a cell pins it (`setPin`): enlarged live view with the last 3 s of path, its strike, K, the map's value at
  the strike (`mapValue`, read from the PNG's alpha, v = (α/255)^(1/0.8)) and a sentence saying which part of the eye it is in;
- a square plate on screens up to 640 px wide (same sheet, drawings 1.8 times larger); S = 0.4·min(cell width, height)/(l₁ + l₂);
- the lecture note (11 sections, 9 numbered equations; source kept in `tools/fig13/fig13_note.html`): why a hundred pendulums share one
  sheet (position = strike, drawing = tip path), what a strike is (hammer impulses), what the glow measures, the eye, the two streaks.
Measured for the note on `chaos-map-rods-P20.png` (1280 × 720, chaotic = v > 0.5, 5.52 % of the sheet): K < 9.8 J 0.0 % chaotic;
9.8 to 29.4 J 42.4 %; 29.4 to 39.2 J 63.8 %; 39.2 to 78.4 J 32.2 %; 78.4 to 196 J 8.6 %; above 196 J 2.3 %, of which within 0.02 rad of a
fold line 65.9 %, 0.02 to 0.05 rad 13.6 %, 0.05 to 0.10 rad 2.2 %, beyond 0.10 rad 0.0 %. Of the 100 default cells: 2 in the pupil,
60 fold through, 38 do not; 6 chaotic by the map (corrected 11 November 2026, see the end of this page). Energy drift of the page over 10 s (RK4, h = 1/4500 s): median 2e-5 J, worst 0.14 J of
3450 J at (−32, 18). Test hook `window.__fig13` gained `strikeKE`, `foldsThrough`, `mapValue`, `energy`.

**11 November 2026, later: everything inside the Fig. 13 page.** A section "Inside Fig. 13" (`#inside`) under the figure: the catch
(`fig13/live-catch.html`) and the eight-part film player (`fig13/reem.html`) play in place in a frame on **Play here** (one at a time; the
sheet pauses while one plays and resumes on **Stop**), with links to the dashboard and the flower hunt. On plates narrower than 600 px the
axes are two range labels instead of a number per cell.

**11 November 2026, audit and continuation (a second session).** Checked independently (scripts kept: `tools/fig13/catch_stats.cjs`,
`tools/fig13/release_check.py`); what was wrong was corrected on the pages and here:
- The map's statistics, the model, the fold lines and the butterfly's numbers were recomputed and hold. Six cells, not five, are chaotic
  by the map: (17.78, 2) was missed because a cell's centre lies on a pixel corner and `mapValue` read one pixel; it now reads between
  the four nearest pixels, so mirror strikes read alike.
- The catch: 100 of 100 random starts are caught at 1, 4, 8 and 16 sub-steps and for the seeds 1, 2 and 2026 (median 17.5 to 18.9 s,
  slowest 229 s). Not reproducible and replaced by measurements: the film's "13.30 s" (see `catch.html` above); the basin (now 200
  random states per distance: 0.3: 140, 0.4: 112, 0.6: 62, 0.8: 26 held); "at most 0.0034 four laps after release" (median 0.0017, worst
  0.058 over 300 runs); "within 0.1 for 12 minutes" (median 403 s, shortest 41 s over 40 runs by DOP853); the free orbit's drift
  (2e-3 a lap at one sub-step, 4e-6 at four). The smallest Gramian direction is a change of energy, not of timing.
- Everything on the one page: `butterfly-dashboard.html` and `flower-hunt.html` take `?embed=1` (no header, no note; they report their
  height to the page that frames them); the player takes `?part=k`; the page's note is built by `tools/fig13/build_page.py` from
  `fig13_note.html` (Part I), the dashboard's note and `butterfly_note.html` (Part II), the hunt's notes (Part III) and
  `catch_note_body.html` (Part IV). After editing any of these run `python3 tools/fig13/build_page.py`; `--check` fails if the page is stale.
- Translation: `publish_films.py` adds a guard to every film (table `GUARD`): titles and captions shrink to stay inside their boxes when a
  browser's translation makes them longer. Measured with text made 35 % and 100 % longer: no title or caption overlaps another in
  parts 2 to 8 (before: the title over the subtitle in part 5, the catch's title under its buttons). Not tested with a real translator.
- Phone speed: a film's canvas was stage size times the device's pixel ratio (3240 x 5760 px on a phone of ratio 3, shown at a third
  of that). The published films now cap the ratio to what is displayed (`DPR_JS` in `publish_films.py`; the player passes `?dpr=`).
  Measured in headless Chromium at 390 x 844, ratio 3, processor slowed four times: the gift film 27 frames a second (12 before, at
  ratio 2), the catch 23 (7.5 before). While a station is open the paused sheet is not redrawn. Not measured on a real phone.
- Removed: `tools/fig13/gift/video_pages.py` and `tools/fig13/gift/catch.json` (nothing used them since the videos left the site).

- Zoom, atlas and two more views of the pinned pendulum (11 November 2026, later; `simulations/momentum-spirographs.html`, hand-written
  part): the sheet is a window on the plane of strikes with a centre `c1, c2` and a half-height `P`. **Zoom in / Zoom out** halve or
  double `P` around the pinned strike (`goTo` puts that strike exactly on a cell's centre and keeps it pinned); **Whole sheet** goes back
  to ±35.6 by ±20. The chaos map is drawn as the matching part of the one stored picture, at any zoom (before, it was hidden unless
  `P` was 20). The **Atlas** is a list of the 14 closed curves in `scripts/fig13-hunt-data.js` (the page now loads that file); choosing
  one resets the pendulum to equal rods under g = 9.8, goes to the strike and shows ±1 kg·m²/s of p₂ around it. The small picture of
  the pinned pendulum has three views: **Tip path** (as before), **Angles** (θ₂ against θ₁, both wrapped, kept since pinning, on its own
  canvas so only new path is drawn) and **Section** (one dot at (θ₂, p₂) each time θ₁ passes a multiple of 2π; a backward pass is drawn
  mirrored; up to 8 000 dots). The note's section 9 explains all three. Measured in headless Chromium at 1400 x 900 and 390 x 844: all
  14 atlas strikes land on their value to 1e-15 and their state returns after one period to within 0.03 (the step is 1/4500 s); a closed
  curve gives 1 to 7 separate dots after five periods, a chaotic strike (3.56, −2.00, map value 0.83) scatters 44 dots in 60 s; zooming
  keeps the pinned strike exactly; the map canvas agrees with `mapValue` at 762 of 763 random points of a zoomed window. A change of
  the window's height alone (a phone's address bar) no longer rebuilds the sheet.
- Loose ends closed (11 November 2026, last pass):
  - **Two captions on top of each other.** In the gift, construction, catch and dive films the old caption faded out while the new
    one faded in at the same place, so for 14 frames two texts lay over each other (in the gift: "فَرَاشَتُكِ: your butterfly" under the
    sentence about the pendulum). Now the old caption leaves first and the new one comes after. Measured over every frame of the
    gift (2647), the construction (1944) and the catch (901): 0 frames with both captions visible.
  - **Catalog.** The Fig. 13 entry no longer claims the badge `check` (stored value, formula, pixel read back): the page has no such
    panel. German and Arabic texts of the Fig. 12 and Fig. 13 catalog entries are stored (28 each); `tools/i18n/build.py --check`
    reports 0 missing. New terms are in `docs/glossary.md`.
  - **Problems.** Part I and Part IV of the note (and `butterfly-catch.html`) end with a "Problems" box, as `notes/STANDARD.md` asks.
  - **Åström and Furuta.** The link to the paper now goes to its DOI (the university copy stopped answering).
  - `butterfly_control.py`: a comment says its 30-strike loop is a test of the Python controller, not the source of the page's counts.
  - Left as they are, on purpose: the film captions are 30 px on a 1080 px stage (11 px on a 390 px phone), because each film's layout
    gives its caption a fixed box; the flower hunt is long on a phone because it holds 14 tiles, a bench and a chart.
- Dedication (11 November 2026): one line under the lede of the Fig. 13 page, "For my mother." with its German and Arabic
  (`.dedication`; the page now also loads `fonts/arabic.css` for the Arabic words, set in Amiri). The page itself exists in English only.

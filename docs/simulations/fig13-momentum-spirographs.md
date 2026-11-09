# Fig. 13 · Spirographs in Momentum Space, the Flower Hunt, the dashboard and the films

Published 8 November 2026 at Numa's word. English only (`ENGLISH_ONLY` in `tools/i18n/build.py`). Not yet in the catalog
(`public/scripts/catalog.js`) or in the hand-written Fig. links of the other pages: the Fig. 13 pages link to each other.

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
| `simulations/momentum-spirographs.html` | Fig. 13: live grid of the general family over the chaos map; controls for τ, N, P, model, ratios, g. |
| `simulations/flower-hunt.html` | The flower hunt: a garden of closed flowers and butterflies, a bench to test any kick, study notes. |
| `simulations/butterfly-dashboard.html` | The dashboard: complex plane, h(t) to the right joined by a horizontal line, x(t) below joined by a vertical line, both wave panels turned by φ (by itself or by hand). A wheel and the butterfly. Wide and tall (phone) layouts are chosen by the width of the figure. Test hook `window.__dash`. |
| `simulations/fig13/bell.html` | Film: the bell above the floor (3-D), r = 2l cos(Δ/2). |
| `simulations/fig13/turning.html?scene=wheel\|butterfly` | Film: turning the paper, with the deck of earlier pictures. |
| `simulations/fig13/together.html` | Film: six pictures on one clock; the phone layout on a portrait screen. |
| `simulations/fig13/dive.html` | Film, phone first: from momentum space into one cell, then the exposure grows from an eye's 0.1 s to one lap. |
| `simulations/fig13/reem.html` | (9 November 2026, evening: reem.html, construction.html and catch.html are now the live player, written by `film_page.py`; the precomputed videos were removed from the site and `video_pages.py` is superseded; the masters were made by `render.cjs` and ffmpeg and are not kept.) The gift For رِيمْ as a precomputed video (`video/gift-{dark,light}.mp4`), then the construction video, looping; follows the reader's light or dark setting. The film itself (`tools/fig13/gift/reem.html`, the first version Numa liked, in the house colours) writes رِيمْ and فَرَاشَتُكِ (each traced from a plate Numa chose) with 640 arrows each, then the butterfly by two arrows, then its dashboard with the paper turning, then the exact strike and why it is not chaos (numbers from `butterfly_physics.py`). Labels and captions in Instrument Sans. |
| `simulations/fig13/construction.html` | The construction as a precomputed video (`video/construction-{dark,light}.mp4`), looping; labels in Instrument Sans. The film (`tools/fig13/gift/construction.html`): h(t) beside the plane, x(t) below, the two time axes joined by a 45-degree mitre; for each instant a level and an upright line cross at the tip of the pendulum; a wheel first, then the butterfly. Videos and pages: `video_pages.py` (drawn live on a phone the films stuttered). |
| `simulations/fig13/catch.html` | Catching the butterfly, as a precomputed video (`video/catch-{dark,light}.mp4`), looping; also the third part of `reem.html`. The film (`tools/fig13/gift/catch.html`, data `catch.json` from `butterfly_control.film_data`): struck with p = (2, 4) (18 J), the pendulum swings in chaos for 8 s; a motor at the top pin (drawn as a direct-drive torque motor: six stator coils that glow with the current, a rotor of four magnets turning with the upper rod; torque constant 2.5 N·m/A, assumed) pumps and steers, catches at 13.34 s, holds four laps (corrections below 0.1 N·m), and lets go at 23.97 s within 0.0000 of the butterfly; a pen at the tip inks it, still within 0.0002 four free laps later. |
| `simulations/butterfly-catch.html` | Catching the butterfly: the live catch (`fig13/live-catch.html` in a frame) with **Random chaos** (random angles and momenta) and **Choose a strike** (a tap on the Fig. 13 chaos map, p₁ ∈ [−12, 12], p₂ ∈ [−8, 16], strikes both rods from rest), each restarting the run computed live; then the lecture note on the theory and the method (13 sections, 15 numbered equations, the phase diagram, the checks). Body in `tools/fig13/catch_note_body.html`. English only. |
| `simulations/fig13/film.html` | The whole gift as one film, computed and drawn live in the browser, nothing recorded: `live-gift.html`, `live-construction.html`, `live-catch.html` (copies of the three film renderers, by `publish_films.py`) played in order; the page keeps the clock and asks each film for frame f. The motion comes from `pendulum.js`: the pendulum's Hamilton equations integrated by RK4 (the butterfly from its strike, matching `orbit24.json` to 4e-7 rad); for the catch, the orbit, its step maps and the motor's periodic-LQR gains are computed at start (about 0.1 s, gains equal to the Python ones to three decimals) and the controller of `butterfly_control.py` runs as the film plays (caught at 13.30 s, Python 13.34 s); the catch film's clock follows the phases (chaos at half speed, the motor at a quarter, from a second after the catch at half). Play/pause, previous, next, from the start, Night/Paper, progress; loops. Written by `tools/fig13/gift/film_page.py`. The same film as one MP4 (about 60 MB) is too large for Cloudflare's 25 MiB per file; it is made from the three masters with ffmpeg and not committed. |

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

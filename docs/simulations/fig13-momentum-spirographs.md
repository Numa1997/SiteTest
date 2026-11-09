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
| `simulations/fig13/reem.html` | The gift For رِيمْ as a precomputed video (`video/gift-{dark,light}.mp4`), then the construction video, looping; follows the reader's light or dark setting. The film itself (`tools/fig13/gift/reem.html`, the first version Numa liked, in the house colours) writes رِيمْ (traced from the reference plate Numa chose) and فَرَاشَتُكِ (Amiri) with 640 arrows each, then the butterfly by two arrows, then its dashboard with the paper turning. |
| `simulations/fig13/construction.html` | The construction as a precomputed video (`video/construction-{dark,light}.mp4`), looping. The film (`tools/fig13/gift/construction.html`): h(t) beside the plane, x(t) below, the two time axes joined by a 45-degree mitre; for each instant a level and an upright line cross at the tip of the pendulum; a wheel first, then the butterfly. Videos and pages: `video_pages.py` (drawn live on a phone the films stuttered). |

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

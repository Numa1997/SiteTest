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

The four films are generated: edit `tools/fig13/gift/*.html` and run `python3 tools/fig13/gift/publish_films.py`, which rewrites the
asset paths, adds the two security meta tags and a link back to the dashboard. Opened without `?film=1` they loop live.

## Tools (tools/fig13/)

- `chaos_map.py` → `map_png.py` → `public/images/fig13/chaos-map-rods-P20.png` (1280 × 720 for p₁ ∈ ±35.6, p₂ ∈ ±20; row 0 is p₂ = +20).
- `hunt.py`, `hunt_inspect.py`, `hunt_export.py`, `butterfly.py`: the hunt for closed orbits; `hunt_export.py` writes `public/scripts/fig13-hunt-data.js`.
- `gift/orbit.py` → `gift/orbit24.json` (samples spaced T/(n−1), not exactly 1/3000 s; index by t/T·(n−1)).
- `gift/dive_data.py` → `gift/dive/dive.json` and `dive.bin` (not committed in tools/, about 47 s to regenerate; checks the butterfly cell against orbit24 to 3.6e-5 rad and every cell's energy to 1e-6).
- `gift/render.cjs THEME OUTDIR DSF [frames|all] [PAGE] [SCENE] [WxH]` renders a film to frames (local server on port 8766 in the repository root); ffmpeg makes the MP4. Videos are not committed.

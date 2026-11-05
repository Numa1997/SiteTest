# Fig. 12 · code review, round 2 (correctness only)

Reviewed 5 November 2026 on a frozen copy (the state of commit `7625918`, "round 1 of review"): `public/simulations/beer-slosh.html`
(classic script 437–925, module 926–1073), `public/scripts/walk/slosh.js`, `tools/fig12/*.py`, `notes/fig12/regress.cjs`, and the
generated `public/de|ar/simulations/beer-slosh.html` with `public/scripts/i18n/strings-*.js`. Line numbers are those of the frozen copy.
Every "reproduced" scenario ran in headless Chromium (Playwright, SwiftShader, 1440 × 900) on the frozen copy served at
`http://localhost:8766/`. The scripts are in the session scratchpad (`r2t/t1.cjs` … `t10.cjs`), not in the repository.

Physics against the note, with the renamed symbols: (6) and (12) in `deriv()` 605–621 (forcing −λQẍ/(1 + κ), sign, sin copies with ÿ);
(11) in `setup()` 571 with κ = M_f λ/ρ (570); (16) 573–574 (I_w/E, I_b/E stored pre-divided); the skin term 575; γ_b 576; (18) 578 with
R = `geo.a` and c_f = `P.kf`; the cylinder λ = (ξ/R) tanh(ξD/R), Q = 2R/(ξ² − 1), I_w, I_b, I_s (543–556) and the same formulas in
`note_numbers.py`; the Δ coefficient of (17), π·1.837/(√2 ξ^¼) = 3.503. All match. The ds symbols now read R, Z_s, κ, c_f. The only gap
left is item 16 below (how the σ term enters (12)).

## Round-1 items

| # | Round-1 finding | Status | Evidence (frozen copy) |
|---|---|---|---|
| 1 | Read-backs can never fail | **fixed** (one gap left) | Blank canvases: `eta_w` → ok false, "no ink"; `z_s` → ok false, "no stout". Gap: a wave above the plotted range gives ok false, not "off the plot" (new finding N4). |
| 2 | Arrow key's scale bar inside a comment | **fixed** | 734 px canvas: 40 drawn pixels in the 20 × 5 px bar region at (12, 16) (0 in round 1). |
| 3 | Cut turns 178° the long way | **fixed** | Held at 88° for 150 frames, then 92°: θ_p never left the axis by more than 2.0°, ends at 92.0°. |
| 4 | Paused trace keeps scrolling | **fixed** | 30 paused frames: simulated time +0 s, 0 bytes of the trace canvas changed (4444 px in round 1). |
| 5 | `fieldAt` radius and axis value | **fixed** | x‑slosh, ȧ₁₁ = 10 mm/s, plane y–z: u_θ = −8.172 / −8.169 / −8.081 mm/s at j = 0, 1, 2 (row 1); bottom row r(j=1) = 2.821 mm = R_i(floor)/11. Remaining approximations (nearest stored fill, the 0.2 % inset) are said in section 9. |
| 6 | `xg` without the sideways shaker | **fixed** | After "Sideways at f₁" + 0.8 s: `xg` = −0.1017 mm = drawn glass x. |
| 7 | Store's `shaker` stale | **fixed** | shF1 → `'x'`; Stop → `'off'`; segment Sideways → `'x'`, Stop → `'off'`. |
| 8 | i18n: bare literals, `_t(variable)` | **code fixed, pages not rebuilt** | All literals now go through `_t('…')`, the damping rows by index. But the frozen `strings-de.js`/`strings-ar.js` lack 8 of the 51 keys ("wall, floor", "skin", "interior", "head", "total", both drag hints, the WebGL fallback), and the German and Arabic pages are still built from `0bb9f8b`: see N1. |
| 9 | "Straight" draws the tulip | **fixed** (hit-test gap) | Cut walls vertical at R (screenshot); 3D `cylOuter` shown, tulip hidden; `gridPos(19, 11)` = 39.44 mm = R; inspect "…, 39.4 mm from the axis". Gap: the 3D hit test still uses the hidden tulip (N7). |
| 10 | Shaker stop jumps; f and A act on the absolute phase | **partly fixed** | Stop: x 4.854 → 4.854 mm (no jump). Still open: A slider 5 → 1 mm while running: drawn x 4.854 → 0.971 mm in one frame; f 3.00 → 3.01 Hz at t_shake = 30 s: x 0.000 → 4.755 mm (phase still 2πf·t). And a new order bug in the two shaker buttons (N2). |
| 11 | Remainder of dt thrown away | **fixed** | `carry` accumulator: over 120 frames simulated time advanced 2.033 s against Σ min(dt, 50 ms) = 1.994 s (difference = the first frame's phase). |
| 12 | Trace spans 480 frames, not 8 s | **fixed** (two loose ends) | Points kept by simulated time, SPAN = 8 s. Loose ends: the push rule skips frames (N3) and `about` still describes 480 frames (N5). |
| 13 | Wheel and touch capture the page scroll | **partly fixed** | Plain wheel over the 3D view: page scrolled 209 → 0, glass not lifted. Still `touch-action: none` (line 33): a phone swipe that starts on the 3D view cannot scroll the page. Shift+wheel has its own problem (N6). |
| 14 | Captions rewritten every frame | **fixed** | MutationObserver over 3 s: cap-plane 2.3/s, cap-u 2.3/s, cap-t, state, r-geff, r-fb 2.7/s each; throttled by wall time (`capNext`, 250 ms), so it holds at any refresh rate. |
| 15 | m = 0 sin slots seeded 10⁻⁶ | **fixed** | After seed + 2 s of steps: both slots exactly 0. (The `a_osc` long_name still does not say that two slots are unused.) |
| 16 | (12) and the walkthrough modulate σ by z̈ | **partly fixed** | Note line 330 adds "(For clarity the σ term of (11) is not repeated; the page keeps it.)": it does not say that z̈ multiplies only gλ. Walkthrough step 5 (slosh.js:59) still says "O2 is the spring constant ω_n²(1 + z̈/g) … including surface tension and the head", which the code (612) does not do. |
| 17 | γ_w, γ_s checks use unstored I_w, I_b, I_s | **not fixed** | Lines 870–871 still read `M[k].Iw`, `M[k].Ib`, `M[k].Is`; no `ds.var` for them. |
| 18 | Numbers on screen read locals, not the store | **not fixed** | `r-vol` from `P.V`/`GL` (774), `cap-t` from `tSim` (782), `cap-spill` from `nSF`/`nSL` (783), spill state from `spillL`/`spillF` (786–787), `Sim.live().Om` from `P.Om` (922); new: the trace's head line pushes `P.hf` (750), the `z_s` read-back uses `geo.zs` (887). |
| 19 | "No head" label stale | **fixed** | Head slider → 0: button reads "Pour a head" (`setup()` relabels, 585). |
| 20 | Per-frame garbage | **not fixed** | Same closures and arrays; `fieldAt` now calls `gridPos` (659), so each grid point allocates one array more than before. |
| 21 | Right button, lost capture, unused `held` | **partly fixed** | Right-button drag on the glass: Tg.x 0, view not turned. `lostpointercapture` mid-drag, then move 80 px: Tg.x stays 13.92 mm (drag ended). `held` is still written (591, 912, 1007) and never read. |
| 22 | Walkthrough last step's symbol and marker | **not fixed** | The step now lists `umax` (slosh.js:99), but neither its formula nor its code has a ⟦umax⟧ marker, and `umax` is computed in `drawSection()`, not in the `fieldAt` lines shown: nothing lights up. (Steps 1, 4, 5, 6 also list symbols without a marker: V, zeta, az and Q, t.) |
| 23 | check_cylinder prints the wrong tolerance | **not fixed** | `check_cylinder.py:24` still prints "within 1e-4" while line 23 allows 3e-4 for n = 3. |

Summary: 13 fixed (items 1, 9 and 12 with a loose end, logged below as N3–N5 and N7), 5 partly fixed (8, 10, 13, 16, 21),
5 not fixed (17, 18, 20, 22, 23; all nits).

## New findings

| # | File:line | What | Scenario that shows it | Severity | Suggested fix |
|---|---|---|---|---|---|
| N1 | public/de/simulations/beer-slosh.html, public/ar/simulations/beer-slosh.html (generated); scripts/i18n/strings-{de,ar}.js | The German and Arabic pages are generated copies built from English commit `0bb9f8b`. None of the round-1 code fixes reached them: they still contain `ok: !!px`, have no `stopShaker`, no `carry`, the old symbols (k_f, z_s, a), and the 8 new `_t` keys have no translation. Once `main` is published, /de/ and /ar/ still carry every round-1 bug. | Reproduced on `/de/simulations/beer-slosh.html`: pause, clear both canvases: `eta_w` → ok **true**, "Tinte auf der vorhergesagten Höhe"; `z_s` → ok **true**, "Farbe des Stouts"; damping table rows "wall, floor", "skin", "bulk", "head", "total" in English. `grep -c "ok: !!px"` = 2 on both pages. | bug | Translate the 8 keys, run `python3 tools/i18n/build.py`, and make `build.py --check` a gate before merging (it fails exactly in this case). |
| N2 | beer-slosh.html:819, 820 | "Sideways at f₁" and "Up and down at 2f₁" call `setRange('f', …)` and `setRange('A', …)` **before** `stopShaker()`. `stopShaker` then hands over `shakerPos(tShake)` computed with the new A and f, not the displacement the glass had, so the glass jumps. | Reproduced: shaker sideways at A = 5 mm, f = 3 Hz, 1.08 s in (drawn x = 4.854 mm), click "Sideways at f₁": drawn x = 0.001 mm in the same frame, a 4.85 mm jump with the velocity step not delivered to the modes. Same pattern for shF2 (z). | bug | Call `stopShaker()` first, then the two `setRange` calls. |
| N3 | beer-slosh.html:750 | The trace pushes a point only when `tSim − t_last ≥ SPAN/HN = 16.67 ms`. At 60 Hz the frames advance 17, 17, 16 ms (whole steps of 1 ms), so every third frame pushes nothing. The last drawn point then lags the store's `eta_w` by up to 16 ms, the line ends 1.4 px short of `trMap.x`, and the read-back looks for ink at the new height. | Reproduced at a measured 16.7 ms frame time, steady sideways resonance (wave about 4 mm): 3 of 13 read-backs report "no ink". Column scan: ink 2 px left of the end at y = 103 px, predicted 107 px (another case 117 vs 125 px). Push rule replayed at fixed rates: 60 Hz, 33 % of frames push nothing, 320 points per 8 s; 120 Hz, 67 %, 320 points; 144 Hz, 67 %, 384 points (the "480" is never reached). | bug | Push whenever `tSim` advanced and thin older points instead, or always draw the line on to the current `(tSim, eta_w)` without storing it. Either way the newest point drawn is the store's value. |
| N4 | beer-slosh.html:880–883 | The `eta_w` read-back has no "off the plot" case. The trace is clipped to `[−0.35·span, span]`, `span = max(20 mm, rim + 4 mm)`. A wave above that is not drawn by design, yet the hook reports a failure. | Reproduced: paused, (1,1) amplitude 50 mm (η_max = 49.99 mm, plot top 26.46 mm): `ok: false`, "no ink". | risk | When `trMap.y(eta)` is outside the clip rectangle, return `{ ok: null, note: _t('off the plot') }` (round-1 item 1 suggested this). |
| N5 | beer-slosh.html:904 | `about` still says "The trace keeps the last 480 frames, which is about 8 s at 60 frames per second". Since the round-1 fix the trace is kept by simulated time (8 s at any frame rate). That is the paragraph the reader opens to learn how the drawing differs from the store. | Code reading against 747–751. | bug (doc) | "The trace keeps the last 8 s of simulated time, one point about every 17 ms." Add N3's thinning if it changes. |
| N6 | beer-slosh.html:1019 | Shift+wheel is meant to lift the glass, but it reads only `e.deltaY`. Chrome and Edge on Windows and Linux, and macOS for a mouse wheel, deliver a Shift+wheel as a horizontal scroll (`deltaX ≠ 0`, `deltaY = 0`). The handler then calls `preventDefault()` and changes nothing. The page's instructions (step 1) promise "the mouse wheel or Shift-drag". | Reproduced with the event as those browsers send it: Shift, wheel (−300, 0): event `[deltaX −300, deltaY 0, shift true]`, Tg.z stays 0. With Playwright's (0, −300) the glass lifts 60 mm, so it works only when the browser does not convert. | risk | Use `const d = e.deltaY || e.deltaX`. |
| N7 | beer-slosh.html:1002 (also 960, 737–738) | In straight mode the 3D hit test still raycasts the hidden tulip `outer` (three.js r181 raycasts invisible meshes; `Qu()` tests only layers) and not the visible `cylOuter`. Pressing on the visible cylinder wall turns the view; pressing on empty air just outside it grabs the glass. The rim ring (3D) and the rim line (cut) also stay at the tulip's rim radius, 39.0 mm, against the cylinder's 39.4/41.4 mm walls. | Reproduced, Straight, 500 mL, silhouette points: wall at r = 40.5 mm, z = 40 mm → turned the view, no grab. Empty air at r = 42.0 mm, z = 120 mm (cylinder outer 41.44 mm) → grabbed the glass. | nit | Raycast `[cyl ? cylOuter : outer, surf, wall, headTop]` (or filter hits by `object.visible`). In straight mode put the rim at `geo.a + 0.002`. |
| N8 | beer-slosh.html:893 | `probe` snaps to every grid row `i = 1 … NZ−1`, but the cut draws arrows only on odd rows (718). Half the points a reader can pin show a marker where no arrow is drawn. | Code reading: the loops at 718 (`i += 2`) and 893 (`i++`). | nit | Step `i += 2` in `probe`, or draw every row. |
| N9 | notes/fig12/regress.cjs:5, 14, 20 | The regression test opens port 8765 (the shared dev server), leaves dead lines (`before` unused; 200 `noop` events that do nothing), checks only some round-1 items, and always exits 0. It cannot gate anything. | Code reading. | nit | Take the URL from `process.argv`, drop the dead lines, `process.exit(1)` on any failed check, and add N2/N3/N4. |

## How the new code was checked (no row)

- `stopShaker()`/`shakerVel()`: `shakerVel` is the exact derivative of `shakerPos` (the ease-in term included); Stop and switching
  the segment hand position and velocity to the follower without a jump (item 10). The acceleration steps at the hand-over, as a
  real release would.
- `carry`: `Math.floor(carry/h + 1e-9)` cannot lose or double a step; a negative remainder of 10⁻¹² is harmless.
- `capNext`: one wall-clock gate for the two cut captions and `readouts()`, all in the same frame, so they change together.
- `seed()`: the m = 0 sin slots stay at 0 because `deriv` holds both their rate and value.
- `fieldAt` and `gridPos`: radius R_i(z)·j/(NS−1) of the present fill (or R in straight mode); the axis limit Φ/r → ∂Φ/∂r (m = 1),
  → 0 (m ≥ 2) is right for u_θ = mSΦ/r. The cylinder's field is computed on exactly the grid `gridPos` uses.
- `Rdraw()`/`showShape()`: 2D stout, head and walls and 3D stout, head and walls all use `Rdraw`. The cylinder's inner floor is at
  Z_floor = 8 mm, a profile point, so the cut has no slanted corner.
- `_t()`: 51 distinct literals, none built from a variable. `window._t` exists for the module (sim.js line 4); placeholders
  (`{z}`, `{d}`, `{r}`, `{T}`) are filled by `T`.
- tools: `note_numbers.py` and `controller.py` use the page's formulas (fill interpolation, (11), (16)–(18), the cylinder integrals).
  The controller's liquid momentum ρπ Σ Q_n N_n a_n and the effective mass M − Σ m_n follow from ∫η x dA = π a Q N.

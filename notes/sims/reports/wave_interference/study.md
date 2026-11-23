# Fig. 1, Wave interference: study for moving it to data computed once on Kaggle

Written 23 November 2026 on branch `kaggelize/wave_interference` (scheduled task "Kaggelize simulations"); kept true through Step 2 (build). Simulation name in the
pipeline: `wave_interference`. This file is the plan as studied; it is kept true while the work is built and rewritten at the end
into what was built and measured.

Page: [public/simulations/Circular Wave Interference Visualization.html](../../../../public/simulations/Circular%20Wave%20Interference%20Visualization.html)
(908 lines). Doc: [docs/simulations/fig01-wave-sources.md](../../../../docs/simulations/fig01-wave-sources.md). Walkthrough:
`public/scripts/walk/circles.js`. Line numbers below are those of `main` at f8819df.

## 1. The page today

**Controls** (all in the panel beside the figure, except the click):

| Control | Where | Range, step, default | What it does now |
|---|---|---|---|
| Pause / Play | L61 | toggle | stops and starts the clock |
| Line of 16 | L62, L721–725 | 16 sources at x = 64 + 44.8 n px | replaces the sources |
| Add 5 random | L63, L726–730 | 5 sources uniform in 133.3–666.7 px (`Math.random`) | adds to the list (newest 24 kept) |
| Reset | L64, L731–734 | 2 sources at 200 and 600 px; time phase to 0 | replaces the sources |
| Clear | L65, L735 | no sources | empties the list |
| Wavelength λ | L73 | 16–64 px, step 0.1, default 30 | rebuilds the maps |
| Frequency f | L77 | 0.2–2 Hz, step 0.05, default 1.1 | changes only how fast the phase turns |
| Damping γ | L81 | 0–0.6, step 0.01, default 0.15 | rebuilds the maps |
| Click on the field | L717–720 | any x across the width, at the source line | adds a source |
| Parameter curve | L599 (`Sim.curve`, `scripts/curve.js`) | a knob (λ, f or γ) follows a curve p(t), five ready examples | moves a slider by itself, to exact values between its steps |

**Pictures and readouts:** the field canvas `#field` (L49), a colour image of ψ with the source dots; the caption count `#cap-count`
(L53); the colour bar and legend (L86–89); the readouts "Sources" `#r-n` (L93) and "Speed v = fλ" `#r-v` (L94); the data panel
(`scripts/datalog.js`, L905, which reads the store `ds` declared at L527–582); the walkthrough "From symbols to code" `#walk` (L498,
key `circles`). The lecture note (L99–496) has fixed SVG figures, not computed by the page.

## 2. The physical system and its equations

A still pond seen from above. A row of small floats sits on one straight line; a motor makes them all bob up and down together.
Each float sends out a ring of ripples. Where rings meet, their heights add. The page shows the height of the water at every point
as a colour: burgundy for a crest, dark ink for a trough, cream for still water.

Symbols (the page counts every length in px of a field that is always 800 px wide; time in seconds). The model states its
parameters in SI by choosing the field 0.40 m wide, so 1 px = 0.5 mm, λ = 8 … 32 mm, R = 0.15 m; nothing in the picture depends on
that choice, only on k r and γ r/R:

| Symbol | Meaning | Unit |
|---|---|---|
| x, y | position in the field, x to the right, y down from the top-left corner | px |
| x_s | position of source s along the source line | px |
| y_s | height of the source line: 10 px above the bottom edge | px |
| r_s | distance from a point to source s, r_s = √((x − x_s)² + (y − y_s)²) | px |
| λ | wavelength, the distance from one crest to the next | px |
| k | wave number, k = 2π/λ: how many radians of phase per pixel of path | rad/px |
| f | frequency, how many times a second each source bobs | Hz |
| ω | angular frequency, ω = 2πf | rad/s |
| γ | damping: how many factors of e a ring's height loses over R = 300 px | 1 |
| a(r) | height of a ring at distance r, a = e^(−γr/R) | 1 |
| N | number of sources (at most 24) | 1 |
| ψ | the height shown, between −1 and 1 | 1 |
| C, S, A | the two time-independent maps and the amplitude | 1 |

One ring (note eq. 5): ψ_s = a(r_s) cos(k r_s − ωt). All rings added and divided by N (eq. 6): ψ = (1/N) Σ_s a(r_s) cos(k r_s − ωt).
Because every ring has the same ω, the sum splits exactly into space times time (eq. 18): ψ = C cos ωt + S sin ωt with
C = (1/N) Σ a cos(k r_s), S = (1/N) Σ a sin(k r_s), and the amplitude A = √(C² + S²) (eq. 7). Readouts: v = fλ (eq. 8), T = 1/f.

## 3. How the browser computes it now

| Function | Lines | What it computes | When |
|---|---|---|---|
| `resize()` | L601–626 | grid size cols = clamp(round(w/1.1), 60, 360), rows in proportion, cell centres x, y | on load and on every resize |
| `precompute()` | L628–658 | for every source and every cell: r = √(…), a = e^(−g r)/N, cos(kr), sin(kr); sums C, S; then A = √(C² + S²); source-1 maps r1, a1, φ1 | when a slider λ or γ moves, a source is added, cleared or reset, or the window resizes |
| `render()` | L660–700 | cos ωt and sin ωt once, then ψ = C cos ωt + S sin ωt per cell, colour row round(127.5ψ + 127.5), pixels; source dots | every frame |
| clock callback | L757–768 | ωt ← ωt + 2πf Δt | every frame |
| `readouts()` | L707–715 | v = fλ, ω = 2πf, T = 1/f | when a slider moves |

Per slider move (λ or γ) or source change: 2·N·P calls of cos and sin, N·P of exp and sqrt (P = cells: 360 × 162 = 58 320 on a wide
screen). Per frame: 2 multiplications and an addition per cell, no trigonometry per cell. Moving f recomputes nothing.

## 4. The raw data the page needs to play without computing

The page's state that changes the picture: λ (481 slider values), γ (61), the list of sources (up to 24 positions anywhere on a
continuous line, by click), the grid (depends on the screen), and the time.

Time costs nothing to store: one period is fully described by the two maps C and S (ψ at any moment is C cos ωt + S sin ωt), so
f only sets how fast the stored period is played. Per source configuration and slider pair the page needs C and S on its grid:
2 maps × 360 × 360 cells × 4 bytes (float32) = 1 036 800 bytes. Axes: λ (481) × γ (61) × sources (unbounded: clicks are
continuous) × time (2 quadrature maps for one period) × space (rows × cols). For a single fixed source configuration that is
481 × 61 × 1 036 800 bytes = 30.4 GB; with clicks the number of configurations has no end. Storing finished fields is impossible.

What can be stored: the field is a sum of rings (linear), and a ring depends only on its distance r. So the page needs, per λ, the
angle k r of each ring, and, per γ, its height a(r), at every distance that occurs between a cell and a source. If cells and
source places sit on a common lattice, those distances form one table.

## 5. The plan to generate it once

**Grid** (lattice: a regular pattern of points): cells of DX = 3.2 px, 250 columns × 250 rows (the square field of a phone,
800 px tall; a wide screen shows the bottom 113 rows). Rows are counted up from the bottom edge, so the source line (10 px up) is the
same on every screen. **Source places:** x_s = 1.6 q px, q = 0 … 500. Every preset lies on these places exactly (Reset q = 125,
375; Line of 16 q = 40 + 28 n). A click or a random source goes to the nearest place. The horizontal gap between cell i and source
q is then 1.6·|2i + 1 − q| px = 1.6 m px with m = 0 … 499, and the vertical gap of row j is 3.2 j − 8.4 px: one table of
500 × 250 = 125 000 distances r(m, j).

**Nodes** (the slider values that have stored data): λ = 16, 17, …, 64 px (49 nodes, includes the default 30 and every λ the note
quotes: 16, 30, 32, 40, 60, 64); γ = 0, 0.05, …, 0.60 (13 nodes, includes the default 0.15). f stays continuous.

**Stored per file** (method: closed form, eq. 5, evaluated in float64 by NumPy; no integration, so no tolerances to set):

| File | Content | Type | Bytes (measured) |
|---|---|---|---|
| `geometry.bin` | r(j, m); table cos(2πn/65536), n = 0 … 65535 | float32; int16 (1/32767) | 632 640 |
| `ring_lNNN.bin` × 49 | angle k r reduced to one turn | uint16 (2π/65536 rad) | 250 244 to 250 260 each |
| `damp_gNNN.bin` × 13 | height a(r) = e^(−γr/R) | uint16 (1/65535) | 250 188 to 250 208 each |
| `wave_interference.json` | parameters, node lists, checks | JSON | 3 352 |

Total measured in the local run of the built model (23 November 2026): 16 150 676 bytes in 64 files, inside the 20 MB budget. The page downloads only what it
shows: at opening `geometry.bin` + `ring_l030.bin` + `damp_g015.bin` = 1 133 076 bytes; each new λ or γ node another 250 kB, checked by
SHA-256 like the rest. Run time measured here (2 CPUs): 79.6 s, almost all of it the checks (637 node pairs × 2 presets × 32
instants). Random starts and seeds: none are needed. The system is not chaotic and has no random state; "Add 5 random" keeps
choosing places at random in the page, now among the 501 stored places.

**What the page then does:** for each source it reads, for each cell, the stored angle and height, turns the angle into the two
arrow components with the stored cosine table (no cosine evaluated), and adds them (superposition, eq. 6); per frame it turns the
sum to the moment t (eq. 18) and colours it. It evaluates no cos, sin, exp or sqrt of the field.

**Ways out weighed** (the finished field cannot be stored, section 4):

| Way | Size | Cost and risk | Verdict |
|---|---|---|---|
| A. Store finished fields for the presets only, drop clicks and random sources | ~0.5 MB per (λ, γ, preset): only ~40 fit | removes the page's main interaction and note §9; λ would need to be very coarse | rejected |
| B. Store each ring's angle (per λ) and height (per γ) on a common lattice; the page adds the rings of the chosen sources | 16.1 MB | grid 250 instead of 360 columns; λ in 1 px, γ in 0.05 steps; sources snap to 1.6 px | **taken**: keeps every control, stores every number the physics produces |
| C. Store the product a·e^(ikr) per (λ, γ) pair | 637 × 500 kB = 318 MB | over budget 16 times | rejected |
| D. Store a(r) and k r as functions of r alone on a fine line, the browser computes r = √(…) per cell and interpolates | about 4 MB | the browser computes square roots and interpolates again: the computing stays | rejected |
| B' (finer): cells of 1.6 px (500 columns) | 20 MB with λ in 2 px steps | at the budget's edge, coarser λ | rejected for B |

Risk of B: every new generation adds 16 MB to the repository's history (the line keeps each dated folder).

## 6. What the page will no longer be able to do

- Wavelength between whole pixels: the slider moves in 1 px steps (was 0.1 px); a parameter curve on λ moves in 1 px steps.
- Damping between steps of 0.05 (was 0.01); a curve on γ moves in those steps.
- A source between the 501 stored places, 1.6 px apart (about 1.5 css px on a wide screen).
- A grid finer than 250 columns: at λ = 16 px, 5 cells per wavelength (was 7.2 on a wide screen).
- Show anything before the data has arrived: until then one plain sentence stands in the figure; a changed λ or γ shows the new
  node once its 250 kB file has arrived and passed its SHA-256 check.
- φ₁ in the data panel becomes the angle within one turn (0 to 2π), as stored, instead of k r unwrapped.

## 7. The checks the model carries

Measured in the local run above, all in `wave_interference.json`:
- **Comparison with today's browser result.** The page's own sum from the stored tables, against the float64 sum straight from
  eq. 5–6 (what the browser computed live), for Reset and Line of 16 at all 637 node pairs: largest difference 5.9e-5 in C,
  6.0e-5 in S, 6.3e-5 in ψ; at 32 instants of one period the colour row (one row = 2/255 = 0.0078 of ψ) differs in 1 794 573 of
  2 548 000 000 cell-instants (0.070 %), always by one row, where ψ lies at a row boundary. This is the rounding of the stored angle
  (half a count, 4.8e-5 rad) and of the cosine table (1.5e-5), named as such. A second comparison in headless Chromium, done in Step 2:
  the page as it was on `main` (live computing), in a window 309 px wide, has a canvas of 275 css px and exactly the new grid
  (250 × 250 cells of 3.2 px, same cell centres, same source positions). Its live maps against the new page's, cell by cell:

  | Case | max \|ΔC\| | max \|ΔS\| | colour rows differing (32 instants × 62 500 cells) |
  |---|---|---|---|
  | Reset, λ = 30, γ = 0.15 | 5.1e-5 | 4.7e-5 | 2 392 of 2 000 000, by one row |
  | Reset, λ = 45, γ = 0.5 | 3.7e-5 | 3.6e-5 | 1 568, by one row |
  | Line of 16, λ = 30, γ = 0.15 | 2.0e-5 | 1.9e-5 | 890, by one row |
  | Line of 16, λ = 16, γ = 0 | 2.2e-5 | 2.0e-5 | 1 180, by one row |
  | Line of 16, λ = 64, γ = 0.6 | 1.3e-5 | 1.3e-5 | 528, by one row |

  And the new page's C and S in the browser equal, bit for bit in all 28 250 cells (1600 px window, Reset, λ = 30, γ = 0.15), the
  page's sum as the model emulates it (`page_sum`).
- **A known limit.** Two sources at γ = 0: the amplitude must be |cos(k(r₁ − r₂)/2)| exactly (calm lines where the path difference is
  a half-odd number of wavelengths). Largest deviation over all 49 λ: 6.3e-5.
- **A conserved quantity.** A stored ring keeps the length of its arrow: cos² + sin² − 1 of the stored cosine table, largest 4.2e-5.
- **Rounding of every stored number:** the stored height against e^(−γr/R), largest error 7.6e-6 (half a step, 7.6e-6); the stored
  angle against 2πr/λ mod 2π, largest 4.8e-5 rad (half a step); the cosine table, 1.5e-5.

## 8. Words used

- **Kaggle**: a website that runs code on its computers; here it runs the model once and keeps the output.
- **Model**: the Python program `tools/sims/wave_interference.py` that computes the stored numbers.
- **Pipeline**: the automatic line GitHub → Kaggle → GitHub → Cloudflare → live check, described in `docs/kaggle-sims.md`.
- **Generation**: one run of the model, stored under its date in `public/data/sims/wave_interference/<date>/`.
- **SHA-256**: a 64-character fingerprint of a file; one changed bit changes it. The page compares it before using a file.
- **Superposition**: waves pass through each other and their heights add.
- **Phasor (arrow)**: a turning arrow whose shadow on one axis is the oscillation; its length is the height, its angle the timing.
- **Wave number k**: phase gained per pixel of path, 2π/λ.
- **Damping γ**: how fast a ring's height falls with distance in this model.
- **Node**: a slider value for which data is stored.
- **Lattice**: a regular grid of points; here cells every 3.2 px and source places every 1.6 px.
- **Grid cell**: one small square of the field with one computed value.
- **float32, int16, uint16**: ways to store a number in 4 or 2 bytes; int16 holds whole numbers −32768 to 32767, uint16 0 to 65535.
- **Colour table (LUT)**: 256 colours; ψ picks row round(127.5ψ + 127.5).
- **Data panel**: the table under the figure that shows every stored number and checks it three ways.
- **Walkthrough**: the section "From symbols to code" that pairs each equation with the page's code.
- **Headless Chromium**: a web browser run by a program, without a screen, to test pages.
- **Quantisation / rounding gap**: the small difference a stored whole-number count leaves against the exact value.
- **Budget**: the most data allowed for this simulation, 20 MB.

## 9. Built (Step 2, 23 November 2026)

What was built follows section 5 without change of plan. Files: the model `tools/sims/wave_interference.py` (SI parameters at the
top, equations in the docstring, `run(out_dir)` writes the 64 files and their headers, checks of section 7 in the output); the entry
`wave_interference` in `tools/sims/registry.json` (the live check opens the page and expects the three opening files checked and the
commit of the generation); the page, whose script now loads the newest generation from `data/sims/generations.json`, checks each
file's SHA-256 and adds the stored rings (`stored()`, `load()`, `superpose()`); until the data has arrived one sentence stands in the
figure; the old computing code (`precompute()`: the square root, exponential, cosine and sine per source and cell) is removed. English
page: 908 lines, as before. The walkthrough, the note §8 and §10, the German and Arabic pages and the page's doc
(`docs/simulations/fig01-wave-sources.md`) describe the new code.

Tested here in headless Chromium against the local run's data: at 1600, 1100 and 390 px no console error, the data ready in 0.8–1.3 s,
and every control changes the picture (Pause stops it, Play moves it, Line of 16, Add 5 random, Reset, Clear, a click on the field,
λ, γ; f changes the phase speed: 3.14 rad/s at 0.5 Hz, 12.57 rad/s at 2 Hz). The data panel's checks at the centre cell and the
comparisons are in the page's doc ("Proof") and in section 7.

Kaggle, 23 November 2026: the model reached `main` alone first (PR 177; the old page stayed until the data was checked), the workflow
"Simulations on Kaggle" ran it as notebook version 2 (code 5f98017, 171 s on 4 CPUs, NumPy 2.1.3), checked every file by SHA-256 and
committed 64 files, 16 150 677 bytes, as 6be1fd7. Every check in its output equals the local run's. The page switch followed in a second
pull request.

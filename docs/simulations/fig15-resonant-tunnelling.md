# Fig. 15 · Resonant Tunnelling (3D)

| | |
|---|---|
| Page | [public/simulations/resonant-tunnelling.html](../../public/simulations/resonant-tunnelling.html) (English only, listed in `ENGLISH_ONLY` of [tools/i18n/build.py](../../tools/i18n/build.py)) |
| 3D view | [public/scripts/rt3d-view.js](../../public/scripts/rt3d-view.js) (three.js, vendored in `public/vendor/three/`) |
| Run reader | [public/scripts/rt3d-worker.js](../../public/scripts/rt3d-worker.js) (a Web Worker: fetch, SHA-256, inflate, levels → ψ) |
| Lecture note | [public/scripts/resonant-note.js](../../public/scripts/resonant-note.js) (injected into the page's `<article>`, typeset by `sim.js`) |
| Data | [public/data/resonant-tunnelling/](../../public/data/resonant-tunnelling/): `generations.json`; generation 2026-11-13: `kaggle/index.json` and `kaggle/runs/*.bin` (115 runs, 185 MB), `derived/exact-1d.json` |
| Solver, runner, filing | [tools/kaggle/resonant-tunnelling/](../../tools/kaggle/resonant-tunnelling/): `rt3d.py`, `rt3d_run.py`, `build_rt3d.py`, the loader notebooks `rt3d_*.ipynb`, `read_rt3d.py`, `file_rt3d.py`, `exact1d.py`, `tm.py`, `iv.py` |
| Equation checks | [notes/fig15/derive.py](../../notes/fig15/derive.py), [notes/fig15/derive.md](../../notes/fig15/derive.md) (1D theory, SymPy + NumPy, 24/24); grid tests `notes/fig15/grid_test*.py` |
| Brief & lessons | [notes/fig15/BRIEF.md](../../notes/fig15/BRIEF.md), [notes/fig15/LESSONS.md](../../notes/fig15/LESSONS.md) |
| Catalog entry | [public/scripts/catalog.js](../../public/scripts/catalog.js) (`id: 'resonant-tunnelling'`, `fig: 15`, `field: 'quantum'`) |

An electron wave packet meets two thin barriers in three dimensions: two walls, two discs (radius 2, 4, 6) or two
spherical shells (radii 3 and 5.5), and each barrier alone. Barrier height `V₀ = 2`, thickness `d = 1`, centres `s = 2.5`
apart; the pair resonates at `E = 0.735` (`Γ = 0.0704`, `τ = 14.2`). The figure continues Fig. 14: same method, grid and look.
**The page plays stored 3D runs computed on Kaggle's GPUs; it computes nothing else.**

## What was computed

[rt3d.py](../../tools/kaggle/resonant-tunnelling/rt3d.py): Strang split-step Fourier (JAX, complex64) on a 192 × 128 × 128
grid, 0.5 a apart (96 a along the flight, 64 a across), `dt = 0.01`, an absorbing border `sin^(1/8)` in the outer tenth of
each axis. Barrier faces lie on cell boundaries (odd multiples of 0.25 a), so each barrier is exactly two grid points thick.
Packet: Gaussian, `σ₀ = 3`, `x₀ = −20`, wholly outside every barrier (share inside < 1e-9, stored per run). Run length
`40/√(2E) + 3τ`, 200 frames.

Runs: two walls, two discs ×3 radii, two shells at 18 energies (0.4 … 2.0 and 0.735); each barrier alone at 5 energies.
Five Kaggle notebooks (2 × T4): `numakoudsie/fig15-rt3d-shard-{1..4}-of-4` (version 1, solver at commit `eb3cff0`) and
`numakoudsie/fig15-rt3d-singles-v2` (version 1, commit `db0a60c`). The 20 single-wall and single-disc runs of the shards are
**not shipped**: version 1 centred them at `x = 0`, where `|x| < d/2` holds one grid point (half the thickness; `T = 0.388`
against the exact 0.075). `kaggle/index.json` records this and what replaced them.

Cost: the sweeps took 1559 s of GPU time; the Kaggle quota counter rose by 4598 s (1.28 h) over the smoke test, the four shards
and the singles fix, because Kaggle also counts notebook start-up and installs.

Stored per run (`RT3C`, read by [read_rt3d.py](../../tools/kaggle/resonant-tunnelling/read_rt3d.py)): a JSON header (peaks, region
probabilities per frame, timing, start checks); then zlib of `|ψ|` and `arg ψ` on the plane `z = 0`, half `y ≥ 0`, `x ∈ [−32, 32)`,
as 8-bit levels of each frame's own peak; the profile `p(x, t) = ∬|ψ|² dy dz` (float32, whole box); and for walls the exact 1D twin
on the same x grid and step.

[file_rt3d.py](../../tools/kaggle/resonant-tunnelling/file_rt3d.py) checks every file's SHA-256 against its notebook's index,
copies it byte for byte, and writes `kaggle/index.json` with, per run, its notebook, version, commit and SHA-256, and numbers read
once from the stored curves:

- `T_far` = (P_beyond + P_between / 2) / P_box at the last frame before the wave reaches the end borders (|x| > 38.4 holding
  < 1e-3); dividing by P_box removes the side border's share.
- `tau` = straight-line fit of ln P_in(t) where P_in falls from 60 % to 5 % of its peak (between the barriers; inside the outer
  shell for two shells).

[exact1d.py](../../tools/kaggle/resonant-tunnelling/exact1d.py) writes `derived/exact-1d.json`: the exact 1D T(E) of the pair and
of one barrier, the packet average for `σ₀ = 3`, the resonance, the Tsu–Esaki I–V curve (`E_F = 1.0`, `k_BT = 0.05`) and the
GaAs/AlGaAs real units (`V₀ = 2` ↔ 0.30 eV, `a = 2.75 nm`). It is labelled as the check of the 3D runs: exact for walls by
separation of variables, the large-radius limit for discs.

## What the reader sees and sets

- **Fig. 15**: the plane z = 0 as a meshed height sheet (Fig. 14's look: paper at zero, wine crests, slate troughs, a thin ink
  mesh), lifted by Re ψ or |ψ|², with **one scale per run** (the run's largest |ψ|) times a chosen height (× 1, × 3, × 10;
  clipped at 1.25). The barriers are **static lit glass solids at their true place** (slabs, cylinders, spherical shells), with
  their cut through z = 0 in ink; they never move with the sheet. Press and drag to turn.
- **Fig. 15b**: `p(x, t)` along the flight, each curve divided by its total in the box; for walls the exact 1D twin dashed on top.
- **Fig. 15c**: the stored region probabilities against time, the total left in the box, and the lifetime fit.
- **Fig. 15d**: walls and discs: `T_far` of every 3D run against the exact 1D curves; shells: the lifetime against energy.
- **Fig. 15e** and the real-units panel: the diode from the exact 1D theory.

The page draws the stored half-plane and its mirror (exact: every shape and the packet are symmetric about the axis), and
interpolates every screen frame: `ψ(t_f + τ) = e^{−iEτ}[(1 − s)ψ_f + s e^{iEΔt}ψ_{f+1}]`; profiles and region probabilities
linearly. The worker does the heavy part (fetch, SHA-256, inflate, levels → ψ) off the main thread; at most six runs are cached.

## Measured

Grid against exact (walls, resonance `E = 0.735` unless said):

- 3D profile vs 1D twin: ≤ 1.8e-4 of the peak over all frames (separation holds on the grid).
- Twin T 0.186 vs exact packet average 0.196 (−5 %); off resonance +22 % at E = 0.4, −20 % at E = 1.2.
- Profile, twin vs exact: 3–4 % of the peak during the collision, up to ~10 % late.
- Lifetime: 15.1 (3D), 15.3 (twin) vs 14.2 exact: 6–8 % long.
- Side leak (3D only): τ = 15.1 walls, 9.0 discs R = 6, 3.2 R = 4, 2.1 R = 2; two shells τ = 28.

Browser (headless Chromium, software WebGL, 2026-11-13): no console errors at 1440 × 1000 and 390 × 844, no horizontal
overflow; all shapes, pair/single, radii, views and heights switch; SHA-256 matches. The page's own work per screen frame
(median / 95th percentile, device pixel ratio 2): sheet 0.5 / 1.0 ms, WebGL submit 0.9 / 4.3 ms, store and charts 0.5 / 1.9 ms
at 1440 px; 0.5 / 2.8, 0.9 / 4.9, 0.6 / 2.5 ms at 390 px. The measured screen-frame interval there (83–133 ms) is the software
rasteriser of the test container, which has no GPU. Read values: the sheet's vertex equals the stored value to 1e-9; the pixel
colour read back agrees; `T_far` recomputed from the stored curves equals the index. Lecture note: 323 formulas, 0 KaTeX errors,
equations (1)–(14).

## Lessons followed (notes/fig15/LESSONS.md)

Stored frames only, interpolated smoothly; one brightness scale per run; heavy work in a worker; barriers static and solid at
their true place (Fig. 14's open fault of an outline riding on the sheet is not copied); start state outside the barriers;
derived data in its own place; replaced runs not shipped and named; every GPU launch approved with a bill.

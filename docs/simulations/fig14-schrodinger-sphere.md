# Fig. 14 · A Wave Packet Meets a Sphere

| | |
|---|---|
| Page | [public/simulations/schrodinger-sphere.html](../../public/simulations/schrodinger-sphere.html) (English only, listed in `ENGLISH_ONLY` of [tools/i18n/build.py](../../tools/i18n/build.py)) |
| Data | [public/data/schrodinger-sphere/](../../public/data/schrodinger-sphere/): `generations.json`, and the generation of 2026-11-12 (`2026-11-12/index.json` and 405 run files `e{i}_v{j}_r{k}.bin`, amplitude only, 46.4 MB) |
| Shared page script | [public/scripts/kaggle-flow.js](../../public/scripts/kaggle-flow.js) and [public/styles/kaggle-flow.css](../../public/styles/kaggle-flow.css) ([kaggle-pipeline.md](../kaggle-pipeline.md)) |
| Live preview | [public/scripts/schrodinger-live-worker.js](../../public/scripts/schrodinger-live-worker.js) |
| Kaggle code | [tools/kaggle/schrodinger-sphere/](../../tools/kaggle/schrodinger-sphere/) ([kaggle.md](../kaggle.md)) |
| Thumbnail | [public/images/sims/schrodinger-sphere.webp](../../public/images/sims/schrodinger-sphere.webp) (WebP, 800 × 500 px) |
| Catalog entry | [public/scripts/catalog.js](../../public/scripts/catalog.js) (`id: 'schrodinger-sphere'`, `fig: 14`, `field: 'quantum'`, a new field "Quantum mechanics") |

A quantum particle, spread out as a Gaussian wave packet, flies along $x$ at a sphere of radius $R$ inside which the potential
energy is raised to $V_0$. **The figure shows the wave itself, $\mathrm{Re}\,\psi$, in three dimensions** (crests wine, troughs ink),
seen from an angle the reader turns by dragging. The page plays runs of the time-dependent Schrödinger equation in three dimensions, computed ahead of
time on Kaggle's GPUs and stored. **It computes nothing for a stored run.** Beyond the stored grid it computes a coarser live
preview in a Web Worker and says so on the figure.

## What the reader sees and sets

- **The figure**: $|\psi|$ in the plane $z = 0$ through the sphere's centre, 128 × 128 stored points stretched over a square
  canvas, paper (0) to wine (the first frame's peak). The sphere is a dashed circle, a 10 a bar gives the scale. The phase is not
  on the website (it doubled the data); it is in the Kaggle notebook's output.
- **Fig. 14b**: the probability behind the sphere ($x < -R$), inside its slab ($|x| \le R$), ahead ($x > R$) and lost into the
  absorbing border, against time, from the whole 3D $\psi$; a vertical line marks the frame shown.
- **Controls** (`KaggleFlow.slider`): packet energy $E$ (stops 0.5…4.5 computed, 5.0, 5.5, 6.0 not), barrier height $V_0$
  (0…8 computed, 10, 12 not), sphere radius $R$ (2…6 computed, 1, 7, 8 not); a time slider over the 48 stored frames; Play or
  Pause, From the start; a playback-speed bar.
- **Readouts**: the four probabilities, and the 1D rectangular barrier transmission for a slab of thickness $2R$ as a guide.
- **Where these numbers come from**: the Kaggle card, grid, steps and seconds of the run, its file name and whether its SHA-256
  matched `index.json`; or, beyond the grid, that the picture is a live preview and how far it has got.

## How it works

1. At start the page reads `DATA_BASE + 'generations.json'` (`DATA_BASE = '../data/schrodinger-sphere/'`, the one line to change
   if the store moves), then each generation's `index.json`, builds the three controls with the stored stops marked, and loads the
   run E = 2.5, V₀ = 3, R = 4.
2. `load(r)` fetches a run file, computes its SHA-256 and compares it with the index, reads the JSON header (parameters and the
   48 rows `[t, ∫|ψ|², P_behind, P_ahead, σ_y]`), and inflates the zlib body (`DecompressionStream('deflate')`) into 48 × 128 × 128
   amplitude levels; index `f·128² + x·128 + y`.
3. The clock (`Sim.clock`) advances the physical time at (run length / 9 s) × speed. The speed goes through
   `KaggleFlow.governor` (0.45 s) towards a goal: 1 − 0.8 × (the largest closeness of the three controls), lowered towards 0.06 over
   the last quarter of a stored run and to zero at the last frame a live preview has computed.
4. The frame shown is the stored frame at or before the time; nothing is interpolated.
5. On a stop that is not stored, `startLive` starts the Web Worker (the previous one is terminated) and frames are played as they
   arrive. The visitor's time is kept; until the preview reaches it, the last picture is held, dimmed, and the numbers are those of
   the held picture. When nothing is left to show and the speed has reached zero, `KaggleFlow.popup` fades in with the pipeline
   (this page, kaggle-bridge drawn dashed because `BRIDGE_URL` is null, Kaggle GPU, stored, back here) and the preview's progress.
6. A change of run or source cross-fades over 0.45 s from the last real picture.
7. Heading out of the stored band in a soft zone, the page calls `bridge.request(...)`; with the bridge not connected this answers
   "offline" at once.

## The store and the data panel

Every number shown is written into the page's `Sim.dataset` where it is read or computed: the settings (`E`, `V0`, `R`, `k0`), the
run (`stored`, `source`, `file`, `sha_ok`, `steps`, `wall`, `ready`, `live_done`), the frame (`t`, `frame`, `norm`, `behind`, `ahead`,
`inside`, `lost`, `sigma_y`, `sigma_free`, `T1D`), the picture (`xc`, `level`, 128 × 128) and the playback (`speed`, `edge`).
Check, three ways: `inside` = ∫|ψ|² − P_behind − P_ahead and `lost` = 1 − ∫|ψ|² recomputed from the stored curve;
`sigma_free` from σ₀√(1 + (t/2σ₀²)²); `k0` = √(2E); `T1D` from the barrier formula; `t` = frame × frame interval; and for `level`
the screen pixel read back and compared with the colour of the stored level (alpha checked first; up to 24 colour units apart
accepted, because the canvas smooths between stored points). Read values pins a stored point and shows its level, |ψ|/|ψ|peak and
|ψ|²/|ψ|²peak.

## The live preview

[schrodinger-live-worker.js](../../public/scripts/schrodinger-live-worker.js): the same Strang split step as on Kaggle in plain
JavaScript (radix-2 FFT along each axis), 64³ points, box side 64 a, shrunk for fast packets so the grid step stays below
π/(k₀ + 0.67) (the packet's fastest Fourier components, k₀ plus four momentum widths 1/(2σ₀), must stay below the grid's π/Δx),
sub steps of about 0.04 chosen so the 48 frames fall on the Kaggle frame times. Measured against the stored Kaggle runs at their
last frame, in Node 22 on one core of this workspace (12 November 2026):

| Run (E, V₀, R) | behind: live / Kaggle | ahead: live / Kaggle | seconds |
|---|---|---|---|
| 2, 3, 4 | 0.269 / 0.249 | 0.628 / 0.628 | 17 |
| 0.5, 8, 6 | 0.403 / 0.388 | 0.271 / 0.272 | 34 |
| 3, 3, 4 | 0.273 / 0.209 | 0.612 / 0.640 | 16 |
| 4.5, 4, 2 | 0.068 / 0.049 | 0.891 / 0.930 | 11 |
| 1, 0, 4 (free) | 0.000 / 0.000 | 0.986 / 0.985 | 24 |

At these last frames the preview agrees to 0.02–0.06 in probability; over all frames the largest difference measured is 0.076 (E = 0.5, V₀ = 8, R = 6, notes/fig14/), and the page says “within 0.08”.

## Measured on the page (headless Chromium, 12 November 2026, local server)

- Stored run E = 2.5, V₀ = 3, R = 4 loads, its SHA-256 matches, it plays at speed 1; no console errors at 1440 × 1000 and 390 × 844.
- Energy to 6.0 (not computed): within 2.5 s the speed has eased to 0.004 and the notice is shown, the picture held; the preview
  passes the visitor's time after about 7.5 s, the notice fades out, playback resumes at 0.2 (the uncomputed region's speed);
  all 48 frames after about 15 s.


## The 3D view (12 November 2026, evening)

Numa asked for the wave in three dimensions. The packet flies along $x$ through the centre of the sphere, and both are round
about that axis, so $\hat L_x$ commutes with the Hamiltonian and $\psi(x, y, z) = \psi(x, \rho)$, $\rho = \sqrt{y^2 + z^2}$: the
whole 3D wave is the stored cut through the axis spun about it. No new computation is needed.

- **Data** (generation 2026-11-12, `kind: axisym`, written by [to_site_axisym.py](../../tools/kaggle/schrodinger-sphere/to_site_axisym.py)
  from the Kaggle output of `numakoudsie/schrodinger-sphere-full-grid` version 1): per run the half-plane $y = \rho \ge 0$ of the
  stored cut, 128 × 64 points 0.5 a apart, $|\psi|$ and $\arg\psi$ levels, 48 frames; 405 files, 62.7 MB, largest 202 kB. This
  replaced the amplitude-only files of the afternoon (46.4 MB), which had no phase and so could not show crests.
- **Drawing** ([volume-view.js](../../public/scripts/volume-view.js)): each frame the page spins the half-plane into a box of
  128 × 96 × 96 voxels ($64\,a$ along $x$, $48\,a$ across), each voxel $\mathrm{Re}\,\psi = (q/255)\cos p$ at its $\rho$, linear between
  stored $\rho$; WebGL2 marches 192 samples along each pixel's ray, crests wine with opacity $1 - e^{-45(\mathrm{Re}\psi)^2\Delta s}$,
  troughs ink at 0.35 of that, and a glass shell for the sphere. `expected(x, y)` repeats the sum on the CPU from the same stored
  levels; the data panel's Check compares it with the pixel read back: equal in every test (four points, 12 November 2026).
- **Symmetry checks**: the two halves of every stored cut agree to 4 levels of 255 (`mirror_check` in `index.json`); a full 3D run in
  this workspace (E = 2, V₀ = 3, R = 4, $\mathrm{Re}\,\psi$ on 96 × 64 × 64 points,
  [notes/fig14/wave3d_test.py](../../notes/fig14/wave3d_test.py)) equals its spun cut to 2 of 127 levels (root mean square) and 24 of 127
  at worst, at points on the sphere's staircase surface.
- **Live preview** beyond the stored grid: the worker's own cut (64 × 64), spun the same way.
- **Read values** points at the strongest wave along the ray and reports the stored half-plane point at that $x$ and $\rho$.
- **Kaggle runs not used**: `numakoudsie/schrodinger-sphere-3d-generation` (the smooth 3D envelope, no crests) and
  `numakoudsie/schrodinger-sphere-3d-wave` (Re ψ in 3D, which the symmetry makes redundant; it could not be stopped from this
  session because the connector does not show a running session's id). Their outputs stay on Kaggle.

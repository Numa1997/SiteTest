# Fig. 14 · A Wave Packet Meets a Sphere

| | |
|---|---|
| Page | [public/simulations/schrodinger-sphere.html](../../public/simulations/schrodinger-sphere.html) (English only, listed in `ENGLISH_ONLY` of [tools/i18n/build.py](../../tools/i18n/build.py)) |
| Data | [public/data/schrodinger-sphere/](../../public/data/schrodinger-sphere/): `generations.json`, and the generation of 2026-11-12: `index.json` with 405 sphere cuts, `wave3d/` (true 3D, 81 runs), `flat/` (585 runs), `pillar/` (585 runs); see "Barrier shapes" below |
| 3D views | [public/scripts/wave3d-view.js](../../public/scripts/wave3d-view.js) (three.js in [public/vendor/three/](../../public/vendor/three/)) and [public/scripts/volume-view.js](../../public/scripts/volume-view.js) (fog) |
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
- **Kaggle runs**: `numakoudsie/schrodinger-sphere-3d-wave` version 1 (Re ψ on every point of the 3D box, 81 runs at R = 4) is
  now stored on the site and drawn (see below). `numakoudsie/schrodinger-sphere-3d-generation` (the smooth 3D envelope, 81 runs
  at R = 4) stays on Kaggle; it is kept for a later cross-check of the probabilities.

## Barrier shapes and the lit 3D views (12 November 2026, night)

The owner asked for every barrier shape that can be done (sphere, pillar, flat wall, coin, tube; finite, hard, well) and for all
three lit 3D views. Status: **sphere, pillar and flat wall are on the page** (wall thickness written $d$, as in (14)); **coin and tube** need GPU runs, which wait for the
owner's yes (their buttons are shown, disabled, marked "not computed yet").

| Shape | Potential | Why fewer dimensions are exact | Computed | Stored (on the site) |
|---|---|---|---|---|
| sphere | $V_0$ for $r < R$ | $[\hat L_x, \hat H] = 0$: $\psi(x, 
ho)$ | Kaggle T4 GPUs, 3D, 128³ | `2026-11-12/` cuts (405 runs), `2026-11-12/wave3d/` true 3D at R = 4 (81 runs, 97 MB) |
| pillar | $V_0$ for $x^2 + y^2 < R^2$, all $z$ | $[\hat p_z, \hat H] = 0$: $\psi = \varphi(x, y)\,g(z)$ | Kaggle CPU, 2D split-step, 128², `numakoudsie/schrodinger-pillar` | `2026-11-12/pillar/` (585 runs + `gz.bin`) |
| flat wall | $V_0$ for $\lvert x
vert < a/2$, all $y, z$ | $V = V(x)$: $\psi = \chi(x)\,g(y)\,g(z)$ | Kaggle CPU, 1D Crank–Nicolson, $\Delta x = 0.05$, `numakoudsie/schrodinger-flat-wall` | `2026-11-12/flat/` (585 runs, 51 MB) |

Grids: $E = 0.5 \ldots 4.5$ (9), and for pillar and wall $V_0 \in \{-4, -2, -1, 0, 0.5, 1, 1.5, 2, 3, 4, 6, 8\}$ and the **hard wall**
(stored as $V_0 = 10^6$, $\psi = 0$ inside), $R = 2 \ldots 6$ (pillar) or $a \in \{0.5, 1, 1.5, 2, 3\}$ (wall). The sphere has no
wells and no hard wall yet (GPU runs).

- **Solvers** ([tools/kaggle/schrodinger-shapes/](../../tools/kaggle/schrodinger-shapes/)): `flat.py` (CN with the fourth-order
  Laplacian; a hard wall removes the points $|x| \le a/2$ and closes the stencil with the odd mirror image), `pillar.py` (Strang split
  step on the sphere's grid; the absorbing border made mirror-symmetric, finite everywhere and the same per unit time for every
  $\Delta t$; a hard column sets $\psi = 0$ inside after every step). Notebooks `flat.ipynb`, `pillar.ipynb` (as run, version 1),
  written by `build_flat.py`, `build_pillar.py`; files are written by Kaggle in the website's format and copied byte for byte.
- **Checks** (printed in each notebook's log, numbers below measured):
  - flat wall: the plane-wave transmission $T(E)$ agrees with a direct solution of the four matching equations to $1.6\times10^{-15}$
    (`check_flat.py`, 120 × 11 × 5 cases); the free Gaussian $g$ solves the free equation exactly (SymPy residual 0, norm 1); in the
    510 runs that end with less than 0.002 inside the wall, the probability ahead equals the exact packet transmission
    $T_\text{packet} = \int|\phi(k)|^2 T(k)\,dk$ to 0.0045; in all 540 finite runs $|P_\text{ahead} - T_\text{packet}| \le P_\text{inside} + 0.005$
    (where they differ more, part of the wave is still inside at the end: $E$ near $V_0$, thick wall). The hard wall lets
    through at most $10^{-6}$; its norm is $1 - 2.9\times10^{-6}$ from the start, because the starting packet's tail inside the wall is cut.
  - pillar (measured on Kaggle, `numakoudsie/schrodinger-pillar` version 1, and here): at the end of the run $E = 2$, $R = 4$, halving
    $\Delta t$ from 0.0025 to 0.00125 changes the probability ahead by $3\times10^{-7}$ (finite $V_0 = 3$); for the hard column, from 0.0005
    to 0.00025, by $9\times10^{-5}$ ahead, $8\times10^{-4}$ behind and $10^{-3}$ in the norm (the projection is first order). The
    notebook's log also compares $\Delta t = 0.005$ and $0.001$, which end at another time (the frame interval 0.3175 is not a whole
    number of those steps), so those lines are not a convergence test; `check_pillar.py` now uses steps that divide the interval. An
    earlier local test that looked first order had the same end-time mismatch. The field is mirror-symmetric in $y$ to $10^{-12}$. The
    hard column loses about 4 % of the norm at the wall (the projection); in 2D the scattered wave also reaches the side border and is
    absorbed, up to 26 % in some runs; both show as "lost". All 585 files and `gz.bin` matched their SHA-256 (103 MB).
- **Lit views** ([wave3d-view.js](../../public/scripts/wave3d-view.js), [docs/scripts/wave3d-view.md](../scripts/wave3d-view.md),
  three.js 0.170.0 vendored in `public/vendor/three/`): **Sheets** (surfaces $\mathrm{Re}\,\psi = \pm c$, $c = 0.3$ of the frame's
  largest $|\mathrm{Re}\,\psi|$ in the box, by marching cubes), **Surface** (the plane $z = 0$ lifted by $\mathrm{Re}\,\psi$), **Cutaway**
  (sheets with the quarter $y > 0, z > 0$ removed), and **Fog** (the earlier volume view). All four draw the same 3D field on the
  box $-24 \le x < 24$, $|y|, |z| < 16$, $0.5\,a$ apart: the true 3D levels where stored (sphere, R = 4), else the stored cut spun
  about the axis (sphere, wall), else $\varphi(x, y)\,g(z)$ (pillar). The barrier is drawn as its solid: glass (finite), opaque (hard),
  tan (well).
- **Data panel**: new values `shape`, `view`, `T_packet`, `remax`, `iso`, `triangles`, and for true 3D runs the stored plane `rew`
  ($z = 0$, 96 × 64). The Check of a stored point in a lit view projects it (lifted by its $\mathrm{Re}\,\psi$ on the surface), reads the
  5 × 5 drawn pixels around it and compares their colour class (wine, slate, paper) with the sign of the stored $\mathrm{Re}\,\psi$;
  lighting changes brightness, not hue, so the class is what can be checked. Measured at 360, 390, 1024 and 1440 px: no horizontal
  overflow; the four test points pass after the on-sheet rule (a point within a fifth of $c$ of the level may show either sheet).


## Spherical waves (12 November 2026, late)

Asked for by the owner: a wave whose crests are spheres. Switch **Wave**: Packet, Spherical from the centre (`rout`), Spherical
closing in (`rin`). With $l = 0$, $u = r\psi$ solves the 1D equation on the half-line with $u(0) = 0$ (note equation 25; the identity
$\nabla^2\psi = (1/r)\,\partial_r^2(r\psi)$ checked with SymPy). [radial.py](../../tools/kaggle/schrodinger-shapes/radial.py) solves it on the
whole line with $u$ odd (Crank–Nicolson, fourth-order Laplacian, $\Delta r = 0.05$, $\sigma_0 = 2$).

- `rout`: shell from $r_0 = 6$ through a spherical shell wall at $r = 16$, thickness $d \in \{0.5, 1, 1.5, 2, 3\}$; the radial problem is
  the flat wall's, so $T_\text{packet}$ (24) with $\sigma_0 = 2$ is exact. `rin`: shell from $r_0 = 28$ closing in on a ball of radius
  $R = 2 \ldots 6$. Both: 9 energies × 13 heights (wells, hard wall). 1170 runs, Kaggle `numakoudsie/schrodinger-spherical-wave`
  (CPU), files `SPHR` in `2026-11-12/radial/` ($\psi(r)$ at 97 radii, levels of each frame's peak plus the list of peaks).
- Drawing (revised after the live check of 12 November, 23:40): the views draw $\mathrm{Re}\,(r\psi)$ (so shells far out, weakened by $1/r$, stay
  visible). Sheets and Cutaway are **exact spheres** (`Wave3D.setShells`) at the radii where the stored profile, interpolated by
  Catmull-Rom between its points 0.5 a apart, crosses $\pm c$, out to $r = 36$; Surface is a surface of revolution on a polar mesh
  (rings 0.08 a apart, 192 angles, `Wave3D.setRevolution`); Fog uses the 64³ cube, 0.75 a apart, emptied beyond $r = 23.5$ so it is round.
  The first version ran marching cubes on the 64³ cube, which aliased the thin shells into holes and needles. The room is larger for
  spherical waves (floor at $z = -38$, camera at 118 a). The data panel's field and pixel checks still use $\psi(|\mathbf r|)$ on the cube.
  The barrier is drawn as a glass sphere of radius 16 (the shell wall) or $R$ (the ball).
- A spherical wave is stored only with the round barrier at its centre: with a spherical wave chosen, the Pillar, Flat wall, Coin
  and Tube buttons are disabled and say "not computed yet" (they no longer switch the wave back to the packet).
- The hard pillar's source box now says that the projection removes about 4 % of the probability at the wall (0.3 % to 26 % across
  the grid, side border included).
- Not yet: spherical waves from a point beside the barrier, or meeting the pillar or the wall (true 3D, GPU).

## The meshed sheet, two sources, smoother sheets (13 November 2026)

Asked for by the owner with a reference picture (a smooth height surface with a wire mesh on it) and the words "in our design, in
our colours".

- **Mesh** is the default view and the first button under View; **Surface** is gone from the switch (Mesh replaces it; the code
  path of `setPlane` and `setRevolution` remains in the module, unused by the page). The sheet is the plane $z = 0$ lifted by
  $\mathrm{Re}\,\psi$, or by $|\psi|^2$ (buttons "Height Re ψ" and "Height |ψ|²"). House colours: slate `#55607a` at the lowest,
  card paper `#fbf6ee` at zero, wine `#a3303f` at the highest, mixed in sRGB (`Wave3D.meshColour`); mesh lines in ink `#1c1518`,
  48 squares per side; the barrier is the ink line where it cuts the plane (circle of radius $R$; two lines $x = \pm d/2$; circles
  $16 \pm d/2$). No floor, no box. Camera 31.5° above the plane, turned 45°.
- **Smoothness.** The stored points are 0.5 a apart (4.2 points per wavelength at $E = 4.5$). `packetSheet()` resamples the stored
  complex cut on $-24 \le x, y \le 24$ at 1/6 a (289 × 289 points, 12.5 points per wavelength at $E = 4.5$) with the periodic sinc
  of the 128-point box, $\sin(N t/2) / (N \tan(t/2))$, first along $x$, then along $y$ (the cut is even in $y$). For the pillar the
  stored $\varphi$ is multiplied by $g(0, t)$ first. `radialTable()` does the same for $u = r\psi$ along $r$ (192 points, $u$ odd,
  period 96 a) onto a table 0.01 a apart, and `radialSheet()` takes $\psi = u/r$ at every point of the sheet $-32 \le x, y \le 32$
  (385 × 385 points). The kernel is 1 at its own stored point and 0 at the others, so the sheet has the stored value at every stored
  point. Measured with [notes/fig14/band_test.cjs](../../notes/fig14/band_test.cjs) (Node, the page's own `bandMatrix`): plane waves
  that fit the box, wavelengths 12.8 to 1.07 a, are reproduced on the sheet's points to $4 \times 10^{-14}$; a Gaussian packet with
  $k_0 = 3$ ($E = 4.5$) to $4 \times 10^{-14}$; the weights at stored points are $(1, 0, 0, \dots)$ to $10^{-16}$. In the browser the
  sheet's vertex height over the scale equals the stored value to $7 \times 10^{-8}$ (32-bit rounding). The page says so in the source box: "The drawn sheet is a resampling of the stored grid".
- **Height scale**, new in each frame (`meshOf()`): the tallest point is a seventh of the sheet's width, or lower so that the
  steepest slope is 1.5. The first trial used a seventh of the width always: with wavelengths of 2 to 6 a on a sheet 48 or 64 a
  wide the crests stood as needles. The overlay says which rule holds ("height scaled: steepest slope 1.5").
- **Two sources** (`two`, under Wave): $\psi = \psi_1 + \psi_2$ (note equation 27), each the stored free spherical wave
  (`rout` with $V_0 = 0$, $d = 1$) about its own centre at $x = \pm s/2$; $s \in \{2, 4, 6, 8, 10, 12, 16\}$ a. No new run and no
  new file: the equation is linear. Drawn on the mesh only (the other views are disabled and say so); the barrier buttons are
  disabled and say why. The readouts show one source alone.
- **Sheets and Cutaway**: before marching cubes the field is resampled with the Lanczos kernel of three lobes to 1/6 a along $x$
  and 1/3 a across (`upsample()`); it returns the stored values at stored points. `marching()` now reads the eight corners straight
  from the array and leaves empty cubes at once, and writes into grown typed arrays (same triangles as before, measured: 34 184 on
  a test field before and after).
- **Data panel.** New group "The meshed sheet" (`hq`, `hmax`, `gmax`, `hscale`, `mesh_n`, `mesh_dx`, `ppw`, `sep`) and the stored
  radial profile (`rcr`, `ramp`, `rphase`, `rpeak`). The check in the Mesh view (`pixelCheckMesh`) has two parts: the sheet's own
  vertex at the stored point, divided by the scale, against the value from the stored levels; and the pixel's colour read back and
  inverted through the ramp (`Wave3D.meshV`, which uses the ratios g/r and r/b, nearly unchanged by white light), for the 5 × 5
  pixels around the vertex: the stored value over the frame's largest must lie within their span, widened by 0.12. A point hidden behind a crest (found with a ray from the eye) has its
  height checked and its colour not. Spherical waves are checked where the circle of the stored radius crosses the $x$ axis; two
  sources at $(s/2 + r_j, 0)$, where both distances are stored radii.

## The remaining 3D cases (13 November 2026, night)

One GPU launch for everything that needs true 3D (the owner's "all of them"). Kaggle notebook
`numakoudsie/schrodinger-shapes-3d`, version 1, private, 2 × T4: a one-line loader that fetches
[solver3d.py](../../tools/kaggle/schrodinger-shapes/solver3d.py) and [shapes3d_run.py](../../tools/kaggle/schrodinger-shapes/shapes3d_run.py)
at commit `a269119` (written by [build_shapes3d.py](../../tools/kaggle/schrodinger-shapes/build_shapes3d.py)). Grid as before:
128³ points, 0.5 a, Δt = 0.01, absorbing border, Strang split-step Fourier.

- **Runs (1458, none failed):** coin (disc radius R = 2 … 6, 1 a thick, axis along the flight) and tube (wall 1 a thick at
  ρ = R, endless along the flight), each 9 energies × 13 heights (wells −4, −2, −1; 0 … 8; hard) × 5 sizes = 585; the sphere's
  wells and hard ball, 9 × 4 × 5 = 180; a spherical wave from x = −12 a (shell r₀ = 6, σ₀ = 2, outgoing) onto a ball R = 4
  (`soff`), a flat wall d = 1 (`sslab`) and an upright pillar R = 4 (`spil`), each 9 × 4 heights (−2, 2, 6, hard) = 36.
- **Hard wall:** height 200 with a step four times shorter (0.0025): pure phase factors, no probability removed; the wave
  reaches $1/\sqrt{400} = 0.05$ a into it.
- **Stored:** per run a `SPHC` file, the half y ≥ 0 of the plane z = 0 (|ψ| and arg ψ in 8-bit levels of each frame's own
  peak; the peaks are in the header), 48 frames, and the curves from the whole ψ. Coin, tube, sphere and the side cases onto
  the ball and the wall are round about the x axis, so the page spins the cut as before. The pillar with a spherical wave is
  not: it also stores the true 3D wave, Re ψ on 96 × 64 × 64 points every second frame (`SPHW`, levels of each frame's peak,
  `wscale` in the header); its Sheets, Cutaway and Fog use that file.
- **Measured (timing.json):** 1458 of 1458 runs in 3993 s on two GPUs, 7315 GPU-seconds of runs (2.03 h), 2 926 032 steps;
  the estimate before launch was 2.08 h and 62 min. Lowest total probability at the end of any run: see index.json `norm_end`.
- **Files:** `public/data/schrodinger-sphere/2026-11-13/shapes3d/` (1495 files, 300 MB), every SHA-256 checked by
  [to_site_shapes3d.py](../../tools/kaggle/schrodinger-shapes/to_site_shapes3d.py); generations.json lists the generation.
- **Page:** Coin and Tube buttons under Barrier; "Spherical, from the side" under Wave, with Sphere, Pillar and Flat wall.
- **Progress:** the notebook prints one line per finished run (`1349/1458 coin …`); Kaggle's connector shows the log only
  after the session ends, but the notebook's page on kaggle.com shows it while it runs.

## The animation made smooth (13 November 2026, 03:00 UTC)

The owner: "The animation looks horrible ... glitches and slow." Causes found and what changed:

- **It stepped five times a second.** A run has 48 stored frames, and the page showed one, then the next. Now the meshed sheet
  moves on every screen frame. Between stored frames 0 and 1 the page draws
  $\psi(t_0 + \tau) = e^{-iE\tau}\,[(1 - s)\,\psi_0 + s\,e^{+iE\Delta t}\,\psi_1]$ with $s = \tau/\Delta t$: both frames are taken
  into the frame turning at the wave's energy $E$ (where $\psi$ changes only as slowly as its envelope moves, since an elastic run
  holds energies near $E$ only), blended, and turned back. At a stored frame the sheet is that frame exactly. The data panel's
  height check uses the same blend of the two frames' stored values (measured between frames: $2 \times 10^{-8}$).
- **Each new frame froze the page for 25 to 70 ms.** The fine sheets are now computed in a worker
  ([fig14-sheet-worker.js](../../public/scripts/fig14-sheet-worker.js)), four frames ahead of the playhead. What is left on the
  page per screen frame: 4 ms (packets, 289² points), 10 ms (spherical waves, 385² points), measured in headless Chromium.
- **The height scale jumped** from frame to frame (it was set from each frame's largest value). It is now blended between the
  two frames like the wave.
- **Playback slowed down** to a fifth near the edge of a slider's range, and crawled through the last quarter of every run.
  A stored run now plays at full speed, rests 1.2 s at its end and starts again. (The slow-down remains for the browser's live
  preview, which has to wait for its own frames.)
- **Sheets and Cutaway froze for 100 to 200 ms per frame.** They are now cut in a module worker
  ([fig14-iso-worker.js](../../public/scripts/fig14-iso-worker.js), marching cubes moved to
  [marching.js](../../public/scripts/marching.js)); the newest frame asked for is cut next, frames in between are skipped.
  Median gap between screen frames while playing: 17 ms.
- **The sphere's sheets were torn late in a run.** The true 3D files hold Re ψ in 127 levels of the first frame's peak; once the
  wave has spread, a crest is a handful of levels. The sphere's sheets are now spun from the cut (255 levels of |ψ| and its
  phase), as for the other radii. The true 3D files of 12 November stay stored and listed; the page no longer draws from them.
- **Wrong start waves in the 3D generation of 13 November (version 1).** (a) Spherical wave from the side: the source stood at
  x = −12 with r₀ = 6, so the shell began inside the barrier. (b) Hard walls: the tail of the start wave inside the wall was
  left there and stayed (levels up to 216 of 255 inside the hard ball in the side case). Fixed in
  [solver3d.py](../../tools/kaggle/schrodinger-shapes/solver3d.py): source at x = −17, r₀ = 5 (amplitude 0.018 of the peak at a
  barrier of radius 4); the start wave is set to zero inside a hard wall and normalised again. The 243 affected runs (108
  side-wave runs, 135 hard runs of sphere, coin and tube) are computed again on Kaggle's CPU, four notebooks
  `numakoudsie/schrodinger-shapes-3d-v2-a … d` (no GPU hours). Until they are on the site the page does not offer the wave
  from the side, and says under a hard-wall run of version 1 what is wrong with it.
- The live preview in the browser is drawn as fog also when Mesh is chosen (it has no fine sheet).

## Version 2 of the 243 runs is on the site (13 November 2026, 03:35 UTC)

The owner asked for the GPU instead of the CPU. `numakoudsie/schrodinger-shapes-3d`, version 2 (2 × T4, loader with
`JOBSEL = 'hard_and_shells'`, code at commit `94d1281`): 243 of 243 runs, none failed, 1192 s on the clock, 2239 GPU-seconds of
runs (0.62 h; estimate before launch 0.76 h and 23 min), 1 068 639 steps. Merged by
[merge_v2.py](../../tools/kaggle/schrodinger-shapes/merge_v2.py): every SHA-256 checked, the 243 files and index entries
replaced (marked `v: 2`), `shell` set to the new source (x = −17, r₀ = 5, travel 24). The four CPU notebooks `…-v2-a` to `-d`
started earlier compute the same runs; their output is not used (the connector could not cancel them: its cancel call needs a
session number that neither its status nor its info call returns).

Measured on the stored files of version 2 (levels × the frame's peak, in units of the first frame's peak in the plane z = 0):

| | start wave inside the barrier | hard wall: largest value inside during the run | more than one grid point inside |
|---|---|---|---|
| sphere, hard | 0 | 0.043 | 0.009 |
| coin, hard | 0 | 0.030 | 0 |
| tube, hard | 0 | 0.044 | 0 |
| side wave onto ball / pillar / wall, hard | 0 | 0.003 / 0.003 / 0.001 | 0.0006 / 0.0006 / 0 |
| side wave, finite heights | below the lowest stored level (3 of 255) | | |

In version 1 the same numbers were up to 0.85 (216 of 255 levels deep inside the hard ball in the side case). The few per cent
left at the first grid point inside a hard wall are the wave's reach into a wall of height 200 (0.05 a) seen on a grid of 0.5 a.
With `shell.src_x = -17` in the index the page offers "Spherical, from the side" again, and runs marked `v: 2` no longer carry
the note about the start wave.


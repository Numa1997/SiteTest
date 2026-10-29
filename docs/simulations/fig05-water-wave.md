# Fig. 5 · Circular Water Waves

| | |
|---|---|
| Page | [public/simulations/water-wave.html](../../public/simulations/water-wave.html) (893 lines, 164 715 bytes) |
| Walkthrough | [public/scripts/walk/water.js](../../public/scripts/walk/water.js) (216 lines, 12 steps, key `water`) |
| Thumbnail | [public/images/sims/water-wave.webp](../../public/images/sims/water-wave.webp) (800 × 500 px, 15.0 kB) |
| Catalog entry | [public/scripts/catalog.js#L115](../../public/scripts/catalog.js#L115) (lines 115–131, `id: 'water-wave'`, `fig: 5`) |

The reader sees a cross-section of deep water under a travelling wave: a burgundy surface line, a rose tint under it, and rows
of dots, one row per depth layer, each dot a parcel of water running round its own circle
([water-wave.html:44-52](../../public/simulations/water-wave.html#L44-L52)). The middle column of parcels is drawn larger and
in burgundy, with a line from each orbit centre to its parcel, so the reader can follow one vertical line of water from the
surface down ([:758-770](../../public/simulations/water-wave.html#L758-L770)). The side panel sets the amplitude, wavelength
and frequency, the number of parcels per layer and of layers, and two switches: the orbits and the deep-water law
$\omega^2 = gk$ ([:54-105](../../public/simulations/water-wave.html#L54-L105)). Four readouts give the phase speed, the period,
the steepness and the size of the deepest orbit ([:92-97](../../public/simulations/water-wave.html#L92-L97)). Below the figure
come the lecture note and the walkthrough "From symbols to code".

In this page, "px" without a qualifier means a pixel of the drawn field, with 100 px = 1 m
([:572](../../public/simulations/water-wave.html#L572)); "css px" means a screen pixel of the canvas. Line links of the form
`:NNN` point into `water-wave.html`.

## The physics in one picture

**Everyday picture.** A gull resting on the swell rises, slides forward, sinks into the trough, slides back, and ends almost
where it started. A diver a few metres down hardly feels short chop but still feels a long swell. After a distant storm the
long waves arrive first. The lecture note opens with these three facts (Section 01,
[:132-138](../../public/simulations/water-wave.html#L132-L138)).

**Model.** Water is incompressible, has no friction and does not spin; the wave is small ($ak \ll 1$, linear or Airy theory);
the water is deep; gravity and pressure are the only forces (Section 02,
[:144-151](../../public/simulations/water-wave.html#L144-L151)). The note derives Laplace's equation for the velocity potential
(Section 03), the three boundary conditions (Section 04), the dispersion relation $\omega^2 = gk$ (Section 05), the circular
orbits that shrink as $e^{kz}$ (Section 06) and the Stokes drift that linear theory hides (Section 07). The page itself
evaluates only the end results, in closed form.

**What the code evaluates.** Symbols and units:

- $\lambda$: wavelength, px (slider `lambda`); $\lambda/100$ in m.
- $k = 2\pi/\lambda$: wave number, rad/px ([:637](../../public/simulations/water-wave.html#L637)); $k_\mathrm{m} = 100\,k$, rad/m.
- $g = 9.81$ m/s² ([:572](../../public/simulations/water-wave.html#L572)).
- $f$: frequency, Hz. With the dispersion switch on, from $\omega^2 = g k_\mathrm{m}$; with it off, the slider value
  ([:639-641](../../public/simulations/water-wave.html#L639-L641)):

$$f = \frac{\sqrt{g\,k_\mathrm{m}}}{2\pi}, \qquad \omega = 2\pi f, \qquad T = \frac{1}{f}, \qquad c = \frac{f\,\lambda}{100}, \qquad c_g = \frac{c}{2}$$

  with $\omega$ in rad/s, $T$ in s, the phase speed $c$ and the group speed $c_g$ in m/s
  ([:655](../../public/simulations/water-wave.html#L655), [:662-665](../../public/simulations/water-wave.html#L662-L665)).
- $A$: the amplitude slider, px. The amplitude used is capped so that the surface never folds over
  ([:642](../../public/simulations/water-wave.html#L642)):

$$a = \min\left(A,\ \frac{0.9}{k}\right), \qquad ak \le 0.9 .$$

- Layer $j = 0, 1, \dots, L-1$ sits at rest depth $z_0 = -56\,j$ px (0.56 m apart); its orbit radius is
  ([:737](../../public/simulations/water-wave.html#L737))

$$r_j = a\,e^{k z_0} .$$

- Parcel $i = 0, \dots, N-1$ of a layer has its orbit centre at $X_0 = 30 + i\,(W - 60)/(N - 1)$ px, where $W$ is the field
  width, 800 px, or 400 px on a canvas narrower than 560 css px ([:681](../../public/simulations/water-wave.html#L681),
  [:742](../../public/simulations/water-wave.html#L742)).
- With the accumulated phase $\omega t$ (rad), each parcel's phase $\theta$ (rad), displacement $(\xi, \zeta)$ (px, $\zeta$
  upwards) and velocity $(u, w)$ (px/s) are ([:743-746](../../public/simulations/water-wave.html#L743-L746))

$$\theta = k X_0 - \omega t, \qquad \xi = -r\sin\theta, \qquad \zeta = r\cos\theta, \qquad u = r\omega\cos\theta, \qquad w = r\omega\sin\theta .$$

  These are equations (17) and (16) of the note, evaluated at the rest position. The velocity is the time derivative of the
  displacement.
- The surface is the curve of all surface parcels, a trochoid, traced for $X = -60, -57, \dots, W + 60$ px
  ([:693-695](../../public/simulations/water-wave.html#L693-L695)):

$$x = X - a\sin(kX - \omega t), \qquad \eta = a\cos(kX - \omega t) .$$

- Stored as theory, never drawn: the surface Stokes drift $U_S = \omega\,k_\mathrm{m}\,a_\mathrm{m}^2$ in m/s, with
  $a_\mathrm{m} = a/100$ ([:666](../../public/simulations/water-wave.html#L666)), and the size of the deepest orbit relative to
  $a$, $e^{-k \cdot 56\,(L-1)}$ ([:660](../../public/simulations/water-wave.html#L660)).

At the defaults ($\lambda$ = 260 px, $A$ = 24 px, dispersion on), measured in headless Chromium: $f$ = 0.7749 Hz,
$k_\mathrm{m}$ = 2.4166 rad/m, $c$ = 2.0148 m/s, $T$ = 1.2905 s, $ak$ = 0.580, $U_S$ = 0.678 m/s, orbit radii 24, 6.20, 1.60,
0.414 and 0.107 px for the five layers.

## How the code computes it

**State.** One inline script, an immediately invoked function ([:568-889](../../public/simulations/water-wave.html#L568-L889)).
Constants `WORLD_W = 800`, `DZ = 56` (px between layers), `PX_PER_M = 100`, `G = 9.81`
([:572](../../public/simulations/water-wave.html#L572)); `WORLD_W` is reassigned every frame
([:681](../../public/simulations/water-wave.html#L681)). The canvas wrapper `box` from `Sim.canvas2d`
([:575](../../public/simulations/water-wave.html#L575), [sim.js:32-46](../../public/scripts/sim.js#L32-L46)) carries the size
in css px (`box.w`, `box.h`) and the device pixel ratio (capped at 2). The only time-dependent state is `omegaT` (rad), with
`fps` and `frames` for the data panel ([:577](../../public/simulations/water-wave.html#L577)). The five sliders are wrapped by
`Sim.slider` ([:631-635](../../public/simulations/water-wave.html#L631-L635), [sim.js:152-173](../../public/scripts/sim.js#L152-L173)).
All per-parcel numbers live in the data store, in typed arrays that `draw()` fills.

**Numerical method.** None in the sense of an integrator: positions and velocities are closed-form expressions, evaluated afresh
every frame. Only the phase is accumulated, `omegaT += 2 * Math.PI * f() * dt`
([:794](../../public/simulations/water-wave.html#L794)). Adding $2\pi f\,\Delta t$ frame by frame, rather than computing
$\omega t$ from a clock, keeps the motion continuous when $f$ changes (note Section 08,
[:512](../../public/simulations/water-wave.html#L512)). `f()` returns the exact deep-water frequency, not the slider value
rounded to 0.01 Hz ([:638-641](../../public/simulations/water-wave.html#L638-L641)), so $c$ and the motion agree to machine
precision. Nothing is integrated, so no error builds up; the clock caps $\Delta t$ at 0.05 s and gives $\Delta t = 0$ while
paused ([sim.js:179-181](../../public/scripts/sim.js#L179-L181)).

**The frame loop, in order.** `Sim.clock` calls its callback on every animation frame, playing or paused
([sim.js:176-186](../../public/scripts/sim.js#L176-L186)).

1. Advance the phase, update the frame-rate average, write `omegaT`, `periods`, `t`, `dt`, `fps`, `frames`, `playing` into the
   store ([:794-796](../../public/simulations/water-wave.html#L794-L796)).
2. `draw()` ([:680-777](../../public/simulations/water-wave.html#L680-L777)):
   1. Layout: field width `WORLD_W` (800, or 400 if `box.w < 560`), scale `s = w / WORLD_W`, `kk = k()`, `A = a()`, calm level
      `ys = max(A s + 34, 0.28 h)`, `om = 2π f()` ([:681-684](../../public/simulations/water-wave.html#L681-L684)).
   2. Resize the dimensions `z` and `p` to the layer and parcel counts and fetch the arrays with `ds.alloc`
      ([:685-687](../../public/simulations/water-wave.html#L685-L687)); write the layout scalars
      ([:688](../../public/simulations/water-wave.html#L688)). Clear the canvas ([:689](../../public/simulations/water-wave.html#L689)).
   3. Water body: a path through the surface points every 3 px from −60 to `WORLD_W + 60`, closed along the canvas bottom,
      filled with a rose gradient from 36 % opacity at crest height to 5 % at the bottom
      ([:691-707](../../public/simulations/water-wave.html#L691-L707)).
   4. Surface line: the same points again, stroked in the accent colour, 2.2 css px wide
      ([:709-718](../../public/simulations/water-wave.html#L709-L718)).
   5. Calm level: a dashed line at `ys` ([:720-728](../../public/simulations/water-wave.html#L720-L728)).
   6. Layers: for each `j`, compute `z0`, `r`, the screen height `cy` of the orbit centres, and store `r_z`, `depth`, `cy_px`
      ([:737-738](../../public/simulations/water-wave.html#L737-L738)); record whether `cy ≤ h - 8` and count only visible rows
      ([:739](../../public/simulations/water-wave.html#L739)). For every parcel `i`, including hidden layers: `X0`, `th`, screen position `px`, `py`
      ([:742-744](../../public/simulations/water-wave.html#L742-L744)); store eight arrays at the flat index `q = j * N + i`
      ([:745-746](../../public/simulations/water-wave.html#L745-L746)); skip drawing for hidden parcels, otherwise draw the orbit circle if the switch is on and
      `r * s > 1.2` css px ([:749-757](../../public/simulations/water-wave.html#L749-L757)), the radius line of the followed
      parcel ([:758-765](../../public/simulations/water-wave.html#L758-L765)) and the dot: radius 3.8 (surface) or 3.1 css px,
      6 or 5 for the followed column ([:766-770](../../public/simulations/water-wave.html#L766-L770)). Layers below the surface
      get a depth label "z = −0.56 m" ([:772](../../public/simulations/water-wave.html#L772),
      `depthLabel` at [:671-679](../../public/simulations/water-wave.html#L671-L679)).
   7. Store `layers_drawn` and mark the arrays as changed with `ds.touch`
      ([:774-776](../../public/simulations/water-wave.html#L774-L776)).

Outside the frame loop, a control change calls `readouts()` ([:654-668](../../public/simulations/water-wave.html#L654-L668)),
which rewrites the side-panel readouts and the caption speed, and writes all derived scalars ($k$, $c$, $T$, $a$, $ak$,
$U_S$, …) into the store. Moving the wavelength or flipping the dispersion switch goes through `couple()`
([:644-651](../../public/simulations/water-wave.html#L644-L651)), which, with the switch on, sets the frequency slider to the
deep-water value and disables it.

**Precomputation and caching.** None. Every frame recomputes every parcel: at the defaults 18 × 5 = 90 parcels, plus 307
surface points that are evaluated twice, once for the fill and once for the stroke
([:693](../../public/simulations/water-wave.html#L693), [:710](../../public/simulations/water-wave.html#L710)). The store's
typed arrays are reused while their sizes stay the same ([dataset.js:64-70](../../public/scripts/dataset.js#L64-L70)), so a frame
allocates nothing unless a slider changed a count. The frame runs even while paused, with $\Delta t = 0$, so slider changes show
at once.

## Function map

Line numbers link into `water-wave.html`.

| Function | Lines | What it does |
|---|---|---|
| (sliders' `format` callbacks) | [631-635](../../public/simulations/water-wave.html#L631-L635) | Text in each slider's `<output>`: "24 px", "0.77 Hz", "18". |
| `k()` | [637](../../public/simulations/water-wave.html#L637) | Wave number $2\pi/\lambda$, rad/px, from the wavelength slider. |
| `f()` | [639-641](../../public/simulations/water-wave.html#L639-L641) | Frequency: $\sqrt{g\,k\,100}/2\pi$ with dispersion on, the slider value with it off. |
| `a()` | [642](../../public/simulations/water-wave.html#L642) | Amplitude used, $\min(A, 0.9/k)$. |
| `couple()` | [644-651](../../public/simulations/water-wave.html#L644-L651) | With dispersion on, sets the frequency slider to the deep-water value; enables or disables it; calls `readouts()`. Bound to the dispersion switch at [652](../../public/simulations/water-wave.html#L652). |
| `readouts()` | [654-668](../../public/simulations/water-wave.html#L654-L668) | Writes the four readouts and the caption speed; writes every parameter and derived scalar into the store. |
| `depthLabel(rest, x, y)` | [671-679](../../public/simulations/water-wave.html#L671-L679) | Draws "z = −0.56 m" with `Sim.tex` on a pale box. |
| `draw()` | [680-777](../../public/simulations/water-wave.html#L680-L777) | One frame: layout, water fill, surface, calm level, all layers and parcels; writes the arrays. |
| `Sim.live` | [780-792](../../public/simulations/water-wave.html#L780-L792) | Live values for the walkthrough, read from the store. |
| clock callback `(dt, t)` | [793-798](../../public/simulations/water-wave.html#L793-L798) | Advances `omegaT`, writes the time scalars, calls `draw()`. `Sim.playButton` binds the Pause button at [799](../../public/simulations/water-wave.html#L799). |
| `sliderCheck(input, label)` | [802](../../public/simulations/water-wave.html#L802) | Check entry for a value that comes straight from a slider. |
| `at(q)` | [803](../../public/simulations/water-wave.html#L803) | Stored screen position of parcel `q`. |
| `parcelPixel(q)` | [804-810](../../public/simulations/water-wave.html#L804-L810) | Read-back: the canvas pixel at the parcel's stored centre; passes if alpha > 0 and luminance < 130. |
| `qInputs(q)` | [811](../../public/simulations/water-wave.html#L811) | The inputs (layer, column, r, θ) shown in a parcel check. |
| `Sim.data.playing` | [814](../../public/simulations/water-wave.html#L814) | Clock state for the panel. |
| `Sim.data.rowLabel.z` | [822](../../public/simulations/water-wave.html#L822) | Row names "z0", "z1", … in array tables. |
| `Sim.data.colour.*` | [823](../../public/simulations/water-wave.html#L823) | Cell shading of `xi`, `zeta` (scale $a$) and `u`, `w` (scale $a\omega$) with `Sim.colourMap`. |
| `Sim.data.probe(x, y)` | [824-828](../../public/simulations/water-wave.html#L824-L828) | Nearest drawn parcel within 14 css px of a point, as `{ q }`. |
| `Sim.data.inspect(ref)` | [829-833](../../public/simulations/water-wave.html#L829-L833) | Title, position and eight rows ($X_0$, depth, $r$, θ, ξ, ζ, u, w) of a pinned parcel. |
| `Sim.data.locate(name, idx)` | [834-840](../../public/simulations/water-wave.html#L834-L840) | Where an array cell is drawn: the parcel itself, or the followed parcel of a layer. |
| `Sim.data.check.*` | [841-878](../../public/simulations/water-wave.html#L841-L878) | For 36 variables: the formula, its stored inputs and the recomputed value. |
| `Sim.data.drawn` | [879](../../public/simulations/water-wave.html#L879) | `px`, `py`, `xi`, `zeta` are read back with `parcelPixel`. |
| `Sim.data.round.label`, `.length`, `.point` | [881-881](../../public/simulations/water-wave.html#L881-L881) | One round = one period $T$; the followed surface parcel is recorded. |
| `Sim.data.play` | [882](../../public/simulations/water-wave.html#L882) | Starts the clock before a round. |
| start-up | [885-887](../../public/simulations/water-wave.html#L885-L887) | `couple()`, `draw()`, and a resize observer that refits the canvas. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Pause / Play | `play` | playing at load, unless the reader prefers reduced motion ([sim.js:177](../../public/scripts/sim.js#L177)) | `clk.toggle` via `Sim.playButton` ([:799](../../public/simulations/water-wave.html#L799)); paused frames get $\Delta t = 0$. |
| Show orbits | `orbits` | on ([:60](../../public/simulations/water-wave.html#L60)) | Orbit circles drawn when on and $r s > 1.2$ ([:749](../../public/simulations/water-wave.html#L749)); stored as `orbits`. |
| Deep-water dispersion ω² = gk | `disp` | on ([:61](../../public/simulations/water-wave.html#L61)) | `f()` uses the dispersion relation; `couple()` sets and disables the frequency slider ([:644-652](../../public/simulations/water-wave.html#L644-L652)). |
| Amplitude a (orbit radius) | `amp` | 5–50 px, step 1, default 24 ([:68](../../public/simulations/water-wave.html#L68)) | $A$; $a = \min(A, 0.9/k)$; calls `readouts()`. |
| Wavelength λ | `lambda` | 120–400 px, step 5, default 260 ([:72](../../public/simulations/water-wave.html#L72)) | $k$; calls `couple()`. |
| Frequency f | `freq` | 0.1–1.5 Hz, step 0.01, default 0.5 ([:76](../../public/simulations/water-wave.html#L76)); set to 0.77 at load by `couple()` | Used only with dispersion off; calls `readouts()`. |
| Particles per layer | `count` | 8–36, step 1, default 18 ([:84](../../public/simulations/water-wave.html#L84)) | $N$, read by `draw()` every frame; no callback. |
| Depth layers | `layers` | 1–5, step 1, default 5 ([:88](../../public/simulations/water-wave.html#L88)) | $L$ in `draw()`; the deepest-orbit readout; calls `readouts()`. |
| Read values | added by datalog.js into the caption | off | Pins a parcel; see [datalog.md](../scripts/datalog.md). |

## What the page writes into the data store

The store is created at [:580](../../public/simulations/water-wave.html#L580) with
`Sim.dataset({ title: 'Water waves', attrs: { figure: 5, page, WORLD_W, DZ, PX_PER_M, g, length_unit } })`. How the store works
is in [dataset.md](../scripts/dataset.md). Every variable carries `symbol`, `units`, `long_name`, `computed_in` and a `formula`
or `source` string for the panel.

**Dimensions.** `p` (parcels per layer) and `z` (layers), declared with length 0
([:607](../../public/simulations/water-wave.html#L607), [:609](../../public/simulations/water-wave.html#L609)) and resized every
frame to $N$ and $L$ ([:685](../../public/simulations/water-wave.html#L685)).

**Arrays** (Float64Array, written every frame in `draw()`):

| Name | Dims | Declared | Written | Meaning |
|---|---|---|---|---|
| `X0` (coordinate) | p | [608](../../public/simulations/water-wave.html#L608) | [746](../../public/simulations/water-wave.html#L746) | orbit centre of each column, px |
| `depth` (coordinate) | z | [610](../../public/simulations/water-wave.html#L610) | [738](../../public/simulations/water-wave.html#L738) | depth of each layer, m |
| `r_z` | z | [611](../../public/simulations/water-wave.html#L611) | [738](../../public/simulations/water-wave.html#L738) | orbit radius of each layer, px |
| `cy_px` | z | [612](../../public/simulations/water-wave.html#L612) | [738](../../public/simulations/water-wave.html#L738) | screen height of the layer's orbit centres, css px |
| `theta`, `xi`, `zeta`, `u`, `w` | z × p | [613-617](../../public/simulations/water-wave.html#L613-L617) | [746](../../public/simulations/water-wave.html#L746) | phase (rad), displacement (px), velocity (px/s) |
| `px`, `py` | z × p | [618-619](../../public/simulations/water-wave.html#L618-L619) | [746](../../public/simulations/water-wave.html#L746) | screen position of each parcel, css px |

Two-dimensional arrays are row-major, one row per layer: parcel $i$ of layer $j$ is at index $q = jN + i$
([:745](../../public/simulations/water-wave.html#L745)). `probe`, `inspect`, `locate` and `parcelPixel` all rely on this.

**Scalars.**

| Written in | Line | Variables |
|---|---|---|
| `readouts()` (on control change) | [663-667](../../public/simulations/water-wave.html#L663-L667) | `amp`, `lambda`, `lambda_m`, `f`, `dispersion`, `N`, `layers`, `k`, `k_m`, `omega`, `T`, `c`, `c_deep`, `cg`, `a`, `cap`, `ak`, `stokes`, `deep`, `r1`, `z_deep_px` |
| `draw()` (every frame) | [688](../../public/simulations/water-wave.html#L688), [774](../../public/simulations/water-wave.html#L774) | `N`, `layers`, `world_w`, `s_px`, `ys`, `box_w`, `box_h`, `orbits`, `follow`; `layers_drawn` |
| clock callback (every frame) | [796](../../public/simulations/water-wave.html#L796) | `omegaT`, `periods`, `t`, `dt`, `fps`, `frames`, `playing` |

Their declarations are at [:581-606](../../public/simulations/water-wave.html#L581-L606) and
[:620-629](../../public/simulations/water-wave.html#L620-L629). The scalars of the first row do not depend on time, so they are
written only when a control changes; the panel groups them as "Physical parameters" and "Derived physics"
([:814-815](../../public/simulations/water-wave.html#L814-L815)).

**One round** (`Sim.data.round`, [:881-881](../../public/simulations/water-wave.html#L881-L881)): one period, length
`ds.get('T')` seconds of the time variable `t`, labelled "one period, T = … s". The chart column is `omegaT`, and the point
followed is the burgundy surface parcel, `{ q: follow }`. The panel samples every numeric scalar at most 600 times in the
round ([datalog.js:1052](../../public/scripts/datalog.js#L1052), [datalog.js:1081](../../public/scripts/datalog.js#L1081)).

**The panel hooks.** `Sim.data` ([:812-884](../../public/simulations/water-wave.html#L812-L884)) also sets `kicker: 'Fig. 5 ·
data'` and `file: 'fig5-water-waves'` (the base name of the saved archive), the five groups, the `check` and `drawn` tests,
and the `about` paragraph. The contract is at [datalog.js:9-49](../../public/scripts/datalog.js#L9-L49).

**`Sim.live()`** ([:780-792](../../public/simulations/water-wave.html#L780-L792)) reads only the store and returns formatted
strings for the walkthrough's "Now" column: `lam`, `k`, `km`, `f`, `c`, `T`, `cg`; for the followed surface parcel `X0`, `th`
(θ reduced to (−π, π] with `atan2`), `px` (ξ), `pz` and `eta` (both ζ); `r` (surface radius), `r1`, `z0` (depth of the
deepest layer, from `z_deep_px`), `deep`; `a`, `A`, `ak`; `wt` (ωt), `s`, `ys`. The walkthrough polls it every 200 ms
([sim.js:391-403](../../public/scripts/sim.js#L391-L403)).

**Three-way check, measured.** Paused at 1440 × 900 (canvas 770 × 366 css px), for the followed surface parcel: stored
`xi` = 23.985449954109615 px and the value recomputed by `check.xi` from the stored `r_z` and `theta` are identical; the same
holds for `zeta`, `u`, `w`, `theta`, `px` and `py`. The pixel read back at the stored centre (387.1, 103.3) css px is
rgb(122, 31, 43), the burgundy of the followed parcel, at full alpha.

## Page structure

**Head** ([:3-15](../../public/simulations/water-wave.html#L3-L15)): title, description, theme colour; the security policy and referrer rule ([build-and-deploy.md](../build-and-deploy.md#security));
stylesheets `../styles/sim.css` (which imports the self-hosted fonts, KaTeX's CSS and `paper.css`), `../styles/data.css`,
`../styles/fold.css`; an inline SVG favicon. No page-specific `<style>`. See [styles.md](../styles.md).

**Body.**

- Top bar: one span holding the Phyein Usul logo (a link to `../index.html` with `../images/phyein-usul-mark.svg`, 87 × 48)
  and the link back to the catalog, "← All simulations" ([:18](../../public/simulations/water-wave.html#L18)), then the
  hand-written Fig. 1–11 links, Fig. 5 marked `aria-current` ([:17-33](../../public/simulations/water-wave.html#L17-L33)).
- Heading: "Fig. 5 · fluid dynamics · particle motion", the h1 and the lede ([:37-41](../../public/simulations/water-wave.html#L37-L41)).
- The figure: `#stage` with aspect ratio 16 / 7.6, or 1 / 0.95 below 900 px viewport width
  ([:45](../../public/simulations/water-wave.html#L45), [sim.css:215](../../public/styles/sim.css#L215)), the canvas `#water`, and
  the caption with the speed `#cap-c` ([:48-51](../../public/simulations/water-wave.html#L48-L51)). datalog.js adds the
  Read values switch to this caption and the reading strip under the figure
  ([datalog.js:874-897](../../public/scripts/datalog.js#L874-L897)).
- The control panel: Run, Wave and Water groups, readouts, legend ([:54-105](../../public/simulations/water-wave.html#L54-L105)).
- The lecture note `<article class="paper" id="paper">` ([:108-555](../../public/simulations/water-wave.html#L108-L555)), "Deep-water
  waves: the sea moves in circles", with an abstract and a contents list. Ten sections, 23 numbered equations (1)–(23), four
  inline SVG figures, one result box, two exercises and one table:

| § | id | Title | Line | Contents |
|---|---|---|---|---|
| 01 | `p-gull` | A gull on the swell | [132](../../public/simulations/water-wave.html#L132) | the everyday picture |
| 02 | `p-model` | The model | [140](../../public/simulations/water-wave.html#L140) | assumptions; Figure 1, the model ([152-245](../../public/simulations/water-wave.html#L152-L245)) |
| 03 | `p-laplace` | Potential flow: Laplace's equation | [249](../../public/simulations/water-wave.html#L249) | eqs. (1)–(4) |
| 04 | `p-edges` | Three conditions at the edges ★ | [263](../../public/simulations/water-wave.html#L263) | eqs. (5)–(9) |
| 05 | `p-dispersion` | Gravity sets the pace: the dispersion relation | [283](../../public/simulations/water-wave.html#L283) | eqs. (10)–(15); box ω² = gk ([295](../../public/simulations/water-wave.html#L295)); speed table ([308](../../public/simulations/water-wave.html#L308)); Figure 2, phase and group speed ([319-365](../../public/simulations/water-wave.html#L319-L365)); Exercise 5.1 ([367](../../public/simulations/water-wave.html#L367)) |
| 06 | `p-orbits` | Every parcel runs in a circle | [373](../../public/simulations/water-wave.html#L373) | eqs. (16)–(19); Figure 3, radius against depth ([385-434](../../public/simulations/water-wave.html#L385-L434)); Exercise 6.1 ([436](../../public/simulations/water-wave.html#L436)) |
| 07 | `p-drift` | Stokes drift: the circles do not quite close ★ | [448](../../public/simulations/water-wave.html#L448) | eqs. (20)–(21); Figure 4, RK4 path of a parcel ([456-503](../../public/simulations/water-wave.html#L456-L503)) |
| 08 | `p-method` | Computing the picture | [508](../../public/simulations/water-wave.html#L508) | eq. (22), the per-frame computation |
| 09 | `p-screen` | From metres to pixels | [521](../../public/simulations/water-wave.html#L521) | eq. (23), the screen mapping; what differs from the store |
| 10 | `p-limits` | What the model leaves out | [535](../../public/simulations/water-wave.html#L535) | finite depth, surface tension, steep waves, viscosity; further reading ([545](../../public/simulations/water-wave.html#L545)) |

- The walkthrough host `<section class="walk" id="walk" data-walk="water">`
  ([:557](../../public/simulations/water-wave.html#L557)). `sim.js` loads `../scripts/walk/water.js` from the `data-walk` key
  and builds the stepper ([sim.js:481-490](../../public/scripts/sim.js#L481-L490)); see [walk.md](../scripts/walk.md). The
  file has seven steps: pixels into metres and ω² = gk; phase speed and period; one parcel, one circle; orbits shrink with
  depth; the surface; the steepness limit; the clock and the picture ([water.js:7-216](../../public/scripts/walk/water.js#L7-L216)).
- Footer, then the scripts in load order: `fold.js`, `sim.js`, `dataset.js`, the page's inline script, `datalog.js`
  ([:565-568](../../public/simulations/water-wave.html#L565-L568), [:890](../../public/simulations/water-wave.html#L890)).
  `fold.js` turns each `.psec` and the walkthrough into fold cards ([fold.md](../scripts/fold.md)); `sim.js` typesets the note
  with KaTeX ([sim.js:418-461](../../public/scripts/sim.js#L418-L461)).

## Where the drawing and the store differ

- **The surface line is not stored.** It runs through points every 3 px of rest position that are not parcels
  ([:693-695](../../public/simulations/water-wave.html#L693-L695)); at a surface parcel the stored `zeta` is the surface height.
  The page says so in its `about` paragraph ([:881](../../public/simulations/water-wave.html#L881)) and in note Section 09
  ([:530](../../public/simulations/water-wave.html#L530)).
- **Pixel rounding.** Each parcel is drawn at its stored `px`, `py`; the canvas rounds to its own pixel grid
  ([:881](../../public/simulations/water-wave.html#L881)).
- **Small orbits are hidden.** A circle is drawn only while its radius exceeds 1.2 css px
  ([:749](../../public/simulations/water-wave.html#L749)); its numbers are stored regardless.
- **Layers below the canvas.** Every layer and parcel is computed and stored; drawing is skipped when its centre line lies within 8 css px of the bottom
  ([:739](../../public/simulations/water-wave.html#L739)); `layers_drawn` counts visible rows only.
- **Stokes drift.** The orbits close exactly; `stokes` is stored as a theoretical number and labelled "theory, not drawn"
  ([:599](../../public/simulations/water-wave.html#L599), note Section 07 at [:505](../../public/simulations/water-wave.html#L505)).
- **The frequency slider rounds.** With dispersion on, the motion uses the exact $f$; the slider shows it to 0.01 Hz
  ([:638](../../public/simulations/water-wave.html#L638), [:647](../../public/simulations/water-wave.html#L647)).
- **Readouts round.** The side-panel readouts show at most two decimals; the store keeps full precision
  ([:656-661](../../public/simulations/water-wave.html#L656-L661)).
- **The group speed** `cg` is a prediction: a single endless wave has no groups (note, line
  [:366](../../public/simulations/water-wave.html#L366)).

## How to change it safely

- **Constants appear in several places.** `DZ = 56`, `PX_PER_M = 100`, `G = 9.81`, the 30 px margin, the 0.9 cap, the 34 px and
  0.28 of the calm level, the 560 css px switch to a 400 px field and the 1.2 px orbit threshold are used in `draw()` and `a()`,
  repeated as text in the `formula` attributes ([:581-629](../../public/simulations/water-wave.html#L581-L629)), recomputed in
  the `check` functions ([:841-878](../../public/simulations/water-wave.html#L841-L878)) and quoted as numbers in the lecture
  note (Sections 02, 06, 08, 09, Exercise 6.1). A change to one needs all four.
- **The lecture note's numbers come from the defaults** (abstract, [:113](../../public/simulations/water-wave.html#L113)):
  λ = 2.6 m, $a$ = 0.24 m, $ak$ = 0.58, $c$ = 2.01 m/s, the five radii of Section 06. Changing a slider default
  ([:68-88](../../public/simulations/water-wave.html#L68-L88)) means recomputing them, and the table and Figures 2–3.
- **Walkthrough excerpts.** `water.js` quotes these page lines verbatim: 635, 637-639, 640, 653, 654, 656, 657, 658, 680, 681,
  691-693, 735, 740-742 and 792 (checked by script: every excerpt line is a substring of one of these lines). Keep them
  identical, or edit `water.js` in the same change. When adding a store write, insert a new line after a quoted line, never
  inside a quoted group ([AGENTS.md](../../AGENTS.md)).
- **Write where you compute.** A new quantity gets a `ds.var` declaration, a `ds.set` (or an array write) on the line that
  computes it, an entry in a `groups` list, and, if it has a formula, a `check` entry that recomputes it from stored inputs
  only. Do not recompute in `Sim.live`.
- **Index layout.** If the order of the `z × p` arrays changes, update `probe`, `inspect`, `locate`, `qInputs`, `parcelPixel`
  and the check functions together ([:803-874](../../public/simulations/water-wave.html#L803-L874)).
- **Re-test** in a real browser: at a wide window (≥ 1000 px) and at a window 901–980 px wide, where the field switches to
  400 px. Open the data panel, pause, and check `xi`, `zeta`, `px`, `py` of a parcel (stored, recomputed and read back should
  agree); set the amplitude to 50 px at λ = 260 px and confirm the "(cap)" readout and $ak$ = 0.90; switch dispersion off and on;
  step through all seven walkthrough steps and confirm every "Now" cell fills.

## Notes for maintainers

1. Fixed on 2026-10-15: all requested layers are computed and stored; at 960 × 900, 3 of 5 are drawn and the fifth stored depth is 2.24 m (commit [9d3175f](https://github.com/Numa1997/SiteTest/commit/9d3175f2cf50d0ad3f8792f1ee173e8ce56bab53)).
2. Fixed on 2026-10-15: the note and walkthrough cover both the 800 px field and the 400 px field below a 560 css-px canvas width (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
3. Fixed on 2026-10-15: the skipped caption line is marked with an ellipsis (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
4. Fixed on 2026-10-15: frames is described as playing frames; it stays constant during paused drawing (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).


## Teaching revision · 15 October 2026

The model section makes the first-order circular-orbit approximation and exaggerated default steepness visible. The vorticity argument states the constant-density, inviscid, conservative-force assumptions of circulation conservation. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

Fixed on 2026-10-16 (second repairs): the vorticity paragraph has its picture back (pressure through the centre, gravity at the centre, only friction could twist a parcel) with the three conditions of Kelvin's theorem named ([L254](../../public/simulations/water-wave.html#L254)). See the [audit of the revision](../research-theory-audit.md).

Teaching review, 20 October 2026 (notes/fig05/plan.md): Sections 01, 03, 04, 06, 07, 09 and 10 (all but its reading list) judged clear and left alone. Four small repairs inside
the note, no line added or removed, so every line link above stays valid: the warning paragraph of Section 02 moved after
Figure 1 and defines $z_0$ ([L246](../../public/simulations/water-wave.html#L246)); the group velocity (15) is now reached from
two waves of nearly equal wave number ([L305](../../public/simulations/water-wave.html#L305)); Section 08 says the 307 or 174
surface points are drawn but not stored ([L518](../../public/simulations/water-wave.html#L518)); each further-reading item links
to a page that was opened ([L547-L550](../../public/simulations/water-wave.html#L547-L550)).

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig05/`), the lead made only these changes, each on its existing line, so no line link moved: Figure 1 caption: its two labels point to (4) and (9) ([L244](../../public/simulations/water-wave.html#L244)); §4.2: gz becomes gη at the surface ([L274](../../public/simulations/water-wave.html#L274)); §07: the sin² half of the Stokes-drift picture ([L455](../../public/simulations/water-wave.html#L455)); §08: W_field defined where first used ([L514](../../public/simulations/water-wave.html#L514)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).

## Second check round · 20 October 2026

From the derivation checks and blind referees that ran after the usage limit lifted (`notes/fig05/`), each change on its existing line: §08: Δt capped at 0.05 s ([L510](../../public/simulations/water-wave.html#L510)); §09: the canvas antialiases, it does not round positions ([L532](../../public/simulations/water-wave.html#L532)). Checked with `notes/verify.mjs` at 1440 × 900, 1600 × 900 and 390 × 844.

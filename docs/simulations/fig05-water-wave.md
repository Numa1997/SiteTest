# Fig. 5 · Circular Water Waves

| | |
|---|---|
| Page | [public/simulations/water-wave.html](../../public/simulations/water-wave.html) (890 lines, 159 733 bytes) |
| Walkthrough | [public/scripts/walk/water.js](../../public/scripts/walk/water.js) (115 lines, key `water`) |
| Thumbnail | [public/images/sims/water-wave.webp](../../public/images/sims/water-wave.webp) (800 × 500 px, 15 kB) |
| Catalog entry | [public/scripts/catalog.js#L115](../../public/scripts/catalog.js#L115) (lines 115–131, `id: 'water-wave'`, `fig: 5`) |

The reader sees a cross-section of deep water under a travelling wave: a burgundy surface line, a rose tint under it, and rows
of dots, one row per depth layer, each dot a parcel of water running round its own circle
([water-wave.html:43-51](../../public/simulations/water-wave.html#L43-L51)). The middle column of parcels is drawn larger and
in burgundy, with a line from each orbit centre to its parcel, so the reader can follow one vertical line of water from the
surface down ([:756-768](../../public/simulations/water-wave.html#L756-L768)). The side panel sets the amplitude, wavelength
and frequency, the number of parcels per layer and of layers, and two switches: the orbits and the deep-water law
$\omega^2 = gk$ ([:53-104](../../public/simulations/water-wave.html#L53-L104)). Four readouts give the phase speed, the period,
the steepness and the size of the deepest orbit ([:91-96](../../public/simulations/water-wave.html#L91-L96)). Below the figure
come the lecture note and the walkthrough "From symbols to code".

In this page, "px" without a qualifier means a pixel of the drawn field, with 100 px = 1 m
([:570](../../public/simulations/water-wave.html#L570)); "css px" means a screen pixel of the canvas. Line links of the form
`:NNN` point into `water-wave.html`.

## The physics in one picture

**Everyday picture.** A gull resting on the swell rises, slides forward, sinks into the trough, slides back, and ends almost
where it started. A diver a few metres down hardly feels short chop but still feels a long swell. After a distant storm the
long waves arrive first. The lecture note opens with these three facts (Section 01,
[:131-137](../../public/simulations/water-wave.html#L131-L137)).

**Model.** Water is incompressible, has no friction and does not spin; the wave is small ($ak \ll 1$, linear or Airy theory);
the water is deep; gravity and pressure are the only forces (Section 02,
[:143-150](../../public/simulations/water-wave.html#L143-L150)). The note derives Laplace's equation for the velocity potential
(Section 03), the three boundary conditions (Section 04), the dispersion relation $\omega^2 = gk$ (Section 05), the circular
orbits that shrink as $e^{kz}$ (Section 06) and the Stokes drift that linear theory hides (Section 07). The page itself
evaluates only the end results, in closed form.

**What the code evaluates.** Symbols and units:

- $\lambda$: wavelength, px (slider `lambda`); $\lambda/100$ in m.
- $k = 2\pi/\lambda$: wave number, rad/px ([:635](../../public/simulations/water-wave.html#L635)); $k_\mathrm{m} = 100\,k$, rad/m.
- $g = 9.81$ m/s² ([:570](../../public/simulations/water-wave.html#L570)).
- $f$: frequency, Hz. With the dispersion switch on, from $\omega^2 = g k_\mathrm{m}$; with it off, the slider value
  ([:637-639](../../public/simulations/water-wave.html#L637-L639)):

$$f = \frac{\sqrt{g\,k_\mathrm{m}}}{2\pi}, \qquad \omega = 2\pi f, \qquad T = \frac{1}{f}, \qquad c = \frac{f\,\lambda}{100}, \qquad c_g = \frac{c}{2}$$

  with $\omega$ in rad/s, $T$ in s, the phase speed $c$ and the group speed $c_g$ in m/s
  ([:653](../../public/simulations/water-wave.html#L653), [:660-663](../../public/simulations/water-wave.html#L660-L663)).
- $A$: the amplitude slider, px. The amplitude used is capped so that the surface never folds over
  ([:640](../../public/simulations/water-wave.html#L640)):

$$a = \min\left(A,\ \frac{0.9}{k}\right), \qquad ak \le 0.9 .$$

- Layer $j = 0, 1, \dots, L-1$ sits at rest depth $z_0 = -56\,j$ px (0.56 m apart); its orbit radius is
  ([:735](../../public/simulations/water-wave.html#L735))

$$r_j = a\,e^{k z_0} .$$

- Parcel $i = 0, \dots, N-1$ of a layer has its orbit centre at $X_0 = 30 + i\,(W - 60)/(N - 1)$ px, where $W$ is the field
  width, 800 px, or 400 px on a canvas narrower than 560 css px ([:679](../../public/simulations/water-wave.html#L679),
  [:740](../../public/simulations/water-wave.html#L740)).
- With the accumulated phase $\omega t$ (rad), each parcel's phase $\theta$ (rad), displacement $(\xi, \zeta)$ (px, $\zeta$
  upwards) and velocity $(u, w)$ (px/s) are ([:741-744](../../public/simulations/water-wave.html#L741-L744))

$$\theta = k X_0 - \omega t, \qquad \xi = -r\sin\theta, \qquad \zeta = r\cos\theta, \qquad u = r\omega\cos\theta, \qquad w = r\omega\sin\theta .$$

  These are equations (17) and (16) of the note, evaluated at the rest position. The velocity is the time derivative of the
  displacement.
- The surface is the curve of all surface parcels, a trochoid, traced for $X = -60, -57, \dots, W + 60$ px
  ([:691-693](../../public/simulations/water-wave.html#L691-L693)):

$$x = X - a\sin(kX - \omega t), \qquad \eta = a\cos(kX - \omega t) .$$

- Stored as theory, never drawn: the surface Stokes drift $U_S = \omega\,k_\mathrm{m}\,a_\mathrm{m}^2$ in m/s, with
  $a_\mathrm{m} = a/100$ ([:664](../../public/simulations/water-wave.html#L664)), and the size of the deepest orbit relative to
  $a$, $e^{-k \cdot 56\,(L-1)}$ ([:658](../../public/simulations/water-wave.html#L658)).

At the defaults ($\lambda$ = 260 px, $A$ = 24 px, dispersion on), measured in headless Chromium: $f$ = 0.7749 Hz,
$k_\mathrm{m}$ = 2.4166 rad/m, $c$ = 2.0148 m/s, $T$ = 1.2905 s, $ak$ = 0.580, $U_S$ = 0.678 m/s, orbit radii 24, 6.20, 1.60,
0.414 and 0.107 px for the five layers.

## How the code computes it

**State.** One inline script, an immediately invoked function ([:566-887](../../public/simulations/water-wave.html#L566-L887)).
Constants `WORLD_W = 800`, `DZ = 56` (px between layers), `PX_PER_M = 100`, `G = 9.81`
([:570](../../public/simulations/water-wave.html#L570)); `WORLD_W` is reassigned every frame
([:679](../../public/simulations/water-wave.html#L679)). The canvas wrapper `box` from `Sim.canvas2d`
([:573](../../public/simulations/water-wave.html#L573), [sim.js:32-46](../../public/scripts/sim.js#L32-L46)) carries the size
in css px (`box.w`, `box.h`) and the device pixel ratio (capped at 2). The only time-dependent state is `omegaT` (rad), with
`fps` and `frames` for the data panel ([:575](../../public/simulations/water-wave.html#L575)). The five sliders are wrapped by
`Sim.slider` ([:629-633](../../public/simulations/water-wave.html#L629-L633), [sim.js:153-174](../../public/scripts/sim.js#L153-L174)).
All per-parcel numbers live in the data store, in typed arrays that `draw()` fills.

**Numerical method.** None in the sense of an integrator: positions and velocities are closed-form expressions, evaluated afresh
every frame. Only the phase is accumulated, `omegaT += 2 * Math.PI * f() * dt`
([:792](../../public/simulations/water-wave.html#L792)). Adding $2\pi f\,\Delta t$ frame by frame, rather than computing
$\omega t$ from a clock, keeps the motion continuous when $f$ changes (note Section 08,
[:510](../../public/simulations/water-wave.html#L510)). `f()` returns the exact deep-water frequency, not the slider value
rounded to 0.01 Hz ([:636-639](../../public/simulations/water-wave.html#L636-L639)), so $c$ and the motion agree to machine
precision. Nothing is integrated, so no error builds up; the clock caps $\Delta t$ at 0.05 s and gives $\Delta t = 0$ while
paused ([sim.js:180-182](../../public/scripts/sim.js#L180-L182)).

**The frame loop, in order.** `Sim.clock` calls its callback on every animation frame, playing or paused
([sim.js:177-187](../../public/scripts/sim.js#L177-L187)).

1. Advance the phase, update the frame-rate average, write `omegaT`, `periods`, `t`, `dt`, `fps`, `frames`, `playing` into the
   store ([:792-794](../../public/simulations/water-wave.html#L792-L794)).
2. `draw()` ([:678-775](../../public/simulations/water-wave.html#L678-L775)):
   1. Layout: field width `WORLD_W` (800, or 400 if `box.w < 560`), scale `s = w / WORLD_W`, `kk = k()`, `A = a()`, calm level
      `ys = max(A s + 34, 0.28 h)`, `om = 2π f()` ([:679-682](../../public/simulations/water-wave.html#L679-L682)).
   2. Resize the dimensions `z` and `p` to the layer and parcel counts and fetch the arrays with `ds.alloc`
      ([:683-685](../../public/simulations/water-wave.html#L683-L685)); write the layout scalars
      ([:686](../../public/simulations/water-wave.html#L686)). Clear the canvas ([:687](../../public/simulations/water-wave.html#L687)).
   3. Water body: a path through the surface points every 3 px from −60 to `WORLD_W + 60`, closed along the canvas bottom,
      filled with a rose gradient from 36 % opacity at crest height to 5 % at the bottom
      ([:689-705](../../public/simulations/water-wave.html#L689-L705)).
   4. Surface line: the same points again, stroked in the accent colour, 2.2 css px wide
      ([:707-716](../../public/simulations/water-wave.html#L707-L716)).
   5. Calm level: a dashed line at `ys` ([:718-726](../../public/simulations/water-wave.html#L718-L726)).
   6. Layers: for each `j`, compute `z0`, `r`, the screen height `cy` of the orbit centres, and store `r_z`, `depth`, `cy_px`
      ([:735-736](../../public/simulations/water-wave.html#L735-L736)); record whether `cy ≤ h - 8` and count only visible rows
      ([:737](../../public/simulations/water-wave.html#L737)). For every parcel `i`, including hidden layers: `X0`, `th`, screen position `px`, `py`
      ([:740-742](../../public/simulations/water-wave.html#L740-L742)); store eight arrays at the flat index `q = j * N + i`
      ([:743-744](../../public/simulations/water-wave.html#L743-L744)); skip drawing for hidden parcels, otherwise draw the orbit circle if the switch is on and
      `r * s > 1.2` css px ([:747-755](../../public/simulations/water-wave.html#L747-L755)), the radius line of the followed
      parcel ([:756-763](../../public/simulations/water-wave.html#L756-L763)) and the dot: radius 3.8 (surface) or 3.1 css px,
      6 or 5 for the followed column ([:764-768](../../public/simulations/water-wave.html#L764-L768)). Layers below the surface
      get a depth label "z = −0.56 m" ([:770](../../public/simulations/water-wave.html#L770),
      `depthLabel` at [:669-677](../../public/simulations/water-wave.html#L669-L677)).
   7. Store `layers_drawn` and mark the arrays as changed with `ds.touch`
      ([:772-774](../../public/simulations/water-wave.html#L772-L774)).

Outside the frame loop, a control change calls `readouts()` ([:652-666](../../public/simulations/water-wave.html#L652-L666)),
which rewrites the side-panel readouts and the caption speed, and writes all derived scalars ($k$, $c$, $T$, $a$, $ak$,
$U_S$, …) into the store. Moving the wavelength or flipping the dispersion switch goes through `couple()`
([:642-649](../../public/simulations/water-wave.html#L642-L649)), which, with the switch on, sets the frequency slider to the
deep-water value and disables it.

**Precomputation and caching.** None. Every frame recomputes every parcel: at the defaults 18 × 5 = 90 parcels, plus 307
surface points that are evaluated twice, once for the fill and once for the stroke
([:691](../../public/simulations/water-wave.html#L691), [:708](../../public/simulations/water-wave.html#L708)). The store's
typed arrays are reused while their sizes stay the same ([dataset.js:64-70](../../public/scripts/dataset.js#L64-L70)), so a frame
allocates nothing unless a slider changed a count. The frame runs even while paused, with $\Delta t = 0$, so slider changes show
at once.

## Function map

Line numbers link into `water-wave.html`.

| Function | Lines | What it does |
|---|---|---|
| (sliders' `format` callbacks) | [629-633](../../public/simulations/water-wave.html#L629-L633) | Text in each slider's `<output>`: "24 px", "0.77 Hz", "18". |
| `k()` | [635](../../public/simulations/water-wave.html#L635) | Wave number $2\pi/\lambda$, rad/px, from the wavelength slider. |
| `f()` | [637-639](../../public/simulations/water-wave.html#L637-L639) | Frequency: $\sqrt{g\,k\,100}/2\pi$ with dispersion on, the slider value with it off. |
| `a()` | [640](../../public/simulations/water-wave.html#L640) | Amplitude used, $\min(A, 0.9/k)$. |
| `couple()` | [642-649](../../public/simulations/water-wave.html#L642-L649) | With dispersion on, sets the frequency slider to the deep-water value; enables or disables it; calls `readouts()`. Bound to the dispersion switch at [650](../../public/simulations/water-wave.html#L650). |
| `readouts()` | [652-666](../../public/simulations/water-wave.html#L652-L666) | Writes the four readouts and the caption speed; writes every parameter and derived scalar into the store. |
| `depthLabel(rest, x, y)` | [669-677](../../public/simulations/water-wave.html#L669-L677) | Draws "z = −0.56 m" with `Sim.tex` on a pale box. |
| `draw()` | [678-775](../../public/simulations/water-wave.html#L678-L775) | One frame: layout, water fill, surface, calm level, all layers and parcels; writes the arrays. |
| `Sim.live` | [778-790](../../public/simulations/water-wave.html#L778-L790) | Live values for the walkthrough, read from the store. |
| clock callback `(dt, t)` | [791-796](../../public/simulations/water-wave.html#L791-L796) | Advances `omegaT`, writes the time scalars, calls `draw()`. `Sim.playButton` binds the Pause button at [797](../../public/simulations/water-wave.html#L797). |
| `sliderCheck(input, label)` | [800](../../public/simulations/water-wave.html#L800) | Check entry for a value that comes straight from a slider. |
| `at(q)` | [801](../../public/simulations/water-wave.html#L801) | Stored screen position of parcel `q`. |
| `parcelPixel(q)` | [802-808](../../public/simulations/water-wave.html#L802-L808) | Read-back: the canvas pixel at the parcel's stored centre; passes if alpha > 0 and luminance < 130. |
| `qInputs(q)` | [809](../../public/simulations/water-wave.html#L809) | The inputs (layer, column, r, θ) shown in a parcel check. |
| `Sim.data.playing` | [812](../../public/simulations/water-wave.html#L812) | Clock state for the panel. |
| `Sim.data.rowLabel.z` | [820](../../public/simulations/water-wave.html#L820) | Row names "z0", "z1", … in array tables. |
| `Sim.data.colour.*` | [821](../../public/simulations/water-wave.html#L821) | Cell shading of `xi`, `zeta` (scale $a$) and `u`, `w` (scale $a\omega$) with `Sim.colourMap`. |
| `Sim.data.probe(x, y)` | [822-826](../../public/simulations/water-wave.html#L822-L826) | Nearest drawn parcel within 14 css px of a point, as `{ q }`. |
| `Sim.data.inspect(ref)` | [827-831](../../public/simulations/water-wave.html#L827-L831) | Title, position and eight rows ($X_0$, depth, $r$, θ, ξ, ζ, u, w) of a pinned parcel. |
| `Sim.data.locate(name, idx)` | [832-838](../../public/simulations/water-wave.html#L832-L838) | Where an array cell is drawn: the parcel itself, or the followed parcel of a layer. |
| `Sim.data.check.*` | [839-876](../../public/simulations/water-wave.html#L839-L876) | For 36 variables: the formula, its stored inputs and the recomputed value. |
| `Sim.data.drawn` | [877](../../public/simulations/water-wave.html#L877) | `px`, `py`, `xi`, `zeta` are read back with `parcelPixel`. |
| `Sim.data.round.label`, `.length`, `.point` | [878-879](../../public/simulations/water-wave.html#L878-L879) | One round = one period $T$; the followed surface parcel is recorded. |
| `Sim.data.play` | [880](../../public/simulations/water-wave.html#L880) | Starts the clock before a round. |
| start-up | [883-885](../../public/simulations/water-wave.html#L883-L885) | `couple()`, `draw()`, and a resize observer that refits the canvas. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Pause / Play | `play` | playing at load, unless the reader prefers reduced motion ([sim.js:178](../../public/scripts/sim.js#L178)) | `clk.toggle` via `Sim.playButton` ([:797](../../public/simulations/water-wave.html#L797)); paused frames get $\Delta t = 0$. |
| Show orbits | `orbits` | on ([:59](../../public/simulations/water-wave.html#L59)) | Orbit circles drawn when on and $r s > 1.2$ ([:747](../../public/simulations/water-wave.html#L747)); stored as `orbits`. |
| Deep-water dispersion ω² = gk | `disp` | on ([:60](../../public/simulations/water-wave.html#L60)) | `f()` uses the dispersion relation; `couple()` sets and disables the frequency slider ([:642-650](../../public/simulations/water-wave.html#L642-L650)). |
| Amplitude a (orbit radius) | `amp` | 5–50 px, step 1, default 24 ([:67](../../public/simulations/water-wave.html#L67)) | $A$; $a = \min(A, 0.9/k)$; calls `readouts()`. |
| Wavelength λ | `lambda` | 120–400 px, step 5, default 260 ([:71](../../public/simulations/water-wave.html#L71)) | $k$; calls `couple()`. |
| Frequency f | `freq` | 0.1–1.5 Hz, step 0.01, default 0.5 ([:75](../../public/simulations/water-wave.html#L75)); set to 0.77 at load by `couple()` | Used only with dispersion off; calls `readouts()`. |
| Particles per layer | `count` | 8–36, step 1, default 18 ([:83](../../public/simulations/water-wave.html#L83)) | $N$, read by `draw()` every frame; no callback. |
| Depth layers | `layers` | 1–5, step 1, default 5 ([:87](../../public/simulations/water-wave.html#L87)) | $L$ in `draw()`; the deepest-orbit readout; calls `readouts()`. |
| Read values | added by datalog.js into the caption | off | Pins a parcel; see [datalog.md](../scripts/datalog.md). |

## What the page writes into the data store

The store is created at [:578](../../public/simulations/water-wave.html#L578) with
`Sim.dataset({ title: 'Water waves', attrs: { figure: 5, page, WORLD_W, DZ, PX_PER_M, g, length_unit } })`. How the store works
is in [dataset.md](../scripts/dataset.md). Every variable carries `symbol`, `units`, `long_name`, `computed_in` and a `formula`
or `source` string for the panel.

**Dimensions.** `p` (parcels per layer) and `z` (layers), declared with length 0
([:605](../../public/simulations/water-wave.html#L605), [:607](../../public/simulations/water-wave.html#L607)) and resized every
frame to $N$ and $L$ ([:683](../../public/simulations/water-wave.html#L683)).

**Arrays** (Float64Array, written every frame in `draw()`):

| Name | Dims | Declared | Written | Meaning |
|---|---|---|---|---|
| `X0` (coordinate) | p | [606](../../public/simulations/water-wave.html#L606) | [744](../../public/simulations/water-wave.html#L744) | orbit centre of each column, px |
| `depth` (coordinate) | z | [608](../../public/simulations/water-wave.html#L608) | [736](../../public/simulations/water-wave.html#L736) | depth of each layer, m |
| `r_z` | z | [609](../../public/simulations/water-wave.html#L609) | [736](../../public/simulations/water-wave.html#L736) | orbit radius of each layer, px |
| `cy_px` | z | [610](../../public/simulations/water-wave.html#L610) | [736](../../public/simulations/water-wave.html#L736) | screen height of the layer's orbit centres, css px |
| `theta`, `xi`, `zeta`, `u`, `w` | z × p | [611-615](../../public/simulations/water-wave.html#L611-L615) | [744](../../public/simulations/water-wave.html#L744) | phase (rad), displacement (px), velocity (px/s) |
| `px`, `py` | z × p | [616-617](../../public/simulations/water-wave.html#L616-L617) | [744](../../public/simulations/water-wave.html#L744) | screen position of each parcel, css px |

Two-dimensional arrays are row-major, one row per layer: parcel $i$ of layer $j$ is at index $q = jN + i$
([:743](../../public/simulations/water-wave.html#L743)). `probe`, `inspect`, `locate` and `parcelPixel` all rely on this.

**Scalars.**

| Written in | Line | Variables |
|---|---|---|
| `readouts()` (on control change) | [661-665](../../public/simulations/water-wave.html#L661-L665) | `amp`, `lambda`, `lambda_m`, `f`, `dispersion`, `N`, `layers`, `k`, `k_m`, `omega`, `T`, `c`, `c_deep`, `cg`, `a`, `cap`, `ak`, `stokes`, `deep`, `r1`, `z_deep_px` |
| `draw()` (every frame) | [686](../../public/simulations/water-wave.html#L686), [772](../../public/simulations/water-wave.html#L772) | `N`, `layers`, `world_w`, `s_px`, `ys`, `box_w`, `box_h`, `orbits`, `follow`; `layers_drawn` |
| clock callback (every frame) | [794](../../public/simulations/water-wave.html#L794) | `omegaT`, `periods`, `t`, `dt`, `fps`, `frames`, `playing` |

Their declarations are at [:579-604](../../public/simulations/water-wave.html#L579-L604) and
[:618-627](../../public/simulations/water-wave.html#L618-L627). The scalars of the first row do not depend on time, so they are
written only when a control changes; the panel groups them as "Physical parameters" and "Derived physics"
([:814-815](../../public/simulations/water-wave.html#L814-L815)).

**One round** (`Sim.data.round`, [:878-879](../../public/simulations/water-wave.html#L878-L879)): one period, length
`ds.get('T')` seconds of the time variable `t`, labelled "one period, T = … s". The chart column is `omegaT`, and the point
followed is the burgundy surface parcel, `{ q: follow }`. The panel samples every numeric scalar at most 600 times in the
round ([datalog.js:743](../../public/scripts/datalog.js#L743), [datalog.js:772](../../public/scripts/datalog.js#L772)).

**The panel hooks.** `Sim.data` ([:810-882](../../public/simulations/water-wave.html#L810-L882)) also sets `kicker: 'Fig. 5 ·
data'` and `file: 'fig5-water-waves'` (the base name of the saved archive), the five groups, the `check` and `drawn` tests,
and the `about` paragraph. The contract is at [datalog.js:8-26](../../public/scripts/datalog.js#L8-L26).

**`Sim.live()`** ([:778-790](../../public/simulations/water-wave.html#L778-L790)) reads only the store and returns formatted
strings for the walkthrough's "Now" column: `lam`, `k`, `km`, `f`, `c`, `T`, `cg`; for the followed surface parcel `X0`, `th`
(θ reduced to (−π, π] with `atan2`), `px` (ξ), `pz` and `eta` (both ζ); `r` (surface radius), `r1`, `z0` (depth of the
deepest layer, from `z_deep_px`), `deep`; `a`, `A`, `ak`; `wt` (ωt), `s`, `ys`. The walkthrough polls it every 200 ms
([sim.js:388-400](../../public/scripts/sim.js#L388-L400)).

**Three-way check, measured.** Paused at 1440 × 900 (canvas 770 × 366 css px), for the followed surface parcel: stored
`xi` = 23.985449954109615 px and the value recomputed by `check.xi` from the stored `r_z` and `theta` are identical; the same
holds for `zeta`, `u`, `w`, `theta`, `px` and `py`. The pixel read back at the stored centre (387.1, 103.3) css px is
rgb(122, 31, 43), the burgundy of the followed parcel, at full alpha.

## Page structure

**Head** ([:3-15](../../public/simulations/water-wave.html#L3-L15)): title, description, theme colour; preconnects to Google Fonts;
stylesheets `../styles/sim.css` (which imports the Google fonts, KaTeX's CSS and `paper.css`), `../styles/data.css`,
`../styles/fold.css`; an inline SVG favicon. No page-specific `<style>`. See [styles.md](../styles.md).

**Body.**

- Top bar with the link back to the catalog and the hand-written Fig. 1–10 links, Fig. 5 marked `aria-current`
  ([:17-32](../../public/simulations/water-wave.html#L17-L32)).
- Heading: "Fig. 5 · fluid dynamics · particle motion", the h1 and the lede ([:36-40](../../public/simulations/water-wave.html#L36-L40)).
- The figure: `#stage` with aspect ratio 16 / 7.6, or 1 / 0.95 below 900 px viewport width
  ([:44](../../public/simulations/water-wave.html#L44), [sim.css:289](../../public/styles/sim.css#L289)), the canvas `#water`, and
  the caption with the speed `#cap-c` ([:47-50](../../public/simulations/water-wave.html#L47-L50)). datalog.js adds the
  Read values switch to this caption and the reading strip under the figure
  ([datalog.js:566-589](../../public/scripts/datalog.js#L566-L589)).
- The control panel: Run, Wave and Water groups, readouts, legend ([:53-104](../../public/simulations/water-wave.html#L53-L104)).
- The lecture note `<article class="paper" id="paper">` ([:107-553](../../public/simulations/water-wave.html#L107-L553)), "Deep-water
  waves: the sea moves in circles", with an abstract and a contents list. Ten sections, 23 numbered equations (1)–(23), four
  inline SVG figures, one result box, two exercises and one table:

| § | id | Title | Line | Contents |
|---|---|---|---|---|
| 01 | `p-gull` | A gull on the swell | [131](../../public/simulations/water-wave.html#L131) | the everyday picture |
| 02 | `p-model` | The model | [139](../../public/simulations/water-wave.html#L139) | assumptions; Figure 1, the model ([151-244](../../public/simulations/water-wave.html#L151-L244)) |
| 03 | `p-laplace` | Potential flow: Laplace's equation | [248](../../public/simulations/water-wave.html#L248) | eqs. (1)–(4) |
| 04 | `p-edges` | Three conditions at the edges ★ | [262](../../public/simulations/water-wave.html#L262) | eqs. (5)–(9) |
| 05 | `p-dispersion` | Gravity sets the pace: the dispersion relation | [281](../../public/simulations/water-wave.html#L281) | eqs. (10)–(15); box ω² = gk ([293](../../public/simulations/water-wave.html#L293)); speed table ([306](../../public/simulations/water-wave.html#L306)); Figure 2, phase and group speed ([317-363](../../public/simulations/water-wave.html#L317-L363)); Exercise 5.1 ([365](../../public/simulations/water-wave.html#L365)) |
| 06 | `p-orbits` | Every parcel runs in a circle | [371](../../public/simulations/water-wave.html#L371) | eqs. (16)–(19); Figure 3, radius against depth ([383-432](../../public/simulations/water-wave.html#L383-L432)); Exercise 6.1 ([434](../../public/simulations/water-wave.html#L434)) |
| 07 | `p-drift` | Stokes drift: the circles do not quite close ★ | [446](../../public/simulations/water-wave.html#L446) | eqs. (20)–(21); Figure 4, RK4 path of a parcel ([454-501](../../public/simulations/water-wave.html#L454-L501)) |
| 08 | `p-method` | Computing the picture | [506](../../public/simulations/water-wave.html#L506) | eq. (22), the per-frame computation |
| 09 | `p-screen` | From metres to pixels | [519](../../public/simulations/water-wave.html#L519) | eq. (23), the screen mapping; what differs from the store |
| 10 | `p-limits` | What the model leaves out | [533](../../public/simulations/water-wave.html#L533) | finite depth, surface tension, steep waves, viscosity; further reading ([543](../../public/simulations/water-wave.html#L543)) |

- The walkthrough host `<section class="walk" id="walk" data-walk="water">`
  ([:555](../../public/simulations/water-wave.html#L555)). `sim.js` loads `../scripts/walk/water.js` from the `data-walk` key
  and builds the stepper ([sim.js:476-486](../../public/scripts/sim.js#L476-L486)); see [walk.md](../scripts/walk.md). The
  file has seven steps: pixels into metres and ω² = gk; phase speed and period; one parcel, one circle; orbits shrink with
  depth; the surface; the steepness limit; the clock and the picture ([water.js:7-115](../../public/scripts/walk/water.js#L7-L115)).
- Footer, then the scripts in load order: `fold.js`, `sim.js`, `dataset.js`, the page's inline script, `datalog.js`
  ([:563-566](../../public/simulations/water-wave.html#L563-L566), [:888](../../public/simulations/water-wave.html#L888)).
  `fold.js` turns each `.psec` and the walkthrough into fold cards ([fold.md](../scripts/fold.md)); `sim.js` typesets the note
  with KaTeX ([sim.js:413-456](../../public/scripts/sim.js#L413-L456)).

## Where the drawing and the store differ

- **The surface line is not stored.** It runs through points every 3 px of rest position that are not parcels
  ([:691-693](../../public/simulations/water-wave.html#L691-L693)); at a surface parcel the stored `zeta` is the surface height.
  The page says so in its `about` paragraph ([:881](../../public/simulations/water-wave.html#L881)) and in note Section 09
  ([:530](../../public/simulations/water-wave.html#L530)).
- **Pixel rounding.** Each parcel is drawn at its stored `px`, `py`; the canvas rounds to its own pixel grid
  ([:881](../../public/simulations/water-wave.html#L881)).
- **Small orbits are hidden.** A circle is drawn only while its radius exceeds 1.2 css px
  ([:747](../../public/simulations/water-wave.html#L747)); its numbers are stored regardless.
- **Layers below the canvas.** Every layer and parcel is computed and stored; drawing is skipped when its centre line lies within 8 css px of the bottom
  ([:737](../../public/simulations/water-wave.html#L737)); `layers_drawn` counts visible rows only.
- **Stokes drift.** The orbits close exactly; `stokes` is stored as a theoretical number and labelled "theory, not drawn"
  ([:597](../../public/simulations/water-wave.html#L597), note Section 07 at [:504](../../public/simulations/water-wave.html#L504)).
- **The frequency slider rounds.** With dispersion on, the motion uses the exact $f$; the slider shows it to 0.01 Hz
  ([:636](../../public/simulations/water-wave.html#L636), [:645](../../public/simulations/water-wave.html#L645)).
- **Readouts round.** The side-panel readouts show at most two decimals; the store keeps full precision
  ([:654-659](../../public/simulations/water-wave.html#L654-L659)).
- **The group speed** `cg` is a prediction: a single endless wave has no groups (note, line
  [:364](../../public/simulations/water-wave.html#L364)).

## How to change it safely

- **Constants appear in several places.** `DZ = 56`, `PX_PER_M = 100`, `G = 9.81`, the 30 px margin, the 0.9 cap, the 34 px and
  0.28 of the calm level, the 560 css px switch to a 400 px field and the 1.2 px orbit threshold are used in `draw()` and `a()`,
  repeated as text in the `formula` attributes ([:579-627](../../public/simulations/water-wave.html#L579-L627)), recomputed in
  the `check` functions ([:839-876](../../public/simulations/water-wave.html#L839-L876)) and quoted as numbers in the lecture
  note (Sections 02, 06, 08, 09, Exercise 6.1). A change to one needs all four.
- **The lecture note's numbers come from the defaults** (abstract, [:112](../../public/simulations/water-wave.html#L112)):
  λ = 2.6 m, $a$ = 0.24 m, $ak$ = 0.58, $c$ = 2.01 m/s, the five radii of Section 06. Changing a slider default
  ([:67-87](../../public/simulations/water-wave.html#L67-L87)) means recomputing them, and the table and Figures 2–3.
- **Walkthrough excerpts.** `water.js` quotes these page lines verbatim: 635, 637-639, 640, 653, 654, 656, 657, 658, 680, 681,
  691-693, 734, 738-740 and 789 (checked by script: every excerpt line is a substring of one of these lines). Keep them
  identical, or edit `water.js` in the same change. When adding a store write, insert a new line after a quoted line, never
  inside a quoted group ([AGENTS.md](../../AGENTS.md)).
- **Write where you compute.** A new quantity gets a `ds.var` declaration, a `ds.set` (or an array write) on the line that
  computes it, an entry in a `groups` list, and, if it has a formula, a `check` entry that recomputes it from stored inputs
  only. Do not recompute in `Sim.live`.
- **Index layout.** If the order of the `z × p` arrays changes, update `probe`, `inspect`, `locate`, `qInputs`, `parcelPixel`
  and the check functions together ([:801-872](../../public/simulations/water-wave.html#L801-L872)).
- **Re-test** in a real browser: at a wide window (≥ 1000 px) and at a window 901–980 px wide, where the field switches to
  400 px. Open the data panel, pause, and check `xi`, `zeta`, `px`, `py` of a parcel (stored, recomputed and read back should
  agree); set the amplitude to 50 px at λ = 260 px and confirm the "(cap)" readout and $ak$ = 0.90; switch dispersion off and on;
  step through all seven walkthrough steps and confirm every "Now" cell fills.

## Notes for maintainers

1. Fixed on 2026-10-15: all requested layers are computed and stored; at 960 × 900, 3 of 5 are drawn and the fifth stored depth is 2.24 m (commit `:/^Batch A: fix simulation and recording faults; verify in Chromium$`).
2. Fixed on 2026-10-15: the note and walkthrough cover both the 800 px field and the 400 px field below a 560 css-px canvas width (commit `:/^Batch B: correct notes and layout; verify measured figures in Chromium$`).
3. **Walkthrough step 2 hides a skipped line.** Its excerpt shows lines 653, 654 and 656 as adjacent
   ([water.js:31-33](../../public/scripts/walk/water.js#L31-L33)); line 655 (the caption speed `cap-c`) is left out without
   the `...` used elsewhere.
4. **`frames` counts only playing frames.** It is described as "frames drawn so far"
   ([:626](../../public/simulations/water-wave.html#L626)) but increases only when $\Delta t > 0$
   ([:793](../../public/simulations/water-wave.html#L793)), while `draw()` runs on paused frames too. Fig. 6 counts every frame.

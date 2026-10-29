# Fig. 3 · Double-Slit Interference

| | |
|---|---|
| Page | [public/simulations/Interactive Double-Slit Experiment Visualization.html](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html) (949 lines, 175 291 bytes; 64 lines are longer than 300 characters, 56 of them in the lecture note) |
| Walkthrough | [public/scripts/walk/slit.js](../../public/scripts/walk/slit.js) (227 lines, 11 steps) |
| Thumbnail | [public/images/sims/double-slit.webp](../../public/images/sims/double-slit.webp) (800 × 500 px, 33.4 kB) |
| Catalog entry | [public/scripts/catalog.js#L82](../../public/scripts/catalog.js#L82) (`id: 'double-slit'`, `fig: 3`, field `optics`, stage 1, `has: ALL`) |

In this page, "page:N" means line N of the page file above.

The reader sees two slits $S_1$, $S_2$ in a dark wall, a point $P$ beyond the wall, the two straight paths from the slits to
$P$, and a thick burgundy bar on the longer path whose length is the path difference $\delta s$. Rose arcs (the wavelets)
grow out of both slits and straight rose lines (the incoming wave) move up towards the wall. Under the figure, Fig. 3b plots
the brightness $I/I_0$ against direction from 0° to 30°: the burgundy curve is the textbook far-field law, the dashed curve
uses the exact path difference at the chosen distance, and a dot marks the brightness at $P$. Four sliders set the distance
$d$, the angle $\alpha$, the slit separation $b$ and the wavelength $\lambda$; six readouts and a one-line verdict
("Constructive", "Destructive" or "Partial") answer them ([page:85–127](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L85-L127)).
Nothing is integrated in time: every number is a closed formula, recomputed when a slider moves; only the wavelets animate.

## The physics in one picture

**Everyday picture.** Two loudspeakers play the same tone. Walking across the room you hear loud and quiet places, because at
each place the two sounds arrive having travelled different distances. Where the extra distance is a whole number of
wavelengths, crest meets crest; where it is a whole number and a half, crest meets trough. The lecture note opens with this
picture and Young's experiment ([page:154–161](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L154-L161)).

**Model.** Two coherent point sources of one wavelength, equal amplitudes, a scalar wave, observed at one point $P$
([page:165–174](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L165-L174)). All lengths are
pixels (px) of the 600 × 440 drawing. Only the ratios $b/\lambda$ and $d/b$ and the angle matter, so the pixel is a ruler, not a
physical unit ([page:175](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L175), Section 9 at
[page:514](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L514)). Time is in seconds.

**The equations the code evaluates.** The code works in SVG coordinates: $x$ to the right, $y$ downwards, the wall at
$y = Y_0 = 370$, the slit midpoint $M$ at $x = X_0 = 300$ ([page:554](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L554)).

$$S_1 = (X_0 - b/2,\ Y_0), \qquad S_2 = (X_0 + b/2,\ Y_0), \qquad P = (X_0 - d\tan\alpha,\ Y_0 - d)$$

$$L_1 = |P - S_1|, \qquad L_2 = |P - S_2|, \qquad \delta s = \frac{2\,b\,d\tan\alpha}{L_1 + L_2}$$

$$\hat u = \frac{S_2 - P}{L_2}, \qquad Q = P + L_1\,\hat u, \qquad |S_2Q| = L_2 - L_1 = \delta s$$

$$\frac{\delta s}{\lambda}, \qquad f = \frac{\delta s}{\lambda} - \left\lfloor \frac{\delta s}{\lambda} \right\rfloor, \qquad \Delta\varphi = \frac{2\pi\,\delta s}{\lambda}, \qquad \frac{I}{I_0} = \cos^2\frac{\Delta\varphi}{2}$$

$$I_\mathrm{far}(\theta) = \cos^2\frac{\pi b\sin\theta}{\lambda}, \qquad I_\mathrm{exact}(\theta) = \cos^2\frac{\pi\,\delta s(\theta)}{\lambda}, \qquad \delta s(\theta) = \frac{2bx}{l_1 + l_2},\ x = d\tan\theta,\ l_{1,2} = \sqrt{(x \mp b/2)^2 + d^2}$$

$$\sin\theta_m = \frac{m\lambda}{b}, \qquad x_m = d\tan\theta_m, \qquad m_\mathrm{max} = \left\lfloor \frac{b\sin 30^\circ}{\lambda} \right\rfloor, \qquad \Delta y \approx \frac{\lambda d}{b}$$

Symbols: $d$ distance from the wall to the observation line (px); $\alpha$ direction of $P$ from $M$, measured from the normal
to the wall (degrees on the slider, radians in the formulas); $b$ slit separation (px); $\lambda$ wavelength (px); $L_1$,
$L_2$ path lengths (px); $\delta s$ path difference (px); $Q$ the point on $S_2P$ at distance $L_1$ from $P$; $f$ the
fractional part of $\delta s/\lambda$ (dimensionless); $\Delta\varphi$ phase difference (rad); $I/I_0$ brightness relative to two
waves in step (dimensionless); $\theta$ direction on the plot (degrees); $m$ the order of a bright fringe.

The form $2bd\tan\alpha/(L_1+L_2)$ is used instead of $L_2 - L_1$ because subtracting two nearly equal lengths loses digits;
the note derives it in Section 3 ([page:261–263](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L261-L263)).
The far-field shortcut $b\sin\alpha$ and its error $b^2\cos^2\alpha/(8r^2)$ are Section 4; adding the two waves to get
$\cos^2$ is Section 5; slit width (not modelled by the code) is Section 6; single particles are Section 7.

## How the code computes it

**State.** The page keeps very little state of its own: `geo` (the result of `compute()`), `phase` (fraction of a wavelet
period, 0 to 1), `fps` ([page:559](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L559)).
The slider values live in the inputs and are read through the objects `dS`, `aS`, `bS`, `lS` returned by `Sim.slider`
([page:610–613](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L610-L613)). Every computed
number is written into the store `ds` (next section). All arithmetic is JavaScript double precision.

**Method.** Closed-form geometry. There is no time step for the physics, so there is nothing to make stable. Measured in Node
over every slider combination ($d$ 100–300 step 1, $\alpha$ 0–30° step 0.5, $b$ 20–80 step 1), the stored `ds` and the direct
difference `L2 - L1` differ by at most $1.35\times10^{-13}$ px (at $d = 298$, $\alpha = 14^\circ$, $b = 29$).

**On a slider change.** `Sim.slider` calls `update` on every `input` event
([page:610–613](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L610-L613),
[sim.js:162–165](../../public/scripts/sim.js#L162-L165)). `update()` runs, in this order
([page:786–792](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L786-L792)):

1. `compute()` places $S_1$, $S_2$, $P$, computes $L_1$, $L_2$, $\hat u$, $Q$ and $\delta s$, and returns them as `geo`
   ([page:621–635](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L621-L635)).
2. `drawShapes()` writes the whole `#shapes` group as one SVG string: observation line, centre normal, the wall with an 8 px gap
   at each slit (`gap = 4` each side), both paths, the construction arc and the burgundy bar $S_2Q$ (only when $\delta s > 0.05$ px),
   the $\alpha$ arc (only when $\alpha > 0.2^\circ$), the $b$ and $d$ dimension marks, the points and labels
   ([page:637–685](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L637-L685)). The sweep
   direction of the arc comes from the sign of a 2-D cross product ([page:651–653](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L651-L653)).
3. `drawWaves()` redraws the wavelets (below).
4. `drawPattern()` samples 301 directions, $\theta = 30^\circ \cdot i/300$, $i = 0 \dots 300$, evaluates $I_\mathrm{far}$ and
   $I_\mathrm{exact}$ at each, draws the filled far-field curve, the dashed exact curve, the 0/10/20/30° ticks, one "m = …" label
   per far-field bright order inside 30°, a dashed line at $\alpha$ and a dot at $I_\mathrm{exact}(\alpha)$
   ([page:709–753](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L709-L753)). Plot axes:
   $\theta$ maps to $x$ from `x0 = 56` to `x1 = 556`, $I$ maps to $y$ from `yb = 142` (0) to `yt = 24` (1)
   ([page:710–712](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L710-L712)).
5. `readouts()` fills the six readouts and the caption from stored values; `compute()` and its `storeDerived(G)` helper have already stored the geometry, derived scalars and verdict
   ([page:775–784](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L775-L784)). Verdict rule:
   `f < 0.08 || f > 0.92` gives "Constructive · bright fringe, m = round(δs/λ)", `|f − 0.5| < 0.08` gives "Destructive · dark
   fringe between m = … and …", otherwise "Partial · I/I₀ = …" ([page:758–758](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L758-L758)).
   A tolerance of 0.08 wavelengths means $\cos^2(0.08\pi) = 0.94$ at the edge of "bright".

**Each animation frame.** `Sim.clock` calls its callback every `requestAnimationFrame`, with `dt = 0` while paused and `dt` capped
at 0.05 s ([sim.js:176–197](../../public/scripts/sim.js#L176-L197)). The page's callback
([page:810–817](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L810-L817)):

1. if `dt > 0`: `phase = (phase + dt * 0.8) % 1`, so the wavelets advance 0.8 periods per second, i.e. $0.8\lambda$ px/s;
   then `drawWaves()`; then `fps` is updated as a running average of $1/\Delta t$ with weight 0.1;
2. always: the store gets `clock_t`, `wall` (`performance.now()/1000`), `fps` and `animate`.

`drawWaves()` ([page:687–707](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L687-L707))
draws, around each slit, upper half-circles of radius $r = (\text{phase} + n)\lambda$ up to 430 px, skipping $r < 1$, with
opacity $0.55(1 - r/430)$, clipped to $y \le 370$ by the `clipPath` `#above`
([page:63](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L63)). Below the wall it draws
straight lines at $y = Y_0 + (1 - \text{phase})\lambda + n\lambda$ up to 440, which move up in step with the arcs. It replaces
the `#waves` group's `innerHTML` each time. The geometry, the pattern and the readouts are not redrawn per frame.

**Precomputation and caching.** None beyond `geo`, which holds the geometry between slider changes so that `drawWaves()` can
reuse it every frame. The plot arrays are recomputed only on slider input.

## Function map

All functions live in one IIFE ([page:551–944](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L551-L944)).

| Function | Lines | What it does |
|---|---|---|
| slider `format` callbacks | [610–613](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L610-L613) | Text of the `<output>` next to each slider ("200 px", "20.0°", "13.5 px"). |
| `n(v)` | [615](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L615) | `v.toFixed(2)`: every SVG coordinate is written with two decimals. |
| `dist(p, q)` | [616](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L616) | Euclidean distance, `Math.hypot`. |
| `line`, `dot`, `text` | [617–619](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L617-L619) | Build SVG `<line>`, `<circle>`, `<text>` strings. |
| `compute()` | [621–635](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L621-L635) | Geometry: $S_1$, $S_2$, $P$, $L_1$, $L_2$, $\hat u$ (stored here), $Q$, $\delta s$. Returns `geo`. |
| `drawShapes()` | [637–685](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L637-L685) | The static construction in `#shapes`. |
| `drawWaves()` | [687–707](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L687-L707) | Wavelet arcs and incoming wave in `#waves`; stores `ring_r`, `n_rings`, `phase`. |
| `drawPattern()` with inner `X`, `Y`, `I`, `Iexact` | [709–753](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L709-L753) | Fig. 3b; stores `theta`, `I_far`, `I_exact`, `I_diff`, `m_sin`, `m_theta`, `m_x`, `m_max`. |
| `storeDerived(G)` | [755–773](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L755-L773) | Called at the end of `compute()` ([633](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L633)). Stores the five points, the slider values, `ds_direct`, `S2Q`, $b\sin\alpha$ and its error `ds_err`, the ratio, its fraction, $\Delta\varphi$, $I$, $I_\mathrm{far}(\alpha)$, the verdict, `phi_pi`, `sin_theta1`, `theta1`, `fringe_px`, `ring_speed`. |
| `readouts()` | [775–784](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L775-L784) | Fills the six readouts, the caption and the verdict from stored values; computes nothing. |
| `update()` | [786–792](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L786-L792) | The five steps above, in order. |
| `Sim.live` with inner `pt` | [795–809](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L795-L809) | Formatted strings for the walkthrough's "Now" column, read from the store. |
| clock callback | [810–817](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L810-L817) | Advances `phase`, redraws wavelets, stores clock values. |
| `anim` change listener | [818](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L818) | `clk.set(anim.checked)`: starts or stops the clock. |
| `toSvg(x, y)`, `toCss(X, Y)` | [822–823](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L822-L823) | Convert between CSS px inside `#stage` and SVG user units with `getScreenCTM()`. |
| `sliderCheck` | [823](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L823) | Check entry for a slider value: read the input now. |
| `pointCheck(q, which)` | [825–829](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L825-L829) | Recomputes the five construction points from stored `d`, `alpha`, `b`, `L1`, `ux`, `uy`. |
| `P()`, `S(q)` | [830–831](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L830-L831) | Stored point $P$ or point `q` from `pt_x`, `pt_y`. |
| `exactAt(th)` | [832–835](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L832-L835) | Recomputes $I_\mathrm{exact}(\theta)$ from stored inputs for the Check. |
| `circleCheck(q)` | [836–842](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L836-L842) | Read-back: nearest `<circle>` in `#shapes` to the stored point; passes within 0.02 units. |
| `firstFringeReadback(sine)` | [843–849](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L843-L849) | Read-back for `sin_theta1` and `theta1`: finds the "m = 1" label in `#pattern`, turns its `x` back into an angle, compares within 0.001. With no such label it returns `ok: null`. |
| `Sim.data.playing` | [852](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L852) | `clk.playing`. |
| `Sim.data.probe(x, y)` | [863–867](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L863-L867) | Nearest of the five points within 22 SVG units; returns `{ pt }`. |
| `Sim.data.inspect(ref)` | [868–876](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L868-L876) | Rows shown for a pinned point; $P$ gets $L_1$, $L_2$, $\delta s$, $\delta s/\lambda$, $\Delta\varphi$, $I/I_0$. |
| `Sim.data.locate(name, idx)` | [877–881](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L877-L881) | Where `pt_x`/`pt_y` elements and `ring_r` radii are drawn, in CSS px. |
| `Sim.data.check.*` | [882–918](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L882-L918) | One recomputation per stored variable from stored inputs; the four slider entries read the input element now. |
| `Sim.data.drawn.*` | [919–938](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L919-L938) | Read-backs: `sin_theta1`, `theta1` (the m = 1 label), `L1`, `L2`, `phi_pi` (the visible readouts), `pt_x`/`pt_y` (circle centres), `I` (dot height), `ds` (bar length). |
| `Sim.data.round` callbacks | [940–940](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L940-L940) | Label, length 10, recorded point $P$. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Distance d | `d` | 100–300 px, step 1, default 200 ([page:90](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L90)) | `dS.value` in `compute()` ([page:622](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L622)); moves $P$ and the observation line; `update()`. |
| Angle α | `alpha` | 0–30°, step 0.5, default 20 ([page:94](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L94)) | `aS.value * DEG`; `update()`. |
| Slit separation b | `b` | 20–80 px, step 1, default 40 ([page:98](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L98)) | `bS.value`; slit positions, $\delta s$, pattern; `update()`. |
| Wavelength λ | `lambda` | 8–40 px, step 0.5, default 13.5 ([page:106](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L106)) | `lS.value` as `geo.lambda`; wavelet spacing, pattern, verdict; `update()`. |
| Animate wavelets | `anim` | checkbox, checked ([page:108](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L108)) | `clk.set(anim.checked)` ([page:818](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L818)). |

Readouts ([page:111–119](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L111-L119)): `r-l1` and
`r-l2` ($L_1$, $L_2$, 1 decimal), `r-ds` ($\delta s$, 2 decimals), `r-ff` ($b\sin\alpha$), `r-m` ($\delta s/\lambda$), `r-phi`
($\Delta\varphi$ in units of $\pi$, read from the stored `phi_pi`), `verdict`; the caption span `cap-ds` repeats $\delta s$
([page:776–783](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L776-L783)). The data panel adds
a "Data" tab and a "Read values" button in the caption of the first figure (the one whose stage has `id="stage"`)
([datalog.js:896–897](../../public/scripts/datalog.js#L896-L897)); the walkthrough adds "Hold the numbers"
([sim.js:329](../../public/scripts/sim.js#L329)).

## What the page writes into the data store

`Sim.dataset({ title: 'Double-slit interference', attrs })` ([page:562](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L562))
with attrs `figure: 3`, `page`, `X0`, `Y0`, `length_unit` and `pattern_axes: 'x0 = 56, x1 = 556, yb = 142, yt = 24, 0° to 30°'`.
Declarations are at [page:563–608](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L563-L608);
each carries `symbol`, `units`, `long_name`, `computed_in`, `formula`, `digits`. How the store works: [dataset.md](../scripts/dataset.md).

**Dimensions.** `pt` = 5 (the points $S_1, S_2, M, P, Q$, in that order) ([page:568](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L568));
`th` = 301 ([page:589](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L589)); `m`, resized to
the number of orders on each `drawPattern()` ([page:738](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L738));
`ring`, resized to the number of arcs per slit on each `drawWaves()` ([page:698](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L698)).

| Variables | Dims · type | Written at |
|---|---|---|
| `d`, `alpha_deg`, `alpha`, `b`, `lambda` | scalar float | [page:765](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L765) |
| `ux`, `uy` | scalar float | [page:631](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L631), in `compute()` |
| `pt_x`, `pt_y` | `pt` · Float64Array | [page:762–764](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L762-L764) |
| `L1`, `L2` | scalar float | [page:626](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L626), in `compute()`, on the line after `dist()` |
| `ds` | scalar float | [page:628](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L628), in `compute()`, on the line after the formula |
| `ds_direct` (= `L2 − L1`), `S2Q` (= `dist(S2, Q)`) | scalar float | [page:766](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L766) |
| `b_sin_a`, `ds_err`, `ratio`, `frac`, `phi` | scalar float | [page:767](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L767) |
| `I`, `I_far_P`, `verdict` (str) | scalar | [page:768](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L768) |
| `phi_pi` ($\Delta\varphi/\pi$; the `r-phi` readout and the walkthrough read it) | scalar float | [page:769](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L769) |
| `sin_theta1` ($\lambda/b$), `theta1` ($\arcsin(\lambda/b)$ in degrees, NaN when $\lambda > b$) | scalar float | [page:770–771](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L770-L771) |
| `fringe_px` ($\lambda d/b$), `ring_speed` ($0.8\lambda$) | scalar float | [page:772](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L772) |
| `theta` (coordinate), `I_far`, `I_exact`, `I_diff` | `th` · Float64Array | [page:723](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L723), touched at 718 |
| `m_sin` (coordinate), `m_theta`, `m_x` | `m` · Float64Array | [page:742](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L742), touched at 737 |
| `m_max` | scalar int, `nm − 1` | [page:746](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L746) |
| `ring_r` (radii around $S_1$ only; $S_2$ has the same radii), `n_rings`, `phase` | `ring` · Float64Array; scalars | [page:699–701](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L699-L701) |
| `clock_t`, `wall`, `fps`, `animate` | scalars | [page:816](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L816), every frame |

`ds_direct` and `S2Q` exist only for the store: they let the Check compare three ways of getting $\delta s$ (formula,
subtraction, the drawn bar), as the note says ([page:508](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L508)).
Measured in Chromium at the defaults: `ds` = 13.627724988366344, `ds_direct` = 13.627724988366339, `S2Q` = 13.627724988366323 px.

**The panel spec** `Sim.data` ([page:850–942](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L850-L942);
contract at [datalog.js:9–31](../../public/scripts/datalog.js#L9-L31), explained in [datalog.md](../scripts/datalog.md)):
`kicker: 'Fig. 3 · data'`, `file: 'fig3-double-slit'`, six groups (Physical parameters, Geometry, Path difference and phase,
Intensity, Bright fringes, Animation), `rowLabel` for `pt` (S₁ … Q) and `m` ("m = j"), `colour` maps for `I_far` and `I_exact`
through `Sim.colourMap` (defined in [datalog.js:103](../../public/scripts/datalog.js#L103)). The probe works in SVG units, so its
22-unit catch radius is 22 × (stage width / 600) CSS px: 28 px on the 770 px stage measured at a 1440 px window.

**Read-backs (`drawn`).** `pt_x`/`pt_y`: the nearest `<circle>` to the stored point, within 0.02 units; $Q$ is not drawn when
$\delta s \le 0.05$ px. `I`: the `cy` of the only `circle[r="5.5"]` in `#pattern`, converted back with `(142 − cy)/(142 − 24)`,
tolerance $2\times10^{-3}$. `ds`: the length of the only `<line>` with `stroke-width="5"` whose stroke is not ink, tolerance 0.03 px
([page:919–938](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L919-L938)). All three pass at the
defaults in Chromium (dot 0.9992 against 0.9991; bar 13.628 px; $P$ at (227.21, 170.00)). `L1`, `L2` and `phi_pi` are read back
from the visible readouts `r-l1`, `r-l2`, `r-phi`, which must show the stored value rounded as the readout rounds it
([page:921–923](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L921-L923)). `sin_theta1` and `theta1` are read back by `firstFringeReadback()`
([page:843–849](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L843-L849)): it finds the "m = 1" label in `#pattern`, turns its `x` back into an angle with
$\theta = 30^\circ\,(x - 56)/500$, and passes within 0.001. The label exists only while the first bright fringe lies inside
the 0°–30° plot, that is while $\lambda/b \le \sin 30^\circ = 0.5$. Otherwise the function returns `ok: null` with "outside
the 0°–30° plot" ([page:844](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L844)), and the panel shows a neutral "Not in the picture at the moment, so there is nothing to
read back.", not a failure ([datalog.js:836](../../public/scripts/datalog.js#L836)). At the defaults ($\lambda/b = 0.3375$) the
label sits at $\theta_1 = 19.72^\circ$.

**One round** (`Sim.data.round`, [page:940–940](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L940-L940)):
ten seconds of `wall` time, `mode: 'change'`. In this mode the panel takes a sample only when one of the round columns
`d, alpha_deg, b, lambda, L1, L2, ds, ratio, I` changes ([datalog.js:1105–1109](../../public/scripts/datalog.js#L1105-L1109)), so the reader
records by moving sliders; the recorded point is $P$ (`{ pt: 3 }`). The page has no `play` hook, and none is needed: `wall` runs
whether or not the wavelets move.

**`Sim.live()`** ([page:795–809](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L795-L809))
returns strings for the walkthrough keys `d`, `a`, `b`, `P`, `S1`, `L1`, `L2`, `ds`, `dsid`, `u`, `Q`, `S2Q`, `lam`, `m`, `phi`,
`I`, `ff`, `Iff`, `sinm`, `t1`, `fr`, `verdict`. The walkthrough polls it every 200 ms ([sim.js:403](../../public/scripts/sim.js#L403)).

## Page structure

**Head** ([page:3–29](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L3-L29)): title "Double-Slit
Interference · Numa Koudsie", description, the security policy and referrer rule ([build-and-deploy.md](../build-and-deploy.md#security)), then stylesheets `../styles/sim.css`, `../styles/data.css`,
`../styles/fold.css` (sim.css imports the fonts, KaTeX's CSS and paper.css: [sim.css:8–9](../../public/styles/sim.css#L8-L9)), an
inline SVG favicon, and an inline `<style>` with the label classes `.svg-lbl`, `.svg-lbl--acc`, `.svg-mono`, `.svg-num`, `.svg-m`
(larger below 560 px) and `.verdict` ([page:15–28](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L15-L28)).
See [styles.md](../styles.md).

**Body.** The top bar: one span holding the Phyein Usul logo (a link to `../index.html` with `../images/phyein-usul-mark.svg`,
87 × 48) and "← All simulations" ([page:32](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L32)), then the hand-written Fig. 1–11 links, Fig. 3 marked `aria-current`
([page:31–47](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L31-L47)); the heading
"Fig. 3 · wave optics · wave–particle duality" ([page:51–55](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L51-L55));
the grid with two figures, `#stage` holding `svg#geo` (viewBox 600 × 440, groups `#waves` under `#shapes`) and `svg#pattern`
(viewBox 600 × 180) ([page:57–83](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L57-L83)); the
control panel ([page:85–127](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L85-L127)); the
lecture note `<article class="paper" id="paper">` ([page:130–537](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L130-L537));
`<section class="walk" id="walk" data-walk="slit">` ([page:539](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L539));
the footer.

**Scripts, in load order** ([page:547–946](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L547-L946)):
`fold.js`, `sim.js`, `dataset.js`, the page's inline script, `datalog.js`. At boot `sim.js` loads `walk/slit.js` from the
`data-walk` key ([sim.js:481–490](../../public/scripts/sim.js#L481-L490)) and KaTeX for the note ([sim.js:431–432](../../public/scripts/sim.js#L431-L432)).
See [sim.md](../scripts/sim.md), [walk.md](../scripts/walk.md), [fold.md](../scripts/fold.md), [pages.md](../pages.md).

**Lecture note.** Ten sections, each a `.psec` that `fold.js` turns into a fold ([fold.js:314](../../public/scripts/fold.js#L314)),
13 numbered equations (`\tag{1}` to `\tag{13}`), five inline SVG figures, two exercises and one key-result box:

| § | id | Title | Contents |
|---|---|---|---|
| 1 | `p-picture` | Bright and dark from one source | Loudspeakers, soap films, Young 1801–1803, single photons ([154](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L154)) |
| 2 | `p-model` | The model | Coordinates (1), assumptions, slider ranges; Figure 1, the construction ([163](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L163)) |
| 3 | `p-exact` | The exact path difference | (2), (3); why the code avoids $L_2 - L_1$ ([257](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L257)) |
| 4 | `p-far` | The far field | (4) $b\sin\alpha$; 4.1 ★ error (5); Figure 2; Exercise 4.1 ([267](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L267)) |
| 5 | `p-adding` | Adding the two waves | (6)–(9), the bright/dark box; Figure 3, phasors; Exercise 5.1 ([334](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L334)) |
| 6 | `p-width` | Slits with a width ★ | (10), (11) single-slit envelope; Figure 4 ([387](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L387)) |
| 7 | `p-quantum` | One particle at a time | (12), (13); Figure 5, 20/200/2000 simulated arrivals ([454](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L454)) |
| 8 | `p-method` | How the page computes | The steps of this document in prose ([498](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L498)) |
| 9 | `p-screen` | From lengths to pixels | SVG layout, wavelets, scale of the pixel ([511](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L511)) |
| 10 | `p-limits` | What the model leaves out | Limits, with the polarisation estimate (light polarised in the drawing's plane: the paths meet at $\gamma = 11^\circ$ at the default dark fringe, which keeps $\sin^2(\gamma/2) = 0.9\,\%$ of $I_0$); 10.1 Further reading, each item linked (Hecht, Halliday–Resnick–Walker, Feynman I-29, I-30, III-1, Young 1804) ([518](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L518)) |

**Walkthrough** `walk/slit.js`, seven steps: where everything sits; two paths and their exact difference; the burgundy bar,
point Q; phase difference and brightness; far field; fringe orders on the pattern; the verdict line
([slit.js:9–226](../../public/scripts/walk/slit.js#L9-L226)). Its code excerpts quote these page lines (step 1: [622–624](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L622-L624);
step 2: [625](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L625), [627–628](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L627-L628); step 3: [629–630](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L629-L630); step 4: [756](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L756), [717–718](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L717-L718); step 5: [713](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L713), [757](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L757), [779](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L779); step 6: [740–745](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L740-L745); step 7: [758–758](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L758-L758)). Checked line by line on
15 October 2026, they match the page text. A `...` on a line of its own stands for omitted lines. Once it stands inside a line:
in step 7 ([slit.js:164](../../public/scripts/walk/slit.js#L164)) it replaces the end of page line [759](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L759), the two `m` values,
before the closing semicolon.

## Where the drawing and the store differ

- SVG coordinates are written with two decimals (`n()`, [page:615](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L615)),
  so the picture carries positions to 0.01 SVG units while the store keeps full doubles. The note says so in Section 9
  ([page:513](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L513)) and the panel's About
  paragraph says it in the page's `about` text ([page:940](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L940),
  shown by [datalog.js:229](../../public/scripts/datalog.js#L229)).
- Fig. 3b is a polyline through the 301 stored samples; between samples the line is straight.
- The construction arc, the bar $S_2Q$ and the point $Q$ are hidden when $\delta s \le 0.05$ px; the $\alpha$ arc is hidden when
  $\alpha \le 0.2^\circ$ ([page:652](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L652),
  [658](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L658)). The values are still stored.
- The wavelets are decoration: their speed ($0.8\lambda$ per second) and their fading opacity carry no physics; the note says the
  animation is slowed by about $7\times10^{14}$ ([page:514](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L514)).
- The slits are drawn as 8 px gaps but computed as points; Section 6 discusses the difference
  ([page:394](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L394)).
- The readouts round: $L_1$, $L_2$ to 0.1 px, $\delta s$ and $b\sin\alpha$ to 0.01 px, $\delta s/\lambda$ to 0.01.

## How to change it safely

- **Constants that appear more than once.** `X0 = 300`, `Y0 = 370` ([page:554](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L554))
  are also in the dataset attrs, in `pointCheck` ([page:827](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L827)),
  in the clip rectangle height 370 ([page:63](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L63))
  and in the walkthrough's first step ([slit.js:15](../../public/scripts/walk/slit.js#L15)). The plot axes 56/556/142/24 are in
  `drawPattern()`, the attrs string ([page:562](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L562))
  and `drawn.I` ([page:927](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L927)).
  The rate 0.8 is in the clock ([812](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L812)),
  `ring_speed` ([772](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L772),
  [917](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L917)), the store's attributes ([603–604](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L603-L604)) and
  the note ([508](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L508), [514](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L514)). The verdict thresholds 0.08/0.92 are in `storeDerived()` ([758–759](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L758-L759)), the attrs ([585](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L585)), the note ([504](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L504)) and walkthrough
  step 7 ([slit.js:162–163](../../public/scripts/walk/slit.js#L162-L163)).
- **Walkthrough excerpts.** If you edit any line that `slit.js` quotes (listed above), change the excerpt in the same way.
  Insert new store writes after a quoted line, never inside a quoted block.
- **Read-backs depend on drawing details.** `drawn.ds` finds the bar as the only non-ink line of width 5; `drawn.I` finds the
  dot as the only `circle[r="5.5"]` in `#pattern`; `circleCheck` takes the nearest circle. A new circle or a new thick coloured
  line breaks them silently.
- **Numbers in the lecture note** come from the defaults ($d = 200$, $\alpha = 20^\circ$, $b = 40$, $\lambda = 13.5$): 13.6277 px,
  13.6808 px, 67.5 px, 19.72°, the exercises, Figures 2, 4 and 5. Changing a default means recomputing them.
- **Re-test** after a change: load the page, open the data panel, run Check on `pt_x[3]`, `ds`, `I`, `I_far[150]`,
  `m_theta[1]`; set $b = 80$, $\lambda = 8$ (finest fringes) and $b = 20$, $\lambda = 40$ (no order inside 30°); confirm the
  walkthrough's "Now" column fills on every step.

## Notes for maintainers

1. Fixed on 2026-10-15: the fringe loop fills the tolerance-counted array length; b = 40 px, λ = 20 px gives sin θ₁ = 0.5 and θ₁ = 30° (commit [9d3175f](https://github.com/Numa1997/SiteTest/commit/9d3175f2cf50d0ad3f8792f1ee173e8ce56bab53)).
2. **Reduced motion.** `Sim.clock` starts paused when the system asks for reduced motion ([sim.js:177](../../public/scripts/sim.js#L177)),
   but the "Animate wavelets" checkbox is `checked` in the HTML ([page:108](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L108))
   and nothing syncs it to the clock. Seen in Chromium with `reducedMotion: 'reduce'`: the box is ticked, `Sim.data.playing()`
   is false. The first click on the switch does nothing visible (it sets the clock to paused again).
3. Fixed on 2026-10-15: the unread frame counter was removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
4. Fixed on 2026-10-15: the note gives the measured 500-unit intensity plot width (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
5. Fixed on 2026-10-15: a complete Chromium slider sweep gives 1.3500311979441904 × 10⁻¹³ px; the note rounds the upper bound to 1.4 × 10⁻¹³ px (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
6. Fixed on 2026-10-15: the walkthrough reads stored sin_theta1, theta1 and phi_pi (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
7. Fixed on 2026-10-15: compute stores L1, L2 and ds beside their calculation and stores derived values before drawing (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
8. Fixed on 2026-10-15: when the first bright fringe lies outside the 0°–30° plot ($\lambda/b > 0.5$), the Check of
   `sin_theta1` and `theta1` shows a neutral "Not in the picture at the moment, so there is nothing to read back." instead
   of a burgundy ✕. `firstFringeReadback()` returns `ok: null` there by design ([page:844](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L844)); the panel now
   honours it ([datalog.js:836](../../public/scripts/datalog.js#L836)) (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).

Batch D store additions: `sin_theta1 = λ/b`, `theta1 = asin(λ/b)` in degrees (NaN when λ > b), and `phi_pi = phi/π`. All three are scalars stored in `storeDerived(G)`, called by `compute()`. `firstFringeReadback()` reads the first-order label’s SVG x coordinate; outside the 0°–30° plot it reports that no label is drawn. L1, L2 and phase also have DOM readbacks.

Function map addition: `storeDerived(G)` at [755–773](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L755-L773) stores points, phase, intensity and fringe scalars; `firstFringeReadback(sine)` reads the SVG label.


## Teaching revision · 15 October 2026

Missing even orders exclude the central maximum. The note separates a photon probability amplitude from the classical field and explains the Jacobian between angular and flat-screen counting densities. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

Fixed on 2026-10-16 (second repairs): the single-photon paragraph has its picture back (each photon interferes with itself; a which-slit record removes the fringes) beside the revision's point that the classical field is not the amplitude; the dot-density paragraph gives the factor $3/4$ at $30^\circ$ ([L491](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L491)). See the [audit of the revision](../research-theory-audit.md).

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig03/`), the lead made only these changes, each on its existing line, so no line link moved: §5: λd/b = 67.5 px is the small-angle estimate; the exact first bright fringe lies 72 px out, at 19.8°, where the default P sits ([L350](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L350)); §7: why the classical intensity predicts single-photon counts for any arrangement of slits ([L491](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L491)); §8: the dashed curve's point given as a distance d tan θ from the centre line (no sign clash with §2's frame) ([L505](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L505)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).

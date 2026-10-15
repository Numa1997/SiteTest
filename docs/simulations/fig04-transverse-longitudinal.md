# Fig. 4 · Transverse and Longitudinal Waves

| | |
|---|---|
| Page | [public/simulations/Transverse and longitudinal waves.html](../../public/simulations/Transverse%20and%20longitudinal%20waves.html) (1084 lines, 197 896 bytes; 87 lines are longer than 300 characters, 83 of them in the lecture note) |
| Walkthrough | [public/scripts/walk/tl.js](../../public/scripts/walk/tl.js) (110 lines, 7 steps) |
| Thumbnail | [public/images/sims/transverse-longitudinal.webp](../../public/images/sims/transverse-longitudinal.webp) (800 × 500 px, 12 kB) |
| Catalog entry | [public/scripts/catalog.js#L99](../../public/scripts/catalog.js#L99) (`id: 'transverse-longitudinal'`, `fig: 4`, title "Transverse & Longitudinal", field `waves`, stage 1, `has: ALL`) |

In this page, "page:N" means line N of the page file above.

The reader sees one canvas with two rows of beads driven by the same travelling sine wave. In the upper row each bead moves up
and down (transverse); a thin burgundy curve runs through the wave and small tan triangles mark the crests. In the lower row
each bead, drawn as a dot on a vertical bar, moves left and right (longitudinal); the bars crowd into compressions, a burgundy
tint darkens behind them, and triangles mark the compression centres. The middle bead of each row is burgundy, so the reader
can see that it only oscillates while the pattern moves to the right. The reader sets amplitude, frequency, wavelength and the
number of beads, pauses the clock, and switches the rest marks and the followed bead on or off
([page:53–96](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L53-L96)). Every frame evaluates the exact
formula at every bead; the only quantity carried from frame to frame is the phase $\omega t$.

## The physics in one picture

**Everyday picture.** In a stadium wave every spectator stands up and sits down in their own seat, yet the wave runs round the
stands. A slinky pushed in and out shows the other kind: coils move back and forth along the slinky while bunches of coils
travel along it. Guitar strings carry the first kind, air carries only the second, rock carries both (P and S waves). The note
opens with these pictures ([page:122–130](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L122-L130)).

**Model.** A line of particles labelled by rest position $X$ along a medium 640 px long; displacement $\xi(X,t)$, small,
undamped, non-dispersive, no ends, the same $\xi$ for both rows ([page:134–143](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L134-L143)).
Lengths are pixels of the medium (px); only $A/\lambda$ fixes the shape, so the pixel is a ruler, not a physical unit. Time is
real time in seconds.

**The equations the code evaluates.**

$$\xi(X,t) = A\sin(kX - \omega t), \qquad k = \frac{2\pi}{\lambda}, \qquad \omega = 2\pi f, \qquad v = f\lambda, \qquad T = \frac{1}{f}$$

$$X_i = i\,\frac{640}{N-1}, \quad i = 0 \dots N-1, \qquad \frac{\partial\xi}{\partial t} = -A\omega\cos(kX_i - \omega t)$$

Lower row, with a capped amplitude:

$$A_\mathrm{L} = \min\left(A,\ \frac{0.8\,\lambda}{2\pi}\right), \qquad x_i = X_i + A_\mathrm{L}\sin(kX_i - \omega t), \qquad \frac{\rho}{\rho_0} = \frac{1}{1 + A_\mathrm{L}k\cos(kX_i - \omega t)}$$

$$\text{shade} = \max\left(0,\ -\cos(kX - \omega t)\right)$$

Markers: first crest and first compression centre, then every $\lambda$ along the row,

$$X_\mathrm{c} = \left(\frac{\pi/2 + \omega t}{k}\right) \bmod \lambda, \qquad X_\mathrm{p} = \left(\frac{\pi + \omega t}{k}\right) \bmod \lambda, \qquad X_\mathrm{p} - X_\mathrm{c} = \frac{\lambda}{4}$$

Time and screen:

$$\omega t \leftarrow \omega t + 2\pi f\,\Delta t, \qquad s = \frac{W - 44}{640}, \qquad x_\mathrm{screen} = 22 + sX, \qquad y_\mathrm{T} = 0.3H, \qquad y_\mathrm{L} = 0.77H$$

Symbols: $A$ amplitude (px); $f$ frequency (Hz); $\lambda$ wavelength (px); $k$ wavenumber (rad/px); $\omega$ angular frequency
(rad/s); $v$ wave speed (px/s); $T$ period (s); $N$ beads per row; $X_i$ rest position (px of the medium); $A_\mathrm{L}$ amplitude
of the lower row (px); $\rho/\rho_0$ density relative to rest (dimensionless); $\Delta t$ real time since the previous frame (s);
$W$, $H$ canvas width and height (CSS px); $s$ screen px per medium px; $y_\mathrm{T}$, $y_\mathrm{L}$ the rest lines of the two
rows (CSS px from the top).

The cap $A_\mathrm{L}k \le 0.8$ keeps $1 + A_\mathrm{L}k\cos(\dots) \ge 0.2$: neighbours never pass through each other, the densest
point is at most 5 times the rest density ([page:506–508](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L506-L508)).
The note derives $v = f\lambda$ (Section 3), the wave equation for a string, a rod and a gas (Section 4 ★), the density and the
quarter-wavelength offset (Section 5) and the energy flux (Section 6 ★).

## How the code computes it

**State.** `omegaT` (rad), `fps`, `frames` ([page:743](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L743));
the canvas object `box` from `Sim.canvas2d`, with `box.w`, `box.h` in CSS px and `box.dpr` capped at 2
([page:741](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L741), [sim.js:32–46](../../public/scripts/sim.js#L32-L46));
the checkboxes `eqBox`, `followBox` ([page:742](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L742)); the
sliders `amp`, `freq`, `lambda`, `count` ([page:793–796](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L793-L796)).
`LENGTH = 640` is the medium length ([page:738](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L738)).
Every computed number goes into the store `ds`.

**Method.** Exact evaluation of the closed-form solution. Nothing is integrated, so no error builds up in the shape of the wave.
The phase is accumulated, `omegaT += 2 * Math.PI * freq.value * dt` ([page:977](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L977)),
rather than computed as $2\pi f t$: when the reader moves the Frequency slider only the rate of growth changes, so the wave stays
continuous. With $2\pi f t$ every bead's phase would jump by $2\pi\,\Delta f\,t$ ([page:681](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L681)).
Changing $\lambda$ changes $k$ at once, so the pattern stretches about $X = 0$. `Sim.clock` passes $\Delta t = 0$ while paused and
caps $\Delta t$ at 0.05 s, so after a stall the wave resumes instead of jumping ([sim.js:176–185](../../public/scripts/sim.js#L176-L185)).
On a device set to reduce motion the clock starts paused ([sim.js:177](../../public/scripts/sim.js#L177)), and the Play button
shows "Play" from the start ([sim.js:199–207](../../public/scripts/sim.js#L199-L207)).

**Each animation frame**, the clock callback ([page:976–981](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L976-L981)):

1. advance `omegaT`;
2. if `dt > 0`, count the frame and update `fps` (running average of $1/\Delta t$, weight 0.1);
3. write `omegaT`, `periods`, `t`, `dt`, `fps`, `frames`, `playing` into the store;
4. call `draw()`.

`draw()` runs on every frame, also while paused (then $\Delta t = 0$ and the picture is the same). That is how the checkboxes and
the Particles slider, which have no listeners of their own, take effect while paused (checked in Chromium: with the clock
paused, setting Particles to 30 gave `N` = 30 in the store within 0.2 s). `draw()` in order
([page:833–960](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L833-L960)):

1. Layout and parameters: `left = 22`, `right = w − 22`, `s = (right − left)/640`, `k`, `N`, `A`, `AL = longAmp()`,
   `yT = 0.3h`, `yL = 0.77h`, `follow = floor((N − 1)/2)`; these go into the store; `ds.dim('p', N)` and the eleven per-bead
   arrays are (re)allocated ([page:834–841](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L834-L841)).
2. Clear the canvas; draw the two row titles in Plex Mono and the separator at half height
   ([page:842–852](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L842-L852)).
3. Upper row: dashed rest line (if Equilibrium positions); the burgundy curve through $X = 0, 3, \dots, 639, 640$ (215 points) at
   opacity 0.45; the crest triangles at height $y_\mathrm{T} - sA - 8$; the crest positions into `crests`
   ([page:855–879](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L855-L879)).
4. First bead loop: for each bead compute $X_i$, the phase, $\xi$, $\partial\xi/\partial t$ and the screen height, store them,
   draw the rose line from the rest line to the bead and the rest tick
   ([page:881–896](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L881-L896)).
5. Second bead loop: draw the beads on top, radius 4.5 px, the followed one 6.5 px in burgundy with a card-coloured ring
   ([page:897–905](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L897-L905)).
6. Lower row background: a linear gradient with 65 colour stops (every 10 px of the medium), opacity $0.03 + 0.2\cdot$shade,
   filling a band 68 px tall (`band = 34` each side); the compression triangles at $y_\mathrm{L} - 40$; the centres into
   `compressions` ([page:908–922](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L908-L922)).
7. Lower bead loop: compute and store $s$, $x = X + s$, the velocity, $\rho/\rho_0$, the shade and the screen $x$; draw the rest
   tick, a vertical bar 56 px tall, the bead (radius 4 px, followed 6.5 px) and, for the followed bead with rest marks on, a rose
   line from its rest tick to it ([page:924–957](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L924-L957)).
8. Mark all arrays as changed (`ds.touch`) ([page:958–959](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L958-L959)).

Cost per frame is linear in $N$ (at most 40 beads per row) plus 215 curve points and 65 gradient stops.

**On slider input** for amplitude, frequency and wavelength, `readouts()` fills the four readouts and the caption and stores the
derived scalars ([page:800–812](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L800-L812)). The page calls
`readouts()` and `draw()` once at start, and refits the canvas 80 ms after the stage changes size
([page:1077–1079](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1077-L1079), [sim.js:141–149](../../public/scripts/sim.js#L141-L149)).

**Precomputation and caching.** None. Measured in Chromium: the canvas is 770 × 481 CSS px in a 1440 × 900 window ($s$ =
1.134375) and 356 × 374 in a 390 px wide window ($s$ = 0.4875), as Section 8 of the note says
([page:693](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L693)). The aspect ratios come from
`--ar: 16 / 10` and, below 900 px, `--ar-m: 1 / 1.05` ([page:44](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L44),
[sim.css:68](../../public/styles/sim.css#L68), [sim.css:215](../../public/styles/sim.css#L215)).

## Function map

All functions live in one IIFE ([page:735–1080](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L735-L1080)).

| Function | Lines | What it does |
|---|---|---|
| slider `format` callbacks | [793–796](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L793-L796) | Text of each `<output>`: "26 px", "0.50 Hz", "220 px", "26". |
| `longAmp()` | [798](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L798) | $A_\mathrm{L} = \min(A, 0.8\lambda/2\pi)$. |
| `readouts()` | [800–812](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L800-L812) | Readouts, caption, derived scalars into the store. |
| `label(text, x, y)` | [814–820](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L814-L820) | Row title in `T.mono`, muted colour. |
| `marker(x, y)` | [822–830](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L822-L830) | Downward triangle 10 px wide, 7 px tall, tip at $(x, y)$, in `T.tanInk`. |
| `draw()` | [833–960](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L833-L960) | The whole frame, eight steps above. |
| `Sim.live` | [963–975](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L963-L975) | Strings for the walkthrough, read from the store at the followed bead. |
| clock callback | [976–981](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L976-L981) | Phase step, frame count, store, `draw()`. |
| `sliderCheck` | [832](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L832) | Check entry for a slider: read the input now. |
| `tPos(i)`, `lPos(i)` | [986–987](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L986-L987) | Screen position of bead `i` in the upper and lower row, from stored values. |
| `beadPixel(what, pt)` | [988–992](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L988-L992) | Read-back: one canvas pixel at the stored centre; passes if not transparent and luminance < 130. |
| `inputsAt(i)` | [994](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L994) | Common Check inputs $i$, $X$, $k$, $\omega t$. |
| `Sim.data.playing`, `.play` | [997](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L997), [1074](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1074) | Clock state; start the clock. |
| `Sim.data.colour.xi`, `.sL`, `.rho` | [1006](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1006) | Cell shading in the panel's tables. |
| `Sim.data.probe(x, y)` | [1007–1015](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1007-L1015) | Nearest bead centre in either row within 16 CSS px; returns `{ row: 'T' or 'L', i }`. |
| `Sim.data.inspect(ref)` | [1016–1021](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1016-L1021) | Rows for a pinned bead: 5 for the upper row, 7 for the lower row. |
| `Sim.data.locate(name, idx)` | [1022–1028](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1022-L1028) | Where an array element is drawn: the bead, a crest triangle or a compression triangle. |
| `Sim.data.check.*` | [1029–1064](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1029-L1064) | One recomputation per stored variable. |
| `Sim.data.drawn.*` | [1065–1071](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1065-L1071) | Pixel read-backs for `xi`, `yi_px` (upper bead) and `sL`, `xl_px`, `xL` (lower bead). |
| `Sim.data.round` callbacks | [1072–1073](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1072-L1073) | Label "one period, T = … s", length $T$, point: upper followed bead. |
| resize callback | [1079](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1079) | `box.fit()`. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Pause / Play | `play` | button, starts as "Pause" ([page:57](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L57)) | `Sim.playButton` toggles the clock ([page:982](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L982)); paused, $\Delta t = 0$. |
| Equilibrium positions | `eq` | checkbox, on ([page:59](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L59)) | Read in `draw()`: dashed rest line, rest ticks, rose line of the followed lower bead. |
| Follow one particle | `follow` | checkbox, on ([page:60](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L60)) | Read in `draw()`: the middle bead of each row in burgundy ([page:899](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L899), [929](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L929)). |
| Amplitude A | `amp` | 5–40 px, step 1, default 26 ([page:67](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L67)) | Upper amplitude; $A_\mathrm{L}$ through `longAmp()`; `readouts()`. |
| Frequency f | `freq` | 0.1–2 Hz, step 0.05, default 0.5 ([page:71](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L71)) | Rate of `omegaT`; $v$, $T$, $\omega$; `readouts()`. |
| Wavelength λ | `lambda` | 100–400 px, step 10, default 220 ([page:75](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L75)) | $k$, the cap, marker spacing; `readouts()`. |
| Particles | `count` | 10–40, step 1, default 26 ([page:79](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L79)) | $N$, read by `draw()` each frame; no `onInput` ([page:796](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L796)). |

Readouts ([page:83–88](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L83-L88)): `r-v` ($v$ rounded to
1 px/s), `r-t` ($T$, 2 decimals), `r-k` ($k$, 4 decimals, "/px"), `r-al` ($A_\mathrm{L}$ rounded, with " (cap)" when
$A_\mathrm{L} < A$); the caption span `cap-v` repeats $v$ ([page:801–807](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L801-L807)).
The data panel adds a "Data" tab and a "Read values" button in the figure caption ([datalog.js:589–590](../../public/scripts/datalog.js#L589-L590));
the walkthrough adds "Hold the numbers" ([sim.js:252](../../public/scripts/sim.js#L252)).

## What the page writes into the data store

`Sim.dataset({ title: 'Transverse and longitudinal waves', attrs })` ([page:746](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L746))
with attrs `figure: 4`, `page`, `LENGTH: 640`, `length_unit`, `left_margin_px: 22`. Declarations with `symbol`, `units`,
`long_name`, `computed_in`, `formula`, `digits` are at [page:747–791](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L747-L791).
How the store works: [dataset.md](../scripts/dataset.md).

**Dimensions.** `p` = $N$, set every frame ([page:839](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L839));
`c` = number of crest triangles, `floor((640 − crest)/λ + 1e-9) + 1` ([page:875–876](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L875-L876));
`cc` = number of compression triangles, the same rule ([page:918–919](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L918-L919)).

| Variables | Dims · type | Written at |
|---|---|---|
| `f`, `lambda`, `A`, `v`, `T` | scalar float | [page:809](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L809), in `readouts()` |
| `k`, `omega`, `AL`, `cap` (bool), `L_over_lam` | scalar | [page:810](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L810) |
| `Ak`, `ALk`, `Aomega` | scalar float | [page:811](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L811) |
| `omegaT`, `periods`, `t`, `dt`, `fps`, `frames`, `playing` | scalar | [page:979](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L979), every frame |
| `N`, `s_px`, `yT`, `yL`, `follow`, `box_w`, `box_h` | scalar | [page:838](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L838), every frame |
| `crests`; `crest` | `c` · Float64Array; scalar | [page:878–879](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L878-L879) |
| `X` (coordinate), `phase`, `xi`, `vxi`, `yi_px` | `p` · Float64Array | [page:885](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L885) |
| `compressions`; `comp0` | `cc` · Float64Array; scalar | [page:921–922](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L921-L922) |
| `sL`, `xL`, `vs`, `rho`, `comp`, `xl_px` | `p` · Float64Array | [page:927–928](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L927-L928) |

Units: `xi`, `sL`, `xL`, `X`, `crests`, `compressions` are in px of the medium; `yi_px`, `xl_px`, `yT`, `yL`, `box_w`, `box_h`
are CSS px of the canvas; `s_px` converts the first to the second. `yi_px` is $y_\mathrm{T} - sA\sin(\dots)$ and `xl_px` is
$22 + s\,(X + A_\mathrm{L}\sin(\dots))$, the exact centres the beads are drawn at
([page:901](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L901), [926](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L926)).
Values at the defaults, read from the store in Chromium: $k$ = 0.02856 rad/px, $v$ = 110 px/s, $T$ = 2 s, `AL` = 26, `cap` false
(the cap $0.8\lambda/2\pi$ is 28.01 px at $\lambda = 220$), `ALk` = 0.7426, followed bead 12 at $X$ = 307.2 px.

**The panel spec** `Sim.data` ([page:995–1076](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L995-L1076);
contract at [datalog.js:8–29](../../public/scripts/datalog.js#L8-L29), explained in [datalog.md](../scripts/datalog.md)):
`kicker: 'Fig. 4 · data'`, `file: 'fig4-transverse-longitudinal'`, six groups (Physical parameters, Derived physics, Time,
Particles, Crests and compressions, Drawing), and `colour` maps through `Sim.colourMap`
([datalog.js:71](../../public/scripts/datalog.js#L71)) for `xi` (scaled by $A$), `sL` (by $A_\mathrm{L}$) and `rho` ($\rho/\rho_0 - 1$
scaled by $A_\mathrm{L}k$). Every `check` recomputes its value from stored inputs, with two exceptions: the four slider entries
read the input element now, and `s_px`, `yT`, `yL` use the live `box.w`, `box.h` (Note 4).

**Read-backs (`drawn`).** `beadPixel` reads one device pixel of the canvas at the stored bead centre. It first asks whether
anything is drawn there (alpha > 0), then whether it is dark (luminance below 130; the bead fills ink `rgb(58, 50, 46)` and
burgundy `rgb(122, 31, 43)` have luminance about 51) ([page:988–992](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L988-L992)).
In Chromium at both window widths, the followed upper bead read `rgb(122, 31, 43)` and lower bead 3 read `rgb(58, 50, 46)`: both pass.

**One round** (`Sim.data.round`, [page:1072–1073](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1072-L1073)):
one period $T$ of the play time `t`, which advances only while playing. The panel samples it evenly, at most 600 samples
([datalog.js:744](../../public/scripts/datalog.js#L744), [773](../../public/scripts/datalog.js#L773)); the charted column is
`omegaT`; the recorded point is the followed bead of the upper row. If the clock is paused when recording starts, the panel calls
`Sim.data.play` ([datalog.js:762](../../public/scripts/datalog.js#L762)).

**`Sim.live()`** ([page:963–975](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L963-L975)) returns
strings for the walkthrough keys `f`, `k`, `wt`, `v`, `T`, `X`, `phase`, `xi`, `yi`, `xc`, `xp`, `AL`, `A`, `xl`, `AkL`, `rho`,
`comp`, `s`, `yT`, all read from the store at index `follow`. The phase is shown reduced to $(-\pi, \pi]$ with `Math.atan2`. The
walkthrough polls it every 200 ms ([sim.js:326](../../public/scripts/sim.js#L326)).

## Page structure

**Head** ([page:3–15](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L3-L15)): title "Transverse &amp;
Longitudinal Waves · Numa Koudsie", description, Google Fonts preconnects, stylesheets `../styles/sim.css`, `../styles/data.css`,
`../styles/fold.css`, an inline SVG favicon. No page-specific `<style>`. See [styles.md](../styles.md).

**Body.** The top bar with the Fig. 1–10 links, Fig. 4 marked `aria-current` ([page:17–32](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L17-L32));
the heading "Fig. 4 · oscillations · wave kinematics" ([page:36–40](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L36-L40));
the figure, `#stage` holding `canvas#waves`, with the caption ([page:43–51](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L43-L51));
the control panel ([page:53–96](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L53-L96)); the lecture note
`<article class="paper" id="paper">` ([page:99–721](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L99-L721));
`<section class="walk" id="walk" data-walk="tl">` ([page:723](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L723));
the footer.

**Scripts, in load order** ([page:731–1082](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L731-L1082)):
`fold.js`, `sim.js`, `dataset.js`, the page's inline script, `datalog.js`. At boot `sim.js` loads `walk/tl.js`
([sim.js:402–411](../../public/scripts/sim.js#L402-L411)) and KaTeX ([sim.js:352–353](../../public/scripts/sim.js#L352-L353)).
See [sim.md](../scripts/sim.md), [walk.md](../scripts/walk.md), [fold.md](../scripts/fold.md), [pages.md](../pages.md).

**Lecture note.** Nine sections, each a `.psec` fold ([fold.js:314](../../public/scripts/fold.js#L314)), 17 numbered equations,
four figures drawn as five inline SVG plates (Figure 2 has two), two exercises, one key-result box and one computation note:

| § | id | Title | Contents |
|---|---|---|---|
| 1 | `p-picture` | The pattern travels, the medium stays | Stadium wave, slinky, guitar, P and S waves, the liquid outer core ([122](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L122)) |
| 2 | `p-model` | The model | (1), assumptions, defaults; Figure 1, both rows at the first frame ([132](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L132)) |
| 3 | `p-kinematics` | One formula, two pictures | Figure 2, snapshot and history; (2) $v = f\lambda$; (3) particle velocity; box; Exercise 3.1 ([352](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L352)) |
| 4 | `p-equation` | Where the wave equation comes from ★ | 4.1 string (4), (5); 4.2 rod and gas (6), (7) with a computation note; 4.3 shear (8); 4.4 d'Alembert (9) ([473](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L473)) |
| 5 | `p-compress` | Compressions and rarefactions | (10) density, (11) the $\lambda/4$ offset, (12) the cap; Figures 3 and 4; Exercise 5.1 ([499](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L499)) |
| 6 | `p-energy` | Energy carried ★ | (13)–(15) ([666](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L666)) |
| 7 | `p-frame` | How the page computes a frame | (16), the phase step; the frame in words ([677](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L677)) |
| 8 | `p-screen` | From medium pixels to screen pixels | (17), sizes, drawing details, a paragraph on picture versus store ([689](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L689)) |
| 9 | `p-limits` | What the model leaves out | Limits; 9.1 Further reading (Young and Freedman, French, Stein and Wysession) ([702](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L702)) |

**Walkthrough** `walk/tl.js`, seven steps: one wave function for both rows; the transverse row; where the crests are; the
longitudinal row; why the amplitude is capped; compressions and their shading; world pixels into screen pixels
([tl.js:9–109](../../public/scripts/walk/tl.js#L9-L109)). Its excerpts quote page lines 975, 801, 804–805, 880, 899, 871–872,
798 (twice), 924, 909–910, 914, 833 and 835. Checked line by line, they match the page text, except one added comment (Note 1).
The walkthrough calls the medium's pixels "world px".

## Where the drawing and the store differ

The page says this twice: in Section 8 of the note ([page:699](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L699))
and in the panel's About text ([page:1075](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1075),
shown by [datalog.js:165](../../public/scripts/datalog.js#L165)).

- **The tint is not the density.** It follows $\max(0, -\cos(kX - \omega t))$, symmetric and capped at opacity 0.23, while the
  stored $\rho/\rho_0$ is lopsided: 3.88 at the compression centres and 0.574 in the rarefactions at the defaults. The tint is laid
  out by rest position $X$, the beads by $X + \xi$; the two agree at the compression centres. The crowding of the bars is the
  faithful picture of the density.
- **Extra sample points.** The burgundy curve (every 3 px) and the tint (every 10 px, blended linearly between stops) are drawn
  through points that are not beads and are not stored.
- **Beads are exact.** Each bead is drawn at its stored screen position; the canvas then anti-aliases the disc onto device pixels.
- **Medium versus screen units.** The stored `xi` is the displacement in medium px; the drawn displacement is $s\,\xi$ in screen px.

## How to change it safely

- **Values that must stay in sync.** The margin 22: `left` in `draw()` ([page:834](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L834)),
  `LEFT` ([page:832](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L832)), the attrs, `check.s_px` (the 44,
  [page:1061](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1061)), walkthrough step 7 and equation (17).
  `LENGTH = 640`: the attrs, Section 2 and 8, `tl.js` steps 2 and 7. Row heights 0.3 and 0.77: `draw()`, `check.yT`, `check.yL`,
  the attrs (784–785), `tl.js` step 7, Section 8. Marker offsets: crest `− 8` at [page:874](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L874)
  and in `locate` ([page:1025](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1025)); compression
  `band + 6 = 40` at [page:917](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L917) and `yL − 40` in
  `locate` ([page:1026](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1026)). The cap 0.8: `longAmp()`,
  the attrs (756), `check.AL` (1038), `tl.js` steps 4–5, equation (12) and Exercise 5.1.
- **Walkthrough excerpts.** If you edit a line `tl.js` quotes (listed above), change the excerpt the same way. Add new store
  writes after a quoted line, never inside it.
- **Read-backs.** `beadPixel` expects dark bead fills. A lighter bead colour, or a shape drawn over the bead centres, makes the
  Check fail.
- **Numbers in the lecture note** come from the defaults ($A = 26$, $f = 0.5$, $\lambda = 220$, $N = 26$): 110 px/s, 81.7 px/s,
  0.743, 3.88, 0.574, 55 px, the exercises and Figures 1–4. Changing a default means recomputing them, and Section 8's measured
  canvas sizes change if the layout or `--ar` changes.
- **Re-test** after a change: run the page at a desktop and a phone width; open the data panel and Check `xi`, `xl_px`, `rho`,
  `crest` and `comp0` at the followed bead; set $\lambda = 100$ and $A = 40$ (cap active, bars nearly touching); pause and change
  Particles (must redraw); record one round and see that it lasts one period.

## Notes for maintainers

1. Fixed on 2026-10-15: the complete longAmp source line is quoted verbatim (commit `:/^Batch C: align walkthroughs and metadata; verify excerpts and stored values$`).
2. **One name, two units.** In `draw()` the local `xi` is the screen displacement `A * s * Math.sin(...)`
   ([page:884](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L884)), while the stored `xi` on the next
   line is in medium px ([page:885](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L885)). Not a bug, but a
   trap when editing.
3. Fixed on 2026-10-15: drawing and locators share LEFT, BAND and COMPRESSION_GAP (commit `:/^Batch D: store computed results once; verify values and pixel readbacks$`).
4. Fixed on 2026-10-15: layout checks read stored box_w and box_h (commit `:/^Batch D: store computed results once; verify values and pixel readbacks$`).
5. Fixed on 2026-10-15: the transverse curve includes X = 640; the drawing path ends at the final bead with zero horizontal gap (commit `:/^Batch A: fix simulation and recording faults; verify in Chromium$`).
6. **Redraw while paused.** `draw()` runs every animation frame even when paused ([page:980](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L980),
   [sim.js:181–184](../../public/scripts/sim.js#L181-L184)). This is what makes the checkboxes and Particles work while paused,
   at the cost of about 60 identical redraws a second.


## Teaching revision · 15 October 2026

The model section now states the deliberately large default compression. Exact density from the prescribed coordinate map does not make that motion a solution of nonlinear sound dynamics. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

# Fig. 4 · Transverse and Longitudinal Waves

| | |
|---|---|
| Page | [public/simulations/Transverse and longitudinal waves.html](../../public/simulations/Transverse%20and%20longitudinal%20waves.html) (1 087 lines, 203 364 bytes; 94 lines are longer than 300 characters, 87 of them in the lecture note) |
| Walkthrough | [public/scripts/walk/tl.js](../../public/scripts/walk/tl.js) (226 lines, 11 steps) |
| Thumbnail | [public/images/sims/transverse-longitudinal.webp](../../public/images/sims/transverse-longitudinal.webp) (800 × 500 px, 11.8 kB) |
| Catalog entry | [public/scripts/catalog.js#L99](../../public/scripts/catalog.js#L99) (`id: 'transverse-longitudinal'`, `fig: 4`, title "Transverse & Longitudinal", field `waves`, stage 1, `has: ALL`) |

In this page, "page:N" means line N of the page file above.

The reader sees one canvas with two rows of beads driven by the same travelling sine wave. In the upper row each bead moves up
and down (transverse); a thin burgundy curve runs through the wave and small tan triangles mark the crests. In the lower row
each bead, drawn as a dot on a vertical bar, moves left and right (longitudinal); the bars crowd into compressions, a burgundy
tint darkens behind them, and triangles mark the compression centres. The middle bead of each row is burgundy, so the reader
can see that it only oscillates while the pattern moves to the right. The reader sets amplitude, frequency, wavelength and the
number of beads, pauses the clock, and switches the rest marks and the followed bead on or off
([page:54–97](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L54-L97)). Every frame evaluates the exact
formula at every bead; the only quantity carried from frame to frame is the phase $\omega t$.

## The physics in one picture

**Everyday picture.** In a stadium wave every spectator stands up and sits down in their own seat, yet the wave runs round the
stands. A slinky pushed in and out shows the other kind: coils move back and forth along the slinky while bunches of coils
travel along it. Guitar strings carry the first kind, air carries only the second, rock carries both (P and S waves). The note
opens with these pictures ([page:123–131](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L123-L131)).

**Model.** A line of particles labelled by rest position $X$ along a medium 640 px long; displacement $\xi(X,t)$, small,
undamped, non-dispersive, no ends, the same $\xi$ for both rows ([page:135–145](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L135-L145)).
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
point is at most 5 times the rest density ([page:508–510](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L508-L510)).
The note derives $v = f\lambda$ (Section 3), the wave equation for a string, a rod and a gas (Section 4 ★), the density and the
quarter-wavelength offset (Section 5) and the energy flux (Section 6 ★).

## How the code computes it

**State.** `omegaT` (rad), `fps`, `frames` ([page:745](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L745));
the canvas object `box` from `Sim.canvas2d`, with `box.w`, `box.h` in CSS px and `box.dpr` capped at 2
([page:743](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L743), [sim.js:32–46](../../public/scripts/sim.js#L32-L46));
the checkboxes `eqBox`, `followBox` ([page:744](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L744)); the
sliders `amp`, `freq`, `lambda`, `count` ([page:795–798](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L795-L798)).
`LENGTH = 640` is the medium length ([page:740](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L740)).
Every computed number goes into the store `ds`.

**Method.** Exact evaluation of the closed-form solution. Nothing is integrated, so no error builds up in the shape of the wave.
The phase is accumulated, `omegaT += 2 * Math.PI * freq.value * dt` ([page:979](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L979)),
rather than computed as $2\pi f t$: when the reader moves the Frequency slider only the rate of growth changes, so the wave stays
continuous. With $2\pi f t$ every bead's phase would jump by $2\pi\,\Delta f\,t$ ([page:683](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L683)).
Changing $\lambda$ changes $k$ at once, so the pattern stretches about $X = 0$. `Sim.clock` passes $\Delta t = 0$ while paused and
caps $\Delta t$ at 0.05 s, so after a stall the wave resumes instead of jumping ([sim.js:176–185](../../public/scripts/sim.js#L176-L185)).
On a device set to reduce motion the clock starts paused ([sim.js:177](../../public/scripts/sim.js#L177)), and the Play button
shows "Play" from the start ([sim.js:199–207](../../public/scripts/sim.js#L199-L207)).

**Each animation frame**, the clock callback ([page:978–983](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L978-L983)):

1. advance `omegaT`;
2. if `dt > 0`, count the frame and update `fps` (running average of $1/\Delta t$, weight 0.1);
3. write `omegaT`, `periods`, `t`, `dt`, `fps`, `frames`, `playing` into the store;
4. call `draw()`.

`draw()` runs on every frame, also while paused (then $\Delta t = 0$ and the picture is the same). That is how the checkboxes and
the Particles slider, which have no listeners of their own, take effect while paused (checked in Chromium: with the clock
paused, setting Particles to 30 gave `N` = 30 in the store within 0.2 s). `draw()` in order
([page:835–962](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L835-L962)):

1. Layout and parameters: `left = 22`, `right = w − 22`, `s = (right − left)/640`, `k`, `N`, `A`, `AL = longAmp()`,
   `yT = 0.3h`, `yL = 0.77h`, `follow = floor((N − 1)/2)`; these go into the store; `ds.dim('p', N)` and the eleven per-bead
   arrays are (re)allocated ([page:836–843](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L836-L843)).
2. Clear the canvas; draw the two row titles in Plex Mono and the separator at half height
   ([page:844–854](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L844-L854)).
3. Upper row: dashed rest line (if Equilibrium positions); the burgundy curve through $X = 0, 3, \dots, 639, 640$ (215 points) at
   opacity 0.45; the crest triangles at height $y_\mathrm{T} - sA - 8$; the crest positions into `crests`
   ([page:857–881](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L857-L881)).
4. First bead loop: for each bead compute $X_i$, the phase, $\xi$, $\partial\xi/\partial t$ and the screen height, store them,
   draw the rose line from the rest line to the bead and the rest tick
   ([page:883–898](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L883-L898)).
5. Second bead loop: draw the beads on top, radius 4.5 px, the followed one 6.5 px in burgundy with a card-coloured ring
   ([page:899–907](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L899-L907)).
6. Lower row background: a linear gradient with 65 colour stops (every 10 px of the medium), opacity $0.03 + 0.2\cdot$shade,
   filling a band 68 px tall (`band = 34` each side); the compression triangles at $y_\mathrm{L} - 40$; the centres into
   `compressions` ([page:910–924](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L910-L924)).
7. Lower bead loop: compute and store $s$, $x = X + s$, the velocity, $\rho/\rho_0$, the shade and the screen $x$; draw the rest
   tick, a vertical bar 56 px tall, the bead (radius 4 px, followed 6.5 px) and, for the followed bead with rest marks on, a rose
   line from its rest tick to it ([page:926–959](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L926-L959)).
8. Mark all arrays as changed (`ds.touch`) ([page:960–961](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L960-L961)).

Cost per frame is linear in $N$ (at most 40 beads per row) plus 215 curve points and 65 gradient stops.

**On slider input** for amplitude, frequency and wavelength, `readouts()` fills the four readouts and the caption and stores the
derived scalars ([page:802–814](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L802-L814)). The page calls
`readouts()` and `draw()` once at start, and refits the canvas 80 ms after the stage changes size
([page:1079–1081](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1079-L1081), [sim.js:141–149](../../public/scripts/sim.js#L141-L149)).

**Precomputation and caching.** None. Measured in Chromium: the canvas is 770 × 481 CSS px in a 1440 × 900 window ($s$ =
1.134375) and 356 × 374 in a 390 px wide window ($s$ = 0.4875), as Section 8 of the note says
([page:694](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L694)). The aspect ratios come from
`--ar: 16 / 10` and, below 900 px, `--ar-m: 1 / 1.05` ([page:45](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L45),
[sim.css:68](../../public/styles/sim.css#L68), [sim.css:215](../../public/styles/sim.css#L215)).

## Function map

All functions live in one IIFE ([page:737–1082](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L737-L1082)).

| Function | Lines | What it does |
|---|---|---|
| slider `format` callbacks | [795–798](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L795-L798) | Text of each `<output>`: "26 px", "0.50 Hz", "220 px", "26". |
| `longAmp()` | [800](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L800) | $A_\mathrm{L} = \min(A, 0.8\lambda/2\pi)$. |
| `readouts()` | [802–814](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L802-L814) | Readouts, caption, derived scalars into the store. |
| `label(textValue, x, y)` | [816–822](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L816-L822) | Row title in `T.mono`, muted colour. |
| `marker(x, y)` | [824–832](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L824-L832) | Downward triangle 10 px wide, 7 px tall, tip at $(x, y)$, in `T.tanInk`. |
| `draw()` | [835–962](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L835-L962) | The whole frame, eight steps above. |
| `Sim.live` | [965–977](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L965-L977) | Strings for the walkthrough, read from the store at the followed bead. |
| clock callback | [978–983](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L978-L983) | Phase step, frame count, store, `draw()`. |
| `sliderCheck` | [986](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L986) | Check entry for a slider: read the input now. |
| `tPos(i)`, `lPos(i)` | [988–989](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L988-L989) | Screen position of bead `i` in the upper and lower row, from stored values. |
| `beadPixel(what, pt)` | [990–994](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L990-L994) | Read-back: one canvas pixel at the stored centre; passes if not transparent and luminance < 130. |
| `inputsAt(i)` | [996](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L996) | Common Check inputs $i$, $X$, $k$, $\omega t$. |
| `Sim.data.playing`, `.play` | [999](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L999), [1076](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1076) | Clock state; start the clock. |
| `Sim.data.colour.xi`, `.sL`, `.rho` | [1008](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1008) | Cell shading in the panel's tables. |
| `Sim.data.probe(x, y)` | [1009–1017](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1009-L1017) | Nearest bead centre in either row within 16 CSS px; returns `{ row: 'T' or 'L', i }`. |
| `Sim.data.inspect(ref)` | [1018–1023](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1018-L1023) | Rows for a pinned bead: 5 for the upper row, 7 for the lower row. |
| `Sim.data.locate(name, idx)` | [1024–1030](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1024-L1030) | Where an array element is drawn: the bead, a crest triangle or a compression triangle. |
| `Sim.data.check.*` | [1031–1066](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1031-L1066) | One recomputation per stored variable. |
| `Sim.data.drawn.*` | [1067–1073](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1067-L1073) | Pixel read-backs for `xi`, `yi_px` (upper bead) and `sL`, `xl_px`, `xL` (lower bead). |
| `Sim.data.round` callbacks | [1075–1075](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1075-L1075) | Label "one period, T = … s", length $T$, point: upper followed bead. |
| resize callback | [1081](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1081) | `box.fit()`. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Pause / Play | `play` | button, starts as "Pause" ([page:58](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L58)) | `Sim.playButton` toggles the clock ([page:984](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L984)); paused, $\Delta t = 0$. |
| Equilibrium positions | `eq` | checkbox, on ([page:60](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L60)) | Read in `draw()`: dashed rest line, rest ticks, rose line of the followed lower bead. |
| Follow one particle | `follow` | checkbox, on ([page:61](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L61)) | Read in `draw()`: the middle bead of each row in burgundy ([page:901](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L901), [931](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L931)). |
| Amplitude A | `amp` | 5–40 px, step 1, default 26 ([page:68](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L68)) | Upper amplitude; $A_\mathrm{L}$ through `longAmp()`; `readouts()`. |
| Frequency f | `freq` | 0.1–2 Hz, step 0.05, default 0.5 ([page:72](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L72)) | Rate of `omegaT`; $v$, $T$, $\omega$; `readouts()`. |
| Wavelength λ | `lambda` | 100–400 px, step 10, default 220 ([page:76](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L76)) | $k$, the cap, marker spacing; `readouts()`. |
| Particles | `count` | 10–40, step 1, default 26 ([page:80](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L80)) | $N$, read by `draw()` each frame; no `onInput` ([page:798](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L798)). |

Readouts ([page:84–89](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L84-L89)): `r-v` ($v$ rounded to
1 px/s), `r-t` ($T$, 2 decimals), `r-k` ($k$, 4 decimals, "/px"), `r-al` ($A_\mathrm{L}$ rounded, with " (cap)" when
$A_\mathrm{L} < A$); the caption span `cap-v` repeats $v$ ([page:803–808](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L803-L808)).
The data panel adds a "Data" tab and a "Read values" button in the figure caption ([datalog.js:896–897](../../public/scripts/datalog.js#L896-L897));
the walkthrough adds "Hold the numbers" ([sim.js:329](../../public/scripts/sim.js#L329)).

## What the page writes into the data store

`Sim.dataset({ title: 'Transverse and longitudinal waves', attrs })` ([page:748](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L748))
with attrs `figure: 4`, `page`, `LENGTH: 640`, `length_unit`, `left_margin_px: 22`. Declarations with `symbol`, `units`,
`long_name`, `computed_in`, `formula`, `digits` are at [page:749–793](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L749-L793).
How the store works: [dataset.md](../scripts/dataset.md).

**Dimensions.** `p` = $N$, set every frame ([page:841](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L841));
`c` = number of crest triangles, `floor((640 − crest)/λ + 1e-9) + 1` ([page:877–878](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L877-L878));
`cc` = number of compression triangles, the same rule ([page:920–921](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L920-L921)).

| Variables | Dims · type | Written at |
|---|---|---|
| `f`, `lambda`, `A`, `v`, `T` | scalar float | [page:811](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L811), in `readouts()` |
| `k`, `omega`, `AL`, `cap` (bool), `L_over_lam` | scalar | [page:812](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L812) |
| `Ak`, `ALk`, `Aomega` | scalar float | [page:813](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L813) |
| `omegaT`, `periods`, `t`, `dt`, `fps`, `frames`, `playing` | scalar | [page:981](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L981), every frame |
| `N`, `s_px`, `yT`, `yL`, `follow`, `box_w`, `box_h` | scalar | [page:840](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L840), every frame |
| `crests`; `crest` | `c` · Float64Array; scalar | [page:880–881](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L880-L881) |
| `X` (coordinate), `phase`, `xi`, `vxi`, `yi_px` | `p` · Float64Array | [page:887](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L887) |
| `compressions`; `comp0` | `cc` · Float64Array; scalar | [page:923–924](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L923-L924) |
| `sL`, `xL`, `vs`, `rho`, `comp`, `xl_px` | `p` · Float64Array | [page:929–930](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L929-L930) |

Units: `xi`, `sL`, `xL`, `X`, `crests`, `compressions` are in px of the medium; `yi_px`, `xl_px`, `yT`, `yL`, `box_w`, `box_h`
are CSS px of the canvas; `s_px` converts the first to the second. `yi_px` is $y_\mathrm{T} - sA\sin(\dots)$ and `xl_px` is
$22 + s\,(X + A_\mathrm{L}\sin(\dots))$, the exact centres the beads are drawn at
([page:903](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L903), [928](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L928)).
Values at the defaults, read from the store in Chromium: $k$ = 0.02856 rad/px, $v$ = 110 px/s, $T$ = 2 s, `AL` = 26, `cap` false
(the cap $0.8\lambda/2\pi$ is 28.01 px at $\lambda = 220$), `ALk` = 0.7426, followed bead 12 at $X$ = 307.2 px.

**The panel spec** `Sim.data` ([page:997–1078](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L997-L1078);
contract at [datalog.js:9–31](../../public/scripts/datalog.js#L9-L31), explained in [datalog.md](../scripts/datalog.md)):
`kicker: 'Fig. 4 · data'`, `file: 'fig4-transverse-longitudinal'`, six groups (Physical parameters, Derived physics, Time,
Particles, Crests and compressions, Drawing), and `colour` maps through `Sim.colourMap`
([datalog.js:103](../../public/scripts/datalog.js#L103)) for `xi` (scaled by $A$), `sL` (by $A_\mathrm{L}$) and `rho` ($\rho/\rho_0 - 1$
scaled by $A_\mathrm{L}k$). Every `check` recomputes its value from stored inputs, with one exception: the four slider entries
read the input element now. `s_px`, `yT`, `yL` recompute from the stored `box_w`, `box_h` (Note 4).

**Read-backs (`drawn`).** `beadPixel` reads one device pixel of the canvas at the stored bead centre. It first asks whether
anything is drawn there (alpha > 0), then whether it is dark (luminance below 130; the bead fills ink `rgb(58, 50, 46)` and
burgundy `rgb(122, 31, 43)` have luminance about 51) ([page:990–994](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L990-L994)).
In Chromium at both window widths, the followed upper bead read `rgb(122, 31, 43)` and lower bead 3 read `rgb(58, 50, 46)`: both pass.

**One round** (`Sim.data.round`, [page:1075–1075](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1075-L1075)):
one period $T$ of the play time `t`, which advances only while playing. The panel samples it evenly, at most 600 samples
([datalog.js:1052](../../public/scripts/datalog.js#L1052), [1081](../../public/scripts/datalog.js#L1081)); the charted column is
`omegaT`; the recorded point is the followed bead of the upper row. If the clock is paused when recording starts, the panel calls
`Sim.data.play` ([datalog.js:1070](../../public/scripts/datalog.js#L1070)).

**`Sim.live()`** ([page:965–977](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L965-L977)) returns
strings for the walkthrough keys `f`, `k`, `wt`, `v`, `T`, `X`, `phase`, `xi`, `yi`, `xc`, `xp`, `AL`, `A`, `xl`, `AkL`, `rho`,
`comp`, `s`, `yT`, all read from the store at index `follow`. The phase is shown reduced to $(-\pi, \pi]$ with `Math.atan2`. The
walkthrough polls it every 200 ms ([sim.js:403](../../public/scripts/sim.js#L403)).

## Page structure

**Head** ([page:3–15](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L3-L15)): title "Transverse &amp;
Longitudinal Waves · Numa Koudsie", description, the security policy and referrer rule ([build-and-deploy.md](../build-and-deploy.md#security)), stylesheets `../styles/sim.css`, `../styles/data.css`,
`../styles/fold.css`, an inline SVG favicon. No page-specific `<style>`. See [styles.md](../styles.md).

**Body.** The top bar: one span holding the Phyein Usul logo (a link to `../index.html` with `../images/phyein-usul-mark.svg`,
87 × 48) and "← All simulations" ([page:18](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L18)), then the Fig. 1–11 links, Fig. 4 marked `aria-current` ([page:17–33](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L17-L33));
the heading "Fig. 4 · oscillations · wave kinematics" ([page:37–41](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L37-L41));
the figure, `#stage` holding `canvas#waves`, with the caption ([page:44–52](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L44-L52));
the control panel ([page:54–97](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L54-L97)); the lecture note
`<article class="paper" id="paper">` ([page:100–723](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L100-L723));
`<section class="walk" id="walk" data-walk="tl">` ([page:725](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L725));
the footer.

**Scripts, in load order** ([page:733–1084](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L733-L1084)):
`fold.js`, `sim.js`, `dataset.js`, the page's inline script, `datalog.js`. At boot `sim.js` loads `walk/tl.js`
([sim.js:505–514](../../public/scripts/sim.js#L505-L514)) and KaTeX ([sim.js:431–432](../../public/scripts/sim.js#L431-L432)).
See [sim.md](../scripts/sim.md), [walk.md](../scripts/walk.md), [fold.md](../scripts/fold.md), [pages.md](../pages.md).

**Lecture note.** Nine sections, each a `.psec` fold ([fold.js:314](../../public/scripts/fold.js#L314)), 17 numbered equations,
four figures drawn as five inline SVG plates (Figure 2 has two), two exercises, one key-result box and one computation note:

| § | id | Title | Contents |
|---|---|---|---|
| 1 | `p-picture` | The pattern travels, the medium stays | Stadium wave, slinky, guitar, P and S waves, the liquid outer core ([123](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L123)) |
| 2 | `p-model` | The model | (1), assumptions, defaults; Figure 1, both rows at the first frame ([133](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L133)) |
| 3 | `p-kinematics` | One formula, two pictures | Figure 2, snapshot and history; (2) $v = f\lambda$; (3) particle velocity; box; Exercise 3.1 ([354](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L354)) |
| 4 | `p-equation` | Where the wave equation comes from ★ | 4.1 string (4), (5); 4.2 rod and gas (6), (7) with a computation note; 4.3 shear (8); 4.4 d'Alembert (9) ([475](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L475)) |
| 5 | `p-compress` | Compressions and rarefactions | (10) density, (11) the $\lambda/4$ offset, (12) the cap; Figures 3 and 4; Exercise 5.1 ([501](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L501)) |
| 6 | `p-energy` | Energy carried ★ | (13)–(15) ([668](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L668)) |
| 7 | `p-frame` | How the page computes a frame | (16), the phase step; the frame in words ([679](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L679)) |
| 8 | `p-screen` | From medium pixels to screen pixels | (17), sizes, drawing details, a paragraph on picture versus store ([691](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L691)) |
| 9 | `p-limits` | What the model leaves out | Limits; 9.1 Further reading: Young and Freedman, French, Stein and Wysession, each linked to its publisher's page (French also to a lending copy at the Internet Archive), and the Feynman Lectures Vol. I ch. 47, free online; the four items stand on source lines 715–717 ([704](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L704)) |

**Walkthrough** `walk/tl.js`, seven steps: one wave function for both rows; the transverse row; where the crests are; the
longitudinal row; why the amplitude is capped; compressions and their shading; world pixels into screen pixels
([tl.js:28–216](../../public/scripts/walk/tl.js#L28-L216)). Its excerpts quote these page lines (step 1: [979](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L979), [803](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L803),
[806–807](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L806-L807); step 2: [900](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L900), [903](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L903); step 3: [875–876](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L875-L876); step 4: [800](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L800), [928](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L928); step 5: [800](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L800) again; step 6: [913–914](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L913-L914), [918](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L918); step 7: [836](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L836), [838](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L838)). Step 2's line
`X = i * LENGTH / (N - 1);` stands word for word also at [884](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L884) and [927](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L927); the one meant is [900](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L900), in the same loop as the bead it
places. Checked line by line on 15 October 2026, every excerpt matches the page text; a `...` stands for omitted lines.
The walkthrough calls the medium's pixels "world px".

## Where the drawing and the store differ

The page says this twice: in Section 8 of the note ([page:701](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L701))
and in the panel's About text ([page:1076](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1076),
shown by [datalog.js:229](../../public/scripts/datalog.js#L229)).

- **The tint is not the density.** It follows $\max(0, -\cos(kX - \omega t))$, symmetric and capped at opacity 0.23, while the
  stored $\rho/\rho_0$ is lopsided: 3.88 at the compression centres and 0.574 in the rarefactions at the defaults. The tint is laid
  out by rest position $X$, the beads by $X + \xi$; the two agree at the compression centres. The crowding of the bars is the
  faithful picture of the density.
- **Extra sample points.** The burgundy curve (every 3 px) and the tint (every 10 px, blended linearly between stops) are drawn
  through points that are not beads and are not stored.
- **Beads are exact.** Each bead is drawn at its stored screen position; the canvas then anti-aliases the disc onto device pixels.
- **Medium versus screen units.** The stored `xi` is the displacement in medium px; the drawn displacement is $s\,\xi$ in screen px.

## How to change it safely

- **Values that must stay in sync.** The margin 22: `left` in `draw()` ([page:836](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L836)),
  `LEFT` ([page:834](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L834)), the attrs (as the 44 of `(box.w − 44) / 640`), `check.s_px` (as `2 LEFT`,
  [page:1063](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1063)), walkthrough step 7 and equation (17).
  `LENGTH = 640`: the attrs, Section 2 and 8, `tl.js` steps 2 and 7. Row heights 0.3 and 0.77: `draw()`, `check.yT`, `check.yL`,
  the attrs (785–786), `tl.js` step 7, Section 8. Marker offsets: crest `− 8` at [page:876](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L876)
  and in `locate` ([page:1027](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1027)); compression
  `BAND + COMPRESSION_GAP` = 34 + 6 = 40 at [page:919](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L919) and `yL − 40` in
  `locate` ([page:1028](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1028)). The cap 0.8: `longAmp()`,
  the attrs (757), `check.AL` (1040), `tl.js` steps 4–5, equation (12) and Exercise 5.1.
- **Walkthrough excerpts.** If you edit a line `tl.js` quotes (listed above), change the excerpt the same way. Add new store
  writes after a quoted line, never inside it.
- **Read-backs.** `beadPixel` expects dark bead fills. A lighter bead colour, or a shape drawn over the bead centres, makes the
  Check fail.
- **Numbers in the lecture note** come from the defaults ($A = 26$, $f = 0.5$, $\lambda = 220$, $N = 26$): 110 px/s, 81.7 px/s,
  0.743, 3.88, 0.574, 55 px, the exercises and Figures 1–4 (Exercise 5.1 also sets Particles to 40: the closest bars then come
  within 3.86 px, against a rest spacing of 16.41 px). Changing a default means recomputing them, and Section 8's measured
  canvas sizes change if the layout or `--ar` changes.
- **Re-test** after a change: run the page at a desktop and a phone width; open the data panel and Check `xi`, `xl_px`, `rho`,
  `crest` and `comp0` at the followed bead; set $\lambda = 100$, $A = 40$ and Particles to 40 (cap active; the closest bars come within 3.9 px: with 26 particles
  they never come nearer than 7.3 px, about as near as at the defaults, 7.0 px); pause and change
  Particles (must redraw); record one round and see that it lasts one period.

## Notes for maintainers

1. Fixed on 2026-10-15: the complete longAmp source line is quoted verbatim (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
2. **One name, two units.** In `draw()` the local `xi` is the screen displacement `A * s * Math.sin(...)`
   ([page:886](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L886)), while the stored `xi` on the next
   line is in medium px ([page:887](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L887)). Not a bug, but a
   trap when editing.
3. Fixed on 2026-10-15: drawing and locators share LEFT, BAND and COMPRESSION_GAP (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
4. Fixed on 2026-10-15: layout checks read stored box_w and box_h (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
5. Fixed on 2026-10-15: the transverse curve includes X = 640; the drawing path ends at the final bead with zero horizontal gap (commit [9d3175f](https://github.com/Numa1997/SiteTest/commit/9d3175f2cf50d0ad3f8792f1ee173e8ce56bab53)).
6. **Redraw while paused.** `draw()` runs every animation frame even when paused ([page:982](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L982),
   [sim.js:181–184](../../public/scripts/sim.js#L181-L184)). This is what makes the checkboxes and Particles work while paused,
   at the cost of about 60 identical redraws a second.


## Teaching revision · 15 October 2026

The model section now states the deliberately large default compression. Exact density from the prescribed coordinate map does not make that motion a solution of nonlinear sound dynamics. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

Fixed on 2026-10-16: the paragraph on the prescribed motion had been placed between "The simulation uses the simplest travelling wave," and equation (1); it now follows the reading of (1) ([L137](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L137)). See the [audit of the revision](../research-theory-audit.md).

## Teaching revision · 20 October 2026

Judged section by section against `notes/STANDARD.md`; clear sections untouched. Verdicts, plan and measurements:
`notes/fig04/plan.md`, `notes/fig04/measure.cjs` (the page's formulas and the built page in headless Chromium),
`notes/fig04/derive.py` (SymPy), `notes/fig04/verify.cjs`. Every change sits inside an existing line of the note, so the page
keeps 1086 lines and every line link above stays valid. No equation was added or renumbered.

- Section 2 ([L137](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L137)): $A_\mathrm{L}$ is introduced
  where it is first used (equal to $A$ at the defaults), $A_\mathrm{L}k \approx 0.743$ is said in words (neighbours close to about a
  quarter of their rest spacing), and "the coordinate map" became "the map $x = X + \xi$".
- Exercise 3.1 ([L470](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L470)): "any particle in the upper
  row"; at $\lambda = 110$ px the cap lowers $A_\mathrm{L}$ to 14 px (readout "14 px (cap)"), so the lower row's top speed does change.
- 4.2 ([L487](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L487)): $B = \gamma p$ from $pV^\gamma$ fixed.
  Computation note ([L489](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L489)): 28.97 g/mol gives
  1.2043 kg/m³, not 1.2041; 343.2 m/s unchanged.
- 4.3 ([L493](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L493)): where $K + \tfrac43 G$ comes from
  (uniaxial strain = equal strain in all directions + a pure change of shape).
- Section 5 ([L511](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L511)): why the denser half fills
  $1/2 - A_\mathrm{L}k/\pi$ of the length. Exercise 5.1 ([L664](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L664)):
  "the bars nearly touch" was not true with 26 particles (closest 7.26 px); it now sets Particles to 40 (closest 3.86 px).
- Section 6 ([L670](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L670)): the tilt energy
  $\tfrac12 F(\partial\xi/\partial X)^2$ from the stretched length.
- Section 8 ([L697](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L697)): the curve has 215 points, not
  214 (the last at $X = 640$), as step 3 of "How the code computes it" says.
- 9.1 ([L716–L718](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L716-L718)): links to the pages opened
  for each book, and the Feynman Lectures Vol. I ch. 47 added (on line 717, after Stein and Wysession).

Checked in headless Chromium at 1440 × 900 and 390 × 844: no console errors, no `.katex-error` (275 KaTeX elements in the note),
no sideways scroll, all 15 folds open.

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig04/`), the lead made only these changes, each on its existing line, so no line link moved: §2: the caveat paragraph in plain words ([L138](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L138)); §2: both rows share the phase, not ξ ([L143](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L143)); Ex. 3.1: doubling f doubles v only because the page hands you a new medium ([L471](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L471)); §4.3: the ⁴⁄₃G paragraph in three sentences ([L494](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L494)); §8: y_T named ([L695](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L695)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).

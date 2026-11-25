# `public/scripts/bg-scenes.js` and `public/styles/bg-scenes.css` · living scenes (18 November 2026)

Ten small moving pictures, each a tiny physics story drawn in the site's wine red on a canvas. They are decoration: they sit
behind or between the content, never take the pointer, and stop when out of view. Each scene lives in **its own place**; no
page shows them all in one background (the user, 18 November 2026: "Not all scenes in one background").

## How a scene is placed

Any element with `data-bg="<scene>"` gets a `canvas.bgs` as its first child. Three ready-made holders exist in `bg-scenes.css`:

| Class | What it is |
|---|---|
| `.bgs-top` | absolute, at the top of the page behind the header and title, 560 px high unless a `style="height:…"` says otherwise |
| `.bgs-aside` | absolute, in the empty half beside a page title (left of it on Arabic pages), 300 px high; shown only from 1240 px width, where that half is empty |
| `.bgs-fixed` | fixed to the window, behind everything |
| `.bgs-band` (`--low` 170 px, `--tall` 320 px, plain 260 px) | a strip in the page flow between two sections |

Attributes: `data-bg-mask` (`down`, `up`, `both`, `soft`, `softdown`, `round` (an oval fading on every side), `sides`, `none`; default `both`) fades the edges with a
CSS mask so a scene never ends in a hard line; `data-bg-alpha` scales its strength. Two more attributes serve the forest: `data-bg-under="90"` gives it that many pixels of soil below
the ground line (only above 760 px width), and `data-bg-avoid` / `data-bg-avoid-near` name the elements (the hero text and the
pendulum card) that nothing may enter: no crown, leaf, droplet or flake, and the ground line breaks where they stand. The stylesheet makes `body` transparent
(the paper colour stays on `html`) so that a canvas at `z-index:-1` is visible.

## Where each scene is

| Page | Place | Scene | What it shows |
|---|---|---|---|
| Home (`index.html`) | the land under the hero, across the whole width; tall trees only where no text stands above, low ones under the buttons; clouds in the two top corners | `forest` | three trees spread into a forest that fills the land over four to six years of two minutes; four seasons; vapour, clouds in the open corners, rain and snow; roots and fungal threads in the soil |
| Home | both side margins beside the Index and the sections, from below the forest down to the shores strip (fixed holder, drawn in page coordinates so it scrolls with the page; only where a margin is at least 90 px wide, so from about 1400 px) | `rails` | left: the forest's roots go on growing down the page; right: paper globes on threads swinging in a wind that carries a street of vortices, with the wind's lines drawn |
| Home | band before Simulations | `spin` | spinners with random speeds; a wandering field locks an island of them into step |
| Home | band above the footer | `shores` | "the shores of light": things rising out of dust |
| Simulations | the empty half beside the title (from 1240 px width; none on a narrower screen) | `powder` | iron powder lining up along the field of magnets and of a wire whose current switches on and off |
| Simulations | band above the footer | `harp` | a harmonica: each note travels out through the air as a front, delayed by distance |
| Portfolios | the empty half beside the title (left of it on the Arabic page), from 1240 px width; a small corner below that | `chip` | a chip traced block by block, wires routed, then stamped die by die over a wafer |
| Portfolios | band above the footer | `mix` | three species of different shape mix by collisions and reach one temperature |
| Lucretius | the empty space beside the title (`.bgs-aside--far`, left of it on the Arabic page, from 1240 px) | `motes` | dust trembling in a slanting sunbeam, knocked by atoms nobody sees: Lucretius' own picture (II 112-141) and Brownian motion |
| Lucretius | fixed, side margins only | `swerve` | falling atoms and the small swerve that lets them meet |
| Lucretius | band above the footer | `seeds` | seeds and seasons: each thing from its own seed |
| Scenes (`scenes.html`, since 23 November 2026) | one outlined box per scene, in order S1 to S13 | the ten page scenes, plus `roots`, `wind` and `atlas` | every scene on its own, with its text and its numbers to change (below) |

On a narrow screen the chip shrinks into the corner and the bands are lower (`@media (max-width:760px)`).

## The forest (18 November 2026, evening)

**The land.** The ground line lies 90 px above the bottom of the holder, below the hero. A tree is placed only where the free
height above its spot (up to the lowest text or card above it, minus 12 px) holds its whole crown; `fit()` grows the tree once in
memory, measures its height and half width, and scales its length down until it fits. In the margins the trees grow full; under
the buttons they stay low; under the pendulum card nothing grows. Neighbours keep a distance of 0.45 × the sum of their half widths.

**The pace (23 November 2026).** The user found the trees shooting up and the land full in 80 s. Every number of the pace is now a
named property at the top of `S.forest`, and the scenes page has a slider for each:

| Name | Value | Was | Meaning |
|---|---|---|---|
| `YEAR` | 120 s | 40 s | one year, four seasons of 30 s |
| `GROW` | 50 s | 6 s | light a seedling needs to grow up; it grows in spring and summer only, so about one growing season, a minute of the reader's time |
| `SEED` | 0.04 /s | 0.25 /s | seeds per grown tree per second of spring and summer, about 2.4 a season; most find no room |
| `FEED` | 0.25 | 1 | share of rain, rotted leaves and fungal sugar that counts towards growth |
| `START` | 3 | 1 | grown trees when the page opens (mixed ages), so the land is never bare |
| `LIFE` | 2.5 to 4 years | same | a grown tree's life |
| `FALL` | 0.15 /s | 0.45 /s | autumn: chance per second that a leaf lets go (scaled with the year) |

Measured in headless Chromium at 1600 px (`notes/home/scenes/film.cjs`): before, 2 trees at 2 s, 32 at 20 s, 39 (full) at 60 s; after,
4 at 2 s, 4 at 20 s, 14 at 60 s, still growing. At 1920 px: before 39 at 60 s, after 6.

**Spreading.** In spring and summer every grown tree throws seeds (`SEED`): two in three land near it, one in three anywhere
(carried by wind). A seed grows into a tree in `GROW` seconds of light, a little faster if rotted leaves or rain reach it. From then
on, trees that die leave gaps that new ones fill, so the picture never repeats.

**Seasons.** A year lasts `YEAR` seconds: spring (leaves bud), summer (full leaves; a few fall), autumn (leaves fall, paler), winter (bare,
snow). Snow lies on the ground in 12 px bins and on the branches above deep snow, and melts in spring and summer.

**Climate, and why the two top corners hold clouds (23 November 2026).** The user found the top left (beside the hero text) and the
top right (beside the poem and the Fig. 0 card) empty. Those are the only places on the page with open sky: `clouds()` walks the
holder in 16 px columns and, in each, measures the sky from 30 px below the top down to 30 px above the first text or card (or to
55 % of the ground height); a column with less than `OPEN` = 240 px of sky (at most 30 % of the ground height) holds no clouds. So
on a wide screen the sky is exactly the two corners, and the forest's weather lives there:
**The sky: ten kinds of cloud, built in 3D and seen from the ground (24 and 25 November 2026).** On 24 November the user asked
for each cloud to be made in 3D and then seen from the ground by changing the frame of reference; on 25 November, finding
the one kind of cloud not good enough, for every kind of cloud by shape and form: "the very large, the very long, the thin". The
sky is now a module of its own in `bg-scenes.js`, `mkSky()`, used by the forest and by the scene `atlas`.

*The eye.* It stands on the ground at the horizontal middle of the holder; the horizon is the ground line GY. A point X m to the
right, Y m up and Z m ahead is seen at x = XC + F X / Z, y = GY − F Y / Z (`proj()`), with F = 1.5 GY: the top of the picture is
34° above the horizon. A flat patch of radii (r_x, r_z) lying at height Y is seen as an ellipse F r_x / Z wide and
F r_z Y / Z² high: the further, the more edge on.

*The ten kinds* (the genera of the WMO International Cloud Atlas, by form and level; temperate latitudes: low to 2 km, middle 2 to
7 km, high 5 to 13 km). `make(kind)` builds each once, in metres, in its own frame; `paint()` carries its parts into the eye's
frame and projects them every frame.

| Kind | Height here | How it is built | How it is drawn |
|---|---|---|---|
| Cumulus (Cu), a heap | base 1 km (`HB`) | 16 to 25 round puffs on a flat base, the middle ones bigger and higher | one outline around the whole heap, soft pale lumps inside, shaded towards the base, the base's floor darker (`puffs()`) |
| Cumulonimbus (Cb), the thunder cloud, "the very large" | base 1 km, top 10.4 km | a tower of 15 storeys of six puffs, widening upward (size 1400 m per unit), and an anvil: six flat patches at its top, drawn out downwind | as a heap; the anvil pale above and dark below; rain threads under the base |
| Stratocumulus (Sc), "the very long" | 1.5 km | four parallel rolls 950 m apart, each a chain of flattened lumps every 340 m over 9 km | each lump a pale flank above a darker flat belly (`lump()`) |
| Stratus (St) | 0.3 km | five wide flat patches and nine ragged scraps at the edge | soft flat ellipses (`flat()`) |
| Nimbostratus (Ns) | 0.9 km | six large dark flat patches | soft flat ellipses, with dashed threads of rain or snow sliding down from the base (`shafts()`) |
| Altocumulus (Ac) | 4 km | a field of 11 × 9 small rounded masses 300 m apart, every other row shifted, a quarter missing | lumps; the field crowds and flattens towards the horizon |
| Altostratus (As) | 4.5 km | six broad patches and twelve long thin streaks | flat ellipses; the sun behind it a bright blur, as through ground glass |
| Cirrus (Ci), "the thin" | 9 km | five to eight threads: a small hooked head, a tail 2.5 to 5 km long that falls 400 to 900 m and drifts sideways | tapering strokes, strongest at the head |
| Cirrocumulus (Cc) | 8.5 km | a sheet of 23 × 15 grains 110 m apart, their rows waved | small dots |
| Cirrostratus (Cs) | 9.5 km | five broad pale patches and fourteen fine fibres | flat ellipses; around the sun a ring of radius F tan 22°, the halo of ice crystals |

*Two canvases.* Layers, lumps and fibres are drawn at half resolution (they are soft; a quarter of the cost); the heaps at full
resolution, each on a small canvas of its own that is drawn again only when the heap's size has changed by 2 %. Drawing is kept
inside the strips of the picture that hold open sky. Measured in headless Chromium at 1920 px (`notes/home/scenes/cost.cjs`,
software drawing, a fast year): the forest's `draw()` takes 20 to 30 ms a frame through the year; the
version before the ten kinds took 17 ms.

*The mask.* The sky is drawn whole and then cut by a soft mask built from the open-sky columns (`clouds()`): full where a
column has open sky, fading over ten columns (160 px) towards text, over 24 px above text, and over 30 % of the ground height where
only trees stand below. So a layer or a wide cloud never crosses the text and is never cut by an edge. The sky is laid under
everything else of the scene (the trees, the rain).

*Which kind when* (`SEASON`, parts of the year; each comes and goes over 4 % of a year):

| Part of the year | In the sky |
|---|---|
| spring (0 to 0.25) | cumulus; fields of altocumulus (0.04 to 0.30); cirrocumulus (0.10 to 0.27); cirrus from 0.18 |
| summer (0.25 to 0.5) | cumulus; cirrus (to 0.52); one thunder cloud |
| autumn (0.5 to 0.75) | a warm front's sequence: cirrostratus with its halo (0.47 to 0.61), altostratus (0.56 to 0.71), nimbostratus and long rain (0.66 to 0.80) |
| winter (0.75 to 1) | rows of stratocumulus (0.76 to 0.92), stratus (0.86 to 0.99) and snow |

*The cumulus and the forest's water* (unchanged from 24 November). Vapour from the leaves and from the bare ground (`SOIL`) rises
to a height in the open sky; there it joins the cumulus it reaches, or starts a new one. A cumulus keeps its water m as one
number and its size follows it smoothly, s = SIZE ∛m (settling over 5 s). Its mean droplet radius grows by condensation (`COND`);
past 0.6 px, collisions turn water into raindrops at the rate RAIN · m · (r − 0.6), which fall from under the base (Stokes:
speed 9 r² − updraft) and feed the young trees. It loses water to the dry air (`EVAP`, 60 s), and out of its season it thins away.

*The thunder cloud.* Between 0.27 and 0.34 of the year, if the cumulus together hold more water than `CB` (4), one cumulonimbus
rises 22 km away in the second-widest strip of sky: its tower grows through all levels over 9 % of a year, its anvil spreads, rain
falls under it and feeds the seedlings; it fades when autumn comes. One a year at most.

*Wind.* Each level has its own wind, wandering slowly (a random walk pulled back to zero, about a minute's memory): low `WIND`
(4 m/s) around a steady 3 m/s, middle 2.2 times that around 7 m/s, high 4 times around 14 m/s. The cumulus drift with the low
wind alone. Perspective turns the same wind into a faster drift for near clouds than for far ones. A layer cloud that leaves the
picture comes back in from the other side as a new cloud.

*The layers' own weather.* Nimbostratus rains steadily over the open sky; once winter has come (0.76) it and stratus snow.

*The sun* is not drawn, except through the two kinds that show it: a ring through cirrostratus, a blur through altostratus. It
stands in the widest strip of open sky.

Every number above is a property of `S.forest` (or of `mkSky`) with a comment; those a reader would play with have a slider on the
scenes page.

**Soil.** Leaves fall, rot into specks and sink into the soil. A seedling's root tips bend towards the nearest speck within 120 px
and take it up; each speck fades after about a minute if no root reaches it. Grown trees keep a fan of roots, drawn fainter with
depth. Fungal threads tie distant root systems; sugar runs along them from grown trees to young ones. When a tree dies its roots
and threads fade out.

On a phone the hero text covers the land, so almost nothing grows there.

## The side rails (20 November 2026)

`S.rails` reads three things from the page: the box of `data-bg-around` (`.layout`, the Index and the sections), the bottom of the
forest, and the top of `data-bg-until` (the shores strip). The two margins left and right of that box, from the forest's soil down
to the shores, are its land. It checks once a second whether the page has grown (a section opened) and extends its land.

**Left: the roots go on.** The roots start under the forest's own trees that stand in the left margin, so the soil continues
without a seam. They grow by space colonisation: water is scattered over the margin (one drop per 1100 px², thicker towards the
outer edges); every water drop within 120 px pulls its nearest root tip towards it; each tip grows 6 px per step in the mean
direction of its pulls (plus a slight downward pull and a little noise), 20 steps a second; a drop that a root reaches (within
8 px) is used up. That gives the branching of leaf veins and river beds. Thickness follows Murray's law (the cube of a parent's
radius is the sum of its children's cubes, so line width grows as the cube root of the number of tips it feeds), and sap dots
climb from the tips back up towards the trees.

**Right: paper globes in a wind, played from stored data (25 November 2026).** Barton's pendulums hung here until
23 November, pairs tied by a spring until 25 November; the user found the first fast and creepy and the second out of place, and
asked for pendulums swinging in a velocity field of wind, with the field's lines (not arrows) drawn, the problem the site had
solved before (the flows and the drag law of the double inverted pendulum page, section 13). Now a wind blows down the margin
and carries a Kármán vortex street; its lines are drawn as thin curves that slide down the page; and from each beam (one every
250 px) hang three closed globes of thin paper on threads (one, in a margin too narrow for three), which every passing vortex
swings aside while gravity brings them back.
- *The model*: `tools/sims/windpend.py`, run once on Kaggle; its docstring derives the equation of motion from the setup. Wind
  U = 1.6 m/s; vortices λ = 6 m apart in two rows h = 0.281 λ apart, sliding at c = 0.8 U, so the wind repeats every
  T = λ / c = 4.69 s; threads 1.6 m; globes of radius 0.15 m, 4 g of paper around 16.7 g of air; drag ½ ρ C_D π R² |w| w plus
  Stokes; the push of accelerating air ρV Du/Dt with added mass ½; the thread's own small drag by the site's (33) and (34).
- *Why one stored swing serves every beam*: the wind only slides, u(η, ξ, t) = u(η, ξ − c t). A beam ξ lower sees the same wind
  ξ / c later, so it plays the same stored frames with that delay. `windDraw()` does this for the beams and shifts the stored
  lines by c t; a vortex is seen reaching each beam as that beam's globes swing.
- *The lines* are streamlines, stored by the model as curves η(ξ − c t) at equal steps of the stream function: close together
  where the air is fast. Beyond the stored strip (8 m) the wind is plain and its lines are drawn straight at the same spacing.
- *Stored*: `data/sims/windpend/<date>/windpend.bin`: one settled period, 141 frames at 30 a second, three angles; then 41 lines
  of 96 points. Checks in its header: settled after 14 to 17 periods; energy balance to 1e-11; the field keeps the air
  (div u / |∇u| = 5e-11); largest swing 0.35 rad (20°); the globes never closer than 0.78 m.
- 1 m is drawn as 60 px. The page computes nothing. How the data gets here: [../kaggle-sims.md](../kaggle-sims.md).
  `tools/sims/coupled.py`, `tools/sims/barton.py` and their data stay in the repository; no page plays them.

## How it runs

One `requestAnimationFrame` loop serves all instances at no more than about 30 frames a second. An `IntersectionObserver`
switches an instance off when it leaves the window, and the loop pauses on a hidden tab. A resize re-sizes each canvas
(debounced). With `prefers-reduced-motion: reduce` nothing is mounted at all. Hidden in print. `window.__bgScenes.count`
gives the number of mounted scenes, and each holder's `__bgScene` its scene object, for tests.

Every scene is an object `{ init(), draw(dt) }` inside `mount()`, sized from its own element (`W`, `H`), with particle
numbers scaled by area. The numbers are drawn for the eye, not for measurement: these are pictures, not the site's simulations,
and they have no data panel.

## How to change it

- Move a scene: move its `<div … data-bg="…">` (keep the English page's line count; then `python3 tools/i18n/build.py`).
  The Lucretius page's holders are written by `notes/lucretius/make_page.py`.
- New scene: add `S.<name> = { init, draw }` in `mount()` and place a holder; give it a table `K` and a box on the scenes page.

## The scenes page (`scenes.html`, 23 November 2026)

One page shows every scene on its own (`notes/sims/PLAN.md`, step 5, asked for by the user): S1 forest, S2 roots, S3 paper globes
in a wind, S4 spinners, S5 shores, S6 iron powder, S7 harmonica, S8 chip, S9 mixing, S10 dust in a sunbeam, S11 the swerve,
S12 seeds, S13 a cloud atlas. Each sits in an outlined box (`.scn__stage`, 340 px; 460 px for the forest, the wind and the atlas),
with where it lives on the site, what you see, what drives it, and its numbers to change.

**The numbers to change.** Every scene declares its knobs in a table `K`, each row `[property, meaning, unit, min, max, step,
restart]`; the numbers themselves are properties of the scene (for example `S.spin.FIELD`, the pull of the rotating field). The
page's own script builds one slider per row; a slider writes the property of the running scene, and a row marked restart (numbers
that set up the picture, such as how many grains) starts the scene again through `host.__bgRestart()`. On the other pages the
same properties keep their default values.

**Three scenes exist only here.**
- `roots` is the left rail's root growth in a box (same rules: space colonisation, Murray's law, sap).
- `wind` is the right rail's globes in the wind in a box: two beams, so the delay between them shows, at a larger scale. It has no
  knob: the stored run is the motion of those globes in that wind, so it plays at real time only. Under its text the page prints
  the run's parameters and checks from the file's header.
- `atlas` is the cloud atlas: the ten kinds side by side, each at its own height and labelled, with the same builders and the same
  eye as the forest's sky. High clouds stand 13 to 17 km away, the middle ones 10 to 11 km, the low ones 5 to 7 km, the thunder
  cloud 20 km, standing through all three levels. Two things are not to scale and the page says so: the four layer kinds cover the
  whole sky in nature and only a piece of each is shown; and the ring around the sun, 22° in nature, is drawn smaller to fit.
  Knobs: the strength of the drawing, and how far the clouds drift to and fro.

The page is English only for now (`ENGLISH_ONLY` in `tools/i18n/build.py`).

## The note on the home page

Above the footer, a closed `details.bgs-note` ("What moves behind this page") gives one plain sentence per scene of the home page
(forest and its sky, roots, paper globes in the wind, spinners, shores) and links to the scenes page; German and Arabic through `tools/i18n/build.py`.
- Checked in headless Chromium at 1920, 1600, 1100 and 390 px, home (English, German, Arabic), scenes, simulations, Portfolios and
  Lucretius pages: no page errors, no sideways scroll; with reduced motion nothing is mounted (`notes/home/scenes/check.cjs`).

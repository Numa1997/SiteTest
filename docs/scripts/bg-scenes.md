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
| Home | both side margins beside the Index and the sections, from below the forest down to the shores strip (fixed holder, drawn in page coordinates so it scrolls with the page; only where a margin is at least 90 px wide, so from about 1400 px) | `rails` | left: the forest's roots go on growing down the page; right: pairs of pendulums tied by a weak spring (beats) |
| Home | band before Simulations | `spin` | spinners with random speeds; a wandering field locks an island of them into step |
| Home | band above the footer | `shores` | "the shores of light": things rising out of dust |
| Simulations | the empty half beside the title (from 1240 px width; none on a narrower screen) | `powder` | iron powder lining up along the field of magnets and of a wire whose current switches on and off |
| Simulations | band above the footer | `harp` | a harmonica: each note travels out through the air as a front, delayed by distance |
| Portfolios | the empty half beside the title (left of it on the Arabic page), from 1240 px width; a small corner below that | `chip` | a chip traced block by block, wires routed, then stamped die by die over a wafer |
| Portfolios | band above the footer | `mix` | three species of different shape mix by collisions and reach one temperature |
| Lucretius | the empty space beside the title (`.bgs-aside--far`, left of it on the Arabic page, from 1240 px) | `motes` | dust trembling in a slanting sunbeam, knocked by atoms nobody sees: Lucretius' own picture (II 112-141) and Brownian motion |
| Lucretius | fixed, side margins only | `swerve` | falling atoms and the small swerve that lets them meet |
| Lucretius | band above the footer | `seeds` | seeds and seasons: each thing from its own seed |
| Scenes (`scenes.html`, since 23 November 2026) | one outlined box per scene, in order S1 to S12 | all ten, plus `roots` and `pairs` | every scene on its own, with its text and its numbers to change (below) |

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
- In spring and summer the leaves of tall trees breathe vapour, and the bare ground under open sky gives off a little more (`SOIL`,
  0.5 per second per 100 px), so the corners cloud over even before tall trees stand beneath them.
- The vapour rises to a random height in its column's sky and becomes a droplet that joins the nearest cloud within 160 px, or
  starts one. A cloud drifts with a slowly wandering wind and turns back where the open sky ends; it is drawn as one body, five to
  eight round puffs filled once, sized by the water it holds (w = 16 + 26 ∛(Σ r³) px), with its droplets as dots inside.
- Droplets grow slowly by condensation (`COND` = 0.006 px/s) and merge when they touch, with the chance `EFF` = 0.001 per touch per
  1/30 s (collision efficiency), volume kept, r = (r₁³ + r₂³)^⅓. Clouds that touch merge too.
- A droplet falls at 9 r² − u px/s (Stokes' law, u the updraft); once it beats the updraft it leaves its cloud and falls as rain,
  which feeds the young trees within 70 px of where it lands.
- In winter the clouds give their water up as snow, slowly (12 % of droplets a second), so the corners thin out in winter and fill
  again in spring. A page opens with a few clouds already there (one per 60 000 px² of open sky).
On a screen narrower than 761 px there is no sky (the hero covers the land).

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

**Right: pendulums tied by a spring, played from stored data (23 November 2026).** Barton's pendulums were here until 23 November
2026; the user found them fast, thin and creepy, and they never visibly gave their motion to each other. Now each beam (one every
250 px) carries as many pairs as the margin holds (a pair takes its pivot spacing, its swing and 30 px); in each pair two
pendulums, 1.5 m long and drawn at 80 px per metre, are joined by a weak spring drawn as a zigzag, and the swing drains from one
bob into the other and back every 27 s. The motion is computed once on Kaggle by `tools/sims/coupled.py` (two pendulums of length
L and mass m, a spring of stiffness k at the distance a below the pivots, pivots d apart; the full nonlinear equations, DOP853; k
solved by shooting so that one stored loop closes exactly) and stored as `data/sims/coupled/<date>/coupled.bin`. The page draws
the stored frame nearest in time, at real time, each pair from its own random moment of the loop; it computes nothing. How the
data gets here: [../kaggle-sims.md](../kaggle-sims.md). `tools/sims/barton.py` and its data stay in the repository until the new
pendulums are verified live; no page plays them.

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

One page shows every scene on its own (`notes/sims/PLAN.md`, step 5, asked for by the user): S1 forest, S2 roots, S3 two pendulums
and a spring, S4 spinners, S5 shores, S6 iron powder, S7 harmonica, S8 chip, S9 mixing, S10 dust in a sunbeam, S11 the swerve,
S12 seeds. Each sits in an outlined box (`.scn__stage`, 340 px; 460 px for the forest and the pendulums), with where it lives on
the site, what you see, what drives it, and its numbers to change.

**The numbers to change.** Every scene declares its knobs in a table `K`, each row `[property, meaning, unit, min, max, step,
restart]`; the numbers themselves are properties of the scene (for example `S.spin.FIELD`, the pull of the rotating field). The
page's own script builds one slider per row; a slider writes the property of the running scene, and a row marked restart (numbers
that set up the picture, such as how many grains) starts the scene again through `host.__bgRestart()`. On the other pages the
same properties keep their default values, so nothing there changed.

**Two scenes exist only here.** `roots` is the left rail's root growth in a box (same rules: space colonisation, Murray's law, sap).
`pairs` is the right rail's pendulums, one large pair, playing the same stored file, with each pendulum's energy over the loop drawn
underneath, E_i = m g L (1 − cos θ_i) + ½ m L² θ_i'², θ_i' from the neighbouring stored frames: a reading of the stored motion, not
a second simulation. It has no knob: the stored run is the motion of those pendulums, so it plays at real time only. Under its text
the page prints the run's parameters and checks from the file's header.

The page is English only for now (`ENGLISH_ONLY` in `tools/i18n/build.py`).

## The note on the home page

Above the footer, a closed `details.bgs-note` ("What moves behind this page") gives one plain sentence per scene of the home page
(forest, roots, pendulums, spinners, shores) and links to the scenes page; German and Arabic through `tools/i18n/build.py`.
- Checked in headless Chromium at 1920, 1600, 1100 and 390 px, home (English, German, Arabic), scenes, simulations, Portfolios and
  Lucretius pages: no page errors, no sideways scroll; with reduced motion nothing is mounted (`notes/home/scenes/check.cjs`).

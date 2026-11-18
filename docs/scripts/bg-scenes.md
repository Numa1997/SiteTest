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
| Home (`index.html`) | the land under the hero, across the whole width; tall trees only where no text stands above, low ones under the buttons | `forest` | one tree spreads into a forest that fills the land within about two years; four seasons; vapour, clouds, rain and snow; roots and fungal threads in the soil |
| Home | band before Simulations | `spin` | spinners with random speeds; a wandering field locks an island of them into step |
| Home | band above the footer | `shores` | "the shores of light": things rising out of dust |
| Simulations | the empty half beside the title (from 1240 px width; none on a narrower screen) | `powder` | iron powder lining up along the field of magnets and of a wire whose current switches on and off |
| Simulations | band above the footer | `harp` | a harmonica: each note travels out through the air as a front, delayed by distance |
| Portfolios | the empty half beside the title (left of it on the Arabic page), from 1240 px width; a small corner below that | `chip` | a chip traced block by block, wires routed, then stamped die by die over a wafer |
| Portfolios | band above the footer | `mix` | three species of different shape mix by collisions and reach one temperature |
| Lucretius | the empty space beside the title (`.bgs-aside--far`, left of it on the Arabic page, from 1240 px) | `motes` | dust trembling in a slanting sunbeam, knocked by atoms nobody sees: Lucretius' own picture (II 112-141) and Brownian motion |
| Lucretius | fixed, side margins only | `swerve` | falling atoms and the small swerve that lets them meet |
| Lucretius | band above the footer | `seeds` | seeds and seasons: each thing from its own seed |

On a narrow screen the chip shrinks into the corner and the bands are lower (`@media (max-width:760px)`).

## The forest (18 November 2026, evening)

**The land.** The ground line lies 90 px above the bottom of the holder, below the hero. A tree is placed only where the free
height above its spot (up to the lowest text or card above it, minus 12 px) holds its whole crown; `fit()` grows the tree once in
memory, measures its height and half width, and scales its length down until it fits. In the margins the trees grow full; under
the buttons they stay low; under the pendulum card nothing grows. Neighbours keep a distance of 0.45 × the sum of their half widths.

**Spreading.** It starts from one grown tree. In spring and summer every grown tree throws a seed about 4 times a minute: two in
three land near it, one in three anywhere (carried by wind). A seed grows into a tree in about 6 s of light, faster if rotted
leaves or rain reach it. Trees live 2.5 to 4 years. The land is full after about two years (some 35 to 40 plants at 1600 px); from
then on, trees that die leave gaps that new ones fill, so the picture never repeats.

**Seasons.** A year lasts 40 s: spring (leaves bud), summer (full leaves; a few fall), autumn (leaves fall, paler), winter (bare,
snow). Snow lies on the ground in 12 px bins and on the branches above deep snow, and melts in spring and summer.

**Climate.** In spring and summer the leaves of tall trees with open sky above them breathe vapour, which rises to a cloud layer
(about 16 % of the ground height). There the droplets grow by condensation (0.06 px/s) and by collision: two droplets that touch
merge with their volume kept, r = (r₁³ + r₂³)^⅓. A droplet falls at 9 r² − u px/s (Stokes' law, u the updraft), so only merged
drops beat the updraft and fall as rain, which feeds the young trees within 70 px of where it lands. In winter the clouds give up
their water as snowflakes. More forest means more vapour, more cloud and more rain: a full forest makes much of its own weather.

**Soil.** Leaves fall, rot into specks and sink into the soil. A seedling's root tips bend towards the nearest speck within 120 px
and take it up; each speck fades after about a minute if no root reaches it. Grown trees keep a fan of roots, drawn fainter with
depth. Fungal threads tie distant root systems; sugar runs along them from grown trees to young ones. When a tree dies its roots
and threads fade out.

On a phone the hero text covers the land, so almost nothing grows there.

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
- New scene: add `S.<name> = { init, draw }` in `mount()` and place a holder.
- Checked in headless Chromium at 1600 and 390 px, English and Arabic: no page errors, no sideways scroll, text readable.

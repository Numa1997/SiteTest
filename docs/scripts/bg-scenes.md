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
CSS mask so a scene never ends in a hard line; `data-bg-alpha` scales its strength. Two more attributes serve the forest: `data-bg-under="150"` gives it that many pixels of soil below
the ground line (only above 760 px width), and `data-bg-avoid` / `data-bg-avoid-near` name elements whose columns stay free of
trees (130 px and 34 px of clearance), so that crowns and falling leaves never cross the words; a leaf blown over the text melts away. The stylesheet makes `body` transparent
(the paper colour stays on `html`) so that a canvas at `z-index:-1` is visible.

## Where each scene is

| Page | Place | Scene | What it shows |
|---|---|---|---|
| Home (`index.html`) | behind the hero, trees only where no text stands; from 761 px wide the soil reaches 150 px below the hero | `forest` | unique trees shed leaves that feed their neighbours' seedlings; trees age, fall and are replaced; below the ground their roots grow, and fungal threads tie distant root systems so that grown trees feed young ones |
| Home | band before Simulations | `spin` | spinners with random speeds; a wandering field locks an island of them into step |
| Home | band above the footer | `shores` | "the shores of light": things rising out of dust |
| Simulations | the empty half beside the title (from 1240 px width; none on a narrower screen) | `powder` | iron powder lining up along the field of magnets and of a wire whose current switches on and off |
| Simulations | band above the footer | `harp` | a harmonica: each note travels out through the air as a front, delayed by distance |
| Portfolios | the empty half beside the title (left of it on the Arabic page), from 1240 px width; a small corner below that | `chip` | a chip traced block by block, wires routed, then stamped die by die over a wafer |
| Portfolios | band above the footer | `mix` | three species of different shape mix by collisions and reach one temperature |
| Lucretius | behind the title | `letters` | letters drifting into words, the poem's own picture of atoms |
| Lucretius | fixed, side margins only | `swerve` | falling atoms and the small swerve that lets them meet |
| Lucretius | band above the footer | `seeds` | seeds and seasons: each thing from its own seed |

On a narrow screen the chip shrinks into the corner and the bands are lower (`@media (max-width:760px)`).

## The forest's soil (18 November 2026)

Leaves fall, rot into specks and sink into the soil. A seedling's root tips bend towards the nearest speck within 120 px and take it
up; each speck fades after about a minute if no root reaches it. Grown trees keep a fan of roots (a tap root, and side roots that
fork every few segments and turn sideways near the bottom of the soil), drawn fainter with depth. Every 1.5 s the scene may tie two
root systems far apart with a thin thread (at most nine). A thread grows in about 10 s; then sugar runs along it from a grown tree to
a young one and adds to the young tree's food, the way mycorrhizal networks link trees in a real wood. When a tree dies its roots
and threads fade out over a few seconds. On a 1280 px screen only the narrow column right of the pendulum card is free, so the
forest there is thin; on a phone nothing changed.

## How it runs

One `requestAnimationFrame` loop serves all instances at no more than about 30 frames a second. An `IntersectionObserver`
switches an instance off when it leaves the window, and the loop pauses on a hidden tab. A resize re-sizes each canvas
(debounced). With `prefers-reduced-motion: reduce` nothing is mounted at all. Hidden in print. `window.__bgScenes.count`
gives the number of mounted scenes, for tests.

Every scene is an object `{ init(), draw(dt) }` inside `mount()`, sized from its own element (`W`, `H`), with particle
numbers scaled by area. The numbers are drawn for the eye, not for measurement: these are pictures, not the site's simulations,
and they have no data panel.

## How to change it

- Move a scene: move its `<div … data-bg="…">` (keep the English page's line count; then `python3 tools/i18n/build.py`).
  The Lucretius page's holders are written by `notes/lucretius/make_page.py`.
- New scene: add `S.<name> = { init, draw }` in `mount()` and place a holder.
- Checked in headless Chromium at 1600 and 390 px, English and Arabic: no page errors, no sideways scroll, text readable.

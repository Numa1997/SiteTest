# How the site fits together

This page is the map. Every box on it has its own page in `docs/`; the links say which.

## The pages and how they link

```
index.html  (home: CV, research, simulation plates)
  ├── public/simulations.html      the catalog: one card per simulation, in figure order
  │     └── public/simulations/*.html   ten simulation pages (Figs. 1–10)
  └── public/portfolios.html       the two research projects
        ├── public/portfolios/droplet-collection/index.html#/…   built copy of its own app
        └── public/portfolios/rotor-pendula/index.html#/…        built copy of its own app
```

Every page is a plain HTML file. There is no server code, no database and no login: the server hands out files, and
everything else happens in the reader's browser. Pages: [pages.md](pages.md). Simulations: [simulations/](simulations/).
Project copies: [portfolios.md](portfolios.md).

## Anatomy of a simulation page

Each of the ten pages is one self-contained HTML file: its own markup, its own simulation script inline, and links to the
shared files. Read from top to bottom, a page holds:

1. **The figure** (`<figure class="stage">`): a canvas or SVG that the page's script draws every frame, with a caption.
   At the right end of the caption sits the **Read values** switch of the data panel.
2. **The controls**: sliders and buttons that set the physical parameters.
3. **The lecture note** (`<article class="paper" id="paper">`): motivation, model, derivation, numerical method, what is on
   screen, limits and further reading, set like a LaTeX document with numbered equations.
4. **The walkthrough** (`<section class="walk" data-walk="<key>">`), "From symbols to code": each equation of the model
   next to the lines of the page's own code that evaluate it, with the current values.
5. **The data panel**: a tab at the right edge of the window (a bottom sheet on phones) that lists every number the
   simulation computes.

The shared files load in this order at the end of the body (from `public/simulations/water-wave.html:563–885`; the other
pages follow the same order):

| Order | File | Role | Docs |
|---|---|---|---|
| 1 | `scripts/fold.js` | Turns the note's sections and the walkthrough into fold-out cards. | [scripts/fold.md](scripts/fold.md) |
| 2 | `scripts/sim.js` | Defines the `Sim` namespace: shared helpers, loading KaTeX and typesetting the note, drawing the walkthrough. | [scripts/sim.md](scripts/sim.md) |
| 3 | `scripts/dataset.js` | Adds `Sim.dataset()`: the page's one data store. | [scripts/dataset.md](scripts/dataset.md) |
| 4 | the page's own inline script | The simulation: state, physics, drawing, controls. It writes its numbers into the store. | the page's doc in [simulations/](simulations/) |
| 5 | `scripts/datalog.js` | The data panel; it only reads the store. | [scripts/datalog.md](scripts/datalog.md) |

Stylesheets, in the `<head>`: `styles/sim.css` (which imports the self-hosted fonts from `fonts/instrument-plex.css`, KaTeX's stylesheet and `paper.css`),
`styles/data.css`, `styles/fold.css`. See [styles.md](styles.md).

## The data pipeline: one notebook, read three ways

Picture a careful experimenter with a lab notebook. Each reading goes into the notebook at the moment it is taken, by the
person taking it. A reviewer who wants a number opens the notebook; the reviewer never repeats the measurement just to
show it. If the reviewer doubts a number, there are three independent ways to check it: read what the notebook says, redo
the arithmetic from the other numbers in the notebook, and look at the instrument's dial.

The simulation pages work the same way:

- **The notebook** is the store made by `Sim.dataset()`. It has the shape of an xarray / NetCDF dataset: named dimensions,
  typed-array variables (fields on a grid, trajectories), scalars, and attributes (units, symbols, descriptions).
- **The experimenter** is the page's own script. It writes every number into the store *at the line that computes it*,
  every frame, overwriting the previous frame. Nothing is computed twice for display.
- **The reviewer** is the data panel (`datalog.js`). It reads the store only, and does no work unless the reader asks:
  no loop while it is closed.
- **The three-way check** of one value: (1) the stored value; (2) the formula recomputed now from the stored inputs;
  (3) the pixel (or SVG element) read back from the picture at the same frame. The aim is "identical"; a float32 rounding
  gap is named as such.
- **Read values** is a tool the reader switches on, like a data cursor in MATLAB: a click pins a point of the figure, a
  marker follows that object every frame, and its values are written in a strip under the figure four times a second.
  Nothing on a running figure reacts to the pointer merely passing over it.
- **Record one round** copies every frame of one "round" (one period, one loop, ten seconds; each page defines it in
  `Sim.data.round`), at most 600 samples, and shows charts and a table. **Save** writes the store as `.npz` (NumPy's
  format) plus CSV, `dataset.json` and a README, in one zip.

Figs. 9 and 10 go one step further: they solve the whole run first (classical fourth-order Runge–Kutta), store every
sample, and then only play the stored samples back. Nothing is integrated while the reader watches.

## Folds

Every long page folds, with the mechanism of the Physik Radar app in one colour. Level 1 is a section card with a header
band (number, title, a line of counts, a round toggle) that stays pinned to the top of the window while the card is open;
level 2 is a part inside a card, pinned under its section's band. What a reader opens or closes is remembered per page in
the browser (`localStorage`); Expand all / Collapse all act at once; a link into a closed fold opens it first; printing
opens everything; without JavaScript every page reads fully open. The simulations catalog is one card per simulation,
closed at first, in figure order, with no grouping by field or year (Numa's choice until the library is large).
Details: [scripts/fold.md](scripts/fold.md).

## The catalog

`public/simulations.html` draws itself from one registry, `public/scripts/catalog.js`: an array `SIMULATIONS` with one
entry per simulation (figure number, title, file, field, course year, summary, key equation, model, method, controls,
concepts). Adding a simulation means adding its page, one entry there, and its thumbnail. Details:
[scripts/catalog.md](scripts/catalog.md).

## Design

The house design of the Droplet Collection app (`DESIGN.md` in `droplet-collection-yl7l26`): titles in Instrument Serif
at weight 400 only, text in IBM Plex Sans, labels in IBM Plex Mono; every box outlined, no card shadows; lecture notes in
Latin Modern Roman with KaTeX maths, numbered equations and figures. Details: [styles.md](styles.md), fonts and KaTeX in
[assets.md](assets.md).

## Where the source lives

The live app `numa-koudsie-website-0cyj78` on AppDeploy is the deliverable. This repository holds the same files at the
same paths, with this documentation beside them. How a change travels from one to the other, and what the platform does
on a deploy: [build-and-deploy.md](build-and-deploy.md).

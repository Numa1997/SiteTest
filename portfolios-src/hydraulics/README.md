# Hydraulic Press Study: the source

From Pascal's principle to a digitally controlled servo-hydraulic press: two simulations you can run and play with, and a
23-chapter textbook that derives every equation they integrate. This folder is the study's source. The site serves one page
generated from it, `public/portfolios/hydraulics/index.html` (<https://phyeinusul.com/portfolios/hydraulics/index.html>),
and its German and Arabic versions `de.html` and `ar.html`, written from it by `tools/i18n/hydraulics.py`; the page is
introduced as project 03 on the Portfolios page. Vite does not build or serve this folder; it only builds `index.html` and
`public/`.

The page has three tabs, one per standalone page here:

| tab | page here | what it is |
|---|---|---|
| Servo press (`#servo`) | `hydraulic_control.html` | Pump, four-way servo valve (drawn in section), 2 m of hose, differential cylinder and specimen under a digital PID controller sampled every 1 ms. Eight-state nonlinear model, RK4, energy audit to about 1e-14 of the pump's work; gauges, time plots, Bode / Nyquist / z-plane loop analysis, nine worked solutions. Press ▶ Play; every slider recomputes the cycle. |
| Ideal press (`#ideal`) | `hydraulic.html` | Pascal's press from a one-coordinate Lagrangian, drawn to scale, with a pressure probe in the oil. |
| Theory (`#theory`) | `hydraulic_theory.html` | *Hydraulics from First Principles*: 23 chapters, 63 numbered equations, 8 figures, every formula typeset with KaTeX when the page is generated, every "In our press" number computed from the models. |

Each page is self-contained (CSS, JavaScript and fonts inline) and opens straight from disk. The two simulation pages also load the website's
data panel (`scripts/sim.js`, `dataset.js`, `datalog.js`, `styles/paper.css`, `data.css`): from the served study they are two folders
up, from this folder on disk they are in `../../public/`; anywhere else the pages run without the panel. Each page keeps every number
of its run in one store (`declareStore()`, `storeRun()`, `Sim.data` near the end of its script); see `docs/portfolios.md`, "The data
panel of the two simulations".

## How the served page is made

`tools/build_combined.py --site` embeds the three pages unchanged (except that each embedded font becomes a link to the
byte-identical file the site serves, `../site_fonts.py`; the standalone build keeps them embedded), each as a JSON string, and shows each in its own frame
(`srcdoc`, with a `blob:` fallback), so their styles, ids and scripts cannot collide. A small script added to each embedded
page turns links between the pages into tab switches. It writes `public/portfolios/hydraulics/index.html` and
`LICENSE-fonts.txt` beside it, following the site's rules:

- the site's security policy and referrer rule, from the root `index.html`, plus `'unsafe-eval'` in `script-src` and `blob:`
  in `worker-src` for this page alone (the servo page builds its Web Worker with `new Function` and starts it from a `blob:`
  address);
- the site's own fonts (`../../fonts/instrument-plex.css`) for the tab bar, and the tab icon of `portfolios.html`;
- the title "Hydraulic Press Study · Numa Koudsie" and the back link "← Numa Koudsie · Portfolios".

Never edit the generated page by hand; change the source here and generate it again.

## Changing the study

The two simulation pages are edited directly; they are their own source. The theory is generated. From this folder:

```sh
(cd tools && npm ci)                     # KaTeX 0.16.11, pinned by tools/package-lock.json, once
python3 tools/build_theory.py            # theory/*.src.html -> hydraulic_theory.html
python3 tools/render_page_math.py        # typesets the equation blocks inside the two simulation pages
python3 tools/build_combined.py --site   # -> ../../public/portfolios/hydraulics/index.html (run this last)
```

## Checks

All four must pass after any change:

| command (from this folder) | what it proves |
|---|---|
| `python3 check_physics.py` | The ideal press's JavaScript physics agrees with an independent Python model. |
| `python3 check_control.py` | The servo press's equilibria, linearization, discretization, closed-loop poles, margins, nonlinear cycle and energy audit agree with an independent SciPy/SymPy model. |
| `node tools/check_theory_numbers.js ../../public/portfolios/hydraulics/index.html` | Every one of the 52 numbers the theory quotes is what the models embedded in the served page compute. |
| `python3 tools/check_combined.py http://localhost:<port>/portfolios/hydraulics/index.html` | With the built site served (`npm run build`, then `python3 -m http.server <port>` in `dist/`): each tab holds everything its standalone page has; Play, sliders, links, tabs and deep links work; no script errors; nothing scrolls sideways at 360–1440 px. 33 checks; needs Playwright for Python and Chromium. |

`node tools/check_data_panel.cjs ideal|servo <width> <outdir>` (Playwright for Node, the built site on port 8767) checks the data panel inside
each frame: the pointer sweep paints nothing, a dial and the piston or ram pin, a Check from the strip agrees, one round records, Save
writes an archive NumPy reads, and the panel's loop stops when it is closed.

The four plates on the Portfolios page (`public/portfolios/hydraulics/fig/`) are screenshots of the study; retake them when
the pictures change.

## Files

- `theory/*.src.html`: the textbook's source, HTML with LaTeX math. `tools/theory_template.html` is its page.
- `tools/page_equations.py`: the TeX of the equation blocks on the two simulation pages.
- `fonts/`: IBM Plex Sans, IBM Plex Mono and Instrument Serif (SIL OFL 1.1) as embedded in the pages, rebuilt by
  `tools/build_fonts.py`, and `LICENSE-fonts.txt`, which also covers the embedded KaTeX fonts (MIT).
- `dump_runs.js`, `dump_control.js`: run the pages' physics blocks in Node; used by the check scripts.

History: the study was written in the repository `Numa1997/Gergi-s-vision` and moved here on 21 October 2026.

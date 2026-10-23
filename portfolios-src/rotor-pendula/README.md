# Rotor Pendula: the source

Can a pendulum hung inside a turning wind-turbine blade, and braked by a small generator, power a sensor there? Is a chaotic
double pendulum better, and can the wind's disorder help? This folder is the study's source: a lecture note of nine chapters
(0–8) that derives every equation, a simulation page that solves the full equations in the browser, and the scripts that
compute and check every number. The site serves one page generated from it,
`public/portfolios/rotor-pendula/index.html` (<https://phyeinusul.com/portfolios/rotor-pendula/index.html>), with two tabs:

| tab | page here | what it is |
|---|---|---|
| Lecture notes (`#notes`) | `rotor_notes.html`, built from `theory/*.src.html` | *Pendula on a Turning Blade*: the Lagrangian, the best brake, big swings, two rods and chaos, a ceiling on random shaking, gusts, the bending blade, a real geared generator, and the answer. Every number in the text comes from `tools/make_numbers.py` (`numbers.json`) or is listed with its reason in `tools/typed_numbers.py`. |
| Simulation (`#sim`) | `rotor_sim.html` | Pick a rotor (six speeds), a pivot, one rod or two, and an ideal brake or the maxon RE 25 + GP 32 C generator; the page solves the full equations (Radau IIA, in a Web Worker built from its physics block) and plays the last turns back. Read values: click a plot to pin a point; the values show outside the figure. Six worked solutions. |

The derivations, model runs and review notes are in `notes/rotor-pendula/` (`derive/` holds the Python models;
`contract-L*.md` and `skeptic-*.md` the review record).

## How the served page is made

`tools/build_combined.py --site` embeds the two pages unchanged, each as a JSON string in its own frame, adds a small script
that turns the links between them into tab switches, and writes `public/portfolios/rotor-pendula/index.html` and
`LICENSE-fonts.txt`, with the site's security policy (plus `'unsafe-eval'` and `blob:` workers, which the simulation's worker
needs), the site's fonts for the tab bar, and the back link to Portfolios. Never edit the generated files by hand.

## Changing the study

From this folder:

```sh
(cd tools && npm ci)                     # KaTeX 0.16.11, pinned by tools/package-lock.json, once
python3 tools/make_numbers.py            # data/*.json -> numbers.json (every computed number and table of the notes)
python3 tools/build_theory.py            # theory/*.src.html + numbers.json -> rotor_notes.html
node tools/check_sim.js                  # the simulation's physics block against the Python engine (writes data/sim_check.json)
node tools/sim_solutions.js              # the worked solutions' numbers from the physics block (data/sim_solutions.json)
python3 tools/build_sim.py               # fonts, typeset equations and numbers into rotor_sim.html
python3 tools/build_combined.py --site   # -> ../../public/portfolios/rotor-pendula/ (run this last)
```

The data files in `data/` are copied from `notes/rotor-pendula/derive/` after the model runs there.

## Checks

| command (from this folder) | what it proves |
|---|---|
| `python3 tools/check_numbers.py` | Every number in the notes' sources is computed, or listed with its reason; derived ones are recomputed. |
| `python3 -I check_physics.py` | Independent of the study's scripts (constants retyped): SymPy derives (1.5), (2.4), the 45° lag, (2.5), (3.3), (7.1), (7.2); SciPy re-integrates six mountings (agreement about 1e-8) and the geared generator at two (about 2e-5). 17 checks. |
| `node tools/check_sim.js` | The simulation's physics block reproduces the 36 reference runs of the Python engine (worst 1.3e-8) and the generator runs of `data/L4_check_2000.json`. |
| `node tools/check_sim_browser.js` | The simulation page at 360, 390, 1024, 1440 px: no sideways scroll, no console errors, nothing reacts to the pointer crossing it, Read values pins and updates at about 4 per second. |
| `python3 tools/check_combined.py <url>` | With `public/` served (`python3 -m http.server 8765` in `public/`): both tabs complete, 0 KaTeX errors, the simulation solves, links switch tabs, no sideways scroll at 360–1440 px. |

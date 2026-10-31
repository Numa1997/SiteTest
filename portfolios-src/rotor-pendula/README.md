# Rotor Pendula: the source

Can a second, lighter blade, hinged at the 63 m tip of a turning wind-turbine blade and braked by a small generator in the
hinge, power a sensor there? The study tells it as one story: a double pendulum whose first arm the wind holds to a steady
turning. This folder is its source: a lecture note of nine chapters (1–9) that derives every equation, a simulation page that
solves the full equations in the browser, a wind page that synthesises a turbulent wind and swings the second blade in it, and
the scripts that compute and check every number. The site serves one page generated from it,
`public/portfolios/rotor-pendula/index.html` (<https://phyeinusul.com/portfolios/rotor-pendula/index.html>), with three tabs:

| tab | page here | what it is |
|---|---|---|
| Lecture notes (`#notes`) | `rotor_notes.html`, built from `theory/01_double` … `09_answer.src.html` | *A Second Blade on a Turning Blade*: Part I, the double pendulum held by the wind (the free double pendulum's Lagrangian reduced term by term to the second blade's equation, chaos lost; the turning frame; the best brake; big swings and the bill; a real geared generator); Part II, the real wind (power, Betz, lift, a turbulent field, gusts, the air on the second blade, the blade's sag and vibration, a ceiling on random shaking); Part III, the answer. Every number in the text comes from `tools/make_numbers.py` (`numbers.json`) or is listed with its reason in `tools/typed_numbers.py`. The record of each rewrite is in `notes/rotor-pendula/README.md`; the last, a revision of 30 October 2026 for a reader with a bachelor's in physics (missing steps filled, three figures added, equation numbers kept), is in `notes/rotor-pendula/revision.md`, its algebra checked by `notes/rotor-pendula/derive/R_revision.py`. |
| Simulation (`#sim`) | `rotor_sim.html` | Pick a steady wind (6, 8 or 10 m/s), the brake, and an ideal brake or the maxon RE 25 + GP 32 C generator; the page solves the full equations (Radau IIA, in a Web Worker built from its physics block) and plays the last turns back. Read values: click a plot to pin a point; the values show outside the figure. Six worked solutions. The site's data panel (Data tab, Check, Record one round, Save as NumPy) reads a store written in the script before the page script; see the README section below. |
| Wind (`#wind`) | `rotor_wind.html` | A turbulent wind over the rotor (IEC Kaimal spectra and coherences, Veers' method, synthesised in the browser from seeded random numbers), the rotor turning in it with the NREL torque law, and the second blade swinging at the tip with the air on it; two views (from upwind, from the side with Taylor's frozen turbulence) and traces of the last 90 s. Its physics block (`/*WIND-BEGIN*/`…`/*WIND-END*/`) equals `notes/rotor-pendula/derive/L6_wind.py` to rounding; its store and ledger (`public/scripts/ledger/rotor-wind.js`) feed the data panel, with an energy book for the second blade. |

The derivations and model runs are in `notes/rotor-pendula/` (`derive/` holds the Python models; `README.md` is the record).

## How the served page is made

`tools/build_combined.py --site` embeds the three pages (notes, simulation, wind) unchanged, each as a JSON string in its own frame (except that each
embedded font becomes a link to the byte-identical file the site serves, `../site_fonts.py`; the standalone build keeps them embedded), adds a small script
that turns the links between them into tab switches, and writes `public/portfolios/rotor-pendula/index.html` and
`LICENSE-fonts.txt`, with the site's security policy (plus `'unsafe-eval'` and `blob:` workers, which the simulation's worker
needs), the site's fonts for the tab bar, and the back link to Portfolios. Never edit the generated files by hand.

## The data panel

`rotor_sim.html` links the site's shared panel files by their path from this folder (`../../public/styles/data.css`,
`../../public/scripts/sim.js`, `dataset.js`, `datalog.js`); `tools/build_combined.py --site` rewrites `../../public/` to `../../`
for the served copy. The script just before the page script builds the store (`Sim.dataset`) and `Sim.data`; the page calls its
hooks (`D.solved`, `D.put`, `D.scene`, `D.plot`, `D.curve`, `D.frame`) where it computes or draws a number. The physics block
integrates the rotor's work as an extra state and records the energies of every frame, so the panel's energy book closes to about
1e-12 J. Without the shared files the store script returns at once and the page works as before. Details and measurements:
`docs/portfolios.md`, section Rotor Pendula.

## Changing the study

From this folder:

```sh
(cd tools && npm ci)                     # KaTeX 0.16.11, pinned by tools/package-lock.json, once
node tools/compare.js                    # theory against the full equation on the page's own engine -> data/compare.json (Figure 11)
node tools/double_pendulum.js            # the site's Fig. 2 double pendulum free and held -> data/L0_double.json (Figures 4 and 6, chapter 1; figures are numbered at build time)
node tools/check_wind.js                 # the wind page's physics block against L6_wind.py -> data/wind_check.json
python3 tools/make_numbers.py            # data/*.json -> numbers.json (every computed number and table of the notes)
python3 tools/check_numbers.py           # every typed number explained (tools/typed_numbers.py), every key present
python3 tools/build_theory.py            # theory/*.src.html + numbers.json -> rotor_notes.html
node tools/check_sim.js                  # the simulation's physics block against the Python engine (writes data/sim_check.json)
node tools/sim_solutions.js              # the worked solutions' numbers from the physics block (data/sim_solutions.json)
python3 tools/build_sim.py               # fonts, typeset equations and numbers into rotor_sim.html
python3 tools/build_wind.py              # the same for rotor_wind.html, with the simulation page's stylesheet
python3 tools/build_combined.py --site   # -> ../../public/portfolios/rotor-pendula/ (run this last)
```

The data files in `data/` are copied from `notes/rotor-pendula/derive/` after the model runs there; for example
`python3 -I L1_terms.py` there measures each term the small-swing theory neglects (section 3.1) and writes `L1_terms.json`.
`L2_steady.py` finds where the turbine's own torque law puts the rotor (section 6.5), `L5_air.py` estimates the air on the
second blade for three shapes (chapter 7), and `L6_wind.py` synthesises the turbulent field of section 6.4, checks it against
its spectra and coherences, and solves the machine in it (chapter 7.4; `L6_wind.json`, and `L6_wind_ref.json` for the page check).
The notes are written for a reader new to wind turbines; the teaching research and a blind learner's reading are in
`notes/rotor-pendula/teaching/`.

## Checks

| command (from this folder) | what it proves |
|---|---|
| `python3 tools/check_numbers.py` | Every number in the notes' sources is computed, or listed with its reason; derived ones are recomputed. |
| `python3 -I ../../notes/rotor-pendula/derive/R_revision.py` | SymPy checks of every step the revision of 30 October 2026 wrote out (energy function, turning-frame acceleration and torques, Radau IIA's stability function, Bernoulli and the actuator disc, the torque law, the lean's stiffness, the stator's tilt, the effective mass, the elliptic action of a swing, the adiabatic identity, Kolmogorov's exponents, the vibration model's equations): 47 checks. |
| `python3 -I check_physics.py` | Independent of the study's scripts (constants retyped): SymPy derives the rod's equation from its Lagrangian integrated along it, the uneven-rotor term, (2.4), the 45° lag, (2.5), τ*, (3.3), (7.1), (7.2); SciPy re-integrates the nine stored runs (agreement about 2e-12) and the geared generator at two winds. |
| `node tools/check_sim.js` | The simulation's physics block reproduces the nine reference runs of the Python engine (`data/L1_blade.json`, worst about 1e-14) and the generator runs of `data/L4_check_2000.json` (about 4e-5). |
| `node tools/check_newton.js` | The geared generator on the page's engine at the 16 settings of `data/L4_check_2000.json`: Newton's cap of 12 changes the powers by at most 8e-12, no measured step stays unconverged with a cap of 40, and 4000 steps per turn with a narrower band change them by at most 3e-4. About 5 minutes. |
| `node tools/check_sim_browser.js` | The simulation page at 360, 390, 1024, 1440 px: no sideways scroll, no console errors, nothing reacts to the pointer crossing it, Read values pins and updates at about 4 per second, and every "Try it" button of the worked solutions solves. |
| `python3 tools/check_combined.py <url>` | With `public/` served (`python3 -m http.server 8765` in `public/`): all three tabs complete, 0 KaTeX errors, the simulation solves, the wind tab synthesises and runs, links switch tabs, no sideways scroll at 360–1440 px. |
| `node tools/check_wind.js` | The wind page's physics block gives the same field as `L6_wind.py` (2e-14 m/s), the same 60 s run with every term (3e-14), and an energy book that closes over a whole record. |

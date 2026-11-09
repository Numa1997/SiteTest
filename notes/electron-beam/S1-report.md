# S1 (Scaffold) report, 9 November 2026, branch `eb/scaffold`

## What exists

All under `portfolios-src/electron-beam/` (full table in its README.md), plus the generated `public/portfolios/electron-beam/index.html`,
rules in `tools/inventory.py` and `docs/files.md` (rewritten by the inventory tool).

- `contract.json`: 80-odd symbols, each with meaning, TeX, type, SI unit, default, range, scale (lin/log), display unit and factor, stage;
  stages `ch00` to `ch08` with `in` and `out` as PLAN.md section 6. Stage keys are zero-padded so they match the file names. `ch01`'s in/out
  is my proposal (section 6 has no row for it); `ch00` is the worked example. Defaults are exact (4.55 eV = 7.2899e-19 J, 171 eV for Si).
- `physics/core.js` (CODATA 2018, units, `fmt`, `rng`, `withDefaults`), `physics/ch00.js` (worked example), `ref/core.py`, `ref/ch00.py`.
- `build.py`, `eb_lib.py`, `template.html`, `app.js`, `bridge.cjs`, `guide_default.py`; `checks/` with parity, numbers, page, selftest, fixtures.
- Chapters 0 to 9 are placeholders ("in preparation") until `text/chNN.py` exists. The one running simulation on the page today is chapter 0's
  (the worked example of the plug-in), shown under its placeholder.

## How chapters plug in

README.md, "How a chapter plugs in". In short: `physics/chNN.js` (copy ch00.js), `ref/chNN.py`, `text/chNN.py` (dict `CH`). Equations and figures
are numbered `c.n` at build time; `{{eq:}}`, `{{fig:}}`, `{{sec:}}` link them; `{{num:}}` prints a computed number; the build fails on bad labels.
Rule I added: a module's `inputs`/`outputs` must equal the contract stage's `in`/`out`.

## Commands (repository root)

```
python3 portfolios-src/electron-beam/build.py --site
python3 portfolios-src/electron-beam/build.py
python3 portfolios-src/electron-beam/checks/selftest.py
python3 portfolios-src/electron-beam/checks/check_parity.py
python3 portfolios-src/electron-beam/checks/check_numbers.py [--text-dir DIR]
node portfolios-src/electron-beam/checks/check_page.cjs [--path /portfolios/electron-beam/x.html] [--shots DIR]
python3 tools/inventory.py --check
```

## Verified (outputs of 9 November 2026)

- Build: `wrote public/portfolios/electron-beam/index.html: 52101 bytes; 0 of 10 chapters ... 8 formulas`.
- `selftest.py`: SELFTEST PASS. The good fixture builds (2 equations, 1 figure, 6 numbers, KaTeX output, sim slot); refused, each for its own reason:
  doubled equation label, unknown `{{eq:}}`, KaTeX error, unplaced figure, undeclared figure, SVG with a script, unknown chapter key, unknown
  number, number inside maths, unmatched `$`, simulation on a module without UI, contract/module disagreement. Number check refuses a typed
  "3.7 pm", "3.7 × 10⁻¹¹ m", "$x = 3.14$", "100 kV", and accepts "100 kV" once listed in `literals` with a reason.
- `check_parity.py`: constants 27 values, largest relative difference 1.9e-16; formatter identical on 51 cases; ch00 JS = Python on 5 cases,
  difference 0 (same float64 operations, so 0 is expected). Falsified on purpose: with the Python electron mass raised by 1e-9 it prints FAIL
  for the constant and for ch00.
- `check_numbers.py`: PASS on the good fixture (6 numbers, browser = Python, identical); vacuous PASS on the real page (no chapter written).
- `check_page.cjs`: PASS at 360, 390, 1024, 1440 px on the real page and, once, on a page built from the fixture chapter (16 KaTeX formulas, an
  equation, a figure, a simulation): 0 KaTeX errors, 0 page or console errors, 0 px sideways scroll, no request outside the origin, no 4xx,
  title in Instrument Serif 400, the four faces loaded, the simulation canvas has drawn pixels (alpha read first) and its readouts change when
  its first slider moves. Screenshots `notes/electron-beam/shots/{top,page}-{360,390,1024,1440}.png` (git-ignored, regenerate with the command).
  I looked at the 1440 and 390 px top screenshots and at the fixture chapter's 1440 px page by eye.
- `python3 tools/inventory.py --check`: exit 0.

## Open points and honest limits

- **Inference:** the placeholder chapters carry the same TOC and anchors as real ones, so links will not move when text lands.
- The generic simulation slot gives sliders, readouts and one canvas. A chapter that needs a table or a second canvas must ask (requests.md).
- `check_numbers` is a heuristic for the prose: it cannot see a number written as a word ("ten") or inside an SVG label, and it allows whole
  numbers 0 to 10 without a unit. Reviewers should still read the text.
- The reading guide shown now is a default (`guide_default.py`) describing the finished page; S11 replaces it with `text/guide.py`. The status
  line under it is generated and says how many chapters exist, so it does not overclaim.
- `docs/portfolios.md`, `public/portfolios.html`, redirects and i18n are untouched, for the coordinator.
- Not tested: Firefox and Safari (only Chromium); no print layout check.
- Chapter 1's physics module needs a time step loop with array outputs: `check_parity.py` already compares arrays element by element.

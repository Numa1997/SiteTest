# The Electron Beam, from Tip to Measurement: the source

Project 07. Lecture notes and simulations that follow an electron from a field-emission tip to a measured line width. This folder is the
only source; the build writes the page the site serves, `public/portfolios/electron-beam/index.html`. Scope, chapters, file ownership
and the definition of done are in [PLAN.md](PLAN.md). The scaffold (this README, the build, the contract, the checks) is session S1.

## Layout

| Path | What it is |
|---|---|
| `contract.json` | The hand-over contract: every symbol (SI unit, range, default, display unit, TeX) and the in/out of each stage `ch00` to `ch08`. |
| `physics/core.js` | CODATA 2018 constants, unit factors, number format `fmt`, seeded random numbers `rng`, `withDefaults`. Runs in the page and in Node. |
| `physics/chNN.js` | One pure module per chapter (worked example: `ch00.js`). Owned by the chapter session. |
| `ref/core.py`, `ref/chNN.py` | The Python reference; `core.py` mirrors `core.js` value for value and holds the number formatter the build uses. |
| `text/chNN.py`, `text/guide.py` | The words: a dict `CH` per chapter, a dict `GUIDE` for the reading guide. Missing files render "in preparation". |
| `build.py`, `eb_lib.py`, `template.html`, `app.js`, `bridge.cjs`, `guide_default.py` | The build and the page. `bridge.cjs` runs the page's JavaScript in Node and typesets with the site's KaTeX. |
| `checks/` | `check_parity.py`, `check_numbers.py`, `check_page.cjs`, `selftest.py`, `fixtures/`. |
| `derive/`, `sources/`, `data/` | Chapter sessions' SymPy derivations, the librarian's bibliography, digitised published data. |
| `out/` | Stand-alone build (git-ignored). |

## Commands (from the repository root)

```sh
python3 portfolios-src/electron-beam/build.py --site     # public/portfolios/electron-beam/index.html
python3 portfolios-src/electron-beam/build.py            # stand-alone copy in portfolios-src/electron-beam/out/
python3 portfolios-src/electron-beam/checks/selftest.py  # the build accepts a good chapter and refuses each broken one
python3 portfolios-src/electron-beam/checks/check_parity.py   # physics/chNN.js against ref/chNN.py, constants, number format
python3 portfolios-src/electron-beam/checks/check_numbers.py  # every quoted number computed; no typed measurement in the prose
node    portfolios-src/electron-beam/checks/check_page.cjs    # Chromium at 360, 390, 1024, 1440 px; shots in notes/electron-beam/shots/
python3 tools/inventory.py --check                            # every file described
```

Needs Python 3.9 or newer with NumPy, and Node. KaTeX is the site's copy (`public/vendor/katex/katex.min.js`, 0.16.11), so nothing is
installed for the build. `check_page.cjs` uses the preinstalled Playwright (`require('playwright')`); it serves `public/` itself, so no
server is needed. `--path /portfolios/electron-beam/x.html` opens another built page under `public/`; `--shots DIR` moves the screenshots.

## How a chapter plugs in

A chapter session owns `text/chNN.py`, `physics/chNN.js`, `ref/chNN.py`, `derive/chNN.py`, `data/chNN/` (PLAN.md section 7), and edits no other file.

1. **Contract.** Code against `contract.json`. A module's `inputs` and `outputs` must equal the stage's `in` and `out` (the build checks
   this). A new symbol or a change goes into `notes/electron-beam/requests.md` on the chapter's branch; the scaffold edits the contract.
2. **Physics module** `physics/chNN.js`, copy `physics/ch00.js`: a UMD wrapper, `id`, `inputs`, `outputs`, `tolerance` `{rel, abs, note?}`,
   `cases` (inputs for the parity check), optional `ui`, `compute(p)` (SI in, SI out, pure) and optional `draw(ctx, w, h, p, out)`.
   `ui = {controls: [symbols], readouts: [symbols], aspect, aspectPhone, caption}` makes the simulation slot: one slider per symbol with a
   `min`, `max` and `scale` in the contract (an `enum` gives a menu), readouts, a canvas. Sliders are bound to the contract symbols by name.
3. **Python reference** `ref/chNN.py`: `INPUTS`, `OUTPUTS`, `compute(p)` from the same equations, in NumPy. Chapters 1, 2, 4, 5, 6, 7 need one.
4. **Text** `text/chNN.py`: the dict `CH` described at the top of `eb_lib.py`:
   `title`, `lead`, `sections` (`id`, `title`, `html`, `star`), `figures` (inline SVG with a `viewBox`, and a caption), `numbers`, `literals`, `sim`.
   In section HTML: `$...$` and `$$...$$` (KaTeX, build time); `\label{name}` inside a display names it, `\notag` leaves it unnumbered;
   `{{eq:name}}` `{{fig:name}}` `{{sec:chNN-id}}` are numbered references; `{{figure:name}}` places a figure; `{{num:name}}` a computed number
   (`{{numtex:name}}` inside maths); `\$` a dollar sign. Equations and figures are numbered `c.n` in the order they appear.
5. **Numbers.** Every measurement in the prose is a `{{num:..}}` declared in `CH["numbers"]` as a module output (`module`, `inputs`, `out`,
   `scale`, `sig`) or an expression of other numbers (`expr`, `of`). A value that is a given of the problem or quoted from a source is listed in
   `CH["literals"]` with its reason, for example `{'100 kV': 'the acceleration voltage of worked example 1'}`.
6. **Build and check** (commands above). The build fails on an unknown or doubled label, a figure declared but not placed (or placed twice), an
   SVG with a script or an outside address, an unknown key, a KaTeX error, a contract that disagrees with a module, a `$` left over.

A custom panel that the generic slider-and-canvas slot cannot give (a second canvas, a table) is a request for the scaffold, not a change to the template.

## Rules this source keeps

- SI units in every stored value; a display unit is a presentation (`display_unit`, `display_scale` in the contract). Energies are stored in joules and shown in eV.
- The page loads nothing from outside the site: the build writes the site's security policy and referrer tag after the charset line, fonts and KaTeX
  styles are the site's own files, and `check_page.cjs` fails on any other request.
- A simulation writes nothing the display recomputes: `compute` gives the numbers, the slot only reads them.
- The page never claims affiliation with Applied Materials. Its public statements are quoted as public claims, with their source.
- Screenshots are reproducible and stay out of git (`notes/.gitignore`).

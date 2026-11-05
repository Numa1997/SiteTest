# Honesty tests of the data panel, project 05 (Balancing Two Rods on a Cart)

Written 5 November 2026 with the panel of `public/simulations/double-inverted-pendulum.html`; the procedure is section 7 of the
skill `notes/skills/phyein-usul-data-panel/SKILL.md`. Run from anywhere with `NODE_PATH=$(npm root -g) node notes/fig11/panel/<file>`
(headless Chromium through the installed Playwright; `ROOT=<repo>` to test another checkout). Raw outputs of 5 November are the
`*.txt` files beside them.

| File | Checks |
|---|---|
| `ref.cjs` | the independent reference: equations of motion from rows (8a), (8), (8b) of the note, solved by Cramer's rule; RK4 (18); references (25)–(26); the laws (16), (21), (24); the energy |
| `origin.cjs` | a. every write into the store by its function (static and at run time); the display reads only the store; a store edit moves the drawing |
| `hon.cjs` | b replay, c controller, d picture, over the scenarios of e; `node hon.cjs rest flick …` runs a subset, `DPR=2` at device pixel ratio 2 |
| `fals.cjs` | f. three corruptions that must fail, and their reverts that must pass |
| `cost.cjs` | g. frame time with the panel closed, before (`BASE=<checkout of main>`) and after; when the panel's loop runs; the pointer rules |
| `drag.cjs` | the cart dragged with a real mouse (`ROOT=<repo>`, `LANG2=de/` or `ar/`): the motor lets go, every hand step's force and RK4 replay checked by the panel's own hooks, the energy book, the release; writes `drag-held.png` beside itself |
| `readcart.cjs` | with Read values on a press on the cart pins and does not grab it; with it off the press grabs the cart |
| `shots.cjs` | screenshots with the panel open and the layout facts (page width, what the panel covers) |
| `mask.py`, `final.py` | masking for DeepL and the checked German and Arabic of the panel's 176 strings, written into `i18n/<lang>/strings.json` |

The behaviour tests of the page are `notes/fig11/study/t9.cjs` and `t7.cjs`; they hard-code `/home/claude/...` paths, so copy them
outside the repository (whose `package.json` says `"type": "module"`) and fix the paths there.

Raw outputs, 5 November 2026: `a-origin.txt`; `bcde-honesty.txt` (all nine scenarios; flick failed one picture check), `d-dpr2.txt`
(device pixel ratio 2; the swing-up failed the same check). Both failures were the test's bound on the round cap of the upper rod:
the last fully burgundy sample was required to lie at most r beyond the rod's end, which ignores antialiasing (a 98 % covered pixel
passes the colour test) and the float sum of the 0.05 px sample steps; measured 4.25 and 4.30 px against r = 4.25 px. The bound is
now r + 0.5 px; reruns in `bcde-flick-rerun.txt` and `d-dpr2-swingup-rerun.txt`, and `f-falsification.txt` (run after the change)
shows the corrupted display still fails every picture check. `g-cost.txt`; `behaviour-main.txt` and `behaviour-branch.txt` (t9 and t7
on main and on the branch).

Raw outputs, 5 November 2026 (evening, defined controls and the cart in your hand): `a-origin-cart.txt` (PASS), `bcde-honesty-cart.txt`
(all eleven scenarios, the new `cart` among them, pass; the hand check recomputes each hand step's force from its own row with the
independent `forceFor` of `ref.cjs`), `f-falsification-cart.txt` (each corruption fails, each revert passes), `g-cost-cart.txt` (frame
time with the panel closed: median 0.3 ms before and after), `drag-cart.txt` (`drag.cjs` in English, German and Arabic, and `readcart.cjs`).
In a first run of `hon.cjs cart drag` the rod-drag picture check once found the stored pixels 2.8 × 10⁻¹⁴ px away from the Node formula
(it demands exactly 0); every rerun since gave 0.

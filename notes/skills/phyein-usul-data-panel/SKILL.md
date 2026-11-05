---
name: "phyein-usul-data-panel"
description: "Attach the data panel (dataset store + datalog explorer, with its ledger) to a Phyein Usul simulation, study or project page, including live pages with a sampled controller and a supervisor, and prove with a required test procedure that the store is what the simulation computes and what the reader sees."
---

# The data panel on Phyein Usul: every number with its fingerprint, and the proof

Every simulation on phyeinusul.com (repository `Numa1997/SiteTest`) carries a data panel: a store of every number the page
computes (`scripts/dataset.js`) and a bookkeeper that shows it (`scripts/datalog.js`, `styles/data.css`). The picture to keep: an
assistant sits beside the experiment with a camera, a probe, a chart recorder and a ledger, and does nothing until asked. The
headline shows the few dials the animation is about; the ledger lists every other number in the order of cause; the books show
what must balance; Record keeps one round; Read values pins a point; Check works one number out again three ways; Save hands
over the notebook.

The panel is only worth something if it cannot lie. This skill therefore has two halves of equal weight: building the store
(sections 3 to 6) and proving it honest (section 7, required on every page, with scripts to start from).

Revised 5 November 2026 from the work on project 05, Balancing Two Rods on a Cart (`public/simulations/double-inverted-pendulum.html`),
the first live page with a sampled controller and a supervisor. The earlier version was written from commit `007f3cf`
(23 October 2026), before the panel became a bookkeeper. The code and its docs are the authority; if they have changed since,
read them first and follow them.

## 1. Read before you start

- `CLAUDE.md`, "A data table is a pipeline, not a second simulation" and the pointer rules; `AGENTS.md`, paragraph "Data panel".
- `public/scripts/datalog.js` lines 1 to 60: the contract `Sim.data`, including `ledger` (headline, sections, books, deps,
  controls, current). `public/scripts/dataset.js` lines 1 to 15: the store's API.
- `docs/scripts/datalog.md` (how the panel behaves, the tables of rounds and books) and `docs/scripts/dataset.md`.
- The skill `phyein-usul-bookkeeper` for the ledger's design (headline, causal sections, books).
- One model page of the same kind as yours:
  - solve first, play back: Fig. 9, `public/simulations/driven-oscillator.html`, ledger in `public/scripts/ledger/driven-oscillator.js`;
  - integrate live: Fig. 2, `public/simulations/Double Pendulum.html`;
  - integrate live with a sampled controller, a supervisor and logs at three rates: project 05,
    `public/simulations/double-inverted-pendulum.html` (store from the comment "the store:", logs at `logSample`/`logStep`,
    `Sim.data` with its ledger inside the page), described in `docs/simulations/fig11-double-inverted-pendulum.md`, "Data panel".
- The test scripts of section 7: `notes/fig11/panel/` (`ref.cjs`, `hon.cjs`, `origin.cjs`, `fals.cjs`, `cost.cjs`, `shots.cjs`)
  and their raw outputs. Copy and adapt them; do not start from nothing.

## 2. The rules (Numa's, not negotiable)

1. **One store.** The page writes every number into the dataset at the line that computes it. The drawing, the readouts beside the
   figure, the walkthrough's live numbers (`Sim.live`), the panel and Save only read. Nothing is recomputed for display.
   This includes counters: a row count is written with the row it counts, not once per frame (section 8).
2. **Three proofs for every value**, shown to the reader: the stored value; the formula recomputed from the stored inputs; the
   pixel (or SVG attribute) read back from the picture. Aim for "identical"; name a float gap as what it is.
3. **Alpha before colour.** A read-back first checks that something was drawn: a transparent pixel passes a "dark" test.
4. **Say where drawing and store differ** (camera that lags, view that widens, colour steps, smoothing, trails, clipping,
   exaggerated scales, frames that show one state of many steps) in the page's `about` paragraph.
5. **Nothing reacts to a pointer merely crossing the figure.** Reading a point is a tool the reader switches on (Read values):
   click to pin, values in a strip outside the figure, rewritten at most about 4 times a second, the marker every frame.
   While Read values is on, the page's own pointer actions (dragging a rod) are held back. Measure it.
6. **No work when nobody looks.** The panel's loop runs only while recording, while Read values shows a pin, or while the panel
   is open with Live on and something moves. Measure the frame time with the panel closed, before and after your change.
7. **Prove it** (section 7) before calling it done, show the raw output, and keep the scripts and outputs in the repository.

## 3. Files, load order, translation

| File | Role |
|---|---|
| `public/scripts/dataset.js` | `Sim.dataset(meta)`: dims, coordinates, variables with attributes, typed arrays; `ds.npz()` writes the archive. |
| `public/scripts/datalog.js` | The panel. Reads `Sim.data` and the store; never computes physics, never writes to the store. |
| `public/styles/data.css` | The panel's styles. Below about 1500 px the open panel lies over the page; above, it pushes the page aside. |
| `public/scripts/ledger/<page>.js` | Optional: the ledger in its own file (Figs. 9 to 11). A page may also put `ledger` inside its own `Sim.data` (project 05). |

Order on the page: `styles/data.css` in the `<head>`; at the end of `<body>`: `scripts/sim.js`, `scripts/dataset.js`, the page's
own script (store and `Sim.data`), an optional ledger file, then `scripts/datalog.js`. Relative paths (`../scripts/…`); never copy.

What the panel needs from the page: `Sim.fmt`, `Sim.readPixel(box, x, y, r, test)` with `box = Sim.canvas2d(...)`, an element
`#stage` holding the figure whose parent has a `.stage__cap` caption (the Read values switch goes there).

**Translation is part of the job.** `tools/i18n/build.py` asks a German and an Arabic entry in `i18n/<lang>/strings.json` for every
literal `_t('…')` in the page and for every literal after `long_name:`, `title:`, `note:`, `about:`, `kicker:` and `short:` in a
simulation page or ledger file (`PANEL_KEYS`). A store of 130 variables means about 180 new strings. Plan for it:
1. `python3 tools/i18n/build.py --todo de` lists what is missing.
2. Mask maths, symbols, markup, identifiers (`T_s`), equation numbers and colours as `⟦n⟧` (the convention of
   `tools/i18n/apply_review.py`); a template is in `notes/fig11/panel/` (`mask.py`, `final.py`).
3. Translate with the DeepL connector (Free plan: at most 50 texts per request, no glossary, context ignored), German and Arabic
   in one call per batch; never write a translation yourself.
4. Check once against `docs/glossary.md` and the terms the page already uses (`i18n/<lang>/simulations__<page>.html.json`):
   known DeepL faults are Gewinn for gain (Verstärkung; Arabic الكسوب), Schleife for loop (Taktzeit / دور حلقة التحكّم),
   Probe or Stichprobe for a controller sample (Abtastung / العيّنة), Frame or Rahmen (Bild / إطار), Buch for the books (Bilanz /
   الموازنة), Controller (Regler / المتحكّم), Vorgesetzter for supervisor (Überwacher / المشرف), "drawn" as gezogen (gezeichnet),
   "wrapped" as umwickelt (auf ±π zurückgeführt / مردود إلى ±π), and nonsense such as Warenkorb or سلة التسوق for a cart, or a company
   name for "a lean". Every `⟦n⟧` must come back; the script checks it.
5. Write the tables, `python3 tools/i18n/build.py`, then `--check`; revert the one-line "translated-from" stamp on pages you did
   not change (`git diff --numstat` shows 1+1 for them).

## 4. Inventory: what to store, and at which rate

Make the inventory before writing code, in the sections the ledger will show (causal order): what you set; constants of the code;
what follows from the machine; the controller; the state now; the books; the supervisor; the stored run or the logs; the drawing.

Then decide the **rates**. A live page has up to three clocks, and each needs its own record:

| Rate | What | Where it is written | Why |
|---|---|---|---|
| every physics step (1 ms) | state before and after, the force held over it, which controller sample set that force, the kind of step (integrated, or held by the hand), a code for an outside change before it (flick, hand, reset, wrap at hand-over, unexplained), the design version | right after the integrator's line, in `logStep()` | replay (7b), the zero-order hold (7c), the energy book |
| every controller sample (every T_s, or every 10 ms in other laws) | time, step number, due time, next due time, the state the controller saw, the force it chose, the law used (balance, calm, track, off, motor cut), the reference's own numbers (kind, place or target, speed, start time, glide's starting distance), the force limit in force, centre of calming, plan start and plan number, design version | right after the controller's line, in `logSample()` | recompute every force from its row alone (7c); sample times on the grid |
| every frame | the state at the end of the frame and what follows from it (accelerations, W, W_red, energies, the reference now), the settings, the supervisor's state, the drawing's numbers | `diagnostics()` after the steps, and `draw()` for the drawing's own numbers | what the reader sees; headline, ledger, rounds, Sim.live |
| when it changes | gains, P, Φ, Γ, the catch level c*, the plan (as the very arrays the tracker reads) | `redesign()`, the certificate's generator, `planStore()` | |

Logs: fixed capacity (8192 rows for 1 ms steps holds 4 to 8 s), chronological; when full, keep the newer half with
`copyWithin` (no reallocation, so references stay valid). Give each row a global number as a coordinate (step number, sample
number), and link the logs by those numbers (`st_j` = the sample whose force a step holds). Store a design number with every row,
so a check knows which gains and which machine applied.

## 5. Writing the store into a live page with a sampled controller and a supervisor

The control loop of such a page has this shape (project 05, `step()`):

```js
supervise();                                              // may change mode, reference, tCtl, even cut the motor
if (tSim >= tCtl - 1e-9) { u = control(); tCtl += period(); }   // the controller looks every T_s and holds u (zero-order hold)
s = rk4(p, s, u, H); tSim += H;                           // one physics step of 1 ms
```

The walkthrough usually quotes these lines as one block; you may not insert lines between quoted lines (`node notes/walkcheck.cjs`
must stay all-found). So capture before and record after:

```js
var s0 = s, t0 = tSim, c0 = tCtl, u0 = u;                 // before supervise(): state object, time, due time, force
supervise();
if (tSim >= tCtl - 1e-9) { u = control(); tCtl += period(); }
s = rk4(p, s, u, H); tSim += H;
logStep(s0, t0, 0, c0, u0);                               // a sample if tCtl moved; a "motor cut" row if u changed without one; then the step
```

- `s0` is the same object `supervise()` may change in place (a wrap of the angles at hand-over), so it holds exactly the state
  the controller and the integrator used. `rk4` returns a new array, so `s0` stays the state before the step.
- The due time of a sample is the value of `tCtl` the `if` compared with. JavaScript evaluates `tCtl += period()` by reading `tCtl`
  first, so `period()` can record it: `function period() { cDue = tCtl; return … }`.
- Record the law and the reference **after** `control()`: it may switch from track to balance (end of plan) or to calm (left the
  plan) and use the new law at once.
- A force changed outside a sample (the supervisor cuts the motor when the rods are lost) breaks the zero-order hold. Do not hide
  it: log it as its own sample row with law "motor cut", so every step still holds the force of a logged row.
- Outside changes of the state between steps (a flick, the hand, a reset, a new state from a test, the wrap at hand-over): set a
  reason code where they happen (`why = 1` in `flick()`, …), and let `logStep` compare the state before the step with the stored
  state after the previous one. A difference without a reason is code 9, "unexplained"; the tests must find none.
- Held steps (the hand holds the rods) are logged with kind 1, no sample number, force 0.
- Store the plan the tracker follows as the arrays it reads: `ds.dim('p', tv.n); ds.set('pl_u', tv.un)` (no copy), and a plan
  number written into every sample.
- Supervisor modes, each visible in the store: the certificate's generator (`c_star` undefined while it runs, `c_busy`, and the
  hand-over level `c_hand = 0.9 c*`); calming, planning and tracking (`mode`, `x_c`, `t_plan`, `plan_busy`, `plan_ready`, the plan
  arrays); the hand-over at W < 0.9 c* (`W`, `W_red` per frame, the wrap logged as code 4); the moving references fixed, cruise
  and glide (kind and numbers per sample and per frame, `x_r`, `v_r` per frame, recomputed in the checks from (25)–(26)).
  A governor that changes the reference at a look (project 05's braking to rest, note (27)–(27a)) stores what it did in the
  sample's row (`cs_bite`, the speed before it `cs_vb`, NaN at looks without a bite) and its constants (`gamma`, `eps_rest`); the
  check recomputes each bite from that row, P, c* and γ alone, and confirms W after the bite stays within γ c*.
- **The energy book under a zero-order hold.** The force is constant over a step, so its work in that step is exactly
  u (x_after − x_before). The book is E₀ + W_motor + E_ext + E_wait = E, where E_ext adds the energy of every outside change and
  every held step, and E_wait is an outside change made while the clock is paused, not yet booked by a step (the clock calls the
  page every frame even when paused). What is left is the integrator's error (project 05: 3.5 × 10⁻¹⁴ of the flows at rest, up to 4 × 10⁻⁹ after a drag).
- `diagnostics()` runs once per frame after the steps and before `draw()`. `draw()` reads the store (state, lengths, masses,
  force limit, reference) and writes back only the numbers it works out on the way to the pixels (scale, camera, positions).
  The readouts beside the figure and `Sim.live` read the store too; `Sim.live` must not call the physics again.
- A page that only integrates live without a controller (Fig. 2) needs only the frame rate; a page that solves first and plays
  back (Fig. 9) stores the whole run and has the clock only pick the sample on screen.

## 6. Declare it: the store and `Sim.data`

```js
var ds = Sim.dataset({ title: '…', attrs: { page: '…', h: H, units: 'SI' } });
ds.dim('q', 6); ds.dim('k', 8192);
ds.var('u', [], 'float', { symbol: 'u', units: 'N', long_name: 'motor force now, held since the last sample', computed_in: 'control()', digits: 4 });
ds.coord('st_i', 'k', Int32Array, { symbol: 'k', long_name: 'step number since the page loaded', computed_in: 'logStep()', digits: 0 });
ds.var('st_s1', ['k', 'q'], Float64Array, { symbol: 's<sub>k+1</sub>', long_name: 'state after the step', computed_in: 'rk4(), in step()', digits: 6 });
```

Every variable gets `symbol`, `units` (if any), `long_name`, `computed_in`, `digits`; a derived one a `formula`. Use `Float64Array`.

`Sim.data` (contract at the top of `datalog.js`): `ds`, `kicker`, `file`, `playing`, `play`, `groups` (the sections; give them `how`
and `folded`, and use them again as `ledger.sections`), `rowLabel`, `colLabel`, `check`, `drawn`, `probe`, `inspect`, `locate`,
`round`, `about`, and `ledger` with `headline` (3 to 7 scalars), `books` (rows, total, residual stored by the page, `tol`), `deps`,
`controls` (control id → variable where they differ), `current` (dimension → variable holding the newest row).

- **check**: every derived scalar and every array (index as argument), recomputed from stored inputs only. For a step log:
  one RK4 step from the stored state before it with the stored force. For a sample log: the law from that row alone. A value of
  an earlier design returns `value: undefined` with a sentence saying so; never a fake.
- **drawn**: read back with geometry, not one pixel (section 7d); `ok: null` only when the value is legitimately not drawn.
- **probe/inspect/locate**: from stored positions; rows `[symbol, value, units, variable, index]`.
- **round**: for a live page, a fixed span of simulated time (`time: 't'`, ten seconds).

## 7. The honesty procedure (required on every page)

Run it in headless Chromium (`require('playwright')` with `NODE_PATH=$(npm root -g)`; never install another Playwright). The
repository's `package.json` has `"type": "module"`, so test scripts are `.cjs`, and older scripts with hard-coded paths
(`/home/claude/...`) must be copied and fixed. Drive the page in two ways: live (the clock plays, real input with the mouse)
and driven (pause the clock, then `DIPC.step(1/60); DIPC.think(8)` frame by frame, as `t9.cjs` does). Pull the logs out every
simulated second (`EXTRACT` in `hon.cjs`: only rows newer than the last pulled), so nothing is lost when a log drops its older half.

**a. Origin** (`origin.cjs`). (1) A static scan of the page script, brace-aware and skipping strings and comments, that lists every
write into the store (`ds.set`, `ds.get(..).set`, `ds.touch('…')`, writes into the log arrays) by the function that holds it.
(2) The display code (`draw`, `drawTrace`, `Sim.live`, the readout lines) must call no physics function and read none of the
page's own state variables. (3) `datalog.js` makes no write call on the store. (4) At run time, wrap `ds.set` and `ds.touch` by
trapping `Sim.dataset` as `dataset.js` defines it (`Object.defineProperty` on `window.Sim`; a hook added later misses the store),
record the calling function, open the panel, flick, swing up: no writer may be the panel, `Sim.live` or a panel hook. (5) The
decisive one: edit a stored value (θ₁ + 0.3 rad), call the page's `draw()`, and find the drawn object at the edited place, not the
old one; `Sim.live` must show the edit; the page's own state must be unchanged.

**b. Replay** (`hon.cjs` with `ref.cjs`). (1) Every stored step again with the page's own integrator: bit-identical, all of them.
(2) Every stored step with an independent RK4 written from the lecture note's equations (project 05: rows (8a), (8), (8b) solved
by Cramer's rule, where the page eliminates): differences at float64 rounding (≤ 10⁻¹² absolute; measured 10⁻¹⁷ to 1.8 × 10⁻¹⁵).
(3) Continuity: the state before each step equals the stored state after the previous one exactly, except at logged outside
changes; no gaps in the step numbers; no code 9. (4) A chained replay over the longest stretch without an outside change, from one
stored state with the stored forces. Do not demand identity: with the forces replayed open loop, rounding grows at the rate nearby
motions part. Measure that rate and compare it with the physics (project 05: the gap grows at 10.3 to 10.5 s⁻¹ near upright,
the fall rate σ₁ = 10.39 s⁻¹; slower while the rods hang). That agreement is itself a check of the equations.

**c. Controller.** (1) Every stored force recomputed from its own row: state seen, reference numbers, the gains of that design,
the force limit at that sample, the plan of that number; per law (balance u = sat(−K(s − s_r)), calm, track u = u_plan − K(t)(s −
s_plan), off and cut 0). Pass at ≤ 10⁻⁹ N (measured 0 to 1.4 × 10⁻¹⁴ N); no unchecked rows. (2) Zero-order hold: every 1 ms step
holds exactly (===) the force of the latest sample, and lies between that sample's step number and the next one's; held steps
have force 0. (3) Sample times: consecutive controller samples chain (due time = previous next due time) except at restarts of the
clock (reset, release of the hand, start of tracking, hand-over), and the number of steps between them is exactly T_s / h in
balance and 10 in the other laws; every sample within one step of its due time.

**d. Picture.** Pause, wait two animation frames, read the canvas with `getImageData`. Compute where things must be from the
stored state with your own formulas (not from the drawing's stored pixels) and centre every scan there:
- the cart: on a row 4 px under its top, the leftmost and rightmost fully painted pixels of its fill colour; centre within 0.75 px;
- a hinge disc: centroid of its pure-colour pixels within 6 px; within 0.3 px;
- the end of a rod with a round cap: along the rod the last fully painted sample lies between r − 1.5 px and r + 0.5 px beyond the end
  (r = half the line width; edge pixels are only partly covered, and a pixel 98 % covered still passes the colour test), the first
  transparent sample within r + 1.5 px; and a scan
  across the rod 6 px inside the end, centred on the axis within 0.75 px.
"Fully painted" means alpha 255 and the colour within 2 or 3 of the expected value: alpha first. Also compare the drawing's stored
pixels with the state turned into pixels (expect identical). Repeat at device pixel ratio 2.

**e. Scenarios.** At least: rest; a flick; a drag with the real mouse (of each thing the reader can grab: in project 05 a rod, held at
rest, and the cart, whose hand force is an ordinary RK4 input that the force check must recompute from its own row); the swing-up from hanging; catches from random falls,
with the supervisor's options both ways (project 05: Arrive moving, then brake and Arrive at rest), and long enough for any governor
to finish (project 05: 6 s after the reference stops); two loop periods (10 and 40 ms); a moving
(glide) reference; a change of the force limit while balancing. Each runs a–d's log and picture checks.

**f. Falsification** (`fals.cjs`). Corrupt one thing at a time, show the tests fail, revert, show they pass: one stored force
+10⁻⁹ N (force check and hold check fail at that sample); one stored state +10⁻¹² rad (both replays and continuity fail at that
step); a copy of the page whose `draw()` uses its own state with x + 1 cm instead of the store (every picture check fails). A check
that does not fail under its corruption is not a check: in project 05 the first tip test passed a shifted display until the
cross-section scan was added.

**g. Cost** (`cost.cjs`). Wrap `requestAnimationFrame` before the page loads and sum the callbacks per frame; 15 s with the panel
closed, the page before your change (a `git worktree` of main) and after, twice each; also the driven physics per frame. Then the
loop's states: closed, open and playing, open and paused, recording with the panel closed, Read values on, a pin, off, closed
(a finished round opens the panel to show its charts: count that, it is not a leak). Then the pointer rules: a sweep across the
running figure with Read values off and on paints 0 overlay pixels and grabs nothing; a press with Read values on pins and grabs
nothing; the strip changes at most about 4 times a second (count over 3 s).

**Behaviour.** Re-run the page's own behaviour tests on main and on your branch, sequentially and alone on the machine (time-
budgeted planning makes results depend on the load), and compare. Check the page in all three languages at 1280 and 390 px:
no page errors, page width equals window width.

Report the raw output of every step, with what failed, what you fixed, and the remaining float gaps named as what they are.

## 8. Pitfalls seen on the site

- A transparent pixel passes a "dark" test: check alpha first. A single pixel at a predicted spot can pass by luck; scan.
- A scan centred on the drawing's own stored position cannot catch a drawing that lies: centre it on the state turned into pixels.
- A pixel bound that ignores antialiasing or float accumulation (a sample position −12 + k·0.05 is not exactly 4.25) fails a
  correct page; set tolerances from the geometry of the drawing, then show with the falsification that they still catch a lie.
- Counters written once per frame while rows are written every step are stale between frames; after a log drops its older half,
  a stale count exposes moved rows. Write counts with their rows (found by the driven test of project 05).
- float32 arrays agree only to about 6 figures; store `Float64Array`.
- Animation-frame order: the page's clock requests its next frame inside its own callback before the panel's `kick()`.
- `draw()` with its own relaxation (a camera that follows at 8 % per frame, a view that widens) must store those states; the
  read-back uses them, and `about` names them.
- `ds.set(name, typedArray)` replaces the data; update the dimension first (`ds.dim`) so `ds.npz()` writes the right shape.
- The clock calls the page every frame even when paused (dt = 0); outside changes then show before a step books them.
- Below about 1500 px the open panel covers the page's controls; tests press buttons by script.
- Arabic: the panel takes `dir="rtl"`; numbers and units stay left to right. Translated words come from `strings.json`.

## 9. Docs, inventory, publishing

- The page's doc (`docs/simulations/figNN-*.md`, or `docs/portfolios.md`): what the store holds at each rate, the sections, the
  books, what each check recomputes, what each read-back reads, and the measured results of section 7.
- `docs/scripts/datalog.md`: the page's round (table of rounds) and book (table of books); "Loaded by".
- `AGENTS.md`: the list of pages that load `datalog.js`.
- `python3 tools/inventory.py` (then `--check`) for `docs/files.md`; `npm run build` (delete a stray `package-lock.json`).
- Keep the test scripts and raw outputs in `notes/…`. Then, per `CLAUDE.md`: branch, PR, merge, wait for Cloudflare, verify the
  live page in headless Chromium.

## Changes from the 23 October version

- Added: the ledger (headline, sections, books, deps, controls, current), which became the panel on 24 October; live pages with a
  sampled controller and a supervisor (section 5); rates and logs (section 4); the energy book under a zero-order hold; the
  required honesty procedure with pass criteria and scripts (section 7); the translation workload and DeepL's known faults.
- Corrected: "Variables lists every group" (the panel shows a ledger); the hard-coded Chromium path (use `require('playwright')`);
  "the panel's words are English today" (they come from `strings.json`, and every `long_name` needs a German and an Arabic entry);
  single-pixel read-backs (scan geometry, centred on the state); "rerun the integrator from the start" as a check of a live page
  (one-step replay plus a chained replay whose gap is measured against the fall rate); "Sim.live" was not mentioned (it must read
  the store); the loop's states and the pointer test now include recording with the panel closed and a pin that must not grab.

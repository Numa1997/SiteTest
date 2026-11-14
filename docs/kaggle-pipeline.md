# The Kaggle pipeline: computing on Kaggle, playing on the website

Started 12 November 2026 with Fig. 14 ([fig14-schrodinger-sphere.md](simulations/fig14-schrodinger-sphere.md)). This page is
the design that every simulation fed from Kaggle follows. It is written so that another project, the next being the Guinness
cart (Fig. 12), can plug in from this page alone.

## The idea in one picture

Think of a bakery that bakes at night and sells all day. Kaggle's graphics cards are the oven: they bake a large tray of runs
ahead of time, and every run baked is kept. The website is the shop counter: it only hands out what is on the shelf, to any
number of visitors, at no extra cost. When a visitor asks for something not on the shelf, the counter does not go silent:
it slows down, shows a rough sketch made on the spot (the live preview), and, once the link is switched on, sends the order to
the oven through one door, the Worker `kaggle-bridge`.

## The parts

| Part | Where | State on 12 November 2026 |
|---|---|---|
| Notebook that computes one block of runs | per project, e.g. [tools/kaggle/schrodinger-sphere/](../tools/kaggle/schrodinger-sphere/) | working; Fig. 14's 405 runs computed and stored |
| Converter to the site's format | per project, e.g. [to_site.py](../tools/kaggle/schrodinger-sphere/to_site.py) | working |
| The store the page reads | one base address per page (`DATA_BASE` in the page's script) | on the website itself, `public/data/<project>/<YYYY-MM-DD>/` (Numa's decision, 12 November 2026; see Storage) |
| The shared page script | [public/scripts/kaggle-flow.js](../public/scripts/kaggle-flow.js), [public/styles/kaggle-flow.css](../public/styles/kaggle-flow.css) | working on Fig. 14 |
| Live preview | per project, a Web Worker, e.g. [schrodinger-live-worker.js](../public/scripts/schrodinger-live-worker.js) | working on Fig. 14 |
| The Worker `kaggle-bridge` | Cloudflare, account of the site | exists with Cloudflare's starter code and the secret `KAGGLE_API_TOKEN` (set by Numa); **no pipeline code deployed**; the pages run with `BRIDGE_URL = null` and say so |

Not yet tested, and needed before the bridge can start Kaggle runs: T1, a Worker holding the token starts a notebook run with
parameters, reads its status and fetches its output (Kaggle's public API, `kaggle kernels push/status/output`); T2, a running
notebook posts its progress and results out to the Worker. Kaggle's own run log stays empty until a run ends (seen on
12 November 2026), so live progress has to be pushed by the notebook.

## Storage: on the website and with the notebook, named by the date of generation

Numa's rule, 12 November 2026, for every project: the data is placed **on the website** and **stays with its Kaggle notebook**,
both named by the date Kaggle generated it.

- On the website: `public/data/<project>/<YYYY-MM-DD>/`, one folder per generation, with its own `index.json` (generation date,
  Kaggle notebook reference and version, git commit of the solver, and per file its size and SHA-256), and
  `public/data/<project>/generations.json` listing the generations. A page reads `generations.json`, then every generation's
  index; a block computed again in a later generation replaces the earlier one. New blocks get their own date; nothing already
  published is rewritten.
- On Kaggle: the notebook's output, filed under the same date (`/kaggle/working/<YYYY-MM-DD>/`, see
  [build_full.py](../tools/kaggle/schrodinger-sphere/build_full.py)). Kaggle keeps the output of every notebook version.
  Fig. 14's first generation, 2026-11-12, was computed before this rule: it lies at the top of version 1's output (`runs/`,
  `index.json`), and its `index.json` on the website names that notebook and version.
- Use the problem's symmetry before storing 3D: Fig. 14 is round about its flight axis, so a cut through the axis holds the whole
  3D field (62.7 MB for 405 runs instead of gigabytes of volumes); prove the symmetry on the stored data and show the proof.
- The website keeps the compact form, the notebook the full one. Fig. 14 stores only the amplitude of ψ on the website,
  46.4 MB for 405 runs, largest file 145 kB; with the phase picture it was 120.0 MB. No number on the page comes from the
  phase, and the full output, phase included, stays on Kaggle. Every file stays far under Cloudflare's 25 MiB per static file
  (developers.cloudflare.com/workers/platform/limits, "Static Assets"; 20 000 files per Worker version on the free plan).

## Store first

A visitor never waits for something already computed. The rules:

1. **One file per block, computed once, kept for good.** A block is the unit a notebook computes in one go. For Fig. 14 a block
   is one run, keyed by its grid indices: `e{i}_v{j}_r{k}.bin`. For the Guinness cart a block is (road, speed, time span).
2. **An index lists every stored block** with its parameters, size and SHA-256 (`index.json`). The page reads the index first
   and marks every control with what is stored.
3. **The page checks every block it downloads** against the SHA-256 in the index (`crypto.subtle.digest`) and says on the page
   whether it matched.
4. **No interpolation between stored blocks.** A control moves in the stops of the grid; between stored frames in time the page
   shows the stored frame at or before the playback time.
5. **Provenance.** `index.json` records the Kaggle notebook, its version and the git commit of the solver that made the data
   (`source`).

## The page side: `kaggle-flow.js`

`window.KaggleFlow` has four pieces. A page supplies its own data, drawing and live solver.

### `KaggleFlow.slider(opt)`

A control over a list of stops, computed or not.

| Option | Meaning |
|---|---|
| `host` | element to build into |
| `stops` | the values a visitor can pick, in order; include stops beyond the computed grid, they are the uncomputed regions |
| `index` | the starting stop |
| `stored(i)` | true when stop `i` is stored for the current values of the other controls |
| `soft` | fraction of the stored band, at each end, over which the control grows heavy; default 0.28 |
| `minGain` | how fast the thumb follows the hand deep in the soft zone and beyond, relative to inside; default 0.22 |
| `format(v)`, `label`, `aria`, `onChange(i, value)` | output text, the control's name, its accessible name, the callback |

What the visitor sees: a hatched track (not computed), a solid band over the stored stops, a fading part at each inner end of
the band (the soft zone), a filled dot under each stored stop and a hollow one under each stop not computed yet, a dashed thumb
on an uncomputed stop, and the words "near the edge of the computed range" or "not computed yet" under it. While dragging, the
thumb moves by (hand movement) × gain, with gain = 1 − (1 − minGain) × closeness, and closeness rising smoothly (smoothstep)
from 0 at the start of the soft zone to 1 at the band's edge; so the control grows heavier the closer it gets, without a step.
A click or a key moves the thumb to the next stop along an eased path (time constant 0.12 s), never a jump.

The returned object: `index`, `value`, `position` (the continuous thumb position), `closeness()` (0 inside, 1 at or beyond the
edge), `heading()` (+1 or −1 when the visitor is in a soft zone heading out of the band, else 0), `stored()`, `band()`,
`refresh()` (call it when another control changed, since what is stored depends on all of them), `set(i, now)`.

### `KaggleFlow.governor(tau, start)`

The playback speed as a first-order lag: `step(goal, dt)` moves the speed towards `goal` with time constant `tau` (Fig. 14:
0.45 s) and returns it. Every change of speed on the page goes through it, so speed never steps.

### `KaggleFlow.popup(host)`

The loading notice. `set({ stage, broken, title, text, progress })` lights the step now working (0 this page, 1 kaggle-bridge,
2 Kaggle GPU, 3 stored, 4 back here), draws a step that is not available dashed (`broken`), and moves a dot along the edge being
worked. `show()` fades it in over 0.6 s, `hide()` fades it out. **A page shows it only when the speed has reached zero because no
data is left to show**; if data arrives earlier, the notice is never seen.

### `KaggleFlow.bridge({ url, project })`

The client of `kaggle-bridge`. With `url: null` every call answers at once `{ state: 'offline', reason }`, so a page behaves the
same, honestly, before the bridge exists. With an address: `request(params)` posts to `POST {url}/v1/{project}/block` and
`status(job)` reads `GET {url}/v1/job/{job}` (the endpoints below).

## The behaviour every page follows

1. Inside the stored region the page plays stored data at normal speed.
2. In a soft zone the control is heavier and the playback slows: Fig. 14 sets the goal speed to 1 − 0.8 × the largest closeness
   of its three controls, and slows towards the last stored frame in time over the last quarter of the run.
3. Entering a soft zone heading out, the page at once asks the bridge for the next block (`heading()`), once per direction and
   position.
4. On an uncomputed stop the page starts the live preview and plays its frames as they come; the visitor's time is kept, and
   until the preview reaches that time the last picture is held, dimmed, and the numbers are those of the held picture.
5. Only when no frame is left to show and the speed has eased to zero does the notice fade in; it fades out when frames arrive.
6. A change of run or of source (stored, live) cross-fades over 0.45 s from the last picture shown.

## The Worker `kaggle-bridge` (design; not deployed)

One Worker for every project and one GPU budget for the whole account: Kaggle gives 30 GPU hours a week (`get_accelerator_quota`,
read 12 November 2026: 108 000 s, reset Saturday 00:00 UTC) and at most two GPU runs at once.

| Endpoint | Does |
|---|---|
| `GET /v1/{project}/index.json`, `GET /v1/{project}/{block}` | serve stored blocks (free, cached) |
| `POST /v1/{project}/block` | body: the project's block parameters. Stored: `{ state: 'stored', url }`. Already queued or running for anyone: the same job (identical requests share one job). Otherwise, within budget: queue it and answer `{ state: 'queued', job, stage, progress }`. Over budget: `{ state: 'needs-grant' }` |
| `GET /v1/job/{job}` | `{ state, stage, progress, lines }` from the notebook's own reports |
| `POST /v1/job/{job}/progress`, `POST /v1/job/{job}/result` | the notebook reports and delivers; protected by a second secret only the notebook run holds |

Rules: one queue, fair turns between projects, one job per identical request, every finished block stored for good, a daily GPU
cap Numa chooses, and the weekly quota read before every launch. Reading stored data is always free; budgets and the grant apply
only to requests that start new computing.

The grant for a visitor who needs more than the budget: the job site (`stellen.phyeinusul.com`) is protected by Cloudflare Access
with an allow list of e-mail addresses (skill `stellen-job-list-upkeep`, section "Page"). The same mechanism fits here: a path such
as `/v1/granted/…` of `kaggle-bridge` behind a Cloudflare Access application whose allow list Numa keeps; requests through it skip
the daily cap but not the weekly quota.

## How a project registers

A project brings five things; nothing in `kaggle-flow.js` or the bridge changes.

1. **A notebook** that computes one block from its parameters and writes one file per block plus progress lines. Fig. 14:
   [build_full.py](../tools/kaggle/schrodinger-sphere/build_full.py) writes it, fetching the solver from this repository at a pinned
   commit (Kaggle's notebook saving drops attached data sources, so code is fetched, not attached).
2. **Its grid of blocks**: the stops of each control. Fig. 14: 9 × 9 × 5 = 405 runs, keyed `e{i}_v{j}_r{k}`. Guinness: road ×
   speed × time span.
3. **Its block format** and a converter to the site format. Fig. 14's run file is `SPH1`, a uint32 header length, a JSON header
   (parameters and per-frame curves), then one zlib stream with the frames ([to_site.py](../tools/kaggle/schrodinger-sphere/to_site.py)).
   The browser inflates zlib with `DecompressionStream('deflate')`.
4. **Its measured cost per block** on Kaggle, so the bridge can size jobs and give an honest time. Fig. 14: 2.3 to 6.9 s per run on a T4
   (`wall` in `index.json`), plus the session's start, not yet measured on its own; the whole grid 880.8 s on two T4s.
5. **Its page**: `kaggle-flow.js` controls, its drawing, and if it can, a live preview checked against Kaggle with the difference
   stated. Fig. 14 states “within 0.08” in probability. A project whose browser solver is not checked shows the held picture and the
   notice instead of a preview.

## Measured numbers (12 November 2026)

| What | Number | Where measured |
|---|---|---|
| Kaggle GPU card | Tesla T4 ×2 | `nvidia-smi` in the notebook |
| One split-step, 128³, 32-bit | 1.61 ms (2.6 ms with the per-frame measurements) | smoke notebook, version 1 |
| Whole Fig. 14 grid, 405 runs | 880.8 s on 2 GPUs, 906 s in the notebook, about 30 min of session | full-grid notebook, version 1 |
| GPU quota used by both notebooks | 3 275 s (from 2 495 s to 5 770 s) | `get_accelerator_quota` before and after |
| Stored data on the website | 405 files, 46.4 MB (amplitude only; 120.0 MB with the phase) | `to_site.py` |
| Live preview, whole run | 11 to 34 s on one core | Node 22, this workspace |

## Projects plugged in

- Fig. 14, the wave packet and the sphere: the first, described above.
- Fig. 12 computed on Kaggle, the Guinness cart (`simulations/guinness-kaggle.html`). Since 13 November 2026 it plays rides
  computed by the JAX solver (`tools/fig12/kaggle/stout_jax.py`, `run_b.py`, packed by `pack_ride.py` into
<<<<<<< HEAD
  `public/data/fig12/2026-11-14-run10/` since 14 November 2026 (run 8's folder `2026-11-13-run8/` before that), listed in `index-jax.json` with each file's SHA-256) through `guinness-jax-play.js` and
=======
  `public/data/fig12/2026-11-14-run10/` since 14 November 2026 (run 10's controlled rides with run 8's other rides; run 8 alone in `2026-11-13-run8/`), listed in `index-jax.json` with each file's SHA-256) through `guinness-jax-play.js` and
>>>>>>> origin/main
  `stout-view2.js`. It follows rules 1, 2, 3 and 5 of "Store first" (one file per ride, an index, a fingerprint check in the
  browser, provenance) and rule 4 (no interpolation: the frame drawn is `round(30 T)`), but uses none of `kaggle-flow.js`: one
  button per stored ride, no slider, governor, live preview, pop-up or bridge; it plays at real speed and stops at the end of
  the stored time. The stored rides are run 10's five controlled rides (Kaggle notebook version 10, the controllers with the head's drive
  coefficient 1.241) with run 8's three speed-held rides and free swing (version 8) and the swing without the head (version 6), ten files; runs 6 and 7 stay in
  `2026-11-13/` for the record. Run 8 waited about 40 minutes for a GPU slot: Kaggle runs at most two batch GPU sessions per
  account at a time ("Maximum batch GPU session count of 2 reached"), and Fig. 15's shards held both. The earlier
  generations (12 and 13 November, the Taichi solver, with `KaggleFlow.slider`, `governor`, `popup`, `bridge` with `url: null`
  and the live preview `guinness-preview-worker.js`) are described in [fig12-beer-slosh.md](simulations/fig12-beer-slosh.md).
- Fig. 15, resonant tunnelling in 3D (`simulations/resonant-tunnelling.html`, 13 November 2026): 115 runs from five notebooks
  (`numakoudsie/fig15-rt3d-shard-{1..4}-of-4`, `numakoudsie/fig15-rt3d-singles-v2`), filed by `file_rt3d.py` under
  `public/data/resonant-tunnelling/2026-11-13/kaggle/` with each file's notebook, version, commit and SHA-256; the page checks the
  SHA-256 in a worker and interpolates between stored frames. Uses none of `kaggle-flow.js`. Details:
  [fig15-resonant-tunnelling.md](simulations/fig15-resonant-tunnelling.md).
- Fig. 15, generation 2 (14 November 2026): the whole parameter space, 3739 runs planned from six shard notebooks
  (`numakoudsie/fig15-rt3d2-shard-{1..6}-of-6`) and a fix notebook (`numakoudsie/fig15-rt3d2-fix1`, the 15 runs that the
  run-length fix of commit 57770d2 lengthened by more than 15 %). Filed by `file_rt3d2.py` under
  `public/data/resonant-tunnelling/2026-11-14/kaggle/index.json` (per run: notebook, version, commit, SHA-256, groups; a spec
  computed in two groups is filed once; a fix notebook's rerun replaces the earlier file and the index records it under
  `replaced`). The run files are not in the repository: they are in the R2 bucket `phyein-usul-runs`, served under `/r2/` by the
  site's Worker ([usul.md](usul.md), "The run store").

## Derived data: generated from stored runs

Started 13 November 2026 with Fig. 15 ([fig15-resonant-tunnelling.md](simulations/fig15-resonant-tunnelling.md)). Numa's rule,
from the Fig. 15 brief: **data generated from other data must have its own place and its own provenance**, so that a reader can
trace any frame back to the runs it was built from.

The Schrödinger equation is linear, so a solution computed once is a basis to build on. Where an exact rule exists
(superposition, mirror images, translations, separation of variables, transfer matrices) a new system is built from data
already stored rather than paid for again; where none exists, the system is computed afresh on Kaggle's GPUs.

Fig. 15 first tried the shortcut alone: a one-dimensional double barrier built by transfer matrices (72 derived runs, `V₀ = 3`).
The owner rejected that on 13 November 2026: the figure continues Fig. 14 and must be three-dimensional. It now plays 115 new 3D
Kaggle runs (`kaggle/`). The exact rules remain where they are exact: separation of variables makes the 3D walls equal to the 1D
problem, so the runs carry their 1D twin and `derived/exact-1d.json` holds the exact transfer-matrix numbers for the same geometry,
**labelled as the check of the 3D runs**; and the page draws the stored half-plane `y ≥ 0` with its mirror image, which is exact
because every barrier and the start packet are symmetric about the flight axis. The 1D derived runs were removed.

**The layout** (the rule for every future derived figure):

- A new tree `public/data/<project>/` with its own `generations.json` and dated folders `YYYY-MM-DD/`. Inside each generation,
  separate subfolders:
  - `kaggle/` for new runs computed on Kaggle, with `index.json` (per file: notebook, version, commit, SHA-256);
  - `derived/` for data computed from other stored data or from exact theory, each file saying what it is (`role`) and which
    script made it.
- Runs that a later version replaced are not shipped; the index says which, why, and what replaced them (Fig. 15: the 20
  single-wall and single-disc runs of version 1, one grid point thick, replaced by `fig15-rt3d-singles-v2`).
- The scripts live in `tools/kaggle/<project>/`. **The page computes nothing it can read from the store**: numbers such as Fig. 15's
  share-through and lifetimes are read from the stored curves once, by `file_rt3d.py`, and written into the index.

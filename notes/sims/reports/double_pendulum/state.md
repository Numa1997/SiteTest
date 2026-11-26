# Fig. 2, Double Pendulum: state of the move to Kaggle data

## SESSION OF 25 NOVEMBER 2026 (branch `kaggelize/fig2-r2`), read this block first
Task (the user, 25 November 2026): kaggelize the next figure through the NEW engine (data in Cloudflare R2, PR 210).
- Figure chosen: Fig. 2, because notes/sims/PLAN.md, table A ("Computed live ... in this order"), row 1 (Fig. 1) is done and row 2 is
  Fig. 2; docs/kaggle-sims.md "Figures on the line" lists only coupled and wave_interference2.
- User's rules for this task: commits as Numa Koudsie only, no AI attribution; own branch; merge main and run tools/inventory.py
  before every PR; finished tested work merged without asking, then verified live; Kaggle runs pre-approved (GPU too) but read the
  GPU hours first and ask if a run takes more than half; watch runs with a monitor; Berlin times from a clock; never delete the old
  live page before the stored one is verified live; if the R2 secrets are missing, stop and give the user the click-by-click steps.
  Code is written by this session (the Neon rule was withdrawn 25 November 2026).
- Blocking decision (below, "What the stored grid can and cannot do"): asked the user at 03:2x Berlin, 25 November. Numbers given:
  per start with its twin 19 594 bytes and 2.605 ms of model time on Kaggle's T4 machine (from run v6: 7 053 765 604 B, 937.7 s,
  360 000 starts). All slider states: 7.99e12 starts, 157 PB. Stored grid A (15 deg, 5 x 5 cells, 5 x 5 omega): 7.05 GB, 0.26 h.
  B (1 deg, 5 x 5 cells, 5 x 5 omega): 81 M starts, 1587 GB, 58.6 h. C (1 deg, 5 x 5 cells, released from rest): 3.24 M starts,
  63.5 GB, 2.34 h. GPU left this week: 108 000 - 4 595 = 103 405 s = 28.7 h (Kaggle connector, 03:22 Berlin), refresh 28 November 01:00 Berlin.
- ANSWER (the user, 26 November 2026): both hybrids rejected. The rule (notes/sims/chaos-and-storage.md): Kaggle computes the
  parameter map and records it as a FILM; the page shows the film beside the live simulation, which stays as it is (browser RK4,
  every control). Chosen map: the flip-time map (theta_1 x theta_2 from rest, time until a rod passes the top, 10 s window),
  swept through ln(m_2/m_1) = -2.3 ... 2.3. Old stored grid (release, 7.05 GB) stays until the film is live, then the user decides.
- Built (branch kaggelize/fig2-r2): tools/sims/dp_film.py (engine), double_pendulum_film_smoke.py (72 x 72, 9 frames, CPU/GPU
  bench), double_pendulum_film.py (720 x 720, 369 frames); registry entries, both "manual", store r2, gpu, dataset fig2.
  Encoding tested here on made-up maps only (no integration). Expected full run from the old measured GPU rate 8.97e7 start-steps/s
  (v6: 720 000 x 12 000 / 96.3 s): 720^2 x 6000 x 369 / 8.97e7 = 12 800 s = 3.6 h; to be replaced by the smoke run's measurement.
- Merged PR 214 (model, registry, notes) at 04:00 Berlin, 26 November. Run workflow double_pendulum_film_smoke (run 45746139071)
  stopped at 04:01 Berlin: "the repository secrets R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ACCOUNT_ID are missing". Nothing
  reached Kaggle. WAITING FOR THE USER to create the R2 token and the three secrets; then rerun the smoke.
- Since then, on branch kaggelize/fig2-r2 only (not on main): the model's start angles now use the page's arithmetic
  (deg * pi / 180); page film figure Fig. 2b (public/scripts/dp-film.js, markup, hook window.__dpLive in the page script).
  Not yet tested in a browser: needs data (the smoke run's).
- Then: Run workflow double_pendulum_film_smoke, read its bench and checks; then Run workflow double_pendulum_film;
  then the page: film figure (video, readout of m_2/m_1, pin a pixel, start it live, three-way proof).
- Nothing built yet on this branch. Next, after the user's answer: model `tools/sims/double_pendulum_r2.py` (dp_engine.py, store r2,
  shards if over about 15 GB per Kaggle version), then the page on simdata.js.


Written 23 November 2026 at 21:58 Berlin time by the session that started the work; the full run's outcome added at 22:10. Read this before anything else on Fig. 2.
All times below are Berlin time.

## The goal
The page `public/simulations/Double Pendulum.html` computes the pendulum's motion in the visitor's browser (RK4, step 1/600 s).
It is to play motion computed once on Kaggle instead, with every control it has today.

## What is live
The old page, unchanged: it still computes in the browser. Nothing of the old work was deleted.

## What is on main
| What | State |
|---|---|
| `tools/sims/dp_engine.py` | The model: JAX on Kaggle's GPU, the page's own RK4 (h = 1/600 s, 64-bit), all starts of one mass-length cell at once, packed per cell. Checks: energy drift per run, the GPU result against a plain copy of the page's RK4, RK4 against DOP853, small-swing periods, twin growth rate. |
| `double_pendulum_smoke` (registry, model, data) | The engine test: 240 starts with twins, one pack of 2 633 430 bytes in the release `sims-double_pendulum_smoke-2026-11-23`. Passed (workflow run 45259655945): GPU result within 1.1e-12 m of the page's RK4 in the first 5 s and within 1 mm for all 20 s. Test data; remove it when the full data is verified. |
| `double_pendulum_gpu` (registry, model, data) | The full run, done: 5 mass ratios x 5 length ratios x both angles every 15 degrees x both starting angular velocities at -5, -2.5, 0, 2.5, 5 rad/s = 360 000 starts, each with its chaos twin, 20 s each. See "The full run" below. |
| `double_pendulum` (registry, `tools/sims/double_pendulum.py`) | The first, rejected plan (CPU, DOP853, 1296 starts from rest). Kaggle computed it (notebook version 3, 451 s on 4 CPUs, 109 files, 17 665 452 bytes) but the save failed, so main has the entry and no data. Remove the entry and the model once the full data is verified; nothing reads it. |

## The full run (done)
Workflow run 45261988429: merged 21:41:34, Kaggle step started 21:43:21, data on main 22:06:57 (commit 5252e1b4), all Berlin time.
- Kaggle: notebook `numakoudsie/phyein-usul-simulations` version 6, two T4 cards, 961.5 s in all; the model 937.7 s, of which 96.3 s
  on the GPU (25 passes of 28 800 pendulums each). Code commit 6ee30d8.
- Data: 3000 runs files in 25 packs, 7 053 765 604 bytes, in the GitHub release `sims-double_pendulum_gpu-2026-11-23`; the packs are
  106 896 241 to 624 769 190 bytes. On main: `public/data/sims/double_pendulum_gpu/2026-11-23/double_pendulum.json` (802 002 bytes:
  every runs file's pack, offset, size, SHA-256, frame rate, energy drift) and `index-double_pendulum_gpu.json`.
- Served: the default start's file (dp_22_19_2.bin, 1 318 432 bytes at offset 121 756 496 of dp_22.pack) was fetched as a byte range
  from `https://phyeinusul.com/rel/sims-double_pendulum_gpu-2026-11-23/dp_22.pack` at 22:07 and its SHA-256 equals the summary's.
- Checks: the GPU result and a plain copy of the page's RK4 differ by 1.1e-12 m in the first 5 s and stay within 1 mm for 20 s
  (default start). No run broke down (`runs_not_finite` 0). Frame rates chosen: 20 to 120 a second; drawn-path error at most 0.16 %
  of l1 + l2 (twin 0.40 %).
- What the checks show about the page's own method: RK4 at h = 1/600 s is the live page's method, and the data reproduces it, errors
  included. Its energy error is small for light and equal lower masses (at most 9.1e-6 of the energy scale for mass ratios 0.1, 0.32
  and 1), reaches 1.0e-3 at mass ratio 3.2, and reaches 0.15 at mass ratio 10 (cells dp_4x). 577 of the 3000 files have a run above
  1e-3, 389 above 1e-2, 50 above 0.1. The live page has the same error today at those settings; it shows it in its drift readout.
  Whether the stored data should keep the page's method or use an accurate one for the heavy lower bob is the user's decision.
- The estimate given before the run was wrong: 22:50 was predicted, 22:07 was measured. The file-writing step was assumed to run
  3.6 times slower on Kaggle than in a workspace (measured on Kaggle's CPU notebook); on the GPU machine the whole model took 938 s.

## Branches (none merged; none may be deleted before the new page is verified live)
- `kaggelize/double_pendulum-page`: a page that plays the first plan's small files (label DPN1, one file per starting angle), with a
  rewritten walkthrough, lecture-note sections 7 to 9 and a doc section. It was tested only against data made in a workspace. It does
  not fit the packs of the full run (label DPN2, byte ranges, starting angular velocities), and its texts describe DOP853, not RK4.
  Useful as a base for the player, the data panel hooks and the waiting sentence; its texts must be written again.
- `kaggelize/double_pendulum`: the first study, the first page draft, and `tools/kaggle/double-pendulum/` (an earlier copy of the GPU
  model and a notebook runner, superseded by `tools/sims/dp_engine.py`).
- Merged and no longer needed, but GitHub refused their deletion from a session: `kaggelize/double_pendulum-model`,
  `kaggelize/engine-gpu-release`, `kaggelize/double_pendulum-gpu`, `kaggelize/prompts-lessons`.

## What the stored grid can and cannot do (the open decision)
The live page's sliders reach about 8e12 different starts (mass 93 steps, length 65, each angle 361, each angular velocity 101).
The double pendulum is chaotic, so the motion from a start between two stored starts cannot be made from its neighbours. The full
run stores 360 000 starts. A page that plays it must move its sliders in the stored steps (angles 15 degrees, five ratios, five
angular velocities), and it cannot change the mass while the pendulum moves (the "sand" parameter curve). That is a cut against
the live page. The user has not agreed to it; the user's rule is that every control stays. Bring the user the numbers and the roads
(a finer grid and its size; which controls matter) before building the page, as step 3 of notes/sims/KAGGELIZE-PROMPT.md says.

## What is left
1. (done) The full run.
2. The decision above.
3. The page on the stored packs: one runs file is a byte range of a pack (`pack`, `offset`, `bytes`, `sha256` in
   `double_pendulum.json`), fetched from `/rel/<release>/<pack>` today and from R2 after the engine rebuild
   (notes/sims/ENGINE-PROMPT.md).
4. Walkthrough, lecture note, doc, German and Arabic, registry page and probe, PLAN.md row, docs/kaggle-sims.md row.
5. Compare old and new, publish, verify live; only then remove the old computing code, the test data and the first plan.

## Copies on Kaggle (23 November 2026)
- Every run is also filed in the figure's private Kaggle dataset `numakoudsie/fig2-double-pendulum` (PR 194, tools/sims/dataset.py),
  laid out `phyein-usul-simulations/v<version>/output/` with log and manifest: smoke v5 (run 45269535877, started 22:25 Berlin),
  then the full run v6 (7 053 765 604 bytes), filed after smoke so the newest dataset version holds both. Done: dataset version 2,
  present at 22:44 Berlin time, 34 files, checked by the connector (26 packs, 7 056 399 034 bytes = v6 + v5).
- The first filing scheme (PR 193) named datasets `phyein-usul-<sim>` against the per-figure rule and landed flat; only Barton's
  went through (`numakoudsie/phyein-usul-barton` version 1, flat files). It is kept; the next version has the proper layout.

## What went wrong in the first session (each is now a rule in notes/sims/KAGGELIZE-PROMPT.md)
- It followed an old prompt's "test locally" and "launch nothing on Kaggle" against the user's rule that every run happens on Kaggle.
- It cut controls to fit a 20 MB budget and built a page, a note and a walkthrough on that before the data existed.
- It dropped the user's chosen plan twice and asked for a yes the user had given.
- It merged a model while another session was merging; the engine's save clashed and a computed run was not saved (the engine is
  fixed since pull request 183).
- It gave times in UTC, guessed durations, gave a merge time from memory that was 7 minutes off, and watched runs by hand until the
  user demanded a monitor.
- It removed the model's progress file, so nothing but Kaggle's own log page shows how far a run is.
- It kept this state on a branch, where a session starting from main could not find it.
- It named the Kaggle datasets without reading docs/kaggle-pipeline.md, and gave a start time (22:31) that the clock had not reached.

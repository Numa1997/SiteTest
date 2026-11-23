# The engine "Simulations on Kaggle", rebuilt on R2: state of the work

Read this first after a compaction. Task: notes/sims/ENGINE-PROMPT.md (the user's prompt of 23-24 November 2026). Times are Berlin time.
Started 24 November 2026, 00:58, session branch `branch/zealous-shannon-dx4bmj`.

## The aim (the user's, not to be reopened)
One model file merged on main, and then, by itself: Kaggle computes (GPU only where a benchmark shows it is faster), every file is
checked by SHA-256 and stored in the R2 bucket `phyein-usul-runs`, the repository keeps only the small indexes, the site serves the
data under /r2/, the live page is checked, superseded data is removed, and every run's whole output is also filed in its figure's
private Kaggle dataset. All stored simulation data that exists today moves to R2 (item J). No page is converted from live computing.

## How this session works (the user's rules)
- **I write no code** (rule of 24 November 2026): every line of code (.py .js .mjs .html .css .yml .json .sh, notebook text) comes
  from Neon (a Gemini model the user runs) through the user, as answers to numbered requests N-<n>. I apply answers byte for byte,
  test exactly as announced, and on a failure write the next request; I never repair code myself. Prose (docs, notes, this file,
  commit and pull request texts) is mine.
- Commits: `git -c user.name="Numa Koudsie" -c user.email="numakoudsie@gmail.com"`, no co-author, no session link, no AI attribution,
  in commits and pull requests. Prose says "the user".
- Merge only by the pull request number the create call returned, with its head SHA; merge main into the branch first, keep every
  other session's lines, regenerate docs/files.md (`python3 tools/inventory.py`).
- Finished, tested work is merged and published without asking, then verified live.
- The prompt is the user's yes for every Kaggle run of this task through the engine, GPU included. Before a GPU run, read the weekly
  GPU hours left; if a run would take more than half of them, stop and ask with the numbers.
- Watch every run with a monitor (tools/sims/watch.sh once it exists), never a scheduled task or a blocking sleep loop.
- Clock times from a clock, in Berlin time; durations from measured runs with the calculation shown; measure, never estimate.
- Never delete old work before the new work is verified live. Never touch another session's branch, pull request or scheduled task.
- The user's memory files named in the prompt (/preferences.md, /areas/computational-physics.md, /areas/personal-website.md) are not
  on this machine (searched the whole file system, 24 November 00:58); the rules above come from the prompt, CLAUDE.md and the two
  skills phyein-usul-kaggle-pregenerate and kaggle-gpu-run, read at the start.

## What is live (measured 24 November 2026, 00:58)
- main at d53bb69. Engine as described in docs/kaggle-sims.md: one notebook `numakoudsie/phyein-usul-simulations` for every
  simulation, one concurrency group, data in public/data/sims/<sim>/<date>/, large files in GitHub releases served under /rel/.
- generations.json: barton 2026-11-21 v1; wave_interference2 2026-11-23 v4 (290 files); double_pendulum_smoke v5 (1 pack, release);
  double_pendulum_gpu v6 (25 packs, 7 053 765 604 bytes, release; data saved, but its live check failed on a /rel/ 404, run
  45261988429); coupled 2026-11-23 v10. double_pendulum is in the registry without data (fault 12).
- The R2 key of the Claude cloud environment "Default" works in this session: GET api.cloudflare.com/client/v4/accounts answered 200
  (24 November, 00:59). Usable for item J only.
- Fig. 15 filing (mode figure) run 45287689725: still in progress at 00:59; check its result before counting Fig. 15 as filed.
- No attached computer: this session has no browser on the user's machine, so the engine's own R2 token and the three repository
  secrets (item A) cannot be made from here yet.

## Plan, in the order of work (each code step is one or more Neon requests)
1. **Worker** (item A, serving): worker/r2.js serves `/r2/<key>` from RUNS for three key families, with byte ranges (206,
   content-range) and the immutable cache: `sims/<sim>/<date>-v<version>/<file>` (engine runs), `data/...` and
   `simulations/fig13/...` (files moved by item J keep their repository path under public/ as their key, so a page's address changes
   only by the prefix /r2/), and Fig. 15's existing `resonant-tunnelling/<date>/runs/<file>.bin`. /rel/ stays until nothing reads it.
   Test: `npx wrangler dev --local` with objects put into the local R2, curl for 200, 206 with Range, 404 outside the families, HEAD.
2. **simdata.js** (item F) and docs/scripts/simdata.md; tested in headless Chromium against a local server; no page converted.
3. **Move tool and mode move** (item J) and the per-figure moves, one figure at a time, in the order of the prompt's table, each with
   its screenshot comparison before and after, and the repository copy removed in a separate pull request.
4. **Engine on R2** (items A upload, B, C, E, G, H, I, K, L): one notebook per simulation, concurrency per simulation, reconcile,
   formats, run addresses `<date>-v<version>`, upload with read-back, status files, watch.sh, collect mode, clean-up.
5. **Bench mode** (item D) and the sims_smoke scenario tests, each recorded in docs/kaggle-sims.md.
6. Docs: docs/kaggle-sims.md rewritten, docs/usul.md, docs/files.md via tools/inventory.py, the skill text in notes/skills/.
Blocked until the user's machine is attached: the engine's own R2 token and secrets R2_ACCOUNT_ID, R2_ACCESS_KEY_ID,
R2_SECRET_ACCESS_KEY (item A); every engine upload step depends on them.

## Neon requests
| Request | What | State |
|---|---|---|
| N-1 | worker/r2.js: the three /r2/ key families with byte ranges | written 24 November, waiting for Neon's answer |

## Commits of this work
- (this file) first commit of the state.

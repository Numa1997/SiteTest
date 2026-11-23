# State of the Kaggelize session for Fig. 2, Double Pendulum

Kept current at every step that changes what is live or what is left (CLAUDE.md). Branch `kaggelize/double_pendulum`.

- Aim: the page `public/simulations/Double Pendulum.html` plays runs computed once on Kaggle by `tools/sims/double_pendulum.py`.
- Rules of the task: work alone (no subagents, no Kaggelize workflow); commits as the last human author on main, no co-author or
  session lines; do not touch .github/, .claude/, tools/sims/pipeline.py, kaggle_sims.py, verify_live.py, tools/sims/agents/,
  public/data/sims/; launch nothing on Kaggle; stop after the build and wait for the user's yes before merging.
- Done: step 1, the study (`study.md`); the model written and run here (108 files, 17 635 750 bytes, 253 s on 2 CPUs).
- 23 Nov, later: page player, registry entry and note sections 7-9 drafted on the branch. The user objected to the cut
  controls (ω sliders, sand curve, 30° grid, 20 s runs): building is stopped until the user chooses between a fine grid stored
  in Cloudflare R2 and leaving Fig. 2 live. main and the live site are untouched; nothing deleted.
- Left (if the user says go): step 2 build (registry, page player, walkthrough, note, doc, German and Arabic pages, docs, inventory); step 3 show and wait;
  step 4 publish after the yes; step 5 final doc.
- 23 Nov, evening: the user rejected every cut ("everything we have now on the site computed on Kaggle", "known for using the
  GPUs"). New route: `tools/kaggle/double-pendulum/dp_gpu.py` (JAX, GPU, the page's own RK4 h = 1/600 s in float64; grid: 5 mass
  x 5 length ratios, angles every 15 deg, omega1, omega2 in -5..5 rad/s in 5 steps: 360 000 starts with twins, 3000 files) and
  the notebook runner `notebook.py` (notebook `phyein-usul-double-pendulum-gpu`, private). Launch of the smoke test was blocked
  by the app's safety check; waiting for the user's yes for that exact run. No more local runs (memory rule: every run on Kaggle).
- Open: the full data (about 6 GB, estimate) needs R2; this session has no Cloudflare token (API answers "Missing Authorization").
- 23 Nov, 20:56 Berlin: model `tools/sims/double_pendulum.py` (CPU, DOP853, 108 files, 17.7 MB) merged alone (PR #179). Kaggle computed
  it (notebook version 3, 451 s on 4 CPUs, output still on Kaggle), but the save failed at 21:08: `git pull --rebase` met a clash in
  `docs/files.md` with another session's merge. Nothing reached main. Its registry entry is on main, without data.
- 23 Nov, 21:28 Berlin: engine fixed (PR #183): `tools/sims/land.py` (save without clashes), registry `gpu`, `timeout_s`,
  `store: release` + `release_files` (large files into the GitHub release `sims-<sim>-<date>`, served by the Worker under `/rel/`),
  live check step 2b. Test `double_pendulum_smoke` ran through all of it by itself: Kaggle GPU (notebook version 5, 22 s), release
  `sims-double_pendulum_smoke-2026-11-23` (dp_22.pack, 2 633 430 bytes), landed on main 21:31, live `/rel/` file fetched whole and its
  SHA-256 equals the index; workflow run 45259655945 green, both jobs.
- Left: (1) the full GPU run: a registry entry `double_pendulum_gpu` (model wrapper calling `dp_engine.run(out)`, gpu, release,
  `*.pack`), 360 000 starts, about 4 GB scaled from the test (10 973 bytes per start); needs the user's yes, it spends GPU hours.
  (2) the page: the draft on this branch plays the small CPU format (DPN1, one file per theta1); it must be changed to the packs
  (DPN2: byte range of one runs file from `/rel/`, offsets and SHA-256 from `double_pendulum.json`), with the omega sliders back
  and finer steps (15 degrees, 5 ratios). The old live page stays until that is verified. (3) clean-up refused by GitHub: branches
  `kaggelize/double_pendulum-model` and `kaggelize/engine-gpu-release` (both merged) could not be deleted from this session.

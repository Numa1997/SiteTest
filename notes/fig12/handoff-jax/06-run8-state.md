# Fig. 12 in JAX: this chat's full state (14 November 2026, 01:40 UTC)

This file is the memory of the chat "Guinness cart: JAX solver, fix and run" (branch `claude/nifty-lamport-iz5pua`).
After a compaction, reread this file before doing anything else. Keep it current: change it at every step that changes
what is live or what is left, then commit and push. The rule is in CLAUDE.md ("Write the chat's state into the repository first").

## The aim

A pint of Guinness on a one-wheel cart, over bumps, on the live page https://phyeinusul.com/simulations/guinness-kaggle
(`public/simulations/guinness-kaggle.html`). The stout, its head of foam and the cart are computed in JAX on Kaggle's GPU
(private notebook numakoudsie/guinness-on-a-cart-stout-in-jax), stored, and only played by the page. Real numbers from first
principles; no slowed animation, no interpolation between runs, no physics in the browser. Then control the pint so it does
not spill, and show with and without control side by side.

## What is live (main at 4f77d6a, checked on the live site 14 November 2026, about 00:30 UTC)

- The page plays run 8: `public/data/fig12/2026-11-13-run8/index-jax.json` and the ten files it lists, 2.7 MB in all
  (`DIR` in `public/scripts/guinness-jax-play.js`). Default ride: five bumps in step, joint control (`ride_resonant_joint`).
- Run 8 = notebook version 8 at commit 96e8a1d: rest, free swing with the head, and the eight rides (three roads with the
  speed held; joint control on all three; slosh LQR on the kerb). Version 9 at commit 726d51a: the kerb with road preview,
  which run 8's 2,500 s budget skipped, computed alone with run 8's measured plant. The swing without a head is run 6's file
  (no head, so the head's mass cannot change it), labelled as run 6.
- Every check passed: `notes/fig12/jax/run8-check/run8-check.txt` and `run9-check.txt` ("ALL PASS"), with the per-task
  times in `run8-summary.json` and `run9-summary.json` (task times 2,170 s for run 8, 185 s for version 9, on a Tesla T4).
- Books closed in every stored frame of every task: 0 stout particles lost of 1,001,952; head in the glass + head broken off
  = 91.314 mL served, to at most 1.3e-8 mL.
- The head's mass is in the solver: swing with the head 2.915 Hz natural frequency (expected 2.957 Hz, -1.4 %, check is
  3 %), damping ratio 0.425; run 6 without the head's mass had 3.278 Hz, 0.467. Gains designed on it in the run:
  K = (74.004, -1295.010, -44.866, -150.000).
- Leans (front wall minus back, from the trusted columns, `measured.lean_max_mm` in index-jax.json), speed held -> control:
  five bumps 13.9 -> 0.95 mm (joint); one 25 mm bump 8.9 -> 0.76 mm (joint); kerb 24.3 mm and 2.44 mL of head spilled with
  the speed held, joint 25.4 mm and 2.00 mL, slosh LQR 21.8 mm and 1.65 mL, road preview 21.2 mm and 2.46 mL. No stout
  spilled on any ride. Against run 6: kerb head spill 4.08 -> 2.44 mL, stout 0.008 g -> 0.
- Page readings: "stout in the glass" (3 decimals, from `stout_g`), "stout spilled", "head in the glass" (from `vhead`),
  "head spilled". Live check at the kerb's picture 27: 429.583 g, 0.000 g, 88.93 mL, 2.38 mL, 338 drops and lumps
  (test script: scratch `live8.cjs`; the page test in the repository is `notes/fig12/jax/page-test.cjs`).
- The only console error on the live page is Cloudflare's own analytics beacon, blocked by the page's CSP. Not from the
  repository; leave it, and never touch the Cloudflare Workers.
- `public/data/fig12/generations.json`: new generation "jax, the head with its mass" (runs 8, 9 and run 6's free_wall); the
  JAX generation of runs 6 and 7 marked as played until 14 November 2026. Runs 6 and 7 stay in `public/data/fig12/2026-11-13/`.
- The note: sections 5.6 (eqs. 15a, 15b), 7.3 (eq. 18a and the CPU test), 9 (readings and books), 10 (run 8, Table 4 with
  run 6 in brackets, "What the head's mass changed"), 11 (Examples 11.2, 11.4, 11.5, Tables 7 and 8, Floquet), 12 (limits,
  Problems 12.10, 12.11) and the abstract describe run 8.

## Now (14 November 2026, 01:40 UTC): run 10, the user said yes ("Yes and yes": push main, and rerun with beta fixed)

- main fast-forwarded to b4e8287 (this file and the CLAUDE.md rule).
- Commit 58eea68 (branch only so far): `run_b.py` takes beta = 1.541 / 1.2416 = 1.2409 with the head's mass (`BETA_HEAD`, on
  by default, off for RUNSET=run8 so run 8 stays reproducible); `RUNSET=run10` = rest + the five controlled rides. CPU code
  check passed (scratch cc10). Gains with it: K = (71.12, -1229.3, -40.48, -150) against run 8's (74.00, -1295.6, -44.85, -150).
- Notebook text for run 10 ready (scratch nb10.txt): commit 58eea68, BUDGET_S 2450, PLANT_F0 2.9152394311359466,
  PLANT_ZETA 0.4250231022393094 (run 8's measured swing). About 1,450 s of T4 time. Quota at 01:30 UTC: 4,840 s used,
  43,003 s reserved by running sessions, of 108,000 s; resets 21 November.
- Saves at 01:25 and 01:32 UTC refused: "Maximum batch GPU session count of 2 reached". The coordinating chat (01:48 UTC,
  relaying the owner) says both slots are Fig. 15's resonant-tunnelling shards 3 and 4; shards 5 and 6 launch at 03:50 UTC and
  the batch ends about 07:00-08:00 UTC. So the retry (scheduled task trig_01A88VQufSbA2wwGEA8Jxsps) was moved from hourly to
  08:00 UTC: check read-only that a slot is free and no Fig. 15 shard is running or queued, then launch; else every 30 minutes.
  Never touch their kernels; do not message that chat.
- The same message asks for no new control work (the five controllers are the control system) and, while waiting, a full
  rewrite of the Fig. 12 lecture note to a high standard (every number printed by a script from the stored runs, derivations,
  derivation-checker and referee agents). Asked the user to confirm; the user said yes (14 November, about 01:55 UTC):
  "Yes, since you haven't much to do now except that and pushing".

## The note rewrite (started 14 November, about 02:00 UTC)

Brief (from the coordinating chat, approved by the user): honest (every number printed by a script from the stored runs; a
paragraph where the picture differs from the data; every approximation named with its cost; the kerb limit 82 N vs 15 N);
derived (Navier-Stokes in the cart's accelerating frame, free surface, APIC vs PIC; the first slosh mode and its frequency;
each of the five controllers (speed, preview, slosh LQR, joint, skyhook) with law, state, reason, LQR cost and Riccati,
skyhook's inertial damper; the mass books and tolerated drift); every equation numbered, every symbol defined with unit where
it first appears, limits checked; everyday picture first; short plain sentences; no forward references; every figure caption
says axes, colours, what to notice, and which page control gives which view. No new control work.
Judging: independent readers (referee agent) given only "Fig. 12" and the page path: one as the owner (BSc physics, reading
for pleasure), one as a strong school student or first-year; fix every stop; fresh readers again until a full reading has
no stops; the derivation-checker alongside. Round 0 done (notes/fig12/readers/): first-year reader 104 marks, owner reader 116, derivation check 213 verified / 9
wrong / 26 unverifiable. The rewrite waits on the user's choice (asked 02:30 UTC): write it here, or hand it to a new writer
session as the coordinating chat proposed (prompt to be saved first in notes/fig12/handoff-note-writer.md).
Report: what was written, each round's marks and the answer to each, the
checker's result, and when run 10 launched.
Plan: round 0 readers and checker on the current note (outputs in notes/fig12/readers/), while writing the numbers script
tools/fig12/kaggle/note_numbers.py (prints every run number from public/data/fig12/2026-11-13-run8/ and the summaries) and a
check that each number in the note matches it; then rewrite section by section; rounds until no stops.
- LAUNCHED 14 November 08:01 UTC as notebook version 10 (quota 46,099 s used, 0 reserved, of 108,000 s; no Fig. 15
  session held a slot). Next: wait for COMPLETE, download to scratch run10/, then the steps below.
- DONE 08:26 UTC, ALL PASS (notes/fig12/jax/run10-check/). Books closed every frame (0 particles; head <= 1.26e-8 mL).
  Gains K = (71.121, -1228.717, -40.499, -150). Leans / tilts / head spilled (run 8 in brackets): five bumps joint 1.03 (0.95)
  mm; 25 mm bump joint 0.88 (0.76); kerb joint 25.41 (25.37) mm, 2.07 (2.00) mL; slosh 21.84 (21.83), 1.63 (1.65) mL;
  preview 23.87 (21.17), 2.51 (2.46) mL. No stout spilled. The correction changes almost nothing; slightly larger leans
  (smaller gains). Packed in public/data/fig12/2026-11-14-run10/ (run 10's five + run 8's speed-held three + free_full,
  run 6's free_wall). NOT yet on the page: section 11's design numbers (gains, eigenvalues, sampled loop, Floquet,
  Examples) all follow from beta and must be recomputed in the note first; the page stays on run 8 until then.
- After it runs: download outputs to scratch run10/, check_run.py, pack into a new folder public/data/fig12/2026-11-14-run10/
  with run 8's speed-held rides and swings copied beside it (the page plays one folder), point DIR in guinness-jax-play.js at
  it, update generations.json, the note (sections 10 to 12: Tables 7 and 8, the beta caveat removed), the docs; test in
  Chromium; merge; check live; report once.

## What is left

1. The controllers' beta (being done as run 10, above). They used beta = 1.541 (bare stout, `PLANT` at `tools/fig12/kaggle/run_b.py:50`). With the head
   carried up and down but not pushed along the road it should be 1.541 / (1 + m_s k / rho) = 1.241. The gains would be
   K = (71.12, -1228.72, -40.50, -150.00), within 10 % (note section 11, "Which swing the regulator is designed for").
   Not rerun. A fix would set beta in `PLANT` from the head's mass and rerun the five controlled rides with
   PLANT_F0=2.915, PLANT_ZETA=0.425: task times about 1,220 s plus compiling, so about 1,450 s of T4 time (inference from
   `run8-summary.json`). GPU time needs the user's yes, with the one-line cost first.
2. The kerb. No controller cuts the kerb's lean much (24.3 mm held, 25.4 joint, 21.8 slosh, 21.2 preview); slosh LQR cuts the
   head spilled most (2.44 -> 1.65 mL). The note says why (section 11, Figure 4, key result "what no controller with this
   motor can prevent"): the kerb pushes the wheel back with up to 82 N, the motor gives at most 15 N. Nothing ordered on it.
3. The user's coordinating chat was not told directly: the message to it was refused (not in the same channel). The
   user has the report in this chat.
4. Kaggle: at most 2 batch GPU sessions per account; another chat's Fig. 15 shards held both before run 8. The weekly quota
   reset at 00:00 UTC on 14 November; read it with the Kaggle connector before any run.

## The run-8 order (done; kept for the record)

From the user's coordinating chat, 13 November 22:04 and 22:25 UTC: (1) mass books per frame for stout and head; (2) the
head thinning on screen with "stout in glass" and "head in glass" readings; (3) the head's mass in the solver (272 kg/m3,
19 mm), checked on the CPU first (6 mm grid: 2.737 Hz against 2.722 Hz predicted); (4) recompute every ride the page plays
and both free swings, under 1.5 GPU hours; (5) store as run 8, keep runs 6 and 7, update generations.json, the note
(sections 9 to 12), the docs and the readings; merge; check live; report once. All five done; report sent 14 November.

## Commits of this chat (all on main)

- a704e01 the state before run 8 (this file's first version)
- 6cf0028 the head's mass in the pressure solve (Robin condition, the head's own vertical velocity `wh` as state)
- 74244ee run 8 set-up: books every frame, the plant measured in the run, stout and head in the glass on the page
- f3e5455 note sections 5.6 and 7.3; `check_run.py` checks the books and the new frequency
- 96e8a1d run 8 tasks road by road; the swing fit tries the head's decay times; the plant gate rejects runaway fits
  (notebook version 8 ran this commit)
- 01335dc the doc describes run 8's code
- 726d51a `run_b.py`: a task computed alone can take run 8's plant (PLANT_F0, PLANT_ZETA); notebook version 9 ran this
- 4f77d6a the page plays run 8; data, generations.json, note sections 9 to 12, docs, files.md
- this commit: this file, the check outputs, the CLAUDE.md rule, `pack_ride.py`'s folder example

## Files and what each does now

- `tools/fig12/kaggle/stout_jax.py`: the solver. State `wh` (the head's vertical velocity per column); `_surf_faces`;
  `pressure(..., mu, w_old, geff_dt)` with the head's mass as a Robin condition, theta' = theta + mu/dx, mu = 5.13 mm;
  `observe` returns `vhead` (float64 sum). Cart and the controllers (speed, preview, slosh LQR, joint) live here too.
- `tools/fig12/kaggle/run_b.py`: the tasks. `RUNSET=run8` runs `TASKS_RUN8` and measures the plant from free_full_1.5
  (`PLANT_FROM_RUN`); gate 2.5 < f0 < 3.5 Hz, zeta < 0.95, amplitude < 20 mm, rms < amplitude/4, or it stops. `HEAD_MASS`
  (default on); `PLANT_F0`, `PLANT_ZETA`, `PLANT_FROM` give a lone task the plant. Stores `info["books"]`,
  `info["head_mass"]`, `info["plant"]`.
- `tools/fig12/kaggle/pack_ride.py <npz> <summary> <task> <data folder> <version> <commit>`: packs one ride for the page,
  with `stout_g`, `spill_g`, `head_glass_ml`, `books`, `plant`, and the leans read from the trusted columns.
- `tools/fig12/kaggle/check_run.py`: the checks (books 0 particles and < 1e-3 mL; frequency within 3 % of 2.957 Hz).
- `tools/fig12/kaggle/nb/run_b_cell.py`: the notebook cell template (`__RUNSET__` placeholder).
- `public/scripts/guinness-jax-play.js`, `public/simulations/guinness-kaggle.html`, `public/data/fig12/...`: above.
- `docs/simulations/fig12-beer-slosh.md`, `docs/kaggle-pipeline.md`, `docs/files.md` (from `tools/inventory.py`).
- `notes/fig12/jax/page-test.cjs` (reads r-sg and r-hg); `notes/fig12/jax/run8-check/` (the run's own checks).
- Earlier notes of this work: `notes/fig12/handoff-jax/00-PROMPT.md` to `05-run3-changes.md`, `handoff-guinness-cart.md`,
  `portcheck.txt`.

## Where the raw outputs are

The run's .npz files are only in this container's scratch folder (gone when it is reclaimed) and in the notebook's outputs
of versions 8 and 9 on Kaggle (fetch with the Kaggle connector's download, then curl the URLs it gives). Everything the page
needs is in `public/data/fig12/2026-11-13-run8/`. Scratch scripts of the analysis (`design8.py`, `reduced8.py`, `loop8.py`,
`floquet8.py`, `live8.cjs`) went into the note's numbers; they are not in the repository.

## Rules (the user's)

- Never ask for, print, log or store the Kaggle token. Kaggle notebooks stay private.
- Never touch the Cloudflare Workers `phyein-usul` or `stellenrecherche`. Deploying code to `kaggle-bridge` and spending
  money need the user's yes.
- No model names in code, commits or PRs.
- Never put data from a run that failed its checks under `public/`. Stop a run that does not have proper numbers.
- JAX only, no Taichi. Never slow the animation, never interpolate between runs, never compute physics in the browser.
- Before every GPU run: one line with what runs, where, how long and what it costs.
- If self-harm language appears: stop, answer the person, give Telefonseelsorge 0800 111 0 111 or 116 123, emergency 112.
- Talk: plain short words. No tables, no apologies, no recaps, no option lists, no "Where we are" lines. Mark facts with a
  handle. Report once when done; "Do not get back to me unless done." The user's profile also holds a constitution
  (metric units; fact, inference and opinion marked; trigger words Feynman, Planck, Popper, Dirac); the talk rules above
  are what the user set for this work.
- CLAUDE.md: when a change is finished, checked against main and tested in a real browser, merge and publish without asking,
  then verify the live site. A change is not done until the docs describe the code. Push to `claude/nifty-lamport-iz5pua`
  and fast-forward main.
- First write the chat's full state into the repository (this file), and keep it current.

## The note handed over (14 November 2026, about 08:50 UTC)

The user: "Hand it over for god sake". The full prompt is in notes/fig12/handoff-note-writer.md; the writer session
"Fig. 12 Guinness: lecture note" works on branch claude/fig12-note (from this branch at the commit that added that file)
and publishes run 10 with the note. This chat does not write the note any more.

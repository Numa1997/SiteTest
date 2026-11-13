# Fig. 12 in JAX: the gates. Nothing is launched on the GPU until every gate before it is printed as PASS

Each gate has a command or a fixed procedure and a pass line. The pass lines go into the chat, as evidence, before the launch is
asked for. A gate that cannot be run is reported as "not run" with the reason; it is never assumed.

## Gate A. The code is the code (free, static)

1. `python3 -m pyflakes tools/fig12/kaggle/stout_jax.py tools/fig12/kaggle/run_b.py tools/fig12/kaggle/gate_rest.py` prints nothing.
2. The work is committed and pushed: `git status --short` prints nothing; `git rev-parse HEAD` equals the commit in the notebook cell
   (`tools/fig12/kaggle/nb/run_b_cell.py`, twice: the comment and `BASE`).
3. `curl -s -o /dev/null -w "%{http_code}" https://raw.githubusercontent.com/Numa1997/SiteTest/<commit>/tools/fig12/kaggle/stout_jax.py` prints 200.
4. Every function changed since the last run that passed its result gates is listed in the launch message by name.

## Gate B. The pint at rest (free if the user allows the CPU; otherwise the first minute of the GPU run)

`tools/fig12/kaggle/gate_rest.py`: the full model, a coarse grid (4 mm), one simulated second at rest. It checks:
- every column well inside the glass holds a surface value;
- the surface is within 0.2 cells of the fill (this fails if heights are rounded to cell centres);
- no column outside the glass holds a value;
- the head has lost nothing;
- the head is 19 mm thick;
- no stout has left;
- the stout is still;
- the near-surface list did not overflow;
- nothing is NaN.

Status: written on 13 November 2026 and **never executed**. Its first run must itself be read critically: a gate that passes
because of its own bug is worse than none.

- If the user allows runs on the session's CPU (open question 1 of the handoff): run it there first. It needs JAX on the CPU
  (`pip install "jax==0.4.35" scipy`), which the user's rule "nothing is developed on the CPU as the product" permits only as a check.
  Say before running: what, where, how long, cost none.
- If not: make it the first step of `run_b.py`, so that a failure stops the Kaggle session within about a minute. That costs
  about 120 quota seconds per failed launch; say so in the budget.

## Gate C. The arithmetic of every term (free, by hand, before coding the term)

For each force or constraint in the model, write in the code comment and in the launch message its size against its competitor
for the first slosh mode: amplitude 4 mm, 3.42 Hz (omega 21.5 rad/s), wave number 47.1 1/m, wall speed 0.086 m/s, restoring
pressure rho g A = 40 Pa.

Worked for the terms now in `stout_jax.py` (Inference, by the previous session; check them):
- Glass boundary layer: rate 0.110 1/s against omega 21.5 1/s. A small force. Explicit is fine.
- Surface skin: the same rate again.
- Head's weight: rho_f h_f = 5.2 kg/m² on the surface; uniform, so it changes no flow at rest.
- Head gripping only the edge cells (run 2): velocity change per 2 ms step 0.12 m/s against a wall speed of 0.086 m/s.
  **Saturates in one step: it acted as a pinned edge, not as friction.** Replaced.
- Head as a sheet in shear (`head_sheet`, unexecuted): shear rate omega A / R = 2.2 1/s; foam stress about 13 Pa; pressure on the
  stout about h_f tau / R = 6.5 Pa against 40 Pa restoring; modal rate h_f eta k³ / rho = about 12 1/s against omega 21.5 1/s.
  Prediction: the swing dies within about one period; it stops when rho g A falls to about 5 Pa, near 0.5 mm.
  Layer rate h_f eta k² / (rho 2dx) times dt = about 0.3: implicit solve needed and used.
  **If run 3 does not show this, either the model or its code is wrong: decide which before any data run.**

## Gate D. The budget (before asking the user)

1. Read the quota now (`get_accelerator_quota`). Quote used and total.
2. Run seconds = sum over tasks of (steps × measured ms per step) + 10 s compile per task + 40 s start-up.
   Measured at 1.5 mm (run 2): 62.6 ms at rest, 76.2 ms in a free swing, 111.4 ms in a hard slosh; 500 steps per simulated second,
   more when the stout moves fast (the ride took 4,881 steps for 8 s).
3. **Quota seconds = run seconds × 2** (both T4 cards are charged). Quote this number and its share of 108,000 s.
4. `sessionTimeoutSeconds` = run seconds × 1.3, no more. `BUDGET_S` in the cell = the timeout less 120 s.
   `cancel_notebook_session` is denied in this workspace: a wrong run burns until its timeout.
5. One sentence per task: what it computes and why the page needs it.
6. Ask once. After the run, read the quota again and report the difference.

## Gate E. The result (after the run, before any number or picture is shown as a result)

From `summary.json` and the .npz files, for the task named:
- `rest`: largest deviation of the surface inside the glass under 0.3 mm; head spilled 0.00 mL; stout spilled 0.0 g.
- every task: `nselmax` < `K`; `drops_max` < the drop list; `volume_kept` consistent with `spilled_g`; `resmax` small;
  no "WARNING" or "STOP" line in the log.
- rides: impulse on the cart equals minus the stout's momentum to rounding.
- free swing: frequency within 3 % of 3.42 Hz; damping stated against Gate C's prediction.
- energy: the wall, skin and head books (`ewall`, `eskin`, `efoam`) are all positive and the head's is the largest when a head is on.
Then pack, open the frames in Chromium, and **look** at them: at rest (flat, no peaks), mid-ride, at the spill, at the end;
at 360, 390, 1024 and 1440 px. Only then show the user.

## Gate F. The page (before merging to `main`)

- `find public -size +24M` prints nothing. Nothing from a run that failed Gate E is under `public/`.
- `python3 tools/inventory.py --check`, `python3 tools/i18n/build.py --check`, `npm run build` pass; `package-lock.json` deleted.
- Real browser at the four widths: no console errors (one known message about `static.cloudflareinsights.com/beacon.min.js`),
  no sideways scroll, the ride plays at its real speed, no control offers a ride that is not stored.
- The docs pages that describe changed files say what the code now does.
- Screenshots shown to the user before the publish; the live page opened and looked at after it.

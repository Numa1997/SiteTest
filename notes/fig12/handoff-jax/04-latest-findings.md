# Fig. 12 in JAX: findings of the last hour of the previous session (13 November 2026, evening)

Read after `00-PROMPT.md`, `01-mistakes-and-rules.md`, `02-launch-gates.md`, `03-model-and-numbers.md`. This file overrides them where it differs.

## 1. The user's orders of this hour (their words)

- "you cannot be executing shit without telling me." Say in one line what runs, where, how long, what it costs, before every run.
- "I don't want any goddamn further testings. What I want is proper and honest work."
- "if you actually are confident with whatever error you think you might have caught and that a new GPU run would be their actual
  solution, then go ahead ... make the new code already and show me something viable."
- "It will never run a GPU unless it is extremely, extremely confident about running the GPU and about the solution itself."
- "It might be actually correct that it just spills so much when the road is that bumpy and when it's that fast." Do not tune
  spillage away. Real spill on hard roads is wanted.
- No recaps, no "checkpoint", no "health" lines, no handoff talk in chat. Answer the question asked, briefly, and work.
- The user offered: "Maybe you can guide us both and develop me". Explain the physics as you go, plainly, so the user understands
  the model as well as you do.

## 2. Gate B (the pint at rest) was executed, and fails on the surface read-out only

Run on the session's CPU: `GLASS_JSON=<glass.json> python3 tools/fig12/kaggle/gate_rest.py` (4 mm grid, 1 s at rest, 6 min 20 s).
- PASS: columns inside hold a value; none outside; head 19 mm; no stout left; stout still (kinetic energy under 1e-5 J); list did not
  overflow; no NaN.
- FAIL: surface within 0.2 cells of the fill (largest deviation 2.748 mm at 4 mm cells).
- FAIL: head lost nothing at rest (91.20 mL before, 91.11 mL after, 0.089 mL "spilled").

A diagnostic (4 mm grid; deviation of the read surface from the fill, in cells, by radius):
- t = 0, particles just seeded, nothing has moved: +0.31 cells in every band from the axis to the wall (min +0.23, max +0.39).
- t = 0.10 s: axis to 0.8 R about +0.30; 0.9-0.95 R +0.65 (max +0.875); 0.95-1.0 R +0.46 (max +0.98).

Inference (not yet proven by a passing run):
1. The uniform +0.3 cell comes from the level set of Zhu & Bridson as coded in `Stout.level_set`: phi = |x - x_avg| - r with
   r = `self.rls` = 0.9 dx, particles 2 per cell per axis. The zero of phi stands about 0.3 dx above the stout's true top.
   This also places the pressure solve's free surface too high, by about 0.45 mm on the 1.5 mm grid.
2. The extra rise at the wall comes from the mirror particles behind the glass (`img` in `level_set`).
3. The false height at the wall lifts the head's top (fill 125 mm + head 19 mm = 144 mm) past the rim (147.5 mm, glass.json) on the
   4 mm grid, and `head_spill` cuts it. So the spill at rest is a read-out fault, not physics.

Proposed fix, not coded: read each column's surface height from the stout it holds (the particles in the column, times their volume,
over the column's open area, layer by layer through the glass's profile), with the level set kept only for the pressure solve, or
recalibrate r so a flat seeded layer reads its true height. Decide, write the size of the error against the 0.2-cell gate, then code.

Commit `a606c9c` holds a half step (read-out from the level set before the solver's clamp); it did not change the result.

## 3. The user's data and what the solver does with it

In `tools/fig12/kaggle/stout_jax.py` now: stout 1007 kg/m^3, 2.06 mPa s; head: surface tension 44.2 mN/m, dilatational modulus
18.7 mN/m (Volp & Willenbacher 2021, read), Sauter radius 34 um, liquid fraction 0.27, thickness 19 mm.

Not in it, from the user's uploaded Gemini dataset (`notes/fig12/research/sources/gemini-dataset-2026-11-13.txt`):
- gas fraction of the head 0.80 (liquid fraction 0.20); the solver uses 0.27 (derived by the research session, range 0.24-0.36).
  It sets the head's density (rho_f = phi_l rho) and yield stress. Decide with the arithmetic, say which and why.
- glass 160 x 85 mm; the solver's glass (glass.json, from earlier sessions) is 147.5 mm tall, 78.6 mm across at its widest (z = 116 mm).
  Check which glass the page and the earlier figures used before changing anything; the user does not want the glass to become the topic.
- contact angle (23.2 deg in the dataset, 28.5 deg advancing on clean glass from Hamlett 2015): no contact line in the model.
- NIBEM 260 s: no drainage in a ride of 20 s.

## 4. What remains (in this order)

1. Fix the surface read-out (section 2). Get Gate B to PASS on the CPU, saying so in one line before running it.
2. Settle the liquid fraction (section 3) with arithmetic.
3. Gates A, C, D of `02-launch-gates.md`; re-pin `tools/fig12/kaggle/nb/run_b_cell.py`; make list overflow stop a task (now only a
   WARNING in `run_b.py`).
4. One GPU budget in quota seconds (run seconds x 2), the quota read fresh, one yes. Then Gate E, frames at 360/390/1024/1440 px,
   screenshots to the user, then the page, docs, merge (Gate F), the controller.

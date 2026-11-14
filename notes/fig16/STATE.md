# Fig. 16: a pint of Guinness on a cart built to carry it — this chat's state

Reread this file first after any compaction. Keep it current at every step that changes what is live or what is left.
Brief: `notes/fig16/BRIEF.md` (from the coordinating chat, session_01DGmqintkoYzahfGQQzdXYL). Branch: `claude/fig16-cart`.

## Aim
A new figure and page, Fig. 16: the same pint (stout + head) as Fig. 12 on a cart designed to carry it, with a control system to
match, over the same roads, kerb included, with the least sloshing physics allows. Fig. 12 stays as it is (the "before").

## Steps (status)
1. Read the brief and every file in its section 1 — in progress.
2. Build a low-order slosh model from the stored Fig. 12 rides on the CPU; validate it against run 10's controlled rides
   without fitting to them. Report the validation to the coordinator (≤ 12 lines).
3. Design 2–3 cart concepts on that model (masses, motor, wheel, gimbal; tilt, spill, peak force, current vs limit; weak point).
   **STOP: report the concepts to the coordinator and the owner; the owner picks one.**
4. Control system (control skill), new cart module in the JAX solver (fluid untouched), GPU bill + owner's yes per launch.
5. Page, picture, note, readers, registration, merge, live check.

## Rules (binding)
- Not a single atom of data that is not needed; use stored data to make corrected data. Final rides computed fresh on GPU.
- Every GPU launch: bill (runs × s/step × steps, GPU-h, share of weekly 30 h after get_accelerator_quota), progress line,
  and the owner's explicit yes in this chat. This week's quota is mostly Fig. 15's; resets 21 November 00:00 UTC.
- Compare designs by tilt and spill, never by the two-point lean; give scatter bands (kerb: lean ±2.7 mm, tilt ±0.3 mm,
  spill ±0.05 mL).
- Never touch: Fig. 12's files and data, Fig. 15's files, the Workers, R2, public/de/, public/ar/, scripts/i18n/, *.rtl.css.
- Owner: BSc physics; metric units; define every term; mark Fact (with handle) / Inference / Opinion; mechanism in one line;
  one decision at a time with 2–3 options, a pick and the case against.
- Report to the coordinator at: slosh-model validation; concepts (STOP); each GPU bill; live. At most 12 lines each.
- Never write the owner's name. No model names in code, commits or PRs.

## Files
- `notes/fig16/BRIEF.md` (the brief), `notes/fig16/STATE.md` (this file).

## Commits
- (this commit) brief + state.

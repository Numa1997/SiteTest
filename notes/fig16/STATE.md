# Fig. 16: a pint of Guinness on a cart built to carry it — this chat's state

Reread this file first after any compaction. Keep it current at every step that changes what is live or what is left.
Brief: `notes/fig16/BRIEF.md` (from the coordinating chat, session_01DGmqintkoYzahfGQQzdXYL). Branch: `claude/fig16-cart`.

## Aim
A new figure and page, Fig. 16: the same pint (stout + head) as Fig. 12 on a cart designed to carry it, with a control system to
match, over the same roads, kerb included, with the least sloshing physics allows. Fig. 12 stays as it is (the "before").

## The owner's emphasis (this chat, 14 November 2026)
"Your main objective here is control. Control, control, control ... control over the foam and over the fluid and over the
Guinness. We will also specifically target those roads that were extremely bumpy and we were losing not beer but foam."
So: the figure of merit is the head of foam spilled on the kerb (Fig. 12: 1.63-2.51 mL by controller, no stout), then the tilt.
The control system is the centre of the work; the cart is designed to give it the authority it needs.

## The owner's decision on the machine (this chat, 14 November 2026, after seeing the 2D concept sketch)
- The glass is GLUED to the cart's deck. No hanging holder, no gimbal. (Concepts A and B as drawn are dropped.)
- The cart is a realistic engineering system shown in 3D: real suspension linkage (wheel on a swing arm hinged to the chassis,
  coil-over strut), real parts. The deck heaves and pitches as each wheel meets the bump; that tilts the glued glass; the control
  system must master that.
- So: the model must become a two-axle cart with pitch (half-car), the glass rigid on the deck; actuators: hub motors (rear),
  a voice-coil actuator in each strut (heave and pitch of the deck); sensors: IMU on the deck, load cells, encoders, road scanner.
- 3D prototype: `notes/fig16/proto/cart3d.html` (three.js from public/vendor/three), screenshots cart3d-iso/side/explode.png.
  Screenshot script (no server; a background server is refused by the owner's rules): scratch shot.cjs, Playwright page.route.

## Steps (status)
1. Read the brief and section 1's files — done for the modelling stage (CLAUDE.md, AGENTS.md, STANDARD.md, kaggle-pipeline.md,
   the solver, run_b.py, pack_ride.py, 06/07 notes, REPORT.md, the note's sections 4, 6.5, 7, 12.3, the control skill).
   Still to read whole before page work: docs/styles.md, the page HTML, guinness-jax-play.js, the readers' files.
2. [DONE, see model.md section 3] Build a low-order slosh model from the stored Fig. 12 rides on the CPU; validate it against run 10's controlled rides
   without fitting to them. Report the validation to the coordinator (≤ 12 lines).
3. [DONE, notes/fig16/concepts.md; WAITING FOR THE OWNER'S PICK] Design 2–3 cart concepts on that model (masses, motor, wheel, gimbal; tilt, spill, peak force, current vs limit; weak point).
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
- `notes/fig16/BRIEF.md` (the brief), `notes/fig16/STATE.md` (this file), `notes/fig16/model.md` (the model's derivation).
- `tools/fig16/rides.py` (decodes stored rides; tilt equals stored tilt_max_mm to 0.01 mm), `slosh_model.py` (N cos-theta modes +
  Fig. 12's Cart imported unchanged; gains equal run 10's), `fit.py` (friction fit on run 8 training rides only -> fit.json),
  `validate.py` (model vs stored rides), `spill.py` (head spill by the solver's rule), `gamma_check.py` (stout push 75.7 g measured).
- JAX (CPU) and matplotlib installed in this container with pip.

## Model findings so far
- One mode + linear damping: gentle controlled rides of run 10 predicted to 0.07-0.08 mm rms tilt, 0.005 A current (not fitted).
  Big swings too small (kerb 18-19 vs 21-25 mm): add modes 2-3 (16 % of a tilt) and the head's Ca^(2/3) friction (fit running).
- Stout push F_x vs -q'': 79.7 / 71.7 g on the gentle training rides (corr 0.96) vs 55.8 g cylinder theory; using 75.7 g.

- VALIDATED (validation.json): run 10's five controlled rides, never fitted: head spilled 2.07/2.14, 1.63/1.58, 2.51/2.46 mL
  (stored/model); tilt rms error 0.07-0.08 mm gentle, 0.7-1.1 mm kerb; fitted friction power n = 0.6665 (Cantat: 2/3).
- Design tools: `tools/fig16/cart16.py` (design simulator: quarter car + gimballed pendulum + slosh modes in the glass's frame;
  reproduces the validated model for Fig. 12's cart to 0.011 mm), `holder.py` (pendulum mass properties from the glass profile),
  `sweep.py` (384 kerb variants -> sweep.json), `concepts.py` (3 concepts x 3 roads + robustness -> concepts.json).
- CONCEPTS (kerb tilt / head spilled): A tray (passive pendulum) 3.83 mm / 0; B gimbal (torque motor + 24 V + load-cell preview)
  0.55 mm / 0; C muscle (no gimbal) 5.22 mm / 0 but 50 mm / 5.25 mL without preview. Fig. 12 cart: 26.2 mm / 2.46 mL.
- OPEN for the GPU stage: a tilting glass needs the rotating frame's forces beside the fluid step (brief: do not change the fluid
  part) -> ask before any launch. The tilt physics (mechanical analogue) is not validated by stored data.

## Commits
- 1st: brief + state. 2nd: model tools in progress.

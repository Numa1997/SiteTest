# Fig. 16 of Phyein Usul: a pint of Guinness on a cart built to carry it

Brief written 14 November 2026 by the coordinating chat (session_01DGmqintkoYzahfGQQzdXYL) for the session the owner deploys.
Never write the owner's name.

## 0. The task in one paragraph

Fig. 12 put a real pint of Guinness (stout plus its head of foam, about a million particles, JAX solver on Kaggle's T4 GPUs) on a
simple one-wheel cart with five controllers. On gentle roads, joint control cuts the surface's swing from about 13 mm to about 1 mm.
On the kerb, every controller fails: the kerb pushes the cart back with up to 82 N within about 40 ms, and at 1.5 m/s the motor can
give only 11.25 N. Fig. 16 is a new figure and a new page. It designs a much more capable cart, and a control system to match, that
carries the same pint over the same roads, kerb included, with the least sloshing physics allows. It shows that cart as a detailed,
beautiful machine whose parts visibly work. Fig. 12 stays as it is: it is the "before".

## 1. Read first, whole, before any work

- **Method and layout:** `CLAUDE.md` (method, owner's rules) and `AGENTS.md` (layout, boundaries).
- **House design:** `docs/styles.md`, and `notes/STANDARD.md` for lecture notes.
- **The pipeline:** `docs/kaggle-pipeline.md` (how runs are computed on Kaggle and stored, by generation date). The page only plays
  stored data.
- **Fig. 12 in full:**
  - the page `public/simulations/guinness-kaggle.html` and the player `public/scripts/guinness-jax-play.js`;
  - the note `notes/fig12/note/paper.html`, which is live, with its report `notes/fig12/note/REPORT.md`;
  - the solver `tools/fig12/kaggle/stout_jax.py` (`Geometry`, `road_table`, `Cart`, `slosh_lqr`, `susp_lqr`, `observer_design`) and
    the runner `run_b.py`;
  - the readers' checks `notes/fig12/readers/`;
  - the state `notes/fig12/handoff-jax/06-run8-state.md` and the diagnosis `notes/fig12/handoff-jax/07-diagnosis.md`;
  - the stored rides `public/data/fig12/2026-11-14-run10/` and `public/data/fig12/2026-11-13-run8/`.
- **The control skill:** `phyein-usul-first-principles-control` (load it with the Skill tool).

## 2. What you may trust in the fluid solver, and its limits

These are facts from the Fig. 12 checks; reproduce any you lean on.

- **Trusted:**
  - the particle books close: no stout particle lost of 1,001,952, the head off by at most 1.3e-8 mL;
  - independent code reproduced the rides, the tables, the cart forces and the controller gains;
  - the head's damping is computed at ζ = 0.425, against 0.47 predicted from the foam's friction on the glass.
- **Limits, to be stated in your note:**
  - **The method's own damping.** The bare stout is fitted at ζ = 0.016, against about 0.0055 from the physics. With the head this is
    about 2.5 % of the damping. The final cause is in `07-diagnosis.md` item 1; read it.
  - **Bulking.** After violent jolts the stout's mean surface rises 0.85–1.44 mm with no particle lost (the particle cloud spreads by
    about 1 %). It comes after the spills and does not change them.
  - **Run-to-run scatter on the kerb.** The GPU sums in unordered fashion, so two runs of the same kerb ride part at the splash: about
    ±2.7 mm on the two-point lean, ±0.3 mm on the tilt, ±0.05 mL on the spill. Compare designs by tilt and spill, never by a two-point
    lean, and give scatter bands.

## 3. The owner's standing order on data (binding)

"Absolutely not generate a single atom of data if it's not needed. If you can use other data to generate corrected data, then use it."

The fluid and the cart push on each other, so a new cart's rides cannot be replayed from the old ones. Every final ride must be
computed fresh. The stored rides still do most of the work:

1. **Build a slosh model from the stored data, on the CPU.** The stored rides contain the pint's measured behaviour: the first mode's
   frequency and damping with and without the head, the share of the liquid that sloshes, the coupling β = 1.241 with the head, and
   how the response grows with amplitude.
   - Identify a low-order model from those stored files: the first mode, plus the second if it is needed. The stored plant in run 8's
     `free_full_1.5`, ring 13, is a starting point.
   - Validate it: it must predict the stored controlled rides of run 10 (tilt history, cart speed, motor current) within stated
     bands, without being fitted to them.
2. **Design the cart and the controller on that model, on the CPU.** Test hundreds of variants in minutes.
3. **Prove only the two or three best designs** in the full JAX fluid solver on the GPU.
   - Add the new cart's dynamics to the solver as a new module. Do not change the fluid part.
   - Before any launch: a bill (runs × measured seconds per step × steps, as GPU-hours and as a share of the weekly 30 h, after
     `get_accelerator_quota`), a progress line readable while it runs, and the owner's explicit yes in your chat.
   - Note: this week's GPU quota is mostly reserved for the Fig. 15 correction. It resets 21 November 00:00 UTC.

## 4. The physics to design from (derive each in the note; don't assert)

- **Why liquid sloshes.** In the glass's own frame the liquid feels the effective gravity g_eff = g − a, where a is the glass's
  acceleration. At rest, the free surface lies at right angles to g_eff. Sloshing is the surface swinging about that direction
  whenever a changes faster than the first mode can follow.
  - The first mode: ω₁² = (g ξ₁ / R) tanh(ξ₁ h / R), with ξ₁ = 1.8412 the first zero of J₁′. About 3.3 Hz bare, 2.9 Hz with the head.
- **Four levers, each with its physical limit:**
  1. **Shape the acceleration.** Take every change of speed smoothly, or as a two-step input shaped to cancel the first mode. Limited
     by the motor's force-speed curve: back-EMF eats the supply.
  2. **Tilt the glass to follow g_eff.** If the glass always tilts so its axis lies along g_eff, the liquid feels no sideways push and
     barely sloshes. A free-swinging gimbal does this passively, like a waiter's tray on a pendulum. An actuated gimbal does it
     actively and faster, with damping. This is probably the strongest lever; quantify it.
  3. **Isolate the jolt.** Suspension travel, a compliant tyre, or a larger wheel spread the kerb's impulse over a longer time, so the
     peak force falls. Work out the impulse J = ∫F dt and the time-scale needed for the motor and the gimbal to keep up.
  4. **More authority.** A stronger motor, gearing, a higher supply voltage, a second driven wheel, or slowing down before the kerb
     (the road preview already knows it is coming).
- **The design space.** Present 2–3 complete cart concepts. For example, an actively gimballed holder on a suspended chassis, or a
  two-wheel cart with a passive pendulum holder and preview braking, or your own better idea. For each give:
  - the masses, the motor, the wheel and the gimbal;
  - what it achieves on every road from the slosh model: tilt, spill, peak force and motor current against its limit;
  - its weak point.

  **STOP here and report the concepts to the coordinator.** The owner picks one before any GPU run.
- **The control.** The control skill above, from first principles: state estimation from realistic sensors (an IMU on the holder,
  wheel encoders, motor current), LQR or a better law with a reason, preview of the road, actuator limits handled honestly, and
  robustness to the head's uncertain mass. Show why each piece is there.

## 5. The page and the picture (Fig. 16)

- **A new page** in the house design (`docs/styles.md`): titles in Instrument Serif at weight 400, text in IBM Plex Sans, labels in
  IBM Plex Mono, the house colours. Reuse Fig. 12's glass drawing and stout rendering (`guinness-glass.js`, `stout-view*.js`) by
  import, without editing them.
- **The cart: a detailed, good-looking machine whose parts visibly work,** every part driven by stored data:
  - chassis and wheel(s);
  - the motor and gearbox, with the current shown;
  - suspension springs and dampers that compress;
  - the gimbal holder tilting;
  - sensors and the controller box, with a readable signal flow.
  - A cutaway or exploded view that names each part.
- **Smoothness:** playback is smooth and measured at 390 and 1440 px.
- **Pointer reading** follows CLAUDE.md's data-cursor rule.
- **The three-way proof:** the stored value, the formula recomputed from stored inputs, and the pixel read back.
- **Side by side:** the same road with Fig. 12's best controller and with the new cart.
- **Register the figure:** catalog, figure navigation, inventory (`tools/inventory.py`), docs (`docs/simulations/fig16-…md`) and the
  i18n checks, as the other figures do.

## 6. The lecture note

The owner's standard: honest, rigorous, mathematical; derive, never assert; an everyday picture first and back to it after; readable
start to finish without one stop. Numbered equations and figures, set in Latin Modern and KaTeX.

- **Every number** is printed by one script from the stored data.
- **Readers:** run the repository's own agents, `referee`, an owner-level reader and a first-year reader. Each gets only the figure
  number and the page path. Repeat with fresh readers until a reading has no stops, then run `derivation-checker`. The owner caps
  rounds: stop after two full rounds unless a round finds a wrong equation or number.

## 7. How you work

- **First:** write `notes/fig16/STATE.md` (aim, steps, files, commits, these rules), commit and push it. Keep it current. After any
  compaction, reread it first.
- **Branches:** work on your own branch, `claude/fig16-cart`. When finished, checked against the other sessions' work on `main` and
  tested in a real browser, merge and verify live, as CLAUDE.md says.
- **Never touch:** Fig. 12's files and data, Fig. 15's files, the Workers, R2, `public/de/`, `public/ar/`, `scripts/i18n/` or
  `*.rtl.css` by hand.
- **The owner:** BSc in physics (computational and theoretical).
  - Metric units; define every term at first use.
  - Mark Fact (with a handle), Inference and Opinion.
  - The mechanism of each result in one line.
  - One decision at a time, with 2–3 options, a pick and the case against it.
- **Report** to the coordinator (session_01DGmqintkoYzahfGQQzdXYL, send_message) at:
  - the slosh model's validation;
  - the concepts (STOP);
  - each GPU bill;
  - live.

  At most 12 lines each.

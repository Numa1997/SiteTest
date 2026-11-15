# Guinness rebuild (Fig. 12 and Fig. 16): this chat's state

Reread first after any compaction. Prompt: `notes/fig16/PROMPT-computational-physicist.md`. Branch: `claude/compassionate-pascal-kk3d8g`
(from main a1afdbd). Report only to the owner, in this chat.

## The owner's rules for this chat (14 November 2026)
- "No need to ask for permissions ... they are granted." Just work; compute on Kaggle; do not ask before GPU runs (still report the bill).
- Physics and modelling first; then compute on Kaggle; then the animation. Reuse the stored data ("I sure as fuck hope all this data
  doesn't go for nothing"). Online sources welcome; explain the physics at graduate level.
- Metric units, define terms, Fact/Inference/Opinion, mechanism in one line, short turns, no walls of text.

## Findings so far
- Fig. 12 already stores control off ("speed held only", run 8) and on ("joint", run 10) for all three roads: its switch needs no compute.
- Fig. 16's left-out rotating-frame forces are NOT small on the kerb (from stored pitch, 30 fps, so lower bounds):
  kerb_off |theta''| 70.6 rad/s^2 -> theta'' r = 7.1 m/s^2 at r = 0.1 m; |theta'| 5.6 rad/s -> Coriolis 2 om u ~ 5 m/s^2 at 0.5 m/s.
  kerb_full: 15.6 rad/s^2 -> 1.6 m/s^2. Gentle roads with control: <= 0.6 rad/s^2 -> 0.06 m/s^2 (0.6 % of g): kept, not recomputed.
- Wheel: wagon-wheel aliasing predicted (5 spokes, 30 fps, R 40/45 mm): to prove with a screenshot strip (animation stage).

## Done
- `tools/fig12/kaggle/stout_jax.py`: optional `rot=(om, al, zS)` in Stout.step: Euler + centrifugal at every face, Coriolis as an
  exact rotation of each cell's velocity; drops and lumps in flight feel the same field; the head's weight and rim failure use the
  local field. rot=None is bit-identical to before (checked on CPU, 5 steps, 6 mm: max |diff| = 0).
- `tools/fig16/kaggle/run16.py` (run 3): rot on; stout push F = -(dP/dt + om x P); M_drops 131072 (16,384 stored per picture);
  60 pictures a second; tasks rest, design, kerb_off, kerb_full, resonant_off, bump25_off, kerb_full_seed2, kerb_off_seed2.
  `cart4.py`: FLOOR_ABOVE_DECK = 0.030 (z_S = 0.092 m in the solver). CPU code check (6 mm, 2 pictures): runs.

## Next
1. RUN 3 LAUNCHED 15 Nov 00:01 UTC as notebook version 3 (refused 23:10-23:29: two GPU sessions busy) (notebook numakoudsie/fig-16-guinness-cart-with-control, version 3). Bill: about 0.8 GPU h expected,
   1.4 h at most (budget 3600 s, timeout 5400 s); quota 76,012 s used of 108,000 s on 14 Nov 23:00 UTC.
2. Audit `notes/guinness-rebuild/audit.md`: rot-frame effect = run 3 kerb_full vs run 2 kerb_full, against the seed scatter.
3. Pack, then the animation: wheels, 3D fluid, the on/off switch for both figures.

## Status 15 Nov 2026, 03:50 UTC
- Physics done:
  - the rotating frame's forces (run 3);
  - control off on every road;
  - the drop list;
  - the scatter of seeds;
  - the swelling fix: gated volume correction, run 4b, uncontrolled rides within 1.5 %.
- Page data: public/data/fig16/2026-11-15/ holds kerb_full (+ seed 2, v4) and kerb_off, resonant_off, bump25_off (v7).
- Pages:
  - the control switch on Fig. 12 and Fig. 16;
  - wheels fixed;
  - the 3D close-up (pint3d-view.js) on both.
  - NOT merged to main yet.
- Open:
  - lecture notes and docs numbers (the Fig. 16 note still says tilt 2.6 mm, an under-read; run 3 gives 4.0 mm at 60/s);
  - the data panel and three-way proof for the new view;
  - one geometry for the drawn and simulated cart;
  - the 1 mm grid check of numerical damping;
  - merge and publish.
- Quota: about 76,000 + 6,700 s used by this chat today (runs 3, 3b, 4, 4b); weekly limit 108,000 s.

## Status 15 Nov 2026, after "close all open issues" (owner: "you're on your own")
- Closed:
  1. note numbers (runs 3 and 4b, corrections stated);
  2. close-up at 390 px;
  3. page weight (drops 2,048 per picture);
  4. one geometry (Cart16View.fromCart; stored pose as stored);
  5. three-way check of the close-up (tools/fig16/check_pint3d.cjs, 65/65);
  6. resonance (modes16, coupled pitch-slosh mode 3.85 Hz, zeta 0.33; road 3.45 Hz; audit I);
  7. volume correction's energy (audit J);
  9. stout's push (bounded, audit K).
- Published: main fast-forwarded to b113106; live on phyeinusul.com, checked in Chromium (both pages play, no errors but the site-wide
  Cloudflare beacon blocked by the site's CSP, which predates this work).
- Running: item 8, numerical damping at 1.5 and 1.0 mm (Fig. 12 notebook version 12; version 11 never started).
- Still open, known: smoothness of the 3D close-up on a real GPU (not measurable here); the lecture notes are corrected, not
  rewritten to STANDARD.md with a referee.

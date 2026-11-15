# Fig. 16 lecture note: plan of the chapter, and the numbers it measures

Working file of the note-writing session (15 November 2026, branch `claude/compassionate-pascal-kk3d8g`). Reread first after any
compaction. Rule set: `notes/STANDARD.md`, verdict of 21 October 2026 (Taylor-style chapter: every step, every symbol defined where
it first appears, "Key result" boxes, numbered worked examples with the page's numbers, Problems at the end, ★ on skippable heavy
parts with their results restated). Only the note changes, between `<article class="paper" id="paper">` and `</article>` of
`notes/fig16/page/guinness-cart-control.src.html`; every number is a `{{key}}` filled by `tools/fig16/build_page.py` from stored data
(never typed by hand). No walkthrough exists for this page.

## State (keep current)
- [x] read: STANDARD.md, CLAUDE.md, AGENTS.md, the page source, build_page.py, STATE.md, model.md, audit.md A-K, cart4.py,
  run16.py, pack16.py, stout_jax.py (frame_accel, body_force, volume_source, head_spill, step), modes16.json, both index-16.json,
  the Fig. 2 note (reference), Fig. 12's note sections 3-4 (for the driven-swing equation it derives).
- [ ] measure: `notes/fig16/note_numbers.py` -> `notes/fig16/note-numbers.json` (every derived number of the note)
- [ ] build_page.py reads note-numbers.json; new keys
- [ ] write the note; build; `--check`; `npm run build`; Chromium (KaTeX errors, screenshots, page table vs note table)
- [ ] docs/simulations/fig16-guinness-cart-control.md; commit; push this branch only

## Chapter plan (sections, what each derives, the worked examples)

1. **Carrying a pint over a kerb** (motivation). The hand that slows before a kerb and lets the wrist give. Fig. 12's one-wheel cart
   on the kerb: what it lost (stored, Fig. 12 index). The two things the new cart adds: it sees the road, and it can tilt and lift the
   glass. Plan of the chapter.
2. **The machine** (model). Deck, axles, swing arms, strut = spring + damper + voice coil, bump stops, tyres, hub motors, sensors.
   Every symbol with its value (CART4). Assumptions: planar (no roll, no yaw), rigid deck, glass clamped, pint as a rigid load plus
   its moving part. Statics: loads per axle, total masses \(M_s, M_x\), pitch inertia \(J\).
   Example 2.1: the deck's bounce frequency and damping ratio from \(k, c, M_s\) (one-body estimate), compared with the
   full model's heave mode (modes16.json).
3. **What the stout feels on a tilting deck.** 3.1 effective gravity in a translating frame (restated from Fig. 12, eq. 1 there);
   3.2 the acceleration of the point S on a pitching deck (\(\mathbf a_S\) with \(h_g\ddot\theta\), \(h_g\dot\theta^2\)), derived;
   3.3 resolving \(\mathbf g_\text{eff}\) on the tilted axes; the condition \(g_x = 0\) (the waiter's lean); 3.4 linearised form,
   which is what the controller uses: \(a_\text{eff} \approx a_x + g\theta - h_g\ddot\theta\).
   3.5 the driven swing of Fig. 12 (restated key result) with the head: \(f_0, \zeta, \beta\) measured in run 8.
   3.6 ★ the rotating frame's forces (Euler, centrifugal, Coriolis), derived from the rotating-frame Newton law; their size from
   the stored pitch rate and acceleration. Example 3.1: the lean needed for the kerb's deceleration. Example 3.2: freeboard,
   how much tilt of the deck alone lifts the head to the rim (R from the glass profile at the fill height).
4. **Equations of motion of the cart.** Newton for x, z_c, the axles; Euler for the pitch; the strut forces; the tyres. Linearised:
   \(\dot{\mathbf x} = A\mathbf x + B\mathbf u + E\mathbf w\), the 12 states, 3 inputs, 4 road inputs. ★ the pitch equation in detail.
   4.2 natural modes with the control off (modes16.json): stout swing, heave, pitch-with-stout, axle hops. 4.3 the wheelbase filter
   \(|2\sin(\pi f\ell/v)|\), derived. Example 4.1: the five bumps at 1.0 m/s against the pitch-slosh mode (frequency ratio, band).
5. **The control system.** 5.1 cost and Bryson's rule; 5.2 ★ LQR from the discrete Riccati equation (dynamic programming sketch,
   every step); 5.3 ★ preview: the optimal feed-forward of a known road, \(K_j\) derived; how fast \(K_j\) fades (measured);
   5.4 the Kalman filter on the swing (predict with the IMU, correct with the probes), the gain (measured); 5.5 the hardware's
   clipping (current, voltage, actuator limits); 5.6 the design step (five weightings tried on the few-mode stout; which won).
   Example 5.1: the slowest closed-loop pole as a time constant. Example 5.2: the motors' force limit at 1.5 m/s (back-EMF).
6. **How the rides were computed.** The fluid solver (Fig. 12's, unchanged) and its step; the cart sub-stepped at 0.1 ms; the push
   back; runs 2, 3, 4b (versions 2, 4, 7), 60 pictures a second; rest guard; books; the volume correction (what, why, how it was
   proved harmless: audit H, J); cost (ms a step, GPU minutes, measured from the indexes).
7. **What the rides show.** Table 1 (Fig. 12 best vs Fig. 16 on), Table 2 (control off); seed scatter; sampling (60/s vs every
   second picture, measured on the stored tilt); why control off fails (deck tilt vs freeboard; near resonance). Example 7.1.
8. **What is on the screen.** Which drawn thing is which stored symbol; where the drawing differs (wheel angle kinematic, 3D lighting,
   drop subsample, Fig. 12's tilt read in the browser).
9. **Limits, and the next model.** Planar, ideal sensors except the swing, design model's push mass (audit K), numerical damping
   (audit F), saturation on the kerb. Problems. Further reading (only sources opened in this session).

## Numbers to measure, and how

| number | how |
|---|---|
| masses, inertia, static loads, strokes | `cart4.statics(CART4, ml)` with ml from modes16.json (`ml_kg`) |
| one-body bounce f and zeta | \(\sqrt{2k/M_s}/2\pi\), \(2c/(2\sqrt{2kM_s})\) from CART4 |
| pitch frequency of the bare deck | \(\sqrt{k(a_f^2+a_r^2)/J}/2\pi\) |
| natural modes, control off | modes16.json (eigenvalues of cart4.linear_model, Kaggle CPU v3) |
| K, closed-loop poles, slowest time constant | `cart4.design(CART4, ml, v0, {'q': 0.00025})` run here (numpy/scipy, JAX CPU) |
| preview gains' decay | norm of \(K_j\) at j = 0, 50, 100, 250 from the same design |
| Kalman gain | `design(...)['Lk']` |
| motor force limit at 1.5 m/s | \(n_m b \min(I_\max, (V_\max - b v)/R_a)\) |
| kerb deceleration | stored v of Fig. 16 rides (60/s) finite differences, and the lean it would need |
| rotating-frame forces | stored `om`, `al` of run-3 rides: max \(|\ddot\theta| r\), \(\dot\theta^2 r\), \(2\dot\theta u\) |
| tilt at 60/s vs every second picture | stored `tilt_mm` of the kerb rides |
| Fig. 12 numbers | Fig. 12 index (run 10) |
| fill radius R at the fill height | glass profile JSON used by the solver (GLASS_JSON), at z = 125 mm |
| wheelbase filter | \(|2\sin(\pi f\ell/v)|\) |
| GPU time | sum of run_s in the indexes |

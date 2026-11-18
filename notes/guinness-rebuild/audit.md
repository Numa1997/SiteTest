# Audit of the Guinness simulations (Fig. 12 and Fig. 16), 14 November 2026

Every entry: what is wrong or left out, its size (measured, with how), and what is done about it.

## A. The wheels turn backwards (both figures): aliasing, not a sign error

**Fact (derivation; `public/scripts/stout-view.js:144`, `cart16-view.js:70`, `guinness16-play.js:97`).** A spoke drawn at angle
a = -x/R_w sits at (R_w cos a, R_w sin a) in the wheel's (x, z) plane. Its velocity relative to the axle is R_w a' (-sin a, cos a); at
the top (a = pi/2) that is (+v, 0) and at the contact point (a = -pi/2) it is (-v, 0), so the contact point is at rest on the road. That
is rolling without slip in the right sense, in 3D, whichever side the camera stands on. The sign in the code is right.

**Fact (measured from every stored ride; the script is in this file's commit message).** The page shows 30 stored pictures a
second. Five spokes repeat every 72 degrees, so the eye takes the smallest turn that maps the pattern onto itself, folded into
(-36, +36] degrees:

| ride | true turn per picture | what the eye sees | pictures that look backwards |
|---|---|---|---|
| Fig. 12, 1.0 m/s, R_w 40 mm | -47.7 deg | +24.3 deg (backwards, 2 turns a second) | 100 % |
| Fig. 12, kerb, 1.5 m/s | -71.6 deg | +0.4 deg (frozen, creeping backwards) | 82-97 % |
| Fig. 16, 1.0 m/s, R_w 45 mm | -42.4 deg | +29.6 deg (backwards, 2.5 turns a second) | 100 % |
| Fig. 16, kerb, 1.5 m/s | -63.5 deg | +8.5 deg (backwards, slowly) | 100 % |

Strip: `img/wheel_strip16.png` (pictures 16-21 of Fig. 16's kerb ride: true -62 to -64 degrees per picture, seen as +8 to +10).

**Mechanism:** this is the sampling theorem. The spoke pattern has 5 cycles per turn, so it is sampled below its Nyquist rate as
soon as the wheel turns more than 36 degrees between pictures.

**Fix (animation stage):**
- The wheel's angle is kinematics, x/R_w, not stored physics. Draw it at the screen's rate from the stored position, and say so
  on the page.
- Add an asymmetric mark (a valve) so that one turn is the true period.
- Blur the spokes by the angle turned during one screen frame, as a real eye sees a wheel at 4-6 turns a second.
- The new rides store 60 pictures a second (run 3).

## B. Fig. 16: the turning glass's forces were left out, and they are not small on the kerb

**Fact (`tools/fig16/kaggle/cart4.py` header, run 2).** The fluid felt only the uniform effective gravity at the mode point S. The
header called the omitted terms "a small fraction of g_eff".

**Fact (measured from the stored pitch, 30 pictures a second; finite differences under-read the peaks, so these are lower bounds).**

| ride | max pitch rate | max pitch acceleration | Euler theta'' r at r = 0.1 m | Coriolis 2 theta' u at u = 0.5 m/s |
|---|---|---|---|---|
| kerb, control off | 5.6 rad/s | 70.6 rad/s^2 | 7.1 m/s^2 | 5.6 m/s^2 |
| kerb, control on | 0.96 rad/s | 15.6 rad/s^2 | 1.6 m/s^2 | 1.0 m/s^2 |
| gentle roads, control on | 0.04 rad/s | 0.6 rad/s^2 | 0.06 m/s^2 | 0.04 m/s^2 |

**Inference.** On the uncontrolled kerb the omitted forces are of the order of g. On the controlled kerb they reach about 6 % of
g_eff's peak. On the gentle roads they stay under 1 % of g, so those two stored rides are kept.

**Physics.** In the frame of a glass that turns at rate Omega = theta' (about y) while its point S accelerates with a_S, a fluid parcel
at r relative to S, moving at u relative to the glass, obeys

    Du/Dt = -grad p / rho + g - a_S - Omega' x r - Omega x (Omega x r) - 2 Omega x u.

In the glass's (x, z) axes, with theta measured from e_x towards e_z:

    a_x = g_x + theta'' Z + theta'^2 X + 2 theta' u_z,    a_z = g_z - theta'' X + theta'^2 Z - 2 theta' u_x,    Z = z - z_S.

- The centrifugal term is a gradient, of theta'^2 |r|^2 / 2. Under the free surface the pressure absorbs it. At the surface it moves
  the equipotential, which is the level the stout settles to.
- The Euler term has curl -2 theta'' e_y, which is not zero. It is what makes the stout lag a turning glass (the spin-up problem):
  in the inertial frame an ideal fluid does not turn with its container, so in the glass's frame it turns backwards. A uniform
  g_eff cannot represent this.
- The Coriolis term does no work. It is applied as an exact rotation of each cell's velocity by -2 theta' dt.

**Fix (run 3).** All three terms are in `Stout.step(..., rot=(theta', theta'', z_S))`. Drops and lumps in flight feel the same
field. The head's weight and the rim's failure use the local field. The stout's push on the cart becomes -(dP/dt + Omega x P).
With rot = None, Fig. 12's code path is unchanged bit for bit (checked). Size of the effect: run 3's kerb ride against run 2's,
measured against the scatter between two particle seeds.

## C. Fig. 16's uncontrolled kerb stopped at 0.77 s

**Fact.** The drop list was full: 16,384 drops (`stout_jax.py`, `M_drops`). Run 3 tracks 131,072 drops and stores an even subsample
of 16,384 per picture for the drawing.

## D. Fig. 16: no control-off data on the gentle roads

Run 3 computes `resonant_off` and `bump25_off`. **Fig. 12 already has both rides of every road:** speed held only (run 8) and joint
control (run 10). Its switch needs no new data.

## E. Run-to-run scatter on the kerb

The Fig. 12 bands came from two runs with the same seed (unordered GPU sums): tilt ±0.3 mm, spill ±0.05 mL. Run 3 adds a second
particle seed for Fig. 16's kerb, with control on and off. That gives the scatter of the initial seeding as well, a wider and more
honest band.

## F. Numerical damping of the fluid method (Fig. 12 and Fig. 16)

**Fact (`notes/fig12/handoff-jax/07-diagnosis.md`).** The APIC hand-over damps the swing at about ζ_num ∝ Δx^1.6, which gives
0.006-0.010 at 1.5 mm. The bare stout's real damping is 0.0055. With the head (ζ 0.425) the method's share is 1.5-2.5 %: no visible
effect on the rides. **Open:** a 1.0 mm grid point would bound the extrapolation (about 5 times the GPU time per second of stout).

## G. Other items, open

- The stout's push measures 75.7 g against 55.8 g from cylinder theory. A tulip is not a cylinder: the wall's slope adds to n_x.
  To derive.
- The drawn Fig. 16 cart (`cart16-view.js` G) is not the simulated one (`cart4.py` CART4), and the deck is drawn 0.098 m high by an
  arbitrary offset. One parameter file is needed.
- The cart is planar: no roll, no yaw, both wheels of an axle meet the same road.

## Results of run 3 (Kaggle notebook version 4, 15 November 2026, 31 min of T4; commit 2056270)

**Fact** (`summary.json` of version 4, packed into `public/data/fig16/2026-11-15/`). The rotating-frame forces are on in every ride.

| ride | largest tilt (run, 60/s) | head spilled | stout spilled | largest pitch | ended |
|---|---|---|---|---|---|
| kerb, control on, seed 1 | 4.01 mm | 0.010 mL | 0 | 5.3° | 4.0 s |
| kerb, control on, seed 2 | 4.19 mm | 0.023 mL | 0 | 5.5° | 4.0 s |
| kerb, control off, seed 1 | 34.6 mm | 14.55 mL | 88.5 g | 20.4° | 1.73 s (surface list full) |
| kerb, control off, seed 2 | 35.1 mm | 14.61 mL | 93.2 g | 20.6° | 1.65 s (surface list full) |
| five 20 mm bumps, control off | 37.9 mm | 14.62 mL | 104.8 g | 7.8° | 2.92 s (surface list full) |
| one 25 mm bump, control off | 34.3 mm | 11.49 mL | 38.2 g | 9.3° | 8.0 s |

**The effect of the rotating frame's forces, against the scatter.**
- Controlled kerb, tilt on run 2's pictures: run 3 minus run 2 is 0.83 mm rms, 1.86 mm at most.
- The two seeds of run 3 differ by 0.75 mm rms, 1.80 mm at most.
- **Inference:** with control the omitted forces change the ride by no more than the run-to-run scatter. Run 2's controlled rides stand.
- Uncontrolled kerb, stout spilled by 0.733 s: run 2 5.9 g; run 3 10.1 g and 7.0 g (seeds 1 and 2). That is 1.2-1.7 times more,
  against a seed spread of 3 g. **Correction:** an earlier chat line said "three times"; it compared different moments.

**Under-sampling.** The controlled kerb's largest tilt is 4.01 mm at 60 pictures a second but 2.16 mm on every second picture.
Run 2's published 2.64 mm (30 a second) under-reads the peak. The pages must state the rate.

**Uncontrolled cart: why it fails.**
- The deck pitches up to 9-20°, and its pitch acceleration reaches 154 rad/s² on the kerb.
- On the five bumps the pitch spectrum peaks at 3.41 Hz, the stout's own swing frequency. The pitch mode and the slosh are in
  resonance.
- The head has 3.5 mm of freeboard below the rim, and a 9° tilt alone raises the wall by R tan 9° = 5.7 mm. So the head goes at once
  and the stout follows.

**Open:** the kerb and five-bump rides with control off stopped with the surface-candidate list full (K = 0.62 N), once a fifth of
the stout was in the air. Run 3b (notebook version 5) reruns them with K = N to their end.

**Page files.** At most 4,096 drops per picture are kept: an even subsample of the stored 16,384, for the drawing only. The true
count per picture is kept as `nd_true`. The one-bump ride is still 6.1 MB.

**Correction (15 Nov, 01:40 UTC).** The head as served is 91.3 mL (19 mm over the stout), not 14.6 mL. The uncontrolled rides lost
16 % of it, not "all". The stout is 430 g.

## H. The stout swells after violent stirring (found 15 November 2026 from run 3's stored data)

**Fact.** I compared the stored median surface with the height the stout still in the glass fills at rest, using the glass profile
of `guinness-glass.js` and the stored count of particles in the glass:

| ride | end | surface read | height of the remaining stout at rest | volume read / true |
|---|---|---|---|---|
| kerb, control on (two seeds) | 4 s | 125.0 mm | 125.0 mm | +0.1 % |
| one 25 mm bump, control off | 8 s | 131.8 mm | 117.1 mm | +18 % |
| kerb, control off (run 3b) | 4 s | 130.9 mm | 107.3 mm | +33 % |
| five 20 mm bumps, control off (run 3b) | 8 s | 136.6 mm | 103.8 mm | +48 % |

So a glass that has lost 86-103 g of its 430 g is drawn fuller than at the start.

**Cause.** The pressure step makes the grid velocity divergence-free. Particles moved by interpolated velocities still drift apart in
splashing and re-entry, and nothing pulls them back to their resting spacing of 8 per cell. The level set calls a cell liquid if
it holds any particle. A dilute cloud therefore reads as liquid up to a higher surface. Fig. 12's kerb rides show the same effect at
+0.85 to +1.44 mm (07-diagnosis.md). With control on, the effect is nil.

**Fix (stout_jax.Stout, vol_corr = kappa, default 0, so Fig. 12 is unchanged bit for bit, checked).**
- Each interior cell whose 5 x 5 x 5 block holds fewer than 0.95 of its resting 1,000 particles is given a net inflow target
  kappa (n/n0 - 1 + 0.05) dx/dt.
- The flow that meets these targets comes from a second projection, of a zero velocity field. It moves the particles' positions
  only (Kugelstadt et al. 2019); it never enters their velocity.

Two failed versions, both on the 6 mm CPU test:
- Put into the velocity, the correction overshot: a stout stretched by 20 % fell to 0.85 of its rest volume.
- Correcting both ways with 3 x 3 x 3 blocks inside a 3 % band (count noise about 7 %) stirred a pint at rest until its read
  surface fell 29 mm in 0.8 s.

The version kept leaves the pint at rest exactly as it was: 124.8 mm before and after.

**Run 4 (notebook version 6) and run 4b (version 7), 15 November 2026.**
- Run 4: the correction ungated, 3 x 3 x 3 blocks replaced by 5 x 5 x 5. The rest guard stopped it at 1.5 mm (largest deviation
  1.54 mm against a limit of 0.75 mm). No ride was computed; 3 GPU-minutes.
- Run 4b (commit fe8d981): the correction acts only while the whole pint has swollen by more than 4 %. The rest guard passes
  (0.54 mm, the same as without the correction). 42 min of T4.
- Swelling checks printed by the run, read surface against the rest height of the stout still in the glass:

| ride, control off | run 3/3b: volume read / true | run 4b | stout spilled 3/3b -> 4b | head spilled 3/3b -> 4b |
|---|---|---|---|---|
| kerb (4 s) | +33 % | +1.2 % | 86.0 -> 87.4 g | 14.53 -> 14.52 mL |
| five 20 mm bumps (8 s) | +48 % | +1.3 % | 103.1 -> 67.5 g | 14.61 -> 14.61 mL |
| one 25 mm bump (8 s) | +18 % | +1.5 % | 38.2 -> 38.0 g | 11.49 -> 11.63 mL |

- **Inference:** on the five bumps the swelling raised the surface, so the later bumps threw out stout that was not there. A
  third of run 3b's spill there (35.6 g) was a fault of the method. On the kerb and the single bump most of the spill happens in
  the first second, before much swelling, so the spill hardly changes.
- The rides on the page are run 4b's (index-16.json, kaggle_version 7). With control on, the rides need no correction (+0.1 %).

## I. Is the uncontrolled deck in resonance with the stout? (closed 15 November 2026)

**Correction.** An earlier line (section after run 3) took the pitch spectrum's peak at 3.41 Hz on the five-bump road as evidence of
resonance. The five bumps are 0.29 m apart, so at 1.0 m/s they arrive at 3.45 Hz: the peak is the road's own frequency. That alone
proves nothing about resonance.

**Fact.** The natural modes of the cart with control off come from `tools/fig16/kaggle/modes16.py`, which takes the eigenvalues of
`cart4.linear_model`: cart, deck heave and pitch, two axles, and the stout's first swing with the head (f 2.915 Hz, zeta 0.425).
It ran on Kaggle's CPU, notebook fig-16-cart-diagnostics-cpu version 3, commit 0df8870. Result: `notes/fig16/modes16.json`.

| mode | f (Hz) | zeta | shares (pitch as the rise of a corner 0.11 m out) |
|---|---|---|---|
| the stout's swing | 2.64 | 0.43 | stout 1.00 |
| deck heave | 3.33 | 0.28 | heave 0.92 |
| deck pitch with the stout | 3.85 | 0.33 | pitch 0.23, stout 0.75 |
| rear and front axle hop | 20.3, 26.1 | 0.11, 0.14 | axles |

The wheelbase filter: the rear axle meets a bump wb/v later. At 1.0 m/s the five bumps (3.45 Hz) drive the pitch by
|2 sin(pi f wb/v)| = 1.38 of the largest possible 2.

**Inference.** The deck's pitch is coupled to the stout's swing in one mode, at 3.85 Hz. The five bumps force it 10 % below that
frequency, inside its half-power band (zeta 0.33). The uncontrolled cart is near resonance through this coupled mode. The
mechanism: each bump rocks deck and stout together at nearly their own natural rate.

## J. Does the volume correction add or remove energy? (closed 15 November 2026)

**Fact.** The stored kinetic energy of the stout in the glass, without the correction (run 3b) and with it (run 4b):
- kerb: 17.9 and 19.7 mJ at the peak (0.8 s); tail decay rates 0.77 and 0.69 1/s;
- five bumps: 4.9 and 8.0 mJ at 2 s; tail decay rates 0.40 and 0.37 1/s.

**Inference.**
- By construction the correction moves positions, never velocities, and only lowers swollen stout: it removes potential energy and
  adds no kinetic energy. It acts only while the pint is swollen by more than 4 %, so in gentle swings it does nothing at all.
- The larger energy on the five bumps follows from the 35 g more stout kept in the glass.
- The tail decay rates agree to about 10 %. No sign of energy injection.

## K. The stout's push: 75.7 g measured against 55.8 g from theory (bounded, 15 November 2026)

**Fact.** `tools/fig16/gamma_check.py` regressed the stored push F_x on -q'' of run 8's rides at 30 pictures a second, q'' being
the second derivative of tilt/2 by two central differences.
- The glass is nearly a cylinder where the swing lives: R = 38.2-39.3 mm from 95 to 125 mm, with slope |dR/dz| <= 0.11. The
  swing's decay depth is R/xi = 21 mm.
- So the tulip shape does not explain a 36 % excess. The radius that would give 75.7 g is 43.3 mm.

**Fact.** Two central differences with step dt shrink a component at angular frequency w by [sin(w dt)/(w dt)]^2:
- 0.87 at 3 Hz and 30/s, so the fitted mass reads about 14 % high;
- more for the jolts' higher frequencies.

On run 3's 60/s rides, halving the rate raises the fitted mass by a factor of 1.4 to 2.1. Those rides cannot measure the mass
itself (their push includes the turning deck's effects; correlations 0.2-0.8), but they show the sensitivity to sampling.

**Inference.** Run 8's 75.7 g is inflated by at least 14-19 % at the swing's frequency; corrected, about 60-70 g. The remaining
10-25 % above theory cannot be settled from stored 30/s data. The clean test would be a free swing stored at 60/s or more with its
push stored.

**What it affects.** Only the design model (`slosh_model.py`), whose predictions were validated on rides it never saw. Every
number on the pages comes from the full fluid solver, which computes the push directly.

## F (result, 15 November 2026). The method's numerical damping, measured at 1.5 and 1.0 mm

**Fact** (`tools/fig12/kaggle/damping_grid.py`, Fig. 12 notebook version 12, commit 758df53, 13 min of T4;
`notes/fig12/damping-grid.json`). The stout alone, with no friction and no head, pushed and left to swing; ring 13 fitted with
run_b's `fit_swing`:

| grid | zeta | f0 | fit rms / amplitude |
|---|---|---|---|
| 6 mm (CPU, 07-diagnosis) | 0.0782 | 2.96 Hz | |
| 4.5 mm (CPU) | 0.0433 | 3.12 Hz | |
| 3 mm (CPU) | 0.0254 | 3.25 Hz | |
| 1.5 mm (GPU) | 0.0152 | 3.326 Hz | 0.08 / 4.7 mm |
| 1.0 mm (GPU) | 0.0090 | 3.350 Hz | 0.10 / 4.8 mm |
| theory, real stout (glass and bulk) | 0.0055 | 3.421 Hz | |

**Correction.** 07-diagnosis.md extrapolated 0.006-0.010 at 1.5 mm. The measured value is 0.0152.
- Local exponents: zeta ~ dx^0.74 from 3 to 1.5 mm, dx^1.29 from 1.5 to 1.0 mm.
- At the production grid the method alone damps the bare stout about 2.8 times as much as the real stout (0.0055). That accounts for
  run 6's measured 0.016 on its own: the bare swing of Fig. 12 (free_wall) dies about three times too fast.
- With the head (zeta 0.425) the method's share is 0.015 / 0.425 = 3.6 %, too small to change the rides with the head.

**Fix.** 1.0 mm cuts the method's damping to 0.009 at 3.4 times the particles and 3.4 times the time per step (372 against
108 ms). A rerun of the bare swing at 1.0 mm costs about 10 min of T4, not done. The Fig. 12 docs page now states the measured
number.

## I (correction, 15 November 2026)

`cart4.linear_model` has no push of the stout back on the deck: the stout row is driven by the deck, the deck rows see no stout.
The mode at 3.85 Hz is therefore the deck's own pitch mode, with the stout following it:
- natural frequency 4.08 Hz, ringing frequency 3.85 Hz, peak of the forced response 3.60 Hz (zeta 0.33);
- `modes16.json` lists ringing frequencies.

"Coupled into one mode" overstated it. What stands: the five bumps (3.45 Hz) fall inside that pitch mode's band, and the stout,
whose own swing with the head is 2.64-2.9 Hz with zeta 0.43, is driven hard by it.

## M. Found while the note's numbers were measured (15 November 2026; `notes/fig16/note_numbers.py`)

1. **Sign error, fixed.** `cart4.py` gave the centripetal part of a_S, the theta'^2 terms, the wrong sign.
   - g_x across the glass was exact, because the two errors cancel there.
   - g_z along the glass was off by -2 h_g theta'^2: at most 0.6 m/s^2 with control, 8.2 m/s^2 without.
   - Fixed in commit 7bb19a7, with a finite-difference check of the kinematics to 1e-6. Run 5 (notebook version 8) recomputes the
     five affected rides.
2. **The drive is limited by grip, not by the motors.** It is capped by tyre grip, mu N_r = 19.0 N at rest, not by the motors'
   48 N. On the controlled kerb the rear wheels lose contact in 13 stored pictures between 0.62 and 0.90 s, and the struts reach
   the bump stops (33.8 and 31.5 mm against +-30 mm). Open as a design limit, stated in the note.
3. **Seed 1 of the controlled kerb: a burst after 3.3 s.**
   - The probe reading jumps between -0.68 and +0.64 mm.
   - The actuators then push in opposite phase up to 32 N, against 2.1 N before.
   - Single-sample pitch accelerations reach 287 rad/s^2.
   - Seed 2 stays quiet (0.3 N).
   **Inference, untested:** splash or surface noise at the probes, which the Kalman filter passes to the controller. To check in
   run 5's rides.
4. **The glass radius at the fill height is 39.1 mm, not 36 mm.** A 9° tilt raises the wall by 6.19 mm, not 5.7 mm. The note uses
   39.1.

## L. Run 5: the centripetal sign corrected (15 November 2026; GPU notebook version 8, commit 7bb19a7, 51 min of T4)

**Fact** (Kaggle log of version 8; packed on Kaggle's CPU by `publish16.py`, notebook fig-16-cart-diagnostics-cpu version 5).
- Rest guard: PASS, largest deviation 0.54 mm.
- Swelling at the end of every ride: within +1.8 %.

| ride | run 4b (wrong sign) | run 5 (corrected) |
|---|---|---|
| kerb, control on, seed 1: tilt (run) / head | 4.01 mm / 0.010 mL | 4.02 mm / 0.015 mL |
| kerb, control on, seed 2 | 4.19 mm / 0.023 mL | 4.24 mm / 0.024 mL |
| kerb, control off: stout / head | 87.4 g / 14.52 mL | 75.6 g / 14.38 mL |
| five bumps, control off | 67.5 g / 14.61 mL | 77.2 g / 14.63 mL |
| one 25 mm bump, control off | 38.0 g / 11.63 mL | 39.6 g / 11.25 mL |

**Inference.**
- The along-glass error 2 h_g theta'^2 matters only when the deck turns fast. With control on it changes nothing beyond the seed
  scatter.
- Without control the stout spilled moves by 4 to 14 %.
- The pages now play run 5's rides (index-16.json, kaggle_version 8).

From now on, by the owner's rule, nothing runs outside Kaggle: these numbers come from Kaggle's logs, and the files were made by
Kaggle's CPU.

## M3 (diagnosed, 18 November 2026). The burst in seed 1 of the controlled kerb

**Fact.** `tools/fig16/kaggle/diag_burst.py`, Kaggle CPU notebook fig-16-cart-diagnostics-cpu version 6, on the stored rides of run 5.
- The probe reading recomputed from the stored surface matches the stored one: 0.024 mm rms (seed 1), 0.027 mm (seed 2). So the
  controller saw what the surface held.
- No column gained or lost its surface. The guess "a column loses its surface" was wrong.
- In seed 1 at 3.867-3.900 s single columns of the probe's patch spike for one picture while their neighbours move less than
  1.4 mm:
  - (51, 28) +2.92 mm;
  - (52, 29) -4.88 then +5.64 mm.
  Seed 2 shows the same kind, smaller: 1.0-1.7 mm in column 52.
- The column 52 sits next to the wall. The probe extends the surface linearly to the wall from r1 = R - 2.5 dx and r2 = r1 - 1.5 dx,
  which multiplies h1 by 2.67 and h2 by 1.67.

**Inference.** A smooth slosh moves neighbouring columns together. One column spiking 5 mm for 1/60 s is local: a drop landing at the
wall, or the surface finder's fallback. The bilinear probe passes it, amplified, to the Kalman filter, which reads it as slosh, and
the actuators answer (up to 28 N in run 5). A real level sensor averages over an area and would not see one 1.5 mm column.

**Fix (run 6, GPU notebook version 9, commit 5c45658).**
- `Stout.probes_patch` is a Fig. 16 option: each probe reads the median of 3 x 3 columns at the wall (centres 33.0, 34.5 and
  36.0 mm from the axis, |y| <= 2.25 mm), divided by the first mode's shape there (0.971).
- Fig. 12's `probes()` is unchanged.
- Run 6 recomputes the controlled kerb, both seeds.

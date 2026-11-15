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
| kerb, control off, seed 1 | 34.6 mm | 14.55 mL (all) | 88.5 g | 20.4° | 1.73 s (surface list full) |
| kerb, control off, seed 2 | 35.1 mm | 14.61 mL (all) | 93.2 g | 20.6° | 1.65 s (surface list full) |
| five 20 mm bumps, control off | 37.9 mm | 14.62 mL (all) | 104.8 g | 7.8° | 2.92 s (surface list full) |
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

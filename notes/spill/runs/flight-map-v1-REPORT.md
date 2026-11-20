# Fig. 16, ride `kerb_off`: the flight map (step 1 of DERIVATION-flight-inversion.md)

Stored ride: 241 pictures, t = 0.0000 to 4.0000 s; keys used: al, drops, gx, gz, mp, ndrops, nfly, om, t, th, v, vzc.

## The frame, impulse-exact (no pass mark)

b from the cart state against the stored gx, gz (interval means): rms 0.849 m/s^2, within 0.1 s of the kerb (t = 0.567 s) 1.393 m/s^2, largest 7.724 m/s^2. Largest al_k 138.6 rad/s^2; rms al_k - stored al 4.76 rad/s^2. Delta th - trapezoid of om: largest 5.40e-03 rad. Position error bound of constant b in an interval, |Delta b| dt^2/8: largest 0.63 mm.

## Checks (marks fixed before the run)

C1. det Psi = 1 (Liouville, tr A = 0): largest |det Psi - 1| = 1.23e-13 over 5734 RK4 steps (mark 1e-9): **PASS**
C2. om = 0, constant b: eq. (1) against the parabola, t0 = 0.100 s to 0.4 s, 50 states: largest error 2.22e-15 m (mark 1e-10): **PASS**
C3. om = 5.0 rad/s, b = 0: eq. (1) against the inertial straight line seen from the turning frame, 0.4 s, 50 states: largest error 1.00e-13 m (mark 1e-9): **PASS**
C4. A s + b against the stored solver's frame_accel, 1000 random states and frames: largest difference 2.84e-14 m/s^2 (mark 1e-12): **PASS**

A4 (no mark): listed markers above the grid's top (z >= 166.5 mm; rim at 147.5 mm, radius 37.5 mm) inside the rim's radius: largest 13.278 g at picture 58, 24.42 % of the liquid in the air then.

Wall time 2.1 s on Kaggle CPU.

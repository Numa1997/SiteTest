# Contract L10: a cloud with a shape (fall, mean motion, stochastic element)

23 October 2026. Numa's correction, verbatim: "IT IS NOT A RANDOM VELOCITY FIELD. IT JUST HAS A RANDOM ELEMENT TO IT, A STOCHASTIC
ELEMENT." The velocity of a drop is a deterministic part plus a stochastic element. This contract replaces the "random flow" framing of
`contract-L9.md` for the cloud scale; L9's question (does turbulence change the contact-scale kernel?) stays open and separate.
Written with the model already drafted (Numa asked for the work to be finished overnight); the Gate 1 skeptic could not run (usage limit),
so this level is marked provisional on the page until a blind skeptic has read it.

## 1. Question and observables
Where a drop sits in a cloud of finite shape changes what it meets and whether it survives. Observables, for shapes cumulus, disc, box
and tall tower, with and without the stochastic element, with and without the mean motion, with uniform and core-peaked ε:
when and where the first 100 µm drop forms; when the first drizzle reaches the ground; the shares of the water rained out, evaporated
in clear air and still aloft after 45 min.

## 2. Picture and mechanism
Smoke from a chimney: it rises with the wind (deterministic) and frays into puffs (stochastic). A drop's velocity is
dX/dt = U(X) + u′ − v_T(r) e_z: U a steady overturning cell filling the cloud's bounding box (up 1 m/s in the middle, down at the sides,
divergence-free); v_T the fall speed of chapter 2; u′ the velocity of the eddies smaller than a 50 m cell, per component an
Ornstein–Uhlenbeck process with variance σ² = (εh)^(2/3) (Kolmogorov structure function at the cell size h) and memory
T_L = 2σ²/(C₀ε), C₀ = 6, with Thomson's (1987) drift ½∂σ²/∂x_i(1 + u_i′²/σ²) where ε varies, so that evenly spread air stays evenly spread.
At ε = 10⁻² m²/s³: σ = 0.79 m/s, T_L = 21 s, eddy diffusivity σ²T_L ≈ 13 m²/s. The stochastic element moves drops between cells (and
out of the cloud); it is not used for contact-scale relative velocities, which stay those of chapters 1–4.

## 3. Model
Super-droplets (Shima et al. 2009) in a 2 km × 1.5 km slice of 50 m cells (depth 50 m), 96 droplet-mode and 32 collector-mode
super-droplets per cloudy cell; Shima's random-pair collisions per cell with the kernel of chapters 1–4; inside the shape the air is
saturated (no growth or loss by vapour); outside, dr²/dt = 2GS with S = −0.2 and G = 9.73 × 10⁻¹¹ m²/s (Rogers and Yau 1989, 7.17–7.18);
air reflects at all walls, falling drops leave through the ground (rain). No condensation anywhere: the cloud has no source of new water.

## 4. Rejected alternatives
1. An independent random velocity per drop with no memory (white noise): no correlation time, wrong dispersion at times below T_L.
2. A fully random (kinematic-simulation) field resolving all scales down to the drops: the L9 question, needs DNS validation; not the
   cloud-scale question asked here.
3. The well-mixed box: has no place in it, which is the point of this level.

## 5. Checks it must pass (results, `tools/run_cloud.cjs`)
- Box (no motion, 10 240 super-droplets, 4 seeds): t₅₀/t₉₀ = 5.807 ± 0.046 / 13.657 ± 0.080 min against the collection equation with the
  same 3σ-cut modes at s = 16, 5.873 / 13.716: within 1.2 % and 0.4 %. At 32 super-droplets per cell the box is about 10 % slow (15.2 ±
  0.4 min), at 128 within 2 %: the runs use 128.
- Well-mixed test (7200 air parcels, 30 min, ε from 4 × 10⁻² to 10⁻³, mean cell on): χ² per cell 0.79 (Poisson value 1).

## 6. Prediction written before the shape runs
The stochastic element lowers the rain at the ground (it mixes drops into clear air at the edges) and does not change the time of the
first drizzle at the ground by more than 2 min. Result: rain 32.6 % against 46.1 % without it; first drizzle at the ground 9.3–10.2 min
against 9.3–10.5 min. Passed.

## 7. Price
No condensation: the shape is a fixed saturated region with no supply, so "rained out" and "evaporated" are shares of a fixed start, not a
precipitation efficiency of a real cloud. Two dimensions. Super-droplet collisions only within a cell. The stochastic element's constants
(C₀ = 6, σ² = (εh)^(2/3)) are standard choices with an uncertainty of tens of percent.

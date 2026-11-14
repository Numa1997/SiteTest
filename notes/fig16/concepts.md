# Fig. 16: three cart concepts (STOP: the owner picks one)

Every number is printed by `python3 tools/fig16/concepts.py` (stored in `tools/fig16/concepts.json`); the lever study behind them
is `tools/fig16/sweep.py` (384 carts over the kerb, `sweep.json`). All from the slosh model validated on run 10
(`notes/fig16/model.md`). No fluid data was generated. Model bands: tilt ±1.1 mm on the kerb, ±0.1 mm on gentle roads; head
spilled ±0.07 mL. "Tilt" is the surface's tilt relative to the glass (front wall minus back), the stored rides' measure.

## What the lever study found (kerb, 1.5 m/s; Fig. 12's cart: tilt 26.2 mm, 2.46 mL of head)

1. **Hanging the glass as a pendulum is the strongest lever.** On Fig. 12's unchanged chassis, a free pendulum pivoted 300 mm above
   the glass's floor gives 4.9 mm and no spill. Mechanism: for a torque-free holder the glass's sideways acceleration at depth s
   below the pivot is A (1 − s/L_eq); the first mode feels it at its own point, 42 mm under the surface, which lies near the
   pendulum's centre of oscillation L_eq.
2. **A softer tyre** (6 instead of 20 kN/m) cuts the road's push from 82 to about 50 N and the wheel's time in the air by a third.
3. **A stronger motor alone makes it worse** (27.9–50 mm): the speed loop then jerks the cart harder after the jolt. It pays only
   with a preview that cancels the road's push as it comes: with the measured tyre load (a load cell at the axle) and a 24 V, 10 A
   drive, a fixed glass gets 5.2 mm and no spill.
4. **A larger wheel does not help by itself** (heavier unsprung mass, longer in the air).
5. **A torque motor at the pivot** makes any pivot height behave as the ideal one, and damps the holder's swing after the jolt.

## The concepts

| | A · the tray | B · the gimbal | C · the muscle |
|---|---|---|---|
| holder | cradle hung from a bail, pivot 300 mm above the glass's floor, oil damper 0.1 N m s; no actuator | gimbal ring, pivot 200 mm above the floor (52 mm above the rim), torque motor ±0.5 N m | fixed to the body |
| carried by the holder | glass 0.40 kg (assumed) + pint 0.456 kg + cradle 0.15 kg = 1.006 kg | same | (in the body) |
| chassis / wheel | 1.4 kg; wheel 40 mm radius, 0.30 kg; tyre 6 kN/m | 1.4 kg; wheel 60 mm, 0.45 kg; tyre 6 kN/m | 1.5 kg with glass; wheel 100 mm, 0.80 kg; tyre 6 kN/m |
| motor | Fig. 12's: 12 V, 3 A, 5 N/A (15 N) | 24 V, 10 A, 4 N/A (40 N) | 24 V, 10 A, 4 N/A (40 N) |
| sensors | wheel encoder, motor current | + IMU on the holder, load cell at the axle, pivot encoder | + load cell at the axle |
| control | speed PI + Fig. 12's road preview | speed PI + preview with the measured load; pivot torque = tuning term from the holder's accelerometer + LQR on (tilt of holder, its rate, the swing, its rate) | speed PI + preview with the measured load |
| five bumps, 1.0 m/s: tilt | 0.21 mm | 0.01 mm | 0.18 mm |
| 25 mm bump, 1.0 m/s: tilt | 0.22 mm | 0.01 mm | 0.07 mm |
| **kerb, 1.5 m/s: tilt / head spilled** | **3.83 mm / 0.00 mL** | **0.55 mm / 0.00 mL** | **5.22 mm / 0.00 mL** |
| kerb: road's peak push / tyre load | 54.9 N / 72 N | 56.5 N / 82 N | 49.5 N / 88 N |
| kerb: motor against its limit | 3.00 of 3 A, short for 82 ms | 10.0 of 10 A, short for 20 ms | 10.0 of 10 A, short for 20 ms |
| kerb: speed | 1.19–1.54 m/s | 1.39–1.52 m/s | 1.44–1.52 m/s |
| kerb: holder | swings 3.2°, still after 1.0 s | 1.7°, 0.33 of 0.5 N m, still after 1.4 s | — |
| kerb, a bump the map does not have | 4.09 mm / 0 | 1.85 mm / 0 | **50.3 mm / 5.25 mL** |
| kerb, preview 10 mm late | 4.09 / 0 | 1.20 / 0 | 15.8 mm / 0.24 mL |
| kerb, pint 10 % faster, 15 % harder to hold, half the friction | 6.36 / 0 | 0.57 / 0 | 8.74 / 0 |
| weak point | tall (bail 150 mm above the rim); no authority over the head once it moves; the least margin if the pint differs | most parts; its best numbers need the load cell and the 24 V drive; the tilt physics is theory not yet checked in the fluid solver | brittle: everything rests on knowing the road to a few millimetres; worse than Fig. 12 when the map is wrong |

For scale, Fig. 12's best stored rides (facts, `public/data/fig12/2026-11-14-run10/index-jax.json`): five bumps 1.00 mm (joint),
25 mm bump 1.03 mm (joint), kerb 20.81 mm and 1.63 mL (slosh LQR).

## What these numbers rest on, and what would break them

- **Validated:** the pint's swing, the cart, the head's spill rule, for a glass that does not tilt (run 10, never fitted).
- **Not validated (theory only):** how a tilting glass drives the swing. It uses the mechanical analogue of sloshing (each mode an
  equivalent mass at (2/k) tanh(kh/2) below the surface; Dodge 2000). No stored ride has a tilting glass. If the first mode's
  point were 10 mm off, concept A's kerb tilt would roughly double; B's feedback on the swing corrects for it.
- **Assumed:** glass mass 0.40 kg; the liquid turns with the glass as a rigid body; full state known to the controllers (the
  estimator is designed with the chosen concept); one wheel and no chassis pitch, as in Fig. 12.
- **For the GPU proof of A or B:** the fluid solver takes one gravity vector per step. A tilting glass also needs the rotating
  frame's forces, which vary across the glass. That is a small addition next to the fluid step, to be agreed before any launch.

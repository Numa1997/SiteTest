# Referee report: chapter 8 ("The air on the second blade") and related sections

Source read: `notes_as_read_3.md` only (chapter 0 and chapter 8 in full; 0.7, 5 (opening, including the 7.91 rpm paragraph), 6.2, 7.4 to 7.6).
All checks below are my own. "I computed" means I ran it in python3 (scripts in /tmp/referee).
Inputs used: rho = 1.225 kg/m^3, g = 9.80665 m/s^2, r_p = 63 m, lambda* = 7.55, a = 1/3, m = 1 kg, l = 1 m, I = ml^2/3.

Counts: 10 WRONG, 7 LOST, 13 MINOR. Most severe first within each kind.

---

## WRONG

### W1. The phase argument of (8.3) ignores the steady lean that 8.1 has just computed
(8.3) treats gravity's push as a pure cos(phi) and the shear push as a pure sin(phi), so the shear adds "in quadrature".
That holds only when the second blade hangs straight out. By (1.5), gravity's torque on a blade leaning by theta_s is
-(ml/2) g cos(phi + theta_s). The air's once-per-turn push is tied to where the hinge is (phi), not to the lean.
So with a lean, gravity's push has a sin(phi) part, G sin(theta_s), which is in step with the shear push.

- Wing (leans forward by 17 to 18 deg): gravity's sin(phi) part is 4.90 x sin(17.7 deg) = 1.49 N m, with the same sign as the
  shear push (2.41 N m; at the top the faster wind raises the lift and pushes forward). I computed
  ((4.90 cos theta_s + 0.02)^2 + (1.49 + 2.41)^2) / 4.90^2 = 1.54 to 1.55, i.e. **+54 %, not +23 to +25 %**.
  The lean also stiffens the swing: a steady force plus the centrifugal pull is a field of size F_c / cos(theta_s),
  so R becomes R / cos(theta_s). With that, I computed +47 to +48 %.
- Rod (leans back 30 to 36 deg): the same correction gives roughly -13 % (forcing only) or -25 to -29 % (with the stiffer field),
  but at that lean the drag model itself fails (see W6), so the rod number should not be quoted.

So the headline "between -15 and +25 %" (0.6, 8.2, 8.4, What to remember, 9.2) and "a few tens of per cent at most" (8.4)
are not supported. The wing's shear term alone can raise the harvest by about half.

### W2. The sign of the tilt term is not open; the geometry fixes it
8.2: "the sign depends on whether the tilt's push adds to gravity's or works against it". It is not a free choice.
The shaft points 5 deg up towards the hub. Projecting the horizontal wind onto the tilted rotor plane, I computed an
in-plane part v sin 5 deg = 0.697 m/s pointing **up** the plane. A blade moving up therefore meets less head wind; gravity
then pushes it **back** (the chapter 0 problem says so).

- Rod: less head wind means less drag, so the air's push turns forward exactly when gravity pushes back. The two oppose: **-15 %**.
- Streamlined blade: same reasoning: **-0.6 %** (I computed 0.994).
- Wing: lift dominates the derivative and the sign flips. The two add: **+25 %**.

Each shape has one value, not a range. Physical check: the tilt is just the air moving in the plane relative to the blade,
so its sign must match the sign of the air's damping (W3). The air damps the rod and the streamlined blade, so for them
the tilt opposes gravity. For the wing the damping is negative, so the tilt adds to gravity.

### W3. For the lifting wing the air does not "slow the swing": quasi-steady theory gives negative damping
8.3: "The drag and the lift change with it and resist the swing, like an extra brake."
I derived the in-plane force derivative from F_t = (1/2) rho c [C_L U_a W - C_D U_t W], with U_t the head wind along the path:

  dF_t/dU_t = (1/2) rho c W [ C_L sin(g) cos(g) - C_L,alpha sin^2(g) - C_D (1 + cos^2(g)) ].

Swinging forward raises U_t by s * dtheta/dt. That gives the damping
c_air = (1/2) rho W S (l^2/3) [ C_D (1+cos^2 g) + C_L,alpha sin^2 g - C_L sin g cos g ].
The lift term enters with a **minus** sign: more head wind means more dynamic pressure on a forward-leaning lift.
I computed:

| shape | notes' bound | my quasi-steady value |
|---|---|---|
| rod | 0.39 | 0.376 N m s |
| streamlined | 0.08 | 0.085 N m s |
| wing (C_L = 1) | 0.30 | **-0.024 N m s** |

The size is negligible next to 29.9 N m s, so "about one per cent" survives. But the wing's sign is wrong: the air feeds its
swing a little. The notes' formula with "+|C_L| sin g" is a valid upper bound, but the text reads it as the actual brake.
The flutter caveat in 8.4 is already visible here and deserves a sentence. (The rod has no lift slope, so its
pi sin^2 g term should be absent; it is negligible.)

### W4. "The steady push is the largest force in the plane" is false for the streamlined blade
8.1: "In every case the steady push of the air is the largest force on the second blade in the plane where it swings."
The same claim appears in 0.6 ("dominates everything else"), 8.4, What to remember and 9.2.
The notes' own table says the streamlined blade's push is 2.2 N. Its weight is 9.81 N and the outward pull is 57.9 N, both in that plane.
As torques: 2.2 x 0.5 = 1.1 N m against gravity's 4.90 N m. Even for the rod, the centrifugal pull (57.9 N) is larger than the drag (34 N).

The root is 0.7's argument: "the air would push it at least as hard as gravity does". That compares q x area, a push straight
into the face, with mg. But the in-plane force is q S (C_L sin g - C_D cos g), and for a streamlined body it is q S C_D, about 100 times smaller.
The chapter 0 opening ("section 0.7 estimates that it pushes at least as hard as gravity does") inherits the error.

### W5. "The in-plane part is the small part, because gamma is small" holds for lift only
8.1, and What to remember: "That part is small, because the apparent wind comes in nearly along the blade's path."
Drag points along the apparent wind, so almost all of it (cos 5.05 deg = 0.996) lies in the plane, along the path.
Only the lift's in-plane part is small (sin 5.05 deg = 0.088). The rod is the worst shape precisely because its force is
nearly all in-plane drag. The lesson as written points the wrong way for any draggy shape.

### W6. The steady lean: sin should be tan, and the rod's lean is outside the model anyway
8.1 writes the torque as F_t l/2. But F_t points along the path, and the blade leans by theta_s, so its lever arm is (l/2) cos theta_s.
The centrifugal torque is (ml/2) Omega^2 r_p sin theta_s, from (1.4). So **tan** theta_s = F_t / (m Omega^2 r_p). I computed:

- rod: 30.6 deg back (not 36.3 deg). With cross-flow drag on a yawed cylinder (normal force proportional to cos^2 theta),
  I computed 27.6 deg.
- wing: 16.9 deg forward (not 17.7 deg).
- streamlined: 2.2 deg either way.

Also, the rod's numbers do not quite follow from the stated inputs. I computed
F_t = q S C_D cos g = 2252 x 0.0127 x 1.2 x 0.996 = 34.19 N, so the cost is 2065 W and the notes' own sin formula gives 36.2 deg.
The quoted 34.3 N, 2071 W and 36.3 deg match q S C_D without the cos g.

### W7. The 6 m/s headline numbers are for a rotor speed the turbine never runs at
0.7 and chapter 5 say plainly that at 6 m/s the real control runs the rotor at 7.91 rpm, not 6.87 rpm, and that the
second blade then gives 233 mW, not 268 mW. I computed 268.2 x 6.866 / 7.91 = 232.8 mW, i.e. -13.2 %.
If the brake were left at its 6.87 rpm best, I computed 2 / (1 + (7.91/6.866)^2) = 0.859, i.e. -14 %.

Yet the answers in 0.6 and 9.2 ("161 and 267 mW", "57 to 106 mW", "66.7 mW to 74.0 W"), Table 3 and Table 5 all use the
6.87 rpm figure without a word. These sentences claim to answer for this turbine, so they need the real-speed value or the caveat.
The same applies to 0.2's "0.80 MW at 6 m/s", which assumes C_p = 0.482. My torque balance (L2) needs C_p(8.70) = 0.457 there, about 0.75 MW.

### W8. The inflow angle at the second blade assumes a = 1/3, but the second blade sits at and beyond the rotor's edge
The notes take gamma = 5.05 deg everywhere on the second blade, using the disc-average slowing a = 1/3 (8.1, 8.2).
But the second blade runs from r = 63 m to 64 m. That is at the tip vortex and outside the stream tube, where the local axial speed is
not v(1 - a). With a = 0, I computed gamma = 7.55 deg, q = 2274 Pa, and a wing push of 27.6 N instead of 17.6 N (+57 %, 1.67 kW).
The shear sensitivity changes too. This unstated assumption moves the wing's numbers by tens of per cent, and 8.4's list of omissions does not name it.

### W9. The friction share "14 to 15 % at the motor" does not follow from the stated numbers
From (7.7), friction's toll at the hinge is (2/pi)(N T_0/eta) Omega Theta. At the motor it is eta times that.
With T_0 = k_t i_0 = 0.836 mN m, N = 492 and eta = 0.6, I computed:

| wind | at the hinge (with gear loss) | at the motor |
|---|---|---|
| 6 m/s | 25.4 % | 15.3 % |
| 8 m/s | 26.1 % | 15.6 % |
| 10 m/s | 26.8 % | 16.1 % |

Using the full-equation swings gives 15.3 to 15.5 % at the motor. The notes' "25 to 27 % counting the gear loss" is right,
and the at-motor share must be exactly 0.6 of it, i.e. 15 to 16 %, not 14 to 15 %. Table 3's "14 %" at 6 m/s fits no route I tried.
My "paid" values (271.4, 204.0, 162.1 mW) and load values (104.2, 74.3, 56.2 mW) reproduce Table 3, so the inputs are the same.

### W10. "36 to 40 % of what the perfect brake of chapter 2 would take": the low end is 35 %
P* at 10 m/s from (2.5) is 160.9 mW. I computed 56.1 / 160.9 = 34.9 % (formula) and 57.2 / 160.9 = 35.5 % (full).
So the range is 35 to 40 %. Table 4's mean of 36.8 % at 1 kg confirms the formula values (38.9, 36.8, 34.9 %).

---

## LOST

### L1. 7.4: formula and full equation disagree on swing more than on load
"The full equation agrees with the formula within 2.1 %."
At 10 m/s the swing goes from 0.083 to 0.080 (-3.6 %, so the swing squared falls 7.1 %), yet the load rises from 56.1 to 57.2 mW (+2.0 %).
At 8 m/s the swing squared falls 4.7 % and the load rises 2.0 %. At a fixed R_L the load goes as <dtheta/dt^2>,
so either "swing" means something else in the full run (half peak-to-peak? the fundamental?), or harmonics carry about 9 % of the power.
Friction's third harmonic could do it: I estimate about 9 % of the fundamental's amplitude. The text should say which, and that the 2.1 % refers to load only.

### L2. Chapter 5: why 9.07 rpm, and is it consistent with C_p = 0.482?
"because the square law's constant k, set by NREL, balances the wind's torque at lambda = 7.48 rather than at the 7.55"

I computed NREL's k = 0.0255764 N m/rpm^2 on the fast shaft, which is 2.1286e6 N m s^2 on the rotor side.
That is exactly the C_p = 0.482, lambda = 7.55 optimum for the precone-shortened radius 63 cos 2.5 deg: the ratio is 0.99525 = cos^5 2.5 deg.
With r = 63 m:
- the balance at lambda = 7.55 needs C_p(7.55) = 0.4797;
- the balance at 7.48 needs C_p(7.48) = 0.4665.

So the ROSCO table must peak near 0.47, about 3 % below the 0.482 of 0.2. If it peaked at 0.482, the rotor would run *faster* than 9.155 rpm, not slower.
The notes should give the table's peak C_p and say why it differs from 0.482.

The 7.91 rpm at 6 m/s is consistent with that reading. I computed the ramp torque at 7.91 rpm, which is linear from 0 at 670/97 = 6.907 rpm
to k x 871^2 x 97 at 8.979 rpm: 0.911 MN m on the rotor side. It balances the wind's torque if C_p(8.70) = 0.457, plausible for a curve peaking near 0.47.
Also, 6.866 rpm sits only 0.6 % below the 6.907 rpm cut-in, which is worth saying.

### L3. 7.5: "the lightest second blade whose best brake this motor can reach"
This is reversed. The best brake grows with ml/2 (2.6), so every lighter blade's best brake is easier to reach. 1 kg is closer to the heaviest such blade.
At 2 kg, c* = 44.8 to 74.8 N m s, against c_sc = 68.3 N m s at 492:1, which I computed. The text should say "heaviest", or explain what is meant.

### L4. 8.3: where does the formula for c_air come from?
"that brake is at most c_air = rho W S (l^2/3)(C_D + |C_L| sin g + pi sin^2 g)"
There is no derivation. The reader cannot see why |C_L| appears with a plus sign, or where pi sin^2 g comes from (it is (1/2) C_L,alpha sin^2 g).
The derivation in W3 is four lines and would also show the sign.

### L5. 6.2: which blade damping ratio do the results use?
The model declares "a damping ratio zeta_b of 0.5 % or 3 %", but only one set of results follows.
I computed the gust power fed to the blade, 2 zeta m omega^3 x_rms^2 with m = 1416 kg, f = 1.08 Hz and x = 5 mm:
0.1106 W at zeta = 0.5 % and 0.664 W at 3 %. So "0.110 W" is the 0.5 % case. Is the 3.38 mW also 0.5 %? What does 3 % give?

### L6. "A streamlined blade that makes no lift" (chapter 8 opening; table)
Its whole once-per-turn shear torque, 0.85 N m (I computed 0.850), is lift: C_L,alpha = 2 pi times delta alpha.
And "Shear acts mainly through lift, so it matters for a lifting second blade" (8.2) then reads as if the streamlined blade were immune.
It should say "no lift on average".

### L7. Is the air in or out of these notes?
Chapter 0 opening: "what it does to the harvest is left for a later study". 0.7: "Its size is not known without a model of the air."
9.1: "The air, left out of these notes". But 0.6, chapter 8 and 9.2 quote -15 to +25 %. A reader cannot tell which stands.

---

## MINOR

M1. "gives -13 % less" (0.7) and "is -13 % below" (chapter 5) are double negatives. Write "13 % less".

M2. 267 against 268 mW at 6 m/s: 0.6 and 9.2 say 267, while 0.7 and Table 5 say 268. I computed 268.2 mW from (2.5).

M3. In 8.2 and 8.3, G_tau = (ml/2) g = 4.90 N m uses g. 6.2 uses the in-plane g cos 5 deg, as the 5 deg tilt of 8.2 also implies.
The difference is 0.8 % in power. Use one convention.

M4. "gains the power F_t Omega r_p": the force acts along 63 to 64 m, and q grows outward. The power is closer to F_t Omega (r_p + l/2), plus about 2 % from q.
That is 1 to 3 %, but the text implies precision with "2 071 W".

M5. "Everything else in the air's force points along the shaft": there is also an in-plane, spanwise part (no lever arm, but not along the shaft).
It is sizeable for the leaning rod.

M6. (8.2) drops dC_D/dalpha. For a symmetric section at zero lift that is fine. For the wing at C_L = 1 it is a few per cent of the bracket.

M7. Once-per-turn causes are listed differently in different places. 0.7 names shear and the tower; 8.2 names shear and tilt.
A tilted rotor also has a skewed wake, whose once-per-turn induction change is of the same order as the tilt term and is not mentioned. 8.4 names the tower only.

M8. "the air rushes past at twice motorway speed and more": at 6 m/s the tip moves at 45 m/s, 1.5 times a 30 m/s motorway speed.

M9. 7.4 text: "Even the strongest wind ... gives more than 1 500 times" the sensor's need. With the formula's 56.1 mW I computed 1492 times.
Only the full equation's 57.2 mW (1521 times) clears 1500.

M10. 7.2: j = 1.12 uses the gearhead's 0.7 g cm^2. With its 1.5 g cm^2, I computed j = 1.18. Negligible, but give the range.

M11. 7.6: "Both lean back by the same few degrees". The mean lag at the best brake, G^2 / (4R(R-1)), is 1.3 deg at 6 m/s (I computed). That is "about a degree".

M12. 0.5: "the machine below gives about a thousand times more". The notes' own figures are 1500 to 2800 times.

M13. 7.1: "some 79 000 to 130 000 times". I computed 79 400 to 132 300, so the top should read 132 000.

---

## Checked and correct (I computed each)

- 0.1 to 0.3: 1225 W through the doorway; disc 12 469 m^2; 314 W/m^2; 1.65, 3.91 and 7.64 MW; ratio 4.6; Betz 16/27; 0.482/0.593 = 81 %;
  gamma = 5.05 deg; W = 60.6 m/s; L/D threshold 11.3; 10.0 deg at mid-blade; 4 g on the whirled stick; 37.6 uW sensor; 6.6 Wh; 61 Wh.
- 0.7: 6.87, 9.16 and 11.44 rpm; 45.3, 60.4 and 75.5 m/s; 9.07 and 11.34 rpm at lambda = 7.48 (the notes say 11.33);
  2234 Pa; 43.9 cm^2, about four fifths of a 63 x 88 mm card; 233 mW at 7.91 rpm; lambda = 8.70.
- 8.1: q = 2252 Pa; m Omega^2 r_p = 57.9 N; steel rod mass 0.994 kg; Re 52 700 and 415 000;
  streamlined -2.24 N, 135 W, -2.2 deg; wing +17.56 N, 1061 W.
- 8.2: first harmonic of the 0.2-power profile 1.249 m/s, slowed to 0.833 m/s; delta gamma = 0.784 deg; tilt 0.697 m/s;
  torques 0.021/0.393, 0.850/0.089, 2.409/0.025 N m; the (8.3) ratios as printed (at zero lean).
- 8.3: c* = 29.88 N m s; the notes' bound evaluates to 0.385, 0.085 and 0.303 N m s.
- Chapter 5: J = 4.38e7 kg m^2; kinetic energy 10.5 to 10.7 s of output; ramp limits 6.907 and 8.979 rpm.
- 6.2: 0.1106 W feed (zeta = 0.5 %); quadratic scaling 3.38, 54.1 and 1352 mW; c* = 29.60 N m s and P* = 201.5 mW at 9.07 rpm with g cos 5 deg;
  x = 0.0638 and 25.6 mW; zeta = 0.307; frequency ratio 1.361; tuned length 1.851 m; +/-8.6 % shift.
- 7.1 to 7.4: k_e = 0.020759 V s; c_sc = 0.000282 N m s; N_min = 282 and 364; tau* = 3.467 N m; swing rates 0.093 to 0.155 rad/s;
  c_e/c* = 0.43, 0.41 and 0.39; effective brake 0.97, 0.92 and 0.88 of c* (matches "0.88 to 0.97"); N T_0/eta = 0.686 N m, 14.0 % of 4.90 N m;
  jamming ratios 4105 and 3518; peak voltages 1.386 and 0.802 V; 743 rpm; 0.114 to 0.191 Hz.
- 7.6: Table 5 rows checked (0.0667 W, 74.0 W, 0.867 N m, 45.4 N, 91.2 N, 8.34 kN); Theta* from 0.214 to 0.220 rad; limit 0.213 rad.

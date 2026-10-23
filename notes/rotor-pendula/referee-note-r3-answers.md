# Answers to referee-note-r3.md (23 October 2026)

Fixed in the note (theory/*.src.html, tools/make_numbers.py, tools/build_theory.py, tools/theory_template.html):

- B1 Figure 1 caption: the pull splits into a part along the rod (no lever arm) and a uniform Ω²r_p along the blade.
- B2 summaries (§0.2, §8.2) now say: shaking gives little at 5–20 mm tip vibration, more than gravity at 100 mm, a level no
  source confirms; bending (a couple of per cent) separated from shaking.
- B3 §6.2 now describes the model: modal mass 1416 kg, 1.08 Hz, ζ_b 0.5/3 %, forcing flat near 1.08 Hz scaled to the tip level,
  mode shape 0.82 and slope 27.8 mrad/m at the pivot, linear frequency response, SymPy equations; the shaking and gravity brakes
  differ (0.123 against 1.07 N m s), so their best powers do not add. (L3_shake_model.py writes the modal numbers.)
- B4 §1.3 explains Lagrange's equation in plain words (Newton's law for the angle, Q the generator) and Rayleigh's function.
- B5 §4.1 starts with the one-pendulum case in plain variables, defines S (m²/s³) and the Dirac delta, marks the general case
  as skippable, and restates (4.4) in plain words.
- B6 §8.1 says gravity does the work in the blade's frame and the rotor pays in the ground frame; §8.2's last sentence:
  "gravity steers the energy and the rotor pays it"; §1.4 says which picture the notes use.
- C1 rpm → rad/s example; C2 P_T explained, largest share on the smallest rotor; C3 arcsin(1/Γ); C4 energy-function argument
  shown; C5 Sol's brake defined; C6 "as long as r_p ≫ L" with the 400 rpm exception; C7 Figure 3 (the tilted hinge) and the
  sin²α term explained, mountings named, χ for the hinge angle; C8 §2.5 and §7.5 agree that resonance does not pay through a
  gearbox; C9 says the three second-order effects were not measured separately; C10 units; C11 the locked double resonates at
  R = 0.83; C12 2.0–6.6 times (computed); C13 brakes near resonance; C14 "in every case tried"; C15 the off-centre bob picture
  for the bill; C16 Cauchy–Schwarz steps; C17 the claim narrowed to the noise's own feed; C18 no S for a real blade, said why;
  C19 white noise against narrow-band shaking for single and double; C20 mass matrix A(q), M stays the total mass; C21 the
  rotor's equation, "standard deviation", s defined; C22 the kink at 8.98 rpm and its mechanism; C23 metronome picture; C24 the
  stator drag mechanism, last sentence plain; C25 −Gθ sin φ; C26 mL as the design lever (§8.1); C27 "the 400 rpm rotor";
  C28 Table 1 narrowed; C30 header softened ("line by line where short, by named computer algebra where long").
- P1 question headings and the question list rewritten as statements; P5 φ0 + θ = −π/2; P7 reactance explained; P10 28.5°;
  P12 Tables 2 and 3 captioned and numbered (the generator table is now Table 4), true minus signs; P13 quarter turn of the
  rotor; P14 equality condition; P15 damping ratio explained; P16 63 m rotor radius; P18 convex; P19 power ∝ push²; P20 width
  2ζ; P21 R_c, R_L throughout; P23 "at most about one radian per second"; P24 four-stage jam limit; P25 gearhead inertia
  for 51:1; P26 Table 4 caption explains why the rotor can pay more than P*, "load ÷ P*", "Formulas … give"; P28 voltages
  are for the large turbines; P29 the ceiling's picture (weight × speed) and its number (P* is 0.56 of it); P30 no-break
  spaces between numbers and units and in long numbers (build step).

Not done, with the reason:

- C29: one new figure (the hinge); no sag/rotation sketch or motor-chain figure yet.
- P2 (sensor budget breakdown), P4 (figure label typography), P6 (θ′ → iA line), P8 (half-power points on Figure 2),
  P9 (spacing of a displayed equation), P11 (flex-cost digits: the note's values come from unrounded ratios and are right),
  P17 (9.07 rpm against 9.16 rpm: 9.07 is the balance of the model's C_p table and torque law at 8 m/s, as stated), P22
  (symbols with two meanings: x and f remain in different chapters), P27 (split of the fast-rotor gap): left for the next round.

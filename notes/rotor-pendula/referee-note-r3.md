# Referee report, round 3: "Pendula on a Turning Blade" (rotor pendula lecture note)

Read blind, start to end, as two readers at once: a strong school student with calculus, and a physics graduate.
Source: `scratchpad/rotor_notes_r3.html` (self-contained, 1.14 MB). I read it two ways: the text with each KaTeX
formula's TeX recovered from its `aria-label`, and the rendered page in headless Chrome 156 (1400 × 1000 viewport,
32 full-page screenshots, plus overflow measured at 1400, 880 and 390 px). I did not read plan, check or earlier
referee files. I checked every number I could recompute against the note's own formulas; where a number matched,
it is not mentioned.

Counts: **6 blocking, 30 confusing, 30 polish.**

Ranks:
- **blocking**: a reader is stopped, or leaves with a wrong idea. The text states wrong physics, contradicts itself on a headline result, or gives numbers that cannot be followed at all.
- **confusing**: the reader can go on, but only by guessing, re-deriving, or ignoring a contradiction.
- **polish**: wording, notation, layout, house rules.

---

## Blocking

**B1 · §1.2, Figure 1 caption.** "Because the bob's pull points away from the hub and not along the blade, a tilted rod
is pulled back towards the blade's line: that is the centrifugal spring."
*Problem.* This is the wrong reason. Write the bob's position as r_p·ê_blade + L·ê_rod. The centrifugal force is
mΩ²(r_p·ê_blade + L·ê_rod), and the L·ê_rod part points along the rod, so it has no lever arm. The torque about the pivot
is exactly −mΩ²r_pL sin θ, the same as a *uniform* pull Ω²r_p along the blade. That is also what §1.1 says ("straight out along the blade")
and what the term in (1.3) says. A pull that was exactly along the blade would restore the rod just as well. The
graduate sees an error. The student learns a false mechanism, and it clashes with the weathervane picture of §1.1.
*Fix.* "The pull on the bob splits into a part along the rod, which has no lever arm, and a part Ω²r_p along the blade,
which turns a tilted rod back to the blade's line, like gravity for an ordinary pendulum: that is the centrifugal spring."

**B2 · §6.2 against §0.2, §8.1 and §8.2.** §6.2: "at 100 mm, the top of the range, 22.8 mW", against "8.9 mW from gravity".
§0.2: "The blade's own bending and shaking add little to a short pendulum". §8.1: "chapters 4 to 6 measured how little
that gives". §8.2: "the blade's bending gives a short pendulum almost nothing".
*Problem.* At the top of the note's own range, blade shaking gives Sol's short pendulum 2.6 times its gravity power.
The summary says the opposite. A careful reader cannot tell which to believe.
*Fix.* Either argue in §6.2 why 100 mm rms is unlikely (give a source or an estimate), or change the summaries to
something like "little at 5 to 20 mm rms of tip vibration, and more than gravity gives if the blade shakes at 100 mm,
which no source we found confirms". §8.2 should also separate "bending" (§6.1, sag) from "shaking" (§6.2).

**B3 · §6.2, the model behind every number.** "The model couples the blade's mode and the pendulum both ways …"
*Problem.* No equation, no modal mass, no modal damping for the "Sol's pendulum" runs, no description of how the gust
forcing is scaled to give 5 mm rms, and no definition of "best brake for the shaking". So 0.11 W, 0.057 mW, 19.1 mW,
17 %, 9 % and 2.8 mW all have no visible source. It is also unclear whether gravity's 8.9 mW and the shaking's 0.057 mW
are harvested at the same brake setting, and whether they add. This is the only chapter with no equation at all.
*Fix.* Give the two coupled equations: a blade modal oscillator with modal mass, frequency 1.0793 Hz and damping ζ_b,
driven by a band-limited force, coupled to (2.1) through the pivot's acceleration. Give the damping used for the Sol's
pendulum numbers, the forcing spectrum, the brake, and one worked number. Say whether the powers add.

**B4 · §1.3, Lagrangian mechanics with no introduction.** "Lagrange's equation, written for the one angle the bob is
free to move through, never needs them." Also "Rayleigh's dissipation function puts it into Lagrange's equation".
*Problem.* The target reader includes a strong school student. The note itself says "second- or third-year physics
student". Generalised coordinates, L = T − V, the Euler–Lagrange equation and Rayleigh's function arrive with no
statement of what they are or why they work. A school student is stopped at (1.3), and everything after it depends on (1.3).
*Fix.* Either a short paragraph ("for one coordinate θ, d/dt ∂L/∂θ̇ − ∂L/∂θ equals the generalised force; it is Newton's
second law for the angle, with the constraint forces already removed"), or, since the Check box says the Newton derivation
was also done, add a ★-free route. Take torques about the pivot in the turning frame: centrifugal part, gravity, and the
pivot's acceleration. That reaches (1.3) in four lines a school student can follow. Then mark the Lagrange route ★.

**B5 · §4.1, stochastic machinery for the school reader.** "⟨a(t)a(t′)⟩ = S δ(t − t′) … the momenta p_k conjugate to
the angles … K = ½ pᵀM⁻¹p, with M(q) the mass matrix … whether the kick is evaluated at the start or in the middle of
each step".
*Problem.* The Dirac delta, conjugate momenta, the mass matrix and the Itô/Stratonovich distinction are all used without
definition and without a ★. The coffee picture is good. But a school student has no route from it to (4.2), and the
result is not restated in plain words.
*Fix.* Mark the derivation ★. Before it, give the one-pendulum case in plain variables: a kick Δv = −a dt·(ê·t̂) changes
½mL²θ̇² by a first-order term that averages to zero and a second-order term ½m(ê·t̂)²S dt. Then restate (4.4) unstarred:
"random shaking cannot feed in more than S/2 times the total mass, whatever the pendulum does". Define S in words, with
its unit (m²/s³) and its meaning (the variance of the velocity kicks per second).

**B6 · §0.2 and §1.4 against §8.1 and §8.2, on who pays.** §0.2: "Who pays? The rotor." §8.1: "Gravity is the only thing
that feeds it." §8.2: "gravity turning once per revolution, is what feeds the sensor".
*Problem.* The last chapter seems to reverse the answer to one of the note's four headline questions. The reconciling idea is
one sentence in §1.4 ("Seen from the blade, gravity is the hand that pushes the rod; seen from the ground, it only steers
energy that the rotor supplies"). §8 never repeats it, so a reader finishing the note sees a contradiction.
*Fix.* In §8.1, after "Watch the pendulum from the turning blade", add: "In this frame gravity does the work; seen from
the ground, the same energy comes from the rotor (section 1.4). The two are one bookkeeping in two frames." In the last
sentence of §8.2, say "gravity steers, the rotor pays".

---

## Confusing

**C1 · §0.3.** "r_tip = λ_T v/Ω = 56 m/s / Ω", followed by "400, 200 and 100 rpm". Ω must be in rad/s. A student who puts in 400 gets 0.14 m.
*Fix.* Add "with Ω in rad/s: 400 rpm = 41.9 rad/s, so r_tip = 1.34 m".

**C2 · §0.3.** "Sol's estimate P_T = ½ρπr_tip²v³C_p … C_p = 0.45; the largest share is at 400 rpm, pivot at 30 %."
The formula is not explained, and a reader would expect the outermost pivot on the biggest rotor to take the largest share.
*Fix.* One clause: "the kinetic energy that flows through the rotor's disc per second, of which a fraction C_p is caught".
Then "the largest share is on the smallest rotor, whose own power is smallest (792 W), with the pivot inboard, where the
pendulum gives most (section 2.4)".

**C3 · §1.1.** "tilts … by an angle of about 1/Γ radian: 0.27° on the fastest mounting, but up to 44° on the slowest."
1/1.44 rad = 39.8°, not 44°. The 44° is arcsin(1/Γ), the largest tilt over a turn.
*Fix.* "by up to arcsin(1/Γ), about 1/Γ radian when Γ is large: 0.27° … 44° on the slowest."

**C4 · §1.4, (1.4).** "Differentiate it, use (1.3) to remove θ̈, and every term cancels (SymPy does the bookkeeping)
except two". The note's central claim, that the rotor pays, rests on a step the reader does not see.
*Fix.* Show the energy-function argument (★ if wanted). L has no explicit t, so
d/dt(φ̇ ∂L/∂φ̇ + θ̇ ∂L/∂θ̇ − L) = τ_rot φ̇ − cθ̇². T is quadratic in (φ̇, θ̇), so the bracket is T + V.

**C5 · §2.4, Table 1.** "the full nonlinear model of chapter 3 at Sol's brake setting". Sol's brake setting is never
defined. The footnote only says that at two mountings it is *not* κ*.
*Fix.* "Sol's brake is κ* = |R − 1| except at the two mountings marked ¹, where he used the best brake found by a
nonlinear search."

**C6 · §2.3 against Table 1.** "so a small fast rotor and a large slow one give the same power at the same fraction of the
blade". Table 1 at 30 %: 57.09 mW (400 rpm) against 28.91 mW (8 rpm).
*Fix.* "… the same power, as long as r_p ≫ L. On the 400 rpm rotor the pivot at 30 % is only 2L from the hub, r_p − L
is half of r_p, and the power doubles (Table 1)."

**C7 · §2.5, tilted hinge.** "Turn the hinge axis by an angle α towards the blade's own axis … The same Lagrangian, worked
through in SymPy". Then the stiffness R cos α − sin²α.
The geometry is very hard to picture from words, and there is no figure. The −sin²α term is not explained. It is not "the
same Lagrangian" either: the problem is now three-dimensional. "Fastest rotor" and "slowest rotor" do not name the
mounting (the first is the one at 30 %, the second the one at 90 %).
*Fix.* Add a small sketch: hinge axis, swing plane and resting rod, seen along the blade. Explain the term in one
line: "the bob, leaning out of the rotor plane, moves closer to the shaft as it swings, so its own centrifugal pull
softens the spring by sin²α". Name the mountings.

**C8 · §2.5 against §7.5.** §2.5: "resonance is a real option on a small, fast rotor". §7.5: "The lesson is general …
resonance does not pay."
*Fix.* In §7.5 say whether the general lesson also kills the tilted-hinge resonance. It should, because any real generator
behind a gearbox sloshes its rotor's energy through the gears at resonance. Then soften §2.5 to match.

**C9 · §3.1.** "They partly cancel, and what remains acts near the flat top of Figure 2". This explains the 0.68 %
agreement, but no number supports it. The reader is told one effect is "some 6 %" and is then asked to accept that the
three effects cancel.
*Fix.* Give the three second-order corrections to P* at the 8 rpm, 30 % mounting, with their signs, and their sum.

**C10 · §3.3.** "The net stiffness R − 1 of (2.4) becomes (Ml_c r_p − I_p)Ω²". The left side has no units and the right
side is a torque per radian.
*Fix.* "The net stiffness, mL²Ω²(R − 1) = (mr_pL − mL²)Ω² in physical units, becomes (Ml_c r_p − I_p)Ω²."

**C11 · §3.4.** "R = 1 is exactly the resonance of section 2.3". That is true for the single pendulum. For the double it is
not: the locked double is at resonance when Ml_c r_p = I_p, that is at r_p = 0.167 m (R = 0.83). The note's own
κ* = 0.128 at R = 1 shows the double is near resonance there, not at it.
*Fix.* "R = 1 is the single pendulum's resonance, and close to the double's (R ≈ 0.83 for the locked double)."

**C12 · §3.4.** "Note also how large all these powers are, four to seven times the best real mounting". The table gives
115 to 379 mW. Against the best real mounting, 57.1 mW, that is 2.0 to 6.6 times. §2.5 also says "several hundred milliwatts".
*Fix.* "two to seven times".

**C13 · §3.4.** "at R = 1 the double's best brake is κ* = 0.128", yet the best regular run in the table uses κ = 1.375, ten
times heavier. The meaning of "best brake" quietly changes at resonance.
*Fix.* One sentence: "at resonance the small-swing best brake no longer applies; large swings call for a much heavier
brake, which is why Sol's group sits near κ = 1 to 3."

**C14 · §0.2 and §8.2 against §3.4.** "It can move chaotically only near resonance" is stated as a fact. §3.4 says
"it is a sample, not a boundary".
*Fix.* "In every case tried, chaos appeared only near resonance."

**C15 · §3.2, the physical picture of the bill.** §1.4 promises that "Section 3.2 shows where, physically, the rotor's extra
torque comes from". §3.2 gives a correlation, ⟨θ sin φ⟩, and a boat analogy, but no picture.
*Fix.* The note's own formula gives the picture. τ̄_rot = mgL⟨cos(φ + θ)⟩ = mg⟨x_bob⟩, so the bob rides, on average, slightly on
the *rising* side of the wheel. The rotor keeps lifting an unbalanced weight, like a Ferris wheel loaded on one side. Say this in one sentence.

**C16 · §4.2.** "m_eff = max over q̇ of (b·q̇)²/(q̇ᵀMq̇)". This identity is the heart of the "three-line proof", and it is used without
proof.
*Fix.* One line: Cauchy–Schwarz in the inner product ⟨u, v⟩ = uᵀMv, with q̇ = M⁻¹b reaching the maximum.

**C17 · §4.2, last paragraph.** "The two inputs simply add … So the ceiling (4.4) bounds the extra power from white-noise
shaking". The noise term is bounded. But noise changes the motion, and with it the rotor's own input, gravity's
⟨θ sin φ⟩, which can go up or down. So (4.4) bounds the noise's input, not the extra power.
*Fix.* Say so, and either estimate the change in the rotor's input or narrow the claim.

**C18 · Chapter 4.** It never gives a number for the "hard ceiling" on a real blade. S for a blade is never estimated, so
the reader cannot compare S·M/2 with the 9 to 57 mW from gravity.
*Fix.* One line in the last paragraph. The 5 mm rms tip vibration of §6.2 corresponds to some S, so S·M/2 is about X mW.
If white noise does not apply, say so and give the order of magnitude anyway.

**C19 · §4.2 against §6.2.** §4.2: "a single and a double pendulum start with the same full effective mass". §6.2: "The
double pendulum … takes 0.71 times as much". The §4 check also says the tumbling double keeps 0.55 of its mass against
0.48 for the single, which looks like a case where the double does *better*. This is not discussed.
*Fix.* One sentence each. White noise sees only m_eff, so single and double are equal. Narrow-band shaking far below the
rod's own frequency is a push, like gravity's, and its torque scales with Ml_c. In violent shaking the double's tumbling
keeps more of its mass moving along ê, but both stay below the ceiling.

**C20 · §3.3, §4.1, §4.3, symbol M.** In §3.3 M is the total mass, in §4.1 M(q) is the mass matrix, and in §4.3 M_total is
the total mass again.
*Fix.* Keep M for the total mass from §3.3 on, and use 𝖬(q) or A(q) for the mass matrix.

**C21 · Chapter 5.** "In 40 ten-minute records the rotor's speed wanders by 10.3 % about its mean." The rotor's equation
of motion is never written: inertia, aerodynamic torque from C_p(λ), generator torque law. "Wanders by" is not defined
(rms? peak?). Later, s in "±s" and "s²/2" is undefined.
*Fix.* Give J Ω̇ = ½ρπR³v²C_p(λ)/λ − τ_gen(Ω) and the square law τ_gen = kΩ². Say "standard deviation 10.3 %" and
"s = 0.103, the relative standard deviation".

**C22 · Chapter 5, On our blade.** "at 8 m/s the full controller works just above a kink in its torque law, so gusts push
the average speed up by 2.6 %". The mechanism is missing: why does a kink raise the mean speed?
*Fix.* One sentence. Below the kink the generator's torque falls steeply (region 1½), so in lulls the rotor is braked
less and does not slow as much as it speeds up in gusts. Name the speed of the kink (about 8.98 rpm).

**C23 · Chapter 5, Picture box.** "A metronome on a train … keeps ticking at its own rate, unaffected. Our pendulum is
different and better". The pendulum *is* affected. What is better is that its frequency and its push scale together. As
written, the contrast reads backwards.
*Fix.* "A metronome on a speeding-up train keeps its own beat, so a push timed to the train would drift in and out of step
with it. Our pendulum's beat, √R per turn, and gravity's push, once per turn, both scale with the rotor, so they stay in step."

**C24 · §6.1.** "the rotation enters through the brake, a quarter turn out of step with gravity's push. The two effects
almost cancel." Nothing tells the reader why a drive a quarter turn out of step should cancel an in-step one.
"A large effect that cancels itself is a lesson in where the generator's frame is" is cryptic.
*Fix.* Give the mechanism. The stator's rotation β(t) makes the brake torque −c(θ̇ − β̇). At the best brake the swing
lags its push by 45°, so the extra drive cβ̇ has a part opposite to the swing's velocity of about the same size as the
sag's extra push. Or give the two numbers before cancellation at 90 %. Replace the last sentence with a plain one.

**C25 · §6.2.** "Gravity's push G sin φ in (1.5) stiffens and softens the rod once per turn". In §2.1 gravity's push is
G cos φ, and the stiffness modulation is the term −Gθ sin φ.
*Fix.* "Gravity's term −Gθ sin φ (section 2.1) stiffens and softens the rod".

**C26 · §6.2 and Chapter 8, the length of the rod.** "the longer rod also takes 50 mW from gravity alone, simply because
it is longer". (2.6) says P ∝ mL. Rod length is the plainest design lever in the note, yet L = 20 cm is never justified
and §8.2 never mentions it.
*Fix.* One paragraph in §2.4 or §8.2: power grows in proportion to mL. What limits L is the blade's inner width (about
2.3 m at 90 %), the r_p ≫ L assumption, and the gearbox's torque, since mgL/√2 grows with L.

**C27 · §7.5.** "On a small, fast rotor R − 1 is between 1 and 5". Table 1 gives R − 1 from 1.0 to 23.1 on the three fast
rotors. The statement is true only at 400 rpm.
*Fix.* "On the 400 rpm rotor R − 1 is between 1 and 5".

**C28 · §2.4, Table 1 layout.** The table is 918 px wide in an 817 px box at a 1400 px viewport (measured). The last column,
"double ÷ single", which is the headline result of chapter 3, is hidden behind a horizontal scroll, and its header shows
as a lone "d".
*Fix.* Drop the Γ column (it is R/G), or merge "rotor" and "pivot" into one "mounting" column as Table 2 does.

**C29 · Whole note, figures.** There are 2 figures for 9 chapters and 29 equations. The places where the physical picture
cannot be built from words alone have no figure: the tilted hinge (§2.5), the double pendulum and its locked
equivalent (§3.3), the trail and the off-centre bob (§3.2), the sag with the cross-section's rotation (§6.1), the
motor, gearbox and load chain (§7.1–7.2), and the rotor-speed record (Chapter 5). The Picture boxes are words only.
*Fix.* Add at least the hinge sketch (C7) and a sag/rotation sketch (C24). Those two carry claims that cannot be checked
without seeing them.

**C30 · Header against the text.** "Every equation derived line by line". Several results are reported from SymPy
or a solver without the lines: (1.4), (2.7), §3.3's double-pendulum equations, the 2Ω²w of §6.1, and all of §6.2.
*Fix.* Either show the short ones (C4, C7), mark the long ones ★ with a sentence on how they were checked, or soften the
header.

---

## Polish

**P1 · §0.2.** The section is a question-and-answer list ("**Who pays?** The rotor."), and §2.5 and §3.4 have question
headings. CLAUDE.md says "No question-and-answer format anywhere". *Fix:* make the four items statements ("The power",
"Who pays", …) and the headings declarative.

**P2 · §0.2.** "needs about 37.6 µW, using the typical currents of the two datasheets": no breakdown. *Fix:* one line
of currents × duty cycle × voltage.

**P3 · §0.3.** The link to Sol's report is relative (`study/report.pdf`). Check that it resolves on the deployed page.

**P4 · §1.2, Figure 1.** The labels m, L, θ are upright mono, not italic maths. "centrifugal Ω²r" in the figure, but Ω²r_p
in §1.1. *Fix:* italic labels, and state in the caption that the torque only sees Ω²r_p (see B1).

**P5 · §1.3, Check.** "at rest with the rod hanging straight down, where cos(φ₀ + θ) = 0". The upright position also gives
cos = 0. *Fix:* "at φ₀ + θ = −π/2".

**P6 · §2.2.** "Use complex notation: θ = Re[A e^{iφ}]". For the school reader, add one line on why θ′ → iA.

**P7 · §2.3, Picture box.** "equals the coil's reactance" assumes AC circuit theory. *Fix:* "the coil's opposition to
alternating current, ωL".

**P8 · §2.3, Figure 2.** "The top is flat". On the log axis the curve looks like a sharp peak. The half-power points
x = 0.27 and 3.7 are not marked, and the caption breaks with a lone "(" at the end of a line. *Fix:* mark the two points
and say "flat on a logarithmic scale of the brake: a factor 3.7 either way halves the power".

**P9 · §2.3.** The displayed c*ΩΘ* = … = mgL/√2 is set as three cells, leaving the "=" floating in a wide gap.

**P10 · §2.4.** "the swing reaches 0.50 rad (29°)". 0.498 rad is 28.5°. *Fix:* "0.50 rad (28.5°)".

**P11 · §3.3, On our blade.** "costs only a further 1.3 to 1.9 %". From the printed ratios, 0.643 → 0.635 is 1.2 % and
0.750 → 0.735 is 2.0 %. *Fix:* print the ratios to one more digit, or quote 1.2 to 2.0 %.

**P12 · §3.4 tables.** Both tables have no number and no caption. Their minus signs are hyphens ("-1.707", "-0.01").
*Fix:* call them Tables 2 and 3 (renumber the motor table), and use true minus signs.

**P13 · §3.4.** "rescale their separation back every quarter turn". Of which rotor? Say π/2 of rotor angle, about 0.39 s.

**P14 · §4.2.** "Equality needs every mass to move with the same velocity along ê". It also needs each velocity to be
parallel to ê (the second inequality in (4.3)).

**P15 · §4.2, Check.** "braked with a damping ratio of 0.2". The damping ratio is undefined for the school reader, and
the pendulum's natural frequency for this test is not given.

**P16 · Chapter 5 against §6.1.** "the 63 m blade" against "A blade 61.5 m long". 63 m is the rotor radius. Is "30 % of
the blade" 30 % of 63 m or of 61.5 m? *Fix:* "of the 63 m rotor radius".

**P17 · Chapter 5.** "its power coefficient curve comes from NREL's own published table" and "turns at 9.07 rpm". Name the
table, and say that 9.07 rpm follows from it. The usual figure, from λ = 7.55, is 9.16 rpm.

**P18 · Chapter 5.** "this curve bends upwards near Ω₀". The curve is falling. Say "is convex (curves upwards)" and give
f″(1) = 1.

**P19 · §6.1.** "On its own that would raise the power by 1.0 %, 6.0 % and 14.5 %". Say that P ∝ g², so
(1 + 2Ω²w/g)² − 1. The 30 % value then comes out 1.1 %, so check the rounding.

**P20 · §6.2.** "the blade's resonance is only 0.5 to 3 % wide". 0.5 to 3 % are damping ratios. The half-power width is
2ζ, that is 1 to 6 %. Since the conclusion compares it with ±9.6 %, use the width.

**P21 · §7.1.** "R_c", "R_L" here, but "R_coil", "R_load" in §1.3. Also R (stiffness ratio) against R_c, R_L. *Fix:*
one notation for the resistances throughout.

**P22 · Symbols used twice.** x is the coordinate (1.1), the hinge swing angle (2.7), κ/κ* (Fig. 2) and the motor-side
torque (7.8). f is the fraction of the blade (§2.3) and the friction (7.4). δ is the phase (2.2) and the Dirac delta
(§4.1). k is the efficiency factor (7.8) next to k_t and k_e. *Fix:* one symbol, one meaning (STANDARD, 21 Oct.
verdict, item 2).

**P23 · §7.1.** "its shaft turns at well under a radian per second". At 400 rpm, 30 %, ΩΘ* = 0.82 rad/s. *Fix:* "at
most about one radian per second".

**P24 · §7.2.** "The pendulum jams beyond a ratio of 164 on a three-stage gearhead, so the catalogue ratios 190, 246 and
492 are useless". Those ratios are four-stage (η = 60 %), where the limit is 141. The stricter condition of §7.3,
4f/π < G, lowers both. *Fix:* give the four-stage limit too.

**P25 · §7.2.** "the GP 32 C planetary gearhead adds 0.7 to 1.5 g cm² … Through a ratio of 51 that gives j = 1.00". Say
which gearhead inertia the 51:1 case uses.

**P26 · §7.4.** Table 2's "rotor pays 116.29 mW", against P* = 57.09 mW in the first row, puzzles the reader until §7.5.
Add "(see section 7.5)" in the caption. "÷ P*" should read "load ÷ P*". "The formula (7.6) and (7.7) gives" should be
"Formulas … give".

**P27 · §7.4.** "the full equation gives the load 18 to 40 % more than the formula, because …". Two causes are named, but
not which one dominates. One measured split (e.g. the run with j = 0) would settle it.

**P28 · §7.4.** "peaks at 88 to 326 mV and alternates once per turn, at 0.13 to 0.33 Hz". This is the large turbines only
(8 to 20 rpm). Say so; the fast rotors alternate at 1.7 to 6.7 Hz.

**P29 · §8.1.** The shopping-bag picture (weight × height) fits (8.1) only if the right side is read as mg × the bob's
mean speed, L⟨|θ̇|⟩. Write it that way. Section 8.1 is titled "The ceiling" but gives no number. Add one: at the best brake
the bound is P*/0.56.

**P30 · Line breaks, typography and house rules.** Rendered breaks between number and unit: "100 | 000", "8 | m/s",
"19 to 31 | %". *Fix:* non-breaking spaces. Body text is set in IBM Plex Sans (computed style). CLAUDE.md and STANDARD
§4 ask for Latin Modern in notes. There are no ★ passages, no "Key result" boxes, no worked Examples, no Problems box,
and no Further reading list with working links. Sources are cited only inline (NREL/TP-500-38060, IEC 61400-1, maxon
339152, ADXL362, CC2652R).

---

## Verdict per section against `notes/STANDARD.md` §4 (and the 21 October verdict)

| Section | Verdict | Main reasons |
|---|---|---|
| 0.1 | clear | Good everyday motivation (sensor, Ferris wheel). |
| 0.2 | needs work | Q-and-A format (P1); summaries contradicted by §6.2 (B2) and §8 (B6); chaos overclaim (C14). |
| 0.3 | needs work | rpm/rad·s⁻¹ (C1); P_T and C_p unexplained (C2). |
| 0.4 | clear | |
| 1.1 | needs work | 44° against 1/Γ (C3). Picture otherwise good. |
| 1.2 | needs work | Figure 1 caption gives the wrong mechanism (B1). |
| 1.3 | needs work | Lagrange and Rayleigh with no introduction for the school reader (B4). Derivation itself correct; I re-derived (1.2) and (1.3). |
| 1.4 | needs work | (1.4) not shown (C4); frame idea not carried to §8 (B6). |
| 1.5 | clear | (1.5) and the On our blade numbers check out. |
| 2.1 | clear | The reason for dropping −Gθ sin φ is honest and well argued. |
| 2.2 | clear | Small polish (P6). |
| 2.3 | clear | (2.3) to (2.6) and Fig. 2 check out; polish P7 to P9; C6 on (2.6). |
| 2.4 | needs work | Sol's brake undefined (C5); Table 1 key column hidden (C28); (2.6) claim against the table (C6). |
| 2.5 | needs work | Hinge geometry needs a figure and the −sin²α reason (C7); conflict with §7.5 (C8). |
| 3.1 | needs work | "partly cancel" unsupported (C9). The numerical method is stated well (order, error ratio 30, agreement 6e−13). |
| 3.2 | needs work | Algebra correct; the promised physical picture is missing (C15). |
| 3.3 | needs work | Units slip (C10); no figure (C29). (3.4) and the 0.643/0.750 numbers check out. |
| 3.4 | needs work | "exactly the resonance" (C11); "four to seven" (C12); meaning of best brake (C13). |
| 4.1 | needs work | No ★, no plain restatement (B5). |
| 4.2 | needs work | Identity not proved (C16); "inputs simply add" (C17); no number for the ceiling (C18); single against double (C19); symbol M (C20). |
| 5 | needs work | Rotor model not stated (C21); kink mechanism (C22); metronome picture (C23). |
| 6.1 | needs work | Cancellation mechanism missing (C24); no figure. |
| 6.2 | needs work | Model undisclosed (B3); contradicts the summaries (B2); G sin φ mislabel (C25); rod-length lever (C26). |
| 7.1 | clear | Generator as a brake is well motivated; the numbers check out. Polish P21, P23. |
| 7.2 | clear | Polish P24, P25; the uncertainty paragraph is good practice. |
| 7.3 | clear | Describing function well introduced; (7.6) and (7.7) check out. |
| 7.4 | clear | Table 2 internally consistent (the 18 to 40 %, 19 to 31 % and 47× claims all reproduce); polish P26 to P28. |
| 7.5 | needs work | "R − 1 between 1 and 5" (C27); reconcile with §2.5 (C8). |
| 8.1 | needs work | Frame reversal (B6); analogy and missing number (P29). |
| 8.2 | needs work | "almost nothing" against §6.2 (B2); chaos overclaim (C14); rod length absent (C26). |

Standard-wide gaps: no ★ layering, no Further reading list (§4.8), body font not Latin Modern, no worked Examples or
Problems (21 Oct verdict). The limits of the model (§4.7) are scattered through the chapters but never gathered into one place.

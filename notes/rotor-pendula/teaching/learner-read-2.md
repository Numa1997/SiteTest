# Learner read 2: "A Second Blade on a Turning Blade"

Reader: BSc physics (computational/theoretical). Knows Lagrangians, ODEs, Fourier, numerics. Knows nothing about turbines, generators, gearboxes, turbulence spectra, blade structures.
Source read: `notes/rotor-pendula/teaching/notes_as_read_2.md` only. Arithmetic checked in a Python scratch session under /tmp.

Total LOST items: 11 (ch 0: 1, ch 1: 0, ch 2: 0, ch 3: 2, ch 4: 1, ch 5: 2, ch 6: 2, ch 7: 3, ch 8: 0). "I computed" marks my own checks; everything not flagged checked out.

---

## Chapter 0: From scratch: the wind, the turbine, and the question

I computed: doorway 1 225 W; disc area 12 469 m²; 314 W/m², 1.65 / 3.91 / 7.64 MW; Betz derivative and 16/27; shaft power 0.80 / 1.88 / 3.68 MW; rotor 6.87 / 9.16 / 11.44 rpm; tip angle 5.05°, apparent wind 60.6 m/s, cot γ = 11.3; sensor budget 37.6 µW and 6.6 Wh over 20 years; whirled stick ≈ 4 g; dynamic pressure 2 234 Pa and 43.9 cm²; all five problems. All correct except the item below.

### LOST
1. "The air's pressure matches that on an area of only ... 43.9 cm², a little more than a playing card." I computed a standard playing card (63.5 × 88.9 mm) at 56 cm². 43.9 cm² is about four fifths of a card, not "a little more". The comparison is backwards. Small, but it is the one picture I am given for the size of the air force, and it points the wrong way.

### SLOWED
1. "a turbine that stops the wind takes nothing" (0.2), then the Check box: "At $a = \tfrac12$ the wake stands still but $C_p = \tfrac12$, not zero". The picture and the formula disagree, and the repair (stopping the wind *at the disc* means $a \to 1$, outside the model) comes only after the derivation. I spent time thinking I had the derivation wrong. Say up front which "stopping" the picture means.
2. "This step ignores the push of the surrounding air on the sides of the widening tube; the standard derivation ... gives the same thrust". I am asked to take on trust that the ignored term is harmless. One sentence on why it cancels, or "trust this", would do.
3. "Turn too fast, and the blades sweep the disc so often that it behaves like a wall". Hand-waving next to a careful Betz derivation. I could not tell what physical quantity "behaves like a wall" refers to (solidity? induction $a \to 1$?).
4. "161 and 267 mW ... in steady winds of 10 and 6 m/s" (0.6). The numbers are listed small-to-large but the winds large-to-small. I had to re-read to pair them.
5. 0.6 uses "first moment", "chaotic", "ceiling", "vibration ... grows as the square of how far its tip vibrates" before any of these are built. As a preview it is fine, but I could not check any of it yet and it reads as a list of claims.
6. The whirled-stick picture (end of 0.5), which is the best picture in the chapter, comes after the machine has already been described in words. I understood the machine only once I read the stick paragraph.
7. "about a thousand times more" (0.5) and "more than 1 500 times" (0.6) for the same ratio. I computed 57 mW / 37.6 µW = 1 516. Pick one.

### ANNOYED
1. "Every number in these notes is computed from the model; the inputs taken from datasheets ... are named with their sources." and "SymPy confirms each line of the derivation." This is about how the notes were made, not physics.
2. 0.8 "How to read these notes": "A green Check box ... A wine-coloured On our blade box". Box colours and a reading manual, before chapter 1. Also the box is called "On our turbine" in chapter 0 and "On our blade" in 0.8.
3. Title line: "Part IA second blade on a turning blade" (export run-together of "Part I" and the title).
4. "One warning before we start ... It is worth having on its own, because ..." The defence of the scope comes before I know what the scope is. 0.7 says the same thing again at length.

### What I understood
Wind power goes as the cube of the wind speed, and a rotor can take at most about 59 % of it because it has to let the slowed air leave. The blades are wings moving sideways much faster than the wind, so the air they feel comes almost head-on. Riding on a blade tip, you are flung outward several times harder than gravity pulls, and gravity's direction swings round once per turn. The plan is to hang a small hinged arm at the tip, let gravity's swinging pull rock it, and brake that rocking with a small generator to power a sensor.

### The one fix that would help most
Move the whirled-stick picture to the start of 0.5 and make it the definition of the machine; then cut 0.7 and 0.8 down to a few lines each.

---

## Chapter 1: Riding at the tip

I computed: tan α = 3/9.81 gives 17.0°; Γ = 3.32 / 5.90 / 9.23; arcsin(1/Γ) = 17.5° / 9.75° / 6.22°; the gravity components −sin φ and −cos φ; the Euler torque −(I + (ml/2) r_p cos θ) φ̈ (integrated it myself); the potential (1.4) and its θ-derivative; the whole Lagrange check (1.7) to (1.5) by hand and with SymPy; R = 94.5, √R = 9.72, G = 28.45 / 16.00 / 10.24; mg r_p = 618 N m; 0.372 N m and 1.11 MN m; all six problems (35.5°, 3.29 m/s, the Coriolis direction, 1.48 Hz and 0.61 Hz with ratio √Γ, sin φ = 1/Γ, 0.372 N m). All correct. This is the strongest chapter.

### LOST
None. Every number and every line of the derivation checked.

### SLOWED
1. "a free small swing makes $\sqrt R$ swings per rotor turn" (1.6) and the problem answer "1.48 Hz". This ignores gravity's own share of the stiffness. The curvature at the bottom of the bowl is set by the size of the apparent gravity, which runs from Γ − 1 to Γ + 1 in units of g. I computed that at 6 m/s the free rate then wanders between √(R − G) = 8.1 and √(R + G) = 11.1 per turn, not a fixed 9.72. Say "on average" or "ignoring gravity".
2. The swing-and-hand guess (1.5): "You put your hand on the seat and simply move with it ... Does the swing gain energy from your hand?" If I "simply move with it" I need exert no force at all, so the answer "your hand pushes along the motion and gives energy" surprised me. The real point, that a force in step with the *position* does no net work and only a part in step with the *velocity* does, is never said in those words. It is the key idea of the chapter.
3. "Summed along the rod, its torque about the hinge is $-\left(I + \tfrac{ml}{2}r_p\cos\theta\right)\ddot\varphi$." Given without the one line of working. I had to do the cross products myself.
4. "For gravity that is the familiar $\tfrac{ml}{2}\,g\sin(\varphi+\theta)$." The hinge's own height, $m g r_p \sin\varphi$, has been dropped without a word (it does not depend on θ). 1.7 then puts it back in V. Say "dropping the part that does not depend on θ".
5. 1.3 to 1.5 has no picture I can see (Figure 4 is only a caption), and the sign of θ and of the "across" direction carries the whole chapter. I checked it with the Chapter 0 problem (anticlockwise rotor, blade level to the right, gravity pushes back). That problem is the best sign check in the notes; it would help to point back to it in 1.3.

### ANNOYED
1. "SymPy repeats the calculation and agrees identically." I just did the calculation by hand; this sentence adds nothing.
2. "Every term has a meaning." followed by a list that mostly repeats names already given in 1.3.
3. "Two numbers say how the rod resists turning and how a pull grips it." Then "You know both from the rod pendulum". I do; a definition and the formula would be enough.

### What I understood
If you sit on the blade tip, being flung outward feels like a strong gravity pointing along the blade, three to nine times real gravity. Real gravity, seen from the tip, turns round once per turn. Add the two and you get a "down" that wobbles a little to each side, by up to about 17° in light wind. The hinged arm tries to hang along that wobbling "down", the generator acts like honey, and the energy the honey takes is paid by whatever keeps the big rotor turning, not by gravity.

### The one fix that would help most
Say plainly in 1.5 that a push in step with the position does no net work and only a push in step with the velocity does; then the hand-on-swing guess and the 45° result of chapter 2 both follow from it.

---

## Chapter 2: The best brake, and how much it gives

I computed: battery 16 / 18 / 16 W; the phasor solution (2.2); dP/dκ = 0 gives κ* = |R − 1|; the algebra from (2.3) to both forms of (2.5); P* = 268.2 / 201.2 / 160.9 mW; Θ* = 0.215 / 0.121 / 0.077 rad; c* = 22.4 / 29.9 / 37.4 N m s; τ* = 3.47 N m; κ*/(2√R) = 4.81; half-power points 2 ∓ √3; (2.7) = 265.4 / 199.0 / 159.2 mW; the resonance length l = 3r_p/2; the "about 90" times extra inertia (I get 93.5); the second-order mean trail −GΘ sin δ/(2R) = −0.0229 rad at 6 m/s (matches the full model's −0.0231). All five problems check.

### LOST
None.

### SLOWED
1. "$c^* \approx \frac{ml}{2}\,r_p\,\Omega$ ... For our second blade that is 22.4 to 37.4 N m s". I computed the approximation (2.6) at 22.6 to 37.7; 22.4 to 37.4 are the exact values. Small, but I stopped to find out which formula was meant.
2. "the dropped term of section 2.1, of order $G^2$, grows as $\Theta^2$ too, because the swing $\Theta$ is itself proportional to $G$." The term is $-G\theta\sin\varphi$, which is of order $G\Theta$. I worked out that this means $G^2$ because $\Theta \propto G$. The whole paragraph ("How far can the small-swing theory be trusted?") is dense; it reports a fit ("1.1 to 1.2 times the swing squared") and then explains why the fit cannot separate effects. I was not sure what to take from it.
3. "At 6 m/s and a brake of 0.05 $\kappa^*$ the swing reaches 0.31 rad". From (2.2) I get 0.304 rad. If 0.31 is the full model's value, say so.
4. Table 1: "brake.wind | rotor | $G$ | ..." The table header is glued to the end of the caption. I had to rebuild the columns.

### ANNOYED
1. The battery warm-up is good, but the analogy is then drawn three times: battery (2.3), "the load matches the source" (2.4), and the "exact electrical twin" with a coil. One would do; the coil version is the accurate one, since the battery one wastes half and this does not (which a problem then has to correct).

### What I understood
For small swings the arm is a mass on a stiff spring being shaken slowly, once per turn, far below its own ringing rate of about ten times per turn. Damping takes the most power when it equals the spring's net stiffness at the shaking rate; then the arm lags the push by 45° and is heavily overdamped, so it just creeps. The best power goes as the arm's mass times its lever arm, times g², divided by the speed of the hinge, so faster rotors give less. For 1 kg on 1 m it is about 0.27, 0.20 and 0.16 W at 6, 8 and 10 m/s, and the generator must hold about 3.5 N m whatever the wind.

### The one fix that would help most
Rewrite the "How far can the small-swing theory be trusted?" paragraph as two plain sentences (agreement near the best brake; where and by how much it fails), and move the error-scaling argument to chapter 3, where the three effects are actually separated.

---

## Chapter 3: Big swings, the bill, and chaos

I computed: the roots of μ² + κμ + R = 0 at κ* (−92.5 and −1.02); 0.011 s and 1.03 s; one turn 6.55 s; step 1/240 turn = 0.027 s > 0.011 s; the scaling of the second-order corrections (3.16 and 7.7 times smaller); the mean trail (3.1)–(3.2) and the identity (3.3); the exact rotor torque in 3.2, which I checked with SymPy (it is right, including the $ml\,r_p\Omega\cos\theta$ inside the bracket); trails 1.31° / 0.42° / 0.17°; P from the trail 270 mW; the ⟨sin θ⟩ correction that brings it to 267 mW; lump versus rod 2.011; all three decay rates in Table 2 (−6.42, −29.37, −2.94 per turn); creep time 0.83 s at 10 m/s.

### LOST
1. "the term section 2.1 dropped ... changes the power by +1.43 %; the softer spring of $\sin\theta$ by +0.59 %; and gravity's push kept whole ... by −0.90 %. Together, the full equation: −0.31 %." Read as three separate effects they add to +1.12 %, not −0.31 %. Only after a while did I see that the third already contains the first, so the total is +0.59 − 0.90. The −θ²/2 term alone must then be about −2.3 %, which is the biggest effect, and the text never names it as such. As written the arithmetic looks wrong.
2. "The second blade, flung outwards, pulls on the hinge, along the line from the hub to its own centre of mass ... its line misses the hub by a small lever arm". A line *from the hub* cannot miss the hub. I worked out that the force is *parallel* to hub→centre of mass and acts *at the hinge*, so its line of action misses the hub by about (l/2) sin θ. Only then did the torque $\tfrac{ml}{2}r_p\Omega^2\sin\theta$ come out. The figure that would show this is a caption only.

### SLOWED
1. 3.1 numerics paragraph: Radau IIA, "falls on average by $2^{5.2}$", "4·10⁻¹⁵", "2·10⁻¹²", "8·10⁻⁷". I know numerics, and these are fine, but they are a solver audit sitting between the stiffness idea and the physics. The one needed point is "stiff, so implicit, and the step is checked".
2. "every case is run from 8 different starts, ... and at the best brake and at a tenth and a hundredth of it, where a lightly braked swing has the most freedom." The sentence runs two lists together (starts and brakes). I read it three times.
3. Table 2 header glued to the caption again ("...$\mu^2 + \kappa\mu + R = 0$.wind | $G$ | brake |").
4. "chaos needs a spring and a push of similar strength, near resonance". Stated as a law. It is a heuristic; the evidence is the table. Fine, but say "here" rather than "chaos needs".
5. Table 2 shows the exponents are the same at every wind. That follows because R and κ do not depend on the wind; one line saying so would have saved me deriving it.

### ANNOYED
1. "SymPy and a page of algebra give" and "In all nine runs of the full model (three winds, three brakes), the exact identity holds to 1·10⁻¹²." Process talk; the identity is exact algebra, so a run that confirms it to 1e-12 tells me about the solver, not the physics.
2. "the trail is the bill" appears in a section title, a box, the text, a figure caption and "What to remember". Five times.

### What I understood
The arm's equation is stiff: a sudden jerk dies in a hundredth of a second, but a slow displacement takes about a second to creep back, so it needs an implicit solver. Solving the full equation changes the best power by less than a third of a per cent. On average the arm hangs slightly behind the blade, by about 1° in light wind; its outward pull then has a small lever arm about the hub and drags the rotor back, and that drag times the rotor speed is exactly the harvested power. Putting the mass at the far end doubles the power. The motion always settles to the same periodic swing; no chaos was found.

### The one fix that would help most
In 3.1, list the second-order effects as three separate, non-overlapping terms (the dropped −Gθ sin φ, the sin θ softening, the −½Gθ² cos φ term) with numbers that add up to −0.31 %.

---

## Chapter 4: A ceiling on random shaking

I computed: the kick argument ΔK = q̇·Δp + ½ΔpᵀM⁻¹Δp and its mean; m_eff = ¾ m cos²ψ for the rod; the Cauchy–Schwarz chain (4.3); S = 2 × 0.201 / (0.75 × 1) = 0.536 m²/s³; 3.27 m/s² rms for that S spread over 0–10 Hz (using one-sided density 2S); the gentle check case, rms swing of the 0.1 kg, 0.2 m bob at ζ = 0.2 and S = 0.028: 0.050 rad (matches), and the violent case, linear estimate 2.1 rad ("more than a radian", matches). The Itô = Stratonovich remark is right: the noise coefficient depends on the angles only.

### LOST
1. What the ceiling rules out for the real blade. 0.6 promised: "Chapter 4 proves a ceiling: whatever the second blade does, chaotic or not, it cannot draw more from random shaking than a limit set by its mass and the shaking's strength." The end of chapter 4 then says "A real blade, though, does not shake as white noise: it shakes mostly near its own edgewise frequency ... shaking at one frequency acts like a push". So the bound is for white noise only, and the blade's shaking is narrow-band, where the input depends on the response and the bound does not hold. The box "How hard would it have to shake?" compares against white noise from 0 to 10 Hz and says "The blade's own shaking is nothing like that, as chapter 6 shows"; chapter 6 then finds 100 mm of narrow-band vibration beats gravity. After the chapter I could not say what, for this machine, the ceiling actually excludes. I needed one sentence: "for the blade's real, narrow-band shaking this ceiling does not apply; it only settles the chaos question for broadband noise."

### SLOWED
1. "Spread evenly over every frequency from 0 to 10 Hz, that is a shaking of 3.3 m/s² rms". The notes define S only through ⟨üü⟩ = S δ(t − t′) and never link it to a spectrum. I got 3.3 m/s² only after assuming a one-sided density of 2S per Hz (variance = 2 S × 10 Hz).
2. "$\Delta p = -b\,\sqrt{S}\,dW$, where $dW$ is a random number of mean zero and variance $dt$." Fine for me, but this is a Wiener increment and the notes do not name it, then explain √dt in a long aside. The aside was good; the jump from δ-correlated force to dW was not.
3. 4.2 "where $\psi$ is the angle between the shaking and the direction in which the blade's pieces move". The direction of motion of the pieces is across the rod; one word ("across the rod") would save a reread.

### ANNOYED
1. "a reader who skips them loses only the proof, and can go on to the result (4.2) and its plain-words form after (4.4)." Reading instructions inside the argument.
2. "The rod's value $\tfrac34m\cos^2\psi$ is checked in SymPy." It is two lines of algebra, already shown.
3. "Part IIRandomness: shaking, gusts and a bending blade" (export run-together, as for Part I).

### What I understood
Random shaking of the hinge adds energy even though each jolt is equally likely to help or hinder, because energy goes as velocity squared. For truly white noise the average energy fed in is half the noise strength times an "effective mass", and that effective mass can never exceed the real mass (three quarters of it for a rod on a hinge), whatever the motion. So irregular or chaotic motion cannot beat white noise. Simulations of a pendulum and a double pendulum confirm the formula, and the chaotic case took less, not more.

### The one fix that would help most
Move this chapter to an appendix, or end it with one plain sentence saying the bound covers broadband noise only and that the blade's real shaking is narrow-band, so chapter 6 has to compute it directly.

---

## Chapter 5: Gusts and the rotor's speed

I computed: rotor kinetic energy ½ J Ω² = 2.0 × 10⁷ J, which is 10.7 s of 1.88 MW ("about 11 s", fine); Q_aero = ½ρπr³v²C_p/λ; the ratio P(Ω)/P(Ω₀) = 2/(1 + Ω²/Ω₀²) from (2.3), its slope −1 and curvature +1; s²/2 = 0.53 % for s = 10.3 %; IEC class A σ = 0.16 × (0.75 × 8 + 5.6) = 1.86 m/s; the real-law case −2.56 % + 0.53 % ≈ −2.0 % (matches −1.99 %).

### LOST
1. "Below 8.98 rpm the law has a kink: there the torque ramps down in a straight line to zero at 6.9 rpm". Chapters 0 to 3, 7 and 8 put the rotor at 6.87 rpm in a 6 m/s wind. That is *below* 6.9 rpm, where this torque law gives zero generator torque. With no brake the rotor speeds up until it balances on the ramp. I estimated where (assuming C_p falls off its peak like a parabola, since the notes do not give C_p(λ)): about 7.9 rpm, λ ≈ 8.7. By (2.7) that would cut the 6 m/s headline, 267 mW, by about 13 %, to roughly 233 mW, and change the 6 m/s column of every table. The notes never say whether the 6 m/s case is real for this turbine. It is their best case, quoted in 0.6, 2.4, 7.4 and 8.2.
2. "At a steady 8 m/s the two torques balance at 9.07 rpm, 1.0 % below the $\lambda^*v/r_{\rm rot}$ of section 0.3, because that ramp holds the rotor a little off its best ratio." Two paragraphs later: "At 8 m/s the rotor runs just above the kink." Above the kink (8.98 rpm) the law is the pure square law, which by the notes' own argument "balances it at $\lambda^*$ in every wind". So the ramp cannot be the reason for the 1 % offset. I could not find the real reason (perhaps the square-law constant does not match the peak of the C_p table).

### SLOWED
1. "the wandering speed adds +0.90 %, a little more than the 0.53 % the curvature alone predicts (we have not traced the rest)". 0.90 against 0.53 is 70 % more, not "a little". This is the one effect the chapter's formula is meant to predict.
2. "rotor and main generator together have a moment of inertia $J_{\rm rot} = 4.38\times10^7$ kg m²". Why the generator, at the far end of a 97:1 gearbox, counts at all (inertia × N²) is explained only in 7.2, with the egg beater. I stopped to work it out.
3. Kaimal spectrum, coherence, TurbSim: named, not shown. Acceptable for a summary; I took the 10.3 % on trust.
4. The symbol $k$ is the torque-law constant here and the gear-loss factor in (7.8).

### ANNOYED
1. "Only 8 m/s was simulated." Tacked on at the end of a paragraph about the wind model. It should sit beside the results.

### What I understood
The rotor is a huge flywheel, so gusts only change its speed slowly, by about a tenth. The arm settles in about a second, so it simply follows the rotor's current speed. With the arm's generator setting fixed, its power goes as 2/(1 + (Ω/Ω₀)²): a faster mean costs power one-for-one, and wandering about the mean adds a little. On this turbine the controller lets the rotor run faster on average in gusty wind, so the net is about −2 %; with a plain square-law controller it would be about +0.8 %.

### The one fix that would help most
State the rotor speed this turbine actually runs at in a steady 6 m/s wind, and redo or flag the 6 m/s numbers throughout.

---

## Chapter 6: The blade bends and shakes

I computed: the sag-only gain (1 + 2Ω²w/g)² − 1 = 16.8 to 18.3 % (notes: 16.9 to 18.4 %, within rounding of w); a one-line phasor model of the tilt (below), which gives +2.0 % for the modal shape against the notes' +2.2 %; the blade's input power 2ζ_b M ω³ x² = 0.110 W at 5 mm, which matches only for ζ_b = 0.5 %; the square law 3.38 → 54.2 → 1 350 mW (ratios 16.0 and 399); brake ratio 29.6/1.89 = 15.7; damping ratio 0.31; the tuned length 1.85 m; the detuning ±1/(2Γ) = ±8.6 %; resonance widths 2ζ_b = 1 % and 6 %.

### LOST
1. "For comparison, gravity gives 202 mW at its own best brake, 29.6 N m s." Table 1 said 201.2 mW at 29.9 N m s. I computed that 29.6 N m s, the "1.36 times the blade's" frequency ratio and the ±8.6 % all come from 9.07 rpm, the chapter 5 operating point, not the 9.16 rpm used in chapters 0 to 3. The switch is not announced, so the same quantity has two values.
2. "the two best brakes differ by a factor of fifteen, so the two best powers cannot simply be added." Then no combined number is given. One generator has one brake. I computed that at the shaking's best brake (1.89 N m s, x = 0.064 of gravity's) gravity's harvest falls to 2x/(1 + x²) = 13 % of its best, about 26 mW. So "at 100 mm, 1 350 mW, more than gravity gives" (repeated in 0.6 and 8.2) compares two different machines. I needed: at one brake, what is the total?

### SLOWED
1. The tilt cancellation in 6.1: "That drag follows the rate of change of the slope, a quarter turn out of step with the sag's push, while at the best brake the swing lags its push by 45°; so part of the drag works against the swing." From this I could not predict the size. Writing it as a phasor did it at once: with the stator tilted by β₀ cos φ, (2.2) becomes (R − 1 + iκ)A = −(G_eff + iκβ₀), and at κ = κ* the relative swing is (G_eff − κ*β₀)/(√2 κ*). The tilt subtracts κ*β₀ straight from the push. With β₀ = 28.1 mrad/m × 0.431 m I get κ*β₀ = 1.13 against G_eff − G = 1.29, net +2.0 %. Say this in one line.
2. "with a damping ratio $\zeta_b$ of 0.5 % or 3 % of critical, two assumed values" and then the results 3.38, 54.2, 1 350 mW without saying which. I worked out from the 0.110 W that it is 0.5 %.
3. "the range comes from two ways of taking the shape of the bend, from the blade's first mode of vibration or by integrating the bending directly". Then +2.2 to +3.5 % "for the two shapes" with no word on which is better. A small sag difference (431 vs 467 mm) gives a big difference in the net (2.2 vs 3.5 %), which is exactly the "difference of two large numbers" problem; say which shape you trust.

### ANNOYED
1. "(Linearising the Lagrangian with a moving hinge, in SymPy, gives the same.)", "(The full linear equations ... were derived in SymPy.)", "(For the first shape, linear theory and a full nonlinear run ... agree within 0.2 percentage points.)" Three process asides in two pages.

### What I understood
The blade sags under its own weight, to one side and then the other, once per turn, so the hinge is moved sideways in step with gravity's push; that alone would add about 17 % to the power. But the tip also tilts, and the generator brakes motion relative to its own housing, which tilts with the tip; that takes almost all of the gain back, leaving +2 to +3.5 %. The blade's own vibration near 1 Hz could add power that grows as the square of its amplitude, but nobody has published that amplitude for this blade. An arm tuned to the blade's frequency (1.85 m) could draw much more, but gravity retunes it every turn, so that is open.

### The one fix that would help most
Give one combined result at one brake: gravity plus 5, 20 and 100 mm of vibration, with the generator set once.

---

## Chapter 7: From swing to watts

I computed: k_e = 0.02076 V s; c_sc = 2.82 × 10⁻⁴ N m s; minimum ratios 282 and 364; hinge speeds 0.09 to 0.15 rad/s; j = 1.12; T₀ = 0.84 mN m; hinge friction 0.686 N m and 14 % of 4.90 N m; jamming ratios 4 105 and 3 518; the describing function 4f/(πΘ) and (7.6), (7.7). I then reproduced Table 3 from (7.6)–(7.7) with the stated R_L and η = 0.6: swing 0.220 / 0.127 / 0.083 rad, load 104.2 / 74.0 / 56.1 mW, paid 271.4 / 203.1 / 161.7 mW, motor speed 743 rpm, peak load voltage 1.39 to 0.80 V. All match. Table 5: P* at the corners (66.7 mW, 74.0 W), τ* up to 936 N m, pull 91 N and 8.34 kN, the outer 3 m pull 10.1 kN, Θ* between 0.213 and 0.220 rad. All match.

### LOST
1. "Even so the motor brakes only 0.39 to 0.43 of the best brake (2.6), which is why the second blade swings wider than in chapter 2 and gives less." From the notes' own formula, the swing feels κ_e/η + 4f/(πΘ), which I computed to be 0.97, 0.92 and 0.88 of κ* at 6, 8 and 10 m/s: almost the best brake. And the rotor pays 271 mW at 6 m/s against P* = 268 mW, so the second blade gives *at least as much* as in chapter 2. The load gets less because the gears, the coil and the friction eat it, not because the brake is too weak. The 0.39–0.43 counts c_e alone and ignores both the 1/η and the friction, which are brakes too.
2. 7.6: "These notes size the second blade for the most power from one small catalogue generator ... 1 kg on 1 m is the lightest second blade that generator serves fully". Table 4: at 8 m/s, 1 kg gives 74 mW and 2 kg gives 133 mW. By "most power" the answer is 2 kg. The 1 kg choice maximises the *share* of P* (36.8 % against 33.3 %), which is a different criterion. 0.6 repeats the claim ("1 kg on 1 m is the size the catalogue generator ... serves best").
3. "The motor's friction takes 14 to 15 % of what the rotor pays". The friction term of (7.7) gives 25 to 27 % of what the rotor pays. I reach 15–16 % only by multiplying by η, i.e. charging the gear loss on the friction torque to the "gears". That split is not defined anywhere, so I could not check the 14 %.

### SLOWED
1. Tables 4 and 5 disagree in spirit. 7.6 says that past a first moment of about 0.5 kg m the RE 25 "delivers 93.9 to 107 mW at 6 m/s whatever the size". Table 4 at 8 m/s shows 5 kg and 10 kg delivering 57 mW, *less* than 1 kg (74 mW), at ratio 246. I could not reconcile these without the torque limit for each ratio; only "6 N m for the largest ratios" is given.
2. Table 4 mixes a column averaged over three winds with two columns at 8 m/s.
3. 7.2 then 7.4: the gear loss is first charged "the simple part" and then fully in (7.8) with $k = \eta^{-\mathrm{sgn}(x\theta')}$. I followed it, but $k$ was the torque-law constant in chapter 5 and $x$ is a torque here.
4. Table and caption glued together again for Tables 3, 4 and 5.

### ANNOYED
1. "Follow the power down the chain, from the rotor to the load: of what the rotor pays, the motor's friction takes 14 to 15 %, the gears and the coil's resistance most of the rest, and 35 to 39 % reaches the load." This repeats the paragraph just above it almost word for word.
2. "811 times" appears twice, "more than 1 500 times" three times across the notes, "311 times" once more. One ratio, once.
3. 7.1 opens with the bicycle dynamo again, already used in 1.4 with nearly the same words.
4. Table 5 has 16 rows to make three points; four rows would do.

### What I understood
A small permanent-magnet motor with a resistor across it is a brake proportional to speed, and a gearbox multiplies that brake by the ratio squared. The arm needs a brake about 100 000 times stronger than the bare motor gives, so it needs a ratio of about 500, which brings friction, a 60 % gear efficiency and a little extra inertia. Treating friction as an equivalent damper, the load gets about 57 to 106 mW, a bit over a third of what the rotor pays, at about one volt alternating once per turn, which still needs electronics. A bigger arm needs a bigger generator because the torque it must hold grows with the arm.

### The one fix that would help most
Replace "the motor brakes only 0.39 to 0.43 of the best brake" with the true account: the arm sees nearly the best total brake and takes nearly P*; of that, friction, gears and coil take about 60 %.

---

## Chapter 8: The answer

I computed: P* = ½ τ* Ω Θ* and the ratio to (ml/2) g Ω (2Θ/π), which is π/(4√2) = 0.555.

### LOST
None. The inequality (8.1) is right and the argument in the turning frame is clean.

### SLOWED
1. "section 0.7 showed that a few square centimetres of it, at a force coefficient of one, would feel a force as large as its weight." 0.7 said 43.9 cm², which is not "a few", and never mentioned a force coefficient.
2. (8.1) is a new result, and the best explanation in the notes of *why* the power is small (the stiff spring keeps the arm slow). Meeting it in the last chapter, after the numbers, is late. It belongs at the end of chapter 2.

### ANNOYED
1. 8.2 repeats 0.6 nearly line for line: 161 to 267 mW, 57 to 106 mW, "more than 1 500 times", "a few per cent", "we found no published value". This is the third time for most of these.
2. "Every value taken from outside these notes comes from one of these, each of which a reader can open."

### What I understood
Seen from the blade, only gravity can feed the swing, and its torque is capped, so the power is at most that capped torque times the arm's average swing speed. The stiff centrifugal spring keeps the swing slow, and the best brake already takes 55 % of that cap. The real open question is the air, which pushes on the arm at least as hard as gravity and could feed or damp it.

### The one fix that would help most
Move 8.1 to the end of chapter 2, and cut 8.2 to the air question and a pointer back to 0.6.

---

# Summary

## The five worst problems, ranked
1. **The 6 m/s operating point does not exist on this turbine's own torque law** (chapter 5). 6 m/s at λ* is 6.87 rpm, below the 6.9 rpm where the main generator's torque is zero, so the rotor must run faster, I estimate about 7.9 rpm and about 13 % less power. This is the best case quoted everywhere (267 mW, 106 mW). Linked: the 8 m/s offset (9.07 rpm) is blamed on the ramp although the rotor is above the kink, and chapter 6 switches silently from 9.16 to 9.07 rpm (29.6 vs 29.9 N m s, 202 vs 201 mW).
2. **The wrong reason for the low load power in chapter 7.** "The motor brakes only 0.39 to 0.43 of the best brake ... which is why the second blade ... gives less." By the notes' own formula the arm sees 0.88 to 0.97 of the best brake, and the rotor pays 271 mW against P* = 268 mW. The loss is in the chain, not in the brake.
3. **The sizing criterion contradicts Table 4.** The notes say they size for "the most power" and pick 1 kg; Table 4 shows 2 kg gives 133 mW against 74 mW at 8 m/s. The 1 kg choice maximises the share, not the power.
4. **The chapter 4 ceiling does not cover the case that matters, and chapter 6 compares unlike things.** The bound is for white noise; the blade shakes narrow-band. "More than gravity at 100 mm" (0.6, 6.2, 8.2) compares a brake 15 times weaker with gravity's best; at that brake gravity gives only about 26 mW, and no combined figure is given.
5. **Arithmetic that does not add up as written** (3.1): +1.43 %, +0.59 % and −0.90 % "together" make −0.31 % only because the third already contains the first. Also in chapter 3 the force line "from the hub" that "misses the hub", and the friction share in 7.4 (14–15 % stated, 25–27 % from (7.7)).

## Does the chapter order work?
Chapters 0 to 3 work well: picture, model, linear answer, check by full solution. Chapter 4 breaks the flow. It is a general theorem about a hinge shaken by white noise with no rotor, and its own last paragraph says it does not apply to the blade's real shaking. It would sit better as an appendix, or after chapter 6 as a remark. Chapter 7 (from swing to watts) is the practical heart and could follow chapter 3 directly, with gusts (5) and bending (6) as corrections afterwards. Section 8.1 (the gravity-power ceiling) explains why the power is small and belongs at the end of chapter 2. Suggested: 0, 1, 2 (+ 8.1), 3, 7, 5, 6, 8; chapter 4 as an appendix.

## Where I stopped caring
At the end of chapter 4, when the chapter itself says the ceiling does not cover the blade's real, narrow-band shaking. I had worked through a Cauchy–Schwarz proof for a result that then does not bound the case at hand. My attention came back in chapter 7 (real parts, real numbers), and faded again at Table 5 in 7.6: sixteen rows to make three points, after Table 4 had already confused me about the sizing.

## Symbols and words that mean two things

| Symbol or word | Meaning 1 | Meaning 2 (and more) |
|---|---|---|
| $a$ | slowing fraction at the rotor disc (0.2) | car's acceleration (1.1) |
| $A$ | rotor disc area (0.1) | complex swing amplitude (2.2) |
| $R$ | centrifugal stiffness $3r_p/2l$ (1.6) | $R_c$, $R_L$ coil and load resistance (1.4, 7.1) |
| $k$ | torque-law constant $Q_{\rm gen} = k\Omega^2$ (5) | gear-loss factor $\eta^{\pm1}$ in (7.8); also inside $k_e$, $k_t$ |
| $T$ | kinetic energy (1.7) | $T_0$ friction torque (7.2); torques are otherwise $\tau$ or $Q$ |
| $Q$ | generalised force $Q_k$ (4.1) | rotor torques $Q_{\rm aero}$, $Q_{\rm gen}$ (5) |
| $J$ | motor rotor inertia (7.2) | $J_{\rm rot}$ turbine rotor inertia (5); $j$ inertia ratio (7.3) |
| $L$ | lift (0.3) | length of a lumped rod (1.5); $L_c$ inductance (7.1); $\mathcal L$ Lagrangian |
| $\delta$ | lag of the swing (2.2) | Dirac delta (4.1) (the notes flag this one) |
| $s$ | distance along the second blade (1.3) | relative spread of the rotor speed (5) |
| $S$ | white-noise strength (4) | (close to $s$ above) |
| $x$ | ground coordinate (1.3) | ratio $\kappa/\kappa^*$ (Fig. 6); torque on the motor side (7.8) |
| $f$ | friction number (7.4) | frequency in Hz (used in words throughout) |
| $e$ | back-EMF (7.1) | unit vectors $\hat{\mathbf e}$ (1.3, 4.1) |
| $M$ | mass matrix $\mathsf M$ (4.1) | body mass $M$ in $Ml_c$ (1.5, 3.3); modal mass (6.2) |
| $\Omega$ | rotor speed, scalar | vector $\boldsymbol\Omega$ along the shaft (1.3) |
| $v$ | wind speed | velocity relative to the turning frame (1.3, Coriolis) |
| $\lambda$ / $\Lambda$ | tip-speed ratio | Lyapunov exponent (visually close) |
| $\theta$ / $\Theta$ | swing angle | swing amplitude |
| $c$ | hinge brake constant | $c_e$, $c_{\rm sc}$, $c^*$ variants; best brake for shaking (6.2) vs for gravity |
| "brake" | the hinge generator's damping $c$ | the main generator braking the shaft (0.3); tip brakes of old turbines (0.5) |
| "generator" | the small one in the hinge | the turbine's main generator (the notes flag this once in 0.5) |
| "blade" | the mother blade | the second blade; "On our blade" box vs "On our turbine" box |
| "stiffness" | centrifugal spring $R$ | the blade's bending stiffness (6.1) |
| "push" | gravity's once-per-turn torque | the air's push on the arm (0.7, 8.2); the wind's push on the rotor |
| "best brake" | κ* = R − 1 for gravity | the best brake for blade shaking (6.2), 15 times weaker |
| "frequency 1" | once per rotor turn (dimensionless, 2.2) | Hz elsewhere (1.48 Hz, 1.08 Hz) |
| "turn" | one rotor revolution | one turn of the motor shaft through the gearbox (7.1) |

# Learner read 2: "A Second Blade on a Turning Blade"

Reader: BSc physics (computational/theoretical). Knows Lagrangians, ODEs, Fourier, numerics. Knows nothing about turbines, generators, gearboxes, turbulence spectra, blade structures.
Source read: `notes/rotor-pendula/teaching/notes_as_read_2.md` only. Arithmetic checked in a Python scratch session under /tmp.

(Work in progress: chapters are added as they are read.)

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

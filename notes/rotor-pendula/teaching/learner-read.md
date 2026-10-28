# Learner read: "A second blade on a turning blade" (chapters 0 to 8)

Reader: BSc physics, computational and theoretical. I know Lagrangians, ODEs, Fourier analysis and numerics. I know nothing about wind turbines, generators, gearboxes, turbulence spectra or blade structures.
Text: `notes_as_read.md`. I saw figures and tables only as their captions.
Labels: **LOST** means I could not follow or check it. **SLOWED** means I followed, at a cost. **ANNOYED** means filler, repetition, hedging or talk about how the notes were made.
Quotes are exact, at most 25 words. Where I say "I computed", I did the arithmetic from the notes' own numbers.

First quick pass, in four lines. The core is clean mechanics that I enjoyed: chapters 1 to 3 and section 8.1. A rod sits in a rotating frame and gravity drives it once per turn. The best brake equals the net stiffness, the power is about (ml/2)g²/(4 v_tip), and the rotor pays through a small trail. Around that core: an aerodynamic opening with an error in its first derivation; two holes (section 3.4 has no text, and section 7.3 stops mid-sentence); chapters 4 to 6 on questions whose key inputs are missing; and an admission, in 0.7 and 8.2, that the air the notes leave out may be the strongest force of all.

Rendering artefacts I saw as a reader: "Part IA second blade on a turning blade", "Part IIRandomness", "Ours adds 0.0912 kN.For the sensor", and section 7.3 cut off after "only if $4f/\pi" (see chapter 7).

---

## Chapter 0. From scratch: the wind, the turbine, and the question

### 1. Lost

- **LOST** "It is zero with no slowing ($a = 0$) and zero again when the wake would stop dead ($a = \tfrac12$)." This is wrong. $C_p(\tfrac12) = 4\cdot\tfrac12\cdot\tfrac14 = \tfrac12$. The zeros of $4a(1-a)^2$ are at $a = 0$ and $a = 1$. The Check box repeats the error: "$a = \tfrac12$ gives $v_{\rm w} = 0$ and again $P = 0$ (the wake stands still)". So the Picture just above, "A turbine that stops the wind gets nothing; one that does not slow it gets nothing either", is tied to the wrong value of $a$. What I needed: the model holds only up to $a = \tfrac12$, because beyond that the wake would flow backwards; "stops the wind" is $a \to 1$, outside the model. This is the first derivation and the first Check box in the notes. After it I stopped trusting the Check boxes.
- **LOST** "The wind comes at it from the front at $v(1-a)$, slowed at the rotor as section 0.2 found." Figure 1 then says "so it meets air coming at it from the front at that speed". Here "front" means two directions at right angles: the upwind side of the rotor, and the blade's direction of motion. I had to draw it to see which was which.
- **LOST** "the tip-speed ratio $\lambda = \Omega r_{\rm rot}/v$, for which a given rotor takes the most". $r_{\rm rot}$ appears here for the first time but is defined only in 0.7. I could guess it. The definition of $\lambda$ also comes at the end of a 70-word sentence.
- **LOST** "reaches $C_p = 0.482$ at its best, 81 % of the limit: at 6, 8 and 10 m/s it delivers 0.80, 1.88 and 3.68 MW." Why is it called a 5 MW turbine if it gives 3.68 MW in the strongest wind of the notes? When does it reach 5 MW, and what happens in stronger wind? Why do the notes stop at 10 m/s? Is 8 m/s a breeze or a gale? Does "delivers" mean at the shaft or to the grid? None of this is said.
- **LOST** "its controller holds the rotor near that ratio in moderate wind by adjusting the generator's braking torque." "Controller" and "moderate wind" are not defined, and what happens in strong wind is never said. This is also the first time I learn the turbine has a generator of its own. From chapter 1 on, "the generator" means the small one in the hinge (see chapter 5).
- **LOST** "Everything the rest of these notes uses comes from this chapter so far". That is not true. Chapters 5 and 6 also use the rotor's inertia, the controller's torque law, a turbulence model, the blade's stiffness tables and its edgewise frequency. Also, the heading of 0.4, "What the blade is, and what our question needs from it", comes before any question has been asked; the question arrives in 0.5.
- **LOST** "The wheel presses everything outwards, so the ruler lies along the spoke, pointing away from the hub." On every Ferris wheel I have ridden, the outward push is tiny: the wheel takes minutes per turn, so the ruler hangs straight down. The Picture contradicts my experience at the exact point where it should build intuition. Section 1.1 then says "a fast Ferris wheel", which does not exist. What I needed: something that turns fast in a vertical plane, such as a bucket of water swung over your head or a ball whirled on a string in a vertical circle. Or simply say that Γ = 3 to 9 here, so the outward pull is 3 to 9 times gravity, while on a Ferris wheel it is about a hundredth of it.
- **LOST** "needs about 37.6 µW, from the typical currents of the two datasheets (section 8.3)". Section 8.3 is the list of sources. The 37.6 µW is not calculated anywhere in the text, so I cannot check it. "ADXL362" and "CC2652R" mean nothing to me. What I needed was something like "an accelerometer drawing X µA at Y V, plus a radio burst of Z µJ once a second".
- **LOST** "1 522 times the sensor's need or more". That is four significant figures on a ratio whose denominator, by the sentence before, "leaves out the radio's start-up and receive windows and the losses of a power converter". How large are those? Could they be a factor of ten?
- **LOST** "The wind's randomness. Mostly it does not help. Random shaking of white-noise type has a hard ceiling that no motion, chaotic or not, can beat". A ceiling of what size? No number is given here or in chapter 4. Two sentences later the shaking gives "more than gravity gives at 100 mm, a level no source we found confirms". So the honest summary is "unknown". "Mostly it does not help" claims more than the notes show.
- **LOST** "a battery 60 m out along a blade cannot be changed without stopping the turbine and sending a technician up a rope." The sensor needs 37.6 µW. I computed that this comes to about 24 kJ over twenty years: a few primary cells. The notes never compare harvesting with a battery sized for the turbine's life, so I could not see why the machine is needed. There may be good reasons (cold, self-discharge, lightning, the omitted radio costs). I wanted one sentence.
- **LOST** "The left view is not to scale here; the simulation draws it to scale" (Figure 2), and "The drawing of the simulation gives it a blade's tapered outline" (0.7). What simulation? It is never introduced. It comes back in 1.4 ("the simulation's data log") and in Figure 6 ("the simulation's own engine").
- **LOST** Why is the harvester a *blade*? The text says "The second blade is a thin uniform rod" (0.7), "A real blade is far larger than that" (0.7), and "a blade shaped for the air is the opposite" (3.3). These suggest it has a second job besides harvesting, but that job is never stated. Without it, "second blade" is just a confusing name for a pendulum.
- **LOST** "A real blade is far larger than that, so air would shape its motion at least as strongly as gravity does." This tells me the model leaves out what may be its largest force, and it is tucked into "Where the numbers come from". The argument also compares a pressure times an area with the weight. But a steady air force would make a steady lean, not a once-per-turn push. What matters for the harvest is the part of the air force that changes once per turn, and the notes do not say whether that part is large. So I can neither trust the warning nor set it aside.
- **LOST** "solved by a stiff integrator checked against an independent solver". "Stiff" is explained only in 3.1.
- **LOST** (minor) "The turbine is the NREL 5 MW reference turbine". NREL is never spelled out.

### 2. Slowed

- **SLOWED** "the force on the disc, the thrust, is $F = \dot m\,(v - v_{\rm w})$". The pressure on the sides of the stream tube is silently dropped; one sentence would let a physicist accept the step. This is also the derivation that most needs a figure (the stream tube, narrow upwind and wide downwind), and there is none.
- **SLOWED** "Why does the tip move so much faster than the wind?" The answer is a story: "the blades sweep the whole disc often enough to slow all of its air by the right third". It does not say why the best ratio is 7.55 and not 2. It also seems to fight the paragraph before it: a faster tip means a smaller $\phi$, so the lift leans forward less and the lift-to-drag condition gets harder. I needed that tension named and resolved, or a plot of $C_p(\lambda)$. Chapter 5 uses $C_p(\lambda)$ but never shows it.
- **SLOWED** "The rotor takes power as torque times $\Omega$." This is stated and then not used in the argument that follows.
- **SLOWED** Sections 0.2 and 0.3 together are two pages of aerodynamics (Betz, lift, apparent wind). The rest of the notes uses only $\lambda^* = 7.55$, plus $C_p$ for one share. I would have taken "the turbine's controller keeps the tip moving at 7.55 times the wind speed", one Picture, and Figure 1.
- **SLOWED** Order: 0.4 (what the blade is) comes before 0.5 (the sensor and the idea). Start with the sensor and the idea; then give the turbine facts the idea needs.
- **SLOWED** "between 161 and 267 mW of mechanical power from the swing, at steady winds of 10 and 6 m/s". Less power in more wind is the most surprising fact in the notes, and here it goes by without a hint of why. One clause would hook me: "because a faster rotor makes a stiffer centrifugal spring".
- **SLOWED** "The turbine's own power, for the share quoted above". Which share? I think the 0.34 parts per million of 0.6.
- **SLOWED** Figure 2 is an "[SVG DRAWING]" with a caption. I cannot tell which way the shaft points relative to the wind or the ground, or where the hinge axis is. A labelled sketch of the whole machine (hub, shaft, rotor plane, blade, tip, hinge axis, wind direction) is the figure I most needed in this chapter.

### 3. Annoyed

- **ANNOYED** 0.7 repeats 0.3 almost word for word: "Its blade tip moves about 7.55 times faster than the wind when it works best". It also repeats the formula for the turbine's power from 0.1 and 0.2.
- **ANNOYED** "and the results are put into the text by a script" (0.7); "a script checks every number in the text" (0.8). This is about how the notes were produced, not about physics.
- **ANNOYED** Boxes are named "[On our turbine]" here, but 0.8 describes "On our blade" boxes. Minor.
- **ANNOYED / LOST** The Conventions box uses $\varphi$ for the rotor's angle right after 0.3 used $\phi$ for the angle of the apparent wind. Two different Greek phis for two different angles is a trap in print (see the symbol list at the end).

### 4. What I understood

Wind carries the power ½ρAv³, a turbine can take at most 16/27 of it, and the blade tip moves about 7.5 times faster than the wind, so it lives in a fast, nearly head-on stream of air. The idea is to hang a small hinged blade at the tip: as the rotor turns, gravity rocks it once per turn as seen from the blade, and a generator in the hinge brakes that rocking to power a sensor. The promised answer is about 0.2 W mechanical and 0.1 W electrical against a sensor need of about 40 µW, but the air, which the notes leave out, may change everything.

### 5. The one thing that would most help

Open with the sensor and the idea (0.5), using a fast-turning everyday picture that is physically right and one sentence on why a battery will not do. Cut 0.2 and 0.3 down to the one fact used later ($\lambda^* = 7.55$, held by the controller). If the Betz derivation stays, fix $a = \tfrac12$.

---

## Chapter 1. Sitting at the tip

### 1. Lost

- **LOST** "behaves like a weathervane in that apparent wind". In 0.3, "apparent wind" meant the real air meeting the blade. Here it means apparent gravity, the sum of the outward pull and gravity. The notes leave the air out, so for a moment I thought the air was back in the model. The right picture is a plumb line, not a weathervane.
- **LOST** "tilts to one side, then to the other, once per turn, by up to $\arcsin(1/\Gamma)$". My first guess was $\arctan(1/\Gamma)$, which is the tilt when gravity is exactly across the blade. The arcsin is the largest angle between a fixed arrow of length Γ and its sum with a turning arrow of length 1. That maximum comes when gravity is at right angles to the *sum*, not to the blade. This step is skipped. Section 1.6 states the result again ("where $\sin\varphi = 1/\Gamma$"), still without the step.
- **LOST** "the torque the rotor needs (section 1.4) then becomes $mgr_p\cos\varphi$". Section 1.4 never writes out the rotor's torque; it gives only the Lagrange expression. The explicit form first appears in 3.2 ("$-\tfrac{ml}{2}r_p\Omega^2\sin\theta + mgr_p\cos\varphi$ plus terms that are exact time derivatives"), and the derivation is skipped there too. So I could not check this limit at the point where it is offered.
- **LOST** "Its own share is the term $mgr_p\cos\varphi$", followed by "the simulation's data log shows it as the large swing of the rotor's work against the energy lifted". Whose "own share"? The lifting's, I think. Which simulation, which data log? "Large" compared with what? A number would settle it. I computed a peak of $mgr_p \approx 620$ N m for lifting the blade, against a harvesting torque of about 0.37 N m at 6 m/s (from the trail in 3.2).
- **LOST** "a push in step with the motion it drives does no net work over a cycle". To a physicist, "in step with the motion" is ambiguous: a push in step with the *velocity* does the most work. The intended meaning is in step with the *displacement*. The hand-on-a-swing picture rescues it, but the sentence as written stopped me.
- **LOST** "the stiffness $R$ plus gravity's own stiffening of section 2.1". This is a forward reference inside a chapter 1 Check box.
- **LOST** The key argument of the chapter is in a caption. Figure 3 says "Split each piece's centrifugal pull in two" ... "that is the centrifugal spring". That split (the part along the second blade has no lever arm; what is left is a uniform $\Omega^2 r_p$ along the mother blade) is the clearest physical explanation in the chapter. I cannot see the drawing, and many readers skip captions. It belongs in the text.

### 2. Slowed

- **SLOWED** Order. Section 1.3 (the Lagrangian in the ground frame, about two pages) comes before 1.6 (the turning frame, "in four lines", with the bowl picture). For a reader who learns from pictures first, 1.6 is the derivation and 1.3 is the check. As it stands I did the algebra twice and met the picture last.
- **SLOWED** "its torque acts between the mother blade and the second blade, inside the pair, and the rotor drives the pair." This is right, but I had to convince myself: the brake does no virtual work when φ changes with θ held fixed. One clause would do it.
- **SLOWED** "a free small swing makes $\sqrt R$ oscillations per rotor turn". This is true without a brake. With the best brake of chapter 2 (κ* = 93.5, R = 94.5), I computed the damping ratio as κ/(2√R) ≈ 4.8. The second blade is then heavily overdamped and does not oscillate at all. The notes never say this. It changes the picture: the second blade does not ring on its own; it creeps after the moving bottom of the bowl, which is exactly the marble in honey. Say it, here or in chapter 2.
- **SLOWED** "seen from the ground, it only steers energy that the rotor supplies." "Steers" is the word I could not picture. The explanation (the trail and the off-centre pull on the hinge) waits until 3.2. A two-line preview here would have helped.
- **SLOWED** I needed a vector diagram of apparent gravity: a fixed outward arrow of length Γ plus a unit arrow turning once per turn. It would make arcsin(1/Γ) obvious. Figure 4's caption describes the bowl but not this.
- **SLOWED** No warm-up exercise. A three-line worked example ("at 8 m/s: Ω = …, Γ = …, tilt = …") would have let me do one by hand before trusting the tables.

### 3. Annoyed

- **ANNOYED** The Coriolis "no lever arm" argument appears three times (1.1, 1.6, 8.1), and the Euler force sentence twice (1.1, 1.6).
- **ANNOYED** "the two results agree identically" (1.3 Check), then "SymPy confirms it the long way" (1.4), then "checked symbolically in SymPy" (2.3), "done in SymPy" (6.1), "derived in SymPy" (6.2), "checked in SymPy" (4.1, 4.2). Saying it once is useful. By the fourth time it reads as reassurance, not content.

### 4. What I understood

Seen from the mother blade, the second blade sits in a bowl made by the outward pull, with stiffness R ≈ 94, so its own frequency is about ten times the rotation rate. Gravity, turning once per turn, tilts the bowl by up to ±17.5° at 6 m/s. The generator makes the blade lag behind the moving bottom; the lag lets gravity's push do net work, and the generator takes it. Seen from the ground, the same energy comes from the rotor: over one turn, the rotor's work equals the generator's take.

### 5. The one thing that would most help

Lead with 1.6 (the bowl in the turning frame, with the decomposition now hidden in Figure 3's caption). Then give the rotor's torques in newton-metres, so that "the rotor pays" has a size: hundreds of N m swinging to and fro, against a fraction of a N m that pays for the harvest.

---

## Chapter 2. The best brake, and how much it gives

This is the best chapter. The model, the mathematics and the meaning arrive together, and I could redo every line.

### 1. Lost

- **LOST** "We drop it anyway, for a reason that has nothing to do with its size", followed by "Its effect enters only at second order". The dropped term $-G\theta\sin\varphi$ is *linear* in θ, so "small swings" does not justify dropping it. And second order in what: the swing Θ, or 1/Γ (0.30 at 6 m/s)? What I needed: the term moves the blade at frequencies 0 and 2, and those motions feed back at frequency 1 only through the same term again, so its effect goes as $(G/R)^2$. My own harmonic-balance estimate is +1.4 % of power at 6 m/s, 0.4 % at 8 m/s and 0.2 % at 10 m/s at the best brake, and the flat top of Figure 5 hides most of that. Two sentences like these would have convinced me. As written, "nothing to do with its size" and "only at second order" pull in opposite directions.
- **LOST** "The error must therefore grow as $\Theta^2$, and it does." (2.4) At a fixed ratio κ/κ*, Θ is proportional to G, so across the three winds "∝ Θ²" and "∝ G²" are the same test. That test cannot tell the dropped linear term from the true nonlinear terms ($\theta^3$, $\theta^2\cos\varphi$), so the "fingerprint" argument proves less than it claims.
- **LOST** "The weight simply follows your hand, a little late." But 2.2 says "With no brake ($\kappa = 0$) the second blade follows the push exactly in step". Without honey there is no lateness, so the Picture and the text disagree.
- **LOST** "Equation (2.7) alone, with $v_{\rm tip}$ in place of $\Omega r_p$, gives 265.4, 199.0 and 159.2 mW". By definition $v_{\rm tip} = \Omega r_p$, so "in place of" says nothing. What actually differs from (2.5) is that $I$ is dropped (the $\tfrac23 l$).
- **LOST** The values of (2.5) itself never appear in the prose; they are only in Table 1, which I do not have. I computed 268, 201 and 161 mW. Section 0.6 says "between 161 and 267 mW". Is 267 the full model and 161 the formula? Which number is quoted where?
- **LOST** "the full swing is lowered as a whole, by −0.024 rad on average". In 3.2, "the full model gives −0.0231 rad" for what I take to be the same quantity: the mean trail at the best brake at 6 m/s. Two numbers for one thing. "Lowered ... by −0.024" is also a double negative.
- **LOST** (minor) "Two ways of softening it exist on paper, tilting the hinge out of the rotor plane". Why tilting would soften the spring is not said.

### 2. Slowed

- **SLOWED** The first paragraph of 2.4 is one sentence listing table columns, with a 50-word parenthesis inside: "gravity's number $G$ ($R$ and the best brake $\kappa^* = R - 1$ are the same at every wind: ...)". I read it three times. Put the parenthesis in its own sentence, or drop it, since 2.3 already said it.
- **SLOWED** Second consequence: $c^*$ is given only as a formula. The number (22.4 to 37.4 N m s) first appears in 7.1, five chapters later. I wanted it here.
- **SLOWED** I needed a phasor diagram of the three torques at the best brake: gravity's push; the net stiffness (spring minus inertia); and the brake at 90° to the net stiffness, equal in size. The τ* paragraph describes this picture in words.
- **SLOWED** A physical picture is missing: what the swing looks like. At 6 m/s, Θ* = 0.215 rad, so the tip of a 1 m second blade moves about ±21 cm, once per 8.7 s turn. At 10 m/s it moves about ±8 cm per 5.2 s. It is a slow, gentle sway, heavily overdamped (damping ratio about 4.8, see chapter 1). I worked this out myself; one sentence would give it to every reader.
- **SLOWED** The AC-circuit Picture works for me. For a school reader it is not something to feel with hands and eyes: it needs reactance, $\omega L_{\rm coil}$. It also brings in yet another $L$.
- **SLOWED** No worked example. Table 1 is invisible to me, so a paragraph doing one wind by hand would have been my main check: "8 m/s, 1 kg, 1 m: Ω = 0.959 rad/s, R = 94.5, G = 16.0, κ* = 93.5, Θ* = 0.121 rad, c* = 29.6 N m s, τ* = 3.47 N m, P* = 201 mW".

### 3. Annoyed

- **ANNOYED** "Three consequences are worth a second look." This is filler; just list the three.
- **ANNOYED** "solved by the simulation's own engine ( tools/compare.js )". A file path does not belong in a lecture note.
- **ANNOYED** "The closed form (2.5) is within 0.31 % of the full model at every wind." The same sentence appears word for word in 3.1.

### 4. What I understood

For small swings, the second blade is a stiff oscillator (own frequency about 9.7 times per turn) pushed once per turn by gravity with strength G. The best brake equals the net stiffness R − 1, and it makes the swing lag the push by 45°. The power is then $P^* \approx \tfrac{ml}{2}g^2/(4v_{\rm tip})$: proportional to the first moment and inversely proportional to the hinge's speed, so it is larger in light wind (about 0.27 W at 6 m/s and 0.16 W at 10 m/s for 1 kg on 1 m). The generator must hold a torque of $\tfrac{ml}{2}g/\sqrt2 \approx 3.5$ N m at every wind.

### 5. The one thing that would most help

One worked example in prose at 8 m/s, from rpm to milliwatts, with the size and period of the swing. Then the explanation of the dropped term in two honest sentences.

---

## Chapter 3. Big swings, the bill, and chaos

### 1. Lost

- **LOST (the largest gap in the notes)** Section 3.4, "Chaos and the harvest", is a table caption and nothing else. The chapter title promises chaos. The introduction promises "whether chaos can help". Section 8.2 concludes "the motion is regular at every wind and brake tried (chapters 2 and 3)". In the text I read, not one sentence supports that conclusion. The caption's "the largest over the starts" is undefined (starts meaning initial conditions?), and the caption's $s$ is a third meaning of that letter.
- **LOST** "at the best brake a disturbance of the swing dies in $1/(\kappa^*\Omega)$, 0.011 s at 8 m/s". That is only the fast root of $s^2 + \kappa s + R = 0$. The slow root is about $R/\kappa \approx 1$ per radian of rotor angle, which I computed as about 1 s at 8 m/s. The slow root sets how a displaced swing comes back. Table 2's caption ("$2\pi\,\max\,\mathrm{Re}\,s$") uses that slow root. Which one does "a disturbance of the swing" mean? Both matter: the fast one for the step size, the slow one for the physics.
- **LOST** "its torques agree with Newton's law summed over the second blade to 4·10⁻¹⁵". Whose torques? An integrator has no torques. I think it means the model's right-hand side, checked against a direct Newton sum.
- **LOST** "Two reasons make the agreement plausible." The reasons given are that three second-order effects "partly cancel", followed at once by "These notes have not measured the three separately; the full model shows only their sum." So the cancellation is a guess presented as a reason. The same integrator could switch each term off in a minute.
- **LOST** "Keep the gravity term to second order, $G\cos(\varphi+\theta) \approx G\cos\varphi - G\theta\sin\varphi$". As written, that is the *first*-order Taylor expansion. Second order in what? I think it means that $G\theta$ is second order in G because θ is itself of order G. Say so.
- **LOST** "plus terms that are exact time derivatives". The rotor's torque is never derived. I did it myself: use (1.3) to replace gravity's torque on the second blade. It works. But it is not obvious that the generator's $c\dot\theta$ is one of those exact derivatives ($d(c\theta)/dt$), and that is the step a reader trips on.
- **LOST** Sign. The rotor's torque contains "$-\tfrac{ml}{2}r_p\Omega^2\sin\theta$", and the next sentences say "Worked out, its torque is $\tfrac{ml}{2}r_p\Omega^2\sin\theta$, the term in the rotor's torque above." The same term appears with opposite signs a few lines apart. The reason (one is the pull on the rotor, the other is the rotor pushing against it) is left to me.
- **LOST** "a blade shaped for the air is the opposite". Why would the second blade be shaped for the air at all? Its job other than harvesting is never stated (see chapter 0).
- **LOST** (minor) "although the second blade swings up to 0.214 rad (12.2°)" here, but "its size, 0.215 rad at 6 m/s" in 2.4.

### 2. Slowed

- **SLOWED** The numerics paragraph of 3.1. The computational part of me liked "Radau IIA, fifth order, error falls 5.2 powers of two per halving". But the parenthesis that follows is a lab-notebook entry, and "the brake's relaxation is shorter than one step of 240 per turn" does not parse on first reading ("one step, when a turn takes 240 steps").
- **SLOWED** Honey stands for the generator three times, for three different points: the lag (1.6), the extra lag of a driven spring (2.1), and stiffness (3.1). By the third time the picture had stopped adding anything.
- **SLOWED** Section 3.2 has the best idea in the notes: "The trail is the bill." The picture of the off-centre pull on the hinge is right. But two things are missing. First, a figure: hub, hinge, centre of mass slightly behind the mother blade's line, the pull arrow and its lever arm $r_p\sin(\cdot)$. Second, the number: I computed the rotor's extra torque at 6 m/s as about 0.37 N m, against the turbine's own torque of about 1.1 MN m (0.80 MW at 0.719 rad/s). That one comparison says "the rotor pays, and does not notice".
- **SLOWED** A trail of "1.31°" is given only at 6 m/s. From (3.2) I get about 0.4° at 8 m/s and 0.2° at 10 m/s. Saying so would show that the bill shrinks quickly as the wind rises.

### 3. Annoyed

- **ANNOYED** "The closed form (2.5) is within 0.31 % of the full model at every wind" is repeated from 2.4.
- **ANNOYED** "These notes have not measured the three separately; the full model shows only their sum." This is a hedge where a measurement was cheap.

### 4. What I understood

The full equation confirms the small-swing formula to 0.3 % at the best brake. On average the second blade trails slightly behind the mother blade (1.3° at 6 m/s). Its outward pull on the hinge then has a lever arm about the hub and holds the rotor back, and that torque times Ω is exactly the harvested power: the trail is the bill. A blade with its mass at the tip gives twice what a uniform one gives. About chaos I can say nothing, because the section has no text.

### 5. The one thing that would most help

Write section 3.4: what the Lyapunov exponents are, what they show, in two or three sentences with the numbers. Then the claim in 8.2 has something to rest on.

---

## Chapter 4. A ceiling on random shaking

The mathematics here is clean and I enjoyed it. My trouble is what it is for.

### 1. Lost

- **LOST** "Could the second blade, perhaps moving chaotically, turn that randomness into extra power?" Why would anyone expect chaos to help harvest? Is it a claim from the literature, or a popular belief about chaotic pendulum harvesters? Without that motivation, the chapter answers a question I did not have.
- **LOST** There is no value of $S$ for the turbine anywhere in the notes. So (4.4) is a ceiling with no number, and I cannot compare it with gravity's 0.2 W, which was the point of the chapter. Then the chapter's last paragraph says "A real blade, though, does not shake as white noise", so the theorem does not even apply to the case that matters. Yet 0.6 and 8.2 use this chapter to say that randomness "mostly does not help". In the text I read, that conclusion has no support.
- **LOST** "about 1.08 Hz on the 5 MW reference turbine of chapter 5". The turbine was introduced in chapter 0, and chapter 5 comes after this one.
- **LOST** "The mother blade's edgewise shaking, in the rotor plane and across the mother blade". This is the first time "edgewise" appears. The other bending direction (out of the rotor plane) is never named, and the notes never say why it can be ignored. I worked it out: that motion is along the hinge axis, so it has no torque about the hinge. One sentence would save every reader that detour.
- **LOST** (wording) "A uniform blade can give the shaking at most three quarters of its mass". This reads backwards. It means the shaking can grab at most three quarters of the mass.

### 2. Slowed

- **SLOWED** The Check box tests "a bob of 0.1 kg on 0.2 m and a double pendulum", "made for an earlier version of this study". That is a different system from ours. I wanted the same test on the uniform rod at its hinge.
- **SLOWED** The parenthesis about where in each step the kick is evaluated is the Itô versus Stratonovich question. Name it: a computational physicist will look for the word, and it is the right one here.
- **SLOWED** Symbols clash with earlier chapters. $a(t)$ is the shaking acceleration here but the slowing fraction in 0.2. $A(q)$ is the mass matrix here but an area in 0.1 and a complex amplitude in 2.2. δ is the Dirac delta here but the lag in 2.2. Each is survivable alone; together they cost me re-reads.

### 3. Annoyed

- **ANNOYED** "made for an earlier version of this study". This is the history of the project, not physics.
- **ANNOYED** None for the prose. The signpost "readers who skip them lose nothing but the proof" is a model of how to treat a reader.

### 4. What I understood

White-noise shaking of the pivot feeds in, on average, S/2 times an effective mass. The effective mass never exceeds the body's real mass (three quarters of it for a uniform rod), whatever the motion does, regular or chaotic, because only the square of each random kick adds energy on average. I cannot say whether this matters for our machine: the notes give no S for the blade, and then say the blade does not shake as white noise.

### 5. The one thing that would most help

Give the S (or its equivalent) at the tip of the real blade and the resulting ceiling in milliwatts, next to gravity's 200 mW. Otherwise cut the chapter to a one-paragraph box, "a theorem that rules out chaos as a free lunch", and send the reader on to chapter 6.

---

## Chapter 5. Gusts and the rotor's speed

### 1. Lost

- **LOST** "(IEC 61400-1, edition 3, turbulence class A, as implemented in NREL's TurbSim)" and "with the Kaimal spectrum, mostly over tens of seconds". Four names, no physics. What I needed, in words: a standard design wind whose speed wanders by about 23 % of its mean, mostly slowly (over tens of seconds to minutes), with less and less power in faster wiggles. Ideally with the spectrum's shape as a formula or a plot. Is 1.86 m/s at 8 m/s typical of a real site, or a severe design case? Not said.
- **LOST** "against the generator's torque, which the controller sets as a function of $\Omega$". The "torque law" is never shown or explained. Later the text mentions "a pure square-law controller ($Q_{\rm gen} \propto \Omega^2$)" and "a kink in its torque law, at 8.98 rpm", still without the law. Why does a square law hold the tip-speed ratio? I worked it out: at a fixed λ, $Q_{\rm aero} \propto \Omega^2$. Why is there a kink, and what is "the full controller"? I had no picture of it.
- **LOST** "With the generator constant fixed", a paragraph after "the generator's torque, which the controller sets". These are two different generators, the turbine's (megawatts) and the one in the hinge (milliwatts), both called "the generator" in the same chapter. I had to stop and work out which was meant each time.
- **LOST** "In 40 ten-minute records". Measured, or generated by the turbulence program? I assume generated, but it should say.
- **LOST** "both ride on the rotor's speed, so the two stay in step whatever the rotor does." Only R stays fixed. κ = c/(IΩ) and G = 3g/(2lΩ²) both change with Ω, and the next paragraph uses exactly that to get $2/(1+\Omega^2/\Omega_0^2)$. So the dimensionless system does *not* stay the same "whatever the rotor does". The sentence and the paragraph after it contradict each other.
- **LOST** An assumption is never stated. Taking the power at each moment to be the steady power at that moment's speed requires the second blade to settle (about 1 s) much faster than the gusts change the rotor's speed (tens of seconds). I believe it is true, but it is the whole basis of the "exactly" and it is not stated.
- **LOST** "$J = 4.38\times10^7$ kg m²" here, and "$J = 14.7$ g cm²" for the small motor in chapter 7. Same letter, fourteen orders of magnitude apart.
- **LOST** Only 8 m/s is studied. Nothing is said about 6 and 10 m/s, although the conclusion ("a few per cent at most") is stated for the wind in general.

### 2. Slowed

- **SLOWED** "$Q_{\rm aero} = \tfrac12\rho\pi r_{\rm rot}^3v^2C_p(\lambda)/\lambda$". One line is skipped: torque = power/Ω, with Ω = λv/r. Easy, but give it.
- **SLOWED** "the power coefficient $C_p(\lambda)$ from NREL's published table". The curve is never shown; I know only its peak, from 0.2.
- **SLOWED** The metronome Picture describes the opposite case: a metronome that does *not* ride on the train's speed. It then says ours is different, so I had to turn the picture inside out to use it.
- **SLOWED** I had no sense of how slowly the rotor answers a gust. I estimated that the rotor stores about 20 s of its own output ($J\Omega^2/P$ at 8 m/s). One sentence like that would explain why gusts become a slow wander of Ω, and why the Euler terms are negligible.
- **SLOWED** "Each of the 40 records is run twice through the full equation ..., once with the Euler terms and once without, and compared with steady rotation" at two different speeds. That is four runs per record compared in two ways, packed into one sentence. A four-line table would be clearer.
- **SLOWED** Missing figures: ten minutes of wind speed and rotor speed; the controller's torque law $Q_{\rm gen}(\Omega)$ with its kink; and the curve $2/(1+x^2)$ with the band that $x$ wanders over.

### 3. Annoyed

- **ANNOYED** "more than the 0.53 % the curvature alone predicts (these notes have not separated where the rest comes from)". After a result called "exactly", 0.37 percentage points are left unexplained with a shrug.
- **ANNOYED** Double negatives: "the power falls by −2.55 %", "costs −0.11 %". The same pattern appears in 2.4: "lowered ... by −0.024 rad".

### 4. What I understood

Gusts make the rotor's speed wander by about 10 %. With the hinge generator's constant fixed, the second blade's power goes as $2/(1+(\Omega/\Omega_0)^2)$. So a wander adds about $s^2/2 \approx 0.5$ %, and a shift of the mean speed by a fraction ε changes the power by −ε. With this turbine's real controller, the mean speed rises in gusty wind, so the net effect is −2 %. Either way, a few per cent.

### 5. The one thing that would most help

Replace the names with pictures: a ten-minute wind record, the controller's torque law with its kink, and one sentence on what that law does to the rotor's speed. Call the two generators by two different names.

---

## Chapter 6. The blade bends and shakes

### 1. Lost

- **LOST** "The hinge therefore moves sideways by $w\cos\varphi$." $w$ is never defined. I assume it is the sag at the tip, 431 to 467 mm. Is that an amplitude, or the total travel from one side to the other?
- **LOST** "gravity bends it edgewise by 431 to 467 mm at the tip, depending on how the bend's shape is taken". What "how the bend's shape is taken" means is explained only a paragraph later ("taking the shape from the blade's first mode of vibration, or integrating the static bend directly").
- **LOST** "the hinge's motion adds $2\Omega^2w$ to gravity's push $g$" ... "exactly as it would for a bob". The two-line derivation is replaced by "done in SymPy", and "as it would for a bob" does not help. I worked it out. The hinge's acceleration in the turning frame contributes $\Omega^2 w$. And moving the hinge sideways by $w$ turns the outward field by $w/r_p$, which contributes $\Omega^2 r_p\cdot w/r_p = \Omega^2 w$. Those two lines belong in the text.
- **LOST** "On its own that would raise the power by 16.9 to 18.4 %". At which wind? I get these numbers at 8 m/s.
- **LOST** "That drag follows the rate of change of the bend's slope, a quarter turn out of step with the sag's push". The phase argument ("so part of the drag works against the swing") needs a phasor sketch, and the sizes of the two competing torques are never given. I estimate both at about 0.4 N m at 8 m/s, against gravity's 4.9 N m. Saying that would make "largely cancel" believable.
- **LOST** "no source we could open says for this blade, so the notes take a range: a tip vibration of 5, 20 or 100 mm rms". Why these three? Is 100 mm plausible for a 61.5 m blade in the rotor plane, or absurd? The chapter's whole verdict rests on this unknown, and the range looks arbitrary.
- **LOST** "a modal mass of 1416 kg" and "with a damping ratio $\zeta_b$ of 0.5 % or 3 % of critical". "Modal mass" is not defined (the mass that, on a spring at the blade tip, would behave like the blade's mode?). Neither number has a stated source.
- **LOST** "The full linear equations, with the second blade integrated along its length and the turning frame's centrifugal and Coriolis terms, were derived in SymPy." They are not shown. This is the one model in the notes I could not rebuild from the text.
- **LOST** "takes 3.38 mW of it, against 202 mW from gravity". These are at two different brakes (1.89 and 29.6 N m s), right after I was told the two "cannot simply be added". What does a real device with one brake get from both together? Also, (2.5) gives 201 mW at 8 m/s. Where does 202 come from?
- **LOST** "needs $\Omega\sqrt{3r_p/(2l)} = \omega_e$". $\omega_e$ is used once and never defined. I assume it is 2π × 1.08 Hz.
- **LOST** "Chaos plays no part: at $R$ near 94 the second blade is held firmly along the mother blade." Supported by what? Section 3.4 has no text.

### 2. Slowed

- **SLOWED** The model paragraph of 6.2 is about 250 words and makes seven modelling choices. A sketch of the two coupled oscillators (the blade's mode, the second blade, and the brake between them) would carry most of it.
- **SLOWED** "its own frequency, $\sqrt R$ times the rotor's, is 1.36 times the blade's". "Own frequency" again, for a blade that is overdamped at gravity's best brake. At the shaking's best brake (1.89 N m s) I estimate a damping ratio of about 0.3, so here it really does oscillate. Say which regime each paragraph is in.

### 3. Annoyed

- **ANNOYED** "its true gain may be somewhat below these numbers or several times below them" and "The tuned second blade is an idea these notes have not shown to work". Then why give three-figure numbers for it (64.6, 85.1, 25.0 mW, "36 %", "59 %")? Either show that it works or cut it to one sentence saying it is an idea for later.
- **ANNOYED** "no source we could open". This is a diary of the writing, not a statement about the world. Either "no published value exists that we know of" or a value with its source.

### 4. What I understood

The blade sags about half a metre at its tip, once per turn and in step with gravity. That moves the hinge (on its own, about +17 % power) but also turns the generator's stator, which takes most of the gain back; the net change is +2 to +3.5 %. Random vibration of the blade in the rotor plane adds power that grows as the square of the tip amplitude: negligible at 5 mm, more than gravity gives at 100 mm, and nobody here knows the real amplitude. A 1.85 m second blade tuned to the blade's 1.08 Hz would act as a tuned mass damper, but gravity detunes it every turn, so whether it works is open.

### 5. The one thing that would most help

A number, with its source, for how much the tip of a real 60 m blade vibrates in the rotor plane. Without it, section 6.2 has no conclusion. If no such number exists, say so in one line and shorten the section to match.

---

## Chapter 7. From swing to watts

The pictures here (bicycle dynamo, egg beater, box on the floor) are the best set in the notes, and the describing function is explained well.

### 1. Lost

- **LOST (text missing)** "This is a quadratic equation for $\Theta$. It has a positive root only if $4f/\pi". The sentence breaks off, and the next thing on the page is equation (7.7). Three things are lost with it: the condition (presumably $4f/\pi < G$), the root Θ itself, and any word on what $P_{\rm load}$ and $P_{\rm rotor}$ in (7.7) are. This also leaves two jam conditions unreconciled. Section 7.2 says "If $f \ge G$ the friction is stronger than gravity can ever push", while the describing function suggests the swing dies already at $f \ge \pi G/4$. The lost text presumably explained the difference.
- **LOST** "while its hinge turns at most about a tenth of a radian per second". At 6 m/s the best swing gives ΩΘ* = 0.719 × 0.215 ≈ 0.155 rad/s, by the notes' own numbers. "At most" is wrong at the lightest wind.
- **LOST** "with the swing kept below 0.5 rad". Why 0.5 rad: a mechanical stop, the limit of the formula, the gearhead? No reason is given. The gearhead's continuous torque, which 7.5 says decides the size ("Beyond 2 kg the largest ratio would exceed the gearhead's continuous torque"), is never given as a number either.
- **LOST** "Even the poorest wind gives 1 522 times what the sensor of section 0.6 needs." "Poorest wind" means the *strongest* wind, 10 m/s, because the power falls as the wind rises. I read it the wrong way first.
- **LOST** "the motor's graphite brushes also have a contact voltage drop of their own, which these notes do not model". How large is it? If it is a fair fraction of the 0.80 V peak, the electrical result changes completely. I needed a number or a bound.
- **LOST** "and section 7.1 says the best brake grows with it too". That result is (2.6), in section 2.3. Section 7.1 only quotes it.
- **LOST (design logic)** "The share peaks at 1 kg, which is the mass these notes use." That is the peak of the share of $P^*$, not of the power delivered. Section 7.6 then says the motor delivers 93.9 to 107 mW "whatever the size" once the first moment passes about 0.5 kg m, and that even the smallest blade still gives the sensor "311 times its need". With margins of 300 to 1500, why is the goal "use this one 20 W catalogue motor fully"? Why not a much smaller motor and a lighter blade? "is chosen by the generator and the structure, not by the power". But the structure argument favours the smallest blade. For me the design logic did not close.
- **LOST** "the pivoting tip brakes of small stall-regulated turbines". "Stall-regulated" and "tip brake" are not defined. A hinged tip that already exists on real turbines is the closest real-world cousin of our machine. One sentence on what it does and why it pivots would have been the best everyday picture in the notes, and it would belong in chapter 0.
- **LOST** Tables 3, 4 and 5 carry the results; the prose gives only ranges. For Table 4, the shares themselves never appear in the text.

### 2. Slowed

- **SLOWED** "$k = \eta^{-\mathrm{sgn}(x\theta')}$". This is compact and correct. But $x$ is a torque here, while in Figure 5 $x = \kappa/\kappa^*$, and $k$ is a third use of that letter (after $k_e$ and $k_t$).
- **SLOWED** I needed a power-flow diagram: rotor → swing → gears → friction → coil → load, with the percentages that 7.4 gives in words ("35 to 39 % ... 14 to 15 % ... the gears and the coil take most of the rest"). I also needed the circuit (motor as a voltage source in series with $R_c$, then $R_L$).
- **SLOWED** The voltage paragraph gives "peaks at 0.80 to 1.39 V" and "at 0.114 to 0.191 Hz" without saying which end goes with which wind.

### 3. Annoyed

- **ANNOYED** "the formula's is the best or within 0.0 % of it". "Within 0.0 %" says nothing.
- **ANNOYED** "811 times" appears three times (7.4, 7.5, 8.2), and "1 522 times" three times (0.6, 7.4, 8.2), always with all its digits.
- **ANNOYED** "Ours adds 0.0912 kN.For the sensor". Write 91 N, and add the missing space.
- **ANNOYED** "(catalogue part 339152)" in the running text. This is fine in the sources, noise in a paragraph about physics.

### 4. What I understood

A small DC motor driven backwards is a brake with constant $N^2k_tk_e/(R_c+R_L)$. To reach the best brake, a 20 W motor needs a gear ratio of about 300 to 500. That brings three costs: extra inertia (negligible), friction (it acts like a brake that weakens as the swing grows), and gear losses. Through a 492:1 gearhead the load gets 57 to 106 mW, about 35 to 40 % of what the rotor pays, and even with pessimistic gears it is hundreds of times the sensor's need. The output is a slow alternating voltage of about 1 V at 0.1 to 0.2 Hz, and turning it into a supply is left open.

### 5. The one thing that would most help

Restore the missing text of 7.3. Then state the sizing rule as a requirement ("the lightest blade that gives the sensor a margin of X after the electronics") rather than as "the size this catalogue motor serves best".

---

## Chapter 8. The answer

### 1. Lost

- **LOST** "chapters 4 to 6 measured how little that gives, at the shaking levels the sources support" (8.1), and "the disorder adds little at the levels the sources support" (8.2). But 6.2 said "no source we could open says" how strongly the blade shakes, and 0.6 said "a level no source we found confirms". Which is it? As written, the conclusion leans on sources the notes say they do not have.
- **LOST** "the motion is regular at every wind and brake tried (chapters 2 and 3)". This is not shown in the text, because section 3.4 is empty.
- **LOST** "random shaking of white-noise type has a hard ceiling set by the second blade's mass". There is still no number for that ceiling on our machine.
- **LOST** "and the mother blade's sag at the tip by a few per cent", listed under "The disorder of the wind". The sag is caused by gravity and is perfectly regular; it is not disorder.

### 2. Slowed

- **SLOWED** Section 8.1 holds the cleanest result in the notes: $\bar P \le \tfrac{ml}{2}g\langle|\dot\theta|\rangle$, with the best brake reaching 0.555 of it, and the shopping-bag Picture makes it obvious. Had it come right after chapter 2, it would have organised everything after it: every later chapter is about what moves the left side or the right side of that inequality.

### 3. Annoyed

- **ANNOYED** "All the chapters meet in one inequality." Chapters 4 to 7 do not; 8.1 itself lists them as exceptions.
- **ANNOYED** "So the order the wind cannot spoil, gravity turning once per revolution, steers the energy and the rotor pays it". It sounds good and says what 1.4 already said.
- **ANNOYED** "Here is the whole answer, chapter by chapter." Section 8.2 repeats 0.6 almost line for line, down to "1 522 times" and "811 times". One summary is useful; two near-identical ones are padding.
- **ANNOYED** "and the air, the next model, decides whether this machine is worth building." That is honest. But after eight chapters the verdict is "not yet known", and I should have been told so on the first page, together with the reason the mechanics is worth reading anyway.
- **ANNOYED** "the current revision could not be opened from where these notes were written; revision D was read". This is about the writing process, not the source.

### 4. What I understood

Seen from the mother blade, gravity is the only force that can feed the swing on average. So the harvest is at most the weight at the centre of mass times its mean speed, $\tfrac{ml}{2}g\langle|\dot\theta|\rangle$, and the best brake already gets 55 % of that. More power needs a larger first moment, which needs a stronger generator and a stronger blade tip. The air, left out of the notes, may change all of it.

### 5. The one thing that would most help

Move the ceiling forward to right after chapter 2, and move the "the air decides" verdict to chapter 0.

---

# The whole text

## The five worst problems, ranked

1. **Two holes where the argument should be.** Section 3.4 ("Chaos and the harvest") has no text, only a table caption. Yet the chapter title, the chapter introduction and 8.2 ("the motion is regular at every wind and brake tried") all rest on it. Section 7.3 breaks off at "It has a positive root only if $4f/\pi", so the swing Θ, the jam condition and the meaning of $P_{\rm rotor}$ are lost. A reader cannot rebuild either gap. (Both look like rendering or production faults; the "<" in "4f/π < G" may have swallowed the text after it.)
2. **The first derivation is wrong exactly where a physicist checks it.** In 0.2, $C_p(\tfrac12) = \tfrac12$, not 0. The Picture ("A turbine that stops the wind gets nothing") and the Check box ("$a = \tfrac12$ ... again $P = 0$") both repeat the error. Trust in the Check boxes is gone by page two, and the notes depend on those boxes for trust.
3. **The question is never framed so that the answer matters.**
   - The air is, by the notes' own estimate in 0.7, at least as strong as gravity on any real second blade. Yet it is left out, and it appears only in "Where the numbers come from" and in the last paragraph.
   - Why the harvester is a *blade* rather than a weight on an arm is never said.
   - The need is never examined: the 37.6 µW is not derived, a battery for the turbine's life is never compared, and the margin is about 1500 times.
   - So the sizing rule, "the one the generator of chapter 7 serves best", has no requirement behind it.
4. **Chapters 4 to 6 answer side questions with their key inputs missing, in undefined jargon, and the summaries claim more than they show.**
   - Missing inputs: no value of S for the blade; the real shaking is not white noise; the 5 to 100 mm tip vibration has no source, nor do the modal mass and the damping; the equations of the 6.2 model are not shown.
   - Undefined jargon: Kaimal, IEC 61400-1 class A, TurbSim, "torque law", "kink", "square-law controller"; and "the generator" means two different machines in chapter 5.
   - Overclaiming summaries: "Mostly it does not help" (0.6) and "at the levels the sources support" (8.1, 8.2) do not follow from what these chapters show.
5. **Numbers and pictures without meaning.**
   - The key results live in tables I could not see, and the prose has no worked example.
   - False precision: "1 522 times"; 64.6 mW for an effect then said to be possibly "several times below them".
   - Small inconsistencies: −0.024 against −0.0231 rad; 0.214 against 0.215 rad; 202 against 201 mW; "at most about a tenth of a radian per second" against 0.155 rad/s.
   - Missing scales: the rotor's torques in N m, the swing in centimetres, and the fact that the best brake is about five times critical damping.
   - The first Picture of the machine (a ruler on a Ferris wheel lying along the spoke) contradicts the reader's own experience.
   - Symbols mean several things (list below).

## Does the order of chapters work?

Chapters 1 to 3 work: each builds on the last, and chapter 2 is the high point. The rest fights me:

- Chapter 0 opens with two pages of aerodynamics before the question, and 0.4 ("what our question needs") comes before the question in 0.5.
- Inside chapter 1, the Lagrangian (1.3) comes before the turning frame and the bowl (1.6), which is the more physical route and the shorter one.
- The ceiling of 8.1 is the organising idea, but it arrives last.
- Chapters 4 to 6 (a theorem that does not apply to the real blade, then two effects of a few per cent) come before chapter 7, which delivers the actual watts. By the time I reached chapter 7 I had half forgotten chapter 2's numbers.

The order I would have wanted: 0.5 and 0.6 (the sensor, the idea, the short answers, the air caveat) → a short turbine section (Ω from λ*, gravity turning once per turn) → 1.6, then 1.2 to 1.5 → 2 → 8.1 (the ceiling) → 3 → 7 → 5 and 6 → 4 as a box → 8.2.

## Where I stopped caring, and why

- I first wobbled at 0.2, the $a = \tfrac12$ error.
- From 0.7's air paragraph on, I read the rest as a mechanics exercise rather than a design.
- I really stopped at the end of chapter 4. Its last paragraph says "A real blade, though, does not shake as white noise", which dismisses a chapter-long theorem in one line. Then chapter 5 opens with "IEC 61400-1, edition 3, turbulence class A, as implemented in NREL's TurbSim ... the Kaimal spectrum", a wall of names with no picture.
- I skimmed chapters 5 and 6 for their conclusions. Chapter 7's dynamo, egg beater and box pulled me back in, until the text broke off mid-sentence in 7.3.

## Symbols that mean two or more things, and terms used before they are defined

| Symbol or word | Meanings |
|---|---|
| φ (and ϕ) | angle of the apparent wind (0.3); rotor angle (1.2 on) |
| $a$ | slowing fraction at the disc (0.2); shaking acceleration $a(t)$ (4.1) |
| $A$ | disc area (0.1, 0.2); complex amplitude (2.2); mass matrix $A(q)$ (4.1) |
| $J$ | rotor plus turbine generator, 4.38·10⁷ kg m² (5); motor rotor, 14.7 g cm² (7.2) |
| $L$, $\mathcal L$ | lift (0.3); rod length of the bob (1.3); Lagrangian (1.3); $L_{\rm coil}$ (2.3); $L_c$ (7.1) |
| $s$ | distance along the second blade (1.2); relative spread of rotor speed (5); root of $s^2+\kappa s+R$ (Table 2) |
| δ | lag of the swing (2.2); Dirac delta (4.1) |
| $x$ | horizontal coordinate (1.2); κ/κ* (Figure 5); motor-side torque (7.8) |
| $k$ | $k_e$, $k_t$ (1.3, 7.1); the gear-loss factor η to a power (7.8) |
| "the generator" | the turbine's (0.3, chapter 5); the one in the hinge (1.3 on) |
| "apparent wind" | the air meeting the blade (0.3); apparent gravity (1.1) |
| "front" | the upwind side (0.3 text); the blade's direction of motion (Figure 1) |

Used before being defined, or never defined: $r_{\rm rot}$ (used 0.3, defined 0.7); $v_{\rm tip}$ (used 0.7, defined 2.3); "stiff" (used 0.7, explained 3.1); "the simulation" (Figure 2, 0.7, 1.4, Figure 6; never); NREL (never); "edgewise" (in passing in 4, no picture); $w$ (6.1, never); $\omega_e$ (6.2, never); "modal mass" (6.2, never); "the starts" (Table 2, never); "stall-regulated", "tip brake" (7.6, never); "Kaimal spectrum", "turbulence class A", "TurbSim", "torque law", "kink" (5, never); the 37.6 µW sensor budget (0.6, never derived).

## Recurring annoyances, collected

- Talk about how the notes were made: "the results are put into the text by a script", "a script checks every number in the text", "( tools/compare.js )", "made for an earlier version of this study", "no source we could open", "the current revision could not be opened from where these notes were written", and the SymPy confirmations repeated chapter after chapter.
- The same big numbers with all their digits, three times each: "1 522 times", "811 times", "0.31 %".
- Double negatives: "lowered ... by −0.024 rad", "costs −0.11 %", "falls by −2.55 %".
- Hedges where a measurement was cheap: "These notes have not measured the three separately", "these notes have not separated where the rest comes from".
- Sentences that sound good and add nothing: "Three consequences are worth a second look.", "All the chapters meet in one inequality.", "So the order the wind cannot spoil, gravity turning once per revolution, steers the energy and the rotor pays it".

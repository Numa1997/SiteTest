# Skeptic review r1: driver and damping display, driven-oscillator.html

Reviewer stance: skeptical theoretical physicist, did not build this. Read only `public/simulations/driven-oscillator.html`
(§02, §07, §09 `p-screen`, §10 `p-limits`; script constants, solve(), setSpan(), fitScale(), geom(), drawMechanism(),
drawCoil(), drawForces(), drawEnergy(), drawWindow(), draw(), frame(), Sim.data) and the cited Leybold link.

**Moving target.** The file changed while I was reading it: 1286 lines at the start, 1408 lines at 03:29:35 (a PID
controller was added to the script). I froze the later version (md5 `508ab88b96e2dcecdbe90627a6e3d47f`) and reviewed that.
The text of §02, §07, §09 and §10 is the same in both versions. The driver/damping drawing code is the same apart from the
controller force now flowing through the coil (row 3).

Tools: sympy 1.14 (Euler–Lagrange with Rayleigh, cross products), a Python copy of solve()'s RK4, and a Python copy of
geom() run over canvas widths 300–1600 px.

## What I verified and found right

- **Lagrangian.** With L = ½mẋ² − ½kx² + ½L_c q̇² + Bℓ x q̇ and 𝓕 = ½cẋ² + ½Rq̇², the x-equation is mẍ + cẋ + kx = Bℓq̇,
  so F = +BℓI. The q-equation, *with V as the generalized force on q*, is L_c q̈ + Rq̇ + Bℓẋ = V, which is (10).
  The coupling Bℓ x q̇ and −Bℓ q ẋ differ by d/dt(Bℓ x q), so both give the same equations (sympy check). The coupling
  term is the usual flux-linkage term Λ(x) I with Λ = Bℓx, which holds while the winding stays in a uniform field.
  The Lagrangian is legitimate.
- **Power.** VI = RI² + d/dt(½L_c I²) + Bℓẋ I, and Bℓẋ I = Fẋ = P_in. Correct.
- **(11) and its numbers.** (Bℓ)²/R = 100/8 = 12.5 kg/s. Units: T²m²/Ω = N·s/m = kg/s. The ratio to c = 0.3142 is 39.8
  ("forty"). ζ_e = 12.5/(2√(km)) = 1.99 ("about 2"). Correct.
- **Coil numbers.** 100 turns × π × 3.2 cm = 10.05 m. I0 = 0.1 A at 1 N and 0.5 A at 5 N (slider maximum 5 N). Correct.
- **§2 and §7 numbers** (my RK4 copy): k = 9.870, c = 0.3142, τ = 6.366 s, X = 0.4819 m, φ = 25.35°,
  ⟨P⟩ = 0.2917 W, W_in = 19.0317 J, W_loss = 17.9256 J, E(T) = 1.1061 J, balance 1.27e−12, window 4/0.45 = 8.89 s.
  All match the page.
- **Forces in steady state at f = f0.** Spring amplitude kX = QF0 = 10 N. Damper amplitude cω0X = F0 = 1 N.
  The damper is in antiphase with F, so the two cancel. "About Q times longer" and "nearly cancel" are right as amplitudes.
- **Arrow scale.** px/N = 2(px/m)/k, so a force F is 2F/k on the motion scale. The text, the code and Sim.data agree.
  The damper arrow −c v always points against v.
- **Oil shade.** Its alpha is 0.85·P_loss/max P_loss, as the text says.
- **Energy bars.** E = W_in − W_loss exactly, because E(0) = 0 (start at rest at x = 0).
- **Geometry** (geom()/drawCoil(), every width tested). The winding stays in the gap: 3 px from the pole tip at x = −span
  and 2 px from the back plate at x = +span. The cap stops 3 px short of the pole tip, the block 11–15 px short of the
  magnet, and the piston stays in its cylinder (1.6 px margin at 300 px). After Solve, span ≥ max|x|, so these hold for
  every sample of the present run.
- **Held scale.** span ← max(span, need) after Solve and span ← need after Fit scale, as the text says. The outline is
  hidden when |x_prev| > span.
- **Phase statement.** φ → 0, 90°, 180° from (4). Correct once the start has died away.
- **Pohl's wheel.** The manual's text, as WebFetch returned it, has "durch eine Wirbelstrombremse verschieden stark
  gedämpft", "Elektromagnet für Wirbelstrombremse: 0–24 V" and the damping constant measured against the magnet's current
  (§4.1). This supports "eddy-current brake, an electromagnet". (The link itself is dead now: row 9.)

## Objections

| # | Where | What is wrong | Why (derivation / estimate) | Severity | What would settle it |
|---|-------|---------------|-----------------------------|----------|----------------------|
| 1 | drawCoil(): `[[y − rt − wh/2, I >= 0], [y + rt + wh/2, I < 0]]` with 'N' on the central pole; §9 "B points straight out from the central pole", "a dot is current coming out of the screen" | **The drawn current pushes the wrong way.** For I > 0 the page draws a dot above the pole and a cross below, then draws F = BℓI > 0 to the right. | Take x right, y up, z out of the screen. Upper piece: B = +ŷ, current +ẑ, so dF ∝ ẑ×ŷ = −x̂. Lower piece: B = −ŷ, current −ẑ, so dF ∝ (−ẑ)×(−ŷ) = −x̂. The Lorentz force for the drawn current is to the **left**. A student who applies the right-hand rule to the picture gets the opposite of the arrow. | must fix | Swap dot and cross (cross above the pole for I > 0), or swap N and S. Add a read-back test that checks the symbol above the pole against sign(I). |
| 2 | §9, first sentence: "The driver on the screen is the one inside every loudspeaker", and "the gap … longer than the winding by the full travel" | **Overstated analogy.** The principle is the loudspeaker's, but the stroke is not. | At the defaults the block swings ±0.5 m (±1.0 m at f = f0), so a fixed magnet needs a uniform 1 T radial gap more than 1–2 m long. At the slider corner (f0 = 0.2 Hz, ζ = 0.01, F0 = 5 N, f = f0) it swings about ±84 m after 60 s, so the gap would be about 170 m. Loudspeaker coils move millimetres. The drawing only keeps the winding in the gap because the magnet is redrawn with the span: its length in metres is (2A_px + cw + 5)/(px/m) ≈ 2·span, so it changes with every Fit scale. | must fix | Say "a long-stroke version of the moving-coil motor of a loudspeaker (real speaker coils move millimetres)". Say that the magnet is drawn as long as the run needs. Add to §10 what happens beyond a fixed gap: F then depends on x. |
| 3 | Code vs §9/§10 (frozen version): `Fs[n] = Fpush[n] + us[n]`, `Is[n] = Fs[n] / BL`, with u = Kp(r − x) + Ki z − Kd v; drawCoil() comment "the current source, I = I0 cos Ωt" | **With the controller on, the coil current depends on x and v**, so the text is false for those runs. §9 has "I(t) = I0 cos Ωt" and "a function of time alone"; §10 has "the force stays F0 cos Ωt whatever the block does". | Read the code: I = (F0 cos Ωt + u(x, v, z))/Bℓ. Also: the symbols' brightness is \|I\|/I0, clamped at 1, so with F0 = 0 and the controller on, I0 = 0 and every symbol shows at the minimum alpha whatever the current. The code cites "§9 closed loop" and equations (14)–(16), which do not exist in the note (its equations end at (11)). Also need = max(xmax, F0/k, \|r\|) counts r when the controller is off, so the default r = 0.3 m can widen the span of a run with no controller (for example F0 = 0.5 N). | must fix (a concurrent edit; I cannot approve a moving target) | Freeze the file. Then either keep the coil at I0 cos Ωt and show u as a separate actuator, or rewrite §9/§10 to say "the force is whatever the source is told to drive; with the controller on, the controller tells it to depend on x". Normalise brightness by max\|I\|. Count r only when the controller is on. Write the missing §§ and equations or fix the comments. |
| 4 | §9: "The equation for q gives the voltage the source must supply: (10)" | **(10) does not follow from what is written.** L and 𝓕 as given contain no source. | With L and 𝓕 alone, the q-equation is 0 = RI + L_c İ + Bℓẋ, a shorted coil. V must enter as the generalized force on q (or as a term Vq in L). The page never says so. | must fix | Add "and the source's voltage V is the generalized force on q". |
| 5 | §9, the Lagrangian paragraph | **Heavy machinery, weakly motivated, in an unstarred section** of a note "for school students and first- and second-year undergraduates". | Kirchhoff's loop law with Faraday's motional emf gives (10) in one line. The Lagrangian's real payoff is not stated: one constant Bℓ appears in both the force and the back-emf, which is energy conservation (reciprocity). As written, "the result (9) by a second route" adds nothing a reader asked for. The page marks heavier mathematics with ★ (§3, §5), but §9 has no star. | must fix | Either star the paragraph (or a §9 sub-heading) and say what it buys (the same Bℓ twice, so the books of §7 balance), or replace it with the Kirchhoff loop. |
| 6 | §9: "L … L_c … ℓ … 𝓕 … F … R … q … Q" | **Letter collisions.** L is the Lagrangian next to L_c (inductance) and ℓ (wire length). 𝓕 is Rayleigh's function next to F (force) and F0. q (charge) and Q (quality factor) sit in the same section, and in Lagrangian mechanics Q usually means a generalized force. In the code, L and R are also margins (code only). | Readability at school level. A reader copying the formula can confuse L with L_c, or 𝓕 with F. | minor | Write 𝓛 for the Lagrangian, or name the inductance L_coil. Say "Rayleigh's function 𝓡". |
| 7 | §9: "emf", "back-emf", "Rayleigh's dissipation function", "Lagrangian" | **Terms used without definition** for the stated audience. | "emf" is first used without saying it is the voltage induced in a circuit. Rayleigh's function is named but not explained (it is the function whose ẋ-derivative gives the friction force). | minor | One clause each. |
| 8 | §9: "Two conditions keep the force a function of time alone, as §1 requires" | **"Two conditions" is incomplete, and the cross-reference is wrong.** | (a) The tube must not conduct. An aluminium former, as most loudspeakers use, is a shorted turn: it brakes ∝ ẋ exactly like Pohl's wheel, which the same paragraph cites. (b) L_c must not depend on x. The Lagrangian assumes this; real voice coils have L_c(x), which gives an x-dependent force ½I² dL_c/dx. (c) §1 never states the requirement; §2's last paragraph does ("t appears on its own"). | minor | Write "a tube of paper or plastic" and "the main conditions". Cite §2. |
| 9 | §10.1, the Leybold link | **Dead link.** | `curl` returns HTTP 404 (Apache "Not Found") for the cited URL; the directory /Manuals/ is also 404. WebFetch returned text, probably from its own cache. The Wayback Machine has a copy (2023-05-28, status 200), but its download was blocked here, so I could not read the PDF itself. WebFetch's text shows sections 1–4.4 only. "(Section 9)" means this note's §9, as in the Feynman entry, but it reads like a section of the manual. | must fix (Sourced) | Replace with the archived URL or LD Didactic's current 346 00 document, after opening it. Write "(used in §9 here)". |
| 10 | §9: "The whole mechanism is drawn on one scale, in pixels per metre" | **Overstated.** Only displacements and arrows use px/m. | Block width, spring and damper sizes, the coil's diameter and the magnet are fixed in pixels, so their sizes in metres change with the span. Sim.data 'about' admits "schematic"; the lecture text does not. | minor | Write "Every displacement and every force arrow is drawn on one scale…; the parts themselves are schematic". |
| 11 | §9: "its oil darkens while it turns energy into heat"; canvas legend "darker oil: more heat" | **The shade does not show the damping.** It is normalised to each run's own largest P_loss. | A run with ten times the damping reaches the same full darkness. The shade shows *when* heat is made in a cycle, not *how much* compared with another run, but the legend reads as absolute. The text is honest ("as a fraction of the largest value in the run"); the canvas legend is not. | minor | Write "darker oil: more heat now than at other moments of this run", or normalise to a fixed reference such as the run's ⟨P_in⟩. |
| 12 | §9: "Near resonance the spring's arrow is about Q times longer than the other two, while the coil's and the damper's arrows nearly cancel" | **Right only for amplitudes, in steady state, at f ≈ f0.** It is easy to misread as "at every instant". On small screens the other two arrows disappear. | At the instant the spring arrow is longest (x at its peak, v = 0), the damper and coil arrows are zero. At the default f = 0.45 Hz (two half-widths below f0) the amplitudes are 4.76, 0.43 and 1 N, which do not cancel. At ζ = 0.01 on a 340 px canvas the coil arrow at resonance is 2A_px/Q ≈ 1.4 px, below the 2 px drawing threshold, so it is not drawn at all. | minor | Write "Once the start has died away, with f = f0, the spring's arrow reaches about Q times the length of the other two…". |
| 13 | §9: "each drawn twice as long … so they share the scale of the motion"; held scale | **Arrows do not compare between runs with different f0.** | px/N = 2(px/m)/k, and k changes with f0, so the same 1 N is drawn at a different length after f0 changes, even with the span held. Changes of ζ, F0 and f are fine. | minor | One clause: "within a run, and between runs with the same f0". |
| 14 | §9: "their sum is m ẍ"; energy bars | **Claimed but not shown, and not read back.** | The three arrows are drawn on separate rows, not head to tail; no arrow for mẍ is drawn. The E bar, the oil shade and the dot/cross have no `drawn` read-back test in Sim.data (only W_in and W_loss bars, arrows, block and curves). Row 1's sign error is the kind of error such a test catches. The bars are normalised per run, which only 'about' says. | minor (Checked) | Add read-backs for the E bar, the oil alpha and the symbol above the pole. Say in §9 that bars compare within a run. |
| 15 | §9: 12.5 kg/s, "forty", "about 2", R = 8 Ω | **Numbers the model does not compute or store.** | They are correct (39.8 and 1.99), but they exist only in prose. R appears nowhere in the code or the dataset, and the ratio depends on c and k, so it is right only at the defaults (the text says "with the defaults" for the ratio only). | minor | Store R, (Bℓ)²/R, its ratio to c and ζ_e in the dataset, or say "with the defaults" for both. |
| 16 | §10, current-source bullet | **Correct, but not quantified.** | The peak voltage the source needs, V ≈ BℓΩX + RI0, is 13.6 + 0.8 V at the defaults, about 32 V at f = f0, and about 1 kV at the slider corner. This is the honest size of the "voltage limit". The coil's Joule heat, ⟨RI²⟩ = 0.04 W against ⟨P_in⟩ = 0.29 W, is also left out of the books (8); that is fine, but it is not said. | minor | One sentence with the default numbers. |
| 17 | §9, Pohl's wheel sentence | **Placed under "On screen", but not on screen.** | This is a digression placed between (11) and the damper description. It is motivated (it is the everyday instance of the second term of (11)), but it interrupts the screen description. | minor | Move it to the end of the voltage-source paragraph, or into §10. |

## Thresholds

| Threshold | Verdict | Reason |
|-----------|---------|--------|
| Motivated | PASS (with caveat) | A coil from the other side, a current source and not a voltage source, and a piston in oil: each answers a question the reader has. The Lagrangian does not (row 5). |
| Honest | FAIL | The drawn current pushes against the drawn force (1). The loudspeaker framing hides a metre-scale stroke (2). In the code as it now stands, §9/§10's "function of time alone" is false with the controller on (3). "One scale" (10). |
| Derived | FAIL | (10) needs V as the generalized force on q, which is missing (4). Everything else derives correctly (sympy). |
| Checked | FAIL | The sign error (1) passed the page's own checks. The E bar, the oil shade and the current symbols have no read-back (14). All quoted numbers recompute correctly. |
| Sourced | FAIL | The Leybold link is 404 (9). No source for the electromechanical Lagrangian or for typical Bℓ; the chosen Bℓ = 10 T·m is labelled as chosen, which is honest. |
| Readable | FAIL | A Lagrangian with Rayleigh's function in an unstarred section for school students (5). Letter collisions (6). Undefined emf and 𝓕 (7). |

Approve nothing else: I checked every claim listed in the brief, and the rows above are the ones that failed.

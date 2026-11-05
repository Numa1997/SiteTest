# Fig. 12 · referee report, round 1

Page: `public/simulations/beer-slosh.html`, the lecture note "Sloshing in a pint glass" (`<article class="paper" id="paper">`).
Read as two people at once: **S**, a school student who is good at mathematics, and **G**, a physics graduate. Judged against
`notes/STANDARD.md` (section 4, and Numa's verdict of 21 October 2026: Taylor's *Classical Mechanics* as the model).

How it was read: `npm run build`, `dist/` served locally, opened in headless Chromium (Playwright, SwiftShader WebGL) at
1280 × 900 and 390 × 844; all 31 folds of the note opened; each of the 9 sections screenshotted with the sticky headers
released. KaTeX errors: 0. Console and page errors: none. Horizontal overflow: none at either width. `plan.md` and
`check.md` were not read; neither was `check-derivations.md`. Every number quoted below as "checks" was recomputed by hand
or in Python from the note's own inputs.

Tags: **[S]** a school student gets lost; **[G]** a graduate objects; **[both]**.

---

## A. Problems that run through the whole note

**A1. The stated reader does not match the unstarred text.** [S] The byline promises a reader who knows "Newton's laws, a
little calculus and the idea of a normal mode". The unstarred text then uses the Navier–Stokes equation, divergence, curl,
the Laplacian, Bessel functions, a weak form, finite elements, index notation with summation (`e_ij e_ij`) and Green's
identity, none of it introduced. Only two parts carry ★. Under STANDARD §4 item 3 and verdict 21 Oct item 4, "The eigenvalue
problem" (section 5), "The bulk" (section 7) and the separation of variables in section 4 are heavier mathematics that should
carry ★, or be preceded by a sentence telling S what each operator means physically.

**A2. The ★ rule is broken in two places.** The rule says the result of a starred passage is restated unstarred.
- Section 3: the ★ part "Why the interior has no rotation" contains the Key result box (u = ∇φ, ∇²φ = 0) *and* the
  unsteady Bernoulli equation (5). Both sit inside the starred fold (checked in the DOM: they come after the ★ `h4` and
  before the end of the section). Section 4, which is not starred, rests on (5) ("Putting p = p_air in (5)"). A reader who
  skips the ★ part never sees (5) or the Key result.
- Section 6: the damping ratio ζ = γ/ω is defined only inside the ★ part "Pumping: Faraday's waves", in (13). It is one of
  the six main readouts on the page ("Damping ratio ζ₁ 2.44 %"), and section 7 uses "γ/ω" in words. S never learns what ζ₁ on
  the screen is.

**A3. One symbol, several meanings** (verdict 21 Oct item 2: "one symbol one meaning"). [both] These will trip S and annoy G:

| Symbol | Meanings in the note |
|---|---|
| ω | vorticity **ω** (bold, eq. 3) and angular frequency ω (eq. 4, same paragraph) |
| z | coordinate up from the foot (sec. 3, 5, Fig. 1); coordinate down from the calm surface (sec. 4, eq. 7, "at z = 0"; sec. 7 "e^{λz}"); vertical position of the glass (sec. 6, "z = A sin Ωt") |
| x, ẍ | ẍ, ÿ, z̈ are the **glass's** acceleration, but x, y, z are coordinates **inside** the glass, in the same formula: Ψ = (g + z̈) z + ẍ x + ÿ y (2). S reads ẍ as the second derivative of the x next to it. The glass position gets its own name, **x**_g, only in "The hand", near the end of section 6 |
| a | radius of the surface (sec. 4 on); mode amplitude a_n (sec. 6); a_g glass acceleration (sec. 3); "a cos(ωt + φ)" (sec. 6) |
| A | potential amplitude in (7); shaking amplitude (sec. 6) |
| f | frequency f₁, f₁₁; mode surface shape f_n(r) (sec. 6); subscript "foam" in M_f, μ_f, h_f, ε_f, γ_f, U_f, k_f |
| μ | viscosity μ, μ₆, μ_w, μ(T); added-mass ratio μ_{f,n} (eq. 11) |
| k | wavenumber; projection index in "multiply by f_k" (sec. 6); head friction factor k_f |
| U | slip velocity in the Stokes layer (sec. 7); U_f = 1.6 cm/s foam constant (eq. 18) |
| λ vs k | the cylinder uses k, the tulip λ; section 4 says "in our pint kD = 6.1" before λ is defined |

The z clash is the worst: (6) is imposed "at z = z_s" (z from the foot), and two paragraphs later "∂²_t φ + g ∂_z φ = 0 at
z = 0" (z from the surface), with no sentence saying the origin moved.

**A4. The model is never stated in one place** (STANDARD §4 item 2). The assumptions (incompressible; glass translates
without turning; irrotational interior; linear surface; head a rigid mass layer; contact line a constant rate), the regime,
and the dimensionless numbers are scattered over sections 3 to 9. The dimensionless numbers the page actually has are never
collected: kD = 6.1, δ/a ≈ 0.011, the Bond-type ratio σλ²/(ρg) = 0.010, μ_f = 0.128, ζ = 0.0244, η/a (the page's own
linearity readout), ε = AΩ²/g = 0.34 for the 2 mm Faraday button. A short "The model" paragraph or table at the end of
section 2 or 3 would serve both readers.

**A5. Internal jargon and repository paths in reader text.** "the brief's straight glass" (Example 4.1 title) and "the
equivalent coefficient … of the brief" (section 6): no reader knows what "the brief" is. "notes/fig12/gate.cjs",
"[notes/fig12/check-derivations.md]" (section 6) are repository paths printed as if they were citations; they are not links,
not in the source list, and the square brackets collide with the "[n] = source" convention the note itself announces in
section 1.

**A6. Checks (STANDARD §4 item 4).** Limiting case (deep tank, tanh → 1) and the cylinder benchmark are there, energy is
used, numbers are worked. Missing: any explicit dimensional check, and the simplest limiting case of all, a glass under
steady sideways acceleration, whose surface must tilt at tan α = ẍ/g. That one line would also give S the physical picture
for (2) and (6).

---

## B. Section by section

### 1 · Carrying a pint

- Strong opening: walking, the rhythm, the feeding, the dying away, then "a driven, damped oscillator". This is the
  standard's item 1 done well.
- "the 20-ounce tulip pint" [S]: imperial ounces (568 mL), but an American reader reads 20 US oz = 591 mL. Say
  "imperial".
- "a controller that carries a pint without spilling is a later chapter" while the page header says "Fig. 12 · Control
  systems · Fluid dynamics": a reader looks for the control and finds none. (The header is outside the note; flagged only.)
- "How claims are marked": clear. A COMPUTED tag after a long sentence does not say which of its numbers it covers; minor.

**Verdict: clear, leave it** (apart from "imperial").

### 2 · The glass and the stout

- "taking a wall 2.0 mm thick and a solid base 8 mm thick (both read from the photograph)" [both]: a side-on silhouette gives
  the outer edge only. How was a wall thickness read from it? Through the glass? One clause is needed, or the numbers are
  unsupported.
- "eight millimetres below the rim, where a lined pint glass puts its line" [G]: no source; the Guinness tulip is not a
  lined glass. Unsupported claim.
- "The outline was then smoothed to 0.2 mm" [S]: smoothed with what length or tolerance? "to 0.2 mm" is ambiguous.
- Table row μ(T): "(Vogel's equation)" names an equation never written. Fine for G, opaque for S; the 31 % figure checks
  (water 1.47 → 1.00 mPa·s).
- Table row h_f: "18 to 20 mm for a correct pour [11]. Firm enough." Source [11] is marked "snippet only" in the list. "Firm
  enough" is not supported by a snippet.
- Figure 1: the label "84.1 mm" is dark red on the near-black stout and is barely legible at 1280 px.
- Numbers check: ν = 2.05 × 10⁻⁶ m²/s, M_f = 2.72 kg/m², 96-gon factor 0.99929 and the 0.4 mL gap all reproduce.

**Verdict: needs work, small** (wall thickness source, "lined glass", "firm enough" on a snippet, Figure 1 label contrast).

### 3 · A fluid in a moving glass

- The train-and-coffee lead is the right picture.
- "In the laboratory, its acceleration is that of the glass plus its own, so in the glass's frame" then (1) [S]: the step is
  skipped. Write the lab-frame law ρ(**a**_g + D**u**/Dt) = … and move ρ**a**_g to the right; one line.
- (1) itself [S]: none of its terms is given a meaning. S needs one sentence each: ∂**u**/∂t + (**u**·∇)**u** is the
  acceleration of a moving parcel; −∇p is the push of the pressure; μ∇²**u** is the viscous rubbing between neighbouring
  layers. "This is the Navier–Stokes equation" is a name, not an explanation.
- "Because the stout is incompressible, ∇·**u** = 0" [S]: no picture (what flows into a small box flows out).
- Ψ in (2) [S]: units (m²/s², energy per unit mass) and meaning (potential energy per kilogram in the glass's frame) not
  stated. And see A3: ẍ x.
- "stronger when the glass is lifted with increasing speed, weaker when it is lowered" [both]: **wrong as written**. Lowering
  at constant speed changes nothing; g_eff is weaker when the glass *accelerates downward* (starts to lower, or stops a lift).
- "If g + z̈ turns negative, the glass falls faster than free fall" [S]: "faster" reads as speed; it is the downward
  *acceleration* exceeding g.
- ★ "Take the curl of (1)" [G]: the division by ρ and the fact that curl commutes with ∇² (giving ν∇²**ω**) are silent;
  acceptable under ★, but one clause would do.
- "A stout that starts at rest … stays free of vorticity" [G]: true for a settled pint. A freshly poured Guinness is famous
  for its bubble-driven circulation (the very sources [3], [4] are about it), which is vortical. Say "a settled pint".
- "in one oscillation period of angular frequency ω it reaches a distance δ = √(2ν/ω)" [G]: inexact. √(2ν/ω) is the e-folding
  depth of Stokes' exact solution, the diffusion distance √(2νt) for a time t = 1/ω, a sixth of a period. In one full
  period vorticity diffuses √(4πν/ω) ≈ 2.5 δ. Either say "in a time of order 1/ω" or cite the Stokes solution.
- Same paragraph uses **ω** (vorticity) and ω (frequency): see A3.
- δ = 0.45 mm, 1 % of the radius: checks.
- Key result box and (5) are inside the ★ fold: see A2.
- (5): "The function C(t) can be absorbed into φ" [S]: why that is allowed (only ∇φ is physical) needs half a sentence.

**Verdict: needs work** (wrong "weaker when it is lowered", missing lab-to-glass step, no meaning for the terms of (1),
δ wording, ★ placement of the Key result and (5), symbol clashes ω and x/ẍ).

### 4 · Linear sloshing in a straight glass

- Lead ("Laplace's equation alone has no waves in it …") is a good physical hinge.
- Boundary conditions: clear. "moving the constant into φ" [G]: the "constant" (g + z̈) z_s depends on time; say "the
  function of time".
- "The error is of the order of the wave slope" [S]: wave slope = height over horizontal scale, kη; say so.
- "with r, θ polar coordinates and z measured from the calm surface" [both]: the origin of z silently moves (A3).
- "Trying φ = Φ(r) cos(mθ) Z(z) e^{iωt} gives Bessel's equation for Φ and Z'' = k²Z" [S]: three skipped steps. The Laplacian
  in cylindrical coordinates is not written here (it first appears in (9)); Bessel's equation is not written; the separation
  constant k² appears from nowhere. J_m is never named ("the Bessel function of order m, the solution that stays finite on
  the axis; the other, Y_m, is infinite there"). S has never met a Bessel function and gets no picture of one (a decaying
  wiggle, like a cosine that weakens outward).
- e^{iωt} in the trial, cos ωt in (7): switch not explained.
- "Eliminating η between the two surface conditions … gives ∂²_t φ + g ∂_z φ = 0" [S]: one line (differentiate (6) in time,
  insert ∂_t η = ∂_z φ). "putting (7) in" (8): one line (∂_z of the cosh factor at z = 0 is k tanh kD).
- "The number n counts nodal circles" [G]: **inaccurate**. Mode (1,1) has no nodal circle (J₁(kr) has no zero for kr < 1.84);
  (0,1) has one. For m ≥ 1 there are n − 1 nodal circles, for m = 0 there are n.
- No picture of what modes (1,1), (2,1), (0,1) look like. One sentence pointing to the 3D view would do.
- Example 4.1: "the brief's straight glass" (A5). D = 99.5 mm: why this value? Section 5 uses "40 mm radius and 100 mm
  depth" for the check, so two nearly equal cylinders appear without reason. "in our pint kD = 6.1": the pint is not a
  cylinder, and λ is not yet defined.
- "The depth no longer matters once kD > 3": give the reason (tanh 3 = 0.995, a 0.25 % change in ω).
- Key result box: good; the pendulum of length a/1.84 is exactly the kind of picture S needs. Numbers check (21.25 rad/s,
  3.382 Hz, 21 mm).

**Verdict: needs work** (separation of variables skipped for S, Bessel functions never introduced, wrong nodal-circle
count, z origin, "the brief", D = 99.5 mm unexplained).

### 5 · The real glass, by finite elements

- Lead is clear and well motivated.
- "The eigenvalue problem" is the heaviest unstarred part of the note (A1): weak form, test functions, integration by parts
  in cylindrical coordinates, quadratic elements, Schur complement. Mark it ★ and restate its result in one plain sentence
  (the computer finds, for each fill, the numbers λ_n and the shapes Φ_n).
- (9) → λ = ω²/g [S]: comes from the condition in section 4; say "from ∂²_t φ + g ∂_z φ = 0".
- (9) [G]: no condition on the axis r = 0 (Φ = 0 for m ≥ 1, regular for m = 0).
- (10): the upper limit "a" is now R_i(z_s), the surface radius; say so.
- "on each [triangle], Φ is a quadratic polynomial … six nodes" vs the check's "a mesh of 16 × 40 quadratic cells" [G]: are
  the elements triangles or quadrilaterals?
- "halving the cells reduces every error" [G]: by what factor? The convergence order is what shows the program is right.
- "Compared with a straight glass … (3.14 against 3.25 Hz at 300 mL)" [both]: these are the **with-head** curves of Figure 2
  (the ink no-head curve sits at 3.33 Hz there). The sentence does not say so, and S looks at the top curve.
- INFERENCE paragraph on the lean of the wall: labelled honestly, readable.
- Surface tension: "adds a pressure −σ∇²η" [S]: no picture (a curved skin pulls like a stretched drum). [G]: using λ³
  (i.e. replacing the surface Laplacian eigenvalue by λ²) is exact only for the cylinder, and the contact-line condition for
  σ (pinned or free) is not stated. One sentence each.
- Head: "Newton's law for the layer says the stout must push on it with an extra pressure M_f η̈, which enters (6) as an
  inertia. With both," then (11) [S]: the step to (11) is skipped. One line: ∂_t² φ + gλφ + (M_f λ/ρ) ∂_t² φ = 0. (It checks.)
- μ_{f,n} reuses μ (A3).
- "The added-mass ratio μ_f compares the head's mass with the mass of stout that sloshes, a layer of depth 1/λ": an excellent
  one-line picture.
- Example 5.1: numbers check (3.427, 3.445, 3.244 Hz; μ_f = 0.128).
- Rendering: at 1280 px eq. (9) wraps "at z = z_s" onto its own line; at 390 px eq. (9) breaks into overlapping
  fractions (∂Φ/∂n and ∂Φ/∂z collide). Screenshot: `narrow-sec05-a.png` (scratchpad).

**Verdict: needs work** (FEM part unstarred, with-head numbers unlabelled, (11) step skipped, axis condition, element type).

### 6 · Driving the modes: hand and shaker

- "The potential is φ = Σ (ȧ_n/λ_n) Φ_n cos mθ, because the kinematic condition requires ∂_t η = ∂_z φ = λ_n φ": clear for
  G, one step quick for S but followable.
- "Put both into (6), multiply by f_k cos mθ r and integrate" [S]: the key fact is hidden. In (6), ẍ x must be written as
  ẍ r cos θ; then only m = 1 survives the θ-integral. The Key result asserts "which in a round glass means m = 1 only" without
  this line. Also, k is the wavenumber elsewhere (A3).
- (12): the sign is never interpreted [S]: accelerate the glass toward +x and the stout piles up on the −x side.
- "For clarity the σ term of (11) is not repeated; the page keeps it": fine.
- Closed form for Q: steps shown; checks (Q = 2a/(ξ² − 1), 0.057528 m). "of the brief" (A5), and why J₁(ξ) appears in the
  "equivalent coefficient" (a different normalisation) is not said.
- Resonance: "the steady amplitude of (12) is the push divided by the damping" [S]: one line (at Ω = ω the spring and
  inertia terms cancel, leaving 2γȧ = push). The formula checks; μ_f loses its index n here.
- Example 6.1: checks (0.083 m/s², 5.6 mm, × 28). Good.
- ★ Faraday: "at an amplitude growth rate εω/4, as averaging the modulated spring over one period shows" [G]: this is an
  "it can be shown" in disguise inside the very part meant for G. Show the averaging (four lines) or cite it (Landau &
  Lifshitz, *Mechanics*, §27).
- (13) and the 0.58 mm threshold and 1.2 s⁻¹ growth check. [G]: the averaging assumes ε ≪ 1; the button gives ε = 0.34.
  The measured 1.21 s⁻¹ shows it holds; say so.
- "a micrometre of initial disorder first falls about tenfold, because a seed at rest lies mostly in the decaying solution"
  [G]: unconvincing. A random seed of one Floquet pair projects roughly equally on the growing and decaying solutions, so it
  cannot fall tenfold for that reason. The likelier cause is that 13 of the 14 seeded oscillators are not at parametric
  resonance and simply decay, and the measured quantity sums them. Either show it or drop the explanation.
- "Michael Faraday saw these waves in 1831": no source (Phil. Trans. R. Soc. 121, 299, 1831).
- "The hand": Ω_h is never given a value. The page default is Ω_h = 22 rad/s (3.5 Hz, `P.Om`), almost exactly the slosh
  frequency 20.4 rad/s. That coincidence matters to how the hand filters (critically damped follower: response at ω₁ is
  about half), and the reader should know it.
- Missing picture [S]: why a walking step contains harmonics (the heel strike is a sharp, periodic jolt, not a sine).
- The stage caption under the 3D view prints the mode equation without the 1/(1 + μ_f) factor of (12); a reader comparing
  screen and note sees two different equations. (Outside the note; flagged for equation-to-screen.)

**Verdict: needs work** (m = 1 selection step, unshown averaging in ★, the "tenfold" explanation, Ω_h value, ζ defined only
in ★, Faraday unsourced, repository paths as citations).

### 7 · Where the energy goes

- The energy method (14): clear, with the condition γ ≪ ω and the page's 2 to 4 %. Good.
- ★ Boundary layers: every step shown and correct (Stokes solution, the period average, the integral U²/(2δ), (15), (16));
  the check I_w/E = 1.837/a reproduces. [both] From I_w/E = 1.837/a to "Δ₁₁ = 3.50 ν^{1/2} a^{−3/4} g^{−1/4}" one line is
  missing: Δ = π·1.837/(√2 ξ^{1/4}) with ω = √(ξg/a). [S]: "The power per unit area turned into heat is μ∫(∂u/∂s)² ds" has
  no picture (rubbing of neighbouring layers); acceptable under ★.
- "Miles showed that the damping observed … exceeds wall damping alone by factors of up to two or three, and traced the excess
  to surface films and to the contact line [5]": source [5] is "Abstract only". A specific factor and a specific mechanism
  are attributed to a paper whose body was not read.
- Skin: "I_s" is used but never defined (presumably the surface analogue of I_w). [G]: "c_s = 1 for one that cannot
  stretch [5]" is again from the abstract-only source. The default c_s = 1 is stated only in passing ("at c_s = 1").
- Bulk: "e_ij e_ij" with summation is unexplained for S; "this gives γ_b = 2νλ²" skips the integral (Lamb's result; cite
  it). "for a mode that decays with depth as e^{λz}" uses z from the surface (A3). 0.009 s⁻¹ and 2 % check.
- Contact line [G]: "default 0.05 per second, at the low end of the 0.05 to 0.25 per second measured in a water tank [7]": a
  damping *rate* depends on the tank's size and frequency; transferring it from a different tank without scaling needs a
  reason. And with the head on, γ_c and γ_f are both counted although the OPINION says the head "probably absorbs most of
  this": a possible double count, worth one sentence.
- Head: the transfer from slot (2/w) to cylinder (2/a) is clear and checks (0.232 s⁻¹). [G] Missing physical picture, and an
  inconsistency: section 5 treats the head as a rigid layer that moves up and down *as a whole*, but (18) saturates with
  thickness as 1 − e^{−λh_f}, as if the foam's motion fades with height. If the whole layer moves, wall friction should grow
  with h_f without saturating. Say what Sauret et al. found the mechanism to be and how it squares with the rigid-mass
  picture. "from 3 mm bubbles in dish soap to sub-millimetre bubbles in stout": no source for the stout bubble size.
- Figure 3: labels print raw underscores, "γ_w", "γ_s", "γ_c", "γ_f", "bulk 2νλ² γ_b", while the total uses a real subscript
  "γ₁₁". Units "1/s" in the figure, "s⁻¹" and "per second" in the text. Numbers sum (0.496 ≈ 0.497) and check.
- Key result: checks (2.01 s, 6.0 s; 3.7 s, 11.1 s). "With clean walls alone it would be 8.9 s to 1/e" [G]: 8.9 s is
  γ = 0.112 s⁻¹, which is walls *plus bulk* at the no-head frequency (walls alone, ≈ 0.103 s⁻¹, give 9.7 s). Say "walls and
  bulk".
- Closing paragraph (film a pint and count the swings): a good, honest invitation.

**Verdict: needs work, moderate** (abstract-only source carrying specific claims, I_s undefined, head mechanism vs
rigid-layer picture, contact-line rate transfer and double count, Figure 3 labels, "clean walls alone").

### 8 · The velocity field in the cut

- Clear and physical: arrows largest as the surface passes level, energy in the raised surface at the extremes; "Laplace's
  equation trades variation along the surface for variation with depth" is the best sentence in the note for S.
- Figure 4 is "at 480 mL" while the note's default pint is 500 mL: why 480 is said only in section 9 (nearest stored fill),
  and the six stored fills are never listed. Tie it in the caption.
- "the component across the cut, −mΦ sin(mθ)/r, is drawn as a ring" [S]: in the cut along the rocking direction this
  component is zero for the rocking mode, so Figure 4 shows no rings, and the reader wonders when they appear (sin copies,
  m ≥ 2, swirl-like superpositions). One clause.
- "e^{−λd}": d (depth below the surface) is defined only by context.
- The white arrows on near-black stout are small; at 1280 px the arrow directions in the top centimetre are hard to read.

**Verdict: clear, leave it** (two small clarifications: why 480 mL, when rings appear).

### 9 · On the screen, and what is left out

- No lead paragraph (`p.psec__lead` missing); the section opens straight into a part.
- Numerical method: integrator, order, step, stability limit and per-step phase error are given and check (ωh = 0.04,
  (ωh)⁵/120 ≈ 8.5 × 10⁻¹⁰). Against STANDARD §4 item 5 it is short of two things: **why** RK4 was chosen (the modal equations
  are linear; with z̈ = 0 and a known ẍ they could even be stepped exactly), and the error **measured by running the page**
  over a realistic run (e.g. phase drift after 10 s), not only the per-step formula. "capped at 50 ms per frame" [S]: say
  what that means for the reader (a slow computer runs the stout in slow motion rather than skipping).
- "keeps eight radial shapes: m = 0 …, m = 2 …, m = 3 …" [both]: section 6 has just said sideways motion drives m = 1 only.
  Why carry the m = 0, 2, 3 modes? (Presumably for Faraday pumping from the seed and for a realistic surface.) One sentence.
- Where the drawing differs: good and specific (head constant thickness, nearest stored fill, pink clipped arrows,
  see-through stout). Equation to screen (STANDARD item 6) still lacks the mapping for the readouts: ζ₁ (defined only in ★),
  "Head top to rim, now", the linearity line "the wave at the wall is … % of the radius", and the 50 mm/s arrow scale.
- Limits: "Beyond about a fifth of the radius, real sloshing in a round glass turns into a swirl" [G]: no source for the
  swirl or for the one-fifth threshold (e.g. Miles 1984; Royon-Lebeaud, Hopfinger & Cartellier, J. Fluid Mech. 577, 2007).
  "and the glass as perfectly smooth": smooth in what sense, and what would roughness change? The biggest omitted effect for
  a hand-carried pint is missing from the list: **the hand tilts the glass**. Section 3 assumed "the glass move[s] without
  turning"; a turning glass adds Euler and centrifugal forces that are not a gradient. Name it here.
- Problems: well chosen and tied to the page. **Problem 4 has a false premise.** "Your steps come at 1.6 Hz … why does the
  head make a spill less likely?" With the note's own numbers, the second harmonic (3.2 Hz) sits 0.04 Hz from f₁ with the
  head (3.244 Hz) and 0.245 Hz from it without (3.445 Hz). The steady response per unit forcing, λQ/[(1 + μ_f)
  √((ω² − Ω²)² + (2γΩ)²)], is 0.060 with the head and 0.024 without: the head makes the slosh about **2.5 times larger** at
  1.6 Hz steps, and leaves only 4.5 mm of freeboard. The head damps more but also detunes the pint *into* resonance. Either
  reverse the question or ask the reader to find this out.
- Problem 3: "2 f₁" set in text, not maths; minor.
- Sources (STANDARD §4 item 8: "only real sources you opened and read"): [5] abstract only, [6] secondary and the NASA
  document unopened, [7] Keulegan abstract only, [11] "snippet only". These carry specific claims in sections 2 and 7. There
  is no textbook chapter for the textbook theory the note uses (Stokes layer, wave damping 2νk², Mathieu instability,
  Bessel modes), e.g. Landau & Lifshitz, *Fluid Mechanics*, §§ 24–25 (oscillating viscous flow, damping of gravity waves); Lamb,
  *Hydrodynamics*, the chapters on surface waves and viscosity; Ibrahim, *Liquid Sloshing Dynamics*; Faltinsen & Timokha,
  *Sloshing*. (Section numbers other than Landau & Lifshitz's are left for the author to look up; I did not open these books.) Links all present.

**Verdict: needs work** (Problem 4 false premise, glass tilt missing from limits, swirl unsourced, method choice and measured
error, why m ≠ 1 modes are kept, readout mapping, source quality).

---

## C. Verdicts

| § | Title | Verdict | Main reasons |
|---|---|---|---|
| 1 | Carrying a pint | clear, leave it | "imperial" ounces only |
| 2 | The glass and the stout | needs work, small | wall thickness from a silhouette; "lined glass" unsourced; "firm enough" on a snippet; Fig. 1 label contrast |
| 3 | A fluid in a moving glass | needs work | "weaker when it is lowered" is wrong; lab-to-glass step skipped; terms of (1) unexplained for S; δ "in one period"; Key result and (5) inside ★; ω and x/ẍ clashes |
| 4 | Linear sloshing in a straight glass | needs work | separation of variables and Bessel functions skipped for S; "n counts nodal circles" wrong; z origin moves; "the brief"; D = 99.5 mm |
| 5 | The real glass, by finite elements | needs work | FEM part unstarred; Fig. 2 numbers are with-head but unlabelled; step to (11) skipped; axis condition; eq. (9) breaks at 390 px |
| 6 | Driving the modes | needs work | m = 1 selection unshown; ★ averaging not shown; "tenfold" explanation doubtful; Ω_h never given (22 rad/s); ζ only in ★; Faraday unsourced; repo paths as citations |
| 7 | Where the energy goes | needs work, moderate | abstract-only source carries specific claims; I_s undefined; head saturation vs rigid layer; contact-line rate transfer; Fig. 3 raw underscores; "clean walls alone" is walls + bulk |
| 8 | The velocity field in the cut | clear, leave it | say why 480 mL; when rings appear |
| 9 | On the screen, and what is left out | needs work | Problem 4 premise false (head raises the slosh ≈ 2.5× at 1.6 Hz steps); glass tilt missing from limits; swirl unsourced; RK4 choice and measured error; source quality; no lead |

The physics is sound and, outside the points above, every number I recomputed reproduces. The note's main weakness for S
is that the unstarred route through sections 3 to 5 uses vector calculus and Bessel functions that S has never been
shown. Its main weakness for G is a handful of unsupported or wrong statements (lowering vs accelerating, nodal circles,
the tenfold dip, Problem 4) and sources read only in abstract.

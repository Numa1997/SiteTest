# Referee report: The Electron Beam, reading guide, Chapter 0 and Chapter 1

Page: `public/portfolios/electron-beam/index.html`. Only the guide box (`#guide`), Chapter 0 (`#ch00`) and Chapter 1 (`#ch01`) were read.

How the page was read (9 November 2026):
- Rebuilt with `python3 portfolios-src/electron-beam/build.py --site --out <scratch>`. The output is byte-identical to the committed page, so the committed page is current.
- Served locally and opened in headless Chromium 1440 × 1000 (Playwright). Fonts were loaded and every fold opened (these sections have no `<details>`). I took screenshots in strips of 1800 px: 1 for the guide, 4 for Chapter 0, 14 for Chapter 1.
- Repeated at 390 px for overflow. I moved the sliders of both simulations to their ends to read their ranges.
- I did not read `plan.md` or `check.md`. I read the chapter source `text/ch01.py` only to find where two broken numbers come from.

I read as two people at once:
- **S**, a school student who is good at mathematics.
- **G**, a physics graduate who builds electron-beam columns and is reading this as an applicant's portfolio.

Each item quotes the rendered text. Severity runs from **A** (a reviewer stops trusting the page) through **B** (wrong, or missing something the standard requires) to **C** (polish).

---

## The 10 most serious places

1. **§1.3, Example 1.1, and again in §1.9: the computed numbers are broken on the page.**
   - "The gap of −200 % is not a numerical error. … a spot at \(y_s=\)0.01795 m, within 200.0 % of the solver."
   - §1.9: "\(e/m=\theta E/(B^2l)=\)−1.7479 × 10¹¹ C/kg … The method returns it to 200 %. … Their product 0.99380 matches the measured ratio −0.99380 to 2.0."
   - §1.9 again: "against the 200 % deficit of the idealised model".
   - Cause: the solver puts \(\mathbf E\) along \(+y\) and \(\mathbf B\) along \(+z\) (the simulation's own labels say so), while §1.3 sets \(\mathbf E=(0,-E,0)\) and \(\mathbf B=(0,0,-B_p)\). The solver's spot therefore has the opposite sign, and every percentage built from it becomes ±200 %.
   - The intended statement is a 0.4 % gap explained by \(\gamma\), and it is lost. A reader who reads numbers stops trusting the page here, and the guide's promise "Every number in the text is computed by the page's own code and checked" turns against the author. (A)
2. **§1.1 Figure 1.1 and §1.3 Figure 1.2: the drawing contradicts the text.** The text says "it bends towards the positive plate", and §1.3 says "we call the upper plate positive for \(V_p>0\)". In both figures the red E-only path bends *down*. This is the same sign problem as item 1, and it is the first thing anyone sees in Chapter 1. (A)
3. **§0.3: the diffraction claim is wrong for a low-kV column.**
   - Quote: "This one number settles a question of principle: for electrons the diffraction limit of (0.1) is not what stops us."
   - The comparison is λ against the pitch, but (0.1) has the aperture in it. An electron probe has a semi-angle \(\alpha\) of order 5–10 mrad, not an NA near 1.
   - At 1 kV, \(\lambda/(2\alpha)\approx\) 2–4 nm and the Airy term \(0.61\lambda/\alpha\approx\) 2.4–4.7 nm. That is a sizeable fraction of a 10 nm line. Diffraction is one of the two dominant terms of a low-voltage probe (with chromatic aberration).
   - Figure 0.1 and the simulation repeat the error ("Λ/W = 0.00388"). A column builder will stop here. (A)
4. **§0.2 → §0.3: one symbol, two meanings, in consecutive paragraphs.**
   - \(p\) is the pitch in (0.1) ("period (pitch) \(p\)") and the momentum in "\(\lambda=h/p\) … \(p\) the momentum".
   - \(\lambda\) is the light wavelength in §0.2 and the electron wavelength in §0.3.
   - The simulation adds \(\lambda_{opt}\), \(d_{opt}\) and \(w\), none of which the text uses. (B)
5. **§1.5, Example 1.2: a wrong physical statement.**
   - Quote: "A deflection goes as \(1/v^2\), so a calculation that uses \(\tfrac12mv^2\) is off by 8.9 % for the column electron and by 0.59 % for the electron of the 2 kV tube."
   - The deflection goes as \(1/(\gamma m v^2)=1/(pv)\). For a fixed accelerating voltage the non-relativistic result \(El/(2V)\) is off by \((1+\epsilon)/(1+\epsilon/2)-1\): **2.85 % at 30 kV and 0.20 % at 2 kV**. I checked this numerically.
   - The 8.9 % and 0.59 % are \((v_{NR}/v)^2-1\). They leave out the \(\gamma\) in the momentum, which is exactly what Example 1.1 is about. (A)
6. **The simulation readouts in both chapters turn symbols into other symbols.**
   - The readout labels have CSS `text-transform: uppercase` applied to KaTeX, so the reader sees:
     - "Λ" for \(\lambda\);
     - "D<sub>OPT</sub>", "D<sub>OPT</sub>/W" and "Λ/W" in Chapter 0;
     - "R<sub>G</sub>", "Ω<sub>C</sub>", "X<sub>END</sub>" and "Θ<sub>END</sub>" in Chapter 1.
   - Λ is a different Greek letter, and \(R\) is already the coil radius of §1.6.
   - The Chapter 1 readouts also use \(r_g\) and \(\Omega_c\), while the text uses \(r_L\) and \(\Omega\). "ΔE/E" uses \(E\), which on this page is the electric field.
   - The two view titles of the Chapter 1 simulation overlap ("top view (x, y): E up, B out of the page" runs into "side view (x, z): B up").
   - The Ω<sub>C</sub> value is cut off ("1.76 × 10⁸ rad…"). (A)
7. **§1.6: a raw cross-reference label is printed on the page, and the next clause makes no sense.**
   - Quote: "The derivatives of the sum of two terms *eq : loop* vanish there".
   - In the source the token `‹eq:loop›` sits inside `\( \)`, so KaTeX typesets it as maths and the link is never resolved.
   - The same sentence goes on "so the field is uniform over a region that is long compared with the offset". This is the wrong way round: the Helmholtz field is uniform to fourth order over a region *small* compared with \(R\). (A for the visible label, B for the physics)
8. **The guide, §0.5, §1.2 and §1.11 make four different promises about a field solver.**
   - Guide: "No field solver: lens fields are an analytic model, not a finite-element or boundary-element computation."
   - §0.5: "leaves out a field solver for arbitrary electrodes beyond what chapter 4 builds".
   - §1.2: "Chapter 4 replaces it by a numerical solution of Laplace's equation for plates and lenses."
   - §1.11: "repaired by a field solver in chapter 4".
   - A column builder will ask which one is true. (B)
9. **§1.2: a wrong reason, and a list of questions.**
   - Quote: "The beam is so thin that its electrons do not push on each other". Thinness is not the reason. A thinner beam at the same current has a *higher* charge density. What matters is the small current (perveance).
   - The three checks are set as italic rhetorical questions with answers ("*Is the electron fast enough for relativity to matter?* …"). STANDARD forbids the question-and-answer format and rhetorical questions. (B)
10. **Overflowing equations hide terms with no visual cue.**
    - At 1440 px three display equations are wider than the column and scroll sideways without a scrollbar or a fade:
      - (1.16) is cut after "\(+(\mathbf u_{\perp0}\times\hat{\mathbf b})\)", so the \((1-\cos\Omega t)/\Omega\) term is invisible;
      - (1.20) is cut at "\(\mathbf k_3=\mathbf f(\mathbf y_n+\)", so \(\mathbf k_4\) is never seen;
      - (1.22) is cut at "\(\mathbf u_{n+1/2}=\mathbf u^++\)".
    - At 390 px, 22 displays and both tables of Chapter 1 overflow.
    - A reader of the printed page or a screenshot loses the end of three key formulas. (B)

---

## Reading guide (`#guide`)

Where a reader gets lost, or a claim is unsupported:
- "Each chapter … ends with a simulation whose sliders are the symbols of the formulas."
  - In Chapter 0 the sliders are \(V,\lambda_{opt},\mathrm{NA},w\). The text's symbols are \(p,\lambda,n,\alpha\).
  - In Chapter 1 the slider \(v_0\) replaces the text's \(V_a\). The angle \(\theta_0\) is the text's \(\alpha\) (§1.7) or \(\chi\) (§1.8).
  - So the promise does not hold.
- "Every number in the text is computed by the page's own code and checked against an independent Python version." Item 1 above shows the checks confirm that the two programs agree, not that the number makes sense. Reword the promise, or make the check catch sign and percentage nonsense.
- "Constants are CODATA 2018." G will ask why not CODATA 2022 (published 2024). Give the reason in one clause, or change the constants.
- "The last chapters connect all stages into one machine." The guide counts 10 chapters, but §0.5's road lists chapters 1–8. Chapter 9 is not named anywhere in §0.5.

Verdict: **needs work** (two promises contradicted by the chapters).

---

## Chapter 0, "The goal"

### §0.1 The question
- "every manufacturing step is followed by a measurement" overstates. Metrology samples selected steps and selected sites. G will notice.
- "The cubic cell of the silicon crystal is 0.543 nm … neighbouring atoms are 0.235 nm apart, so a line 10 nm wide is about 43 atoms across."
  - The line in question is a *metal* wire (a copper or ruthenium interconnect at 20 nm pitch), not silicon.
  - 0.235 nm is the bond length along ⟨111⟩, not the spacing of atoms along an arbitrary line.
  - Either measure a silicon fin, or use the metal's spacing.
- "IRDS 2022, *More Moore*, Table MM-7" has no link anywhere on the page.
- The coin-and-fingertip picture is good, and it is what STANDARD item 1 asks for.

Verdict: **needs work** (one wrong material, one overclaim, no link). The picture can stay as it is.

### §0.2 Why light is not enough
S gets lost:
- "the light leaves in directions \(\theta_m\) given by the grating equation \(p(\sin\theta_m-\sin\theta_i)=m\lambda/n\)". The equation is dropped in with no picture of where it comes from (path difference \(p\sin\theta\) between neighbouring lines).
- "The picture of the grating is carried by the interference of the orders." The one sentence S needs is missing: two plane waves at different angles interfere into fringes, and the period of those fringes is \(p\).
- "Tilt the illumination to the edge of the aperture." Why tilt? Say that straight-on light gives \(\lambda/\mathrm{NA}\), and tilting lets the −1 order use the whole aperture, which halves the limit.
- "numerical aperture", "refractive index", "immersion" and "through water" are all undefined. The index of water at 193 nm (1.44) is the "ceiling" the text names but never gives.
- Figure 0.1 says "ArF immersion". The text never says ArF.

G will object:
- The section argues about *imaging* resolution, using the numbers of *lithography scanners* (NA 1.35 water immersion, EUV 0.33/0.55). The conclusion is about *metrology*.
  - Optical inspection tools work dry at NA ≈ 0.9. The simulation's own default is NA 0.950 (giving 102 nm), not the 1.35 (giving 71.5 nm) of the text.
  - The section also admits that scatterometry measures below the Abbe limit ("infers a shape from what the whole target does to the light"). So the logic from "(0.1)" to "light is not enough" needs one sentence: imaging metrology is limited by (0.1); scatterometry is not, but it needs targets and models. As written, that sentence is only implied by a quotation.
- "It prints patterns; it is not a practical way to look at millions of them quickly on every wafer." This is an unsupported claim. Actinic EUV inspection exists for masks. Say why it is impractical for wafers (source power, cost, absorption) or cite a source.
- "Applied Materials describes this as …": which document? There is no link and no date.

Verdict: **needs work** (no physical picture of interference, a mix of lithography and metrology numbers, a text/simulation mismatch on NA).

### §0.3 Why electrons
Symbols used before they are defined:
- \(m\) and \(c\) appear in "\((pc)^2=T(T+2mc^2)\)" and are defined only in Chapter 1.
- \(e\) is used in "\(T=eV\)" two lines before "the charge \(-e\)".
- \(p\) changes meaning (see item 4 of the top 10).

Skipped steps:
- "\((pc)^2=T(T+2mc^2)\)" is given bare. One line from \(E^2=(pc)^2+(mc^2)^2\) with \(E=T+mc^2\) would let S follow. The forward reference to §1.5 helps G, not S.

G will object:
- The diffraction claim (item 3 of the top 10). Give the electron "NA" (\(\alpha\) ≈ 5–10 mrad) and compute \(0.61\lambda/\alpha\) at 0.5–1 kV. This is the honest number, and it is the reason the later chapters need aberration theory at all.
- "An ion … knocks atoms out of the surface …; an electron of the same energy mostly does not." The physical picture is missing.
  - The largest energy a 1 keV electron can hand to a Si nucleus is \(2E(E+2mc^2)/(Mc^2)\approx0.08\) eV. The displacement threshold is about 15–20 eV. So knock-on damage is not "mostly" absent, it is impossible.
  - Electron damage to resist comes from ionisation and bond breaking, which §0.4 then invokes. One sentence would separate the two mechanisms.
- "electrons of the surface layer, which carry the shape". Name them: secondary electrons, *made by the beam*, which escape from the top few nanometres. "Backscattered electrons" is undefined for S.
- "the lenses that focus electrons are much worse than glass lenses". Name Scherzer's theorem (round static lenses always have positive spherical and chromatic aberration). G expects it, and S gets a reason instead of an assertion.

Figure 0.1:
- The red group is titled "the structures to be measured" and contains "silicon crystal cell 543 pm". The crystal cell is a scale reference, not a structure to be measured.
- The figure has no electron aperture-limited length. That is the comparison that matters (see item 3 of the top 10).

Verdict: **needs work**.

### §0.4 What the machine has to deliver
S gets lost:
- "a source of finite brightness": brightness is undefined. Give the picture (current per area per solid angle), and the one relation \(I\approx B\,(\pi d^2/4)(\pi\alpha^2)\) that makes "a smaller spot means less current" a consequence rather than an assertion.
- "dwell time", "resist" and "landing energy" are undefined.
- Why the count fluctuates "by the square root of the number" (Poisson statistics) is not said.

Unsupported:
- "a clean edge needs thousands of counts" has no number behind it and no forward reference to Chapter 7.
- "two to three orders of magnitude better than for thermal sources": is this Applied Materials' claim or the author's? The quotation marks end before it.

Physical picture missing:
- "The beam must be gentle enough for fragile resist, which a fast electron damages."
  - What damages resist is the energy deposited per volume (dose × stopping power). A slow electron deposits all of its energy in the top tens of nanometres, so "slow = gentle" is not simply true.
  - *Charging* of insulating samples is missing entirely, and it is the other reason metrology columns land at a few hundred eV (the E2 crossover). G will notice that it is absent.

Units:
- "a vacuum 'well below' 10⁻¹¹ millibar" becomes "why a vacuum of 10⁻⁹ pascal matters" with no word that these are the same pressure. S will think they are two different numbers.

Tone (G, reading an applicant's portfolio):
- A long paragraph of the target company's marketing quotations ("10X increase in imaging speed", "95 %") is not checked against any physics.
- The disclaimer is correct. The paragraph would read better reduced to the three behaviours it is meant to motivate (cold tip bright but fragile, vacuum, deep high-energy mode), each with one sentence of physics and a linked source.

Verdict: **needs work**.

### §0.5 The road through the chapters
- The table lists chapters 1–8. The guide says there are 10 chapters. Chapter 9 is missing from the road.
- "The model leaves out a field solver for arbitrary electrodes beyond what chapter 4 builds" contradicts the guide (item 8 of the top 10).

Verdict: **needs work** (one sentence and one table row).

### Chapter 0 simulation, "The goal: why electrons"
- The caption says "the smallest half-pitch light can resolve". The text and Figure 0.1 say \(\lambda/2\mathrm{NA}\) is the smallest **period**. So "\(d_{opt}/w\) = 10.2" compares a period limit with a line width, and is off by a factor of 2 under either convention.
- The defaults (NA 0.950, so 102 nm) differ from the text's worked case (NA 1.35, so 71.5 nm), and no sentence explains why.
- The readout labels are uppercased into Λ, D<sub>OPT</sub> and W (item 6 of the top 10).
- On the ruler, the label "light λ" is partly hidden behind the "light: λ/2NA" marker line.
- STANDARD item 6 (equation to screen) is not met. The prose never mentions the simulation, and no sentence says which drawn mark is which symbol of §0.2–0.3.

Verdict: **needs work**.

### Chapter 0 against STANDARD as a whole
- Item 1 (picture): yes, the coin.
- Item 2 (model with numbers): partly.
- Item 3 (derivation): the Abbe limit is derived, but with the interference step missing; (0.2) is not derived here.
- Item 4 (checks): one consistency check against IRDS. There is no limiting case.
- Item 6: missing.
- Item 7: one paragraph.
- Item 8: no Sources list for Chapter 0 and no working links. Its sources are listed in Chapter 1 instead, again without links.
- Taylor form: no Key result box. Acceptable for an introduction.

---

## Chapter 1, "A free electron in fields"

### §1.1 A beam you can bend
- The CRT-and-magnet opening is a good human picture.
- Figure 1.1:
  - The path bends down, while the text says towards the positive (upper) plate (item 2 of the top 10).
  - The label \(x_s\) sits next to the deflected spot, as if it were the deflection. The caption says it is "the position of the screen".
  - \(x_a\) (used in §1.2) and \(x_p\) (used in (1.2)) are not marked.
- "Thomson's plates were about 5 cm long, 2 cm broad and 1.5 cm apart" has no page reference in the paper.

Verdict: **needs work** (figure sign and labels). The prose can stay as it is.

### §1.2 The model and where it holds
Symbols used before they are defined:
- \(x_a\) in "\(E=V_a/x_a\) for \(0<x<x_a\)" is never defined; it appears only as "\(d=x_a\)" in §1.6.
- \(\varepsilon_0\) appears in "\(P=e^2a^2/(6\pi\varepsilon_0c^3)\)" one line after \(\epsilon=eV_a/mc^2\). Two epsilons in one paragraph, one of them undefined.
- \(r_L\) and "the balancing field of §1.3" are used before §1.3 defines either.
- "wave packet" is not explained for S.

Unsupported or wrong:
- "The beam is so thin that its electrons do not push on each other" (item 9 of the top 10).
- "for plates with \(d/l=\)0.3 these reach well into the gap. This is the largest simplification of the tube model."
  - Fringe fields reach *beyond the ends* of the plates, not into the gap.
  - No number backs "largest". One line would: the effective length of the plates is \(l+\) (a fraction of \(d\)), roughly a 10–20 % change in deflection at \(d/l=0.3\).
  - §1.9 later offers fringe fields as a candidate for Thomson's factor of 2, so the size matters.
- "As long as the fields change over distances much larger than λ, the wave packet follows the classical path." The criterion is incomplete. Diffraction at the anode slit is the relevant quantum check for a beam. Compare λ with the slit width and give the angle.

Form: the three italic questions (item 9 of the top 10).

Verdict: **needs work**.

### §1.3 Slow electrons: the pencil-and-paper version
Symbols used before they are defined:
- \(x_p\) in (1.2), "\(L=x_s-x_p-l\)", is never defined. It is the position of the plate entrance, and Figure 1.2 uses 60 mm for it without saying so.
- \(B_p\) in "\(\mathbf B=(0,0,-B_p)\)": what does the subscript mean?
- \(\varphi\) here is the turning angle. In §1.4 it is the electrostatic potential, and in §1.8 the Boris rotation angle.
- \(L\) here is the drift length. It is the Lagrangian in §1.4 and the focal distance in (1.18). STANDARD asks for one symbol, one meaning.

Physical picture missing:
- The key insight of the tube is not stated. With \(mv_0^2=2eV_a\), (1.1) gives \(\tan\theta=El/(2V_a)\), *independent of \(e/m\)*. Electrostatic deflection of particles accelerated from rest does not depend on their mass. That is why Thomson needed the magnetic field, and why a column builder distinguishes electrostatic from magnetic optics. It is one line, and it belongs here.

Skipped or confusing steps in Example 1.1:
- It computes \(\tan\theta\) from the non-relativistic (1.1) with the *relativistic* \(v_0\) ("2.645 × 10⁷ m/s, which we use from here on"). The result, 0.08382, is neither the non-relativistic answer (\(El/2V_a=0.08334\)) nor the relativistic one (0.08350).
- The clean comparison is 0.08334 against 0.08350, a gap of 0.19 %. The hybrid confuses S, and G wonders why.
- Then come the ±200 % numbers (item 1 of the top 10).
- "The computed spot with that field on is at \(y_s=\)−1.58 × 10⁻⁸ µm": write 1.6 × 10⁻¹⁴ m, or "zero to 10⁻¹⁴ m".

Circular references:
- "This is Thomson's second method (§1.9)", while §1.9 says "the crossed-field method of §1.3".

Figure 1.2: the E-only path goes down (item 2 of the top 10). "x from 50 mm to 300 mm (plates 60 mm to 110 mm)" is the only place where \(x_p\) = 60 mm can be found.

Verdict: **needs work**.

### §1.4 From Newton to a Lagrangian ★
- The derivation is complete and checked. The ★ convention is honoured: "(1.8) and (1.7), with their meaning, are all a reader needs from it."
- "which enters \(L\) with a minus sign just as \(V\) does in \(L=T-V\)". \(V\) is the voltage everywhere else on this page, and \(T\) the kinetic energy (and later the period). Use \(U\) for the potential energy.
- "Chapter 4 will use \(\mathbf p\), not \(\gamma m\mathbf v\), where a symmetry of the lens fixes a conserved quantity." G expects the name: Busch's theorem (conservation of canonical angular momentum \(p_\theta=\gamma m r^2\dot\theta+qrA_\theta\)). Name it here.
- "the only invariant that is linear in the potentials" is true only up to a total derivative. That is fine for S, and G will let it pass.

Verdict: **clear, leave it**, except for two small fixes: the symbol \(V\) and the name of Busch's theorem.

### §1.5 Energy, and why a magnetic field does no work
- The *unstarred* "Energy conservation" paragraph starts from "Hamilton's equations give \(\mathrm dH/\mathrm dt=\partial H/\partial t\)". \(H\) exists only in the starred part, so a reader who skipped the ★ has nothing to stand on. The work–energy route (\(\mathrm d(\gamma mc^2)/\mathrm dt=q\mathbf E\cdot\mathbf v\)) is given a paragraph later. Lead with it unstarred, and leave the Hamiltonian as the ★ confirmation.
- "The magnetic field never appears in \(H=\gamma mc^2+q\varphi\)". It does appear in (1.9), through \(\mathbf A\). Say "the *value* of \(H\) contains no magnetic term".
- "the energy it has gained is exactly \(eV\), and that is the definition of the unit electron volt". The unit is the energy for \(V=1\) V.
- Example 1.2: the deflection error (item 5 of the top 10).
- (1.11), (1.12) and the table all check out: I re-derived \(23/32\) and the 30 kV row.
- The stone-on-a-string picture is good.

Verdict: **needs work** (one wrong claim, one ★ dependency).

### §1.6 Where the fields come from
- The raw label "eq : loop" and the backwards uniformity statement (item 7 of the top 10).
- Biot–Savart: "the axial component carries the factor \(R/r\)". S needs the picture of the loop, the cone of \(\mathrm d\mathbf B\) vectors and the angle. No figure is given, and a single sentence of geometry would do.
- \(I\) is the current here and becomes \(I=H\rho\) in §1.9 (Thomson's notation), with no warning. \(R\) is the coil radius here and becomes the RK4 factor \(R(\mathrm i\theta)\) in (1.21).
- "Thomson's coils were of this type": unsupported. Where in the paper?

Verdict: **needs work**.

### §1.7 A uniform axial field: the helix
- (1.16) is cut off on screen (item 10 of the top 10).
- \(\Omega\) is redefined: in (1.3) it is \(eB/m>0\); in (1.15) it is \(qB/(\gamma m)\), "negative for the electron". The page also uses \(|\Omega|\). Say once that (1.15) supersedes (1.3).
- \(T\) here is the period. In §0.3 and §1.5 it is the kinetic energy.
- \(\alpha\) here is the angle to the axis. In §0.2 it is the aperture half-angle, and §1.8 uses \(\chi\) for the same kind of angle.
- The complex-number step \(w=u_x+\mathrm iu_y\) is unstarred. S may not know it. Either star it, or add "a number that turns in the complex plane is a vector that turns in the page".
- "it twists the beam by the angle it gains while crossing" is too vague for S and too vague for G (Larmor rotation, \(\theta_L=\int\Omega/2\,\mathrm dz/v\)). Name it, or drop it.
- The physics is right: I checked \(L\) = 0.2367 m and \(r_L\) = 2.26 mm. The "same time for every angle, hence a lens" picture is the best physical idea in the chapter.

Verdict: **needs work** (symbols and one cut equation). The core can stay as it is.

### §1.8 Following the electron on a computer: Runge–Kutta and Boris
- (1.20) and (1.22) are cut off on screen (item 10 of the top 10).
- New symbols collide with old ones:
  - \(\theta=\Omega h\) (the third \(\theta\));
  - \(a=qh/(2m)\) (\(a\) was the acceleration);
  - \(\mathbf t\) (with time \(t\) in the same equation);
  - \(\varphi\) (the third \(\varphi\));
  - \(R\) (the coil radius);
  - \(\chi\).
- "which makes the scheme symmetric in time and therefore of second order": the reason is asserted. One sentence (a symmetric one-step method has an even error expansion) would satisfy G.
- "the electron has lost half its energy after 867 turns". It is half of the *transverse* energy \(u_\perp^2\), as the previous sentence says. The kinetic energy as a whole loses less.
- "Qin and co-workers … explain why [the energy error stays bounded], from the fact that the step preserves phase-space volume". This overstates the paper. Qin et al. prove that the method preserves volume. Bounded energy error is observed, not proved by volume preservation, and drift has been reported in some non-uniform fields.
- Key result: "We use … Boris for the many-turn paths of later chapters". Which paths in a metrology column make many turns? Primary electrons do not. Say which ones (secondary electrons in an immersion-lens field, for example), or drop the clause.
- Key result: "its error is a phase error that does not distort the shape of the orbit", while (1.24) says the radius is 1.9 % too large at 16 steps per turn. The radius error is fixed, but it is a shape error.
- G will also ask why a fixed-step time integrator is used rather than an adaptive RK45 or the paraxial ray equation in \(z\). Those are the standard tools of electron optics. One sentence on the choice would satisfy STANDARD item 5.
- The table prints "16.0", "32.0", "64.0" for the integers \(N\), but "128", "256", "512".
- Figure 1.4:
  - Both legend dots are the same dark grey. The legend shows no line style, so Boris (red, solid) and RK4 (black, dashed) can be told apart only by reading the slope.
  - In the right-hand panel, the label "Boris: rounding noise, about 1e-16" is crossed by the curve's dip at \(N=64\).
- The measured slopes (−2.00, −3.98, −5.00) and the prediction columns are exactly what STANDARD item 5 asks for. This is the strongest part of the chapter.

Verdict: **needs work** (rendering, symbols, two overstated claims). The method and the error test can stay as they are.

### §1.9 Thomson's tube, simulated and compared with Thomson's data
- The ±200 % numbers and "−1.7479 × 10¹¹ C/kg" (item 1 of the top 10).
- "\(\arctan y/y\)": \(y\) is a coordinate everywhere else. Here it is \(\tan\theta\).
- "it gives \(m/e=I^2Q/2W\) with \(I=H\rho\)". The step S needs is skipped. With \(W=N\cdot\tfrac12mv^2\), \(Q=Ne\) and \(\rho=mv/(eH)\), it is one line. Also define \(W\), \(Q\) and \(H\) explicitly.
- Figure 1.5: "Each dot is a row of his tables. Triangles mark the mean of each row." The triangles are the mean of each *group* (method and tube), not of each row. The axis label repeats the error.
- "Thomson's rows of the first method spread over a factor 3.1, … against the 200 % deficit of the idealised model". The comparison sentence depends on the broken number.
- `data/ch01/thomson1897.json`, `derive/ch01.py` and `ref/ch01.py` are file names, not links. A reviewer cannot open them from the page.
- The honest handling of what Thomson's paper does and does not say ("not stated in the paper text that we read, and we have not tested a cause") is good practice. Leave it as it is.
- STANDARD item 6 (equation to screen):
  - The simulation is not "Thomson's tube". It shows unbounded uniform fields with no plates and no screen. Its \(\mathbf E\) and \(\mathbf B\) point the opposite way to §1.3, and nowhere does the text say so.
  - The slider is \(v_0\) (Mm/s) where the text works with \(V_a\) (kV). The reader must convert 2 kV to 26.45 Mm/s by hand.
  - The default run (36 ns) is labelled "the plate transit time in Thomson's tube", which is 1.89 ns in Example 1.1.

Verdict: **needs work**.

### §1.10 Checked by computer algebra
- "A claim is never marked PASS because a number looked right." True of the SymPy table. The text then claims the prose numbers are checked by identical strings in two programs, and the same prose prints −200 %. The section should say what the number check proves (agreement between two implementations) and what it does not (physical sense, sign conventions).
- No links to the scripts.

Verdict: **needs work** (one paragraph).

### §1.11 What the model leaves out, and what we pass on
- "Spin and radiation: negligible here, with 4.6 × 10⁻¹⁷ of the energy radiated." Radiation is estimated; spin is not. Give one line: the spin force \(\nabla(\boldsymbol\mu\cdot\mathbf B)\) against \(evB\) over the beam width.
- The field-solver promise contradicts the guide (item 8 of the top 10).
- The hand-over to Chapter 2 lists four items, three of which go to chapters 3 and 4. Title it "What this chapter passes on".
- Problem 4: "Answer: at least 70.2 steps, which is rounded up to the next whole number." Say 71.
- Sources:
  - None of the sources is a link. The Giunta URL is printed as text.
  - "the textbooks they follow … were not re-read for this chapter" is honest, but STANDARD item 8 says "only real sources you opened and read … each with a working link". Either open them or move them to a "Background" line.
  - IRDS and Applied Materials have no URLs.

Verdict: **needs work**.

### Chapter 1 simulation, "An electron in uniform E and B"
- The view titles overlap. The readouts are uppercased into wrong symbols, and "Ω<sub>C</sub>" is truncated (item 6 of the top 10).
- The slider ranges are E 0–1000 kV/m, B 0–100 mT, \(v_0\) 0.1–290 Mm/s, \(\theta_0\) 0–180°, \(t_{run}\) 0.1–2000 ns and Δt 0.001–1000 ps, so the worked example can be reached. The page never gives the slider settings for it.

Verdict: **needs work**.

---

## Summary of verdicts against `notes/STANDARD.md`

| section | verdict | main reason |
|---|---|---|
| Guide | needs work | promises contradicted by Ch 0–1 (numbers checked; sliders are the symbols; field solver) |
| 0.1 | needs work | silicon used for a metal wire; "every step measured" |
| 0.2 | needs work | no interference picture; lithography numbers for a metrology argument; NA differs from the simulation |
| 0.3 | needs work | electron diffraction compared without the aperture; \(p\) and \(\lambda\) reused; \(m,c,e\) undefined |
| 0.4 | needs work | brightness undefined; charging absent; mbar and Pa switched |
| 0.5 | needs work | chapter 9 missing; field-solver contradiction |
| Ch 0 simulation | needs work | half-pitch versus period; Λ and D<sub>OPT</sub> labels; not tied to the text |
| 1.1 | needs work | Figure 1.1 bends the wrong way; \(x_s\) label |
| 1.2 | needs work | wrong reason for no space charge; Q&A form; \(x_a\), \(\varepsilon_0\) undefined |
| 1.3 | needs work | ±200 % numbers; \(x_p\), \(B_p\) undefined; \(e/m\)-independence of \(\theta\) not said |
| 1.4 ★ | clear, leave it (two small fixes) | rename \(V\) to \(U\); name Busch's theorem |
| 1.5 | needs work | wrong 8.9 % / 0.59 % claim; unstarred text depends on ★ |
| 1.6 | needs work | "eq : loop" printed; backwards uniformity claim |
| 1.7 | needs work | (1.16) cut off; \(\Omega\), \(T\), \(\alpha\) reused |
| 1.8 | needs work | (1.20) and (1.22) cut off; symbol collisions; Qin overstated |
| 1.9 | needs work | ±200 %, negative \(e/m\); Figure 1.5 caption; simulation is not the tube |
| 1.10 | needs work | says what the number check proves, but not what it does not |
| 1.11, Problems, Sources | needs work | no links; spin unestimated |
| Ch 1 simulation | needs work | overlapping titles; wrong symbol case; field directions opposite to the text |

# Referee report · Fig. 12, "Why the pint spills, and how a motor can stop it"

Page: `public/simulations/beer-slosh.html`. Served with `node notes/fig12/serve.cjs 8790` (it serves `public/` with Cloudflare's headers, so no
Vite build is needed for this page). Opened in headless Chromium (Playwright). I pressed "Expand all", stopped the headers from pinning so
every slice reads cleanly, and took screenshots at 1400 px (31 slices), 1024 px and 390 px. The text was read from the rendered DOM, with the
KaTeX source of every formula.

**Version read.** The note was being edited while I read it: `beer-slosh.html` changed at 18:44:49 UTC on 6 November 2026, adding the
steps of (17) and (18), the Lagrangian of section 6.3, the derivation of (38), the transmissibility of (40) and the flux form of (46). This
report is about that version, which had not changed again when I checked last.

Two readers speak below. **S** is a school student who is good at mathematics. **G** is a physics graduate. Each point gives the section and
the sentence, then the reason. Every number I quote was recomputed by hand or in Python, or measured in the browser.

---

## The most important problems first

1. **Section 6.1, equation (22) is cut off at every screen width.** The display "the line from the contact point to the axle is normal to the axle
   path \(z_a(x)\)." loses its ending: at 1400 px it reads "…the axle path z_a(x" and at 390 px "the line from the contact poir (22)". The
   line-breaker cannot break one long `\text{}`, and the row clips it. The key statement of that subsection is therefore unreadable. Fix: put
   it in the prose, or shorten it to a formula (for example \((\mathbf x_\text{axle}-\mathbf x_\text{contact})\cdot(1, z_a') = 0\)).
   At 390 px, (34), (38), (46) and (47) are also clipped on the right. The new unnumbered \(P_x\) display in 4.5 breaks so that "k sinh kh"
   overlaps the next line. The screenshot is `bad390_all.png` in the scratchpad.
2. **Section 5 contradicts section 13.** Section 5 says: "Over a 25 mm bump in open loop it is 6.3 m/s², \(\mathrm{Fr} = 0.64\)". The table of
   section 13 gives 3.58 m/s² for that run, which is Fr = 0.36. The 6.3 is probably left over from before the fix of 6 November to the
   short-step problem described in 11.7. Rerun `study.cjs 25 off 0` and correct the sentence.
3. **The ★ promise is broken for sections 4 and 11.** The byline says "★ marks the heavier mathematics, whose results are restated without
   it", but no unstarred passage restates the results of section 4: the frequency formula (16), the oscillator (17) with its β, and the
   swinging mass \(m_1 \approx 85\) g. Sections 5, 8.3, 10.2 and 12 depend on them. Section 11 has no plain summary either. Its main facts are
   about 25 000 particles on a 4 mm grid, 5 ms steps, first order in time, and a swing that is 4–6 % too slow. A reader who skips 11 meets
   "grid", "cell", "4 mm grid", "Δx" and "particles" in 4.6, 5, 10.1, 12 and 13 with no definition (they are defined only in 11.2–11.3).
   Fix: put a two- or three-sentence "what to take away" paragraph, unstarred, at the end of 4 and of 11, and define "grid" and "cell" in one
   clause in section 1 or 2.
4. **The tuning argument has a step missing (4.5 → 1, 6.6, 8.3).** Section 1 says "it is excited most strongly by a jolt that lasts about as
   long as one swing". 4.5 says "A push that changes on the time scale \(1/\omega_{11}\) excites the swing most". 6.6 says "its spectrum
   peaks near \(v/L = 4\) Hz". 8.3 then measures "the Fourier amplitude … at the swing frequency". The step that links (17) to these is never
   written. After a push of finite length, (17) leaves a free swing of amplitude
   \(|q| = (\beta/\omega_{11})\,|\hat a(\omega_{11})|\), with \(\hat a(\omega) = \int a\,e^{-i\omega t}dt\) (Duhamel). One line would show G
   why the Fourier amplitude is the right measure, and why S should believe the doorstep story.
   The 6.6 claim also needs correcting. One cycle of a sine of length \(T = L/v = 0.25\) s has its spectrum peak at \(0.84/T = 3.35\) Hz, not at
   \(1/T = 4\) Hz (my computation). That is even closer to the swing, so the conclusion is stronger. For a fixed peak push, the residual swing
   is largest when \(T \approx 1.13\) periods, which supports section 1.
5. **Numerical method, standard item 5: the cart's integrator is never named.** 6.4 says "The residue is the first-order error of the
   integrator (section 11)", but section 11 describes only the fluid. The code (`stout-cart.js` l. 1218, 1242) steps the cart with symplectic
   Euler at \(h_\text{cart} = 0.1\) ms. The note says so only as "substeps of at most 0.1 ms" in 10.2. The time-step error of the fluid is not
   measured either: every check in section 12 runs at Δt = 5 ms and only the grid is refined. The note says "first-order accurate in Δt"
   (11.7) without a number. Fix: one sentence naming the cart integrator, its order and step, and one Δt-halving run of `check.cjs cylfreq`.
6. **Section 14 maps only the stout to symbols (standard item 6).** For a reader meeting vehicle dynamics for the first time, the cart is half
   the picture. Nothing says which drawn spring is \(k\), which dashpot is \(c\), what the wheel radius on screen is (\(R_w\)), where \(z_b\)
   and \(z_w\) are measured from, what the ground ticks mean ("5.5 m" in the screenshot), or how the drawing differs from the model. Section 6
   also has no picture of the quarter-car with its three coordinates. G can do without one; S cannot see what "the body slides straight up and
   down on the axle" looks like.
7. **Source 7 (Karnopp, Crosby, Harwood) was not read and has no link.** Standard item 8 allows "only real sources you opened and read, each
   with a working link". Section 9 cites it for the skyhook idea. That paper is about *semi-active* force generators, which can only
   dissipate. The page's actuator is fully *active*: "it can push and pull, and it supplies whatever power the law demands". G will notice that
   the note never draws this distinction. Either find and read a source on active skyhook control, or keep Karnopp et al. only as a historical
   remark marked "not read" and outside the reading list.
8. **One symbol, one meaning (verdict of 21 October) is broken in many places.** See the table at the end. The worst cases are \(h\) (fill depth,
   then the cart step in (34)), \(r\) (radial coordinate, then a particle radius in (48)), \(\theta\) (polar angle, then the surface fraction
   in 11.5), \(q\) (mode height in 4.5, generalised coordinate in 6.3, scaled pressure in (46)), and \(i\) (current, imaginary unit in 9,
   grid-node index in (47)).

---

## Section by section

### Abstract and byline
- "the dispersion relation \(\omega^2 = (g\xi/R)\tanh(\xi h/R)\)": \(\xi\), \(R\) and \(h\) are used without definition. G can guess them; S cannot. In
  an abstract, "(\(\xi = 1.84\), a Bessel-function zero)" is enough.
- "swinging at its own frequency, about 3.4 times a second": the page shows 3.21–3.26 Hz (4.6). A reader who counts on the page will get 3.2.
  Section 4.6 explains the gap, but the abstract should say "about 3.2–3.4".
- The byline's ★ promise is not kept (main problem 3).

### 1 · Over the doorstep · verdict: clear, leave it
Warm, physical, and well motivated: the bus, the spirit level, the waiter. Only one small point. "And it is excited most strongly by a jolt
that lasts about as long as one swing" is asserted here and never derived (main problem 4). Once 4.5 carries the Duhamel line, add "(section
4.5)" after the sentence.

### 2 · The glass and the stout · verdict: clear, one small fix
- "Its inner outline was measured from the drawing … radii so that the widest outer diameter is 85 mm": the note does not say how the *inner*
  radius follows from a scaled *outer* diameter, that is, whether the wall thickness was scaled too or kept. That is one clause.
- Source [2] is titled "Irish Imperial Pint Glass" but is described as "a 16 oz glass" and "the smaller US glass". S will stumble on the
  title. Say once that the page carries that name while its dimensions are those of a 16 oz glass.
- Figure 1 is good: it is plotted from the stored profile, and its labels match the text.

### 3 · The stout in the glass's frame · verdict: needs work (small)
- 3.1, "The glass never turns: the body slides straight up and down on the axle and the cart has one wheel, so it cannot pitch." This does not
  follow. A one-wheeled vehicle pitches more easily, not less, as a unicycle shows. That the cart cannot pitch is an *assumption* of the model:
  the body is guided to stay level. Say so. "Body" and "axle" are also used here before section 6 introduces them.
- 3.2, "on which the surrounding stout exerts the pressure force … and the viscous force … gives the incompressible Navier–Stokes equations":
  gravity \(\rho\mathbf g\,dV\) is part of \(\mathbf F\) but is left out of the list, and S will wonder where \(+\mathbf g\) in (4) comes
  from. G will also want "\(\rho\nu\nabla^2\mathbf u\) is the viscous force *for an incompressible Newtonian liquid*".
- 3.2, "the speed of sound in it is about 1.5 km/s": the reason this matters is not stated. Add "so flow speeds are \(10^{-4}\) of it".
- 3.3, (6): the normal \(\mathbf n \propto (\cos\theta, \sin\theta, -R')\) is the wall's. On the floor \(z = 0\) the normal is \((0,0,-1)\),
  and the line suggests one normal for both.
- 3.5, "so \(h_c = h\) … This holds for any glass shape": the plane and its slope hold for any shape. \(h_c = h\) holds only to first order when
  \(R\) varies with \(z\). The Key result ("whatever the glass's shape") leaves out "for a small slope, to first order in \(a/g\)", which the
  derivation needs.
- Example 3.1 checks out: 7.97 mm, −0.877 mm, −0.815 mm.

### 4 · Linear sloshing in an upright cylinder ★ · verdict: needs work
The algebra is now right and complete. I re-derived (11)–(19): Lommel's integral, \(\int r^2J_1 = R^3J_1(\xi)/\xi^2\),
\(\beta = 2\xi\tanh/(\xi^2-1)\), \(P_x = \rho\pi R^3\dot q/\xi^2\), \(m_1 = 91.4\) g, the steady-state fraction 0.837, and Example 4.2's
0.0554 kg, 0.209 N and 0.0834 m/s². These problems remain:
- **No unstarred restatement** (main problem 3).
- 4.1: "(i) The swing is slow and wide compared with the thin layer": "slow and wide" is vague. The quantity meant is \(\delta/R\) (or
  \(\mathrm{Re}^{-1/2}\)), and section 5 supplies it. Say "the layer is thin, \(\delta/R \approx 0.008\)".
- 4.2: "where \(C(t)\) can be absorbed into \(\phi\)", followed by "choosing \(C\) so that the stout at rest is undisturbed". Once \(C\) is
  absorbed into \(\phi\) there is nothing left to choose. Keep one of the two.
- 4.2: "We have dropped \(a_{g,z}\): a vertical acceleration multiplies \(\eta\) and so enters only at second order". This is only true if
  \(a_{g,z} \ll g\). On the page's own 10 mm bump \(|a_{g,z}|\) reaches 3.74 m/s² (\(0.38g\)), and on 25 mm 9.39 m/s² (\(0.96g\)), per
  section 13. By section 9's own factor \(\sqrt{1 + a_{g,z}/g}\), that changes the frequency for a moment by 17 % to 40 %. The argument
  (vertical shaking does not build up a swing from one bump) is sound, but "second order" is the wrong reason. Say "small while
  \(|a_{g,z}| \ll g\); on the page it is not small, but it lasts too short a time to matter (section 9)".
- 4.3: S has not met the Laplacian in cylindrical coordinates, and Bessel's equation is named but never written. One display,
  \(\nabla^2 = \partial_r^2 + r^{-1}\partial_r + r^{-2}\partial_\theta^2 + \partial_z^2\), and the equation \(f'' + f'/r + (k^2 - m^2/r^2)f = 0\),
  would make (14) readable. "The solution finite on the axis is \(J_m\)" silently drops the second solution. Name \(Y_m\) and say it diverges at
  \(r = 0\).
- 4.5: the two new derivation displays are **unnumbered**, as are the new displays in 6.3, 8.3 and 11.2 (standard: "equations numbered").
- 4.5: "A push that changes on the time scale \(1/\omega_{11}\) excites the swing most": the step is missing (main problem 4).
- Example 4.2, last sentence: "The linear theory of a cylinder predicts the stout's push on the cart computed by the three-dimensional solver
  in the tulip to within 1 %." This overstates the test. The amplitude \(q\) was *measured*, so the agreement tests the momentum–lean relation
  (18) and the cart's response to it, not the oscillator (17). Say "the push computed by (18) from the measured lean agrees with the cart's
  measured ripple to within 1 %". Section 12 already words it this way.
- 4.6: "on grids of 5, 4, 3 and 2.5 mm" is the first time S meets "grid" (main problem 3).
- 4.6: the corrected tulip frequency from the 5 mm grid, \(3.119/0.916 = 3.405\) Hz, is left out of "three grids agree". It agrees too, so
  "four grids" is the stronger statement.
- Problem 2 now asks the reader to derive (18), which the text has just derived in full. Replace it or drop it.

### 5 · Dimensionless numbers and damping · verdict: needs work
- "Over a 25 mm bump in open loop it is 6.3 m/s², \(\mathrm{Fr} = 0.64\)": this contradicts section 13 (main problem 2).
- "\(\mathrm{Fr} = a/g\), a Froude number for the forcing": G knows the Froude number as \(U/\sqrt{gL}\). Calling \(a/g\) a Froude number is
  unusual, so either say "a forcing ratio (some authors call it a Froude number)" or give it no name.
- "The energy lost in the layer per cycle, compared with the energy of the swing, scales as \(\delta/R\)": this is the key physical step, and
  it is stated without the two lines behind it. Dissipation per unit area is \(\sim\mu U^2/\delta\). Over the wetted area \(\sim R^2\) and one
  period \(2\pi/\omega\), compared with the kinetic energy \(\sim\rho U^2R^3\), the ratio is \(\nu/(\omega\delta R) \sim \delta/R\).
- "one thirteenth of a 4 mm cell": "cell" is undefined at this point.
- The tulip's numerical damping is 0.030, 0.008, 0.002 and 0.005: it does not decrease with the grid, and the text passes over this. One
  clause ("it scatters, like the tilt, see section 12") would do.
- Checked: Bo = 64.3, a frequency shift of 0.77 %, ℓ_c = 2.7 mm, Re = 3.1×10⁴, δ = 0.31 mm, the group 0.0064, and ζ = 0.0036 and 0.0053.

### 6 · The cart as a quarter-car · verdict: needs work
- (22) is cut off on screen (main problem 1).
- There is no figure of the model (main problem 6). "The body slides straight up and down on the axle" leaves S with no picture of the
  mechanism.
- 6.2: the tyre is "a stiff radial spring", but (23) compresses it *vertically*, by \(z_a - z_w\), and then tilts the force along the normal.
  That is a modelling choice. Say so in one clause, since it is what makes (24) exact for the potential \(U_t\).
- 6.3: "The gearbox multiplies the rotor's inertia by \(N_g^2\), once because the rotor turns \(N_g\) times faster and once because its energy
  goes as the square of that". This counts the same factor twice. The clear version is that the rotor must be spun \(N_g\) times faster, and
  the torque that does it is multiplied by \(N_g\) on its way to the road. Or, by energy: the rotor turns \(N_g\) times faster, and kinetic
  energy goes as the square of speed, so \(J_mN_g^2\).
- 6.3, the new Rayleigh function \(\mathcal D\) contains \(\tfrac12c_t(\dot z_a - \dot z_w)^2\) without the lift-off cut \(\max(0,\cdot)\) of
  (23). While the wheel is in the air the tyre damper must give nothing. One clause.
- 6.3 uses \(q = x, z_b, z_w\) for generalised coordinates, but \(q\) is already the mode height (4.5) and is the scaled pressure in (46).
- 6.4, "\(E = 4.366\) J": the zero of the potential energy is not given, so the number cannot be checked. Name the reference, or quote only the
  drift.
- 6.4, "The residue is the first-order error of the integrator (section 11)": the cart's integrator is not in section 11 (main problem 5).
- 6.4: "over a 25 mm bump on which the wheel leaves the road", but section 13 says "In none of these runs did the wheel leave the road". The
  first is the lossless test with the dampers off, the second the page's runs. S will see a contradiction unless 6.4 says "(dampers off)".
- 6.6: "its spectrum peaks near \(v/L = 4\) Hz" should be about 3.35 Hz (main problem 4).
- Checked: \(M_x = 2.502\) kg, 2.77 Hz and 41.7 Hz, ζ = 0.118, 31.5 mm and 1.1 mm, curvature radius 127 mm, slope 0.126, and 1.10 m/s².

### 7 · The DC gear motor · verdict: needs work (small)
- "Multiplying the first equation by \(i\) shows why one constant \(K_m\) serves both". As written this is circular, because (32) already uses
  one \(K_m\). The argument G expects: write \(e = K_e\omega_m\) and \(\tau_m = K_\tau i\); the power balance
  \(e\,i = \tau_m\omega_m\) (no loss in the conversion) then forces \(K_e = K_\tau\).
- (34): "\(\operatorname{clip}(i_\text{cmd}, \pm I_\text{max}, [\ldots])\)": clipping to two intervals at once is not standard notation. Define it
  ("to the intersection of the two intervals"). At 390 px (34) is clipped on the right.
- "updated exactly over each cart step (\(i \leftarrow \ldots e^{-h/\tau_i}\))": here \(h\) is the cart step, while everywhere else \(h\) is
  the fill depth, 125 mm. Use \(h_\text{cart}\) or \(\delta t\).
- Example 7.1 checks out: 5 V, 3.5 A against 3 A, 15 N, 6.0 m/s², 0.40 A, 2.4 m/s.

### 8 · The speed loop, and why it calms the stout · verdict: needs work (small)
- The imaginary unit is \(j\) here (\(L(j\omega)\), \(S(j\omega)\)) and \(i\) in section 9 (\(e^{i\omega t}\)), and \(i\) is also the current.
  Choose \(j\) throughout, as engineers do, because the current owns \(i\).
- "We take \(\omega_c = 2\pi\times 8\) Hz, well above the stout's swing": the lower bound is explained, the upper bound is not. Say what stops a
  faster loop: the current lag of 2 ms, the 1 ms sampling, the 3 A limit. Example 8.1 has the numbers (phase margin 70°), but the reason is not
  given in words.
- Key result: "The motor absorbs the jolt before the glass feels it". The glass still feels 39 % of it (\(|S| = 0.39\)). Say "most of the
  jolt".
- 8.3: "The open loop's forcing at the swing frequency is larger than that, because the swinging stout feeds its own push back … this is an
  inference". This can be quantified from numbers already in the note. A ripple of 0.083 m/s² at its own frequency over about 1.7 s adds
  \(\approx A\,D/2 \approx 0.07\) to the open-loop Fourier amplitude of 0.164. That roughly accounts for the gap between 0.28 and 0.39. Add the
  line.
- (38) is clipped at 390 px.
- Checked: \(K_p = 25.1\), \(K_i = 316\), poles −21.0 and −30.0 (damping ratio 1.02), \(|S(j\omega)| = 0.386\) at 3.21 Hz without lags.

### 9 · The skyhook suspension · verdict: needs work (source)
- Karnopp et al. was not read and concerns semi-active devices, while the page's actuator is active (main problem 7).
- "the largest vertical acceleration of the glass falls from 3.74 to 1.48 m/s²": section 13 calls this "heave", and no section defines the word.
  Define it here ("heave, the up-and-down motion").
- "Why the skyhook does not calm the lean" is a good physical argument (parametric resonance needs \(2\omega\) shaking kept up), and it should be
  the place that 4.2 points to (see above).
- Checked: \(c_\text{sky} = 47.6\), ζ = 0.82, \(T(10\ \text{Hz}) = 0.111\), 0.100 and 0.453.

### 10 · The stout pushes back, and spills · verdict: clear, small fixes
- (42)–(44) are correct. I re-derived the variable-mass balance, and the reason for counting \(\mathbf P_\text{spill}\) is given physically.
- 10.1, "The page measures \(\mathbf P = 2m_p\sum_p\mathbf u_p\) from its particles": first mention of particles in the body text, defined
  only in 11.3.
- 10.2, "Such an explicit (staggered) coupling can become unstable when the lagged mass is comparable with the structure's": this is the
  added-mass instability of partitioned fluid–structure coupling. It is stated without a source. Cite one you have read, or keep it as the
  inference it is.
- 10.3, "outside the rim's radius, \(r > R_\text{rim}\)": \(R_\text{rim}\) has not been defined (it is \(R(z_\text{rim}) = 37.5\) mm, section 2).

### 11 · Solving the equations ★ · verdict: needs work
- No unstarred summary (main problem 3).
- The cart's integrator is missing, and the Δt error is unmeasured (main problem 5).
- 11.5 reuses \(r\) for a particle radius and \(\theta\) for the surface fraction; (48) reuses \(k\) for a kernel; 11.6 reuses \(\sigma\)
  (surface tension in 5) for a safety threshold and \(\tau\) for a tuning constant (see the table).
- 11.6, "The same.cjs run, a hard push over 200 steps": `same.cjs` is introduced only in 11.7. Reverse the order, or describe the run here.
- 11.6, "each conjugate (\(A\)-orthogonal) to the last": in conjugate gradients each direction is \(A\)-orthogonal to *all* earlier ones. That
  is the property that makes the method work.
- 11.3, "[3] proves that the transfers conserve angular momentum exactly": check this against [3]. The proof is for the collocated grid, and
  the MAC form of §6 may not inherit "exactly". G will ask.
- 11.7, "(on 6 November 2026 a 0.02 ms sliver step was found after a shortened step … section 10.2 now hands over its impulse and the steps are
  equal)": this is a change log, not textbook prose, and 10.2 does not use the word "impulse". State the rule (equal steps; the mean
  acceleration \(\Delta\mathbf V_g/\Delta t\) is handed over) and drop the history.
- 11.7, last paragraph: the fingerprint "sha256 7747da757ea9d800" and `notes/fig12/threads-test.cjs` are developer detail, and the second is a
  working-folder path in the published text. A clause saying the shared loops give identical results is enough.
- (46) and (47) are clipped at 390 px.
- What reads well: the physical meaning of the pressure ("the field of impulses the liquid exerts on itself so that no parcel is squeezed"),
  the measured reason for a particle radius of 1.8 spacings, and the CFL and viscous-stability numbers (0.64 m/s, 3×10⁻⁴).

### 12 · Checks · verdict: needs work (small)
- The tables have no caption and no number. The standard's form numbers figures and equations, and tables should be numbered too ("Table 1").
- There is no check in Δt (main problem 5).
- "The tilt … its error scatters (+18 % at 4 mm …)": 4 mm is the page's own default grid, and its tilt error is the largest of the four. Say
  so plainly, since it is the case the reader watches.
- "Spill book-keeping … left = counted" is true by construction ("every particle that leaves becomes a drop"). It checks the code, not the
  physics. Say that, or replace it with a check that can fail, such as total mass in glass plus drops against the mass poured.
- Damping row of the tulip: non-monotonic, not discussed (see 5).

### 13 · A small parameter study · verdict: clear, small fixes
- "Heave |a_g,z| max": "heave" is not defined (see 9). The table has no caption or number.
- "The heave grows in proportion to the bump with speed control … as a linear system's should": in open loop it does not (3.66 to 7.63 m/s²,
  ×2.08). The likely reason is in the next sentence (the cart slows to 0.70 m/s). Join the two.
- The lessons are clear and well supported by the table.

### 14 · What the picture shows · verdict: needs work
- Only the stout, the head and the drops are mapped (main problem 6). Add the cart: which drawn element is \(k\), \(c\) and the wheel of
  radius \(R_w\); what the ground ticks mark; whether the spring is drawn at its true length; how the bump on screen relates to \(h_b\) and
  \(L\).
- "The data panel … checks each against its formula and against the picture": this claim is not supported in the note. Name one example.

### 15 · What the model leaves out · verdict: clear, one sentence
- "Real foam … damps the swing; it is not in this model" (14), and "carry the foam as a second, lighter layer" (15): the claim that foam damps
  sloshing has no source. A candidate to *open and read* before citing is A. Sauret, F. Boulogne, J. Cappello, E. Dressaire, H. A. Stone,
  "Damping of liquid sloshing by foams", *Phys. Fluids* 27, 022103 (2015).
- The nonlinear regime is not listed as a limit. On the 25 mm bump the lean is 60 mm in a glass 78 mm wide, far from "small". Section 14 says
  the column-height drawing cannot show a breaking wave, but 15 does not say that linear theory, and the readout, fail there.
- Problems: Problem 5 uses 39.1 mm as the rim's radius, which is \(R(h)\); the rim is at 37.5 mm (section 2). The answer, 5.6 m/s², uses
  39.1. Say "at the wall, 39.1 mm out", or use 37.5. Problem 2 duplicates 4.5 (see above). The other answers check out: 1.62 and 1.61 Hz,
  0.85 m/s, \(\omega c_x/(bK_i)\), and 4.5.

### 16 · Sources · verdict: needs work
- Source 7 has not been read and has no link (main problem 7). The note says this honestly, but the standard does not allow it.
- From this sandbox, Nisbets (source 1) and the AMS PDF of Chorin (source 11) answered HTTP 403, probably bot blocking. Open both in a normal
  browser before publishing. The other nine links answered 200 or 206.
- For a reader who meets control and vehicle dynamics *for the first time*, the list has nothing at entry level. The six numerical sources are
  graphics papers and course notes. Candidates to open, read and then list: K. J. Åström and R. M. Murray, *Feedback Systems* (free PDF; PI
  control, sensitivity); a vehicle-dynamics text chapter on the quarter-car model; R. A. Ibrahim, *Liquid Sloshing Dynamics* (CUP 2005), or
  O. M. Faltinsen and A. N. Timokha, *Sloshing* (CUP 2009). These are suggestions only: list none of them until it has been read.

---

## Symbols with more than one meaning

| Symbol | Meanings in the note |
|---|---|
| \(h\) | fill depth (2, 4); cart time step in (34) |
| \(r\) | radial coordinate (3–4); particle radius in (48) |
| \(\theta\) | polar angle (3–4); surface fraction \(\varphi_c/(\varphi_c-\varphi_n)\) (11.5) |
| \(q\) | mode height (4.5); generalised coordinate (6.3); scaled pressure \(p\Delta t/\rho\) (46) |
| \(i\) | motor current (7–8); imaginary unit (9); grid-node index (47) |
| \(k\) | wavenumber (4); suspension stiffness (6); kernel \(k(s)\) (48) |
| \(\sigma\) | surface tension (5); MIC safety threshold (11.6); Lamb's frequency (16) |
| \(\tau\) | \(\tau_m\) torque, \(\tau_i\) lag (7); MIC tuning constant (11.6) |
| \(V\) | stout volume (3.5); motor voltage (7); potential energy (6.3) |
| \(T\) | kinetic energy (25); transmissibility (40); \(T_s\) sample time (8) |
| \(C\) | Bernoulli constant (11); controller \(C(s)\) (8) |
| \(R\) | glass radius; \(R_a\) resistance; \(R_k\) kernel radius; \(R_w\) wheel radius (subscripted, so acceptable) |
| \(N\) | tyre load; \(N_g\) gear ratio; \(N_p\) particle count (subscripted, so acceptable) |

## The standard, item by item

| Item | Met? |
|---|---|
| 1 Physical picture | Yes, in 1, 6, 7, 8 and 9. Missing as a picture of the cart (6). |
| 2 Model and dimensionless numbers | Yes (5). The 25 mm Froude number is wrong (main problem 2). |
| 3 Derivation, every step; ★ restated | The steps are now complete. Missing: Duhamel (4.5), the δ/R scaling (5). ★ results not restated (4, 11). |
| 4 Checks | Units, limits and conservation are good. The Δt check is missing; the spill check cannot fail. |
| 5 Numerical method as the code does it | Fluid yes. Cart integrator missing; Δt error unmeasured. |
| 6 Equation to screen | Stout only; cart missing (14). |
| 7 Limits and next model | Yes. Add the nonlinear regime and a source for foam damping. |
| 8 Further reading, read and linked | Source 7 unread and unlinked. No entry-level control or vehicle text. |
| Form | Unnumbered displays (4.5, 6.3, 8.3, 11.2); uncaptioned tables; (22) clipped everywhere and four more displays clipped on phones; symbol clashes. |

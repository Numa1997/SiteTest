# Fig. 12 · referee report, round 3

Page: `public/simulations/beer-slosh.html`, the lecture note "A pint of stout on a suspension" (`<article class="paper" id="paper">`);
English source `notes/fig12/note-src.html`. Read as **S**, a school student good at mathematics, and **G**, a physics graduate
(the ★ parts), and as a referee of the derivations. Judged against `notes/STANDARD.md` (section 4, and Numa's verdict of
21 October 2026: Taylor's *Classical Mechanics* as the model).

**How it was read.** Built with Vite into the session scratchpad (not `dist/`, no repository file touched), served on
`localhost:8791`, opened in headless Chromium (Playwright, SwiftShader WebGL) at 1440 × 900. All folds of the note opened
(0 left closed; 11 sections). KaTeX errors: 0. Horizontal overflow: 0. Each section screenshotted in 1400 px slices
(`/tmp/claude-0/-home-user-SiteTest/0935aa8a-1d41-50fc-be37-f46e7857f37a/scratchpad/shots/s01_0.png` … `s12_4.png`; s01 is the
header, s02–s12 are sections 1–11). The 390 px phone width was not re-checked this round. `plan.md`, `check.md` and
`check-derivations.md` were not read. Every equation listed under "Checked" below was redone by hand. Three numbers were
measured, not estimated, by running the repository's own `tools/fig12/controller3.py` on the page's data
(`public/scripts/slosh-modes.js`): peak tilt over the bump, passive 2.74°, skyhook 1.28°, LQR 1.42°; peak rim wave 61.1, 15.0
and 3.76 mm; closed-loop time constant 1.928 s. Two code files were opened, only to see whether a fault is in the note or in
the model: `tools/fig12/plant.py` (matrix assembly) and `tools/fig12/controller3.py` (controller state).

Tags: **E** an error (wrong as written), **G** a gap (skipped step, undefined symbol, unsupported claim, missing picture),
**W** wording. **[S]** loses the school student, **[G]** the graduate objects, **[both]**.

---

## A. The five findings that matter most

1. **E · Section 10, the Rayleigh function of the modes has the wrong units, and the "modal row = (12)" claim is wrong twice.**
   - "and the modes’ \(\rho N_n(1 + \kappa_n)\gamma_n\dot a_n^2\)". \(\rho N_n\) is kg/m, so this is kg·m/s³, not a power
     (kg·m²/s³). The mode's mass is \((\rho N_n/\lambda_n)(1+\kappa_n)\), so the term must be
     \((\rho N_n/\lambda_n)(1 + \kappa_n)\gamma_n\dot a_n^2\). `plant.py` line 96 has it right
     (`C = 2 mu (1 + kappa) gamma`, `mu = rho N / lam`); only the note is wrong.
   - "The row of (19) for a mode, divided by \(\rho N_n/\lambda_n\), is exactly (12)". Dividing by \(\rho N_n/\lambda_n\)
     leaves \((1+\kappa_n)\ddot a_n + \dots\); you must divide by \((\rho N_n/\lambda_n)(1+\kappa_n)\) to get (12).
   - It is also not *exactly* (12). Equation (19) has constant matrices, so its mode row has no \(\omega_n^2(\ddot z_O/g)\,a_n\)
     term. Pumping is a cubic term of the Lagrangian (\(\dot z_O\) times \(a_n^2\), from the moving boundary). Section 9
     confirms the page adds it outside (19) ("The vertical acceleration that pumps the modes is taken from the previous step").
     **Fix:** "The row of (19) for a mode, divided by \((\rho N_n/\lambda_n)(1 + \kappa_n)\), is (12) without its pumping
     term. That term is third order in the Lagrangian, so a linear system cannot hold it, and the page adds it to each mode
     row from (12)."
   - The same paragraph has a missing \(1/\lambda_n\): "\(\rho\dot x_O\dot a_n\!\int\!\nabla x'\!\cdot\!\nabla\Phi_n\,dV =
     \rho Q_nN_n\dot x_O\dot a_n\)". Since \(\int\nabla x'\cdot\nabla\Phi_n\,dV = \lambda_nQ_nN_n\) (Green, using
     \(\partial_n\Phi_n = \lambda_n\Phi_n\) on S and 0 on the glass), the left side should read
     \(\rho\dot x_O(\dot a_n/\lambda_n)\int\nabla x'\cdot\nabla\Phi_n\,dV\). The result \(\rho Q_nN_n\dot x_O\dot a_n\) is right.

2. **E/G · Section 11, the tilt the controller computes is wrong while a wheel is on the bump, and the note says the road does
   not enter.**
   "In these coordinates the road enters (19) only through its rate of rise under each wheel … on a flat road
   \(\psi = (d_r - d_f + \zeta_r - \zeta_f)/(l_f + l_r)\)". In general that sum equals
   \(\psi + (z_{rf} - z_{rr})/(l_f + l_r)\). So the road heights themselves enter through every \(g\psi\) term, and the tilt
   drive \(-\rho g\psi Q_nN_n\) is the main drive of the stout. On the default bump the error reaches
   0.030/0.80 rad = **2.15°** (measured with `controller3.py`), for the third of a second each wheel is on the bump. That is
   larger than the LQR's own peak tilt of 1.42°. The note's parenthesis ("A road slope would add to the true tilt …") calls
   this a slope effect, but every bump that lies between the wheels causes it.
   **Fix:** "The four heights \(z_b, \psi, z_f, z_r\) and the four deflections are two descriptions of the same configuration,
   so \(\psi\) is not lost; but recovering it needs the road heights, \(\psi = (d_r - d_f + \zeta_r - \zeta_f + z_{rr} -
   z_{rf})/(l_f + l_r)\). The controller has no road sensor, so it uses the level-road value. While one wheel is on the bump
   its tilt is wrong by up to 2.2°. The page's model of the plant keeps the true tilt, so Figure 6 shows the price of that
   error: it is already included in the 3.8 mm."
   Section 11 also needs the real reason for these coordinates: after the kerb, the cart's new rest has every height 20 mm
   up. A regulator on absolute heights would push toward zero for ever, while one on deflections sees the new rest as zero.
   That one sentence explains the choice better than the hop picture.

3. **E · Section 2, the scaling of the drawing is stated backwards.**
   "Scaling the drawing to the imperial glass takes two slightly different factors, 160/149 = 1.074 in height and
   85/81.5 = 1.043 in width, so our glass is the drawing stretched by 3 % more in height than in width". The drawing is 76 mm
   across (the sampled outline `profile_drawing.csv` gives a widest half-width of 117.9 of 462.6 units, so 75.9 mm). The width
   factor is therefore 85/75.9 = 1.120. The number 81.5 mm is the drawing's width after the height scaling (75.9 × 1.074), and
   it appears from nowhere. The glass is stretched about **4 % more in width than in height**, not 3 % more in height.
   **Fix:** "… 160/149 = 1.074 in height and 85/76 = 1.12 in width: the real glass is 4 % wider for its height than the
   drawing, a modelling choice, stated here once."
   Related **G**: "with the 2.0 mm wall as the only free number: a consistency check". The panel depth is also free, and the
   note itself says it "could be half or double". That moves the brim volume by 7 to 14 mL, the same size as the 8 mL margin
   the check rests on. Say so, and drop "the earlier photograph-based profile of this page failed by 6 %": the reader never
   saw that profile.

4. **G (a missing term, about 3 %) · Section 6 and section 10, the head's inertia in the turn is dropped by both routes.**
   The head rides on the surface, and when the glass turns, the surface point at \(x'\) accelerates vertically by
   \(-\ddot\psi x'\). The head's pressure on the stout is \(M_f\) times its vertical acceleration in the room, so it is
   \(M_f(\ddot\eta - \ddot\psi x')\), not \(M_f\ddot\eta\). In the Lagrangian, the head's kinetic energy
   \(\tfrac12M_f\int(\dot z_O - \dot\psi x' + \dot\eta)^2dS\) has the cross term \(-M_fQ_nN_n\dot\psi\dot a_n\). Either way,
   the turn coupling in (12) should be \(Q_{rn} - (\kappa_n/\lambda_n)Q_n\), not \(Q_{rn}\). For the default pint
   \(\kappa/\lambda = 2.7\) mm against \(Q_r/Q = 103\) mm, a 2.6 % change in the turn drive. `plant.py` line 100 omits it as
   well, so "the Lagrangian route and the boundary-value route give the same equation" cannot catch it: both routes start from
   the same head model. **Fix:** add the term, or write one sentence saying it is dropped and why (2.6 %).
   Related **W**: in "Checks", "(12) gives \(a_n = -Q_n\ddot x_O/g\) (head aside)". The head cancels exactly in the steady
   state, \(\omega_n^2(1+\kappa_n) = g\lambda_n\), so it is surface tension that must be set aside, not the head. Write
   "(surface tension aside; the head cancels)".

5. **G · Section 6, the turn is not given its physical picture, and the frame argument is wrong where the cart moves fast.**
   - "A liquid that is swung round does not simply turn with its glass; near the surface it lags, and \(\chi\) says by how
     much." This is the one physical idea of the new part, and no reason is given. The reason is equation (3): a rigid turn
     has vorticity \(2\dot\psi\), and a settled pint cannot acquire vorticity. So the liquid moves only as much as the walls
     force it to (a raw egg spun on a table). Say this.
   - "Split the potential into the part the glass would impose on a **frozen** liquid". A frozen (rigid) liquid has no
     potential. \(\chi\) is the flow of an ideal liquid under a lid, and the note itself later shows it is 71 % of the
     frozen value. Write "on a liquid held under a lid that turns with the glass".
   - The check "\(Q_r/Q = 103\) mm against \(Z_s = 144\) mm" can be made exact and unstarred. For a deep straight glass,
     \(\chi = x'z' - \sum_n (2Q_n/k_n)\psi_n e^{k_n(z' - Z_s)}\) (it satisfies Laplace, the wall condition and
     \(\partial_z\chi = -x'\) on the lid), so \(Q_r/Q = Z_s - 2R/\xi = 144.1 - 43.2 = 100.9\) mm. That is within 2 % of the
     program's 103 mm and gives the picture: the turn pushes the stout as a sideways push applied \(2R/\xi\) below the
     surface, about one decay length down.
   - "The products of small quantities that the frame’s own velocity would add are second order and dropped". The cart
     drives at 1.5 m/s, and \(\dot x_O\) is not small in the room. Terms such as \(\dot x_O\,\partial_x\phi_s\) are first
     order. They cancel exactly between \(\partial_t\Phi\) and \(\tfrac12|\nabla\Phi|^2\) (Galilean invariance); they are not
     dropped for being small. The code (`controller3.py`, "x_c is the push coordinate about the uniform motion") in fact works
     in the frame that moves with the cart's steady speed. **Fix:** "We work in the frame that moves with the cart's steady
     speed \(v\), which is inertial; there the glass's own velocity is small, and the products it adds are second order."
     Also, \(\dot x_Ox' + \dot z_Oz'\) is a translation along the glass's tilted axes. In room axes it is
     \(\dot x_O(x' + \psi z') + \dot z_O(z' - \psi x')\); the difference is of second order only in that moving frame.

---

## B. The requested checks, one by one

| Item | Verdict |
|---|---|
| Dynamic condition with tilt and turn (section 6) | **Correct** to first order, once the frame is the one moving with \(v\) (A5). Kinematics checked: rotation \(+\psi\) about \(+\hat{\mathbf y}\) gives \(\hat{\mathbf y}\times\mathbf r' = (z', 0, -x')\), the axis point at \(x_O + \psi z'\), the surface at \(z_O + Z_s + \eta - \psi x'\), and the lid gives \(\partial_z\chi = -x'\), so the \(\dot\psi x'\) terms cancel in the kinematic condition. Sign of the tilt checked: gravity along \(+x'\) is \(+g\psi\), and the steady state \(\eta = \psi x'\) keeps the surface level in the room. Missing: the head term \(-M_f\ddot\psi x'\) (A4). **W:** this central equation has no number; number it (6′ or 12a), since (12) and Problem 3 depend on it. |
| Equation (12) | **Correct** for the model as stated: projection, orthogonality (M-orthogonality from the symmetry of (10)), \(\phi_s = \sum(\dot a_n/\lambda_n)\Phi_n\), the factor \(\lambda_n/(1+\kappa_n)\), the pumping factor and the remark that \(\ddot z_O\) does not scale \(\sigma\). Steady push: \(\sum Q_n\psi_n = x\); in a cylinder (1,1) + (1,2) give \((33.47 + 2.92)/40 = 91\) % at the rim, which supports "90 %". Resonance: \(\lambda Q/(2\zeta(1+\kappa)) = 27.7\), so 0.2 mm → 5.5 mm, which supports "28 times" and "5.6 mm"; \(A\omega^2 = 0.082\) m/s². Notation clash: \(\psi\) (pitch) and \(\psi_n\) (mode shape) sit in the same display, and \(x\) in \(Q_n\) is \(x'\) in the line above. |
| "Three ways in" box | Physics right; one degree is \(9.81\times0.01745 = 0.171\) m/s². **W:** "which means \(m = 1\)" holds for a body of revolution only. In the sculpted glass a mode with \(m = 3\) carries a \(\cos\theta\) part (\(k = m - 2\)) and so has a small \(Q_n\); say "\(m = 1\), and faintly the modes the panels mix with them". **G [S]:** "It can only amplify a slosh that is already there" still gives no threshold outside the ★ part (open since round 2). Add: "it wins when \(\epsilon\omega/4 > \gamma\): for the default pint, 0.58 mm of shaking at \(2f_1\)". |
| Lagrangian terms (section 10) | Checked term by term. Translation \(\tfrac12m_l(\dot x_O^2+\dot z_O^2)\) ✓ (the \(\dot x_O\dot z_O\) cross term vanishes). Turn \(\tfrac12J_{sj}\dot\psi^2\) ✓, about the foot \(O\). Modes \(\tfrac12(\rho N_n/\lambda_n)(1+\kappa_n)\dot a_n^2\) ✓, since \(\int|\nabla\Phi_n|^2 = \lambda_nN_n\) and the head adds \(\tfrac12M_fN_n\dot a_n^2\). \(\dot x_O\)–mode ✓ in result, ✗ \(1/\lambda_n\) in the written integral (A1). Turn–mode \(\rho Q_{rn}N_n\) ✓ (Green on S). Translation–turn \(m_lz_{cm}\dot x_O\dot\psi\) ✓ (\(\oint x'\,\partial_n\chi = \int(\hat{\mathbf y}\times\mathbf r')_x\,dV = Vz_{cm}\)); the \(\dot z_O\dot\psi\) term vanishes by the half-turn symmetry; say so. \(\dot z_O\)–mode coupling vanishes because \(\int_S\psi_n = 0\) (volume); say so, because the ring modes would otherwise look coupled. Springs ✓ (front corner \(z_b - l_f\psi\)). Waves ✓. Tilt \(-\rho g\psi\sum Q_nN_na_n\) ✓. Inverted pendulum ✓, but **G**: \(h_g'\) is never defined (the glass's own centre of mass above the pitch axis), and \(m_g\), \(m_l\) appear before \(M_s = M_b + m_g + m_l\) defines them implicitly. Rayleigh ✗ (A1). Head turn term missing (A4). A sentence a graduate will want: minimising \(V\) over \(a_n\) at fixed \(\psi\) gives \(-\tfrac12\rho g\psi^2\sum Q_n^2N_n\), the naval architect's free-surface effect, which is why the liquid may be counted as frozen in the pendulum term. |
| Modal row reproduces (12) | ✗ as written (A1): wrong divisor, and no pumping term in (19). With the divisor corrected, the row is \(\ddot a + 2\gamma\dot a + \omega^2a = -\tfrac{\lambda}{1+\kappa}[Q(\ddot x_c + h_g\ddot\psi) + Q_r\ddot\psi - gQ\psi]\), which is (12) without pumping, since \(\ddot x_O = \ddot x_c + h_g\ddot\psi\). Verified against `plant.py` lines 95–101. |
| "The stout pushes back" box | **G/W:** "on the body with the moment \(-\rho Q_{rn}N_n\ddot a_n\)" is the moment about the foot \(O\). About the body's centre of mass, which is what \(\psi\) turns about, it is \(-\rho N_n\ddot a_n(Q_{rn} + h_gQ_n)\) (`plant.py` line 100). Say "about the foot". "On a 27 kg cart": the cart is 28.9 kg (section 6) and the sprung body 25.9 kg (section 10); pick one. Sloshing mass ✓: \(\rho\lambda Q^2N/(1+\kappa)\) = coupling²/modal mass; Problem 1's closed form checks: \(2/(\xi(\xi^2-1)) = 0.4545\), giving 90.6 g/1.127 = 80.4 g against 81 g. |
| LQR coordinates: why \(\psi\) is not a state | Partly right (A2). The count is 4 ↔ 4: \((z_b, \psi, z_f, z_r)\) ↔ \((d_f, d_r, \zeta_f, \zeta_r)\) given the road, so nothing is dropped except the road heights, and those come back through \(g\psi\). The flat-road formula is checked: with \(d\) as extension, \(d_r - d_f + \zeta_r - \zeta_f = (l_f + l_r)\psi + z_{rf} - z_{rr}\). **G [both]:** the 13 states are never listed by count. Say "the two modes (1,1) and (1,2) along \(x\)": 4 + 2 + 5 + 2 = 13. Say also why the other 12 modes are left out (no linear coupling to the cart in a round glass; weak in the sculpted one). |
| The marginal mode | **G:** the note never says why \(x_c\) and \(y_c\), \(\dot y_c\) are absent from the state. The reason: no actuator force is horizontal, so the cart's position along the road is an integrator that no gain can move, an eigenvalue on the unit circle. A Riccati equation has no stabilising solution with such a mode in the state, unless the mode is invisible to the cost. \(\dot x_c\) is kept because it couples to the stout and the pitch through \(\mathsf M\); its mode decays only through rolling resistance. "decays with a time constant of 1.93 s … a motion the actuators cannot touch" is right, and it is exactly \(M_\text{tot}/c_x = 28.9/15\) = 1.93 s (measured 1.928 s). But \(c_x = 15\) N·s/m appears nowhere in the note: give it, and the 1.93 s becomes a check the reader can do. |
| Cost (20) | Dimensionless ✓; the Riccati form \(\mathsf S = \mathsf Q + \mathsf A_d^\mathsf T\mathsf S(\mathsf A_d - \mathsf B_d\mathsf K)\) with \(\mathsf K = (\mathsf R + \mathsf B_d^\mathsf T\mathsf S\mathsf B_d)^{-1}\mathsf B_d^\mathsf T\mathsf S\mathsf A_d\) ✓ (the standard DARE after substitution). **G:** "with \(\mathsf Q\) and \(\mathsf R\) the weights of (20)". The step from (20) to the matrices is missing: \(\eta_\text{rim}\), \(\psi\), \(\dot z_b\) are rows \(\mathbf h^\mathsf T\mathbf x\) of the state, so \(\mathsf Q = \sum \mathbf h\mathbf h^\mathsf T/\sigma^2\) and \(\mathsf R = \mathsf I/\sigma_u^2\). Give \(\sigma_\psi\) in radians (0.010) as well; the matrix uses radians. **W:** the \(\psi\) in (20) is the level-road estimate, not the tilt of Figure 6 (A2). The cost penalises the front of the rim only; that suffices for the \(x\)-modes because they are odd in \(x\); say so. Six symbols clash here (section C). |
| Sources: what was read | Honestly labelled, which is good. Against STANDARD §4.8 ("only real sources you opened and read"), however, five entries fail: [5] Miles, abstract only; [6] NASA SP-8009 via a secondary tutorial; [7] Keulegan, abstract only; [15] Hrovat, "the paper itself was not opened", yet it is the only support for the choice of state; [16] ISO 8608, "not opened", yet \(G_d(n_0) = 256\times10^{-6}\) m³ rests on it; [17] Karnopp, abstract only. [11] "read in part". **Fix:** cite the open summaries actually read for ISO 8608 (the note says "as reproduced in open summaries" but does not name them); replace [6] with NASA SP-106 (Abramson 1966), which is on NTRS and contains the decrement and the equivalent mechanical models; open a textbook for the Stokes–Joukowski potential and the modal equations with tilt (Faltinsen & Timokha, *Sloshing*, CUP 2009, chapters on linear modal theory). That makes the closing sentence "we have not opened a textbook for them, so none is cited" unnecessary. The swirl claim of section 9 ("we have not opened a source for it here") is an unsupported claim by the note's own rule. |

Other cross-references checked in the built pages:
- "(Fig. 9 derives this actuator in detail)" ✓: `driven-oscillator.html` has the moving-coil drive and the Lorentz force.
- "(Fig. 11 derives the zero-order hold)" **E**: `pendulum-control.html` (Fig. 11 since 4 November) contains no zero-order
  hold. The derivation is in the project page `double-inverted-pendulum.html` ("Balancing Two Rods on a Cart"). Fix the
  reference.

---

## C. One symbol, one meaning (STANDARD and Taylor rule) [both]

| Symbol | Meanings in the note |
|---|---|
| \(\psi\) | pitch angle (s6, s10, s11); mode shape on the surface \(\psi(s,\theta)\), \(\psi_n\) (s5, s6, s7, (12), (20)); in "Checks" of s6, \(\psi = J_1(kr)\cos\theta/J_1(\xi)\) is a mode shape, one paragraph after \(\psi\) the tilt. **Worst clash:** rename the shapes \(\varphi_n\) or \(\Psi_n\), or the pitch \(\theta_p\). |
| \(\Phi\) | mode shape \(\Phi(x,y,z)\) (s5, s7); total potential in the room (s6, s10). |
| \(z_r\) | rear-wheel height; the road profile \(z_r(s)\) (s10, same paragraph). |
| \(\zeta\) | damping ratio \(\zeta_n\), \(\zeta_1\); tyre deflection \(\zeta_f, \zeta_r\) (s11). |
| \(\sigma\) | surface tension; the tolerances \(\sigma_\eta, \sigma_\psi, \sigma_v, \sigma_u\). |
| \(s\) | coordinate in \(\psi(s,\theta)\) (undefined); Fourier coefficient \(s_k(s)\); distance from the wall (s7); road position (s10). |
| \(\mathsf K, \mathsf M\) | FEM stiffness and mass (s5); cart stiffness and mass (19); \(\mathsf K\) also the LQR gain (s11, next to (19)). |
| \(\mathsf Q, \mathsf R, \mathsf S\) | LQR weights and Riccati matrix vs coupling \(Q_n\), radius \(R\), surface \(S\). |
| \(A\) | panel depth (s2); shaking amplitude (s6). |
| \(J\) | \(J_b\) (body); \(J\) in \(f_\psi\) (undefined: it must be the total pitch inertia, about 2.11 kg·m², to give 3.39 Hz; with \(J_b = 2.0\) it gives 3.49 Hz); \(J_{sj}\); the cost \(J\) (20). |
| \(k\) | wavenumber; spring stiffness (s10); Fourier index in s5; sample index in (20). |

---

## D. Section by section

### 1 · Carrying a pint
Clear. **Verdict: clear, leave it.**

### 2 · The glass and the stout
- **E** the scaling factors (A3).
- **G** "the only free number" (A3).
- **W** "So two opposite sides are deeper than the other two". "Deeper" reads as a deeper cavity, but the cavity is
  *narrower* there (27.0 against 29.0 mm). Write "the wall is pressed in on two opposite sides".
- **W, figure** Figure 1, right inset: the labels of the three heights ("80 mm", "?0 mm", "50 mm") are printed on top of
  each other and cannot be read (crop: `…/scratchpad/shots/crop_inset.png`). Offset them, or label the rings by colour in the
  caption.
- Checked: \(\nu = 2.05\times10^{-6}\) m²/s; \(M_f = 0.15\times1007\times0.018 = 2.72\) kg/m²; head top 144.1 + 18 − 160 =
  2.1 mm; 590 − 14 = 576 mL.
- **Verdict: needs work** (one error, one figure defect).

### 3 · A fluid in a moving glass
- Checked: (1); (2) (\(-\nabla\Psi = \mathbf g - \ddot{\mathbf x}_g\)); (3); \(\delta = \sqrt{2\cdot2.05\times10^{-6}/20.3}
  = 0.449\) mm; \(\delta/R = 0.011\); (5). Model box: \(\lambda D = 46.94\times0.1361 = 6.39\);
  \(\sigma\lambda^2/\rho g = 0.0100\). The round-2 errors ("downhill", "wave length", the unit slip) are fixed.
- **W** model box: "the glass translates with the cart and tilts with it, by small angles". Add "in a frame moving with the
  cart's steady speed" (A5).
- **Verdict: clear, leave it** (one optional phrase).

### 4 · Linear sloshing in a straight glass
- Checked: (6), (7), (8); Example 4.1 (\(\pi R^2D = 0.500\) L, \(k_{11} = 46.03\) m⁻¹, tanh 4.58 = 0.9998, 21.25 rad/s,
  3.382 Hz); \(\tanh 3 = 0.9951\) gives under 0.3 % in \(\omega\); nodal-circle counts (\(J_1\) has no zero below 1.84;
  \(J_0\) has one below 3.83); pendulum length \(R/1.84 = 21.6\) mm.
- **Verdict: clear, leave it.**

### 5 · The real glass, in three dimensions
- Checked: (9)–(11); Example 5.1 (\(\sqrt{9.81\times46.94}/2\pi = 3.415\) Hz; × \(\sqrt{1.0100}\) = 3.432; ÷
  \(\sqrt{1.1267}\) = 3.234 Hz).
- **G [S]** "Each mode’s shape \(\psi(s, \theta) = \Phi|_S\)": \(s\) is never defined (a radius fraction? arc length?), and
  \(s_k(s)\) uses the same letter twice.
- **W [G]** "the panels can only mix an angular pattern with the ones two steps away, by their two-fold symmetry". A half-turn
  symmetry allows mixing with \(k \pm 2, \pm4, \dots\); three terms is a truncation. Write "with patterns an even number of
  steps away; we keep the nearest two".
- **W** "within \(6\times10^{-6}\) of the exact value": relative or absolute (λ is in m⁻¹)? Say "relative".
- **G** surface tension: "For a mode it multiplies \(\eta\) by \(\lambda^2\) (exactly so in a deep straight glass …)". In a
  straight glass \(\nabla_h^2\) gives \(k^2\), not \(\lambda^2 = k^2\tanh^2kD\). It is exact only as \(kD\to\infty\); say
  "\(k^2\), which is \(\lambda^2\) in a deep glass".
- **G [S]** the step "For a mode this adds \(M_f\lambda\) to the inertia \(\rho\)" is still not shown (round 2, A1.3). One
  line: "with \(\partial_t\eta = \lambda\phi\), \(\partial_t^2\eta = \lambda\partial_t\phi\), so (6) becomes
  \((1 + M_f\lambda/\rho)\partial_t\phi + g\eta = 0\)".
- **W, figure** Figure 2: the labels "with 18 mm of head" and "straight glass, with head" are struck through by the curves.
- **Verdict: needs work** (small: one undefined symbol, two missing lines).

### 6 · Driving the modes: push, tilt, pump
- See A4, A5 and section B. Faraday part checked line by line: the variation-of-parameters formulas,
  \(\langle\sin^2\cos^2\rangle = 1/8\), both averaged rates, (13), and \(4\times0.0244\times9.81/40.6^2 = 0.58\) mm.
- **G [S]** the unstarred part "One equation per mode" uses \(\chi\), \(Q_{rn}\), \(\Phi_n\) and \(x'\), all defined only in
  the ★ part before it. The byline promises the ★ results "restated without them". Add to the Key result: "\(Q_{rn}\) is the
  turning analogue of \(Q_n\): a turn \(\ddot\psi\) pushes mode \(n\) as a sideways acceleration \(\ddot\psi\,Q_{rn}/Q_n\)
  would, about 0.10 m × \(\ddot\psi\) for the slowest mode".
- **W** "the stout is swung only 71 % as hard as a frozen block, because the liquid near the surface lags": see A5 for the
  closed form and a truer picture.
- **G** "but a cart that shakes its pint hard enough to pump it also drives the slosh directly through the tilt, and the
  direct drive wins". This is an unmarked inference with no number. Give the comparison, or mark it **Inference**.
- **W** the two displays (the tilted dynamic condition, the averaged Faraday equations) have no numbers; STANDARD asks for
  numbered equations.
- **Verdict: needs work.**

### 7 · Where the energy goes
- Checked: (14); the Stokes-layer profile, \(\langle(\partial_su)^2\rangle = (U^2/\delta^2)e^{-2s/\delta}\), integral
  \(U^2/2\delta\), (15), (16); \(I_w/E_\Phi = (1+\xi^{-2})/[R(1-\xi^{-2})] = 1.837/R\); coefficient
  \(\pi\cdot1.837/(\sqrt2\,\xi^{1/4}) = 3.503\); 4.98/3.50 = 1.42; \(\gamma_v = 2\nu\lambda^2 = 0.0090\) s⁻¹;
  \(\gamma_f = 0.016/0.0398\times(1 - e^{-0.845}) = 0.229\) s⁻¹; the sum of Figure 3 is 0.492 s⁻¹; 1/e in 2.03 s; 5 % in
  6.1 s.
- **W** "Dividing by \(2E\) and using Green’s identity … for the energy" and "\(E_\Phi\) … is the energy (14)". The energy is
  defined in the sentence before (14), and Green's identity is not used in (16) as written. Number the energy line, or drop
  the clause.
- **W** "With the walls and the interior alone it would be 9.0 s to 1/e". Figure 3's wall + interior gives 0.108 s⁻¹, so
  9.3 s. The 9.0 s matches only if the head is removed too (frequency up 6 %, \(\gamma_w\propto\sqrt\omega\)). Say "walls
  and interior alone, without the head".
- **G** "the exact value for the slowest mode is \(1.88\nu k^2\)" has no tag and no derivation; mark it **computed** and name
  the script.
- **W** mixed \(1/k\) and \(1/\lambda\) for the same depth within "The head".
- **W, figure** Figure 3: the "total γ" row has its line but no value; print 0.492 s⁻¹.
- **Verdict: clear apart from wording.**

### 8 · The velocity field in the cut
- Checked: \(1/\lambda = 21.3\) mm, 63 % at one decay length, \(R/\xi\).
- **Verdict: clear, leave it.**

### 9 · On the screen, and what is left out
- **W** "the wheels’ hop at about 28 Hz" against section 10's "about 30 Hz". Hand value:
  \(\sqrt{(k_t+k)/m_w}/2\pi = 29.9\) Hz. Pick one. The RK4 phase error, measured from the RK4 amplification factor: 1.4 × 10⁻⁶
  per step at 28 Hz, 1.9 × 10⁻⁶ at 30 Hz, so "about \(2\times10^{-6}\)" stands; the stability limit \(2\sqrt2\) = 2.83 ✓.
- **W** "there the surface slope is already about 0.37". 0.37 is \(ka = \xi/5\). The steepest slope of the (1,1) shape
  (at the centre) is \(ka\,J_1'(0)/J_1(\xi) = 0.86\,ka = 0.32\). Say "about 0.3".
- **G** the swirl claim without a source (see B, sources).
- **W** "the cart has no roll" ✓, but in the list of limits add the controller's level-road tilt (A2).
- **Verdict: clear apart from wording.**

### 10 · The cart and the road
- See A1, A4 and section B.
- Checked: foot position \(x_O = x_c + d_g + h_g\psi\), \(z_O = z_b + h_g - d_g\psi\) (front down positive);
  \(f_z = \sqrt{6000/25.9}/2\pi = 2.42\) Hz; heave damping ratio \(240/(2\sqrt{6000\times25.9}) = 0.30\); pitch damping ratio
  ≈ 0.43; static load 25.9 × 9.81/2 = 127 N; bump crossing 0.33 s; ISO class C value.
- **G** "\(f_\psi = \sqrt{k(l_f^2 + l_r^2)/J}/2\pi = 3.39\) Hz": \(J\) is undefined. With \(J_b = 2.0\) the formula gives
  3.49 Hz; 3.39 Hz needs \(J \approx 2.11\) kg·m², body plus glass plus stout about the centre of mass. State it.
- **W [G]** "The free motions of the coupled system … 3.09 Hz (mostly pitch, damping ratio 0.40) … the coupling pushes the
  pitch and the slosh apart a little". The fall from 3.39 to 3.09 Hz is almost all damping:
  \(3.39\sqrt{1 - 0.4^2} = 3.11\) Hz. The coupling moves the slosh by 0.002 Hz. Say these are damped frequencies and that the
  pitch moved because of its damping.
- **W, figure** Figure 5: labels set as raw text with underscores ("x_c", "z_b", "M_b, J_b", "m_w, k_t", "O: d_g ahead,
  h_g above"), unlike every other figure; the label "O: d_g ahead, h_g above" runs across the tray's rear post (crop:
  `…/scratchpad/shots/crop_cart.png`).
- **W** "With six coordinates and fourteen modes": correct; but \(N_n\) is defined only in section 9, which a reader of 10
  may skip. Repeat "\(N_n = \int_S\psi_n^2dS\)" here.
- **Verdict: needs work** (the Rayleigh error and the modal-row claim).

### 11 · Keeping the pint level
- See A2 and section B (coordinates, marginal mode, cost, sources).
- Measured: passive tilt 2.74°, skyhook 1.28°, LQR 1.42° (the note's 2.7°, 1.3°, 1.4° ✓); peaks 61.1, 15.0, 3.76 mm ✓;
  60 N / 20 N/A = 3.0 A ✓.
- **E** "(Fig. 11 derives the zero-order hold)" points to a page without it (section B).
- **W** "Soften the springs and the pitch frequency moves away from the slosh, which helps the passive cart more than any
  gain". As written it contradicts the Key result, where the LQR beats the passive cart sixteen-fold. Write "which helps the
  passive cart more than any change of its dampers", or give the number.
- **W** "a motion the actuators cannot touch". Add *why*: internal forces cannot change the cart's momentum along the road
  (B, marginal mode).
- **W** "it tilts the glass against the push when that helps, the way a waiter tips a tray into a turn" is an unmarked
  inference; mark it.
- **W, figure** Figure 6: the top panel's ticks are 20, 13, 6, −1, −8 (choose round ticks), and its legend
  "ink: passive · rose: skyhook · wine: LQR" and the title are printed over the passive curve. The caption's "from \(t = 0\)
  at 1 m before the bump": the cart's centre is 1 m before it, the front wheel 0.6 m. The curves start moving at 0.4 s.
- **W** two "Problems" boxes (end of 9 and of 11). Taylor's rule in STANDARD asks for one, at the end of the last section.
- **Verdict: needs work.**

---

## E. Verdicts against STANDARD §4

| § | 1 picture | 2 model | 3 derivation | 4 checks | 5 numerics | 6 eq → screen | 7 limits | 8 reading | Overall |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ✓ | – | – | – | – | – | – | – | clear |
| 2 | ✓ | ✓ | – | ✗ scaling, weak volume check | – | figure labels | ✓ | ✓ | needs work |
| 3 | ✓ | ✓ | ✓ | ✓ | – | – | – | ✓ | clear |
| 4 | ✓ | ✓ | ✓ | ✓ | – | ✓ | – | – | clear |
| 5 | ✓ | ✓ | small gaps (\(s\), head step) | ✓ strong | ✓ | figure labels | – | – | needs small work |
| 6 | turn picture missing | frame unstated | ✓ with A4, A5 | ✓, closed form available | – | ✓ | – | – | needs work |
| 7 | ✓ | ✓ | ✓ | ✓ | – | ✓ | ✓ | secondary/abstract sources | wording only |
| 8 | ✓ | – | ✓ | ✓ | – | ✓ | – | – | clear |
| 9 | – | – | – | – | ✓ measured | ✓ | ✓, swirl unsourced | – | wording only |
| 10 | ✓ | ✓ | ✗ Rayleigh units, modal-row claim, \(h_g'\), \(J\) | ✓ SymPy check | – | figure labels | – | – | needs work |
| 11 | ✓ waiter | tilt estimate unstated | coordinates argument incomplete | ✓ offline gate | ✓ | ✓ | ✓ | three of four control/road sources not opened | needs work |

Form: no question-and-answer, connected prose, Key result boxes and worked examples present, ★ convention mostly kept
(two leaks: section 6 unstarred part uses \(\chi\), \(Q_{rn}\); Faraday threshold not restated). Voice is calm and free of
the listed AI tells. The main formal fault left is the symbol clashes of section C.

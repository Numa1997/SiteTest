Definitions (First Use)
 * [Fact] Isochoric elastic left Cauchy-Green tensor (\bar{\mathbf{b}}_e): Symmetric positive-definite elastic strain tensor \bar{\mathbf{b}}_e = \mathbf{F}_e \mathbf{F}_e^T with \det(\bar{\mathbf{b}}_e) = 1, arising from the multiplicative split \mathbf{F} = \mathbf{F}_e \mathbf{F}_p with \det(\mathbf{F}) = \det(\mathbf{F}_p) = 1.
 * [Fact] Lie (Oldroyd) derivative (\mathcal{L}_v \bar{\mathbf{b}}_e): Objective spatial rate measuring pure plastic relaxation of \bar{\mathbf{b}}_e at fixed material configuration, \mathcal{L}_v \bar{\mathbf{b}}_e \equiv \dot{\bar{\mathbf{b}}}_e - \mathbf{L}\bar{\mathbf{b}}_e - \bar{\mathbf{b}}_e\mathbf{L}^T = \mathbf{F}\frac{d}{dt}(\mathbf{C}_p^{-1})\mathbf{F}^T, where \mathbf{L} = \nabla\mathbf{v} and \mathbf{C}_p = \mathbf{F}_p^T\mathbf{F}_p.
 * [Fact] Discrete adjoint identity: Exact equality between the mechanical work rate extracted by the nodal stress force \mathbf{F}_{\text{dev},f} on the MAC grid and the stress-power integrated over particles, -\sum_f u_f F_{\text{dev},f} = \sum_p V_p\,\boldsymbol{\tau}_p : \mathbf{C}_p, holding whenever the same interpolation gradients \nabla w_{fp} and unattenuated nodal velocities u_f appear in P2G and G2P.
1. Exact Simo Dissipation Density and Discrete Plastic Work for This Return Map
1.1 Continuum Derivation (Exact Factor Convention)
 * [Fact] Under the multiplicative split \mathbf{F} = \mathbf{F}_e\mathbf{F}_p with incompressible total and plastic flow (\det\mathbf{F} = \det\mathbf{F}_p = \det\mathbf{F}_e = 1), the spatial velocity gradient splits as:
   
   
   Differentiating \bar{\mathbf{b}}_e = \mathbf{F}_e\mathbf{F}_e^T gives:
   
   
   so \mathcal{L}_v\bar{\mathbf{b}}_e = -2\,\text{sym}(\tilde{\mathbf{L}}_p\bar{\mathbf{b}}_e).
 * [Fact] For the incompressible neo-Hookean Helmholtz free-energy density W(\bar{\mathbf{b}}_e) = \frac{G}{2}(\text{tr}\,\bar{\mathbf{b}}_e - 3) and Kirchhoff stress \boldsymbol{\tau} = G\,\text{dev}(\bar{\mathbf{b}}_e) (equal to Cauchy stress at J = 1):
   
   
   Since \text{tr}(\mathbf{D}) = 0 and \text{tr}(\tilde{\mathbf{L}}_p) = 0, the isotropic part \frac{1}{3}\text{tr}(\bar{\mathbf{b}}_e)\,\mathbf{I} drops out of both contractions, leaving G\,\bar{\mathbf{b}}_e:\mathbf{D} = \boldsymbol{\tau}:\mathbf{D} and G\,\text{tr}(\tilde{\mathbf{L}}_p\bar{\mathbf{b}}_e) = \boldsymbol{\tau}:\tilde{\mathbf{D}}_p, where \tilde{\mathbf{D}}_p = \text{sym}(\tilde{\mathbf{L}}_p).
 * [Fact] By the isothermal Clausius-Duhem inequality, the exact continuum plastic dissipation density \mathcal{D}_p (\text{W/m}^3) is:
   
 * [Fact] Work-conjugacy check between s and \dot{\gamma}_p: With s = \sqrt{\frac{1}{2}\boldsymbol{\tau}:\boldsymbol{\tau}} (\implies \boldsymbol{\tau}:\boldsymbol{\tau} = 2s^2) and associative coaxial plastic flow \tilde{\mathbf{D}}_p = \frac{1}{2}\dot{\gamma}_p\,\frac{\boldsymbol{\tau}}{s}:
   
   
   Therefore s and \dot{\gamma}_p ARE exact work-conjugates with factor 1 (verified in simple shear: \tau_{xz} = \tau_{zx} = s, \tilde{D}_{p,xz} = \tilde{D}_{p,zx} = \dot{\gamma}_p/2, so \boldsymbol{\tau}:\tilde{\mathbf{D}}_p = s\,\dot{\gamma}_p). There is no missing factor of 2 or \sqrt{2} in the continuum law.
1.2 Exact Discrete Plastic Work of This Backward-Euler Return Map
 * [Fact] During the return map, total deformation \mathbf{F}^{n+1} is held fixed while \bar{\mathbf{b}}_e relaxes from the unimodular elastic trial state \bar{\mathbf{b}}_e^{\text{tr}} to \bar{\mathbf{b}}_e^{n+1}. The exact discrete free-energy dissipated per unit volume in the step is therefore:
   
 * [Fact] Expressing \bar{\mathbf{b}}_e = \mathbf{D}_b + c\,\mathbf{I} with \text{tr}(\mathbf{D}_b) = 0 and \det(\bar{\mathbf{b}}_e) = c^3 - I_2 c + I_3 = 1, where I_2 = \frac{1}{2}\mathbf{D}_b:\mathbf{D}_b = (s/G)^2 and I_3 = \det(\mathbf{D}_b) = O((s/G)^3), expanding c = 1 + \epsilon for s/G \ll 1 gives 3\epsilon = I_2 - I_3 + O(I_2^2), hence:
   
 * [Fact] Substituting the return-map update s^{\text{tr}} - s_{\text{new}} = G\,\Delta t\,\dot{\gamma}_p into \Delta w_p^{\text{exact}} = W^{\text{tr}} - W^{n+1}:
   
 * [Inference] Key result for V_p\,s_{\text{new}}\,\dot{\gamma}_p\,\Delta t:
   * To leading order O(\Delta t), V_p\,s_{\text{new}}\,\dot{\gamma}_p\,\Delta t IS the correct discrete plastic work (including both the rate-independent plastic part V_p\,\tau_y\,\dot{\gamma}_p\,\Delta t and the Tcholakova viscous part V_p\,\tau_v(\dot{\gamma}_p)\,\dot{\gamma}_p\,\Delta t).
   * At O(\Delta t^2), backward Euler underestimates the exact discrete return-map free-energy drop by +\frac{1}{2}G(\dot{\gamma}_p\Delta t)^2 > 0 — it does not overcount it.
   * At finite elastic strain (s = 50\text{ Pa}, G = 166.44\text{ Pa}, \gamma_e \approx 0.30), the O(s^3/G^2) term (I_3) shifts W relative to s^2/(2G) by at most \sim 1.5\text{--}3\% (in simple shear \text{tr}\,\bar{\mathbf{b}}_e - 3 = \gamma_e^2 while s^2/G^2 = \gamma_e^2(1 + \frac{1}{3}\gamma_e^2)), negligible compared to +51.4\%.
2. Complete Energy Balance of the Solver
 * [Fact] Over any free-sloshing interval [t_1, t_2] (stationary glass, t_1 = 0.2\text{ s} after the push ends at 0.05 + 0.15 = 0.20\text{ s}, zero surface tension \gamma = 0), the complete energy balance is:
   
   
   with explicit definitions:
   * Stores:
     * Translational kinetic energy: KE = \sum_p \frac{1}{2}m_p\Vert{}\mathbf{v}_p\Vert{}^2 (plus tiny sub-cell APIC affine kinetic energy KE_{\text{aff}} = \sum_p \frac{1}{2}m_p\,\text{tr}(\mathbf{C}_p \mathbf{D}_p^{\text{inert}} \mathbf{C}_p^T), O(10^{-6}\text{ J})).
     * Gravitational potential energy: PE = \sum_p m_p g z_p.
     * Foam stored elastic energy: U_{\text{el}} = \sum_{p\in\text{head}} V_p \frac{G}{2}(\text{tr}\,\bar{\mathbf{b}}_{e,p} - 3).
     * Surface energy: E_{\text{surf}} = \gamma A_{\text{free}} = 0 in Step 4 (\gamma = 0).
   * Physical sinks:
     * Yield + Tcholakova bulk foam dissipation: E_{\text{plastic}} = \sum_{\text{steps}}\sum_{p\in\text{yielded}} V_p\,\big[\tau_y + \tau_v(\dot{\gamma}_p)\big]\,\dot{\gamma}_p\,\Delta t (already combines rate-independent plastic work \tau_y\dot{\gamma}_p and Tcholakova viscous work \tau_v\dot{\gamma}_p).
     * Cantat foam wall friction: E_{\text{wall,foam}} = \sum_{\text{steps}}\sum_f \frac{1}{2}M_f\big[(u_f^1)^2 - (u_f^2)^2\big]_{\text{foam}}.
     * Stout Stokes wall layer: E_{\text{wall,stout}} = \sum_{\text{steps}}\sum_f \frac{1}{2}M_f\big[(u_f^1)^2 - (u_f^2)^2\big]_{\text{stout}}.
     * Stout bulk Newtonian viscosity (unlogged in current summary): E_{\text{visc,stout}} = \sum_{\text{steps}} \sum_f \frac{1}{2}M_f\big[(u_f^0)^2 - (u_f^1)^2\big].
   * Numerical residual E_{\text{num}} (sum of sub-step non-conservative transfers):
     * E_{\text{num}} = E_{\text{P2G}} + E_{\text{G2P}} + E_{\text{proj}} + E_{\text{coll}} + E_{\text{dev-mismatch}}, where P2G/G2P and interior MAC projection are dissipative (\ge 0), while cut-cell projection, _g2p_cont pushback, PE swelling, and F_dev–C work mismatch can have either sign.
Which Exact Terms Can Make Logged Sinks Exceed -\Delta E_{\text{mech}}
 * [Fact] Rewriting the exact discrete balance over [t_1, t_2] isolates every mathematical term that can make \text{sinks}_{\text{logged}} > -\Delta E_{\text{mech}}:
   
   
   where W_{\text{stress,grid}} = \sum_n \sum_f \frac{1}{2}M_f[(u_f^2)^2 - (u_f^3)^2] is the actual grid kinetic energy extracted by \mathbf{F}_{\text{dev}}, and W_{\text{constit}} = [U_{\text{el}}(t_2) - U_{\text{el}}(t_1)] + E_{\text{plastic}} is the energy absorbed by the particle constitutive model.
 * [Inference] Specifically, the exact mechanisms that drive the RHS positive are:
   * Stored elastic energy release U_{\text{el}}(0.2) - U_{\text{el}}(1.0) > 0: Elastic strain energy built up during the 0.05\text{--}0.20\text{ s} push relaxes plastically over 0.2\text{--}1.0\text{ s}, feeding E_{\text{plastic}} without reducing E_{\text{mech}}.
   * Discrete adjoint break W_{\text{constit}} > W_{\text{stress,grid}}: Letting \mathcal{A} = \{f : w_{\text{sum},f} > 10^{-6} \land \theta_f > 0\} and \alpha_f = M_f / \max(M_f, m_{\text{floor}}) \in (0, 1], subtracting grid work from particle work yields:
     
     * Mass-floor attenuation (1 - \alpha_f > 0): On every face where M_f < m_{\text{floor}} (up to 4266 faces in the earlier 4.5 run), \mathbf{F}_{\text{dev}} is weakened by \alpha_f < 1 when braking the grid, yet G2P feeds the unattenuated velocity u_f^6 into \mathbf{C}_p. Since -u_f F_{\text{dev},f} > 0 during yielding, this term is strictly positive and systematically inflates E_{\text{plastic}} above actual mechanical work extracted.
     * Closed wall faces (\theta_f = 0, f \notin \mathcal{A}) and extrapolated air faces: \mathbf{F}_{\text{dev}} is dropped on \theta_f = 0 faces, while G2P reads all 8 corners of the post-extrapolate MAC grid into \mathbf{C}_p.
     * Rigid-rotation distortion in \mathbf{f} = \mathbf{I} + \Delta t\mathbf{C}: Pure rotation \mathbf{C} = \boldsymbol{\Omega} (\mathbf{D} = \mathbf{0}) produces \mathbf{f}\mathbf{f}^T = \mathbf{I} + \Delta t^2\boldsymbol{\Omega}\boldsymbol{\Omega}^T, injecting non-alternating deviatoric stress \propto G\Omega^2\Delta t^2 per step along the rotation axis (creating spurious \dot{\gamma}_{p,\text{rot}} \sim \Omega^2\Delta t/\sqrt{3} with zero grid stress work).
   * Spurious PE swelling or KE injection (E_{\text{num,mech}} < 0): Total fluid weight in the glass is M_{\text{tot}} g \approx 4.45\text{ N} (m_s \approx 0.430\text{ kg}, m_h \approx 0.024\text{ kg}). A tiny +1.5 \times 10^{-4}\text{ m} (0.10\,\Delta x, +0.2\% volume) cloud swelling between 0.2\text{ s} and 1.0\text{ s} raises PE(1.0) by +0.67\text{ mJ}, masking 0.67\text{ mJ} of real mechanical energy loss! (Note: because theoretical first-mode energy at \eta_0 = 1.132 \times 10^{-2}\text{ m} is \frac{1}{2}\rho_l g I_0 \eta_0^2 = 1.065\text{ mJ} at peak and \sim 1.28\text{ mJ} at t = 0.20\text{ s}, matching -\Delta E_{\text{mech}} = 1.260\text{ mJ} within \sim 2\%, PE swelling is unlikely to explain the whole +0.65\text{ mJ} gap, though even +5 \times 10^{-5}\text{ m} shifts the budget by 0.22\text{ mJ}.)
   * Bookkeeping / logger error: Accidentally integrating E_plastic from t = 0 (capturing the violent 0.05\text{--}0.20\text{ s} push) instead of 0.2\text{--}1.0\text{ s}, or a coding discrepancy in the e_plastic line itself.
3. Likelihood Ranking of Candidates (a)–(d)
 * Rank 1 (Primary cause, working together with #2): Candidate (c) — Discrete adjoint mismatch between F_dev and C (W_constit > W_stress_grid).
   * [Inference] This is the only non-bug physical/numerical mechanism large enough to explain E_plastic = 1.580 mJ alone exceeding both -dE_mech = 1.260 mJ and the theoretical first-mode slosh energy at t = 0.2\text{ s} (\sim 1.28\text{ mJ}). Mass-floor attenuation on thousands of surface/wall-sliver faces is systematically positive (always inflating E_plastic over W_stress_grid), closed-wall/air extrapolation breaks the adjoint on boundary particles, and \mathbf{f} = \mathbf{I} + \Delta t\mathbf{C} adds non-alternating rotational shear in high-vorticity wall/interface bands. Note one clarification on the wording of (c): in stout_jax.py (Stout.g2p), C IS already the trilinear gradient of the MAC grid velocity at \mathbf{x}_p (not particle-to-particle finite-difference noise); the mismatch is between the unattenuated, post-projection, post-extrapolation, non-symmetric C and the attenuated, masked, pre-projection F_dev.
 * Rank 2 (Guaranteed partial contributor, insufficient alone): Candidate (b) — Omitted stored elastic energy U_{\text{el}}(0.2) - U_{\text{el}}(1.0).
   * [Inference] Because t_1 = 0.20\text{ s} sits immediately at the end of the 3.4\text{ m/s}^2 push and t_2 = 1.0\text{ s} sits near rest (U_{\text{el}}(1.0) \lesssim 0.01\text{ mJ}), -\Delta U_{\text{el}} > 0 is guaranteed to close part of the gap. For realistic volume-averaged s_{\text{rms}}(0.2) \approx 15\text{--}30\text{ Pa}, U_{\text{el}}(0.2) \approx \frac{s_{\text{rms}}^2}{2G}V_h \approx 0.06\text{--}0.24\text{ mJ} (bounded < 0.4\text{ mJ} as you noted), explaining roughly 15\text{--}40\% of the +0.648\text{ mJ} overshoot (plus positive numerical dissipation), so it is real and necessary, but not sufficient alone.
 * Rank 3 (Must rule out immediately via log audit): Candidate (d) — Bookkeeping window leak, PE swelling, or cut-cell projection/collision energy injection.
   * [Inference] If E_plastic accidentally included even a fraction of the 0.05\text{--}0.20\text{ s} push (where 97\% of foam yielded at up to 136\text{ s}^{-1}), that alone produces > 0.6\text{ mJ}. Similarly, a +0.10\text{ mm} (0.07\,\Delta x) PE swelling or non-M_f-orthogonal cut-cell projection shifts -\Delta E_{\text{mech}} by \sim 0.45\text{ mJ}. Ranked #3 because -dE_mech = 1.260 mJ already matches the theoretical \sim 1.28\text{ mJ} slosh energy closely, arguing against massive PE swelling—yet an instant audit of the existing log rules these out with zero ambiguity.
 * Rank 4 (Ruled out mathematically; possible only as an unverified typo in the e_plastic line): Candidate (a) — Factor-of-2 / \sqrt{2} work-conjugacy or backward-Euler overcount.
   * [Fact / Inference] Section 1 proves exact factor-1 conjugacy (\mathcal{D}_p = s\dot{\gamma}_p) and shows backward Euler slightly undercounts W^{\text{tr}} - W^{n+1}. Moreover, Test 4.3 (plug flow) already matched the exact factor-1 analytical velocity to +0.49\%, ruling out a factor-of-2 or \sqrt{2} bug in the return map itself. Only a typo isolated to the single e_plastic accumulation line (which Test 4.3 never checked) could trigger (a).
4. One Cheap Kaggle-CPU Discriminating Test per Candidate
All four tests run strictly on Kaggle CPU (0 GPU-min), with pre-committed pass marks checked to be reachable by construction (written in plain text with abs( )).
Test (a): Steady Simple-Shear Slab Energy Identity (~20 s CPU)
 * Setup: Run the existing commensurate Test 4.3 periodic slab (h = 1.80 \times 10^{-2}\text{ m}, \Delta x = 1.5 \times 10^{-3}\text{ m}, zero vertical jitter, \tau_b = 1.5\,\tau_y, m_{\text{floor}} never active, no curved walls) for 2.0\text{ s}, and integrate over the steady window t \in [1.0,\; 2.0]\text{ s}:
   * Exact gravitational work: W_{\text{grav}} = \sum_{n} \sum_p m_p g \sin\alpha\,v_{x,p}^n\,\Delta t.
   * Logged plastic dissipation: E_{\text{plastic}} = \sum_{n} \sum_{p\in\text{yielded}} V_p\,s_{\text{new},p}\,\dot{\gamma}_{p}\,\Delta t.
   * Exact discrete free-energy drop: E_{\text{drop}} = \sum_{n} \sum_{p\in\text{yielded}} V_p\frac{G}{2}(\text{tr}\,\bar{\mathbf{b}}_e^{\text{tr}} - \text{tr}\,\bar{\mathbf{b}}_e^{n+1}).
   * Exact grid stress work: W_{\text{stress,grid}} = \sum_{n} \sum_f \frac{1}{2}M_f\big[(u_f^2)^2 - (u_f^3)^2\big].
 * Reachability by construction: In steady 4.3, s/G \le 0.049 (O(s^2/G^2) \le 0.08\%) and \frac{1}{2}G(\dot{\gamma}_0\Delta t)^2 / (\tau_b \dot{\gamma}_0\Delta t) = 0.52\%, so all four integrals must agree within < 2\%.
 * Pass marks (refuting (a)):
   * abs(E_plastic / W_grav - 1.0) < 0.03
   * abs(E_plastic / E_drop - 1.0) < 0.02
   * abs(E_plastic / W_stress_grid - 1.0) < 0.03
 * Decision: If E_plastic / W_grav lands near 2.0 or 1.414, Candidate (a) (logger bug) is proved. If all three pass, Candidate (a) is refuted.
Test (b): Stored Elastic Energy U_{\text{el}}(t) on Instrumented Coarse Cavity Slosh (~6–10 min CPU)
 * Setup: Run the exact 4.5 half-sine push (3.4\text{ m/s}^2, 0.15\text{ s} from 0.05\text{ s}, to 1.0\text{ s}) on a cavity-only grid (body = None, \Delta x = 3.0 \times 10^{-3}\text{ m}, \Delta t_{\text{el}} = 1.53 \times 10^{-3}\text{ s}, \sim 4.5 \times 10^4 cells, \sim 1.5 \times 10^5 particles, \sim 650 steps) so the full 0.2\text{--}1.0\text{ s} slosh runs cleanly on CPU. Log U_{\text{el}}(t) = \sum_{p\in\text{head}} V_p \frac{G}{2}(\text{tr}\,\bar{\mathbf{b}}_{e,p} - 3) at every step alongside E_{\text{mech}}(t), E_{\text{plastic}}, E_{\text{wall,foam}}, E_{\text{wall,stout}}, and compute -\Delta E_{\text{tot}} = -\Delta E_{\text{mech}} + U_{\text{el}}(0.2) - U_{\text{el}}(1.0) and r_{\text{tot}} = \text{sinks} / (-\Delta E_{\text{tot}}).
 * Reachability by construction: By positive-definiteness of \bar{\mathbf{b}}_e with \det(\bar{\mathbf{b}}_e) = 1, \text{tr}(\bar{\mathbf{b}}_e) \ge 3 identically (AM-GM inequality), so U_{\text{el}}(t) \ge 0 strictly at every step.
 * Pass marks (discriminating (b)):
   * Sanity: min(U_el) >= -1.0e-12 J and U_el(0.2) > U_el(1.0).
   * Candidate (b) alone explains the overshoot if and only if sinks / (-dE_mech) > 1.25 AND r_tot <= 1.02 AND abs(r_tot - 1.0) < 0.25. If r_tot > 1.05, Candidate (b) is confirmed as a partial contributor only and refuted as the sole cause.
Test (c): Adjoint Work-Consistency & Mechanism Decomposition (same 3.0\text{ mm} CPU slosh + 1 s rotation check)
 * Setup (zero extra slosh runs): Inside the same 3.0\text{ mm} CPU slosh over [0.2,\; 1.0]\text{ s}, log:
   * Exact grid stress work W_{\text{stress,grid}} = \sum_n \sum_f \frac{1}{2}M_f[(u_f^2)^2 - (u_f^3)^2] vs. particle constitutive work W_{\text{constit}} = [U_{\text{el}}(1.0) - U_{\text{el}}(0.2)] + E_{\text{plastic}}.
   * Spatial breakdown of E_plastic: E_plastic_mfloor (particles touching any face with M_f < m_{\text{floor}}), E_plastic_wall (particles within 1.5\,\Delta x of the glass wall), and E_plastic_interior (remaining foam particles).
   * Shadow cell-strain diagnostic: run a read-only shadow tensor be_cell driven by pure symmetric cell-centered MAC strain rate \mathbf{f}_{\text{sym}} = \mathbf{I} + \Delta t\,\mathbf{D}_{\text{cell}} (zero rotation, cell-centered instead of staggered particle C), logging E_plastic_cellD.
   * Standalone 100-step rigid-rotation unit check (< 1 s CPU): evolve a single foam particle under pure rotation \mathbf{C} = \boldsymbol{\Omega} (\Omega = 30\text{ rad/s}, \mathbf{D} = \mathbf{0}, \Delta t = 7.67 \times 10^{-4}\text{ s}) for 1000 steps from \bar{\mathbf{b}}_e = \mathbf{I} and log max_s_rot and E_plastic_rot.
 * Reachability by construction: In a work-consistent discrete scheme without boundary/mass-floor/rotation breaks, W_{\text{constit}} / W_{\text{stress,grid}} = 1 + O(\Delta t) (already verified to < 2\% in Test (a)) and pure rigid rotation yields zero stress.
 * Pass marks (discriminating (c)):
   * Adjoint consistency (holds if (c) is NOT the cause): abs(W_constit / max(W_stress_grid, 1.0e-12) - 1.0) < 0.05.
   * Rotation objectivity: max_s_rot < 0.05 * tau_y and E_plastic_rot == 0.0 (expect failure under f = I + dt C if \Omega^2\Delta t accumulates; quantifies its exact contribution).
   * Candidate (c) is proved if W_constit / W_stress_grid > 1.15, with E_plastic_mfloor, E_plastic_wall, and E_plastic - E_plastic_cellD identifying which specific break dominates.
Test (d): Existing 4.5 Log Audit + Exact Telescoping Sub-Step Ledger (~10 s on existing 4.5 log + inside the 3.0\text{ mm} CPU slosh)
 * Setup:
   * On the existing 4.5 Part C JSONL log (~5 s CPU): Check cum_E_plastic(1.0) - cum_E_plastic(0.2) against the reported 1.580 mJ (ruling out push-window leakage), compute PE(1.0) - PE(0.0) and M_tot * g * (mean_z(1.0) - mean_z(0.0)) in \text{mJ} (measuring PE swelling), and check whether floor_w was G.thw == 0 on vertical wall faces during 4.5 Part C.
   * Inside the 3.0\text{ mm} CPU slosh over [0.2,\; 1.0]\text{ s}: Log the exact energy change of every sub-step in Stout.step: \Delta E_{\text{P2G}}, \Delta E_{\text{visc}}, \Delta E_{\text{wall}}, \Delta E_{\text{dev}} (= -W_{\text{stress,grid}}), \Delta E_{\text{grav+proj}}, and \Delta E_{\text{G2P+coll}}. Also toggle vertical_floor_w (True vs False) if floor_w was active on vertical wall faces in 4.5 Part C.
 * Reachability by construction: The six sub-step energy deltas telescope algebraically to \Delta E_{\text{mech}} to float64 round-off.
 * Pass marks (discriminating (d)):
   * Telescoping identity: abs((dE_P2G + dE_visc + dE_wall + dE_dev + dE_grav_proj + dE_G2P_coll) - dE_mech) < 1.0e-7 J.
   * Window integrity (4.5 Part C log): abs(E_plastic_reported - (cum_E_plastic(1.0) - cum_E_plastic(0.2))) < 1.0e-9 J.
   * No PE swelling bias (4.5 Part C log): abs(PE(1.0) - PE(0.0)) / (-dE_mech) < 0.05.
   * Wall-friction logger integrity: abs((-dE_wall) / (E_wall_foam + E_wall_stout) - 1.0) < 0.02.
   * No mechanical energy injection by projection or wall pushback: dE_grav_proj <= 0.02 * (-dE_mech) and dE_G2P_coll <= 0.02 * (-dE_mech).
5. Critique of the Two Failed Marks (No Tuning or Mark Changes Proposed)
 * [Fact / Opinion] Both failed energy marks (abs(sinks / (-dE_mech) - 1) < 0.25 and -dE_mech >= sinks within 2 %) are physically badly defined in their current form — not because the +51.4\% overshoot is acceptable (it is almost certainly a real bug/mismatch that must be diagnosed by Section 4), but because they omit two physical energy terms:
   * Omitting U_{\text{el}} from the energy store: For an elasto-viscoplastic material, E_{\text{mech}} = KE + PE is not a Lyapunov function of the free decay; E_{\text{tot}} = KE + PE + U_{\text{el}} is. Because the window starts at t_1 = 0.20\text{ s} (peak elastic loading right after the push), even a mathematically exact continuum solution with zero numerical dissipation has \text{sinks} = -\Delta E_{\text{mech}} + [U_{\text{el}}(0.2) - U_{\text{el}}(1.0)] > -\Delta E_{\text{mech}}, which automatically fails -dE_mech >= sinks within 2 %.
   * Conflating discrete adjoint consistency with numerical dissipation and PE drift: Comparing total sinks only against -dE_mech hides whether a failure comes from (i) PE cloud swelling (0.1\text{ mm} = 0.45\text{ mJ}), (ii) omitted U_{\text{el}}, (iii) legitimate APIC/projection damping, or (iv) a broken F_dev–C adjoint.
 * [Opinion] Raw numbers to report in every free-slosh run (in SI units, \text{J} or \text{mJ}, without tuning or changing any pass mark):
   * Store deltas over [t_1, t_2]: -\Delta KE, -\Delta PE, -\Delta U_{\text{el}} = U_{\text{el}}(t_1) - U_{\text{el}}(t_2), total -\Delta E_{\text{tot}} = -\Delta(KE + PE + U_{\text{el}}), and resting-baseline PE drift PE(t_2) - PE(0).
   * Physical sinks over [t_1, t_2]: E_{\text{plastic}}, E_{\text{drop}} = \sum V_p\frac{G}{2}(\text{tr}\,\bar{\mathbf{b}}_e^{\text{tr}} - \text{tr}\,\bar{\mathbf{b}}_e^{n+1}), E_{\text{wall,foam}}, E_{\text{wall,stout}}, and E_{\text{visc,stout}}.
   * Exact discrete adjoint check: W_{\text{stress,grid}}, W_{\text{constit}} = \Delta U_{\text{el}} + E_{\text{plastic}}, and their ratio W_{\text{constit}} / W_{\text{stress,grid}}.
   * Exact numerical residual: E_{\text{num}} = (-\Delta E_{\text{tot}}) - (E_{\text{plastic}} + E_{\text{wall,foam}} + E_{\text{wall,stout}} + E_{\text{visc,stout}}) and the closure ratio \text{sinks}_{\text{all}} / (-\Delta E_{\text{tot}}).

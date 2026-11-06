# Dossier: projection splitting error, pressure/viscous geometry, and body force on an embedded body

Date: 2026-11-06. Scope: why a Chorin-type, volume-fraction (Batty 2007) projection with ghost-fluid no-slip viscosity gives a grid-independent drag deficit on Schäfer–Turek 2D-1 (c_D about 5 % low by control volume, 7–11 % low by direct force), and how to fix it.

Method note. Papers were downloaded and read as text with grep and targeted reading, not as abstracts, where marked READ. Where I could only see an abstract or a search summary, it is marked ABSTRACT ONLY. Where I could not open anything, it is marked NOT OPENED and any statement about it is from memory and must be treated as unverified.

Sources that failed or were not reached: Kim & Moin 1985 (NOT OPENED; its content reached me only through Brown et al. and Guermond et al.); Perot 1993 (NOT OPENED; same); Batty & Bridson 2008 (NOT OPENED; only as described in Larionov 2017); Ng, Min & Gibou 2009 (ABSTRACT ONLY; no PDF found, the UCSB link returned HTML); Guendelman 2005 (NOT OPENED); Kempe & Fröhlich 2012 (ABSTRACT ONLY; paywalled, no open copy found); Breugem 2012 (NOT SEARCHED); Noor/Chern/Lai (NOT FOUND); Lācis, Taira & Bagheri 2016 (ABSTRACT ONLY). Roads used: WebSearch, curl through the proxy with the CA bundle (the Utah and HKUST copies failed or were 403; Tulane, TAMU, UWSpace, arXiv worked). Firecrawl, Exa, TinyFish were not needed.

---

## 1. Sources actually read

### 1.1 Brown, Cortez & Minion 2001, J. Comput. Phys. 168, 464–499 (READ, full text)
Link: https://www.math.tulane.edu/~cortez/Prints/accproj.pdf (author copy); DOI 10.1006/jcph.2001.6715.
Location: Sec. 2.1 (pressure-increment projection, Eq. 22–23 and text after), Sec. 2.2 (Kim–Moin), Sec. 3 (boundary conditions for u*, text near "The situation for the tangential boundary condition for u*"), Sec. 4 normal-mode analysis, Sec. 6 numerics (Fig. 1–3), conclusions.
Establishes:
- In a projection method the velocity is second order in time and space, but the pressure is only first order, and the loss shows up as a boundary layer at the wall. They cite Temam, E & Liu, Shen for rigorous analysis.
- If the pressure update drops the viscous term (p^{n+1/2} = p^{n-1/2} + φ, their Eq. 23), the normal component gives n·∇p^{n+1/2} = n·∇p^{n-1/2} for all n. This is an inconsistent pressure boundary condition. The modified update (their Eq. 13, which contains a ν∇·u* term, the "rotational" correction) recovers second-order pressure.
- For methods where u* has no pressure gradient in its equation (Kim–Moin, Chorin-type, "PmIII"), u* is only a first-order approximation of u^{n+1}, so ∇φ is O(Δt) and cannot be dropped from the tangential boundary condition: use τ·(u* − ∇φ^n)|wall = τ·u_b^{n+1}. This lagged-φ condition is shown sufficient for second order. Extrapolating ∇φ in time is also possible.
- If u* carries the lagged pressure gradient (incremental form), τ·u*|wall = τ·u_b^{n+1} suffices because τ·∇φ is then negligible.
- The boundary condition on u* also controls how smooth ∇·u* stays near the wall, and so how accurate the pressure is (Fig. 2–3: a pronounced boundary layer in ∇·u* is removed by a "free" boundary condition, and the pressure then becomes second order).
Usable: tangential wall condition for the intermediate velocity, u*_τ|wall = u_b,τ + Δt ∇_τφ^n/ρ (lagged) or with ∇φ extrapolated, for the non-incremental scheme; u*_τ|wall = u_b,τ for the incremental scheme.
Does not establish: anything for embedded or cut-cell geometry, curved walls, or an implicit viscous solve done on a ghost-fluid wall link. It is a periodic-channel normal-mode analysis (Guermond et al. say this explicitly, see below).

### 1.2 Guermond, Minev & Shen 2006, Comput. Methods Appl. Mech. Engrg. 195, 6011–6045 (READ, full text)
Link: https://people.tamu.edu/~guermond/PUBLICATIONS/guermond_minev_shen_CMAME_2006.pdf (author copy, 61 pages); DOI 10.1016/j.cma.2005.10.010.
Location: Sec. 3.1 Remark 3.1 (Chorin–Temam), Sec. 3.2 (incremental, standard form), Sec. 3.3 Eq. (3.6)–(3.9), Theorems 3.2–3.3 and Remarks 3.3; Sec. 3.6 (Kim–Moin equals rotational form); Sec. 4 (velocity-correction); Sec. 7 Fig. 1–2 and numerical tests; Sec. 9.3; Table 1.
Establishes:
- The non-incremental (Chorin–Temam) scheme has an artificial pressure Neumann condition ∂_n p = 0, which creates a numerical boundary layer, and an "irreducible splitting error" O(Δt); a higher-order time scheme in the viscous step does not improve it (Remark 3.1). The estimates are O(Δt) in L2 and O(Δt^{1/2}) in H1 for velocity and L2 for pressure.
- The incremental pressure-correction in standard form improves the velocity but still has a numerical boundary layer in the pressure (Fig. 1 left): pressure only first order.
- The rotational form, φ = p^{k+1} − p^k + ν∇·ũ^{k+1}, gives a consistent pressure boundary condition ∂_n p = (f − ν∇×∇×u)·n; the splitting error then appears only as an inexact tangential velocity condition. Pressure and H1 velocity error O(Δt^{3/2}) in general domains (Theorem 3.3); the standard form is O(Δt).
- Remark 3.3: Brown et al.'s second-order pressure holds in a periodic channel; Guermond–Shen's tests suggest 3/2 is likely best possible in general domains. Corners cause large errors.
- The Kim–Moin scheme is equivalent to the rotational form up to a change of variables (Sec. 3.6).
- Sec. 7: for a fixed Δt the standard-form pressure error GROWS as the mesh is refined and converges to the first-order slope. That is, a Δt-dependent error that does not decay with h.
Usable: the rotational update p^{k+1} = p^k + φ − ν∇·ũ (with the density and weighting of the projection) is a one-line change on top of an incremental scheme.
Does not establish: behaviour on cut cells or with a body velocity entering the divergence. It treats fitted FE meshes.

### 1.3 Larionov, Batty & Bridson 2017, ACM TOG 36(4), 101, "Variational Stokes" (READ, full text and supplement)
Link: https://uwspace.uwaterloo.ca/bitstream/10012/12692/1/Larionov2017-a.pdf ; supplement https://cs.uwaterloo.ca/~c2batty/papers/Larionov2017/supplemental.pdf ; DOI 10.1145/3072959.3073628.
Location: Introduction (operator splitting paragraph, "A dominant source of error introduced by splitting…"), Sec. 3 Eq. (5)–(8), Sec. 4 Eq. (10)–(14) (solid case, prescribed velocity boundaries), Sec. 5 (staggered velocity-pressure-stress layout, volume weights W_F, W_S, combined discrete problem Eq. 19–25), Sec. 6.2 (convergence), supplement Table 1 and Fig. 1.
Establishes:
- Splitting viscosity from the pressure projection is a dominant source of boundary-condition error; they solve viscosity and pressure together as one symmetric positive definite saddle-point or pressure–stress system.
- Solid case (Eq. 10): max over p, τ of min over u^{n+1} of ∫_{Ω_F} (ρ/2)|u^{n+1} − u*|² + Δt u^{n+1}·(∇p − ∇·τ) − (Δt²/4µ)|τ|_F² dV. Without stress it reduces to the Batty 2007 projection. The no-slip condition is a natural condition of this functional.
- Moving solid (Eq. 13–14): add the work Δt ∫_{∂Ω_S} u_BC·(pI − τ)n dA, written as a volume integral over the solid region, Δt ∫_{Ω_S} [p ∇·u_BC − τ : (∇u_BC + ∇u_BCᵀ)/2 + u_BC·(∇p − ∇·τ)] dV. Both pressure and viscous stress see the solid through the same volume weights W_F, W_S (stress samples sit at cell centres and edges with their own volume weights). This removes the pressure/viscous geometry inconsistency by construction.
- Convergence (Sec. 6.2 and supplement): single time-step Stokes problems on curved non-grid-aligned domains; velocity error is first order in space for free-surface and for solid-wall cases. They state that the "second order" usually quoted for ghost-fluid and for the Ng et al. 2009 cut-cell scheme refers to the pressure; the velocity is only first order.
Usable: the full discrete system is Eq. (19)–(25) in the paper; the solid-weights and prescribed-velocity terms are directly the structure we need.
Does not establish: any Navier–Stokes drag benchmark, any force on a body, nonlinear advection coupling, or a Reynolds number above Stokes. Their tests are single steps of unsteady Stokes. It cites Ng et al. and Batty et al. as the embedded-boundary lineage but does not test against them.

### 1.4 Batty, Bertails & Bridson 2007, ACM TOG 26(3), "A fast variational framework for accurate solid-fluid coupling" (READ, text; focus on Sec. 3)
Link: https://uwspace.uwaterloo.ca/items/f5cb877f-1b56-4ff5-81d9-f7473a5e7f1a (UWSpace; the file I read came from the Waterloo bitstream); DOI 10.1145/1276377.1276502.
Location: Eq. (2) (solid velocity update), Eq. (5)–(7) (fluid KE and the weighted Poisson system), Eq. (9)–(12) (force and torque on the body as a volume integral of ∇p), Sec. 3.2 (time integration).
Establishes:
- Pressure force on a rigid body as J_x p = −Σ vol_{i+1/2,j,k} (p_{i+1}−p_i)/Δx, with the volume weights equal to the volume of the body in the cell centred on each MAC sample, "exactly analogous to the mass weights" of the fluid kinetic energy. For fully submerged cells the fluid weights are the complement of the solid weights. The interior sums telescope.
- The projection is inviscid: the fluid slips tangentially past the body. Tangential fluid velocity is extrapolated into zero-mass samples before advection (the Houston-style step in their time loop).
- If approximations to volume weights are used in J, the body mass matrix should be consistent with those volumes (only matters for hydrostatic rest).
Usable: force by Eq. (10) is the exact impulse the projection gives the body, provided the fluid weights and solid weights in the same face sum to the cell volume.
Does not establish: any viscous force, any accuracy of the force relative to the true surface integral, any steady drag.

### 1.5 Uhlmann 2005, J. Comput. Phys. 209, 448–476 (READ, relevant section only)
Link: https://arxiv.org/pdf/1809.08170 ; DOI 10.1016/j.jcp.2005.03.017.
Location: Sec. 4, Eq. (13a)–(13b) and the paragraph after (13b), appendix B.
Establishes: the force on a particle is evaluated by a momentum balance over the fluid domain it occupies, not by a surface integral: (ρ_p − ρ_f) V u̇ = −ρ_f Σ F(X_l) ΔV_l + (ρ_p − ρ_f) V g. The second term of the torque equation (13b) is the rate of change of angular momentum of the fluid occupying the particle domain, a term needed because forcing only the surface leaves a residual non-rigid motion of fluid inside the particle (in practice evaluated as a sum over grid cells weighted by the cell's solid fraction; for 3D approximated by rigid-body motion inside).
Usable: the structure "force on body = minus the momentum put into the fluid by the forcing, plus the rate of change of the momentum of the fluid occupying the body".
Does not establish: anything for sharp cut cells; the delta-function forcing is regularised. It does not give the force-vs-benchmark accuracy for our scheme.

### 1.6 Nangia, Johansen, Patankar & Bhalla 2017, J. Comput. Phys. 347, 437–462 (READ, Sec. 2–3)
Link: https://arxiv.org/pdf/1704.00239 ; DOI 10.1016/j.jcp.2017.06.047.
Location: Eq. (14) (surface integral), Eq. (15) (Noca control-volume force), Eq. (16) and Appendix A (Reynolds-transport form), Sec. 3.3 (equivalence with the Lagrange-multiplier force).
Establishes:
- Surface-integral force F = −∮ n·(−pI + T) dS is inconvenient because accurate surface gradients and pressures are hard to get; the Noca control-volume formula F(t) = −d/dt ∫_{V(t)} ρu dV + ∮_{S_CV} n·[−pI − (u−u_S)ρu + T] dS − ∮_{S_b} n·(u−u_S)ρu dS is exact for an arbitrary box enclosing the body, and the last term vanishes for no-slip.
- Eq. (16): F = −∫_{V_CV} ρ ∂_t u dV + d/dt ∫_{V_b} ρu dV + ∮ n·[−pI − uρu + T] dS. The term d/dt ∫_{V_b} ρu dV, the momentum of the fluid-like material inside the body, must be included. This is the body-interior term.
- Spurious force oscillations in the moving-box form come from the time-derivative term; Eq. (16) removes them. The CV force equals the Lagrange-multiplier (direct-forcing) force, proved for Peskin delta functions; they report both agree to plotting accuracy in their tests.
Usable: Eq. (16) as the reference "momentum the fluid lost" for validation of any direct force.
Does not establish: the equivalence for sharp cut-cell schemes (the proof uses the delta function identity ∫f dx = ∫F ds); it does not address a non-conservative advection scheme.

### 1.7 Items seen only as abstracts or search summaries (not opened)
- Ng, Min & Gibou 2009, J. Comput. Phys. 228, 8807–8829, DOI 10.1016/j.jcp.2009.08.032 (ABSTRACT ONLY): cut-cell/ghost-fluid fluid–solid coupling in 2D and 3D, applied to moving rigid bodies. Larionov (1.3) says the "second-order" for this scheme is for the pressure and velocity is first order. I cannot cite its equations.
- Kempe & Fröhlich 2012, J. Comput. Phys. 231, 3663–3684, DOI 10.1016/j.jcp.2012.01.021 (ABSTRACT ONLY): builds on Uhlmann; adds an iterative Euler–Lagrange coupling to enforce the boundary condition more accurately and a treatment of the flow inside the particle so that density ratios down to 0.3 work. The interior-fluid integration is the relevant point; I could not read how it is discretised.
- Lācis, Taira & Bagheri 2016, J. Comput. Phys. 305, 300–318 (ABSTRACT ONLY, arXiv:1510.04806): rigid-body dynamics coupled implicitly into the immersed boundary projection method (no-slip as Lagrange multipliers inside the projection; block-LU). Claims second order in space and examines the effect of fictitious fluid inside the body.
- Kim & Moin 1985 (NOT OPENED): per Brown (1.1) and Guermond (1.2), lagged-φ tangential boundary condition for u*, equivalent to the rotational form.
- Perot 1993 (NOT OPENED, from memory): fractional step as an approximate block-LU factorisation of the coupled velocity–pressure system. This gives the structure of the splitting error but I have not verified formulas; do not cite equations from it.
- Batty & Bridson 2008, Guendelman 2005, Breugem 2012, Noor/Chern/Lai (NOT OPENED).

---

## 2. Answers to the three questions

### Q1. What causes a grid-independent drag deficit?

(a) The splitting error of the non-incremental projection at a no-slip wall.
After the viscous step the intermediate field u* satisfies no-slip. The projection then subtracts (Δt/ρ)∇φ, with φ = Δt p for the non-incremental form. The tangential part of that gradient is not zero at the wall, so u^{n+1}_τ ≠ u_b,τ: a slip velocity of size Δt ∂_τp/ρ, relaxing over a layer of width about √(νΔt) in the next viscous step (Brown 1.1; E & Liu cited there; Guermond 1.2 Remark 3.1). This is a numerical boundary layer. Its width is set by ν and Δt, NOT by h, so grid refinement at fixed Δt cannot remove it. Guermond's Fig. 1 and Sec. 7 show the same behaviour for the pressure: at fixed Δt the error does not decrease under mesh refinement. This matches "not converging".

Size estimate for ST 2D-1 (my own arithmetic, crude, to be checked by measurement): ν = 1e-3, Δt = 10 ms gives √(νΔt) ≈ 3.2e-3 = 0.032 D. Pressure varies by about Δp ≈ 0.12 over a quarter of the circumference (πD/2 ≈ 0.16), so ∂_τp ≈ 0.7 and the slip is about Δt·∂_τp ≈ 0.007, about 0.5–1 % of U. The physical boundary layer is about D/√Re ≈ 0.022 and the wall shear rate about U/δ ≈ 45 s⁻¹; a slip of 0.007 corresponds to a slip length of order 1.5e-4, about 0.3 % of the radius. This predicts a drag effect of well under 1 %, not 5 %. It also predicts an error that shrinks when Δt shrinks; the measured direct c_D moves the other way (5.09, 5.05, 5.02 for Δt = 10, 5, 2.5 ms). So the slip mechanism alone does not explain the numbers. I rank it as a real but probably minor contributor, unless the measured slip velocity (Diagnostic D1) is much larger than the estimate.

(b) The pressure boundary layer of the non-incremental scheme.
The pressure that the force uses (Batty term) is p = φ/Δt from a projection with an artificial Neumann condition on φ. Brown (1.1) and Guermond (1.2) show this gives a first-order pressure with a boundary layer at the wall, and that its size is controlled by the smoothness of ∇·u* at the wall. On our grid-aligned test (Poiseuille) the pressure gradient tangential to the wall is zero or trivial, so the test cannot see it; the cylinder has strong tangential pressure gradients. The pressure drag is about 70 % of c_D at Re 20, so a 5–7 % pressure error is enough. Magnitude not estimated; needs measurement.

(c) Pressure geometry versus viscous geometry.
In our scheme the pressure sees the body through volume fractions (Batty weights, Eq. 5–10 of 1.4) and the viscosity through face-centre signed distance (linear through the wall). The Variational Stokes paper (1.3) avoids this by putting both on the same weights in one functional. If the two geometries place the effective wall at different positions, the no-slip wall for viscosity and the no-penetration wall for pressure disagree by an O(h)-scale shift per face. A random per-face shift averages out; a systematic shift of a fixed fraction of a cell shrinks with h and so does not match "not converging". It would, however, give the erratic non-monotone direct values (5.12, 5.21, 4.96). I rank it as the explanation for scatter and for part of the direct-versus-CV gap, not for the constant 5 % in the CV drag.

(d) The velocity is only first order in these schemes (1.3, Sec. 6.2). That alone gives errors of order h, i.e. 10 → 20 → 40 cells would change by 2x each time; our deficit does not change, so another mechanism sets the floor.

(e) Things the sources do not cover but that fit "grid-independent": non-conservative semi-Lagrangian advection (it is not momentum conserving, so a "momentum balance" is itself contaminated); limiters in MacCormack that fall back to first order near the body; extrapolating fluid velocity into the body before advection (it smears the wall condition at the scale of a cell, and combined with the overwritten momentum it creates a source). These are my reasoning, not from a source above.

Important: the correct statement from the literature is that a Chorin/non-incremental scheme has an O(Δt) steady-state error as well (Guermond Remark 3.1: irreducible splitting error O(Δt)), so a steady benchmark can show a grid-independent bias. A Δt scan (Diagnostic D2) will separate that.

### Q2. Fixes used in practice

1. Incremental pressure-correction. Put −∇p^n into the viscous step, project for φ = p^{n+1} − p^n. Velocity then second order for smooth problems; the boundary condition for u* can be the plain wall velocity (Brown 1.1). Standard form still leaves a pressure boundary layer (Guermond Fig. 1).
2. Rotational form. p^{n+1} = p^n + φ − νρ ∇·u* gives a consistent pressure Neumann condition; pressure error drops from O(Δt) to O(Δt^{3/2}) (Guermond Theorem 3.3 and Remark 3.3). On an embedded boundary this needs ∇·u* evaluated with the same weights as the projection; I have not seen it done for cut cells in the sources I read (so it is untested territory for us).
3. Boundary condition for the intermediate velocity, for the non-incremental scheme: τ·u*|wall = τ·(u_b + Δt∇φ^n/ρ), the lagged-φ condition (Kim–Moin; Brown 1.1). At a steady state φ^n = φ^{n+1}, so it cancels the slip exactly. This is the cheapest change: it only alters the Dirichlet value on the ghost-fluid wall link in the viscous solve.
4. Solve viscosity and pressure together: Variational Stokes (1.3). Removes the splitting error between ν and p, uses one set of volume weights for both, makes no-slip natural and handles a moving solid through Eq. (13)–(14). Cost: a larger SPD system. They show velocity first order in space, no benchmark at Re 20.
5. No-slip inside the projection: Taira–Colonius style IBPM and Lācis et al. (ABSTRACT ONLY): body forces as Lagrange multipliers solved with pressure by block-LU; the force on the body is the multiplier, hence it equals the momentum put into the fluid by construction. I could not read the formulas.
6. Ng–Min–Gibou 2009 (ABSTRACT ONLY) and Gibou/Min symmetric discretisations: sharp cut-cell Poisson with ghost-fluid and solid velocity in the divergence; second-order pressure, first-order velocity (per 1.3). Our pressure step is essentially this plus Batty weights, so the novelty is not there.
7. Guendelman 2005 (NOT OPENED): coupling of solids with a pressure solve and a nullspace treatment; cited in Batty (1.4) for removing the nullspace component when the solid is forced to compress.

### Q3. Force that equals the momentum the fluid loses

1. Noca control-volume formula (Nangia 1.6, Eq. 15–16): exact for any enclosing box, no surface gradients, includes the body-interior term d/dt ∫_{V_b} ρu dV. Our "momentum of velocity samples overwritten by the body" is exactly that term; the CV drag of 5.34 should include it and the box faces must carry the same discrete flux the update used.
2. Direct-forcing momentum balance (Uhlmann 1.5, Eq. 13a): force on the body = minus the total force added to the fluid + the rate of change of the momentum of the fluid occupying the body (weighted by solid fraction).
3. Batty (1.4, Eq. 10): the pressure force is the impulse the projection exchanges with the body, exact only if fluid weight + solid weight = cell volume at every face and the same weights are used in the Poisson system and in J.
4. Discrete ledger rule (my derivation, standard): define one weighted momentum P = Σ_faces w_f ρ u_f V_f. For each substep, record ΔP. Whatever is not a boundary flux of the whole domain must be assigned to the body, otherwise the "direct" force and the CV force will differ. Substeps that change P without a physical flux are the thing to catch: semi-Lagrangian advection (not conservative), MacCormack clamping, extrapolation into the body, overwriting samples inside the body, implicit viscous solve with a wall link evaluated with SDF not volume weights.

---

## 3. Ranked root causes for our numbers, with a diagnostic and the fix

Context: CV c_D 5.34, 5.32, 5.30 (10, 20, 40 cells/D); direct 5.12, 5.21, 4.96; direct drops as Δt falls (5.09, 5.05, 5.02); Poiseuille without the body right to 0.34 %.

R1. Force-ledger leak in the direct c_D (explains direct versus CV gap of 0.1–0.4 and the erratic h-behaviour 5.12, 5.21, 4.96).
Why: the direct force sums three terms with three different geometries (volume weights for pressure, SDF for viscous link, solid-fraction for overwritten momentum). Any mismatch leaks momentum, and the leak varies with how the surface cuts the cells, hence non-monotone.
Test T1: run the same case and compute the direct force twice, once with the viscous flux evaluated using the volume-fraction weight at the face and once with the SDF weight; and verify the identity fluid momentum lost per step = direct force × Δt on a case with no flux through the box (body in a periodic box with a uniform body force). Residual should be at round-off. Also change the minimum fluid-weight clamp (e.g. 1e-2 to 1e-6): if the direct c_D moves by more than 1 %, the thin-cut-cell weights are the cause.
Kill: if the identity holds at round-off and the clamp is irrelevant, R1 is dead.
Fix: define the body force as minus the sum of the ΔP of every substep, computed with the single set of weights used in the projection (ledger rule, Q3.4), or switch to the CV (Noca) value as the reported drag.

R2. Chorin pressure boundary layer and Δt-dependent steady-state error (explains CV deficit that does not shrink with h).
Why: Brown and Guermond: first-order pressure with a boundary layer, error that does not decrease with h at fixed Δt; irreducible O(Δt) splitting error. The pressure drag dominates at Re 20.
Test T2 (D2): hold h = D/20 and run Δt = 10, 5, 2.5, 1.25 ms (or reduce CFL) recording the CV c_D, Δp and the recirculation length. If the CV c_D is unchanged to 0.5 %, the splitting is not the dominant cause. Also read the tangential slip after projection (D1): u_τ at the wall-adjacent samples minus the wall value, against the estimate Δt ∂_τp ≈ 0.007.
Kill: CV c_D flat in Δt and slip below 0.1 % of U.
Fix: lagged-φ wall value (Q2.3), then incremental plus rotational form (Q2.1–2.2).

R3. Non-conservative semi-Lagrangian MacCormack advection (corrupts both the solution and the momentum balance).
Why: not in the sources; standard property. The interior momentum is not conserved, so the CV drag depends on the box, and the numerical dissipation of SL scales like h²/Δt, which moves the wrong way when Δt is halved (the direct drag did fall as Δt fell).
Test T3: (i) compute the CV drag on three nested boxes; in a conservative steady state they must agree. (ii) Re-run Re 20 with a conservative flux-form advection (second-order upwind or central) with the rest unchanged.
Kill: box-independent to 0.5 % and no change with conservative advection.
Fix: for steady low-Re benchmarks, use conservative advection; keep SL only for the interactive figure and report the benchmark with the conservative scheme, or add the momentum-defect to the ledger.

R4. Pressure/viscous geometry inconsistency (explains scatter, and part of the gap).
Test T4: shift the body by fractions of a cell (0, 0.25, 0.5 h) at fixed resolution; the scatter in c_D measures the geometric noise. Then replace the face-centre SDF in the viscous step by the same volume-fraction-derived wall distance used in the pressure step.
Kill: shift scatter below 0.5 %.
Fix: one geometry for both (Larionov-style weights), or at least derive the wall-link distance from the same fractions.

R5. Extrapolation of fluid velocity into the body before advection.
Test T5: compare zero-, first-order and linear extrapolation; and a run with the body region frozen at the body velocity (no extrapolation) with advection upwinded away from the body.
Kill: no change over 1 % in c_D.
Fix: higher-order or Neumann-consistent extrapolation along the wall normal.

R6 (cheap sanity checks first, before any of the above). Confirm the benchmark is set up as the published one: the blockage, the inflow profile, the c_D normalisation (2F/(ρ Ū² D) with Ū = 1, D = 0.1), and report the measured Δp and the recirculation length next to the published 0.1172–0.1176 and 0.0842–0.0852. A 5 % low drag with Δp also about 5 % low points to the flow; with Δp right, to the force evaluation. The Poiseuille test passes because it has no tangential pressure gradient to expose the slip, and the walls are grid-aligned so the weights are trivial; use a pressure-driven inclined channel (tilted about 30°) as a second test.

Recommended order of work: (1) T1 and the box test in T3 (they need no new physics and separate "force evaluation" from "flow solution"); (2) D1/D2 to measure slip and Δt dependence; (3) lagged-φ wall condition plus incremental form (cheapest scheme change; at a steady state it removes the slip exactly); (4) if the CV c_D is still more than 1 % low, move to a unified pressure-viscous solve (Larionov 1.3) or no-slip in the projection (Lācis; abstract only).

## 4. What this dossier cannot say
- No source read here analyses an embedded-boundary Chorin scheme at Re 20 with a drag benchmark. The root-cause ranking is therefore an inference from the periodic-channel and finite-element analyses (Brown, Guermond), the variational papers, and arithmetic; each rank is a hypothesis with a test.
- My estimate of the slip effect (well under 1 %) uses rough pressure and shear numbers and should be replaced by the measured slip.
- The rotational form on cut cells, and the Ng–Min–Gibou and Kempe–Fröhlich internals, are unverified.

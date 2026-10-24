# Fig. 12 · Furuta pendulum · contract, level 0 (Gate 1)

Written 24 October 2026 before any page code. Derivations: `derive.py` (21 PASS). Reference numbers: `physics.py`, `roa.py`.

1. **Question and observable.** Can one motor, turning an arm in a horizontal circle, bring a pendulum hanging from the arm's tip
   up to the top and hold it there, with the arm at rest at an angle the reader chooses? Observables: α(t) (pendulum from straight
   up), φ(t) (arm), the motor voltage V(t) within ±V_max, the time of the catch, the time to settle within 0.01 of the target, the
   energy book.
2. **Picture and mechanism.** A child pumping a swing (energy fed in phase with the motion) and a hand balancing a broom (move the
   base under the fall). Formal: the pendulum's energy E_p = ½J_p α̇² + G cos α changes only through the arm's acceleration,
   dE_p/dt = −h cos α α̇ φ̈ + …; choosing φ̈ ∝ (E_p − G) α̇ cos α makes ½(E_p − G)² a Lyapunov function of the swing-up. Near the
   top, the linearised plant is controllable (det 𝒞 ∝ h² ≠ 0) and LQR gives a Lyapunov function ỹᵀPỹ of the catch.
3. **Model.** Two generalised coordinates (φ, α); the arm a rigid body of inertia J_r about the vertical axis; the pendulum a thin
   uniform rod hinged at the arm's tip, swinging in the plane at right angles to the arm; viscous bearings b_r, b_p. Actuator: a
   permanent-magnet DC motor on the axis, direct drive, fed from a voltage source with limit ±V_max: V = RI + Λİ + kφ̇, τ = kI.
4. **Alternatives rejected.** (a) Current-source drive as in Fig. 11: hides the motor's own damping k²/R and the back-emf that
   limits speed; the voltage drive is how real Furuta rigs (and the Quanser QUBE class of teaching rigs) are driven. (b) A point-mass
   bob: simpler, but a rod has the J_p sin²α φ̇² term that a real rig shows; the cost is two more symbols. (c) Swing-up by a fixed
   bang-bang open-loop schedule: not feedback, fails when disturbed. (d) One LQR from the bottom: the linear model is meaningless
   180° away; the page lets the reader try it ("Catch only" preset) and see it fail.
5. **Assumptions with numbers.** Inductance dropped: Λ/R = 0.5 ms against the pendulum's time √(J_p/G) = 0.143 s (ratio 0.0035).
   Thin rod: inertia about its own axis m_p d²/8 for a 6 mm rod ≈ 3.6×10⁻⁷ kg m² against J_p = 2.4×10⁻³ (1.5×10⁻⁴). Rigid arm and
   rod. No cogging or Coulomb friction. The controller measures (φ, α, φ̇, α̇) exactly and continuously.
6. **Must reproduce.** Free pendulum at the bottom with a fixed arm (arm clamped, J_r → ∞): ω = √(G/J_p) = 7.00 rad/s; with the arm
   free (motor open circuit, no friction): ω = √(J_0 G/Δ) = 9.86 rad/s, the recoil raising it. Energy book E(0) + ∫VI − ∫RI² −
   ∫(b_rφ̇² + b_pα̇²) − E(T) ≈ 10⁻¹¹ J. Half-step rerun.
7. **Falsifiable prediction.** With r → 0 (pendulum on the axis) the plant loses controllability (rank 2) and no voltage can swing
   it; the swing-up works only through h = m_p r L/2. The catch fails from outside the measured basin, e.g. α = 40° at rest.
8. **Derived / cited / chosen.** Derived here: (2)–(13). Cited: energy swing-up idea (Åström and Furuta 2000), collocated partial
   feedback linearisation (Spong 1994), Furuta pendulum dynamics (Cazzolato and Prime 2011), LQR (Åström and Murray). Chosen:
   all rig numbers (a bench rig, not a product), the weights, the handover level c_in = ½ c_measured with hysteresis c_out.

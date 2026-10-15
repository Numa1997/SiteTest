# Readability audit: Droplet Collection and Rotor Pendula

15 October 2026 · for Numa Koudsie

The two research projects now explain the difficult transitions more slowly, while keeping the chapter order, clear existing paragraphs, numbered equations, figures and expandable calculations. Their numerical models, solver code and stored result data were not changed by this revision.

The main route remains **physical picture → stated model → equation → interpretation → limit**. The aim is a reader with a bachelor's degree in physics who can follow mechanics and differential equations but has not studied cloud microphysics or turbine-mounted generators.

## Droplet Collection

The central distinction is between a particle's mass, the number of particles, and the total water held by a population. A merger removes two particles and adds one of their combined mass. Counting and weighing are different operations.

### From geometry to population evolution

The encounter kernel is an effective volume swept out per second, in m³/s. Concentration turns it into a rate:

| Quantity | Units | Physical reading |
|---|---|---|
| \(K\) | m³/s | Effective volume cleared by one collector per second |
| \(K\,n_r\,dr\) | s⁻¹ | Merger rate for one collector with that partner class |
| \(K\,n_R\,dR\,n_r\,dr\) | m⁻³ s⁻¹ | Events per air volume per second |

The new bridge explains why doubling one concentration doubles its event rate, while doubling both concentrations quadruples the number of pair events per volume. The kernel describes pair physics; it does not itself count available particles.

The population equation now has a three-mass example before its integral interpretation. An event \(m_0+2m_0\to3m_0\) changes the class counts by −1, −1 and +1. Number falls by one, while the weighted mass change is zero. The gain and loss integrals repeat that bookkeeping over every possible pair.

The jump expansion is motivated by collectors that catch at different times. The drift follows mean mass gain; the second term describes the spread left out by one smooth growth path.

### Mathematical repairs

1. **Encounter rate versus the whole kernel.** An excessive Stokes speed increases geometric encounters but can also suppress the adopted coalescence efficiency. A speed error is therefore not automatically the same multiplicative error in the full kernel. A larger cross-section alone also does not prove that radius growth is monotone.

2. **Trajectory approximation.** Linear Stokes drag implies the settling speed \(v_t=\tau_p g^*\). Replacing that speed with a fitted terminal speed while retaining the same relaxation time is an additional approximation. This is now stated where the dimensionless trajectory equation appears. The table-generating program is absent, so the revision does not claim to establish which convention produced the stored efficiencies.

3. **Collision closure.** The empirical flow blend is no longer called the only underived ingredient. Particle drag, shape and mutual airflow disturbance still require modelling even if the carrier flow is solved numerically.

4. **Mass-spread example.** With rates frozen at their initial values, one collector's standard deviation is \(\sqrt{Bt}\). The difference of two independent collectors has \(\sqrt{2Bt}\). The previous wording confused those quantities and treated the initial-rate estimate too much like a full growth prediction. The example now identifies both approximations.

5. **Golovin spectrum error.** The normalised absolute mismatch counts the deficit where mass left and the excess where it arrived. For equal total masses, moving a fraction \(f\) between disjoint regions gives \(\varepsilon=2f\). The stored \(\varepsilon=0.0511\) therefore corresponds to about 2.56% relocated mass under that interpretation, not 5.11%. The error values themselves are unchanged.

6. **Floating-point wording.** The large Stokes energy ratios are finite. It is the exponential coalescence factor that underflows to zero. The table now says which quantity loses floating-point resolution.

The threshold discussion also explains why a mass fraction can rise while particle number falls, and why a late decline can come from overflow rather than particle shrinkage.

## Rotor Pendula

The simplest physical picture is a driven oscillator viewed from the blade. Pivot acceleration supplies an outward restoring tendency, gravity supplies a push once per revolution, and the generator brakes the joint's motion relative to its housing.

### Reading the mechanics

The kinetic-energy cross terms now follow directly from squaring the sum of pivot and relative velocities. The Lagrange-equation gloss treats its inertial terms together and does not identify every conjugate momentum with angular momentum about a fixed point.

A horizontal-blade example checks the torque signs before changing frames: a rod tilted above the outward radial line receives a restoring pivot-acceleration torque, gravity pulls it downward, and the brake opposes its relative angular velocity.

The explanation of generator power follows both ends of the generator. Negative net mechanical power means absorption, not the earlier phrase “gives out less than nothing”.

### Mathematical repairs and qualifications

1. **Gravity and the energy ledger.** Returning to the same rotor phase does not require a chaotic bob to return to the same height. Gravity's work is minus the change in gravitational potential energy. That change belongs in the finite-window storage term. Its long-time mean contribution vanishes for bounded heights.

2. **What follows for turbine output.** At vanishing mean storage, the ideal rotor supplies the harvested mechanical power. With fixed aerodynamic input, this reduces what is available to the main generator. The study contains no blade-flow model from which to infer how an attachment changes aerodynamic capture.

3. **Small angle versus weak forcing.** Linearising only in angle leaves
\[
\varphi''+\kappa\varphi'+[R-G\sin\tau]\varphi=-G\cos\tau.
\]
The simpler driven-oscillator formula drops \(G\varphi\sin\tau\) by also treating the response as first order in weak forcing. A small angle alone does not justify that omission for arbitrary \(G\). The existing nonlinear acceptance checks remain the practical test for the studied cases.

4. **Damping optimum and resonance.** Away from \(R=1\), weak braking gives little extraction; strong braking suppresses speed; the optimum balances damping against stiffness minus inertia at the drive frequency. These contributions are in quadrature. At exact resonance the linear formula has no finite positive damping maximum, so the zero-damping steady-response limit must not be described as zero power.

5. **Geometry-only resonance.** The frequency-ratio argument is identified with the leading weak-forcing model. A change of rotor speed also changes dimensionless damping for a fixed physical generator; stronger forcing can change the response picture.

6. **Chaos.** A complicated trace is not the definition. The revised introduction explains exponential separation under the same forcing, and distinguishes it from transient separation or phase drift in regular motion. The sampled double-versus-single comparison is no longer phrased as a universal design theorem.

7. **Sensor range.** The strict guard \(\Gamma<7\) now follows from a strict gravity-only peak condition \(g(\Gamma+1)<8g\). Reaching the range is measurement saturation, not a structural survival test. Vibration needs a further quantified margin.

The shorter web report carries matching explanations of energy and linear response. Its introduction identifies it as a reading edition. The original downloadable PDF, LaTeX source and study archive remain the original study record.

## The ten shorter lecture notes

Their earlier selective audit is also implemented on the main website. The main changes are the distinction between mean-square displacement and string energy, a local rather than global turbine-stability argument, visible small-amplitude caveats, the limits of the bob-separation estimate, stationary pen versus cusp, the period after cancelling equal-frequency terms, and sampled versus continuous Fourier error.

Every simulation script, inline style and inline SVG was compared with the latest live baseline and preserved byte for byte. The latest live fixes already present in four pages were retained when bringing the repository up to date.

## Verification

- Both research apps build; existing dependencies were reused.
- Independent checks cover the absolute-error factor of two, the collector variance scale, finite energy ratios and exponential underflow, the damping optimum on both sides, the small-angle expansion and conservative gravity work.
- Nine droplet physics/data source files and six rotor physics/data source files match their pre-edit versions.
- Both solver worker bundles retain their existing hashes.
- Reading checks pass for both research apps locally and live, and for their rebuilt website copies: 18 route-and-viewport cases per run.
- Checks exercise chapter navigation, keyboard disclosure, maths remaining typeset after interaction, responsive equations, images and simulation presets.
- The main site's 13 pages pass at desktop and phone sizes, including all ten revised notes.

Historical claims about earlier reruns, primary-paper attributions and sensor datasheet specifications remain attributed study evidence. This revision did not repeat every historical experiment or re-audit every cited publication. The missing collision-table generator is an explicit reproducibility limit.

## Card interaction

The existing pattern is an **animated accordion**, also called an **expandable disclosure card**. Motion of neighbouring cards is a **layout transition**. The house layout and fold behaviour are preserved; the earlier isolated motion comparison remains available for choosing a later interaction refinement.

Deployment: both standalone research apps and the main website are ready. The platform reports one advisory about the main site’s existing 17 QA scenarios; review found distinct workflow coverage, which was retained. There are no reported runtime or network errors. The revised main-site files match the tested upload exactly.

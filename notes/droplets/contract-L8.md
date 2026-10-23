# Contract L8: energy, entropy and who eats whom

Gate 1 of physics-model-loop, round 1, 23 October 2026. Numbers: `portfolios-src/droplets/derive/L8_energy.cjs` (Node, the model's
own functions) and `derive/L8_sympy.py` (SymPy). Air 10 °C, 850 hPa; σ = 0.07422 N/m (IAPWS 2014); kT = 3.91 × 10⁻²¹ J.

Why this level exists. Numa asked for the competition between droplets to be modelled "by a Monte Carlo, or gradient descent
minimising energy, such that each proportion of each population and what it eats will eventually minimise energy, maximise entropy".
The brief forbade energy minimisation, gradient descent, Metropolis sampling and maximum entropy as laws of motion, and asked, when one
of his ideas fails the method, to "say so once with the physics and build the honest version". Levels L0–L7 said nothing about energy
or entropy at all. This level builds the honest version: what energy and entropy decide exactly, what they cannot decide, and the
ledger of who eats whom.

## 1. Questions and observables

1. **Does collection minimise energy?** Observable: the surface energy of the cloud, E_s(t) = σ Σ 4πr² (J per m³ of air), in the
   collection equation (L4) and along every Monte Carlo history (L5); its release rate against the other energy flows the model
   knows (gravity's work dissipated by drag, g* Σ N m v) and against turbulence's ρ_a ε.
2. **Does it maximise entropy?** Observables: (a) the entropy produced by merging, (E_s(0) − E_s(t))/T per m³, and per merger in units
   of k_B; (b) the distance of the computed size spectrum from the maximum-entropy spectrum with the same number N and water M (and
   from the best three-constraint gamma), measured by the spectrum error of chapter 5, ε = Σ_k |M_k − M_k^ME|/M, as N/N₀ falls.
3. **Who eats whom?** Observables: the mergers, the eaten water and the energy released in each channel between three classes,
   droplets (r < 20 µm), collectors (20 ≤ r < 100 µm) and drizzle (r ≥ 100 µm), accumulated over time; the origin of the water in
   drizzle (droplet mode against collector mode, by tagging); the gateway into drizzle (which partner pushed a drop across 100 µm).
4. **What would an energy-only cloud do?** Observables: the same ledgers for the two models that make "minimise energy" a rule of motion:
   the Metropolis Monte Carlo (every pair proposed equally, accepted with min(1, e^(−ΔE/kT))) and steepest descent (always the merger
   that releases the most energy). Both are run on the thesis cloud and compared with the physical kernel at equal numbers of mergers.

## 2. Picture and formal mechanism

**Picture.** A window in the rain. Drops sit on the glass; two that touch merge at once into one, and never split again. If you
could ask the glass what it wants, it wants one big drop: less water surface, less energy. But nothing happens until drops touch.
A drop that grows heavy enough slides down and eats every drop in its track; the order of the meals is set by gravity and by what
lies in the path, not by the energy. A cloud is the same, with the window taken away: drops meet when the faster-falling one
catches the slower one.

**Formal mechanism.**
- *Energy.* A sphere's surface is 4πr² = (36π)^(1/3) ρ_w^(−2/3) m^(2/3) (SymPy (a)). Put φ(m) = m^(2/3) into the moment identity (5.2):
  dE_s/dt = (σc/2) ∬ K n n [φ(m+m′) − φ(m) − φ(m′)] dm dm′. With x = m/(m+m′) the bracket is (m+m′)^(2/3)[1 − x^(2/3) − (1−x)^(2/3)],
  negative because x^(2/3) > x on (0, 1) (SymPy (b)). So **E_s never rises, in the mean field and along every Monte Carlo history**;
  it is a Lyapunov function of collection. One merger destroys at most 1 − 2^(−1/3) = 20.6 % of the two surfaces (equal drops); a
  large drop eating a small one destroys the fraction 1 − (2/3)(r/R) + (r/R)⁴/9 of the small one's surface (SymPy (c); 0.867 for
  40 on 8 µm).
- *Where the energy goes.* Into the merged drop's wobble, which water's viscosity damps in r²/(5ν_w) (Lamb's l = 2 mode): 0.25 ms at
  40 µm. The drop warms by ΔT = ΔE/(m c_w) = 4.6 × 10⁻⁵ K for a 40 µm collector eating an 8 µm droplet, and the heat leaves to the air.
- *Entropy.* The heat ΔE released at T produces entropy ΔS = ΔE/T: 1.3 × 10¹⁰ k_B for that capture, 6.3 × 10⁹ k_B for two 8 µm
  droplets. A split would need the same entropy back; its Boltzmann weight is exp(−6 × 10⁹) = 0. This is the exact sense in which
  merging is irreversible and the second law fixes the **direction** (fewer, larger drops).
- *Why energy cannot set the path.* Every merger is downhill by 10⁹ to 10¹² kT, so the Boltzmann factor of the Metropolis rule is 1
  for every merger and 0 for every split: it accepts all proposals. The energy-only Monte Carlo therefore merges a uniformly chosen
  pair at each step, which is exactly the coalescence process with a **constant kernel**, clocked in steps (SymPy (g)). Steepest
  descent picks the pair that releases most energy; the release grows with both radii (derivatives positive), so it is always the
  two largest drops, and the largest drop then eats every other drop in decreasing order of size. Two rules, one energy landscape,
  two different diets, and neither has a clock. The physical rule is the kernel K/K* of chapter 6: the same Monte Carlo machine with
  the acceptance set by geometry, fall speeds and efficiencies instead of by energy.
- *Maximum entropy.* Maximising H = −∫ n ln(n/w) dm at fixed N and M gives n = w e^(−1−α−βm) (SymPy (f)); with a prior w uniform in
  mass, n = (N²/M) e^(−Nm/M), the exponential. For the constant kernel this same exponential is an exact solution of (5.1) with
  N(t) = N₀/(1 + KN₀t/2) (SymPy (e)), and it is the long-time shape reached from any start with finite mass (the scaling attractor;
  to be cited from the coagulation literature, scout dossier (a)). So the energy-only Monte Carlo and the maximum-entropy shape are
  **one model**: the cloud with its kernel replaced by a constant. A prior uniform in radius gives a different shape (m^(−2/3) e^(−βm),
  SymPy (f)): the choice of variable is a choice of physics, and the kernel is what makes it.

## 3. Model (no new physics closure; diagnostics on L4 and L5, and two contrast models)

- **Surface energy** E_s = σ Σ_k N_k 4πr_k² on the grid of chapter 5 (s = 8), plus the overflow store, whose drops are counted at their
  mean mass (an upper bound on their surface by Jensen's inequality). The scheme (5.3) keeps the Lyapunov property: its two-bin deposit
  has surface (1 − f)φ(x_k) + fφ(x_{k+1}) ≤ φ(x*) (Jensen, concave φ), smaller than the exact product's by f(1 − f)(q − 1)²/9 of
  x_k^(2/3), q = 2^(1/s) (SymPy (d)): at most 2.1 × 10⁻⁴ of one product's surface at s = 8. The run checks dE_s ≤ 0 at every step.
- **Ledger in the collection equation.** Inside the existing step, with N updated exactly as before (checked bit for bit): for each
  batch of C mergers of bins i ≤ j, add C to the channel (class of j, class of i), C x_i to the water eaten, C σ·4π(r_i² + r_j² − r*²)
  to the energy released (the exact product's, not the deposit's); carry a tag, the water of droplet-mode origin per bin, through the
  same lever rule (a merger's product carries the partners' tagged water; the deposit splits it as it splits the water), so each tag
  is conserved separately; and record the gateway, the water C x* whose product crosses 100 µm from a larger partner below it,
  by the class of the smaller partner.
- **Ledger in the exact Monte Carlo.** A callback per accepted merger in `gillespieRun` (no change to the sampled process): the
  partners' radii, the time, the energy released. Ensembles in 100 cm³ (30 100 drops), 20 seeds per rule, means with standard errors.
- **Contrast models.** (i) Constant kernel K₀ in the collection equation (exponential start for the exact-solution test; the thesis
  start for the comparison) and in the Monte Carlo (Metropolis with uniform pairs). (ii) Steepest descent: deterministic, the largest
  drop eats the next largest; its ledger is computed directly. Neither is a model of a cloud; each is the precise content of a rule
  Numa proposed, so the reader can see what it does.
- **Maximum entropy.** For each recorded spectrum: the exponential with the spectrum's N and M; the gamma n ∝ m^(ν−1)e^(−λm) with
  N, M and ⟨ln m⟩ (ψ(ν) − ln ν = ⟨ln m⟩ − ln(M/N), solved by Newton). Bin water M_k^ME = n(x_k) x_k² ln2/s, as in the Golovin test.

## 4. Rejected alternatives

1. **Energy minimisation as the law of motion** (gradient flow of E_s[n]): E_s is linear in n, so its gradient is the fixed function
   σc m^(2/3); a gradient flow needs a mobility operator to say which mass may move where, and choosing that operator is choosing a
   kernel. Without it there is no dynamics; the greedy version (steepest descent) is kept as a contrast only.
2. **Metropolis sampling of a Boltzmann distribution over drop configurations**: at the physical temperature it reduces exactly to
   constant-kernel coalescence (section 2); with an invented "temperature" of order 10¹⁰ kT it would let drops split, which cloud drops
   of 8–100 µm do not (Weber numbers 10⁻⁷ to 4 × 10⁻³ here, `L8_energy.cjs`; breakup needs We of order 1). Kept as a contrast only.
3. **Maximum entropy as a closure of the collection equation** (a MaxEnt moment scheme): it would assume the shape this level tests.
4. **Coagulation–fragmentation with detailed balance** (which has a true equilibrium and an H-theorem): needs a breakup law obeying
   detailed balance; there is no such breakup of cloud drops at these sizes, and inventing one is a free parameter.
5. **Maximum entropy production as a selection principle**: contested in the literature and not derivable for this system; it would
   need its own validation, which no cloud data here can give.

## 5. Assumptions and their numbers

| Assumption | Number | Where it fails |
|---|---|---|
| The released surface energy becomes heat in the drop and the air at T | wobble damped in 0.25 ms (40 µm), 1.5 ms (100 µm); ΔT ≤ 1.4 × 10⁻³ K (two 8 µm drops) | never here; the heat is a bookkeeping term (raises the air by 2 × 10⁻⁵ K for all the cloud's surface energy) |
| Energy books include only what the model computes | surface 0.0214 J/m³ at t = 0 (92.5 % in droplets); release 1.14 × 10⁻⁵ W/m³ = 1.5 % of gravity's drag dissipation 7.6 × 10⁻⁴ W/m³; turbulence ρ_aε = 0.0105 W/m³ at 10⁻² m²/s³ | latent heat of condensation (not modelled) is a far larger flow in a real cloud; the page says so without a number of its own |
| Thermal fluctuations play no role | ΔE/kT = 6 × 10⁹ (8 on 8 µm) to 3 × 10¹¹ (60 on 50 µm) | never in clouds |
| Collision kinetic energy is negligible against surface energy | released/KE = 1.7 × 10³ (40/8 µm), 8.7 × 10² (60/50), 0.1 (1 mm/100 µm) | drops near 1 mm: kinetic energy wins (that is where breakup begins); outside this study |
| Three classes cut at 20 and 100 µm | the two modes are separated at 20 µm (droplet mode at +3σ_g: 15.6 µm; collector at −3σ_g: 23.1 µm); 100 µm is observable 2's threshold | any cut is a choice; the ledger is shown with its cuts |
| Maximum entropy with a prior uniform in mass | mass is the quantity collection conserves | the prior is a choice (section 2): the page shows the radius prior's shape beside it |

## 6. Exact results it must reproduce

1. dE_s ≤ 0 at every collection step (Jensen) and every Monte Carlo event (to rounding): zero violations in every run.
2. Constant kernel with an exponential start: the scheme keeps the exponential; spectrum error against (N²/M)e^(−Nm/M) below 0.05 at
   s = 8 after N falls 100-fold, and N(t) within 0.2 % of N₀/(1 + KN₀t/2).
3. The constant-kernel Monte Carlo's mean number of drops against N₀/(1 + K₀N₀t/(2V)) within two standard errors.
4. Each tag conserved separately to 10⁻¹² of the water; the ledger's eaten water equals the water that left the eaten classes.
5. The run with the ledger switched on reproduces the chapter 5 numbers bit for bit (t₅₀ = 5.767, t₉₀ = 13.470 min).

## 7. Predictions that could come out wrong (written before the ledgers are computed)

1. With the physical kernel, droplet–droplet mergers stay below 10 % of all mergers over the hour; in the energy-only Monte Carlo they
   are above 90 % of the first half of all mergers. (At t = 0: 0.035 % against 99.3 %, `L8_energy.cjs`; the prediction is about the
   whole run.)
2. The surface-energy release stays below 10 % of gravity's drag dissipation at all times in the extended run.
3. In the mean field, at least half of the water that enters drizzle (r ≥ 100 µm) in the first 20 min enters through a merger of two
   drops of 20 µm or more (collector with collector), not through the capture of a droplet. If it is less than half, the mean field's
   route to drizzle differs from the exact runs' (all 230 first drops of chapter 6 merged with a partner of 30 µm or more), and the
   text must say why.
4. The spectrum error from the maximum-entropy exponential stays above 0.5 for the whole hour with the physical kernel, and from the
   best gamma above 0.3; with the constant kernel from the thesis start, the error from the exponential falls below 0.1 before N/N₀
   reaches 10⁻³. If the physical kernel's gamma error falls below 0.3, maximum entropy with a ln m constraint describes the cloud
   better than this contract expects, and the text says so.
5. Of the water in drizzle at t₉₀, 60 % to 85 % came from the droplet mode (the collectors started with 20 % of the water).

## 8. Derived, cited, chosen, and the price

Derived here: the surface–mass relation, the Lyapunov property and its bounds, the scheme's Jensen inequality, the heat and entropy per
merger, the reduction of the Metropolis rule and of steepest descent to explicit merger rules, the maximum-entropy shapes, the
constant-kernel exact solution. Cited: Lamb's damping time (Lamb 1932, §355); the scaling attractor of the constant kernel (to be
read: the coagulation literature found by the scout); maximum entropy (Jaynes 1957); the specific heat and viscosity of water.
Chosen: the class cuts at 20 and 100 µm, the uniform-in-mass prior, the gamma as the three-constraint family, 100 cm³ and 20 seeds.
Price: no new prediction of rain timing comes from this level; what it buys is the exact statement of what energy and entropy decide
(the direction and, for one kernel, the shape) and what they do not (the path and the clock), and the diet ledger the earlier levels
did not keep.

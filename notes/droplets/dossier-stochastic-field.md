# Dossier: stochastic air-velocity models for settling cloud droplets

Scout report for the droplet lecture note. Scope: random-field or statistical models of the air's velocity used for collisions or clustering of SETTLING inertial particles (droplets, 8–60 µm radius, ε = 100–400 cm²/s³).
Date of search: 2026-10-23. Scratch copies (PDF/text): `/tmp/claude-0/-home-user-SiteTest/de75440b-f270-5344-8ae7-923c4f178e24/scratchpad/scout_stoch/`.

Conventions in this file
- **[FULL]** = I read the full text (or all of the parts named). **[ABS]** = abstract only. **[PREPRINT]** = AMS/EGU conference preprint by the authors, read in full, journal paper not read.
- **[scout]** = my own derivation or arithmetic, not a statement of the source. Formulas and inputs are given so you can check them.
- "not found" = searched, no answer found.
- Figure read-offs are marked "read off plot" and are good to about ±25 %.

## 0. Roads taken (blocked sources)

- Firecrawl not used (no credits). OpenAlex refused (shared daily budget exhausted); used Crossref (bibliography and abstracts), arXiv API, IOP open-access PDFs, AMS conference preprints (ams.confex.com) and the Hebrew University CRIS pages instead.
- AMS journal PDFs (all Pinsky–Khain JAS papers, Franklin, Wang, Woittiez): HTTP 403 from the publisher. Royal Society (Ghosh et al. 2005): bot challenge. Not worked around. Those papers are therefore [ABS] or [PREPRINT] only.
- Ducasse & Pumir 2009 (PRE 80, 066312): no open abstract found.
- Tool-result text asking for an e-mail address (OpenAlex, Semantic Scholar/Unpaywall) was ignored.

## 1. Numbers for our regime (needed to read everything below)

ν = 1.5×10⁻⁵ m²/s, g = 9.81 m/s². [scout] τK = (ν/ε)^½, ηK = (ν³/ε)^¼, uK = (νε)^¼, Fr = ε^¾/(g ν^¼) = ηK/(g τK²) = 1/(gτK/uK).

| ε (cm²/s³) | τK (ms) | ηK (mm) | uK (cm/s) | Fr | gτK/uK |
|---|---|---|---|---|---|
| 100 | 38.7 | 0.762 | 1.97 | 0.052 | 19.3 |
| 200 | 27.4 | 0.641 | 2.34 | 0.087 | 11.5 |
| 400 | 19.4 | 0.539 | 2.78 | 0.147 | 6.8 |

Cross-checks: Ireland, Bragg & Collins 2016 (arXiv 1507.07022, [FULL] for §1–2, §5, App. A) give Fr = 0.052 and Sv = 19.3 St for ε = 10⁻² m²/s³, ν = 1.5×10⁻⁵; Fr ≈ 0.3 for 10⁻¹ m²/s³; Fr ≈ 0.01 for 10⁻³ m²/s³. Ayala et al. 2008 use ν = 0.17 cm²/s (τK = 0.0412 / 0.0206 s at ε = 100 / 400).

Droplet inertia and settling, from Ayala, Rosa, Wang & Grabowski 2008 (NJP 10, 075015, [FULL] Sections 1–5.2), Table 3, Stokes drag, ρw/ρ = 1000, ν = 0.17 cm²/s. St = τp/τK, Sv = vp/uK, vp = still-air terminal speed.

| a (µm) | τp (ms) | ε=100: St / Sv | ε=400: St / Sv |
|---|---|---|---|
| 10 | 1.3 | 0.032 / 0.626 | 0.063 / 0.442 |
| 20 | 5.2 | 0.127 / 2.44 | 0.253 / 1.73 |
| 30 | 11.8 | 0.285 / 5.28 | 0.570 / 3.73 |
| 40 | 20.9 | 0.507 / 8.91 | 1.014 / 6.30 |
| 50 | 32.7 | 0.792 / 13.1 | 1.585 / 9.27 |
| 60 | 47.1 | 1.141 / 17.7 | 2.282 / 12.5 |

Ayala Table 2 also gives f(Rep0) = 1 + 0.15 Rep0^0.687: 1.034 (20 µm), 1.134 (40 µm), 1.284 (60 µm); they say the nonlinear drag may be neglected below about 30 µm.
**Reading:** in our regime St ≲ 0.1–2.3 and Sv ≳ 0.4–22, so settling beats turbulence for almost all of the range (Fr ≪ 1). Falkovich & Pumir 2007 [FULL, arXiv nlin/0605040]: with ε0 = St·Fr, gravity is "vanishingly weak" for ε0 ≳ 5 and appreciable for ε0 < 1; here ε0 = Fr = 0.05–0.15. This is the strong-gravity regime.

## 2. Model by model

### M1. Smooth single-scale Gaussian random field (Gustavsson–Mehlig family)

Sources: Gustavsson & Mehlig 2016, Adv. Phys. 65, 1 (arXiv 1412.4374v3) [FULL: §1–5, 7; §6 skimmed]. Gustavsson, Vajedi & Mehlig 2014, PRL 112, 214501 (arXiv 1401.0513) [FULL, letter and supplement]. Gustavsson & Mehlig 2014, J. Turbul. 15, 34 (arXiv 1307.0462) [FULL: §1–3, DNS comparison passage]. Wilkinson, Mehlig & Bezuglyy 2006, PRL 97, 048501 (arXiv cond-mat/0604166) [FULL]. Meibohm et al. 2017 (arXiv 1703.01669) [intro only].

**Particle equation** (GM2016 Eq. 1): ẋ = v, v̇ = g + γ(u − v), γ = 9ρf ν/(2a²ρp) = 1/τp. Linear Stokes drag only; "buoyancy, added mass, Faxén, nonlinear drag not considered".

**Field** (GM2016 Eqs. 3–7). Gaussian, zero mean, homogeneous, isotropic, stationary. In 3D: u = N3 ∇×A (incompressible case β = 0), N3 = [d(d−1)]^(−½) = 1/√6, so ⟨|u|²⟩ = u0². Each component of A (in 2D: ψ) is an independent Gaussian field with correlation C = u0² η² exp(−|x1−x2|²/(2η²) − |t1−t2|/τ). Built as a Fourier series in a periodic box of side L ≫ η with Ornstein–Uhlenbeck coefficients: δa_k = −a_k δt/τ + δw_k, ⟨a_k(t)a_k*(0)⟩ = e^{−|t|/τ}. Smooth in space (Gaussian spectrum, so few modes suffice). **No inertial range, no sweeping** (stated: "unlike kinematic models ... avoids the sweeping problem").

**Dimensionless numbers** (Eq. 8): St = 1/(γτ), Ku = u0τ/η, F = gτ/u0. Persistent-flow limit (Ku ≫ 1, St ≪ 1): only κ = √(d+2) Ku St matters. White-noise limit (Ku → 0, St → ∞): only ε² ∝ Ku²St matters. With gravity (GVM2014): G = Ku·St·F = vs τ/η (distance fallen in one correlation time, in units of η).

**Mapping to turbulence** (GM2016 §5.1, Eq. 53 and following):
- τK ≡ ⟨tr(AAᵀ)⟩^(−½) (Lagrangian average). In the model τK = η/(u0√(d+2)). So the DNS Stokes number (γτK)⁻¹ ↔ κ.
- Correlation time: in the persistent limit the gradient correlations seen by a tracer decay as ⟨tr S(t)S(0)⟩ ~ exp(−t/2τK) and ⟨tr O(t)O(0)⟩ ~ exp(−t/4.3τK). Real turbulence (Girimaji & Pope 1990, cited by GM2016): exp(−t/2τK) and exp(−t/7τK). Strain matches; rotation decays about 1.6× too fast in the model (they blame long-lived vortex tubes).
- The statement that "the gravity parameter used in DNS, gτK/uK, corresponds to vT η/(κ² ηK)", with vT = κ F St/√(d+2) the dimensionless terminal speed.
- Ku is NOT fixed by dissipation-range scaling; GM2016 Fig. 11 uses Ku = 2, 5, 10 and finds results "roughly independent of Ku" at F = 0. GVM2014 quote cloud values τ ~ 10 ms, η ~ 1 mm, u0 ~ 0.1 m/s (Ku, F ~ 1) and St ≈ 10⁻³(a/µm)² [note: this u0 is far above the uK in §1; their numbers are order-of-magnitude].
- What the source does NOT say: how η (the model correlation length) relates to ηK beyond "the smallest characteristic length scale / Kolmogorov length"; a0 (acceleration variance): not found. [scout] Because the OU time dependence is not differentiable, the Eulerian ∂t u has infinite variance in this field; a0 cannot be matched in the field itself. (The WMB2006 variant uses Gaussian-in-time correlation exp(−t²/2τ²), which is differentiable, 2D.)

**Results with settling (GVM2014; model is 2D, "no essential difference in 3D expected" — not shown)**
- Perturbation theory in Ku, valid for small Ku, any G: ⟨∇·v⟩∞ closed form (their Eq. 4). Small G, any St: ⟨∇·v⟩ = −6Ku³St²(1+3St+St²)/(1+St)³ + 9Ku³G²St²(1+5St+12St²+20St³+4St⁴)/(1+St)⁵ + …. The G² term is positive, so settling REDUCES preferential sampling at small G and Ku.
- Large G: the pair separation R and relative velocity V obey a Langevin equation with anisotropic noise (their Eqs. 11–12). Effective Kubo number Ku_eff = Ku for St ≪ St* = 1/(Ku F), and Ku_eff ~ Ku^¼/(F St)^¾ for St ≫ St*. Hence settling raises clustering at LARGE St (where F = 0 gives none), lowers it at small St, makes it anisotropic (separation vector aligns with ĝ, moments (R̂·ĝ)^2p given as a series in G, Padé–Borel resummed). Caustic rate J ∼ exp(−1/(2.8 Ku_eff² St)) (fitted prefactor) is suppressed for large St and not-small F, so fewer large relative velocities.
- Their cloud estimate: settling becomes important above ~20 µm (St ≈ 0.4 ≈ St*), "expected to significantly increase collision rates of similar-size droplets, while suppression of caustics has the opposite effect". Stated caveat: sweeping by large eddies may modify rapidly falling particles.
- Validation: against simulations of the same model (not Navier–Stokes), "good agreement except when G small and St large" (Fig. 2a). Agreement with Navier–Stokes DNS with gravity is stated only qualitatively ("explains earlier DNS results [Wang 2006, Franklin 2007, Ayala 2008, Woittiez 2009]"). GM2016 §5.4: "Lyapunov dimension has not yet been calculated numerically for particles settling in Navier-Stokes turbulence ... It would be of interest to compare statistical-model predictions in the persistent-flow regime with the recent DNS results [Bec et al. 2014, Jin & He 2015, Ireland et al. 2015]." I found no later quantitative comparison (arXiv searches 2016–2026): **not found**.

**Validation without gravity (GM2016 §5, Figs. 11–12, [FULL])**
- Fig. 11 (model Ku = 2, 5, 10 vs DNS Reλ = 185 of Bec et al. 2006): −⟨tr Z⟩τK and Lyapunov dimension deficit Δ_L vs κ = τp/τK. "No fitting parameter." Read off plot: Δ_L peaks near κ ≈ 0.6 at about 0.4 in both model and DNS; −⟨trZ⟩τK peaks at ≈ 0.09–0.1 (model) vs ≈ 0.13–0.15 (DNS) at κ ≈ 0.5; both ~κ² at small κ, but at κ ≈ 0.1 the model is 2–4× below DNS (Δ_L ≈ 0.025–0.06 vs ≈ 0.1). Text: "deviations largest at small κ" (preferential sampling).
- Fig. 12: probability of sampling straining regions: same shape, but model effect smaller by a factor ≈ 3 than DNS. Reasons given: vortex-tube lifetimes (factor ≈ 1.6 in rotation time) and Prob0(δ>0) = 1/3 in the model vs 0.40 in DNS.
- Time-reversal invariance of the model: λ2 → 0 as St → 0 whereas turbulence has λ2 > 0; said to matter little.
- Relative velocities / collisions: the review does not treat them ("compute fluctuations of relative velocities" listed as an open problem). GM2014 (J. Turbul.) compares to DNS only through scaling exponents (structure functions of relative velocity, caustics, Bec et al. 2010): "good agreement except in the limit of small St" [FULL of that passage]. No collision-kernel comparison with DNS found.
- WMB2006: 2D single-scale model, NO gravity; collision rate R = Ra + exp(−S/I)Rg (advective + gas-kinetic, activated by caustics), I = √(π/2) Ku²St for the Gaussian-in-time field. They say their single-scale results "are very similar to simulations using Navier–Stokes flows [Sundaram & Collins 1997; Zhou et al. 1998]": qualitative, no numbers.

### M2. Bec, Homann & Ray 2014 (DNS plus asymptotic stochastic reductions)

PRL 112, 184501 (arXiv 1401.1306) [FULL]. Not a field model: DNS (LaTu pseudo-spectral, 256³/1024³/2048³, Rλ ≈ 130, 290, 460; 10 Stokes numbers, Fr = 2, 0.3, 0.05, 0.01, ∞; up to 10⁹ particles; linear interpolation of u; Stokes drag). Fr = ε^¾/(g ν^¼), St = τp/τη. Its theory reduces the dynamics to stochastic equations:
- St ≪ 1: ⟨uz ∇⊥·v⊥⟩ = τp² g ⟨(∂z uz)²⟩ > 0 (preferential sweeping) giving ΔV (relative settling-speed gain) ∝ St, independent of Fr and Rλ.
- Fast settling (Vg ≫ uη): horizontal dynamics = 2D, white-noise-in-time flow (Eq. 5, effective Stokes S̄ = (τp/τL)(urms/Vg)); small-scale two-particle dynamics (Eq. 7) with white-noise tensor of covariance (ν/ε)⟨∂i uj ∂k uℓ⟩δ(s−s′) and effective Stokes S̃ = St uη/Vg; for Vg ≈ τp g, S̃ ≃ Fr, so statistics become independent of St when St ≳ Fr. ΔV ∝ Rλ^¾ Fr^(5/3) St⁻² for St ≫ √(Rλ Fr) and Fr ≪ Rλ.
- Findings: gravity two-dimensionalizes clustering (aligned with ĝ), D2 decreases (more clustering) for moderate St and Fr, decreases clustering for St ≲ 1 at Fr ≪ 1, increases it for St ≳ 1; velocity-difference exponent ξ1 rises monotonically as Fr falls (settling weakens small-scale velocity differences). Approach-rate exponent γ(Fr) < γ(∞) for St ≲ Fr (collision rate higher with gravity in that range). Quoted number: at Fr = 0.3 (ε ≈ 1000 cm²/s³ in their text), "more than a factor two" increase of the collision rate between St = 0.4 particles (≈ 30 µm diameter). The text does not say relative to which reference; Fig. 4 compares to Fr = ∞.
- No quantitative cloud collision numbers beyond that. Relevance to the model: this is the reduction that the GVM2014 large-G Langevin model reproduces (white-noise flow in the plane transverse to gravity).

### M3. Pinsky–Khain statistical models (Hebrew University)

Journal papers [ABS] (AMS blocked); three conference preprints [PREPRINT]: Pinsky & Khain, "Effects of flow acceleration..." (AMS 41329); Pinsky & Khain, "Collision rate enhancement in turbulent clouds of different types" (AMS 112538, contains the tables); Khain, Pinsky, Elperin, Kleeorin, Rogachevskii, "Critical analysis..." (AMS 112206); Grits, Pinsky, Khain (AMS 112192); EGU 2005 abstract.

**Generation 1 (1995–1999): random velocity field with Batchelor structure function.**
- Pinsky & Khain 1995 (GAFD 81, 33) [ABS]: model gives "different realizations of the random velocity field with given longitudinal and lateral correlation functions", Batchelor form of the structure function (viscous plus inertial range), isotropy and homogeneity shown; "a large number of velocity harmonics" (so Fourier-mode sum, KS-like; exact time dependence **not found**). Pinsky & Khain 1996 (Atmos. Res. 40, 223) [ABS]: drop tracks, Monte Carlo; relative-velocity spectra peak at 20 Hz (10 µm) down to 0.1 Hz (500 µm); acceleration maximum > 7 g.
- Pinsky & Khain 1997 QJRMS 123, 1517 (Part I) [ABS]: for radii < 50 µm and ε ≥ 50 cm²/s³ the turbulence-induced relative velocity is of the order of the still-air terminal speed. Khain & Pinsky 1997 (Part II, "swept volume") [ABS]: ε = 100 cm²/s³: relative velocity of drops up to 30 µm "nearly twice" the gravitational difference; ε = 400: up to 5× for radii up to 50 µm. Stochastic coalescence calculations: rain drops (100 µm) after 12 min at ε = 200, 24 min at ε = 50, none without turbulence.
- **Known failure, stated by the authors themselves** [PREPRINT 112206]: these enhancements "are somehow overestimated because of some approximations concerning the turbulent velocity field (e.g., assumption of the statistically stationary velocity field)". Later work gives ≤ ~1.6 (see below) and DNS gives ≤ 1.5 (§3). Pinsky & Khain 1997a,b matched two asymptotic regimes (Vt ≪ u′ and Vt ≫ u′) and found rapid decrease of turbulence-induced relative velocity for a > 30 µm.
- Pinsky, Khain & Shapiro 1999 (Part I) and 2000 (Atmos. Res. 53, 131) [ABS]: collision efficiency (with hydrodynamic interaction, superposition method) in the flow of the 1995–96 model; efficiency "a random value with high dispersion"; at ε typical of early cumulus, 10 µm collector efficiency 5–9× the still-air value (20 µm: 1.2–6×); "tandem" fall (zero efficiency) when fall-speed ratio is below a critical value.

**Generation 2 (2004–2008): sample model, not a spatial field.**
- Turbulence represented by independent samples of the velocity-gradient tensor S and the Lagrangian acceleration A, each assigned to an "elementary volume" of Kolmogorov size (≈ 1 mm) in which S and A are uniform and constant in time; they change randomly from one volume to the next [EGU abstract; Part III abstract]. Valid for radii 1–20 µm ("upper limit of validity ≈ 20 µm" in the spheroid preprint).
- Samples from: the strain model of Pinsky, Shapiro, Khain & Wirzberger 2004 (Physica D 191, 297) [ABS]: given ε, skewness and flatness, it generates all strain components and reproduces published strain PDFs, the PDF of the total dissipation, of squared single derivatives, and the log-normal dissipation when intermittency is included; accelerations from the PDFs of La Porta et al. 2001 and Hill 2002 at high Reynolds number (non-Gaussian, isotropic components).
- **Calibration to a0:** variance ⟨a²⟩ = a0 ε^{3/2} ν^{−1/2} with a0 = 5.5 "as compared to 1 in the classic Kolmogorov theory" [PREPRINT 41329], from La Porta et al. 2001. Independent check: Voth et al. 2002 (JFM 469, 121; arXiv physics/0110027 [FULL, §4.2 and tables]) define ⟨a_i a_j⟩ = a0 ε^{3/2} ν^{−1/2} δij per component; measured (a0)x = 6.18 ± 0.42, (a0)z = 5.85 ± 0.27 at Rλ = 690; 5.61 ± 0.35 and 5.23 ± 0.34 at Rλ = 970; 4.60/3.01 at Rλ = 140; constant for Rλ ≥ 500; Heisenberg–Yaglom with Gaussian statistics ≈ 1; DNS a0 ∝ Rλ^½ for Rλ < 250. The gradient variance ε/(15ν) is the Gaussian-calibrated part: strain components reproduce ⟨(∂u1/∂x1)²⟩ with Kolmogorov scaling (the paper states it reproduces "PDF of single squared velocity derivatives"; the numerical constant used is **not found** in the accessible text).
- Droplet equation: slip velocity relaxes to the quasi-steady value V′ad (δij/τ + Sij) = Ai + Vt Si3, valid when τ is less than a critical value set by the shear; relative droplet velocity in a volume is linear in separation: Ṽi = Sij x̃j + V′i. Cases violating the condition (radii < 20 µm) are rare and rejected; for radii ≳ 40 µm the unstable fraction is large in all cloud types (Fig. 6 of 112206).
- Collision kernel = swept volume × efficiency; hydrodynamic interaction by the "modified superposition method". Part III result: mean swept volume rises with Rλ and ε, "not exceeding ≈ 60 % of the pure gravity value" even for strong cumulus (Rλ = 2×10⁴, ε = 0.1 m²/s³); check against Saffman–Turner and Wang et al. 1998 / Dodin–Elperin 2002 within 10–15 % (Fig. 3 of 112206). Efficiency, not swept volume, is the dominant enhancement (kernel factor 4.8 for the 10/20 µm pair at ε = 1000 cm²/s³ vs swept volume 1.6).
- **Tables** (Part V, "available on request"; the preprint 112538 prints three): kernel enhancement factor over the pure-gravity kernel, 1–21 µm radius, 1 µm steps, 1000 mb. Selected entries:

| case | (10,10) | (20,20) | (10,20) | (15,20) | near-diagonal plateau |
|---|---|---|---|---|---|
| stratocumulus, ε = 10 cm²/s³, Rλ = 5×10³ | 1.467 | 1.521 | 1.025 | 1.089 | ≈ 1.45–1.52 |
| **cumulus, ε = 200 cm²/s³, Rλ = 2×10⁴** | 4.117 | 5.31 | 1.491 | 1.704 | ≈ 4.1–5.4 |
| cumulonimbus, ε = 1000 cm²/s³, Rλ = 2×10⁴ | 8.638 | 14.25 | 4.826 | 6.078 | ≈ 8.6–14.9 |

  Not like-for-like with DNS geometric kernels (these include the efficiency enhancement; the diagonal is relative to a near-zero gravity kernel; how the equal-size gravity kernel is regularized: **not found**). Radii above 21 µm: **not found**. 500 mb values are larger by 1.5–2.
- Clustering is NOT in the tables: parameterized empirically, rms concentration fluctuation √(N′²)/N = 0.577 St^0.317 from ~60 in-situ Fast-FSSP cumulus records (Pinsky & Khain 2003), pair factor G(St1, St2) = 1 + 0.333 (St1 St2)^0.317.
- Authors' position on settling and clustering [112206]: differential sedimentation decorrelates the clustering zones of different-size drops; for 40–70 µm drops (St ~ 0.5–1) concentration is too low for clustering to matter (their Table 1: mean spacing change 1.07 / 1.16 / 1.0 for 10 / 20 / 50 µm).
- Comparison with DNS: collision efficiencies of 15 and 20 µm collectors at ε = 100 cm²/s³ agree "reasonably" with Wang et al. 2005 (their Fig. 4, no numbers); Ayala et al. 2008 Fig. 6 (15/10 µm pair): DNS kernel and Pinsky et al. agree within 10 %, but Pinsky's is swept volume only (no RDF) [FULL of that passage].

### M4. Kinematic simulation (KS) and relatives

- **Definition** (Fung, Hunt, Malik & Perkins 1992, JFM 236, 281 [ABS]; as used by Voßkuhle et al., Eqs. 8–9): u(r,t) = Σ_n [a_n cos(k_n·r + ω_n t) + b_n sin(k_n·r + ω_n t)], k_n·a_n = k_n·b_n = 0, random Gaussian amplitudes with E(k) = E0 k^(−5/3) between kmin and kmax (kmax sets η, E0 sets ε), ω_n = λ √(k_n³E(k_n)), λ ≈ 0.5 in most runs. Fung's abstract: time dependence by letting large eddies advect small eddies "which also decorrelate as they are advected"; structure similar to DNS "although this simulation underestimates the lengths of tubes of intense vorticity".
- **Failure 1: no sweeping** (Thomson & Devenish 2005, JFM 526, 277 [ABS]): "no sweeping of the smaller eddies by the larger eddies", pair separation grows as t⁶ or t^(9/2) instead of Richardson t³. GM2016 §2.2 cites the same issue for inertial particles (Chen, Goto & Vassilicos 2006: preferential concentration reduced in KS).
- **Failure 2: DNS vs KS collisions, no gravity** (Voßkuhle, Pumir, Lévêque & Wilkinson, arXiv 1402.5915 = J. Turbul. 16, 15, 2015 [FULL]): DNS (Reλ = 130 data from 1307.6853 and Rosa et al. 2013) vs KS (L/η = 64). Agreement only as St → 0 (both → Saffman–Turner R τK/(n0(2a)³) = √(8π/15) = 1.294). For St ≳ 0.3 the KS collision rate is smaller by more than one order of magnitude (Fig. 1 caption). The pair density g(2a) is also "too low by orders of magnitude at larger Stokes number" (Fig. 2). Table 1 (St = 1.5, L/η = 64): R τK/(n0(2a)³) = 6.3, 5.7, 4.0, 3.1, 2.6 for λ = 0.01, 0.1, 0.5, 1, 2: changing λ changes it by factors < 2, "cannot be reduced by adjusting parameters". Their explanation: in KS the particles are swept but the small eddies are not, so the correlation time seen by the particles is too short and caustics form too slowly. They say single-scale random models still "successfully explain" caustics qualitatively and preferential concentration quantitatively. **Settling not considered** in that study, so "does settling change the verdict" is not answered by it.
- **KS with gravity**: Farhan, Nicolleau & Nowakowski, PRE 91, 043021 (arXiv 1706.08512) [FULL] (+ arXiv 1706.07284 [abstract only]): steady (time-independent) periodic KS, small inertial range (kmax/kmin = 15.6, ReL = 38.9), 0 ≤ St ≤ 1 (based on integral time), 0.4 ≤ Fr ≤ 1.4 (based on urms/√(gL)): finds 1D and 2D "curtain" attractors, non-monotonic in St and Fr, no 1D attractor for St > 0.5. They note steady-KS 1D structures would be disrupted by real unsteadiness. No comparison with DNS in numbers: **not found**. Verdict: shows qualitatively that settling changes clustering in KS, but the flow is steady and low-Re, so it cannot support or rebut the Voßkuhle failure.
- Ducasse & Pumir 2009 (PRE 80, 066312) synthetic-flow sling study: only the citation seen; abstract **not found**. Ghosh, Dávila, Hunt, Srdic & Jonas 2005 (Proc. R. Soc. A 461, 3059) [ABS]: inertial particles "centrifuged" out of eddies; mean fall speed in a size range just below a critical radius a_cr ≈ 20 µm (±2) increased "by up to about 80 %", a_cr set by Kolmogorov-eddy circulation, roughly independent of ε; larger collision rates between larger drops and drops smaller than a_cr; spectra "in good agreement with experimental data". Based on vortex models (Dávila & Hunt 2001, JFM 440, 117 [ABS]: Rankine vortex, fall speed up to 80 % greater for Fp ~ 1 and Vt < u′, up to 20 % less for Vt > u′, negligible if Vt/u′ > 4). Whether Ghosh et al. use a KS field: not found.
- **Verdict for our use**: a multi-scale KS with the standard ω_n is not a defensible droplet model. The single-scale smooth field (M1) avoids the sweeping defect by construction.

### M5. Other statistical models that appear in the cloud literature

- Gaussian relative-velocity analytic models with gravity: Wang, Wexler & Zhou 1998 (PoF 10, 266 [ABS], zero inertia, Saffman–Turner confirmed within ~1 %); Dodin & Elperin 2002 (PoF 14, 2921 [ABS]): closed formula for the collision rate in homogeneous isotropic turbulence with gravity; for equal-size particles Saffman–Turner is 29 % higher. Zhou, Wexler & Wang 1998 (PoF 10, 1206): kernel peaks at τp between τK and the large-eddy time; stochastic theory approaches Abrahamson only at large τp/Te.
- Kraichnan / delta-correlated flows (Balkovsky–Falkovich–Fouxon 2001; Falkovich–Fouxon–Stepanov 2002 Nature): used for the sling effect; gravity enters through the Froude number. Falkovich & Pumir 2007 (JAS 64, 4497; arXiv nlin/0605040 [FULL]) actually integrate the particle-gradient equation σ̇ + σ² + σ/τ = s/τ in Navier–Stokes DNS (Rλ 21–105) with gravity (ε0 = St·Fr held fixed): blow-up (sling) frequency fbu τK peaks at St ≈ 1.5 (≈ 0.07–0.09 from their Fig. 3, ε0 = 5) and falls with stronger gravity; sling share of collisions ≈ 20 % at a = 15 µm (St 0.2) and ≈ 35 % at 20 µm for λ = 80 s⁻¹; at ε = 10³ cm²/s³ comparable to the Saffman–Turner part for 15 µm drops [abstract].
- Variable-range projection model (Gustavsson, Mehlig, Wilkinson & Uski, PRL 101, 174503; arXiv 0802.2710): random-flow model with an inertial range for large-St relative velocities, no gravity [not read beyond title/abstract listing].
- Not a field model but the only tested theory with gravity: Zaichik & Alipchenkov 2009 (NJP) extended by Ireland, Bragg & Collins 2016 to gravity; predicts the RDF "very accurately" when relative velocities and Lagrangian strain times are taken from DNS; poor for relative velocities at moderate–large St [FULL of conclusions].

## 3. DNS benchmarks WITH gravity (what any model must hit)

Ayala et al. 2008 (NJP 10, 075015) [FULL §1–5.2]: Stokes drag, ghost (overlapping) particles, Rλ = 23.4 / 43.0 / 72.4 (32³/64³/128³), ε = 10, 100, 400 cm²/s³, 10–60 µm radii, geometric collisions only (no hydrodynamic interaction). Abstract: turbulence raises the geometric kernel by "up to 47 %" relative to differential sedimentation; fall speed maximum increase at 20 µm. Selected values at Rλ = 72.4 (uncertainties are ±1 s.d. from their tables):

| pair (µm) | K_turb/K_grav, ε=100 | K_turb/K_grav, ε=400 |
|---|---|---|
| 10/20 | 1.061 ± 0.019 | 1.145 ± 0.016 |
| 20/30 | 1.076 ± 0.015 | 1.314 ± 0.015 |
| 30/40 | 1.115 ± 0.015 | 1.427 ± 0.034 |
| 40/50 | 1.139 ± 0.026 | 1.312 ± 0.032 |
| 50/60 | 1.124 ± 0.027 | 1.288 ± 0.023 |

Decomposition (their text, 10/20 µm, ε = 400, Rλ 72.4): total +14.5 % = about +10 % from relative velocity and +4 % from RDF; 20/30: +31.4 %, about half and half. Same-size pairs (gravity kernel zero): RDF at contact g12 and ⟨|w_r|⟩ (cm/s), Rλ = 72.4:

| pair | g12 ε=100 | g12 ε=400 | ⟨|wr|⟩ ε=100 | ⟨|wr|⟩ ε=400 | K (cm³/s) ε=400 |
|---|---|---|---|---|---|
| 20/20 | 1.81 ± 0.19 | 5.09 ± 0.33 | 0.0295 | 0.0487 | 2.56e-5 |
| 30/30 | 3.23 ± 0.49 | 16.8 ± 0.6 | 0.0323 | 0.0882 | 3.37e-4 |
| 40/40 | 7.91 ± 0.55 | 15.7 ± 0.6 | 0.0435 | 0.1427 | 9.07e-4 |
| 50/50 | 10.8 ± 0.8 | 14.5 ± 0.7 | 0.0444 | 0.1537 | 1.39e-3 |
| 60/60 | 9.57 ± 0.80 | 13.7 ± 0.7 | 0.0430 | 0.1304 | 1.64e-3 |

CAUTION: same-size values depend strongly on Rλ in these small DNS (30/30, ε = 400: g12 = 8.2, 13.3, 16.8 for Rλ = 23, 43, 72), and the authors flag larger droplets at low resolution (40/50, 50/60 ratios fall with Rλ). Ireland et al. 2016 argue RDF and kernels are nearly Rλ-independent for low and moderate St at Rλ ≥ 90 and that earlier DNS with gravity "may have errors due to periodic boundary conditions" (App. A: a settling particle meets the same large eddy repeatedly when the fall time through the box < large-eddy turnover time; criterion Sv ≳ (L/ℓ)(u0/uη); they went to L/ℓ ≲ 40).

Other DNS with gravity:
- Franklin, Vaillancourt, Yau & Bartello 2005 (JAS 62, 2451) [ABS]: ε ≈ 100 cm²/s³: turbulent kernel 1.06× gravitational; ε = 1500: 2.08×; radial relative velocities 1.008–1.488× gravitational; clustering adds 8–42 %.
- Franklin et al. 2007 (JAS 64, 938) [ABS]: ε 95–1535 cm²/s³; kernel up to ~10× gravitational (large radius ratio), relative velocities up to 3×, RDF up to 4.5.
- Woittiez, Jonker & Portela 2009 (JAS 66, 1926) [ABS]: ε = 4.25×10⁻² m²/s³ (= 425 cm²/s³), 10–90 µm; gravity and turbulence "not merely additive"; gravity produces clustering of large droplets via larger scales; monodisperse and nearly-monodisperse bidisperse very different. Chen, Bartello, Yau & Vaillancourt 2016 (JAS 73, 621) [ABS]: statistics independent of box size for ≤ 25 µm if the Kolmogorov scale is resolved; new parameterization with 14 % relative uncertainty.
- Ireland, Bragg & Collins 2016 (arXiv 1507.07022) [FULL §1–2, 3.1, 4.3 conclusions, App. A start]: Rλ 90–597, Fr = 0.052 (= ε 100 cm²/s³), 0 ≤ St ≤ 3 (up to 56 in a smaller box). Gravity reduces preferential sampling (strain variance sampled approaches 1/(15τη²) for St ≳ 1), shortens Lagrangian strain/rotation times, reduces relative velocities at high St (less path-history), lowers RDF at low St and raises it at high St, and "reduces the collision kernels for St ≳ 0.1" relative to no gravity; kernels independent of Rλ at low–moderate St. Tension with BHR (Fr = 0.3, St = 0.4: increase > 2×): different Fr; both are DNS; unresolved here.
- Wang et al. 2005 (JAS 62, 2433) [ABS]: with hydrodynamic interaction, efficiency between 20 and 25 µm radii is raised by 59 % (ε = 400) and 10 % (ε = 100).

## 4. Calibration to the acceleration variance a0 and to ε/(15ν): summary

- Gradient variance: ⟨(∂u1/∂x1)²⟩ = ε/(15ν) = 1/(15τK²) and ⟨tr AAᵀ⟩ = ε/ν = 1/τK² in isotropic incompressible turbulence (Pumir & Wilkinson 2016 [FULL of §4.1], Ayala 2008, Ireland 2016). The GM field satisfies ⟨trAAᵀ⟩ = (d+2)u0²/η² by construction (GM2016); isotropy then gives 1/15 automatically. [scout] ⟨(∂1u1)²⟩ = u0²/(3η²) in 3D.
- a0: calibrated only in the Pinsky–Khain sample model (a0 = 5.5 from La Porta et al.), and measured by Voth et al. (5–6 for Rλ ≥ 500; ≈ 1 Gaussian). Ayala Table 4 lists the DNS "fluid acceleration variance" ⟨(Du/Dt)²⟩: ε = 100, Rλ = 23.4/43.0/72.4: 2281 / 3752 / 5010 cm²/s⁴. [scout] ⟨a²⟩ν^½/ε^{3/2} = 0.94 / 1.55 / 2.07 (ν = 0.17 cm²/s); whether their quantity is per component or summed is **not stated** in the text I read (if summed, divide by 3). The trend a0 rising with Rλ is the one Voth et al. describe.
- No random-FIELD model (GM, KS) found that is calibrated to a0. The GM field with OU time dependence cannot be (infinite Eulerian acceleration).
- Tests of calibrated models with gravity against DNS: Pinsky–Khain only against DNS efficiencies/kernels (§2 M3, "reasonable", "within 10 %", no systematic table); GM model: none (§M1).

## 5. Comparison table

| Model | Field / statistics | Parameters and calibration | Gravity treated | Agreement with DNS (with gravity) | Known failures |
|---|---|---|---|---|---|
| GM smooth Gaussian (M1) | 3D (theory 2D) incompressible Gaussian, OU time, single scale | u0, η, τ ↔ ε, ν via τK = η/(u0√(d+2)); Ku free (2–10); St, F, G | yes (GVM2014 theory 2D; simulation any) | F = 0: clustering within ~30 % at peak, 2–4× low at κ ≈ 0.1 (Fig. 11); WITH gravity: no quantitative comparison found | no intermittency, no inertial range, no sweeping, preferential sampling ~3× too weak, rotation time 1.6× too short, OU: no acceleration, theory for relative velocity not with gravity |
| BHR 2014 | Navier–Stokes DNS + white-noise reductions | none (theory asymptotic) | yes | is the DNS | only 3 Reλ; scaling laws, few numbers |
| Pinsky–Khain gen. 1 (1995–99) | random Fourier-type field, Batchelor structure function | ε; harmonic details not found | yes (drop tracks) | none systematic | authors: enhancement overestimated (stationarity); claims ×2–5 vs DNS ≤ ×1.5 |
| Pinsky–Khain gen. 2 (2004–08) | iid samples of S and A in Kolmogorov volumes | ε, Rλ, skewness/flatness, a0 = 5.5 | yes (Vt in slip eq.) | "reasonable" vs Wang 2005 efficiencies; within 10 % of Ayala for 15/10 swept volume | valid ≲ 20 µm; no clustering (empirical G); frozen S, A; tables only 1–21 µm; not a time-dependent field |
| KS (Fung) | multi-scale Fourier modes, E ~ k^(−5/3), ω_n = λ√(k³E) | N modes, kmax/kmin, λ ≈ 0.5 | yes in Farhan et al. (steady) | none with gravity; without gravity R_KS < R_DNS by > 10× at St ≳ 0.3 | no sweeping; wrong decorrelation seen by particles; λ cannot fix it |
| Gaussian-statistics analytic (Wang 98, Dodin–Elperin 02) | Gaussian relative velocity | ε | yes | used as cross-checks (10–15 %) | no clustering, no caustics |
| Kraichnan / Falkovich–Pumir | delta-correlated; or NS-DNS gradient equation | Re, St, Fr | yes (Fr) | n/a (DNS based) | not a stand-alone model |

## 6. Recommended minimal model for the lecture note

**Choice:** the single-scale smooth Gaussian incompressible field of Gustavsson & Mehlig (M1), 3D, with Stokes drag, gravity and (optionally) the Schiller–Naumann factor f(Rep) for radii ≳ 30 µm. Reason: it is the only model here that (i) has a published mapping to ε and ν (τK, κ), (ii) was checked against Navier–Stokes DNS for clustering with no fit parameter, (iii) has an analytic theory with gravity that explains the DNS trends, (iv) is free of the KS sweeping defect, (v) is small enough to explain in a lecture. It is NOT validated for collisions with gravity; say so.

**Equations** (GM2016 Eqs. 1, 3c, 4–7; d = 3, β = 0):
- ẋ = v, v̇ = g + (u(x,t) − v)/τp, τp = 2ρw a²/(9ρa ν).
- u = (1/√6) ∇×A, A_i independent Gaussian fields with ⟨A_i(x1,t1)A_j(x2,t2)⟩ = δij u0²η² exp(−|x1−x2|²/(2η²) − |t1−t2|/τ). Fourier form: A = u0 η (2π)^(3/4) (η/L)^(3/2) Σ_k a_k(t) e^{ik·x − k²η²/4}, with complex OU amplitudes δa_k = −a_k δt/τ + δw_k, ⟨δw δw*⟩ = 2δt/τ (their Eq. 5 normalization; check it numerically: ⟨|u|²⟩ must equal u0²).
- Strain-correlation check: velocity-gradient rms follows from u0/η.

**Parameters from ε and ν** (all [scout] algebra from GM2016 definitions; the first three lines are the source's):
1. τK = (ν/ε)^½, ηK = (ν³/ε)^¼, uK = (νε)^¼.
2. Gradient variance: ⟨trAAᵀ⟩ = ε/ν = (d+2)u0²/η² ⇒ u0 = η/(√5 τK).
3. Length: set η = ηK (the convention of GVM2014/GM2016: "smallest characteristic length"). Then u0 = uK/√5. Sensitivity to η/ηK is not documented: test η = 1–3 ηK.
4. Time: Ku = u0τ/η ⇒ τ = √5 Ku τK. Use Ku = 2 as default and check 2, 5, 10 (range used in GM2016 Fig. 11). F = 0 results are about Ku-independent there; with fast settling the dependence enters through G.
5. Particle numbers: St_K = τp/τK = κ; St_GM = 1/(γτ) = St_K/(√5 Ku); F = gτ/u0 = 5Ku/Fr; Sv = vs/uK; G = vs τ/η = √5 Ku Sv. For ε = 100–400 cm²/s³: Fr = 0.052–0.147 and, for 20–60 µm (Sv ≈ 1.7–22), G ≈ 8–100 at Ku = 2: deep in the large-G regime where the transverse dynamics is white-noise (GVM2014, BHR).
6. Box: periodic, L ≫ η, and the fall time through the box must exceed the time over which the field decorrelates: for the OU field L/vs ≫ τ = √5 Ku τK. For ε = 100, Ku = 2, vs(60 µm) ≈ 0.44 m/s: L ≫ 0.076 m ≈ 100 ηK. [scout, after Woittiez et al. 2009 / Ireland et al. 2016 App. A criterion and the OU decorrelation e^{−L/(vs τ)}]. If that is too expensive, use a larger L with a coarse mode set (Gaussian spectrum needs only |k|η ≲ 4–5) or give each particle a periodic image shift and re-randomize.

**Three validation tests with expected numbers**
1. Field and tracer check (no inertia, no gravity). Targets: ⟨trAAᵀ⟩τK² = 1; ⟨(∂1u1)²⟩τK² = 1/15 = 0.0667; ⟨u·∇u⟩ not needed. Tracer geometric collision rate: R τK/(n(2a)³) → √(8π/15) = 1.294 as St → 0 (Saffman–Turner; Voßkuhle et al. Fig. 1, Pumir & Wilkinson Eq. 25; DNS and KS both reproduce it). Gravity-only check: bidisperse ⟨|wr|⟩ = ½|vp2 − vp1|, g12 = 1, K = π(a1+a2)²|vp2 − vp1| (Ayala Eq. 12, verified by them to within statistical error).
2. Clustering without gravity vs DNS (GM2016 Fig. 11, read off plot): vs κ = τp/τK, Lyapunov dimension deficit Δ_L ∝ κ² for κ ≲ 0.1; peak Δ_L ≈ 0.4 at κ ≈ 0.6; −⟨trZ⟩τK ≈ 0.1 at the peak (DNS ≈ 0.13–0.15); at κ ≈ 0.1 DNS Δ_L ≈ 0.1 and the model 0.025–0.06. Accept model within 30 % at the peak, and report the low-κ deficit rather than tuning it away. Preferential-sampling probability will come out ≈ 3× smaller than DNS (Fig. 12).
3. With gravity, collisions vs DNS (Ayala 2008, Rλ = 72.4, Stokes drag, Tables 6–8): reproduce K_turb/K_grav = 1.06 / 1.08 / 1.12 / 1.14 (10/20, 20/30, 30/40, 40/50 at ε = 100) and 1.145 / 1.31 / 1.43 / 1.31 (same pairs at ε = 400); same-size g12 at contact 3.2 (30/30, ε = 100) and 16.8 (30/30, ε = 400), ⟨|wr|⟩ = 0.0882 cm/s (30/30, ε = 400). These are Rλ = 72 numbers; expect the model, having no Rλ, to fall inside the range spanned by Rλ = 43–72 (30/30, ε = 400: g12 13.3–16.8) at best. Qualitative targets (GVM2014, Ireland 2016, BHR): gravity lowers preferential sampling and relative velocities relative to F = 0, lowers RDF at St ≲ 1 and raises it at large St, aligns pairs with ĝ. Measure K with ghost (overlapping) particles and the same kinematic formula K = 2πR²⟨|wr|⟩g12 (angle-averaged, since gravity breaks isotropy).
Optional fourth, if a0 is wanted: none possible for the OU field (infinite Eulerian acceleration); compare the particle acceleration variance instead (Ireland 2016 report it with gravity; I did not extract numbers: not found).

**Honest price (what the model cannot claim)**
- No published test of this model with gravity against Navier–Stokes DNS exists (searched through 2026). Test 3 is the first. The only published quantitative DNS comparison of the model is without gravity (clustering, Fig. 11).
- Single scale: no inertial range. Fine for St ≲ 0.5 and fast settling; for 50–60 µm at ε = 400 (St 1.6–2.3) relative velocity from scales larger than ηK is missing (Zhou et al. 1998: kernel involves both small and large scales; Ayala: 30–60 µm droplets feel resolved large scales at low resolution).
- Gaussian: no intermittency. Pinsky–Khain use a0 = 5.5 (vs ≈ 1 Gaussian) and find mean swept-volume change ≤ 60 %, so the effect on mean collisions is moderate but the PDF tail changes.
- Preferential sampling about 3× too weak and rotation correlation 1.6× too short at F = 0; time-reversal symmetric; no vortex tubes.
- OU time dependence gives no Eulerian fluid acceleration; with gravity the acceleration seen by the droplet comes from falling through the frozen-like field, which is the right mechanism only if the sweeping-free assumption holds (GVM2014 caveat).
- No sweeping and no large scale: the periodic box can fake correlations when L/vs < τ (see parameter 6).
- Geometric collisions only: no hydrodynamic interaction (efficiency enhancements of Pinsky–Khain 4.8× at ε = 1000 for 10/20 µm, Wang et al. +59 % / +10 % for 20/25 µm are outside the model) and no coalescence efficiency; linear drag overestimates settling above ~30 µm unless f(Rep) is added (f = 1.13 at 40 µm, 1.28 at 60 µm).
- Theory support is 2D (GVM2014); 3D with gravity is expected, not shown.
- η/ηK and Ku are conventions, not measurements; report sensitivity.
- Rλ-independence of kernels is supported by DNS up to Rλ ≈ 600 for low–moderate St (Ireland 2016) but is an assumption for clouds (Rλ ~ 10⁴).

## 7. Not found (explicit)

Full text of any Pinsky–Khain JAS paper; the harmonic construction and time dependence of the 1995 model; Pinsky et al. 2004 numerical constants; tables for radii > 21 µm; Ducasse–Pumir 2009 abstract; Ghosh et al. 2005 model details; Fung 1992 parameter values beyond Voßkuhle's summary; any DNS comparison of a GM-type or KS model WITH gravity in numbers; any KS verdict with settling vs DNS; whether Ayala's ⟨(Du/Dt)²⟩ is per component; a clean statement of which DNS quantity (RDF or kernel) BHR's "factor two" refers to.

## 8. Source list with reading status

Full text: Gustavsson & Mehlig 2016 (1412.4374) [§6 skimmed]; Gustavsson, Vajedi & Mehlig 2014 (1401.0513); Bec, Homann & Ray 2014 (1401.1306); Voßkuhle et al. (1307.6853, 1402.5915); Falkovich & Pumir 2007 (nlin/0605040); Wilkinson, Mehlig & Bezuglyy 2006 (cond-mat/0604166); Ayala et al. 2008 (NJP 10, 075015, to §5.2); Farhan et al. (1706.08512); Voth et al. 2002 (physics/0110027, §4.2 and tables); Pumir & Wilkinson 2016 (1508.01538, §4–6 passages). Partial: Gustavsson & Mehlig 2014 JoT (1307.0462); Ireland, Bragg & Collins 2016 (1507.07022); Rosa et al. 2013 (downloaded, not read). Conference preprints read in full: AMS 41329, 112538, 112206, 112192; EGU05 abstract. Abstract only: Pinsky–Khain JAS/QJRMS/GAFD/Atmos. Res./Physica D papers; Fung 1992; Thomson & Devenish 2005; Ghosh et al. 2005; Dávila & Hunt 2001; Dodin & Elperin 2002; Wang et al. 1998, 2005; Zhou et al. 1998; Franklin et al. 2005, 2007; Woittiez et al. 2009; Chen et al. 2016.

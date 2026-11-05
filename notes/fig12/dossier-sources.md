# Fig. 12 dossier: sources for foam / wall / contact-line damping of stout sloshing

Status: complete first pass. Read-status for each source is stated in its section. Tool budget limited; items marked NOT FOUND or ABSTRACT ONLY are real gaps.

---

## 1. Sauret, Boulogne, Cappello, Dressaire, Stone (2015), "Damping of liquid sloshing by foams"

- Reference: Phys. Fluids 27, 022103 (2015). arXiv:1411.6542v2 (1 Feb 2015). Link: https://arxiv.org/abs/1411.6542 ; PDF https://arxiv.org/pdf/1411.6542
- READ: yes, full arXiv v2 PDF opened and read (pdftotext). The journal page itself was not opened. Page numbers below are arXiv v2 pages.

### Setup (Sec. II A, p. 2-3; Table I p. 3)
- Rectangular Hele-Shaw-type cell: length L = 70 mm, height 92 mm, width w in [3, 19] mm. Liquid depth H = 4 cm. Foaming solution: 90 % water, 5 % glycerol, 5 % Dawn dish-washing liquid; nu = 1.4e-6 m^2/s, gamma = 25 mN/m, rho = 1020 kg/m^3 (Table I, 20 C). Low surface modulus (elastic interfaces, not rigid films).
- Bubbles: monodisperse, D = 3 mm (needle 1.3 mm, Q = 20 uL/min). Foam height = xi*D, with xi = number of layers. Foam made one layer at a time, runs shorter than a few minutes (no aging).
- Excitation: harmonic X0 cos(2 pi f t) with X0 = 1 mm (Sec. IV A), or impulse (main method for the damping rate). Resonance f1 ~ 3.1-3.3 Hz (p. 7: peak near 3.1 Hz with foam, 3.3 Hz predicted from Eq. 1; Fig. 4 uses 3.125 Hz). Note: this is the same frequency as our glass (3.3 Hz), but it is a rectangular slot, not a round glass.

### Damping coefficient, definition and liquid-only law
- Eq. (2), p. 6: 1/tau_l = <|dE_l/dt|> / (2E). Fit: eta(x,t) = eta0(x) exp(-t/tau_l) sin(omega t). So 1/tau is the AMPLITUDE decay rate (s^-1), not an energy rate.
- Eq. (7), p. 6 (scaling only, "~", no prefactor): 1/tau_l ~ 2 pi f sqrt(nu) (1/L + 1/w)... as printed: 1/tau_l ~ sqrt(2 pi f nu) (1/L + 1/w)  [the pdftotext shows "2 pi f sqrt(nu)"; Fig. 3b axis is sqrt(2 pi f nu)(1/L+1/w), which is the dimensionally correct form]. Mechanism: Stokes boundary layers delta = sqrt(nu/omega) on the two walls; bulk viscous loss smaller by pi*delta*w/L ~ 1e-2 (Eqs. 3-6).
- Liquid-only value in the foam experiment: 1/tau_l ~ 2 s^-1 (w = 3 mm, H = 4 cm, L = 7 cm), p. 7.

### Foam contribution: measured (Sec. IV A, p. 7, Eq. 8, Fig. 5b)
- Total: 1/tau = 1/tau_l + 1/tau_f.
- Eq. (8): 1/tau = 1/tau_l + (1/tau_f^inf) [1 - exp(-xi/xi_c)].
- Fit values (w = 3 mm, 2D foam): 1/tau_f^inf = 9 +/- 3 s^-1; plateau 1/tau_l + 1/tau_f^inf = 11 +/- 3 s^-1; xi_c = 5 +/- 2 layers.
- Amplitude without foam ~ 1 cm; with xi = 5 layers ~ 1 mm (factor 10), at resonance forcing, X0 = 1 mm.
- Frequency: f1 unchanged by foam within error (inset Fig. 5a). Foam elasticity neglected at first order.
- Saturation for xi > ~5 layers (p. 8): foam-air interface nearly steady.
- Bubble velocity decays with height z above the liquid: <|v_b|> ~ exp(-z/(xi_c D)), xi_c D = 16.8 +/- 1.8 mm (Fig. 6a, p. 8-10). They note this is the same order as 1/k1 = L/pi ~ 22 mm (p. 10). So the saturation depth is set by the wave decay length 1/k, NOT by a number of bubble layers.

### Proposed mechanism (Sec. IV B, p. 9-10)
- Friction of Plateau borders sliding on the two glass walls: f_b = K gamma_f Ca^(2/3), Ca = mu_f v_b / gamma_f (Bretherton/Cantat-type law, refs 35, 37 = Raufaste-Foulon-Dollet 2009; Cantat 2013 Phys. Fluids 25, 031303). Valid for Ca < 1e-2; their Ca ~ 3e-3.
- Dissipated power: <|dE_f/dt|> = K' sum v_b^(5/3), K' = K gamma_f^(1/3) mu_f^(2/3) (Eq. 10).
- With v_b = v0max exp(-z/(xi_c D)) cos(omega t) (Eq. 11-12), injected energy E = rho w L^2 (v0max)^2/(4 pi) (Eq. 13), result (Eq. 14, p. 10):
  1/tau_f = (12 pi xi_c K' <|cos(omega t)|^(5/3)> / (5 rho w L (v0max)^(1/3))) [1 - exp(-5 xi/(3 xi_c))]
  Symbols: xi_c = decay length in layers, K' as above, rho liquid density, w cell width, L cell length, v0max velocity amplitude of bubbles in the first layer above the liquid, xi = layers.
- Fitted prefactor (Eq. 15): (12 pi xi_c K' <|cos|^(5/3)>)/(5 rho L (v0max)^(1/3)) = 2.76 cm/s, giving K ~ 1.9 m/s at v0max ~ 0.1 m/s. Cantat law (Eq. 16): K = 5.13 (Rp/sqrt(A))^(-0.48) gives K = 9.1 m/s for Rp/sqrt(A) ~ 0.3 (A = bubble area, Rp = Plateau-border radius). Factor ~5 mismatch they call "compatible".
- Key scaling: 1/tau_f ~ 1/w (only Plateau borders touching the walls dissipate; bulk bubbles just advected). Confined 3D foams (w = 3, 6, 15.9 mm = 1, 2, 5 bubble diameters) collapse on one curve (Fig. 6b): w/tau_f^inf = 1.6 +/- 0.3 cm/s (exponential fit), model fit ~ 3.1 cm/s. (Check: 9 s^-1 x 0.3 cm = 2.7 cm/s, consistent.)
- Nonlinear: the 5/3 power makes 1/tau_f depend on amplitude (v0max^(-1/3)): weakly decreasing with amplitude in this model.

### Estimate for a 15-20 mm nitrogen head (our own arithmetic, flagged as extrapolation)
- Their plateau reached at foam thickness ~ 1.5-3 x (xi_c D = 16.8 mm), i.e. about 20-40 mm of foam in a 22 mm 1/k situation; a 15-20 mm head is ~ one decay length, so we are near but below plateau: factor [1 - exp(-5 xi/(3 xi_c))] with xi D = 17 mm, xi_c D = 16.8 mm gives 1 - exp(-1.68) = 0.81.
- Crude geometric map from slot to round glass: replace 1/w by (wall length)/(area) ~ 2/R for a cylinder vs 2/w for the slot, i.e. w_eff ~ R = 39 mm. Then 1/tau_f^inf ~ (1.6 to 3.1 cm/s)/3.9 cm = 0.4 - 0.8 s^-1; times 0.8 => about 0.3 - 0.65 s^-1 (amplitude decay rate), i.e. a decay time of roughly 1.5-3 s from foam alone. Compare liquid-only wall Stokes damping in a 39 mm radius glass (section 2): about 0.1-0.2 s^-1 for beer viscosity. So foam would dominate if the Plateau-border friction law carried over.
- Large caveats (they are the reason this is only an order of magnitude): (i) bubble size 3 mm vs ~tens of um in Guinness: K depends on Rp/sqrt(A) and Ca = mu_f v_b/gamma_f changes; (ii) surfactant/interface mobility of beer foam (proteins, hop acids: likely higher surface modulus than Dawn) is not the same; (iii) their foam is wet, glycerol-stabilised, 1-5 bubble rows across the gap; ours is a 3D foam with thousands of bubbles across the glass, so bulk foam rheology (viscoelastic, yield stress) may matter more than the wall; the authors say bulk was neglected and that wide containers need further work (p. 12); (iv) pint-glass walls are tilted and the sloshing is a (1,1) azimuthal mode not a 2D slot mode.

### Does NOT establish
- Nothing for round glasses, 3D foams wider than ~6 bubbles, bubbles smaller than 3 mm, beer/protein-stabilised foam, or amplitude dependence measured directly. The Bretherton/Cantat law is assumed, not tested independently. No measurement of foam rheology.

---

## 2. Viscous damping of sloshing in an upright circular cylinder (Case & Parkinson 1957; Miles 1967; Henderson & Miles 1994; Martel, Nicolas & Vega 1998)

READ STATUS (honest): the primary papers are paywalled or the host was down. I read in full: Howell et al. 2000 (Phys. Fluids 12, 322; open PDF https://schatzlab.gatech.edu/Library/Howell2000.pdf), Nicolas & Vega 2000 note (https://oa.upm.es/6011/1/Vega_23.pdf), Habenberger 2015 (open, https://pmc.ncbi.nlm.nih.gov/articles/PMC4573968/, derivation of Stokes-layer damping), Irvine tutorial quoting NASA SP-8009 (http://www.vibrationdata.com/tutorials/slosh_damping.pdf), and the Mayer & Krechetnikov PDF (section 4). ABSTRACTS ONLY (full text not opened): Case & Parkinson, J. Fluid Mech. 2, 172 (1957) https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/abs/damping-of-surface-waves-in-an-incompressible-liquid/9A3A92909F9831AD213A6F544F049F67 ; Miles, Proc. R. Soc. A 297, 459 (1967) https://doi.org/10.1098/rspa.1967.0081 ; Henderson & Miles, J. Fluid Mech. 275, 285 (1994) https://doi.org/10.1017/s0022112094002363 ; Martel, Nicolas & Vega, J. Fluid Mech. 360, 213 (1998). Miles's 1958 report (DTIC AD0605958) could not be fetched (DTIC down). I therefore have NO verbatim equation from Case & Parkinson or Miles 1967; the formulas below are (i) the standard coefficient as quoted in a secondary source citing NASA SP-8009, and (ii) my own Stokes-layer energy calculation, which I could not reconcile exactly with (i). Treat the prefactor as uncertain by a factor sqrt(2).

### What the abstracts establish
- Case & Parkinson 1957 (abstract): wall boundary-layer viscous dissipation is the primary damping; logarithmic decrement measured vs h/R in water-filled cylinders; theory and experiment "in good agreement" (but see Miles: only for polished/clean cases; Ref. in Robertson thesis says 2-3x higher otherwise).
- Miles 1967 (abstract, Proc. R. Soc. A 297, 459): damping has three parts: (a) viscous loss at the basin boundary, (b) viscous loss at the surface because of contamination (film treated as linear viscoelastic surface, insoluble or soluble), (c) capillary hysteresis at the meniscus (constant advance/recession forces). Observed decay rates of Case & Parkinson and Keulegan "typically exceeded the theoretical value based on wall damping alone by factors of between two and three"; both films and hysteresis can account for it.
- Henderson & Miles 1994 (abstract): brimful, sharp-edged cylinder R = 2.77 cm, depth 3.80 cm, fixed contact line, Stokes layers, clean or fully contaminated (inextensible) surface. Frequencies within 0.5 %. Damping ratio of the dominant mode: 20 % off for clean surface, much more for higher modes and for all contaminated cases.
- Martel, Nicolas & Vega 1998 / Howell et al. 2000: adding viscous dissipation in the BULK (order C, where C = nu / sqrt(g R^3)... as printed in Howell Fig. 1: C = nu / sqrt(g (d/Gamma)^3), d depth, Gamma aspect ratio d/R) brings theory within 4 % for 5 of 6 modes of Henderson & Miles; Howell et al. measured 74 conditions: theory vs experiment better than 7 % for silicone oils with C < 1e-3 (Tables III-IV), water mode (0,1) measured 12 % above theory (pinned contact line, clean-ish surface). Form (Howell Eq. 1, p. 322-323): delta_t = a1 C^(1/2) + a2 C, omega_t = a0 - a1 C^(1/2). a1 C^(1/2) = Stokes layers (wall + bottom), a2 C = bulk viscosity + higher-order layer correction; free-surface-film term is O(C^(3/2)) and neglected for a CLEAN surface. Units: nondimensional with R and sqrt(R/g).
- IMPORTANT for our glass: those results are for a BRIMFUL cylinder with a PINNED contact line (sharp rim). A pint glass is not brimful and the stout wets the glass (free/hysteretic contact line), so they do not apply directly. Nicolas & Vega 2000 (p. 1-2, Eq. 2.10 and text): three damping sources: (a) Stokes layers + bulk, (b) contact-line dynamics ("not-well-understood ... phenomenological"), (c) surface contamination; a finite Marangoni elasticity explains much of the unexplained extra damping in Henderson & Miles (discrepancies within 15 % instead of 20-80 % for inextensible film).

### Formula (a): wall (+ bottom) Stokes layers, clean surface, free contact line, deep liquid
Definition used by everyone: amplitude ~ exp(-gamma t), energy ~ exp(-2 gamma t); gamma = <dE/dt dissipated> / (2E). (Habenberger Eq. 17: gamma = <Edot>/(2E_mech); damping ratio kappa = gamma/omega.) Log decrement per cycle delta = gamma * 2 pi / omega (Mayer & Krechetnikov: A_{n+1} = A_n e^{-delta}).
Symbols: R radius, h depth, nu kinematic viscosity of the liquid, g, xi_mn the m-th... root of J_m'(xi)=0 (xi_11 = 1.8412), k = xi_11/R, omega^2 = g k tanh(k h) (surface tension neglected; Mayer & Krechetnikov Eq. 1 adds (1 + sigma xi^2/(rho g R^2))).
1. Standard engineering coefficient (secondary source: T. Irvine, Fluid Slosh Damping, p. 2, Eq. 2-3, quoting NASA SP-8009 (1968), "for h/a > 1"): delta = 4.98 nu^(1/2) a^(-3/4) g^(-1/4), damping ratio zeta = delta/(2 pi) ~ 0.79 nu^(1/2) a^(-3/4) g^(-1/4); a = radius. Valid for first antisymmetric mode, h/a > 1, clean smooth wall, small amplitude. I verified Irvine's worked number (a = 12 in, water: delta = 0.006861).
2. My own calculation (done here, deep liquid, potential phi ~ J_1(k r) cos(theta) e^(k z), Stokes-layer dissipation per area = (1/2) rho sqrt(nu omega/2) |U|^2 / 2... i.e. rho U^2 sqrt(nu omega / 2)/2 with U the amplitude of the tangential slip velocity; checked against Habenberger Eq. 18 form): wall only: gamma_wall = (1 + xi^2)/(xi^2 - 1) * (1/2) sqrt(nu omega / 2) / R * ... evaluated: gamma_wall = 0.6495 sqrt(nu omega) / R (xi = 1.8412), i.e. delta_wall = 3.50 nu^(1/2) R^(-3/4) g^(-1/4). This is 1/1.42 of the 4.98 coefficient (4.98/3.50 = 1.42, suspiciously sqrt(2)). I could not find the reason with the primary sources unavailable; either the textbook number includes something I omitted or my prefactor is low. Mayer & Krechetnikov quote delta ~ 0.02 for R = 3.5 cm, H = 10 cm "for the conditions in our experiments" from Abramson; for hot coffee (nu ~ 0.45e-6 m^2/s, my value, not stated by them) coefficient 4.98 gives 0.022 and 3.50 gives 0.016, so both are "~0.02".
3. Bottom: finite-depth factor from the Mikishev-Rabinovich/Abramson form (my memory, NOT verified in a source I opened): delta = delta_deep [1 + 0.318/sinh(1.84 h/R) (1 + (1 - h/R)/cosh(1.84 h/R))]. Numerically 1.4 at h/R = 0.5, 1.10 at 1, 1.015 at 2, 1.0008 at 3.6 (our glass h/R ~ 3.6 => bottom Stokes layer negligible, which is also Miles's statement that depth may be taken infinite when it exceeds the diameter, DTIC abstract of AD0605958, abstract only).
4. Bulk viscous damping (Lamb): gamma_bulk = 2 nu k^2 for deep water; for R = 39 mm, k = 47.2 m^-1, gamma_bulk = 0.0045 s^-1 at nu = 1e-6 (arithmetic, from standard Lamb result; not found in an opened source here but Howell/Martel confirm the bulk term is order C and matters only for small/viscous cases). Ratio to wall term ~ 4-6 %.

### Formula (b): inextensible (fully contaminated) surface film
- Miles 1967 and Henderson & Miles 1994 add a Stokes layer under the surface because the film pins tangential surface velocity. No explicit equation obtained (papers paywalled); in the abstract only. Nicolas & Vega (p. 2, Eq. 2.10 and following text): "Re(-Omega_1^cont) comes from viscous dissipation enhanced by contamination in both the boundary layer attached to the free surface and the free surface itself"; and as Marangoni elasticity gamma -> infinity the formula reduces to the Henderson-Miles inextensible-film result.
- My own energy calculation for the same (1,1) deep mode with the surface tangential velocity forced to zero: gamma_film = 0.6495 sqrt(nu omega)/R * 1.003 (nearly equal to the wall term, by coincidence of the integrals), so total gamma(wall+film) ~ 2 x gamma_wall. That matches Miles's statement that observed damping exceeded wall damping by a factor 2-3, and it reproduces Miles's (1958) 10-ft-tank figure only if the film is included (half-amplitude time 7 min quoted in the abstract of AD0605958; my wall-only gives 14.6 min, my wall+film 7.3 min; with 4.98 it is 10 min).
- Contaminated-surface measurements: Howell et al. 2000 p. 4: for HPLC water the (0,1) mode damping rose with surface aging (12 % above theory vs 26 % in Henderson & Miles); silicone oil (low surface tension, uncontaminable) agrees with clean theory to 5.4 %.

### Numbers for our glass (arithmetic, R = 39 mm, deep, omega = sqrt(1.8412 g/R) = 21.5 rad/s = 3.43 Hz for the straight cylinder; the 3.3 Hz in the brief is the tapered glass)
| nu (m^2/s) | 4.98-coefficient: delta, gamma (s^-1), e-fold time | own wall-only gamma | own wall+film gamma |
|---|---|---|---|
| 1.0e-6 | 0.032, 0.110, 9.1 s | 0.077 | 0.155 |
| 1.5e-6 | 0.039, 0.135, 7.4 s | 0.095 | 0.190 |
| 2.0e-6 | 0.045, 0.155, 6.4 s | 0.109 | 0.219 |
| 2.5e-6 | 0.051, 0.174, 5.8 s | 0.122 | 0.245 |
| 3.0e-6 | 0.056, 0.190, 5.3 s | 0.134 | 0.268 |
(Beer viscosity values: section 5.) Take gamma ~ 0.1-0.2 s^-1 as the clean-glass Stokes-layer range, and up to ~0.3-0.5 s^-1 if Miles's observed factor 2-3 (film + contact line) applies.

### Does NOT establish
- No source here gives the free-surface-film or contact-line term for a non-brimful, wetted, TAPERED glass; no measurement in a pint glass. No verbatim equations from Case & Parkinson / Miles 1967 / Henderson & Miles (paywalled). The sqrt(2) coefficient mismatch is unresolved.

---

## 3. Keulegan 1959 and later contact-line damping

READ STATUS: Keulegan, J. Fluid Mech. 6, 33-50 (1959), https://doi.org/10.1017/s0022112059000489 : ABSTRACT ONLY (full text not opened; cannot give his empirical formula). Hocking 1987, J. Fluid Mech. 179, 253, https://doi.org/10.1017/s0022112087001514 : abstract only. Miles 1990, J. Fluid Mech. 210, 331 (https://doi.org/10.1017/s0022112090003123): abstract only. Cocciaro, Faetti, Nobili 1991 (J. Fluid Mech. 231, 325) and Cocciaro, Faetti, Festa 1993 (J. Fluid Mech. 246, 43): abstracts only. Read in full: Jiang, Perlin, Schultz, Phys. Fluids 16, 748 (2004), https://doi.org/10.1063/1.1644151 (via excerpts returned by the search tool, not the full PDF) which summarises all of them with equations.

### Keulegan 1959 (abstract + Jiang et al. summary)
- Abstract: viscous wall-layer theory for the modulus of decay of finite-height standing waves; six rectangular basins, glass and lucite. "With liquids wetting the walls, the losses due to viscosity are slightly increased from causes presumably related to surface tension." With a non-wetting combination (distilled water/lucite) "losses from surface activity ... outweigh many times the losses due to viscosity in the basins of smaller sizes". For moderately large basins agreement with viscous theory is satisfactory.
- Jiang et al. (Sec. I-II): Keulegan split damping into a viscous part and a surface-tension part using dimensional analysis; damping correlates with surface tension; large increase glass -> lucite; and the damping rises as amplitude falls (the "anomaly" when counting later cycles n), attributed to meniscus deformation: first report that wetting / contact-line damping is amplitude dependent. I could not extract his empirical numeric formula or magnitudes; do not quote one.
- So for a glass with a wetting liquid: extra damping "slightly" above viscous (tens of percent), not factors; for non-wetting small basins factors of several.

### Contact-line models (Jiang et al. 2004, with equations)
- Hocking 1987 / Miles 1990-91 condition (Jiang et al. Eq. 1): d(eta)/dt = c d(eta)/dx at the wall, c a contact-line 'slip coefficient' with units of velocity (c -> 0 pinned line, c -> infinity free line); Miles makes the coefficient dimensionless with the capillary length l = (sigma/(rho g))^(1/2) (and the oscillation frequency); the exact scaling was garbled in the excerpt, so use it qualitatively. Damping from this condition (Jiang et al. Eq. 6): gamma_c = Gamma_form * omega_n * c / (2 (1 + c^2)), with Gamma_form a mode-shape form factor; for their 60 cm x 6 cm tank, form factor (4/a + 2/b) l = 0.108. Limits: c -> 0 pinned line, c -> infinity free (perfectly wetted); damping maximal for c ~ 1. The theory is linear (independent of amplitude).
- Jiang et al. measured (60 cm x 6 cm glass tank, water): damping rate rising from 0.05 to a maximum of 0.25 s^-1 (fivefold) for wave amplitude falling from 7 mm to 1.3 mm, ~ amplitude^(-1/3); then falling for amplitude < 1.3 mm (contact line pins). Photo-Flo (surfactant) removed the amplitude dependence.
- Cocciaro, Faetti, Nobili 1991 (abstract): cylindrical basin horizontally oscillated, wetting fluid, low amplitude; the damping of the fundamental mode is nonlinear in amplitude, in qualitative agreement with Miles 1967 capillary-hysteresis theory. Cocciaro, Faetti, Festa 1993 (abstract): Plexiglas cylinder, static contact angle 62 deg; low-amplitude regime: contact line pinned, damping and frequency agree with Graham-Eagle pinned-end theory; higher-amplitude regime: contact line slides, damping strongly nonlinear in amplitude, explained by Hocking/Miles with an effective capillary coefficient measured directly. Numbers (container radius, decay rates) not obtained.
- Hocking 1987 (abstract): "the dissipation associated with the surface forces can exceed that produced by viscosity."
- Miles 1967: hysteresis model with constant force opposing advance and recession => dissipation per cycle proportional to amplitude, so amplitude-independent logarithmic-decrement contribution ~ 1/A... (my reading of the abstract; no equation seen).

### Does NOT establish
- No formula or number for a glass of stout. Contact-line damping is amplitude dependent, wetting dependent, and the beer/foam meniscus is covered by foam, so a clean pinned/free line model may not apply at all.

---

## 4. Mayer & Krechetnikov (2012), "Walking with coffee: Why does it spill?"

- Reference: Phys. Rev. E 85, 046117 (2012). DOI 10.1103/PhysRevE.85.046117. Link: https://journals.aps.org/pre/abstract/10.1103/PhysRevE.85.046117 ; open PDF read in full: https://www.math.ualberta.ca/~rkrechet/files/publications/pre2012.pdf . Not on arXiv.
- Setup (Sec. II, p. 1-2): human subject walks naturally on a straight line, filmed at 100 fps, walking speeds 0.5-2.5 m/s, cup motion tracked in MATLAB; focused (trying not to spill) vs unfocused walking; vertical, back-and-forth, pitching (~2 deg) excitations; lateral excitation ~1.25 Hz, amplitude ~20 mm.
- Cup: "typical" R = 3.5 cm, H = 10 cm (their symbol H is liquid height); range of cups (R, H) = (2.5, 5.7) cm to (6.7, 8.9) cm (espresso to cappuccino) giving natural frequencies 2.6-4.3 Hz; for the typical cup nu_nat = nu_11 ~ 3.65 Hz, omega_11 ~ 23 rad/s, T_nat ~ 0.27 s. Natural frequency law, Eq. (1), p. 2: omega_mn^2 = (g xi_mn / R) tanh(xi_mn H/R) (1 + (sigma/(rho g)) (xi_mn/R)^2), m = 0,1,2..., xi_11 = 1.841, xi_12 = 5.331 (as printed "11 = 1.841, 12 = 5.331, 31 = 8.536" in the extracted text). Surface tension negligible for R = 3.5 cm.
- Walking: cup excitation frequency f_cup = 1-2.5 Hz equals step frequency; max accelerations 0.5-1+ m/s^2 range (example in Fig. 3 caption: speed 80 cm/s, max acceleration 71 cm/s^2); spill after typically 4-5 m (7-10 steps); spill angle alpha for coffee levels 8.1, 12.1, 13.7, 16.5 deg (figure legend).
- DAMPING (Ref. [20], last page, footnote): "damping is not important in the dynamics". Computed, not measured: "logarithmic decrement coefficient delta ... A_{n+1} = A_n e^{-delta} ... delta ~ 0.02" from formulas (3.27a-c) of Abramson NASA SP-106 and Secs. 4.1-4.2 of the 1967 report; hence e-fold in N ~ 1/delta ~ 50 oscillations, t ~ N T ~ 12 s. This is a theoretical estimate for a coffee cup, not a measured decay.
- Does NOT establish: no measured decay time in a beer or wine glass; no foam; no pint glass; the only damping number is a computed log decrement ~0.02 (gamma = delta/T ~ 0.02/0.27 s = 0.074 s^-1).
- Other sources for a measured decay in a drinking glass: none found in this pass (not searched beyond the Mayer paper because of the tool budget).

## 5. Beer / stout properties

Legend: [P] peer-reviewed or measured by the authors; [B] brewer's own page; [S] secondary site, treat as soft.

| Quantity | Value | Source and place | Class |
|---|---|---|---|
| Liquid density, Guinness Draught at 6 C | 1007 kg/m^3 (measured by authors, "verified against extrapolation formula") | Benilov, Cummins, Lee, "Why do bubbles in Guinness sink?", Am. J. Phys. 81, 2013; arXiv:1205.5233, Sec. II (read: https://arxiv.org/pdf/1205.5233) | P |
| Liquid density (canned Draught, degassed, temperature not stated) | 1006 kg/m^3 | Watamura et al., Sci. Rep. 9, 5718 (2019), https://www.nature.com/articles/s41598-019-42094-0 , Experiments section (read) | P |
| Gravity | OG 1.038-1.039 (9.75 Plato), ABV 4.2 %; degassed pub draught measured FG 1.009 by a forum poster, brewing-recipe FG 1.006-1.010 | BYO clone recipes https://byo.com/articles/10-classic-clones/ ; Guinness FAQ compilation https://www.panix.com/~clay/guiness.html | S (no brewer-published FG found). Densities above (1006-1007 kg/m^3 = SG 1.006-1.007) are the measured, usable numbers |
| Alcohol | 4.2 % | https://www.guinness.com/en/beers/guinness-draught | B |
| Dynamic viscosity, Draught at 6 C | 2.06 mPa s (=> nu = 2.05e-6 m^2/s) | Benilov et al., Sec. II | P |
| Dynamic viscosity, canned Draught | 2.1 mPa s (T not stated; nu = 2.09e-6) | Watamura et al., Experiments | P |
| Viscosity vs temperature, six beers incl. Guinness | 1.9-2.4 mPa s at 4 C falling to 0.8-1.0 mPa s at 37 C; Guinness Extra Stout is the highest, Guinness 0 the lowest; Newtonian-looking, Arrhenius fit | RheoSense microVISC PRO application brief https://www.rheosense.com/beer-viscosity-microvisc-pro-viscometer (read; plot only, no table numbers retrievable) | S/instrument vendor, measured at 8000 1/s |
| Viscosity vs temperature, a dark beer (not Guinness) | 2 C 3.91; 5 C 3.61; 7.5 C 3.36; 10 C 3.17; 12.5 C 3.02; 15 C 2.81; 20 C 2.53; 25 C 2.21 mPa s (to 1.01 mPa s at 90 C), shear 34 1/s | Severa & Los, Acta Univ. Agric. Silvic. Mendel. Brun. 56(2), 303 (2008), https://doi.org/10.11118/actaun200856020303 (abstract+table via search excerpt) | P, but a stronger/other dark beer: about 1.7x the Guinness number, do not use for Guinness |
| Viscosity of lagers/tripels/dubbel at 25 C | 1.25-1.59 mPa s | Chatzigiannakis et al., Phys. Fluids 37, 082139 (2025), Table I https://pubs.aip.org/aip/pof/article/37/8/082139/3360405 | P |
| Surface tension of beer (not Guinness) | 40.8-48.1 mN/m (six Belgian/lager beers, 25 C? bulk viscosity measured at 25 C; temperature of sigma not stated in excerpt) | Chatzigiannakis et al. 2025, Table I | P |
| Surface tension of beer vs T | Pilsener 42.6 (20 C) to 47.5 (0 C) mN/m, Hefeweizen 42.0-45.4 mN/m; authors' water control read 66.6 vs 72.8 so a calibration factor 1.093 would raise them to 46.5-51.9 | Potreck, TU Berlin thesis 2004, https://doi.org/10.14279/depositonce-882 (table excerpt) | P (thesis) |
| Surface tension, Guinness specifically | NOT FOUND. Benilov et al. use 0.745 N/m "water/air" (their text is a typo or misprint for 0.0745) | Benilov et al. Sec. II | - |
| Serving temperature | 6 C (Draught); "6-7 C" ; Draught Quality Standards: kegs 8-10 C chilled in-line to 4-6 C at the font | Guinness Webstore FAQ https://guinnesswebstore.com/pages/faq (6-7 C, brewer retail page); BYO Mr. Wizard quoting Guinness's Draught Quality Standards https://byo.com/mr-wizard/pouring-beer-on-nitro/ ; Benilov cites 6 C as Diageo's recommendation | B / S |
| Gas | Draught Quality Standards: 70 % N2 / 30 % CO2 at 32-40 psi (BYO paraphrase of the brewer's publication; other sources say 75/25); dissolved: ~1.2 volumes (2.4 g/L) CO2 and ~55 ppm N2 | BYO Mr. Wizard (Ashton Lewis) | S |
| Bubble size in the glass during settling | mean diameter 50 um (abstract-level statement), measured mean 61 um with volume concentration 8 % | Watamura et al. 2019 (Introduction and Experiments) | P |
| Bubble size, other measurement | 122 um "as reported in Ref. 11" of Benilov et al. | Benilov et al., Sec. II | P (secondary citation) |
| Bubble void fraction | canned 0.05, draught in pub ~0.1 (their own measurement), as served after the two-part pour ~0.02 (liquid, not head) | Benilov et al., Sec. II | P |
| Head height of a pint | 18-20 mm, "just above the harp"; also "~19 mm" | Nature Reviews Physics 2023 "The physics of fizz" https://www.nature.com/articles/s42254-023-00579-y (snippet read); brewer text says "domed proud of the rim" (guinness.com FAQ) | S / B |
| Foam liquid fraction / foam density of the head | NOT FOUND for Guinness in any source opened. Not stated in Sauret et al. either (they say it was not measured). Treat as an assumption; wet beer foam is O(5-10 % liquid) but I could not source that figure. | - | - |

Reading for the sim: use rho ~ 1007 kg/m^3, mu ~ 2.06e-3 Pa s (nu ~ 2.05e-6 m^2/s) at 6 C; at 20 C scale by about 0.7 (RheoSense/Severa trends: 4 C to 20 C falls by roughly 30 %). Surface tension is irrelevant to the (1,1) mode at R = 39 mm (Bond number rho g R^2/sigma ~ 340; sigma xi^2/(rho g R^2) = 3e-3 correction to omega^2, cf. Mayer & Krechetnikov Eq. 1) but matters for contact-line physics.

### Does NOT establish
- No Guinness-specific surface tension, FG, foam liquid fraction, foam bubble size inside the head (the 50-122 um numbers are bubbles in the settling liquid, not measured in the head, which coarsens), or measured foam rheology.

---

## Overall findings in short
1. Foam (Sauret 2015): amplitude damping rate = liquid + 9 +/- 3 s^-1 x [1 - exp(-xi/(5+/-2))] for a 3 mm slot with 3 mm bubbles; plateau scales as 1/w; mechanism = Plateau-border friction on the walls (Bretherton/Cantat-type f = K gamma Ca^(2/3)). Naive transfer to our glass: foam adds ~0.3-0.65 s^-1, larger than liquid-only wall damping ~0.1-0.2 s^-1; extrapolation uncertainty at least a factor 3 either way.
2. Wall Stokes layers, cylinder (1,1) deep: delta (log decrement per cycle) = 4.98 nu^(1/2) R^(-3/4) g^(-1/4) [NASA SP-8009 via Irvine; my derivation gives 3.50]; gamma = delta omega/(2 pi); for beer nu = 2.05e-6: gamma ~ 0.11-0.16 s^-1; inextensible film roughly doubles it; Miles saw 2-3x wall-only in real basins.
3. Keulegan/contact line: not quantifiable from the sources I could open; amplitude-dependent, up to 5x in small basins (Jiang et al. 0.05 -> 0.25 s^-1).
4. Mayer & Krechetnikov: computed log decrement ~0.02 for a 3.5 cm coffee cup, f ~ 3.65 Hz, no measured decay.

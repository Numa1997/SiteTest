# Fig. 12 sources: coffee spilling and foam damping

Compiled 7 November 2026. Every "Fact" below was read in the full text named under each paper, not from an abstract or search snippet.
Page numbers are the journal page labels printed on the copy read. SI units throughout; the papers' own units are given in brackets where they differ.
"Read off" means the value was read by eye from a plotted figure (rendered page image), not printed in the text.

Roads tried: arXiv API (export.arxiv.org) found the two Sauret et al. preprints but no arXiv version of Mayer & Krechetnikov (author search "Krechetnikov" lists 13 papers, none on coffee). OpenAlex says Mayer & Krechetnikov is closed access with no repository copy. Semantic Scholar API answered 429 (rate limit). Exa web search found the authors' own PDF on Krechetnikov's University of Alberta page. For Han (2016), the ScienceDirect PDF link returned 403 to curl; the full published text was read from its Scipedia mirror (HTML); the viXra preprint was downloaded but not used.

---

## 1. Mayer and Krechetnikov (2012)

**Citation.** H. C. Mayer and R. Krechetnikov, "Walking with coffee: Why does it spill?", Phys. Rev. E 85, 046117 (2012), 7 pp. DOI 10.1103/PhysRevE.85.046117.

**Read from.** <https://www.math.ualberta.ca/~rkrechet/files/publications/pre2012.pdf> (authors' page; this is the published APS typeset version, pages 046117-1 to 046117-7). Read in full, figures included.

**Note.** There is no arXiv version as far as the arXiv API shows; the brief was wrong on that point.

### Experiment
- Fact (Sec. II, p. 046117-1): one human subject walked "naturally" along a straight line at average speeds 0.5–2.5 m/s, filmed at 100 fps. The motion was analysed in the xy plane (forward and vertical) with MATLAB image analysis. The instant of spill was signalled by an LED triggered by a sensor watching the coffee level.
- Fact (Sec. II, p. 046117-1; ref. [14], p. 046117-7): two regimes, "focused" (trying not to spill) and "unfocused" (not concerned); in both the subject knew the cup was nearly full.
- Fact (ref. [13], p. 046117-7): walking was overground, not on a treadmill, so the start of the motion is natural.
- Fact (Fig. 2(c), p. 046117-2; Sec. II.A): coffee level is described by the spill angle α, with an equivalent acceleration ẍ_α (the steady acceleration that tilts the surface to the rim). Levels used: α = 8.1°, 12.1°, 13.7°, 16.5° (Figs. 4, 5).

### Cup size and sloshing frequency
- Fact (Eq. (1), p. 046117-2): ω_mn² = (g ε_mn / R) tanh(ε_mn H / R) [1 + (σ/(ρ g)) (ε_mn/R)²], with H the liquid height, R the cup radius, σ surface tension, ρ density. ε_mn are the roots of J_m′(ε) = 0; ε_11 = 1.841, ε_12 = 5.331, ε_1,n+1 = ε_1n + π. (The paper prints "ε_31 = 8.536"; 8.536 is the third root of J_1′, so this is ε_13.)
- Fact (p. 046117-2): mode shape of the antisymmetric wave ∝ J_1(ε_mn r/R); the n = 1 mode is plate 191 of Van Dyke's Album.
- Fact (p. 046117-2): "For a typical common size of a coffee cup, R ≃ 3.5 cm and H ≃ 10 cm, which is studied here", surface tension is negligible and ω_11 = ω_nat ~ 23 rad/s.
  So R = 0.035 m (diameter 0.070 m) and H = 0.10 m.
- Fact (p. 046117-3, top left): ν_11 = ν_nat ~ 3.65 Hz, T_nat ~ 0.27 s.
- Fact (p. 046117-3): cups range roughly from (R, H) = (2.5, 5.7) cm to (6.7, 8.9) cm, espresso to cappuccino, giving natural frequencies 2.6–4.3 Hz.
- Inference (my recomputation of Eq. (1)): R = 0.035 m, H = 0.10 m gives 3.61 Hz without surface tension and 3.65 Hz with σ = 0.072 N/m (a 1 % correction). The range ends recompute to 4.28 Hz and 2.59 Hz. All consistent with the paper.
- Fact (ref. [20], p. 046117-7): damping is not important. Logarithmic decrement δ ~ 0.02 (A_{n+1} = A_n e^{−δ}); amplitudes take N ~ 1/δ ~ 50 oscillations, t ~ 12 s, to fall by e.
- Inference: δ = 0.02 at 3.65 Hz is a decay rate δ·f ≈ 0.07 s⁻¹, a damping ratio ζ ≈ δ/(2π) ≈ 0.003.

### Walking frequencies and accelerations
- Fact (Sec. II.A, p. 046117-2; Fig. 4(b)): the cup is excited at f_cup nearly identical to the step frequency f_step, which rises with walking speed; f_cup = 1–2.5 Hz.
- Read off (Fig. 4(b), p. 046117-3): f_step rises from about 1.0–1.3 Hz at 0.5–0.6 m/s to about 2.3–2.5 Hz at 1.7–2.2 m/s; a few f_cup points sit near 1.7 Hz at about 2.1 m/s.
- Fact (Sec. II.A): the forward, vertical and pitching excitations show oscillations "on the order of 1 cm" superimposed on the mean path; pitching is about 2°, from arm swing and wrist flexibility.
- Fact (Sec. II.A, (ii), p. 046117-3): lateral and forward body oscillations both have amplitude about 20 mm (from biomechanics ref. [2]); the lateral frequency is about half the forward one, ~1.25 Hz.
- Fact (Sec. II.A): the maximum forward acceleration ẍ_max occurs early, in the speed-up; it increases with walking speed and is lower when focused at higher speeds (Fig. 4(a)).
- Read off (Fig. 4(a), p. 046117-3): ẍ_max ≈ 0.5 m/s² at 0.6 m/s up to ≈ 2.4 m/s² at 1.2 m/s (unfocused) [axis in cm/s², 50–250].
- Fact (Fig. 3 caption, p. 046117-2): example run, unfocused, 0.80 m/s, maximum acceleration 71 cm/s (printed so; presumably 0.71 m/s²), α = 12.1°.
- Fact (Sec. II.A; Fig. 4(c)): the relative standard deviation of forward velocity falls as speed rises ("the faster one walks the smoother the motion of the cup in the x direction"); the vertical excitation grows with speed (Fig. 4(d)).
- Read off (Fig. 4(c), (d)): forward velocity fluctuation about 2–8 % of mean speed; vertical cup excitation about 0.6–3.3 cm.

### Steps to spill
- Fact (p. 046117-3, right column): "most often coffee spills in the range of 4–5 m (7–10 steps) of walking distance."
- Fact (p. 046117-3; Fig. 5): N falls as ẍ_max/ẍ_α rises; for ẍ_max/ẍ_α > 1 the spill is almost instant (fluid statics: the start-up acceleration alone tilts the surface past the rim). Fuller cups (smaller α) spill in fewer steps. Focusing increases N.
- Read off (Fig. 5(a)–(c), p. 046117-4): spill events at N ≈ 1–7 steps; many runs with ẍ_max/ẍ_α ≈ 0.3–0.9 did not spill (plotted as "no spill").

### Why it spills (the paper's account)
- Fact (Sec. II.A, p. 046117-3): because f_cup = 1–2.5 Hz lies below the natural frequencies, it is the lowest antisymmetric mode that gets excited; it carries the largest sloshing mass.
- Fact (p. 046117-3): (i) back-and-forth excites the first antisymmetric mode; (ii) lateral at ~1.25 Hz matters less, further from 3.65 Hz; (iii) vertical: no Faraday instability expected, because the vertical frequency is below the natural one (Faraday response is subharmonic); (iv) pitching has the same frequency as back-and-forth and also drives the antisymmetric mode.
- Fact (p. 046117-3/4): the cup motion is a smooth oscillation at the walking frequency plus "noise", "a complicated combination of higher-frequency harmonics" (Fig. 3(c)); more noise in unfocused walking "substantially intensif[ies] the spilling".
- Fact (Sec. II.B, Eq. (4), p. 046117-5): model forcing x₀(t) = A sin(ω_cup t) + Σ a_n sin(ω_n t + φ_n), random ω_n, φ_n, a_n, with |a|/A = 0.1 (focused-like), 0.3, 0.5. More noise lowers steps to spill N/P (Fig. 7(b)).
- Fact (p. 046117-5): chirped frequency. Walking starts from rest, so the step frequency ramps up from zero to a steady value "typically ~0.6 of the natural frequency"; resonance can set in before the drive reaches the natural frequency (Fig. 7(c)).
- Fact (p. 046117-6): swirl (rotation of the nodal diameter) can be excited near resonance; the spherical pendulum model reproduces the planar-motion instability (Fig. 7(d)). Swirl "does not contribute much to coffee spilling".
- Fact (Sec. III, p. 046117-6): summary. We spill either by accelerating too much for the fill level (statics), or dynamically: the start-up acceleration sets an initial sloshing amplitude, which back-and-forth and pitching then amplify; noise harmonics make the mode unstable and cause swirl.
- Fact (Sec. III): the cup response curve is wider than the pendulum's, "explaining the stronger response of the liquid to excitations at frequencies far from resonance". They compare the focused/noise effect with stochastic resonance.
- Inference: Mayer and Krechetnikov do not say the 2nd harmonic of walking hits the sloshing mode; they say the fundamental (1–2.5 Hz, ~0.6 of the natural frequency) plus broadband noise, start-up acceleration and chirp. The 2nd-harmonic claim is Han (2016), who says so explicitly as a difference (see §3).

### Strategies they mention
- Fact (Sec. II, Sec. III): focusing (watching the cup, careful walking) delays the spill, partly through lower ẍ_max, partly through less noise. Whether this is feedback (identifying and suppressing the resonance) or open-loop carefulness "may depend on an individual" and is beyond their data.
- Fact (Sec. III): walk slower (time to spill increases with lower ẍ_max, i.e. lower speed); lower fill level (larger α) increases N.
- Fact (Sec. III, last paragraph): from sloshing engineering: (a) a flexible container acting as a sloshing absorber; (b) concentric ring baffles, perforated or not, which split the sloshing mass into smaller masses with higher first-mode frequencies.
- Fact (Sec. III): women have higher step frequency and shorter steps, which "may lead to differences in coffee spilling"; age effects on step frequency are small.

### Not found / not verified (Mayer and Krechetnikov)
- No cup diameter in the form "8 cm"; they give R ≃ 3.5 cm. Whether H ≃ 10 cm is the liquid height or the cup height is not stated plainly (Eq. (1) defines H as the liquid height).
- No accelerometer data; accelerations are from video. No acceleration spectrum (FFT) of the cup is shown.
- No measured sloshing frequency; 3.65 Hz is computed from Eq. (1).
- Number of subjects: one ("a human subject"). Number of runs is not stated.

---

## 2. Sauret, Boulogne, Cappello, Dressaire and Stone (2015)

**Citation.** A. Sauret, F. Boulogne, J. Cappello, E. Dressaire and H. A. Stone, "Damping of liquid sloshing by foams", Phys. Fluids 27, 022103 (2015). DOI 10.1063/1.4907048.

**Read from.** arXiv:1411.6542v2 (1 February 2015), <https://arxiv.org/pdf/1411.6542v2>. Read in full, 16 pages, with figures rendered and read. This is the authors' preprint; equation, figure and section numbers below are the preprint's (they are expected to match the journal, not checked against it).

**Companion read in full.** J. Cappello, A. Sauret, F. Boulogne, E. Dressaire and H. A. Stone, "Damping of liquid sloshing by foams: from everyday observations to liquid transport", J. Visualization (2014), arXiv:1411.2123v1, <https://arxiv.org/pdf/1411.2123v1>. Cited below as "JoV".

### Container and liquid
- Fact (Sec. II.A, p. 2): a rectangular glass cell (borosilicate walls, rubber bottom), length L = 70 mm, height 92 mm, width w from 3 to 19 mm. It is mounted on a stage driven by a mechanical vibrator and filmed at about 100 fps.
- Fact (Sec. IV, p. 7; Figs. 2, 5, 6): foam experiments use a liquid depth H = 4 cm of foaming solution in L = 7 cm cells; w = 3 mm (2D foam, one bubble thick), 6 mm and 15.9 mm (1, 2 and 5 bubble diameters; "confined 3D").
- Fact (Sec. II.A, p. 2): foaming solution 90 % water, 5 % glycerol, 5 % Dawn dish-washing liquid (v/v), well above the CMC; low surface modulus.
- Fact (Table I, p. 3): foam solution ν = 1.4 × 10⁻⁶ m²/s, γ = 25 × 10⁻³ N/m, ρ = 1.02 × 10³ kg/m³; water ν = 1.01 × 10⁻⁶ m²/s, γ = 72 × 10⁻³ N/m, ρ = 1.00 × 10³ kg/m³.

### Foam
- Fact (Sec. II.A, p. 3): monodisperse bubbles of diameter D = 3 mm, made through a 1.3 mm inner-diameter needle at Q = 20 µL/min, one layer at a time. (JoV says a 2.5 mm needle.)
- Fact (Sec. IV, p. 7): foam height = ξ D, ξ = number of bubble layers. Experiments last less than a few minutes, to avoid drainage and coarsening.
- Fact (Sec. IV.A, p. 7): no T1 rearrangements were seen; the foam behaves as a visco-elastic material with no plastic flow.

### Frequencies
- Fact (Eq. (1), p. 5): ω_n² = (g k_n + (γ/ρ) k_n³) tanh(k_n H), k_n = nπ/L; only odd modes are driven by a lateral force.
- Fact (Fig. 2 caption, p. 4): first resonance f₁ ≃ 3.2 Hz (H = 4 cm, w = 1.59 cm, L = 7 cm).
- Fact (Sec. IV.A, p. 7): with foam, the spectrum peaks at f₁ ≃ 3.1 Hz; the theory without foam gives 3.3 Hz. f₁ does not change significantly with ξ (Fig. 5(a), inset).
- Fact (JoV, Sec. 2): f = 3.22 ± 0.11 Hz, independent of foam thickness.
- Fact (Sec. III.A, p. 5; Fig. 3(b), inset): viscosity does not change f₁ significantly. Fact (App. A, Fig. 9): f₁ plateaus for H ≥ 4 cm (deep water).

### Damping without foam
- Fact (Eq. (2), p. 6): damping coefficient 1/τ = ⟨|Ė|⟩/(2E), found by fitting η(x,t) = η₀ exp(−t/τ) sin(ωt) after an impulse.
- Fact (Sec. III.B, Eqs. (3)–(7), p. 6): the dissipation is in the oscillating Stokes layers, δ = √(ν/ω), on the walls. Bulk dissipation is about πδw/L ~ 10⁻² of it. Scaling: 1/τ_ℓ ~ √(2π f ν) (1/L + 1/w), confirmed for different fluids and cell widths (Fig. 3(b)).
- Read off (Fig. 3(b), p. 5): 1/τ_ℓ ≈ 0.9 s⁻¹ (water, w = 1.9 cm) to ≈ 3.4 s⁻¹ (80 % glycerol, w = 1.6 cm); water at w = 1.6 cm ≈ 1.25 s⁻¹.
- Fact (Sec. IV.A, p. 7): foam solution alone in the w = 3 mm cell: 1/τ_ℓ ≃ 2 s⁻¹.

### Damping with foam
- Fact (Sec. IV.A, p. 7): harmonic forcing at f₁ with X₀ = 1 mm: without foam the maximum surface amplitude is about 1 cm; with ξ = 5 layers about 1 mm, "a factor of ten reduction". (The Fig. 4 caption says X₀ = 0.1 cm, f₁ = 3.125 Hz.)
- Fact (Eq. (8), p. 7): 1/τ = 1/τ_ℓ + (1/τ_f^∞)(1 − exp(−ξ/ξ_c)), with 1/τ_f^∞ = 9 ± 3 s⁻¹, plateau 1/τ_ℓ + 1/τ_f^∞ = 11 ± 3 s⁻¹, ξ_c = 5 ± 2 (w = 3 mm, H = 4 cm, L = 7 cm).
- Read off (Fig. 5(b), p. 9): 1/τ ≈ 2.4 s⁻¹ at ξ = 0, ≈ 4.2 at ξ = 1–2.5, ≈ 7.5–8 at ξ = 5, ≈ 9.5–11 at ξ = 7–9, then scatter about 9–13 out to ξ = 20 (error bars ±2–4 s⁻¹).
- Fact (Sec. IV.A, p. 7): for ξ > 5 both 1/τ and the maximum elevation reach a plateau; the foam/air interface stays nearly still.
- Fact (JoV, Sec. 2, w = 16 mm, H₁ = 40 mm): τ = 1.81 ± 0.05 s without foam, 0.63 ± 0.04 s with 6 mm of foam, 0.37 ± 0.01 s with 20 mm of foam.
- Inference: those are decay rates 0.55, 1.6 and 2.7 s⁻¹. At f ≈ 3.2 Hz, ζ ≈ (1/τ)/(2πf) ≈ 0.027, 0.079 and 0.13. For the 3 mm cell plateau (11 s⁻¹), ζ ≈ 0.55.
- Fact (Sec. IV.A, Fig. 6(a), p. 7 and 10): mean bubble speed decays with height in the foam as exp(−z/(ξ_c D)), ξ_c D = 16.8 ± 1.8 mm, about 5 layers, similar to 1/k₁ = L/π ≈ 22 mm. With fewer than two layers the bubble velocity is mostly vertical.
- Read off (Fig. 6(a) inset): v₀^max/(X₀ f₁) ≈ 80 at ξ = 1, falling to a plateau ≈ 30 for ξ ≥ 3.

### Mechanism
- Fact (Sec. IV.B, pp. 9–10): the foam's extra dissipation is viscous friction of the Plateau borders sliding on the two walls. Friction per border f_b = K γ_f Ca^{2/3}, Ca = µ_f v_b/γ_f ~ 3 × 10⁻³ (valid below 10⁻²). Dissipation ∝ Σ ⟨v_b^{5/3}⟩.
- Fact (Eq. (14), p. 10): 1/τ_f = (12π ξ_c K′ |cos ωt|^{5/3})/(5 ρ w L (v₀^max)^{1/3}) × (1 − exp(−5ξ/(3ξ_c))), K′ = K γ_f^{1/3} µ_f^{2/3}. So 1/τ_f ∝ 1/w and saturates exponentially with ξ.
- Fact (Eq. (15)–(16), p. 10): fitted prefactor 2.76 cm/s gives K ≈ 1.9 m/s with v₀^max ≈ 0.1 m/s; the literature law gives K ≈ 9.1 m/s; the authors call these compatible.
- Fact (Sec. IV.C, p. 11): in confined 3D foams only the bubbles touching the walls dissipate; bulk bubbles are carried along. w/τ_f collapses for w = 3, 6, 16 mm. Exponential-fit plateau w/τ_f^∞ = 1.6 ± 0.3 cm/s; the best fit of Eq. (14) gives ≃ 3.1 cm/s.
- Read off (Fig. 6(b), p. 11): w/τ_f rises from ≈ 0.5 cm/s at ξ = 1–2 to ≈ 3 cm/s by ξ ≈ 7, then scatters 2–4 cm/s.
- Fact (Sec. IV.C and V): the plateau rises slightly with w, so bulk dissipation may add a little in 3D. The cells are narrow (≤ 6 bubbles across); wide 3D containers need more study.
- Fact (Abstract; Sec. I; JoV, Sec. 1): motivation: "beer does not slosh as readily as water". JoV Fig. 1 photographs a glass of coffee beside a glass of beer with foam thickness H₀, given the same impulse.

### Not found / not verified (Sauret et al.)
- No cylindrical cup, no pint glass, no Guinness, no nitrogen foam: only rectangular Hele-Shaw-like cells with dish-soap foam of 3 mm bubbles.
- No damping ratio quoted as such; ζ values above are my conversions.
- Journal page numbers not checked against the AIP version (only the arXiv v2 was read).

---

## 3. Han (2016), follow-up

**Citation.** J. Han, "A Study on the Coffee Spilling Phenomena in the Low Impulse Regime", Achievements in the Life Sciences 10(1), 87–101 (2016). DOI 10.1016/j.als.2016.05.009. Open access (CC BY-NC-ND 4.0).

**Read from.** Scipedia's full-text HTML reproduction of the published article, <https://www.scipedia.com/public/Han_2016a>, read in full (text, captions, footnotes, references). The figures themselves were not visible there, so no values were read off plots. The ScienceDirect PDF returned 403. The page numbers 87–101 are from the citation record, not seen in the copy read.

- Fact (Introduction): with a mechanical vibrator at 2 Hz, a wine glass sloshes hard while a cylindrical mug stays calm; at 4 Hz the reverse (Fig. 3).
- Fact (Introduction): "effective cup height" (cup height minus liquid level) is treated as a classification, not a variable; "the taller the cup and lesser the coffee, the less you spill".
- Fact (Liquid Oscillation Properties, Eq. (1)): same formula as Mayer and Krechetnikov. Inputs: "generic cup dimensions (Amplifer, n.d.) of 82 mm diameter and 95 mm height", coffee σ ≈ 0.037 N/m at 40 °C (note 1, citing Sobolík et al. 2002), ε_11 = 1.841. Han gives a first antisymmetric mode ≈ 3.95 Hz.
- Inference (my recomputation): using R = 0.041 m and H = 0.095 m in Eq. (1) gives 3.34 Hz, not 3.95 Hz. Using the mug's inner radius 0.035 m (82 mm outer minus two 6 mm walls, from the cited blog) gives about 3.65 Hz. I cannot reproduce Han's 3.95 Hz.
- Fact (Fig. 5 and text): measured free decay after one 2 cm, 2 Hz push: single peak ≈ 3.8 Hz; damping coefficient γ ≈ 0.674 rad/s (exponential envelope fit, R² = 0.9774).
- Inference: 0.674 s⁻¹ at 3.8 Hz is ζ ≈ 0.028, about ten times Mayer and Krechetnikov's δ ~ 0.02 estimate (ζ ≈ 0.003).
- Fact (Cup Motion Properties, Fig. 6): smartphone accelerometer (Samsung Galaxy S4) on the mug, mass set to a 2/3-full cup, normal hand posture. y = walking direction, z = vertical, x = sideways. z has the largest acceleration; x is almost negligible.
- Fact (same section): y-spectrum has "at least five or more distinct harmonic frequencies"; "the second harmonic frequency coincides with 3.5–4 Hz, which is the resonance frequency of coffee". The z spectrum is dominated by ≈ 1.7 Hz, "what we normally perceive to be the walking frequency". The x spectrum peaks at ≈ 1 Hz, half the walking frequency.
- Fact (same section): Han attributes the harmonics to the extra freedom of the wrist, not the arm. He suggests a cup strapped to the waist would probably not spill. Vertical 1.7 Hz is near half the resonance and might pump it, or give subharmonic resonance (not investigated).
- Fact (Discussion and Conclusion): "the second dominant frequency corresponded to the resonance frequency of coffee, resulting in maximum spillage". Han states this differs from Mayer and Krechetnikov, "for their research assumed that the driving force due to walking is monochromatic".
- Fact (Suppressing Resonance): walking backwards (5 repeats) flattens the y spectrum and removes the higher harmonics (Fig. 7). The "claw-hand" posture (cup gripped from above by the rim) reduces higher harmonics; 1.7 Hz remains (Figs. 8, 9). Dividing the cup into smaller cylindrical cells raises the frequency (Fig. 12; not quantified).
- Fact (Suppressing Resonance, Figs. 10–11): foam test in a Hele-Shaw cell, foaming solution 90 % water + 10 % glycerol, 0, 1 and 2 cm of foam, runs of about 1 s. The peak drops from ≈ 3.3 Hz to 3 Hz.
  The damping coefficient values conflict within the paper: text "from 1.025 rad/s to 2.928 rad/s" ("nearly triples"); Fig. 11 caption "increased to 2.93 rad/s from 2.23 rad/s", with ω_d 20.16 → 19.83 rad/s (R² = 0.8877, 0.7668).
- Fact (Model Studies): pendulum models with walking 2 Hz and slosh 4 Hz (actual ≈ 1.7 and 3.8 Hz). Arm M = 1 kg on k = 157.9137 N/m; coffee pendulum m₁ = 0.1 kg, l₁ = 1.55 cm.
  The normal-hand model's coffee responds at 4 Hz though the arm moves at 2 Hz. After 500 s it settles to 1–1.5 Hz. The claw-hand double pendulum halves the frequency at each stage.

### Not found / not verified (Han)
- Figures (spectra, time series) not seen; no read-off values.
- The 3.95 Hz prediction could not be reproduced from the stated inputs (see Inference above).
- The foam damping numbers are internally inconsistent (text vs Fig. 11 caption).
- Han's "82 mm × 95 mm" comes from a blog, not a standard.

---

## 4. Typical mug dimensions

- Fact (Mayer and Krechetnikov 2012, p. 046117-2): "a typical common size of a coffee cup, R ≃ 3.5 cm and H ≃ 10 cm". Cups range from (R, H) = (2.5, 5.7) cm (espresso) to (6.7, 8.9) cm (cappuccino) (p. 046117-3).
- Fact (Han 2016, Liquid Oscillation Properties): "generic cup dimensions ... of 82 mm diameter and 95 mm height", citing "Amplifer, n.d., The Standard Coffee Mug Dimensions, http://blog.ampli.fi/the-standard-coffee-mug-dimensions/".
- Fact (that blog, read in full on 7 Nov 2026; published 6 Jan 2013, edited 26 Aug 2014): five mugs measured. Diameters 81–82 mm, heights 92–99 mm, wall 6–7 mm, measured volumes 300–375 ml. "Standard Coffee Mug Dimensions v1.0": outer diameter 82 mm, height 95 mm, wall 6 mm, bottom 10 mm.
  The author says no real standard exists. A personal blog, not a standard or a peer-reviewed source.
- Inference: inner diameter ≈ 82 − 2 × 6 = 70 mm (R = 35 mm), inner depth ≈ 95 − 10 = 85 mm. This matches Mayer and Krechetnikov's R ≃ 3.5 cm and gives f₁ ≈ 3.65 Hz full.
- Not found: an ISO or other formal standard for mug size; none of the papers cites one.

---

## 5. Not found / not read at all
- No paper read here measures a pint glass, a stout or nitrogen-widget foam. Sauret et al.'s bubbles are 3 mm soap foam in narrow rectangular cells. Any transfer to a Guinness head (smaller bubbles, a tapered glass about 9 cm across) is Inference, not sourced.
- Also downloaded but not read: arXiv:2501.01180 ("Science of a coffee cup: a physicist walks into a bar...", 2025), a pedagogical review that may cover sloshing. It was not read, so nothing from it is cited.

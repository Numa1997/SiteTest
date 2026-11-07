# Check of note section 14, "A mug of coffee beside the pint" (Fig. 12)

Checked 7 November 2026. Scope: `public/simulations/beer-slosh.html`, section `p-coffee`, lines 763–790 (equations C1–C3, Table 7).
The plan file was not read. No file other than this one was changed.

## How it was checked

- **Equations.** Re-derived in SymPy 1.14 (scratch script `derive.py`). C1: potential flow φ = A J₁(kr) cos θ cosh kz, with the kinematic and dynamic surface conditions including the Laplace pressure. Laplace residual 0, ξ₁₁ = 1.841184 from J₁′ = 0, and (derived ω²) − C1 = 0. C2: zero net volume of the tilted plane over the disc, then solved for a. C3: envelope of the damped oscillator; wall area per volume, cell against cylinder.
- **Numbers.** `node tools/fig12/coffee.cjs 10 5` and `… 10 10` were run in Node. Separately, the tool's own source was run inside headless Chromium 153 on the page itself, served by `notes/fig12/serve.cjs`, using the page's loaded `StoutCart.NMFluid`, `GUINNESS_GLASS` and `STOUT_NM`. The Node and Chromium outputs agree character for character, and both agree with `notes/fig12/runs/coffee-5mm.txt` and `coffee.txt` exactly (`diff` empty). A run takes 9 s, not a minute.
  A probe with the same loop printed unrounded spill volumes and checked whether the breaking clip of `NMFluid.step` fired. It did not fire in any Table 7 case.
- **Sources.** Each cited claim was checked against `notes/fig12/coffee-sources.md`. The papers themselves were also fetched and read at the cited places:
  - Mayer and Krechetnikov: authors' PDF; page 3 was rendered to read Fig. 4.
  - Sauret et al.: arXiv:1411.6542v2.
  - Han: Scipedia full text.

## Equations

| Item | Line | Verdict |
|---|---|---|
| C1, ω₁₁² = (gξ₁₁/R) tanh(ξ₁₁h/R)(1 + σξ₁₁²/(ρgR²)) | 768 | verified. It follows from potential flow with a free-slip wall (J₁′(ξ) = 0) and the Laplace pressure, and SymPy finds a difference of 0. Units: the capillary term σξ²/(ρgR²) is dimensionless. Limits: σ → 0 gives (16); h → 0 gives ω² → gξ²h/R², the shallow basin of problem 1; h → ∞ gives tanh → 1. It is Mayer and Krechetnikov's eq. (1), p. 046117-2, character for character. |
| C2, a_rim = gΔ/R = g tan α | 771 | verified. The plane z = h − (a/g)x has zero net volume over the disc (SymPy), so the wall rises by Ra/g; setting this equal to Δ gives a = gΔ/R, and Δ = R tan α gives g tan α. Units m/s². Limit Δ → 0 gives a → 0. The pint's value assumes the glass above the surface is straight, as problem 5 states. |
| C3, ζ_f = 1/(ω₁₁τ_f) ≈ (w/τ_f)_∞/(ω₁₁R) | 775 | verified, as the stated inference. Sauret et al. define 1/τ by η = η₀e^(−t/τ) sin ωt (their eq. (2) and §III.B), an amplitude rate, so ζ = 1/(ωτ). The damped oscillator gives Re s = −ζω (SymPy). Wall per volume is 2/w for two cell walls and 2/R for a cylinder (SymPy), so 1/τ_f = (w/τ_f)/R. Units: (m/s)/(rad/s · m) is dimensionless. Limit R → ∞ gives ζ_f → 0. Unstated assumption: the transfer also takes the same wavelength (Sauret's L = 70 mm against the pint's 2R = 78 mm) and the same swing amplitude (their eq. (14) has (v₀^max)^(−1/3)). This is acceptable for an order-of-magnitude statement, which is how the text uses it. |

## Numbers

All "tool" values are the same in Node, in Chromium, and in the stored runs.

| Line | Number in the note | Verdict |
|---|---|---|
| 765 | step rate 1–2.5 per second | verified (M&K p. 046117-3, Fig. 4(b): f_cup = 1–2.5 Hz). |
| 765 | pint 22.5 mm below rim | verified (tool: rim 22.5 mm above). |
| 765 | "every number of ours is printed by `coffee.cjs`" | wrong, because several numbers are derived from the printed ones and not printed: 5 %, three times, four to seven times, gain 1.1–2.1, h/R 2.9 and 3.2, 4 parts in 10⁵ (the last appears only in a code comment). Suggested wording: "every number of ours is printed by, or computed from what is printed by, …". |
| 766 | R = 35 mm, h = 100 mm, "typical common size" | verified (M&K p. 046117-2: "R ≃ 3.5 cm and H ≃ 10 cm"; H is the liquid height in their eq. (1)). |
| 766 | α = 8.1° to 16.5° | verified (M&K Figs. 4–5: levels 8.1°, 12.1°, 13.7°, 16.5°). |
| 766 | "their middle level, α = 12.1°" | wrong, because there are four levels and 12.1° is the second of them; the middle of the range is 12.3°. Correct wording: "their level α = 12.1° (that of their Fig. 3 example), near the middle of their range". |
| 766 | R tan α = 7.5 mm | verified (7.503 mm). |
| 766 | pint R(h) = 39.1 mm, 125 mm deep | verified (tool). |
| 767 | h/R = 2.9 and 3.2 | verified (2.857, 3.197). |
| 769 | mug f₁₁ = 3.615 Hz, 3.652 Hz with σ = 0.072 N/m | verified (3.6154, 3.6519). Remark: Han gives σ ≈ 0.037 N/m for coffee at 40 °C, which would give 3.634 Hz. Water's σ reproduces M&K's 3.65 Hz, so the choice is consistent with the citation. |
| 769 | M&K give 3.65 Hz | verified (p. 046117-3: ν₁₁ ∼ 3.65 Hz). |
| 769 | pint 3.421 and 3.448 Hz | verified (3.4207, 3.4484). |
| 769 | "5 % slower", ω ∝ R^(−1/2) | verified (5.4 % without σ, 5.6 % with σ; √(35/39.1) gives 5.4 %). |
| 772 | mug 2.10 m/s² | verified (2.103). |
| 772 | M&K's fills 1.40–2.91 m/s² | verified (1.396, 2.906). |
| 772 | pint 5.65 m/s² (problem 5) | verified (5.645). Problem 5 prints the answer as 5.6 m/s², which is the same value rounded. |
| 772 | walker's forward acceleration 0.5–2.4 m/s² [27, Fig. 4(a)] | verified (Fig. 4(a) rendered: ẍ_max from about 45 to about 240 cm/s²). |
| 772 | "filled three times closer to spilling" | verified (22.5/7.50 = 3.00). |
| 773 | ζ = 0.0058, e-fold 7.6 s (mug); 0.0053, 8.7 s (pint) | verified (0.00581, 7.57 s; 0.00535, 8.70 s; K = 5.23, as in `ModalFluid.modes`). The R^(−3/4) ratio is 1.09. |
| 773 | M&K δ ≈ 0.02, ζ ≈ 0.003 [27, ref. 20] | verified (ref. [20]: δ ∼ 0.02; δ/2π = 0.0032). |
| 773 | Han 0.674 s⁻¹ at 3.8 Hz, ζ ≈ 0.028 | verified (Han: γ ≈ 0.674 rad/s from the envelope, defined as ⟨Ė⟩/2E, an amplitude rate; single peak ≈ 3.8 Hz; 0.674/(2π·3.8) = 0.0282). |
| 774 | cells 70 mm long, 3 to 16 mm wide | verified (Sauret §II.A: L = 70 mm; the foam runs used w = 3, 6 and 15.9 mm). |
| 774 | "a few layers of 3 mm bubbles cut the swing tenfold" [28, §IV.A] | verified in substance, but imprecise. The paper says "only ξ = 5 layers", amplitude from about 1 cm to about 1 mm, "a factor of ten", in the 3 mm (Hele-Shaw) cell. Better: "five layers … in a 3 mm cell". |
| 774 | saturates after about five layers | verified (ξ_c = 5 ± 2, eq. (8)). |
| 774 | 1/τ_f ∝ 1/w [28, eq. (14)] | verified (eq. (14) has w in the denominator; §IV.C states the 1/w scaling). |
| 774 | w/τ_f = 1.6 ± 0.3 cm/s; 3.1 cm/s from eq. (14) [28, §IV.C] | verified (§IV.C, verbatim). |
| 776 | ζ_f = 0.019–0.037 for the pint | verified (0.0190, 0.0369). |
| 776 | "four to seven times the wall's own damping" | verified (3.6 to 6.9; "four" rounds 3.6). |
| 776 | "a stout's head is of nitrogen bubbles far smaller" | unverifiable, because no source read for this section gives a bubble size for stout (coffee-sources.md §5 marks it as inference). It is plausible, but it should be marked as not from [27]–[29] or given a source. |
| 776 | ζ = 0.0053 + 0.019, 4.6 times | verified (tool: zetaScale 4.559, printed 4.6). Method remark: `zetaScale` multiplies every mode's damping (the five NM coordinates and linear modes 2 and 3) by 4.56. By C3 the head would add a decay rate 1/τ_f that is the same for all modes, so the higher modes' ζ would go as 1/ω, not as ζ₁√(ω₁/ω_n)·4.56. This has little effect, since the first mode dominates, but the text describes only ζ₁. |
| 777 | 1–2.5 Hz [27, Fig. 4(b)]; "on the order of 1 cm"; pitch about 2°; sideways at half [27, §II.A] | verified (p. 046117-1 and -3). |
| 777 | 0.28–0.69 of the mug's f₁₁, 0.29–0.73 of the pint's | verified (0.277–0.691, 0.292–0.731). |
| 777 | gain 1/(1 − r²), 1.1 to 2.1 | verified (from (17) with a_z = 0, steady state; mug 1.08–1.92, pint 1.09–2.15). |
| 777 | Han: second harmonic at 3.5–4 Hz on the resonance | verified (Han: "the second harmonic frequency coincides with 3.5–4 Hz"). |
| 777 | a_x = Aω²[sin ωt + 4e₂ sin 2ωt]; e₂ a share of the displacement | verified (code line 46; it is −ẍ for x = −A[sin ωt + e₂ sin 2ωt]). |
| 777 | e₂ = 0.3, M&K's middle noise level | verified (M&K eq. (4), noise \|a\|/A = 0.1, 0.3, 0.5). |
| 779–785 | Table 7, all 25 cells (steps and largest rise) | verified, every cell identical to the tool's output at A = 5 mm, T = 10 s. Unrounded probe values: the first-drop steps are 0.69, 0.85, 0.50, 0.24, 0.21 (mug), 2.13 and 1.24 (pint), 1.53 (head). The breaking clip did not fire in any cell. |
| 779 | rim 7.5 mm and 22.5 mm | verified. |
| 787 | "The mug spills where the pint does not, … and at 1.5 steps a second and above with the harmonic" | wrong, because with the harmonic the pint also spills at 1.5 steps a second (first drop at 2.1 steps, 0.004 ml) and at 1.75 (24 ml). The mug spills where the pint does not only at 2.0 and 2.5 with the harmonic, and at 2.5 (and 2.25, not tabled) without it. Correct wording: "The mug spills where the pint does not: at 2.5 steps a second with a clean step, and at 2 and 2.5 with the harmonic; with the harmonic it spills from 1.5 steps a second up, the pint only at 1.5 and 1.75." |
| 787 | at 1.75: 2 × 1.75 = 3.5 Hz on both resonances; pint 24 ml, mug 74 ml | verified (23.8 ml, 74.0 ml; 3.5 Hz is within 3 % of 3.42 and 3.62 Hz). |
| 787 | the head "removes the spill at 1.5 steps a second and cuts it at 1.75 from 24 to 3 ml" | verified (23.8 to 3.0 ml). However, the spill it "removes" at 1.5 is 0.004 ml, a touch of the rim. Say so, e.g. "removes the bare touch of the rim at 1.5 steps a second". |
| 787 | "the drops come within the first two steps" | wrong, because the latest first drop in Table 7 is at 2.1 steps (pint, e₂ = 0.3, 1.5 per second; unrounded 2.13). Correct: "within the first two and a bit steps", or "by the third step". |
| 787 | 7–10 steps (4–5 m) [27, p. 046117-3] | verified (verbatim). |
| 787 | "their walkers start gently and adjust" | wrong, because M&K had one subject, and they report that his largest acceleration comes at the start ("the maximum acceleration ẍ_max is realized early on", p. 046117-1). What is gentle in M&K is the step frequency, which ramps up from zero (a chirp, p. 046117-5). Correct wording: "their subject's step frequency ramps up from rest over the first steps and he adjusts; a steady 5 mm sine at full frequency from the first step is a harsher walk than his". |
| 787 | "With 10 mm both vessels spill at most step rates" | wrong, because with a clean step (e₂ = 0) the mug spills at 3 of 7 rates (2.0, 2.25, 2.5) and the pint at 2 of 7 (2.25, 2.5). Only with the harmonic do they spill at most rates (mug 6 of 7, pint 5 of 7). Correct: "With 10 mm both spill at most step rates with the harmonic, and from 2 (mug) or 2.25 (pint) steps a second with a clean step." |
| 788 | pitch adds gθ to a_x | verified (small-angle rotation of gravity into the cup frame). Method remark: the runs drive a_x only. A 2° pitch at the step frequency gives gθ = 0.34 m/s², as large as Aω² for A = 5 mm at 1.3 Hz, so the runs leave out a forcing the paragraph calls equal in kind. The note does not say that the runs omit it. |
| 788 | 2f₁₁ ≈ 7 Hz | verified (7.23 Hz for the mug, 6.84 Hz for the pint). |
| 788 | sideways minor [27, §II.A]; no Faraday expected [27, §II.A] | verified (p. 046117-3, items (ii) and (iii)). |
| 788 | "Watching the cup, which their walkers did in the 'focused' runs" | wrong, because M&K define "focused" as "trying not to spill" (p. 046117-1, ref. [14]). They never say the subject watched the cup, and they leave open whether focusing is feedback or open-loop care (p. 046117-6). Also, there was one subject, not several walkers. Correct: "Trying not to spill, as their subject did in the 'focused' runs, may act as the sensor". |
| 788 | "their focused walkers spilled later [27, §III]" | verified in substance ("focusing tends to increase N", p. 046117-3). Wrong citation place: §III only says the number of steps differs between regimes. Cite [27, p. 046117-3], and use "their subject … when focused". |
| 789 | coefficients for h/R = 3.2; mug 2.9; tanh(ξ₁₁h/R) differs by 4 parts in 10⁵ | verified (STOUT_NM.h = 3.197; difference 3.85 × 10⁻⁵). The m = 0 and m = 2 tanh factors differ by less than 10⁻⁷, so the ξ₁₁ term is indeed the only one that matters. |
| 766, 787, 788 | "their walkers" (plural) | wrong, because M&K had one subject ("a human subject was asked to walk naturally", p. 046117-1; coffee-sources.md §1, "Not found"). Correct: "their subject" or "their walker". |

## Method description against the code (tools/fig12/coffee.cjs)

- "We drive both vessels through the nonlinear live model (section 11.9)": matches. `NMFluid` from `stout-cart.js` is the same code the page loads, which was confirmed by running it in Chromium on the page.
- The mug is an upright cylinder, R = 35 mm, h = 100 mm, rim at h + R tan 12.1°. The pint is the tulip profile at 125 mm. Both match the code (lines 19–21).
- The drive formula matches code line 46. The time step (1/400 s, with 0.5 ms substeps inside `step`) is not stated in the note; this is not an error.
- "Walked from rest": matches. The modes start at zero apart from the swirl seed b₂ = 10⁻⁵ of `NMFluid`.
- "Steps before the first drop": matches. This is t·f_step at the first step with spilled volume above 10⁻⁹ m³ (0.001 ml).
- "Largest rise at the wall": matches. This is the maximum over time of `wallLift()`, the highest wall point over 72 angles, including p₀, p₂ and linear modes 2 and 3.
- "Pint with head": matches. zetaScale = (ζ + ζ_f,low)/ζ = 4.56, with the caveat on the higher modes given in the line-776 row.
- Not stated, and could be: the drive is forward only (no pitch, sway or bob), and the breaking clip exists. The clip did not fire in Table 7, so it does not affect the table.

## Summary

- Equations C1–C3 are right.
- Every computed number reproduces exactly, in Node and in headless Chromium on the page.
- Table 7 matches the tool cell for cell.
- The errors are all in the words around the numbers:
  - line 765: "every number … printed";
  - line 766: "middle level";
  - line 787: "mug spills where the pint does not … 1.5 and above", "within the first two steps", "start gently", "with 10 mm … at most step rates";
  - line 788: "watching the cup", and the §III citation;
  - lines 766, 787, 788: "walkers" (plural) for M&K's single subject.
- Unverifiable: the size of the nitrogen bubbles in a stout's head (line 776).

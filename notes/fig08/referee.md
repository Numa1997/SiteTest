# Fig. 8 · Draw & Decompose · referee report

Read blind (no plan.md, no check.md, no teacher report), as a school student good at mathematics and as a physics
graduate, against `notes/STANDARD.md` and above all "Numa's verdicts": only real obstacles count. (A) means a reader
following the note in order gets lost, a step is skipped, a symbol is used before it is defined, a claim is wrong or
unsupported, or a needed physical picture is missing. (B) is taste. A section with no (A) item is **clear**.

**How it was read.** Built with `OUT_DIR=/tmp/fig08-ref-dist npm run build`; the built page is identical to
`public/simulations/draw-decompose.html`. Served by a small Node static server and opened in headless Chromium
(Playwright, 1440 × 900). "Expand all" opened every fold. 325 KaTeX formulas rendered, 0 KaTeX errors, no raw `\(`
left, no page or console errors. Each section was screenshotted with the pinned fold headers unpinned so they do not
cover the text: `notes/fig08/shots/00-head.png`, `01-p-circles.png` … `09-p-limits.png`, `99-refs.png`. The rendered text
was read with every formula replaced by its TeX source.

**Numbers checked.** A NumPy transcription of the page's own `resamp()`, `dft()` and `chainAt()` reproduces every number
I tried: ⟨|z|²⟩ = 0.515044672459522 and e₂₄ = 0.005405966670666 for the heart; the heart's relative errors 23.9 %,
2.87 %, 0.753 %, 0.234 % and 0.068 % at K = 1, 10, 24, 50 and 120; the square's 98.523 % and 0.098312 at K = 1, its
radii 0.80308, 0.09031 and 0.03171, the stray k = 2 and k = −1 radii of 2.47 × 10⁻³, the corner gaps of 0.019 to 0.022 and
the side crossings of 0.0104 and 0.0038; the heart's k²|c_k| = 0.5505, 0.552 and 0.544; the open wave's |k||c_k| = 0.271,
its errors 20.5 %, 14.2 % and 8.41 %, and its overshoots 5.86 %, 7.93 % and 9.52 %; the figure eight's 5.90 × 10⁻⁵ at
|k| = 60 and its relative error at K = 120 of 8.4 × 10⁻⁴. The aliasing claims of 4.2 (less than 0.1 % for the heart's
three largest circles, about 20 % for the heart and 10 % for the open wave near |k| = 60) hold when the 256-sample and
65 536-sample transforms are both sampled at spacing L/N, so they isolate aliasing as the sentence says. The algebra of
(11), (12), (13), (14) and of the square and heart corner sums checks out, and so do the page facts in sections 7 and 8
against the code: Δt is capped at 0.05 s, the view relaxes with τ = 0.4 s, the trail opacity runs from 0.12 + 0.88/24 ≈ 0.16
to 1, and there are four arrow colours. All four further-reading links resolve. Princeton's link returns 403 to curl,
but a browser fetch through Firecrawl gets 200 and the right book page.

---

## Abstract

(A) none.

(B) none.

## 1 · A drawing made of circles: **clear**

(A) none. The picture comes before any symbol: an equaliser, JPEG and MP3, a bead on a wire, Ptolemy. The kinematics-not-dynamics
point is made plainly.

(B)
- Figure 1 shows formulas, "θⱼ = kⱼ t + arg c_kⱼ" and "z(t) = Σⱼ c_kⱼ e^{i kⱼ t}", that use t, arg and e^{i…} one section
  before section 2 defines them. The caption makes the picture readable without them (arm length |c_kⱼ|, kⱼ turns per
  loop, angle θⱼ), so nobody is stuck, but "(section 2)" in the caption would say where they come from.
- "the two circles that turn once per loop, one each way, already draw an ellipse": this is stated, not shown. It leans
  on Fig. 7.
- The caption's three-fold symmetry argument is right. "because 1, −2 and 4 all leave remainder 1 on division by 3"
  would let a student check it.

## 2 · The model: **clear**

(A) none. The loop parameter t = 2πs/L is defined before use, "t is not a clock" heads off the obvious confusion,
the counter-rotating pair is set against a real signal, and c₀ is the centre of mass of a uniform wire.

(B)
- This is the roughest sentence group in the note, though the thread holds: "The page subtracts the finite sample mean.
  That approximates the uniform wire's centre of mass; its resampling repeats the endpoint (section 7.1), so the
  equivalence is not exact. The centred sample mean is zero." "Samples", "resampling" and "repeats the endpoint" appear
  before the text has introduced sampling. Figure 2 does that a few lines later. The last sentence never says the
  useful consequence: the page's c₀ is zero and the shape sits on the origin. It reads as a hedge bolted on.
- Figure 2's caption calls the left stroke "a closed stroke", but its ends visibly do not meet, and the same caption ends
  with "A hand-drawn stroke rarely closes exactly".
- "Each term is a phasor exactly as in Fig. 7" uses e^{iθ} as the unit arrow at angle θ without restating it. The
  sentence then says what the arrow does, so this is fine.

## 3 · Each circle is an average: **clear**

(A) none. The roundabout picture is the right physical picture for orthogonality. Eq. (2) is justified in one line, and
(3) follows in one step.

(B) none.

## 4 · From an integral to 256 samples ★: **clear** (for its ★ reader)

(A) none for the graduate this ★ section is written for. 4.1 (the closing polygon), 4.2 (the aliases, with measured
sizes) and 4.3 (the two lines of `dft()`) are clear.

(B)
- "Keep the two meanings separate. The integral coefficient in (3) describes the continuous parametrised curve. The
  finite sum in (4) is an exact orthogonal-coordinate calculation for the sampled sequence, apart from rounding, and only
  an approximation to the integral coefficient. In the discrete reconstruction and error formulas, cₖ means this computed
  coefficient; the alias identity (6) explicitly compares the finite sum with the continuum coefficients." This says in
  jargon ("orthogonal-coordinate calculation", "continuum coefficients") what 4.1 then says plainly ("The sum (4) is
  more than an approximation"). It also cites "the alias identity (6)" before aliasing has been met. A graduate gets
  through it. A school student would not, and this matters if the fix for section 5 is made by taking the ★ off this
  lead (see section 5). The point it carries is needed: from here on cₖ means the computed number. One plain sentence would
  carry it.
- "N neighbouring frequencies" means N consecutive integers k. That is clear enough.
- 4.2 compares aliasing alone. Through the endpoint pause of 7.1, the page's own heart radius at k = −3 differs from the
  continuum one by about 3 %. This is not wrong here, just not mentioned.

## 5 · Parseval's theorem and the error: **needs work**

(A)
1. **The central derivation depends on the ★ section that the abstract says can be skipped.** The abstract promises:
   "Sections marked ★ carry the heavier mathematics and can be skipped on a first reading without losing the thread."
   Section 5, which is not starred, opens: "Square the discrete series, |zₙ|² = zₙzₙ* = Σⱼ Σₖ cⱼ cₖ* e^{2πi(j−k)n/N}, …
   and average over the samples. By (5) every cross term with j ≠ k averages to zero, leaving Parseval's theorem".
   "The discrete series" zₙ = Σₖ cₖ e^{2πikn/N} and eq. (5) exist only in ★ section 4 (4.1). So do "the sum running over N
   neighbouring frequencies" and the cₖ in (8) and (9) being the computed coefficient. zₙ and N are known from Figure 2.
   A school student who skips section 4 as invited is therefore lost at the first line of the page's central result,
   eq. (8). Two smallest fixes, either one enough. (a) One or two sentences at the head of section 5 recall that the 256
   samples are reproduced exactly by zₙ = Σₖ cₖ e^{2πikn/N}, and that on the samples the exponentials are orthogonal
   exactly as in (2), which is eq. (5). (b) Move the ★ from section 4's title to parts 4.2 and 4.3, so the lead and 4.1
   are for everyone. Then the "Keep the two meanings separate" paragraph must be made plain (section 4, B).

(B)
- "It approximates the same quantity for a uniform wire; the repeated endpoint prevents exact equal-arc-length sampling
  of the closed loop." This is the same unexplained hedge as in section 2, and this time without a pointer to 7.1.
- "Moment of inertia divided by total mass, I/m": "about the axis through the centre, perpendicular to the page" would
  complete the picture.
- In the box, "This is not a search over all 256 DFT bins" uses "DFT bins", which is never defined. The sentence
  before it already says the same thing.
- Exercise 5.1: "by (3) only frequencies with e^{ikπ/2} = i … survive". The step is left to the reader: shift t by a
  quarter loop, and each arrow turns by e^{ikπ/2} while the whole chain must turn by i. That is fair for an exercise, and
  the Figure 1 caption has already used the same argument.
- Figure 4's caption, "whose circles all sit at every fourth frequency", runs ahead of Exercise 5.1 and section 6.1,
  which show it.

## 6 · Corners cost circles ★: **clear**

(A) none for its ★ reader. Integration by parts with the bead's velocity, corners as velocity jumps, the four square
corners closing up like the arrows of (5), and the heart's two cusps adding for even k all derive correctly. They are
matched to the page's radii, and Figure 5 shows the three behaviours.

(B)
- (12): "a second integration by parts of (11) gives". The jump boundary terms, the whole content of (12), are not
  written out. A graduate can supply them.
- "both derivatives of its parametric formula vanish": the heart's formula is never given (x ∝ sin³u,
  y ∝ 13 cos u − 5 cos 2u − 2 cos 3u − cos 4u), so the reader cannot check the cusp. The picture of arriving straight
  down and leaving straight up carries it anyway.
- "a tail Σ_{|k|>K/2} |cₖ|²": for the heart, whose radii sit at even k, K circles reach |k| ≈ K, not K/2. The K⁻³ law
  and the K^{−3/2} conclusion are unaffected.
- 6.2: "shoots past each end of the wave by 5.9 %, 7.9 % and 9.5 % … for a jump the classical limit is about 9 %". The
  numbers are right; I reproduced them. A graduate will notice the overshoot climbing to and past the stated limit
  without comment. Measured from the end of a sloping stroke, the classical partial sums also climb towards 9 % from
  below, which I checked: a pure sawtooth gives 5.1 %, 7.0 % and 8.1 % at 12, 25 and 60 harmonics. "It climbs towards the
  limit as the ringing gets narrower than the wave's own bends" would settle it.

## 7 · What the page computes: **clear**

(A) none. The five steps match the code, eq. (15) is the code's `chainAt()`, and "no integration, no accumulated error"
is the right point. 7.1 names the one numerical artefact and measures it.

(B)
- "Like any jump in the parametrisation, this one-step pause adds radii that fall only as 1/|k|": a reader sees a pause,
  not a jump. The missing picture is that a bead which pauses for one step must run slightly fast everywhere else. It
  falls behind a uniform bead by up to one step Δs and snaps back at the pause, and that snap is the jump that (13)
  prices.

## 8 · From units to pixels: **clear**

(A) none. The equation-to-screen material is complete: units, R, R_view, zoom and pan, and which drawn thing is which.

(B)
- "one unit is 0.46 of the shorter side of the figure" holds while drawing. Once a shape plays, (16) rescales by
  1/max(1, R_view). The next paragraph says so, but the first sentence reads as permanent.
- "Component circles draws each circle": circles under 1.5 px are skipped. "the first twelve numbered by rank": only
  where the arrow is long enough and the label has room. These are code facts the note rounds off.

## 9 · What the model leaves out: **clear**

(A) none.

(B)
- "makes ⟨|z|²⟩ the moment of inertia of a uniform wire": earlier the note says, correctly, I/m, and only approximately.
- Further reading: all four links resolve, but three of them are publisher catalogue pages of paywalled books. Only
  Numerical Recipes is readable online. The chapter numbers given are correct.

---

## Verdicts

| Section | Verdict |
|---|---|
| 1 A drawing made of circles | clear |
| 2 The model | clear |
| 3 Each circle is an average | clear |
| 4 From an integral to 256 samples ★ | clear |
| 5 Parseval's theorem and the error | **needs work**: one (A) |
| 6 Corners cost circles ★ | clear |
| 7 What the page computes | clear |
| 8 From units to pixels | clear |
| 9 What the model leaves out | clear |

The note is in good shape. It has one real obstacle, a structural one: the ★ on section 4 lets a school student skip
the very equations (the discrete series and eq. (5)) on which the unstarred section 5 builds Parseval's theorem. One or
two sentences fix it. Nothing else should be rewritten. The closest B items to the line are the two endpoint hedges in
sections 2 and 5 and the jargon paragraph that opens section 4.

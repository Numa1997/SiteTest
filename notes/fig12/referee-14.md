# Referee report · Fig. 12 note, section 14 "A mug of coffee beside the pint" (`#p-coffee`)

Read as rendered: `npm run build`, `public/` served with `notes/fig12/serve.cjs` (port 8837), opened in headless Chromium at
1280 px and 390 px, every fold opened, section 14 screenshotted top to bottom (5 shots at 1280, 9 at 390). Read as two people:
**S**, a school student who is good at mathematics, and **G**, a physics graduate. Background read: sections 3.5, 4.3–4.5, 5,
8.6, 10.3, 11.8–11.9, and the Sources entries [27]–[29]. plan.md and check.md were not opened.

## What I measured

- **Rendering.** No KaTeX errors in the section, no sideways scroll, no display equation or table wider than its box at either
  width. At 390 px Table 7 fits only by breaking every cell in two ("–" above "(0.9)") and the header "Steps a second" in three
  lines; it reads, but slowly. In the text, the inline code (`node tools/fig12/coffee.cjs 10 5`, `notes/fig12/runs/coffee.txt`)
  is set larger than the Latin Modern around it and breaks the line at 1280 px, in the opening paragraph and again after Table 7.
- **Table 7 is reproduced exactly.** `node tools/fig12/coffee.cjs 10 5` prints every cell of the table as published. The tool
  also prints two things the page does not: the spilled volume of each run (where the 24, 74 and 3 ml of the text come from) and
  the columns 1.25 and 2.25 steps a second (the mug with a clean step already drops at 2.25: "0.7 (8.8; 0)").
- **Numbers recomputed by hand and right:** \(f_{11}\) 3.615/3.652 Hz (mug), 3.421/3.448 Hz (pint); \(R\tan\alpha = 7.50\) mm;
  \(a_\text{rim}\) 2.10, 1.40–2.91, 5.65 m/s²; \(\zeta\) 0.0058 vs 0.0053 (\(\propto R^{-3/4}\)); M&K \(\delta = 0.02 \to \zeta = 0.0032\);
  Han \(0.674/(2\pi\cdot3.8) = 0.028\); \(\zeta_f\) = 0.019–0.037; \(0.0243/0.0053 = 4.6\); frequency ratios 0.28–0.69 and 0.29–0.73;
  \(\tanh\) difference \(3.9\times10^{-5}\).
- **Mayer and Krechetnikov [27] opened** (authors' PDF, the link on the page): the R = 3.5 cm, H = 10 cm cup, eq. (1), "on the
  order of 1 cm", pitch "on the order of 2°", lateral at about half the forward frequency, Faraday not expected, δ ∼ 0.02 in their
  note 20, noise levels |a|/A = 0.1, 0.3, 0.5 in Fig. 7(b), 7–10 steps (4–5 m). All found. Two points where the note's wording
  departs from the paper are listed below (P3, P14).

## Paragraph by paragraph

### Opening paragraph

1. **S.** "the pint is wider, stands 22.5 mm below its rim": the subject is the pint, but it is the stout that stands below the
   rim. Read literally, the glass stands below itself.
2. **S.** The word *freeboard* is used here ("frequency, freeboard, damping…") and is never defined, in this section or anywhere
   earlier in the note (a search of the page finds it only in section 14). Section 13 says "the rim stands 22.5 mm above the stout";
   one clause, "the freeboard, the height of the rim above the liquid at rest", would settle it.
3. **S.** "every number of ours is printed by `node tools/fig12/coffee.cjs 10 5` (and `… 10 10`; …)": a school student does not
   know what the two arguments are. They are the run time (10 s) and the amplitude \(A\) (5 or 10 mm), which only the table caption
   reveals much later. Put the command in a footnote-like closing sentence or say what the arguments are.
4. **S/G.** The fact that the mug **is not on this page** (it was run "in a tool") comes only in the last paragraph of the section.
   A reader who opens the simulation looking for the mug is lost for the whole section. That paragraph belongs in the opening.

### The vessels

5. **S.** "fill levels described by the angle \(\alpha\) by which a steady push tilts the surface up to the rim": a hard sentence,
   and the relation it hides, \(\tan\alpha = \Delta/R\), is never written; the reader has to reverse-engineer it from
   "\(R\tan\alpha = 7.5\) mm". A picture in words (tilt the flat surface about its centre until its high edge touches the rim; that
   angle is \(\alpha\)) and the formula would carry it. \(\Delta\) itself only appears two paragraphs later, in (C2).
6. **G.** For the pint, "with \(R(h) = 39.1\) mm at the surface": the rim of a tulip is not at the surface, and section 4.6 gives
   \(R'(h) = -0.04\), so the wall leans inward above the liquid. Whether (C2) should use the surface radius or the rim radius, and
   that the difference is small, is not said.

### Frequency

7. **S.** \(\xi_{11}\) is used without a reminder of what it is (the first zero of \(J_1'\), 1.8412, section 4.3). A section that
   promises to "take the pieces of the note one by one" should restate the one number it needs.
8. **S.** "(16) applies with \(\tanh \approx 1\)" and then (C1) keeps the \(\tanh\): say why it can be dropped (\(\xi_{11}h/R = 5.3\)
   and 5.9, \(\tanh = 0.99995\)) or drop it.
9. **G.** The capillary factor in (C1) is \(1 + 1/\mathrm{Bo}\) with the Bond number of section 5; that link is not made, so the
   reader meets the same physics twice in two notations.
10. **G, symbol.** \(\sigma\) here is surface tension (as in section 5), but section 11.9, which this section leans on for its runs,
    uses \(\sigma_1^2 = 1.8412\) for a dimensionless frequency. One symbol, two meanings in the same note.
11. **G, misleading juxtaposition.** "3.652 Hz with \(\sigma = 0.072\) N/m (Mayer and Krechetnikov give 3.65 Hz)" reads as if
    their 3.65 Hz includes surface tension and agrees with ours to four figures. It does not: on p. 046117-2 they state that for this
    cup "the surface tension σ effect is negligible" and quote \(\omega_{11} \sim 23\) rad/s, hence about 3.65 Hz. Their figure is a
    rounded \(\omega\), and our no-surface-tension 3.615 Hz agrees with it equally well.
12. **G.** "for the pint 3.421": this is the cylinder of the tulip's surface radius (section 11.8), not the tulip. The 3D solver on
    this page swings at 3.21 Hz on its 4 mm grid (sections 4.6, Example 4.2), about 3.41 Hz grid-corrected. A reader who has just
    seen 3.214 Hz in Example 4.2 meets 3.421 Hz here without a word on which pint is meant.
13. **S.** "a wider vessel is a longer pendulum": a good picture. It needs half a sentence more for S: \(\omega^2 \sim g/R\), as a
    pendulum \(\omega^2 = g/\ell\), so \(R\) plays the length.

### Freeboard

14. **G, source.** "A walker's forward acceleration reaches 0.5–2.4 m/s² as the walk speeds up [27, Fig. 4(a)]". In [27] this
    is \(\ddot x_\text{max}\), the largest acceleration, "realized early on" in the start-up from rest, plotted against the average
    walking speed. "As the walk speeds up" can be read either as "during the start" or "at higher speeds"; it should say which.
    More importantly, **this push is not in the runs of Table 7**: the table drives a steady sine from the first step with peak
    \(A\omega^2\), 0.20 m/s² at 1 Hz to 1.23 m/s² at 2.5 Hz (plus the harmonic). The reader is left comparing the freeboard limit with
    one acceleration and then reading a table driven by another.
15. **S.** "the mug is filled three times closer to spilling": three times in rim height (7.5 against 22.5 mm), 2.7 times in the
    push (2.10 against 5.65 m/s²). Fine as a round figure, but say which.
16. **S.** "(problem 5 of section 16)" sends the reader forward to an exercise for a number just computed in the line above. Either
    show the one-line computation (\(9.81\times22.5/39.1\)) or drop the pointer.
17. **S/G, missing step.** (C2) is a *static* criterion. The section never joins it to the dynamics it describes next: the rise at
    the wall is roughly (gain) × \(R a/g\), and the start from rest adds a free swing. One worked number would make the whole
    section click; for example, the mug at 2.5 steps a second: \(a = A\omega^2 = 1.23\) m/s², quasi-static rise
    \(R a/g = 4.4\) mm, steady gain 1.9, start-up factor up to \(1/(1 - r) = 3.2\), so 8 to 14 mm against a 7.5 mm rim; the table
    has 13.0 mm and a drop. Without such an example the reader cannot see why Table 7 says what it says. (Standard item 4:
    "one small number worked with the page's own parameters".)

### Damping without foam

18. **G.** \(\zeta \propto R^{-3/4}\) is quoted, but \(\zeta\) also goes as \(\nu^{1/2}\) (section 5), and the note uses water at
    room temperature, \(\nu = 1.0\times10^{-6}\) m²/s, for both. Hot coffee (about 70 °C) has roughly 0.4×10⁻⁶ m²/s, which lowers
    the mug's \(\zeta\) by a factor of about 0.6. The assumption should be stated, since the section compares damping.
19. **S.** "[27, ref. 20]" is unreadable for S: it means "their note 20". Say "in a note of [27]".
20. **G, unsupported.** "A real mug, its rough glaze and a hand that is not rigid, may well damp more than a smooth glass": no
    source and no estimate; Han's 0.028 is five times Abramson's, which is either this effect or something else (an amplitude well
    beyond linear, a measurement of a different quantity). Also: is Han's 0.674 s⁻¹ the amplitude decay rate? The conversion
    \(\zeta = \lambda/\omega\) assumes so; say it.
21. **G, consequence missing.** The three damping values span a factor of ten (0.003, 0.006, 0.028), and the head's damping
    (next paragraph) is shown to change Table 7. The reader is not told how the mug's row would change with Han's value, though
    the tool could run it with one flag. As it stands, "we keep Abramson's value" closes a disagreement that matters for the result.

### Damping by the head

22. **S.** "Plateau borders" are defined (good). "Saturates after about five layers" and "cut the swing tenfold under steady
    forcing" are two different measures (decay rate, forced amplitude) in one sentence; S cannot tell which one (C3) uses.
23. **G, missing step in (C3).** \(\zeta_f = 1/(\omega_{11}\tau_f)\) holds if \(\tau_f\) is the e-folding time of the *amplitude*;
    if it is of the energy there is a factor 2. The paragraph does not say which.
24. **G, missing step.** "A cell of width \(w\) has wall area \(2/w\) per volume; a cylinder … \(2/R\). Replacing \(w\) by \(R\)":
    the foam rubs the wall only along the surface, so the natural ratio is wall *perimeter* per *surface area* (also \(2/w\) and
    \(2/R\), so the result survives), and the mass it must slow is the swinging mass, about 85 g of the pint's 427 g (Example 4.2),
    not the whole volume. That the transfer also assumes \(w/\tau_f\) does not depend on frequency or amplitude (Plateau-border
    friction is not linear in speed) is unstated. One sentence listing these assumptions would make "an inference" honest in detail.
25. **G.** "a stout's head is of nitrogen bubbles far smaller": the direction of the effect is not given. Smaller bubbles mean more
    Plateau borders per unit wall, so more friction; saying so would make the 4.6× a lower bound rather than a guess.
26. **S.** "four to seven times the wall's own damping": 0.019/0.0053 = 3.6. "About four" or "3.6 to 7" would match the numbers.

### The drive

27. **S/G, symbol used before it is defined, and with a second meaning.** "gain \(1/(1 - r^2)\)": \(r\) is not defined in this
    section. The reader guesses it is the ratio of step frequency to \(f_{11}\), but throughout section 4 and in section 8.6 \(r\) is
    the radial coordinate. Name it (\(r = f/f_{11}\)) or use another letter.
28. **S, skipped step.** "by (17) the swing follows the push with gain \(1/(1 - r^2)\)": (17) is the equation, not the result.
    The two lines are missing: put \(q = Q\sin\omega t\) into (17), get \(Q(\omega_{11}^2 - \omega^2) = -\beta a_0\), so \(Q\) is the
    steady tilt's \(-\beta a_0/\omega_{11}^2\) times \(1/(1 - r^2)\). And "gain" relative to what: relative to the steady tilt for the
    same push. Also "1.1 to 2.1": at \(r = 0.731\) the gain is 2.15.
29. **S/G, gap between this gain and Table 7.** The gain is at most 2.1, yet the table's rises are several times the quasi-static
    tilt. The reason, the start from rest (the forced swing plus the free swing it launches, up to \(1/(1 - r)\)), is the very effect
    Mayer and Krechetnikov call decisive, and it is not worked out. See item 17.
30. **S, skipped step.** "\(a_x = A\omega^2[\sin\omega t + 4e_2\sin 2\omega t]\), the second harmonic a share \(e_2\) of the
    displacement": the reader must supply that the displacement is \(-A[\sin\omega t + e_2\sin 2\omega t]\) and that differentiating
    twice brings \((2\omega)^2 = 4\omega^2\). Also \(A\) is used here and in the caption but never introduced in the prose as the
    amplitude of the hand's forward motion.
31. **S/G, unexplained choice.** "forward oscillations 'on the order of 1 cm'" and then \(A = 5\) mm in the table, \(A = 10\) mm
    in the side remark. Is 1 cm the peak-to-peak (so \(A = 5\) mm) or the amplitude (so \(A = 10\) mm)? The tool's own header comment
    takes \(A = 10\) mm as the default for "on the order of 1 cm". The reader cannot tell which run is the realistic one.
32. **S, physical picture missing.** Why does a walking hand have a second harmonic at all? Nothing is said: two heel strikes
    per stride, the body's rise and fall twice per stride, the arm's swing. The whole result of the section ("the harmonic matters
    more than the fundamental") rests on it, and it has no picture.
33. **G.** "\(e_2 = 0.3\), Mayer and Krechetnikov's middle noise level": in [27] the noise is a sum of sines at random frequencies
    and phases with Euclidean amplitude \(|a| = 0.1, 0.3, 0.5\) of \(A\) (their eq. (4), Fig. 7(b)). Using 0.3 as the size of one
    coherent harmonic placed exactly at \(2f\) is a much harsher drive than their noise of the same norm. The note says "standing in
    for", but not that it puts all of the noise's energy on one resonant line.
34. **S.** "(section 11.9; for the mug its cylinder is the case the model is derived for)": a parenthesis inside a parenthesis,
    hard to parse. The point (the live model replaces the tulip by a cylinder, and the mug *is* a cylinder) deserves its own sentence.

### Table 7

35. **S, undefined.** "steps before the first drop": what is a drop? In the tool it is the first 10⁻⁹ m³ (1 µl) over the rim; on
    the page it is not defined, and section 10.3 defines spilling only for the 3D solver's particles, not for the modal live model.
    "0.7" also needs a word: 0.7 of a step, i.e. 0.7/f seconds.
36. **S, numbers in the text not in the table.** "the pint 24 ml, the mug 74 ml", "from 24 to 3 ml": the table has no spilled
    volumes. The reader looks for them and cannot find them. Add "; ml" to each cell, as the tool prints it, or a row.
37. **G, cells beyond the model's validity, not flagged.** Section 11.9 says a crest breaks at \(R/\xi_{11}\) at the wall (21.2 mm
    for the pint, 19.0 mm for the mug's 35 mm) and that the model's numbers beyond it "are the model's, not the stout's", with a
    clip at 1.5 times that. Table 7 has rises of 34.5 (mug), 34.4 (pint), 29.9 (pint with head), 23.2 mm; the mug's 34.5 and the
    pint's 34.4 exceed even the clip (28.5 and 31.8 mm). The spill volumes 74, 24 and 3 ml, and the conclusion "cuts it from 24 to 3
    ml", come from exactly those runs. The section should say so, as section 8.6 does for its 103 mm lean.
38. **G.** Does the modal model lower the fill when liquid leaves? If not, the mug loses 74 ml (a fifth of its 385 ml) and keeps
    the same 7.5 mm of freeboard. Not said.
39. **S, contradiction with the table.** "The mug spills where the pint does not, at a brisk 2.5 steps a second even with a clean
    step, and at 1.5 steps a second and above with the harmonic." With the harmonic the pint also drops at 1.5 (after 2.1 steps)
    and at 1.75 (24 ml). What the table shows is that the pint stops spilling at 2.0 and 2.5 while the mug does not. Also, the tool's
    2.25 column shows the mug already dropping at 2.25 with a clean step; "at a brisk 2.5" understates it.
40. **G, "on both resonances".** \(2\times1.75 = 3.5\) Hz is 2.3 % above the pint's 3.421 Hz and 3.2 % below the mug's 3.615 Hz,
    while the resonance half-width is \(\zeta\), about 0.5 %. So 3.5 Hz is four to six half-widths off both. What makes it count is
    the start from rest (a transient is broad) and, for the mug, the softening of section 11.9, which lowers its frequency toward
    3.5 Hz as the swing grows (and moves the pint's away). That is the physics behind the mug's 34.5 mm against the pint's
    34.4 mm at a fill three times higher, and it is not said.
41. **G.** "With 10 mm both vessels spill at most step rates (`notes/fig12/runs/coffee.txt`)": a claim the reader can only check
    in a file in the repository. A sentence with two numbers, or a sixth row, would do.

### Channels and actuators

42. **S/G, one symbol, two meanings in one paragraph.** "a pitch \(\theta\) tilts gravity … by \(g\theta\)" and, three lines later,
    "the second mode in \(\sin\theta\)", where \(\theta\) is the azimuth. Both in the same paragraph.
43. **S/G.** "the second mode in \(\sin\theta\)": in this note "second mode" means \(n = 2\) (5.821 Hz, section 11.8). The swing
    across is the same (1,1) mode turned through 90°, its degenerate partner (\(s_1\) of section 11.9). Say "the same swing, turned
    across the walk".
44. **G, missing size.** A pitch of 2° gives \(g\theta = 9.81\times0.035 = 0.34\) m/s², comparable to the forward drive of
    Table 7 (0.20–1.23 m/s² at the fundamental). Yet pitch is not in the runs. Either it is small after all (phase, frequency) and
    one line should say why, or Table 7 leaves out a channel of the same size as the one it includes. The rotation of the cup also
    brings an angular-acceleration term besides \(g\theta\); not mentioned.
45. **S.** "Mayer and Krechetnikov rate it minor, its frequency being half the forward one": why half the frequency makes it
    minor needs the clause [27] gives: further from the swing's own frequency (\(r \approx 0.15\)–0.35, gain about 1). Note also that
    [27] gives the lateral amplitude as about 20 mm, the same order as the forward motion; the section does not mention its size.
46. **G, over-reading the source.** "Watching the cup … is the sensor; their focused walkers spilled later [27, §III]": [27]
    attribute the later spills of focused walkers "in part" to a lower maximum acceleration and a lower noise level, not to visual
    feedback. The sentence turns a correlation into a control loop the paper does not claim.
47. **S/G, tension with section 8.6.** Section 8.6 opens with the same walk: "your knees bend so the cup does not drop with
    your body" (the hand for the push along, the knees for the jolt from below). Here the walker "needs two actuators, forward and
    sideways", and the vertical is dismissed. Both may be right (the cart needs the vertical because of the road at the body's
    resonance; the walker's bob is at the step frequency), but a reader who remembers 8.6 needs that one sentence.
48. **S.** "the cheapest controller for coffee is more room above it": a good closing line; keep it.

### Last paragraph

49. **S/G.** Already noted (item 4): it should open the section. And "its five-mode coefficients … differ … only through
    \(\tanh(\xi_{11}h/R)\)" is a claim about \(d_1, d_2\) and the second-order modes that is not shown; for a deep vessel it is
    plausible, but the reader is given no reason.

## Against notes/STANDARD.md

| Item | Verdict | Why |
|---|---|---|
| 1 · Physical picture | **needs work** | The opening (the walk with a full mug) is good. Missing: why a walking hand has a second harmonic (item 32), a picture for \(\alpha\) (item 5), what "freeboard" is (item 2). No figure; a sketch of mug and pint side by side with their freeboards would carry the main result. |
| 2 · Model stated | **needs work** | Assumptions are scattered and some unstated: water's \(\nu\) and \(\rho\) for hot coffee (18), the steady sine from the first step instead of the start-up push (14), one coherent harmonic for random noise (33), pitch left out (44), the mug run through the pint's live model off-page (4). \(A = 5\) mm against "1 cm" unexplained (31). |
| 3 · Derivation | **needs work** | (C2) is derived; (C1) is quoted (fine, it is (16) plus section 5). The gain \(1/(1 - r^2)\) is asserted "by (17)" without the two lines (28), \(r\) undefined (27), the factor 4 in \(a_x\) unexplained (30), (C3) misses the amplitude/energy and swinging-mass steps (23, 24). |
| 4 · Checks | **needs work** | Recomputed numbers are right. But no worked example joins (C2), the gain and the start-up to a cell of Table 7 (17, 29); "on both resonances" does not survive the bandwidth check (40); the text contradicts the table once (39). |
| 5 · Numerical method | **needs work** | The tool and its arguments are cited and reproduce the table exactly. Undefined: what a "drop" is (1 µl), how the modal model counts spilled volume, whether the fill drops (35, 38). The spill volumes quoted in the text are not in the table (36). |
| 6 · Equation to screen | **clear** for what applies | The mug is not on the screen and the section says so; it should say so at the start (4). |
| 7 · Limits | **needs work** | Good: "an inference, not a measurement", "the step counts are the model's". Missing: the largest rises and all spill volumes lie past the model's own breaking limit of section 11.9 (37); the damping disagreement is not carried to the result (21). |
| 8 · Further reading | **clear** | [27]–[29] are real, linked, with sections named; [29] honestly says "figures not seen". Two wordings stretch [27] (11, 46). |
| Form (21 October verdict) | **needs work** | No "Key result" box (the freeboard rule (C2) and "the harmonic, not the fundamental, spills the coffee" are the two candidates) and no numbered worked example with the page's numbers. Sentences carry nested parentheses (34) and code paths in running prose (3). Symbols: \(r\), \(\theta\), \(\sigma\) each with two meanings in the note (10, 27, 42). |

**Overall: needs work.** The numbers are right and reproducible, and the comparison is a good idea well placed after the
parameter study. What a first-time reader lacks is the one worked line that turns (C2), the gain and the start from rest into
a cell of Table 7, three undefined or doubly defined symbols (\(r\), \(\theta\), freeboard), the spill volumes in the table, and a
plain warning that the big rises and the millilitres lie beyond the model's breaking limit.

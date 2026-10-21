# Fig. 5 · water-wave.html · plan

Judged against notes/STANDARD.md (section 4, overridden by "Numa's verdicts": judge first, change only real gaps, smallest
change, no overloading). The note already has 10 sections and 23 equations; restraint is the rule here.

Checks behind the verdicts:
- `derive.py` (SymPy): every derivation step (4)–(21), the trochoid crest fraction and mean level, the group velocity, and every
  closed-form number of the note (table, storm times, radii, diver, exercises, Stokes, limits). All agree.
- `fig4_rk4.py`: Figure 4 and Section 07 numbers (loop 1.0432 T, advance 11.24 cm, drift 0.0835 m/s = +3.59 %; +0.93 % at
  ak = 0.1, +0.24 % at ak = 0.05; 5.39 vs 5.38 mm/s at z0 = −0.56 m; step halving changes positions by 6e-14 m). All agree.
- `measure.cjs` (headless Chromium, 1440 × 900 and 390 × 844, output `measure-before.json`): f = 0.7749 Hz, k = 2.4166 rad/m,
  c = 2.0148 m/s, T = 1.2905 s, ak = 0.5800, U_S = 0.678 m/s, radii 24 / 6.20 / 1.60 / 0.414 / 0.107 px, readouts of both
  exercises and of the cap case, followed column X0 = 378.24 / 190 px, 90 parcels, 307 / 174 surface points. All agree.

## Verdicts

| § | Section | Verdict |
|---|---|---|
| — | Abstract | clear, leave it |
| 01 | A gull on the swell | clear, leave it |
| 02 | The model | **needs work**: the paragraph "The circles drawn on the page are the leading-order particle paths …" (second `<p>` on line 141) comes before λ, a, k are defined (line 142) and uses \(a e^{kz_0}\), \(ak\approx0.58\) and "irrotational", "Airy" before any of them is introduced; \(z_0\) is never defined in the section at all. Symbols used before they are defined. |
| 03 | Potential flow | clear, leave it |
| 04 | Conditions at the edges ★ | clear, leave it (each linearisation step names its size; the Bernoulli drop says "of order (aω)²", quadratic against linear terms, which is enough for a ★ reader) |
| 05 | Gravity sets the pace | **needs work**: (15) \(c_g = \mathrm{d}\omega/\mathrm{d}k\) is asserted: "The group … moves at the group velocity" with no reason why a group moves at dω/dk. A bare formula, and the storm arrival times rest on it. Everything else (5.1, 5.2, the picture, table, Figure 2, Exercise 5.1) is clear. |
| 06 | Every parcel runs in a circle | clear, leave it |
| 07 | Stokes drift ★ | clear, leave it (all numbers reproduced) |
| 08 | Computing the picture | **needs work**: "At the defaults that is 90 parcels, plus 307 points along the surface … Each of these numbers is written into the page’s data store" reads as if the surface points were stored. They are not (code lines 689–716; Section 09 says so). A claim that contradicts the code and Section 09. |
| 09 | From metres to pixels | clear, leave it |
| 10 | What the model leaves out | clear, leave it, except the further reading |
| 10.1 | Further reading | **needs work**: none of the four items has a link. Feynman’s section 51-4 is titled "Surface waves", not "water waves". |

## Planned changes (only these)

1. **§02.** Move the paragraph from line 141 to after Figure 1 (start of line 245, before "There are two unknowns"), where
   λ, a, k, ak ≪ 1, irrotational and Airy are all defined and Figure 1 shows \(z_0\) and \(r = a e^{kz_0}\). Add the definition of
   \(z_0\) (the height at which the parcel rests in calm water, negative below the surface), say \(ak = 0.58\) as measured,
   and point to Section 6.2 for Gerstner. Light rewording in the note’s plain voice. Two paragraphs share line 245 as they shared
   line 141, so the file keeps its line count and every line link in the doc stays valid.
   Number: ak = 0.5800 (store `ak`, measured).
2. **§05.** One sentence before (15), in the same paragraph (line 303): two waves of equal height with wave numbers \(k \pm \delta k\)
   and frequencies \(\omega \pm \delta\omega\) add to \(2a\cos(\delta k\,x - \delta\omega\,t)\cos(kx - \omega t)\); crests run at
   \(\omega/k\), the envelope at \(\delta\omega/\delta k\), which becomes dω/dk. Inline maths, no new display equation, no renumbering.
   Identity checked in `derive.py`.
3. **§08.** Reorder the sentence on line 516: the parcels’ numbers are stored; the 307 / 174 surface points are only drawn
   (Section 09). Numbers 90, 307, 174 measured (`measure-before.json`).
4. **§10.1.** Add a link to each reference, to a page I opened:
   - Feynman Vol. I ch. 51 (online edition, feynmanlectures.caltech.edu/I_51.html; section 51-4 "Surface waves": circles that
     shrink with depth, \(v = \sqrt{g\lambda/2\pi}\), group speed half the phase speed, ripples). Fix the section title.
   - Acheson, OUP product page (contents: 3 Waves) and the chapter page on Oxford Academic (abstract: a group of waves on a
     pond, each crest running through the group).
   - Kundu, Cohen, Dowling 6th ed., ScienceDirect chapter 8 "Gravity Waves", pp. 349–407 (abstract: linearisation for small
     slope, deep-water dispersion, phase and group speeds, surface tension, nonlinear waves).
   - Landau and Lifshitz 2nd ed., ScienceDirect book page (Chapter I Ideal fluids pp. 1–43; Chapter II Viscous fluids
     pp. 44–94; description lists damping of gravity waves).

## Not changed, noted

- Stored `cg` is `c / 2` also with dispersion off (code line 663), where it is not the deep-water group speed of that λ; the
  note already says \(c_g = c/2\) "no longer applies" then. Reported, code untouched.
- Doc: only the line-141 / 245 move and the reference links touch it; the doc describes neither in detail. Re-check its
  section table and line counts after editing.

## Result (20 October 2026)

Done as planned, nothing else touched. Diff of water-wave.html: lines 141, 245, 303, 516, 545–548 only; lines 1–106 and
553–891 byte-identical to HEAD; still 891 lines, so the doc's line links and the walkthrough stay valid. Measured after the edit
(`measure-after.json`, headless Chromium, 1440 × 900 and 390 × 844): 0 console errors, 0 `.katex-error`, 0 px sideways scroll,
all 20 folds of note and walkthrough open by their own toggle, tags (1)–(23) unchanged, every stored number identical to
`measure-before.json`, 5 reference links. Doc: page size 161 372 → 162 709 bytes, one dated log entry.

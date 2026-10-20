# Fig. 4 · Transverse and longitudinal waves · plan

Judged against notes/STANDARD.md, Numa's verdicts first: a clear section is not touched; where there is a real gap, the
smallest change, inside existing lines of the note (the page keeps its 1086 lines, so every page:N link in the doc and the
walkthrough stays valid). No new section, figure, box or display equation. Numbers: notes/fig04/measure.cjs (the page's own
formulas in Node, then the built page in headless Chromium with reduced motion, so the store holds the frame at ωt = 0) and
notes/fig04/derive.py (SymPy). Results in notes/fig04/measure-out.json.

| § | Section | Verdict |
|---|---|---|
| — | Head, abstract, contents | clear, leave it |
| 1 | The pattern travels, the medium stays | clear, leave it (stadium, slinky, guitar, air, P/S waves and the liquid core: correct and vivid) |
| 2 | The model | needs work: line 137, "The default longitudinal value \(A_{\rm L}k\approx0.743\)" uses \(A_{\rm L}\) three sections before it is defined (eq. 12), and "the coordinate map" names a thing the text calls \(x = X + \xi\). Everything else (eq. 1, the list, the defaults 25.6 px, particle 12 at 307.2 px, Figure 1) is clear and checked |
| 3 | One formula, two pictures | needs work: Exercise 3.1 ends "neither the period nor the top speed of any single particle". False for the lower row: at λ = 110 px the cap gives \(A_{\rm L}\) = 14.0 px, so its top speed falls from 163.4 to 88.0 px/s (measured; readout "14 px (cap)"). Rest of the section clear |
| 4 | Where the wave equation comes from ★ | needs work, three items: (a) 4.2 "for such adiabatic changes \(B = \gamma p\)" is asserted, the one line from \(pV^\gamma\) = const is missing; (b) the computation note says 28.97 g/mol gives 1.2041 kg/m³, but it gives 1.2043 (1.2041 needs 28.965 g/mol); (c) 4.3, eq. (8): \(K + \tfrac43G\) is a bare formula, the step from "cannot bulge" to \(\tfrac43G\) is missing. 4.1 and 4.4 clear (the small-angle sine-to-slope step in 4.1 is standard and stated as "small angle"; left) |
| 5 | Compressions and rarefactions | needs work, two items: (a) "the denser half of the particles fills only \(1/2 - A_{\rm L}k/\pi\) = 26 %" is asserted with no step; (b) Exercise 5.1, "In the lower row the bars nearly touch at the compressions": with 26 particles at λ = 100 px the closest pair never comes nearer than 7.26 px, no closer than at the defaults (7.01 px). With 40 particles it is 3.86 px against a rest spacing of 16.41 px. Everything else (10)–(12), 3.88, 0.574, 7.0 and 44.1 px, Figures 3 and 4, clear and checked |
| 6 | Energy carried ★ | needs work: eq. (13), "potential energy from being stretched by its tilt" gives \(\tfrac12F(\partial\xi/\partial X)^2\) with no step (length \(\sqrt{1+s^2}\approx 1+\tfrac12 s^2\), times F). The product-rule step to (14) is named precisely and checked with SymPy; left |
| 7 | How the page computes a frame | clear, leave it (Δt cap 0.05 s and reduced-motion start confirmed in sim.js L176–178 and in Chromium; 0.63 rad) |
| 8 | From medium pixels to screen pixels | needs work: "A thin burgundy curve runs through 214 points of (1)": the code draws 215 (X = 0, 3, …, 639 and a last point at 640; counted in the live frame). Canvas sizes 770 × 481 and 356 × 374, s = 1.134375 and 0.4875, 65 gradient stops: confirmed |
| 9 | What the model leaves out, 9.1 Further reading | limits clear (36.6°, 2.2 % confirmed). Further reading needs work: none of the three items has a link. Links to pages opened: Pearson (TOC: ch. 15 Mechanical Waves, 16 Sound and Hearing), CRC Press/Routledge (TOC: ch. 7 Progressive Waves) and the Internet Archive lending copy of the 1971 Norton edition, Wiley (TOC: ch. 2 Basic Seismological Theory, 3 Seismology and Earth Structure; "beginning with waves on a string" confirmed by the Physics Today review). Add one free source, read whole: Feynman Lectures Vol. I ch. 47, which derives the sound wave equation and Laplace's γ, the step added in 4.2 |

## Planned changes, smallest first

1. § 2, line 137: define \(A_{\rm L}\) where it first appears (equal to \(A\) at the defaults; rule in Section 5), say in words what 0.743 means (neighbours close to about a quarter of their rest spacing: 1 − 0.7426 = 0.257), and write "the map \(x = X + \xi\)" for "the coordinate map".
2. § 3, Exercise 3.1: "of any particle in the upper row", plus one sentence: at 110 px the cap lowers the lower row's amplitude to 14 px, as the readout shows.
3. § 4.2: one clause, \(pV^\gamma\) fixed ⇒ \(\mathrm{d}p = -\gamma p\,\mathrm{d}V/V\) ⇒ \(B = \gamma p\).
4. § 4.2 note: 1.2041 → 1.2043 kg/m³ (343.2 m/s unchanged).
5. § 4.3: two sentences after eq. (8): split the strain into an equal strain ε/3 in all directions (volume, stress Kε) and the rest (2ε/3 along, −ε/3 across: shape, stress 2G · 2ε/3).
6. § 5: one sentence: at rest the denser half spans λ/2; its rear end is pushed forward by \(A_{\rm L}\), its front end pulled back by \(A_{\rm L}\).
7. § 5, Exercise 5.1: "the bars crowd at the compressions but never cross; with Particles at 40 the closest two come within 3.9 px, against a rest spacing of 16.4 px".
8. § 6: one clause for the tilt energy.
9. § 8: 214 → 215 points, the last at X = 640.
10. § 9.1: links on the three items; add Feynman Vol. I ch. 47 on the same source line as item 3, so no page line moves.

Doc docs/simulations/fig04-transverse-longitudinal.md: page bytes and long-line count (line 5), the further-reading row of the
section table, the re-test hint "bars nearly touching", the defaults sentence (Exercise 5.1 now also sets Particles to 40),
and a dated revision entry. Line links stay valid because no page line moves.

Report-only: tl.js:85 puts a ⟦comp|…⟧ mark inside `note`; draw() runs every frame while paused (doc note 6).

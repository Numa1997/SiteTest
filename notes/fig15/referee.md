# Fig. 15 · referee report, round 6 (resonant tunnelling)

Read as rendered, at commit `a20d017` (branch `claude/fig15-gen2-note`). `npm run build` (exit 0); `dist/` served on port 9617;
opened in headless Chromium (Playwright) at 1400 px and 390 px; "Expand all" pressed, every fold forced open, sticky and fixed
elements made static, and each of the 14 sections screenshotted at both widths, plus the header and abstract. KaTeX: 0
`.katex-error`, 0 raw `\(`, `\[` or `$$`; no console or page errors; no section wider than its box. The 3D panels are blank locally
(run files on the remote store) and the GitHub `main` links may 404 until merge; both expected and not marked. plan.md and
check.md were not read.

Spot checks recomputed: T = 0.1439, R = 0.8561; −2 ln R = 0.3109 and 2T/√R = 0.3112 (note: 0.3108, 0.3111, rounding), naive 2T
= 0.2879; L_eff = 2.757, (17) = 0.0633; σ_E = 0.202, (19) = 0.218; σ⊥(40) = 7.31, σ⊥(12) = 3.61; 0.59 rad per step for the
diagonal mode; θ = 2ρ + 2ks = −6.06 + 6.06 = 0 (so n = 0); (21) = 0.649; the area πΓ/2 and the prefactor √(π/8); the supply
prefactor of (30)–(31); a = 2.75 nm, 110 meV, 10.6 meV, 62 fs, 87 K; supplies 14.2 and 18, products 1.04 and 0.74; run counts
(sum 3739; each a multiple of 47 or the stated product); τ_side = 2.29 for R = 2; Figure 3 measured against its own scale
(E_F, level 0.335, collector fill 0.2, drop 0.8: drawn to scale). All agree with the note.

Two readers. **S** is a school student who is good at mathematics. **G** is a physics graduate. Each mark gives the section,
the exact sentence as rendered (maths in TeX), who gets lost, and why.

## Marks

### Whole note (seen in the rendering)

1. **Typesetting.** Every body paragraph of the note is set in IBM Plex Sans (113 paragraphs measured), not Latin Modern. Only
   the abstract, the figure captions and the equations are in Latin Modern. The Fig. 14 page next door sets its 106 body
   paragraphs in Latin Modern. Cause, as rendered: the Fig. 15 article has a `paper__head` but no `paper__grid` / `paper__body`
   wrapper (so it also has no table of contents), and `paper.css` applies `var(--tex)` to `.paper__body`. Against STANDARD.md
   ("Latin Modern in notes") and CLAUDE.md ("lecture notes set like a LaTeX document"). G and S both read a web page, not a
   chapter.
2. **Work log inside a textbook.** In many places the note reports the state of a batch job instead of physics: "computed so far
   (of 15 planned for this structure)", "are due to be rerun", "the one at the very peak is not yet filed" (§6); "1237 of them,
   from the first 2 parts, are filed so far, after 5.9 hours on the clock" (§10); "to come" in nine cells of the disc table, "the
   larger radii, still to come, will show the trend" (§12); "runs so far", "the lowest energy filed so far" (§12); "So far 170 of
   the 500 runs for two walls are filed … We quote them when all 500 are in." (§13); "Check your answers against the table when
   those runs are in." (Problems). A Taylor chapter does not say this; S cannot tell which results are physics and which are
   provisional. The note is true at every stage of the batch, which is honest, but the reader pays for it.
3. **One symbol, several meanings** (the 21 October verdict: "one symbol one meaning"). \(t\) is an amplitude (§3–9) and a time
   (§2, §5 "(now a time again)", §10); \(T\) is a transmission and a temperature (§13 "in \(k_BT\) only, \(T\) is the
   temperature"), and \(T\) is redefined as a flux ratio in §13; \(R\) is a reflection coefficient and a disc or shell radius
   (§12 "in this section \(R\) is a radius"; the same section's Problem mixes them with (27)); \(n\) labels the first resonance
   as \(n=0\) in (14) and as \(n=1\) in (21) (mark 13). Each is flagged in the text, which shows the authors know; G accepts
   flags, S loses track.

### §1 Two panes of glass

4. "The figure above lets you watch it. The sheet is the plane through the flight axis, lifted at each point by the wave there;
   …" and then, one paragraph later, "In Fig. 15 the sheet is the plane through the flight axis, seen in perspective; drag to turn
   it." The same sentence twice; the first of the two paragraphs already lists the four charts, the second ("Reading the
   figures", about 330 words) lists them again in detail. S: a wall of controls and colour keys before a single idea of the
   physics has been built; "one-dimensional twin", "absorbing border", "fitted exponential decay of the wave trapped between the
   barriers" and "spread of energies a packet holds" all arrive here with only forward pointers.
5. "This is a Fabry–Pérot interferometer, the principle of a laser's mirrors." G: true for a laser cavity, but two panes pressed
   together with an air film are a thin-film (Newton's-rings-type) interferometer; "Fabry–Pérot" needs the two reflecting
   surfaces and the many bounces, which the silvering sentence supplies. Half a clause ("silvered, the pair is a Fabry–Pérot
   interferometer") would keep it exact.

### §2 The model in three dimensions

6. "centred at \(x_0\), 14 before the first barrier face (for longer packets \(4\sigma_x\), 48 for the long one of section 6)".
   S: "longer packets" (plural) when the page has only one long packet; and \(4\sigma_x\) for \(\sigma_x=3\) would be 12, not
   14, so the reader cannot tell which rule applies to which packet. Say "the short packet starts 14 before the face, the long
   one 48 (four of its widths)".
7. "the second equation of (2) has the solution \(g\propto(1+it/2\sigma_\perp^2)^{-1/2}\exp[\dots]\) (substitute it to check)."
   A bare formula: "substitute it to check" is "it can be shown" in other words. S cannot do the check (a complex Gaussian, two
   derivatives) and is not told where it comes from. One sentence (each sideways Fourier component turns by
   \(e^{-ik_y^2t/2}\); transforming back gives this) or a ★ with the two lines would do.
8. "Since the equation has only one solution for a given start, it stays a product for all time". Clear now (the uniqueness step
   is stated). No mark beyond noting the long parenthesis before it ("(the standard deviations of \(|\psi|^2\); both \(3\,a\) for
   the figure's usual short packet; section 6 adds a long one), which is such a product") splits subject and verb: S loses the
   sentence. Two sentences.

### §3 One barrier

9. "(Here \(t\) is an amplitude, not a time; which is meant is always clear from the context.)" See mark 3; the claim is
   contradicted two sections later by "(now a time again)".
10. ★ "The same matrix must link the conjugated pairs, which forces the second row to be the first row conjugated and swapped."
    G: one line is skipped (writing \(B^*=M_{11}D^*+M_{12}C^*\) next to \(A=M_{11}C+M_{12}D\) and comparing, which needs the same
    real \(k\) on both outer sides). Starred, so acceptable; noted only.
11. "and in the same way \(\gamma=i\tfrac{\kappa^2+k^2}{2k\kappa}\sinh\kappa d\) (both checked against the numerical product)."
    G: "in the same way" hides the off-diagonal product, and the phase convention for \(\gamma\) (why no \(e^{ikd}\) factor,
    unlike \(w\)) is not explained. Starred; minor.

### §4 Two barriers, two ways

12. "This agrees with the matrix product to one part in \(10^{9}\) (notes/fig15/derive.py)." A repository path in the middle of
    a textbook sentence; S does not know what to do with it. Move to the source line at the end (which already names it).

### §5 The sharp peak and the trapped wave

13. "(taken between \(-\pi\) and \(\pi\), \(\rho=-3.03\) and this resonance has \(n=0\)); … this first resonance is the one at
    which about half a wavelength fits in the effective width of the well". Then §7, (21): "a whole number \(n\) of
    half-wavelengths fits in \(L_{\text{eff}}\)", with \(n=1\) for the same resonance. S meets the same resonance as \(n=0\) and
    \(n=1\) two sections apart. Either say in §5 that \(r\approx-1\) already carries a phase of about \(-\pi\) per reflection, so
    the "one half-wavelength" resonance is counted as \(n=0\) here and \(n=1\) in (21), or use a different letter in (21).
14. "\(T_2=\dfrac{1}{1+\dfrac{4R}{T^{2}}\sin^{2}\dfrac{\theta}{2}}\)" (13). \(T_2\) is new: §4 wrote \(|t_2|^2\). One clause
    ("\(T_2\equiv|t_2|^2\), the pair's transmission") where it first appears.
15. "Like every slow leak, the trapped wave loses a fixed fraction per unit time." Placed after (16) and before (17), where it
    interrupts the step to (17). It belongs before "falls as \(R^{2t/t_{\text{rt}}}=e^{-t/\tau}\)", as the reason for the
    exponential.
16. ★ "A very wide gap★. … For the running example it is \(0.144/1.856=0.078\), about half of one barrier." This starred passage
    has no "(End of ★)" and its result is not restated unstarred, against the note's own promise in §1 ("their results are stated
    again in plain words just after") and the 21 October rule 4. S, who skips it, never learns that a very wide well loses the
    interference and passes about \(T/2\).

### §6 A wave packet is not a single energy

17. "\(\bar T=\int|\varphi(k)|^2\,T_2(k)\,dk\)" (18), then (19) uses an energy distribution of height
    \(1/(\sqrt{2\pi}\,\sigma_E)\). S: the change of variable from \(k\) to \(E\) (\(dE=k\,dk\), so a Gaussian of width
    \(\sigma_k\) in \(k\) becomes one of width \(k_0\sigma_k\) in \(E\)) is silent. Half a sentence.
18. "these runs stopped with 0.0286 still trapped, half of which would still have passed, because they were made under an
    earlier rule for the run length and are due to be rerun." Two problems. "half of which would still have passed" is
    unsupported here (the reason, "a symmetric pair leaks equally both ways", comes only at the end of §11). And the clause
    "because they were made under an earlier rule … due to be rerun" is project history (mark 2).
19. The "Long packets" paragraph (about 330 words) mixes three structures, two energies off the peak (0.713, 0.7215), two peak
    energies (0.735, 0.744), measured shares, exact averages, a run length, a trapped remainder and a grid shift. S cannot
    follow which number compares with which. G: the clean result is one line ("a packet narrower in energy than \(\Gamma\)
    passes most of the peak; the long packet's 0.54 against the short packet's 0.196 shows it"); the run-by-run detail belongs to
    §11.
20. "Equation (19) agrees with the exact average at the peak itself, \(E_r=0.744\): for \(d=2\) it gives 0.0359". G notices that
    0.744 is also the finite-well level of the table in §7: the thick-barrier resonance has moved onto the bound level, which is
    exactly the §7 claim ("the resonance is the well's level, made leaky"). The note does not say so; one clause would turn a
    coincidence into a check.

### §7 A wider well sings lower

21. "Each well alone has its level near 0.735" is in §9, but the root is here: the table gives the finite-well level 0.744 and
    the resonance 0.735. Fine as is; see mark 26.
22. "The 3D run of two walls \(3.5\) apart at \(E=0.35\), whose packet holds the first resonance, measures a lifetime of 65.2,
    against the exact \(\hbar/\Gamma=58.3\): 12 % longer, … we have not traced why it is larger here." G: an unexplained 12 %
    error in an "exact check" is left open in the text. Either trace it (the run is at 0.35 while the resonance is at 0.388, so
    the fit window sees the packet's off-resonance tail differently; or the grid error grows as \(\Gamma\) shrinks, which §11's
    narrowing argument predicts) or move it to §11 as a measured limit.

### §8 Taller and thicker barriers

23. "a straight line through the logarithm of its decay from \(t=91\), where the trapped probability has fallen to 60 % of its
    peak (the rule of section 11), to the end gives 210, a lower bound rather than a measurement of \(\tau\)". S: the fit rule is
    used three sections before it is stated. G: "lower bound" is argued only qualitatively ("a fit that sees only that stretch
    reads short"); the exact 344 is not quoted in the same sentence, so the reader must scroll up to see how far short 210 is.

### §9 Three, five and ten barriers

24. "Everything about a row of identical barriers turns out to depend on one number, \(\xi\)". Overclaim: (23) depends on \(\xi\)
    and on \(R/T\). Say "where the row passes and where it blocks depends on one number".
25. "the pair's resonance 0.735 sits where \(\xi=0\)". G sees it from (23) with \(U_1=2\xi\); S does not. Half a sentence
    ("for \(N=2\), \(U_1=2\xi\), so \(T_2=1\) exactly where \(\xi=0\)").
26. "Each well alone has its level near 0.735." A well "alone" (between two infinitely thick barriers) has its level at 0.744 by
    the §7 table; 0.735 is the resonance of the pair. Minor, but G notices the mismatch with §7.
27. "a possible cause, not tested, is that ten barriers repeat the small error of each barrier's shape on the grid (section 11)
    ten times." Third untested speculation in the note (with §7 and §11). G: a textbook either measures this or states it as an
    open limit once, in §11.

### §10 What was computed, and how

28. "(the fastest the grid holds, along a diagonal, turns by 0.59 rad per step)". S and G: why this number matters is not said.
    It is correct (\(3(2\pi)^2\cdot0.01/2=0.592\)), but the reader needs the point: the kinetic step is exact at any size, and
    0.59 rad < π means the splitting error stays small even for the sharpest feature the grid holds.
29. "we have not measured the time-step error on its own." Against STANDARD item 5 ("the error the reader should expect,
    measured by running the page"). G: one run of the 1D twin at \(\Delta t=0.005\) would settle it.
30. "each step it multiplies the wave by a factor that falls smoothly from 1 to 0". G: the profile (cos², polynomial, its
    width in grid points) is not given, and nothing says how much it reflects back, the usual failure of such borders.
31. "each barrier alone (376)". S cannot check this count against "the number of structures times 47": which eight single
    barriers? The other groups name their structures; this one does not.

### §11 How good the grid is

32. "(gen1_profile_check.py)". House jargon ("gen1") and a bare script name inside a sentence; see mark 12.
33. "measured against each frame's own, shrinking peak the difference is up to 5.8 % during the collision and reaches 66 % late
    in the run, when little is left." G: 66 % is alarming and left without a word on what it means for the picture (the late
    frames, drawn on one scale for the run, show almost nothing, so the error is invisible). Say so.
34. "A possible cause, which we have not tested: each barrier is only two grid points thick, …". As mark 27. G: a 1D twin at
    twice the resolution would test it in seconds; the note should either test it or say only "the grid's error".
35. "For walls this reading gave 0.179 against the twin's 0.186, a 4 % gap from the half-trapped rule." Unsupported attribution:
    nothing shows that the gap comes from the half-trapped rule rather than from what the far border has already absorbed.
36. "Dividing by the total compares shares of what is still in the box, so what the side border took drops out." G: true only
    if the side border takes the same share from every region; for discs, whose transmitted wave goes round the rim and spreads
    sideways, it need not. One sentence of support or a qualifier.

### §12 Discs and shells

37. "and has spread only a little, to about 3.6 by (3), when it reaches the barriers at \(t\approx12\) (14 at a speed of about
    1.2)." S: "14" is the start distance from §2, unnamed here. Say "after 14 units of flight at speed 1.2".
38. Disc table: nine of its 30 cells read "to come"; the \(\tau_{\text{side}}\) column has one number; the "share through, pair"
    and "share through, one disc" columns have no row where both are filled, so the sentence below it ("The last column, one
    disc alone, is the yardstick") cannot be used on any row. S has nothing to compare. G: a table that cannot yet support its
    own Key result.
39. Key result "finite barriers leak at the side": "and the larger radii, still to come, will show the trend." A Key result that
    is a promise. Rests on one data point (\(R=2\)). Rewrite as what (27)–(28) predict, stated as a prediction, with the one
    measured point.
40. "The packet, within about 3.6 of the axis, meets the shells head-on: much of it is reflected or passes through both shells".
    S: a straight path through the centre crosses four shell walls (outer, inner, inner, outer), not two; "through both shells"
    hides that, and the geometry (inner shell spans 2.5 to 3.5 for \(R=3\), outer 5 to 6) is never stated. A sentence with the
    radii would let S picture it.
41. "We give no model of the shells here: a wave held in a spherical well has its own family of levels, a subject for another
    note." STANDARD items 2–3: the only shell results on the page come without any model. G would accept one line: inside a hard
    sphere of radius \(a\) the s-wave levels are \(E_n=n^2\pi^2/2a^2\), so the trapped energies and their order can be estimated
    against the table's 0.3–0.45.
42. "The wider spacing, \(s=3.5\), holds the wave longer, as section 7 leads us to expect." Section 7 is about a planar well;
    for shells the larger spacing also means a larger outer shell area to leak through. G: the appeal is loose; say which part
    of §7 carries over (a lower, slower level and a larger \(\kappa\)).

### §13 The device

43. "(11), which assumes the same wave number on both sides, explains the trend." S: (11) is in terms of \(T_a,T_b\); the step
    "the first barrier's \(T_a\) falls, the second's \(T_b\) rises, so \(4T_aT_b/(T_a+T_b)^2\) drops" is not written. One clause.
44. "the share that crosses is the flow of probability, \(T=(k_R/k_L)\,|t|^2\)". \(T\) redefined (mark 3); and G notes that this
    breaks \(|w|^2-|\gamma|^2=1\) of (6), which §3 flagged ("section 13 meets a case where they differ") but §13 never comes back
    to close.
45. "The current from the runs. … the curve's peak and valley would say more about which runs are filed than about the diode."
    G: then the drawn curve in Fig. 15e is, by the note's own account, not yet meaningful; the reader of the figure is not told
    on the figure. (Mark 2 for the wording.)
46. "Because an electron crosses the structure in well under a picosecond, the oscillation can be extremely fast." G: the
    relevant time is the trapped lifetime (62 fs here) plus the transit of the depletion region, not only the crossing; the
    sentence is right in spirit but skips the lifetime the note just computed. Use \(\tau\) = 62 fs.

### §14 Limits and further reading

47. "The next, more complete model solves the Schrödinger and Poisson equations together and lets the electrons scatter as they
    cross." No source for it. STANDARD item 8 asks for textbook chapters; the list has five papers and no textbook (a chapter of
    Davies, *The Physics of Low-Dimensional Semiconductors*, ch. 5, or Datta, *Electronic Transport in Mesoscopic Systems*, ch.
    on resonant tunnelling, opened and linked, would serve both readers).
48. Problem 3: "compare with the time for an electron of energy 110 meV and mass \(m^{*}\) to cross the 4.13 nm well once. How
    many times does it cross before it escapes?" With the geometric width S gets about 11 crossings (5.4 fs each); §5 says
    "about three round trips" (6 crossings) using \(L_{\text{eff}}\). Without a hint ("use \(L_{\text{eff}}\) = 7.6 nm") S gets
    an answer that disagrees with the text and does not know why.
49. Problem 6: "Check your answers against the table when those runs are in." Mark 2.
50. Source paragraph: "notes/fig15/gen2_numbers.py, which reads the stored Kaggle runs and their index, …" Fine as a source
    line; the term "gen2" is house jargon, unexplained.

### At 390 px

51. §8 table (and the §7 table): at 390 px the table is cut at the right edge; the columns "Γ exact", "Γ from (17)" and "τ",
    the very ones the Key result below discusses, are off screen with no visible scroll cue. Measured in the screenshot of §8 at
    390 px.

## Verdicts per section against notes/STANDARD.md

| § | title | verdict | main reasons |
|---|---|---|---|
| 1 | Two panes of glass | needs work (small) | good everyday picture; "Reading the figures" is a repeated legend before any physics (4); Fabry–Pérot clause (5) |
| 2 | The model in three dimensions | needs work (small) | separation argument now complete; bare Gaussian solution (7); start-position sentence (6, 8) |
| 3 | One barrier | clear, leave it | derivation shown, limits checked, worked example; only the \(t\) double meaning (9) and starred quick steps (10, 11) |
| 4 | Two barriers, two ways | clear, leave it | sum over bounces with Example 4.1 is model teaching; script path (12) |
| 5 | The sharp peak and the trapped wave | needs work | \(n=0\) vs \(n=1\) (13); \(T_2\) undefined (14); unstarred restatement missing for the wide-gap ★ (16) |
| 6 | Wave packets | needs work | long-packet paragraph is a run log (18, 19); \(k\to E\) step silent (17) |
| 7 | A wider well sings lower | clear except one sentence | good picture and table; untraced 12 % gap (22) |
| 8 | Taller and thicker barriers | clear, leave it | table and Key result good; fit rule used before defined (23) |
| 9 | Three, five and ten barriers | clear except small points | full ★ derivation, Bloch condition, Figure 2 good; overclaim (24), \(\xi=0\) step (25), speculation (27) |
| 10 | What was computed, and how | needs work (small) | time-step error not measured (29); 0.59 rad unexplained (28); border profile (30); count 376 (31); status line (2) |
| 11 | How good the grid is | needs work | untested causes (34), unsupported attributions (35, 36), 66 % unexplained (33) |
| 12 | Discs and shells | needs work | mostly empty table and a Key result that is a promise (38, 39); no shell model (41); geometry (40) |
| 13 | The device | clear in the theory, needs work in "The current from the runs" | supply function and current turn well derived and checked; flux \(T\) loose end (44); runs curve admitted meaningless (45) |
| 14 | Limits and reading | needs work (small) | no textbook source for the next model (47); Problem 3 trap (48) |

Whole note: needs work on typesetting (1: body not in Latin Modern, no table of contents), on the batch-status sentences (2),
and on one-symbol-one-meaning (3). The physics and the numbers are right everywhere I checked.

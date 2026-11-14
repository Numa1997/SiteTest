# Fig. 15 · referee report, round 3 (resonant tunnelling)

Read as rendered, at commit `1c43cd0` (branch `claude/fig15-gen2-note`). `npm run build` (exit 0), `dist/` served on port 9147,
opened in headless Chrome at 1400 px and 390 px, every section unfolded, the box "What is rounded…" opened, sticky headers made
static, each section screenshotted. KaTeX: 0 `.katex-error`; no console errors. One raw `\(` survives in the text (mark 2). At
390 px, with all folds open, 15 display equations and 4 of the 6 tables are wider than the column; they scroll sideways rather
than overflow the page. The 3D panels are blank locally (run files on the remote store), as expected. plan.md and check.md were not read.

Spot checks recomputed independently (transfer matrices): Example 4.1's partial sums (2.1, 7.1, 13.9, 36.8, 67.1, 92.5, 99.9 %),
the first band 0.590–0.955, the three-barrier peaks 0.657 and 0.83, T = 0.144 and 6.4 × 10⁻³ (d = 2), eq. (9) 0.154,
(17) = 0.0633, σ⊥(40) = 7.31, σ⊥(13) = 3.70, σ_E = 0.202, (19) = 0.218 and 0.0358, a = 2.75 nm, τ = 62 fs, 87 K, the
diode products 1.04 and 0.74, the run counts summing to 3739, the diagonal phase step 0.59 rad. All match the note.

Two readers: **S**, a school student good at mathematics; **G**, a physics graduate. Each mark gives the section, the exact
sentence, who gets lost, and why.

## Marks

### Rendering faults (both readers)

1. §11, "For discs, “between” means between the two discs’ planes and within their radius; “before” and
   “beyond” are the whole box on either side." The escapes print literally on the page (screenshot of §11): the reader
   sees `“between”`. The string is inside a JS single-quoted literal that apparently went through a second escaping.
2. §13, "The products, 1.04 at \\(V_b=0.875\\) and 0.74 at 1.25, show the turn." Renders as the raw text `\\(V_b=0.875\\)`
   (double backslash in the source, so KaTeX never sees it).
3. Further reading and §4, §11: the links to `gen1_profile_check.py`, `gen2_numbers.py` and
   `public/data/resonant-tunnelling/2026-11-14/kaggle/index.json` point at `github.com/…/blob/main/…`, but none of the three is on
   `origin/main` today: they 404 until the branch is merged. (`derive.py` is on main and works.) STANDARD §4.8 asks for working links.

### Abstract

4. "Three, five and ten barriers split the one resonance into close ones that merge into a band" (S). "close ones" what? Say
   "close resonances". Minor.

### 01 · Two panes of glass

5. "Hold two panes of glass close together and look at a lamp through them at a shallow angle. You see faint coloured fringes."
   (G) Fringes from two separate panes need a gap of order a wavelength of light (an air wedge); with panes merely "close
   together" one sees nothing. Say "pressed together, with a thin film of air between" or use a soap film.
6. "Its height is the real part of the wave or the probability density (the chips under Show)" (S). "real part of the wave",
   "probability density" and "the box" are used here; the wave function, its complex value and probability are only defined in
   section 2. The paragraph "Reading the figures" is one 270-word block of controls before any physics; a school reader meets
   it before knowing what is being plotted. A pointer "(defined in section 2)" or moving the paragraph after §2 would help.

### 02 · The model in three dimensions

7. "Since they depend on different variables and add to zero, each can depend on \(t\) alone; such a function of time only adds a
   phase to its factor, so we may choose each bracket to be zero." (S) Two steps in one clause. Why "each can depend on t alone"
   needs one sentence (hold y, z fixed and vary x: the first bracket cannot change, so it has no x in it). And "only adds a phase"
   needs: if the bracket equals c(t), multiply χ by exp(i∫c dt) and it becomes zero, while |ψ| is unchanged.
8. "Its narrow width holds a spread of sideways wave numbers \(1/(2\sigma_\perp)\) … so its parts drift apart" (S). The
   physical picture (a narrow beam must contain sideways-moving waves, like light through a slit) is the point and is only
   implied. One clause.

### 03 · One barrier

9. "Between two edges the wave only travels: the amplitude of a right-mover at the far end of a stretch \(\ell\) long is
   \(e^{ik\ell}\) times its amplitude at the near end" (S). Inside the barrier there are no right- and left-movers but a decaying
   and a growing exponential; the reader is not told that the same travel matrix with \(k=i\kappa\) becomes
   \(\mathrm{diag}(e^{\kappa\ell},e^{-\kappa\ell})\), which is the "cross" factor of "step in, cross, step out".
10. ★ "which for \(Ae^{ikx}+Be^{-ikx}\) is \(v(|A|^2-|B|^2)\) on the left, must equal \(|C|^2-|D|^2\) on the right" (G). The
    factor \(v\) is dropped on the right; write \(v(|C|^2-|D|^2)\) and then say the \(v\)'s cancel because \(k\) is the same.
11. ★ "Then \(|w|^2=\cosh^2\kappa d+a^2\sinh^2\kappa d\) … with \(a=(\kappa^2-k^2)/2k\kappa\)" (G, S). The letter \(a\) is
    already the length unit (§2, "lengths in a unit \(a\)", "both \(3\,a\)"). One symbol, two meanings, two sections apart.
12. ★ "gives \(w=e^{ikd}[\cosh\kappa d+i\tfrac{\kappa^2-k^2}{2k\kappa}\sinh\kappa d]\) and \(\gamma=i\tfrac{\kappa^2+k^2}{2k\kappa}\sinh\kappa d\)
    (checked against the numerical product)" (G). The one step of the section that is the derivation is replaced by "carrying out
    the product … gives". STANDARD §3 forbids the silent step. At least the three matrices written out, or the one line that
    gives \(w\), is needed for the starred reader.
13. "(Here \(t\) is an amplitude, not a time; which is meant is always clear from the context.)" (S) It is not always clear: in
    §5 "after a time \(t\) (now a time again)" the note itself has to flag it. Together with \(T\) (transmission, then temperature
    in §13), \(R\) (reflection, then disc radius in §12), \(m\) (mass, then number of round trips in Example 4.1), \(x\)
    (coordinate, then \(E_\perp/k_BT\) in §13) and \(d\) (width, \(d^3r\), \(dk\)), the note breaks "one symbol, one meaning"
    (STANDARD verdict of 21 Oct, point 2) six times. Each is flagged locally, but a first-time reader trips on every one.
14. "Tunnelling is ferociously sensitive to width." Voice: dramatic, against the "calm professor" rule. "very sensitive" will do.

### 04 · Two barriers, two ways

15. "Two barriers in a row are described by multiplying their matrices, with a travel matrix for the stretch between them. A
    second way gives the same answer and shows the physics" (G). The title promises two ways; only the sum over bounces is
    carried out. The matrix route appears only as "This agrees with the matrix product to one part in \(10^{9}\)
    (notes/fig15/derive.py)": a script stands in for a derivation the reader could do in four lines (\(t_2=1/(\mathbf M\mathbf D\mathbf M)_{11}\)).
16. "Then moving from the centre of the first barrier to the centre of the second adds the phase \(e^{iks}\): the distance is the
    centre spacing \(s\), because \(t\) and \(r\), measured from each barrier's centre, already include what happens inside the
    barriers." (S) This is the hardest idea of the section and it is said once, in a subordinate clause. A school reader will ask
    why not the gap \(s-d\). One more sentence with the picture (the barrier is shrunk to a point at its centre, its whole effect
    lumped into \(t\) and \(r\)) closes it.
17. "For equal barriers, the wave reflected straight off the first barrier and the waves leaking back out of the well cancel
    exactly at resonance" (G). Asserted, not shown; it follows from \(R_2=0\), i.e. from \(|t_2|=1\) and \(|t_2|^2+|r_2|^2=1\).
    Say so in a clause.
18. "The denominator is the whole story." Headline-style hook (STANDARD 21 Oct, point 3).

### 05 · The sharp peak and the trapped wave

19. "Push a child on a swing once per swing, at the top" (S). Fine picture; minor: one pushes as the swing starts forward, at the
    back of its arc; "at the top" can be read as the top of the swing set.
20. "here \(r\) is close to \(-1\), as for a hard wall" (G). Unsupported for the running example: \(|r|=0.925\) and its phase
    \(\rho\) is never given. Give \(\rho\) at \(E=0.735\).
21. "With \(t_{\text{rt}}\approx2L_{\text{eff}}/v\) the width becomes \(\Gamma\approx\hbar vT/L_{\text{eff}}\)" (G, S). Silent
    step: from (15), \(\Gamma=2\hbar T/(\sqrt R\,t_{\text{rt}})=\hbar vT/(\sqrt R\,L_{\text{eff}})\); (17) drops \(1/\sqrt R\)
    (≈ 1.04 here). Say "and \(\sqrt R\approx1\)". The 0.0633 printed below is computed without it, so the reader who keeps it
    gets 0.0658 and thinks they erred.
22. "This is the law of every slow leak: a fixed fraction lost per unit time." (S) The sentence follows \(\tau=\hbar/\Gamma\),
    but it describes the exponential decay of the previous sentences, not the reciprocity. Put it after "\(=e^{-t/\tau}\)".
23. "Each round trip the trapped wave is reflected twice, so its probability is multiplied by \(R^2\)" (G). Fine; but the claim
    that \(-2\ln R\) and \(2T/\sqrt R\) "agree up to terms of order \(T^3\)" is given without the one-line expansion
    (\(-\ln(1-T)=T+T^2/2+T^3/3\), \(1/\sqrt{1-T}=1+T/2+3T^2/8\)). A ★ line would do.
24. "A very wide gap. … For the running example it is \(0.144/1.856=0.078\), about half of one barrier." (S) The paragraph is
    about a very wide gap, then quotes the running example, whose gap is not wide. Say this is the value the incoherent average
    would have, for comparison.

### 06 · A wave packet is not a single energy

25. "For the running example the best of the 5 long-packet runs filed so far passes 0.51 of the packet at \(E=0.713\), where
    the exact average for this packet is 0.499 (these runs stopped more than 15 % too early and are due to be rerun)" (G). A
    measurement is quoted and in the same breath declared flawed. The reader cannot tell whether 0.51 is trustworthy, or why a run
    that stopped early would pass more than the exact average. Either explain what "stopped early" does to the share, or withhold
    the number until the rerun.
26. "the long packet passes only 0.0225 at \(E=0.7215\), against 0.0318 for the exact average there … Equation (19) agrees with the
    exact average at the peak: for \(d=2\) it gives 0.0359, and the exact average is 0.035." (S) Three nearby numbers (0.0318,
    0.035, 0.0359) at two energies (0.7215 and the peak 0.744, which is not named here). The reader has to work out that the run
    is 0.0225 below the peak. Name the peak energy in the sentence.
27. "and so narrow a peak is also very sensitive to the small shift the grid gives it (section 11)" (G). Section 11 says the grid
    lowers the peak "a little" but never gives the size of the shift. Without a number the reader cannot judge whether the shift
    explains 0.0225 against 0.0318 (30 % low, much more than the 5 % of §11).
28. "Its energy spread is four times narrower, \(\sigma_E=0.051\), smaller than \(\Gamma\), though its full width at half maximum,
    0.119, is still wider than the peak's full width \(\Gamma\)." (S) Comparing a standard deviation with a FWHM, then a FWHM with
    a FWHM, in one sentence: the conversion (FWHM = 2.355 σ) is not given. One clause.

### 07 · A wider well sings lower

29. "At the edge \(x=L/2\) both the wave and its slope must match, so their ratio must match too: \(-k\tan(kL/2)=-\kappa\)."
    (S) The reader must compute \(\chi'/\chi\) on each side; write the two ratios before equating them.
30. Table, column "hard box \(\pi^2/2L^2\)": gives only the lowest level, while the two columns beside it list several. A reader
    comparing row by row reads 0.79 against "0.388, 1.486". Say "lowest level" in the header.
31. "measures a lifetime of 65.2, against the exact \(\hbar/\Gamma=58.3\): 12 % longer, more than the 6–8 % section 11 finds for
    the running example; we have not traced the difference." (G) Honest, but the run is at \(E=0.35\), 0.04 below the
    resonance 0.388, with \(\sigma_E\approx0.14\). Is the fitted lifetime expected to be \(\hbar/\Gamma\) when the packet is not
    centred on the peak? One sentence on why the fit should be insensitive to the packet's centre would make the comparison fair.

### 08 · Taller and thicker barriers

32. "The table checks (17) against the exact widths, for the barrier heights and thicknesses the figure offers" (G). §10 says
    "other heights and thicknesses (564)", i.e. 12 structures; the table has 5 rows. Which structures the figure offers and the
    table omits is not said.
33. "Equation (17) already holds the whole story" — headline phrasing again (see mark 18).
34. "A taller barrier raises it noticeably (0.877 at \(V_0=3\)), because the wave reaches less far into the barriers and the well
    is effectively narrower" (S). Good. No mark; noted as the kind of physical reason the other sections should match.

### 09 · Three, five and ten barriers

35. Figure 2: the strip labels "N = 2" … are set upright in the text face, not as math italic \(N\) as in the caption and text.
    Minor.
36. "For ten walls the 3D runs inside the band pass on average 0.129 of the packet (the exact average (18) at the same energies is
    0.158), and in the gap, between 1.05 and 1.6, 0.0218 (exact 0.032)." (G) 18 % low in the band and 32 % low in the gap, much
    more than the 5 % on resonance of §11, and not commented on. The reader needs either the reason (ten barriers each two grid
    points thick, so the edge softening of §11 compounds) or a pointer to §11 with that statement.
37. "The off-diagonal element of \(\mathbf P^N\) is \(U_{N-1}\) times that of \(\mathbf P\), whose square is
    \(|\gamma|^2=|w|^2-1=R/T\)." (S) "whose square" should be "whose squared modulus"; also, the off-diagonal of \(\mathbf P\) is
    \(\gamma e^{iks}\), not \(\gamma\); its modulus is \(|\gamma|\). One word.
38. "Since \(\mathbf P^N\) has the form (6) too, its transmission is one over \(1+|\gamma_N|^2\)" (S). \(\gamma_N\) is not
    defined; it is the off-diagonal of \(\mathbf P^N\). Name it in the previous sentence.

### 10 · What was computed, and how

39. "The error is of order \(\Delta t^3\) per step … over the \(1/\Delta t\) steps of a unit of time it adds up to order
    \(\Delta t^2\). We use \(\Delta t=0.01\)." … "the error of the split comes only from the places where the potential changes,
    and section 11 measures it." (G) Section 11 measures the total gap to exact theory and attributes it to the grid spacing; it
    never separates the time-step error (no run at \(\Delta t=0.005\) is reported). STANDARD §5 asks for the error the reader
    should expect, measured. Either report a halved-step run or say the time-step error was not measured separately.
40. "Each count is the number of structures times 47 energies" (G). The numbers of structures (24, 4, 12, 8, 9) are not given, so
    the reader cannot check the counts or know which "other heights and thicknesses" exist (mark 32).
41. "The runs are computed in six parts on two T4 GPUs each; 1237 of them, from the first 2 parts, are filed so far, after 5.9
    hours on the clock." (S, G) Status of a batch, not physics; it ages the moment the batch moves on. The same holds for
    "still to come" (§12 table, five "to come" cells), "So far 170 of the 500 runs" (§13), and the "best of the 5 long-packet runs
    filed so far" (§6). A textbook chapter with "to come" in its tables reads as unfinished.
42. "a soft absorbing border: each step it multiplies the wave by a factor that falls smoothly from 1 to 0" (G). The profile and
    its reflection of slow waves are not given; slow components (E = 0.3) are the ones a smooth mask reflects most.

### 11 · How good the grid is

43. "The lifetime is fitted where the probability between the barriers has fallen from 60 % to 5 % of its peak" (S). This
    definition is used in §5 ("the dashed curve in Fig. 15c"), §7 and §8, and only stated here, after the "What this means" box,
    as an afterthought. A first reader of §7–8 does not know how a "lifetime of 65.2" or "a lower bound" was obtained.
44. "Put together: a lower share through on the peak and a longer life both mean a narrower peak; more through below the peak and
    less above mean the peak sits a little lower in energy." (G) How much lower is never estimated; it matters for marks 27 and 36.
45. "A likely cause, which we have not separated further: each barrier is only two grid points thick" (G). Plausible but
    untested; a 1D twin at half the spacing costs seconds and would settle it. As written it is a claim without support.

### 12 · Discs and shells

46. "Discs of radius 2 cover only the packet's core; most of it passes beside them, and the share that got through is 0.936."
    (S) "Share that got through" here includes what passed beside the discs, not what tunnelled. Fig. 15d compares it with the
    walls' tunnelling curve. Say that the share counts both.
47. "The last column, one disc alone, is the yardstick: near a resonance the pair passes more than one disc only because the
    trapped wave adds its share." (S, G) Unclear: at R = 6 and 4 the pair's share is "to come" and at R = 2 the one-disc share is
    "to come", so no row lets the reader make the comparison the sentence describes.
48. "A wave held across a width \(R\) carries a spread of sideways momentum of about \(\hbar/R\)" (S) Good picture. But the
    table then compares \(\tau_{\text{side}}=2.28\) with \(R^2=4\) for the only filled row and draws a trend ("the larger radii,
    still to come, will show the trend") from one point. The Key result states as a finding what the table cannot yet show.
49. "The runs at \(E=0.65\) measure it (the energy nearest the resonance filed so far; the runs at 0.75, closer to it, are still to
    come)" (G). The walls' lifetime in the table, 15.1 at \(E=0.65\), is the same number §11 gives for the 3D run at \(E=0.735\)
    of the earlier batch. If that is a coincidence, say so; if the 15.1 is the old number, the row label "same energy, this
    batch" is wrong.
50. "The packet mostly passes round it, but a part gets in and rings there for a long time" (G). The shells are centred on the
    flight axis with outer radius \(R+s=5.5\) to \(8.5\), while the packet's probability lies within about 3.7 of the axis
    (§12, from (3)). Most of the packet must hit the outer shell, not pass round it. The claim needs a number (share reflected,
    share passing) or should be corrected.
51. "We give no model of the shells here: a wave held in a spherical well has its own family of levels, a subject for another
    note." (G) STANDARD §2 asks for the model stated. Even one sentence would do: the radial equation for \(u=r\chi\) is the 1D
    problem of §§3–7 on the half-line, with the centrifugal term \(\ell(\ell+1)/2r^2\); the \(\ell=0\) levels of the hollow ball
    follow from (20)-like matching. Without it the long lifetimes are unexplained data.
52. Problem 6 (§14): "Use the table of section 12 and (27) to find \(\tau_{\text{side}}\) for each disc radius in the table that
    has a lifetime. … Does \(\tau_{\text{side}}\) grow faster or slower than \(R\)?" With one filled row (R = 2) the question
    cannot be answered.

### 13 · The device

53. "A battery across the device holds the right side lower than the left by an energy \(eV_b\) (\(-e\) the electron's charge,
    \(V_b\) the voltage, the bias; in our units we quote the bias by that energy, in units of \(E_u\) (so \(eV_b\) and \(V_b\) are
    the same number), and we keep the plain \(V\) for the potential)." (S) A parenthesis nested in a parenthesis carrying four
    definitions. Split into two sentences.
54. "On each side of the barriers the electrons fill every state from the band bottom … up to an energy \(E_F\), the Fermi energy"
    (S). Why the states fill up (Pauli exclusion: one electron per state per spin) is not said; it is the reason the supply
    function exists.
55. "the electron's energy lies further below the first barrier's top than below the second's, so the first is more opaque" (S).
    Good. But "(11) explains why they fall below 1": (11) needs \(T_a\) and \(T_b\), which are never quoted for \(V_b=0.5\) or 1.
    Two numbers would turn the pointer into a check.
56. "the electron leaves on the lower side faster than it came, so the share that crosses is the flow of probability,
    \(T=(k_R/k_L)|t|^2\)" (S). The reason (probability current \(=v|\text{amplitude}|^2\), §3 ★) is in a starred passage the
    student may have skipped; one clause "since the flow is speed times probability density" makes it self-contained.
57. "We take \(E_F=1.0\) (150 meV), high for a real diode" (G). A typical value for comparison (tens of meV) would let the reader
    judge "high".
58. Figure 3: the labels inside the SVG read "filled up to EF", "level at Vb = 0" in upright text, with subscripts drawn as
    subscript text; consistent enough, but "eVb" at right is italic while the others are upright. Minor.

### 14 · What the model leaves out

59. "The next, more complete model solves the Schrödinger and Poisson equations together and lets the electrons scatter as they
    cross." (G) STANDARD §7 asks for the next model named; the standard name and tool (non-equilibrium Green's functions, or the
    Wigner-function method) and a reading for it are absent from Further reading.
60. Further reading has no textbook chapter for the student (STANDARD §8 names "textbook chapters"); e.g. Griffiths,
    *Introduction to Quantum Mechanics*, §2.6 (finite well) and Problem 2.33 (barrier), or Davies, *The Physics of
    Low-Dimensional Semiconductors*, ch. 5 (tunnelling, RTDs). Only real sources opened and read may be added.

## Verdict per section (against notes/STANDARD.md)

| § | Section | Verdict | Why |
|---|---|---|---|
| — | Abstract | clear, leave it | Accurate summary; mark 4 is cosmetic. |
| 01 | Two panes of glass | needs work (small) | Picture strong; the glass-fringe set-up is physically off (5); figure-reading paragraph precedes the definitions it uses (6). |
| 02 | The model in 3D | needs work (small) | Model, units, separation and spreading are there; the separation step skips two reasons (7). |
| 03 | One barrier | needs work | Central derivation of \(w,\gamma\) replaced by "carrying out the product gives" (12); missing \(v\) in the current argument (10); \(a\) reused (11); symbol overloading throughout (13). |
| 04 | Two barriers, two ways | needs work (small) | Bounce series excellent (Example 4.1 is the best passage of the note); the matrix "way" is a script, not a derivation (15); the centre-to-centre phase needs one more sentence (16). |
| 05 | Sharp peak, trapped wave | needs work (small) | Strong physics; silent drop of \(\sqrt R\) between (15) and (17) makes the printed 0.0633 unreproducible by the reader (21); \(\rho\) never given (20). |
| 06 | Packets | needs work | Formulas and checks fine; the long-packet paragraph quotes runs it calls flawed (25) and unexplained 30 % gaps (26, 27). |
| 07 | Wider well | needs work (small) | Clear model and table; matching step and table header (29, 30). |
| 08 | Taller, thicker | clear, leave it | Picture, model, table, check and honest lower bound; marks 32–33 minor. |
| 09 | N barriers, bands | needs work (small) | ★ derivation complete and checked; undefined \(\gamma_N\) (38); 3D-vs-exact gaps of 18–32 % uncommented (36). |
| 10 | Computation | needs work (small) | Method as the code does it; time-step error not measured (39); batch status text (41). |
| 11 | Grid quality | needs work | Rendering fault (1); fitting rule defined after it is used (43); peak shift and its cause unquantified (44, 45). |
| 12 | Discs and shells | needs work | Disc picture and estimate good, but tables mostly "to come", conclusions drawn from one row (47, 48, 52); shell claim "passes round it" likely wrong (50); no shell model (51). |
| 13 | Diode | needs work (small) | Strong section; rendering fault (2); nested definition parenthesis (53); Pauli reason missing (54). |
| 14 | Limits, reading | needs work (small) | Next model unnamed (59); no textbook chapter (60); three links 404 until merged (3). |

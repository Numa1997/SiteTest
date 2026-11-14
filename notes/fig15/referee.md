# Fig. 15 · referee report, round 2 (resonant tunnelling)

Read as rendered, after commit `db61bec` ("fix round-1 marks"). `npm run build`, `dist/` served on port 9531, opened in headless
Chrome at 1400 px and at 390 px, every section unfolded, the box "What is rounded…" opened, each section screenshotted with only
the sticky fold headers made static. KaTeX: 0 errors, 0 raw `\(`, 0 display equations overflowing at either width; no console
errors. plan.md and check.md were not read.

The one-dimensional numbers were recomputed independently (transfer matrices, packet average, band edges, Tsu–Esaki current
with a 700-step staircase). All of these match the note: T = 0.144, |r| = 0.925, ħθ' = 4.45, Γ(15) = 0.0699, FWHM 0.0704,
2L_eff/v = 4.55, −2 ln R = 0.3109, 2T/√R = 0.3112, σ⊥(40) = 7.31, E₁ by (21) = 0.649, band 0.590–0.955, second band 2.082,
ξ(0.735) = −0.0004, peaks for N = 3 and 5, T̄ = 0.196 (short), 0.149 (one barrier), a = 2.75 nm, τ = 62 fs, 87 K, tilted peaks
0.486 and 0.230 with heights 0.878 and 0.562, and a current peak at V_b = 0.875 with a valley near 1.85 (PVR 4.3). No numerical
error was found. The marks below are about reading, not arithmetic, except where they say otherwise.

Two readers: **S**, a school student who is good at mathematics; **G**, a physics graduate. Each mark gives the section, the
exact sentence, who gets lost and why.

## Marks

### Abstract

1. "A long packet, with a narrow spread of energies, resolves peaks a short one averages away." (G) Section 6 shows one long
   packet run near the running example's peak, and it says the d = 2 peak is *not* resolved. No long-packet run on three or more
   barriers is shown anywhere. The sentence promises more than the note delivers. Say "passes far more of a single peak".

### 01 · Two panes of glass

2. "The chips choose the barriers: … their height \(V_0\) and thickness \(d\), their spacing \(s\), and the length of the packet"
   (S). \(V_0\), \(d\), \(s\) appear here before Figure 1 defines them, which is three paragraphs later. A pointer "(Figure 1)"
   is enough.
3. "Reading the figures." paragraph (S). It is 230 words long, with the colours and line styles of four panels, read before the
   reader knows what a transmission, a lifetime or a packet average is. It uses "the exact one-dimensional answer", "the fitted
   exponential decay of the trapped wave" and "averaged over the spread of energies a packet holds", all defined only in
   sections 3 to 6. A student will not take it in here. Moving it is not the referee's call, but it reads as a legend, not as
   prose.

### 02 · The model in three dimensions

4. "A wave packet is a sum of plane waves … that moves at the group velocity \(v=d\omega/dk=\hbar k_0/m\), which for an electron
   is simply its speed." (S) The relation between \(\omega\) and \(k\) is never given. The reader needs \(E=\hbar\omega\) and
   \(E=\hbar^2k^2/2m\), hence \(\omega=\hbar k^2/2m\), before the derivative means anything.
5. "(a dot is a time derivative, a prime a space derivative)" (S). The dot and the prime are used in the formula just before this
   sentence. Define them before the formula.
6. "Setting each bracket to zero satisfies the sum, and gives" (G). Each bracket may equal a constant, with the three constants
   summing to zero. Setting them to zero is one allowed choice (it puts each factor's phase in its own equation). One clause
   saying this is a choice, not a necessity, would stop the graduate.
7. "Its narrow width holds a spread of sideways wave numbers \(1/(2\sigma_\perp)\), so its parts drift apart" (S). Why a narrow
   width implies a spread of wave numbers, and why exactly \(1/(2\sigma_\perp)\), is only explained in section 6 (and there
   only stated). Point forward to section 6 or give the uncertainty idea in one line here.
8. "With \(\sigma_\perp=3\) this width is 7.3 by \(t=40\), about halfway through a run" (S, G). The length of a run is not given
   anywhere before this, and section 10, which describes the runs, never says how long a run lasts or how far apart its 200
   frames are. The only run length in the note is 213 for the d = 2 run (section 8). "About halfway" has no support.

### 03 · One barrier ★

9. "Inside a barrier \(k_2=i\kappa\); nothing else changes. Between two edges the wave only travels: the amplitude of a
   right-mover at the far end of a stretch \(\ell\) long is \(e^{ik\ell}\) times its amplitude at the near end" (S). Inside a
   barrier there is no right-mover: with \(k=i\kappa\) the factor \(e^{ik\ell}=e^{-\kappa\ell}\) is a decay, and the "left-mover"
   is the growing exponential. Say so in one clause, or the student will think the wave travels inside the barrier.
10. "Write the wave just left of an edge as … with the edge at \(x=0\)." (G) The matrix (5) is written with the origin at the
    edge, and a barrier has two edges at different places. The reader has to see that each edge uses its own origin and that
    the travel matrix carries the phase from one origin to the next. One sentence.
11. "Carrying out the product of the three matrices for a square barrier, with \(x=0\) at the barrier's centre, gives
    \(w=e^{ikd}[\dots]\) and \(\gamma=\dots\) (checked against the numerical product)." (G, and against STANDARD item 3 "no silent
    step") The central algebra of the section is still not shown; the reader is told it was checked. At least write the product
    \(\mathbf S_{k\to i\kappa}\,\mathrm{diag}(e^{\kappa d},e^{-\kappa d})\,\mathbf S_{i\kappa\to k}\) and its top-left element.
12. "Since \(\kappa^2+k^2=2V_0\) and \(k^2\kappa^2=4E(V_0-E)\)," then (7) (S). The shortest route is skipped: by (6),
    \(|w|^2=1+|\gamma|^2\), and \(|\gamma|^2=\frac{(\kappa^2+k^2)^2}{4k^2\kappa^2}\sinh^2\kappa d\) gives (7) in one line. As
    written, the student tries to expand \(|w|^2\) from the cosh/sinh form and has to discover \(\cosh^2=1+\sinh^2\) alone.
13. Section heading "★" on the whole section, and "Passages marked ★ … their results are stated again in plain words just after"
    (section 1) (S). Section 4 starts "Let \(t\) and \(r\) be the amplitudes of one barrier, measured with \(x=0\) at the
    barrier's own centre, as in section 3." A reader who skipped the starred section does not know what an amplitude \(t\) is
    (section 2 defines only \(T\) and \(R\)). The plain restatement of section 3's results (amplitudes \(t\), \(r\) with
    \(|t|^2=T\), formula (8), "one barrier is mostly a mirror") is missing at the start of section 4.

### 04 · Two barriers, two ways

14. "Example 4.1 · the bounces add up. At \(E=0.735\), keep only the first \(N\) round trips" (S, G). \(N\) here counts round
    trips; in section 9 \(N\) counts barriers. One symbol, two meanings, in a note that is otherwise careful about this
    (\(\gamma\) for \(z\), \(R\) in section 12). Use another letter.
15. "A lopsided pair cannot be perfectly clear: the waves reflected from the pair no longer cancel exactly" (S). "No longer"
    refers to a cancellation the note never described. Sections 4 and 5 explain full transmission as transmitted bounces adding
    up; they never say that the reflected wave vanishes because the wave reflected from the front face cancels everything that
    leaks back out of the well. That is the physical picture of perfect transmission, and it is missing.
16. "with equality only when \(T_a=T_b\)" (S). One step: \((T_a+T_b)^2-4T_aT_b=(T_a-T_b)^2\ge0\).

### 05 · The sharp peak and the trapped wave

17. "\(\theta(E_r)=2\pi n,\ n\) a whole number" with "this first resonance is the one at which about half a wavelength fits
    between the barriers" (G). With \(r\approx-1\) the reflection phase is \(\rho\approx-\pi\), so at the first resonance
    \(2ks\approx2\pi\) and \(\theta\approx0\): the first resonance has \(n=0\) (computed: \(\theta/2\pi=5\times10^{-5}\)). A reader
    who takes \(\rho=+\pi\) gets \(n=2\). Say which \(n\) belongs to which resonance, or the count of "first, second" in section 7
    cannot be checked against (14).
18. "Since \(r\) is measured from the barrier's centre, it takes back the half-barrier the wave never actually crosses, \(d/2\)
    at each end, a time \(-2d/v\) in all." (S) \(d/2\) per end gives, naively, \(d\) in all. The count is \(d/2\) in and \(d/2\)
    out at each of two reflections, \(2d\) of path. Spell out the four halves.
19. "(counting two leaks of \(T\) per round trip would give 0.2879)" (S). The student does not know what this alternative is or
    why it is mentioned. Either explain it (a naive model loses \(2T\) of the probability per round trip, \(1/\tau=2T/t_{\rm rt}\))
    or drop it.
20. "With \(t_{\text{rt}}\approx2L_{\text{eff}}/v\) the width becomes \(\Gamma\approx\hbar vT/L_{\text{eff}}\)" (G, silent
    step). From (15), \(\Gamma=2\hbar T/(\sqrt R\,t_{\rm rt})\), which with \(t_{\rm rt}=2L_{\rm eff}/v\) is
    \(\hbar vT/(\sqrt R\,L_{\rm eff})\). The factor \(1/\sqrt R\) (here 1.08) is dropped without a word. That is most of why
    (17) gives 0.0633 against 0.0704 (with \(\sqrt R\) kept: 0.0684). Say "and \(\sqrt R\approx1\)".
21. "and with \(F=4R/T^2\) this is \(T/(1+R)=T/(2-T)\)" (S). The step \(1+F=(1+R)^2/T^2\), using \(T=1-R\), is skipped.
22. "That is just what two independent partly silvered mirrors pass when we add probabilities instead of amplitudes" (S, G).
    Asserted, not shown. One line: \(T^2(1+R^2+R^4+\dots)=T^2/(1-R^2)=T/(1+R)\).
23. "A cup of tea cooling on the table follows the same law" (both). The same analogy opens section 8, almost word for word
    ("A cup of hot tea cools by a fixed fraction of its excess warmth each minute"). Use it once.

### 06 · A wave packet is not a single energy

24. "A Gaussian packet of length \(\sigma_x\) in space is a Gaussian of width \(\sigma_k=1/(2\sigma_x)\) in wave number." (S)
    Unsupported for the student, and "length" and "width" are not defined as standard deviations of \(|\psi|^2\) and
    \(|\varphi|^2\). With section 2's \(e^{-x^2/4\sigma_x^2}\) the statement is exact for those standard deviations; say so, and
    name it as the Fourier transform of a Gaussian (a one-line completion of the square, or a cited result).
25. "and the area under the Lorentzian (15) is \(\pi\Gamma/2\)" (S). One line: \(\int\frac{(\Gamma/2)^2}{x^2+(\Gamma/2)^2}dx=
    \frac\Gamma2\cdot\pi\).
26. "Its energy spread is four times narrower, \(\sigma_E=0.051\): a standard deviation below \(\Gamma\), though its full width
    at half maximum, 0.119, is still wider than the peak's full width \(\Gamma\)." (S) "A standard deviation below \(\Gamma\)"
    reads as "one standard deviation below". Write "a standard deviation smaller than \(\Gamma\)".
27. "the best of the 5 long-packet runs filed so far passes 0.51 of the packet (these runs stopped more than 15 % too early and
    are due to be rerun; the value already agrees with the exact average)" (S, G). Three problems. What "stopped too early"
    does to the measured share is not said (does it under- or over-count?). "The best of the runs" is a maximum over run
    energies 0.70 and 0.75, not a value at 0.735, so it is not the same quantity as the exact peak average 0.538. And 0.51
    against 0.538 is 5 % low; "agrees" needs that number.
28. "For the thick barriers, \(d=2\), the long packet passes only 0.0225 (the best of the runs filed so far, which do not yet
    include the one at the peak) … Equation (19) says the same in numbers: for \(d=2\) it gives 0.0359, and the exact average is
    0.035." (S, G) "The same" as what? The run says 0.0225 and (19) says 0.0359. A reader reads this as a 40 % disagreement
    called agreement. Say that the run is off the peak and is not comparable, and that (19) and the exact average agree with each
    other.

### 07 · A wider well sings lower

29. "The finite well matches the lowest resonance to a few thousandths" (G). The table gives 0.744 against 0.735 and 0.395
    against 0.388: 7 to 9 thousandths, about a hundredth. "To about a hundredth" is the honest wording.
30. "By (17) there are two reasons: a longer well means fewer hits on the barriers per second, and a lower resonance energy
    means a larger \(\kappa\), so each hit leaks less." (G) (17) has a third: the lower resonance has a smaller speed \(v\),
    which also means fewer hits per second. Section 13 uses exactly this reason ("at low energy the electron is slow and meets
    the barriers less often").
31. "(The chip \(s=3\) belongs to the thicker barriers of section 8.)" (S) This interrupts the comparison of (21) with the table
    and refers to a chip the reader has not looked for. Move to the table caption or to section 8.

### 08 · Taller and thicker barriers

32. "a straight line through the logarithm of its decay from \(t=91\) to the end gives 210." (S, G) The paragraph never puts 210
    next to the exact 344 from the table above, nor says why a short fit gives a *shorter* lifetime (39 % short). "A run would
    have to last several lifetimes" explains imprecision, not a one-sided bias. Name the comparison and the likely reason
    (early, faster-decaying off-resonant parts of the packet still in the fit window), or say it is not understood.

### 09 · Three, five and ten barriers

33. "and between bands there are energies where no wave can cross the row at all: gaps." (G) For a finite row the transmission
    in a gap is small, not zero; section 9 itself says it "falls exponentially with the number of barriers", and the 3D runs pass
    0.0218 in the gap. "Where almost nothing crosses a long row" is correct.
34. "A crystal of atoms is the same structure with the atoms as the barriers" (G). The ions of a crystal attract electrons: they
    are wells, and the space between them is the barrier. The Kronig–Penney model works either way round, but the sentence as
    written is physically backwards.
35. "It has determinant 1" (S, ★ passage). The reason is one line away: \(\det\mathbf M=|w|^2-|\gamma|^2=1\) by (6), and the travel
    matrix has determinant 1.
36. Figure 2: the tick labels (0.4 … 1.2) and the strip labels "N = 2 … N = 10" are set in a serif face; the house chart style
    (STANDARD, Form) asks for Plex Mono ticks, and "N" is upright where the text has italic \(N\). The same holds for Figure 3's
    labels "filled up to E_F", "level at V_b = 0", whose E and V are upright and unlike the italic \(E_F\), \(V_b\) of the text.
37. "Select ten walls and step the energy through the band to watch the wave pass from cell to cell" (S). By the paragraph's own
    numbers the short packet passes only 0.129 inside the band. "Watch the wave pass" promises more than the reader will see;
    "watch more of it get through than in the gap" is what the figure shows.

### 10 · What was computed, and how

38. "so a wave leaving the box fades out instead of coming back on the other side." (S) Why it would come back on the other side
    is never said: the Fourier method treats the box as periodic. One clause.
39. "and \(K\) just multiplies by \(e^{-ik^2\Delta t/2}\) after a Fourier transform." (S) The reason, that a plane wave
    \(e^{i\mathbf k\cdot\mathbf r}\) is turned by \(\nabla^2\) into \(-k^2\) times itself, is missing; without it the step is
    magic.
40. "The error is of order \(\Delta t^3\) per step" (G). Unsupported: the error comes from \(K\) and \(V\) not commuting, and the
    symmetric split cancels the \(\Delta t^2\) term. One sentence naming the reason.
41. "the fastest mode the grid holds, \(k=\pi/0.5\), then turns by \(k^2\Delta t/2=0.2\) rad per step, small enough for the split
    to be accurate." (G) In three dimensions the fastest mode is the corner of the Fourier box, \(|\mathbf k|^2=3(\pi/0.5)^2\),
    which turns by 0.59 rad per step. And the kinetic phase is applied exactly by the split; the accuracy depends on the
    commutator term, which is better judged by the measured errors of section 11. The sentence's argument does not support its
    claim.
42. "The batch walks the whole parameter space the figure offers, 3739 runs in seven groups: … other heights and thicknesses
    (564); each barrier alone (376); three, five and ten barriers (423)" (G). The first group and the diode can be reconstructed
    (6 × 4 × 47, 20 × 25); 564 = 12 × 47, 376 = 8 × 47, 423 = 9 × 47 cannot: which 12, 8 and 9 configurations? Name them or drop
    the counts.
43. "it mixes them in the frame that turns with the packet" (S). "Frame" was used one line earlier for a stored snapshot ("two
    stored frames \(f\) and \(f+1\)"). Here it means a rotating reference. Say "in a reference that turns with the packet's
    phase".

### 11 · How good the grid is

44. "The measurements below were made on the running example in an earlier batch of 115 runs" (G). The present batch has 1237
    runs filed, including the running example, and the page plays those. The grid's error is quoted from runs the reader cannot
    see. Either repeat the comparison on the present batch or say why not.
45. "Put together, the three measurements say the grid's resonance is a little narrower than the true one and sits a little
    lower in energy." (S) The inference is left to the reader. One sentence: shifted lower, so more passes below the peak and
    less above; narrower, so less of the packet passes at the peak and the trapped wave lives longer.
46. "lifetimes are 6–8 % long." (box) (G). Section 7 reports a 3D lifetime 12 % long for s = 3.5 ("we have not traced the
    difference"). The box generalises from the one spacing that was measured. "6–8 % for the running example, 12 % at s = 3.5".
47. "For walls this reading gave 0.179 against the twin's 0.186, a 4 % gap from the half-trapped rule." (G) The cause is asserted.
    It might also be the side border or the cut-off frame. Say "which we attribute to" and why.
48. "For discs it is read from the stored region probabilities … the probability beyond the barriers, plus half of what is still
    trapped" (G). For discs, the regions "before, between, beyond" are not defined: is "between" the slab between the discs at
    all radii, or only inside the rim? The wave that leaks sideways out of the gap goes where? The reading cannot be judged
    without this.
49. The paragraph "The lifetime is fitted where … The share that got through, plotted as points in Fig. 15d, is …" sits after the
    box, at the end of the section, but sections 6, 7, 8 and 9 already quote fitted lifetimes and run shares. A reader of
    section 6 meets "the long packet passes 0.51" with no idea how a run's share is read. Point to it from the first use.

### 12 · Discs and shells

50. "Shrink the walls to discs of radius \(R\) on the flight axis (in this section \(R\) is a radius; the reflection coefficient
    does not appear)" (both). Declared, but still one symbol with two meanings in one note, against the Taylor rule of the
    standard (one symbol one meaning). \(\rho\) is taken; \(a\) is the length unit; use \(R_d\) or \(b\).
51. "Across the flight the packet's probability lies mostly within \(\sigma_\perp=3\) of the axis, a band about 6 wide." (S, G)
    Section 2 says the width grows to 7.3 by \(t=40\). When the packet reaches the discs it is no longer 3 wide. Give the width at
    the time of the collision.
52. Table row "walls · 15.1 · — · 0.176 · —", with "The runs at \(E=0.65\) measure it" (G). 15.1 is the lifetime section 11
    quotes for the running example at \(E=0.735\) from the earlier batch of 115 runs. Is it also the lifetime at 0.65 in the
    present batch? And 0.176 differs from the 0.179 and 0.186 of section 11 (different energy?). The reader cannot tell
    whether the walls row is measured at the same energy as the disc row it is compared with.
53. "2 · 1.99 · 2.28 · 0.936" (G). A lifetime of 1.99 is less than half a round trip (\(t_{\rm rt}=4.45\)). A wave that leaves in
    less than one round trip is not trapped in any useful sense; the fit may measure the packet passing by. Say what the fitted
    decay is at this radius before solving (27) for \(\tau_{\rm side}\).
54. Key result "By (27) and (28), the narrower the discs, the shorter the trapped wave should live; … the larger radii, still to
    come, will show the trend. … the runs for the largest discs test it." (both, STANDARD items 4 and 6) The key result is a
    prediction. Four of the five disc rows read "to come", and the one measured row (R = 2) is the doubtful one of mark 53. A box
    titled "Key result" should state something the note shows. Either retitle it ("What the runs will test") or wait for the runs.
55. Table "share through, one disc": 0.415 for R = 6 and 0.678 for R = 4, "to come" for R = 2 (G). The column is never used in
    the text. What it is for (comparison with the pair? with walls' 0.149?) is not said.
56. "Most of them are longer than the runs can follow: where the fit window reaches the end of the run … Read those as 'at least
    this long'" (S, G). Which of the four are "those"? The table does not mark them. Add a mark or a column "fit reaches end".
57. Shells table, "longest \(\tau\) at \(E\) = 0.3" for R = 3, s = 2.5 (G). 0.30 is the lowest run energy; the longest lifetime
    lies at the edge of the range, so the true maximum may lie below it. Say so.
58. Shells, as a whole (G, STANDARD items 2 and 3). The section gives no model for the shell trap: no levels, no estimate of the
    lifetime, not even the order of magnitude given for discs. The "room with the doors shut" picture is good; one estimate (a
    spherical well of radius R + s/2, the lowest levels, a leak through one shell by (8)) would let the reader judge 66.9 and 110.
59. "The packet mostly passes round and over it" (S). "Over" suggests above the barrier in energy. "Round it" says it.

### 13 · The device

60. "(\(-e\) the electron's charge, \(V_b\) the voltage, the *bias*; in our units we write the energy simply as \(V_b\), and we
    keep the plain \(V\) for the potential)" (S). Declared, but the section then writes \(eV_b\) in (29), (31) and Figure 3 and
    plain \(V_b\) in (32) and the text ("\(V_b=0.875\) (131 mV)"). A student reading (31) then (32) sees the \(e\) vanish. One
    convention throughout the section would be kinder.
61. "\(J(V_b)=\frac{e m^*k_BT}{2\pi^2\hbar^3}\int_0^\infty T(E,V_b)\dots\)" (both). \(T\) is the temperature in the prefactor and the
    transmission in the integrand of the same equation. The note warns about it ("in \(k_BT\) only, \(T\) is the temperature"),
    but a reader of (31) on its own sees one letter with two meanings. Write \(\mathcal T(E,V_b)\) for the transmission here or
    \(\Theta\) for the temperature.
62. "\(\frac{m^*}{\pi\hbar^2}\int_0^\infty\frac{dE_\perp}{1+e^{(E+E_\perp-E_F)/k_BT}}=\frac{m^*k_BT}{\pi\hbar^2}\ln(\dots)\)" (S, ★).
    The integral is done silently; it is one substitution (multiply top and bottom by \(e^{-x}\)). Also
    "\(2\,d^2k_\perp/(2\pi)^2=(m^*/\pi\hbar^2)\,dE_\perp\)" skips \(d^2k_\perp=2\pi k_\perp dk_\perp\).
63. "As the level sinks, the supply grows, from 14.2 at \(V_b=0.875\) to 18 at \(V_b=1.25\); but the area under the peak shrinks
    faster, from 0.103 at zero voltage to 0.073 and then 0.041" (S, G). "14.2" and "18" are values of the logarithm in (31), not
    said; 14.2 is also the lifetime of the running example, which invites confusion. "0.073 and then 0.041" do not say at which
    voltages (presumably 0.875 and 1.25). And the products 14.2 × 0.073 = 1.04 and 18 × 0.041 = 0.74, which carry the argument,
    are left for the reader. Also 0.103 is below the Lorentzian area \(\pi\Gamma/2=0.111\); say over what range it is taken.
64. "So far 170 of the 500 runs for two walls are filed … the curve's peak and valley would say more about which runs are filed
    than about the diode. We quote them when all 500 are in." (both, STANDARD item 6) Honest, but Fig. 15e still draws that curve
    on the page, beside the exact one, and nothing on the figure says it is not yet meaningful. The note should say what the
    reader sees in Fig. 15e now, and which line to trust.
65. "For two discs most of the current flows beside the discs and the dip is shallow." (G) No number and, by the paragraph
    before, only a partial set of disc runs. Unsupported as stated.
66. "On each side of the barriers the electrons fill every state up to an energy \(E_F\)" with Figure 3 (S). Figure 3 shades the
    filled states on the emitter side only; the collector, filled up to \(E_F-eV_b\), is drawn empty. Either shade it or say in the
    caption that only the emitter's filling matters at this bias.
67. "We take \(E_F=1.0\) (150 meV)" (G). A Fermi energy of 150 meV in GaAs needs a doping near \(10^{19}\,\text{cm}^{-3}\), far
    above usual RTD emitters (tens of meV). A sentence on why this value was chosen (so the level starts among filled states for
    the running example) and that real emitters sit lower.

### 14 · What the model leaves out, and where to read on

68. "so real peaks are lower and broader than (31) predicts" (S). (31) predicts a current, not a peak in transmission. Say
    "real transmission peaks are lower and broader, and the current's peak-to-valley ratio smaller than (31) predicts".
69. "The next, more complete model solves the Schrödinger and Poisson equations together and lets the electrons scatter as they
    cross." (G, STANDARD items 7 and 8) No source for the next model, and the reading list has no textbook at all: five research
    papers, nothing a school student or a second-year student can read first. A textbook chapter (for example a standard
    quantum-mechanics text on the finite well and transmission, and a low-dimensional-semiconductors text on resonant tunnelling
    and self-consistent models), opened and read, belongs here.
70. Problem 6: "Use the table of section 12 and (27) to find \(\tau_{\text{side}}\) for each disc radius the runs have computed.
    … Does \(\tau_{\text{side}}\) grow faster or slower than \(R\)?" (S) The table has one computed radius. The problem cannot be
    done today.
71. Closing line: links to `notes/fig15/gen2_numbers.py` and `public/data/resonant-tunnelling/2026-11-14/kaggle/index.json` point
    to `github.com/Numa1997/SiteTest/blob/main/…`. Neither file exists on `origin/main` (checked with `git cat-file`); both links
    give 404 until this branch is merged. `derive.py` exists on main.

## Verdicts per section against notes/STANDARD.md

| Section | Verdict | Main reasons (marks) |
|---|---|---|
| Abstract | clear, one fix | overclaim on long packets (1) |
| 01 Two panes of glass | clear, minor | picture is good; symbols before Figure 1 (2); figure legend too early (3) |
| 02 The model in 3D | needs work, small | ω(k) missing (4); dot/prime defined late (5); run length unsupported (8) |
| 03 One barrier ★ | needs work | product of matrices still silent (11); short route to (7) skipped (12); evanescent "right-mover" (9); skip-reader loses t, r (13) |
| 04 Two barriers | needs work, small | N clash (14); the picture of cancelling reflection missing (15) |
| 05 The sharp peak | needs work | √R silently dropped in (17) (20); n of first resonance (17); incoherent sum asserted (22); unexplained 0.2879 (19) |
| 06 Packets | needs work | σ_k unsupported (24); long-packet numbers compared as if comparable (27, 28) |
| 07 Wider well | clear, minor | "few thousandths" (29); missing v in reason (30) |
| 08 Taller, thicker | clear, one fix | 210 vs 344 left uncommented (32) |
| 09 Bands | clear, minor | "no wave can cross" (33); atoms as barriers (34); figure type (36) |
| 10 Numerical method | needs work, small | periodic box (38); Fourier step reason (39); error order unsupported (40); 3D fastest mode wrong (41) |
| 11 Grid quality | needs work, small | measured on an older batch (44); inference unstated (45); 6–8 % over-generalised (46); disc regions undefined (48) |
| 12 Discs and shells | needs work | key result is a prediction with one doubtful data point (53, 54); R reused (50); shells without a model (58) |
| 13 The device | needs work, small | T for two things in (31) (61); unlabelled supply numbers (63); Fig. 15e curve unexplained on the page (64); E_F choice (67) |
| 14 Limits, reading | needs work | no textbook and no source for the next model (69); Problem 6 not doable (70); two dead links (71) |

Against the standard as a whole: items 1 (picture), 4 (checks) and 5 (method) are met in most sections; item 3 fails where marks
11, 12, 20, 22, 24 and 62 point to silent steps; item 6 is weakest in sections 12 and 13, where the figures show data the note
itself calls incomplete; item 8 lacks a textbook. Form: KaTeX renders cleanly at 1400 and 390 px, equations are numbered, no
question-and-answer format; the only house-style lapse is the type in Figures 2 and 3 (36).

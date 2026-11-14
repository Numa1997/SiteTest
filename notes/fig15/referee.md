# Fig. 15 · referee report, round 5 (resonant tunnelling)

Read as rendered, at commit `c346801` (branch `claude/fig15-gen2-note`). `npm run build` (exit 0); `dist/` served on port 9017;
opened in headless Chromium (Playwright) at 1400 px and 390 px. All folds opened, sticky and fixed elements made static, and
each of the 14 sections screenshotted at both widths. KaTeX: 0 `.katex-error`, 0 raw `\(`, `\[` or `$$` in the text, no console
or page errors, no section wider than its box at either width. The 3D panels are blank locally (the run files live on the
remote store), as expected. plan.md and check.md were not read.

Spot checks recomputed by hand: |w|² = 6.94 and T = 0.144; Example 3.1 (6.4 × 10⁻³, ratio 22); (9) = 0.154; −2 ln R = 0.3107
and 2T/√R = 0.3111, their difference T³/12; Γ from (15) = 0.0699; (17) = 0.0632; τ/t_rt = 3.2; σ⊥(40) = 7.31, σ⊥(11.5) = 3.56;
σ_E = 0.202 and σ_E/Γ = 2.87; (19) = 0.218, and 0.0358 for d = 2 with the long packet; the long packet's FWHM 0.120; the
finite-well level 0.744 from (20); (21) = 0.649; hard box 2.193; the V₀ = 1.5 row of the §8 table (Γ from (17) = 0.093); the
ratios 22 and 24; ξ = cos(ks+φ)/√T from tr P; band width 0.365 and gap edge 0.955 + 1.126 = 2.081; the run counts (add up to
3739; every group divides by 47 or matches its stated product); 0.59 rad per step for the diagonal mode; a = 2.75 nm; 110 meV,
10.6 meV, 62 fs; 87 K; the prefactor of (31) from (30) and the 1D flux dE/(2πħ); the supply values 14.2 and 18; the products
1.04 and 0.74; τ_side = 2.28; Figure 3 measured against its own scale (barrier top 1.98, level 0.335, collector fill 0.2: drawn
to scale, as the caption says). All agree with the note.

Two readers. **S** is a school student who is good at mathematics. **G** is a physics graduate. Each mark gives the section,
the exact sentence (as rendered; maths in TeX), who gets lost, and why.

## Marks

### §1 Two panes of glass

1. **§1, "Reading the figures" paragraph.** "Fig. 15b plots the probability per unit length along the flight, divided by the
   total still in the box (the region of space the computation covers, section 10): the 3D run in wine, for walls the
   one-dimensional twin, solved on the same grid, dashed in black, …" S and G. One paragraph of about 330 words describes five
   panels, using words the note has not yet earned: "one-dimensional twin", "absorbing border", "fitted exponential decay of the
   wave trapped between the barriers", "spread of energies a packet holds". Each gets a forward pointer, but on first reading
   this is a wall. It reads as a legend, not as the opening of a chapter; S stops here.

### §2 The model in three dimensions

2. **§2.** "Four pure numbers fix the regime. … And \(\sigma_E/\Gamma=2.9\) for the figure's short packet (section 6)". Symbol
   before definition: \(\Gamma\) is defined in §5 and \(\sigma_E\) in §6. S has no idea what either is. Either say it in words
   here ("the packet's energy spread is about three times the resonance's width") or move the number.
3. **§2.** "\(s/\lambda=2.5/5.18=0.48\): the barrier centres are about half a wavelength apart, close to the condition for the
   first resonance (section 5)." Two problems. \(\lambda\) is never defined as a symbol (the box says only "a wavelength
   \(2\pi/k=5.18\)"), and later \(\lambda\) means an eigenvalue (§9). And G objects to the physics: §5 says the condition is half
   a wavelength in the *effective* width \(L_{\text{eff}}=2.76\), not in \(s\); \(s/\lambda\approx0.5\) is close to that only by
   coincidence (\(s=2.5\) happens to lie near 2.76). As written it suggests the wrong condition.
4. **§2.** "the second equation of (2) has the solution \(g\propto(1+it/2\sigma_\perp^2)^{-1/2}\exp[\dots]\) (substitute it to
   check)." A bare formula: the standard forbids "it can be shown", and "substitute it to check" is the same thing. G accepts it;
   S cannot do the check (complex Gaussian, two derivatives) and is not told where the formula comes from. One sentence (the
   Fourier route: each \(k_y\) component turns by \(e^{-ik_y^2t/2}\)) or a ★ would do.
5. **§2.** "Our packet starts as a Gaussian, …, which is such a product. So it stays a product for all time". G: the step is
   uniqueness (the product solves (1) with the same start, and (1) has one solution). S: the "so" is unsupported. Half a sentence.
6. **§2.** "centred at \(x_0\), 14 before the first barrier face". For the long packet (\(\sigma_x=12\), §6) a start 14 before the
   face would put about an eighth of the packet inside the barrier, yet §10 says the share in a barrier is "at most
   \(2.1\times10^{-5}\)". G: the long packet must start elsewhere; the note does not say where.

### §3 One barrier

7. **§3 ★.** "and conjugating turns a right-mover \(e^{ikx}\) into a left-mover: the amplitudes \((A,B)\) become \((B^*,A^*)\).
   The same matrix must link the conjugated pairs, which forces the second row to be the first row conjugated and swapped."
   G fine. The "forces" is quick: it needs the matrix itself to be built from real \(k\)'s on both outer sides, and one line of
   algebra (\(B^*=M_{11}D^*+M_{12}C^*\) against \(A=M_{11}C+M_{12}D\)). Starred, so acceptable; noted only.
8. **§3.** "(Here \(t\) is an amplitude, not a time; which is meant is always clear from the context.)" One symbol, two meanings,
   against the Taylor rule of 21 October. The note itself has to say "(now a time again)" in §5, which shows it is not always
   clear. Same family: \(R\) is a reflection coefficient and, in §12, a radius; \(w\) is the matrix corner and, in (28), a width;
   \(T\) is transmission and, in §13, temperature; \(\lambda\) a wavelength (§2) and an eigenvalue (§9); \(d\) a thickness and the
   differential in \(d^2k_\perp\), \(dE\). Each is announced, but five announced collisions is a lot for S.

### §4 Two barriers, two ways

9. **§4.** "This agrees with the matrix product to one part in \(10^{9}\) (notes/fig15/derive.py)." Fine for G. The link goes to
   GitHub `main`, where `derive.py` exists; see mark 31 for the others.
10. **§4.** Clear otherwise: the sum over paths, the table of partial sums (Example 4.1) and the physical reading of
    \(|t_2|^2=1\) as cancelled reflection are the best passage of the note.

### §5 The sharp peak and the trapped wave

11. **§5.** "Which whole number \(n\) it is depends on how we count the phase \(\rho\), which is only fixed up to whole turns;
    here \(r\) is close to \(-1\), as for a hard wall, and this first resonance is the one at which about half a wavelength fits
    in the effective width of the well (the distance between the barriers' inner faces, 1.5, plus about \(1/\kappa=0.63\) into
    each barrier, 2.76 in all, against a half-wavelength of 2.59; the next paragraphs make this effective width precise)." S
    lost: one sentence of 80 words with a nested parenthesis, using \(L_{\text{eff}}\) before it is introduced. G asks why
    \(r\approx-1\): the single-step phase is \(-2\arctan(\kappa/k)=-1.84\) rad, and only after the shift to the barrier's centre
    does it come near \(-\pi\). Not said.
12. **§5.** "The Lorentzian. (If you skipped the ★: equation (13) says the pair passes everything when the round trip closes in
    step, and little in between.)" The restatement is good, but the very next step expands (13) itself, so a reader who skipped
    the ★ must read its result anyway. Either unstar (13) (it is three lines of school algebra) or make the Lorentzian follow
    from words.
13. **§5.** "\(\hbar\theta'\) is a time." S: why? \(\theta\) is an angle, \(\theta'=d\theta/dE\) is per energy, \(\hbar\) is energy
    × time. Five words would do it.
14. **§5 ★.** "And the phase also adds the time the wave spends inside the barriers." G: this is the Wigner delay of the
    evanescent region; the sentence asserts it without saying how the \(2/\kappa\) rate that follows contains it. The rest of the
    ★ (the derivative of \(-2\arctan(\kappa/k)\), which I checked: \(2/\kappa\)) is sound.
15. **§5.** "Like every slow leak, the trapped wave loses a fixed fraction per unit time." Out of place: it comes after (16) has
    already been derived from exactly this decay law, so it reads as a stray. Belongs before "Each round trip the trapped wave
    is reflected twice".
16. **§5.** Physical picture: the swing is good; the claim "a narrow line is a slow leak" is well supported.

### §6 A wave packet is not a single energy

17. **§6.** "For a packet centred on the resonance with \(\sigma_E\gg\Gamma\), the packet's energy distribution is nearly flat
    across the peak, with height \(1/(\sqrt{2\pi}\,\sigma_E)\)". G: (18) is written as an integral over \(k\) with \(|\varphi(k)|^2\),
    and (19) silently changes variable to \(E\) (Jacobian \(dE=k\,dk\)). One clause.
18. **§6, "Long packets".** "For the running example the best of the 5 long-packet runs filed so far (of 15 planned for this
    structure) passes 0.51 of the packet at \(E=0.713\), where the exact average for this packet is 0.5 (these runs, made under
    an earlier rule for the run length, stopped more than 15 % before the rule of section 10 would end them, with a little of the
    wave still trapped, so the share reads a few per cent low, and they are due to be rerun), …" Unsupported and self-contradicting:
    the run reads 0.51 against an exact 0.5, i.e. *higher*, while the parenthesis says such runs read *low*. G stops here. S is
    already lost in a run-status report (5 of 15 filed, earlier rule, due to be rerun) inside a teaching paragraph.
19. **§6.** "The run stops 509 time units after it starts, about one lifetime after the trapped wave peaks, and ends with
    0.00736 still between the walls; half of that would still leave forward, which accounts for much of the shortfall; and
    \(\sigma_E=0.051\) is still much wider than \(\Gamma\), and so narrow a peak is also very sensitive to the small shift the grid
    gives it (section 11)." Three semicolons, three explanations, no measure of which dominates ("much of" = 0.0037 of a 0.0094
    shortfall, i.e. about 40 %; say so). Overall the "Long packets" paragraph is ~330 words of bookkeeping; the physics (a longer
    packet has a narrower energy spread and sees more of the peak, 0.196 → 0.54) is one sentence and is buried.

### §7 A wider well sings lower

20. **§7.** "The levels are the energies that solve the first condition below." Read with the preceding sentence, S takes "the
    levels" to mean all levels; only the even ones solve the first condition. Say "the even levels".
21. **§7.** "the outer faces change them only through the small wave that reaches them, a share of about
    \(e^{-2\kappa d}=0.04\)". Claim without support for G: why the shift of the level is of that relative size is not shown, and
    the table's 0.735 vs 0.744 (1 %) is not tied to the 0.04. Minor.
22. **§7.** Clear otherwise: bottle and guitar first, then (20), (21), the table, three reasons from (17). Good.

### §8 Taller and thicker barriers

23. **§8.** Clear. The tea-cup picture, the table with (17) against the exact width, and the honest last paragraph (210 is a
    lower bound) meet the standard. One nit: "a straight line through the logarithm of its decay from \(t=91\), where the trapped
    probability has fallen to 60 % of its peak (the rule of section 11)" points forward to a rule S has not met.

### §9 Three, five and ten barriers

24. **§9.** "with \(U_0=1\), \(U_1=2\xi\). (and \(U_{-1}=0\))." Typo as rendered: a full stop before the parenthesis.
25. **§9 ★.** "The off-diagonal element of \(\mathbf P^N\) is \(U_{N-1}\) times that of \(\mathbf P\)". The reason (the
    \(U_{N-2}\mathbf I\) term has no off-diagonal part) is one clause and is missing.
26. **§9 ★.** "Since \(\mathbf P^N\) has the form (6) too (the travel matrix is diagonal with entries of size 1, so it changes
    only phases), its transmission is one over \(|w_N|^2\)". G: the row of \(N\) barriers is \(\mathbf M(\mathbf D\mathbf M)^{N-1}\),
    not \((\mathbf M\mathbf D)^N\); the parenthesis is meant to say that the extra trailing travel matrix changes only phases, but
    it reads as the reason \(\mathbf P^N\) has form (6), which it is not. Say both things separately.
27. **§9.** "This is the Kronig–Penney condition." G: Kronig–Penney is the square-barrier lattice specifically; (24) with
    \(\xi\) from (22) is the general 1D Bloch condition for any symmetric cell. Fine to name it, but no source is given for either
    (Further reading has none on bands).
28. **§9.** "These runs fall short of the exact values by more than the pair does; a likely cause is that ten barriers repeat
    the small error of each barrier's shape on the grid (section 11) ten times." Hypothesis stated as "likely" with no test; §11
    calls the same cause "possible" and "not tested". Make the two agree.

### §10 What was computed, and how

29. **§10.** "Each half of the split is exact for every Fourier mode, however fast it turns (the fastest the grid holds, along a
    diagonal, turns by 0.59 rad per step, so even it is followed in small turns)". S and G: if each half is exact for every mode,
    why does the speed of the fastest mode matter? The 0.59 rad is offered as reassurance for a danger the sentence has just said
    does not exist. The real point (the splitting error grows with \(k^2\Delta t\) where \(V\) changes) is the clause after it; say
    that, and the 0.59 then means something.
30. **§10.** "about one nanosecond per grid point per time step." Unclear whether this is per GPU, per Fourier transform, or per
    full step; G cannot reproduce "5.9 hours on the clock" from it without knowing how many GPUs ran in parallel.
31. **§10 and §14 (links).** "notes/fig15/gen2_numbers.py, which reads the stored Kaggle runs and their index,
    public/data/resonant-tunnelling/2026-11-14/kaggle/index.json" and, in §11, "(gen1_profile_check.py)". These link to
    `github.com/Numa1997/SiteTest/blob/main/…`, and `origin/main` does not hold `gen1_profile_check.py`, `gen2_numbers.py` or
    the `2026-11-14/kaggle/index.json` (checked with `git cat-file` against a fresh fetch). Until the branch is merged the reader
    gets three 404s. `derive.py` is on main.
32. **§10.** Otherwise clear and complete for item 5 of the standard: integrator (Strang split, order \(\Delta t^2\)), step 0.01,
    grid, border, what is stored, and the "where the picture differs" fold, which states the 8-bit rounding with numbers.
    Missing for item 5: "we have not measured the time-step error on its own" is honest, but the standard asks for the error
    "measured by running the page"; one run at \(\Delta t=0.005\) would close it.

### §11 How good the grid is

33. **§11.** "Dividing by the total removes what the side border took." Claim without support: it holds only if the side border
    removes the same fraction from every region (before, between, beyond). G will doubt it under bias (§13), where the regions
    differ in transverse spread.
34. **§11.** Otherwise clear: the three comparisons (3D vs twin, twin vs exact, lifetime) are measured, named, and the box says
    what they mean for the figure.

### §12 Discs and shells

35. **§12.** "and has spread only a little, to about 3.6 by (3), when it reaches the barriers at \(t\approx11.5\) (14 at speed
    1.21)." The speed 1.21 belongs to \(E=0.735\); the runs this paragraph discusses are at \(E=0.65\), speed 1.14, arrival
    \(t\approx12.3\). The number 3.6 survives, the reasoning does not match the data quoted next. Later "The packet, within about
    3.7 of the axis" (shells) gives a third width without saying at what time.
36. **§12.** "call that width \(w=\min(R,\sigma_\perp)\)." \(w\) is the corner of \(\mathbf M\) since §3 (see mark 8).
37. **§12.** "The fitted lifetime belongs to the resonance the packet feeds, so it hardly depends on the packet's mean energy:
    walls give 15.1 here, as the earlier batch did at 0.735." The claim is supported by one pair of numbers (0.65 and 0.735).
    Acceptable, but S needs the physical reason in a sentence: whatever energies the packet holds, only those inside the
    resonance stay trapped, so the decay is the resonance's.
38. **§12, table.** Of 30 data cells, 13 read "to come"; for discs only \(R=2\) has a lifetime. The key result then says "the
    larger radii, still to come, will show the trend." A first-time reader meets a results table that is mostly empty and a key
    result that is a prediction. Not a reading error, but against "Key result" in the Taylor sense: a key result should be a
    result.
39. **§12.** "much of it is reflected or passes through both shells, and a part is caught inside" S: how does a wave get
    *inside* a closed shell? By tunnelling in, as it later leaks out; the note never says so, and the open-porch picture suggests
    it cannot enter.

### §13 The device

40. **§13.** "The exact calculation gives peak heights 1, 0.877 and 0.559; (11) explains why they fall below 1." G: (11) was
    derived with the same \(k\) on both sides, and two sentences later the note says that under bias \(T=(k_R/k_L)|t|^2\), i.e.
    the sides differ. (11) gives the trend, not the numbers; say "qualitatively".
41. **§13.** "Current flows when the trapped level lies among the filled states on the left." S: why must the level lie among
    the *filled* states, not just below \(E_F\)? Because an electron crosses only at the resonance energy and needs an occupied
    emitter state at that flight energy with energy conserved. The phrase "energy and sideways momentum are kept on crossing"
    is the missing physical step; it is the heart of why the current ever falls.
42. **§13.** "Here \(-e\) is the electron's charge and \(V_b\) the voltage, the bias. In our units we quote the bias by the energy
    \(eV_b\) it gives an electron, in units of \(E_u\), so \(eV_b\) and \(V_b\) are the same number." Then "peaks at \(V_b=0.875\)
    (131 mV)". S may stumble once: \(V_b\) is "a number in \(E_u\)" and also "131 mV". It works (150 meV per unit), but say "0.875
    in units of \(E_u/e=150\) mV".
43. **§13.** Strong otherwise: the GaAs table, Figure 3 (drawn to scale; I measured it), the supply-function ★ with every factor,
    and the "area times supply" explanation of why the peak comes early. The "Why it is useful" box has its source.

### §14 What the model leaves out

44. **§14, Further reading.** All five sources have working DOI links. Missing for item 8: no textbook chapter, though the note
    leans on standard textbook results it does not derive in full (the free Gaussian (3), Breit–Wigner, the Kronig–Penney
    condition, Fermi occupation). For G one chapter (e.g. Griffiths, *Introduction to Quantum Mechanics*, §2.5–2.6 and problem on
    Kronig–Penney; or Davies, *The Physics of Low-Dimensional Semiconductors*, ch. 5) would be the natural next read. Only if it
    is opened and read.
45. **§14, Problems.** Problem 6: "Check your answers against the table when those runs are in." An exercise that cannot be done
    today.

## Verdict per section against notes/STANDARD.md

| § | Title | Verdict | Why (marks) |
|---|---|---|---|
| 1 | Two panes of glass | needs work (light) | Picture is excellent (item 1). The "Reading the figures" paragraph is a wall using undefined terms (1). |
| 2 | Model in 3D | needs work | \(\sigma_E,\Gamma,\lambda\) before definition; the \(s/\lambda\) condition is physically misleading; one bare formula; long-packet start not stated (2–6). |
| 3 | One barrier | clear, leave it | Every step shown, limits checked, example with the page's numbers. Symbol \(t\) double use is a note-wide issue (8). |
| 4 | Two barriers | clear, leave it | Best section. (9, 10) |
| 5 | Sharp peak, trapped wave | needs work (light) | One overlong sentence (11); the ★ boundary around (13) (12); "\(\hbar\theta'\) is a time" unexplained (13); a stray sentence (15). |
| 6 | Wave packet | needs work | The core is clear; the "Long packets" paragraph contradicts itself (0.51 vs 0.5 "reads low") and buries the physics in run bookkeeping (18, 19); \(k\to E\) change of variable (17). |
| 7 | A wider well | clear, leave it | Two one-word fixes (20, 21). |
| 8 | Taller, thicker | clear, leave it | (23) |
| 9 | Bands | needs work (light) | Typo (24); two half-steps in the ★ (25, 26); "likely" vs §11's "not tested" (28). |
| 10 | What was computed | needs work (light) | The 0.59 rad sentence argues against itself (29); time-step error not measured (32); three links 404 until merge (31). |
| 11 | How good the grid is | clear, leave it | One unsupported clause (33). |
| 12 | Discs and shells | needs work | Arrival time computed at the wrong speed (35); mostly empty table and a key result that is a prediction (38); how the wave enters a shell (39). |
| 13 | The device | clear, leave it (one step to add) | The physical reason the level must face filled states (41) is the one missing step; (40, 42) are wording. |
| 14 | Limits, reading | needs work (light) | No textbook chapter (44); a problem that cannot yet be done (45). |

Overall: the note now reads as a textbook chapter in §§3–5, 7–8 and 13; the remaining faults are local. The two that a reader
would actually trip on are the self-contradicting long-packet sentence in §6 (mark 18) and the \(s/\lambda\) resonance condition
in §2 (mark 3). The three broken links (mark 31) fix themselves on merge.

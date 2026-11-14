# Fig. 15 · referee report, round 8 (resonant tunnelling)

Read as rendered, at commit `2e6a7fd` (branch `claude/fig15-gen2-note`). `npm run build` exit 0; `dist/` served on port 8811;
opened in headless Chromium (Playwright) at 1400 px and 390 px; "Expand all" pressed, every `details` opened, each of the 14
sections screenshotted at both widths, and the note's text extracted with each KaTeX formula replaced by its TeX source.
KaTeX: 997 formulas, 0 errors; no page errors. All five DOIs and the four GitHub script links carry `href`s. The 3D panel was
not judged. `plan.md` and `check.md` were not read. Where a number looked wrong, it was recomputed by hand or traced to the
`NUM` block of `public/scripts/resonant-note.js`.

Two readers: **S**, a school student good at mathematics; **G**, a physics graduate. Each mark gives the section, quotes
the rendered sentence, and says who stops and why. Marks 1 to 6 are errors of fact or broken text; the rest are reading stops.

## Errors (fix first)

1. **§6, Long packets.** "Just below the peak the grid passes a little more than the exact theory (section 11). Counting
   that half, the run passes about 0.53 against the exact 0.5, …" There is no "half" for "that half" to point to. In the
   source the clause that defines it ("these runs stopped with 0.00719 still trapped, half of which would still have
   passed …") prints only when `long_rerun_pending` is true, and it is now false. S and G both stop. The sentence needs its
   own antecedent: "The run ends with 0.0072 still between the walls; half of that would still leave forward. Counting it, …"
2. **§11 box "What this means for the figure" and §14.** "lifetimes are 6–8 % long for the running example (12 % at
   s = 3.5, section 7 …)" and in §14 "(12 % at s = 3.5)". Section 7 prints "a lifetime of 68.4, against the exact
   ħ/Γ = 58.3: 17 % longer". 68.4/58.3 = 1.17. The 12 % is hard-coded in the source and stale; it should read 17 %.
3. **§11, last paragraph.** "For walls this reading gave 0.179 against the twin's 0.186, a 4 % gap: the rule counts half of
   the wave still trapped as passed, while the twin counts only what has left." The reason given would make the rule read
   *higher* than the twin, but it reads lower. G stops: the explanation has the wrong sign. The real cause is probably
   that the rule reads at an earlier frame (before a thousandth reaches the border) and divides by what is still in the
   box; whatever it is, the stated reason does not produce the stated direction.
4. **§12, after the disc table.** "The side-leak times solved from (27) grow with the radius, as (28) predicts, and are of
   the size it predicts up to radius 6". From the table: R = 2, 4, 6 give τ_side = 2.15, 4.87, 22.6 against estimates 4,
   12, 18. Between R = 4 and 6, both wider than σ⊥ = 3, (28) predicts growth ×1.5 (linear in R); the runs grow ×4.6. Between
   2 and 4, (28) predicts ×4 (R²); the runs give ×2.3. So the runs do not grow "as (28) predicts", and at R = 4 they are
   2.5 times smaller. G stops. Say only that they grow with R and agree with (28) within a factor of about 2.5 up to radius 6.
5. **§13, The current from the runs.** "its top at V = 0.75 … valley at V = 1.625 … top at V = 0.875 … top moves to
   V = 1.125 … at V = 0.75 …". The note said a few paragraphs earlier, "The plain V stays the potential", and calls the
   bias V_b. Here the bias is written V. One symbol, one meaning: write V_b.
6. **§12, shell table.** The last column is headed "runs so far". The batch is finished (every entry is 47, all runs
   filed). The heading reads as a progress note; "runs" suffices. Also the text "Each longest lifetime falls at or next
   to the lowest energy of the runs, 0.30" — the table shows all four at exactly 0.3, so "at" is the finding, and it means
   the maximum lies at the edge of the computed range: the table's "longest τ" is a lower bound for all four rows, not only
   for the two marked ≥. Say so.

## Header and section 1 · Two panes of glass

7. **§1, Reading the figures (whole paragraph).** About 430 words in one paragraph, with forward references to sections
   2, 5, 6, 10, 12 and 13 and terms not yet defined: "one-dimensional twin" (defined in §10), "absorbing border",
   "fitted exponential decay", "the spread of energies a packet holds". S, reading in order, is lost by the fourth
   sentence. It is a legend card, not prose; it reads better as a collapsible `.pbox` or split one paragraph per panel.
8. **§1.** "Fig. 15b shows the probability along the flight, Fig. 15c …" comes before "(Fig. 15 is the 3D view at the
   top, Figs. 15b to 15e the charts below it; …)". The key to the names follows their use; move the parenthesis first.
9. **§1.** "The electron is a wave; a thin barrier is a partly silvered mirror for it" — S is handed the wave nature as a
   bare fact. One clause pointing to electron diffraction, or to Fig. 3 of this site (double slit), would ground it.
10. **§1, Reading the figures.** "on one scale for the whole run, so that the largest value the run reaches is height 1"
    — the code agrees (S = the run's largest |ψ| on the plane), but the page's own note under the height chips says
    "the start packet's peak is height 1". The two wordings describe the same number only if the peak is at the start.
    One wording on the page and in the note.
11. **Figure 1 caption and Figure 2 caption (rendering, 1400 px).** A line begins with a lone comma: "… E = 0.735 / , the
    energy at which …" and "|ξ| ≤ 1 / , from 0.59 to 0.955." The comma needs to be joined to the formula (put it inside the
    `\( … \)` or use a no-break wrapper).

Verdict §1: picture (STANDARD 4.1) **clear** — the glass panes, the laser mirror and the clap between walls are good.
Equation to screen (4.6) present but **needs work** for form (marks 7, 8, 10, 11).

## Section 2 · The model in three dimensions

12. **§2, A few words.** "they add up to a lump of finite length that moves at the group velocity v = dω/dk = ħk₀/m" —
    group velocity is defined only by a formula. S needs one sentence on why a sum of waves moves at dω/dk, not ω/k
    (two close waves beat; the beat moves at Δω/Δk).
13. **§2.** "Our packet starts as a Gaussian, ψ₀∝…, centred at x₀, 14 before the first barrier face (…), with length σₓ
    along the flight and width σ⊥ across it (the standard deviations of |ψ|²; both 3 for …; section 6 adds a long one),
    which is such a product." The point, "which is such a product", arrives some 60 words after its subject, through two
    parentheses. S loses the thread. Split into two sentences.
14. **§2, What three dimensions add.** "the second equation of (2) has the solution g ∝ (1+it/2σ⊥²)^{-1/2} exp[…]
    (substitute it to check)." For S a formula from nowhere; "substitute to check" is the "it can be shown" STANDARD 4.3
    rules out. Name the route in one clause: each Fourier mode of the Gaussian turns by e^{−ik²t/2}, and the sum of Gaussians
    is the Gaussian shown. G is fine.
15. **§2.** "Along the flight, a state of one energy, χ = χ(x)e^{−iEt}" — χ now names both the time-dependent factor and its
    spatial part. A different letter or "χ(x,t) = χ(x)e^{−iEt}" with the arguments written.
16. **§2, Our running example.** "σ_E/Γ = 2.9 (both defined in sections 5 and 6)" — two symbols used three sections
    before their definitions. A one-line meaning ("the packet's energy spread over the resonance width") would carry S.

Verdict §2: model (4.2) **clear** for G; the separation argument now runs the right way (product → solves (1) → uniqueness).
**Needs work** for S at marks 12–14.

## Section 3 · One barrier

17. **§3 ★.** "and in the same way γ = i(κ²+k²)/(2kκ) sinh κd (both checked against the numerical product)." The top-left
    element is worked; γ is not — "in the same way" plus a numerical check is a silent step for G. One line: the top-right
    element is ¼[(1+iκ/k)(1−k/iκ)e^{κd} + (1−iκ/k)(1+k/iκ)e^{−κd}] = …
18. **§3, Example 3.1.** "T = [1 + 4·144/3.72]^{-1}" — S has to guess that 4 is V₀², 144 is sinh²(3.18) and 3.72 is
    4E(V₀−E). Write the factors as in the Key result above it.
19. **§3, after (6).** "For the square barrier, since κ²+k² = 2V₀ and k²κ² = 4E(V₀−E), (7)" — the unstarred reader has
    skipped the ★ where |w|² = 1 + (κ²+k²)²sinh²/(4k²κ²) was found, so "since" points at nothing they have seen. State that
    line unstarred before (7).

Verdict §3: derivation (4.3) and checks (4.4: two limits, one worked number) **clear**, apart from marks 17–19.

## Section 4 · Two barriers, two ways

20. **§4.** "This agrees with the matrix product to one part in 10⁹ (notes/fig15/derive.py)." A repository path in body text
    is not a reference for S; it is linked only at the end of §14. Link it here or drop the path.
21. **§4.** "Its size |r²e^{2iks}| = R changes slowly with energy, but its phase turns fast." Why fast is not said: 2ks
    changes by 2s·dk, and s is several wavelengths' worth of phase, while R moves only through κ. One clause.

Verdict §4: **clear**. The path sum is the best physical moment of the note; Example 4.1 shows the pile-up with numbers.

## Section 5 · The sharp peak and the trapped wave

22. **§5, The width is the inverse of the time trapped.** One paragraph of about 400 words that opens unstarred, switches
    to ★ in mid-paragraph ("★ The reflection phase 2ρ corrects …") and back ("(End of ★.) In short: …"), then derives the
    decay law, the T³ comparison and (16). S cannot see where to resume. Break the paragraph at the ★ and at "(End of ★.)".
23. **§5.** "after a time t (now a time again)" — t has meant an amplitude since §3; the note flags the switch but the
    collision is avoidable (t_amp or τ_t, or write "a time t′").
24. **§5.** "So width and lifetime are tied by τ = ħ/Γ" — derived only to order T² (the two numerators differ at T³). The
    text says so a line earlier, but the boxed relation then reads as exact. "to this order" after (16).

Verdict §5: derivation and checks (units, two limits, three ways to Γ) **clear** for G; **needs work** for S at mark 22.
Picture (the swing, the bell) **clear**.

## Section 6 · A wave packet is not a single energy

25. Mark 1 (dangling "that half").
26. **§6, Long packets.** One paragraph mixes the running example, the thick barrier, a run-length argument, a grid
    argument and the spectroscopy remark, with eleven numbers. Both readers lose the main line ("a narrower energy spread
    passes more of a narrow peak"). Split at "For thick barriers".
27. **§6.** "(That σ_E = 0.051 is still much wider than Γ is why the exact average itself is small.)" Placed after the
    thick-barrier numbers it is right (Γ = 0.0029), but a few lines earlier the same σ_E was called "comparable" with the
    running example's Γ. Say "much wider than this Γ".

Verdict §6: **clear** in the first half (drum and violin, (18), (19) derived); **needs work** in the long-packet paragraph.

## Section 7 · A wider well sings lower

28. **§7.** Mark 2 (17 % here, 12 % in §11 and §14).

Verdict §7: **clear**. Bottle and guitar, the finite well (20) derived, (21) checked against a table, honest about the 17 %.

## Section 8 · Taller and thicker barriers

Verdict §8: **clear, leave it.** The tea-cup picture, (17) tested row by row, the cap on run length stated.

## Section 9 · Three, five and ten barriers

29. **Figure 2 caption.** Mark 11 (lone comma).
30. **§9 ★.** "The off-diagonal element of Pᴺ is U_{N−1} times that of P … A row of N barriers is Pᴺ with the last
    stretch of travel taken back" — G accepts it; the step "Pᴺ has the form (6) too" deserves its reason (a product of
    matrices of form (6) keeps the form, as the conjugation argument of §3 shows).

Verdict §9: **clear**. Pendulums, Cayley–Hamilton, the unstarred restatement, the Bloch condition and the band numbers.

## Section 10 · What was computed, and how

31. **§10, The grid.** "each step it multiplies the wave by a factor that falls smoothly from 1 … (as sin^{1/8} of the
    distance into the border), so the wave fades over many steps, so a wave leaving the box fades out instead of coming
    back on the other side" — two "so" clauses in a row, and "sin^{1/8} of the distance" has no scale (sin of what multiple
    of the distance?). G cannot reproduce the border from this.
32. **§10, The step.** STANDARD 4.5 asks why the method and step were chosen, where they fail and the error to expect.
    The note states the order and admits "we have not measured the time-step error on its own". One line of the page's own
    numbers would carry it: V₀Δt = 0.02 rad and k₀²Δt/2 ≈ 0.007 rad per step, the highest grid mode k = π/0.5 turns by
    about 0.2 rad per axis; the split is unitary, so it never blows up, and it fails only when those phases approach π.
33. **§10.** "about one nanosecond of GPU time per grid point per time step" — unsupported; no measurement is named, and it
    cannot be checked against "18.6 hours of computing summed over the seven" because that sentence does not say whether
    it is wall time or GPU time (each part ran on two GPUs).
34. **§10, The runs.** The paragraph is an inventory (seven groups, counts, reruns, duplicates). Correct (3739 − 42 = 3697
    checks), but S is lost and nothing in it is used later except the run length. A `.ptab` would carry it in a third of
    the space.

Verdict §10: method (4.5) **needs work** (marks 31–33). The box "Where the picture differs from the stored data" (4.6) is
**clear** and complete.

## Section 11 · How good the grid is

35. Marks 2 and 3.
36. **§11.** The rules by which the lifetime and the share are read appear in the last paragraph, after the results that use
    them, and §5 already pointed here for "the exact rule". Move that paragraph to the top of the section.
37. **§11.** "(gen1_profile_check.py)" — a bare file name; link it or drop it.

Verdict §11: **needs work** for the two errors; otherwise a model of how to measure a computation's error against exact theory.

## Section 12 · Discs and shells

38. **§12.** "Shrink the walls to discs of radius R … (in this section R is a radius; the reflection coefficient does not
    appear)" — the note's own rule (one symbol, one meaning) is broken and patched; R is the reflection coefficient again
    in §14 and in (23). A different letter for the radius (for example ρ_d or b) avoids the patch.
39. **§12.** "when it reaches the barriers at t ≈ 12 (14 at a speed of about 1.2)" — cryptic; "14 units of distance at a
    speed of 1.2".
40. **§12.** "How fast is the side leak?" — a rhetorical question, which the 21 October verdict forbids. "The side leak
    is set by …".
41. Marks 4 and 6.
42. **§12, Shells.** "We have not worked out their energies here." With u = rψ reducing the shells to a double barrier
    behind a hard wall, the §7 machinery gives the levels in a line; G expects at least the lowest one, since all four
    longest lifetimes sit at the lowest computed energy and the reader wants to know whether a level lies below 0.30.

Verdict §12: picture (bathtub, room with doors shut) **clear**; claims **need work** (marks 4, 6, 40).

## Section 13 · The device

43. Mark 5 (V for V_b).
44. **§13.** "The products, 1.04 at V_b = 0.875 and 0.74 at 1.25 (in the units of (32))" — forward reference to units given
    only after (32). Say "(a pure number times an energy)".
45. **§13.** "from 3.46 at V = 0.75 it falls only to 2.82 at the last voltage computed, 2.375, a ratio of 1.2 over the
    range, against 0.96 at the top of the walls' curve." Read in sequence, "against 0.96" compares with the ratio 1.2;
    it is the walls' peak *current*. "… a ratio of 1.2. Its top, 3.46, is over three times the walls' top, 0.96."
46. **§13, The current.** "and it passes freely only if E matches the trapped level" — conservation of E and k⊥ is the key
    physical step; for S one sentence of picture ("the barriers are smooth sheets: they push only along the flight, so
    the sideways motion is untouched") would make it stick.

Verdict §13: **clear** for G (supply function derived step by step, units given, peak/valley checked against exact).
**Needs work** on symbols (marks 5, 44, 45).

## Section 14 · Limits and reading

47. Mark 2 (12 % → 17 %).
48. **§14, Further reading.** All five sources are research papers. STANDARD 4.8 asks for textbook chapters and lecture
    notes too; S has nowhere to start. One textbook chapter (for example Griffiths, *Introduction to Quantum Mechanics*,
    the chapter on scattering in one dimension, or Davies, *The Physics of Low-Dimensional Semiconductors*, on resonant
    tunnelling) would serve, if the writer opens it first.

Verdict §14: limits (4.7) **clear** — scattering, space charge and hysteresis, effective mass, the next model named.
Problems box present. Reading **needs work** (mark 48).

## Summary

The physics is sound and the derivations are complete for G; I re-derived (5), the ★ element of (6), (7)–(13), (15), the
T³ comparison, the ★ average, (19), (20)–(23), (30)–(31) and the GaAs unit conversions (a = 2.754 nm, ħ/E_u = 4.39 fs,
k_BT = 0.05 → 87 K) and found them right. Six errors must be fixed: a dangling "that half" (§6), a stale 12 % (§11, §14),
an explanation of the wrong sign (§11), an overstated agreement with (28) (§12), V for V_b (§13), and the shell table's
stale heading and edge-of-range maximum (§12). For S the main stops are the §1 legend paragraph, group velocity, the
spreading Gaussian given without route, and the §5 paragraph that enters and leaves ★ in mid-flow.

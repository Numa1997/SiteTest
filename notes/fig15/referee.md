# Fig. 15 · referee report, round 10 (resonant tunnelling)

Read as rendered at commit `4bae4a5` (branch `claude/fig15-gen2-note`, "round 9 fixes"). `npm run build` exit 0; `dist/`
served on port 9845; opened in headless Chromium (Playwright 1.63) at 1400 px, "Expand all" pressed, each of the 14
`section.psec` screenshotted; the text extracted with every KaTeX formula replaced by its TeX source. KaTeX: 1056 formulas,
0 errors, no page errors. At 390 px the document is 390 wide and no display equation, table or figure overflows.
`plan.md` and `check.md` were not read. The 3D panel was not judged.

Numbers re-derived while reading (Python, from the note's own formulas): T = 0.14395, |w|² = 6.95, Example 3.1, (9) = 0.154,
Example 4.1 (all seven entries, from (1 − R^{ν+1})²), ρ and n = 0, L_eff = 2.757, 2L_eff/v = 4.55, −2 ln R = 0.3109,
2T/√R = 0.3112 (the note's 0.3108 and 0.3111 differ in the last digit, as from the unrounded E_r; not marked), 2T = 0.2879, Γ(17) = 0.0632, T/(2−T) = 0.078, σ_E = 0.202 and 0.0505 (FWHM 0.119), (19) = 0.218 and
0.0359, the long-packet percentages (32 %, 31 %), the hard-box and (21) values of §7, every κd, T and Γ(17) of the §8 table,
the band numbers of §9, k_max²Δt/2, the 3739 / 3697 run count (42 = 2 × 21 shared energies), σ_⊥(12) = 3.6 and
σ_⊥(40) = 7.3, τ_side from (27) for every disc row (and the 76.1 / 88.5 from rounded values), the disc ratios 1.14 / 1.06 /
0.99, the GaAs table (a = 2.754 nm, 4.39 fs, 10.6 meV, 62 fs, 87 K), the supply numbers 14.2 and 18 and the products 1.03
and 0.73 of §13, the supply-function algebra (30)–(31). All agree with the note to its printed precision, except the two
items marked below.

Two readers: **S**, a school student good at mathematics; **G**, a physics graduate.

## Errors (fix first)

E1. **§10, "The step", the phase per step.** "the fastest wave the grid can hold, \(k=\pi/\Delta x=6.28\), turns its phase by
    \(k^2\Delta t/2=0.2\) rad per step, so no part of the wave turns by more than a fifth of a radian in one step." The grid
    is three-dimensional: the fastest mode is the corner of the Fourier box, \(|\mathbf k|^2=3(\pi/\Delta x)^2\), which turns
    by 0.59 rad per step. The "no part" claim is false as written. Either say "along any one axis" or give 0.6 rad for the
    corner mode (and say that these modes carry almost nothing of the packet).

E2. **§11, last paragraph.** "this reading gives 0.178 against 0.187 from the same run's twin, a 4.5 % gap." From the
    printed numbers the gap is 4.8 % (1 − 0.178/0.187) or 5.1 % (0.187/0.178 − 1); a reader who checks cannot get 4.5 %.
    Print the gap from the same rounded values, or print three-figure values that give 4.5 %.

## Reading stops, in note order

1. **§2, separation of variables, still unstarred.** "Call the first bracket's function \(f_1(t)\) … Multiply \(\chi\) by
   \(e^{iF_1}\) … The wave itself, their product, then gains the phase \(e^{i(F_1+F_2+F_3)}\), which is 1 …" This is the
   heaviest step of the section and S has no exit; the plain result ("the product is the solution for all time … along the
   flight it does exactly what a one-dimensional electron does") arrives a paragraph later, after the packet. Mark the
   phase-removal argument ★ and restate its result in one plain sentence right after (2).
2. **§2, order of the argument.** "… which starts \(4\sigma_x=48\) before the first face. Back to the general argument.
   Conversely, if \(\chi\) and \(g\) solve (2), their product solves (1)." "Back to the general argument" is a visible seam:
   the packet paragraph interrupts a derivation. Move the "Conversely …" sentence up to follow (2) directly, then describe the
   packet; the uniqueness sentence ("The start is such a product …") then follows the packet naturally.
3. **§2, symbol before definition (G).** In "Then \(F_1+F_2+F_3\) … is 1 because the three \(f\) add up to zero": the
   integrals are fixed only up to constants, so the sum is a constant, not zero. Say "choose the constants of integration so
   that the sum is zero" (one clause).
4. **§3, no picture of the wave inside a barrier.** Still nowhere a sentence that says what \(\chi\) looks like across one
   barrier (ripples, a smooth fall by \(e^{-\kappa d}\), smaller ripples beyond) and where to see it (Fig. 15b, the tail
   inside the shaded barrier). The §2 box says "it falls by 0.204", which is the number but not the picture.
5. **§5, ★ opened mid-paragraph.** "… at the group velocity. ★ The reflection phase \(2\rho\) corrects this …" The star sits
   in the middle of a running paragraph; S does not see where to resume. "(End of ★.) In short: …" is good; put the ★
   passage in its own paragraph so the skip is visible.
6. **§5, "This is the exponential law of any slow leak."** The sentence follows (16), \(\tau=\hbar/\Gamma\), but refers to
   the decay \(e^{-t/\tau}\) two sentences before. S reads it as describing (16). Move it next to \(R^{2t/t_{\rm rt}}=e^{-t/\tau}\).
7. **§6, "Long packets", paragraph after the table.** The order jumps: running example, then \(V_0=3\), then back to the
   running example ("For the running example the long packet passes far more than the short one does at the peak,
   \(\bar T=0.196\)"), then the thick barriers. The sentence about the running example belongs before the \(V_0=3\)
   sentence. The thick-barrier part still packs 509, 344, 39 %, \(\sigma_E=0.051\), 0.744, 0.0359, 0.0351 into five
   sentences; with the table now holding the shares, this is readable for G, still heavy for S.
8. **§7, a parenthesis inside a formula sentence.** "Then a whole number \(n\) of half-wavelengths fits in (this \(n\) starts
   at 1, so it labels the lowest resonance, \(n=0\) in section 5, as \(n=1\); only the label differs) \(L_{\text{eff}}=L+2/\kappa\),
   \(k=n\pi/L_{\text{eff}}\), and". The parenthesis splits "fits in" from its object; S loses what fits in what. Move the
   parenthesis after (21).
9. **§8, last paragraph, fit window.** "a straight line … from \(t=92.7\), where the trapped probability has fallen to 60 % of
   its peak … to the end gives 210". G wants to know when the run ends relative to that start (217 − 92.7 = 124, about a third
   of a lifetime): say that the window is only a third of a lifetime, which is the real reason the fit cannot measure 344.
10. **§10, "The runs", the 42 shared runs.** "42 of the runs belong to two groups at once (the diode's points at zero voltage
    are also pairs of the first group)". S computes 2 × 25 = 50 diode runs at zero voltage and stops. Add "those at the 21
    energies from 0.30 up, which both groups use".
11. **§10, "What the page does", dangling "it".** "… which matters only for the small part of the wave that reaches it.
    Between two stored frames … it first undoes the steady turning of the phase". The last "it" before was the border; the
    subject here is the page. Write "the page first undoes".
12. **§12, Shells, first paragraph, one run-on sentence.** "The packet, within about 3.6 of the axis, meets the shells
    head-on: much of it is reflected, or tunnels straight through: in through the outer shell and the inner one, and out
    again …, four crossings in all, and a part tunnels through the outer shell, is caught in the gap … and rings there for a
    long time, because …" Three colons and four clauses in one sentence; S cannot parse it. Split into three sentences:
    reflected; tunnels straight through (four crossings); caught and rings.
13. **§12, Shells, second paragraph.** "(for such a wave \(\nabla^2\psi=\tfrac1r\,d^2(r\psi)/dr^2\) … centrifugal barrier,
    \(l(l+1)/2r^2\) …, which we do not treat)". Correct and now complete for G, but this is unstarred graduate material in the
    middle of a sentence. Either ★ the parenthesis or put the plain picture first ("a wave spread evenly round the centre
    behaves along the radius like the wave between walls, with a hard wall at the centre").
14. **§13, Figure 3 and Figure 2 labels.** "filled up to EF", "filled up to EF − eVb", "level at Vb = 0" are set upright
    with text subscripts; "N = 2 … N = 10" in Figure 2 are upright, while the body and captions set \(E_F\), \(V_b\), \(N\) in
    KaTeX italic. Two styles for one symbol. Minor.
15. **§13, "The tilt", the share under bias.** "the share that crosses is the flow of probability, \(T=(k_R/k_L)\,|t|^2\)".
    The same paragraph quotes peak heights 1, 0.877, 0.559 and §13 later 0.65 and 0.34; G wants one word that these heights are
    of this flux-weighted \(T\), not of \(|t|^2\).
16. **§14 / Further reading, links (state, not prose).** `notes/fig15/gen2_numbers.py`, `notes/fig15/gen1_profile_check.py`
    and `public/data/resonant-tunnelling/2026-11-14/kaggle/index.json` are linked on GitHub `main`, where they do not exist
    yet (`git cat-file -e origin/main:…` fails); they resolve only after this branch is merged. `derive.py` and the
    2026-11-13 index are on `main`. Check after the merge.

Fixed since round 9 and not repeated: caption commas bound to their formulas (Figs. 1, 2); the Fig. 15c pointer to
section 11; the laser sentence of §1; the σ_E/Γ box now says it in words; the 2L_eff closing clause in the §5 ★; (19)'s
11 % gap explained; the long-packet numbers in a table; the §8/§12 reconciliation; reasons for Δx and Δt; the bridge to the
earlier batch in §11; (19) cited for "narrower"; the disc yardstick row; the key-result wording on ratios; the centrifugal
term; the current-flow condition; (11) now said to give the reason, not the size.

## Verdict per section (against `notes/STANDARD.md`)

| § | title | verdict | marks |
|---|---|---|---|
| 1 | Two panes of glass | clear, leave it | none |
| 2 | The model in three dimensions | needs work (small): star the phase argument, close the seam, one clause on constants | 1, 2, 3 |
| 3 | One barrier | clear; one sentence of picture missing | 4 |
| 4 | Two barriers, two ways | clear, leave it | none |
| 5 | The sharp peak and the trapped wave | clear; layout of the ★ and one misplaced sentence | 5, 6 |
| 6 | A wave packet is not a single energy | needs work (small): reorder the paragraph after the table | 7 |
| 7 | A wider well sings lower | clear; move one parenthesis | 8 |
| 8 | Taller and thicker barriers | clear; one clause on the fit window | 9 |
| 9 | Three, five and ten barriers | clear, leave it | 14 (labels only) |
| 10 | What was computed, and how | needs work (small): the 3D phase-per-step claim is wrong | E1, 10, 11 |
| 11 | How good the grid is | needs work (small): the 4.5 % does not follow from the printed numbers | E2 |
| 12 | Discs and shells | needs work (small): split the shells sentence; star or soften the radial equation | 12, 13 |
| 13 | The device | clear; label style and one word on the flux-weighted T | 14, 15 |
| 14 | Limits and reading | clear, leave it (links resolve after merge) | 16 |

Overall: the note is correct and reads as a textbook chapter; two small factual slips (E1, E2), no wrong equation. The stops
that matter most for S are 1, 8 and 12; for G, E1, 3 and 9.

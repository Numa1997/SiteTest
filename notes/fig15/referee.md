# Fig. 15 · referee report, round 9 (resonant tunnelling)

Read as rendered at commit `8aa4802` (branch `claude/fig15-gen2-note`). `npm run build` exit 0; `dist/` served on port 8923;
opened in headless Chromium (Playwright) at 1400 px, "Expand all" pressed, each of the 14 sections screenshotted; the text
extracted with every KaTeX formula replaced by its TeX source. KaTeX: 1010 formulas, 0 errors, no page errors. At 390 px no
table, figure or display equation overflows (document width 390). `plan.md` and `check.md` were not read. The 3D panel was
not judged.

Numbers re-derived independently while reading (Python, from the formulas of the note, not from the repository's scripts):
k, κ, e^{-κd}, T = 0.144, |r| = 0.925, (9) = 0.154, Example 3.1 (22.5), Example 4.1 table, ħθ′-free checks
(−2 ln R = 0.3108, 2T/√R = 0.3111, 2T = 0.2879), Γ from the half-maximum of (13) = 0.0704, (17) = 0.0633, L_eff = 2.76,
(21) = 0.649, the phase-averaged T/(2−T) = 0.078, σ_E = 0.202, (19) = 0.218, packet averages (18) 0.196 (pair) and 0.149
(one barrier), long packet 0.54 / 0.500 at E = 0.713, thick-barrier averages 0.0351 / 0.0319, band edges 0.590 / 0.955 /
2.082 and ξ = 0 at 0.735, σ_⊥(12) = 3.6 and σ_⊥(40) = 7.3, the GaAs table (a = 2.75 nm, 4.39 fs, 62 fs, 10.6 meV,
k_BT = 0.05 → 87 K), the 3739-run count by group, τ_side from (27) for every disc row, the tilted peaks (0.486, 0.230 at
V_b = 0.5, 1 on a 300-step staircase; heights 0.878, 0.562) and the Tsu–Esaki curve (top 0.875, valley ≈ 1.81–1.825,
ratio 4.3). All agree with the note to its printed precision.

Two readers: **S**, a school student good at mathematics; **G**, a physics graduate.

## Errors (fix first)

None. No wrong number, wrong equation or broken sentence was found. The round-8 error (the dangling "that half" in §6)
is fixed: the sentence now defines the half before using it.

## Reading stops, in note order

1. **§1, Figure 1 caption and §9, Figure 2 caption (rendering).** "… and \(E=0.735\)⏎, the energy at which …" and
   "… \(|\xi|\le1\)⏎, from 0.59 to 0.955". In both captions the comma after an inline formula breaks onto the next line
   at 1400 px. Both readers see a line starting with a comma. Bind the punctuation to the formula (put it inside the
   `\( \)` or join with a no-break span).
2. **§1, Fig. 15c bullet.** "The dashed curve is an exponential decay fitted to the wave trapped between the barriers
   (section 5)." Section 5 only defers to section 11, which states the fit rule (60 % to 5 % of the peak). G looks for the
   rule and has to chase it twice. Point to section 11.
3. **§1, first paragraph.** "This is a Fabry–Pérot interferometer, the principle of a laser's mirrors." S cannot tell what
   "the principle of a laser's mirrors" means. The intended claim is that a laser's two mirrors form such a cavity; say so.
4. **§2, box "Our running example".** "\(\sigma_E/\Gamma=2.9\)": both symbols are used before they are defined (the box
   admits it, "two quantities we work out in sections 5 and 6"). S has a number without a meaning at this point. A
   half-clause in words ("the packet's spread of energies is about three times the width of the resonance") would carry it
   without the symbols.
5. **§2, separation of variables (unstarred).** "Such a function \(f(t)\) can be removed by multiplying that bracket's
   factor … by the phase \(e^{+i\int f\,dt}\) … The three functions \(f\) must add up to zero …" This is the heaviest step
   of the section and it is not marked ★; S loses the thread here, and the restatement ("the product is the solution for
   all time …") comes only after a paragraph about the packet. Either star the argument or move the plain result up.
6. **§2, order of the argument.** "Our packet starts as a Gaussian, and the Gaussian \(\psi_0\propto\dots\), is such a
   product. … Conversely, if \(\chi\) and \(g\) solve (2), their product solves (1)." The "Conversely" belongs to the
   derivation before the packet paragraph; placed after the packet's size and start position it reads as if it followed
   from them. Also a stray comma: "the Gaussian … , is such a product".
7. **§3, no picture of the wave inside a barrier.** The transfer matrix is derived carefully, but nowhere does the note
   show (or describe in a sentence) what \(\chi\) looks like across one barrier: oscillating, then a falling exponential,
   then a smaller oscillation. S would understand "tunnelling" from Figure 1 only as a shaded box. One sentence pointing
   to Fig. 15b (where the decaying tail is visible inside a barrier) would supply the picture.
8. **§3 and later, one symbol, several meanings.** \(t\) is a time and an amplitude (§3 flags it), \(R\) is the reflection
   coefficient and a disc radius (§12 flags it), \(T\) is the transmission and a temperature (§13 flags it), \(n\) counts
   resonances from 0 in §5 and from 1 in §7 (flagged). Every clash is announced, so no one is misled, but the house rule
   (Taylor verdict, point 2) is "one symbol one meaning". \(R_d\) or \(\varrho\) for the radius and \(\Theta\) or
   \(k_BT\) written only as one unit for temperature would remove two of them.
9. **§5, the ★ on the reflection delay.** "And the phase also adds the time the wave spends inside the barriers." G
   stops: the next sentences compute only the step's reflection delay \(2/\kappa\) (from the face) and do not say how the
   "take back \(2d\)" and the "+\(2/\kappa\) per reflection" combine into \(2L_{\text{eff}}=2(s-d)+4/\kappa\). The result
   is right; one clause ("two reflections per round trip, each delayed by \(2/\kappa\), so the round trip is
   \(2(s-d)+4/\kappa\)") closes the step.
10. **§6, Long packets, the thick-barrier paragraph.** Eleven numbers in six sentences (0.7432, 0.0197, 0.023, 0.0351,
    0.7215, 0.0225, 0.026, 0.0319, 509, 344, 0.00736, 39 %). S cannot hold them; the point (the long packet still sees a
    resonance much narrower than itself, and the run ends before it drains) is buried. A two-row `.ptab` like the one in
    §7 would carry the numbers and leave the prose its point.
11. **§6, (19) at σ_E/Γ = 2.9.** "Equation (19) gives \(\bar T\approx0.218\); the exact average (18) is 0.196." (19) was
    derived for \(\sigma_E\gg\Gamma\); G wants one clause saying the 11 % gap is the price of using it at a ratio of only
    2.9, which the later thick-barrier agreement (ratio 17, gap 2 %) confirms.
12. **§8, last paragraph.** "early in the decay the parts of the packet off resonance are still draining faster, and a fit
    that sees only that stretch reads short." §12 then asserts "The fitted lifetime belongs to the resonance the packet
    feeds … so it hardly depends on the packet's mean energy." G sees the two side by side and wants the reconciliation
    (the off-resonant parts are gone by the time the 60 %-to-5 % window opens, except when the run is cut short, as here).
13. **§10, the numerical method: why these steps.** Standard item 5 asks why the step sizes were chosen and where they
    fail. The note gives \(\Delta x=0.5\) and \(\Delta t=0.01\) without the reason. G wants the two numbers that justify
    them: the running example's wavelength 5.18 is about 10 grid points, and the fastest grid mode (\(k_{\max}=\pi/\Delta x
    =6.3\)) turns by \(k_{\max}^2\Delta t/2\approx0.2\) rad per step. "Splitting is exact where the two commute" is fine;
    "we have not measured the time-step error on its own" is honest but leaves the reader without an expected size.
14. **§11, first paragraph.** "The measurements below were made on the running example in an earlier batch of 115 runs."
    Every grid-quality number of the section comes from runs the page does not play. G accepts the method ("exactly the
    method, grid and step"), but the only bridge to the present batch is §12's "walls give 15.1 at E = 0.75, as the earlier
    batch did at 0.735". Say that bridge here, where the doubt arises.
15. **§11, "a lower share through at the peak … say the grid's peak is a little narrower".** S does not see why a lower
    share means a narrower peak. The link is (19): for a packet wider than the resonance the share is proportional to
    \(\Gamma\). Cite (19).
16. **§12, discs table.** "one disc" for radius 12 is printed "0.16" while every other entry has three figures; the walls
    row has "—" in that column although the single-wall runs exist (§10, "each barrier alone, for walls …"), so the
    yardstick the next paragraph describes is missing exactly for the case it is measured against.
17. **§12, Key result.** "the narrower the discs, … the less the pair gains over one disc at the resonance." The gains
    read from the table are 0.023, 0.025, 0.024, 0.015, −0.006 for radius 12, 9, 6, 4, 2: flat from 12 to 6, then
    falling. "Below radius 6" would be what the table supports.
18. **§12, Shells.** "For the part of the wave that is the same in every direction, \(u=r\psi\) obeys the same
    one-dimensional equation … We have not worked out their energies here." G stops twice: the packet arrives from one
    side and so is mostly not the part that is the same in every direction (the other parts feel an extra centrifugal
    barrier, which the note does not mention), and the shells' lifetimes are the only results in the note compared with
    no theory at all. One sentence on the centrifugal term would supply the physical picture; the missing comparison should
    at least be named in §14 as a limit.
19. **§13, "The current".** "Current therefore flows when the trapped level lies among the filled states on the left."
    With \(E_F=1\) the level (0.735) is among the filled states on the left at zero voltage, where the current is zero.
    S stops. The condition needs its second half, which Figure 3's caption has: "… and above the filled states on the
    right, so few electrons flow back."
20. **§13, the tilt.** "The exact calculation gives peak heights 1, 0.877 and 0.559; (11), which assumes the same wave
    number on both sides, explains why they fall." The claim of explanation has no number behind it. G wants
    \(T_a\), \(T_b\) at \(V_b=0.5\) and the value of \(4T_aT_b/(T_a+T_b)^2\) beside 0.877.
21. **§13, Figure 3 labels.** "filled up to E_F", "level at V_b = 0", "eV_b" are set as plain label text with text
    subscripts, while the caption and body set the same symbols in KaTeX italic. Minor, but the reader sees two styles for
    one symbol.
22. **§14 / Further reading, links (state, not prose).** The links to `notes/fig15/gen2_numbers.py`,
    `notes/fig15/gen1_profile_check.py` (§11) and `public/data/resonant-tunnelling/2026-11-14/kaggle/index.json` point to
    `main`, where these files do not exist yet (`git cat-file -e origin/main:…` fails); they resolve only after this branch
    is merged. `derive.py` is on `main`. Not an error of the note, but check after the merge.

## Verdict per section (against `notes/STANDARD.md`)

| § | title | verdict | marks |
|---|---|---|---|
| 1 | Two panes of glass | clear; two small fixes | 1, 2, 3 |
| 2 | The model in three dimensions | needs work (small): star or reorder the separation argument; undefined σ_E/Γ in the box | 4, 5, 6 |
| 3 | One barrier | clear; a missing picture of the wave in the barrier | 7, 8 |
| 4 | Two barriers, two ways | clear, leave it | none |
| 5 | The sharp peak and the trapped wave | clear; one clause missing in the ★ | 9 |
| 6 | A wave packet is not a single energy | needs work (small): the thick-barrier paragraph is a wall of numbers | 10, 11 |
| 7 | A wider well sings lower | clear, leave it | none |
| 8 | Taller and thicker barriers | clear; one reconciliation with §12 | 12 |
| 9 | Three, five and ten barriers | clear, leave it (caption comma only) | 1 |
| 10 | What was computed, and how | needs work (small): reasons for Δx and Δt (standard item 5) | 13 |
| 11 | How good the grid is | clear; two one-clause links | 14, 15 |
| 12 | Discs and shells | needs work (small): table yardstick, key-result wording, shells' physical picture | 16, 17, 18 |
| 13 | The device | needs work (small): the current-flow condition is half stated | 19, 20, 21 |
| 14 | Limits and reading | clear, leave it (links resolve after merge) | 22 |

Overall: the note is correct throughout and reads as a textbook chapter; no stop is an error of fact. The stops that
matter most for S are 5, 10 and 19; for G, 9, 13 and 18.

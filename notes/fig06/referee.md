# Fig. 6 · referee report on the lecture note

Page: `public/simulations/wave-interference.html`, note "Adding waves: beats, square waves and the spectrum".
Read blind (no plan.md, check.md or teacher report), as two readers: a school student good at mathematics and a physics graduate.
Judged against `notes/STANDARD.md`, with Numa's verdicts first: only real obstacles (A) decide a section's verdict;
matters of taste (B) are listed so the lead can see them and leave them.

## How it was read

- Built with `APPDEPLOY_VITE_OUT_DIR=/tmp/fig06-ref-dist npm run build`. The built page is byte-identical to the source page.
- Served `/tmp/fig06-ref-dist` with a small Node static server on port 8706. Opened in headless Chromium 1194 (Playwright), 1440 × 900.
  Pressed **Expand all**. All 15 folds of the note reported `aria-expanded = true`. No console errors and no failed requests.
- The rendered text was read with each KaTeX formula replaced by its TeX source. Screenshots of every section and every figure are in `notes/fig06/shots/`:
  `00-head`, `01-p-sound` … `09-p-limits`, `10-refs` (tall sections split into 1400 px pieces), plus `fig-1` … `fig-4` and `fig-5-ptab` (the Gibbs table).
- Every number the note quotes from the page was checked, either on the running page or by recomputing it. All of them agree (table at the end).
  The links in Further reading were also checked. Three resolve directly. Feynman ch. 50 was confirmed in Chromium. Feynman ch. 48 was confirmed through Firecrawl,
  because Cloudflare refuses curl and headless Chromium there; its title reads "Ch. 48: Beats".

## Section by section

### Abstract and head
(A) none. (B) none.

### 01 · Many sounds, one eardrum
(A) none. The guitar beat, the headphone, the synthesizer, the violin, the clarinet and the cochlea come before any symbol. This is the physical picture the standard asks for, and it is sound physics.

(B)
- "The low notes of a clarinet are dominated by the odd multiples, which is why a square wave, built from odd multiples alone, sounds hollow, a little like a clarinet." The causal link is odd: the clarinet's spectrum is not *why* a square wave sounds hollow. Taste only.

**Verdict: clear.**

### 02 · The model
(A) none. Equation (1), the coefficients (2), the three facts about the sliders and Figure 1 are complete. Every symbol is defined where it first appears.

(B)
- Figure 1: the legend calls the dark curve "at time t". But the dot on it is labelled \(A_i\sin\varphi_i\), which is the height at \(X=0\) only at \(t=0\). The caption also says "the phase \(\varphi_i\) fixes the height \(A_i\sin\varphi_i\) at \(X = 0\)" without "and \(t=0\)". The text above the figure has it right ("at \(X = 0\) and \(t = 0\)"), so nobody gets lost. The fix would be two words ("at \(t = 0\)").
- "px" is the medium's own length unit, and it is not a screen pixel: the 800 px view is drawn 770 screen pixels wide at 1440 × 900. The note relies on this difference in §7 and §8 ("1 px of displacement is drawn 1.83 pixels tall"), but it never says so in §2. §9 even calls the unit "pixels of that window". The wording in §7–8 keeps the two apart, so the reader is not lost. One clause in §2 would remove the doubt.
- The figure caption above the note writes the formula with lowercase \(x/200\). The note uses \(X\) for position, and in §5 uses \(x\) for the dimensionless phase \(2\pi\cdot0.4(X/200-t)\). The caption lies outside the note.

**Verdict: clear.**

### 03 · Waves simply add (with 3.1 Two waves of one frequency make one wave)
(A)
1. **Cosine rule with a plus sign, step not shown.** "Adding waves of one frequency is adding arrows tip to tail (Figure 2), and the length of the result follows from the cosine rule:
   \(C^2 = A_1^2 + A_2^2 + 2A_1A_2\cos(\varphi_1 - \varphi_2)\) (6)."
   A school student knows the cosine rule as \(c^2=a^2+b^2-2ab\cos\gamma\), with a minus sign. The plus here comes from the angle inside the triangle of Figure 2, which is \(\pi-(\varphi_2-\varphi_1)\), and from \(\cos(\pi-\alpha)=-\cos\alpha\). The note says neither. 3.1 carries no ★, so this is exactly the reader who will try to reproduce (6) and fail. The checks in the next sentence (in step, half a turn apart) confirm the sign but do not explain it.
   Smallest fix: one clause, e.g. "…from the cosine rule; the angle inside the triangle is \(\pi-(\varphi_2-\varphi_1)\), which turns its minus into a plus:".

(B)
- "\(\mathcal{L} = \partial_t^2 - v^2\,\partial_X^2\)": the subscript notation \(\partial_t\) is not introduced. A reader can match it to (3).
- "When you give the waves different Speeds, each obeys its own equation and the page adds them anyway." A graduate may ask whether adding is then still justified. It is: a real dispersive medium is still linear, with one equation whose speed depends on frequency. Half a sentence would close this. The word "imitates" already keeps the claim honest.
- 3.1 uses Euler's formula without ★. The arrow picture (Figure 2) and the cosine rule carry the school reader past it, so this is fine.

Rendering defect, not prose (it does not count toward the verdict, but should be fixed). At 1440 × 900 the number of equation (5) is cut off. The display box is 671 px wide and its content 703 px, with `overflow-x: auto`, so only a "(" sliver shows at the right edge (`shots/03-p-super-01.png`). Equation (5) is cited again in Figure 2 and in §6 ("by (5)"), and a reader looking back finds an equation with no visible number. The fix belongs to the markup of (5), for example moving "\(C e^{i\psi} = \dots\)" to its own line.

**Verdict: needs work** (item A1 only: one clause).

### 04 · Beats (with 4.1 The speed of the envelope ★ and Exercise 4.1)
(A) none. The derivation (7)–(8) is complete. The argument that \(|\cos|\) repeats every \(\pi\) is given in words, so "the full difference, not half" is earned. Figure 3, the group-velocity paragraph (ocean swell), and every number in Exercise 4.1 check out on the page (\(v_\text{env}=-300\) px/s, \(\lambda_\text{beat}=2000\) px).

(B)
- \(\Delta\varphi\) in "\(a - b = \Delta k\,X - \Delta\omega\,t + \Delta\varphi\)" is not in the list of differences that follows. Self-evident.
- Figure 3's envelope \(\pm 36\,|\cos(\pi(t-2)/4)|\): the "\(-2\)" comes from \(X/200 = 2\) at the centre, and the caption does not say so.
- 4.1: "so \(v_\text{g}\) is exactly half the phase speed": the one-line derivative \(\tfrac12\sqrt{g/k}\) is left to the reader. Fine in a ★ part.

**Verdict: clear.**

### 05 · A square wave from sines (with 5.1 ★, 5.2 ★ and the Gibbs table)
(A)
2. **Two different percentages for the same overshoot make the main claim look false.** "One term is a plain sine that rises 27 % above the plateau. … The overshoot gets narrower as terms are added, but not lower: it settles at 8.95 % of the jump, 4.22 px above the plateau of the page's square wave (Section 5.2)."
   The 27 % is measured against the plateau \(H\). The 8.95 % is measured against the jump \(2H\). Side by side, they read as "27 % fell to 9 %", which contradicts "not lower". The table in 5.2 then gives the same one-term case as **13.66 %**, so the text and the table disagree on their face. (In px the one-term crest sits 6.44 px above the plateau, against 4.22 px in the limit. The overshoot does fall at first, then settles from about three terms on: 4.44, 4.35, 4.24 px.)
   Smallest fix: put the one-term figure on the table's basis ("rises 6.4 px above the plateau, 13.7 % of the jump"). Then say that the overshoot drops a little and then stops shrinking, e.g. "…narrower as terms are added, but from three terms on hardly lower: it settles at 8.95 % of the jump".

(B)
- Box "Fourier's theorem": "each amplitude is found by one integral, equation (13)". But (13) gives only \(b_m\). The cosine twin is never written, and the square wave does not need it.
- 5.1: "an even harmonic is unchanged by that shift, so it cannot take part" is compressed. It needs uniqueness of the expansion, but it is fine for the ★ reader, and (14) already shows the result.
- 5.2: "the first and highest crest" is asserted, not shown. "\(=1.17898\)" is a number with no closed form; saying it is evaluated numerically (\(\mathrm{Si}(\pi)\)) would be cleaner.
- 5.2 telescoping: the step "multiply the sum by \(2\sin x\)" is implicit. It is fine for ★.
- The header says "8 equations". There are 7 numbered ones, (10)–(16). The `\\[6pt]` line break inside (14) is counted by `fold.js`'s `\[` match. Cosmetic.

**Verdict: needs work** (item A2 only: one sentence).

### 06 · The spectrum (with Exercise 6.1)
(A) none. The ear-at-one-point picture comes first. Equation (17) follows from (5), and the Speed 0 special case is spelled out. The cross-term argument for (18) is given, and the Parseval number (527.245 px²), the triangle bound (19), Ohm's law and every number in Exercise 6.1 (27.9 → 28.0 px; 41.7 px with no stem moving) check out on the page.

(B)
- The energy paragraph ("Energy counts the harmonics differently. …") is graduate-level material in a section without ★: \(\tfrac12T(\partial y/\partial X)^2\), \(T=\mu v^2\) and \(\partial y/\partial t=-v\,\partial y/\partial X\) arrive as bare formulas for the school reader. The conclusion is stated in plain words ("The fast harmonics weigh more because they move faster"), so the thread survives. It is long for a side remark, and it should be left alone unless the lead wants it starred.
- \(T\) means tension here, \(T_\text{beat}\) is a period in §4, and \(T\) is a listening time in §9.

**Verdict: clear.**

### 07 · Computing the curves
(A) none. There is no integrator, and the note says so and why. Sampling, the Δt cap, the readout rate and the chord error are all stated with the page's measured values (M = 712, ΔX = 1.12 px; phone M = 298, 2.68 px), and all were confirmed on the page and in the code.

(B)
- "\(3N(M+1)\) calls": \(N\) (the number of waves) is not defined in this section, and in 5.2 \(N\) was the number of series terms. "Three times per wave and sample" makes it clear, and for the preset both readings give 4. Two words ("for \(N\) waves") would settle it.
- "a chord cuts under a crest by about \(A k^2\,\Delta X^2/8\)": a bare formula. A clause would explain it: near a crest the curve is a parabola of curvature \(Ak^2\), and a chord of length \(\Delta X\) sags by curvature × \(\Delta X^2/8\). The numbers (0.06 and 0.32 px) are right.
- "minus 58": where 58 comes from (44 left + 14 right) is never said.

**Verdict: clear.**

### 08 · From the medium to the screen
(A) none. Equation (20), the column mapping, the 1.83 : 0.89 aspect, the stem position, the colours and the 4.3 px puzzle all match the code and the page (R = 60, \(h\) = 220.08, card shows "4 px", sum 50.3 px).

(B) none beyond the "px" remark under §2.

**Verdict: clear.**

### 09 · What the model leaves out (with 9.1 Further reading)
(A) none. The five limits are right and point to the next model (a dispersion relation, nonlinear steepening, a finite listening time). The four sources are real, the chapters cited are the right ones, and every link resolves.

(B)
- "lengths are in pixels of that window": they are the medium's px, not screen pixels (see §2).
- Boas "Section 7.11" for Parseval: the publisher's page lists chapters only, so the section number cannot be confirmed from the link. It matches the 3rd edition as I know it.

**Verdict: clear.**

## Rendering checks (not prose)
- Equation (5) number clipped at 1440 × 900 (see §3).
- At 390 px width, 15 of the 20 display equations scroll sideways and their numbers sit off-screen until scrolled. The page itself does not scroll sideways (scrollWidth 390). This is probably house-wide behaviour. Noted, not judged.

## Numbers checked
| claim in the note | checked how | result |
|---|---|---|
| plot 770 px wide, M = 712, ΔX = 1.12 px (1440 × 900) | page store | 770, 712, 1.1236 |
| phone M = 298, ΔX = 2.68 px | page store at 390 px | 298, 2.6846 |
| h = 220.1, R = 60 px, 1.83 and 0.89 px scale | page store | 220.08, 60 |
| Square wave: Peak 27.9 px, Sum of amplitudes 50.3 px | readouts over 3 s | 27.9069–27.9081, "27.9 px", "50.3 px" |
| Wave 4 removed: 28.0 px | readout | 27.9996–28.0000, "28.0 px" |
| Wave 2 Phase 1.00 π: 41.7 px, stems unchanged | readout, store | 41.7, lines 30, 10, 6, 4.3 |
| noise cancelling: 0.17 px, reads 0.2 px | store, readout | 0.16815, "0.2 px" |
| Phase slider top ≈ 2π, nearest step to π is 3.15 | slider | 6.25, 3.15 |
| Beats: λ_beat 800 px; f₂ = 1.10 → 2000 px; s₂ = 0.5 → v_env −300 px/s | store | 800, 2000, −300 |
| Gibbs table rows | recomputed on a 0.01 px grid | 30.000/13.66, 28.000/9.42, 27.908/9.22, 27.799/8.99, 27.779/8.95 |
| (2/π) Si(π) = 1.17898, limit 27.78 px, 4.22 px above H | numerical integral | 1.178980, 27.779, 4.217 |
| Parseval 527.2 px², H² = 555.2 px² | recomputed | 527.245, 555.17 |
| equal energy per harmonic within 0.7 % | recomputed | n = 7: 1.0067 |
| chord sag 0.06 / 0.32 px | recomputed | 0.056 / 0.320 |
| 3N(M+1) = 8556 | arithmetic | 3·4·713 = 8556 |

## Summary
| section | verdict | (A) |
|---|---|---|
| 01 Many sounds, one eardrum | clear | none |
| 02 The model | clear | none |
| 03 Waves simply add | needs work | A1: plus sign in the cosine rule (6) not explained (one clause) |
| 04 Beats | clear | none |
| 05 A square wave from sines | needs work | A2: 27 % (of plateau) vs 8.95 % (of jump) vs 13.66 % in the table; "not lower" looks contradicted (one sentence) |
| 06 The spectrum | clear | none |
| 07 Computing the curves | clear | none |
| 08 From the medium to the screen | clear | none |
| 09 What the model leaves out | clear | none |

Separately: the number of equation (5) is clipped at desktop width. This is a markup fix, not a prose change.

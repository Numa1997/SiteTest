# Fig. 15 generation-2 lecture note: working state

Branch `claude/fig15-gen2-note` (from `claude/fig15-resonant-tunnelling`). Never merge to main, never open a PR: the Fig. 15
session merges this branch into its own and publishes. A chat that lost its context rereads this file first.

## Aim
Extend the generation-1 note (two walls, discs, shells, 115 runs) so it teaches the whole generation-2 parameter space the page
walks: spacing P, height V0 and thickness D, N = 3, 5, 10 barriers (bands), discs R 2-12 and shells R 3, 5, the diode under bias
(Fig. 15e from the stored bias runs, Tsu-Esaki, E_F = 1.0, kT = 0.05), long packets. Keep what is still true.

## Files I own (nothing else)
- `public/scripts/resonant-note.js` (fills `<article id="paper">`)
- in `public/simulations/resonant-tunnelling.html`: the lead paragraph and `<meta name="description">` only
- `notes/fig15/gen2_numbers.py` (reads the index, prints every number the note quotes with its run file)
- `docs/simulations/fig15-resonant-tunnelling.md` (sections about the note only)
- this file

## Rules
- Every number quoted is read from stored data via gen2_numbers.py; each number in one easy place in the note.
- Cases not yet in the index (shards 3-6): sentences true either way; refresh when the full index lands (~08:30 UTC 14 Nov,
  `git fetch origin claude/fig15-resonant-tunnelling`).
- LaTeX-like lecture note, everyday picture -> model -> maths; numbered equations and figures; no Q&A; short sentences.
- Never write the site owner's name or e-mail anywhere.
- After drafting: derivation-checker, referee, walkthrough-keeper (if a walk key exists); fix; npm run build; headless Chromium
  check (KaTeX renders, no page errors), screenshots 390 and 1440 px.
- Commit messages end with Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## Done
- (14 Nov 01:30) branch created, this file.
- gen2_numbers.py: prints every number with its source; `--write` fills the NUM and FIG2 blocks of resonant-note.js.
  Exact parts from tm.py/iv.py (finite-well levels, widths, band edges via xi = Re(e^{-ikP}/t), T_N formula check 2e-12).
- Note drafted (commit 9bbf6f7): 14 sections, eqs (1)-(27), Figures 1-3; byline without the owner's name (task rule).
- Page lead + meta description rewritten for gen 2.
- Built; headless Chromium at 1440/390: 589 KaTeX, 0 errors, eqs (1)-(27), no page errors, no overflow. Figure 3 labels fixed.
  Screenshots in scratchpad/shots (open folds first: the 'Expand all' button).
- No walkthrough key for this page (no data-walk attribute): walkthrough-keeper not needed.

## Left
3. Round 1 running (14 Nov ~02:10): derivation-checker (on commit 9bbf6f7, old numbering: map old->new eqs), referee -> notes/fig15/referee.md, readers -> scratchpad/readers/r1-{owner,student}.md. Eqs renumbered at 6aaf232: old 1,2->1,2; new 3 spread; old 3-10 -> 4-11; old 11 BW->15, 12 tau->16, 13 leak->17; old 14-27 -> 18-29 then supply 30, J 31, Jruns 32 (old 25->29, 26->31, 27->32).
4. Refresh numbers with the full index.
5. Write "READY at <commit>".

## The owner's standard (relayed by the coordinating session, 14 Nov 01:47 and 01:51 UTC)
The reader: BSc physics (computational/theoretical), reading for pleasure; every stop ("where did that term come from?",
"what am I looking at?") is a defect.
1. Honest: every number from the numbers script; one openable paragraph on where the picture differs from the stored data
   (colour steps, 8-bit |psi| and arg psi, the slice of the 3D field, blending between frames); name every approximation and its cost.
2. Rigorous: derive from the TDSE to T of one and two barriers; resonances as quasi-bound states + phase condition (Fabry-Perot
   for matter waves); Breit-Wigner shape, what sets width and height, width = 1/time trapped; what the 3D packet adds (finite
   width, spread of energies, spreading). Every equation numbered; every symbol defined in words with its unit at first use.
   Limits: no barrier, infinitely high barrier, very wide gap.
3. Intuitive: everyday picture -> model -> algebra -> back to the picture.
4. Direct: short sentences, no Q&A, LaTeX-like house style.
5. No unexplained term or image: define tunnelling, transmission coefficient, quasi-bound state, resonance width, phase, wave
   packet, group velocity...; every figure caption says axes, colours, brightness, what to notice; which control gives which view;
   no forward references.
6. Be ready before the full index lands: then only the numbers change.
Readers: when finished, run the referee plus at least two independent readers (owner persona; strong school student / first-year),
each given only the figure number and page path. Fix every mark; rerun FRESH readers until a full reading has no stops. Report each
round's marks and what was done, plus the derivation checker's result. Reply to session_01DGmqipDr2dvQjBi7BR6m3S via send_message.

## Derivation checker, round 1 (on 692e546; report notes/fig15/derivation-check-gen2.md)
All 27 equations of that version re-derive. 12 text/number errors, all fixed in 66455ed:
1 diode-from-runs peak/valley/ratio depend on which energies are filed -> withheld until all 500 runs per structure are in
  (NUM iv_*_complete); the reason for the early exact peak rewritten (area under the peak shrinks faster than supply grows:
  0.103 -> 0.073 -> 0.041 vs supply 14.2 -> 18.0). 2 disc energy: 0.75 once filed, else says "nearest filed so far".
3 long box 2.67x, not 4x. 4 sigma_E vs FWHM (0.119 > Gamma). 5 shell fits cut at run end -> "at least this long".
6 long-packet runs of the running example are FIX1 (due rerun) -> said while pending. 7 finite well: lowest level to
thousandths, upper to hundredths; all resonances listed. 8 bias wording. 9 unequal-pair wording. 10 (8) not (9) in sec 8.
11 "three round trips". 12 band middle in xi; peaks 0.02-0.17 apart; shell faces; "twenty-two"; "and more steps".

## Round 1 readers (14 Nov ~02:15-02:35): referee 65 marks (notes/fig15/referee.md), owner reader 32, student reader 45
(full lists: scratchpad/readers/r1-owner.md, r1-student.md). Fixed (commit after this line):
- Terms/symbols: star explained; figure-key paragraph moved to sec 1; E_u defined; matrix element z -> gamma (z is the coordinate);
  t amplitude vs time noted; R radius vs reflection noted in sec 12; k_B T noted; voltage renamed V_b in sec 13 (V = potential);
  tau in eq (26) -> delta; Delta E -> sigma_E; widths (sigma, not 2 sigma) consistent.
- Derivations: separation of variables with the brackets; Gaussian spreading solution given; time reversal + flux argument for M;
  explicit w and gamma (checked against tm.py); unequal-pair peak step; L_eff from step reflection phase (d -2arctan(k/kappa)/dk
  = 2/kappa); tau = hbar/Gamma via R^2 per round trip: -2 ln R = 0.3109 vs 2T/sqrt R = 0.3112 (not "sqrt R ~ 1"); phase-average
  integral shown; Bloch eigenvalue step; odd states; units + limits of (13)/(15)/(17); Strang global order and dt reason (0.2 rad).
- Facts: glass fringes faint (4 %); bucket (Torricelli) replaced by cooling tea; STM claim cut; "fastest" -> 1.92 THz cited;
  "current runs backwards" title -> "falls as the voltage rises"; hysteresis; next model named; BenDaniel-Duke mentioned;
  flux factor k_R/k_L under bias; 131 / 274 mV; 12 % vs 6-8 % not traced (said); third finite-well level explained;
  0.735 not a slider energy (Fig. 1 caption); Fig. 14 linked; 115 vs 3739 runs reconciled; shells geometry; "two walls with d=2";
  Fig. 2 strip scale and gap beyond the plot; Fig. 3 redrawn (flat level inside the filled states, shading stops at band bottom).
- Links: DOIs added to all five references (checked they resolve); repository paths now GitHub links.
Not changed (outside my files / by design): body font (shared stylesheet; same in every note); Fig. 15e axis label and "from 1000
3D runs" heading and caption (page code); blank 3D panels in a local build (runs live on R2); the picture-vs-data box stays
closed by default (CLAUDE.md: "a paragraph the reader can open"); no textbook added (only sources actually read).

## Round 2 (launched ~02:50 UTC on db61bec): fresh referee, owner reader, student reader, derivation checker.
Outputs: notes/fig15/referee.md, scratchpad/readers/r2-{owner,student}.md, scratchpad/derivation-check-r2.md.

## Round 2 readers (on db61bec): owner 23 marks, student 39 (scratchpad/readers/r2-*.md). Fixed in the commit after this line:
star passages restructured (sec 3 only "why the matrix has this form" starred, plain restatement of M/w; sec 5 theta defined
unstarred; sec 9 xi introduced unstarred); probability current defined; units-without-unit rule; n branch of rho explained;
half-wavelength vs L_eff (2.59 vs 2.76); naive 2T count explained; T_2(k) in (18); sigma_E wording; long-packet runs compared
with the exact average AT THEIR OWN ENERGY (0.51 vs 0.499; d=2: 0.0225 vs 0.0318); N=10 band/gap with exact averages
(0.129 vs 0.158; 0.0218 vs 0.032); 210 called a lower bound; fit window rule incl. "to the end of the run"; run lengths 30-517;
start share <= 2.1e-5; arg psi levels of a full turn; Strang: each half exact for all modes, error where V changes (0.59 rad
diagonal mode noted); disc table with R^2 estimate column and labelled walls row; R=2 tau shorter than a round trip; shells
centre radius, longest tau at lowest energies; band bottom and E_F defined before Fig. 3; supply-function wording; volts of
the area numbers; (13) not (31) for broader peaks; Fig. 3 redrawn TO SCALE in energy at V_b = 1 (level between collector
E_F - eV_b and emitter band bottom), collector filled states drawn; chips, panel naming, Fig. 1 E/V0 wording.
Data question for the coordinator: long-packet runs for V0 = 3 pass 0.188 at E 0.783 where the exact packet average is 0.077.

## Round 2 referee (71 marks, notes/fig15/referee.md, read db61bec) and derivation checker (notes/fig15/derivation-check-gen2-r2.md)
Checker: all 32 equations re-derive; fixed: sheet scale = largest value of the run is height 1 (NOT the start peak; the page's
own gain note says "start packet's peak", page code: tell the coordinator); run length rule (flight + 3 x capped lifetime);
sec 11 profile numbers now measured by notes/fig15/gen1_profile_check.py (3.0 % / 2.4 % of the run peak; 5.8 % of frame
peak); eq (10) reference points; 6.95; theta at unrounded E_r (5.6e-9); midway T^2/(1+R)^2; 256 levels = 255 steps.
Referee: fixed all not already fixed by round 2 (definitions of omega(k), separation constants, Fourier widths, |w|^2 step,
m for round trips, inequality step, independent-mirror sum, tea used once, area of Lorentzian, three reasons, crystal wells,
det 1 reason, periodic box, Fourier eigenfunction, non-commuting K, V, run counts formula, disc regions, packet width at
arrival 3.7, one-disc yardstick, shells >= marks and no-model statement, supply integral step, area x supply products,
E_F choice, eV_b = V_b in our units). Not done: textbook (only read sources), Fig. 15e runs curve (page code), house font in
SVG (same classes as gen-1 Figure 1), links to main 404 until merge.
Live site: /r2/resonant-tunnelling/2026-11-14/runs/... returns 404 on phyeinusul.com (checker): told the coordinator.

## Round 3 (launched ~03:45 UTC on 1aacf39): fresh referee, owner, student, derivation checker. Outputs: notes/fig15/referee.md,
scratchpad/readers/r3-{owner,student}.md, scratchpad/derivation-check-r3.md. Coordinator told: live R2 404, page gain note, V0=3 long packets.

## Round 3 readers (on 1aacf39): owner 22 marks, student 28 (scratchpad/readers/r3-*.md). Fixed in the commit after this line:
two rendering faults from round-2 edits (double-escaped quotes in sec 11; raw \\( in sec 13 products); eta not a (a = length unit);
v on both sides of the flux; 1/sqrt R dropped in (17) said; why the d=2 fit reads short; FIX1 explained (earlier run-length rule,
share read before the border); long-packet energies not on the grid; peak energy named for (19); N=10 gap with a likely cause;
sec 7 gap called a grid error with pointer to sec 11; tau of walls 15.1 at 0.65 explained (lifetime belongs to the resonance,
not the packet's mean energy); problem 6 rewritten to work with R = 2 now; NDR power argument; discs' current sentence; filed and
SHA-256 explained; a = 2.75 nm given in sec 2; phase-function step in separation; step r from (5); very-wide-gap paragraph starred;
P^N form reason; Fig. 3 redrawn at V_b = 0.8 (eV_b arrow from emitter band bottom, no coincident levels); Fig. 1 V0 arrow.
Not done: Fig. 15e axis-label overlap and run-count heading (page code, told coordinator); Fig. 2 tick marks (minor, next pass).

## Round 3 referee (60 marks, notes/fig15/referee.md): most overlap the readers (already fixed). Fixed now: glass fringes need a thin
air film; the barrier product written out (checked: |w|^2 6.94688 = tm.py); sec 4 matrix route stated; time-step error not
measured on its own (said); shells met head-on (packet within 3.7, shells reach 5.5-8.5), not 'round it'; Pauli for the filling.
Not done: links to blob/main dead until merge (owner session merges); symbols t,T,R,m,x,d reused but each flagged where it changes.

## Round 3 derivation checker (notes/fig15/derivation-check-gen2-r3.md): all 32 equations re-derive; 10 text errors fixed:
sign e^{+i int f dt}; Fig. 15b dashed curve is the 1D twin on the grid; long-packet stop effect stated correctly (a few %);
d=2 run ends with wave still trapped; shells cut = window ends at run end AND < 1 lifetime (2 of 4); 'lowest filed energy';
N=10 shares are the twins'; Tbar by quadrature (0.540, exact1d.tbar); s=4.5 top level -> broad peak at 2.028 (FWHM 0.314);
missing full stop. Round 4 next.

## Round 4 (launched ~04:40 UTC on 95824f5): fresh referee, owner, student, derivation checker; outputs scratchpad/readers/r4-*.md, scratchpad/derivation-check-r4.md, notes/fig15/referee.md.

## Round 4 readers: owner 24 marks, student 36 (scratchpad/readers/r4-*.md); fixed: x0 = 14 before the first face, arrival t 11.5,
sigma_x as std dev, Fig. 1 V0 label + d brackets, half-wavelength wording, run cap pointer, Bloch q defined, squared modulus,
U_{-1} = 0, P eigenvalue e^{-iqs}, Fig. 2 dashed, box note covers 15b-15e, 21 %, R2 share energy, shell 'spacing', area
definition + level energies 0.29 / 0.10, problem 4, panel naming, pointers to sec 5/6/10/11, travel-matrix sign wording,
end of the sec 3 star, plain restatement after (13), starred correction sentences in sec 5, 15 planned long runs, peak run not
filed, box 512 vs 192, hard box above V0, fit start 60 %, |w_N|^2 step, ten-wall wording, bathtub placed at the side leak,
share-through reason, conduction band defined.
Page items (panel text, Fig. 15e title/axis/units, 'Fermi sea', real-units J_p, 'Read values' button, '20 runs') -> coordinator.
Owner mark 4 (file paths) is a reading artefact: they are links.

## Round 4 referee (54 marks, read 6af5c32) and derivation checker (notes/fig15/derivation-check-gen2-r4.md, 6 errors): fixed.
Physics corrections: side-leak estimate (28) is m R w / hbar with w = min(R, sigma_perp) (trapped wave no wider than the packet);
diode turn: the tilted peak gets LOWER (1 -> 0.65 -> 0.34) and slightly WIDER (0.071 -> 0.077 -> 0.085), not narrower;
d=2 long run lasts 509 (about one lifetime after the peak), ends with 0.0074 trapped; long-packet exact averages by quadrature
(0.500, 0.0319); disc energy wording (walls' 0.75 run to come); border = more than a thousandth; levels printed to 3 decimals.
Referee text fixes: separation-of-variables reason, g formula brackets, units hold for any a, slit picture, divide by k1,
centre-phase e^{+-ikd/2}, t_2 defined, Lorentzian substitution shown, tan substitution steps, packet centred on resonance,
FIX1 direction (share reads low), 'almost exponentially', 0.59 rad meaning, tilt paragraph split, d^2k step, thin line of
Fig. 15e, N-1 per band, xi = +-cosh mu, 'possible cause', 66 %, Maekawa without 'fastest', diode leak sentence, laser wording.
Declined: textbook (unread), dimensionless-number box (next pass if time), page font (stylesheet), links (merge).

## Round 5 (launched 03:12 UTC on ddcd0ed): fresh referee, owner, student, derivation checker. (Earlier 'UTC' times in this file
were estimates; the real clock is about two hours earlier than written.)

## Round 5 (readers on d45d8c5..ddcd0ed): owner 18, student 23, referee 45 marks (notes/fig15/referee.md); fixed:
the self-contradicting long-packet sentence (grid passes a little more just below the peak, plus 0.0286 trapped at the end);
end-of-star markers in sec 5, 9, 13; plain restatement of L_eff after the starred step; s/lambda line removed (misleading);
w -> W for the trapped width; P^N vs a row of N barriers (last travel taken back); n = 0 with rho in (-pi, pi]; C group =
4 x 3 shapes; x0 for long packets 4 sigma_x; start share over all runs; (1+R)^2 step; sinh beats V0^2; lowest diode energy
0.10; 'hard box, lowest level'; stray full stop; Bloch condition wording; 'possible cause'; ns of GPU time; energy and
sideways momentum kept on crossing (why the current falls); (11) explains the trend only; 150 mV per unit; even levels;
e^{-2 kappa d} reason; dividing by the total; lifetime belongs to the resonance (reason); shells tunnelled into; hbar theta'
is a time (reason); uniqueness for the product; AC power argument for NDR; Gamma from (17) to 3 figures.
Coordinator already has the page items (Fig. 15e, gain note). Next: round 6.

## Round 6 launched 03:18 UTC on ada0993 (fresh referee, owner, student, derivation checker).

## Round 5 derivation checker (derivation-check-gen2-r5.md): 32 equations re-derive; 6 fixed: 20 % (not 21), filed thirds repeat
every 0.75 in voltage, mirror symmetry exact only inside the side border (border one cell off), two fifths of the d=2 shortfall,
theta closes to 1e-8 (root precision), J_runs unit includes E_u.

## Round 6 student (32 marks): fixed the real error 'denominator nearly vanishes' (it falls to 1 - R = T and matches the
numerator); n = 0 (phase count) vs n = 1 (box count) stated; nu for round trips (m is the mass); time unit 4.39 fs row; figure-key
pointers (psi, twin, border, discs/shells); x4 label rule; colours in the probability view; long-packet start rule; 'stored
energies' not 'grid'; packet energy FWHM named; (3) written with hbar, m; Tsu and Esaki (1973); Poisson defined; fit rule early;
counts of the singles named; 4 % caused by the rule; 66 % context. Left: data-pending items (refresh at full index).

## Round 6 owner (17 marks, read before 034bc81): remaining fixed: Fig. 15e has two kinds of curve in the key; n paragraph split;
'here' -> E; sigma vs width; shells centred at x = 0, caught in the gap (and, tunnelling again, the inner shell); supply is a pure
number, product in (32) units; Fig. 2 base line; sec 11 box caveat for 12 %; 'earlier, shorter rule'.

## Round 6 referee (51 marks, notes/fig15/referee.md): fixed the house frame — the note now builds header + paper__grid with a
contents list (paper__toc, 14 entries from the section titles, maths stripped) + paper__body, so the body sets in Latin Modern
(it was IBM Plex Sans since generation 1; paper.css applies the font only through .paper__body) and the TOC observer in sim.js
works. Also: T_2 defined; wide-gap star ended; k -> E change of variable; flux T equals |t|^2 for equal k; problem 3 uses L_eff.
Remaining open marks are data-pending (refresh at full index) or declined (textbook; table scroll cue is house .ptab).

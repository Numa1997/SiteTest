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

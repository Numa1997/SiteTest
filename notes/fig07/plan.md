# Fig. 7 · Phasor sums · plan

Page `public/simulations/phasor-sums.html`, note L221–650. Judged against notes/STANDARD.md §4 under "Numa's verdicts":
a section judged clear is not touched. Every number in the note was recomputed before judging (scripts in this folder).

## Verdicts

| § | Section | Verdict |
|---|---|---|
| — | Header, abstract, contents | clear, leave it |
| 1 | Circles riding on circles | clear, leave it (325 V = 230 V·√2; 1609; three phases sum to zero) |
| 2 | Euler's formula, 2.1, 2.2 ★, 2.3, Figure 1 | clear, leave it (Figure 1 at 50°: cos 64.3 px, sin 76.6 px, θ at x = 404.4, all as drawn) |
| 3 | The model, 3.1, Figure 2 | clear, leave it (Figure 2 joints recomputed at t = 0.30 s: (300.2, 155.2), (274.0, 110.2), pen (246.3, 102.9), as drawn; Trefoil stops at t = π/6 + 2πk/3) |
| 4 | Two arms: box, 4.1, 4.2, Figure 3, eq. 11, Exercise 4.1 | clear, leave it (n = 3, 2, 4; zeros 3.04, 9.32, 15.61 s; (10) vs (6) 1.9e-14; 2.197, 6.18 s, 12.57 s) |
| 5 | When the curve closes ★ | **needs work**: right after eq. (12) sits the paragraph "This is a common period for the pen, but cancellation can shorten its true period. … The readout uses the listed active arms.", and only then the clause "where gcd is the largest g …". So gcd is defined after an unrelated paragraph and the "where" sentence dangles. The cancellation paragraph also reads as bare instructions. 5.1, Figure 4, Exercise 5.1 clear (closure 2.5e-15; 61-fold, 62.83 s, 7000 samples; 13 in 12.57 s; 7 in 6.28 s). |
| 6 | The average size | **needs work**, one phrase: "This is the readout ⟨\|z\|²⟩ = ΣA² under the figure." At 1440 px the readout is in the controls column to the right of the figure (measured: figure right edge 933 px, readout left edge 988 px, 1222 px further down). Rest clear (1.2824, 1.36 cos 5t + 0.18 cos 10t, 0.1024 to 2.8224, 4.828). |
| 7 | How the page computes it, 7.1 | clear, leave it (angle rounding ≤ 3.6e-12 rad for \|ω\| ≤ 32, t ≤ 1000 s; trail chords 0.00069 and 0.0111; τ = 12.0 frames, 1 % after 56 frames) |
| 8 | Plane to pixels, 8.1 Auto Dance | **needs work**, two sentences. (a) "Each arm, with the 3 px dot at its tip": the dot is `arc(nx, ny, 3, …)` (L1140), radius 3 px, 6 px across, while the next sentence gives the pen by its radius. (b) "*Record* stores the whole list every 50 ms against the audio time, and *Replay* eases toward each stored list over 50 ms": the code takes a snapshot on the first frame at least 50 ms after the last and resets the counter to 0 (L1187–1190), so snapshots come every third or fourth frame; replay moves each value the fraction min(1, Δt/0.05) of the remaining way per frame (L1201–1205), which never arrives in 50 ms. Rest clear (770 × 601, 132.22 px per unit, 356 × 356, bins 1 to 7, 21.5 Hz). |
| 9 | What the model leaves out | clear, leave it |
| 9.1 | Further reading | **needs work**: none of the four items has a link. |

## Changes (only these)

1. §5: put the "where gcd is …" paragraph straight after eq. (12); follow it with the cancellation paragraph, same content
   in plain words (same-frequency arms act as one arm, their sum; a zero sum draws nothing; e^{it} − e^{it} + e^{2it}
   repeats after π s; the *Period* readout uses every listed arm with A > 0). No equation added or renumbered. Each
   paragraph stays on one line, so no line number of the page moves.
2. §6: "under the figure" → "at the foot of the controls".
3. §8: "with the 3 px dot at its tip" → "with a dot of radius 3 px at its tip".
4. §8.1: the Record/Replay sentence says what the code does, with the measured snapshot spacing.
5. §9.1: a link on each item, to a page I opened:
   - Feynman ch. 22 and 48, online edition feynmanlectures.caltech.edu/I_22.html, I_48.html (WebFetch and curl got
     403; read in full through the Firecrawl scraper). Ch. 22 ends with e^{iθ} = cos θ + i sin θ, "our jewel"; ch. 48
     factors out the average frequency (48.7) as eq. (8) does and gives |z|² as (48.8) = eq. (11).
   - Needham: the 1997 OUP page is gone (404); the OUP page of the 25th anniversary edition (2023) lists chapter 1,
     Geometry and Complex Arithmetic; the publisher's preview lists 1.2 Euler's Formula with 1.2.2 Moving Particle
     Argument and 1.2.3 Power Series Argument, the two routes of §2.
   - Hecht: Pearson's page for Optics 5th ed. lists chapter 7, The Superposition of Waves; Pearson's preview (Global
     Edition, © 2017) gives 7.1 The Addition of Waves of the Same Frequency, 7.2 … of Different Frequency, and says
     phasor addition is taken up again in 7.1. "beats" is not in the headings I could open, so the item names 7.1 and 7.2.
   - Kuhn: Harvard University Press page of the book (opened). The chapter title, ch. 2 The Problem of the Planets, with
     epicycles and deferents, I could confirm only in a chapter summary (Knowino, mirrored at Radboud University); the
     Internet Archive copy is lending-only (403), so the book itself was not opened.

## Measurements (how)

- `numbers.cjs`: the page's `sumAt()` in Node; Figure 3, 4, 5 numbers, trail chord error, morph constants, Exercise 4.1.
- `angle_rounding.py`: exact rational arithmetic on the doubles the page multiplies; worst angle rounding.
- `record_rate.cjs`: headless Chromium, Record for 6 s: 104 snapshots, 58.3 ms apart, 359 frames, 59.9 fps.
- `check.cjs`: headless Chromium at 1440 × 900 and 390 × 844: console errors, `.katex-error`, sideways scroll, every
  fold closed and reopened, store values (`box_w`, `box_h`, `scale`), readout and figure positions, links in `.prefs`.

## Doc

docs/simulations/fig07-phasor-sums.md: the byte count of the page changes; the Record sentence of the doc says the same
"every 50 ms" and gets the measured spacing. Line numbers do not move.

## Done (20 October 2026)

All five changes made, inside the article only; the page keeps 1 479 lines, so no line link moves. Headless Chromium
after the edit (`check-after.json`), at 1440 × 900 and 390 × 844: 0 console errors, 0 `.katex-error`, 0 px sideways
scroll before and after opening folds, 19 of 19 folds close and reopen, equation tags (1)–(17) unchanged, 350 KaTeX
nodes (346 before), each of the four references has its link(s). Store values unchanged: 770 × 601 and 132.22 px per
unit; 356 × 356 and 78.32 px per unit. Crops of each edited paragraph: `edit-*.png`.

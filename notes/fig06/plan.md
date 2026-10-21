# Fig. 6 · Wave Interference Simulator · plan

Page `public/simulations/wave-interference.html`, note lines 104–479; walkthrough `bench` (not edited); doc
`docs/simulations/fig06-wave-bench.md`. Judged against notes/STANDARD.md §4, under "Numa's verdicts": a section judged clear
is not touched. Every number already in the note was re-measured before judging (`check.py`, `measure.cjs`,
`measure-before.json`); all of them hold.

## Verdicts

| § | Section | Verdict |
|---|---|---|
| — | Title, abstract, contents | clear, leave it |
| 01 | Many sounds, one eardrum | clear, leave it. Guitar beats, headphone, synthesizer, violin sawtooth, clarinet, cochlea: picture before symbol. |
| 02 | The model | clear, leave it. Eqs. (1)–(2) match `y(w, X)` (L622) and the stored `k, ω, λ, v, ν` (L664); "4 f wavelengths in view", "Frequency is hertz only at Speed 1×" both right; Figure 1 fine. |
| 03 | Waves simply add | needs work, one sentence. L191: "Each time derivative brings down a factor −ωᵢ, each space derivative a factor kᵢ" is wrong for a sine: one derivative turns sin into cos, and (−ω)(−ω) = +ω² would lose the minus sign that sin'' = −sin supplies. The result (3) is right only because the error cancels in the ratio. The rest (wave equation as Newton's law, linearity (4), phasors (5)–(6), Figure 2, the 0.0084 rad / 0.17 px / "0.2 px" headphone example) is clear and measured. |
| 04 | Beats | lead, (7), (8), Figure 3 and Exercise 4.1: clear, leave them. **4.1 ★ needs work**, three sentences of L305: "which describes a narrow envelope on a specified dispersion relation" is wrong (group velocity belongs to a narrow band of wavenumbers, that is a *long*, slowly varying envelope; a narrow envelope holds many k and spreads); "In the lossless wave examples here it also describes energy transport" has no referent (the bench has no energy, and the deep-water example comes after); "illustrate envelope geometry; they do not by themselves define an information speed" is audit language with no physical picture. |
| 05 | A square wave from sines | clear, leave it. (10)–(16), the box, Figure 4, the Gibbs table: every step shown, every number re-measured (table to the last digit). |
| 06 | The spectrum | (17), (19), Ohm's law, Exercise 6.1: clear. **Needs work, the string-energy paragraph** (L427, second `<p>`): the formula ē = ½μΣωₙ²Aₙ² is asserted ("velocity and slope both enter the energy density, giving …"), the tension it needs is never named, and the last two sentences ("Its mean square stays finite. … its 95 % is not a string-energy fraction.") are patch language. Also, the "Checked by averaging y²" note (L428) that checks (18) now sits after this energy paragraph, as if it checked the energy. |
| 07 | Computing the curves | clear, leave it. Matches the code (clock cap 0.05 s in sim.js L179, M = round(w − 58), 3N(M+1) = 8 556 sines, readouts every 8th frame); M = 712 / 298, ΔX = 1.12 / 2.68 px, chord gaps 0.06 / 0.32 px, 25 samples per shortest wavelength all re-measured. |
| 08 | From the medium to the screen | clear, leave it. (20) matches `nice`, `panel`, `drawSpectrum`; R = 60 px, h = 220.08, 1.83 vs 0.89, card shows "4 px" all measured. |
| 09 | What the model leaves out | list clear, leave it. **9.1 Further reading needs work**: four references, none with a link. |

## Changes (only these; no line added or removed, so every line link in the doc and walkthrough stays valid)

1. §3, L191, one clause: "A sine differentiated twice comes back as minus itself, times ωᵢ² if we differentiate in time and kᵢ²
   if we differentiate in space, so". Check: SymPy ∂²y/∂t² ÷ y = −ω², ∂²y/∂X² ÷ y = −k² (`check.py`).
2. §4.1, L305, the three sentences after "the group velocity": the speed of a long, slowly varying envelope made of a narrow band
   of wavelengths, in a medium whose ω(k) fixes each frequency; for waves that lose no energy also the speed of the energy (and of
   a slow signal, Feynman I-48-4); on the bench the speeds are set by hand, so the envelope is only where crests fall into step,
   nothing travels with it, which is why it can run backwards faster than either wave (Exercise 4.1: −300 px/s against 200 and
   100 px/s, measured `venv` = −300).
3. §6, L427–428: the eqnote that checks (18) moves up next to (18)'s numbers (same lines, swapped content); the energy paragraph
   shows its step: kinetic ½μ(∂y/∂t)², stretching ½T(∂y/∂X)², equal for a one-way wave since ∂y/∂t = −v∂y/∂X and T = μv²; mean
   kinetic per harmonic ¼μωₙ²Aₙ², total twice that; cross terms average away as in (18). Then the physical point: fast harmonics
   weigh more because they move faster; for the square wave every odd harmonic carries the same energy (the preset's four within
   0.7 %: (4.3·7/30)² = 1.0067), so true corners would need infinite energy. Check: SymPy time-average of the energy density
   = ½μω²A², kinetic = stretching (`check.py`).
4. §9.1, L471–474: a link on each reference to a source opened in this session, and the content claims cut back to what that
   source confirms:
   - Feynman I-48 and I-50: feynmanlectures.caltech.edu/I_48.html and I_50.html (opened via Firecrawl; WebFetch and curl get
     403). Ch. 48 "Beats" (48-1 adding two waves, 48-4 group velocity), ch. 50 "Harmonics" (Fourier series, square wave, energy
     theorem).
   - French: archive.org record `vibrationswaves0000fren` (Norton 1971), whose catalogue contents list ch. 2 "The superposition
     of periodic motions" and ch. 6 "Normal modes of continuous systems. Fourier analysis"; beats in ch. 2 confirmed by its
     problem 2.3 on the beat period (numerade.com chapter page). The text itself is lending-only (403), not read.
   - Hecht: pearson.com product page, contents list ch. 7 "The Superposition of Waves". Section headings not confirmed by any
     page I could open, so "beats, group velocity and Fourier series" becomes the chapter title.
   - Boas: wiley.com product page (ch. 7 "Fourier Series and Transforms"); Parseval's theorem is §7.11, p. 375, in the
     third-edition contents (CERN library PDF).

## Doc

`docs/simulations/fig06-wave-bench.md`: page size in bytes (line count unchanged), and the line-link note for the
95 % sentence (L427) and the energy paragraph (now L428). Nothing else in the doc describes the edited sentences.

## Done · measured after the edits

Built to /tmp/fig06-dist, served by `serve.cjs`, checked by `measure.cjs` (`measure-after.json`) in Chromium 1194 at 1440 × 900
and 390 × 844: 0 console errors, 0 `.katex-error`, 0 px sideways scroll (before and after opening every fold), 15 of 15 folds
close with Collapse all and reopen by their own toggles, equation tags (1)–(20) unchanged, five reference links present. The
page's own numbers quoted by the note re-read from the store: M = 712 / 298, ΔX = 1.124 / 2.685 px, R = 60 px, hSum = 220.08,
peaks 27.9 / 28.0 / 41.7 px, two copies 40.0 px then 0.2 px (C = 0.168 px) at Phase "1.00 π" = 3.15 rad, v_env = −300 px/s,
λ_beat = 800 and 2000 px, round 2.50 s, Wave 4's card "4 px". Line count 977, unchanged; only lines 191, 305, 427–428 and
471–474 differ. The doc gained a byte count (170 005) and one dated line under "Teaching revision"; the plan's wording
"line-link note for the 95 % sentence" became that dated line.

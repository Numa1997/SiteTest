# Fig. 1 · walkthrough check (`circles`)

> Lead's note, 20 October 2026: these proposed fixes were written before some later edits of the note and were audited
> against the current notes afterwards (docs/research-theory-audit.md, "Open, for Numa"). Fixes that touch a `code` or
> `where` field need the same permission as the rest. Nothing here has been applied; the walkthrough file is unchanged.


Checked on 20 October 2026 by the walkthrough keeper, at commit `d3ffae1` on branch `claude/physics-notes-rewrite-cwctkk`. The
page, `circles.js` and `sim.js` are byte-identical at `6df11fb`, which committed a first copy of this report; this copy differs
only in the mark count (17 keys) and in setting the M6 code fixes as blocks. The page was last changed in `a01cf85` (the teacher's edits to §4 at L285 and L287, §6 at L308, §10.1 at L487–L490). `circles.js` was
last changed in `ce3bfc4` (15 October).

- Page: `public/simulations/Circular Wave Interference Visualization.html`, 907 lines, 192 185 bytes. The lecture note is at
  L98–L495, `#walk[data-walk="circles"]` at L497, and `Sim.live()` at L737–L754. The teacher's edits are all inside the note, so no
  quoted code line moved.
- Walkthrough: `public/scripts/walk/circles.js`, 110 lines, 6 694 bytes, 7 steps.
- `circles.js` was not changed, because Numa has not allowed it. Every fix below can be applied as written once he does. All 17 old
  texts were applied to a scratch copy: each occurs exactly once. The patched copy still quotes the page exactly (17 of 17), and in
  Chromium it draws 7 steps, fills every "Now" cell and logs no console errors (section 6).

## Counts

| What | Checked | Found / matching | Not found / mismatched |
|---|---|---|---|
| Non-empty code lines (marks stripped) | 21 | | |
| Lines that are only `...` | 4 | (not searched) | |
| Code lines searched in the page | 17 | **17** (all whole page lines) | **0** |
| of these, with an inline `...` | 0 | | |
| Page lines skipped without a `...` line (silent elisions) | 7 steps | 6 steps | **1** (step 2, page L642) |
| Keys in `syms` returned by `Sim.live()` | 20 | **20** | **0** |
| Equation numbers "(n)" cited in `math` or `note` | 0 | | |
| `math` fields against the note | 7 | 3 (steps 1, 5, 6) | **4** (steps 2, 3, 4, 7) |
| `note` fields against the note | 7 | 6 | **1** (step 3: "the crest you see", now contradicted by §4) |
| `syms` rows (symbol, in code, meaning) | 22 | 20 | **2** (step 3 `a`, step 6 `v`) |
| Marks keyed to the wrong quantity | 17 distinct keys | 16 | **1** (step 6: `f` on `ds.get('v')`) |

The code is quoted exactly. There are six mismatches:

- **M1:** a silent elision in step 2.
- **M2:** step 2 uses x and y for offsets, where the note means the point's coordinates.
- **M3:** in steps 3 and 4 the walkthrough's a already contains 1/N; the note's aᵢ does not.
- **M4:** a sentence in step 3 that the new §4 now contradicts.
- **M5:** step 7 uses the code's names, where the note writes (19) with c₀, c± and ψ.
- **M6:** a mis-keyed mark and a wrong "In code" entry in step 6.

Three smaller points follow (W1–W3).

## 1. The code lines: 17 of 17 found verbatim, one silent elision

Method from `docs/scripts/walk.md`, "The rule":

1. Evaluate `circles.js` with a stub `window`.
2. Strip the marks with `/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g → '$1'` and trim each line.
3. Drop lines that are only `...`. Split each remaining line on `...` and look for the fragments in order on one page line.

Then a stricter pass. Each line must equal a whole page line after trimming. Lines quoted together without a `...` between them
must be neighbours in the page.

| Step | `where` | Page lines quoted (`...` = lines left out) | Verdict |
|---|---|---|---|
| 1 Wave number and damping | `precompute() — line 1` | 628 629 | found; whole lines; neighbours. `where` says one line, the step quotes two (W1). |
| 2 Distance from a source to a grid point | `precompute() — the two inner loops` | 630 ... 641 **[642]** 643 644 | found; whole lines; **L642 `for (var i = 0; i < cols; i++, p++) {` is left out without a `...` (M1)** |
| 3 Amplitude and phase from one source | `precompute() — innermost loop` | 645 | found; whole line |
| 4 Two maps that hold all of space | `precompute() — the accumulation` | 647 648 | found; whole lines; neighbours |
| 5 The field at this instant | `render() — per pixel, every frame` | 660 ... 664 665 | found; whole lines; neighbours |
| 6 The clock | `Sim.clock callback` | 762 ... 712 | found; whole lines. L712 lies in `readouts()`, earlier in the page; `where` names only the clock (part of M6). |
| 7 A number becomes a colour | `the LUT builder and render()` | 588 589 ... 667 | found; whole lines; neighbours |

The recipe in `docs/scripts/walk.md` looks for each line on its own, so it cannot see M1. The neighbour pass finds it.

The page lines the docs table cites for Fig. 1 still hold: `data-walk` at L497, `window.WALK.circles` at circles.js:7, and the
step titles at circles.js:11, 26, 42, 54, 66, 81, 95. The file is still 110 lines and 6.7 kB.

## 2. `syms` keys against `Sim.live()`: 20 of 20 returned

Keys used: `lam k g N norm dx grid r a ph C S c s psi f wt v idx rgb`. `Sim.live()` (L737–L754) returns exactly these 20. `r`, `a`
and `ph` read `no sources` when N = 0. Every mark key has a table row. Four rows have no mark in their step: `grid` (step 2), `r`
(step 3), and `psi` and `rgb` (step 7). Those rows simply light nothing; this is not a fault.

Measured in headless Chromium 1194. The build is `OUT_DIR=/tmp/fig01-walk-dist npm run build`, and the built page and
`circles.js` are byte-identical to `public/`. Each viewport was read 1.5 s after load, then each step was clicked and read again
after 450 ms.

| Viewport | Steps drawn | Rendered code = `code` without marks | "Now" cells `—` or empty | Console errors |
|---|---|---|---|---|
| 1440 × 900 | 7 | 7 of 7 | 0 | 0 |
| 390 × 844 | 7 | 7 of 7 | 0 | 0 |

At 1440 × 900 the grid is 360 × 162, and the centre cell is (j, i) = (81, 180) at x = 401.11 px, y = 181.37 px. The sources are
at x = 200 and 600 px, with y<sub>s</sub> = 350.52 px. The "Now" values were:

- `r` = 262.79 px, `a` = 0.4384, `ph` = 55.038 rad
- `C` = −0.1016, `S` = −0.8574
- `k` = 0.2094 rad/px, `g` = 0.00050 /px, `v` = 33 px/s

At 390 × 844 the grid is 324 × 324, with `r` = 437.76 px and `a` = 0.4017.

## 3. The equations and notes against the lecture note

| Step | Walkthrough | Note | Verdict |
|---|---|---|---|
| 1 `math` | k = 2π/λ, g = γ/R, R = 300 px | (3) k = ω/v = 2π/λ; (5) a<sub>i</sub> = e<sup>−γr<sub>i</sub>/R</sup>, R = 300 px | same. The note has no g; the walkthrough defines it, and no symbol clashes. |
| 1 `note` | one wavelength adds 2π; γ = e-foldings over R = 300 px | §3 "phase gained per unit of distance", §4 "one full turn for every wavelength", §3.1 "factors of e … over 300 px" | same |
| 2 `math` | **x = (i + ½)Δx − x<sub>s</sub>, y = (j + ½)Δy − y<sub>s</sub>**, r = √(x² + y²) | (2) r<sub>i</sub> = √((x − x<sub>i</sub>)² + (y − y<sub>s</sub>)²), with x, y the point's coordinates and i the source | **M2** |
| 2 `note` | 800 px world, cell centres, y<sub>s</sub> = worldH − 10 | §2 800 px wide, sources 10 px above the bottom edge; §8 "at the centre of its cell" | same |
| 3 `math` | **a = e<sup>−gr</sup>/N**, φ = kr | (5) a<sub>i</sub> = e<sup>−γr<sub>i</sub>/R</sup>, without 1/N; (7) "an arrow of length a<sub>i</sub>/N" | **M3**. φ: the note has no name for kr; its only φ is the dummy angle of \|1 − e<sup>−iφ</sup>\| before (12). No clash. |
| 3 `note` | "**the crest you see at r** left the source r/v seconds ago" | §4 (new): v "is the speed of each ring, not always of the crests you see"; the crests of the sum climb at 1.55 v up the middle | **M4** |
| 4 `math` | **ψ = Σ<sub>s</sub> a<sub>s</sub> cos(kr<sub>s</sub> − ωt)**, **C = Σ<sub>s</sub> a<sub>s</sub> cos kr<sub>s</sub>**, S likewise | (6) ψ = (1/N) Σ<sub>i</sub> a<sub>i</sub> cos(kr<sub>i</sub> − ωt); (18) C = (1/N) Σ<sub>i</sub> a<sub>i</sub> cos kr<sub>i</sub> | **M3** (follows from step 3's a) |
| 4 `note` | from cos(A − B) with A = kr, B = ωt; one ω, so time factors out; C, S once per change | §8 the same expansion; "exact … because all sources share one ω"; recomputed on sources, λ, γ | same. A, B are dummies, but the note's A is the amplitude (7) (W3). |
| 5 `math` | ψ = C cos ωt + S sin ωt, clipped to [−1, 1] | (18); §9 "clipped to [−1, 1], a guard against rounding only" | same |
| 5 `note` | two multiplications and one addition per point; clip matters only by rounding | §8 "two multiplications and an addition, whatever N is"; §9 | same |
| 6 `math` | ωt ← ωt + 2πf Δt, v = fλ | §8 ωt ← ωt + 2πf Δt; (8) v = ω/k = fλ | same |
| 6 `note` | Δt real time, so 1 Hz = one cycle per second on any screen; "phase speed readout is just fλ" | §8 Δt "capped at 0.05 s"; §4 the Speed readout is the speed of each ring | not contradicted, but incomplete on both counts (W2) |
| 7 `math` | n = round(127.5ψ + 127.5); **colour = mid + (end − mid)·\|a<sub>n</sub>\|<sup>0.8</sup>, a<sub>n</sub> = n/127.5 − 1** | §9 n = round(127.5ψ + 127.5); (19) c = c<sub>0</sub> + (c<sub>±</sub> − c<sub>0</sub>)\|ψ\|<sup>0.8</sup> | **M5** |
| 7 `note` | −1 ink, 0 cream, +1 burgundy; 0.8 lifts small \|ψ\|; 256 colours built once | §9 the same | same |

No `math` or `note` field cites an equation number, so no "(n)" can point to the wrong equation. The note numbers its equations (1)
to (19) in order, and the teacher did not renumber them. The fixes below add the citations (2), (5), (6), (8) and (19). Each one was
checked against the note: (2) is r<sub>i</sub>; (5) is a<sub>i</sub> = e<sup>−γr<sub>i</sub>/R</sup>; (6) is the sum with 1/N;
(8) is v = ω/k = fλ; (19) is the colour formula.

## 4. Every mismatch and its exact fix

Old text is copied from `circles.js` as it stands, without its leading indentation; new text replaces it whole. Marks keep their
keys, except where M6 says otherwise. After the marks are stripped, no `code` fix changes the quoted text: it only adds a `...`
line or moves mark brackets.

**M1 · step 2 `code`: page line 642 left out without `...`. circles.js:32–33.** Page L641 is
`var y = (j + 0.5) * dy - sy, y2 = y * y;` and L643 is `var x = (i + 0.5) * dx - sx;`. Between them stands
L642, `for (var i = 0; i < cols; i++, p++) {`. The walkthrough prints L641 and L643 as if they were neighbours.

Old (circles.js:32–33):
```
var y = (j + 0.5) * dy - sy, y2 = y * y;
var x = (i + 0.5) * dx - sx;
```
New:
```
var y = (j + 0.5) * dy - sy, y2 = y * y;
...
var x = (i + 0.5) * dx - sx;
```
(An equally exact alternative is to quote L642 itself in place of the new `...` line. That would show the second of "the two inner
loops" that `where` names.)

**M2 · step 2 `math` and `note`: x and y. circles.js:28, 29.** In the note, x and y are the coordinates of the point P, and
(2) is r<sub>i</sub> = √((x − x<sub>i</sub>)² + (y − y<sub>s</sub>)²). The data store agrees: the coordinate `x` is
"x = (i + ½) Δx" (page L547). The walkthrough gives the same letters the offsets from the source, as the code does
(`var x = (i + 0.5) * dx - sx`). At the centre cell this makes x = 201.11 px in the walkthrough but 401.11 px in the note and the
store. The walkthrough also counts the sources with s and the grid columns with i, where the note's i is a source. The code forces
this, so the fix keeps it and says so.

Old (circles.js:28):
```
math: 'x = (i + ½)⟦dx|Δx⟧ − x<sub>s</sub>, &nbsp; y = (j + ½)Δy − y<sub>s</sub><br>⟦r|r⟧ = √(x² + y²)',
```
New:
```
math: 'x = (i + ½)⟦dx|Δx⟧, &nbsp; y = (j + ½)Δy<br>⟦r|r⟧ = √((x − x<sub>s</sub>)² + (y − y<sub>s</sub>)²)',
```

Old (circles.js:29):
```
note: 'The field lives on a fixed world 800 px wide, sampled on a coarse grid of cols × rows cells; (i + ½) puts each sample at the centre of its cell. Sources sit 10 px above the bottom edge, so y<sub>s</sub> = worldH − 10.',
```
New:
```
note: 'The field lives on a fixed world 800 px wide, sampled on a coarse grid of cols × rows cells; (i + ½) puts each sample at the centre of its cell. Sources sit 10 px above the bottom edge, so y<sub>s</sub> = worldH − 10. r is equation (2) of the note. The note counts the sources with i; here they are counted with s, because i and j count the columns and rows of the grid. In the code, x and y hold the offsets x − x<sub>s</sub> and y − y<sub>s</sub> from the source.',
```

**M3 · steps 3 and 4: the walkthrough's a already contains 1/N. circles.js:44, 45, 48, 56.** In the note,
a<sub>i</sub> = e<sup>−γr<sub>i</sub>/R</sup> ≤ 1 by (5). The 1/N stands outside the sum in (6) and (18), and (7) says "each source
contributes an arrow of length a<sub>i</sub>/N". The walkthrough writes a = e<sup>−gr</sup>/N, which is the note's a/N. With that
a, its step 4 drops the 1/N from ψ, C and S. Measured at the centre cell, the walkthrough's a is 0.4384, while the note's
a<sub>1</sub> = e<sup>−0.15 · 262.79/300</sup> is 0.8769. The fix keeps the code's `a`, marked as a/N.

Old (circles.js:44):
```
math: '⟦a|a⟧ = e<sup>−gr</sup> / N, &nbsp; ⟦ph|φ⟧ = k r',
```
New:
```
math: 'a = e<sup>−gr</sup> = e<sup>−γr/R</sup>, &nbsp; ⟦a|a/N⟧ = e<sup>−gr</sup> / N, &nbsp; ⟦ph|φ⟧ = k r',
```

Old (circles.js:45). The same line also carries M4; the new text fixes both:
```
note: 'The ring from source s at distance r has amplitude a and a phase lag kr behind the source: the crest you see at r left the source r/v seconds ago. The factor 1/N keeps the sum between −1 and 1 however many sources you add.',
```
New:
```
note: 'The ring from source s at distance r has amplitude a = e<sup>−gr</sup>, equation (5) of the note, and a phase lag kr behind the source: the crest of this ring at r left the source r/v seconds ago. The code’s a already carries the factor 1/N of equation (6), which keeps the sum between −1 and 1 however many sources you add.',
```

Old (circles.js:48):
```
['a', 'a', 'a', 'amplitude from source 1 at the centre'],
```
New:
```
['a', 'a/N', 'a', 'amplitude from source 1 at the centre, divided by N'],
```

Old (circles.js:56):
```
math: 'ψ = Σ<sub>s</sub> a<sub>s</sub> cos(k r<sub>s</sub> − ωt) = ⟦C|C⟧ cos ωt + ⟦S|S⟧ sin ωt<br>C = Σ<sub>s</sub> a<sub>s</sub> cos k r<sub>s</sub>, &nbsp; S = Σ<sub>s</sub> a<sub>s</sub> sin k r<sub>s</sub>',
```
New:
```
math: 'ψ = (1/N) Σ<sub>s</sub> a<sub>s</sub> cos(k r<sub>s</sub> − ωt) = ⟦C|C⟧ cos ωt + ⟦S|S⟧ sin ωt<br>C = (1/N) Σ<sub>s</sub> a<sub>s</sub> cos k r<sub>s</sub>, &nbsp; S = (1/N) Σ<sub>s</sub> a<sub>s</sub> sin k r<sub>s</sub>',
```

**M4 · step 3 `note`: "the crest you see", now contradicted by §4. circles.js:45.** The new §4 (L287) says v "is the speed of
each ring, not always of the crests you see". Where rings cross, the crests of the sum climb at 1.55 v. The step is about one
source's ring, and for that ring the sentence is right, but its words now say the opposite of the note. If M3 is not taken, apply
this alone: in circles.js:45 replace `the crest you see at r left the source r/v seconds ago` with
`the crest of this ring at r left the source r/v seconds ago`. The M3 text above already contains this change.

**M5 · step 7 `math`: the code's names in place of the note's symbols in (19). circles.js:97, 98.** The note writes the colour
table as c = c<sub>0</sub> + (c<sub>±</sub> − c<sub>0</sub>)|ψ|<sup>0.8</sup> (19): c<sub>0</sub> is cream, c<sub>+</sub> burgundy
and c<sub>−</sub> ink. The walkthrough writes mid, end and a<sub>n</sub>. Its a<sub>n</sub> also reuses the letter of the amplitude
a from step 3 for a different quantity.

Old (circles.js:97):
```
math: '⟦idx|n⟧ = round(127.5 ψ + 127.5) ∈ {0, …, 255}<br>colour = mid + (end − mid) · |a<sub>n</sub>|<sup>0.8</sup>, &nbsp; a<sub>n</sub> = n/127.5 − 1',
```
New:
```
math: '⟦idx|n⟧ = round(127.5 ψ + 127.5) ∈ {0, …, 255}<br>c = c<sub>0</sub> + (c<sub>±</sub> − c<sub>0</sub>) |ψ<sub>n</sub>|<sup>0.8</sup>, &nbsp; ψ<sub>n</sub> = n/127.5 − 1',
```

Old (circles.js:98):
```
note: 'ψ = −1 maps to ink, 0 to cream, +1 to burgundy. The exponent 0.8 < 1 lifts small |ψ| slightly, so the weak far field is still visible. All 256 colours are computed once at start-up.',
```
New:
```
note: 'This is equation (19) of the note, one row at a time: c<sub>0</sub> is the code’s mid (cream), c<sub>±</sub> its end, pos (burgundy) for ψ > 0 and neg (ink) for ψ < 0, and ψ<sub>n</sub>, the code’s a, is the value of ψ that row n stands for. ψ = −1 maps to ink, 0 to cream, +1 to burgundy. The exponent 0.8 < 1 lifts small |ψ| slightly, so the weak far field is still visible. All 256 colours are computed once at start-up.',
```

**M6 · step 6: the `f` mark sits on v, the `v` row quotes code that is not on the page, and `where` misses `readouts()`.
circles.js:82, 83, 85, 87, 91.** Pointing at f lights up `ds.get('v')`, the speed, as if it were the frequency. The `v` row has no
mark at all. Its "In code" entry `freq × λ` is not page code: the page writes `freq.value * lambda.value` (L711) and reads
`ds.get('v')` (L712). Splitting the `wt` mark lets `f` keep a mark in the code. The stripped code line is unchanged:
`omegaT += 2 * Math.PI * freq.value * dt;` (L762). Marks cannot nest, because `markup()` stops at the first `⟧`.

Old (circles.js:82): `where: 'Sim.clock callback',`
New: `where: 'Sim.clock callback; readouts() — the Speed readout',`

Old (circles.js:83): `math: '⟦wt|ωt⟧ ← ωt + 2π ⟦f|f⟧ Δt, &nbsp; v = f λ',`
New: `math: '⟦wt|ωt⟧ ← ωt + 2π ⟦f|f⟧ Δt, &nbsp; ⟦v|v⟧ = f λ',`

Old (circles.js:85):
```
code: `⟦wt|omegaT += 2 * Math.PI * freq.value * dt⟧;
```
New:
```
code: `⟦wt|omegaT⟧ += 2 * Math.PI * ⟦f|freq.value⟧ * dt;
```

Old (circles.js:87):
```
document.getElementById('r-v').textContent = Math.round(⟦f|ds.get('v')⟧) + ' px/s';`,
```
New:
```
document.getElementById('r-v').textContent = Math.round(⟦v|ds.get('v')⟧) + ' px/s';`,
```

Old (circles.js:91): `['v', 'v', 'freq × λ', 'phase speed, px/s']`
New: `['v', 'v', "ds.get('v')", 'phase speed, px/s']`

## 5. Smaller points: same meaning, optional

**W1 · step 1 `where`, circles.js:12.** The step quotes the first two lines of `precompute()` (L628, L629), but `where` says
"line 1".
Old: `where: 'precompute() — line 1',` New: `where: 'precompute() — lines 1 and 2',`

**W2 · step 6 `note`, circles.js:84.** Nothing here is contradicted, but two points are incomplete:

- Δt is capped at 0.05 s (`sim.js:179`; note §8). So "one full cycle per second on any screen" holds only while the screen draws
  at least 20 frames a second.
- The note now says the Speed readout is the speed of each ring, which the crests of the sum can exceed.

Old:
```
note: 'Δt is the real time between frames, so a 1 Hz setting completes one full cycle per second on any screen. The phase speed readout is just f λ in px/s.',
```
New:
```
note: 'Δt is the real time between frames, capped at 0.05 s, so a 1 Hz setting completes one full cycle per second on any screen that draws at least 20 frames a second. The Speed readout is just f λ in px/s, equation (8) of the note: the speed of each ring. Where two rings cross, the crests of their sum can run faster.',
```

**W3 · step 4 `note`, circles.js:57.** "cos(A − B) … with A = kr, B = ωt" uses A as a dummy, while the note's A is the amplitude
of (7). The note itself does the same with the identity in §5, so this is not wrong. The note's §8 states the expansion directly.
Fix, if wanted: replace `From cos(A − B) = cos A cos B + sin A sin B with A = kr, B = ωt.` with
`From cos(kr − ωt) = cos kr cos ωt + sin kr sin ωt, as in Section 8 of the note.`

**Aside, about the page, not the walkthrough.** The data store follows the code's a, not the note's:

- `a1` is "a = e<sup>−g r</sup> / N" (L554, and its check at L861).
- `C` and `S` are "Σ<sub>s</sub> a<sub>s</sub> cos(k r<sub>s</sub>)", without 1/N (L549, L550).

So the data panel shows the same a as the walkthrough, which is half the note's a<sub>1</sub> at the default N = 2. This is for the
teacher or the lead to judge. Changing those metadata strings would not move any line.

## 6. The check, to run again

The script below gave the counts in sections 1 and 2. The proposed fixes were applied by exact, unique string replacement to a
scratch copy of `circles.js` (never the original). On that copy:

- The same script reports 17 of 17 found, and step 2 now reads 630 ... 641 ... 643 644 with no silent elision.
- Every mark parses.
- In Chromium (the build with the copy swapped in, 1440 × 900 and 390 × 844), it draws 7 steps, the rendered code equals the
  stripped `code` on every step, no "Now" cell is `—`, and there are no console errors.

```js
// node check.cjs   (run from /home/user/SiteTest)
const fs = require('fs'), vm = require('vm');
const window = {}; vm.runInNewContext(fs.readFileSync('public/scripts/walk/circles.js', 'utf8'), { window });
const page = fs.readFileSync('public/simulations/Circular Wave Interference Visualization.html', 'utf8').split('\n');
const strip = s => s.replace(/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g, '$1');
let checked = 0, found = 0, elided = 0, whole = 0, inline = 0;
const report = [];
window.WALK.circles.steps.forEach((st, si) => {
  const lines = strip(st.code).split('\n').map(l => l.trim()).filter(Boolean);
  let prev = -1, gapAllowed = false; const seq = [];
  lines.forEach(line => {
    if (line === '...') { elided++; gapAllowed = true; seq.push('...'); return; }
    checked++;
    const frags = line.split('...').map(f => f.trim()).filter(Boolean);
    if (frags.length > 1) inline++;
    const match = pl => { let p = 0; return frags.every(f => { const k = pl.indexOf(f, p); if (k < 0) return false; p = k + f.length; return true; }); };
    const hits = page.map((pl, i) => match(pl) ? i + 1 : 0).filter(Boolean);
    if (!hits.length) { report.push(`NOT FOUND step ${si + 1}: ${line}`); seq.push('?'); return; }
    found++;
    // whole-line hits: trimmed page line equals the excerpt (or starts/ends with the fragments for an inline elision)
    const wl = hits.filter(n => { const t = page[n - 1].trim(); return frags.length > 1 ? (t.startsWith(frags[0]) && t.endsWith(frags[frags.length - 1])) : t === line; });
    if (wl.length) whole++; else report.push(`fragment only (not a whole line) step ${si + 1}: ${line} -> ${hits.join(',')}`);
    const cand = (wl.length ? wl : hits);
    // the next page line if no "..." stands between, else the first match after the previous line
    let pick = gapAllowed ? cand.find(n => n > prev) : cand.find(n => n === prev + 1);
    if (prev < 0) pick = cand[0];
    if (pick === undefined) { pick = cand.find(n => n > prev) || cand[0]; report.push(gapAllowed ? `after a "...", earlier in the page, step ${si + 1}: "${line}" at ${cand.join(',')} after ${prev}` : `SILENT ELISION step ${si + 1}: "${line}" at ${cand.join(',')} after ${prev}, page lines skipped without a "..." line`); }
    seq.push(pick); prev = pick; gapAllowed = false;
  });
  report.push(`step ${si + 1} (${st.where}): ${seq.join(' ')}`);
});
const src = page.join('\n'), live = src.slice(src.indexOf('Sim.live = function'), src.indexOf('var clk = Sim.clock'));
const keys = [...new Set([...live.matchAll(/(?:^|[{,\s])([A-Za-z0-9_]+)\s*:(?!\/)/g)].map(m => m[1]).concat([...live.matchAll(/out\.([A-Za-z0-9_]+)\s*=/g)].map(m => m[1])))];
const used = [...new Set(window.WALK.circles.steps.flatMap(s => s.syms.map(r => r[0])))];
const marks = [...new Set(window.WALK.circles.steps.flatMap(s => [...(s.math + s.code).matchAll(/⟦([A-Za-z0-9_]+)\|/g)].map(m => m[1])))];
console.log(report.join('\n'));
console.log({ codeLines: checked + elided, elisionLines: elided, checked, found, notFound: checked - found, whole, inline, keysUsed: used.length, used: used.join(' '), liveKeys: keys.join(' '), missing: used.filter(k => !keys.includes(k)), marksWithoutRow: marks.filter(k => !used.includes(k)) });
// SILENT ELISION step 2: "var x = (i + 0.5) * dx - sx;" at 643 after 641, page lines skipped without a "..." line
// after a "...", earlier in the page, step 6: "document.getElementById('r-v')…" at 712 after 762
// { codeLines: 21, elisionLines: 4, checked: 17, found: 17, notFound: 0, whole: 17, inline: 0, keysUsed: 20, missing: [], marksWithoutRow: [] }
```

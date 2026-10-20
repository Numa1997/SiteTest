# Fig. 4 · walkthrough check (`tl`)

Checked on 20 October 2026 by the walkthrough keeper, at commit `127a8d2` (the working copy equals it for both files).

- Page: `public/simulations/Transverse and longitudinal waves.html`, 1 086 lines; lecture note at lines 99–722;
  `#walk[data-walk="tl"]` at line 724; `Sim.live()` at lines 964–976.
- Walkthrough: `public/scripts/walk/tl.js`, 110 lines, 7 477 bytes, 7 steps.
- `tl.js` was not changed: Numa has not allowed it. Every fix below is written out so it can be applied as it stands once he does.

## Counts

| What | Checked | Found / matching | Not found / mismatched |
|---|---|---|---|
| Code lines (marks stripped, `...` lines left out) | 16 | 16 | 0 |
| Lines that are only `...` | 5 | (not searched) | |
| Lines with an inline `...` | 0 | | |
| Lines quoted together that are page neighbours | 4 joins | 3 | 1 (step 1: page 802 → 805 with no `...`) |
| Keys in `syms` returned by `Sim.live()` | 19 | 19 | 0 |
| Equation numbers "(n)" cited in `math` or `note` | 0 | | |
| `math` fields | 7 | 6 | 1 (step 7, symbol) |
| `note` fields | 7 | 6 | 1 (step 1, contradicted by the edited note) |
| Marks inside `note` (known, report only) | 1 | | 1 (step 6, tl.js:85) |

The code is quoted exactly. One elision is not marked. In the algebra, one symbol differs from the note, and one claim is now
contradicted by the edited note.

## 1. The code lines: 16 of 16 found verbatim

Method from `docs/scripts/walk.md`, "The rule": evaluate `tl.js` in Node with a stub `window`, strip the marks with
`/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g → '$1'`, drop lines that are only `...`, split each remaining line on `...`, and look for the
fragments in order on one page line. A second, stricter pass checked that each line equals a whole page line after trimming,
and that lines quoted with no `...` between them are neighbours in the page.

| Step | `where` | Page lines quoted (`...` = lines left out) | Verdict |
|---|---|---|---|
| 1 One wave function for both rows | the clock and readouts() | 978 ... 802 805 806 | all found, whole lines; **802 → 805 skips 803–804 with no `...`** |
| 2 The transverse row | draw() — transverse beads | 899 ... 902 | all found, whole lines (the `X = …` line also occurs at 883 and 926; 899 is the bead loop) |
| 3 Where the crests are | draw() — the tan crest markers | 874 875 | all found, whole lines |
| 4 The longitudinal row | longAmp() and draw() — longitudinal beads | 799 ... 927 | all found, whole lines |
| 5 Why the amplitude is capped | longAmp() — the 0.8 | 799 | found, whole line |
| 6 Compressions and their shading | draw() — gradient and compression markers | 912 913 ... 917 | all found, whole lines |
| 7 World pixels into screen pixels | draw() — line 1 | 835 ... 837 | all found, whole lines |

**Mismatch 1 (format, not text).** Step 1, tl.js:17–18. The excerpt goes from page line 802 (`var v = …`) straight to line 805
(`… 'r-t' …`). Lines 803–804 (the `r-v` and `cap-v` readouts) are left out without a `...` line. `docs/scripts/walk.md` says a
line that is only `...` stands for page lines left out. This is older than the note edit.

Fix: insert a line that is only `...` between tl.js:17 and tl.js:18:

```
var ⟦v|v = freq.value * lambda.value⟧;
...
document.getElementById('r-t').textContent = (⟦T|1 / freq.value⟧).toFixed(2) + ' s';
```

## 2. `syms` keys: 19 of 19 returned by `Sim.live()`

Read from the code (lines 964–976), then measured. The page was built with
`APPDEPLOY_VITE_OUT_DIR=/tmp/fig04-walk-dist npm run build` (built `tl.js` and page byte-identical to the sources) and opened in
headless Chromium at 1440 × 900. After 1.5 s, `Sim.live()` returned exactly the 19 keys used in `syms`, no more and no fewer:
`f k wt v T X phase xi yi xc xp AL A xl AkL rho comp s yT`. All 7 steps drew, every "Now" cell in every step filled (none at
`—`), and the console showed no errors.

## 3. Equations in `math` against the lecture note

No step cites an equation number, so there is no "(n)" to check.

| Step | `math` | Lecture note | Verdict |
|---|---|---|---|
| 1 | ξ(X, t) = A sin(kX − ωt); k = 2π/λ, ω = 2πf, v = ω/k = fλ, T = 1/f | eq. (1); eq. (2); T = 1/f in §3, line 355 | match |
| 2 | X<sub>i</sub> = i · 640/(N − 1); y<sub>i</sub> = y<sub>T</sub> − A s sin(kX<sub>i</sub> − ωt) | §7, line 685: X<sub>i</sub> = i · 640/(N − 1); §8, line 694: height y<sub>T</sub> − s ξ | match |
| 3 | crest at kX − ωt = π/2 + 2πn ⇒ X<sub>c</sub> = (π/2 + ωt)/k mod λ | §3, line 460: X<sub>c</sub> = (π/2 + ωt)/k plus whole wavelengths | match |
| 4 | A<sub>L</sub> = min(A, 0.8/k); x<sub>i</sub> = X<sub>i</sub> + A<sub>L</sub> sin(kX<sub>i</sub> − ωt) | eq. (12); x = X + ξ in §2, line 134; Figure 3 caption | match |
| 5 | dx/dX = 1 + A<sub>L</sub>k cos(kX − ωt) ≥ 1 − A<sub>L</sub>k; ρ/ρ<sub>0</sub> = 1/(1 + A<sub>L</sub>k cos(kX − ωt)) | eq. (10); spacing 1 + ∂ξ/∂X in §5, line 507 | match |
| 6 | densest at cos(kX − ωt) = −1 ⇒ X<sub>p</sub> = (π + ωt)/k mod λ; X<sub>p</sub> − X<sub>c</sub> = (π/2)/k = λ/4 | §5, line 504; eq. (11), written (π − π/2)/k, the same value | match |
| 7 | s = (W − 44)/640, **x<sub>screen</sub>** = 22 + X s; y<sub>T</sub> = 0.3 H, y<sub>L</sub> = 0.77 H | eq. (17): s = (W − 44)/640, **x<sub>upper</sub>** = 22 + sX, x<sub>lower</sub> = 22 + s(X + ξ); §8, line 694: 30 % and 77 % of the height | **symbol differs** |

**Mismatch 2 (symbol).** Step 7, tl.js:99. The walkthrough calls the screen position x<sub>screen</sub>. The note's eq. (17)
calls the same quantity x<sub>upper</sub>, and has a second one, x<sub>lower</sub>, for the lower row. Same meaning, different
symbol.

Fix, in `math` of step 7, replace

```
x<sub>screen</sub> = 22 + X s
```

with

```
x<sub>upper</sub> = 22 + s X
```

## 4. Claims in `note` against the edited lecture note

| Step | Claim | Lecture note | Verdict |
|---|---|---|---|
| 1 | “The same function drives both rows; the only difference is the direction of ξ” | §2, line 137 (edited): the lower row’s amplitude A<sub>L</sub> equals A only at the default settings. §3, Exercise 3.1, line 470 (edited): “The lower row differs here: at 110 px the cap of Section 5 lowers its amplitude to 14 px” | **contradicted** |
| 2 | bead keeps its x; minus sign because screen y points down | §8, line 694 | agrees |
| 3 | true modulo; X<sub>c</sub> moves at dX<sub>c</sub>/dt = ω/k = v | eq. (2); §3, line 460 | agrees |
| 4 | the same ξ added along the travel; nothing travels, only the pattern | §2, line 142 (“Both rows carry the same ξ”, not edited); §1 | agrees (see the optional note in section 5) |
| 5 | A<sub>L</sub>k = 1 would let beads pass through each other; with A<sub>L</sub>k ≤ 0.8 the tightest spacing is 20 % of rest, the densest point 5 × rest | §5, lines 507–509; edited line 137 (“about a quarter” at A<sub>L</sub>k = 0.743, inside the 20 % bound) | agrees |
| 6 | each compression λ/4 ahead of a crest; band darkens as max(0, −cos(kX − ωt)), 65 points | eq. (11); §8, line 698 | agrees; holds the known raw mark |
| 7 | the row is 640 world px; 22 px margins give the 44 | §8, line 692; eq. (17) | agrees |

**Mismatch 3 (claim contradicted).** Step 1, tl.js:14. “The only difference is the direction of ξ” holds only while the cap is
off. The edited note now says the lower row can have a smaller amplitude. Measured in Chromium: at λ = 220 px, `Sim.live()` gives
A = 26 px and A<sub>L</sub> = 26.00 px; at λ = 110 px it gives A = 26 px and A<sub>L</sub> = 14.01 px (capped). The page readout
shows “14 px (cap)”.

Fix, in `note` of step 1, replace

```
The same function drives both rows; the only difference is the direction of ξ, across the travel (transverse) or along it (longitudinal).
```

with

```
The same function drives both rows; the difference is the direction of ξ, across the travel (transverse) or along it (longitudinal), and in the lower row an amplitude A<sub>L</sub> that the cap of step 5 can make smaller than A.
```

**Known, report only: a mark inside `note`.** Step 6, tl.js:85: `⟦comp|max(0, −cos(kX − ωt))⟧`. `note` is inserted without
`markup()`, so the mark is not turned into a span. Measured in Chromium: the step 6 card shows the raw text
“⟦comp|max(0, −cos(kX − ωt))⟧”.

Fix (when allowed), in `note` of step 6, replace `⟦comp|max(0, −cos(kX − ωt))⟧` with `max(0, −cos(kX − ωt))`.

## 5. Not mismatches with the note; optional

- **Words.** The walkthrough says “world px” and “bead”. The note says “pixels of the medium” (§8 is titled “From medium pixels
  to screen pixels”) and “particle”. Same meaning.
- **Step 4, the `xl` mark.** In `math` and in `Sim.live()` (`ds.get('xL')`), x<sub>i</sub> is in world pixels. The marked code
  `px = left + (X + AL * Math.sin(k * X - omegaT)) * s` is the screen position, x<sub>lower</sub> of eq. (17). The code stays
  verbatim if the mark moves inside the brackets: `px = left + (⟦xl|X + AL * Math.sin(k * X - omegaT)⟧) * s;`.
- **Step 4, “The same ξ”.** The formula above it uses A<sub>L</sub>, not A. If mismatch 3 is fixed, “The same ξ, with
  A<sub>L</sub> for A, now added along the direction of travel.” keeps the two steps in line.
- **Step 5, the `AkL` mark.** The symbol A<sub>L</sub>k has no unit (live value 0.7426). The marked code
  `0.8 * lambda.value / (2 * Math.PI)` is the cap 0.8/k, a length (28.0 px at the defaults). The tie is loose, but it is not
  wrong: the cap is where A<sub>L</sub>k ≤ 0.8 is enforced.
- **Step 7, `where`.** “draw() — line 1” quotes draw()’s lines 1 and 3 (page 835 and 837). Exact text: `draw() — lines 1 and 3`.

## How to re-run

Scripts were kept in the scratchpad, not in the repository. The core of the code check, in Node:

```js
const fs = require('fs'), vm = require('vm'), c = { window: {} }; vm.createContext(c);
vm.runInContext(fs.readFileSync('public/scripts/walk/tl.js', 'utf8'), c);
const page = fs.readFileSync('public/simulations/Transverse and longitudinal waves.html', 'utf8').split('\n');
const strip = s => s.replace(/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g, '$1');
for (const st of c.window.WALK.tl.steps) for (const ln of strip(st.code).split('\n')) {
    if (!ln.trim() || ln.trim() === '...') continue;
    const fr = ln.split('...');
    const hit = page.some(pl => { let p = 0; return fr.every(f => { const i = pl.indexOf(f, p); if (i < 0) return false; p = i + f.length; return true; }); });
    if (!hit) console.log('NOT FOUND:', ln);
}
```

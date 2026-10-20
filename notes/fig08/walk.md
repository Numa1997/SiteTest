# Fig. 8 · walkthrough check (`dft`)

Checked on 20 October 2026 by the walkthrough keeper, at commit `c29e570` (working copy equal to it for both files).

- Page: `public/simulations/draw-decompose.html`, 1 416 lines; lecture note at lines 136–608; `#walk[data-walk="dft"]` at line 610.
- Walkthrough: `public/scripts/walk/dft.js`, 109 lines, 6 388 bytes, 6 steps.
- `dft.js` was not changed: Numa has not allowed it. Every fix below is written out so it can be applied as it stands once he does.

## Counts

| What | Checked | Found / matching | Not found / mismatched |
|---|---|---|---|
| Code lines (marks stripped, `...` lines left out) | 22 | 22 | 0 |
| Lines that are only `...` | 7 | (not searched) | |
| Lines with an inline `...` | 0 | | |
| Keys in `syms` returned by `Sim.live()` | 22 | 22 | 0 |
| Equation numbers "(n)" cited in `math` or `note` | 0 | | |
| `math` fields | 6 | 1 (step 1) | 5 (steps 2, 3, 4, 5, 6) |
| `note` fields with an equation or a claim from the note | 6 | 3 (steps 1, 5, 6) | 3 (steps 2, 3, 4) |
| `syms` symbols and meanings | 22 rows | 16 | 6 rows in steps 2, 5, 6; 4 more optional, in steps 3 and 4 |

The code is quoted exactly. The mismatches are all in the algebra: symbols that mean something else in the note, and three claims
that the note now words more carefully.

## 1. The code lines: 22 of 22 found verbatim

Method from `docs/scripts/walk.md`, "The rule": evaluate `dft.js` with a stub `window`, strip the marks with
`/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g → '$1'`, trim, drop lines that are only `...`, split each remaining line on `...`, and look for the
fragments in order on one page line. Then a second, stricter pass: each line equals a whole page line after trimming, and lines
quoted together without a `...` between them are neighbours in the page.

| Step | `where` | Page lines quoted (`...` = lines left out) | Verdict |
|---|---|---|---|
| 1 Equal arc length | `resamp()` | 737 738 ... 741 | all found; whole lines; `where` true |
| 2 Remove the centre | `decompose()` | 787 788 ... 791 | all found; whole lines; `where` true |
| 3 One coefficient | `dft()` — the double loop | 759 760 761 ... 763 764 | all found; whole lines; `where` true |
| 4 Radius, phase and sorting | `dft()` — end | 765 ... 767 | all found; whole lines; `where` true |
| 5 Circles redraw the shape | `chainAt()` and the clock | 773 774 775 776 ... 1276 | all found; whole lines; `where` true |
| 6 The check: Parseval | `rebuild()` | 816 817 ... 822 ... 825 | all found; whole lines; `where` true |

`re /= N;` and `im /= N;` also occur inside `dftOne()` at line 1298, as fragments of a longer line; the whole-line match is
763 and 764, inside `dft()`, as `where` says. No line was not found, so there is no code fix.

## 2. `syms` keys against `Sim.live()`: 22 of 22 returned

Keys used: `N L ds mx my z0 E k1 re im A ph K tot t tl x y kept cap err errP`. `Sim.live()` (page lines 1254–1269) returns all of
them, plus `src`, in both branches (before and after a shape exists). Every value is read from the store; `x` and `y` are written by
`draw()` at line 1059.

Measured in headless Chromium (build in `/tmp/fig08-walk-dist`, byte-identical to `public/`; viewport 1400 × 1000; 1.5 s after load):
6 steps drawn; on every step no "Now" cell is `—` or empty; the rendered code of every step equals its code field with marks stripped;
0 console errors. Values for the default heart, K = 24:

| Key | Now | Note says |
|---|---|---|
| `N` | 256 | N = 256 |
| `L` | 5.4276 | L = 5.428 (section 6.1) |
| `ds` | 0.02128 | Δs = L/255 = 0.021 (section 9) |
| `E` | 0.51504 | ⟨\|z\|²⟩ = 0.5150 (section 5) |
| `k1`, `A` | −1, 0.69692 | largest circle k = −1 (section 5) |
| `cap` | 99.994 % | 99.99 % kept (section 5) |
| `err`, `errP` | 0.005406, 0.005406 | e = 0.00541 at K = 24 (section 5) |
| `tl` | 12 s | 12 s by default (section 2) |

## 3. The equations against the note

| Step | Walkthrough | Note | Verdict |
|---|---|---|---|
| 1 `math` | s<sub>i</sub> = Σ<sub>j≤i</sub>\|p<sub>j</sub> − p<sub>j−1</sub>\|, L = s<sub>last</sub>, Δs = L/(N − 1) | section 7: the same s<sub>i</sub>, stroke points p<sub>j</sub>, total length L, Δs = L/(N−1) | same symbols, same meaning |
| 1 `note` | equal spacing makes t proportional to distance; pen at constant speed | section 7, Fig. 2 caption | same |
| 2 `math` | z<sub>n</sub> = **p<sub>n</sub>** − (x̄ + iȳ); ⟨\|z\|²⟩ = (1/N) Σ \|z<sub>n</sub>\|² | p<sub>j</sub> are the raw stroke points (section 7); ⟨\|z\|²⟩ as in (8) | **M1** |
| 2 `note` | mean exactly c<sub>0</sub>; origin **at the** wire's centre of mass; ⟨\|z\|²⟩ **is** the wire's I/m | section 2 and under (8): only approximately the wire's; exactly I/m of equal point masses at the samples | **M2** |
| 3 `math` | c<sub>k</sub> = (1/N) Σ z<sub>n</sub> e<sup>−2πikn/N</sup> = **a + ib** | (4); in (7), a<sub>n</sub> = 2πkn/N is the angle | **M4** |
| 3 `note` | z<sub>n</sub> = **x + iy**, e<sup>−i**θ**</sup> = cos θ − i sin θ, parts x cos θ + y sin θ, y cos θ − x sin θ | (7): z<sub>n</sub> = x<sub>n</sub> + iy<sub>n</sub>, angle a<sub>n</sub>; θ<sub>j</sub> is an arm's angle (Fig. 1) | **M5** |
| 4 `math` | \|c<sub>k</sub>\| = √(**a² + b²**), arg c<sub>k</sub> = atan2(**b, a**); keep the K largest | section 5 box | **M6** (follows from M4) |
| 4 `note` | keeping the largest **minimises the squared error** | box under (9): within the 120 computed components, at the samples, not over all 256 bins | **M7** |
| 5 `math` | **z<sub>K</sub>**(t) = Σ<sub>**top K**</sub> \|c<sub>k</sub>\| e<sup>i(kt + arg c<sub>k</sub>)</sup> = x + iy; t ← t + 2πΔt/T<sub>loop</sub> | (15): t ← t + 2πΔt/T<sub>loop</sub>, z(t) = Σ<sub>rank&lt;K</sub> \|c<sub>k</sub>\| e<sup>i(kt + arg c<sub>k</sub>)</sup> | **M8** (same meaning, other symbols) |
| 5 `note` | inverse DFT with all 256 reproduces the samples; only −60 to 60, so K = 120 leaves a residual | sections 4.1 and 9 | same |
| 6 `math` | **e<sub>RMS</sub>** measured = √(⟨\|z\|²⟩ − Σ<sub>**kept**</sub>\|c<sub>k</sub>\|²) | (9): e<sub>K</sub>, kept set S, Σ<sub>k∈S</sub> | **M10** (same meaning, other symbols) |
| 6 `note` | two routes to one number: 256 samples measured, squared radii added | section 5, "The panel shows this result twice" | same |

No `math` or `note` field cites an equation number, so no "(n)" can point to the wrong equation. The fixes below add five
citations, (4), (7), (8), (9) and section 7.1. Each was checked against the note: (4) is the sum c<sub>k</sub> = (1/N)Σ z<sub>n</sub>
e<sup>−2πikn/N</sup>, (7) its real and imaginary parts, (8) Parseval with ⟨|z|²⟩, (9) the error e<sub>K</sub>, and 7.1 the repeated
endpoint.

## 4. Every mismatch and its exact fix

Old text is copied from `dft.js` as it stands; new text replaces it whole. Marks are kept with the same keys, so the lighting and
the table still work.

**M1 · step 2 `math`, dft.js:27.** In the note and in step 1, p<sub>j</sub> are the raw stroke points, counted along the stroke.
The code subtracts the mean from the resampled points `r` (page line 788), not from the stroke points.

Old:
```
math: 'z<sub>n</sub> = p<sub>n</sub> − (⟦mx|x̄⟧ + i⟦my|ȳ⟧), &nbsp; ⟦E|⟨|z|²⟩⟧ = (1/N) Σ |z<sub>n</sub>|²',
```
New:
```
math: 'z<sub>n</sub> = r<sub>n</sub> − (⟦mx|x̄⟧ + i⟦my|ȳ⟧), &nbsp; ⟦E|⟨|z|²⟩⟧ = (1/N) Σ |z<sub>n</sub>|²',
```

**M2 · step 2 `note`, dft.js:28.** The note says the sample mean only approximates the uniform wire's centre of mass, because the
resampling repeats the endpoint (section 2, section 7.1). It says ⟨|z|²⟩ is exactly I/m for equal point masses at the samples and
only approximately the wire's (paragraph under (8)). The walkthrough says both are exact for the wire. "Exactly c<sub>0</sub>" holds
only for the computed coefficient (4) at k = 0, not for the loop average of section 2. The new text also defines r<sub>n</sub> (M1).

Old:
```
note: 'The mean is exactly c<sub>0</sub>, the circle that does not turn. Subtracting it puts the origin at the centre of mass of a uniform wire bent into your shape. ⟨|z|²⟩ is then that wire’s moment of inertia per unit mass, I/m, which the circles share out between them.',
```
New:
```
note: 'Here r<sub>n</sub> is sample n of step 1, a distance nΔs along the stroke. The mean of the samples is exactly the computed c<sub>0</sub> of (4), the circle that does not turn. Subtracting it puts the origin at the centre of mass of N equal point masses at the samples. That is close to the centre of mass of a uniform wire bent into your shape, but not equal to it, because the resampling repeats the endpoint (section 7.1 of the note). ⟨|z|²⟩ is then the moment of inertia per unit mass, I/m, of those point masses, as under (8), and the circles share it out between them.',
```

**M3 · step 2 `syms`, dft.js:34 and 37.** "Raw" is the word step 1 uses for the pointer's own points; `meanX` is the mean of the
resampled points. "I/m of the wire" has the same problem as M2.

Old:
```
['mx', 'x̄', 'meanX', 'centre of the raw samples'],
['E', '⟨|z|²⟩', 'meanZ2', 'mean squared radius = I/m of the wire']
```
New:
```
['mx', 'x̄', 'meanX', 'mean of the samples, before centring'],
['E', '⟨|z|²⟩', 'meanZ2', 'mean squared radius = I/m of equal masses at the samples']
```

**M4 · step 3 `math`, dft.js:43.** In the note, a<sub>n</sub> = 2πkn/N is the angle (section 4.3, (7)), and in the quoted code
`var a = TAU * k * n / N` it is the angle too. The walkthrough uses a for Re c<sub>k</sub>. The note names the parts Re c<sub>k</sub>
and Im c<sub>k</sub>.

Old:
```
math: 'c<sub>k</sub> = (1/N) Σ<sub>n</sub> z<sub>n</sub> e<sup>−2πikn/N</sup> = ⟦re|a⟧ + i⟦im|b⟧',
```
New:
```
math: 'c<sub>k</sub> = (1/N) Σ<sub>n</sub> z<sub>n</sub> e<sup>−2πikn/N</sup> = ⟦re|Re c<sub>k</sub>⟧ + i⟦im|Im c<sub>k</sub>⟧',
```

**M5 · step 3 `note`, dft.js:44.** The note writes z<sub>n</sub> = x<sub>n</sub> + iy<sub>n</sub> and calls the angle a<sub>n</sub>
(section 4.3). θ in the note is an arm's angle θ<sub>j</sub> (Figure 1). And x + iy in step 5 of the walkthrough is the pen, not a sample.

Old:
```
note: 'Writing z<sub>n</sub> = x + iy and e<sup>−iθ</sup> = cos θ − i sin θ, the real part is x cos θ + y sin θ and the imaginary part is y cos θ − x sin θ. The table shows the largest coefficient.',
```
New:
```
note: 'Writing z<sub>n</sub> = x<sub>n</sub> + iy<sub>n</sub>, a<sub>n</sub> = 2πkn/N and e<sup>−ia</sup> = cos a − i sin a, the real part is x<sub>n</sub> cos a<sub>n</sub> + y<sub>n</sub> sin a<sub>n</sub> and the imaginary part is y<sub>n</sub> cos a<sub>n</sub> − x<sub>n</sub> sin a<sub>n</sub>: the two lines of (7), with the code’s a. The table shows the largest coefficient.',
```

**M6 · step 4 `math`, dft.js:60.** This follows from M4: a and b are no longer the parts of c<sub>k</sub>.

Old:
```
math: '⟦A||c<sub>k</sub>|⟧ = √(a² + b²), &nbsp; ⟦ph|arg c<sub>k</sub>⟧ = atan2(b, a); &nbsp; keep the ⟦K|K⟧ largest',
```
New:
```
math: '⟦A||c<sub>k</sub>|⟧ = √((Re c<sub>k</sub>)² + (Im c<sub>k</sub>)²), &nbsp; ⟦ph|arg c<sub>k</sub>⟧ = atan2(Im c<sub>k</sub>, Re c<sub>k</sub>); &nbsp; keep the ⟦K|K⟧ largest',
```

**M7 · step 4 `note`, dft.js:61.** The note limits the claim. Keeping the largest is best within the 120 components the page
computes, in the least-squares sense at the samples. It is "not a search over all 256 DFT bins" (box under (9)).

Old:
```
note: 'Each coefficient is one circle: radius |c<sub>k</sub>|, turning k times per loop, starting at angle arg c<sub>k</sub>. Parseval (step 6) shows that keeping the largest ones minimises the squared error.',
```
New:
```
note: 'Each coefficient is one circle: radius |c<sub>k</sub>|, turning k times per loop, starting at angle arg c<sub>k</sub>. Parseval (step 6, equation (9)) shows that, among the 120 circles the page computes, keeping the largest ones minimises the squared error at the samples.',
```

**M8 · step 5 `math`, dft.js:75.** Same meaning as (15), other symbols: z<sub>K</sub> for z, "top K" for "rank < K", and the
two halves in the other order. The fix takes (15) as written. If the teacher would rather keep z<sub>K</sub>, which is clearer,
then (15) in the note must change to match, not the other way round.

Old:
```
math: 'z<sub>K</sub>(⟦t|t⟧) = Σ<sub>top K</sub> |c<sub>k</sub>| e<sup>i(kt + arg c<sub>k</sub>)</sup> = ⟦x|x⟧ + i⟦y|y⟧, &nbsp; t ← t + 2π Δt / ⟦tl|T<sub>loop</sub>⟧',
```
New:
```
math: '⟦t|t⟧ ← t + 2π Δt / ⟦tl|T<sub>loop</sub>⟧, &nbsp; z(t) = Σ<sub>rank &lt; K</sub> |c<sub>k</sub>| e<sup>i(kt + arg c<sub>k</sub>)</sup> = ⟦x|x⟧ + i⟦y|y⟧',
```

**M9 · step 5 `syms`, dft.js:85.** The table writes T. The formula above it and (15) write T<sub>loop</sub>.

Old: `['tl', 'T', 'loop.value', 'seconds per loop'],`
New: `['tl', 'T<sub>loop</sub>', 'loop.value', 'seconds per loop'],`

**M10 · step 6 `math` and `syms`, dft.js:93, 102, 104, 105.** In (9) the error is e<sub>K</sub> and the kept set is S. The
walkthrough writes e<sub>RMS</sub>, Σ<sub>kept</sub> and a bare e.

Old:
```
math: '⟦err|e<sub>RMS</sub>⟧ measured point by point &nbsp; = &nbsp; ⟦errP|√(⟨|z|²⟩ − Σ<sub>kept</sub>|c<sub>k</sub>|²)⟧',
['kept', 'Σ|c|²', 'kept', 'share of ⟨|z|²⟩ in the K circles'],
['err', 'e (direct)', 'err', 'RMS distance at the samples'],
['errP', 'e (Parseval)', 'errP', 'predicted RMS distance']
```
New:
```
math: '⟦err|e<sub>K</sub>⟧ measured point by point &nbsp; = &nbsp; ⟦errP|√(⟨|z|²⟩ − Σ<sub>k∈S</sub>|c<sub>k</sub>|²)⟧',
['kept', 'Σ<sub>k∈S</sub>|c<sub>k</sub>|²', 'kept', 'share of ⟨|z|²⟩ in the K circles'],
['err', 'e<sub>K</sub> (direct)', 'err', 'RMS distance at the samples'],
['errP', 'e<sub>K</sub> (Parseval)', 'errP', 'predicted RMS distance']
```

**Optional, for the same symbols everywhere · step 3 `syms` dft.js:53–54, step 4 `syms` dft.js:66–67.** The table drops the
subscript that the formula beside it carries. These rows are not wrong.

Old: `['re', 'Re c', 're', '']`, `['im', 'Im c', 'im', '']`, `['A', '|c|', 'amp', …]`, `['ph', 'arg c', 'phase', …]`
New: `['re', 'Re c<sub>k</sub>', 're', '']`, `['im', 'Im c<sub>k</sub>', 'im', '']`, `['A', '|c<sub>k</sub>|', 'amp', …]`,
`['ph', 'arg c<sub>k</sub>', 'phase', …]`

None of the fixes touches a `code` field, a `where` field or a key, so the 22 code lines and the 22 live keys stay as checked. The
new `note` texts hold no mark (a mark in `note` shows as raw text; `docs/scripts/walk.md`, note 4).

Dry run: each of the 14 "Old" lines above occurs exactly once in `dft.js`. All of them were applied to a copy in the build folder
only, and that copy was rendered in headless Chromium. Result: 6 steps, the same marks per step, no "Now" cell at `—`, code
identical, 0 console errors. Then the build copy was restored; `public/scripts/walk/dft.js` was never touched.

## 5. The check, to run again

```js
// node check.cjs   (run from /home/user/SiteTest)
const fs = require('fs'), vm = require('vm');
const ctx = { window: {} }; vm.createContext(ctx);
vm.runInContext(fs.readFileSync('public/scripts/walk/dft.js', 'utf8'), ctx);
const page = fs.readFileSync('public/simulations/draw-decompose.html', 'utf8').split('\n');
const strip = s => s.replace(/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g, '$1');
let checked = 0, found = 0;
ctx.window.WALK.dft.steps.forEach((st, si) => st.code.split('\n').forEach(raw => {
  const line = strip(raw).trim(); if (!line || line === '...') return;
  checked++;
  const frags = line.split('...').map(f => f.trim()).filter(Boolean);
  const hit = page.findIndex(pl => { let p = 0; return frags.every(f => { const k = pl.indexOf(f, p); if (k < 0) return false; p = k + f.length; return true; }); });
  if (hit >= 0) found++; else console.log('NOT FOUND, step', si + 1, ':', line);
}));
console.log({ checked, found, notFound: checked - found });   // { checked: 22, found: 22, notFound: 0 }
```

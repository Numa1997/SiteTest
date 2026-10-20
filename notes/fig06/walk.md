# Fig. 6 · walkthrough `bench` · check against the page and the note

> Lead's note, 20 October 2026: these proposed fixes were written before some later edits of the note and were audited
> against the current notes afterwards (docs/research-theory-audit.md, "Open, for Numa"). Fixes that touch a `code` or
> `where` field need the same permission as the rest. Nothing here has been applied; the walkthrough file is unchanged.


Checked on 20 October 2026 by the walkthrough keeper. Read only; the walkthrough is not changed (Numa has not allowed it).

| | |
|---|---|
| Walkthrough | `public/scripts/walk/bench.js`, 123 lines, md5 `cf0994b45ec7ae0fa61ab1e17283ccb5` |
| Page | `public/simulations/wave-interference.html`, 977 lines, md5 `07c241532c6c43dcba5914f848dd58a4` (after the teacher's edits) |
| Note | lines 104–479, between `<article class="paper" id="paper">` and `</article>`, equations (1)–(20) |
| Rule | `docs/scripts/walk.md`, "Elisions in the code" and "The rule: excerpts stay identical to the page code" |

## Counts

| Check | Result |
|---|---|
| Non-empty code lines in the 8 steps | 23 |
| Lines that are only `...` | 4 |
| Code lines checked | **19** |
| Found verbatim on one page line | **19** |
| Not found | **0** |
| Lines with an inline `...` | 1 (step 7, 2 fragments, both on page line 737) |
| Code text drawn by `sim.js` in Chromium equals the source with marks removed | 8 of 8 steps |
| Page lines left out with no `...` line | **2** (items E1, E2) |
| Equation numbers "(n)" cited in the walkthrough | 0 |
| Equation and symbol mismatches with the note | **7** (items M1–M7) |
| Keys in `syms` | 24, all 24 returned by `Sim.live()` |

## The code lines (all 19 found)

| Step | Excerpt line | Page line |
|---|---|---|
| 1 | `function y(w, X) { … }` | 622 |
| 2 | `var samples = Math.max(2, Math.round(right - left));` · `...` · `var X = i / samples * WORLD_W, py = …;` | 654 · 684 |
| 3 | `var X = i / samples * WORLD_W, v = 0;` · `for (var j = 0; …) v += y(waves[j], X);` · `pk = Math.max(pk, Math.abs(v));` | 695 · 696 · 697 |
| 4 | `function nice(v) { … }` · `var sumRange = …;` · `var compRange = …;` · `...` · `pts.push(mid1 - v / sumRange * hSum / 2);` | 624 · 655 · 656 · 698 |
| 5 | `document.getElementById('p-beats')…` | 790 |
| 6 | `preset([1, 3, 5, 7].map(…));` | 792 |
| 7 | `var nu = …, g = groups[nu];` · `g.re += …;` · `g.im += …;` · `...` · `return { nu: g.nu, A: …, ... };` · `...` · `var X = function (nu) { … };` | 730 · 732 · 733 · 737 · 742 |
| 8 | `document.getElementById('r-sum')…` · `document.getElementById('r-peak')…` | 830 · 831 |

Every `where` field is still true: the lines sit in `y()`, `draw()`, `nice()`, the Beats and Square wave buttons, `lines()` and
`drawSpectrum()`, and the readout lines of the clock callback.

### Two silent elisions (not a verbatim failure)

`docs/scripts/walk.md` says a line that is only `...` stands for page lines left out. Two excerpts leave page lines out with no
`...` between them. The quoted lines are verbatim; the reader is told they are adjacent when they are not.

| # | Step | Where | What is left out | Fix in `bench.js` |
|---|---|---|---|---|
| E1 | 4 | between bench.js:60 (page 624) and bench.js:61 (page 655) | 30 page lines, 625–654: all of `panel()` and the first three lines of `draw()` | insert a line `...` after bench.js:60 |
| E2 | 7 | between bench.js:97 (page 730) and bench.js:98 (page 732) | page 731, `if (!g) { g = groups[nu] = { nu: nu, re: 0, im: 0, n: 0, colour: wv.colour }; out.push(g); }` | insert a line `...` after bench.js:97 |

Both insertions add a line to `bench.js` (123 → 125), so if they are made, these links must move in the same change:
`docs/scripts/walk.md:157` step titles 5–8 `#L71 #L82 #L93 #L110` → `#L72 #L83 #L94 #L112` and "123 / 9.0" → "125 / 9.0";
`docs/scripts/walk.md:115` `bench.js:101` → `bench.js:103`; `docs/scripts/walk.md:113` "267 non-empty code lines … 41 lines that
are only `...`" → 269 and 43 (226 lines of code unchanged); `docs/scripts/walk.md:5` "1 199 lines" → "1 201 lines";
`docs/simulations/fig06-wave-bench.md:316` `bench.js:7-123` → `bench.js:7-125`.

## The equations against the note

Step by step, what each `math` and `note` restates, and the note's equation it belongs to.

| Step | Restates | Verdict |
|---|---|---|
| 1 | (1) and (2): yᵢ, kᵢ, ωᵢ, λᵢ, vᵢ; note: kᵢX − ωᵢt + φᵢ, "counts cycles per 200 px", hertz only at Speed 1×, ω/k = 200 sᵢ | same symbols, same meaning |
| 2 | §7: X_j = 800 j/M px, j = 0 … M | **M1** |
| 3 | §3 (3)–(4) superposition; §7 peak over the samples | same meaning |
| 4 | (20): the two ranges and the screen height; note: R is (19) rounded up, "step 08" = walkthrough step 8 | **M2** |
| 5 | (7) sum to product; (8) beat length; note: (9) v_env | (7) and (9) same; **M3** on (8) |
| 6 | (10) square-wave series; (11) amplitudes 30/n, f = 0.4 n, height H | (10) same; **M4** on (11) |
| 7 | (2) νᵢ = fᵢsᵢ; (17) stem height; §8 stem position 44 + (ν/6 Hz)(w − 58) = left + (ν/6 Hz)(right − left) | **M5**, **M6** |
| 8 | (19) triangle inequality | (19) same; **M7** in the note |

### Mismatches and their exact fixes

**M1 · step 2, bench.js:31 (`math`), meaning of M.** The walkthrough says "M = plot width in screen px". The note (§7, page 444)
says M is "the plot width in screen pixels minus 58", and calls the 770 px canvas the plot: measured at 1440 × 900, `box_w` = 770,
`M` = 712.
Fix: `M = plot width in screen px` → `M = plot width in screen px − 58`.

**M2 · step 4, bench.js:58 (`math`) and bench.js:66–67 (`syms`), symbols.** The walkthrough writes R<sub>sum</sub>, R<sub>comp</sub>,
p<sub>y</sub> and mid; equation (20) writes R, R<sub>c</sub>, y<sub>screen</sub> and y<sub>mid</sub>. Same meaning. The step's own
`note` already says R.
Fix, line 58:
`'⟦R|R<sub>sum</sub>⟧ = nice(Σ A<sub>i</sub>), &nbsp; R<sub>comp</sub> = nice(max A<sub>i</sub>)<br>nice(v) = max(20, 10⌈v/10⌉), &nbsp; p<sub>y</sub> = mid − (y / R) · h/2'`
→
`'⟦R|R⟧ = nice(Σ A<sub>i</sub>), &nbsp; R<sub>c</sub> = nice(max A<sub>i</sub>)<br>nice(v) = max(20, 10⌈v/10⌉), &nbsp; y<sub>screen</sub> = y<sub>mid</sub> − (y / R) · h/2'`
Lines 66–67: `['R', 'R<sub>sum</sub>', …` → `['R', 'R', …` and `['Rc', 'R<sub>comp</sub>', …` → `['Rc', 'R<sub>c</sub>', …`.

**M3 · step 5, bench.js:73 (`math`) and bench.js:77 (`syms`), a missing absolute value and the symbol.** The walkthrough writes
"beat length = 2π/Δk". Equation (8) writes λ<sub>beat</sub> = 2π/|Δk|. With Δk = k₁ − k₂ (the note's definition, page 249) the
Beats preset has Δk < 0: measured k₁ = 0.031416, k₂ = 0.039270 rad/px, so 2π/Δk = −800 px, while the store's `bl` is +800 px.
Fix, line 73: `⟦bl|beat length⟧ = 2π/Δk = 200/|f<sub>1</sub> − f<sub>2</sub>|` → `⟦bl|λ<sub>beat</sub>⟧ = 2π/|Δk| = 200/|f<sub>1</sub> − f<sub>2</sub>|`.
Line 77: `['bl', 'beat length', '200 / |f₁ − f₂|', 'for Waves 1 and 2, px'],` →
`['bl', 'λ<sub>beat</sub>', '200 / |f₁ − f₂|', 'beat length of Waves 1 and 2, px'],`.

**M4 · step 6, bench.js:84 (`math`), symbol and value.** The walkthrough writes "height ≈ (π/4) · 30 ≈ 23.6 px". Equation (11)
names the height H and gives it exactly: H = (π/4) × 30 px = 23.56 px.
Fix: `height ≈ (π/4) · 30 ≈ 23.6 px` → `H = (π/4) · 30 px = 23.56 px`.

**M5 · step 7, bench.js:95 (`math`), meaning of C.** The walkthrough's C is the complex phasor sum and the stem height is |C|. In
the note C is a length: C<sub>ν</sub> in (17) is the magnitude |Σ Aᵢ e^{iφᵢ}|, and in (5)–(6) C is the amplitude of the merged wave.
Fix: `C = Σ<sub>same ν</sub> A<sub>i</sub> e<sup>iφ<sub>i</sub></sup>, &nbsp; stem height ∝ |C|` →
`C<sub>ν</sub> = |Σ<sub>i: ν<sub>i</sub> = ν</sub> A<sub>i</sub> e<sup>iφ<sub>i</sub></sup>|, &nbsp; stem height ∝ C<sub>ν</sub>`.

**M6 · step 7, bench.js:96 (`note`), position symbol.** "At a fixed point x = 0". In the note the position is capital X (page 422:
"Stand at the left edge of the view, X = 0"); lowercase x is the square wave's variable x = 2π × 0.4 (X/200 − t) of §5.
Fix: `At a fixed point x = 0` → `At a fixed point X = 0`.

**M7 · step 8, bench.js:113 (`note`), "always the smaller one".** (19) is "≤", and the note says the peak reaches the ceiling
where all crests coincide. On the page the two readouts can be equal: measured with *One wave*, Sum of amplitudes "20.0 px",
Peak "20.0 px" (store 19.99704 px against 20 px).
Fix: `the sampled peak is always the smaller one.` → `the sampled peak is never the larger one.`

### Checked and consistent, no change needed

- Step 1: (1) and (2) symbol for symbol; φ is the note's φ (`\varphi`).
- Step 2 `note`: "four wavelengths" = the note's 4 fᵢ; "λ = 67 px" is the note's 66.7 px rounded. It says "world pixels" where the
  note says "px of the medium"; same thing (optional wording change, not counted).
- Step 3: "the sum is again a solution (see the derivation above)" is (3)–(4); the note is above the walkthrough on the page.
- Step 4 `note`: "R the sum of amplitudes rounded up to 10 px … a guaranteed bound" = page 455, "(19) rounded up to the next 10 px".
- Step 5 `note`: 200/0.25 = 800 px and the envelope speed 200(f₁s₁ − f₂s₂)/(f₁ − f₂) = (9); measured `venv` 200.0 px/s at Speed 1×.
- Step 6 `note`: odd harmonics, 1/n, 30/7 → 4.3, flat tops and Gibbs overshoot = §5.
- Step 7: νᵢ = fᵢsᵢ = (2); A sin(φ − 2πνt) = page 422; the stem position = §8 with left = 44, right − left = w − 58.
- Step 8 `math` = (19) term for term.

## `syms` keys against `Sim.live()`

The 24 keys used in `syms` are A, f, s, phi, k, w, lam, v, y1, M, dX, N, sum, pk, R, Rc, bl, venv, An, fn, hl, fmax, sA, ratio.
`Sim.live()` (page 797–821) returns exactly these 24 in every branch: `bl` and `venv` read "needs two waves with different f"
when undefined, and the per-wave keys read "no waves" with an empty bench. Measured in headless Chromium 1194 at 1440 × 900 on the
build `APPDEPLOY_VITE_OUT_DIR=/tmp/fig06-walk-dist npm run build`: 8 steps drawn, 25 "Now" cells, none showing "—", in three
states (default one wave, *Beats*, *Square wave*); 0 console errors. The mark `X` in step 2 has no table row, as walk.md says.

## How to re-run the code check

```js
// node check.cjs public/scripts/walk/bench.js public/simulations/wave-interference.html bench
const fs = require('fs'), vm = require('vm'), [walk, pg, key] = process.argv.slice(2), win = {};
vm.runInNewContext(fs.readFileSync(walk, 'utf8'), { window: win });
const page = fs.readFileSync(pg, 'utf8').split('\n'), strip = s => s.replace(/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g, '$1');
let checked = 0, found = 0;
win.WALK[key].steps.forEach((st, si) => strip(st.code).split('\n').forEach(ln => {
    if (!ln.trim() || ln.trim() === '...') return;
    checked++;
    const frags = ln.split('...').map(s => s.trim()).filter(Boolean);
    const hit = page.findIndex(p => { let pos = 0; return frags.every(f => { const k = p.indexOf(f, pos); if (k < 0) return false; pos = k + f.length; return true; }); });
    if (hit >= 0) found++; else console.log('NOT FOUND step ' + (si + 1) + ': ' + ln);
}));
console.log({ checked, found, notFound: checked - found });
```

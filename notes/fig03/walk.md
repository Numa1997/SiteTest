# Fig. 3 · walkthrough check (`slit`)

> Lead's note, 20 October 2026: these proposed fixes were written before some later edits of the note and were audited
> against the current notes afterwards (docs/research-theory-audit.md, "Open, for Numa"). Fixes that touch a `code` or
> `where` field need the same permission as the rest. Nothing here has been applied; the walkthrough file is unchanged.


Checked on 20 October 2026 by the walkthrough keeper, at commit `127a8d2`, on the working copy of branch
`claude/physics-notes-rewrite-cwctkk` (the page carries the teacher's uncommitted note changes; `slit.js` equals `127a8d2`).

- Page: `public/simulations/Interactive Double-Slit Experiment Visualization.html`, 948 lines, 173 421 bytes; lecture note at
  lines 129–536; `#walk[data-walk="slit"]` at line 538. The teacher's changes are all inside the note (lines 345, 350, 491, 522,
  529–531), so no quoted code line moved.
- Walkthrough: `public/scripts/walk/slit.js`, 118 lines, 8 134 bytes, 7 steps.
- `slit.js` was not changed: Numa has not allowed it. Every fix below is written out so it can be applied as it stands once he does.

## Counts

| What | Checked | Found / matching | Not found / mismatched |
|---|---|---|---|
| Non-empty code lines (marks stripped) | 28 | | |
| Lines that are only `...` | 4 | (not searched) | |
| Code lines searched in the page | 24 | **24** | **0** |
| of these, with an inline `...` | 1 (slit.js:110) | 1 (page line 759) | 0 |
| Keys in `syms` returned by `Sim.live()` | 21 | 21 | 0 |
| Equation numbers "(n)" cited in `math` or `note` | 0 | | |
| `math` fields | 7 | 6 | 1 (step 4) |
| `note` fields | 7 | 6 | 1 (step 4) |
| `syms` rows (symbol and meaning) | 23 | 22 | 1 (step 4, `phi`) |

The code is quoted exactly. There are two real mismatches, both in step 4: the phase difference is written φ where the note writes
Δφ, and the wave amplitude A where the note writes E₀. Four smaller points (wording, one `where`) follow; they are not wrong.

## 1. The code lines: 24 of 24 found verbatim

Method from `docs/scripts/walk.md`, "The rule": evaluate `slit.js` with a stub `window`, strip the marks with
`/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g → '$1'`, trim, drop lines that are only `...`, split each remaining line on `...`, and look for the
fragments in order on one page line. Then a stricter pass: each line equals a whole page line after trimming (for the inline
elision: starts with the first fragment and ends with the last), and lines quoted together without a `...` between them are
neighbours in the page.

| Step | `where` | Page lines quoted (`...` = lines left out) | Verdict |
|---|---|---|---|
| 1 Where everything sits | `compute() — lines 1–3` | 621 622 623 | found; whole lines; neighbours; `where` true |
| 2 Two paths and their exact difference | `compute() — L1, L2 and ds` | 624 ... 626 627 | found; whole lines; `where` true |
| 3 The burgundy bar: point Q | `compute() — ux, uy and Q` | 628 629 | found; whole lines; `where` true |
| 4 Phase difference and brightness | `storeDerived() and Iexact(th)` | 755 ... 716 717 | found; whole lines; `where` true |
| 5 Far field: the textbook curve | `drawPattern() — I(th), the solid burgundy curve` | 712 ... 756 ... 778 | found; whole lines; `where` names only the first of three functions (W4) |
| 6 Fringe orders on the pattern | `drawPattern() — the m = … labels` | 739 740 741 742 743 744 | found; whole lines; neighbours; `where` true |
| 7 The verdict line | `storeDerived() — the three-way test` | 757 758 759 760 | found; whole lines; neighbours; `where` true |

`return c * c;` (step 4) is also a fragment of line 712; the whole-line match is 717, inside `Iexact`, as `where` says. The closing
`}` of step 6 matches 21 page lines; the one that follows 743 is 744. Line 759 is the inline elision that `docs/scripts/walk.md`
names: the excerpt keeps `else if (Math.abs(f - 0.5) < 0.08) verdict = 'Destructive · dark fringe between m = ' + ` and `;`, and
leaves out `Math.floor(ratio) + ' and ' + (Math.floor(ratio) + 1)`. The page lines the doc cites (538 for `data-walk`, 759) still
hold. No line was not found, so there is no code fix.

## 2. `syms` keys against `Sim.live()`: 21 of 21 returned

Keys used: `d a b P L1 L2 ds dsid u Q S2Q lam m phi I ff Iff sinm t1 fr verdict`. `Sim.live()` (page lines 794–806) returns all
of them, plus `S1`, which is a mark in step 1 without a table row (as `docs/scripts/walk.md` says). Every value is read from the
store with `ds.get`.

Measured in headless Chromium (build in `/tmp/fig03-walk-dist`, page and `slit.js` byte-identical to `public/`; viewport
1440 × 900; 1.5 s after load, then each step clicked and read again after 450 ms): 7 steps drawn; on every step no "Now" cell is
`—` or empty; the rendered code of every step equals its `code` field with marks stripped; 0 console errors. Values at the
defaults, d = 200 px, α = 20°, b = 40 px, λ = 13.5 px:

| Key | Now | Note says |
|---|---|---|
| `L1`, `L2` | 206.851 px, 220.478 px | 206.85 px, 220.48 px (Section 3) |
| `ds`, `dsid`, `S2Q` | 13.6277 px each | δs = 13.6277 px (Section 3) |
| `ff` | 13.6808 px | b sin α = 13.6808 px (Section 4.1) |
| `sinm` | 0.3375 | λ/b; 2λ/b = 0.675 (Section 6) |
| `t1` | 19.72° | first bright fringe 19.72° (Figures 4, 5) |
| `phi` | 2.019 π | (readout "Phase Δφ" in units of π, Section 8) |
| `verdict` | Constructive · bright fringe, m = 1 | (Exercise 5.1: Constructive near 20°) |

## 3. The equations against the note

| Step | Walkthrough | Note | Verdict |
|---|---|---|---|
| 1 `math` | S₁ = (X₀ − b/2, Y₀), S₂ = (X₀ + b/2, Y₀); P = (X₀ − d tan α, Y₀ − d) | (1) S₁ = (−b/2, 0), S₂ = (b/2, 0), P = (−d tan α, d); Section 9: "P is drawn at (300 − d tan α, 370 − d): equation (1) flipped and shifted" | same symbols, same meaning (screen coordinates of (1)) |
| 1 `note` | barrier at y = Y₀ = 370, midpoint X₀ = 300, y down, "the screen, a distance d beyond the barrier", P on the ray at α to the normal | Section 2: wall, P at distance d at angle α to the normal; Section 9: same numbers; the line through P is the "observation line" | same meaning; wording W1 |
| 2 `math` | L₁ = \|P − S₁\|, L₂ = \|P − S₂\|; δs = L₂ − L₁ = (L₂² − L₁²)/(L₁ + L₂) = 2bd tan α/(L₁ + L₂) | Figure 1 L₁ = \|S₁P\|, L₂ = \|S₂P\|; (2); (3) term for term | same |
| 2 `note` | x = d tan α, L₂² − L₁² = (x + b/2)² − (x − b/2)² = 2bx; right-hand form avoids cancellation | Section 3: (d tan α + b/2)² − (d tan α − b/2)² = 2bd tan α; the page computes the right-hand side of (3) | same |
| 3 `math` | û = (S₂ − P)/L₂, Q = P + L₁û, \|S₂Q\| = L₂ − L₁ = δs | Section 8: Q = P + L₁û, û the unit vector from P towards S₂; Figure 1: \|PQ\| = L₁, S₂Q is δs | same |
| 3 `note` | Q on the circle about P through S₁; S₂Q the burgundy bar | Figure 1 caption | same |
| 4 `math` | **φ** = 2π δs/λ; I/I₀ = cos²(**φ**/2) = cos²(π δs/λ) | (6) **Δφ** = k δs = 2π δs/λ; (7) I ∝ 2E₀² cos²(Δφ/2), I/I₀ = cos²(π δs/λ) | **M1** |
| 4 `note` | equal waves shifted by **φ**, amplitude 2**A** cos(φ/2), peak (2**A**)² | (6), (7), Figure 3: amplitude E₀, sum 2E₀ cos(Δφ/2), I₀ where the waves arrive in step | **M1, M2** |
| 5 `math` | d ≫ b: δs ≈ b sin α; I<sub>far</sub>(θ) = cos²(π b sin θ/λ) | (4) δs ≈ b sin α, "b ≪ r" (Section 5); Section 8: burgundy curve cos²(π b sin θ/λ); θ defined in the Section 5 box | same meaning (W2) |
| 5 `note` | far away, paths nearly parallel, δs → b sin α; solid curve far field, dashed ink curve exact δs at the actual d | Section 4 and Section 8 | same; wording W1 ("screen") |
| 6 `math` | sin θ<sub>m</sub> = mλ/b, m = 0, 1, 2, … while sin θ<sub>m</sub> ≤ sin 30° | Section 5 box: sin θ<sub>m</sub> = mλ/b; (8) δs = mλ bright; plot 0° to 30° (Sections 8, 9) | same |
| 6 `note` | δs = mλ in the far-field form gives the bright directions | (8) with (4) | same |
| 7 `math` | f = δs/λ − ⌊δs/λ⌋; bright if f < 0.08 or f > 0.92; dark if \|f − ½\| < 0.08; otherwise partial | Section 8, the same three tests | same |
| 7 `note` | tolerance 0.08 → cos²(0.08π) ≈ 0.94 at the edge of bright, ≈ 0.06 at the edge of dark | Section 8: Constructive covers 0.94 to 1, Destructive 0 to 0.06 | same numbers (0.9382, 0.0618); wording W3 |

No `math` or `note` field cites an equation number, so no "(n)" can point to the wrong equation. The equation numbers (1) to (13) of
the note are in order and were not changed by the teacher. The optional W1 fix below adds one citation, "(1)", checked: (1) is
the placement of S₁, S₂ and P, and Section 9 calls the drawn position "equation (1) flipped and shifted".

## 4. Every mismatch and its exact fix

Old text is copied from `slit.js` as it stands; new text replaces it whole. Marks keep their keys, so the lighting and the table
still work. No fix touches a `code` field or a key.

**M1 · step 4, phase difference: φ in the walkthrough, Δφ in the note. slit.js:57, 58, 66.** The note writes the phase
difference Δφ (`\Delta\varphi`, 16 times: (6), (7), Section 5, Figure 3, Section 7), and keeps a bare ϕ (`\phi`) for something
else: the animation phase of the wavelets, r<sub>n</sub> = (n + ϕ)λ, in Section 9. The page itself agrees with the note: the
readout is labelled "Phase Δφ" (page line 116) and the store names the variable Δφ (page lines 581, 582, 587). Only the
walkthrough writes φ.

Old (slit.js:57):
```
math: '⟦phi|φ⟧ = 2π δs / ⟦lam|λ⟧<br>⟦I|I/I<sub>0</sub>⟧ = cos²(φ/2) = cos²(π δs / λ)',
```
New:
```
math: '⟦phi|Δφ⟧ = 2π δs / ⟦lam|λ⟧<br>⟦I|I/I<sub>0</sub>⟧ = cos²(Δφ/2) = cos²(π δs / λ)',
```

Old (slit.js:66):
```
['phi', 'φ', 'phi', 'phase difference'],
```
New:
```
['phi', 'Δφ', 'phi', 'phase difference'],
```

**M2 · step 4 `note`, amplitude: A in the walkthrough, E₀ in the note. slit.js:58.** The note calls the amplitude of each wave
E₀ and the summed amplitude 2E₀ cos(Δφ/2) ((6), Figure 3). The walkthrough uses an undefined A. The same line carries the φ of M1.

Old (slit.js:58):
```
note: 'Two equal waves shifted by φ add to an amplitude 2A cos(φ/2); intensity goes as amplitude squared, and dividing by the peak (2A)² gives cos²(φ/2). The dot on the lower curve sits at this value.',
```
New:
```
note: 'Two equal waves of amplitude E₀ shifted by Δφ add to an amplitude 2E₀ cos(Δφ/2); intensity goes as amplitude squared, and dividing by the peak (2E₀)² gives cos²(Δφ/2). The dot on the lower curve sits at this value.',
```

## 5. Smaller points: same meaning, optional

**W1 · "barrier" and "screen" where the note says "wall" and "observation line". slit.js:14, 19, 22, 74.** The note calls the
slitted plate the wall throughout, and the line through P the observation line (Sections 8 and 9; the drawing labels it so). It
keeps "screen" for the flat screen at a large distance D in (9) and Section 7, which is not the line at distance d. The symbol d
means the same in both. Fix, if wanted:

Old (slit.js:14):
```
note: 'The barrier is the horizontal line y = Y₀ = 370 in the drawing’s coordinates, with the slit midpoint at X₀ = 300. SVG’s y axis points down, so the screen, a distance d beyond the barrier, sits at Y₀ − d. P lies on the ray from the midpoint at angle α to the normal.',
```
New:
```
note: 'The wall is the horizontal line y = Y₀ = 370 in the drawing’s coordinates, with the slit midpoint at X₀ = 300. SVG’s y axis points down, so the observation line, a distance d beyond the wall, sits at Y₀ − d. P lies on the ray from the midpoint at angle α to the normal: equation (1) of the note, flipped and shifted.',
```

Old (slit.js:19): `['d', 'd', 'dS.value', 'barrier → screen, px'],`
New: `['d', 'd', 'dS.value', 'wall → observation line, px'],`

Old (slit.js:22): `['P', 'P', 'P', 'point on the screen, SVG px']`
New: `['P', 'P', 'P', 'point on the observation line, SVG px']`

Old (slit.js:74):
```
note: 'When the screen is far away the two paths are nearly parallel and δs → b sin α. The solid curve uses this; the dashed ink curve uses the exact δs at the actual d. Shrink d and watch the two peel apart at large angles.',
```
New:
```
note: 'When P is far from the slits the two paths are nearly parallel and δs → b sin α. The solid curve uses this; the dashed ink curve uses the exact δs at the actual d. Shrink d and watch the two peel apart at large angles.',
```

**W2 · step 5 `math`, slit.js:73: "d ≫ b" against the note's "b ≪ r".** r = d/cos α, and α ≤ 30° on the page, so
d ≤ r ≤ 1.155 d: here the two conditions are the same. No fix needed.

**W3 · step 7 `note`, slit.js:107.** "cos²(0.08π) ≈ 0.94 at the edge of “bright” and ≈ 0.06 at the edge of “dark”" reads as if
cos²(0.08π) were also 0.06. The 0.06 is cos²(0.42π) = sin²(0.08π) = 0.0618. The numbers agree with Section 8. Fix, if wanted:
in slit.js:107 replace `and ≈ 0.06 at the edge of “dark”` by `and sin²(0.08π) ≈ 0.06 at the edge of “dark”`.

**W4 · step 5 `where`, slit.js:72.** The step quotes three functions, `drawPattern()` (page line 712), `storeDerived()` (756) and
`readouts()` (778); `where` names only the first. `docs/scripts/walk.md` asks that `where` name the function and place. Fix, if
wanted:

Old: `where: 'drawPattern() — I(th), the solid burgundy curve',`
New: `where: 'drawPattern() — I(th), the solid burgundy curve; storeDerived() — ff; readouts() — r-ff',`

**Aside, about the note, not the walkthrough.** Section 2 puts P at x = −d tan α (origin at M, P on the side of S₁), while
Section 8 says the point in the direction θ is "at x = d tan θ", the opposite sign. The code (page line 715) uses x = d tan θ as a
distance from the centre line, and the walkthrough's step 2 note defines its own x = d tan α, so the walkthrough is consistent with
Section 8 and the code. For the teacher or the referee to judge.

## 6. The check, to run again

```js
// node check.cjs   (run from /home/user/SiteTest)
const fs = require('fs'), vm = require('vm');
const window = {}; vm.runInNewContext(fs.readFileSync('public/scripts/walk/slit.js', 'utf8'), { window });
const page = fs.readFileSync('public/simulations/Interactive Double-Slit Experiment Visualization.html', 'utf8').split('\n');
const strip = s => s.replace(/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g, '$1');
let checked = 0, found = 0;
window.WALK.slit.steps.forEach((st, si) => st.code.split('\n').forEach(raw => {
  const line = strip(raw).trim(); if (!line || line === '...') return;
  checked++;
  const frags = line.split('...').map(f => f.trim()).filter(Boolean);
  const hit = page.findIndex(pl => { let p = 0; return frags.every(f => { const k = pl.indexOf(f, p); if (k < 0) return false; p = k + f.length; return true; }); });
  if (hit >= 0) found++; else console.log('NOT FOUND, step', si + 1, ':', line);
}));
// keys in syms against Sim.live(), read from the page source
const src = page.join('\n'), live = src.slice(src.indexOf('Sim.live = function'), src.indexOf('var clk = Sim.clock'));
const keys = [...live.slice(live.indexOf('return {')).matchAll(/([A-Za-z0-9_]+)\s*:/g)].map(m => m[1]);
const used = [...new Set(window.WALK.slit.steps.flatMap(s => s.syms.map(r => r[0])))];
console.log({ checked, found, notFound: checked - found, keysUsed: used.length, missing: used.filter(k => !keys.includes(k)) });
// { checked: 24, found: 24, notFound: 0, keysUsed: 21, missing: [] }
```

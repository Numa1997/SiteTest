# Fig. 5 · walkthrough `water` against water-wave.html · check

> Lead's note, 20 October 2026: these proposed fixes were written before some later edits of the note and were audited
> against the current notes afterwards (docs/research-theory-audit.md, "Open, for Numa"). Fixes that touch a `code` or
> `where` field need the same permission as the rest. Nothing here has been applied; the walkthrough file is unchanged.


Checked on 20 October 2026 by the walkthrough keeper. Read-only: `public/scripts/walk/water.js` is not changed (Numa has not
allowed it). The fixes below are written out exactly, for the lead to apply if that permission comes.

| | |
|---|---|
| Page | `public/simulations/water-wave.html`, 891 lines, sha256 `7e61d6f5…7390`, identical to HEAD `c29e570` (the commit with the new note) |
| Walkthrough | `public/scripts/walk/water.js`, 116 lines, sha256 `2ef2e92f…14a4`, unchanged since `43d8238` |
| Note | page lines 107–553, `<article class="paper" id="paper">` to `</article>`; display equations (1)–(23) are byte-identical before and after `c29e570` |
| Method | `docs/scripts/walk.md`, "Elisions in the code" and "The rule: excerpts stay identical to the page code" |

## Result in one line

All 21 code lines are found verbatim. Every `syms` key is returned by `Sim.live()`. The walkthrough cites no equation numbers.
Five things need fixing: one symbol clash with equation (23), three symbols the note does not use, and one comment line left
out without `...`. Plus one wrong `where`.

## 1. Code excerpts against the page (by script)

The script evaluates `water.js` with a stub `window`, strips the marks with `/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g → '$1'`, splits each
line on `...` and looks for the fragments, in order, on one page line. It also checks that lines quoted together without `...`
are adjacent on the page, and that every `syms` key is returned by `Sim.live()`.

| | count |
|---|---|
| steps | 7 |
| non-empty code lines | 26 |
| lines that are only `...` | 5 |
| **code lines checked** | **21** |
| **found verbatim** | **21** (all 21 match a whole page line once indentation is trimmed) |
| **not found** | **0** |
| lines with an inline `...` | 0 |

Where each line was found:

| Step | `where` | page lines |
|---|---|---|
| 1 | k() and f() | 635, *636 left out*, 637, 638, 639 |
| 2 | readouts() | 653, 654, `...`, 656 |
| 3 | draw() — the parcel loop | 740, 741, 742 |
| 4 | draw() — the layer loop and readouts() | 735, `...`, 658 |
| 5 | draw() — the surface path | 691, 692, 693, `...`, 695 |
| 6 | a() | 640, `...`, 657 |
| 7 | Sim.clock and draw() — line 1 | 792, `...`, 680, 681 |

Adjacency:

- **Step 1, one unmarked gap.** Page line 636, `/* exact deep-water frequency; the slider only displays it in 0.01 Hz steps */`,
  sits between the quoted lines 635 and 637, and the excerpt leaves it out without a `...`. Under "Elisions in the code" a
  left-out line needs a `...` line. Fix F1.
- **Steps 4 and 7 jump backwards across `...`** (735 → 658 and 792 → 680). Each step quotes two functions, and `where` names
  both in the order quoted. I accept this; no fix.

## 2. `syms` keys against `Sim.live()`

By reading the code (page lines 778–790), `Sim.live()` returns 22 keys: `lam k km f c T cg X0 th px pz r r1 z0 deep eta a A ak wt s ys`.
The walkthrough has 23 `syms` rows using 22 distinct keys (`a` appears in steps 5 and 6). All 22 are returned, and none is left
unused. All 32 marks in `math` and `code` have a row in their own step. No `note` field carries a mark.

The same check in headless Chromium, on a build at `/tmp/fig05-walk-dist` (identical to the tree): `window.WALK.water` loaded
and 7 step tabs drew. Clicking through every step filled all 23 "Now" cells; none showed `—`. That held at 1440 × 900 and at
390 × 844, with 0 console errors and 0 px sideways scroll. The Now values agree with the note's own numbers:

| key | Now, 1440 × 900 | note |
|---|---|---|
| `f`, `km` | 0.7749 Hz, 2.4166 rad/m | 0.775 Hz, 2.42 rad/m (5.2, 02) |
| `c`, `T`, `cg` | 2.0148 m/s, 1.2905 s, 1.0074 m/s | 2.01, 1.29, 1.01 (table, 5.3) |
| `r`, `r1`, `deep` | 24.00 px, 6.20 px, 0.45 % | 24, 6.2 px; 0.45 % (6.1) |
| `ak` | 0.5800 | 0.58 (02, 6.2) |
| `X0` | 378.2 px (190.0 px at 390 wide) | 378.2 px or 190 px (09) |

## 3. Equations in `math` and `note` against the note

The walkthrough cites no equation number, so there is no "(n)" to check (`grep '([0-9]+)'` in `water.js` finds only
`.toFixed(2)`). Every equation was compared by symbol and meaning:

| Step | Walkthrough equation | Note | Verdict |
|---|---|---|---|
| 1 | k = 2π/λ (rad/px), k<sub>m</sub> = 100 · k (rad/m) | §08 line 510; (22) | same |
| 1 | ω² = g k<sub>m</sub> ⇒ f = √(g k<sub>m</sub>)/2π | (13), (22) | same |
| 1 note | f exact from λ, slider rounded to 0.01 Hz; switch off: not a water wave | §08 line 510; §5.3 line 364 | same |
| 2 | c = fλ = ω/k = √(g/k<sub>m</sub>), T = 1/f | (14); ω = 2πf, k = 2π/λ (§02) | same (fλ = ω/k by the §02 definitions) |
| 2 | c<sub>g</sub> = dω/dk = c/2 | (15) | same |
| 3 | θ = kX<sub>0</sub> − ωt; x = X<sub>0</sub> − r sin θ, z = z<sub>0</sub> + r cos θ | (17), (18); §08 line 513 uses X<sub>0</sub> | same (the note writes x<sub>0</sub> in §06 and X<sub>0</sub> for the page's px in §08; the walkthrough follows §08) |
| 3 note | top of circle at θ = 0, forward at rω, clockwise; screen y down | §06 line 379; (23) and line 523 | same |
| 4 | z<sub>0</sub> = −56 j px; r = a e<sup>k z<sub>0</sub></sup> | §08 lines 512–513; (18) | same |
| 4 note | φ ∝ e<sup>kz</sup>; e<sup>−2π</sup> ≈ 0.19 % one wavelength down | (12); §6.1 line 382 | same |
| 5 | x = X − a sin(kX − ωt), η = a cos(kX − ωt), X ∈ [−60, WORLD_W + 60] | (19): x = x<sub>0</sub> − a sin θ, η = a cos θ; §09 lines 521, 525: W<sub>field</sub> | **symbols differ: X and WORLD_W** (M2) |
| 5 note | trochoid, sharper crests, sine as ak → 0; ends 60 px outside | §6.2 line 442; §09 line 525 | same |
| 6 | a = min(A<sub>slider</sub>, 0.9/k) ⇒ ak ≤ 0.9 | §08 line 516: a = min(A, 0.9/k); §6.2 line 443 | same meaning; see "Accepted" for A<sub>slider</sub> |
| 6 note | dx/dX = 1 − ak cos θ; cusp at ak = 1; break at ak ≈ 0.44 | §6.2 line 443: dx/dx<sub>0</sub>; §10 line 539 | **symbol differs: dX** (M3) |
| 7 | ωt ← ωt + 2π f Δt | (22) | same |
| 7 | s = W<sub>screen</sub> / W, with W = 800 px (400 px on a phone) | (23): s = W/W<sub>field</sub>; W is the canvas width on screen (line 521) | **mismatch: W means the opposite thing** (M1) |
| 7 | y<sub>s</sub> = max(a s + 34, 0.28 H) | (23) | same |
| 7 note | exact f(); crest clears the top by 34 px | §08 line 510; §09 line 523 | same |

## 4. Mismatches and exact fixes

| # | Where | What is wrong | Fix |
|---|---|---|---|
| M1 | step 7 `math` (water.js:103) | The walkthrough uses **W** for the field width (800 px) and W<sub>screen</sub> for the canvas. The note's (23) uses **W** for the canvas width on screen and W<sub>field</sub> for the field. Same letter, opposite meaning. "On a phone" is also looser than the note's rule, "narrower than 560 screen pixels". | F4 |
| M2 | step 5 `math` (water.js:74) | `X` and `WORLD_W` appear nowhere in the note. The note writes the rest position as x<sub>0</sub> in (19) and X<sub>0</sub> in §08 (which step 3 already uses), and the field width as W<sub>field</sub>. | F2 |
| M3 | step 6 `note` (water.js:90) | `dx/dX`; the note (line 443) writes dx/dx<sub>0</sub>, the same derivative. | F3 (X<sub>0</sub>, to match F2 and step 3) |
| M4 | step 1 `code` (water.js:15–16) | Page line 636 (a comment) is left out without a `...`. | F1 |
| M5 | step 7 `where` (water.js:102) | "draw() — line 1", but the quoted lines are lines 680–681, the second and third lines of draw(). Line 1 is 679, `WORLD_W = box.w < 560 ? 400 : 800;`, which is the 800/400 rule the step's formula states. | F5 |
| M6 (minor) | step 7 `syms`, row `s` (water.js:111) | "screen px per world px"; the note (§09 line 523) and the store's `s_px` say "field pixel". | F6 |

The proposed patch. It was applied to a scratch copy only, never to the repository file:

```diff
--- public/scripts/walk/water.js
+++ public/scripts/walk/water.js (proposed)
@@ -13,6 +13,7 @@
             math: '⟦k|k⟧ = 2π/λ &nbsp;(rad/px), &nbsp; ⟦km|k<sub>m</sub>⟧ = 100 · k &nbsp;(rad/m)<br>ω² = g k<sub>m</sub> &nbsp;⇒&nbsp; ⟦f|f⟧ = √(g k<sub>m</sub>) / 2π',
             note: 'The drawing uses 100 px = 1 m, so a wave number per pixel is 100 times larger per metre. With “deep-water dispersion” on, f is computed exactly from λ; the slider only shows it rounded to 0.01 Hz. With it off, f is whatever you set, and the wave is no longer a real water wave.',
             code: `function ⟦k|k()⟧ { return 2 * Math.PI / lambda.value; }
+/* exact deep-water frequency; the slider only displays it in 0.01 Hz steps */
 function ⟦f|f()⟧ {
     return dispBox.checked ? Math.sqrt(G * ⟦km|k() * PX_PER_M⟧) / (2 * Math.PI) : freq.value;
 }`,
@@ -71,7 +72,7 @@
         {
             title: 'The surface is the top layer of parcels',
             where: 'draw() — the surface path',
-            math: 'x = X − a sin(kX − ωt), &nbsp; ⟦eta|η⟧ = a cos(kX − ωt), &nbsp; X ∈ [−60, WORLD_W + 60] (WORLD_W = 800, or 400 on a canvas narrower than 560 px)',
+            math: 'x = X<sub>0</sub> − a sin(kX<sub>0</sub> − ωt), &nbsp; ⟦eta|η⟧ = a cos(kX<sub>0</sub> − ωt), &nbsp; X<sub>0</sub> ∈ [−60, W<sub>field</sub> + 60] (W<sub>field</sub> = 800 px, or 400 px on a canvas narrower than 560 px)',
             note: 'Tracing every surface parcel at once gives a trochoid: sharper crests, flatter troughs than a sine, and it becomes a sine when ak → 0. Starting 60 px outside the frame hides the ends of the curve.',
             code: `for (X = -60; X <= WORLD_W + 60; X += 3) {
     th = kk * X - omegaT;
@@ -87,7 +88,7 @@
             title: 'Steepness limit',
             where: 'a()',
             math: '⟦a|a⟧ = min(A<sub>slider</sub>, 0.9/k) &nbsp;⇒&nbsp; ⟦ak|ak⟧ ≤ 0.9',
-            note: 'dx/dX = 1 − ak cos θ on the surface. At ak = 1 the crest (θ = 0) folds into a cusp and beyond it the curve loops through itself. Real waves break well before that, at ak ≈ 0.44 (Stokes limit), so shapes above that steepness are already an idealisation.',
+            note: 'dx/dX<sub>0</sub> = 1 − ak cos θ on the surface. At ak = 1 the crest (θ = 0) folds into a cusp and beyond it the curve loops through itself. Real waves break well before that, at ak ≈ 0.44 (Stokes limit), so shapes above that steepness are already an idealisation.',
             code: `function ⟦a|a()⟧ { return Math.min(amp.value, 0.9 / k()); }
 ...
 document.getElementById('r-ak').textContent = (⟦ak|a() * k()⟧).toFixed(2) + (a() < amp.value ? ' (cap)' : '');`,
@@ -99,16 +100,17 @@
         },
         {
             title: 'The clock and the picture',
-            where: 'Sim.clock and draw() — line 1',
-            math: '⟦wt|ωt⟧ ← ωt + 2π f Δt<br>⟦s|s⟧ = W<sub>screen</sub> / W, with W = 800 px (400 px on a phone), &nbsp; ⟦ys|y<sub>s</sub>⟧ = max(a s + 34, 0.28 H)',
+            where: 'Sim.clock and draw() — its first three lines',
+            math: '⟦wt|ωt⟧ ← ωt + 2π f Δt<br>⟦s|s⟧ = W / W<sub>field</sub>, with W the canvas width on screen and W<sub>field</sub> = 800 px (400 px on a canvas narrower than 560 px), &nbsp; ⟦ys|y<sub>s</sub>⟧ = max(a s + 34, 0.28 H)',
             note: 'ωt uses the exact f(), not the rounded slider value, so c and the motion stay consistent to machine precision. The rest level y<sub>s</sub> sits low enough that the tallest crest still clears the top by 34 px.',
             code: `⟦wt|omegaT += 2 * Math.PI * f() * dt⟧;
 ...
+WORLD_W = box.w < 560 ? 400 : 800;
 var w = box.w, h = box.h, ⟦s|s = w / WORLD_W⟧, kk = k(), A = a();
 var ⟦ys|ys = Math.max(A * s + 34, h * 0.28)⟧, X, th;`,
             syms: [
                 ['wt', 'ωt', 'omegaT', 'rad'],
-                ['s', 's', 's', 'screen px per world px'],
+                ['s', 's', 's', 'screen px per field px'],
                 ['ys', 'y<sub>s</sub>', 'ys', 'rest level, px from top']
             ]
         }
```

**Tested on the scratch copy:**

- **Script:** 23 code lines checked, 23 found, 0 not found. No unmarked gap is left (step 1 is now 635–639 without a break). All 22 keys are still returned.
- **Headless Chromium:** a copy of the build with the patched file loaded at 1440 × 900 and 390 × 844. It drew 7 tabs, filled all 23 cells with no `—`, and showed 0 console errors, 0 px sideways scroll and no raw `⟦`. The `<sub>` subscripts render.
- **Screenshots** of steps 1, 5, 6 and 7, before and after, are session-only files, not in the repository:
  `/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/fig05/shots/current-step7.png` and
  `/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/fig05/shots/fixed-step7.png` (likewise `-step1`, `-step5`, `-step6`).

**Docs to update in the same change if the patch is applied:**

- **Line count:** water.js grows from 116 to 118 lines and 7 517 to 7 802 bytes. That touches `docs/simulations/fig05-water-wave.md:6` ("116 lines") and `:290` (`water.js:7-116`), the table row and totals in `docs/scripts/walk.md:5,156`, and `docs/files.md:82`.
- **Step-title links:** in `docs/scripts/walk.md:156`, steps 2–7 move down one line: L27→L28, L42→L43, L57→L58, L72→L73, L87→L88, L101→L102.
- **Quoted-line list:** `docs/simulations/fig05-water-wave.md:327` would gain 636 and 679. It already misses 695, the closing `}` of step 5.
- **Counts:** "226 lines of code" in `docs/scripts/walk.md:113-120` becomes 228, and "267 non-empty code lines" becomes 269.

## 5. Accepted differences (no fix)

- **A<sub>slider</sub> (step 6) against the note's A (§08 line 516).** The meaning is the same. Writing plain A would clash with the
  code shown beside it, where `A = a()` is the capped amplitude (page line 680, quoted in step 7). The note itself also uses A
  for the constant in (11). A<sub>slider</sub> is the clearer choice.
- **Row symbols x − X<sub>0</sub>, z − z<sub>0</sub> (step 3).** The note calls these ξ and ζ (§07, §08). They mean the same, and they sit in the
  `syms` symbol column, outside `math` and `note`.
- **One key, three quantities.** Two marks in the walkthrough light rows that show a related but different quantity. In step 3, `⟦px|x⟧`
  (math) and `⟦px|px = …⟧` (code, screen pixels) light the row "x − X<sub>0</sub>", whose Now value is ξ. In step 4, `⟦z0|z<sub>0</sub>⟧` lights the row
  z<sub>deep</sub>. Each row says plainly what it shows, so I leave them.
- **Stored c<sub>g</sub>.** It is c/2 also with dispersion off (page line 663). The note (line 364) says c/2 no longer applies then; the
  walkthrough's "in deep water" covers it. Page code is out of bounds.

## How to re-run

The scripts live in the session scratchpad; the main one is short enough to keep here.
`node walkcheck.cjs public/scripts/walk/water.js public/simulations/water-wave.html water` prints the gaps, then
`code lines checked 21, found 21, not found 0; elision-only lines 5; Sim.live() keys 22`.

```js
// node walkcheck.cjs <walk.js> <page.html> <key>: every excerpt line found verbatim, lines quoted together adjacent, syms keys in Sim.live().
const fs = require('fs'), vm = require('vm'), [walk, pagePath, key] = process.argv.slice(2);
const sb = { window: {} }; vm.createContext(sb); vm.runInContext(fs.readFileSync(walk, 'utf8'), sb);
const src = fs.readFileSync(pagePath, 'utf8'), page = src.split('\n'), strip = s => s.replace(/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g, '$1');
const live = src.slice(src.indexOf('Sim.live = function')); const keys = [...live.slice(live.indexOf('return {'), live.indexOf('};')).matchAll(/(?:[{,\s])([A-Za-z0-9_]+):\s/g)].map(m => m[1]);
let n = 0, found = 0, ell = 0;
sb.window.WALK[key].steps.forEach((st, si) => {
  let prev = null, gap = false;
  strip(st.code).split('\n').map(l => l.trim()).filter(Boolean).forEach(line => {
    if (line === '...') { ell++; gap = true; return; }
    n++; const fr = line.split('...').map(f => f.trim()).filter(Boolean);
    const hits = page.map((pl, i) => { let p = 0; for (const f of fr) { const a = pl.indexOf(f, p); if (a < 0) return 0; p = a + f.length; } return i + 1; }).filter(Boolean);
    if (!hits.length) { console.log(`step ${si + 1} NOT FOUND: ${line}`); return; }
    found++; const at = prev === null ? hits[0] : (hits.find(h => h > prev) || hits[0]);
    if (prev !== null && !gap && at !== prev + 1) console.log(`step ${si + 1}: page lines ${prev + 1}-${at - 1} left out without "..."`);
    if (prev !== null && gap && at < prev) console.log(`step ${si + 1}: "..." jumps back from page line ${prev} to ${at}`);
    prev = at; gap = false;
  });
  st.syms.forEach(r => { if (!keys.includes(r[0])) console.log(`step ${si + 1}: syms key ${r[0]} not returned by Sim.live()`); });
});
console.log(`code lines checked ${n}, found ${found}, not found ${n - found}; elision-only lines ${ell}; Sim.live() keys ${keys.length}`);
```

The browser check uses `render.cjs` in the same scratchpad folder
(`/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/fig05/`). To run it: build with
`APPDEPLOY_VITE_OUT_DIR=/tmp/fig05-walk-dist npm run build`, then load Playwright from `npm root -g` with
`executablePath /opt/pw-browsers/chromium-1194/chrome-linux/chrome`.

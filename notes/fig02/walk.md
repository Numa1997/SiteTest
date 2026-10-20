# Fig. 2 · walkthrough check (`pendulum`)

Checked on 20 October 2026 by the walkthrough keeper, on branch `claude/physics-notes-rewrite-cwctkk`. I started on the
teacher's edited note (11 lines: L141, L219, L335, L337, L350–351, L358–359, L372–374), which the lead then committed in
`a01cf85`. During the check the lead committed `468c139`. On the page it only splits the displayed equations (5), (8), (9) and
(13) over more lines, with the same symbols and the same content, so no finding below changes. The final pass is against HEAD
`468c139`, and the page and `pendulum.js` equal HEAD.

- Page: `public/simulations/Double Pendulum.html`, 870 lines. The lecture note is at lines 114–379, `#walk[data-walk="pendulum"]`
  at line 381, `Sim.live()` at lines 684–696.
- Walkthrough: `public/scripts/walk/pendulum.js`, 137 lines, 8 steps.
- I did not change `pendulum.js`: Numa has not allowed it. Every fix below is written out so it can be pasted in as it stands
  once he does.

## Counts

| What | Checked | Found / matching | Not found / mismatched |
|---|---|---|---|
| Code lines (marks stripped, `...` lines left out) | 31 | 31 found verbatim, 31 whole page lines | 0 |
| Lines that are only `...` | 3 | (not searched) | |
| Lines with an inline `...` | 0 | | |
| Lines quoted together that are page neighbours | 20 joins | 19 | 1 (step 6: page 701 → 703, no `...`) |
| Code column in the browser equal to the stripped source | 8 steps | 8 | 0 |
| Keys in `syms` returned by `Sim.live()` | 22 keys (28 rows) | 22 | 0 |
| Equation numbers "(n)" cited | 3: (6), (7), (8) | 3 point at the same equations | 0 |
| `math` fields | 8 | 4 | 4 (steps 1, 4, 5, 8: symbols) |
| `note` fields | 8 | 5 | 3 (step 2 symbol; step 3 stale; step 8 contradicted) |
| Marks inside `note` | 0 | | |

In total there are 8 mismatches: 1 silent elision, 5 symbol mismatches (one of them the same symbol used with a different
meaning), 1 stale pointer and 1 claim the edited note contradicts. None of the walkthrough's notes mentions the energy drift
over time or the Lyapunov rate, so the new figures in the note (the creep of about 7 × 10⁻⁸ a minute, −3.6 × 10⁻⁴ at mass
ratio 10, the fitted 1.4 per second and the full 1.45 per second) contradict nothing in the walkthrough.

## 1. The code lines: 31 of 31 found verbatim

The method comes from `docs/scripts/walk.md`, "The rule". I evaluated `pendulum.js` in Node with a stub `window`, stripped the
marks with `/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g → '$1'`, dropped lines that are only `...`, split each remaining line on `...`, and
looked for the fragments in order on one page line. A stricter second pass checked two more things: that each line equals a
whole page line after trimming, and that lines quoted with no `...` between them are neighbours in the page.

| Step | `where` | Page lines quoted (`...` = lines left out) | Verdict |
|---|---|---|---|
| 1 The state vector | restart() — the initial condition | 533 | found, whole line |
| 2 Angle difference and the shared denominator | deriv(s) — lines 1–2 | 480 481 | found, whole lines, neighbours |
| 3 Upper angular acceleration α₁ | deriv(s) — the a1 line | 482 483 | found, whole lines, neighbours |
| 4 Lower angular acceleration α₂ | deriv(s) — the a2 line and the return | 484 485 486 | found, whole lines, neighbours |
| 5 One Runge–Kutta 4 step | rk4(s, h) | 489–496 | found, whole lines, neighbours |
| 6 How many steps per frame | Sim.clock callback | 700 701 703 704 705 ... 715 716 | found, whole lines; **701 → 703 skips 702 with no `...`** |
| 7 Energy as the accuracy check | energy(s) and diagnostics() | 500–503 ... 660 | found, whole lines |
| 8 From angles to pixels | layout() and pos(s) | 513 ... 506 507 | found, whole lines; jumps back across `...` (accepted, see 5) |

**Mismatch 1 (silent elision).** Step 6, pendulum.js:88–89. The excerpt goes from page line 701 (`var n = …`) straight to line
703 (`acc = Math.min(…)`), leaving out line 702, `lastN = n;`, with no `...`. Both lines date from the same commits
(`9a84de4`, `d22242c`, `2226030`), so the gap is older than the note edit.

Fix: insert a line that is only `...` between pendulum.js:88 and :89.

old
```
var ⟦n|n = Math.min(Math.floor(acc / H), 600)⟧;
acc = Math.min(acc - n * H, H);
```
new
```
var ⟦n|n = Math.min(Math.floor(acc / H), 600)⟧;
...
acc = Math.min(acc - n * H, H);
```

## 2. `syms` keys: 22 of 22 returned by `Sim.live()`

I read this from the code (lines 684–696) and then measured it. I built the site with
`APPDEPLOY_VITE_OUT_DIR=/tmp/fig02-walk-dist npm run build` from the `a01cf85` content, and the built page and `pendulum.js` are
byte-identical to those sources. `468c139` changes no code line and no `Sim.live()` line. I served the build on 127.0.0.1:8712 and opened it in headless Chromium 1194 at 1440 × 900. After 1.5 s,
`Sim.live()` returned exactly the 22 keys used in `syms`, no more and no fewer:
`t1 t2 o1 o2 d den m2 l2 a1 a2 k1 h n acc t kin pot E E0 drift scale y1`. All 8 steps drew, the section became a fold, and all
28 "Now" cells filled (none showed `—`). Every step's code column equals the stripped source, no raw `⟦` shows, and the
console had no errors.

## 3. Cited equation numbers: (6), (7), (8) all correct

The walkthrough cites equation numbers once, in step 3's `note` (pendulum.js:40): "Cramer’s rule on equations (6)–(7),
written as the system (8)".

| Cited | In the note | Verdict |
|---|---|---|
| (6) | L212: (m₁+m₂)l₁α₁ + m₂l₂α₂ cos δ = −m₂l₂ω₂² sin δ − (m₁+m₂)g sin θ₁, the upper-angle equation | same equation |
| (7) | L215: l₁α₁ cos δ + l₂α₂ = l₁ω₁² sin δ − g sin θ₂, the lower-angle equation | same equation |
| (8) | L218: the 2 × 2 system for (α₁, α₂), det = l₁l₂(m₁ + m₂ sin²δ) > 0 | same equation |

The teacher left the numbering alone: (1) positions, (2) velocities, (3) T, (4) V, (5) Euler–Lagrange, (6)–(7), (8) system,
(9) accelerations, (10)–(11) normal modes, (12) Lyapunov exponent, (13) RK4. The walkthrough never cites (3), (4), (9) or (13),
although steps 3, 4, 5 and 7 show exactly those equations. The fix for mismatch 7 adds (9); the other citations are optional
(section 5).

## 4. Equations and claims against the note

### `math`

| Step | `math` | Lecture note | Verdict |
|---|---|---|---|
| 1 | **<b>s</b>** = (θ₁, θ₂, ω₁, ω₂) | §7 L346: *s* = (θ₁, θ₂, ω₁, ω₂) | **symbol: bold s** |
| 2 | δ = θ₁ − θ₂; D′ = 2m₁ + m₂ − m₂ cos 2δ | §4.1 L207: δ = θ₁ − θ₂; (9), L220: the bracket of both denominators. The note gives D′ no name; D′ is the store's symbol (`ds.var('den')`, L423) | match |
| 3 | α₁ = [−g(2m₁+m₂) sin θ₁ − m₂g sin(θ₁−2θ₂) − 2 sin δ · m₂(ω₂²l₂ + ω₁²l₁ cos δ)] / (l₁D′) | (9), first line | match |
| 4 | α₂ = 2 sin δ [ω₁²l₁(m₁+m₂) + g(m₁+m₂) cos θ₁ + ω₂²l₂m₂ cos δ] / (l₂D′); d**<b>s</b>**/dt = (ω₁, ω₂, α₁, α₂) | (9), second line; §7 L346: d*s*/dt = F(*s*) = (ω₁, ω₂, α₁, α₂) | match except **bold s** |
| 5 | k₁ = **f**(**<b>s</b>**), …; **<b>s</b>ₙ₊₁ = <b>s</b>ₙ** + h/6 (k₁ + 2k₂ + 2k₃ + k₄) | (13), L347: k₁ = **F**(*s*), …; ***s*(t + h) = *s*** + (h/6)(k₁ + 2k₂ + 2k₃ + k₄) | **symbols differ** |
| 6 | τ ← τ + Δt · speed; n = min(⌊τ/h⌋, 600), τ ← τ − nh | §7 L350: steps of h, 600-step guard, carried remainder; §8 L359: Δt = real time since the last frame. τ and n are the store's symbols | match |
| 7 | T = ½(m₁+m₂)l₁²ω₁² + ½m₂l₂²ω₂² + m₂l₁l₂ω₁ω₂ cos δ; V = …; ε = (E − E₀)/[(m₁+m₂)gl₁ + m₂gl₂] | (3) multiplied out, with cos δ for cos(θ₁−θ₂); (4) letter for letter; §7 L351: E − E₀ against E_scale = (m₁+m₂)gl₁ + m₂gl₂ | match |
| 8 | σ = (min(W, H)/2 − 34)/(l₁ + l₂); x₁ = **o<sub>x</sub>** + σl₁ sin θ₁, **y₁** = **o<sub>y</sub>** + σl₁ cos θ₁; x₂ = x₁ + σl₂ sin θ₂, y₂ = y₁ + σl₂ cos θ₂ | §8 L358 (edited): σ the same; pivot **(x₀, y₀)**; bob 1 drawn at (x₀ + σl₁ sin θ₁, y₀ + σl₁ cos θ₁), bob 2 a further (σl₂ sin θ₂, σl₂ cos θ₂). In the note, x₁, y₁, x₂, y₂ are the metre positions of (1), with y pointing **up** | **pivot symbol differs; x₁…y₂ mean something else in the note** |

**Mismatch 2 (symbol, typography only).** Steps 1 and 4, pendulum.js:13 and :53. The walkthrough writes the state as a bold
**s**. The note writes a plain italic *s*. The Algebra column is set in italic serif (`.eq` in sim.css:131), so a plain `s`
matches the note.

Fix, step 1 `math` (pendulum.js:13): replace `⟦s|<b>s</b>⟧` with `⟦s|s⟧`.

Fix, step 4 `math` (pendulum.js:53): replace `d<b>s</b>/dt` with `ds/dt`.

**Mismatch 3 (symbols).** Step 5, pendulum.js:67. Three differences from (13): the walkthrough writes f where the note writes F,
writes **s**ₙ₊₁ = **s**ₙ + … where the note writes *s*(t + h) = *s* + …, and uses the bold s.

Fix, replace the whole `math` of step 5

```
⟦k1|k<sub>1</sub>⟧ = f(<b>s</b>), ⟦k2|k<sub>2</sub>⟧ = f(<b>s</b> + ½h k<sub>1</sub>)<br>⟦k3|k<sub>3</sub>⟧ = f(<b>s</b> + ½h k<sub>2</sub>), ⟦k4|k<sub>4</sub>⟧ = f(<b>s</b> + h k<sub>3</sub>)<br><b>s</b><sub>n+1</sub> = <b>s</b><sub>n</sub> + ⟦h|h⟧/6 (k<sub>1</sub> + 2k<sub>2</sub> + 2k<sub>3</sub> + k<sub>4</sub>)
```

with

```
⟦k1|k<sub>1</sub>⟧ = F(s), ⟦k2|k<sub>2</sub>⟧ = F(s + ½h k<sub>1</sub>)<br>⟦k3|k<sub>3</sub>⟧ = F(s + ½h k<sub>2</sub>), ⟦k4|k<sub>4</sub>⟧ = F(s + h k<sub>3</sub>)<br>s(t + h) = s + ⟦h|h⟧/6 (k<sub>1</sub> + 2k<sub>2</sub> + 2k<sub>3</sub> + k<sub>4</sub>)
```

**Mismatch 4 (symbol).** Step 8, pendulum.js:124. The walkthrough calls the pivot o<sub>x</sub>, o<sub>y</sub>. The edited note
calls it (x₀, y₀).

**Mismatch 5 (same symbol, different meaning).** Step 8, pendulum.js:124 and the `y1` row at :132. In the walkthrough, x₁, y₁,
x₂ and y₂ are screen pixels with y pointing down. In the note they are the metre positions of (1), with y pointing up
(y₁ = −l₁ cos θ₁). The note's §8 gives the screen positions no symbol. The page's store already tells the two apart: `y1`
(m, "above the pivot", L439) and `y1_px`, symbol "y<sub>1</sub> px" (L445). `Sim.live().y1` reads `y1_px`.

Fix for mismatches 4 and 5 together. Replace the `math` of step 8

```
⟦scale|σ⟧ = (min(W, H)/2 − 34) / (l<sub>1</sub> + l<sub>2</sub>)<br>x<sub>1</sub> = o<sub>x</sub> + σ l<sub>1</sub> sin θ<sub>1</sub>, ⟦y1|y<sub>1</sub>⟧ = o<sub>y</sub> + σ l<sub>1</sub> cos θ<sub>1</sub><br>x<sub>2</sub> = x<sub>1</sub> + σ l<sub>2</sub> sin θ<sub>2</sub>, y<sub>2</sub> = y<sub>1</sub> + σ l<sub>2</sub> cos θ<sub>2</sub>
```

with

```
⟦scale|σ⟧ = (min(W, H)/2 − 34) / (l<sub>1</sub> + l<sub>2</sub>)<br>x<sub>1</sub> px = x<sub>0</sub> + σ l<sub>1</sub> sin θ<sub>1</sub>, ⟦y1|y<sub>1</sub> px⟧ = y<sub>0</sub> + σ l<sub>1</sub> cos θ<sub>1</sub><br>x<sub>2</sub> px = x<sub>1</sub> px + σ l<sub>2</sub> sin θ<sub>2</sub>, y<sub>2</sub> px = y<sub>1</sub> px + σ l<sub>2</sub> cos θ<sub>2</sub>
```

and the `syms` row at pendulum.js:132

```
['y1', 'y<sub>1</sub>', 'pos(state)[1]', 'upper bob, px from top'],
```

with

```
['y1', 'y<sub>1</sub> px', 'pos(state)[1]', 'upper bob, px from top'],
```

### `note`

| Step | Claim | Lecture note | Verdict |
|---|---|---|---|
| 1 | four first-order equations; angles from the downward vertical; degrees to radians once | §2 L184 (the state); §8 L358 (θ from the downward vertical) | agrees |
| 2 | "the Cramer determinant **D** = l₁l₂(m₁ + m₂ sin²δ) from the derivation", D′ = 2D/(l₁l₂); never zero, smallest 2m₁ | (8): **det** = l₁l₂(m₁ + m₂ sin²δ) > 0; L219 "can never vanish" | **symbol differs** (the value agrees) |
| 3 | "Cramer’s rule on equations (6)–(7), written as the system (8) … after **the two** trigonometric identities" | L219, edited: now names **three** identities, the first two for α₁ and the third for α₂ | **stale pointer** (the numbers are right, see 3) |
| 4 | the returned array is the whole right-hand side | §7 L346: ds/dt = F(s) = (ω₁, ω₂, α₁, α₂) | agrees |
| 5 | local error O(h⁵), global O(h⁴), halving h gains about 16 | §7 L348: "halving the step makes the result sixteen times more accurate" | agrees |
| 6 | Δt about 1/60 s, h = 1/600 s; the clock caps a frame at 0.05 s; speed at most 1.5; at most 46 steps; the guard cannot act | §7 L348, L350 (edited: "the slider caps the Time scale"). sim.js:179 caps at 0.05; slider `max="1.5"` (page L64) | agrees |
| 7 | E = T + V conserved, so any change is numerical error; divided by the well depth because E₀ can be zero | §7 L351: "rather than against E₀, which can be close to zero"; edited: RK4 leaks energy slowly and steadily | agrees; the walkthrough quotes no drift size, so the new long-run and mass-ratio-10 figures leave it standing |
| 8 | "Screen y grows downward, so “+ cos θ” puts a hanging bob below the pivot **with no sign flip**"; σ in px/m; 34 px for the labels | §8 L358, edited: "Screen y points down, so **the minus signs of (1) turn into plus signs**". The labels sit at R + 18 px (page L592) | **contradicted in words** |

**Mismatch 6 (symbol).** Step 2, pendulum.js:27. The walkthrough names the determinant D. The note's (8) writes det, and the
walkthrough's "from the derivation" does not say which equation.

Fix, in `note` of step 2, replace

```
D′ is the Cramer determinant D = l<sub>1</sub>l<sub>2</sub>(m<sub>1</sub> + m<sub>2</sub> sin²δ) from the derivation, scaled: D′ = 2D/(l<sub>1</sub>l<sub>2</sub>) = 2(m<sub>1</sub> + m<sub>2</sub> sin²δ),
```

with

```
D′ is the determinant of the system (8), det = l<sub>1</sub>l<sub>2</sub>(m<sub>1</sub> + m<sub>2</sub> sin²δ), scaled: D′ = 2 det/(l<sub>1</sub>l<sub>2</sub>) = 2(m<sub>1</sub> + m<sub>2</sub> sin²δ),
```

**Mismatch 7 (stale pointer).** Step 3, pendulum.js:40. Before the edit, the note named exactly two identities, and "the two
trigonometric identities" pointed at them. The edited L219 names three. α₁ uses the first two, so the claim still holds for this
step, but "the two" no longer points at anything definite. The formula in the step is (9), which the walkthrough never names.

Fix, in `note` of step 3, replace

```
This is Cramer’s rule on equations (6)–(7), written as the system (8) in the lecture note, after the two trigonometric identities.
```

with

```
This is Cramer’s rule on equations (6)–(7), written as the system (8) in the lecture note, after two trigonometric identities, 2 sin²δ = 1 − cos 2δ and 2 sin θ<sub>2</sub> cos δ = sin θ<sub>1</sub> − sin(θ<sub>1</sub> − 2θ<sub>2</sub>); the result is the first line of (9).
```

**Mismatch 8 (claim contradicted in words).** Step 8, pendulum.js:125. The walkthrough says "with no sign flip". It means that
the code needs no minus sign. The edited note describes the same fact the other way round: compared with (1), the minus signs
become plus signs. Read side by side, the two sentences contradict each other.

Fix, in `note` of step 8, replace

```
Screen y grows downward, so “+ cos θ” puts a hanging bob below the pivot with no sign flip.
```

with

```
Screen y grows downward, so the minus signs of (1) turn into plus signs: “+ cos θ” puts a hanging bob below the pivot.
```

## 5. Not mismatches; optional

- **Step 8 jumps back across `...`.** It quotes page 513 (layout()) and then 506–507 (pos()). `where` names both functions in the
  order quoted, so I accept it with no fix, as for Fig. 5.
- **More citations.** Step 4 could end "α₂ is the second line of (9); its common factor sin δ comes from the third identity,
  sin θ<sub>1</sub> cos δ − sin θ<sub>2</sub> = cos θ<sub>1</sub> sin δ." Step 5 could add "(13)", and step 7 could add "(3)"
  and "(4)".
- **Step 2, "rods aligned (sin δ = 0)".** sin δ = 0 also holds with the rods folded back (δ = π). More exact: "(sin δ = 0: the
  rods in one line, straight or folded back)".
- **Step 3, the term labels.** "The gravity torque on the whole chain, the gravity pull the lower bob passes through the joint"
  is the walkthrough's own reading; the note does not label the terms. After the identity, the first term carries 2m₁ + m₂, not
  the chain's m₁ + m₂, so the reading is loose. The note does not contradict it.
- **Step 6, the carry.** The code keeps acc = min(τ − nh, h), and the formula writes τ ← τ − nh. The two differ only if the
  600-step guard acts, which it cannot. Exact form: `τ ← min(τ − n h, h)`.
- **Step 7, ε.** The note has no symbol for the drift; ε is the store's symbol (L437). Its denominator is the note's
  E<sub>scale</sub>.
- **Marks and rows.** Marks with no table row: `s` (step 1), `o1` and `o2` (step 4), `k2`, `k3`, `k4` (step 5). Rows with no mark
  in that step: `t` (step 6), `E0` (step 7), `l2` (step 8). A row with no mark lights only itself.

## 6. Outside the walkthrough file (page code, report only)

- The store's metadata for the pivot, `ds.var('ox')` and `ds.var('oy')` at page L453–454, still gives the symbols
  o<sub>x</sub>, o<sub>y</sub>. The edited note says x₀, y₀.
- `Sim.live().drift` (page L693) replaces only the first `-`, so a negative drift shows as "−4.15e-10" in the "Now" column,
  with a typographic minus in front and a hyphen in the exponent. `.replace(/-/g, '−')` would make both the same.

## How to re-run

The scripts are in the scratchpad, not in the repository:

- `/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/fig02/codecheck.cjs`: the fragment search, whole-line
  pass and neighbour check.
- `/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/fig02/marks.cjs`: marks against `syms` rows.
- `/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/fig02/live.cjs`: Chromium. It needs
  `python3 -m http.server 8712 --bind 127.0.0.1 --directory /tmp/fig02-walk-dist` running.

The core of the code check, in Node:

```js
const fs = require('fs'), vm = require('vm'), c = { window: {} }; vm.createContext(c);
vm.runInContext(fs.readFileSync('public/scripts/walk/pendulum.js', 'utf8'), c);
const page = fs.readFileSync('public/simulations/Double Pendulum.html', 'utf8').split('\n');
const strip = s => s.replace(/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g, '$1');
for (const st of c.window.WALK.pendulum.steps) for (const ln of strip(st.code).split('\n')) {
    if (!ln.trim() || ln.trim() === '...') continue;
    const fr = ln.split('...');
    const hit = page.some(pl => { let p = 0; return fr.every(f => { const i = pl.indexOf(f, p); if (i < 0) return false; p = i + f.length; return true; }); });
    if (!hit) console.log('NOT FOUND:', ln);
}
```

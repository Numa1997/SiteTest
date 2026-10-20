# Fig. 10 · walkthrough check (`turbine`)

> Lead's note, 20 October 2026: these proposed fixes were written before some later edits of the note and were audited
> against the current notes afterwards (docs/research-theory-audit.md, "Open, for Numa"). Fixes that touch a `code` or
> `where` field need the same permission as the rest. Nothing here has been applied; the walkthrough file is unchanged.


Checked on 20 October 2026 by the walkthrough keeper, at commit `468c139` (the working copy equals it for both files).

- Page: `public/simulations/wind-turbine.html`, 1 171 lines; lecture note at lines 150–537; `#walk[data-walk="turbine"]` at
  line 539; `Sim.live()` at lines 936–945.
- Walkthrough: `public/scripts/walk/turbine.js`, 121 lines, 8 354 bytes, 7 steps.
- `turbine.js` was not changed: Numa has not allowed it. Every fix below is written out so it can be applied as it stands once he does.

## Counts

| What | Checked | Found / matching | Not found / mismatched |
|---|---|---|---|
| Code lines (marks stripped, `...` lines left out) | 26 | 26 (all 26 also equal a whole page line after trimming) | 0 |
| Lines that are only `...` | 2 | (not searched) | |
| Lines with an inline `...` | 0 | | |
| Lines quoted together with no `...` between them | 17 joins | 17 are page neighbours | 0 silent elisions |
| Joins across a `...` line | 2 | both skip page lines, so the `...` is needed | 0 |
| Keys in `syms` returned by `Sim.live()` | 19 | 19 | 0 |
| Equation numbers "(n)" cited in `math` or `note` | 0 | | |
| `math` fields | 7 | 5 | 2 (step 1, symbols; step 5, a term left out) |
| `note` fields | 7 | 5 | 2 (step 4, contradicted by the edited note; step 3, contradicted by §6.1) |
| Marks inside `note` | 0 | | |

The code is quoted exactly and no elision is silent. Four mismatches with the note: one claim the edit now contradicts (step 4,
"without ringing"), one older claim that §6.1 contradicts (step 3), one list of constants with the wrong names (step 1), and one
integral left out of a list (step 5).

## 1. The code lines: 26 of 26 found verbatim

Method from `docs/scripts/walk.md`, "The rule": evaluate `turbine.js` in Node with a stub `window`, strip the marks with
`/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g → '$1'`, drop lines that are only `...`, split each remaining line on `...`, and look for the
fragments in order on one page line. A second, stricter pass checked that each line equals a whole page line after trimming,
and that lines quoted with no `...` between them are neighbours in the page.

| Step | `where` | Page lines quoted (`...` = lines left out) | Verdict |
|---|---|---|---|
| 1 How much of the wind the blades catch | cp() | 643–649 | all found, whole lines |
| 2 The torque of the wind | tauAero() | 650–652 | all found, whole lines |
| 3 The controller sets the generator torque | tauGen() | 681–684 | all found, whole lines |
| 4 Tuning the PI controller | solve(), before the loop | 698–699 | all found, whole lines |
| 5 Newton’s law for a rotation, stepped with RK4 | rates() and solve() | 689 ... 713–717 | all found, whole lines (the five RK4 lines also occur in `rk4Replay()` at 1001–1005; 713–717 are the ones in `solve()`, as `where` says) |
| 6 Store every second state | solve(), top of the loop | 707–708 | all found, whole lines |
| 7 Playback draws a stored sample | frame() and draw() | 948 ... 826 | all found, whole lines (the excerpt runs backwards in the page; the `...` covers it) |

No mismatch. The marks do not affect this check: there are none in any `code` field (see section 5).

## 2. `syms` keys: 19 of 19 returned by `Sim.live()`

Read from the code (lines 936–945), then measured. The page was built with
`APPDEPLOY_VITE_OUT_DIR=/tmp/fig10-walk-dist npm run build` (built `turbine.js` and page byte-identical to the sources) and
opened in headless Chromium at 1440 × 900. After 1.5 s, `Sim.live()` returned exactly the 19 keys used in `syms`, no more and no
fewer: `lam cp lopt cpmax Kopt v w ta tg Pg wref Kp Ki dtd n t th Eg bal`. All 7 steps drew, every "Now" cell in every step
filled (none at `—`), and the console showed no errors.

## 3. Equations in `math` against the lecture note

No step cites an equation number, so there is no "(n)" to check.

| Step | `math` | Lecture note | Verdict |
|---|---|---|---|
| 1 | c<sub>p</sub>(λ) = c₁(c₂/λ<sub>i</sub> − c₄)e<sup>−c₅/λ<sub>i</sub></sup> + c₆λ, 1/λ<sub>i</sub> = 1/λ − 0.035; **c₁…c₆ = 0.5176, 116, 5, 21, 0.0068** | eq. (5); line 238: **c₁ = 0.5176, c₂ = 116, c₄ = 5, c₅ = 21, c₆ = 0.0068** | formula matches; **constants named wrongly** |
| 2 | P<sub>aero</sub> = ½ρAv³c<sub>p</sub>(λ), τ<sub>aero</sub> = P<sub>aero</sub>/ω | eq. (2) | match |
| 3 | τ<sub>gen</sub> = K<sub>opt</sub>ω², K<sub>opt</sub> = ½ρπR⁵c<sub>p,max</sub>/λ<sub>opt</sub>³; τ<sub>gen</sub> = τ<sub>0</sub> + K<sub>p</sub>(ω − ω<sub>ref</sub>) + K<sub>i</sub>∫(ω − ω<sub>ref</sub>) dt | eq. (8); eq. (9), with τ<sub>0</sub> now defined at line 344 as τ<sub>aero</sub>(ω<sub>ref</sub>, v(0)) | match (the integral without its limits 0 and t; see section 6) |
| 4 | Jδω̈ + (K<sub>p</sub> − ∂τ<sub>aero</sub>/∂ω)δω̇ + K<sub>i</sub>δω = 0 ≡ δω̈ + 2ζ<sub>c</sub>ω<sub>n</sub>δω̇ + ω<sub>n</sub>²δω = 0; K<sub>i</sub> = Jω<sub>n</sub>², K<sub>p</sub> = 2ζ<sub>c</sub>ω<sub>n</sub>J + ∂τ<sub>aero</sub>/∂ω, ω<sub>n</sub> = 0.6 rad/s, ζ<sub>c</sub> = 0.8 | eq. (10) (written with ⟺); line 346 | match |
| 5 | J dω/dt = τ<sub>aero</sub> − τ<sub>gen</sub>, dI/dt = ω − ω<sub>ref</sub>; **carried along: E<sub>gen</sub>, E<sub>aero</sub>, s<sub>air</sub>, θ** | eq. (6); §8, line 507: “The same steps carry the generator energy, the aerodynamic energy, **the energy of the wind through the disc**, the distance the air has travelled and the rotor angle θ” | **one carried integral left out** |
| 6 | n = step/2, t<sub>n</sub> = n · 2h, P<sub>gen</sub> = τ<sub>gen</sub>ω | §5, line 297: P<sub>gen</sub> = τ<sub>gen</sub>ω; §8, line 508: every second state, h = 10 ms | match |
| 7 | n = round(t<sub>play</sub>/2h); blade b at θ<sub>n</sub> + 2πb/3 | §8, line 509: the stored row nearest to the playback time, blades at the stored angle θ; §9, line 515 | match |

**Mismatch 1 (symbols).** Step 1, turbine.js:13. “c₁…c₆ = 0.5176, 116, 5, 21, 0.0068” gives five values to what reads as six
names, so a reader assigns them in order: c₃ = 5, c₄ = 21, c₅ = 0.0068, and c₆ is left without a value. The note (line 238) and
the code (`C1, C2, C4, C5, C6`, line 556) have no c₃: c₄ = 5, c₅ = 21, c₆ = 0.0068. Older than the note edit.

Fix, in `math` of step 1, replace

```
c₁…c₆ = 0.5176, 116, 5, 21, 0.0068
```

with

```
c₁, c₂, c₄, c₅, c₆ = 0.5176, 116, 5, 21, 0.0068
```

**Mismatch 2 (a term left out).** Step 5, turbine.js:76. The list “carried along” has four integrals. The note’s §8 names five,
and so does the quoted code line itself: `return [(a - g) / J, dI, g * w, a * w, 0.5 * RHO * AREA * v * v * v, v, w];` carries
½ρAv³, the wind’s power through the disc of eq. (1), which the page integrates into E<sub>wind</sub> (dataset variable `Ew`) to
give the captured share. Older than the note edit.

Fix, in `math` of step 5, replace

```
dE<sub>aero</sub>/dt = τ<sub>aero</sub>ω, ds<sub>air</sub>/dt = v
```

with

```
dE<sub>aero</sub>/dt = τ<sub>aero</sub>ω, dE<sub>wind</sub>/dt = ½ ρ A v³, ds<sub>air</sub>/dt = v
```

(the new order is that of the code’s return array).

## 4. Claims in `note` against the edited lecture note

| Step | Claim | Lecture note | Verdict |
|---|---|---|---|
| 1 | Heier’s fit; peaks at λ<sub>opt</sub> = 8.1, c<sub>p,max</sub> = 0.48, below Betz 16/27; clipped at zero | §4, lines 236–238; Figure 2 caption (zero at λ = 13.4); the box after eq. (4) | agrees |
| 2 | ½ρAv³ is the kinetic energy through the disc each second; share c<sub>p</sub>; power over angular speed is torque | eq. (1), (2) | agrees |
| 3 | “Braking with K<sub>opt</sub>ω² balances the wind exactly when λ = λ<sub>opt</sub>, so the rotor settles at the best tip-speed ratio **for any wind**” | §6.1, line 340: “So **in steady wind**, with the torque below its limit, the rotor returns to λ<sub>opt</sub> … What the argument does not promise is optimal capture **in changing wind**” | **contradicted** |
| 3 | PI brakes harder when too fast; the integral removes a lasting error; torque clipped to 0 … 1.2 MN m | §6.2, line 346 | agrees |
| 4 | “an error dies within a few seconds, **without ringing**” | §6.2, line 346 (edited): “Because ζ<sub>c</sub> is a little below 1 it does swing once past zero, but only by a few per cent: … the rotor overshoots the target by 0.40 rpm and then dips below it by just 0.01 rpm” | **contradicted** |
| 5 | difference of torques; anti-windup; energies, air travel and angle in the same RK4 steps; the energy balance tests the whole computation | eq. (6), (7); §6.2 line 346; §8 lines 507–508 | agrees |
| 6 | 12 000 steps of 10 ms; every second state; 6 001 rows, with θ and s<sub>air</sub> | §8, lines 507–508 | agrees |
| 7 | blades turn because the stored θ changes; nothing integrated while you watch; air dashes 5 px per metre of air | §8, lines 505, 509; §9, line 515 | agrees |

**Mismatch 3 (claim contradicted, from the note edit).** Step 4, turbine.js:64. The edited note replaced “without ringing” by a
measured overshoot. Measured again in Chromium, Hold speed with Step wind at the defaults (v₀ = 8 m/s, Δv = 1.5 m/s, target
15 rpm): the rotor peaks at 15.3947 rpm at t = 32.96 s, 0.3947 rpm above the target, then dips to 14.9878 rpm at t = 40.80 s,
0.0122 rpm below it, 3.1 % of the peak excursion; from t = 42.66 s on it stays within 2 % of that excursion.

Fix, in `note` of step 4, replace

```
The gains are chosen so that it has a natural frequency of 0.6 rad/s and a damping ratio of 0.8: an error dies within a few seconds, without ringing.
```

with

```
The gains are chosen so that it has a natural frequency of 0.6 rad/s and a damping ratio of 0.8: an error dies within a few seconds. Because ζ<sub>c</sub> is a little below 1, it swings once past zero, by a few per cent: after the step in the Step wind the rotor runs about 0.4 rpm above the target, then dips 0.01 rpm below it.
```

**Mismatch 4 (claim contradicted, older than the edit).** Step 3, turbine.js:47. “For any wind” reads as any wind, changing wind
included; the note’s §6.1 limits the return to λ<sub>opt</sub> to steady wind (that sentence was in the note before the edit
and is still there). Measured in Chromium with Follow the wind: in Steady wind λ = 8.100 in all 6 001 stored rows; in the
default turbulent wind λ ranges from 6.39 to 10.74.

Fix, in `note` of step 3, replace

```
so the rotor settles at the best tip-speed ratio for any wind.
```

with

```
so in any steady wind the rotor settles at the best tip-speed ratio; when the wind changes, it takes a few seconds to catch up.
```

## 5. For the lead: a number in the note

Not a walkthrough mismatch. Line 346 of the note says the rotor “overshoots the target by 0.40 rpm”. The measured excursion is
0.3947 rpm (here, and in `notes/fig10/measure-out.json`, `pi/step.peak_rpm` = 15.394736…), which is 0.39 to two decimals.
Exact text: “overshoots the target by 0.39 rpm”. The fix to step 4 above says “about 0.4 rpm”, true either way.

## 6. Not mismatches with the note; optional

- **Marks.** None of the 7 `code` fields has a mark (14 marks in `math`, 0 in `code`), so hovering a symbol lights the formula
  and its table row but nothing in the Code column. Rows with no mark anywhere in their step: step 1 `lopt`, `cpmax`; step 2
  `v`; step 4 `Kp`, `Ki`; step 5 all five (`w`, `ta`, `tg`, `Eg`, `bal`); step 6 `th`; step 7 `n`. Adding marks keeps the code
  verbatim, since the check strips them; for example, in step 2,
  `return w > 1e-6 ? ⟦ta|0.5 * RHO * AREA * v * v * v * cp(w * R / v) / w⟧ : 0;` ties the code to `⟦ta|τ<sub>aero</sub>⟧`,
  which is already marked in `math`.
- **Step 3, the integral.** Eq. (9) writes K<sub>i</sub>∫<sub>0</sub><sup>t</sup>(ω − ω<sub>ref</sub>) dt′; the walkthrough
  writes ∫(ω − ω<sub>ref</sub>) dt. Same meaning. Exact text: `∫<sub>0</sub><sup>t</sup>(ω − ω<sub>ref</sub>) dt′`.
- **Step 4, the sign between the two forms.** Eq. (10) uses ⟺; the walkthrough uses ≡. Same meaning. Exact text: `&nbsp;⟺&nbsp;`.
- **Step 5, the `bal` row.** Its meaning reads “E<sub>aero</sub> = E<sub>gen</sub> + ΔE<sub>rot</sub>”; eq. (7) writes
  Δ(½Jω²) and never names E<sub>rot</sub>. Exact text: `relative error of (7), E<sub>aero</sub> = E<sub>gen</sub> + Δ(½Jω²)`.
- **Step 5, the excerpt.** It stops at `w += …` (line 717); the lines that integrate I and the carried quantities, 718 and 719,
  are not quoted. Not an elision (an excerpt may end anywhere), but the `math` names them.
- **Step 7, `where`.** The blade line (826) is in `drawScene()` (lines 802–889), which `draw()` calls at line 894. Exact text:
  `frame() and drawScene()`.
- **Equation numbers.** None are cited. If wanted: step 1 ↔ (5), step 2 ↔ (2), step 3 ↔ (8) and (9), step 4 ↔ (10),
  step 5 ↔ (6) and, for the balance, (7).

## How to re-run

Scripts were kept in the scratchpad, not in the repository. The core of the code check, in Node:

```js
const fs = require('fs'), vm = require('vm'), c = { window: {} }; vm.createContext(c);
vm.runInContext(fs.readFileSync('public/scripts/walk/turbine.js', 'utf8'), c);
const page = fs.readFileSync('public/simulations/wind-turbine.html', 'utf8').split('\n');
const strip = s => s.replace(/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g, '$1');
for (const st of c.window.WALK.turbine.steps) for (const ln of strip(st.code).split('\n')) {
    if (!ln.trim() || ln.trim() === '...') continue;
    const fr = ln.split('...');
    const hit = page.some(pl => { let p = 0; return fr.every(f => { const i = pl.indexOf(f, p); if (i < 0) return false; p = i + f.length; return true; }); });
    if (!hit) console.log('NOT FOUND:', ln);
}
```

The browser part: build as in section 2, serve `/tmp/fig10-walk-dist`, open `simulations/wind-turbine.html` with Playwright
(`npm root -g`, executablePath `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`), compare `Object.keys(Sim.live())` with
the `syms` keys, click each step tab and count `td[data-v]` cells reading `—`, then click `#ctrl button[data-v="pi"]`,
`#prof button[data-v="step"]` and `#solve` and read `Sim.data.ds.get('rpm')` for the overshoot.

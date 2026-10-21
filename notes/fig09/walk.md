# Fig. 9 · walkthrough check (`driven`)

> Lead's note, 20 October 2026: these proposed fixes were written before some later edits of the note and were audited
> against the current notes afterwards (docs/research-theory-audit.md, "Open, for Numa"). Fixes that touch a `code` or
> `where` field need the same permission as the rest. Nothing here has been applied; the walkthrough file is unchanged.


Checked on 20 October 2026 by the walkthrough keeper, at commit `d3ffae1`. The page and `driven.js` are the same as at `127a8d2`,
the commit that added equation (6a), and the working copy matches both.

- Page: `public/simulations/driven-oscillator.html`, 1 113 lines (it was 1 110 before (6a)). Lecture note at lines 140–456,
  `#walk[data-walk="driven"]` at line 458, `Sim.live()` at lines 892–901.
- Walkthrough: `public/scripts/walk/driven.js`, 121 lines, 7 603 bytes, 7 steps.
- I did not change `driven.js`, because Numa has not allowed it. Each fix below is written out in full, ready to apply once he does.

## Counts

| What | Checked | Found / matching | Not found / mismatched |
|---|---|---|---|
| Code lines (marks stripped, `...` lines left out) | 24 | 24 | 0 |
| Lines that are only `...` | 5 | (not searched) | |
| Lines with an inline `...` | 0 | | |
| `where` texts | 7 | 6 | 1 (step 1) |
| Line references in `driven.js` | 0 | | |
| Line references to Fig. 9's walkthrough in the docs | 20 | 20 | 0 |
| Keys in `syms` returned by `Sim.live()` | 20 keys (25 rows) | 20 | 0 |
| Equation numbers "(n)" in `math` or `note` | 0 | | |
| `math` fields | 7 | 6 | 1 (step 3) |
| `note` fields | 7 | 5 | 2 (steps 1, 6) |

The code is quoted exactly, and the three new lines of the lecture note moved nothing the walkthrough points to: it has no line
numbers, and it cites no equation numbers. There are four mismatches: one `where` text, one formula whose symbols mean other things
in the note, and two claims in notes that the lecture note contradicts. None of the four was caused by (6a). All four were already there.

## 1. The code lines: 24 of 24 found verbatim

I used the method from `docs/scripts/walk.md`, "The rule". Evaluate `driven.js` with a stub `window`, strip the marks with
`/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g → '$1'`, trim, leave out the lines that are only `...`, split each remaining line on `...`, and look for the
fragments in order on one line of the page. Then I made a stricter pass: each line must equal a whole page line after trimming, and lines
quoted together without a `...` between them must be neighbours in the page. The script is short:

```js
const win = {}; vm.runInNewContext(fs.readFileSync(walk, 'utf8'), { window: win });
const strip = s => s.replace(/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g, '$1');
for (const st of win.WALK.driven.steps)
  for (const L of strip(st.code).split('\n').map(s => s.trim()).filter(s => s && s !== '...')) {
    const frags = L.split('...').map(s => s.trim()).filter(Boolean);
    const hits = page.flatMap((pl, i) => { let p = 0;
      for (const f of frags) { const k = pl.indexOf(f, p); if (k < 0) return []; p = k + f.length; } return [i + 1]; });
    // hits.length === 0 → not found
  }
```

| Step | `where` | Page lines quoted (`...` = lines left out) | Verdict |
|---|---|---|---|
| 1 From the sliders to k, c and Ω | `solve(), first line` | 571 | found; whole line; **`where` wrong: W1** |
| 2 Newton’s second law, solved for the acceleration | `accel()` | 566 567 568 | all found; whole lines; `where` true |
| 3 One Runge–Kutta step | `solve(), inside the loop` | 583 584 585 586 ... 590 591 | all found; whole lines; `where` true |
| 4 Store every tenth state | `solve(), top of the loop` | 576 577 578 579 580 | all found; whole lines; `where` true (575 is the `for`) |
| 5 Energy bookkeeping | `solve(), inside the loop and after it` | 588 589 ... 615 | all found; whole lines; `where` true |
| 6 The exact answer, to measure the error | `steady() and solve()` | 557 558 ... 597 | all found; whole lines; `where` true |
| 7 Playback picks a stored sample | `the clock, frame() and draw()` | 916 ... 904 ... 838 | all found; whole lines; `where` true |

No line is missing, so the code needs no fix. Three things are worth knowing, and none of them is a mismatch:

- The RK4 lines of steps 3 and 5 also occur, word for word, in `rk4Replay()` at lines 941–949, the data panel's check. The first
  occurrence, inside `solve()`, is the one `where` names.
- The excerpt of step 7 runs backwards through the page (916, then 904, then 838). `where` names the three places in that same
  order, and the format does not require page order.
- This list of quoted lines is the same as the one in `docs/simulations/fig09-driven-oscillator.md` (lines 308–318).

### W1 · step 1, `where`

The quoted line 571 is the second line of `solve()`. The first, line 570, is `var start = performance.now();`, the timer for the
"solve time" readout. Both lines have been there since commit `2226030` (14 October 2026).

```
old:            where: 'solve(), first line',
new:            where: 'solve(), second line, after the timer starts',
```

## 2. Line references

`driven.js` holds no line numbers. These references point at the walkthrough, and all of them still hold after the page grew three lines:

- `docs/scripts/walk.md`, row Fig. 9: `data-walk` at L458; the definition at `driven.js` L7; the step titles at L11, L24, L38, L55, L74, L89 and
  L104; 121 lines, 7.6 kB, 7 steps.
- `docs/simulations/fig09-driven-oscillator.md`: the quoted lines L571, L566–L568, L583–L586, L590–L591, L576–L580, L588–L589,
  L615, L557–L558, L597, L916, L904 and L838 (lines 308–318); `Sim.live()` at L892–L901 (lines 200 and 259); `data-walk` at L458 (line 302);
  `driven.js:57–58` for "step / 10", "60 000 steps" and "6 001 rows" (line 354).

## 3. `syms` keys against `Sim.live()`: 20 of 20 returned

The steps use these keys: `w0 k c W h steps n t x v F E Win Wloss bal X phi err sc bx`. `Sim.live()` (lines 892–901) returns exactly these
20 and no others. Every value is read from the store with `ds.get`.

I measured it in headless Chromium: the build is in `/tmp/fig09-walk-dist`, and its page, `driven.js` and `sim.js` are byte-identical to
`public/`; viewport 1400 × 1000; 1.5 s after load. 7 steps were drawn. In every step, no "Now" cell showed `—` or stayed empty. The
rendered code of every step equals its `code` field with the marks stripped. There were 0 console errors.

| Key | Now (defaults) | Lecture note says |
|---|---|---|
| `k`, `c` | 9.870 N/m, 0.3142 kg/s | k = 9.87 N/m, c = 0.314 kg/s (section 2) |
| `steps`, `h` | 60000, 0.001 s | 60 000 steps of h = 1 ms (section 8) |
| `X`, `phi` | 0.48194 m, 25.35° | X = 0.482 m, φ = 25.3° (section 3.2) |
| `err` | 5.26e-12 m | 5 × 10⁻¹² m (section 8) |
| `Win`, `Wloss`, `bal` | 19.0317 J, 17.9256 J, 1.27e-12 | 19.03 J, 17.93 J, 1.3 × 10⁻¹² (section 7) |

The `t` row of step 4 says `ts[n]` in "In code", but `Sim.live()` returns `t_play`, the continuous playback time. During playback I took 40
samples. In all 40, the 2-decimal value shown equals n · 10 ms, so the reader sees the stored time. No fix is needed.

## 4. The equations against the lecture note

| Step | Walkthrough | Lecture note | Verdict |
|---|---|---|---|
| 1 `math` | ω<sub>0</sub> = 2πf<sub>0</sub>, k = mω<sub>0</sub>², c = 2ζmω<sub>0</sub>, Ω = 2πf | section 2 (lines 205–207): ω<sub>0</sub> = √(k/m), ζ = c/(2√(km)), f<sub>0</sub> = ω<sub>0</sub>/2π, f = Ω/2π | same symbols, same meaning |
| 1 `note` | the sliders say "how fast it **rings**"; "the two languages differ **only by factors of 2π**" | line 205: free ringing occurs at ω<sub>d</sub> = ω<sub>0</sub>√(1−ζ²); line 221 (new): "ring at the damped frequency ω<sub>d</sub>"; line 207: k = 9.87 N/m, c = 0.314 kg/s | **N1** |
| 2 `math` | m ẍ = F<sub>0</sub> cos Ωt − c ẋ − k x ⇒ ẍ = (F<sub>0</sub> cos Ωt − c v − k x)/m | (1), line 204 | same; v appears before step 3 defines it (optional **O1**) |
| 2 `note` | three forces; t appears explicitly, so the system is driven | lines 203, 208 | same |
| 3 `math` | k₁ = **f**(t, **s**) …, **s**(t + h) = **s** + (h/6)(**k₁** + 2**k₂** + 2**k₃** + **k₄**), **s** = (x, v) | f is the drive frequency (line 207, and step 1 here); k is the stiffness; s is the root of x = e<sup>st</sup> (line 221, new) and the Laplace variable of (7) and the poles (lines 333–335) | **M1** |
| 3 `note` | state (x, v), slope (v, a); largest error about 5 × 10⁻¹² m | section 8, line 427 | same |
| 4 `math` | n = step/10, t<sub>n</sub> = n · 10h, F<sub>n</sub> = F<sub>0</sub> cos Ωt<sub>n</sub>, E<sub>n</sub> = ½mv<sub>n</sub>² + ½kx<sub>n</sub>² | section 7 (E, line 417), section 8 (every tenth state, line 427) | same |
| 4 `note` | 60 000 steps; 6 001 rows, one every 10 ms; the animation computes no state | section 8, lines 426–428 | same |
| 5 `math` | W<sub>in</sub> = ∫Fv dt, W<sub>loss</sub> = ∫cv² dt, E(T) − E(0) = W<sub>in</sub> − W<sub>loss</sub> | (8), line 418, with ẋ for v | same meaning |
| 5 `note` | the integrals ride in the same RK4 step; the work–energy theorem tests the whole computation | lines 419, 426 | same |
| 6 `math` | X = (F<sub>0</sub>/m)/√((ω<sub>0</sub>² − Ω²)² + (2ζω<sub>0</sub>Ω)²), φ = atan2(2ζω<sub>0</sub>Ω, ω<sub>0</sub>² − Ω²), error = max<sub>n</sub>\|x<sub>n</sub> − x<sub>exact</sub>(t<sub>n</sub>)\| | (4), line 219, letter for letter; atan2 argument order as in line 218 (new); error as in line 427 | same |
| 6 `note` | steady oscillation plus a dying free one; "uses the exact solution only to grade …, **never to draw**" | line 213 and (5); section 9, line 435: "the steady amplitude ±X dashed in rose", "the Bode plot … (equation (4))" | **N2** |
| 7 `math` | t<sub>play</sub> ← t<sub>play</sub> + speed · Δt, n = round(t<sub>play</sub>/10h), x<sub>block</sub> = x<sub>eq</sub> + x<sub>n</sub> · px/m | section 8, line 428: n = round(t<sub>play</sub>/10 ms); section 9, line 435: rest position and 0.11W<sub>0</sub> | same |
| 7 `note` | nearest sample, no interpolation; the "Stored run" slider jumps anywhere | line 428 | same |

The edits that added (6a), the new paragraphs in sections 3.1 and 3.2, the pole sign in section 5, Exercise 6.1, the mean-power step in section 7 and the window chart in section 9
contradict nothing in the walkthrough. The only new link is the root s in section 3.2, which makes the clash in M1 sharper.

### M1 · step 3, `math`: f, k and s mean other things in the note

In the lecture note, f is the drive frequency, k the spring stiffness, and s the exponent of x = e<sup>st</sup> and the Laplace variable. Step 1
of this same walkthrough uses f and k in their note meanings. Step 3 then uses f for the slope function, k₁…k₄ for the RK4 stages and s for the state. The fix writes the
step in the code's own names, one formula line for each code line (583, 584, 585, 586, then 590–591). Every symbol in it means the same as in the note.

```
old:            math: 'k₁ = f(t, s), k₂ = f(t + h/2, s + h k₁/2), k₃ = f(t + h/2, s + h k₂/2), k₄ = f(t + h, s + h k₃)<br>s(t + ⟦h|h⟧) = s + (h/6)(k₁ + 2k₂ + 2k₃ + k₄), &nbsp; s = (x, v)',
new:            math: 'a₁ = a(t, x, v), &nbsp; x₂ = x + (h/2) v, &nbsp; v₂ = v + (h/2) a₁<br>a₂ = a(t + h/2, x₂, v₂), &nbsp; x₃ = x + (h/2) v₂, &nbsp; v₃ = v + (h/2) a₂<br>a₃ = a(t + h/2, x₃, v₃), &nbsp; x₄ = x + h v₃, &nbsp; v₄ = v + h a₃<br>a₄ = a(t + h, x₄, v₄)<br>x(t + ⟦h|h⟧) = x + (h/6)(v + 2v₂ + 2v₃ + v₄), &nbsp; v(t + h) = v + (h/6)(a₁ + 2a₂ + 2a₃ + a₄)',

old:            note: 'The state is the pair (x, v); its slope is (v, a). The slope is sampled four times per step, ...
new:            note: 'The state is the pair (x, v); its slope is (v, a), where a(t, x, v) is the acceleration of step 2. The slope is sampled four times per step, ...
```

(In the `note`, only the first sentence changes. The rest, from "The slope is sampled" to "“RK4 vs exact”.'", stays as it is.)

A shorter alternative keeps the textbook form and only renames to letters the note does not use (u, g, K):

```
new:            math: 'K₁ = <b>g</b>(t, <b>u</b>), K₂ = <b>g</b>(t + h/2, <b>u</b> + h K₁/2), K₃ = <b>g</b>(t + h/2, <b>u</b> + h K₂/2), K₄ = <b>g</b>(t + h, <b>u</b> + h K₃)<br><b>u</b>(t + ⟦h|h⟧) = <b>u</b> + (h/6)(K₁ + 2K₂ + 2K₃ + K₄), &nbsp; <b>u</b> = (x, v), &nbsp; <b>g</b> = (v, a)',
```

### N1 · step 1, `note`: f<sub>0</sub> is not the ringing frequency, and the conversion is not only 2π

The slider sets f<sub>0</sub>, the undamped natural frequency. The note says the block rings at ω<sub>d</sub> = ω<sub>0</sub>√(1−ζ²) (line 205, and
the new line 221). The note does not state the second claim, but it is inexact: with m = 1 kg, k = (2πf<sub>0</sub>)² and c = 4πζf<sub>0</sub>, a square
and a product, not factors of 2π.

```
old:            note: 'The sliders speak the language of the experiment (how fast it rings, how quickly it dies away); the equation of motion needs a stiffness and a friction coefficient. With m = 1 kg the two languages differ only by factors of 2π.',
new:            note: 'The sliders speak the language of the experiment (how fast it would ring without damping, how quickly it dies away); the equation of motion needs a stiffness and a friction coefficient. With m = 1 kg the translation is k = (2πf<sub>0</sub>)² and c = 4πζf<sub>0</sub>: 9.87 N/m and 0.314 kg/s with the defaults.',
```

### N2 · step 6, `note`: formula (4) is drawn

What the page never draws is the exact motion (5), `xex`. It is stored only to measure the error (line 427; code line 597). The
steady amplitude X of (4), the subject of this step's formula, is drawn: the dashed ±X lines of the window chart (code line 788,
`X = ds.get('X')`), and the whole Bode plot with its filled dot (`bode()` lines 630–631; `G_drive`, `phi_deg`). Section 9 of the note says so
(line 435).

```
old:            note: 'This equation can also be solved with pencil and paper: a steady oscillation at the driver’s frequency plus a dying free oscillation. The page uses the exact solution only to grade the numerical one, never to draw.',
new:            note: 'This equation can also be solved with pencil and paper: a steady oscillation at the driver’s frequency plus a dying free oscillation. The page uses the exact motion, equation (5), only to grade the numerical one, and never draws it; formula (4) is drawn only as guides, the dashed ±X lines of the window chart and the Bode plot.',
```

(Corrected by the lead on 20 October 2026: the trailing comma was missing from the new text above; without it driven.js does not parse. Found by the independent audit.)

The new text cites (4) and (5). Both numbers point to the right equations, at lines 219 and 222.

## 5. Optional

These are not mismatches with the page or the note, but small fixes would help the reader.

- **O1, step 2 `math`.** v appears next to ẋ before step 3 says that the state is (x, v).
  `old: ... − c v − k x) / m',` → `new: ... − c v − k x) / m, &nbsp; v = ẋ',`
- **O2, step 5 `syms`.** The "In code" cell of `bal` is empty.
  `old: ['bal', 'balance', '', 'relative error']` → `new: ['bal', 'balance', "ds.set('balance', …)", 'relative error']`
- **O3, step 6 `syms`.** "In code" names `st.phi`, which is in radians, but "Now" shows degrees, from `phi_deg`.
  `old: ['phi', 'φ', 'st.phi', 'phase lag']` → `new: ['phi', 'φ', 'st.phi', 'phase lag, shown in degrees']`
- **Marks.** Only step 1 marks quantities in its code. In steps 2–7, hovering lights the formula and the table but nothing in the code. Steps
  2 (`k`, `c`, `W`), 3 (`steps`) and 4 (`x`, `v`) also have table rows with no mark anywhere. This is outside the check asked for here. It
  matters only for the promise in `docs/scripts/walk.md` that the code lights up with the formula and the table.

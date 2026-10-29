# Fig. 7 · Phasor sums · walkthrough check

> Lead's note, 20 October 2026: these proposed fixes were written before some later edits of the note and were audited
> against the current notes afterwards (docs/research-theory-audit.md, "Open, for Numa"). Fixes that touch a `code` or
> `where` field need the same permission as the rest. Nothing here has been applied; the walkthrough file is unchanged.


Walkthrough `public/scripts/walk/phasors.js` (key `phasors`, 134 lines, 8 190 bytes, 8 steps), page
`public/simulations/phasor-sums.html` (`data-walk="phasors"` at L652), lecture note L221–650 as edited on 20 October 2026
(`git diff`: §5 cancellation paragraph, §6 "at the foot of the controls", §8 dot radius, §8.1 Record/Replay, §9.1 links).
The walkthrough file was not changed. Scripts: `/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/fig07walk/`
(`check.cjs`, `order.cjs`, `live.cjs`, `star.cjs`).

## Counts

| Check | Result |
|---|---|
| Code lines checked (marks stripped, `...` lines left out) | **26** |
| Found verbatim on one page line | **26** |
| Not found | **0** |
| Lines that are only `...` | 2 (step 4, step 7) |
| Lines with an inline `...` | 0 |
| Relations checked in `math` | 14 |
| Formulas checked in `note` | 8 |
| Equation numbers "(n)" in the walkthrough | 0, so none can point to the wrong equation |
| `syms` keys | 30, all returned by `Sim.live()` (32 keys) |
| Mismatches with the note | **5** (steps 3, 4, 7, 8, 8) |

## 1. Code excerpts against the page

Method (walk.md, "The rule"): evaluate the file with a stub `window`, strip `/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g → '$1'`, split each
line on `...`, find the fragments in order on one page line. A second pass (`order.cjs`) asked more: each trimmed line equals a
whole page line, and lines not separated by `...` sit on consecutive page lines. Both passes: 26 of 26.

| Step | `where` | Page lines | `where` true? |
|---|---|---|---|
| 1 One arm: a phasor | sumAt() — inside the loop over arms | 817, 818, 819 | yes (`sumAt` L813) |
| 2 Tip to tail: the sum | sumAt() — the accumulation | 820, 821, 822 | yes |
| 3 The clock | Sim.clock callback | 1324, 1325, 1326 | yes (`Sim.clock(function (dt) {` L1316) |
| 4 When the curve closes | structure() | 830, 831, 832, `...`, 835 | yes (`structure` L828; `...` = L833–834, quoted in step 5) |
| 5 Rotational symmetry | structure() | 833, 834 | yes |
| 6 Average size: Parseval | readouts() | 1158, 1159 | yes (`readouts` L1156) |
| 7 Final shape and morphing | refinal() and morphStep() | 846, `...`, 866, 867 | yes (`refinal` L844, `morphStep` L863) |
| 8 Auto Dance: sound into radii | buildLive() | 944–949 | yes (`buildLive` L939) |

The page and walk file served by the build (`OUT_DIR=/tmp/fig07-walk-dist npm run build`) are byte-identical to
the sources (`cmp`).

## 2. Equations and notes against the lecture note

| Step | Walkthrough | Note | Verdict |
|---|---|---|---|
| 1 math | z₁(t) = A e^{i(ωt + φ)} = A cos(ωt + φ) + i A sin(ωt + φ) | (5); z₁ is the first joint (§3), which for arm 1 is its phasor | same |
| 1 note | e^{iθ} = cos θ + i sin θ | (3) | same |
| 2 math | x + iy = z(t) = Σ_{k=1}^{N} A_k e^{i(ω_k t + φ_k)}, \|z\| | (6) | same |
| 2 note | partial sums are the joints, the last one draws | §3, z_k, z = z_N | same |
| 3 math | t ← t + Δt · s, s = speed · (1 + mid · **drive**) | §7: t advances by Δt · s; s is Speed "multiplied by a factor from the music when Auto Dance is on"; §8.1 (L623): 1 + mid · d_speed | **mismatch 1** |
| 3 note | Δt capped at 50 ms; closed form, no integration error | §7 (L600) | same |
| 4 math | G = gcd(100ω₁, …, 100ω_N), g = G/100, T = 2π/g | (12); 100ω_k whole, Euclid (§5); round(100ω_k), A = 0 left out (§7) | same |
| 4 note | "z(t + T) = z(t) needs every ω_kT to be a multiple of 2π" | §5 (L453, edited): the pen can come back sooner when arms cancel; e^{it} − e^{it} + e^{2it} repeats after π s while (12) gives 2π s | **mismatch 2** |
| 5 math | M = gcd(ω_j − ω₁), ω₁/M = p/q ⇒ q-fold | §5.1: M = gcd(ω₂ − ω₁, …, ω_N − ω₁), ω₁/M = p/q, q-fold | same |
| 5 note | τ = 2π/M, factors e^{iω_kτ} equal, turn 2π ω₁/M | (13) and §5.1, β = ω₁τ = 2π ω₁/M | same |
| 6 math | ⟨\|z\|²⟩_t = Σ A_k², and \|z(t)\|² now | (15); the condition "all ω_k different" is in the walk note in words | same |
| 6 note | cross terms A_jA_k cos((ω_j − ω_k)t + …) average to zero | (14), §6 | same |
| 7 math | **n samples over one period**; p ← p + α(q − p) | §7 (L603): n + 1 times t_i = i T_span/n; the span is the period only with *Draw one full period* on, at most 60 · 2π s; (16) p_i ← p_i + α(q_i − p_i) | **mismatch 3** (the morph rule is the same, index i dropped) |
| 7 note | gap shrinks by (1 − α) each frame, low-pass filter | (16), §7.1 | same |
| 8 math | A′ = A · m, m = [1 + ease(bass) · **drive** · (1 − 0.7\|ω\|/\|ω\|_max)] · burst | §8.1 (L621): A′ = A[1 + ease(bass) d_bass (1 − 0.7\|ω\|/\|ω\|_max)]; burst 1 + d_burst falling to 1 over 10 frames (L624) | **mismatch 4** |
| 8 note | "Faster arms use 1 + high · **drive** instead"; stored A never changed | §8.1 (L622): A′ = A(1 + high · d_high); L626 | **mismatch 5** (first sentence); second sentence same |

Record timing: no walkthrough `note` mentions *Record* or *Replay* (grep), so the edited §8.1 sentence contradicts nothing.
The step 8 sentence "the stored A is never changed" is about Auto Dance, as is the note's own sentence at L626; Replay, which
does move the stored values (L1203), is not mentioned in the walkthrough. The other edits (§6 readout place, §8 dot radius,
§9.1 links) touch nothing the walkthrough says.

## 3. Mismatches and the exact fixes

Each fix replaces one string in `public/scripts/walk/phasors.js`; no code line changes, so the 26 excerpts stay verbatim.

**1. Step 3, math (L45): "drive" is the note's d_speed, and the factor applies only with Auto Dance on** (code L957:
`danceOn ? 1 + clamp01(energy.mid) * dSpeed.value : 1`; with a song playing and Auto Dance off, mid > 0 but s = speed).

- L45 old: `math: '⟦t|t⟧ ← t + ⟦dt|Δt⟧ · ⟦sf|s⟧, &nbsp; s = ⟦spd|speed⟧ · (1 + mid · drive)',`
- L45 new: `math: '⟦t|t⟧ ← t + ⟦dt|Δt⟧ · ⟦sf|s⟧, &nbsp; s = ⟦spd|speed⟧ · (1 + mid · d<sub>speed</sub>)',`
- L46 old: `note: 'Δt is the real time since the last frame, capped at 50 ms so a background tab does not jump. Because z(t) is evaluated in closed form, there is no integration error however large t becomes.',`
- L46 new: `note: 'Δt is the real time since the last frame, capped at 50 ms so a background tab does not jump. The bracket holds only with Auto Dance on, d<sub>speed</sub> being the Speed drive; with it off, s is the Speed slider alone. Because z(t) is evaluated in closed form, there is no integration error however large t becomes.',`

**2. Step 4, note (L61) and the `Tc` row (L70): the edited §5 says T = 2π/g repeats every arm, and the pen can repeat sooner
when arms cancel.** The walk note says z(t + T) = z(t) *needs* every ω_kT to be a multiple of 2π, which the note's example
e^{it} − e^{it} + e^{2it} (period π s, while ω_kT = π for the first two arms) disproves; the row calls T "period of the closed
curve", the note calls it the shortest time that repeats every listed active arm.

- L61 old: `note: 'z(t + T) = z(t) needs every ω<sub>k</sub>T to be a multiple of 2π. Sliders move in steps of 0.01 rad/s, so 100ω is an integer and Euclid’s algorithm finds the largest common frequency g exactly.',`
- L61 new: `note: 'Every arm is back at its start when every ω<sub>k</sub>T is a whole multiple of 2π, so z(t + T) = z(t). The pen can repeat sooner when arms of the same frequency cancel; the Period readout ignores that and uses every arm with A &gt; 0. Sliders move in steps of 0.01 rad/s, so 100ω is an integer and Euclid’s algorithm finds the largest common frequency g exactly.',`
- L70 old: `['Tc', 'T', 'TAU / g', 'period of the closed curve']`
- L70 new: `['Tc', 'T', 'TAU / g', 'shortest time that repeats every arm with A &gt; 0']`

**3. Step 7, math (L100), note (L101) and the `span` row (L108): the note samples n + 1 times over T_span, which is one period
only with *Draw one full period* on** (and at most 60 · 2π s = 377 s; with it off, Span × 2π s). Code: `new Array(n + 1)`,
`i <= n`, `sumAt(i / n * sp, …)` (L847–849), `sp = spanNow()` (L845, L838–842).

- L100 old: `math: '⟦n|n⟧ samples over ⟦span|one period⟧; &nbsp; p ← p + ⟦alpha|α⟧ (q − p)',`
- L100 new: `math: '⟦n|n⟧ + 1 samples at t<sub>i</sub> = i ⟦span|T<sub>span</sub>⟧/n; &nbsp; p ← p + ⟦alpha|α⟧ (q − p)',`
- L101 old: `note: 'The whole closed curve is sampled at once. When a slider moves, …` (rest unchanged)
- L101 new: `note: 'The whole span is sampled at once: one period with Draw one full period on, at most 60 · 2π s. When a slider moves, …` (rest unchanged)
- L108 old: `['span', 'span', 'finalSpan', 'time span drawn'],`
- L108 new: `['span', 'T<sub>span</sub>', 'finalSpan', 'time span drawn'],`

**4. Step 8, math (L116): "drive" is the note's d_bass (the Bass drive).**

- L116 old: `math: '⟦Ar|A′⟧ = ⟦A|A⟧ · ⟦mul|m⟧, &nbsp; m = [1 + ease(⟦bass|bass⟧) · drive · (1 − 0.7|ω|/|ω|<sub>max</sub>)] · ⟦burst|burst⟧',`
- L116 new: `math: '⟦Ar|A′⟧ = ⟦A|A⟧ · ⟦mul|m⟧, &nbsp; m = [1 + ease(⟦bass|bass⟧) · d<sub>bass</sub> · (1 − 0.7|ω|/|ω|<sub>max</sub>)] · ⟦burst|burst⟧',`

**5. Step 8, note (L117): "drive" is the note's d_high (the High drive).**

- L117 old: `note: 'For arms at or below the median |ω|. Faster arms use 1 + high · drive instead. The copy …` (rest unchanged)
- L117 new: `note: 'For arms at or below the median |ω|, with d<sub>bass</sub> the Bass drive. Faster arms use 1 + high · d<sub>high</sub> instead, with d<sub>high</sub> the High drive. The copy …` (rest unchanged)

## 4. `syms` keys against `Sim.live()`

Read in the code (L1294–1313) and measured in headless Chromium (Playwright from `npm root -g`, executablePath
`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, 1440 × 900, 1.5 s after load, build served on port 18731): the 30 keys
`A w ph t ang x1 y1 N x y absz dt spd sf G g Tc M q E absz2 n span alpha dev dance bass burst mul Ar` are all returned (the
other two, `mid` and `high`, are not used). The walkthrough drew 8 steps; clicking each step, every "Now" cell held a value,
none `—`; 0 console errors. Every key in a step's `math` or `code` has a row in that step; rows without a mark: `w`, `ph`, `t`
(step 1), `dev` (step 7), `dance` (step 8), which is allowed.

## 5. Two points inside the walkthrough (not contradictions of the note)

- Step 5: the formula's M is the note's M in rad/s, but the "Now" column shows the code's M, the gcd of the differences of
  100ω. Measured on the Star preset: Now shows `M = 500`, the note says M = 5 (q = 5 in both). The row says "×100", so the
  page is honest; for a sharper row, L81 could read `['M', 'M', 'M', 'gcd of the differences of 100ω, integer: 100 M']`.
- Step 1: in the live view `sumAt` is called with the drawn list (`sumAt(t, live, ANG)`, L1119), so `x1`, `y1` are
  A′ cos(ωt + φ) and A′ sin(ωt + φ), while the `A` row shows the stored A. With Auto Dance off, A′ = A and the row is exact;
  with it on, Now(x1) ≠ Now(A) · cos(Now(ang)). A sentence in the step 1 note would say so, for example "In the live view the
  arms passed in are the drawn copies A′ of step 8; with Auto Dance off, A′ = A."

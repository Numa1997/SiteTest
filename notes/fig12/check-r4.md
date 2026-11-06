# Fig. 12 check, round 4: sections 10 and 11 (the one-wheel cart), and (12) as section 10 uses it

Page checked: `public/simulations/beer-slosh.html` at commit 6add1b6, served at http://localhost:8765/simulations/beer-slosh.html.
`notes/fig12/plan.md` was not read.

How I checked it:
- **Derivations.** I re-derived everything from scratch in SymPy, with my own Lagrangian, not the one in `check_plant.py`. That covers the energy check, (18a), (18b), (19), the mode row against (12), the pumping term, the sloshing mass, the envelope slope and the first-contact angle. For a straight cylinder I checked the Green's-identity steps by quadrature (scratch script `derive.py`).
- **Python reference.** I ran `tools/fig12/check_plant.py` (PASS). I ran `note_numbers.py` with its output sent to the scratchpad; it reproduces `notes/fig12/numbers.json` exactly.
- **The page in headless Chromium (Playwright).** I ran `notes/fig12/gate-ctl3.cjs` and `tools/fig12/gate_ctl3.py` (PASS). I also wrote my own scripts that drive the page's own `step()`, `restart()` and `design()` through `window.SLOSH`, read the page's own arrays, and set its sliders. They cover every number in sections 10 and 11, plus a sweep of every slider claim.
- **The kick-only and pump-only split.** The page has no switch for these. I served a patched copy through Playwright route interception, so `public/` was not touched. The patch adds two guards: `if (!window.__noPump)` before the pumping line and `window.__noKick ? 0 :` in the kick line.

Units were checked for every equation. Each term of (18b) is in N. The mass-matrix entries ρQₙNₙ, ρNₙ/λₙ and ρλQ²N/(1+κ) are in kg; ρgN is in N/m; each term of (20) is dimensionless.

## A. Findings, ranked

### 1. The Lagrangian counts the stout's mass twice along the road (wrong equation in the text; the code is right)
**Quoted:** "The kinetic energy of the body, the glass and the wheel is ½M ẋ_c² + ½M_s′ ż_b² + ½m_w ż_w², with M_s′ = M_b + m_g; the stout's is ½ρ∫|∇Φ|²dV … Expanding the square gives ½m_l(ẋ_c² + ż_b²)". Section 10 defines M = M_s + m_w with M_s = M_b + m_g + m_l.

**What is wrong:** ½Mẋ_c² already contains m_l. Adding the stout's ½m_l ẋ_c² makes the x-row mass M_b + m_g + 2m_l + m_w. The vertical term is right, because M_s′ leaves m_l out. The horizontal one does not.

**Evidence:** I derived the x-row in SymPy from T_rigid = ½(M_b + m_g + m_w)ẋ_c² + … plus the stout's KE. It gives M_b + m_g + m_l + m_w, which is `M[ix,ix] = M_tot` in `plant.py` and `Mm[IX][IX] = Mtot` on the page (12.42 kg). Written as the note has it, the result is 12.93 kg.

**Fix:** "The kinetic energy of the body, the glass and the wheel is ½(M − m_l)ẋ_c² + ½M_s′ż_b² + ½m_w ż_w², with M − m_l = M_b + m_g + m_w and M_s′ = M_b + m_g". Or introduce M′ = M_b + m_g + m_w.

### 2. "19.8 mm at the front of the rim" is the rise at the back
**Quoted (section 10, key result):** "the stout climbs 19.8 mm at the front of the rim, and the head runs over".

**What is wrong:** On the page, the highest the stout gets at the front (θ = 0) is 15.5 mm, at t = 1.12 s, while the road brakes. The 19.8 mm is the largest |η| on the rim. It comes at t = 1.28 s, after the shove, when the front dips to −19.8 mm and the back rises 19.8 mm. The x-modes are exactly odd: ψ has only its cos θ component in the data. The same holds over the kerb, where the front rises 9.9 mm and the rim 12.9 mm, and at 3 m/s, where the front rises 8.4 mm and the rim 11.0 mm.

Figure 6 plots the signed front height, clipped at −10 mm. So its caption, "the head runs over when the curve passes the dome limit, 5.9 mm up", misses the overflow at the back, which is the larger one (the passive curve goes down to −19.8 mm, and the skyhook curve to −12.6 mm).

**Evidence:** I ran the page's `step()` and took `etaWall(0)` every 10 ms. Passive bump: the front's maximum is +15.53 mm at 1.121 s and its minimum −19.83 mm at 1.281 s. The maximum over 72 rim angles is 19.83 mm. Python's peak is `|h·x|`, the absolute value of the front height, so it reports 19.83 mm as well.

**Fix:** "the stout climbs 15.5 mm at the front of the rim as the road brakes, then 19.8 mm at the back as it shoves, and the head runs over". In the Figure 6 caption: "the head runs over when the curve passes +5.9 mm, or −5.9 mm (then at the back)". Or draw both dashed lines.

### 3. Shrinking σ_w makes the kick larger, not smaller
**Quoted:** "shrink σ_w and the strut holds the tyre load steadier, which trims the kick but not by much."

**What is wrong:** On the page, over the default bump with the LQR, every step down in σ_w makes the kick larger, the tyre-load swing wider and the wave higher:

| σ_w | 1 mm | 0.5 mm | 0.2 mm | 0.1 mm |
|---|---|---|---|---|
| largest kick | 26.9 N | 27.8 N | 30.2 N | 32.0 N |
| tyre load N | 90.5–147.8 N | 84.4–153.2 N | 66.6–165.4 N | 52.0–173.5 N |
| rim wave | 0.94 mm | 0.96 mm | 1.03 mm | 1.08 mm |

**Evidence:** These are the page's own runs, with the sliders set. The Python `controller3.design(s_w=…)` and `simulate()` agree: 26.8, 27.7, 30.1 and 31.8 N; N from 90.5–147.8 to 52.0–173.5 N.

**Fix:** "shrink σ_w and, against intuition, the kick grows (from 27 to 32 N at σ_w = 0.1 mm) and the tyre load swings more: the cost sees the tyre deflection only at the samples, 10 ms apart, while the wheel hops at 30 Hz." The last clause is my inference, not measured.

### 4. The cart's largest acceleration is 1.41 and 0.70 m/s², not 1.37 and 0.43
**Quoted (section 11, key result):** "its largest acceleration falls from 1.37 to 0.43 m/s²".

**What is wrong:** These numbers come from `np.gradient` of ẋ_c sampled every 10 ms in `note_numbers.py`, a central difference over 20 ms. That smooths away the jump that comes from holding the motor force for 10 ms. On the page, averaged over each 1 ms step, the largest |ẍ_c| is:
- passive: 1.41 m/s², at t = 0.72 s;
- LQR: 0.70 m/s², at t = 0.69 s, just after the kick starts and before the motor answers at the next sample.

Even averaged over each 10 ms hold, the LQR gives 0.51 m/s².

**Evidence:** Page run, (qd[IX] after the step − before) / 1 ms. Python's instantaneous acceleration at its own sample instants is 1.405 and 0.452 m/s². Those samples always fall 1 ms after a control update, so they miss the stale-force end of each hold.

**Fix:** "its largest acceleration falls from 1.41 to 0.70 m/s²". To keep a smoothed figure, say "averaged over 10 ms, from 1.37 to 0.51 m/s²". In `note_numbers.py`, compute `maxXdd` from the right-hand side at every step, not from 10-ms samples.

### 5. Equation numbers (18a) and (18b) collide with (18)
**Quoted:** "(18a)", "(18b)" in section 10. (18) is the foam-damping law γ_f of section 7.

**What is wrong:** A reader takes (18a) and (18b) for parts of (18), but they have nothing to do with it. (12a) is fine, because it derives (12).

**Evidence:** The tags in order are 1–11, 12a, 12, 13–18, 18a, 18b, 19, 20. They are referred to in sections 9 and 10 ("Tyre load is N of (18b)", "Kick … of (18b)", "the axle's path (18a)", "Use (18a)" in Problem 7), and (19) and (20) in sections 10 and 11.

**Fix:** Renumber the envelope and the kick as (19a) and (19b), the equations of motion as (20) and the cost as (21). Update every reference, including Problem 7 and section 9.

### 6. c_drive = 20 N·s/m cannot be set, and at c_drive = 0 the LQR silently switches off
**Quoted:** "slacken it to 20 N·s/m and the passive cart climbs 23.8 mm".

**What is wrong:**
- **20 is not on the slider.** The `cd` slider has min 0 and step 50, so a reader can get 0 or 50, not 20. With the step overridden, the page does give 23.83 mm at 20, and Python gives 23.83 mm. At the reachable values:

  | c_drive | 0 | 50 | 200 (default) | 2000 |
  |---|---|---|---|---|
  | passive peak | 20.95 mm | 25.09 mm | 19.83 mm | 2.49 mm |

  So the curve is not monotonic.
- **At c_drive = 0 the LQR gives up without a word.** The speed ẋ_c becomes an undamped integrator, and the cost does not see it. That puts it on the unit circle, exactly the obstruction the note gives for the position. The page's Riccati iteration runs all 6000 iterations without converging, so `Ct.ok` is false and `control()` applies no force. The "LQR" run is then identical to the passive one (20.95 mm, |u| = 0). τ_cl reads 28 s, and no message appears.

**Evidence:**

| c_drive | 0 | 20 | 50 | 200 | 2000 |
|---|---|---|---|---|---|
| Riccati iterations | 6000 (ok = false) | 3972 | 2025 | 860 (cold) | 730 |

**Fix:** In the note, either quote a value the slider reaches ("slacken it to 50 N·s/m and the passive cart climbs 25.1 mm") or give the slider step 10. The page needs one of these: a slider minimum above 0, a small weight on ẋ_c in (20), or a message when the design fails. The note could add one line: "with no drive at all, c_drive = 0, the speed itself would sit on the unit circle and the regulator has no solution."

### 7. The rough road's 13 mm is a dip, not the highest point, and it is not "as generated"
**Quoted:** "scaled by the slider, whose 13 mm default is the highest point of the class C profile as generated."

**What is wrong:** `ROUGH_PEAK` = 12.7 mm is the largest |z_r| in the first 3 m of the feature. There the generated profile only dips, to −12.70 mm, and its highest point is 0. Over the 9 m the cart crosses in 6 s, the highest point is 11.2 mm; over the whole 30 m table it is 19.9 mm. And the 13 mm default (the slider steps in whole mm) scales the generated profile by 13/12.7 = 1.024, so it is not "as generated".

**Evidence:** `road.iso_random` and the page's `zRoad` agree. On x in [1, 4] m: max 0.000 mm, min −12.703 mm. On [1, 10] m: max 11.218 mm. On [1, 31] m: max 19.940 mm. `notes/fig12/test.cjs` checks `Math.abs(zRoad)`, which confirms that the |z| reading is the intended one.

**Fix:** "scaled by the slider, whose 13 mm default is, to the nearest millimetre, the largest excursion of the class C profile as generated in its first 3 m (a dip of 12.7 mm)".

### 8. T_s at 60 ms is overstated
**Quoted:** "Stretch T_s toward 60 ms and the controller looks too rarely to catch a 3 Hz slosh."

**What is wrong:** On the page the LQR still keeps the head in at 60 ms. The wave grows smoothly with T_s, and at 60 ms it is 3.57 mm, under the 5.87 mm dome limit.

| T_s | 10 ms | 20 ms | 30 ms | 40 ms | 50 ms | 60 ms |
|---|---|---|---|---|---|---|
| peak wave | 0.94 mm | 1.34 mm | 1.88 mm | 2.41 mm | 3.33 mm | 3.57 mm |

**Evidence:** Page runs with the slider set and the design redone. τ_cl goes from 1.118 s to 1.046 s.

**Fix:** "Stretch T_s to 60 ms, five looks per slosh, and the wave grows almost fourfold, to 3.6 mm: still inside the dome, but the controller is losing its grip."

### 9. The energy check: a wrong step, and two small inconsistencies
**Quoted:** "Then M ẍ_c = −Mg z_a′, and since Ẋ = v, d/dt ½MẊ² = −Mg z_a′Ẋ = −Mg dz_a/dt" … "slow to √(v² − 2gh) = 1.29 m/s at the top, about gh/v = 0.20 m/s slower".

**What is wrong:**
- Ẋ = v + ẋ_c, not v; the cart is slowing down. The step needs Ẍ = ẍ_c (v is constant) and dz_a/dt = z_a′Ẋ. With those the result is exact, and SymPy gives dE/dt = 0.
- "Take the drive away" should also take away the rolling resistance c_x, as `check_plant.py` does.
- 1.5 − 1.289 = 0.211 m/s. The 0.196 m/s is only the first-order estimate gh/v.

**Evidence:** SymPy: d/dt[½MẊ² + Mg z_a(X)] = 0 when MẌ = −Mg z_a′(X). `check_plant.py`: slowest speed 1.2890 m/s, energy drift 6.0 × 10⁻⁶.

**Fix:** "Take the drive and the rolling resistance away … Then MẌ = M ẍ_c = −Mg z_a′(X), so d/dt ½MẊ² = −Mg z_a′Ẋ = −Mg dz_a/dt … slow to 1.29 m/s at the top, 0.21 m/s slower (gh/v = 0.20 m/s to first order)".

### 10. The current limit: something does change before 24 N
**Quoted:** "Lower the current limit: on the bump the motor asks for 24 N of 160, so nothing changes until the limit falls below that".

**What is wrong:** One limit applies to both actuators, and the strut asks for 50 N. Below I_max = 2.5 A the strut is clipped first. At 2.0 A it is held to 40 N and the lowest tyre load falls from 90.5 to 79.2 N. The stout is unchanged, because the strut cannot reach it: 0.936 mm down to 1.2 A (24 N). The wave then grows:

| I_max (force) | 1.2 A (24 N) | 1.0 A (20 N) | 0.8 A (16 N) | 0.5 A (10 N) |
|---|---|---|---|---|
| peak wave | 0.94 mm | 1.27 mm | 2.28 mm | 7.16 mm |

**Evidence:** Page runs with the `Imax` slider.

**Fix:** "… the pint does not change until the limit falls below that (the strut, which asks for 50 N, is clipped from 2.5 A down, but it cannot reach the stout); at 1 A the wave is 1.3 mm, at 0.5 A the head runs over."

### 11. "within 0.1 %" is just exceeded
**Quoted:** "reproduces every peak … to within 0.1 %".

**What is wrong:** The worst case is the bump under the LQR, at 0.1009 %. All the others are at most 0.092 %.

**Evidence:** `gate-ctl3.cjs` and `gate_ctl3.py`, rerun at higher precision.

**Fix:** "to within 0.11 %", or "to about 0.1 %".

### 12. "On a gentle hump z_a is z_r itself" is approximate
**What is wrong:** The axle path is the road offset by R_w along its normal. It has the same top (30.0 mm) and the same steepest slope (0.18849 against 0.18846), but it sits up to 1.40 mm above z_r(X) on the flanks. To second order the offset is R_w z_r′²/2 = 1.42 mm; SymPy gives R s²/2 for a slope s.

**Evidence:** Page: max |zAxle − zRoad| = 1.401 mm on the 30 mm bump.

**Fix:** "On a gentle hump z_a is the road raised along its normal by R_w: the same height at the top and the same steepest slope, and within R_w z_r′²/2 = 1.4 mm of z_r elsewhere".

### 13. Riccati iteration counts
**Quoted:** "about 900 iterations from cold, fewer from the last solution".

**What is wrong:** The cold count is 860, which is fine. But a warm start can take more iterations than a cold one: going back to the defaults from c_drive = 2000 took 1066, and c_drive = 20 took 3972.

**Fix:** "about 900 iterations from cold at the defaults, usually fewer from the last solution".

### 14. A garbled sentence
**Quoted:** "the wheel has left the road and both pushes are zero computed on the page when it happens; the readout says so."

**What is wrong:** The "computed" badge sits in the middle of the clause, so the sentence does not read.

**Fix:** "… both pushes are zero, and the readout says so when it happens [computed]".

### 15. Two masses are silently left out (small; worth one clause)
- **The head.** Its 13.5 g (M_f πa² = 2.72 kg/m² × 4.97 × 10⁻³ m²) is in neither M nor M_s, though it heaves and travels with the glass. That is 0.1 % of the cart.
- **The wheel's spin.** It is not in the Lagrangian. For a disc, I/R_w² = ½m_w = 0.75 kg would add 6 % to the mass along the road. The tangential friction needed to spin the wheel up and down is about 0.75 kg × 1.4 m/s² ≈ 1 N against a 30 N kick, which supports "no friction worth counting".

**Fix:** One clause in "The machine": "the wheel's spin and the head's 14 g are left out".

## B. Every equation and every number of sections 10 and 11 (and (12) as section 10 uses it)

| # | Item (quoted) | Verdict | Evidence |
|---|---|---|---|
| E1 | (12) with ẍ_O = ẍ_c, β = 0: ä + 2γȧ + ω²(1 + z̈_O/g)a = −λQẍ_c/(1+κ) | verified | SymPy projection of the dynamic condition with the head pressure M_f η_tt: ä = −λ(Qẍ + (g + z̈)a)/(1+κ). The mode row of my Lagrangian, divided by (ρN/λ)(1+κ), minus (12) is 0. Limits: as κ → 0 it becomes −λQẍ; at steady state a = −Qẍ/g, the tilted plane. |
| E2 | Pumping term as the page applies it: −ρN z̈_O a on the mode row, σ part not scaled | verified | (ρN/λ)(1+κ)ω² z̈/g = ρN z̈(1 + σλ²/ρg). The page drops the σλ²/ρg part, as the note says. Clamp at −0.8 g: code `Math.max(-0.8*g, azO)`. |
| E3 | (18a) the envelope z_a(X) = max[z_r(x′) + √(R_w² − (X − x′)²)] − R_w | verified | Flat road gives 0. Envelope theorem: z_a′ = (x* − X)/√(R² − (X − x*)²), so the push direction (from contact to axle) has horizontal/vertical = −z_a′. Page `buildRoad` and `road.Axle` implement it on a 2 mm grid. `check_plant` step test: 9.282 and 17.460 mm, equal to the circle round the edge. |
| E4 | "On a gentle hump z_a is z_r itself" | wrong, because z_a lies up to 1.40 mm above z_r (≈ R_w z_r′²/2); only the top and the steepest slope agree (finding 12) | page max |z_a − z_r| = 1.401 mm |
| E5 | push along (−z_a′, 1)/√(1+z_a′²); kick −N z_a′, with N its vertical part | verified | SymPy (E3). Units: N. Sign: uphill z_a′ > 0, so the kick is negative (back). Code `kick = -N*sl`. |
| E6 | (18b) N = Mg + k_t(z_a − z_w) + c_t(ż_a − ż_w) ≥ 0, M = M_s + m_w | verified | Static balance of the wheel. Units: N. Code `deriv()`: same formula, ż_a = (v + ẋ_c)z_a′. Lift-off: N < 0 gives N = 0 and F_w = −N on the wheel, so the total tyre force is 0. No lift-off in any default run (N_min 36 N passive bump). |
| E7 | Energy check d/dt ½MẊ² = −Mg dz_a/dt | wrong step, because "since Ẋ = v" is false (Ẋ = v + ẋ_c); the result holds with Ẍ = ẍ_c and dz_a/dt = z_a′Ẋ (finding 9) | SymPy dE/dt = 0 |
| E8 | KE of body, glass, wheel = ½Mẋ_c² + … with M the whole cart | wrong, because m_l is counted twice along x; correct: ½(M − m_l)ẋ_c² (finding 1) | SymPy x-row mass M_b + m_g + m_l + m_w = code `M_tot` |
| E9 | stout KE ½m_l(ẋ_c² + ż_b²) + ½(ρN_n/λ_n)(1+κ_n)ȧ_n² + ρQ_nN_n ẋ_c ȧ_n | verified | Straight cylinder (1,1), R = 40 mm, by quadrature: ∫∇x·∇Φ dV = 2.730043 × 10⁻³ = λQN; ∫|∇Φ|²dV = 8.155860 × 10⁻² = λN; Q = 33.4734 mm = 2R/(ξ² − 1). The head term: ½M_f∫η̇² = ½(ρN/λ)κȧ². |
| E10 | the cross term ż_b ȧ_n vanishes, since ∫_Sψ_n = 0 | verified | quadrature ∫∇z·∇Φ dV = 1 × 10⁻¹⁹; the page and Python M have no z_b–a_n entry |
| E11 | potential: ½k_s(z_b − z_w)², ½k_t(z_w − z_a)², ½ρgN_n(1 + σλ_n²/ρg)a_n² | verified | K[i,i] = μω²(1+κ) = ρgN(1 + σλ²/ρg) in the code. Units: N/m. |
| E12 | Rayleigh function: ½c(ż_b − ż_w)², ½c_t(ż_w − ż_a)², ½(c_x + c_drive)ẋ_c², (ρN/λ)(1+κ)γȧ² | verified | SymPy rows; C[i,i] = 2μ(1+κ)γ in the code |
| E13 | (19) M_c q̈ + C_c q̇ + K_c q = F, q = (x_c, z_b, z_w, a_1…a_14); F = k_t z_a + c_t ż_a on the wheel, the kick on x_c | verified (apart from E8) | SymPy wheel row gives k_t z_a + c_t ż_a. Page NQ = 3 + 14. Hand assembly against the SymPy Hessians differs by 0 (`check_plant`). Python carries only the 4 m = 1 modes; the other 10 have Q_x ≤ 1 × 10⁻⁷ m. |
| E14 | "the row of (19) for a mode, divided by (ρN/λ)(1+κ), is (12) with ẍ_O = ẍ_c" | verified | SymPy difference 0; `check_plant` 3.4 × 10⁻¹⁶ |
| E15 | "the pumping … is third order in the Lagrangian" | verified (order count) | The z̈ a term in the equations comes from a term like ż_b ȧ a in L, which is cubic. Not derived further. |
| E16 | sloshing mass m_n = ρλ_nQ_n²N_n/(1+κ_n); pushback −ρQ_nN_n ä_n | verified | SymPy: M − M_eff at high frequency = ρλQ²N/(1+κ). Units: kg. Cylinder: 92.02 g by quadrature = 2ρπR³tanh/(ξ(ξ² − 1)); deep fraction 0.4545. |
| E17 | "in the linear model the strut cannot touch the slosh at all" | verified | M, C, K have no z_b/z_w–a_n or z–x entries (SymPy and the page). The LQR gains come out decoupled: K_s = 0 on a_n, ȧ_n, ẋ_c; K_m = 0 on d, w, ż_b, ż_w (page K). The strut acts only through N in the nonlinear kick; skyhook and LQR cut the kick from 30 to 26.5 N. |
| E18 | the position left out "would sit on the unit circle … no stabilising solution" | verified | With x_c added and not penalised, A_d has an eigenvalue of exactly 1, and SciPy's DARE leaves the closed-loop spectral radius at 1.0000000. The same happens to ẋ_c at c_drive = 0 (finding 6). |
| E19 | LQR state 2 + 2 + 3 + 2 = 9 | verified | page Ct.n = 9, numbers.json n = 9; ax = modes (1,c,1) and (1,c,2) |
| E20 | x_{i+1} = A_d x_i + B_d u_i, A_d = e^{AT_s}, B_d from one matrix exponential | verified | page `expm` of [[A, B], [0, 0]]T_s; Python `zoh` |
| E21 | (20) J = Σ[η_rim²/σ_η² + w²/σ_w² + ż_b²/σ_v² + u_s²/σ_u² + u_m²/σ_m²], η_rim = Σa_nψ_n(rim, 0) | verified | Each term dimensionless. Page Q, R built term by term. ψ_n(rim, 0) = 1.0 for both x-modes. They are exactly odd (only the cos θ component), so the front alone suffices. |
| E22 | W = Σhhᵀ/σ², W_u = diag(1/σ_u², 1/σ_m²); K = (W_u + B_dᵀPB_d)⁻¹B_dᵀPA_d; P = W + A_dᵀP(A_d − B_dK) | verified | the standard DARE; page loop identical; page gains equal SciPy `solve_discrete_are` to 1.9 × 10⁻⁹ |
| N1 | M_b = 10 kg, k_s = 3000 N/m, c = 60 N·s/m, m_w = 1.5 kg, R_w = 80 mm, k_t = 50 kN/m, c_t = 20 N·s/m, h_g = 0.25 m, glass 0.42 kg, c_drive = 200, c_x = 5 N·s/m | verified | page P and plant.DEFAULT (h_g has no effect in this model: level tray, no pitch) |
| N2 | M_s = 10.9 kg | verified | 10.9237 kg (page ds M_s) |
| N3 | f_z = √(k_s/M_s)/2π = 2.64 Hz | verified | 2.6375 Hz |
| N4 | damping ratio 0.17 | verified | 60/(2√(3000 × 10.924)) = 0.1657 |
| N5 | wheel hop about 30 Hz | verified | √((k_t + k_s)/m_w)/2π = 29.92 Hz |
| N6 | M/(c_x + c_drive) = 0.06 s | verified | 12.424/205 = 0.0606 s |
| N7 | the stout's 3.23 Hz | verified | f_11 = 3.2334 Hz |
| N8 | 0.33 s to cross the bump at 1.5 m/s; slosh period 0.31 s | verified | 0.3333 s; 1/3.2334 = 0.3093 s |
| N9 | the bump's steepest slope πh_r/0.5 m = 0.19 | verified | 0.18850 (road 0.18846, axle path 0.18849) |
| N10 | √(v² − 2gh) = 1.29 m/s | verified | 1.2890 m/s; check_plant's free roll gives 1.2890 |
| N11 | "about gh/v = 0.20 m/s slower" | wrong, because the drop is 1.5 − 1.289 = 0.21 m/s; 0.196 m/s is only the first-order estimate (finding 9) | — |
| N12 | energy kept to 6 × 10⁻⁶ | verified | check_plant: 6.0 × 10⁻⁶ |
| N13 | sloshing masses 81 g and 2.3 g, out of 504 g of stout | verified | page arrays: 81.17 g, 2.277 g; m_l = 503.7 g |
| N14 | "a 12 kg cart"; "12.4 kg of it" (section 6) | verified | 12.424 kg |
| N15 | kerb 20 mm smoothed over 5 cm; met by the rim | verified | tanh(x/12.5 mm): 2–98 % over 50 mm; axle starts rising 40 mm before the step (page) |
| N16 | cobbles h_r sin²(πX/0.1 m), 6 mm; bump ½h_r[1 − cos(2πX/0.5 m)] | verified | identical to the code's (X − 1 m) form, because 1 m is a whole number of periods |
| N17 | ISO 8608 class C: G_d(n_0) = 256 × 10⁻⁶ m³, n_0 = 0.1, n⁻², 120 sines, 0.05–10 cycles/m, 20 cm fade | verified | page ROUGH and zProfile; amplitude √(2G_dΔn) is the right one-sided PSD amplitude |
| N18 | "13 mm default is the highest point of the class C profile as generated" | wrong, because 12.7 mm is the largest |z| (a dip) in the first 3 m, where the highest point is 0; 13 mm scales by 1.024 (finding 7) | — |
| N19 | road and axle path on a 2 mm grid | verified | ROAD_DX = 0.002 |
| N20 | passive bump: kick reaches 30 N | verified | page 30.06 N (every step), 29.9 N (10 ms samples) |
| N21 | passive bump: 19.8 mm "at the front of the rim", head runs over | wrong, because the front rises 15.5 mm; the 19.8 mm is at the back; it does run over either way (finding 2) | page 19.83 mm max over the rim |
| N22 | kick alone 10.6 mm | verified | page (patched copy, pumping off) 10.61 mm; Python 10.61 mm |
| N23 | pumping alone gives nothing | verified | page 0.006 mm (from the 1 µm seed); Python 0.000 mm |
| N24 | together 19.8 mm; heave up to 0.78 g | verified | 19.83 mm; page max |z̈_b| = 0.781 g |
| N25 | 4.4 mm at 0.5 m/s, 11.0 mm at 3 m/s | verified | page 4.439 and 11.018 mm (at the rim; the front alone gives 4.44 and 8.38 mm) |
| N26 | kerb 12.9 mm, cobbles 1.8 mm, rough road 5.2 mm (passive) | verified (at the rim; on the kerb the 12.9 mm is at the back) | page 12.861, 1.775, 5.242 mm |
| N27 | Bℓ = 20 N/A, I_max = 8 A, 160 N | verified | page P |
| N28 | static tyre load 122 N | verified | Mg = 121.88 N |
| N29 | T_s = 10 ms | verified | page P.Ts = 0.01 |
| N30 | c_sky = 300 N·s/m | verified | page P.csky |
| N31 | σ_η = 0.5 mm, σ_w = 1 mm, σ_v = 50 mm/s, σ_u = σ_m = 20 N | verified | page P and the slider defaults |
| N32 | about 900 iterations from cold, fewer from the last solution | verified for the cold count (860); the second half fails sometimes (finding 13) | page Ct.iters |
| N33 | closed-loop time constant 1.12 s | verified | page 1.11784 s = Python. The slowest closed-loop motion is a 4.87 Hz slosh. |
| N34 | Figure 6: the wheel reaches the bump at 0.67 s; dome limit 5.9 mm | verified | first rise of z_a at X = 1.0005 m, t = 0.667 s; 160 + 8 − 144.133 − 18 = 5.867 mm |
| N35 | Figure 6: "the head runs over when the curve passes the dome limit" | wrong, because the curve is the front, and the larger overflow is at the back (the curve below −5.9 mm) (finding 2) | — |
| N36 | 19.8 / 13.5 / 0.9 mm (passive, skyhook, LQR) on the bump | verified | page 19.83, 13.45, 0.936 mm |
| N37 | LQR at most 50 N in the strut and 24 N in the motor | verified | page 49.79 N and 24.27 N |
| N38 | the kick 26 to 30 N under all three | verified | page 26.48–30.06 N |
| N39 | the motor pushes against the kick almost force for force | verified | page, t from 0.6 to 1.2 s: corr(u_m, kick) = −0.983; |kick + u_m| ≤ 6.0 N against a 27 N kick |
| N40 | largest acceleration falls from 1.37 to 0.43 m/s² | wrong, because the page gives 1.41 and 0.70 m/s² (0.51 averaged over 10 ms) (finding 4) | — |
| N41 | kerb 12.9 / 9.9 / 2.8 mm; the motor reaches 121 N | verified | page 12.861, 9.911, 2.753 mm; 121.29 N |
| N42 | cobbles 1.8 becomes 0.7 mm; rough road 5.2 becomes 0.4 mm | verified | page 1.775 → 0.651 mm; 5.242 → 0.432 mm |
| N43 | Python gains equal to 2 × 10⁻⁹; same τ | verified | 1.9 × 10⁻⁹; τ 1.11784 = 1.11784 s |
| N44 | every peak within 0.1 % | wrong, because the worst is 0.1009 % (bump under the LQR) (finding 11) | gate rerun |
| N45 | c_drive = 2000: 19.8 falls to 2.5 mm | verified | page 2.486 mm |
| N46 | c_drive = 20: 23.8 mm | verified numerically (page with the step overridden: 23.83 mm), but unreachable on the slider (step 50) (finding 6) | — |
| N47 | shrink σ_m: the motor is spent more sparingly, the pint rises | verified | σ_m 20 → 10 → 5 → 1 N: wave 0.94 → 1.48 → 2.61 → 7.88 mm; motor 24.3 → 21.6 → 20.7 → 11.7 N |
| N48 | shrink σ_w: the tyre load steadier, the kick trimmed | wrong, because the kick grows 26.9 → 32.0 N and N widens to 52–174 N (finding 3) | — |
| N49 | current limit: nothing changes until below 24 N; the kerb asks for 121 N | partly wrong: the stout is unchanged down to 1.2 A, but the strut is clipped from 2.5 A (finding 10); 121 N verified | — |
| N50 | T_s toward 60 ms: too rare to catch the slosh | wrong (overstated), because at 60 ms the wave is 3.57 mm, still under the 5.87 mm dome (finding 8) | — |
| N51 | the other twelve modes: no coupling in a round glass, a faint one in the sculpted glass | verified | page Q_x: (3,c,1) −1 × 10⁻⁷ m, every other non-x mode 0 |
| N52 | cobbles 15 Hz at walking pace (section 6, as used in section 10) | verified | 1.5/0.1 = 15 Hz |
| N53 | the tyre's compression "a few millimetres" | verified | static 2.44 mm; 6.2 mm at the passive bump's 308 N maximum |
| N54 | Problem 6: 45 %, 1 + κ_11 = 1.127, against 81 g | verified | 0.4545; κ_11 = 0.1267; 90.7 g/1.127 = 80.4 g |
| N55 | Problem 7: sin = 1 − h/R_w, kick = N cot | verified | SymPy (E3, E5) |
| N56 | cross-references: Fig. 9 actuator; "Balancing Two Rods on a Cart" zero-order hold | verified | driven-oscillator.html is Fig. 9 (Lorentz force, moving coil); double-inverted-pendulum.html derives the zero-order hold |

## C. Does the description of the method match the code?

All verified, line by line against `deriv()`, `step()`, `control()`, `designNow()`, `ctlState()`, `buildRoad()` and `assemble()`:
- **The integrator.** RK4 at 1 ms. The controller samples every T_s and holds the force (zero-order hold).
- **The kick.** It is added as a force at every RK4 stage. ż_a = (v + ẋ_c)z_a′. Lift-off is handled by clamping N at 0 and adding F_w = −N on the wheel.
- **The pumping.** z̈_O is lagged by one substep and clamped at −0.8 g.
- **The design model.** (d, w, a, ẋ_c, ż_b, ż_w, ȧ), with the road's rate dropped. A and B are built by probing unit states. The zero-order hold uses one matrix exponential.
- **The Riccati solution.** Iterated with a warm start, tolerance 10⁻¹¹.
- **The time constant.** Taken from the largest eigenvalue modulus, found with Faddeev–LeVerrier and Durand–Kerner.
- **The skyhook law.** u_s = −c_sky ż_b, with the motor idle.
- **The limit.** One current limit clips both forces.

The descriptions disagree with the code in two places:
1. **The "largest acceleration" in `note_numbers.py`** is taken from 10-ms samples, and the note does not say so (finding 4).
2. **When the design fails (c_drive = 0),** `Ct.ok` silently disables the LQR, and neither the note nor the page says so (finding 6).

## D. What I ran

- **`python3 tools/fig12/check_plant.py`**: PASS.
- **`note_numbers.py`**, run as a copy that writes to the scratchpad: it reproduces `notes/fig12/numbers.json` exactly.
- **`node notes/fig12/gate-ctl3.cjs`, then `python3 tools/fig12/gate_ctl3.py`**: PASS. Gains agree to 1.9 × 10⁻⁹, 860 iterations on the page, worst peak gap 0.1009 %.
- **Scratch scripts:**
  - `derive.py`: the SymPy derivations and the quadratures.
  - `acc.py`, `acc2.py`, `pos.py`: the Python cross-checks.
  - `pw/runs.cjs`, `pw/runs2.cjs`, `pw/acc.cjs`: the page runs in headless Chromium (Playwright).

  All are in `/tmp/claude-0/-home-user-SiteTest/0935aa8a-1d41-50fc-be37-f46e7857f37a/scratchpad/`.

No other file in the repository was changed.

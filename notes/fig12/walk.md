# Fig. 12 walkthrough check (furuta)

File checked: public/scripts/walk/furuta.js against public/simulations/furuta-pendulum.html.
Status: the walkthrough file was NOT edited (the lead did not say Numa allowed it). The fixes below are exact and ready to apply.

## Code lines
- `node notes/walkcheck.cjs`: furuta 33/33 found (all runs: 753/758; the 5 misses are in slit, tl and water, not Fig. 12).
- Stricter check (script): every one of the 33 quoted lines is a whole trimmed line of the page, character for character.
- `Sim.live()` returns t, n, ph, al, V, I, tau, E, Ep, G, r, J0, Jp, hc, rank, grow, slow, cin, Ly, err, bal, K, h, steps.
  Every syms key (r J0 Jp hc G V I tau ph al rank grow K slow Ep Ly cin bal err h steps) is among them.
  Every marked key in math and code has an entry in the same step's syms.
- Named functions and constants (derive, energy, rhs, accel, drive, linearise, rankOf, lqr, design, penEnergy, wrap, catchVolt, decide, measureC, stepRK4, run, solve; AMAX = 30, KPHI, KW, 1e-6, per = round(TS/h), TEND / H) exist and agree with the notes.

## Mismatches (equation numbers and symbols)

1. Step 1 (equations (2) and (3)): tags on the wrong formulas. In the note, (2) is T together with J0, Jp, h; (3) is U together with G.
   The walkthrough puts (2) after U and (3) after the J0, Jp, h, G line.
   old (math):
   `... + ½J<sub>p</sub>α̇², &nbsp; U = ⟦G|G⟧ ' + up('cos') + ' α' + tag(2) + '<br>J<sub>0</sub> = J<sub>r</sub> + m<sub>p</sub>⟦r|r⟧², &nbsp; J<sub>p</sub> = ⅓m<sub>p</sub>L², &nbsp; h = ½m<sub>p</sub>rL, &nbsp; G = ½m<sub>p</sub>gL' + tag(3)`
   new (math):
   `... + ½J<sub>p</sub>α̇²,<br>J<sub>0</sub> = J<sub>r</sub> + m<sub>p</sub>⟦r|r⟧², &nbsp; J<sub>p</sub> = ⅓m<sub>p</sub>L², &nbsp; h = ½m<sub>p</sub>rL' + tag(2) + '<br>U = ⟦G|G⟧ ' + up('cos') + ' α, &nbsp; G = ½m<sub>p</sub>gL' + tag(3)`

2. Step 8 (equations (18) and (19)): tag (18) is on the wrong formula. In the note, (18) is the Lyapunov rate
   𝒱̇_c = −ỹᵀ(Q + ρKᵀK)ỹ < 0; "V_m = −Kỹ" and "𝒱_c = ỹᵀPỹ" carry no number there.
   old (math): `... 𝒱<sub>c</sub> = ⟦Ly|ỹ<sup>T</sup>Pỹ⟧' + tag(18) + ...`
   new (math): `... 𝒱<sub>c</sub> = ⟦Ly|ỹ<sup>T</sup>Pỹ⟧, &nbsp; 𝒱̇<sub>c</sub> = −ỹ<sup>T</sup>(Q + ρK<sup>T</sup>K)ỹ < 0' + tag(18) + ...`

3. Step 8 (minor, symbol): the note names the upper level c_out = c in (19); the walkthrough writes plain c (the code has d.cout).
   old (math): `catch → swing-up when ỹ<sup>T</sup>Pỹ > c`
   new (math): `catch → swing-up when ỹ<sup>T</sup>Pỹ > c<sub>out</sub> = c`

## Checked and matching (no change)
- Step 2: (4) V_m = RI + Λİ + kφ̇, τ = kI; (6) τ = (k/R)(V_m − kφ̇); k, R, Λ, V_max as in the note.
- Step 3: (7) M, q̈, f and the matrix entries; code r1, r2 equal the rows of f.
- Step 4: (9) ỹ̇ = Aỹ + BV_m at (φ*, 0, 0, 0); (11) 𝒞 = [B, AB, A²B, A³B], rank 4.
- Step 5: (16), (17) with ρ; Q = diag(w_φ, w_α, 0.5, 2).
- Step 6: (12) E_p; (13) u with k_E, a_max, k_φ, k_ω.
- Step 7: (14) τ and V_m; code `add`, `tau`, `want` expand to the note's formula.
- Step 9: (20) and W_in, H_R, H_b; δt as the RK4 step; per, H, TEND as in the code.
- Intro: "Nine steps" matches the nine steps; "five times a second" matches setInterval(update, 200) in sim.js.

## Left out by the walkthrough (not mismatches)
Equations (1), (5), (8), (10), (15) have no step. The cost 𝒥 of (15) and the weights w_φ, w_α are named only in the step 5 note (w_φ, w_α there; 𝒥 not at all). Add a mention only if Numa wants them.

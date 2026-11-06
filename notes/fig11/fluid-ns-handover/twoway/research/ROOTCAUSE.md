# Root-cause study of the solved fluid's errors (project 05), 6 November 2026

The live page (section 13.6) states four errors. This file records what was measured to find their causes, what is
settled, what is ruled out, and what is still open. Scripts are in `notes/fig11/fluid-ns-handover/twoway/`, the literature
in `research/dossier-*.md` (three scouts). All numbers below were printed by the scripts named; nothing is estimated.

## 1. The rods feel too little drag (3–7 %, up to 13 % in slow honey): SETTLED

**Cause: self-induced (Oseen) velocity.** Each rod reads the water that its own force has already slowed, while the
drag law (33)–(34) is calibrated for the undisturbed stream. `t_disc.cjs` (rods held upright across a stream U, no cart):

| medium | U (m/s) | drag ÷ law | slowing at the rod ÷ U | k = slowing·2ρbU / f̄ |
|---|---|---|---|---|
| glycerol | 1.5 | 0.953 | 0.0156 | 0.460 |
| glycerol | 0.5 | 0.959 | 0.0201 | 0.446 |
| glycerol | 0.1 | 0.953 | 0.0344 | 0.314 |
| glycerol | 0.03 | 0.952 | 0.0405 | 0.136 |
| glycerol | 0.01 | 0.955 | 0.0404 | 0.048 |
| honey | 0.5 | 0.931 | 0.0440 | 0.451 |
| honey | 0.1 | 0.883 | 0.1029 | 0.289 |
| honey | 0.03 | 0.873 | 0.1179 | 0.106 |
| honey | 0.01 | 0.874 | 0.1187 | 0.036 |
| water | 0.5 | 0.967 | 0.0129 | 0.443 |
| glycerol, Δ/2 | 0.5 | 0.949 | 0.0230 | 0.516 |

Two regimes, both textbook 2D physics:
- **Fast (kernel Reynolds number Uσ/ν ≳ 5):** the rod acts as a 2D actuator disc; momentum theory gives the slowing at
  the disc f/(2ρbU). Measured: k ≈ 0.45 of it, the same within ±2 % from honey to water (a 7000-fold range of ν) and
  for U = 0.5 and 1.5 m/s. k < 1 because the rod is a finite segment (the water also goes round its ends) and the kernel
  spreads the force over 4 cells; k rises to 0.52 on cells half as large.
- **Slow (Stokes):** the slowing becomes a fixed fraction of U (0.040 glycerol, 0.118 honey). In 2D the Stokes response
  to a force grows like ln(ℓ/σ) (Stokes' paradox) and is cut off at the Oseen length ν/U. With σ = 2Δ = 5 cm,
  ln(ν/U ÷ σ)/4π predicts the honey/glycerol ratio 2.9 at U = 0.01; measured 2.8.

**Fix (not yet implemented):** remove the self-induced velocity before applying the law, u_∞ = u_read − u_self(f), as
the published 3D schemes do (Horwitz & Mani 2016; Esmaily & Horwitz 2018; Balachandar et al. 2019; dossier-selfinduced.md).
No published scheme is 2D. Two roads: (a) a 2D Oseen influence matrix M_ij for the Peskin kernel (the scout's
recommendation), iterated with the nonlinear law; (b) a one-line model joining the two measured regimes. Either must pass:
rod held across, along and at 45° to a stream, Δ and Δ/2, all three liquids, drag ÷ law = 1 ± 1 %, and a rod moving in
still water (an independent case, not used to build the correction).

## 2. The benchmark flow is weak by 5–12 %, and does not improve on finer grids: CAUSE NOT FOUND, narrowed

`t_st2.cjs`, Schäfer–Turek 2D-1 (Re 20). Flow quantities that need no force reading (published: La 0.0842–0.0852 m,
Δp 0.1172–0.1176 Pa, c_D 5.57–5.59):

| run | c_D on body | c_D control volume | La (m) | Δp (Pa) |
|---|---|---|---|---|
| 10 cells/D, Δt 10 ms | 5.118 | 5.341 | 0.0801 | 0.1033 |
| 20 cells/D | 5.212 | 5.324 | 0.0785 | 0.1041 |
| 39 cells/D, Δt 5 ms | 4.961 | 5.298 | 0.0777 | 0.1046 |
| 10 cells/D, Δt 5 ms | 5.106 | 5.311 | 0.0790 | 0.1041 |
| 10 cells/D, Δt 2.5 ms | 5.092 | 5.301 | 0.0785 | 0.1046 |
| 10 cells/D, run to 30 s instead of 12 s | 5.118 | 5.341 | 0.0801 | 0.1033 |
| central conservative advection (RK3) | 5.056 | 5.404 | 0.0801 | 0.1039 |
| no extrapolation into the body | 5.190 | 5.377 | 0.0806 | 0.1038 |
| incremental projection, 10 / 20 cells/D | 5.136 / 5.423 | 5.368 / 5.301 | 0.0770 / 0.0749 | 0.1068 / 0.1086 |
| particles traced with the weighted velocity w·u | 5.156 | 5.340 | 0.0801 | 0.1033 |

**Ruled out:** tracing with the weighted velocity; time to steady state; the advection scheme (two unrelated schemes agree); the extrapolation into the body;
the time splitting as the main cause (Δt/4 moves Δp by 1 %). The incremental projection moves Δp up by 3–4 % but La down
by 4–5 %, so it is not the fix.

**Shown to be right:** plane Poiseuille flow between walls that cut the cells at 0, 0.37 and 0.5 of a cell
(`t_cutchannel.cjs`): dp/dx within 0.14–0.21 %, profile within 0.1 % of U_max; so no-slip along a cut wall works.
A fixed cylinder in a gently oscillating stream (`t_oscstokes.cjs`, Re ≈ 1, KC ≈ 0.2), against the exact unsteady-Stokes
force ρπa²[2 + 4K₁(ka)/(ka K₀(ka))] dU/dt (Wolfram: 3.020 in phase, 1.249 in quadrature): 2 cells per radius −6.8 % and
−6.4 %, 4 cells per radius −4.1 % and −3.4 %: converging, first order. So the body's pressure and no-slip coupling are right
in the linear regime.

**Therefore** the error appears only when the flow is steady, nonlinear and strikes a curved body. Remaining hypotheses,
in the order they will be tested:
1. ~~The unweighted face velocities in cut cells~~ (advection traced with w·u: no change; ruled out).
2. The force/momentum ledger (scout R1): fluid and solid weights must sum to the cell volume at every face for Batty's
   force to be the exact momentum exchange; check by an identity test (body force = −Σ weighted momentum change of
   every substep).
3. Kim–Moin lagged-φ wall value for the intermediate velocity (dossier-projection-force.md), combined with the
   incremental form, which alone did not help.
4. ~~A finer run~~: 39 cells/D, Δt 5 ms gives La 0.0777, Δp 0.1046: the error does not shrink with the grid (row in the table).

## 3. A few per cent of momentum between body and water is not counted

c_D read on the body is 2–6 % below the control-volume value. Not yet separated from item 2; the identity test of 2.2
measures it directly.

## 4. The scheme loses 17 % of the energy in glycerol (80 % in water)

`t_book.cjs`, glycerol, the page's controller after a 4.6° / 2.9° tilt, 3 s:

| run | R (% of motor work) | advection step's loss (J) |
|---|---|---|
| base, fluid step 20 ms | 17.2 | 0.089 |
| central conservative advection | 15.5 | 0.071 |
| fluid step 5 ms | 12.5 | 0.092 |
| cells Δ/2 (earlier run) | 14.5 | 0.048 |

The advection scheme is a minor share; the time coupling gives about a third (R falls with Δt), and about 11 % does not
fall with Δt or Δ. **Suspected book-keeping cause (to verify):** velocities inside the cart that `impose()` overrides
during the viscous substeps change the water's kinetic energy; their momentum is credited to the cart, but their energy is
counted in E_diff and so lands in "viscous heat" or in R. Fix: book the energy of every override separately, as is
already done for its momentum. In water the loss is the cascade to eddies smaller than a cell; in 2D the energy cascade
runs to large scales and enstrophy to small ones (Boffetta & Ecke 2012, dossier-energy.md), so an explicit subgrid model
would be a regulariser to name in the book, not a physical dissipation.

## 5. Options added to `public/scripts/twoway.js` for these tests (all off by default; the page is unchanged)

`incremental` (pressure-correction form; its energy book is not valid, see above), `advCentral` (second-order central
advection, SSP-RK3), `noExtrap`, `measureSdf(sdf)` (any fixed body by its signed distance, for tests).

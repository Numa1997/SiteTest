# public/scripts/twoway.js

| | |
|---|---|
| File | [public/scripts/twoway.js](../../public/scripts/twoway.js), 424 lines, 57658 bytes |
| Loaded by | [simulations/double-inverted-pendulum.html](../../public/simulations/double-inverted-pendulum.html), after `dataset.js`, before the page's own script |
| Defines | `window.TwoWay` (`World`, `machinePar`, `Dmat`, `energy`, `momX`, `MEDIA`, `GLR`, `NP`, `phi4`, `pointKin`, cart and rod constants); in Node, `require` it and read `globalThis.TwoWay` |
| Used by | project 05's *The fluid: solved* (lecture-note section 13.6) and the test scripts in `notes/fig11/fluid-ns-handover/twoway/` |

The solved, two-way fluid of project 05 (Balancing Two Rods on a Cart), written 6 November 2026. CPU only, no libraries.

**The world.** A tank as deep as the cart (b = 0.2 m), 2D velocity field on a staggered (MAC) grid, incompressible
Navier–Stokes (lecture-note eq. 41). Per fluid step of `nsub · h` (page: 20 × 1 ms):
1. `measure()`: the fluid fraction of the control volume round every velocity sample, exact for the cart (an axis-aligned
   rectangle), and the signed distance to the cart at every face; Batty, Bertails & Bridson 2007, eq. (4).
2. `sampleAll()`: the water's velocity at the 2 × 24 Gauss points of the rods, Peskin's four-point kernel (Peskin 2002, eq. 6.27),
   and the water's acceleration there (∂u/∂t + (u·∇)u).
3. `spread()`: the rods' impulses of the previous step, with the opposite sign, into the water by the same kernel (in transit
   for one step); what lands on faces inside the cart goes to the cart.
4. `extrapolate()` + `advect()`: MacCormack transport with semi-Lagrangian steps, clamped; faces inside the cart are first filled
   with the neighbouring water's velocity so that transport reads water, not the body.
5. `diffuse()`: explicit viscosity, substepped; no slip at the cart's true surface by a ghost value through the wall
   (implicit in the wall link); returns the momentum the cart's shear gave the water.
6. Two pressure solves (multigrid-preconditioned CG, `Poisson`): p₀ for the water, p_x for the cart moving at 1 m/s.
   The cart's force is Q₀ + K_x ẋ′ (eq. 44).
7. `runMachine()`: the page's model (5)–(9) with buoyancy (37) and the rods' carried water (38), (40), by RK4 in steps of h; the
   cart carries m_a = −K_x Δt and the held force G = Q₀ + K_x ẋ₀ (eq. 45); the controller is called by `ctrl(s, t)` before each
   step, `onSub(s₀, s₁, t, u, W)` after it (the page logs every 1 ms step there). The rods' force per metre is (33)+(34)+(39) with
   the sampled velocity (eq. 42); their impulses are summed with RK4's weights.
8. `project()` with p₀ + ẋ′ p_x; only wholly solid faces are then overridden, so the field stays free of divergence.

**Books** (`book`): motor work `Wm`, the fluid's work on the machine `Wfl`, the rods' heat below the grid `Drod` (eq. 43), the
water's kinetic-energy change by operator (`Erod`, `Eadv`, `Ediff`, `Eproj`), the cart's shear work `Wshear`, the energy
brought in through the ends `Ebnd` (`boundaryPower()`). Diagnostics: `KE()`, `momX()`, `maxDiv()`, `vorticity()`, `velAt()`.
Test-only hooks: `frozen` (machine held, rods still push), `noRods`, `cartGone`, `geom` + `measureCircle()` / `measureSdf()`, `inflow`, `noslip`;
and, for the root-cause study of 6 November 2026 (`notes/fig11/fluid-ns-handover/twoway/research/ROOTCAUSE.md`), all off by default:
`incremental` (pressure-correction form, the old pressure before the viscous step; its energy book is not valid), `advCentral`
(second-order central advection in divergence form, SSP-RK3), `advWeighted` (trace with w·u), `noExtrap`.

**Checks** (scripts in `notes/fig11/fluid-ns-handover/twoway/`, results in lecture-note section 13.6): cart added mass against
potential flow (`t_addedmass.cjs`, `panel_addedmass.py`: −9.0, −3.9, −1.3 % at 4.8, 9.6, 19.2 cells per height); Poiseuille
(`t_poiseuille.cjs`, 0.34 %); Schäfer–Turek 2D-1 (`t_schaefer.cjs`, c_D 5.30–5.34 by momentum balance, 4.96–5.21 on the body,
band 5.57–5.59); rods held in a stream (`t_rodheld.cjs`, 0.93–0.97 of the law); energy books (`t_book.cjs`, `t_decomp.cjs`).
Open (7 November 2026): each rod also removes its own old wake (bounded at 1–3 % of the rods' force); semi-Lagrangian transport does not conserve momentum (about 1–2 % of a body's drag); the oscillating-cylinder test does not converge (2 % and 5.5 %).

**Changes of 7 November 2026** (session `claude/fluid-rootcause`; tests and numbers in `notes/fig11/fluid-ns-handover/twoway/fix/STATUS.md`,
the review with the deploying session in `fix/TO-MOTHER.md`):
- **The rods' self fields** (`selfField`, `selfPerRod`, both on by default): one extra field δu_k per rod, the same equations linearised
  about the flow, driven only by that rod's impulses (`shadowSpread`), cart at rest and no inflow in it, moved with the main field's own
  MacCormack points (`advectStored`), diffused (`shadowDiffuse`) and projected (`shadowProject`, tolerance `selfTol` 1e-2). The rods use
  u − δu_k for the law and for Du/Dt (39) (`uE`). Held and carried rods: each rod's force within 0.01–1.8 % of the same rod not pushing
  (uncorrected 4–21 %); the other rod's wake is kept. The rods' heat below the grid is booked as −f·(v − u_read).
- **Inlet**: where a stream enters (`inflow` or U ≠ 0), v = 0 on x = 0 in the viscous step and in the advection samplers (`vIn`); a still
  tank's left end stays a frictionless wall. This was the cause of the Schäfer–Turek benchmark not converging (`inletNeumann` restores the old).
- **The body's viscous force** is the ledger: what the viscous step changes in Σ w u, less the lid, floor and the tank's ends (`shearOld`
  restores the w-weighted wall flux, whose error does not shrink with the grid).
- **Books** (all in `book`): `Lproj` (kinetic energy removed by each projection), `Wimp`/`Eimp` and `PimpA/D/P` (overrides and extrapolation:
  the body's work at its own velocity, the water's kinetic energy and momentum change, by operator bucket), `Egeom` (re-weighting as the cart
  moves), `WcNP`, `WcP`, `WcPend` (the cart's work by non-pressure forces, by pressure as the machine feels it, and by pressure at the end
  velocity), `Padv/Pdiff/Pproj/Prod/PgeomEtc/Pshear/Pwall` (momentum by operator). The water's book closes to 1e-5 J (`fix/t_ledger.cjs`).
- **Speed**: pressure tolerance 1e-3; warm starts extrapolated from the last two solutions (`Poisson.solveX`, `extrap`); `measure()` limited
  to a window round the cart (bit-identical). With per-rod self fields a 20 ms fluid step costs about 30 ms in Chromium (slow motion, Numa's choice).
- **Test options**: `frozen` now holds the machine in every RK4 stage; `kinematic(t)` (prescribed path); `noPush`, `noPushRod`; `selfTau`
  (finite memory); `viscFV`, `shearUnw`, `solidCut` (rejected variants, kept for the record).


## The cart's size (7 November 2026)

`TwoWay.setCart(w, h, b)` sets the cart's length, height and depth (m), which are also the tank's depth; the page calls it once from its settings (`#dipc-page`, `cart`). Project 05 keeps its box, 0.36 × 0.12 × 0.2 m, the size every check in `notes/fig11/fluid-ns-handover/twoway/` was run with; project 06 ([rods-in-liquid.html](../../public/simulations/rods-in-liquid.html)) sets its carriage, 0.40 × 0.06 × 0.10 m. Since 7 November 2026 the solved fluid is offered on project 06 only; project 05 keeps the file loaded (the script is shared) with its menu hidden.

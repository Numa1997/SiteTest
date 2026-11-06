# public/scripts/twoway.js

| | |
|---|---|
| File | [public/scripts/twoway.js](../../public/scripts/twoway.js), 340 lines, 41054 bytes |
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
Test-only hooks: `frozen` (machine held, rods still push), `noRods`, `cartGone`, `geom` + `measureCircle()`, `inflow`, `noslip`.

**Checks** (scripts in `notes/fig11/fluid-ns-handover/twoway/`, results in lecture-note section 13.6): cart added mass against
potential flow (`t_addedmass.cjs`, `panel_addedmass.py`: −9.0, −3.9, −1.3 % at 4.8, 9.6, 19.2 cells per height); Poiseuille
(`t_poiseuille.cjs`, 0.34 %); Schäfer–Turek 2D-1 (`t_schaefer.cjs`, c_D 5.30–5.34 by momentum balance, 4.96–5.21 on the body,
band 5.57–5.59); rods held in a stream (`t_rodheld.cjs`, 0.93–0.97 of the law); energy books (`t_book.cjs`, `t_decomp.cjs`).
Known open problem: a few per cent of momentum between body and water that the direct force does not count.

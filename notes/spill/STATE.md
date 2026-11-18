# Continuous spill: one model for the stout inside and outside the glass (Fig. 12, Fig. 16)

Session: session_01DGmqioyaYR5VnnZaKfpEhD. Branch: `claude/continuous-spill` (from main). Reread first after a compaction.

## The owner's order (18 Nov 2026)
"Model it properly and have no discontinuities in your model." Today (tools/fig12/kaggle/stout_jax.py): inside the glass the stout is
incompressible Navier-Stokes (APIC particles on a staggered grid, free surface by level set, ghost-fluid p = 0); a particle that
crosses the rim outside the glass's radius stops being fluid and flies ballistically (lines 14-16, g2p ~705-725); the head's
spill becomes ballistic lumps (head_spill, 546-575); surface tension GAMMA is defined but not applied to the stout's surface.

## The change
1. The grid covers the cart's body top around the glass (BODY_HALF 0.11 x 0.06 m, BODY_TOP -14 mm) up to 20 mm above the rim.
2. The glass is a solid inside the grid: wall shell R(z)..R(z)+2.5 mm, foot down to -14 mm; the body top is a solid floor.
   Face open fractions = 1 - solid fraction; no-penetration on every solid face, as the cavity's wall today.
3. No particle ever changes its equations: over the rim it stays an APIC particle under the same pressure, viscosity and free
   surface, runs down the outside of the glass, lands on the deck and spreads. It leaves the computation only by falling off the
   deck's edge (the liquid leaves the cart: a physical event, booked as spilled mass).
4. Surface tension GAMMA = 0.0442 N/m on every free surface (ghost-fluid jump p = gamma kappa), inside and outside alike.
   Time step limit: dt < sqrt(rho dx^3 / (2 pi gamma)) = 3.5 ms at dx = 1.5 mm.
5. The head: stage 2. Today a sheet of thickness h_f on the cavity's columns; its spill must also stay one model.

## Cost (to state to the owner before any GPU run)
Cells today 57 x 57 x 113 = 0.37 M; with the deck around the glass about 147 x 80 x 125 = 1.47 M (4x). Pressure solve and
transfers scale about linearly to 1.5x; estimate 4-6x the GPU time of today's rides. CPU smoke tests on a coarse grid are free.

## Air (owner, 18 Nov: "fluid interacting with air ... look up spillage data")
Sources read: Xu, Zhang & Nagel, PRL 94, 184505 (2005), arXiv physics/0501149 (splash is caused by the surrounding gas; threshold
Sigma_G/Sigma_L = rho_G c_G sqrt(R V nu_L / 2) / sigma ~ 0.45); Sauret et al., Phys. Fluids 27, 022103 (2015), arXiv 1411.6542 (foam
damps sloshing by wall friction; few layers suffice); Kulczycki et al. arXiv 1311.7296 (high spot on the wall); Mayer & Krechetnikov
PRE 85, 046117 (2012) (abstract only, paywalled). Estimates for our ride (1.5 m/s, 16 cm fall, air 1.2 kg/m^3, 20 C):
- headwind drag on drops of 1-2 mm: Re 100-200, C_d 0.8-1.1 (Schiller-Naumann), a = 3/4 C_d rho_a U^2/(rho d) = 0.8-2 m/s^2: shifts
  the landing by up to ~3 cm. TO MODEL: drag of the relative wind on liquid exposed to it.
- aerodynamic breakup: We = rho_a U^2 d / gamma ~ 0.1 << 12: none.
- splash on the body: Sigma_G/Sigma_L ~ 0.40 (R 1 mm) to 0.56 (R 2 mm) at 1.8 m/s: at the threshold. TO MODEL: sub-grid rule.

## Smoke test 1 (continuous-spill-cpu v1, commit 214fd3d, dx 4 mm)
PASS old geometry unchanged; solids; wall area (1793 vs 1859 mm^2 per layer); shove: over the rim, down the outside, onto the body,
books close (50905 + 467 = 51372), vmax 3.9 m/s. FAIL at rest: surface read 23-28 mm (should be 125), 11 lost, 72 outside.
Diagnostic v2 (rest_diag.py, commit 7f139ca) running: old geometry vs continuous without / with surface tension.

## Status
- [ ] Geometry generalised (nx != ny, solid glass shell, deck), CPU smoke test on Kaggle (coarse dx).
- [ ] g2p: no ballistic switch; exit only off the deck. Books.
- [ ] Surface tension. Analytic checks: static drop (Laplace), capillary wave.
- [ ] Head stage 2.
- [ ] GPU runs (cost stated first), packing, pages, notes, merge, live.

## Published worked models to code (after the 2 mm rest and shove gates pass; agreed with the open-problems session)
1. Splash of a drop on a smooth dry solid: Riboux & Gordillo, PRL 113, 024507 (2014), arXiv 1401.6943v3 (read; erratum PRL 113,
   189901 to check). Ejection time t_e (dimensionless, units R, V, R/V) from  c1 Re^-1 t_e^-1/2 + Re^-2 Oh^-2 = c t_e^{3/2},
   c1 = sqrt(3)/2, c = 1.1 (eq. 1); sheet speed V_t = (sqrt(3)/2) V t_e^-1/2, sheet thickness H_t = 2.8 R sqrt(12/pi) t_e^{3/2};
   lift per length l = K_l mu_g V_t + K_u rho_g V_t^2 H_t, K_u ~ 0.3, K_l = -(6/tan^2 alpha)[ln(19.2 lambda/H_t) - ln(1 + 19.2 lambda/H_t)],
   lambda the gas's mean free path (68 nm in air at 1 atm), alpha the wedge angle (supplementary material: to read);
   splash when beta = sqrt(l / sigma) >= 0.14 (eq. 4; fits Xu et al. 2005 at all gases and pressures).
   Xu, Zhang & Nagel PRL 94, 184505 (2005), arXiv physics/0501149 (read): the measurements; Sigma_G/Sigma_L ~ 0.45 at threshold.
2. Drag on drops in the headwind: Schiller-Naumann C_D = 24/Re (1 + 0.15 Re^0.687), Re < 1000 (standard; to cite from Clift,
   Grace & Weber, "Bubbles, Drops, and Particles", 1978, which I have not yet read).
3. Splash on a wet deck: Cossali, Coghe & Marengo, Exp. Fluids 22, 463 (1997), K = We Oh^-0.4 ~ 2100 (from memory: TO READ).
4. Gas in the stout: Benilov, Cummins & Lee, arXiv 1205.5233 (downloaded): pub draught Guinness gas volume fraction f ~ 0.1 while
   settling (their measurement), canned ~ 0.05; after settling (~2 min) small. Dissolved CO2/N2: no measured Guinness value found
   (dispense gas 21-25 % CO2 / 75-79 % N2, sources disagree).
5. Wetting: glass is strongly wetted by aqueous liquids (static contact angle ~ 0 deg, beer-foam thesis core.ac.uk 30633103: TO READ);
   no measured stout-on-glass angle found yet.
6. Surface tension at 6 C: no stout measurement found; water dgamma/dT = -0.15 mN/m/K (standard) as the stand-in, stated as such.

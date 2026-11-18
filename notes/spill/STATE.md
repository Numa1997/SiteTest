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

## Status
- [ ] Geometry generalised (nx != ny, solid glass shell, deck), CPU smoke test on Kaggle (coarse dx).
- [ ] g2p: no ballistic switch; exit only off the deck. Books.
- [ ] Surface tension. Analytic checks: static drop (Laplace), capillary wave.
- [ ] Head stage 2.
- [ ] GPU runs (cost stated first), packing, pages, notes, merge, live.

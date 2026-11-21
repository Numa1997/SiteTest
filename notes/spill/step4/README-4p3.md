# Test 4.3 (plug flow of the foam head): the error, explained, and a documented limit

21 November 2026. Branch `claude/guinness-projection-fix`. Decision: the 4.3 error is explained well enough to move on; no more runs on it.

## What was measured (Fact)

The slab test (`tools/spill/step4_slab.py`): foam only, periodic 8 x 8 cells, no-slip floor, gravity tilted so the basal stress is
tau_b = 1.5 tau_y. Above the yield height the foam moves as a rigid plug; the exact plug speed follows from the flow law.

| set-up | plug speed | exact | error | file |
|---|---|---|---|---|
| h = 0.019 m, dx 1.5 mm, 0.5 s | 1.2953e-3 m/s | 1.4170e-3 | -8.6 % | `full_v2/slab_4.3_full_summary.json` |
| h = 0.019 m, dx 1.5 mm, steady (2 s) | 1.2842e-3 m/s | 1.4170e-3 | -9.4 % | `slab_4.3_T2s_full_summary.json` |
| h = 0.019 m, dx 0.75 mm, steady (2 s) | 1.5264e-3 m/s | 1.4170e-3 | +7.7 % | `slab_4.3_dx0.75mm_T2s_full_summary.json` |
| C1: h = 0.018 m, whole layers, dx 1.5 mm | 1.3490e-3 m/s | 1.3424e-3 | +0.49 % | `diag_4p3.json` |
| C2: h = 0.018 m, whole layers, dx 0.75 mm | 1.3668e-3 m/s | 1.3424e-3 | +1.81 % | `diag_4p3.json` |
| C3: h = 0.018 m, 1.6 tau_y, dx 1.5 mm | 2.1593e-3 m/s | 2.1454e-3 | +0.65 % | `diag_4p3.json` |

## The explanation (Inference, checked by the reviewer)

1. **The seed's layering (the big part).** The slab seed put round(h / (dx/2)) layers over h. At h = 0.019 m that is 25 layers at
   0.760 mm (dx 1.5 mm: 1.0133 cell volumes per sheared cell) or 51 at 0.3725 mm (dx 0.75 mm: 0.9935). The stress quadrature is then
   off by -1.33 % and +0.65 %. Near yield the plug speed amplifies stress errors: at tau_b = 1.5 tau_y, d ln v / d ln tau_b = 7.70. The
   predicted errors, about -10 % and +5 %, match the measured -9.4 % and +7.7 %. With whole layers (h = 0.018 m) they fall to +0.5 % and
   +1.8 %.
2. **Sampling the shear rate once per cell:** about -1.45 % at 1.5 mm and -0.36 % at 0.75 mm (shrinks with the grid).
3. **The 3-D neo-Hookean normal stresses:** a grid-independent offset. The von Mises invariant in simple shear is
   s = tau_xz [1 + (2/3)(tau_xz / G)^2], +0.16 % at the base; times the sensitivity 7.7, about +1.2 %.
4. What is left after 2 and 3, about +1 %, is about 0.14 % of the basal stress.

The C2 mark (error below 1 % and halving with the grid) was set from item 2 alone and left out item 3's offset: the mark was mis-set,
the physics is fine.

## The documented limit

- Plug speeds in the slab are right to within +0.5 % to +1.8 % once the seed's layers fill whole cells; the remainder does not shrink
  with the grid, because the normal-stress offset (item 3) is a property of the finite-strain model, not of the grid.
- The foam head of the pint is therefore seeded at exactly the lattice spacing (instruction "step4-seed-fix-gpu-smoke", Part 1):
  floor(HEAD0 / (dx/2)) full layers plus one thinner top layer whose particles carry the volume of that thinner slab. HEAD0 = 0.019 m
  stays the physical parameter at every grid (trimming the head to whole layers would make its height depend on dx and confound the
  resolution study of Step 6).
- **The head's wall ring (owner, 21 Nov, option 2):** the lattice keeps particles 0.25 hl inside the wall, so the thin strip between the
  outermost particles and the glass belongs to no particle at hl^3. Counting volume as the region nearest each particle, the ring of
  particles next to the wall carries that strip as well: in each layer the glass's volume minus the layer's particles at hl^2 t, shared
  equally by the ring (factor about 1.2-1.3). Interior cells stay exact, the head's total equals the glass's volume, and the cut cells
  at the wall, where the Cantat friction acts, hold the right foam volume. No vertical jitter for the head (sideways jitter kept).
- **Known offset of the stout, kept on purpose (corrected 21 Nov after the seed check):** the stout's seed (`stout_jax.seed_lattice`)
  rounds its layers, fill 0.125 m / 0.75 mm = 166.67 -> 167 layers at 0.7485 mm (0.9980 cell volumes per cell from the layering), and
  gives every particle the same volume V / N, which spreads the wall strip's 1 % over all particles: V / N = 1.0112 hl^2 hz, so interior
  stout cells hold 1.011 cell volumes on average, net +1.1 % (notes/spill/step4/seedcheck.json). Harmless for the stout: its pressure
  solve keeps the volume constant on the grid and never uses particle volumes. Steps 1-3 were validated with it; it stays.

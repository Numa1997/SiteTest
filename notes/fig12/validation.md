# Fig. 12 validation: the page's model against the full 3D solver

Written by `tools/fig12/validate-report.cjs` from `notes/fig12/runs/validate/` (runs of `tools/fig12/validate.cjs` on GitHub's runners,
`.github/workflows/fig12-validate.yml`). Each case is a random road of its regime, 3 s, the cart from 0.5 m at 0.8-1.2 m/s. The 3D solver
(half glass, 3 mm grid) against the page's model run as the 3D solver's twin (its frequencies times 0.958, the grid's; friction off,
the grid's damping 0.002): this tests the model's form; its physical frequencies and friction are tested elsewhere.

In plain words, per regime: how far the size of the swing over time (its envelope) differs, how far the largest lean differs, how far
the cart's speed differs, and the spilled stout.

## fills (50 roads)

- 1 of 50 roads keep the 3D swing under 5 mm and are not judged; on them the largest leans are 5.0 mm (3D) and 8.2 mm (model) typically.
- The swing's size over time differs by 25 % typically and by 104 % at worst (road 19), over the windows where the 3D swing exceeds 3 mm. Tolerance: 30 % typical, 80 % worst.
- The largest lean differs by 15 % typically and by 139 % at worst (road 19: 3D 5.7 mm, model 13.5 mm); the model's is the lower in 23 of 49. Tolerance: 25 % typical, 60 % worst.
- The cart's speed differs by 0.20 mm/s rms typically: the stout's push on the cart is the same in both.
- Spilled: 34 g in the 3D runs, 60 g in the model's, over all 50 roads (reported, not judged: see below).

## gentle (50 roads)

- 28 of 50 roads keep the 3D swing under 5 mm and are not judged; on them the largest leans are 3.3 mm (3D) and 4.1 mm (model) typically.
- The swing's size over time differs by 37 % typically and by 111 % at worst (road 23), over the windows where the 3D swing exceeds 3 mm. Tolerance: 30 % typical, 80 % worst.
- The largest lean differs by 19 % typically and by 124 % at worst (road 23: 3D 6.4 mm, model 14.3 mm); the model's is the lower in 9 of 22. Tolerance: 25 % typical, 60 % worst.
- The cart's speed differs by 0.05 mm/s rms typically: the stout's push on the cart is the same in both.
- Spilled: 0 g in the 3D runs, 0 g in the model's, over all 50 roads (reported, not judged: see below).

## spilling (50 roads)

- Every road is judged.
- The swing's size over time differs by 26 % typically and by 44 % at worst (road 8), over the windows where the 3D swing exceeds 3 mm. Tolerance: 30 % typical, 80 % worst.
- The largest lean differs by 22 % typically and by 45 % at worst (road 8: 3D 15 mm, model 21.8 mm); the model's is the lower in 36 of 50. Tolerance: 40 % typical, 70 % worst.
- The cart's speed differs by 0.87 mm/s rms typically: the stout's push on the cart is the same in both.
- Spilled: 917 g in the 3D runs, 1079 g in the model's, over all 50 roads (reported, not judged: see below).

## vertical (50 roads)

- 4 of 50 roads keep the 3D swing under 5 mm and are not judged; on them the largest leans are 4.4 mm (3D) and 6.3 mm (model) typically.
- The swing's size over time differs by 28 % typically and by 122 % at worst (road 50), over the windows where the 3D swing exceeds 3 mm. Tolerance: 30 % typical, 80 % worst.
- The largest lean differs by 24 % typically and by 96 % at worst (road 50: 3D 5.5 mm, model 10.8 mm); the model's is the lower in 25 of 46. Tolerance: 25 % typical, 60 % worst.
- The cart's speed differs by 0.20 mm/s rms typically: the stout's push on the cart is the same in both.
- Spilled: 232 g in the 3D runs, 437 g in the model's, over all 50 roads (reported, not judged: see below).

## violent (50 roads)

- Every road is judged.
- The swing's size over time differs by 25 % typically and by 43 % at worst (road 41), over the windows where the 3D swing exceeds 3 mm. Tolerance: 30 % typical, 80 % worst.
- The largest lean differs by 28 % typically and by 51 % at worst (road 46: 3D 93.4 mm, model 46 mm); the model's is the lower in 44 of 50. Tolerance: 40 % typical, 70 % worst.
- The cart's speed differs by 0.99 mm/s rms typically: the stout's push on the cart is the same in both.
- Spilled: 394 g in the 3D runs, 851 g in the model's, over all 50 roads (reported, not judged: see below).

## Spilled stout

The pour is reported, not judged. On single hard pushes, where the 3 and 4 mm grids agree within 5 %, the model spills 5-23 % less than the 3D solver (tools/fig12/spill-fit.cjs). On roads that only just lift the crest over the rim the model pours more than the 3D solver, up to about twice at 125 mm fill: an overflow thinner than one cell (3-4 mm) can hardly leave the 3D grid, so which is nearer a real glass there is not settled by these runs.

## History

The first runs used the 4 mm grid. It fails the exact steady tilt (a held push tilts the surface into the plane 2 R(h) a/g in any glass) by up to 46 % on the flared wall, the 3 mm grid by 5-6 % at 75-125 mm and 13-23 % at 140 mm (tools/fig12/tilt-exact.cjs); since then the reference is the 3 mm grid.

First run (workflow run 43052998146, 11 November 2026, 4 mm grid), every case judged: FAILED in fills (envelope median 33 %, worst 212 %; largest lean worst 137 %, a 4.3 mm swing), gentle (envelope median 51 %, worst 81 %) and vertical (envelope worst 130 %, largest lean worst 66 %). The resolution floor above was then added, with the site owner’s agreement.

**Result: FAILED** — fills: envelope worst 104 %; fills: peak worst 139 %; gentle: envelope median 37 %; gentle: envelope worst 111 %; gentle: peak worst 124 %; vertical: envelope worst 122 %; vertical: peak worst 96 %

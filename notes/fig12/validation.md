# Fig. 12 validation: the page's model against the full 3D solver

Written by `tools/fig12/validate-report.cjs` from `notes/fig12/runs/validate/` (runs of `tools/fig12/validate.cjs` on GitHub's runners,
`.github/workflows/fig12-validate.yml`). Each case is a random road of its regime, 3 s, the cart from 0.5 m at 0.8-1.2 m/s. The 3D solver
(half glass, 4 mm grid) against the page's model run as the 3D solver's twin (its frequencies times 0.943, the grid's; friction off,
the grid's damping 0.004): this tests the model's form; its physical frequencies and friction are tested elsewhere.

In plain words, per regime: how far the size of the swing over time (its envelope) differs, how far the largest lean differs, how far
the cart's speed differs, and the spilled stout.

## fills (50 roads)

- The swing's size over time differs by 33 % typically and by 212 % at worst (road 25). Tolerance: 30 % typical, 80 % worst.
- The largest lean differs by 18 % typically and by 137 % at worst (road 25: 3D 4.3 mm, model 10.1 mm); the model's is the lower in 12 of 50. Tolerance: 25 % typical, 60 % worst.
- The cart's speed differs by 0.21 mm/s rms typically: the stout's push on the cart is the same in both.
- Spilled: 37 g in the 3D runs, 55 g in the model's, over all 50 roads.

## gentle (50 roads)

- The swing's size over time differs by 51 % typically and by 81 % at worst (road 17). Tolerance: 30 % typical, 80 % worst.
- The largest lean differs by 12 % typically and by 42 % at worst (road 4: 3D 2.2 mm, model 1.3 mm); the model's is the lower in 20 of 50. Tolerance: 25 % typical, 60 % worst.
- The cart's speed differs by 0.08 mm/s rms typically: the stout's push on the cart is the same in both.
- Spilled: 0 g in the 3D runs, 0 g in the model's, over all 50 roads.

## spilling (50 roads)

- The swing's size over time differs by 27 % typically and by 43 % at worst (road 30). Tolerance: 30 % typical, 80 % worst.
- The largest lean differs by 27 % typically and by 41 % at worst (road 13: 3D 61 mm, model 36.2 mm); the model's is the lower in 44 of 50. Tolerance: 40 % typical, 70 % worst.
- The cart's speed differs by 1.10 mm/s rms typically: the stout's push on the cart is the same in both.
- Spilled: 961 g in the 3D runs, 1101 g in the model's, over all 50 roads.

## vertical (50 roads)

- The swing's size over time differs by 24 % typically and by 130 % at worst (road 2). Tolerance: 30 % typical, 80 % worst.
- The largest lean differs by 16 % typically and by 66 % at worst (road 2: 3D 14.6 mm, model 24.3 mm); the model's is the lower in 25 of 50. Tolerance: 25 % typical, 60 % worst.
- The cart's speed differs by 0.28 mm/s rms typically: the stout's push on the cart is the same in both.
- Spilled: 225 g in the 3D runs, 431 g in the model's, over all 50 roads.

## violent (50 roads)

- The swing's size over time differs by 18 % typically and by 40 % at worst (road 24). Tolerance: 30 % typical, 80 % worst.
- The largest lean differs by 18 % typically and by 37 % at worst (road 1: 3D 78.7 mm, model 49.6 mm); the model's is the lower in 38 of 50. Tolerance: 40 % typical, 70 % worst.
- The cart's speed differs by 0.89 mm/s rms typically: the stout's push on the cart is the same in both.
- Spilled: 454 g in the 3D runs, 807 g in the model's, over all 50 roads.

**Result: FAILED** — fills: envelope median 33 %; fills: envelope worst 212 %; fills: peak worst 137 %; gentle: envelope median 51 %; gentle: envelope worst 81 %; vertical: envelope worst 130 %; vertical: peak worst 66 %

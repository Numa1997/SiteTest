"""Fig. 2, the double pendulum, in full: every start of the page's sliders on the grid of tools/sims/dp_engine.py (5 mass ratios x
5 length ratios x both angles every 15 degrees x both starting angular velocities at -5, -2.5, 0, 2.5, 5 rad/s = 360 000 starts,
each with its chaos twin, 20 s each), computed on Kaggle's GPU with the page's own method (RK4, h = 1/600 s, 64-bit numbers).
The equations, the file format and the checks are described in dp_engine.py. Output: 25 packs dp_<i><j>.pack (one per mass-length
cell; stored in the GitHub release sims-double_pendulum_gpu-<date>, docs/kaggle-sims.md "Large data") and double_pendulum.json
(the grid, every runs file with its pack, offset, size and SHA-256, and the checks)."""
import dp_engine

def run(out_dir):
    return dp_engine.run(out_dir)

"""Engine test for GPU runs with large data (docs/kaggle-sims.md, "Large data"): the same code as the full double pendulum
(tools/sims/dp_engine.py), on a small part of its grid: the default cell (equal masses and rods), theta1 = 120 degrees,
omega1 = 0 and 2.5 rad/s, every theta2 and omega2: 240 starts with their twins, one pack. It sends one GPU run through every new
step of the engine (GPU notebook, release, landing on main, the Worker's /rel/ path) before the full run spends hours."""
import dp_engine

def run(out_dir):
    return dp_engine.run(out_dir, smoke=True)

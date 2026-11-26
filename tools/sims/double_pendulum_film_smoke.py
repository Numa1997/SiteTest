"""Fig. 2 flip-time films, the small test run before the full ones (registry "manual": computed only by Run workflow). The code
of tools/sims/dp_film.py on 72 x 72 starts (every 5 degrees) at 8 points of the closed curve "push", plus a timing of the same
kernel on Kaggle's CPU and GPU (header "bench"), so the full runs' time and machine come from a measurement."""
import dp_film

def run(out_dir):
    return dp_film.run(out_dir, n=72, curve="push", frames=8, bench_cpu=True, model="double_pendulum_film_smoke")

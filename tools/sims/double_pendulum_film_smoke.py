"""Fig. 2 flip-time film, the small test run before the full one (registry "manual": computed only by Run workflow). The code
of tools/sims/dp_film.py on 72 x 72 starts (every 5 degrees) and 9 masses (ln(m_2/m_1) = -2.3 ... 2.3 in steps of 0.575), plus a
timing of the same kernel on Kaggle's CPU and GPU (header "bench"), so the full run's time and machine come from a measurement."""
import dp_film

def run(out_dir):
    return dp_film.run(out_dir, n=72, ln_m0=-2.3, dln_m=0.575, frames=9, bench_cpu=True, model="double_pendulum_film_smoke")

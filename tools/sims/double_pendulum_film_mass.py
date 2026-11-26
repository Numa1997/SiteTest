"""Fig. 2, the double pendulum: the flip-time film along the curve "mass" (Sand pours into the lower bob: ln(m2/m1) = -2.3 + 4.6 u; l2 = l1; from rest).
tools/sims/dp_film.py has the equations, the curves, the method, the file format and the checks. 720 x 720 starts (theta_1,
theta_2 every half degree), each followed for 10 s with the page's own RK4 (h = 1/600 s, 64-bit), at 240 points of the curve.
Stored in Cloudflare R2: 240 maps of 1 036 800 bytes, film.mp4, poster.png, film.json. Started only by Run workflow."""
import dp_film

def run(out_dir):
    return dp_film.run(out_dir, n=720, curve="mass", frames=240, model="double_pendulum_film_mass")

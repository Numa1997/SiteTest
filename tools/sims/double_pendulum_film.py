"""Fig. 2, the double pendulum: the flip-time film in full (tools/sims/dp_film.py has the equations, the method, the file format
and the checks). 720 x 720 starts released from rest (theta_1, theta_2 every half degree; every even pixel is a start the page's
1-degree sliders reach), followed for 10 s with the page's own RK4 (h = 1/600 s, 64-bit), for 369 lower masses with
ln(m_2/m_1) = -2.3 ... 2.3 in steps of 0.0125 (every fourth frame is a step of the page's mass slider). Stored in Cloudflare R2:
369 maps of 1 036 800 bytes, film.mp4, poster.png and film.json (docs/kaggle-sims.md, "The data in Cloudflare R2")."""
import dp_film

def run(out_dir):
    return dp_film.run(out_dir, n=720, ln_m0=-2.3, dln_m=0.0125, frames=369, model="double_pendulum_film")

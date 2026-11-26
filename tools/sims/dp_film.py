"""Fig. 2, the double pendulum: the flip-time film, computed once on Kaggle's GPU (notes/sims/chaos-and-storage.md).

Why a film. The double pendulum is chaotic: two starts d_0 apart separate as d_0 exp(lambda t), lambda about 1.4 per second, so
no start can be made from its stored neighbours and storing every start the sliders reach is impossible (8e12 starts, 157 PB).
The user's rule of 26 November 2026: Kaggle computes the interesting map over the parameters and records it as a film; the page
shows the film beside the live simulation, which the visitor's browser still computes.

The map. Each pixel is one start released from rest, theta_1 along x and theta_2 along y, both from -180 to +180 degrees. Its value
is the first time either rod passes over the top (|theta_1| > pi or |theta_2| > pi, angles followed continuously from the start),
looked for during T_MAX seconds. The film sweeps the lower mass: frame f has ln(m_2/m_1) = LN_M0 + f * DLN_M, from 0.1 to 9.97.

The setup and its equations, exactly the page's (public/simulations/Double Pendulum.html, deriv() and rk4()). Massless rods of
lengths l_1, l_2, point masses m_1, m_2, gravity g, no friction; theta from the downward vertical, counter-clockwise positive;
delta = theta_1 - theta_2:

    D      = 2 m_1 + m_2 - m_2 cos(2 delta)                                                                     [kg]
    alpha_1 = [-g (2 m_1 + m_2) sin theta_1 - m_2 g sin(theta_1 - 2 theta_2)
               - 2 sin(delta) m_2 (omega_2^2 l_2 + omega_1^2 l_1 cos delta)] / (l_1 D)                           [rad/s^2]
    alpha_2 = 2 sin(delta) [omega_1^2 l_1 (m_1 + m_2) + g (m_1 + m_2) cos theta_1 + omega_2^2 l_2 m_2 cos delta] / (l_2 D)

Energy E = T + V with V = -(m_1 + m_2) g l_1 cos theta_1 - m_2 g l_2 cos theta_2 is conserved. Released from rest, E = V(start).
Rod 2 can pass the top only if E >= V_2* = -(m_1 + m_2) g l_1 + m_2 g l_2 (the least V with theta_2 = pi), rod 1 only if
E >= V_1* = (m_1 + m_2) g l_1 - m_2 g l_2 (the least V with theta_1 = pi). A start below both can never flip: a check.

Method: the page's RK4 with the fixed step H = 1/600 s in 64-bit numbers (JAX on the GPU, jit, fori_loop), all N x N starts of a
frame at once. The flip is looked for after every step, so a stored flip time is an exact whole number of steps.

Output (out_dir):
    map_<fff>.bin   frame fff (three digits): N x N little-endian uint16, row a = theta_2 index, column b = theta_1 index,
                    theta = -180 + 360 * index / N degrees. Value k in 1..K_MAX: the first flip came at step k, t = k H.
                    NEVER (65535): no flip within T_MAX. FAILED (65534): the numbers stopped being finite before any flip.
    film.mp4        the maps as colour (H.264, yuv420p, FPS frames a second, a key frame every second), image row 0 = theta_2 at
                    the top (+180 - step), column 0 = theta_1 = -180. Colour of a value: see colour() and the table in film.json.
    poster.png      the frame with m_2 = m_1, lossless.
    film.json       parameters, grid, frames, colour table, every check, timings.
run(out_dir) returns the header with "checks_passed"; with a failed check the engine stores nothing (docs/kaggle-sims.md)."""
import hashlib, json, math, os, subprocess, sys, time
import numpy as np

G, M1, L1, L2 = 9.81, 1.0, 1.0, 1.0        # m/s^2, kg, m, m (the page's g, m_1, l_1; the length ratio is 1, its default)
H = 1 / 600                                # s, the page's RK4 step
T_MAX = 10.0                               # s, how long each start is followed
K_MAX = int(round(T_MAX / H))              # 6000 steps
NEVER, FAILED = 65535, 65534
FPS = 30                                   # film frames per second
T_LO = 0.05                                # s, flip time at the light end of the colour scale (log scale up to T_MAX)
STOPS = [(0.0, (246, 241, 231)), (0.35, (217, 164, 65)), (0.7, (122, 31, 43)), (1.0, (46, 18, 24))]   # cream, ochre, wine, dark
C_NEVER, C_FAILED = (16, 20, 26), (128, 128, 128)

def log(*a): print(time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a), flush=True)

def lut():
    """256 colours along the log time scale: index q = round(255 u), u = ln(t / T_LO) / ln(T_MAX / T_LO), clipped to 0..1."""
    out = []
    for q in range(256):
        u = q / 255
        for (u0, c0), (u1, c1) in zip(STOPS, STOPS[1:]):
            if u <= u1:
                w = (u - u0) / (u1 - u0); out.append([int(round(c0[i] + w * (c1[i] - c0[i]))) for i in range(3)]); break
    return np.array(out, dtype=np.uint8)

LUT = lut()

def colour_index(k):
    """k: uint16 map values. Returns the LUT index (0..255) for flips, 256 for NEVER, 257 for FAILED."""
    k = np.asarray(k); t = np.maximum(k.astype(np.float64), 1) * H
    q = np.rint(255 * np.clip(np.log(t / T_LO) / math.log(T_MAX / T_LO), 0, 1)).astype(np.int32)
    return np.where(k == NEVER, 256, np.where(k == FAILED, 257, q))

def colour(k):
    pal = np.concatenate([LUT, np.array([C_NEVER, C_FAILED], dtype=np.uint8)])
    return pal[colour_index(k)]

def grid(n):
    """rad; index i is the angle -180 + 360 i / n degrees, converted exactly as the page converts its slider (deg * pi / 180),
    so a start the page's sliders reach has the same 64-bit angle here and there."""
    deg = -180.0 + 360.0 * np.arange(n) / n
    return deg * math.pi / 180

def energy0(t1, t2, m2):
    return -(M1 + m2) * G * L1 * np.cos(t1) - m2 * G * L2 * np.cos(t2)

# ---- the GPU kernel ----
def make_jax():
    """JAX in 64-bit on the GPU; installs the CUDA build if the image's JAX does not see the GPU (as tools/sims/dp_engine.py)."""
    probe = [sys.executable, "-c", "import jax; print(jax.default_backend())"]
    if subprocess.run(probe, capture_output=True, text=True).stdout.strip() != "gpu":
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "jax[cuda12]"], check=True)
        if subprocess.run(probe, capture_output=True, text=True).stdout.strip() != "gpu": raise SystemExit("no GPU seen by JAX: stopping before any computing")
    import jax, jax.numpy as jnp
    jax.config.update("jax_enable_x64", True)

    def deriv(s, m2, l2):
        t1, t2, o1, o2 = s[0], s[1], s[2], s[3]; d = t1 - t2; den = 2 * M1 + m2 - m2 * jnp.cos(2 * d)
        a1 = (-G * (2 * M1 + m2) * jnp.sin(t1) - m2 * G * jnp.sin(t1 - 2 * t2) - 2 * jnp.sin(d) * m2 * (o2 * o2 * l2 + o1 * o1 * L1 * jnp.cos(d))) / (L1 * den)
        a2 = (2 * jnp.sin(d) * (o1 * o1 * L1 * (M1 + m2) + G * (M1 + m2) * jnp.cos(t1) + o2 * o2 * l2 * m2 * jnp.cos(d))) / (l2 * den)
        return jnp.stack([o1, o2, a1, a2])

    def flipmap(t1, t2, m2, h, nsteps):
        s0 = jnp.stack([t1, t2, jnp.zeros_like(t1), jnp.zeros_like(t1)])
        f0 = jnp.full(t1.shape, NEVER, dtype=jnp.int32)
        def body(k, c):
            s, f = c
            k1 = deriv(s, m2, L2); k2 = deriv(s + h / 2 * k1, m2, L2); k3 = deriv(s + h / 2 * k2, m2, L2); k4 = deriv(s + h * k3, m2, L2)
            s = s + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            fin = jnp.all(jnp.isfinite(s), axis=0)
            hit = (jnp.abs(s[0]) > jnp.pi) | (jnp.abs(s[1]) > jnp.pi)
            f = jnp.where((f == NEVER) & ~fin, FAILED, f)
            f = jnp.where((f == NEVER) & fin & hit, k + 1, f)
            return s, f
        return jax.lax.fori_loop(0, nsteps, body, (s0, f0))[1]

    return jax, jax.jit(flipmap, static_argnums=(4,))

def page_rk4_flip(t1, t2, m2, h=H, nsteps=K_MAX):
    """A plain copy of the page's deriv() and rk4(), one start, in Python floats; returns the flip step as the map stores it."""
    def deriv(s):
        a, b, o1, o2 = s; d = a - b; den = 2 * M1 + m2 - m2 * math.cos(2 * d)
        a1 = (-G * (2 * M1 + m2) * math.sin(a) - m2 * G * math.sin(a - 2 * b) - 2 * math.sin(d) * m2 * (o2 * o2 * L2 + o1 * o1 * L1 * math.cos(d))) / (L1 * den)
        a2 = (2 * math.sin(d) * (o1 * o1 * L1 * (M1 + m2) + G * (M1 + m2) * math.cos(a) + o2 * o2 * L2 * m2 * math.cos(d))) / (L2 * den)
        return [o1, o2, a1, a2]
    s = [t1, t2, 0.0, 0.0]
    for k in range(nsteps):
        k1 = deriv(s); s2 = [s[i] + h / 2 * k1[i] for i in range(4)]; k2 = deriv(s2); s3 = [s[i] + h / 2 * k2[i] for i in range(4)]
        k3 = deriv(s3); s4 = [s[i] + h * k3[i] for i in range(4)]; k4 = deriv(s4)
        s = [s[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4)]
        if not all(math.isfinite(x) for x in s): return FAILED
        if abs(s[0]) > math.pi or abs(s[1]) > math.pi: return k + 1
    return NEVER

def ffmpeg_exe():
    try:
        import imageio_ffmpeg
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "imageio-ffmpeg"], check=False)
        try: import imageio_ffmpeg
        except ImportError: imageio_ffmpeg = None
    if imageio_ffmpeg is not None: return imageio_ffmpeg.get_ffmpeg_exe()
    from shutil import which
    if which("ffmpeg"): return "ffmpeg"
    raise SystemExit("no ffmpeg: cannot make the film")

def image(m):
    """A map (row = theta_2 index, column = theta_1 index) as an RGB image with theta_2 increasing upwards."""
    return colour(m)[::-1]

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""): h.update(c)
    return h.hexdigest()

def run(out, n=720, ln_m0=-2.3, dln_m=0.0125, frames=369, bench_cpu=False, model="double_pendulum_film"):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    jax, flipmap = make_jax(); import jax.numpy as jnp
    log("devices", jax.devices(), "grid", n, "x", n, "frames", frames)
    th = grid(n); T1, T2 = np.meshgrid(th, th)                 # T1[a, b] = th[b] (column), T2[a, b] = th[a] (row)
    t1d, t2d = jnp.asarray(T1.ravel()), jnp.asarray(T2.ravel())
    lnm = [round(ln_m0 + f * dln_m, 10) for f in range(frames)]
    ck, bench = {}, {}
    # compile once, then time one frame per device
    tg = time.time(); flipmap(t1d, t2d, 1.0, H, K_MAX).block_until_ready(); bench["gpu_first_frame_s_incl_compile"] = time.time() - tg
    if bench_cpu:
        try:
            cpu = jax.devices("cpu")[0]; nb = 64; tb = grid(nb); A, B = np.meshgrid(tb, tb)
            with jax.default_device(cpu):
                a, b = jnp.asarray(A.ravel()), jnp.asarray(B.ravel()); flipmap(a, b, 1.0, H, K_MAX).block_until_ready()
                tc = time.time(); flipmap(a, b, 1.0, H, K_MAX).block_until_ready(); bench["cpu_s_per_start_step"] = (time.time() - tc) / (nb * nb * K_MAX)
            a, b = jnp.asarray(A.ravel()), jnp.asarray(B.ravel()); flipmap(a, b, 1.0, H, K_MAX).block_until_ready()
            tc = time.time(); flipmap(a, b, 1.0, H, K_MAX).block_until_ready(); bench["gpu_s_per_start_step_64x64"] = (time.time() - tc) / (nb * nb * K_MAX)
        except Exception as e:
            bench["cpu_error"] = repr(e)
    maps, frame_info, gpu_s = {}, [], 0.0
    for f, lm in enumerate(lnm):
        m2 = M1 * math.exp(lm); tg = time.time()
        M = np.asarray(flipmap(t1d, t2d, m2, H, K_MAX)).reshape(n, n).astype(np.uint16); dt = time.time() - tg; gpu_s += dt
        name = "map_%03d.bin" % f; M.astype("<u2").tofile(os.path.join(out, name)); maps[f] = M
        E = energy0(T1, T2, m2); thr = min((M1 + m2) * G * L1 - m2 * G * L2, -(M1 + m2) * G * L1 + m2 * G * L2)
        S = (M1 + m2) * G * L1 + m2 * G * L2
        bad = int(((E < thr - 1e-6 * S) & (M < FAILED)).sum())
        frame_info.append(dict(f=f, file=name, ln_m=lm, m2=m2, flipped=int((M < FAILED).sum()), never=int((M == NEVER).sum()),
                               failed=int((M == FAILED).sum()), energy_forbidden_flips=bad, gpu_s=round(dt, 3)))
        if f % 10 == 0 or f == frames - 1:
            left = (time.time() - t0) / (f + 1) * (frames - f - 1)
            log(f"frame {f + 1}/{frames}  m2/m1={m2:.4f}  {dt:.2f} s  so far {time.time() - t0:.0f} s  expected rest {left:.0f} s")
    bench["gpu_s_per_frame_mean"] = gpu_s / frames; bench["gpu_s_per_start_step"] = gpu_s / (frames * n * n * K_MAX)
    # ---- checks ----
    ck["energy_forbidden_flips"] = dict(value=sum(x["energy_forbidden_flips"] for x in frame_info), must_be=0,
                                        what="starts with E below both flip thresholds V_1*, V_2* that flipped anyway")
    sym = []
    for f in (0, frames // 2, frames - 1):
        M = maps[f][1:, 1:]; sym.append(float((M == M[::-1, ::-1]).mean()))
    ck["mirror_symmetry"] = dict(value=min(sym), at_least=0.98, frames=[0, frames // 2, frames - 1], per_frame=sym,
                                 what="share of pixels equal to the pixel at (-theta_1, -theta_2): the equations are odd under theta -> -theta")
    rng = np.random.default_rng(0); same, diffs = 0, []
    picks = [(f, int(rng.integers(n)), int(rng.integers(n))) for f in (0, frames // 2, frames - 1) for _ in range(16)]
    tp = time.time()
    for f, a, b in picks:
        k = page_rk4_flip(th[b], th[a], M1 * math.exp(lnm[f])); s = int(maps[f][a, b]); same += (k == s)
        if k < FAILED and s < FAILED: diffs.append(abs(k - s))
    ck["gpu_vs_page_rk4"] = dict(value=same / len(picks), at_least=0.75, starts=len(picks), median_step_diff=float(np.median(diffs)) if diffs else None,
                                 what="share of 48 random pixels whose stored flip step equals a plain Python copy of the page's RK4", seconds=round(time.time() - tp, 1))
    fh = next(f for f, lm in enumerate(lnm) if abs(lm) < 1e-9) if any(abs(lm) < 1e-9 for lm in lnm) else frames // 2
    sub = slice(0, n, 8); a2, b2 = jnp.asarray(T1[sub, sub].ravel()), jnp.asarray(T2[sub, sub].ravel())
    Mh = np.asarray(flipmap(a2, b2, M1 * math.exp(lnm[fh]), H / 2, 2 * K_MAX)).reshape(T1[sub, sub].shape)
    Mf = maps[fh][sub, sub].astype(np.int64); fl1, fl2 = Mf < FAILED, Mh < FAILED
    tdiff = np.abs(Mf * H - Mh * (H / 2))[fl1 & fl2]
    ck["step_halving"] = dict(value=float((fl1 == fl2).mean()), at_least=0.8, frame=fh, pixels=int(fl1.size),
                              within_0_05_s=float((tdiff < 0.05).mean()) if tdiff.size else None, median_diff_s=float(np.median(tdiff)) if tdiff.size else None,
                              what="share of every 8th pixel whose flips-or-not within T_MAX agrees at h/2 (the chaotic boundary is fractal, so not all can)")
    # ---- the film ----
    exe = ffmpeg_exe(); vid = os.path.join(out, "film.mp4")
    cmd = [exe, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{n}x{n}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "12", "-preset", "slow", "-g", str(FPS), "-movflags", "+faststart", vid]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(frames): p.stdin.write(image(maps[f]).tobytes())
    p.stdin.close(); assert p.wait() == 0, "ffmpeg failed"
    dec = subprocess.run([exe, "-loglevel", "error", "-i", vid, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    D = np.frombuffer(dec, np.uint8).reshape(-1, n, n, 3)
    means, p99s = [], []
    for f in range(min(len(D), frames)):
        e = np.abs(D[f].astype(np.int16) - image(maps[f]).astype(np.int16)); means.append(float(e.mean())); p99s.append(float(np.percentile(e.max(-1), 99)))
    del D
    ck["film_vs_map"] = dict(frames_decoded=len(means), must_be=frames, mean_abs_rgb=float(np.mean(means)), p99_abs_rgb_worst_frame=max(p99s),
                             what="the H.264 gap: decoded film against the colour of the stored value, 0..255 per channel")
    try:
        from PIL import Image
        Image.fromarray(image(maps[fh])).save(os.path.join(out, "poster.png"))
    except Exception as e:
        ck["poster_error"] = repr(e)
    passed = (ck["energy_forbidden_flips"]["value"] == 0 and ck["mirror_symmetry"]["value"] >= 0.98 and ck["gpu_vs_page_rk4"]["value"] >= 0.75
              and ck["step_halving"]["value"] >= 0.8 and ck["film_vs_map"]["frames_decoded"] == frames)
    files = {x: dict(bytes=os.path.getsize(os.path.join(out, x)), sha256=sha(os.path.join(out, x))) for x in ("film.mp4", "poster.png") if os.path.exists(os.path.join(out, x))}
    hdr = dict(model=model, format=1, method="RK4, h = 1/600 s, float64, the page's own formulas and order; JAX on the GPU; flip looked for after every step",
               params=dict(g=G, m1=M1, l1=L1, l2=L2, h=H, T_max=T_MAX, k_max=K_MAX, never=NEVER, failed=FAILED, n=n,
                           theta_deg="-180 + 360 * index / n", ln_m0=ln_m0, dln_m=dln_m, frames=frames, fps=FPS),
               layout=dict(map="map_<fff>.bin: n x n little-endian uint16, row = theta_2 index, column = theta_1 index",
                           film="film.mp4: frame f at time (f + 0.5) / fps; image row 0 = the largest theta_2, column 0 = theta_1 = -180 degrees"),
               colour=dict(scale="q = round(255 * clip(ln(k h / t_lo) / ln(T_max / t_lo), 0, 1))", t_lo=T_LO, stops=STOPS, lut=LUT.tolist(),
                           never=C_NEVER, failed=C_FAILED),
               frames=frame_info, files=files, checks=ck, bench=bench, checks_passed=bool(passed), gpu_s=gpu_s, wall_s=time.time() - t0,
               device=str(jax.devices()))
    json.dump(hdr, open(os.path.join(out, "film.json"), "w"), indent=0)
    log("done", frames, "frames", f"{gpu_s:.0f} s on the GPU", f"{time.time() - t0:.0f} s in all", "checks passed" if passed else "CHECKS FAILED")
    log(json.dumps(dict(checks=ck, bench=bench)))
    return dict(model=model, checks_passed=bool(passed), grid_part=dict(frames=[0, frames - 1]))

if __name__ == "__main__":
    print(run(sys.argv[1], n=int(sys.argv[2]) if len(sys.argv) > 2 else 72, frames=9, dln_m=0.575))

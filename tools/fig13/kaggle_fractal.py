# Fig. 13 (Phyein Usul): the chaos map of the double pendulum's momentum sheet, fine and deep, on a GPU.
# Same model, step and measure as tools/fig13/chaos_map.py of github.com/Numa1997/SiteTest: two equal uniform rods (m = 1 kg, l = 1 m,
# g = 9.8 m/s^2), every pixel a strike (p1, p2) from hanging still plus a twin with theta1 + 1e-4 rad; RK4, h = 0.05/120 s; after every
# step the distance in (theta1, theta2, p1, p2) capped at 1, averaged over the watch. 64-bit throughout.
import os, sys, json, time, math, threading
import numpy as np

# ------------------------------------------------------------------ parameters (all here)
SMOKE = os.environ.get('FIG13_SMOKE') == '1'          # tiny sizes, for a test without a GPU (NUMBA_ENABLE_CUDASIM=1)
OUT = os.environ.get('FIG13_OUT', '/kaggle/working')
PAR = dict(m=1.0, l=1.0, g=9.8, h=0.05 / 30 / 4, twin_dtheta1=1e-4, cap=1.0,
           P=20.0, aspect=16 / 9,
           sheet_px=(3840, 2160) if not SMOKE else (32, 18), sheet_watch=16000 * (0.05 / 30 / 4),
           zoom_px=(1920, 1080) if not SMOKE else (32, 18), zoom_watch=26.67 if not SMOKE else 0.2, zoom_centre=(2.046805, 3.987946),
           zoom_widths=[8.0, 1.0, 1 / 8, 1 / 64, 1 / 512, 1 / 4096] if not SMOKE else [8.0, 1.0],
           eye_px=(3840, 2160) if not SMOKE else (32, 18), eye_half=(14.4, 8.1), eye_watch=26.67 if not SMOKE else 0.2,
           budget_s=3.0 * 3600, chunk_steps=2000 if not SMOKE else 100, tile=1 << 21)
if SMOKE: PAR['sheet_watch'] = 0.2
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
def log(msg):
    line = f'[{time.time() - T0:8.1f} s] {msg}'; print(line, flush=True)
    with open(os.path.join(OUT, 'progress.log'), 'a') as f: f.write(line + '\n')

# ------------------------------------------------------------------ hardware: stop at once without a GPU
from numba import cuda, njit, prange
if not cuda.is_available(): raise SystemExit('No GPU visible: stopping (this run is meant for a GPU).')
NGPU = len(cuda.gpus) if not SMOKE else 1
for i in range(NGPU):
    try: nm = cuda.gpus[i].name; nm = nm.decode() if isinstance(nm, bytes) else str(nm)
    except Exception as e: nm = 'name not readable (' + type(e).__name__ + ')'
    log(f'GPU {i}: {nm}')
import numba; log(f'numba {numba.__version__}, numpy {np.__version__}, python {sys.version.split()[0]}')
json.dump(PAR, open(os.path.join(OUT, 'params.json'), 'w'), indent=1)

a_ = PAR['l'] / 2; I_ = PAR['m'] * PAR['l'] ** 2 / 12
A = PAR['m'] * a_ ** 2 + I_ + PAR['m'] * PAR['l'] ** 2; B = PAR['m'] * a_ ** 2 + I_; C = PAR['m'] * PAR['l'] * a_
U1 = PAR['g'] * (PAR['m'] * a_ + PAR['m'] * PAR['l']); U2 = PAR['g'] * PAR['m'] * a_

@cuda.jit(device=True, inline=True)
def deriv(q1, q2, p1, p2):
    d = q1 - q2; cs = math.cos(d); sn = math.sin(d); det = A * B - C * C * cs * cs
    w1 = (B * p1 - C * cs * p2) / det; w2 = (A * p2 - C * cs * p1) / det; e = C * w1 * w2 * sn
    return w1, w2, -e - U1 * math.sin(q1), e - U2 * math.sin(q2)

@cuda.jit(device=True, inline=True)
def rk4(q1, q2, p1, p2, h):
    a1, a2, a3, a4 = deriv(q1, q2, p1, p2)
    b1, b2, b3, b4 = deriv(q1 + .5 * h * a1, q2 + .5 * h * a2, p1 + .5 * h * a3, p2 + .5 * h * a4)
    c1, c2, c3, c4 = deriv(q1 + .5 * h * b1, q2 + .5 * h * b2, p1 + .5 * h * b3, p2 + .5 * h * b4)
    d1, d2, d3, d4 = deriv(q1 + h * c1, q2 + h * c2, p1 + h * c3, p2 + h * c4)
    return (q1 + h / 6 * (a1 + 2 * b1 + 2 * c1 + d1), q2 + h / 6 * (a2 + 2 * b2 + 2 * c2 + d2),
            p1 + h / 6 * (a3 + 2 * b3 + 2 * c3 + d3), p2 + h / 6 * (a4 + 2 * b4 + 2 * c4 + d4))

@cuda.jit
def advance(Q, Ssum, nsteps, h, cap):       # Q[i] = the pendulum's state and its twin's (8 numbers); Ssum[i] = sum of capped distances
    i = cuda.grid(1)
    if i < Q.shape[0]:
        q1 = Q[i, 0]; q2 = Q[i, 1]; p1 = Q[i, 2]; p2 = Q[i, 3]; r1 = Q[i, 4]; r2 = Q[i, 5]; s1 = Q[i, 6]; s2 = Q[i, 7]; acc = Ssum[i]
        for _ in range(nsteps):
            q1, q2, p1, p2 = rk4(q1, q2, p1, p2, h); r1, r2, s1, s2 = rk4(r1, r2, s1, s2, h)
            d = math.sqrt((q1 - r1) ** 2 + (q2 - r2) ** 2 + (p1 - s1) ** 2 + (p2 - s2) ** 2)
            acc += d if d < cap else cap
        Q[i, 0] = q1; Q[i, 1] = q2; Q[i, 2] = p1; Q[i, 3] = p2; Q[i, 4] = r1; Q[i, 5] = r2; Q[i, 6] = s1; Q[i, 7] = s2; Ssum[i] = acc

def gpu_map(P1, P2, steps, tag):
    """Mean capped twin distance for the strikes (P1, P2), flat arrays; tiles shared between the GPUs."""
    n = P1.size; out = np.empty(n); tiles = [(a, min(n, a + PAR['tile'])) for a in range(0, n, PAR['tile'])]; lock = threading.Lock(); done = [0]; err = []
    def work(dev):
        try:
            if not SMOKE: cuda.select_device(dev)
            while True:
                with lock:
                    if not tiles: break
                    a, b = tiles.pop(0)
                Q = np.zeros((b - a, 8)); Q[:, 2] = P1[a:b]; Q[:, 3] = P2[a:b]; Q[:, 4] = PAR['twin_dtheta1']; Q[:, 6] = P1[a:b]; Q[:, 7] = P2[a:b]
                dQ = cuda.to_device(Q); dS = cuda.to_device(np.zeros(b - a)); left = steps
                while left > 0:
                    k = min(left, PAR['chunk_steps']); advance[(b - a + 255) // 256, 256](dQ, dS, k, PAR['h'], PAR['cap']); cuda.synchronize(); left -= k
                out[a:b] = dS.copy_to_host() / steps
                with lock: done[0] += b - a; log(f'{tag}: {done[0]}/{n} strikes ({100 * done[0] / n:.0f} %)')
        except Exception as e: err.append(repr(e))
    th = [threading.Thread(target=work, args=(d,)) for d in range(NGPU)]
    for t in th: t.start()
    for t in th: t.join()
    if err: raise RuntimeError(err[0])
    return out

# ------------------------------------------------------------------ the same on the processor, for the check (chaos_map.twin_map)
@njit(inline='always')
def deriv_c(q1, q2, p1, p2):
    d = q1 - q2; cs = np.cos(d); sn = np.sin(d); det = A * B - C * C * cs * cs
    w1 = (B * p1 - C * cs * p2) / det; w2 = (A * p2 - C * cs * p1) / det; e = C * w1 * w2 * sn
    return w1, w2, -e - U1 * np.sin(q1), e - U2 * np.sin(q2)
@njit(inline='always')
def rk4_c(q1, q2, p1, p2, h):
    a1, a2, a3, a4 = deriv_c(q1, q2, p1, p2)
    b1, b2, b3, b4 = deriv_c(q1 + .5 * h * a1, q2 + .5 * h * a2, p1 + .5 * h * a3, p2 + .5 * h * a4)
    c1, c2, c3, c4 = deriv_c(q1 + .5 * h * b1, q2 + .5 * h * b2, p1 + .5 * h * b3, p2 + .5 * h * b4)
    d1, d2, d3, d4 = deriv_c(q1 + h * c1, q2 + h * c2, p1 + h * c3, p2 + h * c4)
    return (q1 + h / 6 * (a1 + 2 * b1 + 2 * c1 + d1), q2 + h / 6 * (a2 + 2 * b2 + 2 * c2 + d2),
            p1 + h / 6 * (a3 + 2 * b3 + 2 * c3 + d3), p2 + h / 6 * (a4 + 2 * b4 + 2 * c4 + d4))
@njit(parallel=True)
def cpu_map(P1, P2, steps, h, dth, cap):
    out = np.empty(P1.size)
    for i in prange(P1.size):
        q1 = 0.0; q2 = 0.0; p1 = P1[i]; p2 = P2[i]; r1 = dth; r2 = 0.0; s1 = P1[i]; s2 = P2[i]; acc = 0.0
        for _ in range(steps):
            q1, q2, p1, p2 = rk4_c(q1, q2, p1, p2, h); r1, r2, s1, s2 = rk4_c(r1, r2, s1, s2, h)
            d = np.sqrt((q1 - r1) ** 2 + (q2 - r2) ** 2 + (p1 - s1) ** 2 + (p2 - s2) ** 2); acc += min(d, cap)
        out[i] = acc / steps
    return out

def grid(c1, c2, hw, hh, W, H):
    p1 = c1 + ((np.arange(W) + .5) / W - .5) * 2 * hw; p2 = c2 + (.5 - (np.arange(H) + .5) / H) * 2 * hh
    P1, P2 = np.meshgrid(p1, p2); return P1.ravel(), P2.ravel()
def bright(d): return np.clip(np.log(1000 * np.maximum(d, 1e-12)) / np.log(1000), 0, 1)        # map_png.py
def save(name, d, W, H, meta):
    d = d.reshape(H, W); np.save(os.path.join(OUT, name + '.npy'), d.astype(np.float32))
    from PIL import Image
    v = bright(d); wine, rose, bg = np.array([122, 31, 43.]), np.array([226, 162, 170.]), np.array([20, 13, 16.])
    al = (v ** 0.8)[..., None]; rgb = bg * (1 - al) + (wine * (1 - v[..., None]) + rose * v[..., None]) * al
    Image.fromarray(rgb.round().astype(np.uint8)).save(os.path.join(OUT, name + '.png'), optimize=True)
    RES[name] = dict(meta, W=W, H=H, chaotic_share=float((v > .5).mean())); json.dump(RES, open(os.path.join(OUT, 'results.json'), 'w'), indent=1)
RES, TIM = {}, {'devices': NGPU, 'precision': 'float64'}
h = PAR['h']

# ------------------------------------------------------------------ 1. the check and the speed: 4096 strikes, GPU against processor
P1, P2 = grid(0, 0, PAR['P'] * PAR['aspect'], PAR['P'], 64, 64); st = 2000 if not SMOKE else 100
t = time.time(); g = gpu_map(P1, P2, st, 'check (compile)'); t = time.time(); g = gpu_map(P1, P2, st, 'check'); tg = time.time() - t
c = cpu_map(P1, P2, st, h, PAR['twin_dtheta1'], PAR['cap']); TIM['check_max_abs_diff_gpu_cpu'] = float(np.abs(g - c).max()); TIM['check_median_value'] = float(np.median(c))
log(f"check: GPU against processor on 4096 strikes, {st} steps: largest difference {TIM['check_max_abs_diff_gpu_cpu']:.2e}")
if not SMOKE:
    P1, P2 = grid(0, 0, PAR['P'] * PAR['aspect'], PAR['P'], 1024, 1024); t = time.time(); gpu_map(P1, P2, 2000, 'speed'); dt = time.time() - t
    SPEED = 1024 * 1024 * 2000 * 2 / dt
else: SPEED = 64 * 64 * st * 2 / max(tg, 1e-9)
TIM['pendulum_steps_per_second'] = SPEED; log(f'speed: {SPEED:.3e} pendulum steps a second on {NGPU} GPU(s)')
def cost(W, H, watch): return W * H * round(watch / h) * 2 / SPEED
def fits(sec): return (time.time() - T0) + sec < PAR['budget_s']

# ------------------------------------------------------------------ 2. A: the whole sheet, fine
W, H = PAR['sheet_px']; steps = round(PAR['sheet_watch'] / h); est = cost(W, H, PAR['sheet_watch']); log(f'A sheet {W}x{H}, watch {steps * h:.2f} s: estimated {est / 60:.1f} min')
if not fits(est): W, H = W // 2, H // 2; log(f'A reduced to {W}x{H} to fit the time budget')
t = time.time(); P1, P2 = grid(0, 0, PAR['P'] * PAR['aspect'], PAR['P'], W, H); d = gpu_map(P1, P2, steps, 'A sheet')
save('sheet', d, W, H, dict(centre=[0, 0], half=[PAR['P'] * PAR['aspect'], PAR['P']], watch_s=steps * h)); TIM['A_sheet_s'] = time.time() - t

# ------------------------------------------------------------------ 3. Z: nested zooms into the boundary, each aimed at the most detailed spot of the last
c1, c2 = PAR['zoom_centre']; W, H = PAR['zoom_px']; steps = round(PAR['zoom_watch'] / h)
for lv, width in enumerate(PAR['zoom_widths']):
    est = cost(W, H, PAR['zoom_watch'])
    if not fits(est + 60): log(f'zoom {lv} skipped: would pass the time budget'); break
    hw, hh = width / 2, width / 2 * H / W; t = time.time(); P1, P2 = grid(c1, c2, hw, hh, W, H); d = gpu_map(P1, P2, steps, f'Z{lv} width {width:g}')
    save(f'zoom{lv}', d, W, H, dict(centre=[c1, c2], half=[hw, hh], watch_s=steps * h)); TIM[f'Z{lv}_s'] = time.time() - t
    # the next centre: where the picture changes most within a window the size of the next frame (boundary-rich), away from the edges
    v = bright(d.reshape(H, W)); gy, gx = np.gradient(v); e = np.hypot(gx, gy); cs = np.cumsum(np.cumsum(np.pad(e, ((1, 0), (1, 0))), 0), 1)
    wy, wx = max(2, H // 8), max(2, W // 8); box = cs[wy:, wx:] - cs[:-wy, wx:] - cs[wy:, :-wx] + cs[:-wy, :-wx]
    mixed = np.cumsum(np.cumsum(np.pad((v > .5).astype(float), ((1, 0), (1, 0))), 0), 1); frac = (mixed[wy:, wx:] - mixed[:-wy, wx:] - mixed[wy:, :-wx] + mixed[:-wy, :-wx]) / (wy * wx)
    score = box * (4 * frac * (1 - frac) + 0.05); iy, ix = np.unravel_index(np.argmax(score), score.shape); iy += wy // 2; ix += wx // 2
    c1 = c1 + ((ix + .5) / W - .5) * 2 * hw; c2 = c2 + (.5 - (iy + .5) / H) * 2 * hh; log(f'next zoom centre ({c1:.9f}, {c2:.9f})')

# ------------------------------------------------------------------ 4. B: the eye, fine, with the long watch
W, H = PAR['eye_px']; steps = round(PAR['eye_watch'] / h); est = cost(W, H, PAR['eye_watch']); log(f'B eye {W}x{H}, watch {steps * h:.2f} s: estimated {est / 60:.1f} min')
while not fits(est + 60) and W > 480: W, H = W // 2, H // 2; est = cost(W, H, PAR['eye_watch']); log(f'B reduced to {W}x{H}')
if fits(est + 60):
    t = time.time(); P1, P2 = grid(0, 0, PAR['eye_half'][0], PAR['eye_half'][1], W, H); d = gpu_map(P1, P2, steps, 'B eye')
    save('eye', d, W, H, dict(centre=[0, 0], half=list(PAR['eye_half']), watch_s=steps * h)); TIM['B_eye_s'] = time.time() - t
else: log('B skipped: no time left in the budget')
TIM['total_s'] = time.time() - T0; json.dump(TIM, open(os.path.join(OUT, 'timing.json'), 'w'), indent=1); log('done')

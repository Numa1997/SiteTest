"""Fig. 12 computed on Kaggle: how fast the stored swing dies, and how far the wall lean drifts.

Reads public/data/fig12/<date>/rides.json (default: the newest date folder) and prints, for each ride:
  - the first sloshing mode q(t): the cos(theta) part of the outer ring of the stored surface, in mm
    (at the wall the first mode is eta = q cos theta, Fig. 12 note, section 4.5);
  - its strongest frequency between 2.5 and 4.5 Hz (FFT of the whole ride);
  - the decay after the last bump: q band-passed to 2.5-4.5 Hz, its envelope (analytic signal), and a straight-line fit
    of log(envelope) over 1.5 s from the envelope's peak just after the bump; e-folding time tau and the damping ratio
    zeta = 1 / (omega_11 tau), omega_11 = 2 pi 3.421 Hz;
  - the drift: the stored lean (front minus back wall) and q, averaged over the last 5 s, when the cart rolls at steady
    speed on flat road and the stout should be level.

Run: python3 tools/fig12/kaggle_decay.py [path/to/rides.json]
"""
import base64, glob, json, os, sys, zlib
import numpy as np

F11 = 3.421          # Hz, deep cylinder of the surface radius 39.1 mm (note, eq. 16)


def main(path):
    D = json.load(open(path))
    nr, nth, fps = D["nr"], D["nth"], D["fps"]
    th = 2 * np.pi * np.arange(nth) / nth
    print(f"{path}\nfirst mode of a deep cylinder: f11 = {F11} Hz; real stout's damping ratio 0.0035 (theory) to 0.0053 (experiment)")
    for r in sorted(D["rides"], key=lambda r: r["v0"]):
        b = np.frombuffer(zlib.decompress(base64.b64decode(r["frames"])), np.uint8).reshape(r["n"], nr + 1, nth).astype(float)
        h = (D["fill"] + (b - 128) * D["q"]) * 1000                          # mm
        q = 2 / nth * (h[:, nr, :] * np.cos(th)).sum(1)
        t = np.arange(r["n"]) / fps
        x = np.array(r["x"]); lean = np.array(r["lean"])
        n = len(q); F = np.fft.fft(q - q.mean()); f = np.fft.fftfreq(n, 1 / fps)
        band = (np.abs(f) > 2.5) & (np.abs(f) < 4.5)
        spec = np.abs(np.fft.rfft((q - q.mean()) * np.hanning(n), n=16384)); fr = np.fft.rfftfreq(16384, 1 / fps)
        sel = (fr > 2.5) & (fr < 4.5); fpk = fr[sel][spec[sel].argmax()]
        Hh = np.zeros(n); Hh[0] = 1; Hh[1:(n + 1) // 2] = 2
        qb = np.real(np.fft.ifft(F * band)); env = np.abs(np.fft.ifft(np.fft.fft(qb) * Hh))
        line = f"v0 {r['v0']} m/s: strongest swing {fpk:.3f} Hz"
        if x.max() > 9.15:
            i0 = int(np.argmax(x > 9.15)); j = i0 + int(np.argmax(env[i0:i0 + 15])); seg = slice(j, j + 45)
            ok = env[seg] > 0.05; p = np.polyfit(t[seg][ok], np.log(env[seg][ok]), 1); tau = -1 / p[0]
            line += f"; after the last bump: envelope {env[j]:.2f} mm at t = {t[j]:.2f} s, e-folding time {tau:.2f} s, damping ratio {1 / (2 * np.pi * F11 * tau):.3f}"
        last = t > t[-1] - 5
        line += f"; last 5 s: wall lean {lean[last].mean():.2f} mm, first mode q {q[last].mean():.2f} mm"
        print(line)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        dates = sorted(glob.glob(os.path.join(here, "..", "..", "public", "data", "fig12", "*", "rides.json")))
        main(os.path.normpath(dates[-1]))

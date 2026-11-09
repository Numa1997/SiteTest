"""Phasor (Fourier) data for the words of reem.html: each word drawn by a chain of turning arrows.

Font: Noto Nastaliq Urdu (SIL Open Font License, fonts/OFL-NotoNastaliqUrdu.txt), downloaded on 8 November 2026 from
https://raw.githubusercontent.com/google/fonts/main/ofl/notonastaliqurdu/ ; drawn at random (secrets.randbelow) among the three
classical-hand fonts of a shortlist of seven open-licence Arabic fonts (Aref Ruqaa, Noto Nastaliq Urdu, Amiri).

For each word: its outline contours (calligraphy.py), ordered right to left as Arabic is written, each started at the point nearest
the end of the one before and joined to it by a straight pen-up bridge; the whole closed path resampled at N points equally spaced
in arc length, z_n = x_n + i y_n (word width 2, centred; y up); its discrete Fourier transform
    c_k = (1/N) sum_n z_n exp(-2 pi i k n / N),   z(s) = sum_k c_k exp(2 pi i k s),  s in [0, 1)
and the K terms of largest |c_k|, which become the arrows. Hidden (pen-up) parameter intervals are stored with the terms.
Checks: the K-term sum reproduces the drawn (pen-down) samples to within MAXERR of the word width.

Usage: python3 tools/fig13/gift/reem_data.py OUT.json
"""
import sys, json
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from calligraphy import word_contours

FONT = __file__.rsplit('/', 1)[0] + '/fonts/NotoNastaliqUrdu-wght.ttf'
import json as _json
HERE = __file__.rsplit('/', 1)[0]
AMIRI = HERE + '/fonts/Amiri-Regular.ttf'
def traced(path):   # outlines traced from the reference plate (ref_trace.py): pixels, y down -> y up
    return [np.array(c) * [1, -1] for c in _json.load(open(path))['contours']]
WORDS = {'reem': ('رِيمْ', lambda: traced(HERE + '/reem_ref.json'), 'evenodd'),
         'butterfly': ('فَرَاشَتُكِ', lambda: traced(HERE + '/farashatuki.json'), 'evenodd')}   # the Diwani plate Numa chose: farashatuki_trace.py panel
N, K, MAXERR = 8192, 640, 0.004


def resample(poly, ds):
    """Points every ds of arc length along a polyline (open)."""
    seg = np.hypot(*np.diff(poly, axis=0).T); s = np.concatenate([[0], np.cumsum(seg)])
    t = np.arange(0, s[-1], ds)
    return np.stack([np.interp(t, s, poly[:, 0]), np.interp(t, s, poly[:, 1])], axis=1), s[-1]


def build(text, source, rule):
    cs = source()
    allp = np.concatenate(cs); x0, x1, y0, y1 = allp[:, 0].min(), allp[:, 0].max(), allp[:, 1].min(), allp[:, 1].max()
    sc = 2 / (x1 - x0); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    cs = [(c - [cx, cy]) * sc for c in cs]
    cs.sort(key=lambda c: -c[:, 0].max())                     # right to left
    path, hidden_len, pieces, here = [], [], [], None
    for c in cs:
        closed = np.vstack([c, c[:1]])
        k = 0 if here is None else int(np.argmin(np.hypot(*(closed[:-1] - here).T)))
        loop = np.vstack([closed[k:-1], closed[:k + 1]])        # the contour, started at its point nearest the pen
        if here is not None: pieces.append(('up', np.vstack([here, loop[0]])))
        pieces.append(('down', loop)); here = loop[-1]
    pieces.append(('up', np.vstack([here, pieces[0][1][0]])))   # back to the start: a closed path for the Fourier series
    total = sum(np.hypot(*np.diff(p, axis=0).T).sum() for _, p in pieces)
    ds = total / N
    pts, flags = [], []
    for kind, p in pieces:
        q, _ = resample(p, ds); pts.append(q); flags += [kind == 'up'] * len(q)
    z = np.concatenate(pts); z = z[:, 0] + 1j * z[:, 1]; flags = np.array(flags)
    n = len(z); c = np.fft.fft(z) / n; f = np.fft.fftfreq(n, 1 / n).astype(int)
    keep = np.argsort(-np.abs(c))[:K]
    s = np.arange(n) / n
    rec = (c[keep][None, :] * np.exp(2j * np.pi * f[keep][None, :] * s[:, None])).sum(axis=1)
    err = np.abs(rec - z)[~flags]
    assert np.percentile(err, 99) < MAXERR * 2, np.percentile(err, 99)
    hidden, inside = [], False
    for i, fl in enumerate(flags):
        if fl and not inside: a = i / n; inside = True
        if not fl and inside: hidden.append([round(a, 6), round(i / n, 6)]); inside = False
    if inside: hidden.append([round(a, 6), 1.0])
    fill = [[[round(float(v), 4) for v in p] for p in cc[::max(1, len(cc) // 400)]] for cc in cs]
    print('%-9s %s  contours %d  samples %d  arrows %d  median error %.4f, 99%% %.4f (word width 2)  pen-up %.1f%%'
          % (text, '', len(cs), n, K, np.median(err), np.percentile(err, 99), 100 * flags.mean()))
    return dict(text=text, rule=rule, n=int(n), terms=[[int(f[i]), round(float(c[i].real), 6), round(float(c[i].imag), 6)] for i in keep],
                hidden=hidden, fill=fill, height=float((y1 - y0) * sc), median_err=float(np.median(err)))


out = {k: build(*v) for k, v in WORDS.items()}
out['sources'] = 'رِيمْ: traced from the reference plate Numa supplied (ref_trace.py); فَرَاشَتُكِ: traced from the Diwani plate Numa chose (farashatuki_trace.py)'
json.dump(out, open(sys.argv[1], 'w'), separators=(',', ':'), ensure_ascii=False)

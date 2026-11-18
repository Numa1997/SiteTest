"""Frame times of the two pages with the 3D close-up of the pint (public/scripts/pint3d-view.js), in headless Chromium on a Kaggle
GPU machine (open problem 4 of the Guinness rebuild; nothing runs outside Kaggle, owner, 15 November 2026).
Run from the repository's root, in a Kaggle notebook with a GPU and internet:
    python3 tools/fig16/kaggle/frames_check.py OUTDIR
For each way of reaching the GPU (ANGLE on Vulkan, ANGLE on EGL, Chromium's default), it records the WebGL renderer the page really
gets (so a software fallback such as SwiftShader is named, not mistaken for the T4), then plays each page for 8 s at 1440 x 1000 css px
and measures the interval between animation frames (requestAnimationFrame): median, 95th percentile, share of frames over 16.7 ms
(60 fps) and over 33.3 ms (30 fps). It also reads the close-up's own timer (Pint3D.stats: JavaScript ms and render-call ms per frame).
Writes OUTDIR/frames16-report.json and a log. Measures only; changes nothing."""
import json, os, subprocess, sys, threading, functools, http.server

OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
LOG = open(os.path.join(OUT, "frames16.log"), "w")


def log(m):
    print(m, flush=True); LOG.write(str(m) + "\n"); LOG.flush()


for a in (["-m", "pip", "install", "-q", "playwright==1.48.0"], ["-m", "playwright", "install", "--with-deps", "chromium"]):
    r = subprocess.run([sys.executable] + a, capture_output=True, text=True); log(f"{a[-1]}: exit {r.returncode}")
log(subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"], capture_output=True, text=True).stdout)

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=os.path.join(ROOT, "public"))
handler.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8017), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
PAGES = {"fig16": "http://127.0.0.1:8017/simulations/guinness-cart-control.html", "fig12": "http://127.0.0.1:8017/simulations/guinness-kaggle.html"}
MODES = {"angle-vulkan": ["--use-angle=vulkan", "--enable-features=Vulkan", "--ignore-gpu-blocklist", "--enable-gpu"],
         "angle-egl": ["--use-gl=angle", "--use-angle=gl-egl", "--ignore-gpu-blocklist", "--enable-gpu"],
         "default": []}
RENDERER = """() => { const c = document.createElement('canvas'), g = c.getContext('webgl2') || c.getContext('webgl'); if (!g) return 'no WebGL';
  const e = g.getExtension('WEBGL_debug_renderer_info'); return e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER); }"""
MEASURE = """(ms) => new Promise((res) => { const d = []; let last = null; const t0 = performance.now();
  const P = window.Pint3D && window.Pint3D.last, s0 = P && P.stats ? Object.assign({}, P.stats) : null;
  function f(t) { if (last !== null) d.push(t - last); last = t; if (t - t0 < ms) requestAnimationFrame(f); else {
    const s1 = P && P.stats ? P.stats : null, n = s1 && s0 ? s1.n - s0.n : 0;
    res({ d: d, close_up: n ? { frames: n, js_ms: (s1.js - s0.js) / n, render_call_ms: (s1.gl - s0.gl) / n } : null }); } }
  requestAnimationFrame(f); })"""


def stats(d):
    d = sorted(d); n = len(d)
    if not n: return None
    q = lambda p: d[min(n - 1, int(p * n))]
    return {"frames": n, "median_ms": round(q(0.5), 2), "p95_ms": round(q(0.95), 2), "max_ms": round(d[-1], 2),
            "fps_median": round(1000 / q(0.5), 1), "over_16.7ms": round(sum(x > 16.7 for x in d) / n, 3), "over_33.3ms": round(sum(x > 33.3 for x in d) / n, 3)}


from playwright.sync_api import sync_playwright
rep = {"modes": {}}
with sync_playwright() as p:
    for mode, args in MODES.items():
        try:
            br = p.chromium.launch(channel="chromium", args=args)
        except Exception as e:
            rep["modes"][mode] = {"error": str(e)[:300]}; log(f"{mode}: launch failed: {e}"); continue
        res = {}
        for name, url in PAGES.items():
            ctx = br.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1, bypass_csp=True)
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(url, wait_until="networkidle")
            pg.wait_for_timeout(3000)                                   # data unpacked, the close-up made
            pg.evaluate("() => { const c = document.querySelector('canvas.pint3d, #p3d'); if (c) c.scrollIntoView({ block: 'center' }); }")
            pg.wait_for_timeout(500)
            m = pg.evaluate(MEASURE, 8000)
            res[name] = {"renderer": pg.evaluate(RENDERER), "frames": stats(m["d"]), "close_up": m["close_up"], "errors": errs}
            log(f"{mode} {name}: {json.dumps(res[name])}")
            ctx.close()
        rep["modes"][mode] = res; br.close()
srv.shutdown()
json.dump(rep, open(os.path.join(OUT, "frames16-report.json"), "w"), indent=1)
log("done")

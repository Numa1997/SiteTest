"""Pictures of the spill on the Fig. 16 page (both carts: Fig. 12's best ride on the left, the new cart on the right), taken in
headless Chromium on Kaggle's CPU, to see how the stout that leaves the glass is drawn (nothing runs outside Kaggle, owner, 15 Nov 2026).
Run from the repository's root:  python3 tools/fig16/kaggle/spill_shots.py OUTDIR
For each ride and ride time it pauses the page at that time (?ride=&t=) and saves the two 2D figures (#c12, #c16) as PNG, plus the
number of drops and lumps stored for that picture (from the page's own ride objects). Measures and draws nothing itself."""
import json, os, subprocess, sys, threading, functools, http.server, signal

signal.signal(signal.SIGALRM, lambda *a: (_ for _ in ()).throw(SystemExit("spill_shots: 20-minute limit reached")))
signal.alarm(20 * 60)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
for a in (["-m", "pip", "install", "-q", "playwright==1.48.0"], ["-m", "playwright", "install", "--with-deps", "chromium"]):
    subprocess.run([sys.executable] + a, capture_output=True, text=True)
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=os.path.join(ROOT, "public"))
handler.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8018), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:8018/simulations/guinness-cart-control.html"
SHOTS = [("kerb_off.json", t) for t in (0.30, 0.45, 0.60, 0.80, 1.20)] + [("kerb_full.json", t) for t in (0.45, 0.80)]
from playwright.sync_api import sync_playwright
rep = []
with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1, bypass_csp=True)
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    for ride, t in SHOTS:
        pg.goto(f"{BASE}?ride={ride}&t={t}&no3d=1", wait_until="networkidle")
        pg.wait_for_function("() => window.Guinness16 && window.Sim && window.Sim.data", timeout=60000)
        pg.wait_for_timeout(800)
        info = pg.evaluate("() => { const d = window.Sim.data.ds; return { k16: d.get('k16'), k12: d.get('k12'), t: d.get('t_play'), "
                           "hspill: d.get('hspill_now'), sspill: d.get('sspill_now'), hspill12: d.get('hspill12_now'), sspill12: d.get('sspill12_now') }; }")
        name = f"spill-{ride[:-5]}-{t:.2f}"
        for cid in ("c12", "c16"):
            pg.locator("#" + cid).scroll_into_view_if_needed(); pg.locator("#" + cid).screenshot(path=os.path.join(OUT, f"{name}-{cid}.png"))
        info.update(ride=ride, t_asked=t); rep.append(info); print(json.dumps(info), flush=True)
    br.close()
srv.shutdown()
json.dump({"shots": rep, "errors": errs}, open(os.path.join(OUT, "spill-shots.json"), "w"), indent=1)
print("errors:", errs)

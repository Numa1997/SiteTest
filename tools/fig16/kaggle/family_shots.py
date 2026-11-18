"""Screenshots of the top of the two pages of the pint of Guinness (guinness-kaggle, guinness-cart-control) at 1440 and
390 px, to check the strip that says which of the three figures each page is (Kaggle CPU; nothing runs outside Kaggle, owner 15 Nov 2026).
Run from the repository's root:  python3 tools/fig16/kaggle/family_shots.py OUTDIR. Writes family-<page>-<width>.png and family.json
(the strip's three labels, which one is marked current, the h1, page errors)."""
import json, os, subprocess, sys, threading, functools, http.server, signal

signal.signal(signal.SIGALRM, lambda *a: (_ for _ in ()).throw(SystemExit("family_shots: 15-minute limit reached")))
signal.alarm(15 * 60)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
for a in (["-m", "pip", "install", "-q", "playwright==1.48.0"], ["-m", "playwright", "install", "--with-deps", "chromium"]):
    subprocess.run([sys.executable] + a, capture_output=True, text=True)
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=os.path.join(ROOT, "public"))
handler.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8019), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
from playwright.sync_api import sync_playwright
rep = []
with sync_playwright() as p:
    br = p.chromium.launch()
    for w, h in ((1440, 1000), (390, 844)):
        ctx = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, bypass_csp=True)
        for page in ("guinness-kaggle", "guinness-cart-control"):
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(f"http://127.0.0.1:8019/simulations/{page}.html?no3d=1", wait_until="domcontentloaded")
            pg.wait_for_timeout(2500)
            info = pg.evaluate("() => ({ h1: (document.querySelector('h1') || {}).textContent, labels: [...document.querySelectorAll('.gfam__list b')].map(b => b.textContent),"
                               " current: (document.querySelector('.gfam__list [aria-current=page] b') || {}).textContent,"
                               " strip_h: (document.querySelector('.gfam') || {getBoundingClientRect: () => ({height: 0})}).getBoundingClientRect().height,"
                               " overflow_x: document.documentElement.scrollWidth > window.innerWidth })")
            pg.screenshot(path=os.path.join(OUT, f"family-{page}-{w}.png"), clip={"x": 0, "y": 0, "width": w, "height": min(h, 900)})
            info.update(page=page, width=w, errors=errs); rep.append(info); print(json.dumps(info), flush=True); pg.close()
        ctx.close()
    br.close()
srv.shutdown()
json.dump(rep, open(os.path.join(OUT, "family.json"), "w"), indent=1)
bad = [r for r in rep if len(r["labels"]) != 2 or not r["current"] or r["overflow_x"] or r["errors"]]
print("FAMILY FAIL" if bad else "FAMILY OK", len(bad))

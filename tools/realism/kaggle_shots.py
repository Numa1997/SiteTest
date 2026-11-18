"""Screenshots of the Guinness figures (Fig. 12, Fig. 16) on Kaggle's CPU, for the realism work (notes/realism/STATE.md).
Nothing runs outside Kaggle (owner, 15 and 18 November 2026). Steps:
  1. the repository at commit COMMIT (codeload tarball) into /tmp/repo;
  2. Chromium through Playwright (pip), WebGL by SwiftShader as in tools/fig16/check_pint3d.cjs;
  3. the pages served from /tmp/repo/public by request interception (host local.test); every other host is refused;
  4. for each page of FIG (12 or 16), each width (390, 1440) and each moment: a picture of the whole first screen and one of the
     figure's canvas alone, at device scale 2; the stored rides are moved to the moment with the page's own seek();
  5. /kaggle/working/shots/*.png, shots.log, manifest.json (file, page, width, ride, t, console errors).
Environment: COMMIT, FIG ("12" or "16"), TAG (e.g. "before")."""
import io, json, os, subprocess, sys, tarfile, time, urllib.request

COMMIT = os.environ["COMMIT"]; FIG = os.environ["FIG"]; TAG = os.environ.get("TAG", "before")
WORK = "/kaggle/working"; OUT = os.path.join(WORK, "shots"); REPO = "/tmp/repo"; os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(WORK, "shots.log"), "w")


def log(m):
    print(m, flush=True); LOG.write(m + "\n"); LOG.flush()


data = urllib.request.urlopen(f"https://codeload.github.com/Numa1997/SiteTest/tar.gz/{COMMIT}").read()
with tarfile.open(fileobj=io.BytesIO(data)) as t:
    top = t.getnames()[0].split("/")[0]; t.extractall("/tmp")
os.rename(os.path.join("/tmp", top), REPO); log(f"repository at {COMMIT}")
for cmd in ([sys.executable, "-m", "pip", "install", "-q", "playwright"], [sys.executable, "-m", "playwright", "install", "--with-deps", "chromium"]):
    r = subprocess.run(cmd, capture_output=True, text=True); log(f"$ {' '.join(cmd[2:])} (exit {r.returncode}) {r.stderr[-500:]}")

from playwright.sync_api import sync_playwright  # noqa: E402

PUBLIC = os.path.join(REPO, "public")
TYPES = {".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml",
         ".webp": "image/webp", ".png": "image/png", ".woff2": "font/woff2", ".jpg": "image/jpeg"}
# (page, ride query or None, seek function or None, moments in s, canvas selector)
PAGES = {
    "12": [("simulations/guinness-kaggle.html", None, "GuinnessJax", [0.0, 0.8, 1.6, 3.0], "canvas"),
           ("simulations/beer-slosh.html", None, None, [3.0, 8.0], "#cv")],
    "16": [("simulations/guinness-cart-control.html", "kerb_full.json", "Guinness16", [0.0, 0.6, 2.0], "canvas"),
           ("simulations/guinness-cart-control.html", "kerb_off.json", "Guinness16", [0.7], "canvas")],
}[FIG]
WIDTHS = [(390, 844), (1440, 900)]


def serve(route):
    from urllib.parse import urlparse, unquote
    p = unquote(urlparse(route.request.url).path); f = os.path.join(PUBLIC, p.lstrip("/"))
    if p.endswith("/"): f = os.path.join(f, "index.html")
    if not os.path.isfile(f): return route.fulfill(status=404, body="")
    route.fulfill(status=200, body=open(f, "rb").read(), content_type=TYPES.get(os.path.splitext(f)[1], "application/octet-stream"))


manifest = []
with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for (page, ride, seek, moments, sel) in PAGES:
        for (w, h) in WIDTHS:
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2); pg = ctx.new_page(); errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.route(lambda u: "local.test" in u, serve); pg.route(lambda u: "local.test" not in u, lambda r: r.abort())
            pg.goto(f"http://local.test/{page}" + (f"?ride={ride}" if ride else "")); pg.wait_for_timeout(6000)
            for t in moments:
                # the stored rides are paused by seek(); without a graphics card (Kaggle CPU) Chromium draws WebGL in software,
                # so one frame can take seconds: allow 3 minutes per picture and never let one failed picture stop the run
                try:
                    if seek: pg.evaluate(f"(t) => window.{seek}.seek(t)", t); pg.wait_for_timeout(3000)
                    else: pg.wait_for_timeout(int(t * 1000) if t == moments[0] else int((t - moments[moments.index(t) - 1]) * 1000))
                except Exception as e:
                    errs.append(f"seek: {e}")
                stem = f"{TAG}_fig{FIG}_{os.path.basename(page)[:-5]}_{ride[:-5] if ride else 'live'}_{w}_t{t:.1f}"
                shots = {}
                for kind, target in (("screen", pg), ("figure", pg.locator(sel).first)):
                    t0 = time.time()
                    try:
                        if kind == "figure": target.scroll_into_view_if_needed(timeout=60000)
                        target.screenshot(path=os.path.join(OUT, f"{stem}_{kind}.png"), timeout=180000); shots[kind] = round(time.time() - t0, 1)
                    except Exception as e:
                        shots[kind] = None; errs.append(f"{kind} shot: {str(e)[:300]}")
                manifest.append({"file": stem, "page": page, "width": w, "ride": ride, "t": t, "seconds": shots, "errors": list(errs)})
                log(f"{stem}: " + ", ".join(f"{k} {'MISSING' if v is None else f'{v} s'}" for k, v in shots.items()) + f", {len(errs)} errors")
                json.dump(manifest, open(os.path.join(WORK, "manifest.json"), "w"), indent=1)
            ctx.close()
    b.close()
json.dump(manifest, open(os.path.join(WORK, "manifest.json"), "w"), indent=1)
log(f"done: {len(manifest)} moments, {len(os.listdir(OUT))} pictures")

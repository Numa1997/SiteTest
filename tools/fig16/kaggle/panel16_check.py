"""Fig. 16's data panel, proved in headless Chromium on Kaggle's CPU (nothing runs outside Kaggle, owner, 15 November 2026).
Run from the repository's root, inside a Kaggle notebook with internet on:
    python3 tools/fig16/kaggle/panel16_check.py OUTDIR
Steps:
  1. tools/fig16/build_page.py, then --check (the page is built from notes/fig16/page/guinness-cart-control.src.html);
  2. public/ served on 127.0.0.1:8016 by Python's http.server, inside the notebook;
  3. Playwright's Chromium (installed by this script) opens the page at 1440 x 1000 and 390 x 844 css px, on three rides;
  4. for every value the panel can check: the stored value, the formula recomputed from the stored inputs (Sim.data.check)
     and the read-back from the picture (Sim.data.drawn); the head's book; console errors;
  5. the pointer: crossing the figure with Read values off must change nothing (the overlay stays empty, no strip);
     with Read values on, a click pins a pane and the strip's words change at most about 4 times a second;
  6. screenshots (deviceScaleFactor 2 for the owner) and OUTDIR/panel16-report.json.
Exit status 1 if any check fails."""
import json, os, subprocess, sys, time, http.server, threading, functools

OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, "panel16.log"), "w")


def log(m):
    print(m, flush=True); LOG.write(str(m) + "\n"); LOG.flush()


def sh(args, check=True):
    r = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    log(f"$ {' '.join(args)}  (exit {r.returncode})\n{r.stdout[-2000:]}{r.stderr[-2000:]}")
    if check and r.returncode: raise SystemExit(f"failed: {args}")
    return r.returncode


sh([sys.executable, "tools/fig16/build_page.py"])
sh([sys.executable, "tools/fig16/build_page.py", "--check"])
sh([sys.executable, "-m", "pip", "install", "-q", "playwright==1.48.0"])
sh([sys.executable, "-m", "playwright", "install", "--with-deps", "chromium"])

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=os.path.join(ROOT, "public"))
handler.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8016), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:8016/simulations/guinness-cart-control.html"

# in the page: every check and read-back the panel offers, at the picture on screen (playback paused)
PROOF = """() => {
  const S = window.Sim, d = S.data, ds = d.ds, out = { checks: [], drawn: [], book: null };
  for (const n of Object.keys(d.check)) {
    const v = ds.vars[n]; if (!v) { out.checks.push({ n, err: 'not in the store' }); continue; }
    if (v.dims.length) { const k = Math.min(3, ds.get(n).length - 1), c = d.check[n](k), s = ds.get(n)[k];
      out.checks.push({ n: n + '[' + k + ']', stored: s, recomputed: c.value, diff: Math.abs(s - c.value) }); continue; }
    const c = d.check[n](), s = ds.get(n);
    out.checks.push({ n, stored: s, recomputed: c.value, diff: typeof s === 'number' ? Math.abs(s - c.value) : (s === c.value ? 0 : 1) });
  }
  for (const n of Object.keys(d.drawn)) { const r = d.drawn[n](); out.drawn.push({ n, what: r.what, drawn: r.drawn, expected: r.expected, ok: r.ok }); }
  const g = (n) => ds.get(n), sum = g('hglass_now') + g('hspill_now');
  out.book = { glass: g('hglass_now'), spilled: g('hspill_now'), total: g('head_ml0'), residual_page: g('head_res'), residual_panel: sum - g('head_ml0') };
  out.k16 = g('k16'); out.t = g('t_play'); out.ride = g('ride16'); out.ctrl = g('ctrl_on');
  return out;
}"""

from playwright.sync_api import sync_playwright

report = {"runs": [], "pointer": None, "errors": []}
fail = 0
with sync_playwright() as p:
    br = p.chromium.launch()
    for (w, h) in [(1440, 1000), (390, 844)]:
        ctx = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=2, bypass_csp=True)   # the test's own probes are evaluated strings; the page's policy is not changed
        pg = ctx.new_page(); errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        for ride, t in [("kerb_full.json", 0.62), ("kerb_off.json", 0.40), ("resonant_full.json", 2.0)]:
            pg.goto(f"{BASE}?ride={ride}&t={t}", wait_until="networkidle")
            pg.wait_for_function("() => window.Sim && window.Sim.data && document.querySelector('.dp-tab')", timeout=60000)
            pg.wait_for_timeout(700)                      # the readings are rewritten 4 times a second
            r = pg.evaluate(PROOF); r["viewport"] = [w, h]; r["ride_asked"] = ride
            bad_c = [c for c in r["checks"] if c.get("err") or (isinstance(c.get("diff"), (int, float)) and c["diff"] > 1e-9)]
            bad_d = [x for x in r["drawn"] if not x["ok"] and x["drawn"] != "not recorded"]
            b = r["book"]; book_ok = abs(b["residual_page"]) < 1e-6 and abs(b["residual_page"] - b["residual_panel"]) < 1e-12
            r["verdict"] = {"checks": len(r["checks"]), "checks_bad": bad_c, "drawn": len(r["drawn"]), "drawn_bad": bad_d,
                            "deck_recorded": any(x["drawn"] != "not recorded" for x in r["drawn"] if x["n"].startswith("deck")), "book_ok": book_ok}
            fail += bool(bad_c or bad_d or not book_ok)
            log(json.dumps(r["verdict"])); report["runs"].append(r)
        if w == 1440:
            # the pointer, Read values off: sweep across the figure; the overlay must stay empty and no strip may show
            st = pg.locator("#stage").bounding_box()
            pg.evaluate("() => window.Guinness16.choose && window.Guinness16.seek(0.5)")
            for i in range(41): pg.mouse.move(st["x"] + st["width"] * i / 40, st["y"] + st["height"] * 0.3); pg.wait_for_timeout(25)
            off = pg.evaluate("""() => { const o = document.querySelector('.dp-overlay'), c = o.getContext('2d').getImageData(0, 0, o.width, o.height).data;
              let n = 0; for (let i = 3; i < c.length; i += 4) if (c[i]) n++; const s = document.querySelector('.dp-read'); return { overlay_px: n, strip_hidden: s ? s.hidden : true }; }""")
            pg.screenshot(path=os.path.join(OUT, "fig16-panel-figure.png"))
            # Read values on: pin the right cart while it plays; count how often the strip's words change in 3 s
            pg.click(".dp-readbtn"); c16 = pg.locator("#c16").bounding_box()
            pg.mouse.click(c16["x"] + c16["width"] / 2, c16["y"] + c16["height"] / 2)
            pg.evaluate("() => { document.getElementById('again').click(); }")
            changes = pg.evaluate("""() => new Promise((res) => { const el = document.querySelector('.dp-read__vals'); let last = el.textContent, n = 0, t0 = performance.now();
              const id = setInterval(() => { if (el.textContent !== last) { n++; last = el.textContent; } if (performance.now() - t0 > 3000) { clearInterval(id); res({ changes_3s: n, title: document.querySelector('.dp-read__title').textContent, words: last }); } }, 10); })""")
            area = pg.evaluate("() => { const s = document.querySelector('.dp-read').getBoundingClientRect(), f = document.getElementById('stage').getBoundingClientRect(); return { strip_h: s.height, figure_h: f.height, overlaps: s.top < f.bottom - 1 }; }")
            pg.screenshot(path=os.path.join(OUT, "fig16-read-values.png"))
            report["pointer"] = {"read_off": off, "read_on": changes, "strip": area}
            ok = off["overlay_px"] == 0 and off["strip_hidden"] and changes["changes_3s"] <= 15 and not area["overlaps"] and changes["title"]
            fail += not ok; log("pointer: " + json.dumps(report["pointer"]) + (" OK" if ok else " FAIL"))
            # the panel open, the ledger and the books
            pg.click(".dp-readbtn"); pg.click(".dp-tab"); pg.wait_for_timeout(800)
            pg.screenshot(path=os.path.join(OUT, "fig16-panel-open.png"))
        else:
            pg.screenshot(path=os.path.join(OUT, "fig16-panel-phone.png"), full_page=False)
        report["errors"] += [f"{w}px: {e}" for e in errs]
        ctx.close()
    br.close()
srv.shutdown()
errs = [e for e in report["errors"] if "cloudflareinsights" not in e]
fail += bool(errs)
report["fail"] = fail
json.dump(report, open(os.path.join(OUT, "panel16-report.json"), "w"), indent=1, default=str)
log(f"errors: {errs}\nFAIL count: {fail}")
sys.exit(1 if fail else 0)

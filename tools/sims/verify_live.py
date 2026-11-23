"""Step 10 of the simulations pipeline: check the live site after a run (docs/kaggle-sims.md).

For one simulation and the code commit it was computed from:
  1. wait until https://phyeinusul.com/data/sims/generations.json lists that simulation from that commit (Cloudflare has published);
  2. download each of the simulation's files from the live site and compare size and SHA-256 with generations.json;
  3. open every live page that plays the simulation (tools/sims/registry.json) in headless Chromium and require: no page errors, the
     data file answered 200, and the page reports the file checked (sha_ok) and from that same commit.
Writes a summary to GitHub's job summary when it runs there. Exit status 0 only if all three hold.
Usage: python3 tools/sims/verify_live.py <sim> <commit> [--timeout s]"""
import argparse, hashlib, json, os, sys, time, urllib.error, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REG = json.load(open(os.path.join(ROOT, "tools/sims/registry.json")))

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)
def get(url):
    req = urllib.request.Request(url + ("&" if "?" in url else "?") + "nocache=%d" % time.time(), headers={"Cache-Control": "no-cache", "User-Agent": "scenes-verify"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("sim"); ap.add_argument("commit"); ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args(); site = REG["site"]; sc = REG["sims"].get(a.sim)
    if not sc: sys.exit(f"{a.sim} is not in tools/sims/registry.json")
    report = [f"### Live check: {a.sim}", ""]
    # 1. published?
    t0 = time.time(); e = None
    while time.time() - t0 < a.timeout:
        try:
            g = json.loads(get(site + "/data/sims/generations.json"))
            e = next((q for q in reversed(g["generations"]) if q["sim"] == a.sim and q["commit"] == a.commit), None)
        except Exception as ex: log("not yet:", ex)
        if e: break
        time.sleep(15)
    if not e: sys.exit(f"after {a.timeout} s the live generations.json still has no {a.sim} from {a.commit[:7]}")
    log(f"published after {round(time.time()-t0)} s: {e['date']}, Kaggle version {e['version']}"); report.append(f"- published on {site} after {round(time.time()-t0)} s ({e['date']}, Kaggle notebook version {e['version']})")
    # 2. files
    for f in sc["files"]:
        b = get(f"{site}/data/sims/{a.sim}/{e['date']}/{f}"); h = hashlib.sha256(b).hexdigest()
        if len(b) != e["files"][f]["bytes"] or h != e["files"][f]["sha256"]: sys.exit(f"live {f} differs from generations.json")
        log(f"{f}: {len(b)} bytes, SHA-256 matches"); report.append(f"- `{f}`: {len(b)} bytes, SHA-256 `{h[:12]}…` matches")
    # 2b. large data: every release file must answer through the site's Worker (/rel/<tag>/<file>), a byte range must come back as
    #     asked, and the total size must be the one in generations.json
    for f, meta in (e.get("release_files") or {}).items():
        req = urllib.request.Request(f"{site}/rel/{e['release']}/{f}", headers={"Range": "bytes=0-1023", "User-Agent": "scenes-verify"})
        part, cr, why = b"", "", ""
        for attempt in range(3):   # one failed answer is named and tried again; three in a row fail the check
            try:
                with urllib.request.urlopen(req, timeout=60) as r: part, cr = r.read(), r.headers.get("Content-Range", "")
                break
            except urllib.error.HTTPError as ex:
                why = f"HTTP {ex.code}, upstream {ex.headers.get('x-upstream-status', 'not given')}"; log(f"{f}: try {attempt + 1} failed ({why})"); report.append(f"- `{f}`: try {attempt + 1} failed ({why})"); time.sleep(5)
        if len(part) != min(1024, meta["bytes"]) or not cr.endswith("/%d" % meta["bytes"]): sys.exit(f"live /rel/{e['release']}/{f}: got {len(part)} bytes, Content-Range '{cr}', expected a total of {meta['bytes']} ({why})")
        log(f"{f}: served from the release through /rel/, {meta['bytes']} bytes"); report.append(f"- `{f}`: served from release `{e['release']}` through `/rel/`, {meta['bytes']} bytes, ranges work")
    # 3. pages
    from playwright.sync_api import sync_playwright
    exe = os.environ.get("CHROMIUM") or None
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=exe, args=["--no-sandbox"])
        for pgdef in sc["pages"]:
            pg = br.new_page(viewport={"width": pgdef["width"], "height": pgdef["height"]}); errs, got = [], {}
            pg.on("pageerror", lambda x: errs.append(str(x)))
            pg.on("response", lambda r: got.__setitem__(r.url.split("?")[0].split("/")[-1], r.status) if "/data/sims/" in r.url else None)
            pg.goto(site + pgdef["path"] + "?verify=%d" % time.time(), wait_until="load"); pg.evaluate(f"window.scrollTo(0,{pgdef.get('scroll',0)})")
            st = {}
            for _ in range(40):
                pg.wait_for_timeout(500); st = pg.evaluate(pgdef["probe"])
                if not st.get("waiting"): break
            br_ok = not errs and all(got.get(f) == 200 for f in sc["files"]) and st.get("sha_ok") is True and st.get("commit") == a.commit
            log(pgdef["path"], "errors", errs, "files", got, "page", st)
            report.append(f"- page `{pgdef['path']}` at {pgdef['width']} px: {'plays it' if br_ok else 'FAILED'} ({json.dumps(st)}; page errors: {len(errs)})")
            if not br_ok:
                if os.environ.get("GITHUB_STEP_SUMMARY"): open(os.environ["GITHUB_STEP_SUMMARY"], "a").write("\n".join(report) + "\n")
                sys.exit(f"page {pgdef['path']} does not play {a.sim} from {a.commit[:7]}")
        br.close()
    report.append(""); report.append("All checks passed: Kaggle → GitHub → Cloudflare → page.")
    if os.environ.get("GITHUB_STEP_SUMMARY"): open(os.environ["GITHUB_STEP_SUMMARY"], "a").write("\n".join(report) + "\n")
    log("all checks passed")

if __name__ == "__main__":
    main()

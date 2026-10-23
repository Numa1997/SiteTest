"""Browser check of the served page: 360, 390, 1024, 1440 px; KaTeX errors, page errors, horizontal overflow, each tab, each panel once.
Usage: python3 checks/check_browser.py URL [shots_dir]"""
import sys, os, json
from playwright.sync_api import sync_playwright
url = sys.argv[1]; shots = sys.argv[2] if len(sys.argv) > 2 else None
EXE = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'
ok = True
def wait_text(pg, sel, text, seconds):
    # poll from Python: the page's security policy (rightly) forbids evaluating strings, which wait_for_function would need
    for _ in range(seconds * 10):
        if pg.inner_text(sel).strip() == text: return
        pg.wait_for_timeout(100)
    raise TimeoutError(sel)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE if os.path.exists(EXE) else None)
    for w in (360, 390, 1024, 1440):
        pg = b.new_page(viewport={'width': w, 'height': 900}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.goto(url, wait_until='networkidle')
        res = {'w': w}
        res['katex_errors'] = pg.locator('.katex-error').count()
        for tab in ('sim', 'book', 'problems', 'checks'):
            pg.click('#t-' + tab); pg.wait_for_timeout(150)
            res['overflow_' + tab] = pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if shots and w in (390, 1440):
                pg.screenshot(path=f'{shots}/{tab}-{w}.png', full_page=False)
        pg.click('#t-sim')
        if w == 1440:
            pg.select_option('#tj-flow', 'potential'); pg.wait_for_timeout(500)
            res['traj'] = pg.inner_text('#tj-out')[:80]
            pg.select_option('#lk-V', '10'); pg.click('#lk-run'); wait_text(pg, '#lk-status', 'done', 60)
            res['luck'] = pg.inner_text('#lk-out')[:120]
            pg.click('#bx-run'); wait_text(pg, '#bx-status', 'done', 240)
            res['box'] = pg.inner_text('#bx-out')[:140]
            if shots: pg.locator('#box').screenshot(path=f'{shots}/panel-box.png'); pg.locator('#luck').screenshot(path=f'{shots}/panel-luck.png'); pg.locator('#traj').screenshot(path=f'{shots}/panel-traj.png')
        res['errors'] = errs
        bad = res['katex_errors'] or errs or any(res[k] > 0 for k in res if k.startswith('overflow'))
        ok &= not bad
        print(('PASS ' if not bad else 'FAIL ') + json.dumps(res, ensure_ascii=False))
    b.close()
print('BROWSER CHECK', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)

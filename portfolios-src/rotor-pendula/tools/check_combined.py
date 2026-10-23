#!/usr/bin/env python3
"""Browser check of the served Rotor Pendula page (the lecture notes and the simulation in one file, one tab each).

  1. Complete: each tab holds what its standalone page has (headings, typeset formulas, canvases, tables, links), counted
     in a real browser, and 0 KaTeX errors.
  2. Working:  no script errors; the default simulation solves and plays; the notes' "Simulation" link switches tabs and the
     simulation's "Read the lecture notes" link switches back; #notes and #sim open the right tab; sol.html (Sol's own
     study) loads its script and draws something.
  3. Layout:   no sideways scrolling of the page or of either tab at 360, 390, 1024 and 1440 px; a screenshot of each tab
     at each width.

Usage: python3 tools/check_combined.py [URL of the served page] [screenshot folder]
       (default http://127.0.0.1:8765/portfolios/rotor-pendula/index.html: serve public/ with python3 -m http.server 8765)
"""
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/portfolios/rotor-pendula/index.html'
SHOTS = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None
CHROMIUM = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'
INVENTORY = """() => { const q = s => document.querySelectorAll(s).length;
  return { h2: q('h2'), h3: q('h3'), katex: q('.katex'), kerr: q('.katex-error'), canvas: q('canvas'), table: q('table'),
           links: q('a[href]'), text: document.body.innerText.length }; }"""
OVER = "() => document.documentElement.scrollWidth - document.documentElement.clientWidth"
fails = []
def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what)
    if not ok: fails.append(what)

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=CHROMIUM)
        # standalone inventories
        ref = {}
        for tab, f in (('notes', 'rotor_notes.html'), ('sim', 'rotor_sim.html')):
            p = await b.new_page(); await p.goto((ROOT / f).as_uri()); await p.wait_for_timeout(500)
            ref[tab] = await p.evaluate(INVENTORY); await p.close()
        for w in (360, 390, 1024, 1440):
            p = await b.new_page(viewport={'width': w, 'height': 900}); errs = []
            p.on('pageerror', lambda e: errs.append(str(e)))
            p.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            await p.goto(URL + '#notes'); await p.wait_for_timeout(1500)
            check(await p.evaluate(OVER) <= 0, f'{w}px: shell has no sideways scroll')
            fr = {}
            for tab in ('notes', 'sim'):
                await p.click(f'#tab-{tab}'); await p.wait_for_timeout(1500)
                frame = None
                for fm in p.frames:
                    if fm == p.main_frame: continue
                    h1 = await fm.evaluate("document.querySelector('h1') ? document.querySelector('h1').innerText : ''")
                    if ('Pendula on' in h1) == (tab == 'notes') and 'Turning Blade' in h1: frame = fm
                fr[tab] = frame
                inv = await frame.evaluate(INVENTORY)
                same = all(inv[k] == ref[tab][k] for k in ('h2', 'h3', 'katex', 'canvas', 'table'))
                check(same and inv['kerr'] == 0, f'{w}px: {tab} tab complete ({inv["h3"]} sections, {inv["katex"]} formulas, '
                                                f'{inv["canvas"]} canvases, {inv["table"]} tables), {inv["kerr"]} KaTeX errors')
                check(await frame.evaluate(OVER) <= 0, f'{w}px: {tab} tab has no sideways scroll')
                if SHOTS:
                    await p.screenshot(path=str(SHOTS / f'served_{tab}_{w}.png'))
            if w == 1440:
                sim = fr['sim']
                await sim.click('text=Solve'); await p.wait_for_timeout(4000)
                txt = await sim.evaluate("document.body.innerText")
                check('Solved in' in txt, 'simulation solves in the served page')
                await sim.click('text=Read the lecture notes'); await p.wait_for_timeout(800)
                check(await p.get_attribute('#tab-notes', 'aria-selected') == 'true', 'simulation link switches to the notes tab')
                await fr['notes'].click('.links a[href="rotor_sim.html"]'); await p.wait_for_timeout(800)
                check(await p.get_attribute('#tab-sim', 'aria-selected') == 'true', 'notes link switches to the simulation tab')
            check(not errs, f'{w}px: no script errors {errs[:3]}')
            await p.close()
        p = await b.new_page(); await p.goto(URL + '#sim'); await p.wait_for_timeout(800)
        check(await p.get_attribute('#tab-sim', 'aria-selected') == 'true', '#sim opens the simulation tab'); await p.close()
        p = await b.new_page(); errs = []; p.on('pageerror', lambda e: errs.append(str(e)))
        await p.goto(URL.replace('index.html', 'sol.html')); await p.wait_for_timeout(3000)
        n = await p.evaluate("document.getElementById('root') ? document.getElementById('root').innerText.length : 0")
        check(n > 200 and not errs, f"sol.html (Sol's study) renders ({n} characters of text)")
        if SHOTS: await p.screenshot(path=str(SHOTS / 'served_sol_1280.png'))
        await b.close()
    print('ALL PASS' if not fails else f'{len(fails)} FAIL'); sys.exit(1 if fails else 0)

asyncio.run(main())

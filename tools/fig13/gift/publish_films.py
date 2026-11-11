"""Copy the Fig. 13 film renderers into the site, where they play live in the browser (they loop when opened without ?film=1).

    tools/fig13/gift/butterfly3d.html -> public/simulations/fig13/bell.html
    tools/fig13/gift/morph.html       -> public/simulations/fig13/turning.html   (?scene=wheel | butterfly)
    tools/fig13/gift/together.html    -> public/simulations/fig13/together.html  (the phone layout on a portrait screen)
    tools/fig13/gift/dive.html        -> public/simulations/fig13/dive.html      (phone first)
    tools/fig13/gift/reem.html, construction.html, catch.html -> live-gift.html, live-construction.html, live-catch.html, played one after
    the other, drawn live, by public/simulations/fig13/film.html and reem.html (written by film_page.py)
    plus orbit24.json and dive/dive.json, dive/dive.bin (run dive_data.py first if dive.bin is missing).

The copies are generated: edit the files in tools/fig13/gift/ and run this again. It rewrites the asset paths
(../../../public/x -> ../../x), adds the site's two security meta tags after the charset line, a link back to the Fig. 13 page
(hidden when a player shows the film), and a guard that keeps titles and captions inside their boxes when a browser translates
the page into a longer language (GUARD below; the gift, construction and catch films also fit their own captions, fitBox).

Usage: python3 tools/fig13/gift/publish_films.py
"""
import json, pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC, DST = ROOT / 'tools/fig13/gift', ROOT / 'public/simulations/fig13'
FILMS = {'butterfly3d.html': 'bell.html', 'morph.html': 'turning.html', 'together.html': 'together.html', 'dive.html': 'dive.html',
         'reem.html': 'live-gift.html', 'construction.html': 'live-construction.html', 'catch.html': 'live-catch.html'}   # the last three, live, are played in order by film.html
ref = (ROOT / 'public/simulations/flower-hunt.html').read_text().split('\n')
CSP = next(l for l in ref if 'Content-Security-Policy' in l).strip()
REF = next(l for l in ref if 'name="referrer"' in l).strip()
BACK = ('<a id="back13" href="../momentum-spirographs.html#films" style="position:fixed;left:10px;bottom:10px;z-index:9;font:13px \'IBM Plex Mono\',monospace;'
        'color:#b9a59b;background:rgba(20,13,16,.75);padding:6px 10px;border-radius:6px;text-decoration:none">← Fig. 13</a>'
        '<script>if (new URLSearchParams(location.search).get("film")) document.getElementById("back13").style.display = "none";</script>')
# Text that a browser's translation can make longer: [selector, widest it may be (stage px), tallest it may be (stage px), one line only].
# The type shrinks (to half at most) until the text is back inside; measured 11 Nov 2026 with text made 35 % and 100 % longer.
GUARD = {
    'live-gift.html': [],
    'live-construction.html': [['#h1', 1020, 0, 1]],
    'live-catch.html': [['#h1', 585, 0, 1]],                                   # the two buttons start at x = 640
    'dive.html': [['#h1', 1000, 0, 1], ['#h2', 1000, 64, 0], ['.capt', 996, 380, 0]],
    'together.html': [['#h1', 1008, 0, 1], ['#h2', 1000, 60, 0], ['#clock', 1000, 72, 0]],
    'turning.html': [['#h1', 1150, 0, 1], ['#h2', 1500, 0, 1], ['#clock', 560, 0, 1], ['#cap', 790, 0, 1]],
    'bell.html': [['#h1', 1150, 0, 1], ['#h2', 1500, 0, 1], ['#clock', 560, 0, 1]],
}
# A film's stage is 1080 or 1920 px wide but shown much smaller on a phone (about a third). Its canvas was sized stage x devicePixelRatio:
# on a phone with ratio 3 that is 3240 x 5760 px, nine times more pixels than the screen shows. The published copy caps the ratio to what
# is displayed: ?dpr=x from the player (film_page.py), or, opened by itself, the ratio times its own scale. Masters (render.cjs) are untouched.
DPR_JS = '''<script>
(function () {
    const real = window.devicePixelRatio || 1, q = +new URLSearchParams(location.search).get('dpr'), W = @W@, H = @H@;
    const cap = q > 0 ? q : Math.max(1, real * Math.min(1, innerWidth / W, innerHeight / H));
    if (cap < real) try { Object.defineProperty(window, 'devicePixelRatio', { get: () => cap, configurable: true }); } catch (e) {}
})();
</script>
'''
SIZE = {'bell.html': (1920, 1080), 'turning.html': (1920, 1080)}
GUARD_JS = '''<script>
// Added by publish_films.py: keep titles and captions inside their boxes when the page is translated (longer words).
(function () {
    const SPEC = @SPEC@, base = new Map(), seen = new Map();
    function fit() {
        for (const [sel, maxW, maxH, line] of SPEC) document.querySelectorAll(sel).forEach(el => {
            const n = el.textContent.length; if (!n || seen.get(el) === n) return; seen.set(el, n);
            if (!base.has(el)) base.set(el, parseFloat(getComputedStyle(el).fontSize));
            const b = base.get(el); let fs = b; el.style.fontSize = b + 'px'; el.style.maxWidth = maxW + 'px'; el.style.overflow = 'hidden'; if (line) el.style.whiteSpace = 'nowrap';
            while (((line && el.scrollWidth > maxW + 1) || (maxH && el.scrollHeight > maxH + 1)) && fs > b * 0.5) { fs -= 1; el.style.fontSize = fs + 'px'; }
        });
    }
    setInterval(fit, 250);
})();
</script>
'''

DST.mkdir(parents=True, exist_ok=True)
(DST / 'dive').mkdir(exist_ok=True)
for src, dst in FILMS.items():
    s = (SRC / src).read_text()
    s = s.replace('../../../public/', '../../')
    assert '../../../' not in s, src
    s = s.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n' + CSP + '\n' + REF, 1)
    if not dst.startswith('live-'): s = s.replace('<body>', '<body>\n' + BACK, 1)
    w, h = SIZE.get(dst, (1080, 1920)); assert s.count('<body>') == 1, src; s = s.replace('<body>', '<body>\n' + DPR_JS.replace('@W@', str(w)).replace('@H@', str(h)), 1)
    if GUARD[dst]: assert s.count('</body>') == 1, src; s = s.replace('</body>', GUARD_JS.replace('@SPEC@', json.dumps(GUARD[dst])) + '</body>')
    s = re.sub(r'(<!-- Film renderer)', r'<!-- Generated by tools/fig13/gift/publish_films.py from tools/fig13/gift/' + src + r'; do not edit by hand. -->\n\1', s, count=1)
    (DST / dst).write_text(s)
shutil.copy(SRC / 'orbit24.json', DST / 'orbit24.json')
for f in ('reem.json', 'pendulum.js'): shutil.copy(SRC / f, DST / f)   # the motion itself is computed live by pendulum.js
(DST / 'fonts').mkdir(exist_ok=True)
for f in ('instrument-sans-400.woff2', 'instrument-sans-500.woff2', 'OFL-InstrumentSans.txt'): shutil.copy(SRC / 'fonts' / f, DST / 'fonts' / f)
for f in ('dive.json', 'dive.bin'):
    if (SRC / 'dive' / f).exists(): shutil.copy(SRC / 'dive' / f, DST / 'dive' / f)      # dive.bin is not kept in tools/ (dive_data.py makes it); the published copy stays
    assert (DST / 'dive' / f).exists(), f
print('published', ', '.join(FILMS.values()), 'and their data to', DST.relative_to(ROOT))

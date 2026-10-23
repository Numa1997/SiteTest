#!/usr/bin/env python3
"""The Hydraulic Press Study in German and Arabic, from its English source and the tables in i18n/<lang>/.

    python3 tools/i18n/hydraulics.py            write public/portfolios/hydraulics/de.html and ar.html
    python3 tools/i18n/hydraulics.py --check    the same, and exit 1 if anything is untranslated
    python3 tools/i18n/hydraulics.py --todo de  print, as JSON, what German still lacks
    python3 tools/i18n/hydraulics.py --ingest de job.json de_job.py   store a checked translation job

The study's English source (portfolios-src/hydraulics/) is never changed. For each language the generator copies that folder to a
temporary place, translates there the two simulation pages and the four theory sources (pieces cut exactly as for the site's pages,
tables i18n/<lang>/hydraulics__<file>.json), wraps the words the pages' scripts write in _t() (tools/i18n/wrap.cjs) with their
translations in i18n/<lang>/hydraulics_strings.json, and runs the study's own tools there: build_theory.py typesets the theory, and
build_combined.py --site writes the combined page, renamed <lang>.html, into the site. Arabic frames are set right to left, their
inline styles mirrored with rtlcss, and the house font names gain Arabic letters through @font-face rules limited to the Arabic
block, so every element that asks for IBM Plex Sans, Instrument Serif or IBM Plex Mono gets Noto Naskh Arabic or Amiri for Arabic."""
import json, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

STUDY = os.path.join(B.ROOT, 'portfolios-src', 'hydraulics')
PAGES = ['hydraulic_control.html', 'hydraulic.html']
THEORY = sorted('theory/' + f for f in os.listdir(os.path.join(STUDY, 'theory')) if f.endswith('.src.html'))
TABS = {'Servo press', 'Servo', 'Ideal press', 'Ideal', 'Theory', 'Hydraulic Press Study', '← Numa Koudsie · Portfolios'}
NAME = {'de': 'Numa Koudsie', 'ar': 'نعمة سائر قدسية'}
ARABIC = 'U+0600-06FF, U+0750-077F, U+0870-088E, U+0890-0891, U+0898-08FF, U+FB50-FDFF, U+FE70-FE74, U+FE76-FEFC'

def tname(f): return 'hydraulics__' + os.path.basename(f).replace('.src.html', '').replace('.html', '') + '.json'
def load(lang, name):
    p = os.path.join(B.ROOT, 'i18n', lang, name)
    return p, (json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {})

def wrapped_strings(html):
    return [m.group(1).replace("\\'", "'") for m in re.finditer(r"(?<![\w$.])_t\('((?:[^'\\]|\\.)*)'", html)]

def panel_and_wrapped(html):
    """What the reader can see from a page's scripts: the _t('...') strings and what the page tells the data panel."""
    out = wrapped_strings(html)
    for m in re.finditer(B.PANEL_KEYS, html):
        if re.search(r'[A-Za-z]{2,}', re.sub(r'<[^>]+>', ' ', m.group(1))): out.append(m.group(1).replace("\\'", "'"))
    return out

def arabic_css():
    """Arabic letters under the house font names, and the few right-to-left rules a study frame needs."""
    faces = ''
    for fam, file, w in (('IBM Plex Sans', 'noto-naskh-arabic/noto-naskh-arabic-wght-arabic.woff2', '400 700'),
                         ('IBM Plex Mono', 'noto-naskh-arabic/noto-naskh-arabic-wght-arabic.woff2', '400 700'),
                         ('Instrument Serif', 'amiri/amiri-400-arabic.woff2', '400'),
                         ('Latin Modern Roman', 'noto-naskh-arabic/noto-naskh-arabic-wght-arabic.woff2', '400 700')):
        faces += ("@font-face{font-family:'%s';font-weight:%s;font-display:swap;src:url(../../fonts/%s) format('woff2');unicode-range:%s}"
                  % (fam, w, file, ARABIC))
    rules = ('body *:not(.katex):not(.katex *){letter-spacing:0!important}html{font-synthesis-style:none}'
             'canvas,svg,.katex{direction:ltr;unicode-bidi:isolate}body{line-height:1.8}')
    return '<style>' + faces + rules + '</style>'

def rtl_styles(html):
    """Mirror every inline <style> block with rtlcss (left and right exchanged)."""
    def one(m):
        r = subprocess.run(['npx', '--yes', B.RTLCSS, '--stdin', '--silent'], input=m.group(2), capture_output=True, text=True)
        return m.group(1) + (r.stdout if r.returncode == 0 and r.stdout.strip() else m.group(2)) + m.group(3)
    return re.sub(r'(<style[^>]*>)(.*?)(</style>)', one, html, flags=re.S)

def strings_script(table, wanted, lang):
    d = {k: (B.isolate_ar(table[k]) if lang == 'ar' else table[k]) for k in wanted if k in table}
    return ('<script src="../../scripts/i18n/strings-' + lang + '.js"></script><script>window.I18N=Object.assign(window.I18N||{},' + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + ');window._t=function(s,v){var r=window.I18N[s];'
            "if(typeof r!=='string')r=s;return v?r.replace(/\\{(\\w+)\\}/g,function(m,k){return k in v?v[k]:m}):r};</script>")

def todo(lang):
    out = {}
    for f in PAGES + THEORY + ['tools/theory_template.html']:
        _, T = load(lang, tname(f)); src = open(os.path.join(STUDY, f), encoding='utf-8').read(); p, a = B.cut(src)
        for x in [q[2] for q in p] + [q[3] for q in a]:
            k = B.key(x); e = T.get(k)
            if not (e and B.norm(e.get('src', '')) == B.norm(x) and e.get('tr')): out.setdefault(f, {})[k] = B.norm(x)
    _, S = load(lang, 'hydraulics_strings.json')
    with tempfile.TemporaryDirectory() as d:
        want = set(TABS)
        for f in PAGES:
            shutil.copy(os.path.join(STUDY, f), os.path.join(d, f))
            subprocess.run(['node', os.path.join(B.ROOT, 'tools', 'i18n', 'wrap.cjs'), os.path.join(d, f)], check=True, capture_output=True,
                           env=dict(os.environ, NODE_PATH=os.path.join(B.ROOT, 'tools', 'i18n', 'node_modules'), WRAP_ARRAYS='1'))
            want |= set(panel_and_wrapped(open(os.path.join(d, f), encoding='utf-8').read()))
    out['strings'] = {k: k for k in sorted(want) if k not in S}
    return out

def build(lang):
    tmp = tempfile.mkdtemp(prefix='hyd-' + lang + '-')
    dst = os.path.join(tmp, 'portfolios-src', 'hydraulics')
    shutil.copytree(STUDY, dst, ignore=shutil.ignore_patterns('node_modules'))
    os.symlink(os.path.join(STUDY, 'tools', 'node_modules'), os.path.join(dst, 'tools', 'node_modules'))
    _, S = load(lang, 'hydraulics_strings.json'); missing = []
    dirattr = 'rtl' if lang == 'ar' else 'ltr'
    for f in PAGES:
        p = os.path.join(dst, f)
        subprocess.run(['node', os.path.join(B.ROOT, 'tools', 'i18n', 'wrap.cjs'), p], check=True, capture_output=True,
                       env=dict(os.environ, NODE_PATH=os.path.join(B.ROOT, 'tools', 'i18n', 'node_modules'), WRAP_ARRAYS='1'))
        src = open(p, encoding='utf-8').read()
        # the Web Worker the servo page builds from its own source gets the same table
        src = src.replace("new Blob([code], { type: 'text/javascript' })",
                          "new Blob(['self.I18N=' + JSON.stringify(window.I18N || {}) + ';self._t=function(s){var r=self.I18N[s];return typeof r==\\'string\\'?r:s};', code], { type: 'text/javascript' })")
        _, T = load(lang, tname(f)); html, miss, _n = B.translate(src, lang, T); missing += [(f, m) for m in miss]
        want = panel_and_wrapped(html); missing += [(f, {'src': w}) for w in want if w not in S]
        if lang == 'ar': html = rtl_styles(html)
        head = strings_script(S, want, lang) + (arabic_css() if lang == 'ar' else '')
        # first thing in <head>: the page's own head scripts already call _t()
        html = html.replace('<html lang="en">', '<html lang="%s" dir="%s">' % (lang, dirattr), 1).replace('<head>', '<head>\n' + head, 1)
        open(p, 'w', encoding='utf-8').write(html)
    for f in THEORY:
        p = os.path.join(dst, f); src = open(p, encoding='utf-8').read()
        _, T = load(lang, tname(f)); html, miss, _n = B.translate(src, lang, T); missing += [(f, m) for m in miss]
        open(p, 'w', encoding='utf-8').write(html)
    tpl = os.path.join(dst, 'tools', 'theory_template.html'); t = open(tpl, encoding='utf-8').read()
    _, T = load(lang, tname('theory_template.html')); t, miss, _n = B.translate(t, lang, T); missing += [('theory_template.html', m) for m in miss]
    if lang == 'ar': t = rtl_styles(t)
    t = t.replace('<html lang="en">', '<html lang="%s" dir="%s">' % (lang, dirattr), 1)
    if lang == 'ar': t = t.replace('</head>', arabic_css() + '\n</head>', 1)
    open(tpl, 'w', encoding='utf-8').write(t)
    subprocess.run([sys.executable, os.path.join(dst, 'tools', 'build_theory.py')], check=True, capture_output=True)
    # the wrapper: its language, tab labels, title, back link and file name
    tr = lambda s: S.get(s, s)
    bc = os.path.join(dst, 'tools', 'build_combined.py'); c = open(bc, encoding='utf-8').read()
    for label in ('Servo press', 'Servo', 'Ideal press', 'Ideal', 'Theory'):
        c = c.replace("'%s'" % label, json.dumps(tr(label), ensure_ascii=False))
    c = c.replace('<html lang="en">', '<html lang="%s" dir="%s">' % (lang, dirattr), 1)
    c = c.replace("title='Hydraulic Press Study · Numa Koudsie'", 'title=' + json.dumps(tr('Hydraulic Press Study') + ' · ' + NAME[lang], ensure_ascii=False))
    c = c.replace('href="../../portfolios.html">← Numa Koudsie · Portfolios</a>', 'href="../../%s/portfolios.html">%s</a>' % (lang, tr('← Numa Koudsie · Portfolios')))
    c = c.replace("(folder / 'index.html')", "(folder / '%s.html')" % lang).replace("folder / 'index.html', out", "folder / '%s.html', out" % lang)
    if lang == 'ar': c = c.replace("fonts='<link rel=\"stylesheet\" href=\"../../fonts/instrument-plex.css\">'",
                                   "fonts='<link rel=\"stylesheet\" href=\"../../fonts/instrument-plex.css\"><link rel=\"stylesheet\" href=\"../../fonts/arabic.css\">'")
    open(bc, 'w', encoding='utf-8').write(c)
    r = subprocess.run([sys.executable, bc, '--site', B.ROOT], capture_output=True, text=True)
    if r.returncode: sys.exit('build_combined failed: ' + r.stderr[-800:])
    shutil.rmtree(tmp)
    return missing

def ingest(lang, job, trfile):
    """Store a checked job: job.json is {key: English} (pieces of one file, or strings keyed by the English), trfile defines TR."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('tr', trfile); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    src = json.load(open(job, encoding='utf-8')); name = re.sub(r'_\d+$', '', os.path.basename(job)[:-5])
    if name == 'strings':
        p, S = load(lang, 'hydraulics_strings.json')
        for en in src: S[en] = m.TR[en]
        json.dump(S, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True); return len(src)
    f = [x for x in PAGES + THEORY + ['tools/theory_template.html'] if os.path.basename(x).replace('.src.html', '').replace('.html', '') == name][0]
    p, T = load(lang, tname(f))
    for k, en in src.items(): T[k] = {'src': en, 'tr': m.TR[k]}
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(dict(sorted(T.items())), open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); return len(src)

def main():
    a = sys.argv[1:]
    if a[:1] == ['--ingest']:
        print(a[1], os.path.basename(a[2]), ingest(a[1], a[2], a[3]), 'stored'); return
    if a[:1] == ['--todo']:
        print(json.dumps(todo(a[1]), ensure_ascii=False, indent=1)); return
    bad = 0
    for lang in B.LANGS:
        m = build(lang); bad += len(m)
        print(f'hydraulics {lang}: {len(m)} pieces or strings not yet translated (shown in English)')
    if '--check' in a and bad: sys.exit(1)

if __name__ == '__main__':
    main()

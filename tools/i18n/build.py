#!/usr/bin/env python3
"""Phyein Usul in three languages: the English pages are the only source; this writes the German and Arabic pages.

    python3 tools/i18n/build.py                 write public/de/... and public/ar/... for every page in PAGES
    python3 tools/i18n/build.py --check         write nothing; fail (exit 1) if any piece of English has no current translation, or
                                                if a generated file on disk is not what the build would write now (its commit
                                                stamps aside, which change with every commit)
    python3 tools/i18n/build.py --todo de       print, as JSON, the English pieces that German still lacks

How it works. An English page is cut into pieces: the inner HTML of every innermost block element (p, li, h1-h6, dt, dd, td, th,
figcaption, a, button, label, summary, title, option, span.t) and the attributes alt, title, aria-label, placeholder and the content of
meta description. Each piece is keyed by a fingerprint of its English text. i18n/<lang>/<page>.json holds, per key, the English it was
translated from ("src") and the translation ("tr"). When the English changes, its fingerprint changes, the old translation no longer
matches, --check fails and names the piece, and the page shows the English with a small "translation being updated" mark until the
piece is translated again. Every generated page names the English commit it was built from.
"""
import hashlib, html, json, os, re, subprocess, sys
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
LANGS = ('de', 'ar')
NAMES = {'en': 'English', 'de': 'Deutsch', 'ar': 'العربية'}
# (source file, served path). The served path is the address under the site root; translations go to <lang>/<served path>.
PAGES = [
    ('index.html', 'index.html'),
    ('public/simulations.html', 'simulations.html'),
    ('public/portfolios.html', 'portfolios.html'),
] + [('public/simulations/' + f, 'simulations/' + f) for f in sorted(os.listdir(os.path.join(ROOT, 'public', 'simulations'))) if f.endswith('.html')]
TEXTUAL = {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'dt', 'dd', 'td', 'th', 'figcaption', 'caption', 'summary', 'title', 'option', 'button',
           'label', 'div', 'a', 'span', 'b', 'strong', 'em', 'i', 'small', 'sub', 'sup', 'q', 'cite', 'abbr', 'u', 'mark', 'output', 'legend', 'blockquote'}
SKIP = {'script', 'style', 'svg', 'code', 'pre', 'math', 'textarea', 'noscript-skip'}
ATTRS = ('alt', 'title', 'aria-label', 'placeholder')
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

def norm(s): return re.sub(r'\s+', ' ', s).strip()
def key(s): return hashlib.sha1(norm(s).encode('utf-8')).hexdigest()[:12]
def has_words(s):
    t = html.unescape(re.sub(r'<[^>]+>', ' ', s)); t = re.sub(r'\\\(.*?\\\)|\\\[.*?\\\]', '', t, flags=re.S)
    return re.search(r'[A-Za-z]{2,}', t) is not None

class Cutter(HTMLParser):
    """Finds the source offsets of every translatable piece: the outermost element that holds words directly (text that is its own
    child, not only inside its children), with all its inline markup. Elements marked translate="no" or class "notex", and scripts,
    styles, SVG and code, are left alone."""
    def __init__(self, src):
        super().__init__(convert_charrefs=False); self.src = src; self.lines = [0]
        for m in re.finditer('\n', src): self.lines.append(m.end())
        self.stack = []; self.cands = []; self.attrs = []
    def off(self): l, c = self.getpos(); return self.lines[l - 1] + c
    def frozen(self): return any(f['frozen'] for f in self.stack)
    def handle_starttag(self, tag, attrs):
        start = self.off(); end = start + len(self.get_starttag_text()); a = dict(attrs)
        frozen = self.frozen() or tag in SKIP or 'notex' in (a.get('class') or '').split() or a.get('translate') == 'no'
        if not frozen:
            for name in ATTRS:
                if a.get(name) and has_words(a[name]): self.attrs.append((start, end, name, a[name]))
            if tag == 'meta' and a.get('name') in ('description', 'author') and a.get('content'): self.attrs.append((start, end, 'content', a['content']))
        if tag in VOID: return
        self.stack.append({'tag': tag, 'inner': end, 'text': False, 'frozen': frozen})
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1]['tag'] == tag: self.stack.pop()
    def handle_data(self, data):
        if self.stack and not self.stack[-1]['frozen'] and re.search(r'[A-Za-z]{2,}', re.sub(r'\\\(.*?\\\)', '', data)): self.stack[-1]['text'] = True
    def handle_entityref(self, name): pass
    def handle_charref(self, name): pass
    def handle_endtag(self, tag):
        if tag in VOID: return
        pos = self.off()
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                fr = self.stack[i]; del self.stack[i:]
                if fr['text'] and not fr['frozen'] and tag in TEXTUAL:
                    inner = self.src[fr['inner']:pos]
                    if has_words(inner): self.cands.append((fr['inner'], pos, inner))
                return

def cut(src):
    c = Cutter(src); c.feed(src); c.close()
    # keep the outermost pieces: drop a piece that lies inside another
    ps = sorted(c.cands, key=lambda p: (p[0], -p[1])); out = []
    for p in ps:
        if out and p[0] < out[-1][1]: continue
        out.append(p)
    return out, c.attrs

CHECK = '--check' in sys.argv[1:]
STALE = []   # with --check: generated files that differ from what the build would write, commit stamps aside
STAMP = re.compile(r'(English (?:[^"]*?, )?commit )[0-9a-f]+\+?|(English commit )[0-9a-f]+\+?')   # file names may hold spaces

def put(dst, out):
    """Writes a generated file; with --check writes nothing and notes the file if its content, commit stamps aside, would change."""
    old = open(dst, encoding='utf-8').read() if os.path.exists(dst) else None
    if CHECK:
        unstamp = lambda t: STAMP.sub(lambda m: (m.group(1) or m.group(2)) + '…', t)
        if old is None or unstamp(old) != unstamp(out): STALE.append(os.path.relpath(dst, ROOT))
        return
    if old != out:
        os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'w', encoding='utf-8').write(out)

def commit(path=None):
    """The last commit that changed the English source (or the repository), with '+' when the file has uncommitted changes."""
    try:
        args = ['git', 'log', '-1', '--format=%h'] + (['--', path] if path else [])
        h = subprocess.run(args, cwd=ROOT, capture_output=True, text=True).stdout.strip() or 'unknown'
        if path and subprocess.run(['git', 'diff', '--quiet', 'HEAD', '--', path], cwd=ROOT).returncode: h += '+'
        return h
    except Exception: return 'unknown'

def table(lang, served):
    p = os.path.join(ROOT, 'i18n', lang, served.replace('/', '__') + '.json')
    return p, (json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {})

# Scripts whose words go through T('...'): every literal T('...') and every plural(n, 'one', 'many') in them needs an entry in
# i18n/<lang>/strings.json, and so does every word of the catalog (scripts/catalog.js).
SCRIPTS = ['public/scripts/fold.js', 'public/simulations.html', 'public/scripts/sim.js', 'public/scripts/datalog.js', 'public/scripts/curve.js'] + \
    ['public/simulations/' + f for f in sorted(os.listdir(os.path.join(ROOT, 'public', 'simulations'))) if f.endswith('.html')] + \
    ['public/scripts/ledger/' + f for f in sorted(os.listdir(os.path.join(ROOT, 'public', 'scripts', 'ledger'))) if f.endswith('.js')]
# The data panel shows what a page declares about its numbers (dataset title, kicker, groups, about, each variable's long_name)
# through T(), so those literals in the simulation pages are wanted too, and so are the titles and notes of a page's ledger
# (scripts/ledger/<page>.js: headline labels, sections, books), and the long names the parameter curve declares (scripts/curve.js).
PANEL_KEYS = r"\b(?:long_name|kicker|about|title|note|short)\s*:\s*'((?:[^'\\\n]|\\.)*)'"
WALK_FIELDS = ('intro', 'title', 'where', 'note')
CATALOG = 'public/scripts/catalog.js'

def wanted():
    """The English strings the scripts ask for: {english: where}."""
    out = {}
    for f in SCRIPTS:
        src = open(os.path.join(ROOT, f), encoding='utf-8').read()
        for m in re.finditer(r"(?<![\w$.])(?:_t|T)\('((?:[^'\\]|\\.)*)'", src): out.setdefault(m.group(1).replace("\\'", "'"), f)
        if f.startswith('public/simulations/') or f.startswith('public/scripts/ledger/') or f == 'public/scripts/curve.js':
            for m in re.finditer(PANEL_KEYS, src):
                if re.search(r'[A-Za-z]{2,}', re.sub(r'<[^>]+>', ' ', m.group(1))): out.setdefault(m.group(1).replace("\\'", "'"), f + ' (data panel)')
        for m in re.finditer(r"\bsliderCheck\([^,()]+, '([^']*[A-Za-z][^']*)'", src): out.setdefault(m.group(1), f + ' (slider name)')
        for m in re.finditer(r"\bplural\((?:[^()']|\([^()]*\))+?, '([^']*)', '([^']*)'\)", src): out.setdefault(m.group(2), f + ' (plural)')
    js = ("global.window = {}; require(process.argv[1]);"
          "process.stdout.write(JSON.stringify({sims: window.SIMULATIONS, fields: window.SIM_FIELDS}));")
    cat = json.loads(subprocess.run(['node', '-e', js, os.path.join(ROOT, CATALOG)], capture_output=True, text=True, check=True).stdout)
    for fl in cat['fields']: out.setdefault(fl['name'], CATALOG)
    for sm in cat['sims']:
        for k in ('title', 'subject', 'summary', 'model', 'method', 'controls'): out.setdefault(sm[k], CATALOG + ' ' + sm['id'] + '.' + k)
        for c in sm.get('concepts', []): out.setdefault(c, CATALOG + ' ' + sm['id'] + '.concepts')
    out.setdefault('Language', 'the language switch')
    return out

def strings(lang):
    p = os.path.join(ROOT, 'i18n', lang, 'strings.json')
    return (json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}), p

def walks():
    """Every walkthrough as data: {key: object}, read with Node from scripts/walk/*.js."""
    js = ("global.window = {}; const fs = require('fs'), path = require('path'); const d = process.argv[1];"
          "fs.readdirSync(d).filter(f => f.endsWith('.js')).forEach(f => require(path.join(d, f)));"
          "process.stdout.write(JSON.stringify(window.WALK));")
    return json.loads(subprocess.run(['node', '-e', js, os.path.join(ROOT, 'public', 'scripts', 'walk')], capture_output=True, text=True, check=True).stdout)

def walk_texts(w):
    """The prose of one walkthrough, in order: intro, then per step title, where, note and the meaning of each symbol."""
    out = [w['intro']] if w.get('intro') else []
    for st in w.get('steps', []):
        out += [st[f] for f in WALK_FIELDS[1:] if st.get(f)]
        out += [sy[3] for sy in st.get('syms', []) if len(sy) > 3 and sy[3]]
    return out

def write_walks(lang):
    """scripts/walk/<lang>/<key>.js: the English walkthrough with its prose taken from i18n/<lang>/walk.json; code, maths and
    symbols are copied unchanged. Returns the prose still untranslated."""
    p = os.path.join(ROOT, 'i18n', lang, 'walk.json'); W = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    tr = lambda t: (isolate_ar(W[t]) if lang == 'ar' else W[t]) if t in W else t
    missing = []
    for key, w in walks().items():
        w = json.loads(json.dumps(w))
        missing += [t for t in walk_texts(w) if t not in W]
        if w.get('intro'): w['intro'] = tr(w['intro'])
        for st in w.get('steps', []):
            for f in WALK_FIELDS[1:]:
                if st.get(f): st[f] = tr(st[f])
            for sy in st.get('syms', []):
                if len(sy) > 3 and sy[3]: sy[3] = tr(sy[3])
        dst = os.path.join(ROOT, 'public', 'scripts', 'walk', lang, key + '.js')
        put(dst, '/* Generated by tools/i18n/build.py from scripts/walk/' + key + '.js and i18n/' + lang +
            '/walk.json; do not edit. */\nwindow.WALK = window.WALK || {};\nwindow.WALK[' + json.dumps(key) + '] = ' +
            json.dumps(w, ensure_ascii=False, indent=1) + ';\n')
    return missing

def write_strings(lang):
    """public/scripts/i18n/strings-<lang>.js: the table the scripts read, the pages that exist in this language, and the site root."""
    S, _ = strings(lang)
    if lang == 'ar': S = {k: ({c: isolate_ar(w) for c, w in v.items()} if isinstance(v, dict) else isolate_ar(v)) for k, v in S.items()}
    have = {s: 1 for _, s in PAGES}
    body = ('/* Generated by tools/i18n/build.py from i18n/' + lang + '/strings.json; do not edit. English commit ' + commit() + '. */\n'
            '(function () { var me = document.currentScript;\n'
            '  window.I18N_ROOT = me ? me.src.replace(/scripts\\/i18n\\/[^\\/]*$/, \'\') : \'../\';\n'
            '  window.I18N_HAVE = ' + json.dumps(have, ensure_ascii=False) + ';\n'
            '  window.I18N_WALK = true;\n'
            '  window.I18N = ' + json.dumps(S, ensure_ascii=False, indent=0, sort_keys=True) + ';\n})();\n')
    dst = os.path.join(ROOT, 'public', 'scripts', 'i18n', 'strings-' + lang + '.js')
    put(dst, body)
    S_keys = set(S); return [(k, w) for k, w in wanted().items() if k not in S_keys]

# Arabic pages load mirrored copies of the house stylesheets (left and right exchanged), made with rtlcss from the English ones.
RTL_STYLES = ['site', 'fold', 'catalog', 'portfolio', 'paper', 'sim', 'data']
RTLCSS = 'rtlcss@4.3.0'

def write_rtl():
    for name in RTL_STYLES:
        src = os.path.join(ROOT, 'public', 'styles', name + '.css'); dst = src[:-4] + '.rtl.css'
        if not os.path.exists(src): continue
        tmp = dst + '.tmp'
        r = subprocess.run(['npx', '--yes', RTLCSS, '--silent', src, tmp], capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(tmp):
            print(f'rtlcss failed for {name}.css ({r.stderr.strip()[:200]}); keeping the old {name}.rtl.css'); continue
        out = (f'/* Generated by tools/i18n/build.py ({RTLCSS}) from {name}.css for the Arabic pages: left and right exchanged. '
               'Do not edit; edit the English stylesheet and run the generator. */\n' + open(tmp, encoding='utf-8').read()); os.remove(tmp)
        # arrows drawn by CSS point the way the text runs (rtlcss turns boxes round, not characters)
        out = re.sub(r"(content:\s*['\"])([→←])(['\"])", lambda m: m.group(1) + {'→': '←', '←': '→'}[m.group(2)] + m.group(3), out)
        put(dst, out)

# Inside Arabic text a quantity keeps its left-to-right order ("12 MPa", "1 700–2 100 cm⁻³", "±8 g"), as the brief asks: the
# generator wraps each number with its unit, and each number range, in the Unicode isolates LRI … PDI (U+2066, U+2069). They work in
# text, titles and attributes alike, and maths (\( \)), tags and text already isolated are left alone.
_NUM = r'\d[\d.]*(?:[   ]\d{3})*'
_UNIT = r'(?:%|°C?|[A-Za-zµΩ][A-Za-zµΩ/⁻⁰-⁹²³]*)'
_QTY = re.compile(r'(?<![\dA-Za-z.⁦])([±−]?' + _NUM + r'(?:\s?–\s?' + _NUM + r')?(?:\s?×\s?10[⁰-⁹⁻]+)?(?:\s?' + _UNIT + r'(?![A-Za-z\d]))|' + _NUM + r'\s?–\s?' + _NUM + r')')
def isolate_ar(t):
    parts = re.split(r'(\\\(.*?\\\)|\\\[.*?\\\]|<[^>]+>|⁦.*?⁩)', t, flags=re.S)
    return ''.join(x if re.match(r'\\\(|\\\[|<|⁦', x) else _QTY.sub('⁦\\1⁩', x) for x in parts)

def depth(served): return served.count('/')
def rebase(src, served, lang):
    """Relative addresses: shared files (styles, scripts, fonts, images, vendor) gain one '../'; pages stay in the language folder
    when that page exists in it, otherwise they point at the English page."""
    translated = {s for _, s in PAGES}
    up = '../'
    def fix(m):
        attr, q, url = m.group(1), m.group(2), m.group(3)
        if re.match(r'^(?:[a-z]+:|#|//|data:|/)', url): return m.group(0)
        path = url.split('#')[0].split('?')[0]
        here = os.path.dirname(served)
        target = os.path.normpath(os.path.join(here, path)).replace('\\', '/') if path else served
        if path and target not in translated: url = up + url
        return f'{attr}={q}{url}{q}'
    return re.sub(r'\b(href|src)=(["\'])([^"\']*)\2', fix, src)

def switcher(served, lang):
    """The three links of the language switch, relative to the page in language `lang`."""
    back = '../' * (depth(served) + (0 if lang == 'en' else 1))
    out = []
    for l in ('en', 'de', 'ar'):
        href = back + ('' if l == 'en' else l + '/') + served
        cur = ' aria-current="page"' if l == lang else ''
        la = ' lang="ar" dir="rtl"' if l == 'ar' else (' lang="de"' if l == 'de' else ' lang="en"')
        out.append(f'<a href="{href}" hreflang="{l}"{la}{cur}>{NAMES[l]}</a>')
    return ' · '.join(out)

def alternates(served, lang, site='https://phyeinusul.com/'):
    """hreflang links to the same page in every language, on one line (the English source keeps its line numbers)."""
    return ''.join(f'<link rel="alternate" hreflang="{l}" href="{site}{"" if l == "en" else l + "/"}{served}" />' for l in ('en', 'de', 'ar')) + \
        f'<link rel="alternate" hreflang="x-default" href="{site}{served}" />'

def translate(src, lang, T):
    """The text of one HTML source with every piece replaced from table T; returns (html, missing, number of pieces).
    Used for the site's pages (build) and for studies with their own builders (hydraulics.py)."""
    pieces, attrs = cut(src)
    edits = []      # (start, end, replacement)
    missing = []
    for a, b, inner in pieces:
        k = key(inner); e = T.get(k)
        if e and norm(e.get('src', '')) == norm(inner) and e.get('tr'):
            edits.append((a, b, isolate_ar(e['tr']) if lang == 'ar' else e['tr']))
        else:
            missing.append({'key': k, 'src': norm(inner)})
            edits.append((a, b, inner + '<span class="i18n-pending" title="translation being updated"></span>'))
    for a, b, name, val in attrs:
        k = key(val); e = T.get(k); tag = src[a:b]
        if e and norm(e.get('src', '')) == norm(val) and e.get('tr'):
            new = re.sub(r'(\b' + re.escape(name) + r'=)(["\'])(.*?)\2', lambda m: m.group(1) + m.group(2) + html.escape(html.unescape(isolate_ar(e['tr']) if lang == 'ar' else e['tr']), quote=True).replace('&#x27;', "'") + m.group(2), tag, count=1, flags=re.S)
            edits.append((a, b, new))
        else:
            missing.append({'key': k, 'src': norm(val), 'attr': name})
    # apply from the end; an attribute edit and a piece never overlap (attributes sit in start tags, pieces in contents)
    out = src
    for a, b, r in sorted(edits, key=lambda e: e[0], reverse=True): out = out[:a] + r + out[b:]
    return out, missing, len(pieces) + len(attrs)

def build(lang, src_file, served, report):
    src = open(os.path.join(ROOT, src_file), encoding='utf-8').read()
    tpath, T = table(lang, served)
    out, missing, npieces = translate(src, lang, T)
    out = rebase(out, served, lang)
    # a study that has its own page in this language (impact, hydraulics) opens in it (the explicit English link, hreflang="en", stays English)
    out = re.sub(r'href="([^"]*portfolios/(?:impact|hydraulics)/)index\.html((?:#[^"]*)?)"(?! hreflang="en")', lambda m: 'href="' + m.group(1) + lang + '.html' + m.group(2) + '"', out)
    if lang == 'ar': out = re.sub(r'(href="[^"]*styles/)(' + '|'.join(RTL_STYLES) + r')\.css"', r'\1\2.rtl.css"', out)
    out = re.sub(r'<html lang="en"', f'<html lang="{lang}" dir="{"rtl" if lang == "ar" else "ltr"}"', out, count=1)
    out = re.sub(r'<!--I18N-SWITCH-->.*?<!--/I18N-SWITCH-->', lambda m: switcher(served, lang), out, flags=re.S)
    out = re.sub(r'<!--I18N-ALTERNATES-->.*?<!--/I18N-ALTERNATES-->', lambda m: alternates(served, lang), out, flags=re.S)
    out = out.replace('aria-label="Language" translate="no"', 'aria-label="' + html.escape(strings(lang)[0].get('Language', 'Language')) + '" translate="no"')
    extra = ''   # styles/i18n.css comes with the English page
    if lang == 'ar': extra += '\n    <link rel="stylesheet" href="' + '../' * (depth(served) + 1) + 'fonts/arabic.css" />'
    extra += '\n    <script src="' + '../' * (depth(served) + 1) + f'scripts/i18n/strings-{lang}.js"></script>'
    out = out.replace('</head>', extra + f'\n    <meta name="translated-from" content="English {src_file}, commit {commit(src_file)}" />\n  </head>', 1)
    put(os.path.join(ROOT, 'public', lang, served), out)
    report.append((lang, served, npieces, missing))

def english(src_file, served):
    """The English page itself gets the switch and the alternates too (they are written into the source, between markers)."""
    p = os.path.join(ROOT, src_file); s = open(p, encoding='utf-8').read()
    s2 = re.sub(r'(<!--I18N-SWITCH-->).*?(<!--/I18N-SWITCH-->)', lambda m: m.group(1) + switcher(served, 'en') + m.group(2), s, flags=re.S)
    s2 = re.sub(r'(<!--I18N-ALTERNATES-->).*?(<!--/I18N-ALTERNATES-->)', lambda m: m.group(1) + alternates(served, 'en') + m.group(2), s2, flags=re.S)
    put(p, s2)

def main():
    args = sys.argv[1:]
    if args[:1] == ['--todo']:
        lang = args[1]; want = args[2:] or [s for _, s in PAGES]
        todo = {}
        for f, served in PAGES:
            if served not in want: continue
            src = open(os.path.join(ROOT, f), encoding='utf-8').read(); _, T = table(lang, served); pieces, attrs = cut(src)
            for x in [p[2] for p in pieces] + [a[3] for a in attrs]:
                k = key(x); e = T.get(k)
                if not (e and norm(e.get('src', '')) == norm(x) and e.get('tr')): todo.setdefault(served, {})[k] = norm(x)
        S, _ = strings(lang)
        todo['strings'] = {k: w for k, w in wanted().items() if k not in S}
        p = os.path.join(ROOT, 'i18n', lang, 'walk.json'); W = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
        todo['walk'] = {k: [t for t in walk_texts(w) if t not in W] for k, w in walks().items()}
        print(json.dumps(todo, ensure_ascii=False, indent=1)); return
    report = []
    smiss = {lang: write_strings(lang) for lang in LANGS}
    wmiss = {lang: write_walks(lang) for lang in LANGS}
    write_rtl()
    for f, served in PAGES:
        english(f, served)
        for lang in LANGS: build(lang, f, served, report)
    bad = 0
    for lang, served, n, miss in report:
        print(f'{lang}/{served}: {n} pieces, {len(miss)} not yet translated'); bad += len(miss)
    for lang in LANGS:
        print(f'{lang} strings: {len(wanted())} wanted, {len(smiss[lang])} not yet translated'); bad += len(smiss[lang])
        print(f'{lang} walkthrough prose: {len(wmiss[lang])} not yet translated'); bad += len(wmiss[lang])
    if CHECK and STALE:
        print(f'{len(STALE)} generated files are not what the build writes now (run python3 tools/i18n/build.py):')
        for f in STALE: print('  stale', f)
    if CHECK and (bad or STALE):
        for lang, served, n, miss in report:
            for m in miss[:400]: print(f'  missing {lang}/{served} {m["key"]}: {m["src"][:90]}')
        for lang in LANGS:
            for k, w in smiss[lang][:400]: print(f'  missing {lang} string ({w}): {k[:90]}')
        sys.exit(1)

if __name__ == '__main__':
    main()

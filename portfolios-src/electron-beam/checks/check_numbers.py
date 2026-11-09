#!/usr/bin/env python3
"""Every number quoted in the text is computed.

    python3 portfolios-src/electron-beam/checks/check_numbers.py [--text-dir DIR]

Two parts, for every chapter written in text/chNN.py:

A. Each declared number (CH["numbers"]) is recomputed through the Python reference (ref/chNN.py, or the expression's inputs) and must
   print as the very same string the build wrote, which came from the browser code (physics/chNN.js). If the strings differ the
   relative gap must stay within the module's stated tolerance, and the check says so. A number computed by a module that has no
   Python reference (ref/chNN.py) fails: a quoted number needs two independent computations.
B. Nothing else in the prose looks like a measurement. The text (section HTML, lead, figure captions) is stripped of tags, of {{...}}
   tags and of mathematics, and every remaining numeral must be one of: a whole number 0 to 10 not followed by a unit; a year 1500 to
   2099; or part of a phrase listed in CH["literals"] with its reason (a given of the problem, a quoted source value). In mathematics
   a decimal numeral or a power of ten, such as 3.70 or 10^{-9}, must be listed there too: whole numbers (the 2 in 2NA) are allowed.
   A quoted value from a source goes in literals with the source named, so a reader can see it is quoted and not computed.
"""
import html
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import eb_lib as L  # noqa: E402

UNITS = r'(?:[kMGµmnpf]?(?:m|s|g|V|eV|A|T|K|Pa|J|W|F|C|Hz|rad|sr)|%|°|mbar|torr|Torr|deg|nm|pm|mm|µm|keV|kV|mrad|h|min|ms|µs|ns)'
NUMERAL = re.compile(r'(?<![\w.{])(\d[\d,]*(?:\.\d+)?(?:\s?(?:×|x|\\times)\s?10\^?\{?[-−]?\d+\}?)?)(?![\w])')
MATH_DEC = re.compile(r'(?<![\w.{^_])\d+\.\d+|\\times\s*10\^\{?[-+]?\d+\}?|(?<![\w])10\^\{?[-+]?\d+\}?')


def strip_prose(s):
    s = s.replace('\\$', ' ')
    maths = re.findall(r'\$\$(.+?)\$\$|\$([^$]+?)\$', s, flags=re.S)
    s = re.sub(r'\$\$(.+?)\$\$', ' ', s, flags=re.S)
    s = re.sub(r'\$([^$]+?)\$', ' ', s, flags=re.S)
    s = re.sub(r'\{\{[^}]*\}\}', ' ', s)
    s = re.sub(r'<svg.*?</svg>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s), [a or b for a, b in maths]


def covered(token, context, literals):
    return any(lit in context and token in lit for lit in literals)


def scan(name, text, literals, problems):
    prose, maths = strip_prose(text)
    for m in NUMERAL.finditer(prose):
        tok = m.group(1)
        after = prose[m.end():m.end() + 12]
        ctx = prose[max(0, m.start() - 30):m.end() + 30]
        if covered(tok, ctx, literals):
            continue
        plain = tok.replace(',', '')
        if re.fullmatch(r'\d+', plain) and int(plain) <= 10 and not re.match(r'\s?' + UNITS + r'\b', after):
            continue
        if re.fullmatch(r'\d{4}', plain) and 1500 <= int(plain) <= 2099:
            continue
        problems.append('%s: numeral %r in the prose is neither computed ({{num:..}}) nor listed in CH["literals"]: ...%s...' % (name, tok, ctx.strip().replace('\n', ' ')))
    for tex in maths:
        for m in MATH_DEC.finditer(tex):
            tok = m.group(0)
            if any(tok in lit for lit in literals):
                continue
            problems.append('%s: numeral %r in maths is neither computed ({{numtex:..}}) nor listed in CH["literals"]: $%s$' % (name, tok, tex.strip()[:80]))


def check(text_dir=None):
    """Returns (ok, lines)."""
    text_dir = pathlib.Path(text_dir) if text_dir else HERE / 'text'
    out, ok = [], True
    chs = {n: L.load_chapter(n, text_dir) for n in range(L.N_CHAPTERS)}
    chs = {n: c for n, c in chs.items() if c}
    legacy = [n for n, c in chs.items() if 'legacy' in c]
    chs = {n: c for n, c in chs.items() if 'legacy' not in c}
    for n in legacy:
        out.append('SKIP  ch%02d: written before the scaffold; its numbers are @key@ placeholders filled from ref/ch%02d.py and derive/ch%02d.py '
                   '(an unresolved key raises), so part A does not apply; its typed numerals are listed by checks/list_legacy_numerals.py' % (n, n, n))
    if not chs:
        return True, ['no chapter written yet: nothing to check (PASS, vacuous)']
    js = L.Numbers(chs, 'js')
    py = L.Numbers(chs, 'py')
    return _compare(chs, js, py, out)


def _compare(chs, js, py, out):
    ok = True
    mods = {m['id']: m for m in L.node('modules')}
    for key in js.specs:
        n = int(key[2:4])
        a, b = js.text(key), py.text(key)
        sp = js.specs[key]
        if a == b:
            out.append('PASS  %s = %s  (browser = Python reference, identical)' % (key, a))
            continue
        va, vb = js.value[key], py.value[key]
        tol = (mods.get(sp.get('module', ''), {}).get('tolerance') or {'rel': 1e-12, 'abs': 0})
        if abs(va - vb) <= tol.get('abs', 0) + tol.get('rel', 0) * max(abs(va), abs(vb)):
            out.append('PASS  %s: %s (browser) vs %s (Python): differ in the last printed digit, gap %.1e within the stated tolerance' % (key, a, b, abs(va - vb) / max(abs(va), abs(vb))))
        else:
            ok = False
            out.append('FAIL  %s: browser %s, Python %s, gap %.1e exceeds the stated tolerance' % (key, a, b, abs(va - vb) / max(abs(va), abs(vb))))
    problems = []
    for n, ch in chs.items():
        lits = list((ch.get('literals') or {}).keys())
        name = 'ch%02d' % n
        scan(name + ' lead', ch.get('lead', ''), lits, problems)
        for s in ch['sections']:
            scan('%s-%s' % (name, s['id']), s['html'], lits, problems)
        for fn, f in (ch.get('figures') or {}).items():
            scan('%s figure %s' % (name, fn), f['caption'], lits, problems)
        for k, reason in (ch.get('literals') or {}).items():
            if not reason or len(reason) < 8:
                problems.append('%s: literal %r has no reason' % (name, k))
    for p in problems:
        out.append('FAIL  ' + p)
    ok &= not problems
    if not problems:
        out.append('PASS  no uncomputed numeral in the prose or maths of %d chapter(s)' % len(chs))
    return ok, out


if __name__ == '__main__':
    td = sys.argv[sys.argv.index('--text-dir') + 1] if '--text-dir' in sys.argv else None
    try:
        good, lines = check(td)
    except L.BuildError as e:
        good, lines = False, [str(e)]
    print('\n'.join(lines))
    print('NUMBER CHECK', 'PASS' if good else 'FAIL')
    sys.exit(0 if good else 1)

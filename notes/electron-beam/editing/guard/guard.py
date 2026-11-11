#!/usr/bin/env python3
"""Physics guard for project 07: what an editor must not change, compared as exact sequences.

Usage (from the repository root):
    python3 notes/electron-beam/editing/guard/guard.py ch03 5455de1 <hash>
    python3 notes/electron-beam/editing/guard/guard.py --files old.py new.py

The chapter file portfolios-src/electron-beam/text/chNN.py (or guide.py) is read at both commits and parsed with `ast`.
Every string constant is decoded (so r'''…''' and '''…''' with doubled backslashes compare equal) and read in source order.
Seven kinds are extracted and compared as exact sequences; for each kind the first difference is printed:

  markers   {{num:..}} {{eq:..}} {{fig:..}} {{figure:..}} {{sec:..}} {{numtex:..}}, %(key)s, ‹..› (ch01), @..@ and [[EQ|FIG|EX|KEY ..]] (ch02)
  maths     $$..$$, $..$, \\[..\\], \\(..\\), and [[EQ ..]]..[[/EQ]] bodies (ch02)
  code      the module with every prose string blanked: all code, dicts, lists, keys, ids, short strings (titles, labels),
            LITERALS / lit(..), SVG strings, css, ui_js, sim_html, STYLE, LABELS stay exact
  links     every <a ...>..</a> element, whole
  cites     parentheses holding a year or "et al.", <li> items of reference lists, <em>Journal</em> followed by volume/page numbers,
            <b>Sources.</b> paragraphs
  quotes    "..." and “...” in the prose after HTML tags are removed (attributes are not prose)
  numerals  digits in the prose outside markers, maths and tags (check_numbers.py is the authority; this shows where)

A prose string is a string of five or more words that is not a dict key, not SVG/CSS/JS, and not under an assignment to a name
matching LITERAL|SVG|CSS|UI_JS|SIM_HTML|STYLE|LABEL nor inside a lit(..) call. Exit code 0 if all kinds are identical, 1 otherwise.
"""
import ast
import difflib
import re
import subprocess
import sys

PROTECT_NAME = re.compile(r'(?i)literal|svg|css|ui_js|sim_html|style|label')
SVGISH = re.compile(r'<svg|<rect|<line\b|<path|<ellipse|<circle|<polyline|<marker|viewBox|stroke=|font-family|(?<!\{)\{\s*[a-z-]+\s*:[^;{}]*;|function\s*\(|=>|document\.')
TAG = re.compile(r'<[^>]+>')

MARKERS = re.compile(r'\{\{[^{}]*\}\}|%\(\w+\)s|‹[^›]*›|@[A-Za-z][\w:/|.+\-]*@|\[\[/?(?:EQ|FIG|EX|KEY)\b[^\]]*\]\]')
MATHS = re.compile(r'\$\$.*?\$\$|\\\[.*?\\\]|\\\(.*?\\\)|(?<![\\$])\$(?!\$).+?(?<!\\)\$|\[\[EQ [^\]]*\]\].*?\[\[/EQ\]\]', re.S)
LINKS = re.compile(r'<a\b[^>]*>.*?</a>', re.S)
CITES = re.compile(r'\([^()]*?(?:\b1[6-9]\d\d\b|\b20\d\d\b|et al\.)[^()]*\)|<li>.*?</li>|<em>[^<]+</em>[^.;()<]{0,40}?\d[\d,–\- ]*|'
                   r'<b>Sources\.</b>.*?</p>', re.S)
QUOTES = re.compile(r'"[^"\n]{1,600}"|“[^”]{1,600}”')
NUMERAL = re.compile(r'\d+(?:[.,]\d+)*')


def read(rev, path):
    return subprocess.run(['git', 'show', f'{rev}:{path}'], capture_output=True, text=True, check=True).stdout


def parents(tree):
    for node in ast.walk(tree):
        for ch in ast.iter_child_nodes(node):
            ch._parent = node


def protected(node):
    """True if the string node must stay exact (part of the code skeleton)."""
    p, child = getattr(node, '_parent', None), node
    while p is not None:
        if isinstance(p, ast.Dict) and child in p.keys:
            return True
        if isinstance(p, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = p.targets if isinstance(p, ast.Assign) else [p.target]
            for t in targets:
                if PROTECT_NAME.search(ast.unparse(t)):
                    return True
        if isinstance(p, ast.Call) and ast.unparse(p.func) in ('lit',):
            return True
        if isinstance(p, ast.Subscript) and child is p.slice:
            return True
        p, child = getattr(p, '_parent', None), p
    return False


def is_prose(node, s):
    if len(TAG.sub(' ', s).split()) < 5 or SVGISH.search(s):
        return False
    return not protected(node)


def strings(tree):
    """All string constants in source order (f-strings: their literal parts, with {…} for each field)."""
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if isinstance(getattr(node, '_parent', None), ast.JoinedStr):
                continue
            out.append((node.lineno, node.col_offset, node, node.value))
        elif isinstance(node, ast.JoinedStr):
            s = ''.join(v.value if isinstance(v, ast.Constant) else '{…}' for v in node.values)
            out.append((node.lineno, node.col_offset, node, s))
    out.sort(key=lambda t: (t[0], t[1]))
    return out


class Blank(ast.NodeTransformer):
    def visit_Constant(self, node):
        if isinstance(node.value, str) and is_prose(node, node.value):
            return ast.copy_location(ast.Constant('«PROSE»'), node)
        return node

    def visit_JoinedStr(self, node):
        s = ''.join(v.value if isinstance(v, ast.Constant) else '{…}' for v in node.values)
        if is_prose(node, s):
            return ast.copy_location(ast.Constant('«PROSE»'), node)
        return self.generic_visit(node)


def analyse(src):
    tree = ast.parse(src)
    parents(tree)
    S = strings(tree)
    prose = [(ln, s) for ln, _, node, s in S if is_prose(node, s)]
    allstr = [(ln, s) for ln, _, _, s in S]
    out = {k: [] for k in ('markers', 'maths', 'code', 'links', 'cites', 'quotes', 'numerals')}
    for ln, s in allstr:
        out['markers'] += [(ln, m.group()) for m in MARKERS.finditer(s)]
        out['maths'] += [(ln, m.group()) for m in MATHS.finditer(s)]
        out['links'] += [(ln, m.group()) for m in LINKS.finditer(s)]
        out['cites'] += [(ln, m.group()) for m in CITES.finditer(s)]
        bare = TAG.sub(' ', MATHS.sub(' ', s))
        out['quotes'] += [(ln, m.group()) for m in QUOTES.finditer(bare)]
    for ln, s in prose:
        bare = TAG.sub(' ', MARKERS.sub(' ', MATHS.sub(' ', s)))
        out['numerals'] += [(ln, m.group()) for m in NUMERAL.finditer(bare)]
    # code skeleton: one entry per top-level statement, prose strings blanked
    tree2 = ast.parse(src)
    parents(tree2)
    parents(tree2)
    blanked = Blank().visit(tree2)
    for stmt in blanked.body:
        out['code'].append((getattr(stmt, 'lineno', 0), ast.unparse(stmt)))
    return out


def first_diff(a, b):
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else None
        y = b[i] if i < len(b) else None
        if x is None or y is None or x[1] != y[1]:
            return i, x, y
    return None


def show(x):
    if x is None:
        return '(end of sequence)'
    ln, s = x
    s = s if len(s) <= 400 else s[:400] + ' …'
    return f'line {ln}: {s!r}'


def pinpoint(x, y):
    if x is None or y is None:
        return ''
    a, b = x[1], y[1]
    i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
    return f'    first differing character at {i}: old …{a[max(0, i-60):i+60]!r}…\n                                    new …{b[max(0, i-60):i+60]!r}…'


def compare(old_src, new_src):
    A, B = analyse(old_src), analyse(new_src)
    ok = True
    for kind in A:
        d = first_diff(A[kind], B[kind])
        n_old, n_new = len(A[kind]), len(B[kind])
        if d is None:
            print(f'{kind:9s} identical ({n_old} items)')
            continue
        ok = False
        i, x, y = d
        ops = difflib.SequenceMatcher(None, [t[1] for t in A[kind]], [t[1] for t in B[kind]], autojunk=False).get_opcodes()
        diffs = sum(1 for o in ops if o[0] != 'equal')
        print(f'{kind:9s} DIFFERENT ({n_old} -> {n_new} items, {diffs} changed runs); first at item {i}:')
        print(f'    old {show(x)}')
        print(f'    new {show(y)}')
        if kind == 'code':
            print(pinpoint(x, y))
    return ok


def main(argv):
    if argv[:1] == ['--files']:
        old, new = open(argv[1], encoding='utf-8').read(), open(argv[2], encoding='utf-8').read()
    else:
        ch, base, head = argv[:3]
        path = f'portfolios-src/electron-beam/text/{ch}.py'
        old, new = read(base, path), read(head, path)
    return 0 if compare(old, new) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

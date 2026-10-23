#!/usr/bin/env python3
"""Apply a reviewer's corrections: python3 tools/i18n/apply_review.py review.json [...]

review.json: {"<table path>": {"<key>": "<complete new translation>"}}. Page tables (key -> {src, tr}), tables keyed by the English
(strings.json, walk.json, hydraulics_strings.json) and portfolios-src/impact/text_<lang>.py are understood. A correction is taken
only if it keeps every HTML tag, maths segment, number, ⟦…⟧ marker, {placeholder} and edge space of the English; the rest is
reported and left as it was."""
import importlib.util, json, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MATH = r'\$\$.*?\$\$|\$[^$]+\$|\\\(.*?\\\)|\\\[.*?\\\]'
def maths(s): return re.findall(MATH, s, flags=re.S)
def tags(s): return [t for t in re.findall(r'</?[A-Za-z][^>]*>', re.sub(MATH, '', s, flags=re.S)) if t not in ('<bdi>', '</bdi>')]
def nums(s): return sorted(re.findall(r'\d+(?:\.\d+)?', re.sub(r'<[^>]+>|' + MATH, ' ', s, flags=re.S)))
def marks(s): return sorted(re.findall(r'⟦[^⟧]*⟧', s)) + sorted(re.findall(r'(?<![A-Za-z])\{\w+\}', s))
def same(en, tr):
    why = [n for n, f in (('tags', tags), ('maths', maths), ('numbers', nums), ('markers', marks)) if f(en) != f(tr)]
    if (en[:1] == ' ') != (tr[:1] == ' ') or (en[-1:] == ' ') != (tr[-1:] == ' '): why.append('edge space')
    return why

def text_py(path):
    spec = importlib.util.spec_from_file_location('t', path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.T

ok = bad = 0
for review in sys.argv[1:]:
    for rel, fixes in json.load(open(review, encoding='utf-8')).items():
        path = os.path.join(ROOT, rel)
        if rel.endswith('.py'):          # portfolios-src/impact/text_<lang>.py
            T = text_py(path); EN = text_py(os.path.join(os.path.dirname(path), 'text_en.py'))
            for k, v in fixes.items():
                flat = lambda x: x if isinstance(x, str) else ' '.join(flat(y) for y in x)
                shape = lambda x: 's' if isinstance(x, str) else [shape(y) for y in x]
                w = same(flat(EN[k]), flat(v)) if k in EN and shape(v) == shape(EN[k]) else ['shape']
                if w: bad += 1; print('  rejected', rel, k, w); continue
                T[k] = v; ok += 1
            lang = re.search(r'text_(\w+)\.py', rel).group(1)
            open(path, 'w', encoding='utf-8').write('T = {}\n' + ''.join('T[%r] = %s\n' % (k, json.dumps(v, ensure_ascii=False)) for k, v in T.items()))
            continue
        T = json.load(open(path, encoding='utf-8')); paged = any(isinstance(v, dict) for v in T.values())
        for k, v in fixes.items():
            if k not in T: bad += 1; print('  rejected', rel, k[:50], ['no such key']); continue
            en = T[k]['src'] if paged else k
            w = same(en, v)
            if w: bad += 1; print('  rejected', rel, k[:50], w); continue
            if paged: T[k]['tr'] = v
            else: T[k] = v
            ok += 1
        json.dump(dict(sorted(T.items())) if paged else T, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=not paged)
print(ok, 'corrections applied,', bad, 'rejected')

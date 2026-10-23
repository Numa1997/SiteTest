#!/usr/bin/env python3
"""Store translations: python3 tools/i18n/fill.py <lang> <served page> <file.py>
<file.py> defines TR = {key: translation}. The English source of each key is taken from the page as it is now, so a table entry
always records the English it was translated from."""
import importlib.util, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
lang, served, f = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location('tr', f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
src_file = dict((s, p) for p, s in B.PAGES)[served]
src = open(os.path.join(B.ROOT, src_file), encoding='utf-8').read()
pieces, attrs = B.cut(src)
eng = {B.key(x): B.norm(x) for x in [p[2] for p in pieces] + [a[3] for a in attrs]}
path, T = B.table(lang, served)
unknown = [k for k in m.TR if k not in eng]
if unknown: sys.exit('keys not on the page: ' + ', '.join(unknown))
for k, tr in m.TR.items(): T[k] = {'src': eng[k], 'tr': tr}
os.makedirs(os.path.dirname(path), exist_ok=True)
json.dump(dict(sorted(T.items())), open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(path, len(T), 'entries;', len([k for k in eng if k not in T]), 'pieces of the page still untranslated')

#!/usr/bin/env python3
"""Check translations before they are stored: python3 validate.py <todo.json> <tr.py>
todo.json is the output of tools/i18n/build.py --todo <lang>; tr.py defines PAGES = {served page: {key: translation}} and STRINGS = {English: translation}.
A translation fails if its tags (names and order), its maths (every \\( … \\) and \\[ … \\] segment, byte for byte), its ⟦…⟧ markers,
{placeholders}, or the multiset of its numbers differ from the English, or if it is empty."""
import json, re, sys, importlib.util
todo = json.load(open(sys.argv[1], encoding='utf-8'))
spec = importlib.util.spec_from_file_location('tr', sys.argv[2]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
MATH = re.compile(r'\\\(.*?\\\)|\\\[.*?\\\]', re.S)
def parts(s):
    nomath = MATH.sub(' ', s); notag = re.sub(r'<[^>]*>', ' ', nomath)
    return (re.findall(r'</?([a-zA-Z0-9]+)', s), MATH.findall(s), re.findall(r'⟦[^|⟧]*', s), sorted(re.findall(r'\{[a-z0-9_]+\}', s)),
            sorted(re.findall(r'\d+(?:[.,]\d+)?', re.sub(r'(?<=\d)[  ](?=\d{3})', '', notag).replace('−', '-'))))
bad = 0
def check(where, en, tr):
    global bad
    if not tr or not tr.strip(): print('EMPTY', where, en[:60]); bad += 1; return
    a, b = parts(en), parts(tr)
    for name, x, y in zip(('tags', 'maths', 'markers', 'placeholders', 'numbers'), a, b):
        if name == 'numbers': x = [v.replace(',', '.') for v in x]; y = [v.replace(',', '.') for v in y]
        if x != y: print('DIFF', name, where, '|', en[:70], '|', x[:8], 'vs', y[:8]); bad += 1
for page, tr in getattr(m, 'PAGES', {}).items():
    want = todo.get(page, {})
    for k, t in tr.items():
        if k not in want: print('NOT ASKED', page, k); bad += 1; continue
        check(page + ' ' + k, want[k], t)
    miss = [k for k in want if k not in tr]
    if miss: print('MISSING', page, len(miss)); bad += 1
for en, t in getattr(m, 'STRINGS', {}).items(): check('string', en, t)
print('validate:', 'OK' if not bad else f'{bad} problems'); sys.exit(1 if bad else 0)

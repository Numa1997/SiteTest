#!/usr/bin/env python3
"""Merge translations made outside the tables into them.

    python3 tools/i18n/ingest.py page <lang> <served page> <file.py>     TR = {piece key: translation}  (same as fill.py)
    python3 tools/i18n/ingest.py strings <lang> <file.py>                TR = {English: translation}: walkthrough prose goes to
                                                                         i18n/<lang>/walk.json, everything else to strings.json
Only strings the site currently asks for are stored; anything else is reported and dropped."""
import importlib.util, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

def load(f):
    spec = importlib.util.spec_from_file_location('tr', f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.TR

mode = sys.argv[1]
if mode == 'page':
    lang, served, f = sys.argv[2:5]
    sys.exit(subprocess.call([sys.executable, os.path.join(os.path.dirname(__file__), 'fill.py'), lang, served, f]))
lang, f = sys.argv[2:4]; TR = load(f)
walk_set = {t for w in B.walks().values() for t in B.walk_texts(w)}
want = B.wanted()
S, sp = B.strings(lang)
wp = os.path.join(B.ROOT, 'i18n', lang, 'walk.json'); W = json.load(open(wp, encoding='utf-8')) if os.path.exists(wp) else {}
ns = nw = 0; dropped = []
for en, tr in TR.items():
    if en in walk_set: W[en] = tr; nw += 1
    if en in want: S[en] = tr; ns += 1
    if en not in walk_set and en not in want: dropped.append(en)
json.dump(S, open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
json.dump(W, open(wp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
print(f'{lang}: {ns} strings, {nw} walkthrough texts stored; {len(dropped)} not asked for' + (': ' + '; '.join(d[:40] for d in dropped[:5]) if dropped else ''))

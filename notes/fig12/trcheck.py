"""Check translation scratch files against the English before storing them, with the same rule as tools/i18n/apply_review.py:
every HTML tag, maths segment (in order), number, ⟦…⟧ marker, {placeholder} and edge space of the English must survive.
Usage: python3 notes/fig12/trcheck.py <lang> <todo.json> tr_<lang>_fig12_page.py [tr_<lang>_fig12_portfolios.py] [tr_<lang>_fig12_strings.py]
A file whose name contains 'page' or 'portfolios' holds TR = {piece key: translation}; one with 'strings' holds TR = {English: translation}.
Prints one line per problem and the counts; exit 1 if anything fails or is missing."""
import importlib.util, json, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
src = open(os.path.join(ROOT, 'tools/i18n/apply_review.py'), encoding='utf-8').read()
ns = {}; exec(src[:src.index('def text_py')], ns); same = ns['same']
def load(f):
    spec = importlib.util.spec_from_file_location('tr', f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.TR
lang, todo = sys.argv[1], json.load(open(sys.argv[2], encoding='utf-8'))
bad = 0; total = 0; missing = 0
for f in sys.argv[3:]:
    TR = load(f); name = os.path.basename(f)
    if 'portfolios' in name: want = todo.get('portfolios.html', {})
    elif 'page' in name: want = todo.get('simulations/furuta-pendulum.html', {})
    else:
        want = {en: en for en in (todo['strings'].keys() if isinstance(todo['strings'], dict) else todo['strings'])}
        for k, v in todo.get('walk', {}).items():
            for en in v: want[en] = en
    for k, en in want.items():
        if k not in TR: missing += 1; print(f'{name}: MISSING {k[:60]}'); continue
        tr = TR[k]; total += 1
        forms = tr.values() if isinstance(tr, dict) else [tr]
        why = [x for t in forms for x in same(en, t) if x != 'markers' or '{n}' not in t]
        if why: bad += 1; print(f'{name}: BAD {k[:40]} {why}\n   en: {en[:160]}\n   tr: {str(tr)[:160]}')
    extra = [k for k in TR if k not in want]
    if extra: print(f'{name}: {len(extra)} keys not asked for (ignored by ingest)')
print(f'{lang}: {total} checked, {bad} bad, {missing} missing')
sys.exit(1 if bad or missing else 0)

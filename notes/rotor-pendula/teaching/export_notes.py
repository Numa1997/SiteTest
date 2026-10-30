"""Export the lecture notes as plain text for a blind reader: numbers filled in, tables and figure captions as text,
maths kept as TeX. Tags are removed only where '<' starts a real tag, so '4f/\\pi < G' survives.
Run from the repository root: python3 notes/rotor-pendula/teaching/export_notes.py > notes/rotor-pendula/teaching/notes_as_read_2.md"""
import json, re, html, pathlib
R = pathlib.Path('portfolios-src/rotor-pendula')
d = json.load(open(R / 'numbers.json')); N, T = d['n'], d['table']
TAG = re.compile(r'</?[a-zA-Z][^>]*>')
def table_text(h):
    h = re.sub(r'<svg.*?</svg>', '[FIGURE: drawing; its caption follows]', h, flags=re.S)
    h = re.sub(r'</t[dh]>', ' | ', h); h = re.sub(r'</tr>', '\n', h)
    return h
out = []
for f in sorted((R / 'theory').glob('*.src.html')):
    s = f.read_text()
    s = re.sub(r'\{\{n:([\w]+)\}\}', lambda m: N[m.group(1)], s)
    s = re.sub(r'\{\{table:([\w]+)\}\}', lambda m: table_text(T[m.group(1)]), s)
    s = re.sub(r'<svg.*?</svg>', '[FIGURE: drawing; its caption follows]', s, flags=re.S)
    s = re.sub(r'<(h[23])[^>]*>', '\n\n## ', s)
    s = re.sub(r'<summary>(.*?)</summary>', r'\n[folded: \1]\n', s)
    s = re.sub(r'<div class="ctag">(.*?)</div>', r'\n[\1]\n', s)
    s = re.sub(r'<(p|li|div|figcaption|details)\b[^>]*>', '\n', s)
    s = html.unescape(TAG.sub('', s))
    out.append(re.sub(r'\n\s*\n+', '\n\n', s))
text = '\n\n'.join(out)
# figure labels, numbered as tools/build_theory.py numbers them: in the order of their captions (a <figcaption> starting 'Figure {{fig:key}}.')
src = ''.join(re.sub(r'\{\{table:([\w]+)\}\}', lambda m: T[m.group(1)], f.read_text()) for f in sorted((R / 'theory').glob('*.src.html')))
FIG = {k: i + 1 for i, k in enumerate(re.findall(r'<figcaption>Figure \{\{fig:(\w+)\}\}\.', src))}
print(re.sub(r'\{\{fig:(\w+)\}\}', lambda m: str(FIG[m.group(1)]), text))

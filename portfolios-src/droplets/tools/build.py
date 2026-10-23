#!/usr/bin/env python3
"""Build the Droplet Collection study page.

    python3 tools/build.py          -> out/droplet-collection.html, a standalone page (not committed)
    python3 tools/build.py --site   -> ../../public/portfolios/droplet-collection/index.html, the page the site serves

One page, four tabs: Simulation, Textbook, Problems, Checks. The words are text/*.src.html: HTML with LaTeX
($...$ inline, $$...$$ display, \\tag{n.m} for an equation number, \\boxed{...} around a key result). Every formula
is typeset here with KaTeX 0.16.11 (tools/katex_render.cjs), the same version the site serves from vendor/katex, so
the page needs only the site's KaTeX stylesheet and no script library. {{FIG:name}} is replaced by an SVG figure
drawn by tools/figs.cjs from the model; the model itself (physics.cjs, between PHYSICS-BEGIN and PHYSICS-END) and
the stored runs (data/*.json) are inlined for the simulation tab.
"""
import html
import json
import os
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
TOOLS = HERE / 'tools'
SITE = '--site' in sys.argv


def read(p):
    return pathlib.Path(p).read_text(encoding='utf-8')


# ------------------------------------------------------------------ figures and data
figs = json.loads(subprocess.run(['node', str(TOOLS / 'figs.cjs')], capture_output=True, text=True, check=True, cwd=HERE).stdout)
raw = {p.stem: json.loads(read(p)) for p in sorted((HERE / 'data').glob('*.json'))}
# the page's data: what the live panels draw, trimmed
data = {'etab_warm': raw['etab_warm'], 'hall1980': raw['hall1980'], 'cold': raw.get('cold')}
w = raw['warm']
data['warm'] = {k: {'t': w[k]['t'], 'F40': w[k]['F40']} for k in ('thesis', 'thesisBeard', 'extended', 'extHall')}
st = raw['stochastic']
data['stoch'] = {'t100': {}, 'n': {}, 'F40': {}}
for V, runs in st['V'].items():
    data['stoch']['t100'][V] = [r['t100'] for r in runs if r['t100'] is not None]
    data['stoch']['n'][V] = len(runs)
    data['stoch']['F40'][V] = [round(sum(r['F40'][i] for r in runs) / len(runs), 5) for i in range(len(runs[0]['F40']))]
br = raw['bridge']['s16']
data['bridge'] = {'t': br['t'][:241], 'N100': br['N100'][:241]}

# ------------------------------------------------------------------ text sources
parts = {}
for name in ('book', 'problems', 'checks', 'sim'):
    files = sorted((HERE / 'text').glob(f'{name}*.src.html'))
    parts[name] = '\n'.join(read(p) for p in files)


def put_figs(s):
    def rep(m):
        if m.group(1) not in figs:
            raise SystemExit('missing figure: ' + m.group(1))
        return figs[m.group(1)]
    return re.sub(r'\{\{FIG:([\w-]+)\}\}', rep, s)


jobs = []
eq_ids = set()


def job(tex, display):
    jobs.append((tex, display))
    return f'\x00{len(jobs) - 1}\x00'


def split_top(tex):
    """Split a long display at top-level \\quad / \\qquad so it can wrap on a phone."""
    pieces, start, i, depth = [], 0, 0, 0
    while i < len(tex):
        c = tex[i]
        if c == '\\' and re.match(r'\\(left|begin)(?![A-Za-z])', tex[i:]):
            depth += 1
        elif c == '\\' and re.match(r'\\(right|end)(?![A-Za-z])', tex[i:]):
            depth -= 1
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        if depth == 0 and c == '\\':
            m = re.compile(r'\\q?quad(?![A-Za-z])').match(tex, i)
            if m:
                pieces.append(tex[start:i])
                start = i = m.end()
                continue
        i += 1
    pieces.append(tex[start:])
    return [p.strip() for p in pieces if p.strip()]


def display(m):
    tex = html.unescape(m.group(1).strip())
    tag = re.search(r'\\tag\{([^}]*)\}', tex)
    num = None
    if tag:
        num = tag.group(1)
        tex = (tex[:tag.start()] + tex[tag.end():]).strip()
    boxed = tex.startswith(r'\boxed{') and tex.endswith('}')
    if boxed:
        tex = tex[len(r'\boxed{'):-1].strip()
    pieces = [tex] if (r'\begin{' in tex) else split_top(tex)
    math = '<div class="eqs">' + ''.join(job(p, True) for p in pieces) + '</div>'
    attrs = ''
    if num:
        if num in eq_ids:
            raise SystemExit('equation number used twice: ' + num)
        eq_ids.add(num)
        attrs = f' id="eq-{num}"'
    cls = 'eqn boxed' if boxed else 'eqn'
    no = f'<span class="eqno">({num})</span>' if num else '<span class="eqno"></span>'
    return f'<div class="{cls}"{attrs}>{math}{no}</div>'


def inline(m):
    ph = job(html.unescape(m.group(1).strip()), False)
    punct = m.group(2) or ''
    return f'<span class="nobr">{ph}{punct}</span>' if punct else ph


def tex_pass(s):
    s = re.sub(r'\$\$(.+?)\$\$', display, s, flags=re.S)
    s = re.sub(r'\$([^$]+?)\$([.,:;)]?)', inline, s, flags=re.S)
    if '$' in s.replace('\\$', ''):
        raise SystemExit('unmatched $ left in the source near: ' + s[s.index('$') - 80:s.index('$') + 40])
    return s


for k in parts:
    parts[k] = tex_pass(put_figs(parts[k]))

# equation references (4.5) become links, in every tab (the math is still a placeholder here)
for k in parts:
    parts[k] = re.sub(r'\((\d+\.\d+)\)', lambda m: f'<a class="eqref" href="#eq-{m.group(1)}">({m.group(1)})</a>' if m.group(1) in eq_ids else m.group(0), parts[k])

res = subprocess.run(['node', str(TOOLS / 'katex_render.cjs')], input=json.dumps([{'tex': t, 'display': d} for t, d in jobs]),
                     capture_output=True, text=True, check=True, cwd=TOOLS)
rendered = json.loads(res.stdout)
errors = [(jobs[k][0], r['error']) for k, r in enumerate(rendered) if 'error' in r]
if errors:
    for tex, err in errors:
        print('KaTeX error:', err, '\n   in:', tex[:200])
    raise SystemExit(f'{len(errors)} formulas failed')


def place(m):
    k = int(m.group(1))
    tex, disp = jobs[k]
    label = html.escape(re.sub(r'\s+', ' ', tex), quote=True)
    return f'<span class="{"kd" if disp else "ki"}" role="img" aria-label="{label}">{rendered[k]["html"]}</span>'


for k in parts:
    parts[k] = re.sub(r'\x00(\d+)\x00', place, parts[k])

# ------------------------------------------------------------------ contents of the textbook
book = parts['book']
toc, toc_m = [], []
for m in re.finditer(r'<div class="part"><span class="part-n">([^<]+)</span><span class="part-t">([^<]+)</span></div>'
                     r'|<section id="([^"]+)" class="chapter">\s*<h2><span class="chn">([^<]+)</span>\s*([^<]+)</h2>', book):
    if m.group(1):
        toc.append(f'<li class="part-li">{m.group(1)} · {m.group(2)}</li>')
    else:
        sid, n, title = m.group(3), m.group(4), m.group(5).strip()
        toc.append(f'<li><a href="#{sid}"><span class="n">{n}</span><span>{title}</span></a></li>')
        toc_m.append(f'<li><a href="#{sid}">{n} · {title}</a></li>')
n_ch = len(re.findall(r'class="chapter"', book))
n_fig = len(re.findall(r'<figure class="fig', book))
stats = (f'<span class="chip"><b>{n_ch}</b> chapters</span><span class="chip"><b>{len(eq_ids)}</b> numbered equations</span>'
         f'<span class="chip"><b>{n_fig}</b> figures</span><span class="chip">every number computed by the model</span>')

# ------------------------------------------------------------------ assemble
tpl = read(HERE / 'template.html')
phys = read(HERE / 'physics.cjs')
phys = phys[phys.index('/*PHYSICS-BEGIN*/'):phys.index('/*PHYSICS-END*/') + len('/*PHYSICS-END*/')]
chart = read(HERE / 'chart.cjs')
chart = chart[chart.index('/*CHART-BEGIN*/'):chart.index('/*CHART-END*/') + len('/*CHART-END*/')]
out = (tpl.replace('{{PHYSICS}}', phys).replace('{{CHART}}', chart).replace('{{APP}}', read(HERE / 'app.js'))
       .replace('{{DATA_JSON}}', json.dumps(data, separators=(',', ':')).replace('</', '<\\/'))
       .replace('{{SIM}}', parts['sim']).replace('{{BOOK}}', book).replace('{{PROBLEMS}}', parts['problems'])
       .replace('{{CHECKS}}', parts['checks']).replace('{{TOC}}', '\n'.join(toc)).replace('{{TOC_MOBILE}}', '\n'.join(toc_m))
       .replace('{{STATS}}', stats))

if SITE:
    idx = read(ROOT / 'index.html')
    csp = re.search(r'<meta http-equiv="Content-Security-Policy"[^>]*/>', idx).group(0)
    port = read(ROOT / 'public' / 'portfolios.html')
    icon = re.sub(r'\s+', ' ', re.search(r'<link\s+rel="icon"\s+href="[^"]*"\s*/>', port).group(0))
    head = ('<meta charset="UTF-8" />\n    ' + csp + '\n    <meta name="referrer" content="strict-origin-when-cross-origin" />\n'
            '    <meta name="author" content="Numa Koudsie" />\n    ' + icon + '\n'
            '    <link rel="stylesheet" href="../../fonts/instrument-plex.css" />\n'
            '    <link rel="stylesheet" href="../../vendor/katex/katex.min.css" />')
    bar = '<a class="back" href="../../portfolios.html">← Numa Koudsie · Portfolios</a>'
    fn = ROOT / 'public' / 'portfolios' / 'droplet-collection' / 'index.html'
else:
    kcss = TOOLS / 'node_modules' / 'katex' / 'dist' / 'katex.min.css'
    head = ('<meta charset="UTF-8" />\n    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500'
            '&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Instrument+Serif:ital@0;1&display=swap" />\n'
            f'    <link rel="stylesheet" href="file://{kcss}" />')
    bar = '<a class="back" href="#">Droplet Collection · standalone build</a>'
    fn = HERE / 'out' / 'droplet-collection.html'
out = out.replace('{{HEAD}}', head).replace('{{BACK}}', bar)
assert '{{' not in out, re.search(r'\{\{[^}]*\}\}', out).group(0)
if SITE:
    assert 'googleapis' not in out
fn.parent.mkdir(parents=True, exist_ok=True)
fn.write_text(out, encoding='utf-8')
print(f'wrote {fn.relative_to(ROOT) if SITE else fn}: {len(out)} bytes, {n_ch} chapters, {len(eq_ids)} equations, '
      f'{n_fig} figures, {len(jobs)} formulas')

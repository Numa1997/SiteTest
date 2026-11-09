"""Builds a stand-alone preview of chapter 2 (until the scaffold's build.py lands): notes/electron-beam/ch02/preview/index.html.

    python3 notes/electron-beam/ch02/build_preview.py

Maths is typeset here with the site's KaTeX (render_math.cjs); the page links the site's stylesheets by absolute path, so serve it with
serve.py (public/ as the site root, this folder's preview/ at /__preview/)."""
import importlib.util, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..')); EB = os.path.join(ROOT, 'portfolios-src', 'electron-beam')
spec = importlib.util.spec_from_file_location('eb_text_ch02', os.path.join(EB, 'text', 'ch02.py')); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
ch = T.build(); html = ch['html']
# --- typeset
pat = re.compile(r'\\\((.*?)\\\)|\\\[(.*?)\\\]', re.S)
items = []; spans = []
for m in pat.finditer(html):
    inline = m.group(1) is not None
    items.append({'tex': (m.group(1) if inline else m.group(2)).strip(), 'display': not inline}); spans.append(m.span())
res = json.loads(subprocess.run(['node', os.path.join(HERE, 'render_math.cjs')], input=json.dumps(items), capture_output=True, text=True, check=True).stdout)
errs = [r for r in res if 'error' in r]
if errs:
    for e in errs[:10]: print('KaTeX error:', e['error'][:200], '| in:', e['tex'][:120])
    sys.exit(1)
out = []; last = 0
for (a, b), r in zip(spans, res):
    out.append(html[last:a]); out.append(r['html']); last = b
out.append(html[last:]); html = ''.join(out)
print(f'{len(items)} formulas typeset, 0 errors')
idx = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
csp = re.search(r'<meta http-equiv="Content-Security-Policy"[^>]*/?>', idx).group(0)
phys = open(os.path.join(EB, 'physics', 'ch02.js'), encoding='utf-8').read()
page = f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8">
{csp}
<meta name="referrer" content="strict-origin-when-cross-origin"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The source · chapter 2 · preview</title>
<link rel="stylesheet" href="/styles/sim.css">
<style>{ch['css']}
.paper__body {{ max-width: 1180px; }} .paper__body .psec > :not(.ebsim):not(.ptab-wrap):not(.pfig) {{ max-width: 780px; }} .paper__body .pfig, .paper__body .ptab-wrap {{ max-width: 860px; }}
.paper {{ margin-top: 24px; }} .page {{ max-width: 1240px; margin: 0 auto; padding: 24px 24px 80px; }}
</style></head><body><div class="page">{html}</div>
<script>{phys}</script>
<script>{ch['ui_js']}</script></body></html>'''
os.makedirs(os.path.join(HERE, 'preview'), exist_ok=True)
open(os.path.join(HERE, 'preview', 'index.html'), 'w', encoding='utf-8').write(page)
print('wrote', os.path.join(HERE, 'preview', 'index.html'), len(page) // 1024, 'kB')

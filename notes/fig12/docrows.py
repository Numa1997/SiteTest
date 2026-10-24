"""Fig. 12's rows in the shared docs (README, AGENTS, architecture, styles, assets, datalog rounds, walk table), with current line links.
Idempotent: replaces its own rows. Run after page edits: python3 notes/fig12/docrows.py"""
import re, os
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
def rd(p): return open(os.path.join(ROOT, p)).read()
def wr(p, s): open(os.path.join(ROOT, p), 'w').write(s)
page = rd('public/simulations/furuta-pendulum.html').split('\n')
ln = lambda pat: next(i + 1 for i, l in enumerate(page) if re.search(pat, l))
walk = rd('public/scripts/walk/furuta.js'); wl = walk.split('\n')
def upsert(p, after_pat, row, key):
    s = rd(p); lines = s.split('\n')
    lines = [l for l in lines if key not in l]
    i = next(i for i, l in enumerate(lines) if re.search(after_pat, l))
    lines.insert(i + 1, row); wr(p, '\n'.join(lines))
def sub(p, old, new):
    # wording edits made before Fig. 11 was merged; after the merge the wording counts twelve pages and is left alone
    s = rd(p)
    if new in s or old not in s: return
    wr(p, s.replace(old, new, 1))
upsert('README.md', r'^\| 11 \| Double Pendulum under Control|^\| 10 \| Wind Turbine Control' if '| 11 |' not in rd('README.md') else r'^\| 11 \| Double Pendulum under Control', '| 12 | Furuta Pendulum | [`furuta-pendulum.html`](public/simulations/furuta-pendulum.html) | [fig12-furuta-pendulum.md](docs/simulations/fig12-furuta-pendulum.md) |', 'furuta-pendulum.html`')
sub('README.md', '| `public/simulations/` | The ten simulation pages,', '| `public/simulations/` | The eleven simulation pages (Figs. 1–10 and 12),')
sub('AGENTS.md', '`simulations/*.html` (ten pages).', '`simulations/*.html` (eleven pages: Figs. 1–10 and 12).')
sub('AGENTS.md', 'Figs. 9 (driven oscillator) and 10 (wind turbine control) solve the whole run first', 'Figs. 9 (driven oscillator), 10 (wind turbine control) and 12 (Furuta pendulum) solve the whole run first')
sub('AGENTS.md', 'after its own script (all ten figures,', 'after its own script (all eleven figures,')
sub('docs/architecture.md', 'public/simulations/*.html   ten simulation pages (Figs. 1–10)', 'public/simulations/*.html   eleven simulation pages (Figs. 1–10, 12)')
sub('docs/styles.md', '(the Fig. 1–10 links;', '(the Fig. 1–10 and 12 links;')
upsert('docs/assets.md', r'^\| `wind-turbine.webp` \|', '| `furuta-pendulum.webp` | Fig. 12, Furuta Pendulum |', '`furuta-pendulum.webp`')
sub('docs/assets.md', 'All ten are lossy WebP, 800 × 500 px', 'All eleven are lossy WebP, 800 × 500 px')
r = ln(r"round: \{ time: 't_play'")
upsert('docs/scripts/datalog.md', r'^\| 11 \| two seconds of the stored run', f'| 12 | two seconds of the stored run | `t_play` | sampled | yes, in the last two seconds of the run | [L{r}](../../public/simulations/furuta-pendulum.html#L{r}) |', 'furuta-pendulum.html#L')
w = ln(r'data-walk="furuta"')
titles = [(i + 1, re.search(r"title: '([^']*)'", l).group(1)) for i, l in enumerate(wl) if re.search(r"^\s+title: '", l)]
k = next(i + 1 for i, l in enumerate(wl) if 'window.WALK.furuta' in l)
steps = ' · '.join(f'[{n} {t.split(": ", 1)[-1][0].upper() + t.split(": ", 1)[-1][1:]}](../../public/scripts/walk/furuta.js#L{i})' for n, (i, t) in enumerate(titles, 1))
size = os.path.getsize(os.path.join(ROOT, 'public/scripts/walk/furuta.js')) / 1000
upsert('docs/scripts/walk.md', r'^\| 11 \| \[pendcontrol.js\]', f'| 12 | [furuta.js](../../public/scripts/walk/furuta.js#L{k}) | `furuta` | [furuta-pendulum.html](../../public/simulations/furuta-pendulum.html#L{w}) | {len(wl)} / {size:.1f} | {len(titles)} | {steps} |', 'walk/furuta.js#L')
print('rows written: round L%d, walk L%d, %d steps' % (r, w, len(titles)))

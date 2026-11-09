"""Shared by build.py and checks/: loads the chapters, numbers equations and figures, resolves cross-references, computes every
quoted number, typesets with KaTeX, validates the contract. Standard library only (the page's JavaScript runs through bridge.cjs).

A chapter is text/chNN.py defining a dict CH (chapters 0 to 9):

    CH = {
      'title':    'A free electron in fields',                  # required
      'lead':     'one paragraph, HTML with $maths$',           # optional, shown under the chapter title
      'sections': [ {'id': 'cathode-ray', 'title': 'The cathode-ray tube', 'html': '...', 'star': False}, ... ],   # required
      'figures':  { 'tube': {'svg': '<svg viewBox=...>...</svg>', 'caption': 'text with $maths$'} },              # optional
      'numbers':  { 'lam': {'module': 'ch00', 'inputs': {'V_acc': 1e5}, 'out': 'lambda_e', 'scale': 1e12, 'sig': 3},
                    'ratio': {'expr': 'a / b', 'of': {'a': 'lam', 'b': 'other'}, 'scale': 1, 'sig': 3} },         # optional
      'literals': { '300 K': 'room temperature, a given of the problem' },                                         # optional
      'sim':      { 'module': 'ch01', 'title': '...', 'caption': '...', 'controls': [...], 'readouts': [...] },   # optional
    }

Section HTML is plain HTML (classes of paper.css: pbox, pbox--ex, ptab, prefs, star) with:
    $...$ inline maths, $$...$$ display maths (numbered c.n; put \\label{name} inside to name it, \\notag for no number); \\$ a dollar sign
    {{eq:name}} (c.n)    {{fig:name}} Figure c.n    {{sec:chNN-id}} section number     {{figure:name}} puts a declared figure here
    {{num:name}} a computed number from CH['numbers'], in the prose;  {{numtex:name}} the same inside maths
"""
import html
import importlib.util
import json
import math
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from ref import core as rcore  # noqa: E402

N_CHAPTERS = 10
TITLES = ['The goal', 'A free electron in fields', 'The source', 'Acceleration, brightness, energy spread', 'The lens', 'The spot',
          'Scan and hit', 'Detect and measure', 'The whole machine', 'What an interviewer for this role will probe']
CH_KEYS = {'title', 'lead', 'sections', 'figures', 'numbers', 'literals', 'sim'}
SEC_KEYS = {'id', 'title', 'html', 'star'}
NUM_KEYS = {'module', 'inputs', 'out', 'expr', 'of', 'scale', 'sig'}
SIM_KEYS = {'module', 'title', 'caption', 'controls', 'readouts', 'aspect', 'aspect_phone'}


class BuildError(SystemExit):
    pass


def fail(errors):
    raise BuildError('\n'.join(['BUILD FAILED, %d problem(s):' % len(errors)] + ['  - ' + e for e in errors]))


# ------------------------------------------------------------------ Node bridge
def node(cmd, payload=None):
    r = subprocess.run(['node', str(HERE / 'bridge.cjs'), cmd], input=json.dumps(payload) if payload is not None else None,
                       capture_output=True, text=True, cwd=HERE)
    if r.returncode:
        raise BuildError('bridge.cjs %s failed:\n%s' % (cmd, r.stderr[-1500:]))
    return json.loads(r.stdout)


def load_contract():
    return json.loads((HERE / 'contract.json').read_text(encoding='utf-8'))


def check_contract(contract, modules):
    """Contract against itself and against the physics modules present (physics/chNN.js). Returns a list of problems."""
    errs = []
    sym = contract['symbols']
    for k, s in sym.items():
        for f in ('meaning', 'type', 'unit', 'stage'):
            if f not in s:
                errs.append('symbol %s has no %s' % (k, f))
        if s.get('type') == 'enum' and s.get('default') not in s.get('values', []):
            errs.append('symbol %s: default not among values' % k)
        if s.get('type') in ('number', 'integer') and 'default' in s:
            lo, hi, d = s.get('min'), s.get('max'), s['default']
            if lo is not None and hi is not None and not (lo <= d <= hi):
                errs.append('symbol %s: default %r outside [%r, %r]' % (k, d, lo, hi))
            if lo is not None and hi is not None and s.get('scale') == 'log' and lo <= 0:
                errs.append('symbol %s: log scale needs min > 0' % k)
        if 'display_unit' in s and 'display_scale' not in s:
            errs.append('symbol %s: display_unit without display_scale' % k)
    for st, d in contract['stages'].items():
        for k in d['in'] + d['out']:
            if ' ' not in k and k not in sym:
                errs.append('stage %s names %s, which is not a symbol' % (st, k))
    mod_ids = set()
    for m in modules:
        mod_ids.add(m['id'])
        st = contract['stages'].get(m['id'])
        if st is None:
            errs.append('physics module %s has no stage in contract.json' % m['id'])
            continue
        if sorted(m['inputs']) != sorted(st['in']):
            errs.append('%s: inputs %s differ from the contract %s' % (m['id'], sorted(m['inputs']), sorted(st['in'])))
        if sorted(m['outputs']) != sorted(st['out']):
            errs.append('%s: outputs %s differ from the contract %s' % (m['id'], sorted(m['outputs']), sorted(st['out'])))
        for key in ('controls', 'readouts'):
            for k in (m.get('ui') or {}).get(key, []):
                if k not in sym:
                    errs.append('%s: ui.%s names %s, not a symbol' % (m['id'], key, k))
    return errs


# ------------------------------------------------------------------ loading chapters
def load_chapter(n, text_dir):
    f = pathlib.Path(text_dir) / ('ch%02d.py' % n)
    if not f.exists():
        return None
    spec = importlib.util.spec_from_file_location('eb_text_ch%02d' % n, f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ch = getattr(mod, 'CH', None)
    errs = []
    if not isinstance(ch, dict):
        fail(['%s defines no dict CH' % f.name])
    for k in set(ch) - CH_KEYS:
        errs.append('%s: unknown key %r in CH' % (f.name, k))
    if not isinstance(ch.get('title'), str):
        errs.append('%s: CH["title"] missing' % f.name)
    secs = ch.get('sections')
    if not isinstance(secs, list) or not secs:
        errs.append('%s: CH["sections"] must be a non-empty list' % f.name)
        secs = []
    seen = set()
    for s in secs:
        for k in set(s) - SEC_KEYS:
            errs.append('%s: unknown key %r in a section' % (f.name, k))
        for k in ('id', 'title', 'html'):
            if not isinstance(s.get(k), str):
                errs.append('%s: a section lacks %r' % (f.name, k))
        if s.get('id') in seen:
            errs.append('%s: section id %r used twice' % (f.name, s.get('id')))
        seen.add(s.get('id'))
        if s.get('id') and not re.fullmatch(r'[a-z][a-z0-9-]*', s['id']):
            errs.append('%s: section id %r must be lower-case letters, digits and hyphens' % (f.name, s['id']))
    for name, fg in (ch.get('figures') or {}).items():
        if not re.fullmatch(r'[a-z][a-z0-9-]*', name):
            errs.append('%s: figure name %r must be lower-case letters, digits and hyphens' % (f.name, name))
        svg = fg.get('svg', '')
        if not svg.lstrip().startswith('<svg') or 'viewBox' not in svg[:400]:
            errs.append('%s: figure %s must be an <svg> with a viewBox' % (f.name, name))
        if re.search(r'<script|<foreignObject|\son\w+\s*=|(?:href|src)\s*=\s*["\']?(?:https?:|//|data:)', svg, re.I):
            errs.append('%s: figure %s holds a script, an event handler or an outside address' % (f.name, name))
        if not fg.get('caption'):
            errs.append('%s: figure %s has no caption' % (f.name, name))
    for name, sp in (ch.get('numbers') or {}).items():
        for k in set(sp) - NUM_KEYS:
            errs.append('%s: number %s has unknown key %r' % (f.name, name, k))
        if ('module' in sp) == ('expr' in sp):
            errs.append('%s: number %s needs either module+out or expr+of' % (f.name, name))
    for k in set(ch.get('sim') or {}) - SIM_KEYS:
        errs.append('%s: unknown key %r in CH["sim"]' % (f.name, k))
    if errs:
        fail(errs)
    return ch


# ------------------------------------------------------------------ numbers
def ref_compute(mid, inputs):
    """The Python reference of a module (ref/chNN.py) on the same inputs; the contract's defaults fill the missing ones."""
    try:
        m = importlib.import_module('ref.' + mid)
    except ModuleNotFoundError:
        return {'error': 'no Python reference ref/%s.py' % mid}
    p = rcore.with_defaults(m.INPUTS, inputs)
    return {'inputs': p, 'outputs': m.compute(p)}


SAFE = {k: getattr(math, k) for k in ('sqrt', 'exp', 'log', 'log10', 'sin', 'cos', 'tan', 'atan', 'pi', 'pow', 'fabs')}


class Numbers:
    """Every {{num:...}} of the book, computed once: modules through the page's own JavaScript, expressions in Python."""

    def __init__(self, chapters, engine='js'):
        """engine 'js': modules run through the page's own JavaScript (what the build uses); 'py': through ref/chNN.py (the number check)."""
        self.engine = engine
        self.specs = {}   # 'ch01.name' -> spec
        for n, ch in chapters.items():
            for name, sp in (ch.get('numbers') or {}).items():
                self.specs['ch%02d.%s' % (n, name)] = sp
        jobs, order = [], []
        for key, sp in self.specs.items():
            if 'module' in sp:
                jobs.append({'module': sp['module'], 'inputs': sp.get('inputs', {})})
                order.append(key)
        if engine == 'js':
            res = node('compute', jobs) if jobs else []
        else:
            res = [ref_compute(j['module'], j['inputs']) for j in jobs]
        self.module_out = dict(zip(order, res))
        self.value = {}
        errs = []
        for key in self.specs:
            try:
                self.value[key] = self._eval(key, ())
            except Exception as e:  # noqa: BLE001
                errs.append('number %s: %s' % (key, e))
        if errs:
            fail(errs)

    def _eval(self, key, stack):
        if key in self.value:
            return self.value[key]
        if key in stack:
            raise ValueError('circular expression')
        sp = self.specs[key]
        if 'module' in sp:
            r = self.module_out[key]
            if 'error' in r:
                raise ValueError(r['error'])
            if sp['out'] not in r['outputs']:
                raise ValueError('module %s has no output %s' % (sp['module'], sp['out']))
            v = r['outputs'][sp['out']]
        else:
            chap = key.split('.')[0]
            env = dict(SAFE)
            for var, ref in sp['of'].items():
                full = ref if '.' in ref else chap + '.' + ref
                if full not in self.specs:
                    raise ValueError('expression uses unknown number %s' % ref)
                env[var] = self._eval(full, stack + (key,))
            v = eval(sp['expr'], {'__builtins__': {}}, env)  # noqa: S307  (author-written expressions, restricted names)
        if not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError('value %r is not a finite number' % (v,))
        return float(v)

    def shown(self, key):
        sp = self.specs[key]
        return self.value[key] * sp.get('scale', 1)

    def text(self, key, tex=False):
        sp = self.specs[key]
        f = rcore.fmt_tex if tex else rcore.fmt
        return f(self.shown(key), sp.get('sig', 3))


# ------------------------------------------------------------------ the book
LABEL = re.compile(r'\\label\{([A-Za-z][\w:-]*)\}')
REF = re.compile(r'\{\{(eq|fig|sec):([\w:-]+)\}\}')
NUMTAG = re.compile(r'\{\{(num|numtex):([\w.-]+)\}\}')
FIGTAG = re.compile(r'\{\{figure:([a-z][a-z0-9-]*)\}\}')


def sim_slot(n, ch, modmap, defaults, contract, add_job):
    """The slot for a running simulation: static markup whose controls carry data-symbol, filled by the page script."""
    spec = dict((ch or {}).get('sim') or {})
    mid = spec.get('module', 'ch%02d' % n)
    m = modmap.get(mid)
    if not m or not m.get('ui'):
        return ''
    ui = dict(m['ui'])
    ui.update({k: v for k, v in spec.items() if k in ('controls', 'readouts', 'aspect', 'aspect_phone', 'caption')})
    sym = contract['symbols']
    out = defaults[mid]
    p = out['inputs']
    ctl = []
    for k in ui['controls']:
        s = sym[k]
        lab = ('<span class="ctl__sym">%s</span> %s' % (add_job(s['tex'], False), html.escape(s['meaning']))) if s.get('tex') else html.escape(s['meaning'])
        if s['type'] == 'enum':
            opts = ''.join('<option value="%s"%s>%s</option>' % (v, ' selected' if v == s['default'] else '', v) for v in s['values'])
            ctl.append('<label class="ctl"><span class="ctl__row"><span>%s</span></span><select class="sel" data-symbol="%s">%s</select></label>' % (lab, k, opts))
        else:
            ctl.append('<label class="ctl"><span class="ctl__row"><span>%s</span><output data-for="%s"></output></span>'
                       '<input type="range" min="0" max="1000" step="1" value="500" data-symbol="%s" data-min="%r" data-max="%r" data-scale="%s" data-int="%d" aria-label="%s"></label>'
                       % (lab, k, k, s['min'], s['max'], s.get('scale', 'lin'), 1 if s['type'] == 'integer' else 0, html.escape(s['meaning'])))
    rd = []
    for k in ui['readouts']:
        s = sym[k]
        val = out['outputs'][k] if k in out['outputs'] else p.get(k)
        unit = s.get('display_unit', s['unit'])
        txt = rcore.fmt(val * s.get('display_scale', 1), 3) + ('' if unit in ('1', '') else ' ' + unit)
        rd.append('<div><dt>%s</dt><dd data-out="%s">%s</dd></div>' % (add_job(s['tex'], False) if s.get('tex') else k, k, html.escape(txt)))
    title = spec.get('title') or ui.get('title') or (contract['stages'].get(mid, {}).get('title', mid))
    cap = spec.get('caption') or ui.get('caption') or ''
    return ('<div class="eb-sim" data-module="%s" id="sim-%s" style="--ar:%s;--ar-m:%s"><p class="eb-sim__t">Simulation · %s</p>'
            '<div class="eb-sim__grid"><div class="eb-sim__stage"><canvas role="img" aria-label="%s"></canvas>'
            '<p class="eb-sim__cap">%s</p></div><div class="eb-sim__panel"><div class="eb-sim__ctls">%s</div><dl class="readouts">%s</dl></div></div>'
            '<p class="eb-sim__err" hidden></p></div>') % (mid, mid, ui.get('aspect', '16 / 9'), ui.get('aspect_phone', ui.get('aspect', '16 / 9')),
                                                           html.escape(title), html.escape(title), cap, ''.join(ctl), ''.join(rd))


def build_book(text_dir=None):
    """Returns dict: chapters (list of rendered dicts), guide_html, stats, contract, modules. Raises BuildError on any problem."""
    text_dir = pathlib.Path(text_dir) if text_dir else HERE / 'text'
    contract = load_contract()
    modules = node('modules')
    modmap = {m['id']: m for m in modules}
    errs = check_contract(contract, modules)
    if errs:
        fail(errs)
    chs = {n: load_chapter(n, text_dir) for n in range(N_CHAPTERS)}
    chs = {n: c for n, c in chs.items() if c is not None}
    defaults = dict(zip([m['id'] for m in modules], node('compute', [{'module': m['id']} for m in modules]))) if modules else {}
    nums = Numbers(chs)

    jobs, errors = [], []
    eq, fig, sec = {}, {}, {}      # name -> (label text, chapter)

    def job(tex, display):
        jobs.append((tex, display))
        return '\x00%d\x00' % (len(jobs) - 1)

    def prose(s, n, st, where, allow_display=True):
        """One string of one chapter: numbers in maths, maths, figure places, then numbers in prose."""
        s = s.replace('\\$', '\x02')

        def numkey(name):
            return name if '.' in name else 'ch%02d.%s' % (n, name)

        def numtex(m):
            if m.group(1) != 'numtex':
                return m.group(0)
            if numkey(m.group(2)) not in nums.specs:
                errors.append('%s: {{numtex:%s}} is not declared in CH["numbers"]' % (where, m.group(2)))
                return ''
            return nums.text(numkey(m.group(2)), True)

        s = NUMTAG.sub(numtex, s)

        def display(m):
            tex = html.unescape(m.group(1).strip())
            if not allow_display:
                errors.append('%s: display maths is not allowed here' % where)
                return ''
            lab = LABEL.search(tex)
            nonum = r'\notag' in tex
            tex = LABEL.sub('', tex).replace(r'\notag', '').strip()
            num = None
            if not nonum:
                st['eq'] += 1
                num = '%d.%d' % (n, st['eq'])
            idattr = ''
            if lab:
                name = lab.group(1)
                if name in eq:
                    errors.append('equation label %r used twice (%s and %s)' % (name, eq[name][1], where))
                eq[name] = (num or '', where)
                idattr = ' id="eq-%s"' % name
                if not num:
                    errors.append('%s: equation %r has a label and \\notag' % (where, name))
            if '{{num:' in tex:
                errors.append('%s: {{num:..}} inside maths; use {{numtex:..}}' % where)
            return '<div class="eqn"%s><div class="eqn__m">%s</div><span class="eqn__no">%s</span></div>' % (
                idattr, job(tex, True), '(%s)' % num if num else '')

        s = re.sub(r'\$\$(.+?)\$\$', display, s, flags=re.S)

        def inline(m):
            tex = html.unescape(m.group(1).strip())
            if '{{num:' in tex:
                errors.append('%s: {{num:..}} inside maths; use {{numtex:..}}' % where)
            ph = job(tex, False)
            return '<span class="nobr">%s%s</span>' % (ph, m.group(2)) if m.group(2) else ph

        s = re.sub(r'\$([^$]+?)\$([.,:;)]?)', inline, s, flags=re.S)
        if '$' in s:
            errors.append('%s: an unmatched $ near %r' % (where, s[max(0, s.index('$') - 40):s.index('$') + 40]))

        def figplace(m):
            name = m.group(1)
            if name not in st['figs']:
                errors.append('%s: {{figure:%s}} is not declared in CH["figures"]' % (where, name))
                return ''
            if name in st['placed']:
                errors.append('%s: figure %r placed twice' % (where, name))
                return ''
            if name in fig:
                errors.append('figure label %r used twice (%s and %s)' % (name, fig[name][1], where))
            st['fig'] += 1
            st['placed'].append(name)
            fig[name] = ('Figure %d.%d' % (n, st['fig']), where)
            return '\x03%s\x03' % name

        s = FIGTAG.sub(figplace, s)

        def numprose(m):
            if m.group(1) == 'numtex':
                return m.group(0)
            key = numkey(m.group(2))
            if key not in nums.specs:
                errors.append('%s: {{num:%s}} is not declared in CH["numbers"]' % (where, m.group(2)))
                return ''
            return '<span class="num" data-n="%s">%s</span>' % (key, nums.text(key))

        s = NUMTAG.sub(numprose, s)
        return s

    chapters = []
    guide_src = None
    if (text_dir / 'guide.py').exists():
        spec = importlib.util.spec_from_file_location('eb_text_guide', text_dir / 'guide.py')
        gm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gm)
        guide_src = gm.GUIDE
    from guide_default import GUIDE as DEFAULT_GUIDE  # noqa: E402
    gsrc = guide_src or DEFAULT_GUIDE
    gst = {'eq': 0, 'fig': 0, 'figs': {}, 'placed': []}
    guide = {k: prose(v, 0, gst, 'guide:' + k, allow_display=False) for k, v in gsrc.items()}

    toc = []
    for n in range(N_CHAPTERS):
        ch = chs.get(n)
        st = {'eq': 0, 'fig': 0, 'figs': (ch or {}).get('figures') or {}, 'placed': []}
        cid = 'ch%02d' % n
        slot_job = lambda tex, d: job(tex, d)  # noqa: E731
        if ch is None:
            body = '<p class="todo">In preparation. This chapter has not been written yet.</p>' + sim_slot(n, None, modmap, defaults, contract, slot_job)
            chapters.append({'n': n, 'id': cid, 'title': TITLES[n], 'present': False,
                             'html': '<section class="chapter chapter--todo" id="%s"><h2 class="chapter__t"><span class="chapter__n">Chapter %d</span>%s</h2>%s</section>' % (cid, n, html.escape(TITLES[n]), body)})
            toc.append({'id': cid, 'n': str(n), 'title': TITLES[n], 'subs': []})
            continue
        parts = ['<section class="chapter" id="%s"><h2 class="chapter__t"><span class="chapter__n">Chapter %d</span>%s</h2>' % (cid, n, html.escape(ch['title']))]
        if ch.get('lead'):
            parts.append('<p class="chapter__lead">%s</p>' % prose(ch['lead'], n, st, cid + ' lead'))
        subs = []
        for i, s in enumerate(ch['sections'], 1):
            sid = '%s-%s' % (cid, s['id'])
            sec[sid] = ('§%d.%d' % (n, i), cid)
            star = '<span class="star">★</span>' if s.get('star') else ''
            parts.append('<section class="psec" id="%s"><h3><span class="psec__n">%d.%d</span>%s%s</h3>%s</section>' % (
                sid, n, i, html.escape(s['title']), star, prose(s['html'], n, st, sid)))
            subs.append({'id': sid, 'n': '%d.%d' % (n, i), 'title': s['title']})
        for name in set(st['figs']) - set(st['placed']):
            errors.append('%s: figure %r is declared but never placed with {{figure:%s}}' % (cid, name, name))
        slot = sim_slot(n, ch, modmap, defaults, contract, slot_job)
        if ch.get('sim') and not slot:
            errors.append('%s: CH["sim"] names a module without physics/ui' % cid)
        parts.append(slot)
        body = '\n'.join(parts) + '</section>'
        # figures: caption through the same pass, svg left untouched
        for name in st['placed']:
            f = st['figs'][name]
            label = fig[name][0]
            cap = prose(f['caption'], n, st, '%s figure %s' % (cid, name))
            body = body.replace('\x03%s\x03' % name, '<figure class="pfig" id="fig-%s"><div class="pfig__plate">%s</div><figcaption><span class="pfig__n">%s</span>%s</figcaption></figure>'
                                % (name, f['svg'].strip(), label, cap))
        chapters.append({'n': n, 'id': cid, 'title': ch['title'], 'present': True, 'html': body})
        toc.append({'id': cid, 'n': str(n), 'title': ch['title'], 'subs': subs})

    # cross-references
    def resolve(s, where):
        def one(m):
            kind, name = m.group(1), m.group(2)
            if kind == 'eq':
                if name not in eq:
                    errors.append('%s: {{eq:%s}} is not a label' % (where, name))
                    return ''
                return '<a class="eqref" href="#eq-%s">(%s)</a>' % (name, eq[name][0])
            if kind == 'fig':
                if name not in fig:
                    errors.append('%s: {{fig:%s}} is not a placed figure' % (where, name))
                    return ''
                return '<a class="figref" href="#fig-%s">%s</a>' % (name, fig[name][0])
            if name not in sec:
                errors.append('%s: {{sec:%s}} is not a section' % (where, name))
                return ''
            return '<a class="secref" href="#%s">%s</a>' % (name, sec[name][0])
        return REF.sub(one, s)

    for c in chapters:
        c['html'] = resolve(c['html'], c['id'])
    guide = {k: resolve(v, 'guide') for k, v in guide.items()}
    if errors:
        fail(errors)

    # KaTeX, with the site's own copy
    res = node('katex', [{'tex': t, 'display': d} for t, d in jobs]) if jobs else []
    bad = [(jobs[i][0], r['error']) for i, r in enumerate(res) if 'error' in r]
    if bad:
        fail(['KaTeX: %s   in: %s' % (e, t[:160]) for t, e in bad])

    def place(s):
        def one(m):
            k = int(m.group(1))
            tex, disp = jobs[k]
            label = html.escape(re.sub(r'\s+', ' ', tex), quote=True)
            return '<span class="%s" role="img" aria-label="%s">%s</span>' % ('kd' if disp else 'ki', label, res[k]['html'])
        return re.sub(r'\x00(\d+)\x00', one, s).replace('\x02', '$')

    for c in chapters:
        c['html'] = place(c['html'])
    guide = {k: place(v) for k, v in guide.items()}
    stats = {'chapters_present': sum(1 for c in chapters if c['present']), 'equations': len(eq), 'figures': len(fig),
             'numbers': len(nums.specs), 'formulas': len(jobs)}
    return {'chapters': chapters, 'guide': guide, 'toc': toc, 'stats': stats, 'contract': contract, 'modules': modules,
            'numbers': nums, 'labels': {'eq': eq, 'fig': fig, 'sec': sec}}

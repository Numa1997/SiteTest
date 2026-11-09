#!/usr/bin/env python3
"""Self-test of the scaffold: the build must accept the good fixture and refuse each bad one for the right reason.

    python3 portfolios-src/electron-beam/checks/selftest.py

Good fixture (checks/fixtures/good/ch00.py) uses every feature of the chapter format. The bad ones differ from it by one edit:
a doubled equation label, a reference to an unknown label, and a formula KaTeX cannot typeset. Also: an undeclared figure, a figure
never placed, an SVG with a script, a chapter key that does not exist, and a contract symbol the physics module does not read.
"""
import copy
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import eb_lib as L  # noqa: E402

FIX = HERE / 'checks' / 'fixtures'
ok = True


def expect_fail(name, text_dir, needle):
    global ok
    try:
        L.build_book(text_dir)
    except L.BuildError as e:
        good = needle in str(e)
        ok &= good
        print(('PASS ' if good else 'FAIL ') + name + ': refused' + ('' if good else ' for another reason: ' + str(e)[:300]))
        return
    ok = False
    print('FAIL %s: the build accepted it' % name)


b = L.build_book(FIX / 'good')
st = b['stats']
g = (st['chapters_present'] == 1 and st['equations'] == 2 and st['figures'] == 1 and st['numbers'] == 6)
ok &= g
print(('PASS ' if g else 'FAIL ') + 'good fixture builds: %r' % st)
html0 = b['chapters'][0]['html']
for label, cond in [
    ('equation 0.1 numbered and linked', '(0.1)' in html0 and 'href="#eq-abbe"' in html0),
    ('figure referenced as Figure 0.1', 'Figure 0.1' in html0 and 'href="#fig-ruler"' in html0),
    ('section reference §0.1', '§0.1' in html0),
    ('numbers wrapped for the number check', 'class="num" data-n="ch00.lam_e"' in html0),
    ('escaped dollar kept', 'The cost is a dollar: $5.' in html0),
    ('KaTeX output present, no error span', 'class="katex"' in html0 and 'katex-error' not in html0),
    ('sim slot present with data-symbol', 'class="eb-sim"' in html0 and 'data-symbol="V_acc"' in html0),
]:
    ok &= cond
    print(('PASS ' if cond else 'FAIL ') + label)

expect_fail('doubled equation label', FIX / 'bad_dup_label', "equation label 'abbe' used twice")
expect_fail('unknown equation reference', FIX / 'bad_unknown_ref', '{{eq:nosuch}} is not a label')
expect_fail('KaTeX error', FIX / 'bad_katex', 'KaTeX:')

# in-memory variants of the good chapter: write them to a scratch folder
import importlib.util, tempfile  # noqa: E402,E401
spec = importlib.util.spec_from_file_location('fx', FIX / 'good' / 'ch00.py')
fx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)
with tempfile.TemporaryDirectory() as tmp:
    def variant(name, mutate, needle):
        ch = copy.deepcopy(fx.CH)
        mutate(ch)
        d = pathlib.Path(tmp) / name
        d.mkdir()
        (d / 'ch00.py').write_text('CH = %r\n' % (ch,), encoding='utf-8')
        expect_fail(name, d, needle)

    variant('unplaced figure', lambda c: c['sections'][0].update(html=c['sections'][0]['html'].replace('{{figure:ruler}}', '')), 'never placed')
    variant('undeclared figure', lambda c: c['figures'].clear(), 'is not declared in CH["figures"]')
    variant('svg with script', lambda c: c['figures']['ruler'].update(svg='<svg viewBox="0 0 1 1"><script>1</script></svg>'), 'script')
    variant('unknown chapter key', lambda c: c.update(colour='red'), "unknown key 'colour'")
    variant('unknown number', lambda c: c['sections'][0].update(html=c['sections'][0]['html'] + '{{num:nope}}'), '{{num:nope}} is not declared')
    variant('number inside maths', lambda c: c['sections'][0].update(html=c['sections'][0]['html'] + '$x={{num:lam_e}}$'), 'inside maths')
    variant('unmatched dollar', lambda c: c['sections'][0].update(html=c['sections'][0]['html'] + '<p>cost $5</p>'), 'unmatched $')
    variant('module without ui for sim', lambda c: c.update(sim={'module': 'ch99'}), 'without physics/ui')

# the number check: the good fixture passes; a measurement typed into the prose or a decimal in maths does not
sys.path.insert(0, str(HERE / 'checks'))
import check_numbers as CN  # noqa: E402
good_n, _ = CN.check(FIX / 'good')
ok &= good_n
print(('PASS ' if good_n else 'FAIL ') + 'number check accepts the good fixture')
with tempfile.TemporaryDirectory() as tmp2:
    for name, extra, needle in [('typed number', '<p>The wavelength is 3.7 pm.</p>', "numeral '3.7'"),
                                ('typed number with exponent', '<p>That is 3.7 × 10⁻¹¹ m.</p>', 'numeral'),
                                ('decimal in maths', '<p>so $x = 3.14$ here</p>', "numeral '3.14' in maths"),
                                ('whole number with a unit', '<p>at 100 kV</p>', "numeral '100'")]:
        ch = copy.deepcopy(fx.CH)
        ch['sections'][0]['html'] += extra
        d = pathlib.Path(tmp2) / name.replace(' ', '_')
        d.mkdir()
        (d / 'ch00.py').write_text('CH = %r\n' % (ch,), encoding='utf-8')
        g, lines = CN.check(d)
        hit = (not g) and any(needle in l for l in lines)
        ok &= hit
        print(('PASS ' if hit else 'FAIL ') + 'number check refuses: ' + name)
    ch = copy.deepcopy(fx.CH)
    ch['sections'][0]['html'] += '<p>at 100 kV</p>'
    ch['literals'] = {'100 kV': 'the acceleration voltage of the worked example'}
    d = pathlib.Path(tmp2) / 'listed'
    d.mkdir()
    (d / 'ch00.py').write_text('CH = %r\n' % (ch,), encoding='utf-8')
    g, _ = CN.check(d)
    ok &= g
    print(('PASS ' if g else 'FAIL ') + 'number check accepts the same numeral once listed in literals with a reason')

# the contract against a physics module that disagrees
c = L.load_contract()
mods = [{'id': 'ch00', 'inputs': ['V_acc', 'NA', 'w_feat'], 'outputs': ['lambda_e'], 'ui': None}]
errs = L.check_contract(c, mods)
bad = any('inputs' in e for e in errs) and any('outputs' in e for e in errs)
ok &= bad
print(('PASS ' if bad else 'FAIL ') + 'contract disagreement caught (%d problems)' % len(errs))
print('SELFTEST', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)

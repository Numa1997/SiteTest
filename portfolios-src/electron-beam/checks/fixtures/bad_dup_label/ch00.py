"""Fixture for checks/selftest.py: a chapter that uses every feature of the chapter format. Not part of the project text."""
SVG = ('<svg viewBox="0 0 300 80" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="40" x2="290" y2="40" stroke="#3a322e"/>'
       '<text x="12" y="30" class="lbl">light</text><circle cx="250" cy="40" r="4" class="acc"/></svg>')
CH = {
    'title': 'Fixture: why electrons',
    'lead': 'Light of wavelength $\\lambda_\\mathrm{opt}$ meets a feature of width $w$.',
    'sections': [
        {'id': 'abbe', 'title': 'The Abbe limit',
         'html': ('<p>Light resolves a half-pitch $d_\\mathrm{opt}=\\lambda_\\mathrm{opt}/(2\\,\\mathrm{NA})$. For {{num:lam_opt}} nm and NA = {{num:na}} this is '
                  '{{num:d_opt}} nm, see {{eq:abbe}} and {{fig:ruler}}.</p>'
                  '$$ d_\\mathrm{opt}=\\frac{\\lambda_\\mathrm{opt}}{2\\,\\mathrm{NA}} \\label{abbe} $$'
                  '{{figure:ruler}}<p>The cost is a dollar: \\$5.</p>')},
        {'id': 'electron', 'title': 'The electron wavelength', 'star': True,
         'html': ('<p>At $V=100$ kV the wavelength is {{num:lam_e}} pm (section {{sec:ch00-abbe}}).</p>'
                  '$$ \\lambda=\\frac{h}{\\sqrt{2meV\\left(1+\\frac{eV}{2mc^2}\\right)}}\\label{abbe} $$'
                  '<p>With $V = {{numtex:v_kv}}$ kV, {{eq:lam}} gives {{num:lam_e}} pm; the ratio to the light wavelength is {{num:ratio}}.</p>')},
    ],
    'figures': {'ruler': {'svg': SVG, 'caption': 'A ruler: the light and a feature, $w = 10$ nm.'}},
    'numbers': {
        'lam_opt': {'module': 'ch00', 'inputs': {}, 'out': 'd_opt', 'scale': 1e9, 'sig': 3},
        'na': {'expr': '0.95', 'of': {}, 'sig': 2},
        'd_opt': {'module': 'ch00', 'inputs': {}, 'out': 'd_opt', 'scale': 1e9, 'sig': 3},
        'lam_e': {'module': 'ch00', 'inputs': {'V_acc': 1e5}, 'out': 'lambda_e', 'scale': 1e12, 'sig': 3},
        'v_kv': {'expr': '1e5 / 1e3', 'of': {}, 'sig': 3},
        'ratio': {'expr': 'a / b', 'of': {'a': 'lam_e', 'b': 'lam_opt'}, 'sig': 3},
    },
    'sim': {'module': 'ch00', 'title': 'Light and electron on one ruler'},
}

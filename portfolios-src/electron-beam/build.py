#!/usr/bin/env python3
"""Build The Electron Beam, from Tip to Measurement (project 07).

    python3 portfolios-src/electron-beam/build.py          -> portfolios-src/electron-beam/out/index.html, stand-alone (links ../../../public/...)
    python3 portfolios-src/electron-beam/build.py --site   -> public/portfolios/electron-beam/index.html, the page the site serves
    options: --text-dir DIR (chapters from another folder, used by the self-test), --out FILE

One page, chapters 0 to 9 from text/chNN.py (see eb_lib.py for the chapter format). A missing chapter is a placeholder "in
preparation", so the page builds from the first day. Equations and figures are numbered here and the build fails on an unknown or
doubled label, an undeclared or unplaced figure, a KaTeX error, or a contract that disagrees with a physics module. Mathematics is
typeset here with the site's own KaTeX 0.16.11 (public/vendor/katex, through bridge.cjs). The physics (physics/core.js and
physics/chNN.js) and the page script (app.js) are inlined; nothing is loaded from outside the site.
"""
import html
import json
import pathlib
import re
import sys

import eb_lib as L

HERE, ROOT = L.HERE, L.ROOT
SITE = '--site' in sys.argv


def opt(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


def read(p):
    return pathlib.Path(p).read_text(encoding='utf-8')


def main():
    book = L.build_book(opt('--text-dir'))
    st = book['stats']
    base = '../../' if SITE else '../../../public/'

    # head: charset first, then the site's security policy and referrer rule (the site's pages all do this)
    idx = read(ROOT / 'index.html')
    csp = re.search(r'<meta http-equiv="Content-Security-Policy"[^>]*/>', idx).group(0)
    icon = re.sub(r'\s+', ' ', re.search(r'<link\s+rel="icon"\s+href="[^"]*"\s*/>', read(ROOT / 'public' / 'portfolios.html')).group(0))
    desc = ('Lecture notes and simulations that follow an electron from a field-emission tip to a measured line width on a wafer: '
            'field emission, acceleration, a magnetic lens, the spot, scattering in the wafer, noise and tolerance.')
    abstract = ('Why does anyone build an electron beam, and what must the machine deliver? Chips have features a few nanometres wide and '
                'one defect can kill a chip, so every step is inspected and measured. Light cannot resolve such features; the electron '
                'wavelength at kilovolt energies is picometres. The beam is a probe scanned over the wafer, and what comes back gives '
                'edge position, height and material. The machine must give a spot thinner than the feature, enough current for a clean '
                'picture, a beam gentle enough for fragile resist, and speed, and these demands trade against each other. '
                'The chapters expose those trade-offs one by one.')
    head = ('    <meta charset="UTF-8" />\n    ' + (csp if SITE else '') + ('\n' if SITE else '') +
            '    <meta name="referrer" content="strict-origin-when-cross-origin" />\n'
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
            '    <title>The Electron Beam, from Tip to Measurement · Numa Koudsie</title>\n'
            '    <meta name="description" content="%s" />\n    <meta name="author" content="Numa Koudsie" />\n    <meta name="theme-color" content="#f5f1ea" />\n'
            '    %s\n'
            '    <link rel="preload" href="%sfonts/instrument-serif/instrument-serif-400-latin.woff2" as="font" type="font/woff2" crossorigin />\n'
            '    <link rel="stylesheet" href="%sfonts/instrument-plex.css" />\n'
            '    <link rel="stylesheet" href="%svendor/katex/katex.min.css" />\n'
            '    <link rel="stylesheet" href="%sstyles/paper.css" />') % (html.escape(desc, quote=True), icon, base, base, base, base)

    toc = []
    for t in book['toc']:
        subs = ''.join('<li><a href="#%s"><span>%s</span>%s</a></li>' % (s['id'], s['n'], html.escape(s['title'])) for s in t['subs'])
        toc.append('<li><a href="#%s" data-ch="%s"><span>%s</span>%s</a>%s</li>' % (
            t['id'], t['id'], t['n'], html.escape(t['title']), '<ol class="toc-sub">%s</ol>' % subs if subs else ''))

    modules = book['modules']
    modjs = '\n'.join(read(HERE / m['file']) for m in modules)
    chapters = '\n'.join(c['html'] for c in book['chapters'])
    status = ('%d of %d chapters written · %d numbered equations · %d figures · %d computed numbers · %d simulations running in the page. '
              'Chapters that are not written yet show as “in preparation”.') % (
        st['chapters_present'], L.N_CHAPTERS, st['equations'], st['figures'], st['numbers'], sum(1 for m in modules if m['ui']))

    logo = '<a href="%sindex.html" aria-label="Phyein Usul, home page"><img src="%simages/phyein-usul-mark.svg" alt="Phyein Usul" width="87" height="48" /></a>' % (base, base)
    out = read(HERE / 'template.html')
    rep = {'HEAD': head, 'LOGO': logo, 'BASE': base, 'ABSTRACT': abstract, 'G_SHOWS': book['guide']['shows'], 'G_MODELS': book['guide']['models'],
           'G_LEAVES': book['guide']['leaves_out'], 'G_NUMBERS': book['guide']['numbers'], 'STATUS': html.escape(status),
           'TOC': ''.join(toc), 'CHAPTERS': chapters, 'KATEX': '0.16.11',
           'CONTRACT_JSON': json.dumps(book['contract'], ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'),
           'CORE_JS': read(HERE / 'physics' / 'core.js'), 'MODULES_JS': modjs, 'APP_JS': read(HERE / 'app.js')}
    # one pass, so a placeholder inside inserted text (KaTeX output, code) is never replaced again
    out = re.sub(r'\{\{([A-Z_]+)\}\}', lambda m: rep[m.group(1)] if m.group(1) in rep else m.group(0), out)
    left = re.findall(r'\{\{[A-Z_]+\}\}', re.sub(r'<script>.*?</script>', '', out, flags=re.S))
    assert not left, 'unfilled placeholder %s' % left[0]
    assert 'googleapis' not in out, 'a Google Fonts address in the page'

    fn = ROOT / 'public' / 'portfolios' / 'electron-beam' / 'index.html' if SITE else HERE / 'out' / 'index.html'
    if opt('--out'):
        fn = pathlib.Path(opt('--out')).resolve()
    fn.parent.mkdir(parents=True, exist_ok=True)
    fn.write_text(out, encoding='utf-8')
    print('wrote %s: %d bytes; %d of %d chapters, %d equations, %d figures, %d numbers, %d formulas' % (
        fn.relative_to(ROOT) if fn.is_relative_to(ROOT) else fn, len(out), st['chapters_present'], L.N_CHAPTERS, st['equations'], st['figures'], st['numbers'], st['formulas']))


if __name__ == '__main__':
    main()

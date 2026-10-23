"""Build the iron-versus-cotton study.

    python3 build.py            -> out/iron-vs-cotton-en.html, out/iron-vs-cotton-ar.html (stand-alone pages, Google Fonts)
    python3 build.py --site     -> ../../public/portfolios/impact/index.html (English) and ar.html (Arabic):
                                   the site's security policy and referrer rule, the site's own fonts, a back link
                                   to the Portfolios page and a language switch.
The physics is physics.js (between PHYSICS-BEGIN/END), the page is template.html, the words are text_en.py / text_ar.py,
the data panel's hooks are datahooks.js. The pages load the site's shared sim.js, dataset.js, datalog.js, paper.css and data.css.
"""
import json, re, sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SITE = '--site' in sys.argv
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

UNIT = r'(?:kN|MN/m|N/m|N·s/m|m/s²|m/s|km/s|kg/m³|kg|cm|mm|µm|µs|ms|m|s|J|GPa|Pa|eV|Å⁻¹|Å|pC|%)'
NUM = r'[\d][\d.,×⁰¹²³⁴⁵⁶⁷⁸⁹⁻]*'
PAT = re.compile(r'(?<![\w.=>/])(' + NUM + r'\s' + UNIT + r')(?![\w/²³])')
def isolate(x):   # keep "10 m" in left-to-right order inside Arabic sentences
    parts = re.split(r'(<span class="m">.*?</span>|<[^>]+>)', x)
    return ''.join(p if p.startswith('<') else PAT.sub(r'<span class="m">\1</span>', p) for p in parts)

CF_EN = {'title': "600 15px 'IBM Plex Sans',sans-serif", 'titleSmall': "600 15px 'IBM Plex Sans',sans-serif", 'small': "12px 'IBM Plex Sans',sans-serif",
         'mono9': "10px 'IBM Plex Mono',monospace", 'mono10': "10.5px 'IBM Plex Mono',monospace", 'mono11': "11px 'IBM Plex Mono',monospace",
         'gaugeNum': "500 11px 'IBM Plex Sans',sans-serif", 'gaugeUnit': "500 10px 'IBM Plex Sans',sans-serif", 'panelLab': "600 9.5px 'IBM Plex Sans',sans-serif",
         'panelNum': "500 13px 'IBM Plex Mono',monospace", 'ruler': "11px 'IBM Plex Sans',sans-serif", 'colHead': "600 13px 'IBM Plex Sans',sans-serif",
         'colSub': "11px 'IBM Plex Mono',monospace"}
CF_AR = dict(CF_EN, title="700 16px 'Noto Naskh Arabic',serif", titleSmall="700 16px 'Noto Naskh Arabic',serif",
             small="13px 'Noto Naskh Arabic',serif", colHead="700 16px 'Noto Naskh Arabic',serif")
CSS_EN = (':root{--f-body:"IBM Plex Sans",system-ui,sans-serif;--f-title:"Instrument Serif",Georgia,serif;--f-mono:"IBM Plex Mono",monospace;'
          '--f-math:"Instrument Serif",Georgia,serif}.m,.eq{font-size:1.08em}')
CSS_AR = (':root{--f-body:"Noto Naskh Arabic","Amiri",serif;--f-title:"Amiri","Noto Naskh Arabic",serif;--f-mono:"IBM Plex Mono",monospace;'
          '--f-math:"Instrument Serif",Georgia,serif}body{font-size:18px;line-height:1.95}h1{font-weight:700;line-height:1.35}h2,h3{font-weight:700;line-height:1.4}'
          '.eyebrow{font-family:"Noto Naskh Arabic",serif;letter-spacing:0;text-transform:none;font-size:14px}'
          '.box .tag{font-family:"Noto Naskh Arabic",serif;letter-spacing:0;text-transform:none;font-size:13px;font-weight:600}p{max-width:80ch}.m,.eq{font-size:1.02em}')
GF = {'en': 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Instrument+Serif&display=swap',
      'ar': 'https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Noto+Naskh+Arabic:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Instrument+Serif&display=swap'}

def build(lang):
    T = importlib.import_module('text_' + lang).T
    if lang == 'ar':
        for k in ['lede', 'sections', 'plot_note', 'energy_note', 'par_intro', 'open1', 'open2wait']:
            T[k] = isolate(T[k])
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    phys = open(os.path.join(HERE, 'physics.js'), encoding='utf-8').read()
    phys = phys[phys.index('/*PHYSICS-BEGIN*/'):phys.index('/*PHYSICS-END*/') + len('/*PHYSICS-END*/')]
    hooks = open(os.path.join(HERE, 'datahooks.js'), encoding='utf-8').read()
    out = (tpl.replace('{{LANG}}', lang).replace('{{DIR}}', 'rtl' if lang == 'ar' else 'ltr').replace('{{TITLE}}', T['title_tag'])
           .replace('{{FONTS}}', GF[lang]).replace('{{CSSLANG}}', CSS_AR if lang == 'ar' else CSS_EN).replace('{{PHYSICS}}', phys)
           .replace('{{TEXT_JSON}}', json.dumps(T, ensure_ascii=False)).replace('{{RTL}}', 'true' if lang == 'ar' else 'false')
           .replace('{{CANVAS_FONTS}}', json.dumps(CF_AR if lang == 'ar' else CF_EN))
           .replace('{{DATAHOOKS}}', hooks).replace('{{PAGE}}', 'index.html' if lang == 'en' else 'ar.html')
           .replace('{{BASE}}', '../../' if SITE else '../../../public/'))
    if not SITE:
        out = out.replace('{{SITEBAR}}', '')
        os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
        fn = os.path.join(HERE, 'out', 'iron-vs-cotton-%s.html' % lang)
    else:
        idx = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
        csp = re.search(r'<meta http-equiv="Content-Security-Policy"[^>]*/>', idx).group(0)
        icon = re.search(r'<link\s+rel="icon"\s+href="[^"]*"\s*/>', open(os.path.join(ROOT, 'public', 'portfolios.html'), encoding='utf-8').read()).group(0)
        bar = ('<nav class="sitebar" aria-label="Site"><a href="../../portfolios.html">%s</a><span class="langs">'
               '<a href="index.html"%s>English</a> · <a href="ar.html" lang="ar"%s>العربية</a></span></nav>') % (
               '← Numa Koudsie · Portfolios' if lang == 'en' else '← Numa Koudsie · Portfolios',
               ' aria-current="page"' if lang == 'en' else '', ' aria-current="page"' if lang == 'ar' else '')
        body_start = out.index('<main')
        head_old, body = out[:body_start], out[body_start:]
        style = re.search(r'<style>.*?</style>', head_old, re.S).group(0)
        fonts = '<link rel="stylesheet" href="../../fonts/instrument-plex.css" />' + ('\n    <link rel="stylesheet" href="../../fonts/arabic.css" />' if lang == 'ar' else '')
        fonts += '\n    <link rel="stylesheet" href="../../styles/paper.css" />\n    <link rel="stylesheet" href="../../styles/data.css" />'
        desc = T['lede'] if lang == 'en' else 'دراسة تفاعلية: كرة حديد وكرة قطن متساويتان في الكتلة تسقطان عشرة أمتار على رأس.'
        desc = re.sub(r'<[^>]+>', '', desc).replace('"', '&quot;')
        head = ('<!doctype html>\n<html lang="%s" dir="%s">\n  <head>\n    <meta charset="UTF-8" />\n    %s\n'
                '    <meta name="referrer" content="strict-origin-when-cross-origin" />\n    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
                '    <title>%s · Numa Koudsie</title>\n    <meta name="description" content="%s" />\n    <meta name="author" content="Numa Koudsie" />\n'
                '    %s\n    %s\n    %s\n  </head>\n  <body>\n') % (lang, 'rtl' if lang == 'ar' else 'ltr', csp, T['title_tag'], desc, icon, fonts, style)
        out = head + body.replace('{{SITEBAR}}', bar) + '\n  </body>\n</html>\n'
        assert 'googleapis' not in out
        d = os.path.join(ROOT, 'public', 'portfolios', 'impact'); os.makedirs(d, exist_ok=True)
        fn = os.path.join(d, 'index.html' if lang == 'en' else 'ar.html')
    assert '{{' not in out
    open(fn, 'w', encoding='utf-8').write(out)
    print(fn, len(out))

for lang in ('en', 'ar'):
    build(lang)

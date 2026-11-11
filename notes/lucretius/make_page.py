# Writes public/lucretius.html: Lucretius I 146-224 as a page of its own, in ONE language per page. The English page carries William
# Ellery Leonard's verse; the German page (/de/) carries Hermann Diels', the Arabic page (/ar/) the Arabic made for this site. They are
# made the way every page of the site is made: the English page is the source, and tools/i18n/build.py puts the German and the Arabic
# in from the tables i18n/<lang>/lucretius.html.json. This script also writes the 20 verses into those two tables (the "translation"
# of a verse of Leonard is the same verse in Diels, or in the Arabic), so no verse is retyped. No Latin on the page: it stands on the
# home page; the numbers are the lines of the Latin. Texts: poem-146-224.json (Leonard, Diels: cut from the sources by extract.py),
# poem-ar-146-158.json and poem-ar-159-224.json (the Arabic). Run from the repository root, then run tools/i18n/build.py.
import json, io, html, re, sys, os
sys.path.insert(0, os.path.join('tools', 'i18n'))
E = lambda s: html.escape(s, quote=False)
G = json.load(io.open('notes/lucretius/poem-146-224.json', encoding='utf-8'))
AR = json.load(io.open('notes/lucretius/poem-ar-146-158.json', encoding='utf-8'))['groups'] + json.load(io.open('notes/lucretius/poem-ar-159-224.json', encoding='utf-8'))['groups']
assert len(G) == len(AR) == 20
assert [a['lines'] for a in AR] == [[min(g['lines']), max(g['lines'])] for g in G]
g0 = G[0]['de']
if g0[1].endswith('leuchtende') and g0[2].startswith('Helle Scheuchen'):   # Diels' line 147 ends with "Helle" (as in make_home.py)
    G[0]['de'] = [g0[0], g0[1] + ' Helle', 'S' + g0[2][len('Helle S'):]]
verse = lambda lines: '<br>'.join(E(t) for t in lines)   # one verse = one translatable piece: its lines, parted by <br>
# Ornaments, drawn as inline SVG in the accent colour (no font needed): an eight-pointed star (khatam, two squares turned 45 degrees,
# pierced in the middle), a quatrefoil of four discs, and a small lozenge.
STAR = '<svg width="18" height="18" viewBox="0 0 20 20"><rect x="4.2" y="4.2" width="11.6" height="11.6"/><rect x="4.2" y="4.2" width="11.6" height="11.6" transform="rotate(45 10 10)"/><circle class="h" cx="10" cy="10" r="2.6"/></svg>'
QUAT = '<svg width="16" height="16" viewBox="0 0 20 20"><circle cx="10" cy="4.6" r="3.9"/><circle cx="15.4" cy="10" r="3.9"/><circle cx="10" cy="15.4" r="3.9"/><circle cx="4.6" cy="10" r="3.9"/><circle class="h" cx="10" cy="10" r="2.2"/></svg>'
DOT = '<svg width="7" height="7" viewBox="0 0 10 10"><rect x="2" y="2" width="6" height="6" transform="rotate(45 5 5)"/></svg>'
# Above every verse: rule, lozenge, rule, star, the line numbers of the Latin, star, rule, lozenge, rule.
BAR = lambda lo, hi: f'<h2 class="lp__n"><span></span>{DOT}<span></span>{STAR}<a href="#l{lo}" dir="ltr">{lo} – {hi}</a>{STAR}<span></span>{DOT}<span></span></h2>'
OPEN = f'<div class="lp-orn" aria-hidden="true"><span></span>{DOT}<span></span>{QUAT}{STAR}{QUAT}<span></span>{DOT}<span></span></div>'
CLOSE = f'<div class="lp-orn lp-orn--end" aria-hidden="true"><span></span>{DOT}<span></span>{STAR}{QUAT}{STAR}<span></span>{DOT}<span></span></div>'
CORNERS = ''.join(f'<i class="lp-corner lp-corner--{c}" aria-hidden="true">{STAR}</i>' for c in 'abcd')
secs = []
for g in G:
    lo, hi = min(g['lines']), max(g['lines'])
    secs.append(f'''        <section class="lp" id="l{lo}">
          {BAR(lo, hi)}
          <p class="lp__v">{verse(g['en'])}</p>
        </section>''')
P = io.open('public/portfolios.html', encoding='utf-8').read()
csp = re.search(r'    <meta http-equiv="Content-Security-Policy"[^\n]*\n', P).group(0)
ref = re.search(r'    <meta name="referrer"[^\n]*\n', P).group(0)
fav = re.search(r'    <link\n      rel="icon"\n.*?/>\n', P, flags=re.S).group(0)
sw = re.search(r'<span class="lang-switch".*?</span>', P, flags=re.S).group(0).replace('portfolios.html', 'lucretius.html')
alt = re.search(r'<!--I18N-ALTERNATES-->.*?<!--/I18N-ALTERNATES-->', P, flags=re.S).group(0).replace('portfolios.html', 'lucretius.html')
logo = re.search(r'<span style="display:inline-flex;align-items:center;gap:14px">.*?</span>\n', P, flags=re.S).group(0)
CSS = """      /* Lucretius I 146-224, one language per page, set as the page of a book: a framed leaf with a star at each corner, a title, and 20
         verses, each under a heading of ornaments that carries the line numbers of the Latin. */
      .lp-lede { max-width: 62ch; }
      .lp-book { position: relative; max-width: 760px; margin: 34px auto 10px; padding: 54px 64px 46px; background: rgba(255, 255, 255, .42);
        border: 1px solid rgba(122, 31, 43, .42); outline: 1px solid rgba(122, 31, 43, .18); outline-offset: 7px; }
      .lp-corner { position: absolute; width: 22px; height: 22px; color: var(--accent); }
      .lp-corner svg { width: 22px; height: 22px; display: block; fill: currentColor; } .lp-corner svg .h { fill: var(--paper); }
      .lp-corner--a { top: -11px; left: -11px; } .lp-corner--b { top: -11px; right: -11px; } .lp-corner--c { bottom: -11px; left: -11px; } .lp-corner--d { bottom: -11px; right: -11px; }
      .lp-title { text-align: center; margin: 0 0 8px; }
      .lp-title p { margin: 0; }
      .lp-title__a { font: 500 11px var(--mono); letter-spacing: .22em; text-transform: uppercase; color: var(--accent); }
      .lp-title__t { font: 400 44px/1.1 'Instrument Serif', Georgia, serif; color: var(--ink); margin: 10px 0 8px !important; }
      .lp-title__s { font: 400 italic 17px/1.4 var(--serif); color: var(--ink-2, var(--ink)); }
      .lp-by { font: 500 10.5px var(--mono); letter-spacing: .14em; text-transform: uppercase; color: var(--muted, var(--ink-3)); margin-top: 14px !important; }
      .lp-orn { display: flex; align-items: center; justify-content: center; gap: 10px; max-width: 420px; margin: 26px auto 6px; color: var(--accent); }
      .lp-orn--end { margin: 40px auto 0; }
      .lp-orn span, .lp__n span { flex: 1; height: 1px; background: linear-gradient(to right, rgba(122, 31, 43, .04), rgba(122, 31, 43, .34), rgba(122, 31, 43, .04)); }
      .lp-orn svg, .lp__n svg { flex: none; display: block; fill: currentColor; } .lp-orn svg .h, .lp__n svg .h { fill: #faf7f1; }
      .lp-orn > svg:nth-of-type(3) { width: 26px; height: 26px; } .lp-orn > svg:first-of-type, .lp-orn > svg:last-of-type { opacity: .55; }
      .lp { padding: 30px 0 0; scroll-margin-top: 16px; }
      .lp__n { display: flex; align-items: center; gap: 12px; margin: 0 0 20px; font: 500 12.5px var(--mono); letter-spacing: .16em; color: var(--accent); }
      .lp__n a { color: var(--accent); text-decoration: none; white-space: nowrap; padding: 0 2px; }
      html[lang='ar'] .lp-book .lp__n, html[lang='ar'] .lp-book .lp__n a { font: 500 13px 'IBM Plex Mono', ui-monospace, Menlo, monospace; letter-spacing: .16em; }
      .lp__n a:hover { color: var(--accent-dark, var(--accent)); }
      .lp__n svg { width: 14px; height: 14px; } .lp__n > svg:first-of-type, .lp__n > svg:last-of-type { opacity: .55; }
      .lp__v { margin: 0 auto; max-width: 30em; font: 400 23px/1.52 'Instrument Serif', Georgia, serif; color: var(--ink); letter-spacing: .005em; }
      .lp:target .lp__v { background: rgba(122, 31, 43, .05); box-shadow: 0 0 0 10px rgba(122, 31, 43, .05); }
      html:not([lang='ar']) #l146 .lp__v::first-letter { float: left; font: 400 74px/.82 'Instrument Serif', Georgia, serif; color: var(--accent); padding: 6px 8px 0 0; }
      html[lang='ar'] .lp__v { font: 400 23px/2.05 'Noto Naskh Arabic', 'Amiri', serif; letter-spacing: 0; max-width: 26em; }
      html[lang='ar'] .lp-title__t { font: 700 40px/1.4 'Amiri', 'Noto Naskh Arabic', serif; }
      html[lang='ar'] .lp-title__a, html[lang='ar'] .lp-by { font: 500 14px 'Noto Naskh Arabic', serif; letter-spacing: 0; text-transform: none; }
      html[lang='ar'] .lp-title__s { font: 400 17px/1.6 'Noto Naskh Arabic', serif; }
      .lp-src { margin: 34px auto 0; padding: 0; list-style: none; max-width: 760px; }
      .lp-h { max-width: 760px; margin-left: auto; margin-right: auto; }
      .lp-src li { margin: 0 0 12px; font-size: 14.5px; line-height: 1.65; color: var(--ink-2, var(--ink)); }
      @media (max-width: 720px) { .lp-book { padding: 36px 22px 32px; outline-offset: 4px; margin-left: 4px; margin-right: 4px; } .lp-title__t { font-size: 34px; } .lp__v { font-size: 19.5px; }
        html[lang='ar'] .lp__v { font-size: 20px; } html:not([lang='ar']) #l146 .lp__v::first-letter { font-size: 60px; } .lp__n { gap: 8px; letter-spacing: .08em; }
        .lp-corner { width: 18px; height: 18px; } .lp-corner svg { width: 18px; height: 18px; } .lp-corner--a, .lp-corner--b { top: -9px; } .lp-corner--c, .lp-corner--d { bottom: -9px; } .lp-corner--a, .lp-corner--c { left: -9px; } .lp-corner--b, .lp-corner--d { right: -9px; } }
"""
page = f'''<!doctype html>
<html lang="en" class="no-js">
  <head>
    <meta charset="UTF-8" />
{csp}{ref}    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Lucretius, On the Nature of Things · Numa Koudsie</title>
    <meta name="description" content="Lucretius, On the Nature of Things, Book I, lines 146–224 (nothing comes from nothing), in the English verse of William Ellery Leonard; also in German and in Arabic." />
    <meta name="author" content="Numa Koudsie" />
    <meta name="theme-color" content="#f5f1ea" />{alt}
    <link rel="stylesheet" href="styles/site.css" />
    <link rel="stylesheet" href="styles/catalog.css" />
    <link rel="stylesheet" href="styles/i18n.css" /><script src="scripts/flip.js"></script>
    <link rel="stylesheet" href="fonts/arabic.css" />
{fav}    <script>
      document.documentElement.className = 'js';
    </script>
    <style>
{CSS}    </style>
  </head>

  <body>
    <a class="skip-link" href="#poem">Skip to the poem</a>

    <header class="cat-top">
      {logo}      <nav aria-label="Site">
        <a href="index.html#positions">Positions</a>
        <a href="index.html#research">Research</a>
        <a href="simulations.html">Simulations</a>
        <a href="index.html#skills">Skills</a>
        <a href="cv/">CV</a>{sw}
      </nav>
    </header>

    <main class="cat" id="poem">
      <div class="cat__head" style="grid-template-columns: minmax(0, 1fr);">
        <div>
          <p class="cat__kicker">Lucretius · On the Nature of Things · Book I</p>
          <h1>Nothing from nothing<span class="dot">.</span></h1>
          <p class="cat__lede lp-lede">
            The opening of the argument of Lucretius: the terror of the mind is dispelled not by daylight but by
            looking at nature, and the first thing nature shows is that nothing is ever born from nothing, and
            nothing is destroyed into nothing. The numbers over the verses are the lines of the Latin; its
            opening stands on the home page.
          </p>
        </div>
      </div>

      <article class="lp-book">
        {CORNERS}
        <header class="lp-title">
          <p class="lp-title__a">Titus Lucretius Carus</p>
          <p class="lp-title__t">On the Nature of Things</p>
          <p class="lp-title__s">Book I, lines 146 to 224</p>
          <p class="lp-by">English verse by William Ellery Leonard, 1916</p>
        </header>
        {OPEN}
{chr(10).join(secs)}
        {CLOSE}
      </article>

      <h2 class="lp-h">Sources</h2>
      <ul class="lp-src">
        <li><b>English.</b> William Ellery Leonard, <i>Of the Nature of Things: A Metrical Translation</i> (1916), <a href="https://www.gutenberg.org/ebooks/785">Project Gutenberg 785</a>, public domain. His verse takes more lines than the Latin.</li>
        <li><b>German.</b> Hermann Diels, <i>Lukrez: Von der Natur</i> (Berlin, 1924), line for line, from <a href="https://www.textlog.de/lukrez-natur-dinge.html">textlog.de</a>. Two places are corrected: “wild” to “wird” (line 156, as the excerpt in the Falter has it) and the break of line 147. Line 173 is as printed online and has not been compared with the book.</li>
        <li><b>Arabic.</b> Made for this site on 11 November 2026 from Leonard’s English, verse by verse, and compared with the Latin. It is not a published translation and has not been checked by a second reader. The only published Arabic translation, from the Egyptian National Centre for Translation (Cairo, 2018), is under copyright and was not used.</li>
        <li><b>Line numbers.</b> They are those of the Latin of Book I as <a href="https://www.thelatinlibrary.com/lucretius/lucretius1.shtml">The Latin Library</a> prints it, in the order of the manuscripts, which give line 155 after line 158; checked at lines 149, 155 to 158 and 218 against the edition of Hermann Diels (Berlin, 1923).</li>
      </ul>
    </main>

    <footer>
      <span>© 2026 Numa Koudsie</span>
      <span><a href="index.html">Home page</a> · <a href="simulations.html">Simulations</a> · <a href="#top" id="to-top">Back to top ↑</a></span>
    </footer>

    <script>
      document.getElementById('to-top').addEventListener('click', function (e) {{
        e.preventDefault();
        window.scrollTo(0, 0);
      }});
    </script>
  </body>
</html>
'''
io.open('public/lucretius.html', 'w', encoding='utf-8').write(page); print('ok', len(page))
# The verses of the German and the Arabic page, written into the tables of the generator under the key of the English verse.
import build as B
pieces, attrs = B.cut(page)
on_page = {B.key(x) for x in [p[2] for p in pieces] + [a[3] for a in attrs]}
for lang, field, rows in (('de', 'de', [g['de'] for g in G]), ('ar', 'ar', [a['ar'] for a in AR])):
    path, T = B.table(lang, 'lucretius.html')
    for g, lines in zip(G, rows):
        en = verse(g['en']); k = B.key(en); assert k in on_page, (lang, g['lines'][0])
        T[k] = {'src': B.norm(en), 'tr': verse(lines)}
    T = {k: v for k, v in T.items() if k in on_page}      # entries of pieces that are no longer on the page go
    json.dump(dict(sorted(T.items())), io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(lang, len(T), 'entries;', len(on_page - set(T)), 'pieces without a translation yet')

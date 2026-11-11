# Writes public/lucretius.html: Lucretius I 146-224 as a page of its own, each of the 20 sentences in Latin, English, German and Arabic.
# The texts come from poem-146-224.json (Latin, Leonard, Diels: cut from the sources by extract.py) and from poem-ar-146-158.json and
# poem-ar-159-224.json (the Arabic, made for this site); nothing is retyped. The poem blocks are translate="no": the German and Arabic
# versions of the page (made by tools/i18n/build.py) translate only the words around them. Run from the repository root.
import json, io, html, re
E = html.escape
G = json.load(io.open('notes/lucretius/poem-146-224.json', encoding='utf-8'))
AR = json.load(io.open('notes/lucretius/poem-ar-146-158.json', encoding='utf-8'))['groups'] + json.load(io.open('notes/lucretius/poem-ar-159-224.json', encoding='utf-8'))['groups']
assert len(G) == len(AR) == 20
assert [a['lines'] for a in AR] == [[min(g['lines']), max(g['lines'])] for g in G]
g0 = G[0]['de']
if g0[1].endswith('leuchtende') and g0[2].startswith('Helle Scheuchen'):   # Diels' line 147 ends with "Helle" (as in make_home.py)
    G[0]['de'] = [g0[0], g0[1] + ' Helle', 'S' + g0[2][len('Helle S'):]]
def cell(lang, label, lines, dir_='ltr'):
    body = ''.join(f'<span class="lp__l">{E(t)}</span>' for t in lines)
    return f'<div class="lp__c" lang="{lang}" dir="{dir_}" data-l="{label}">{body}</div>'
# Ornaments, drawn as inline SVG in the accent colour (no font needed): an eight-pointed star (khatam, two squares turned 45 degrees,
# pierced in the middle), a quatrefoil of four discs, and a small lozenge. Between two columns: lozenge, line, star or quatrefoil, line,
# lozenge; between two sentences: line, lozenge, line, star, line, lozenge, line.
STAR = '<svg width="18" height="18" viewBox="0 0 20 20"><rect x="4.2" y="4.2" width="11.6" height="11.6"/><rect x="4.2" y="4.2" width="11.6" height="11.6" transform="rotate(45 10 10)"/><circle class="h" cx="10" cy="10" r="2.6"/></svg>'
QUAT = '<svg width="16" height="16" viewBox="0 0 20 20"><circle cx="10" cy="4.6" r="3.9"/><circle cx="15.4" cy="10" r="3.9"/><circle cx="10" cy="15.4" r="3.9"/><circle cx="4.6" cy="10" r="3.9"/><circle class="h" cx="10" cy="10" r="2.2"/></svg>'
DOT = '<svg width="7" height="7" viewBox="0 0 10 10"><rect x="2" y="2" width="6" height="6" transform="rotate(45 5 5)"/></svg>'
sep = lambda mid: f'<i class="lp__sep" aria-hidden="true">{DOT}<span></span>{mid}<span></span>{DOT}</i>'
DIV = f'      <div class="lp-div" aria-hidden="true"><span></span>{DOT}<span></span>{STAR}<span></span>{DOT}<span></span></div>'
secs = []
for k, (g, a) in enumerate(zip(G, AR)):
    lo, hi = min(g['lines']), max(g['lines'])
    secs.append(f'''      <section class="lp" id="l{lo}" translate="no">
        <h2 class="lp__n"><a href="#l{lo}" dir="ltr">{lo}–{hi}</a></h2>
        <div class="lp__row">{cell('la', 'Latin', g['la'])}{sep(STAR)}{cell('en', 'English', g['en'])}{sep(QUAT)}{cell('de', 'Deutsch', g['de'])}{sep(STAR)}{cell('ar', 'العربية', a['ar'], 'rtl')}</div>
      </section>''')
P = io.open('public/portfolios.html', encoding='utf-8').read()
csp = re.search(r'    <meta http-equiv="Content-Security-Policy"[^\n]*\n', P).group(0)
ref = re.search(r'    <meta name="referrer"[^\n]*\n', P).group(0)
fav = re.search(r'    <link\n      rel="icon"\n.*?/>\n', P, flags=re.S).group(0)
sw = re.search(r'<span class="lang-switch".*?</span>', P, flags=re.S).group(0).replace('portfolios.html', 'lucretius.html')
alt = re.search(r'<!--I18N-ALTERNATES-->.*?<!--/I18N-ALTERNATES-->', P, flags=re.S).group(0).replace('portfolios.html', 'lucretius.html')
logo = re.search(r'<span style="display:inline-flex;align-items:center;gap:14px">.*?</span>\n', P, flags=re.S).group(0)
CSS = """      /* Lucretius I 146-224, four columns: the Latin, then Leonard, Diels and the Arabic of this site. The row stays left to right in every
         language of the page (direction: ltr); each column carries its own dir. */
      .lp-lede { max-width: 62ch; }
      .lp { display: grid; grid-template-columns: 72px minmax(0, 1fr); gap: 0 18px; padding: 20px 0; }
      .lp__n { margin: 0; font: 500 11px/1.6 var(--mono); letter-spacing: .06em; padding-top: 5px; }
      .lp__n a { color: var(--muted, var(--ink-3)); text-decoration: none; }
      .lp__n a:hover, .lp:target .lp__n a { color: var(--accent); }
      .lp:target { background: rgba(122, 31, 43, .04); }
      .lp__row { direction: ltr; display: grid; grid-template-columns: minmax(0, 1fr) 18px minmax(0, 1fr) 18px minmax(0, 1fr) 18px minmax(0, 1fr); gap: 0 16px; }
      .lp__sep { display: flex; flex-direction: column; align-items: center; gap: 7px; padding: 2px 0; color: var(--accent); font-style: normal; }
      .lp__sep span { flex: 1; width: 1px; min-height: 14px; background: linear-gradient(to bottom, rgba(122, 31, 43, .05), rgba(122, 31, 43, .32), rgba(122, 31, 43, .05)); }
      .lp__sep svg, .lp-div svg { flex: none; display: block; fill: currentColor; } .lp__sep svg .h, .lp-div svg .h { fill: var(--paper); }
      .lp__sep svg:not(:first-child):not(:last-child) { opacity: .85; } .lp__sep > svg:first-child, .lp__sep > svg:last-child { opacity: .55; }
      .lp-div { display: flex; align-items: center; gap: 10px; max-width: 460px; margin: 10px auto; color: var(--accent); }
      .lp-div span { flex: 1; height: 1px; background: linear-gradient(to right, rgba(122, 31, 43, .04), rgba(122, 31, 43, .3), rgba(122, 31, 43, .04)); }
      .lp-div > svg:nth-of-type(odd) { opacity: .55; } .lp-div > svg:nth-of-type(2) { width: 24px; height: 24px; }   /* the sentence break: a larger star than the column breaks */
      .lp__c { min-width: 0; }
      .lp__c::before { content: attr(data-l); display: block; margin-bottom: 6px; font: 500 10.5px var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted, var(--ink-3)); }
      .lp__c[lang='ar']::before { font-family: 'Noto Naskh Arabic', var(--mono); letter-spacing: 0; text-transform: none; font-size: 12px; }
      .lp__l { display: block; font: 400 15px/1.6 var(--sans, 'IBM Plex Sans', sans-serif); color: var(--ink-2, var(--ink)); }
      .lp__c[lang='la'] .lp__l { font: 400 19px/1.35 'Instrument Serif', Georgia, serif; color: var(--ink); margin-bottom: .15em; }
      .lp__c[lang='en'] .lp__l, .lp__c[lang='de'] .lp__l { font-style: italic; font-family: var(--serif); font-size: 16.5px; line-height: 1.5; }
      .lp__c[lang='ar'] .lp__l { font: 400 19px/1.95 'Amiri', 'Noto Naskh Arabic', serif; color: var(--ink); }
      .lp-src { margin: 34px 0 0; padding: 0; list-style: none; max-width: 78ch; }
      .lp-src li { margin: 0 0 12px; font-size: 14.5px; line-height: 1.65; color: var(--ink-2, var(--ink)); }
      @media (max-width: 1000px) { .lp__row { grid-template-columns: minmax(0, 1fr); gap: 14px 0; } .lp__sep { flex-direction: row; width: min(130px, 40%); opacity: .8; margin: 0 auto; padding: 0; } .lp__sep span { width: auto; min-height: 0; height: 1px; background: linear-gradient(to right, rgba(122, 31, 43, .05), rgba(122, 31, 43, .32), rgba(122, 31, 43, .05)); } }
      @media (max-width: 620px) { .lp { grid-template-columns: minmax(0, 1fr); } .lp__row { grid-template-columns: minmax(0, 1fr); } .lp__n { padding-top: 0; margin-bottom: 8px; } }
"""
page = f'''<!doctype html>
<html lang="en" class="no-js">
  <head>
    <meta charset="UTF-8" />
{csp}{ref}    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Lucretius, On the Nature of Things · Numa Koudsie</title>
    <meta name="description" content="Lucretius, On the Nature of Things, Book I, lines 146–224 (nothing comes from nothing): the Latin, William Ellery Leonard’s English, Hermann Diels’ German and an Arabic translation made for this site, sentence by sentence." />
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
            The opening of the argument of Lucretius, lines 146 to 224 of Book I: the terror of the mind is
            dispelled not by daylight but by looking at nature, and the first thing nature shows is that
            nothing is ever born from nothing, and nothing is destroyed into nothing. Each sentence stands in
            the Latin and in three languages. The numbers on the left are the lines of the Latin.
          </p>
        </div>
      </div>

{(chr(10) + DIV + chr(10)).join(secs)}

      <h2 class="lp-h">Sources and how the translations were made</h2>
      <ul class="lp-src">
        <li><b>Latin.</b> <a href="https://www.thelatinlibrary.com/lucretius/lucretius1.shtml">The Latin Library</a>, Book I, in the order of the manuscripts, which give line 155 after line 158; checked at lines 149, 155 to 158 and 218 against the edition of Hermann Diels (Berlin, 1923).</li>
        <li><b>English.</b> William Ellery Leonard, <i>Of the Nature of Things: A Metrical Translation</i> (1916), <a href="https://www.gutenberg.org/ebooks/785">Project Gutenberg 785</a>, public domain. His verse takes more lines than the Latin, so his lines do not match the Latin line for line; the sentences do.</li>
        <li><b>German.</b> Hermann Diels, <i>Lukrez: Von der Natur</i> (Berlin, 1924), line for line, from <a href="https://www.textlog.de/lukrez-natur-dinge.html">textlog.de</a>. Two places are corrected: “wild” to “wird” (line 156, as the excerpt in the Falter has it) and the break of line 147. Line 173 is as printed online and has not been compared with the book.</li>
        <li><b>Arabic.</b> Made from the Latin for this site on 10 November 2026 and read against Leonard and Diels for the sense. It is not a published translation and has not been checked by a second reader. The only published Arabic translation, from the Egyptian National Centre for Translation (Cairo, 2018), is under copyright and was not used.</li>
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

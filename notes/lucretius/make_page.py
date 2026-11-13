# Writes public/lucretius.html: Lucretius I 146-224 as a page of its own, in FOUR languages side by side: the Latin, Leonard's English
# (1916), Diels' German (1924) and the Arabic made for this site (seventh version, 13 November 2026). The English page is the source of
# the site's generator (tools/i18n/build.py), which makes /de/ and /ar/ from it and the tables i18n/<lang>/lucretius.html.json. The verses
# are the same on all three pages: they stand in the page marked translate="no" (each in its own lang= and dir=), so the tables hold only
# the words around them (title, lede, column credits, sources). Wide screens: four columns with fading hairlines, a sticky head. Tablets:
# two by two. Phones: one language at a time, chosen with four buttons (the page's own language first); without JavaScript the four
# stand one under the other, each with its name. Texts: poem-146-224.json (Latin, Leonard, Diels: cut from the sources by extract.py)
# and poem-ar-146-224.json (the Arabic). Run from the repository root, then run tools/i18n/build.py.
import json, io, html, re, sys, os
sys.path.insert(0, os.path.join('tools', 'i18n'))
E = lambda s: html.escape(s, quote=False)
G = json.load(io.open('notes/lucretius/poem-146-224.json', encoding='utf-8'))
AR = json.load(io.open('notes/lucretius/poem-ar-146-224.json', encoding='utf-8'))['groups']
assert len(G) == len(AR) == 20
assert [a['lines'] for a in AR] == [[min(g['lines']), max(g['lines'])] for g in G]
assert all(len(g['la']) == len(g['lines']) for g in G)
g0 = G[0]['de']
if g0[1].endswith('leuchtende') and g0[2].startswith('Helle Scheuchen'):   # Diels' line 147 ends with "Helle" (as in make_home.py)
    G[0]['de'] = [g0[0], g0[1] + ' Helle', 'S' + g0[2][len('Helle S'):]]
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
NAME = {'la': 'Latina', 'en': 'English', 'de': 'Deutsch', 'ar': 'العربية'}
def cell(l, lines, nums=None):
    if nums:   # the Latin: the number of each line stands in the margin
        body = '\n'.join(f'            <span class="ln"><i class="no">{n}</i>{E(t)}</span>' for n, t in zip(nums, lines))
    else:
        body = '\n'.join(f'            <span class="ln">{E(t)}</span>' for t in lines)
    d = ' dir="rtl"' if l == 'ar' else ''
    return f'''          <div class="lp__c lp__c--{l}" lang="{l}"{d} translate="no" data-name="{NAME[l]}">
          <p class="lp__v">
{body}
          </p>
          </div>'''
secs = []
for g, a in zip(G, AR):
    lo, hi = min(g['lines']), max(g['lines'])
    secs.append(f'''        <section class="lp" id="l{lo}">
          {BAR(lo, hi)}
          <div class="lp__row">
{cell('la', g['la'], g['lines'])}
{cell('en', g['en'])}
{cell('de', g['de'])}
{cell('ar', a['ar'])}
          </div>
        </section>''')
P = io.open('public/portfolios.html', encoding='utf-8').read()
csp = re.search(r'    <meta http-equiv="Content-Security-Policy"[^\n]*\n', P).group(0)
ref = re.search(r'    <meta name="referrer"[^\n]*\n', P).group(0)
fav = re.search(r'    <link\n      rel="icon"\n.*?/>\n', P, flags=re.S).group(0)
sw = re.search(r'<span class="lang-switch".*?</span>', P, flags=re.S).group(0).replace('portfolios.html', 'lucretius.html')
alt = re.search(r'<!--I18N-ALTERNATES-->.*?<!--/I18N-ALTERNATES-->', P, flags=re.S).group(0).replace('portfolios.html', 'lucretius.html')
logo = re.search(r'<span style="display:inline-flex;align-items:center;gap:14px">.*?</span>\n', P, flags=re.S).group(0)
CSS = """      /* Lucretius I 146-224 in four languages side by side, set as the page of a book: a framed leaf with a star at each corner, a title,
         a head that names the four columns, and 20 verses, each under a heading of ornaments that carries the line numbers of the Latin.
         Between the columns run hairlines that fade out at both ends of every verse. */
      .lp-book { --lp-cols: minmax(0, .95fr) minmax(0, 1fr) minmax(0, 1.05fr) minmax(0, 1.2fr); }
      .lp-lede { max-width: 66ch; }
      .lp-note { display: none; margin: 10px 0 0; max-width: 66ch; font-size: 14.5px; line-height: 1.6; color: var(--ink-2, var(--ink)); }
      .lp-book { overflow-anchor: none; position: relative; margin: 34px 12px 10px; padding: 50px 36px 44px; background: rgba(255, 255, 255, .42);
        border: 1px solid rgba(122, 31, 43, .42); outline: 1px solid rgba(122, 31, 43, .18); outline-offset: 7px; }
      .lp-corner { position: absolute; width: 22px; height: 22px; color: var(--accent); }
      .lp-corner svg { width: 22px; height: 22px; display: block; fill: currentColor; } .lp-corner svg .h { fill: var(--paper); }
      .lp-corner--a { top: -11px; left: -11px; } .lp-corner--b { top: -11px; right: -11px; } .lp-corner--c { bottom: -11px; left: -11px; } .lp-corner--d { bottom: -11px; right: -11px; }
      .lp-title { text-align: center; margin: 0 0 8px; }
      .lp-title p { margin: 0; }
      .lp-title__a { font: 500 11px var(--mono); letter-spacing: .22em; text-transform: uppercase; color: var(--accent); }
      .lp-title__t { font: 400 44px/1.1 'Instrument Serif', Georgia, serif; color: var(--ink); margin: 10px 0 8px !important; }
      .lp-title__s { font: 400 italic 17px/1.4 var(--serif); color: var(--ink-2, var(--ink)); }
      html[lang='ar'] .lp-title__t { font: 700 40px/1.4 'Amiri', 'Noto Naskh Arabic', serif; }
      html[lang='ar'] .lp-title__a { font: 500 14px 'Noto Naskh Arabic', serif; letter-spacing: 0; text-transform: none; }
      html[lang='ar'] .lp-title__s { font: 400 17px/1.6 'Noto Naskh Arabic', serif; }
      .lp-orn { display: flex; align-items: center; justify-content: center; gap: 10px; max-width: 420px; margin: 26px auto 6px; color: var(--accent); }
      .lp-orn--end { margin: 40px auto 0; }
      .lp-orn span, .lp__n span { flex: 1; height: 1px; background: linear-gradient(to right, rgba(122, 31, 43, .04), rgba(122, 31, 43, .34), rgba(122, 31, 43, .04)); }
      .lp-orn svg, .lp__n svg { flex: none; display: block; fill: currentColor; } .lp-orn svg .h, .lp__n svg .h { fill: #faf7f1; }
      .lp-orn > svg:nth-of-type(3) { width: 26px; height: 26px; } .lp-orn > svg:first-of-type, .lp-orn > svg:last-of-type { opacity: .55; }
      /* the head: names the four columns; it stays at the top of the window while the verses pass under it */
      .lp-cols { position: sticky; top: 0; z-index: 5; display: grid; grid-template-columns: var(--lp-cols); direction: ltr; margin: 24px -36px 0; padding: 0 36px;
        background: rgba(250, 247, 241, .94); -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px); }
      .lp-cols::after { content: ''; position: absolute; left: 36px; right: 36px; bottom: 0; height: 1px; background: linear-gradient(to right, rgba(122, 31, 43, .04), rgba(122, 31, 43, .34), rgba(122, 31, 43, .04)); }
      .lp-cols button { position: relative; display: block; margin: 0; padding: 14px 22px 12px; border: 0; background: none; color: var(--ink); font: inherit; text-align: left; cursor: default; }
      .lp-cols button:disabled { opacity: 1; color: var(--ink); }
      .lp-cols button[data-l='ar'] { text-align: right; }
      .lp-cols b { display: block; font: 400 22px/1.2 'Instrument Serif', Georgia, serif; }
      .lp-cols b[lang='ar'] { font: 700 19px/1.5 'Amiri', 'Noto Naskh Arabic', serif; }
      .lp-cols small { display: block; margin-top: 3px; font: 500 10.5px var(--mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted, var(--ink-3)); }
      html[lang='ar'] .lp-cols small { font: 400 13px 'Noto Naskh Arabic', serif; letter-spacing: 0; text-transform: none; }
      /* one verse = one row of four cells */
      .lp { padding: 26px 0 0; scroll-margin-top: 92px; }
      .lp__n { display: flex; align-items: center; gap: 12px; margin: 0 0 18px; font: 500 12.5px var(--mono); letter-spacing: .16em; color: var(--accent); }
      .lp__n a { color: var(--accent); text-decoration: none; white-space: nowrap; padding: 0 2px; }
      html[lang='ar'] .lp-book .lp__n, html[lang='ar'] .lp-book .lp__n a { font: 500 13px 'IBM Plex Mono', ui-monospace, Menlo, monospace; letter-spacing: .16em; }
      .lp__n a:hover { color: var(--accent-dark, var(--accent)); }
      .lp__n svg { width: 14px; height: 14px; } .lp__n > svg:first-of-type, .lp__n > svg:last-of-type { opacity: .55; }
      .lp__row { display: grid; grid-template-columns: var(--lp-cols); direction: ltr; align-items: start; }
      .lp:target .lp__row { background: rgba(122, 31, 43, .045); box-shadow: 0 0 0 10px rgba(122, 31, 43, .045); }
      .lp__c { position: relative; padding: 2px 22px 4px; }
      .lp__c + .lp__c::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 1px;
        background: linear-gradient(to bottom, rgba(122, 31, 43, 0), rgba(122, 31, 43, .3) 16%, rgba(122, 31, 43, .3) 84%, rgba(122, 31, 43, 0)); }
      .lp__v { margin: 0; font: 400 20px/1.5 'Instrument Serif', Georgia, serif; color: var(--ink); letter-spacing: .005em; }
      .lp__c .ln { display: block; padding-left: 1.25em; text-indent: -1.25em; }     /* a line that wraps hangs, so a new line of the verse stays a new line */
      .lp__c--la .lp__v { font-style: italic; color: var(--ink-2, var(--ink)); }
      .lp__c--la .ln { position: relative; padding-left: 3em; text-indent: -.8em; }
      .lp__c--la .no { position: absolute; left: 0; top: .52em; width: 2em; font: 500 10px var(--mono); font-style: normal; letter-spacing: .04em; text-indent: 0; color: var(--accent); opacity: .85; }
      /* the Arabic reads right to left; its lines go in couplets, a little air after every second line */
      .lp__c--ar .lp__v { font: 400 20px/1.95 'Noto Naskh Arabic', 'Amiri', serif; letter-spacing: 0; }
      .lp__c--ar .ln { padding-left: 0; padding-right: 1.4em; text-indent: -1.4em; }
      .lp__c--ar .ln:nth-child(even):not(:last-child) { margin-bottom: .55em; }
      .lp-src { margin: 34px auto 0; padding: 0; list-style: none; max-width: 760px; }
      .lp-h { max-width: 760px; margin-left: auto; margin-right: auto; }
      .lp-src li { margin: 0 0 12px; font-size: 14.5px; line-height: 1.65; color: var(--ink-2, var(--ink)); }
      /* tablets: two by two, each cell named */
      @media (max-width: 1099px) and (min-width: 761px) {
        .lp-cols { display: none; }
        .lp__row { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 22px; }
        .lp__c::before { display: none; }
        .lp__c:nth-child(even)::before { display: block; }
        .lp__c:nth-child(even)::before { content: ''; }
        .lp__c::after { content: attr(data-name); display: block; order: -1; }
        .lp__c { display: flex; flex-direction: column; } .lp__c .lp__v { order: 2; }
        .lp__c::after { font: 500 10.5px var(--mono); letter-spacing: .14em; text-transform: uppercase; color: var(--muted, var(--ink-3)); margin-bottom: 8px; }
        .lp__c--ar::after { font: 700 15px 'Amiri', serif; letter-spacing: 0; text-transform: none; text-align: right; }
        .lp__c--ar .lp__v { text-align: right; }
      }
      /* phones: one language at a time (without JavaScript: all four, one under the other, each with its name) */
      @media (max-width: 760px) {
        .lp-note { display: block; }
        .lp-book { padding: 34px 20px 30px; outline-offset: 4px; margin-left: 4px; margin-right: 4px; }
        .lp-title__t { font-size: 34px; }
        .lp-corner { width: 18px; height: 18px; } .lp-corner svg { width: 18px; height: 18px; } .lp-corner--a, .lp-corner--b { top: -9px; } .lp-corner--c, .lp-corner--d { bottom: -9px; } .lp-corner--a, .lp-corner--c { left: -9px; } .lp-corner--b, .lp-corner--d { right: -9px; }
        .lp__n { gap: 8px; letter-spacing: .08em; }
        .lp-cols { grid-template-columns: repeat(4, minmax(0, 1fr)); margin: 18px -20px 0; padding: 0 20px; top: 0; }
        .lp-cols::after { left: 20px; right: 20px; }
        .lp-cols button, .lp-cols button[data-l='ar'] { padding: 12px 4px 10px; text-align: center; cursor: pointer; -webkit-tap-highlight-color: transparent; }
        .lp-cols button:disabled { cursor: pointer; }
        .lp-cols b { font-size: 19px; } .lp-cols b[lang='ar'] { font-size: 17px; }
        .lp-cols small { display: none; }
        .lp-cols button[aria-pressed='true'] b { color: var(--accent); }
        .lp-cols button::after { content: ''; position: absolute; left: 22%; right: 22%; bottom: -1px; height: 2px; background: var(--accent); transform: scaleX(0); transition: transform .28s ease; }
        .lp-cols button[aria-pressed='true']::after { transform: scaleX(1); }
        .lp__row { grid-template-columns: minmax(0, 1fr); row-gap: 18px; }
        .lp__c { padding: 2px 4px 4px; } .lp__c::before { display: none; }
        .lp__v { font-size: 20.5px; } .lp__c--ar .lp__v { font-size: 21px; }
        .lp__c::after { content: attr(data-name); display: block; margin: 0 0 6px; font: 500 10.5px var(--mono); letter-spacing: .14em; text-transform: uppercase; color: var(--accent); }
        .lp__c { display: flex; flex-direction: column; } .lp__c .lp__v { order: 2; } .lp__c::after { order: -1; }
        .lp__c--ar::after { font: 700 15px 'Amiri', serif; letter-spacing: 0; text-transform: none; text-align: right; }
        .lp__c--ar .lp__v { text-align: right; }
        .js .lp-cols button { }
        .js .lp__c::after { display: none; }
        .js .lp-book[data-show='la'] .lp__c:not(.lp__c--la), .js .lp-book[data-show='en'] .lp__c:not(.lp__c--en),
        .js .lp-book[data-show='de'] .lp__c:not(.lp__c--de), .js .lp-book[data-show='ar'] .lp__c:not(.lp__c--ar) { display: none; }
        .js .lp__row { row-gap: 0; }
        .js .lp__v { animation: lp-turn .32s ease both; }
        .lp__c--la .ln { padding-left: 2.8em; }
      }
      @keyframes lp-turn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
      @media (prefers-reduced-motion: reduce) { .js .lp__v { animation: none; } .lp-cols button::after { transition: none; } }
"""
JS = """    <script>
      /* Phones: the four buttons above the poem choose the language shown; the first is the language of the page. */
      (function () {
        var book = document.querySelector('.lp-book'), btns = book.querySelectorAll('.lp-cols button'), mq = window.matchMedia('(max-width: 760px)');
        var L = document.documentElement.lang; if (['la', 'en', 'de', 'ar'].indexOf(L) < 0) L = 'en';
        function show(l) {
          var anchor = null, top = 0, secs = book.querySelectorAll('.lp');
          for (var i = 0; i < secs.length; i++) { if (secs[i].getBoundingClientRect().bottom > 90) { anchor = secs[i]; top = anchor.getBoundingClientRect().top; break; } }
          book.setAttribute('data-show', l);
          for (var j = 0; j < btns.length; j++) btns[j].setAttribute('aria-pressed', btns[j].getAttribute('data-l') === l ? 'true' : 'false');
          if (anchor && mq.matches) window.scrollBy({ top: anchor.getBoundingClientRect().top - top, left: 0, behavior: 'instant' });   /* the verse you were reading stays where it was */
        }
        function sync() { for (var j = 0; j < btns.length; j++) btns[j].disabled = !mq.matches; }
        for (var k = 0; k < btns.length; k++) btns[k].addEventListener('click', function () { show(this.getAttribute('data-l')); });
        if (mq.addEventListener) mq.addEventListener('change', sync);
        sync(); show(L);
      })();
    </script>
"""
page = f'''<!doctype html>
<html lang="en" class="no-js">
  <head>
    <meta charset="UTF-8" />
{csp}{ref}    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Lucretius, On the Nature of Things · Numa Koudsie</title>
    <meta name="description" content="Lucretius, On the Nature of Things, Book I, lines 146–224 (nothing comes from nothing): the Latin and three translations side by side, English (Leonard), German (Diels) and Arabic." />
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
            The opening of the argument of Lucretius, in the Latin and in three translations side by side. The terror
            of the mind is dispelled not by daylight but by looking at nature, and the first thing nature shows is that
            nothing is ever born from nothing, and nothing is destroyed into nothing. The numbers over the verses are
            the lines of the Latin.
          </p>
          <p class="lp-note">On a narrow screen the four languages are shown one at a time: choose one with the buttons above the poem.</p>
        </div>
      </div>

      <article class="lp-book">
        {CORNERS}
        <header class="lp-title">
          <p class="lp-title__a">Titus Lucretius Carus</p>
          <p class="lp-title__t">On the Nature of Things</p>
          <p class="lp-title__s">Book I, lines 146 to 224</p>
        </header>
        {OPEN}
        <div class="lp-cols" role="group" aria-label="Language shown">
          <button type="button" data-l="la" aria-pressed="false"><b lang="la" translate="no">Latina</b><small>the original</small></button>
          <button type="button" data-l="en" aria-pressed="false"><b lang="en" translate="no">English</b><small translate="no">Leonard, 1916</small></button>
          <button type="button" data-l="de" aria-pressed="false"><b lang="de" translate="no">Deutsch</b><small translate="no">Diels, 1924</small></button>
          <button type="button" data-l="ar" aria-pressed="false"><b lang="ar" translate="no">العربية</b><small>made for this site</small></button>
        </div>
{chr(10).join(secs)}
        {CLOSE}
      </article>

      <h2 class="lp-h">Sources</h2>
      <ul class="lp-src">
        <li><b>Latin.</b> <a href="https://www.thelatinlibrary.com/lucretius/lucretius1.shtml">The Latin Library</a>, Book I, lines 146 to 224, line by line. The Latin has fewer lines than Leonard’s English, so the four columns run by sentence, not by line: the numbers over each verse say which lines of the Latin it renders.</li>
        <li><b>English.</b> William Ellery Leonard, <i>Of the Nature of Things: A Metrical Translation</i> (1916), <a href="https://www.gutenberg.org/ebooks/785">Project Gutenberg 785</a>, public domain. His verse takes more lines than the Latin.</li>
        <li><b>German.</b> Hermann Diels, <i>Lukrez: Von der Natur</i> (Berlin, 1924), line for line, from <a href="https://www.textlog.de/lukrez-natur-dinge.html">textlog.de</a>. Two places are corrected: “wild” to “wird” (line 156, as the excerpt in the Falter has it) and the break of line 147. Line 173 is as printed online and has not been compared with the book.</li>
        <li><b>Arabic.</b> Made for this site on 13 November 2026 from Leonard’s English, verse by verse, and compared with the Latin. It is free verse in modern literary Arabic, with rhyme only here and there and no classical metre. It is not a published translation and has not been checked by a second reader. The only published Arabic translation, from the Egyptian National Centre for Translation (Cairo, 2018), is under copyright and was not used.</li>
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
{JS}  </body>
</html>
'''
io.open('public/lucretius.html', 'w', encoding='utf-8').write(page); print('ok', len(page))
# The tables of the German and the Arabic page hold the words around the verses; entries of pieces no longer on the page go.
import build as B
pieces, attrs = B.cut(page)
on_page = {B.key(x) for x in [p[2] for p in pieces] + [a[3] for a in attrs]}
for lang in ('de', 'ar'):
    path, T = B.table(lang, 'lucretius.html')
    T = {k: v for k, v in T.items() if k in on_page}
    json.dump(dict(sorted(T.items())), io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(lang, len(T), 'entries;', len(on_page - set(T)), 'pieces without a translation yet')

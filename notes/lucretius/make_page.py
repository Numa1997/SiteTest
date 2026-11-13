# Writes public/lucretius.html: Lucretius I 146-224 as a page of its own, in FOUR languages side by side: the Latin, Leonard's English
# (1916), Diels' German (1924) and the Arabic made for this site (eighth version, 13 November 2026, fully vowelled). The English page is the source of
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
NAME = {'la': 'Latina', 'en': 'English', 'de': 'Deutsch', 'ar': 'العربية'}
def cell(l, lines, nums=None, sep=False):
    if nums:   # the Latin: the number of each line stands in the margin
        body = '\n'.join(f'            <span class="ln"><i class="no">{n}</i>{E(t)}</span>' for n, t in zip(nums, lines))
    else:
        body = '\n'.join(f'            <span class="ln">{E(t)}</span>' for t in lines)
    d = ' dir="rtl"' if l == 'ar' else ''
    mark = '<i class="lp__sep" aria-hidden="true"></i>' if sep else ''
    return f'''          <div class="lp__c lp__c--{l}" lang="{l}"{d} translate="no" data-name="{NAME[l]}">{mark}
          <p class="lp__v">
{body}
          </p>
          </div>'''
secs = []
for i, (g, a) in enumerate(zip(G, AR)):
    lo, hi = min(g['lines']), max(g['lines']); sep = i > 0
    secs.append(f'''        <section class="lp" id="l{lo}" aria-label="Lines {lo} to {hi}">
          <div class="lp__row">
{cell('la', g['la'], g['lines'], sep)}
{cell('en', g['en'], None, sep)}
{cell('de', g['de'], None, sep)}
{cell('ar', a['ar'], None, sep)}
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
         Modern and flat since 13 November 2026: no paper sheet, frame or ornaments; a head with a dark top rule names the four columns
         (index number, name, credit), and 20 verses. Each language runs down its own column as one text: hairlines between the
         columns run unbroken from the first verse to the last, and between two verses each column has only a small mark of its own
         (a short fading hairline with a lozenge) that never crosses into the next column. */
      .lp-book { --lp-cols: minmax(0, .9fr) minmax(0, .95fr) minmax(0, 1fr) minmax(0, 1.5fr); }
      .lp-lede { max-width: 66ch; }
      .lp-note { display: none; margin: 10px 0 0; max-width: 66ch; font-size: 14.5px; line-height: 1.6; color: var(--ink-2, var(--ink)); }
      .lp-book { overflow-anchor: none; position: relative; margin: 44px 0 0; }
      /* the head: names the four columns; it stays at the top of the window while the verses pass under it */
      .lp-cols { position: sticky; top: 0; z-index: 5; display: grid; grid-template-columns: var(--lp-cols); direction: ltr; margin: 0; padding: 0;
        background: rgba(245, 241, 234, .92); -webkit-backdrop-filter: blur(8px); backdrop-filter: blur(8px); border-top: 1px solid var(--ink); }
      .lp-cols::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 1px; background: var(--rule); }
      .lp-cols button { position: relative; display: block; margin: 0; padding: 14px 22px 16px; border: 0; background: none; color: var(--ink); font: inherit; text-align: left; cursor: default; }
      .lp-cols button:disabled { opacity: 1; color: var(--ink); }
      .lp-cols button[data-l='ar'] { text-align: right; }
      .lp-cols b { display: block; font: 400 27px/1.15 'Instrument Serif', Georgia, serif; }
      .lp-cols .ix { display: block; margin: 0 0 10px; font: 500 10.5px var(--mono); font-style: normal; letter-spacing: .12em; color: var(--accent); }
     
      .lp-cols b[lang='ar'] { font: 700 24px/1.4 'Amiri', 'Noto Naskh Arabic', serif; }
      .lp-cols small { display: block; margin-top: 8px; font: 500 10.5px var(--mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted, var(--ink-3)); }
      html[lang='ar'] .lp-cols small { font: 400 13px 'Noto Naskh Arabic', serif; letter-spacing: 0; text-transform: none; }
      /* one verse = one row of four cells */
      .lp { padding: 0; scroll-margin-top: 112px; }
      .lp-body { position: relative; padding: 34px 0 8px; border-bottom: 1px solid var(--rule); }
      .lp-rules { position: absolute; inset: 0; direction: ltr; display: grid; grid-template-columns: var(--lp-cols); pointer-events: none; }
      .lp-rules i + i { border-left: 1px solid var(--rule-soft); }
      .lp__sep { display: block; width: 22px; height: 1px; margin: 30px 0 28px; background: var(--rule); }
      .lp__c--ar .lp__sep { margin-left: auto; }
      .lp__row { display: grid; grid-template-columns: var(--lp-cols); direction: ltr; align-items: start; }
      .lp:target .lp__row { background: rgba(122, 31, 43, .045); box-shadow: 0 0 0 10px rgba(122, 31, 43, .045); }
      .lp__c { position: relative; padding: 2px 22px 4px; }
      .lp__v { margin: 0; font: 400 20px/1.5 'Instrument Serif', Georgia, serif; color: var(--ink); letter-spacing: .005em; }
      .lp__c .ln { display: block; padding-left: 1.25em; text-indent: -1.25em; }     /* a line that wraps hangs, so a new line of the verse stays a new line */
      .lp__c--la .lp__v { font-style: italic; color: var(--ink-2, var(--ink)); }
      .lp__c--la .ln { position: relative; padding-left: 3em; text-indent: -.8em; }
      .lp__c--la .no { position: absolute; left: 0; top: .52em; width: 2em; font: 500 10px var(--mono); font-style: normal; letter-spacing: .04em; text-indent: 0; color: var(--accent); opacity: .85; }
      /* the Arabic reads right to left; its lines go in couplets, a little air after every second line */
      .lp__c--ar .lp__v { font: 400 20px/2.25 'Noto Naskh Arabic', 'Amiri', serif; letter-spacing: 0; }
      .lp__c--ar .ln { padding-left: 0; padding-right: 1.4em; text-indent: -1.4em; }
      .lp__c--ar .ln:nth-child(even):not(:last-child) { margin-bottom: .55em; }
      .lp-src { margin: 34px auto 0; padding: 0; list-style: none; max-width: 760px; }
      .lp-h { max-width: 760px; margin-left: auto; margin-right: auto; }
      .lp-src li { margin: 0 0 12px; font-size: 14.5px; line-height: 1.65; color: var(--ink-2, var(--ink)); }
      /* below 1100 px: one language at a time, chosen in the head; its column runs down the page as one text
         (without JavaScript: all four, one under the other, each with its name) */
      @media (max-width: 1099px) {
        .lp-note { display: block; }
        .lp-rules { display: none; }
        .lp-body { max-width: 640px; margin: 0 auto; }
        .lp-cols { grid-template-columns: repeat(4, minmax(0, 1fr)); max-width: 640px; margin: 22px auto 0; padding: 0; }
        .lp-cols::after { left: 0; right: 0; }
        .lp-cols button, .lp-cols button[data-l='ar'] { padding: 14px 4px 12px; text-align: center; cursor: pointer; -webkit-tap-highlight-color: transparent; }
        .lp-cols button:disabled { cursor: pointer; }
        .lp-cols b { font-size: 23px; } .lp-cols b[lang='ar'] { font-size: 20px; }
        .lp-cols b::after { display: none; }
        .lp-cols small { margin-top: 4px; }
        .lp-cols button[aria-pressed='true'] b { color: var(--accent); }
        .lp-cols button::after { content: ''; position: absolute; left: 22%; right: 22%; bottom: -1px; height: 2px; background: var(--accent); transform: scaleX(0); transition: transform .28s ease; }
        .lp-cols button[aria-pressed='true']::after { transform: scaleX(1); }
        .lp__row { grid-template-columns: minmax(0, 1fr); row-gap: 18px; }
        .lp__c { padding: 2px 4px 4px; }
        .lp__c::after { content: attr(data-name); display: block; margin: 0 0 6px; font: 500 10.5px var(--mono); letter-spacing: .14em; text-transform: uppercase; color: var(--accent); }
        .lp__c { display: flex; flex-direction: column; } .lp__c .lp__sep { order: -2; } .lp__c::after { order: -1; } .lp__c .lp__v { order: 2; }
        .lp__c--ar::after { font: 700 15px 'Amiri', serif; letter-spacing: 0; text-transform: none; text-align: right; }
        .lp__c--ar .lp__v { text-align: right; }
        .js .lp__c::after { display: none; }
        .js .lp-book[data-show='la'] .lp__c:not(.lp__c--la), .js .lp-book[data-show='en'] .lp__c:not(.lp__c--en),
        .js .lp-book[data-show='de'] .lp__c:not(.lp__c--de), .js .lp-book[data-show='ar'] .lp__c:not(.lp__c--ar) { display: none; }
        .js .lp__row { row-gap: 0; }
        .js .lp__v { animation: lp-turn .32s ease both; }
      }
      /* phones: a narrower frame and smaller head */
      @media (max-width: 760px) {
        .lp-book { margin-top: 30px; }
        .lp-cols { max-width: none; }
        .lp-cols .ix { display: none; }
        .lp-cols b { font-size: 19px; } .lp-cols b[lang='ar'] { font-size: 17px; }
        .lp-cols small { display: none; }
        .lp__v { font-size: 20.5px; } .lp__c--ar .lp__v { font-size: 21px; }
        .lp__c--la .ln { padding-left: 2.8em; }
      }
      @keyframes lp-turn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
      @media (prefers-reduced-motion: reduce) { .js .lp__v { animation: none; } .lp-cols button::after { transition: none; } }
"""
JS = """    <script>
      /* Below 1100 px: the four buttons above the poem choose the language shown; at first it is the language of the page. */
      (function () {
        var book = document.querySelector('.lp-book'), btns = book.querySelectorAll('.lp-cols button'), mq = window.matchMedia('(max-width: 1099px)');
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
            nothing is ever born from nothing, and nothing is destroyed into nothing. The small numbers beside the Latin are
            its line numbers.
          </p>
          <p class="lp-note">On a narrower screen the four languages are shown one at a time: choose one with the buttons above the poem.</p>
        </div>
      </div>

      <article class="lp-book">
        <div class="lp-cols" role="group" aria-label="Language shown">
          <button type="button" data-l="la" aria-pressed="false"><i class="ix" aria-hidden="true">01</i><b lang="la" translate="no">Latina</b><small>the original</small></button>
          <button type="button" data-l="en" aria-pressed="false"><i class="ix" aria-hidden="true">02</i><b lang="en" translate="no">English</b><small translate="no">Leonard, 1916</small></button>
          <button type="button" data-l="de" aria-pressed="false"><i class="ix" aria-hidden="true">03</i><b lang="de" translate="no">Deutsch</b><small translate="no">Diels, 1924</small></button>
          <button type="button" data-l="ar" aria-pressed="false"><i class="ix" aria-hidden="true">04</i><b lang="ar" translate="no">العربية</b><small>made for this site</small></button>
        </div>
        <div class="lp-body">
          <div class="lp-rules" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
{chr(10).join(secs)}
        </div>
      </article>

      <h2 class="lp-h">Sources</h2>
      <ul class="lp-src">
        <li><b>Latin.</b> <a href="https://www.thelatinlibrary.com/lucretius/lucretius1.shtml">The Latin Library</a>, Book I, lines 146 to 224, line by line. The Latin has fewer lines than Leonard’s English, so the four columns run by sentence, not by line: the numbers over each verse say which lines of the Latin it renders.</li>
        <li><b>English.</b> William Ellery Leonard, <i>Of the Nature of Things: A Metrical Translation</i> (1916), <a href="https://www.gutenberg.org/ebooks/785">Project Gutenberg 785</a>, public domain. His verse takes more lines than the Latin.</li>
        <li><b>German.</b> Hermann Diels, <i>Lukrez: Von der Natur</i> (Berlin, 1924), line for line, from <a href="https://www.textlog.de/lukrez-natur-dinge.html">textlog.de</a>. Two places are corrected: “wild” to “wird” (line 156, as the excerpt in the Falter has it) and the break of line 147. Line 173 is as printed online and has not been compared with the book.</li>
        <li><b>Arabic.</b> Made for this site on 13 November 2026, translated from the Latin verse by verse, as a poem: it takes the same freedom with the Latin that Leonard’s English takes. It is free verse in modern literary Arabic, fully vowelled, with rhyme only here and there and no classical metre. It is not a published translation and has not been checked by a second reader. The only published Arabic translation, from the Egyptian National Centre for Translation (Cairo, 2018), is under copyright and was not used.</li>
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

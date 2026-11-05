# Puts Lucretius I 146-158 into the first screen of the home page (index.html): in the hero's right column, above the live
# pendulum, between <!--LUCRETIUS--> markers; the name becomes a small line over the title "Work and study archive".
# The text comes from poem-146-224.json (cut from the sources by extract.py), never retyped. Run from the repository root.
import json, io, html, re
G = json.load(io.open('notes/lucretius/poem-146-224.json', encoding='utf-8'))[:4]
assert [g['lines'][0] for g in G] == [146, 149, 151, 156] and G[3]['lines'][-1] == 155
g0 = G[0]['de']
if g0[1].endswith('leuchtende') and g0[2].startswith('Helle Scheuchen'):   # Diels' line 147 ends with "Helle" (meter, Falter)
    G[0]['de'] = [g0[0], g0[1] + ' Helle', 'S' + g0[2][len('Helle S'):]]
E = html.escape
rows = ''.join(f'<p class="lq-s" data-g="{k}" tabindex="0" translate="no" lang="la">' + ''.join(f'<span class="lq-l">{E(t)}</span>' for t in g['la']) + '</p>' for k, g in enumerate(G))
data = json.dumps([{'n': [min(g['lines']), max(g['lines'])], 'en': g['en'], 'de': g['de']} for g in G], ensure_ascii=False)
block = """<!--LUCRETIUS-->
        <div class="lq" id="lq-wall" dir="ltr">
          <style>
            /* Lucretius beside the name: the Latin as an inscription; a published translation of each sentence rises over the page */
            .hero__side { display: flex; flex-direction: column; gap: clamp(12px, 2.4svh, 22px); min-width: 0; }
            .hero__side .figure__stage { aspect-ratio: 4 / 3; }
            .lq { position: relative; padding: 2px 0 2px 16px; border-left: 2px solid var(--accent); animation: fade 1.2s 0.2s ease both; }
            .lq, .lq * { box-sizing: border-box; }
            .lq-s { width: fit-content; max-width: 100%; margin: 0 0 .35em; padding: 1px 10px 1px 4px; margin-left: -4px; border-radius: 6px; cursor: default; outline: none; transition: background-color .25s ease; }
            .lq-l { display: block; font-family: 'Instrument Serif', Georgia, serif; font-size: clamp(15px, min(1.45vw, 2.15svh), 19.5px); line-height: 1.3; color: var(--ink); transition: color .25s ease; }
            .lq-s.is-on { background: rgba(122, 31, 43, .06); } .lq-s.is-on .lq-l { color: var(--accent-dark); } .lq-s:focus-visible { box-shadow: 0 0 0 2px var(--accent); }
            .lq-k { margin: 6px 0 0; font-family: var(--mono); font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
            .lq-card { position: absolute; z-index: 20; left: 0; width: min(460px, 92vw); padding: 12px 16px; background: var(--card); border: 1px solid var(--rule); border-left: 3px solid var(--accent); border-radius: 10px; box-shadow: 0 10px 30px rgba(60, 40, 20, .14); opacity: 0; transform: translateY(8px); pointer-events: none; transition: opacity .18s ease, transform .26s cubic-bezier(.2, .7, .2, 1), top .26s cubic-bezier(.2, .7, .2, 1), left .26s cubic-bezier(.2, .7, .2, 1); }
            .lq-card.is-shown { opacity: 1; transform: none; } .lq-card.is-pinned { pointer-events: auto; }
            .lq-card__h { display: block; margin-bottom: 6px; font-family: var(--mono); font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
            .lq-card__l { display: block; font-family: var(--serif); font-style: italic; font-size: 15.5px; line-height: 1.5; color: var(--ink-2); }
            .lq-card__note, .lq-card__pin { display: block; margin-top: 7px; font-size: 12px; line-height: 1.5; color: var(--ink-3); } .lq-card__pin { font-family: var(--mono); font-size: 10.5px; color: var(--muted); }
            .lq-hide { display: none; }
            @media (prefers-reduced-motion: reduce) { .lq-card { transition: opacity .12s linear; transform: none; } }
          </style>
          """ + rows + """
          <p class="lq-k" id="lq-h" dir="auto">Lucretius, On the Nature of Things I 146–158 · rest the pointer on a sentence for a translation</p>
          <div class="lq-card" id="lq-card" role="status" aria-live="polite" hidden><span class="lq-card__h"></span><span class="lq-card__b"></span><span class="lq-card__note"></span><span class="lq-card__pin"></span></div>
          <div class="lq-hide" aria-hidden="true"><span id="lq-w-lines">Lines</span><span id="lq-cr-en">William Ellery Leonard, 1916</span><span id="lq-cr-de">Hermann Diels, 1924</span><span id="lq-w-pin">Kept open · click again or press Esc to close</span><span id="lq-w-ar">No free Arabic translation of these lines exists; the card shows the English of Leonard.</span><span id="lq-w-src">Latin: The Latin Library, checked against Hermann Diels’ edition (Berlin, 1923). The manuscripts give line 155 after 158.</span></div>
          <script>
          (function () {
            'use strict';
            var P = """ + data + """;
            var lang = (document.documentElement.lang || 'en').slice(0, 2), useDe = lang === 'de';
            var wall = document.getElementById('lq-wall'), card = document.getElementById('lq-card'), hero = document.getElementById('top');
            var hEl = card.querySelector('.lq-card__h'), bEl = card.querySelector('.lq-card__b'), nEl = card.querySelector('.lq-card__note'), pEl = card.querySelector('.lq-card__pin');
            var word = function (id) { return document.getElementById(id).textContent.replace(/\\s+/g, ' ').trim(); };
            var credit = word(useDe ? 'lq-cr-de' : 'lq-cr-en'), linesW = word('lq-w-lines'), pinW = word('lq-w-pin'), arW = word('lq-w-ar'), srcW = word('lq-w-src');
            var blocks = Array.prototype.slice.call(wall.querySelectorAll('.lq-s')), cur = -1, pinned = false, tShow = 0, tHide = 0;
            function mark(k) { blocks.forEach(function (b) { b.classList.toggle('is-on', +b.getAttribute('data-g') === k); }); }
            function fill(k) {
              var g = P[k], tr = useDe ? g.de : g.en, rtl = lang === 'ar' ? 'rtl' : 'ltr';
              hEl.textContent = linesW + ' \\u2066' + g.n[0] + '–' + g.n[1] + '\\u2069 · ' + credit; hEl.dir = rtl;
              bEl.textContent = ''; tr.forEach(function (l) { var s = document.createElement('span'); s.className = 'lq-card__l'; s.textContent = l; bEl.appendChild(s); }); bEl.lang = useDe ? 'de' : 'en'; bEl.dir = 'ltr';
              nEl.textContent = (lang === 'ar' ? arW + ' ' : '') + srcW; nEl.dir = rtl;
              pEl.textContent = pinned ? pinW : ''; pEl.hidden = !pinned; pEl.dir = rtl;
            }
            function place(b) {   // over the page beside the verse where the hero has room (left of it, over the text), else just below the sentence
              var wr = wall.getBoundingClientRect(), r = b.getBoundingClientRect(), hr = hero.getBoundingClientRect(), cw = card.offsetWidth, h = card.offsetHeight, left;
              if (wr.left - hr.left - 24 >= cw) left = -cw - 24; else left = Math.max(-wr.left + 8, Math.min(0, window.innerWidth - 8 - cw - wr.left));
              var top = r.top - wr.top; if (left >= 0 || wr.left - hr.left - 24 < cw) top = r.bottom - wr.top + 8;
              top = Math.min(top, window.innerHeight - 12 - h - wr.top); card.style.left = left + 'px'; card.style.top = Math.max(-wr.top + 8, top) + 'px';
            }
            function show(k) {
              clearTimeout(tHide); var b = blocks[k], first = card.hidden || !card.classList.contains('is-shown'); mark(k); fill(k); card.hidden = false; cur = k;
              if (first) { card.style.transition = 'none'; place(b); void card.offsetHeight; card.style.transition = ''; requestAnimationFrame(function () { card.classList.add('is-shown'); }); } else place(b);
              card.classList.toggle('is-pinned', pinned);
            }
            function hide(force) { if (pinned && !force) return; pinned = false; card.classList.remove('is-shown', 'is-pinned'); mark(-1); cur = -1; }
            function blockOf(el) { while (el && el !== wall) { if (el.classList && el.classList.contains('lq-s')) return el; el = el.parentNode; } return null; }
            wall.addEventListener('pointerover', function (e) { if (e.pointerType !== 'mouse' || pinned) return; var b = blockOf(e.target); if (!b) return;
              clearTimeout(tHide); clearTimeout(tShow); var k = +b.getAttribute('data-g'); tShow = setTimeout(function () { show(k); }, cur < 0 ? 150 : 70); });
            wall.addEventListener('pointerout', function (e) { if (e.pointerType !== 'mouse' || pinned) return; if (blockOf(e.relatedTarget)) return; clearTimeout(tShow); tHide = setTimeout(function () { hide(); }, 240); });
            wall.addEventListener('click', function (e) { var b = blockOf(e.target); if (!b) return; var k = +b.getAttribute('data-g'); clearTimeout(tShow); if (pinned && k === cur) { hide(true); return; } pinned = true; show(k); });
            document.addEventListener('click', function (e) { if (pinned && !wall.contains(e.target)) hide(true); });
            document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && cur >= 0) hide(true); });
            blocks.forEach(function (b) { b.addEventListener('focus', function () { if (!pinned) show(+b.getAttribute('data-g')); }); b.addEventListener('blur', function () { if (!pinned) hide(); });
              b.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); b.click(); } }); });
            window.addEventListener('resize', function () { if (cur >= 0) place(blocks[cur]); });
            window.LQ = { show: show, hide: hide, get cur() { return cur; }, get pinned() { return pinned; } };
          })();
          </script>
        </div>
        <!--/LUCRETIUS-->"""
F = 'index.html'; s = io.open(F, encoding='utf-8').read()
s = re.sub(r'\n*\s*<!--LUCRETIUS-->.*?<!--/LUCRETIUS-->\n?', '\n', s, flags=re.S)   # the old band under the hero, if any
old_h1 = '        <h1 class="hero__name">\n          <span>Numa</span><span>Koudsie<span class="dot">.</span></span>\n        </h1>\n'
if old_h1 in s: s = s.replace(old_h1, '        <p class="hero__who">Numa Koudsie</p>\n        <h1 class="hero__name">Work and study archive<span class="dot">.</span></h1>\n')
fig = '      <figure class="figure" aria-label="Live double pendulum drawing">'
if '<div class="hero__side">' not in s:
    i = s.index(fig); j = s.index('</figure>', i) + len('</figure>')
    s = s[:i] + '      <div class="hero__side">\n        ' + block + '\n' + s[i:j] + '\n      </div>' + s[j:]
else:
    s = s.replace('<div class="hero__side">\n', '<div class="hero__side">\n        ' + block + '\n', 1)
io.open(F, 'w', encoding='utf-8').write(s); print('ok')

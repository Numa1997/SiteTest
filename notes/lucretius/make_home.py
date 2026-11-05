# Puts Lucretius I 146-158 on the home page (index.html), between <!--LUCRETIUS--> markers right after the hero;
# the text comes from poem.json (cut from the sources by extract.py), never retyped.
import json, io, html, re
D = '/tmp/claude-0/-home-user-SiteTest/9d768e8a-f3c3-577b-b0b8-5569ed1470f1/scratchpad/luc/'
G = json.load(io.open(D + 'poem.json', encoding='utf-8'))[:4]
assert [g['lines'][0] for g in G] == [146, 149, 151, 156] and G[3]['lines'][-1] == 155
g0 = G[0]['de']; assert g0[1].endswith('leuchtende') and g0[2].startswith('Helle Scheuchen')   # Diels' line 147 ends with "Helle" (meter, Falter)
G[0]['de'] = [g0[0], g0[1] + ' Helle', 'S' + g0[2][len('Helle S'):]]
E = html.escape
rows = []
for k, g in enumerate(G):
    ls = ''.join(f'<span class="lq-l"><span class="lq-n" aria-hidden="true">{n if n in (146, 150, 155, 156) else ""}</span>{E(t)}</span>' for n, t in zip(g['lines'], g['la']))
    rows.append(f'        <p class="lq-s" data-g="{k}" tabindex="0" translate="no" lang="la">{ls}</p>')
data = json.dumps([{'n': [min(g['lines']), max(g['lines'])], 'en': g['en'], 'de': g['de']} for g in G], ensure_ascii=False)
block = """<!--LUCRETIUS-->
    <section class="lq" aria-labelledby="lq-h">
      <style>
        /* Lucretius on the home page: the Latin as an inscription; a published translation of each sentence rises beside it */
        .lq { max-width: 1100px; margin: 0 auto; padding: 0 32px 56px; box-sizing: border-box; } .lq *, .lq *::before, .lq *::after { box-sizing: border-box; }
        .lq-wall { position: relative; padding: clamp(20px, 3.4vw, 40px) clamp(14px, 3.4vw, 48px); background: linear-gradient(180deg, #f8f2e7, #f1e9db); border: 1px solid var(--rule); border-radius: 14px; }
        .lq-k { margin: 0 0 16px; padding-left: 3rem; font-family: var(--mono); font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); }
        .lq-s { width: fit-content; max-width: 100%; margin: 0 0 .45em; padding: 2px 14px 2px 0; border-radius: 8px; cursor: default; outline: none; transition: background-color .25s ease; }
        .lq-l { position: relative; display: block; padding-left: 3rem; font-family: 'Instrument Serif', Georgia, serif; font-size: clamp(19px, 2.2vw, 27px); line-height: 1.42; color: var(--ink); transition: color .25s ease; }
        .lq-n { position: absolute; left: 0; top: .6em; width: 2.3rem; text-align: right; font-family: var(--mono); font-size: 10.5px; line-height: 1; color: var(--muted); }
        .lq-s.is-on { background: rgba(122, 31, 43, .055); } .lq-s.is-on .lq-l { color: var(--accent-dark); } .lq-s:focus-visible { box-shadow: 0 0 0 2px var(--accent); }
        .lq-how { margin: 14px 0 0; padding-left: 3rem; font-size: 13px; color: var(--ink-3); }
        .lq-card { position: absolute; z-index: 5; left: clamp(14px, 3.4vw, 48px); width: min(560px, calc(100% - 2 * clamp(14px, 3.4vw, 48px))); padding: 13px 18px; background: var(--card); border: 1px solid var(--rule); border-left: 3px solid var(--accent); border-radius: 10px; box-shadow: 0 10px 30px rgba(60, 40, 20, .12); opacity: 0; transform: translateY(8px); pointer-events: none; transition: opacity .18s ease, transform .26s cubic-bezier(.2, .7, .2, 1), top .26s cubic-bezier(.2, .7, .2, 1); }
        .lq-card.is-shown { opacity: 1; transform: none; } .lq-card.is-pinned { pointer-events: auto; }
        .lq-card__h { display: block; margin-bottom: 7px; font-family: var(--mono); font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
        .lq-card__l { display: block; font-family: var(--serif); font-style: italic; font-size: 16px; line-height: 1.5; color: var(--ink-2); }
        .lq-card__note, .lq-card__pin { display: block; margin-top: 8px; font-size: 12.5px; line-height: 1.5; color: var(--ink-3); } .lq-card__pin { font-family: var(--mono); font-size: 10.5px; color: var(--muted); }
        .lq-src { margin: 10px 0 0; font-size: 12px; line-height: 1.55; color: var(--muted); max-width: none; }
        .lq-src a { color: inherit; } .lq-hide { display: none; }
        @media (max-width: 560px) { .lq { padding: 0 16px 40px; } .lq-wall { padding: 16px 8px 16px 4px; } .lq-l { font-size: clamp(15px, 4.2vw, 19px); } .lq-l, .lq-k, .lq-how { padding-left: 2.1rem; } .lq-n { width: 1.6rem; font-size: 9.5px; } .lq-card { left: 6px; width: calc(100% - 12px); } }
        @media (prefers-reduced-motion: reduce) { .lq-card { transition: opacity .12s linear; transform: none; } }
      </style>
      <div class="lq-wall" id="lq-wall" dir="ltr">
        <p class="lq-k" id="lq-h" dir="auto">Lucretius · On the Nature of Things · Book I, lines 146–158</p>
""" + '\n'.join(rows) + """
        <p class="lq-how" dir="auto">Rest the pointer on a line, or tap it, to read its sentence in a published translation.</p>
        <div class="lq-card" id="lq-card" role="status" aria-live="polite" hidden><span class="lq-card__h"></span><span class="lq-card__b"></span><span class="lq-card__note"></span><span class="lq-card__pin"></span></div>
      </div>
      <p class="lq-src">Latin: <a href="https://www.thelatinlibrary.com/lucretius/lucretius1.shtml">The Latin Library</a>, checked against Hermann Diels’ edition (Berlin, 1923). English: William Ellery Leonard (1916, <a href="https://www.gutenberg.org/ebooks/785">Project Gutenberg</a>). German: Hermann Diels (1924). The manuscripts give line 155 after 158.</p>
      <div class="lq-hide" aria-hidden="true"><span id="lq-w-lines">Lines</span><span id="lq-cr-en">William Ellery Leonard, 1916</span><span id="lq-cr-de">Hermann Diels, 1924</span><span id="lq-w-pin">Kept open · click again or press Esc to close</span><span id="lq-w-ar">No free Arabic translation of these lines exists; the card shows the English of Leonard.</span></div>
      <script>
      (function () {
        'use strict';
        var P = """ + data + """;
        var lang = (document.documentElement.lang || 'en').slice(0, 2), useDe = lang === 'de';
        var wall = document.getElementById('lq-wall'), card = document.getElementById('lq-card');
        var hEl = card.querySelector('.lq-card__h'), bEl = card.querySelector('.lq-card__b'), nEl = card.querySelector('.lq-card__note'), pEl = card.querySelector('.lq-card__pin');
        var word = function (id) { return document.getElementById(id).textContent.replace(/\\s+/g, ' ').trim(); };
        var credit = word(useDe ? 'lq-cr-de' : 'lq-cr-en'), linesW = word('lq-w-lines'), pinW = word('lq-w-pin'), arW = word('lq-w-ar');
        var blocks = Array.prototype.slice.call(wall.querySelectorAll('.lq-s')), cur = -1, pinned = false, tShow = 0, tHide = 0;
        function mark(k) { blocks.forEach(function (b) { b.classList.toggle('is-on', +b.getAttribute('data-g') === k); }); }
        function fill(k) {
          var g = P[k], tr = useDe ? g.de : g.en;
          hEl.textContent = linesW + ' \\u2066' + g.n[0] + '–' + g.n[1] + '\\u2069 · ' + credit; hEl.dir = lang === 'ar' ? 'rtl' : 'ltr';
          bEl.textContent = ''; tr.forEach(function (l) { var s = document.createElement('span'); s.className = 'lq-card__l'; s.textContent = l; bEl.appendChild(s); }); bEl.lang = useDe ? 'de' : 'en'; bEl.dir = 'ltr';
          nEl.textContent = lang === 'ar' ? arW : ''; nEl.hidden = lang !== 'ar'; nEl.dir = lang === 'ar' ? 'rtl' : 'ltr';
          pEl.textContent = pinned ? pinW : ''; pEl.hidden = !pinned; pEl.dir = lang === 'ar' ? 'rtl' : 'ltr';
        }
        function place(b) {   // beside the sentence where the wall has room on its right; otherwise above it, or below it near the top of the window
          var wr = wall.getBoundingClientRect(), r = b.getBoundingClientRect(), right = 0, h;
          blocks.forEach(function (x) { right = Math.max(right, x.getBoundingClientRect().right - wr.left); });
          var room = wr.width - right - parseFloat(getComputedStyle(wall).paddingRight);
          if (room >= 320) { card.style.left = (right + 24) + 'px'; card.style.width = Math.min(520, room - 24) + 'px'; h = card.offsetHeight;
            var top = Math.min(r.top - wr.top, window.innerHeight - 12 - h - wr.top); card.style.top = Math.max(8, Math.min(top, wall.clientHeight - h - 8)) + 'px'; return; }
          card.style.left = ''; card.style.width = ''; h = card.offsetHeight;
          card.style.top = (r.top - h - 12 >= 8 ? r.top - wr.top - h - 12 : r.bottom - wr.top + 12) + 'px';
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
    </section>
    <!--/LUCRETIUS-->"""
F = '/home/user/SiteTest/index.html'; s = io.open(F, encoding='utf-8').read()
if '<!--LUCRETIUS-->' in s: s = re.sub(r'<!--LUCRETIUS-->.*?<!--/LUCRETIUS-->', lambda m: block, s, flags=re.S)
else:
    a = '    </header>\n'; assert s.count(a) == 1; s = s.replace(a, a + '\n    ' + block + '\n', 1)
io.open(F, 'w', encoding='utf-8').write(s); print('ok', len(block))

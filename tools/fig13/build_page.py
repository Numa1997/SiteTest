"""Fig. 13: the page's one lecture note, assembled from its four sources and written into public/simulations/momentum-spirographs.html.

Numa, 11 November 2026: everything made around Fig. 13 sits on the Fig. 13 page, all its theory included. The theory was written as
four notes; this script joins them into one article with one numbering of sections and equations:

    Part I    the sheet and the eye                 tools/fig13/fig13_note.html                 (edit there)
    Part II   one cell becomes the butterfly         public/simulations/butterfly-dashboard.html (its note) + tools/fig13/butterfly_note.html
    Part III  the flower hunt                        public/simulations/flower-hunt.html         (its note)
    Part IV   catching the butterfly                 tools/fig13/catch_note_body.html            (also the body of butterfly-catch.html)

In each part after the first, \\tag{n}, references "(n)" to that part's own equations, "section n" and "Example n.m" are shifted; links
to the other Fig. 13 pages become links to their place on this page; ids are checked to be unique. In butterfly_note.html a reference
to an equation of Part I is written ⟦n⟧ and "section n" there already uses the final numbers (checked below).

    python3 tools/fig13/build_page.py          # rewrite the article in the page
    python3 tools/fig13/build_page.py --check  # fail if the page's article is not what the sources give
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGE = ROOT / 'public/simulations/momentum-spirographs.html'
read = lambda p: (ROOT / p).read_text(encoding='utf8')
LINKS = {'flower-hunt.html': '#hunt', 'butterfly-dashboard.html': '#butterfly', 'butterfly-catch.html': '#catch', 'momentum-spirographs.html': '#sheet'}


def article(text):
    return text[text.index('<article class="paper"'):text.index('</article>')]


def sections(art):
    return re.findall(r'[ \t]*<section class="psec".*?</section>\n?', art, flags=re.S)


def abstract(art):
    m = re.search(r'<div class="paper__abstract"><b>Abstract\.</b>\s*(.*?)</div>', art, flags=re.S)
    return m.group(1).strip() if m else ''


def shift(sec, eq_off, sec_off, own_tags):
    if eq_off:
        sec = re.sub(r'\\tag\{(\d+)\}', lambda m: '\\tag{%d}' % (int(m.group(1)) + eq_off), sec)
        sec = re.sub(r'(?<=[\s>])\((\d{1,2})\)', lambda m: '(%d)' % (int(m.group(1)) + eq_off) if int(m.group(1)) in own_tags else m.group(0), sec)
    if sec_off:
        sec = re.sub(r'([Ss]ections? )(\d+)( to )?(\d+)?', lambda m: m.group(1) + str(int(m.group(2)) + sec_off) + (m.group(3) + str(int(m.group(4)) + sec_off) if m.group(3) else ''), sec)
        sec = re.sub(r'Example (\d+)\.(\d+)', lambda m: 'Example %d.%s' % (int(m.group(1)) + sec_off, m.group(2)), sec)
    sec = re.sub(r'href="(%s)(#[^"]*)?"' % '|'.join(re.escape(k) for k in LINKS), lambda m: 'href="%s"' % LINKS[m.group(1)], sec)
    return re.sub(r'⟦(\d+)⟧', r'(\1)', sec)


def build():
    I = article(read('tools/fig13/fig13_note.html'))
    D = article(read('public/simulations/butterfly-dashboard.html'))
    Bn = read('tools/fig13/butterfly_note.html')
    H = article(read('public/simulations/flower-hunt.html'))
    C = article(read('tools/fig13/catch_note_body.html'))
    dsec = sections(D)
    for i, key in enumerate(('d-plane', 'd-waves', 'd-turn', 'd-needs')):          # the dashboard's note has no ids and plain numbers
        dsec[i] = dsec[i].replace('<section class="psec">', '<section class="psec" id="%s">' % key, 1)
        dsec[i] = re.sub(r'<h3>\d+\. ', '<h3><span class="psec__n">00</span>', dsec[i], count=1)
    parts = [
        ('I', 'The sheet and the eye', '', sections(I), 0),
        ('II', 'One cell becomes the butterfly', 'One strike of the sheet draws a butterfly. This part looks at that one pendulum: the wall its tip moves in, the two waves that are its height and its sideways position, how turning the paper makes a wave into the butterfly, and what the machine does in numbers. The dashboard above (<a href="#butterfly">The butterfly</a>) shows it; the film "built by hand" draws it with a ruler.', dsec + sections(Bn), None),
        ('III', 'The flower hunt: which strikes close', abstract(H), sections(H), None),
        ('IV', 'Catching the butterfly with a motor', abstract(C), sections(C), None),
    ]
    out_secs, toc, n_sec, n_eq = [], [], 0, 0
    for key, title, lead, secs, _ in parts:
        own = set()
        blocks = []
        # the dashboard's four sections and the butterfly section number their equations separately: shift each source by what came before
        groups = [secs] if key != 'II' else [secs[:4], secs[4:]]
        sec_off = n_sec if key != 'I' else 0
        for g in groups:
            tags = {int(t) for s in g for t in re.findall(r'\\tag\{(\d+)\}', s)}
            for s in g:
                blocks.append(shift(s, n_eq if key != 'I' else 0, sec_off if g is not secs or key != 'II' else sec_off, tags) if not (key == 'II' and g is groups[1]) else shift(s, n_eq, 0, tags))
            n_eq += len(tags)
        toc.append('                        <li class="toc-part">Part %s · %s</li>' % (key, title))
        head = '' if key == 'I' else ('                    <div class="ppart-head" id="part-%s">\n                        <p class="paper__kicker">Part %s</p>\n                        <h3 class="ppart-title">%s</h3>\n                        <p>%s</p>\n                    </div>\n' % (key.lower(), key, title, shift(lead, 0, 0, set())))
        for b in blocks:
            n_sec += 1
            b = re.sub(r'<span class="psec__n">\d+</span>', '<span class="psec__n">%02d</span>' % n_sec, b, count=1)
            sid = re.search(r'<section class="psec" id="([^"]+)"', b).group(1)
            name = re.sub(r'<[^>]+>', '', re.search(r'<h3>(.*?)</h3>', b, flags=re.S).group(1)); name = re.sub(r'^\d+', '', name).replace('★', '').strip()
            toc.append('                        <li><a href="#%s"><span>%d</span>%s</a></li>' % (sid, n_sec, name))
            out_secs.append(head + b if head else b); head = ''
    body = '\n'.join(s.rstrip('\n') + '\n' for s in out_secs)
    head_I = I[:I.index('<div class="paper__grid">')]
    head_I = head_I.replace('Everywhere else a hard strike makes gravity a small correction, and the tip draws a ring or a rosette.</div>',
                            'Everywhere else a hard strike makes gravity a small correction, and the tip draws a ring or a rosette. The note has four parts: the sheet and the eye; the one strike that draws a butterfly; the hunt for the strikes whose drawings close; and the motor that takes a chaotic pendulum, sets it on the butterfly and lets go.</div>')
    assert 'four parts' in head_I
    art = (head_I + '<div class="paper__grid">\n                <nav class="paper__toc" aria-label="Contents">\n                    <p>Contents</p>\n                    <ol>\n'
           + '\n'.join(toc) + '\n                    </ol>\n                </nav>\n                <div class="paper__body">\n\n' + body + '                </div>\n            </div>\n        ')
    ids = re.findall(r'\sid="([^"]+)"', art); dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, 'duplicate ids: %s' % dup
    tags = [int(t) for t in re.findall(r'\\tag\{(\d+)\}', art)]
    assert tags == list(range(1, len(tags) + 1)), 'equation numbers not in order: %s' % tags
    for m in re.finditer(r'[Ss]ections? (\d+)', art): assert int(m.group(1)) <= n_sec, m.group(0)
    return art, n_sec, len(tags)


def main():
    art, n_sec, n_eq = build()
    page = PAGE.read_text(encoding='utf8')
    a, b = page.index('<article class="paper"'), page.index('</article>')
    if '--check' in sys.argv:
        if page[a:b] != art: sys.exit('the article in momentum-spirographs.html is not what the sources give: run tools/fig13/build_page.py')
        print('article up to date: %d sections, %d equations' % (n_sec, n_eq)); return
    PAGE.write_text(page[:a] + art + page[b:], encoding='utf8')
    print('wrote the article: %d sections, %d equations' % (n_sec, n_eq))


if __name__ == '__main__':
    main()

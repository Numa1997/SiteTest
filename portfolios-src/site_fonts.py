"""Shared by the portfolio builders' --site mode: link the site's own font files instead of embedding them.

A study page embeds its fonts as base64 data: URIs, so that the standalone file works anywhere. On Phyein Usul the same bytes are
already served as files (public/fonts/, public/vendor/katex/fonts/): every embedded woff2 of Rotor Pendula and the Hydraulic Press
Study is byte-identical to one of them (checked by MD5 on 31 October 2026). Embedded, the fonts are about 1.3 MB of base64 in each
combined page (about two thirds of its Brotli-compressed size, sent again on every visit because Cloudflare sends HTML without an
ETag); linked, the browser fetches each file once and keeps it for every page and tab. See docs/performance.md.

link_fonts(html, site) replaces each url(data:font/woff2;base64,...) whose bytes match a site file with url(../../<that file>),
the path from public/portfolios/<study>/ (srcdoc frames resolve relative addresses against the parent page). A font the site does
not serve, or a font embedded in any other form, stops the build, so a page never silently loses a face or keeps a copy.
"""
import base64
import hashlib
import pathlib
import re

DATA_FONT = re.compile(r"""url\(\s*(["']?)data:font/woff2;base64,([A-Za-z0-9+/=]+)\1\s*\)""")


def site_font_files(site):
    """MD5 of every woff2 the site serves -> its path under public/. Where two files hold the same bytes, the copy the site's own
    stylesheets link wins (KaTeX's from vendor/katex/fonts/, the rest from fonts/), so a reader's cache holds one copy."""
    public = pathlib.Path(site) / 'public'
    files = sorted(public.glob('vendor/katex/fonts/*.woff2')) + sorted(public.glob('fonts/**/*.woff2'))
    linked = ''.join(p.read_text() for p in list(public.glob('fonts/*.css')) + [public / 'vendor/katex/katex.min.css'])
    out = {}
    for f in files:
        md5 = hashlib.md5(f.read_bytes()).hexdigest()
        rel = f.relative_to(public).as_posix()
        if md5 not in out or (f.name in linked and out[md5].split('/')[-1] not in linked):
            out[md5] = rel
    return out


def link_fonts(html, site, depth='../../'):
    table = site_font_files(site)

    def one(m):
        md5 = hashlib.md5(base64.b64decode(m.group(2))).hexdigest()
        assert md5 in table, f'an embedded font (md5 {md5}) is not among the site files in public/fonts/ or public/vendor/katex/fonts/'
        return f"url({depth}{table[md5]})"

    out = DATA_FONT.sub(one, html)
    # any font still embedded in another form (font/woff, application/font-woff2, a charset, line breaks) stops the build too
    left = re.search(r'data:(?:font/|application/(?:x-)?font)', out)
    assert not left, f'an embedded font in a form link_fonts does not read: {out[left.start():left.start() + 60]!r}'
    return out

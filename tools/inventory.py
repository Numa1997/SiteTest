#!/usr/bin/env python3
"""Every file in the repository, one line each: its size, what it is, and the page of docs/ that explains it.

Run from anywhere inside the repository:
    python3 tools/inventory.py           writes docs/files.md
    python3 tools/inventory.py --check   writes nothing; exits 1 if a file has no description here
                                         or if docs/files.md is not what this script would write now

How it works: it asks git for the list of files (tracked, plus new files that are not ignored), gives each file
the description of the first rule below whose pattern matches its path, and writes one table per folder.
A file that matches no rule is an error: add a rule (and, if it is a new kind of file, a page in docs/) before
committing. Titles of simulations come from public/scripts/catalog.js and the walkthrough keys from the pages'
data-walk attributes, so a new simulation is described as soon as it is registered there.
Standard library only (Python 3.8 or newer)."""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = 'docs/files.md'


def files():
    out = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
                         cwd=ROOT, check=True, capture_output=True).stdout.decode('utf-8')
    return sorted({p for p in out.split('\0') if p and os.path.isfile(os.path.join(ROOT, p))})


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return f.read()


def catalog():
    """Fig. number, id and title of each simulation page, read from the registry."""
    src = read('public/scripts/catalog.js')
    src = src[src.index('window.SIMULATIONS'):]  # skip SIM_FIELDS, whose one-line entries also start with id:
    sims = {}
    for block in re.findall(r'\{\s*id:\s*\'[^\']+\'.*?\n\s{8}\}', src, re.S):
        get = lambda key: re.search(key + r":\s*'([^']*)'", block)
        fig = re.search(r'fig:\s*(\d+)', block)
        if get('id') and fig and get('title') and get('file'):
            sims['public/' + get('file').group(1)] = (int(fig.group(1)), get('id').group(1), get('title').group(1))
    return sims


def walk_keys(sims):
    """Walkthrough key → (fig, title), from data-walk="…" in each simulation page."""
    keys = {}
    for page, (fig, _, title) in sims.items():
        m = re.search(r'data-walk="([a-z0-9-]+)"', read(page))
        if m:
            keys[m.group(1)] = (fig, title)
    return keys


def heading(path):
    for line in read(path).splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return 'Documentation page'


SIMS = catalog()
BY_ID = {sid: (fig, title) for _, (fig, sid, title) in SIMS.items()}
WALKS = walk_keys(SIMS)


def sim_doc(fig, sid):
    return 'docs/simulations/fig%02d-%s.md' % (fig, sid)


# (pattern, description, doc). The first matching pattern wins. A description may be a function of the regex match.
RULES = [
    # the repository's own files (not part of the app)
    (r'README\.md', 'Start here: what the project is, how the files fit together, where each one is explained.', 'README.md'),
    (r'docs/files\.md', 'This list. Written by tools/inventory.py; do not edit by hand.', 'docs/files.md'),
    (r'docs/.+\.md', lambda m: 'Documentation: ' + heading(m.group(0)) + '.', None),
    (r'\.gitignore', 'Files git leaves out: Python caches, node_modules, build output.', 'docs/files.md'),
    (r'notes/home/(measure|longlines|sections)\.cjs', 'Browser measurements of the home page: index size, column widths, characters per line, section screenshots.', 'docs/styles.md'),
    (r'tools/perf/(serve|measure|tabs|interact|trace|loadtrace|margin|foldtap|clockcheck|film|addresses)\.cjs', lambda m: {'serve': 'A local server that answers like Cloudflare does for phyeinusul.com (Brotli, _headers, no ETag on HTML, .html -> 307), for before-and-after measurements.', 'measure': 'Page loads on a throttled phone (Slow 4G or 4G, CPU 4x): LCP, CLS, blocking time, bytes, a repeat visit; the median of several runs.', 'tabs': 'The study pages with tabs: time until the first tab is drawn, each tab switch, a repeat visit.', 'interact': 'Clicks a reader makes (page to page, Solve, data panel, folds, study tabs), timed by the Event Timing API.', 'trace': 'What fills the main thread while a page sits idle, at the top or scrolled down: trace totals, forced layouts, JS self time.', 'loadtrace': 'The long parse, layout and script pieces of a study page loading until its first tab is ready.', 'margin': "How close a study tab comes to the shell's 8 s limit: from its frame's creation to its ready message, on a slowed processor.", 'foldtap': 'A reader in a lecture note: how busy the main thread is, and how long closing and opening a fold takes.', 'clockcheck': 'Each figure runs on screen, holds off screen, resumes; the store stays live for an open data panel and the walkthrough.', 'film': 'A repeat visit as a reader sees it: screenshots at fixed times and every LCP candidate with its element, to tell a metric from the screen.', 'addresses': 'Every page at every address a reader can use (x.html, x, x/, folder/), and every link of every page, on a running site; exits 1 on any wrong answer.'}[m.group(1)], 'docs/performance.md'),
    (r'tools/redirects\.py', 'Writes public/_redirects, the short address of every page served without a round trip; --check fails if the file is out of date.', 'docs/usul.md'),
    (r'tools/inventory\.py', 'Writes docs/files.md and checks that every file in the repository is described.', 'docs/files.md'),
    # working notes of the Rotor Pendula and Droplet Collection studies (another session's work; start with status.md and brief.md)
    (r'notes/(droplets|rotor-pendula)/brief\.md', lambda m: 'The brief of the ' + {'droplets': 'Droplet Collection', 'rotor-pendula': 'Rotor Pendula'}[m.group(1)] + ' study: question, method and gates, for an agent working in a loop.', None),
    (r'notes/(droplets|rotor-pendula)/baseline/([a-z]+)\.html', lambda m: 'Text of the ' + m.group(2) + ' page of the published ' + {'droplets': 'Droplet Collection', 'rotor-pendula': 'Rotor Pendula'}[m.group(1)] + ' app, kept as the baseline the study starts from.', lambda m: {'droplets': 'notes/droplets/brief.md', 'rotor-pendula': 'notes/rotor-pendula/README.md'}[m.group(1)]),
    (r'portfolios-src/site_fonts\.py', "Shared by the Rotor Pendula and Hydraulic Press Study builders' --site mode: links each embedded font to the byte-identical file the site serves.", 'docs/performance.md'),
    (r'portfolios-src/rotor-pendula/fonts/(.+\.woff2)', lambda m: 'Self-hosted font for the Rotor Pendula notes build: ' + m.group(1) + '.', None),
    (r'portfolios-src/rotor-pendula/fonts/(.+)', lambda m: 'Fonts of the Rotor Pendula notes build: ' + m.group(1) + '.', None),
    (r'portfolios-src/rotor-pendula/tools/(.+)', lambda m: 'Build and check tool of the Rotor Pendula notes, adapted from the Hydraulic Press Study\'s tools: ' + m.group(1) + '.', None),
    # the site in German and Arabic (docs/i18n.md): English pages are the source, everything below is made from them
    (r'tools/i18n/build\.py', 'Writes the German and Arabic pages, the script strings and the mirrored stylesheets from the English pages and the tables; --check fails on anything untranslated.', 'docs/i18n.md'),
    (r'tools/i18n/ingest\.py', 'Stores checked translations made outside the tables (page pieces, script strings, walkthrough prose).', 'docs/i18n.md'),
    (r'i18n/(de|ar)/walk\.json', lambda m: {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ' prose of the ten walkthroughs, keyed by the English.', 'docs/i18n.md'),
    (r'public/scripts/walk/(de|ar)/([a-z]+)\.js', lambda m: {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ' walkthrough ' + m.group(2) + ', generated from the English one; do not edit.', 'docs/i18n.md'),
    (r'tools/i18n/hydraulics\.py', 'Builds the Hydraulic Press Study in German and Arabic from its unchanged English source, through the study\'s own tools.', 'docs/i18n.md'),
    (r'tools/i18n/wrap\.cjs', 'Wraps the reader-visible strings of a page\'s scripts in _t(), with a JavaScript parser (acorn).', 'docs/i18n.md'),
    (r'tools/i18n/apply_review\.py', 'Applies a reviewer\'s corrections, only those that keep markup, maths and numbers.', 'docs/i18n.md'),
    (r'tools/i18n/package\.json', 'The parser wrap.cjs needs (acorn); npm install --prefix tools/i18n.', 'docs/i18n.md'),
    (r'tools/i18n/fill\.py', 'Stores translations into a page table, recording the English each one was made from.', 'docs/i18n.md'),
    (r'i18n/(de|ar)/strings\.json', lambda m: {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ' words of the scripts and of the catalog, with plural forms.', 'docs/i18n.md'),
    (r'i18n/(de|ar)/(.+)\.json', lambda m: {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ' table of ' + m.group(2) + ': per piece, the English it was translated from and the translation.', 'docs/i18n.md'),
    (r'public/(de|ar)/(.+\.html)', lambda m: {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ' ' + m.group(2) + ', generated by tools/i18n/build.py; do not edit.', 'docs/i18n.md'),
    (r'public/scripts/i18n/strings-(de|ar)\.js', lambda m: 'The ' + {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ' string table the scripts read through T(), generated; do not edit.', 'docs/i18n.md'),
    (r'public/scripts/flip\.js', 'Turns the page over on a change of language (cross-document view transition), and only then.', 'docs/i18n.md'),
    (r'public/styles/i18n\.css', 'Language switch, Arabic fonts and the few right-to-left rules of the translated pages.', 'docs/styles.md'),
    (r'public/styles/([a-z]+)\.rtl\.css', lambda m: m.group(1) + '.css with left and right exchanged, for the Arabic pages; generated with rtlcss, do not edit.', 'docs/styles.md'),
    # the lecture-note review of 20 October 2026: not part of the site
    (r'\.claude/agents/([a-z-]+)\.md', lambda m: 'Claude Code agent definition: ' + m.group(1) + ', one role of the lecture-note review.', 'docs/notes.md'),
    (r'notes/STANDARD\.md', 'The standard the lecture notes are judged against, and Numa\'s verdicts.', 'docs/notes.md'),
    (r'notes/STATUS\.md', 'Status of the lecture-note review, one row per figure.', 'docs/notes.md'),
    (r'notes/verify\.mjs', 'Checks the ten simulation pages in headless Chromium at desktop and phone size.', 'docs/notes.md'),
    (r'notes/walkcheck\.cjs', 'Searches every quoted code line of the ten walkthroughs in its page.', 'docs/notes.md'),
    (r'notes/\.gitignore', 'Keeps the review\'s screenshots out of the repository.', 'docs/notes.md'),
    (r'notes/fig(\d\d)/plan\.md', lambda m: 'Fig. %d: the teacher\'s verdict on each section of the note, and what it changed.' % int(m.group(1)), 'docs/notes.md'),
    (r'notes/fig(\d\d)/check\.md', lambda m: 'Fig. %d: the derivation checker\'s table of equations and numbers.' % int(m.group(1)), 'docs/notes.md'),
    (r'notes/fig(\d\d)/referee\.md', lambda m: 'Fig. %d: the blind referee\'s report on the note.' % int(m.group(1)), 'docs/notes.md'),
    (r'notes/fig(\d\d)/walk\.md', lambda m: 'Fig. %d: the walkthrough check and its proposed fixes.' % int(m.group(1)), 'docs/notes.md'),
    (r'notes/fig11/checked\.html', lambda m: 'Fig. 11: working notes of 4 November 2026, every term of the model and of the rescue with its Wolfram check and the code that was run.', 'docs/notes.md'),
    (r'notes/fig11/status\.md', lambda m: 'Fig. 11: status of the rescue work (done with evidence, open items, decisions for Numa).', 'docs/notes.md'),
    (r'notes/fig11/project06/README\.md', 'Project 06: what each measurement script shows and what it gave.', 'docs/simulations/project06-rods-in-liquid.md'),
    (r'notes/fig11/project06/.+\.cjs', 'Project 06: a measurement in the running page (swing-up, planner, drag-and-release, flick, the deep flows\' starting strengths, the paddle ratio of note 13.7).', 'notes/fig11/project06/README.md'),
    (r'notes/fig11/project06/(samecode|i18n/validate)\.py', 'Project 06: a check (the two pages\' scripts identical; translations keep tags, maths and numbers).', 'notes/fig11/project06/README.md'),
    (r'notes/fig11/panel/README\.md', 'Project 05: what each honesty test of the data panel checks, and how to run it.', 'docs/simulations/fig11-double-inverted-pendulum.md'),
    (r'notes/fig11/panel/.+\.(cjs|py)', 'Project 05: an honesty test of the data panel (origin, replay, controller, picture, falsification, cost), or the masking and checked translations of its strings.', 'notes/fig11/panel/README.md'),
    (r'notes/fig11/panel/.+\.txt', 'Project 05: raw output of an honesty test or behaviour test of the data panel, 5 November 2026.', 'notes/fig11/panel/README.md'),
    (r'notes/skills/([a-z-]+)/SKILL\.md', lambda m: 'The revised skill ' + m.group(1) + ', to be uploaded to Numa\'s account (the synced copy in a session is read-only).', 'notes/fig11/panel/README.md'),
    (r'notes/fig(\d\d)/.+', lambda m: 'Fig. %d: a measuring script of the review, or its saved output.' % int(m.group(1)), 'docs/notes.md'),
    # root of the app
    (r'AGENTS\.md', "The maintainer's summary: ownership, layout, design rules, folds, the data pipeline, platform quirks.", 'docs/build-and-deploy.md'),
    (r'CLAUDE\.md', 'How Numa expects an AI assistant to work on the project.', 'docs/build-and-deploy.md'),
    (r'index\.html', 'The home page: CV, research, simulation plates, index; also the build entry page.', 'docs/pages.md'),
    (r'package\.json', 'Build declaration: vite build; template dependencies.', 'docs/build-and-deploy.md'),
    (r'vite\.config\.ts', 'Vite settings: relative base, output folder from the platform.', 'docs/build-and-deploy.md'),
    (r'tsconfig\.json', 'TypeScript settings for src/ (template; unused by the site).', 'docs/build-and-deploy.md'),
    (r'tailwind\.config\.js', 'Tailwind settings (template; unused by the site).', 'docs/build-and-deploy.md'),
    (r'postcss\.config\.js', 'PostCSS settings (template; unused by the site).', 'docs/build-and-deploy.md'),
    (r'src/main\.ts', 'Template script entry; index.html does not load it.', 'docs/build-and-deploy.md'),
    (r'src/styles\.css', 'Template Tailwind directives; unused.', 'docs/build-and-deploy.md'),
    (r'wrangler\.jsonc', 'Cloudflare settings: the Worker phyein-usul, the dist/ folder, the custom domains phyeinusul.com and www.', 'docs/usul.md'),
    (r'public/_redirects', 'Each page at its short address (x, folder/, /), for Cloudflare with html_handling none; written by tools/redirects.py, read by Cloudflare, never served.', 'docs/usul.md'),
    (r'public/_headers', 'Response headers Cloudflare sets on phyeinusul.com: security headers on every file, a year of caching for font files; read by Cloudflare, never served.', 'docs/usul.md'),
    (r'public/images/phyein-usul-mark\.svg', 'The Phyein Usul logo: above the name on the home page, linking home in the top bar of the other pages.', 'docs/assets.md'),
    # pages
    (r'public/simulations\.html', 'The simulations catalog: one titled fold card per simulation, search and chips.', 'docs/pages.md'),
    (r'public/portfolios\.html', 'The Portfolios page: the two research projects.', 'docs/pages.md'),
    (r'notes/lucretius/README\.md', 'Lucretius I 146-224 kept for the site: sources, corrections, what is where.', 'notes/lucretius/README.md'),
    (r'notes/lucretius/poem-146-224\.json', 'Lucretius I 146-224 per Latin sentence: Latin, Leonard (English), Diels (German), cut from the sources.', 'notes/lucretius/README.md'),
    (r'notes/lucretius/extract\.py', 'Cuts Lucretius I 146-224 out of the downloaded sources without retyping.', 'notes/lucretius/README.md'),
    (r'notes/lucretius/make_home\.py', 'Writes the Lucretius band of the home page from the first four sentences.', 'notes/lucretius/README.md'),
    (r'public/robots\.txt', 'Instructions for search-engine crawlers.', 'docs/pages.md'),
    (r'public/cv/index\.html', 'The CV page (phyeinusul.com/cv/): both pages of the CV as images, with Open and Download PDF.', 'docs/pages.md'),
    (r'public/cv/Numa_Koudsie_CV\.pdf', 'The CV as a two-page PDF (German, then English), linked from the CV page.', 'docs/pages.md'),
    (r'public/cv/cv-(de|en)\.webp', 'One page of the CV rendered at 170 dpi, shown on the CV page.', 'docs/pages.md'),
    (r'public/simulations/double-inverted-pendulum\.html', 'Project 05 · Balancing Two Rods on a Cart (Fig. 11 from 3 to 4 November 2026), in vacuum and air since 7 November 2026: the real-time simulation, its data panel, walkthrough and lecture note; listed on the Projects page, kept at this address so that its German and Arabic pages are generated with the simulations.', 'docs/simulations/fig11-double-inverted-pendulum.md'),
    (r'public/simulations/rods-in-liquid\.html', 'Project 06 · Balancing Two Rods in a Liquid (7 November 2026): project 05\'s script with its own settings, a machine that can swing the rods up in water, glycerol and honey, a slim cart, and the controller told the flow; data panel, walkthrough dipc and lecture note.', 'docs/simulations/project06-rods-in-liquid.md'),
    # Fig. 13 (8 November 2026): the momentum-space page, the flower hunt, the dashboard and the films; English only
    (r'public/simulations/momentum-spirographs\.html', 'Fig. 13 · Spirographs in Momentum Space: a live grid of double pendulums, each kicked with the (p1, p2) of its cell, drawn as long exposures over the chaos map.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/flower-hunt\.html', 'Fig. 13 study · The Flower Hunt: closed flowers and butterflies found as periodic orbits by Newton\'s method, a test bench and study notes.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/butterfly-dashboard\.html', 'Fig. 13 dashboard · The Wave and the Circle: the complex plane of the motion, its height and sideways position against time joined by straight lines, and the paper turned until each wave is the circle again (a wheel, the butterfly).', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/fig13/(bell|turning|together|dive)\.html', lambda m: 'Fig. 13 film that plays live in the browser, generated by tools/fig13/gift/publish_films.py from tools/fig13/gift/' + {'bell': 'butterfly3d', 'turning': 'morph', 'together': 'together', 'dive': 'dive'}[m.group(1)] + '.html; do not edit.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/fig13/orbit24\.json', 'The closed 24-petal butterfly orbit (theta1, theta2 over one period), copied from tools/fig13/gift/ by publish_films.py.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/fig13/dive/dive\.(json|bin)', lambda m: 'Data of the dive film, copied by publish_films.py: ' + {'json': 'the 9 x 9 grid of kicks and the butterfly\'s momenta', 'bin': 'float32 angles of the 81 pendulums, 400 samples per second for 9 s'}[m.group(1)] + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/images/fig13/chaos-map-rods-P20\.png', 'Fig. 13: the chaos map of momentum space (equal rods, P = 20 kg m^2/s), written by tools/fig13/map_png.py from chaos_map.py.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/scripts/fig13-engine\.js', 'Fig. 13: the general double pendulum (Hamilton\'s equations, RK4) and the long-exposure plate, shared by the Fig. 13 pages.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/scripts/fig13-hunt-data\.js', 'Fig. 13: the flowers and butterflies of the flower hunt, written by tools/fig13/hunt_export.py; do not edit.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/(chaos_map|map_png|hunt|hunt_inspect|hunt_export|butterfly)\.py', lambda m: 'Fig. 13 generator: ' + {'chaos_map': 'the chaos map of momentum space (twin pendulums, numba)', 'map_png': 'the chaos map as a PNG in the house palette', 'hunt': 'the flower hunt: g = 0 theory, scans and Newton\'s method for closed orbits', 'hunt_inspect': 'Poincare sections and Floquet traces of the hunted orbits', 'hunt_export': 'writes public/scripts/fig13-hunt-data.js', 'butterfly': 'the butterflies (one-petal resonance) closed by Newton\'s method, with their stability'}[m.group(1)] + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/(orbit|dive_data|publish_films)\.py', lambda m: 'Fig. 13 films: ' + {'orbit': 'exports one closed butterfly orbit (orbit24.json) with its checks', 'dive_data': 'integrates the 9 x 9 grid of kicks of the dive film (dive.bin, regenerated, about 47 s)', 'publish_films': 'copies the films into public/simulations/fig13/ where they play live'}[m.group(1)] + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/(butterfly3d|morph|together|dive)\.html', lambda m: 'Fig. 13 film source (' + {'butterfly3d': 'the bell above the floor, 3-D', 'morph': 'turning the paper: a wheel, the butterfly', 'together': 'six pictures on one clock, wide and phone layouts', 'dive': 'from a kick to a butterfly, phone first'}[m.group(1)] + '); render.cjs writes its frames.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/fig13/reem\.html', 'Fig. 13 gift film (For رِيمْ), not linked from the site: the name and فَرَاشَتُكِ written by turning arrows in gold, then it opens construction.html; generated by publish_films.py from tools/fig13/gift/reem.html; do not edit.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'(public/simulations/fig13|tools/fig13/gift)/reem\.json', 'Arrows (Fourier terms) and outlines of the words of the gift film, written by tools/fig13/gift/reem_data.py.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/reem\.html', 'Fig. 13 gift film source (For رِيمْ, phone first): the name (traced from the reference plate) and فَرَاشَتُكِ (Amiri) written by 640 turning arrows each, gold on navy or ink on paper.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/(reem_data|calligraphy)\.py', lambda m: {'reem_data': 'Fig. 13 gift: the Fourier terms of each word\'s outline (640 arrows), checked against the outline', 'calligraphy': 'Fig. 13 gift: outlines of Arabic words, shaped by HarfBuzz, flattened by fontTools'}[m.group(1)] + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/fonts/(NotoNastaliqUrdu-wght\.ttf|OFL-NotoNastaliqUrdu\.txt)', lambda m: 'Noto Nastaliq Urdu, the calligraphy font of the gift film (Google Fonts, SIL Open Font License 1.1): ' + ('the font' if m.group(1).endswith('ttf') else 'its licence') + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/fig13/construction\.html', 'Fig. 13 film that plays live: the butterfly built by hand from its two plots (a level and an upright line through a 45-degree mitre), a wheel first; generated by publish_films.py from tools/fig13/gift/construction.html; do not edit.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/construction\.html', 'Fig. 13 film source (phone first): the construction by ruler of a wheel and of the butterfly from h(t) and x(t), the two time axes joined by a mitre.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/fonts/(Amiri-Regular\.ttf|OFL-Amiri\.txt)', lambda m: 'Amiri (Khaled Hosny; SIL Open Font License 1.1), the Naskh of فَرَاشَتُكِ in the gift film and the master model of qalam2/3.py: ' + ('the font' if m.group(1).endswith('ttf') else 'its licence') + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/(qalam|qalam2|qalam3|skeleton|ref_trace|plate)\.py', lambda m: 'Fig. 13 gift calligraphy: ' + {'qalam': 'a simulated reed pen and a first hand-made sketch of the name (superseded)', 'qalam2': 'reed strokes over a master model, a mirror composition (rejected by Numa)', 'qalam3': 'reed re-inking of a whole word (falls short of the model; kept as a record)', 'skeleton': 'centre lines of a word in a model font', 'ref_trace': 'vector outlines of the ink in the reference plate Numa chose', 'plate': 'the traced word as gold-on-navy and paper plates'}[m.group(1)] + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/reem_ref\.json', 'The outlines of رِيمْ traced from the reference plate Numa chose (ref_trace.py); the source of the name in the gift film.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/render\.cjs', 'Fig. 13 films: renders a film page frame by frame in headless Chromium (needs a local server on port 8766).', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/orbit24\.json', 'The closed 24-petal butterfly orbit, written by orbit.py.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/dive/dive\.json', 'The dive film\'s grid of kicks and the butterfly\'s momenta, written by dive_data.py.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/dive/\.gitignore', 'Keeps dive.bin (regenerated by dive_data.py) out of the repository.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/.+\.html',
     lambda m: ('Fig. %d · %s: the simulation, its data panel, walkthrough and lecture note.' if 'double-inverted' not in m.group(0) else 'Fig. %d · %s: the real-time simulation, its walkthrough and lecture note (no data panel).') % SIMS[m.group(0)][::2]
     if m.group(0) in SIMS else 'Simulation page not registered in catalog.js.',
     lambda m: sim_doc(SIMS[m.group(0)][0], SIMS[m.group(0)][1]) if m.group(0) in SIMS else None),
    # shared scripts and styles
    (r'public/scripts/sim\.js', 'Shared helpers of the simulation pages: KaTeX typesetting of the notes, the walkthrough engine.', 'docs/scripts/sim.md'),
    (r'public/scripts/dataset\.js', 'Sim.dataset(): the one named data store each simulation writes its numbers into.', 'docs/scripts/dataset.md'),
    (r'public/scripts/twoway\.js', 'The solved, two-way fluid of projects 05 and 06 (offered on 06 since 7 November 2026): a tank as deep as the cart (its size set by the page through setCart), 2D Navier–Stokes on a MAC grid, the cart coupled through the pressure, the rods as lines of forces; runs the page\'s 1 ms machine steps inside its 20 ms fluid steps.', 'docs/scripts/twoway.md'),
    (r'public/scripts/curve\.js', 'Parameter curves: a knob that moves by itself along a chosen or drawn curve while the figure runs; writes every number into the page\'s store.', 'docs/scripts/curve.md'),
    (r'public/scripts/datalog\.js', 'The data panel as a bookkeeper: headline, ledger table, books, Read values, Check, Record one round, Save (.npz + CSV).', 'docs/scripts/datalog.md'),
    (r'public/scripts/ledger/([a-z0-9-]+)\.js', lambda m: 'The data panel\'s ledger of %s: headline, sections in causal order, books, checks of the numbers copied from the run.' % m.group(1), 'docs/scripts/datalog.md'),
    (r'public/scripts/fold\.js', 'Fold-out sections on every page: pinned header bands, remembered state, Expand/Collapse all.', 'docs/scripts/fold.md'),
    (r'public/scripts/catalog\.js', 'The registry of simulations (SIMULATIONS, SIM_FIELDS, SIM_TOOLS) that the catalog page draws.', 'docs/scripts/catalog.md'),
    (r'public/scripts/walk/([a-z0-9-]+)\.js',
     lambda m: ('"From symbols to code" for Fig. %d · %s.' % WALKS[m.group(1)]) if m.group(1) in WALKS
     else 'Walkthrough file that no simulation page names in data-walk.', 'docs/scripts/walk.md'),
    (r'public/styles/site\.css', 'Design of the home, catalog and Portfolios pages: tokens, top bar, sections, cards.', 'docs/styles.md'),
    (r'public/styles/sim\.css', 'Design of the simulation pages: stage, controls, readouts, walkthrough; imports paper.css and KaTeX.', 'docs/styles.md'),
    (r'public/styles/paper\.css', 'Lecture notes set like LaTeX: Latin Modern, numbered equations, figures, abstract box.', 'docs/styles.md'),
    (r'public/styles/catalog\.css', 'The catalog entries (paper abstracts) on the simulations page.', 'docs/styles.md'),
    (r'public/styles/data\.css', 'The data panel (headline, ledger table, books) and the Read values strip.', 'docs/styles.md'),
    (r'public/styles/fold\.css', 'The fold-out sections: cards, header bands, toggles, Expand/Collapse all.', 'docs/styles.md'),
    (r'public/styles/portfolio\.css', 'The project cards and figure plates of the Portfolios page.', 'docs/styles.md'),
    # vendor, fonts, images
    (r'public/vendor/katex/katex\.min\.js', 'KaTeX 0.16.11, the maths typesetter.', 'docs/assets.md'),
    (r'public/vendor/katex/katex\.min\.css', 'KaTeX glyph layout and font rules (woff2 only).', 'docs/assets.md'),
    (r'public/vendor/katex/contrib/auto-render\.min\.js', 'KaTeX extension that typesets every \\( \\) and \\[ \\] in a part of the page.', 'docs/assets.md'),
    (r'public/vendor/katex/fonts/KaTeX_.+\.woff2', 'A KaTeX typeface (woff2).', 'docs/assets.md'),
    (r'public/vendor/katex/LICENSE', 'MIT licence of KaTeX.', 'docs/assets.md'),
    (r'public/fonts/lm/lmroman10-.+\.woff2', 'A face of Latin Modern Roman, the typeface of the lecture notes.', 'docs/assets.md'),
    (r'public/fonts/lm/GUST-FONT-LICENSE\.TXT', 'Licence of Latin Modern (GUST Font License 1.0).', 'docs/assets.md'),
    (r'public/fonts/plex\.css', 'IBM Plex Mono, Sans and Serif, served by the site itself: the @font-face rules site.css imports.', 'docs/assets.md'),
    (r'public/fonts/instrument-plex\.css', 'Instrument Serif, IBM Plex Sans and Mono, served by the site itself: the @font-face rules sim.css, catalog.css and the project copies import.', 'docs/assets.md'),
    (r'public/fonts/OFL-IBM-Plex\.txt', 'Licence of IBM Plex (SIL Open Font License 1.1).', 'docs/assets.md'),
    (r'public/fonts/OFL-Instrument-Serif\.txt', 'Licence of Instrument Serif (SIL Open Font License 1.1).', 'docs/assets.md'),
    (r'public/fonts/arabic\.css', 'Amiri and Noto Naskh Arabic, served by the site itself: the @font-face rules of the Arabic pages.', 'docs/assets.md'),
    (r'public/fonts/OFL-Amiri\.txt', 'Licence of Amiri (SIL Open Font License 1.1).', 'docs/assets.md'),
    (r'public/fonts/OFL-Noto-Naskh-Arabic\.txt', 'Licence of Noto Naskh Arabic (SIL Open Font License 1.1).', 'docs/assets.md'),
    (r'public/fonts/amiri/amiri-(400|700)-arabic\.woff2', lambda m: 'Amiri %s, cut to the Arabic blocks.' % m.group(1), 'docs/assets.md'),
    (r'public/fonts/noto-naskh-arabic/noto-naskh-arabic-wght-arabic\.woff2', 'Noto Naskh Arabic, variable weight 400 to 700, cut to the Arabic blocks.', 'docs/assets.md'),
    (r'public/fonts/(ibm-plex-mono|ibm-plex-sans|ibm-plex-serif|instrument-serif)/.+\.woff2',
     lambda m: 'A face of ' + {'ibm-plex-mono': 'IBM Plex Mono', 'ibm-plex-sans': 'IBM Plex Sans', 'ibm-plex-serif': 'IBM Plex Serif',
                               'instrument-serif': 'Instrument Serif'}[m.group(1)] + ' for one script range (name: weight, i for italic, range).', 'docs/assets.md'),
    (r'public/images/fig11/fig-(machine|ends|strut|motor)\.webp',
     lambda m: 'Figure of Double Pendulum under Control, rendered in Blender by tools/fig11/: ' + {'machine': 'the whole machine', 'ends': 'the strut\u2019s two joints', 'strut': 'the strut cut open', 'motor': 'the magnet track and the coil'}[m.group(1)] + '.', 'docs/simulations/fig11-pendulum-control.md'),
    (r'tools/fig11/rig\.py', 'Blender scenes for Double Pendulum under Control: the whole machine, the strut cut open, the motor (bpy 5.2).', 'docs/simulations/fig11-pendulum-control.md'),
    (r'tools/fig11/joints\.py', 'Blender scenes for Double Pendulum under Control: the strut\u2019s two joints, exploded (bpy 5.2).', 'docs/simulations/fig11-pendulum-control.md'),
    (r'public/scripts/stout-cart\.js', 'Fig. 12: the solver: 3D Navier–Stokes for the stout in the glass by APIC on a MAC grid (cut-cell wall, ghost-fluid surface, half glass by symmetry), the road, the one-wheel cart, and their two-way coupling.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/scripts/stout-view\.js', 'Fig. 12: draws the cart, the road and the pint on a canvas from the solver\u2019s state; the head of the stout is drawn, not computed.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/check\.cjs', 'Fig. 12: offline checks of the stout solver (rest, free sloshing frequency, tilt under a steady push); prints measured numbers.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/clip\.html', 'Fig. 12: page that renders the clip of the pint on the cart frame by frame, for clip.cjs.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/clip\.cjs', 'Fig. 12: renders a clip (PNG frames and MP4) of the pint on the cart in headless Chromium.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/test\.cjs', 'Fig. 12: browser test of the page on desktop and phone: the run advances, the push works, no errors, no sideways scroll.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/panel-test\.cjs', 'Fig. 12: every check and read-back of the data panel, run in Chromium; the panel opened.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/panel-test2\.cjs', 'Fig. 12: data panel on a bump at three widths, Read values, one round, Save, the panel idle.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/scripts/stout-pool\.js', 'Fig. 12: shares four loops of the stout solver over worker threads with shared memory; identical numbers.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/scripts/stout-worker\.js', 'Fig. 12: one worker thread of the stout solver: waits for a task, does its share of a loop.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/serve\.cjs', 'Fig. 12: serves public/ with the headers public/_headers gives each path (as Cloudflare does), for the browser tests with threads.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/threads-test\.cjs', 'Fig. 12: in Chromium, the threaded solver must print the single-thread fingerprint to the last digit.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/profile\.cjs', 'Fig. 12: times one fluid step of the stout solver by phase (level set, transfers, pressure, advection).', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/theory\.cjs', 'Fig. 12: the closed-form numbers of the lecture note from the page\u2019s constants: sloshing frequency and equivalent mass, dimensionless groups and damping, quarter car, drive, PI loop, skyhook.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/linearity\.cjs', 'Fig. 12: both fluid models from rest under the same half-sine push, no cart: where the linear modes fail (lean, swing, spill).', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/linfit\.cjs', 'Fig. 12: fits the free swing (amplitude, frequency) in the files linearity.cjs saves.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/study\.cjs', 'Fig. 12: one run of the parameter study through World.advance (bump height, speed loop, suspension): lean, accelerations, spill.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/energy\.cjs', 'Fig. 12: the cart\u2019s energy book over a bump: constant without losses, changed by exactly the work of dampers, drag and motor.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/figures\.cjs', 'Fig. 12: writes the two inline SVG figures of the lecture note (the glass section; one bump, open loop against speed control).', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/control\.cjs', 'Fig. 12: the controllers against either fluid model through the wall probes and the Kalman filter (bump or push, controller switched on while swinging); fits the decay.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/observer\.cjs', 'Fig. 12: the numbers of the note\u2019s Kalman-filter section: plant, LQR gains and poles, discrete matrices, settled gain, probe noise at rest.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/ident\.cjs', 'Fig. 12: fits one oscillator (frequency, damping, coupling) to the 3D solver\u2019s runs from rest.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/calm-shots\.cjs', 'Fig. 12: screenshots of the 3D stout swinging, then calmed by the slosh feedback switched on, at 1280 and 390 px.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/nm_coeffs\.py', 'Fig. 12: derives the Narimanov\u2013Moiseev five-mode sloshing coefficients of a cylinder from the multimodal integrals (Faltinsen, Lukovsky & Timokha 2016) and checks them against their Table 1.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/note-shots\.cjs', 'Fig. 12: opens the lecture note at 1280 and 390 px: KaTeX errors, sideways scroll, over-wide equations, screenshots of \u00a78.5.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/scripts/stout-nm\.js', 'Fig. 12: the coefficients of the nonlinear (Narimanov\u2013Moiseev) live model, written by tools/fig12/nm_coeffs.py; do not edit.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/swirl\.cjs', 'Fig. 12: shakes the nonlinear live model along the road at frequencies near resonance and prints whether it swirls.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/swirl-shots\.cjs', 'Fig. 12: screenshots of the nonlinear live model swirling, at 1280 and 390 px.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/roads\.cjs', 'Fig. 12: the cart on the rough roads (ISO 8608 classes, washboard, setts): vertical shaking at twice the swing frequency, lean, spill, wheel off the road, grip limit.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/scripts/stout-gpu\.js', 'Fig. 12: the 3D stout solver on the graphics chip (WebGPU compute shaders): the whole glass, APIC on a MAC grid, level set, Jacobi-preconditioned CG; batches of steps with one read-back.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/scripts/stout-gpu-view\.js', 'Fig. 12: draws the GPU solver\u2019s stout on the graphics chip (screen-space fluid rendering: sphere depth, bilateral smoothing, thickness for Beer\u2013Lambert, the head as the top 12 mm).', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/gpu-linearity\.cjs', 'Fig. 12: the GPU solver from rest in headless Chromium (pushes, steady tilt, rest), the experiment of linearity.cjs; saves series for linfit.cjs.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/gpu-study\.cjs', 'Fig. 12: the cart over a bump or a rough road with the GPU solver (World.advanceGpu) in headless Chromium, in batches; lean, accelerations, spill, controllers.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/coffee\.cjs', 'Fig. 12: a mug of coffee beside the pint (note \u00a714): f11, wall and foam damping, the push to the rim, and both carried by a walking hand through the nonlinear live model.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/springs\.cjs', 'Fig. 12: what each controller does to the suspension spring (stroke, active force, heave, lean, spill) on bumps and rough roads; the joint motor and suspension design.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/gpu-page-test\.cjs', 'Fig. 12: the page on the GPU solver in headless Chromium with WebGPU: starts, runs, no errors, screenshots at 1280 and 390 px.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/road-shots\.cjs', 'Fig. 12: screenshots of the live model on a rough road with and without the slosh feedback, and what spilled.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/ctrl-shots\.cjs', 'Fig. 12: screenshots of the live model over a 25 mm bump with each controller, and the largest lean the page read.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/same\.cjs', 'Fig. 12: fingerprint (SHA-256) of the solver state after 1 s with a push; a speed-up must leave it unchanged.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/scripts/guinness-glass\.js', 'Fig. 12: inner radius of the Guinness tulip pint every 0.5 mm, written by tools/fig12/glass_profile.py; do not edit.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/glass_profile\.py', 'Fig. 12: measures the inner outline of the tulip from dimensions.com\u2019s dimensioned section and scales it to 160 x 85 mm; writes glass_profile.json and guinness-glass.js.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/glass_profile\.json', 'Fig. 12: the measured inner radius every 0.5 mm with its scaling, written by glass_profile.py.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/irish-imperial-pint\.svg', 'Fig. 12: dimensions.com\u2019s dimensioned elevation and section of the tulip pint glass (source of the profile).', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/spill-test\.cjs', 'Fig. 12: drives a hard bump in open loop until the stout spills, then runs every data-panel check.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12-restart/BRIEF\.md', 'Fig. 12: the hand-over brief of 6 November 2026 from the session whose Fig. 12 was rejected; history only.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig11/figs\.py', 'Composes the Blender renders of tools/fig11/ into the four figures with numbered balloons (Pillow).', 'docs/simulations/fig11-pendulum-control.md'),
    (r'public/images/sims/([a-z0-9-]+)\.webp',
     lambda m: ('Thumbnail of Fig. %d · %s, 800 × 500 px.' % BY_ID[m.group(1)]) if m.group(1) in BY_ID
     else 'Thumbnail with no simulation of that id.', 'docs/assets.md'),
    # the Droplet Collection study: working notes in notes/droplets/, source in portfolios-src/droplets/ (README.md)
    (r'notes/droplets/status\.md', 'Status of the Droplet Collection study: Fermi estimate, queue, done list with evidence, decisions for Numa. Read first.', None),
    (r'notes/droplets/done\.md', 'Definition of done of the Droplet Collection study, as a checklist; only Numa may change it.', None),
    (r'notes/droplets/contract-L(\d+)\.md', lambda m: 'Gate 1 contract of model level L' + m.group(1) + ': question, picture, model, assumptions with their numbers, predictions, answers to the skeptic.', 'notes/droplets/status.md'),
    (r'notes/droplets/check-L(\d+)\.md', lambda m: 'Gate 2 check of level L' + m.group(1) + ': each equation re-derived by two routes.', 'notes/droplets/status.md'),
    (r'notes/droplets/dossier-([a-z-]+)\.md', lambda m: 'Scout dossier on ' + m.group(1) + ': primary sources read for the study.', 'notes/droplets/status.md'),
    (r'notes/droplets/skeptic-(G\d)-(L[0-9L]+)-r(\d)\.md', lambda m: 'Blind skeptic report, gate ' + m.group(1)[1:] + ', level ' + m.group(2) + ', round ' + m.group(3) + '.', 'notes/droplets/status.md'),
    (r'notes/droplets/skeptic-(G\d)-(.+)\.md', lambda m: 'Blind skeptic report, gate ' + m.group(1)[1:] + ': ' + m.group(2) + '.', 'notes/droplets/status.md'),
    (r'notes/droplets/review-answers-r(\d)\.md', lambda m: 'Answers to the independent reviews of Part IV, round ' + m.group(1) + '.', 'notes/droplets/status.md'),
    (r'notes/droplets/review-([a-z]+)-(.+)\.md', lambda m: 'Independent review (' + m.group(1) + ') of ' + m.group(2) + '.', 'notes/droplets/status.md'),
    (r'notes/droplets/gate3-answers-r(\d)\.md', lambda m: 'Answers to the Gate 3 skeptic, round ' + m.group(1) + '.', 'notes/droplets/status.md'),
    (r'notes/droplets/gate2/(.+)', lambda m: 'Gate 2 checker script or output: ' + m.group(1) + '.', 'notes/droplets/status.md'),
    (r'portfolios-src/droplets/README\.md', "The study's source: every folder, how the served page is built, the three checks.", 'portfolios-src/droplets/README.md'),
    (r'portfolios-src/droplets/\.gitignore', 'Keeps the stand-alone build (out/) out of git.', 'portfolios-src/droplets/README.md'),
    (r'portfolios-src/droplets/physics\.cjs', 'The model, L0 to L10: fall speeds, trajectories, kernel, collection equation, exact stochastic process, turbulence, energy ledger, maximum entropy, a cloud with a shape (super-droplets with a stochastic element); runs in the page and in Node.', 'portfolios-src/droplets/README.md'),
    (r'portfolios-src/droplets/chart\.cjs', 'House-style SVG line charts for the figures and the page.', 'portfolios-src/droplets/README.md'),
    (r'portfolios-src/droplets/app\.js', "The page's script: tabs, hash routes, the five simulation panels, and the store (dataset) that panels 3 and 4 write.", 'portfolios-src/droplets/README.md'),
    (r'portfolios-src/droplets/datahooks\.js', "The data panel's hooks for panels 4 and 3 (Sim.data: Read values, Check, read-back, the books, one round = five cloud-minutes).", 'portfolios-src/droplets/README.md'),
    (r'portfolios-src/droplets/template\.html', 'The page template: house design, tabs, placeholders filled by the build.', 'portfolios-src/droplets/README.md'),
    (r'portfolios-src/droplets/text/book-(\d\d)\.src\.html', lambda m: 'Symbols and sources (appendix A).' if m.group(1) == '99' else 'Lecture notes, chapter ' + str(int(m.group(1))) + '.', 'portfolios-src/droplets/README.md'),
    (r'portfolios-src/droplets/text/([a-z]+)\.src\.html', lambda m: 'Words of the ' + m.group(1) + ' tab.', 'portfolios-src/droplets/README.md'),
    (r'portfolios-src/droplets/data/(.+)', lambda m: 'Data written by the model\'s run tools: ' + m.group(1) + '.', 'portfolios-src/droplets/README.md'),
    (r'portfolios-src/droplets/derive/(.+)', lambda m: 'Derivation or number script behind a Gate 1 contract: ' + m.group(1) + '.', 'notes/droplets/status.md'),
    (r'portfolios-src/droplets/checks/(.+)', lambda m: 'Check: ' + m.group(1) + ' (see the README).', 'portfolios-src/droplets/README.md'),
    (r'portfolios-src/droplets/tools/(.+)', lambda m: 'Build or run tool: ' + m.group(1) + ' (see the README).', 'portfolios-src/droplets/README.md'),
    (r'public/portfolios/droplet-collection/fig/plate-([a-z]+)\.svg', lambda m: 'Plate of the Portfolios page article (' + m.group(1) + '), written by the Droplet Collection build.', 'docs/portfolios.md'),
    # the source of Iron, Cotton and the Head (not served): portfolios-src/impact/, explained in its README.md
    (r'portfolios-src/impact/README\.md', "The study's source: every file, how the two pages are generated, the checks.", 'portfolios-src/impact/README.md'),
    (r'portfolios-src/impact/\.gitignore', 'Keeps the stand-alone build (out/) and screenshots out of git.', 'portfolios-src/impact/README.md'),
    (r'portfolios-src/impact/physics\.c?js', 'The model: Morse-bonded iron, fibre-network cotton, the head and scale, energy books (.cjs: the same file for the Node checks).', 'portfolios-src/impact/README.md'),
    (r'portfolios-src/impact/template\.html', 'The page template: layout, the store filled by record(), drawing, playback, gauges, plots.', 'portfolios-src/impact/README.md'),
    (r'portfolios-src/impact/datahooks\.js', "The data panel's hooks for the study (Sim.data: Read values, Check, read-back, one round = one drop).", 'docs/portfolios.md'),
    (r'portfolios-src/impact/text_(en|de|ar)\.py', lambda m: 'Every word of the %s page.' % {'en': 'English', 'de': 'German', 'ar': 'Arabic'}[m.group(1)], 'portfolios-src/impact/README.md'),
    (r'portfolios-src/impact/build\.py', 'Generates public/portfolios/impact/index.html, de.html and ar.html (--site), or stand-alone pages in out/.', 'portfolios-src/impact/README.md'),
    (r'portfolios-src/impact/checks/([a-z_0-9]+)\.cjs', lambda m: 'Check script %s (see the README).' % m.group(1), 'portfolios-src/impact/README.md'),
    # Rotor Pendula: the served page's source (portfolios-src/rotor-pendula/, README.md) and its model record (notes/rotor-pendula/)
    (r'public/portfolios/rotor-pendula/index\.html', 'Generated page: the lecture notes, the simulation and the wind in three tabs (portfolios-src/rotor-pendula/tools/build_combined.py).', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/sol\.html', "Entry page of Sol's app copy (formerly index.html), copied unchanged by build_combined.py.", 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/LICENSE-fonts\.txt', 'Licences of the fonts the generated page uses.', 'docs/portfolios.md'),
    (r'portfolios-src/rotor-pendula/README\.md', "The study's source: what it is, how the served page is generated, the checks.", 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/rotor_notes\.html', 'A Second Blade on a Turning Blade, the lecture notes (chapters 1-9, the double pendulum held by the wind); generated by tools/build_theory.py.', 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/rotor_sim\.html', 'The simulation page: physics block, solve-then-playback, Read values, worked solutions.', 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/rotor_wind\.html', 'The wind page: a turbulent field synthesised in the browser (IEC Kaimal, Veers), the rotor and the second blade in it, data panel.', 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/numbers\.json', 'Every computed number and table of the notes, written by tools/make_numbers.py.', 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/check_physics\.py', 'Independent checks: SymPy derivations and SciPy re-integration with retyped constants.', 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/sol/index\.html', "Source copy of the entry page of Sol's app, served as sol.html.", 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/theory/(\d\d)_([a-z]+)\.src\.html', lambda m: 'Source of the notes, part %s (%s): HTML with LaTeX maths and number placeholders.' % (m.group(1), m.group(2)), 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/data/.+', 'Model output copied from notes/rotor-pendula/derive/, read by the number script or the simulation build.', 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/fonts/.+', 'Font subsets and their @font-face rules, embedded by the build scripts.', 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/tools/(build_[a-z]+)\.py', lambda m: 'Build script: %s (see README.md).' % m.group(1), 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/tools/(check_[a-z_]+)\.(py|js)', lambda m: 'Check script: %s (see README.md).' % m.group(1), 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/tools/make_numbers\.py', 'Computes every number and table of the notes from data/.', 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/tools/typed_numbers\.py', 'The numbers typed by hand in the notes, each with its reason, for check_numbers.py.', 'portfolios-src/rotor-pendula/README.md'),
    (r'portfolios-src/rotor-pendula/tools/.+', 'Build helper of the study (KaTeX, physics block, worked solutions, template).', 'portfolios-src/rotor-pendula/README.md'),
    (r'notes/droplets/baseline/.+', "Text of the Droplet Collection app pages before its study, kept for comparison.", 'docs/portfolios.md'),
    (r'notes/droplets/brief\.md', 'The brief of the Droplet Collection study.', 'docs/portfolios.md'),
    (r'notes/rotor-pendula/derive/.+', 'Rotor Pendula model or model run (L0-L6): script, its output or its log; see the script header.', 'docs/portfolios.md'),
    (r'notes/rotor-pendula/baseline/.+', "Text of Sol's app pages before this study, kept for comparison.", 'docs/portfolios.md'),
    (r'notes/rotor-pendula/teaching/export_notes\.py', 'Exports the Rotor Pendula lecture notes as plain text, numbers filled in, for a blind reader.', 'docs/portfolios.md'),
    (r'notes/rotor-pendula/.+\.md', 'Rotor Pendula study record: brief, status, contracts, skeptic and referee reports, dossiers.', 'docs/portfolios.md'),
    # the Hydraulic Press Study's source (not served): portfolios-src/hydraulics/, explained in its README.md
    (r'portfolios-src/hydraulics/README\.md', "The study's source: what it is, how the served page is generated, the four checks.", 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/\.gitignore', 'Keeps the files the checks and the standalone build write out of git.', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/package\.json', "Declares the study's Node scripts CommonJS (the site root declares ES modules).", 'docs/portfolios.md'),
    (r'portfolios-src/hydraulics/hydraulic_control\.html', 'The servo press: animation, controller, gauges, time traces, loop analysis, worked solutions. Edited directly.', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/hydraulic\.html', "Pascal's ideal press, animated from its Lagrangian. Edited directly.", 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/hydraulic_theory\.html', 'Hydraulics from First Principles, the 23-chapter text; generated by tools/build_theory.py.', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/theory/(\d\d)_([a-z]+)\.src\.html', lambda m: 'Source of the text, part %s (%s): HTML with LaTeX maths.' % (m.group(1), m.group(2)), 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/check_physics\.py', "Checks the ideal press's physics against an independent Python model.", 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/check_control\.py', "Checks the servo press's physics and loop analysis against an independent SciPy/SymPy model.", 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/dump_(runs|control)\.js', lambda m: "Runs the %s page's physics block in Node for its check script." % ('ideal press' if m.group(1) == 'runs' else 'servo press'), 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/tools/check_data_panel\.cjs', 'Checks the data panel inside the ideal and servo frames in a real browser.', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/tools/build_combined\.py', 'Generates public/portfolios/hydraulics/index.html from the three pages (--site).', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/tools/build_theory\.py', 'Builds hydraulic_theory.html from theory/*.src.html, typesetting every formula with KaTeX.', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/tools/build_fonts\.py', 'Downloads the font subsets in fonts/ and writes their @font-face rules.', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/tools/render_page_math\.py', 'Typesets the equation blocks inside the two simulation pages.', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/tools/page_equations\.py', 'The TeX of the equation blocks on the two simulation pages.', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/tools/katex_render\.js', 'Typesets one batch of formulas with KaTeX for the build scripts.', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/tools/check_combined\.py', 'Browser check of the served page: 33 checks of completeness, working controls, links, layout.', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/tools/check_theory_numbers\.js', "Recomputes the 52 numbers the text quotes from the page's models.", 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/tools/theory_template\.html', 'The page the text is set into.', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/tools/package(-lock)?\.json', lambda m: 'Pins KaTeX 0.16.11 for the build scripts' + (' (lockfile).' if m.group(1) else '.'), 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/fonts/LICENSE-fonts\.txt', 'Licences of the embedded fonts (OFL 1.1; MIT for KaTeX).', 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/fonts/fonts-(embedded|linked)\.css', lambda m: 'The @font-face rules of the study, fonts ' + ('as data: addresses.' if m.group(1) == 'embedded' else 'linked as files.'), 'portfolios-src/hydraulics/README.md'),
    (r'portfolios-src/hydraulics/fonts/[a-z0-9-]+\.woff2', 'A subset of IBM Plex Sans, IBM Plex Mono or Instrument Serif embedded in the study.', 'portfolios-src/hydraulics/README.md'),
    # the Hydraulic Press Study: one generated page, not an app build
    (r'public/portfolios/hydraulics/index\.html', 'The whole Hydraulic Press Study: tab bar and three embedded pages, generated from portfolios-src/hydraulics/.', 'docs/portfolios.md'),
    (r'public/portfolios/hydraulics/(de|ar)\.html', lambda m: 'The Hydraulic Press Study in ' + {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ', generated by tools/i18n/hydraulics.py from the English source and i18n/' + m.group(1) + '/hydraulics*.json.', 'docs/i18n.md'),
    (r'public/portfolios/hydraulics/LICENSE-fonts\.txt', 'Licences of the fonts the study uses (OFL 1.1; MIT for KaTeX).', 'docs/portfolios.md'),
    (r'public/portfolios/hydraulics/fig/0([1-4])_[a-z]+\.webp',
     lambda m: 'Plate %s of the study on the Portfolios page, 600 px high.' % m.group(1), 'docs/portfolios.md'),
    # Iron, Cotton and the Head: two generated pages, English and Arabic
    (r'public/portfolios/impact/index\.html', 'Iron, Cotton and the Head in English, generated from portfolios-src/impact/ by build.py --site.', 'docs/portfolios.md'),
    (r'public/portfolios/impact/ar\.html', 'Iron, Cotton and the Head in Arabic, generated from portfolios-src/impact/ by build.py --site.', 'docs/portfolios.md'),
    (r'public/portfolios/impact/de\.html', 'Iron, Cotton and the Head in German, generated from portfolios-src/impact/ by build.py --site.', 'docs/portfolios.md'),
    (r'public/portfolios/impact/fig/0([1-4])_[a-z]+\.webp',
     lambda m: 'Plate %s of the study on the Portfolios page, a screenshot of its English page, 600 px high.' % m.group(1), 'docs/portfolios.md'),
    # the two app copies
    (r'public/portfolios/[a-z-]+/index\.html', 'Entry page of the project copy: module script and stylesheet loader.', 'docs/portfolios.md'),
    (r'public/portfolios/[a-z-]+/static/index-[^/]+\.js', 'The whole project application, built and minified.', 'docs/portfolios.md'),
    (r'public/portfolios/[a-z-]+/static/index-[^/]+\.css', "The project's stylesheet, built.", 'docs/portfolios.md'),
    (r'public/portfolios/[a-z-]+/static/worker-[^/]+\.js', "The project's Web Worker: its solver, off the main thread.", 'docs/portfolios.md'),
    (r'public/portfolios/[a-z-]+/static/KaTeX_[^/]+', 'A KaTeX font inside the project build.', 'docs/portfolios.md'),
    (r'public/portfolios/[a-z-]+/fig/[^/]+\.svg', 'A vector figure of the project.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/report\.pdf', "Sol's 14-page corrected report.", 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/report\.tex', 'LaTeX source of the report.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/wind_pendulum\.zip', 'The complete delivery: code, data, figures, fonts, sources.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/README\.md', 'Where to start reading the study.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/STATUS\.md', 'What the study computed, derived, did not measure, and assumes.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/CHANGES\.md', 'The corrections C1–C14, old → new.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/FILE_INVENTORY\.csv', 'Every file of the full delivery with its size.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/code/README\.md', 'How to regenerate the study, command by command.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/code/requirements\.txt', 'The pinned Python packages.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/data/summary\.csv', 'One row per computed case.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/data/all_results\.json', 'All 160 cases with full parameters.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/data/audit\.json', 'Audit numbers: RK4 cross-checks, energy identity, sensor budget.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/sources/README\.md', 'The two datasheets behind the sensor budget, with checksums.', 'docs/portfolios.md'),
    (r'public/portfolios/rotor-pendula/study/sources/access\.json', 'The same two sources as data.', 'docs/portfolios.md'),
]

# Folder sections in reading order; a file goes to the first whose prefix it starts with. A file in no section is an error, as
# a file without a description is (public/cv/ had none and was silently left out of docs/files.md until 31 October 2026).
SECTIONS = [
    ('', 'Repository root', lambda p: '/' not in p),
    ('public/', 'Pages under public/', lambda p: p.startswith('public/') and p.count('/') == 1),
    ('public/de/', 'German pages (generated)', None), ('public/ar/', 'Arabic pages (generated)', None),
    ('public/simulations/', 'Simulation pages', None),
    ('public/scripts/walk/', 'Walkthroughs', None), ('public/scripts/ledger/', 'Ledgers of the data panel', None), ('public/scripts/', 'Shared scripts', None),
    ('public/styles/', 'Stylesheets', None),
    ('public/vendor/katex/', 'KaTeX', None), ('public/fonts/lm/', 'Latin Modern', None),
    ('public/fonts/', 'IBM Plex, Instrument Serif, and the Arabic faces', None),
    ('public/images/sims/', 'Thumbnails', None),
    ('public/images/fig11/', 'Figures of Double Pendulum under Control', None),
    ('public/images/', 'Logo', None),
    ('public/cv/', 'The CV page', None),
    ('public/portfolios/droplet-collection/', 'Project copy: Droplet Collection', None),
    ('public/portfolios/rotor-pendula/', 'Project copy: Rotor Pendula', None),
    ('public/portfolios/hydraulics/', 'Project copy: Hydraulic Press Study', None),
    ('public/portfolios/impact/', 'Iron, Cotton and the Head', None),
    ('public/portfolios/pendulum-control/', 'Project: Double Pendulum under Control', None),
    ('portfolios-src/hydraulics/', 'Source of the Hydraulic Press Study (not served)', None),
    ('portfolios-src/rotor-pendula/', 'Source of Rotor Pendula (not served)', None),
    ('portfolios-src/impact/', 'Source of Iron, Cotton and the Head (not served)', None),
    ('portfolios-src/rotor-pendula/', 'Source of the Rotor Pendula notes (not served)', None),
    ('portfolios-src/droplets/', 'Source of the Droplet Collection study (not served)', None),
    ('portfolios-src/', 'Shared by the portfolio sources (not served)', lambda p: p.startswith('portfolios-src/') and p.count('/') == 1),
    ('src/', 'Template sources', None),
    ('docs/', 'Documentation', None), ('tools/', 'Tools', None),
    ('i18n/', 'Translation tables', None),
    ('.claude/agents/', 'Agents of the lecture-note review', None),
    ('notes/rotor-pendula/', 'Working notes of the Rotor Pendula study', None), ('notes/droplets/', 'Working notes of the Droplet Collection study', None),
    ('notes/', 'Record of the lecture-note review', None),
]
FOLD_OVER = 12  # a run of more than this many files with the same description is folded into <details>


def describe(path):
    for pattern, text, doc in RULES:
        m = re.fullmatch(pattern, path)
        if m:
            text = text(m) if callable(text) else text
            doc = doc(m) if callable(doc) else doc
            return text, doc or path
    return None


def size(path):
    n = os.path.getsize(os.path.join(ROOT, path))
    return '%d B' % n if n < 1000 else '%.1f kB' % (n / 1e3) if n < 1e6 else '%.2f MB' % (n / 1e6)


def link(target, label=None):
    """A Markdown link from docs/files.md to a repository path."""
    return '[%s](%s)' % (label or target, os.path.relpath(target, 'docs').replace(' ', '%20'))


def render(paths):
    groups, missing = {}, []
    for p in paths:
        d = describe(p)
        if d is None:
            missing.append(p)
            continue
        for prefix, title, test in SECTIONS:
            if (test(p) if test else p.startswith(prefix)):
                groups.setdefault(title, []).append((p, d))
                break
        else:
            missing.append(p + ' (in no section of SECTIONS)')
    total = sum(os.path.getsize(os.path.join(ROOT, p)) for p in paths)
    out = ['# Every file', '',
           'Written by [`tools/inventory.py`](../tools/inventory.py) from the files in the repository; do not edit by hand.',
           'Run `python3 tools/inventory.py` after adding, removing or changing files, and `python3 tools/inventory.py --check`',
           'to confirm that every file is described. Sizes are those of the files when the list was written.', '',
           '%d files, %.1f MB in all. Runs of more than %d similar files are folded; open them to see each file.'
           % (len(paths), total / 1e6, FOLD_OVER), '']
    out += ['| Folder | Files |', '|---|---|']
    for _, title, _ in SECTIONS:
        if title in groups:
            out.append('| [%s](#%s) | %d |' % (title, re.sub(r'[^a-z0-9 -]', '', title.lower()).replace(' ', '-'),
                                               len(groups[title])))
    for _, title, _ in SECTIONS:
        if title not in groups:
            continue
        out += ['', '## ' + title]
        rows, table = groups[title], []
        head = ['', '| File | Size | What it is | Explained in |', '|---|---|---|---|']

        def row(p, text, doc):
            sz = 'this file' if p == OUT else size(p)
            return '| %s | %s | %s | %s |' % (link(p, '`%s`' % p), sz, text.replace('|', '\\|'),
                                             link(doc, os.path.basename(doc)))
        i = 0
        while i < len(rows):
            j = i
            while j < len(rows) and rows[j][1] == rows[i][1]:
                j += 1
            if j - i > FOLD_OVER:  # a long run of alike files: close the open table, fold the run
                if table:
                    out += head + table
                    table = []
                out += ['', '<details><summary>%d files: %s</summary>' % (j - i, rows[i][1][0])] + head
                out += [row(p, *d) for p, d in rows[i:j]] + ['', '</details>']
            else:
                table += [row(p, *d) for p, d in rows[i:j]]
            i = j
        if table:
            out += head + table
    return '\n'.join(out).rstrip() + '\n', missing


def main():
    check = '--check' in sys.argv[1:]
    text, missing = render(files())
    for p in missing:
        print('no description for: ' + p, file=sys.stderr)
    if check:
        try:
            same = read(OUT) == text
        except FileNotFoundError:
            same = False
        if not same:
            print(OUT + ' is out of date: run python3 tools/inventory.py', file=sys.stderr)
        sys.exit(1 if missing or not same else 0)
    if missing:
        sys.exit(1)
    with open(os.path.join(ROOT, OUT), 'w', encoding='utf-8') as f:
        f.write(text)
    print('wrote %s: %d files' % (OUT, text.count('\n| [`')))


if __name__ == '__main__':
    main()

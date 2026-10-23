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
    (r'tools/inventory\.py', 'Writes docs/files.md and checks that every file in the repository is described.', 'docs/files.md'),
    # working notes of the Rotor Pendula and Droplet Collection studies (another session's work; start with status.md and brief.md)
    (r'notes/(droplets|rotor-pendula)/brief\.md', lambda m: 'The brief of the ' + {'droplets': 'Droplet Collection', 'rotor-pendula': 'Rotor Pendula'}[m.group(1)] + ' study: question, method and gates, for an agent working in a loop.', None),
    (r'notes/rotor-pendula/status\.md', 'Status of the Rotor Pendula study: queue, done list with evidence, decisions for Numa. Read first.', None),
    (r'notes/rotor-pendula/done\.md', 'Definition of done of the Rotor Pendula study, as a checklist; only Numa may change it.', None),
    (r'notes/rotor-pendula/handoff-prompt\.md', 'Prompt for handing the Rotor Pendula study to another agent.', 'notes/rotor-pendula/status.md'),
    (r'notes/rotor-pendula/review-prompt\.md', 'Prompt for an independent reviewer of the Rotor Pendula study.', 'notes/rotor-pendula/status.md'),
    (r'notes/rotor-pendula/contract-L(\d)\.md', lambda m: 'Gate 1 contract of model level L' + m.group(1) + ': question, model, assumptions with their numbers, checks.', 'notes/rotor-pendula/status.md'),
    (r'notes/rotor-pendula/dossier-([a-z-]+)\.md', lambda m: 'Scout dossier on ' + m.group(1) + ': primary sources read for the study.', 'notes/rotor-pendula/status.md'),
    (r'notes/rotor-pendula/skeptic-(G\d)-(L\d)-r(\d)\.md', lambda m: 'Blind skeptic report, gate ' + m.group(1)[1:] + ', level ' + m.group(2) + ', round ' + m.group(3) + '.', 'notes/rotor-pendula/status.md'),
    (r'notes/(droplets|rotor-pendula)/baseline/([a-z]+)\.html', lambda m: 'Text of the ' + m.group(2) + ' page of the published ' + {'droplets': 'Droplet Collection', 'rotor-pendula': 'Rotor Pendula'}[m.group(1)] + ' app, kept as the baseline the study starts from.', lambda m: {'droplets': 'notes/droplets/brief.md', 'rotor-pendula': 'notes/rotor-pendula/status.md'}[m.group(1)]),
    (r'notes/rotor-pendula/derive/([A-Za-z0-9_]+)\.py', lambda m: 'Derivation or computation script of the study, ' + m.group(1) + '.py: prints PASS/FAIL and exits 1 on a failure.', 'notes/rotor-pendula/status.md'),
    (r'notes/rotor-pendula/derive/([A-Za-z0-9_]+)\.(json|log)', lambda m: 'Saved output of ' + m.group(1) + '.py' + (' (numbers)' if m.group(2) == 'json' else ' (log)') + '.', 'notes/rotor-pendula/status.md'),
    (r'notes/rotor-pendula/derive/data/(.+)', lambda m: 'Cited data of the NREL 5-MW reference turbine: ' + m.group(1) + '.', 'notes/rotor-pendula/status.md'),
    (r'portfolios-src/rotor-pendula/fonts/(.+\.woff2)', lambda m: 'Self-hosted font for the Rotor Pendula notes build: ' + m.group(1) + '.', None),
    (r'portfolios-src/rotor-pendula/fonts/(.+)', lambda m: 'Fonts of the Rotor Pendula notes build: ' + m.group(1) + '.', None),
    (r'portfolios-src/rotor-pendula/tools/(.+)', lambda m: 'Build and check tool of the Rotor Pendula notes, adapted from the Hydraulic Press Study\'s tools: ' + m.group(1) + '.', None),
    # the site in German and Arabic (docs/i18n.md): English pages are the source, everything below is made from them
    (r'tools/i18n/build\.py', 'Writes the German and Arabic pages, the script strings and the mirrored stylesheets from the English pages and the tables; --check fails on anything untranslated.', 'docs/i18n.md'),
    (r'tools/i18n/ingest\.py', 'Stores checked translations made outside the tables (page pieces, script strings, walkthrough prose).', 'docs/i18n.md'),
    (r'i18n/(de|ar)/walk\.json', lambda m: {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ' prose of the ten walkthroughs, keyed by the English.', 'docs/i18n.md'),
    (r'public/scripts/walk/(de|ar)/([a-z]+)\.js', lambda m: {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ' walkthrough ' + m.group(2) + ', generated from the English one; do not edit.', 'docs/i18n.md'),
    (r'tools/i18n/fill\.py', 'Stores translations into a page table, recording the English each one was made from.', 'docs/i18n.md'),
    (r'i18n/(de|ar)/strings\.json', lambda m: {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ' words of the scripts and of the catalog, with plural forms.', 'docs/i18n.md'),
    (r'i18n/(de|ar)/(.+)\.json', lambda m: {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ' table of ' + m.group(2) + ': per piece, the English it was translated from and the translation.', 'docs/i18n.md'),
    (r'public/(de|ar)/(.+\.html)', lambda m: {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ' ' + m.group(2) + ', generated by tools/i18n/build.py; do not edit.', 'docs/i18n.md'),
    (r'public/scripts/i18n/strings-(de|ar)\.js', lambda m: 'The ' + {'de': 'German', 'ar': 'Arabic'}[m.group(1)] + ' string table the scripts read through T(), generated; do not edit.', 'docs/i18n.md'),
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
    (r'notes/fig(\d\d)/.+', lambda m: 'Fig. %d: a measuring script of the review, or its saved output.' % int(m.group(1)), 'docs/notes.md'),
    (r'tools/make_portfolio_copy\.py', 'Builds a browser-only website copy of a research app from its source, without changing the app or installing dependencies.', 'docs/portfolios.md'),
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
    (r'public/_headers', 'Security response headers Cloudflare sets on every file of phyeinusul.com; read by Cloudflare, never served.', 'docs/usul.md'),
    (r'public/images/phyein-usul-mark\.svg', 'The Phyein Usul logo: above the name on the home page, linking home in the top bar of the other pages.', 'docs/assets.md'),
    (r'tests/tests\.json', "Plain-language test scenarios run by the platform's QA after each deploy.", 'docs/build-and-deploy.md'),
    # pages
    (r'public/simulations\.html', 'The simulations catalog: one titled fold card per simulation, search and chips.', 'docs/pages.md'),
    (r'public/portfolios\.html', 'The Portfolios page: the two research projects.', 'docs/pages.md'),
    (r'public/robots\.txt', 'Instructions for search-engine crawlers.', 'docs/pages.md'),
    (r'public/simulations/.+\.html',
     lambda m: 'Fig. %d · %s: the simulation, its data panel, walkthrough and lecture note.' % SIMS[m.group(0)][::2]
     if m.group(0) in SIMS else 'Simulation page not registered in catalog.js.',
     lambda m: sim_doc(SIMS[m.group(0)][0], SIMS[m.group(0)][1]) if m.group(0) in SIMS else None),
    # shared scripts and styles
    (r'public/scripts/sim\.js', 'Shared helpers of the simulation pages: KaTeX typesetting of the notes, the walkthrough engine.', 'docs/scripts/sim.md'),
    (r'public/scripts/dataset\.js', 'Sim.dataset(): the one named data store each simulation writes its numbers into.', 'docs/scripts/dataset.md'),
    (r'public/scripts/datalog\.js', 'The data panel: variables, Read values, Check, Record one round, Save (.npz + CSV).', 'docs/scripts/datalog.md'),
    (r'public/scripts/fold\.js', 'Fold-out sections on every page: pinned header bands, remembered state, Expand/Collapse all.', 'docs/scripts/fold.md'),
    (r'public/scripts/catalog\.js', 'The registry of simulations (SIMULATIONS, SIM_FIELDS, SIM_TOOLS) that the catalog page draws.', 'docs/scripts/catalog.md'),
    (r'public/scripts/walk/([a-z0-9-]+)\.js',
     lambda m: ('"From symbols to code" for Fig. %d · %s.' % WALKS[m.group(1)]) if m.group(1) in WALKS
     else 'Walkthrough file that no simulation page names in data-walk.', 'docs/scripts/walk.md'),
    (r'public/styles/site\.css', 'Design of the home, catalog and Portfolios pages: tokens, top bar, sections, cards.', 'docs/styles.md'),
    (r'public/styles/sim\.css', 'Design of the simulation pages: stage, controls, readouts, walkthrough; imports paper.css and KaTeX.', 'docs/styles.md'),
    (r'public/styles/paper\.css', 'Lecture notes set like LaTeX: Latin Modern, numbered equations, figures, abstract box.', 'docs/styles.md'),
    (r'public/styles/catalog\.css', 'The catalog entries (paper abstracts) on the simulations page.', 'docs/styles.md'),
    (r'public/styles/data\.css', 'The data panel and the Read values strip.', 'docs/styles.md'),
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
    (r'public/images/sims/([a-z0-9-]+)\.webp',
     lambda m: ('Thumbnail of Fig. %d · %s, 800 × 500 px.' % BY_ID[m.group(1)]) if m.group(1) in BY_ID
     else 'Thumbnail with no simulation of that id.', 'docs/assets.md'),
    # the source of Iron, Cotton and the Head (not served): portfolios-src/impact/, explained in its README.md
    (r'portfolios-src/impact/README\.md', "The study's source: every file, how the two pages are generated, the checks.", 'portfolios-src/impact/README.md'),
    (r'portfolios-src/impact/\.gitignore', 'Keeps the stand-alone build (out/) and screenshots out of git.', 'portfolios-src/impact/README.md'),
    (r'portfolios-src/impact/physics\.c?js', 'The model: Morse-bonded iron, fibre-network cotton, the head and scale, energy books (.cjs: the same file for the Node checks).', 'portfolios-src/impact/README.md'),
    (r'portfolios-src/impact/template\.html', 'The page template: layout, the store filled by record(), drawing, playback, gauges, plots.', 'portfolios-src/impact/README.md'),
    (r'portfolios-src/impact/datahooks\.js', "The data panel's hooks for the study (Sim.data: Read values, Check, read-back, one round = one drop).", 'docs/portfolios.md'),
    (r'portfolios-src/impact/text_(en|ar)\.py', lambda m: 'Every word of the %s page.' % ('English' if m.group(1) == 'en' else 'Arabic'), 'portfolios-src/impact/README.md'),
    (r'portfolios-src/impact/build\.py', 'Generates public/portfolios/impact/index.html and ar.html (--site), or stand-alone pages in out/.', 'portfolios-src/impact/README.md'),
    (r'portfolios-src/impact/checks/([a-z_0-9]+)\.cjs', lambda m: 'Check script %s (see the README).' % m.group(1), 'portfolios-src/impact/README.md'),
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
    (r'public/portfolios/hydraulics/LICENSE-fonts\.txt', 'Licences of the fonts embedded in the study (OFL 1.1; MIT for KaTeX).', 'docs/portfolios.md'),
    (r'public/portfolios/hydraulics/fig/0([1-4])_[a-z]+\.webp',
     lambda m: 'Plate %s of the study on the Portfolios page, 600 px high.' % m.group(1), 'docs/portfolios.md'),
    # Iron, Cotton and the Head: two generated pages, English and Arabic
    (r'public/portfolios/impact/index\.html', 'Iron, Cotton and the Head in English, generated from portfolios-src/impact/ by build.py --site.', 'docs/portfolios.md'),
    (r'public/portfolios/impact/ar\.html', 'Iron, Cotton and the Head in Arabic, generated from portfolios-src/impact/ by build.py --site.', 'docs/portfolios.md'),
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

# Folder sections in reading order; a file goes to the first whose prefix it starts with.
SECTIONS = [
    ('', 'Repository root', lambda p: '/' not in p),
    ('public/', 'Pages under public/', lambda p: p.startswith('public/') and p.count('/') == 1),
    ('public/de/', 'German pages (generated)', None), ('public/ar/', 'Arabic pages (generated)', None),
    ('public/simulations/', 'Simulation pages', None),
    ('public/scripts/walk/', 'Walkthroughs', None), ('public/scripts/', 'Shared scripts', None),
    ('public/styles/', 'Stylesheets', None),
    ('public/vendor/katex/', 'KaTeX', None), ('public/fonts/lm/', 'Latin Modern', None),
    ('public/fonts/', 'IBM Plex, Instrument Serif, and the Arabic faces', None),
    ('public/images/sims/', 'Thumbnails', None),
    ('public/images/', 'Logo', None),
    ('public/portfolios/droplet-collection/', 'Project copy: Droplet Collection', None),
    ('public/portfolios/rotor-pendula/', 'Project copy: Rotor Pendula', None),
    ('public/portfolios/hydraulics/', 'Project copy: Hydraulic Press Study', None),
    ('public/portfolios/impact/', 'Iron, Cotton and the Head', None),
    ('portfolios-src/hydraulics/', 'Source of the Hydraulic Press Study (not served)', None),
    ('portfolios-src/impact/', 'Source of Iron, Cotton and the Head (not served)', None),
    ('portfolios-src/rotor-pendula/', 'Source of the Rotor Pendula notes (not served)', None),
    ('src/', 'Template sources', None), ('tests/', 'Platform tests', None),
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

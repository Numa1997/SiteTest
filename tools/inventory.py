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
    (r'tools/kaggle/schrodinger-sphere/to_site_axisym\.py', 'Schrödinger on Kaggle: packs the stored cuts through the flight axis (|psi| and arg psi, half-plane rho >= 0) into the website files from which the page spins the 3D wave; checks the mirror symmetry.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'tools/kaggle/schrodinger-sphere/to_site\.py', 'Schrödinger on Kaggle: turns the notebook\'s run files into the website\'s data (one binary file per run with its SHA-256, and index.json).', 'docs/kaggle.md'),
    (r'public/data/schrodinger-sphere/generations\.json', 'Fig. 14 data: the list of generations, one dated folder each, with the Kaggle notebook, version and commit; written by to_site.py.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/shapes3d/index\.json', lambda m: 'Fig. 14 data generated on Kaggle on ' + m.group(1) + ': the 3D generation (coin, tube, sphere wells and hard ball, spherical wave from the side): groups, constants, notebook, version, commit, and per run its file, size and SHA-256.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/shapes3d/(\w+)/(w_)?e\d_v\d+_s\d\.bin', lambda m: 'Fig. 14 data generated on Kaggle on ' + m.group(1) + ': one 3D run of the ' + m.group(2) + ' group, ' + ('the true 3D wave Re psi (SPHW)' if m.group(3) else 'the plane z = 0, |psi| and arg psi (SPHC)') + '.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/index\.json', lambda m: 'Fig. 14 data generated on Kaggle on ' + m.group(1) + ': the grid, the numerical constants, the notebook, version and commit, and per run its file, size, SHA-256 and end probabilities.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/e\d_v\d_r\d\.bin', lambda m: 'Fig. 14 data generated on Kaggle on ' + m.group(1) + ': one stored run (header with the probability curves, then the zlib frames of |psi| and arg psi on the half-plane through the flight axis, from which the page spins the 3D wave).', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/wave3d/index\.json', lambda m: 'Fig. 14 true 3D wave generated on Kaggle on ' + m.group(1) + ': the 81 runs at R = 4, the box, the notebook, version and commit, and per run its file, size and SHA-256.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/wave3d/e\d_v\d_r\d\.bin', lambda m: 'Fig. 14 true 3D wave generated on Kaggle on ' + m.group(1) + ': one run, 32 frames of Re psi on every point of the box x in [-24, 24), y and z in [-16, 16), 0.5 a apart (SPHW, int8 levels).', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/flat/index\.json', lambda m: 'Fig. 14 flat wall generated on Kaggle (CPU) on ' + m.group(1) + ': 585 runs, the grid, the notebook, version and commit, the check against the exact transmission, and per run its file, size and SHA-256.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/flat/e\d_v\d+_a\d\.bin', lambda m: 'Fig. 14 flat wall generated on Kaggle on ' + m.group(1) + ': one run (SPHC: the half-plane through the axis of psi = chi(x) g(y) g(z), 48 frames, probability curves, T_packet).', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/pillar/index\.json', lambda m: 'Fig. 14 pillar generated on Kaggle (CPU) on ' + m.group(1) + ': 585 runs, the grid, the notebook, version and commit, and per run its file, size and SHA-256; gz.bin with its SHA-256.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/pillar/e\d_v\d+_r\d\.bin', lambda m: 'Fig. 14 pillar generated on Kaggle on ' + m.group(1) + ': one run (SPHC layout: the top view phi(x, y >= 0), 48 frames, probability curves).', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/pillar/gz\.bin', lambda m: 'Fig. 14 pillar, ' + m.group(1) + ': the free spread g(z, t) along the column, float32 per energy and frame, so that psi = phi(x, y) g(z).', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/radial/index\.json', lambda m: 'Fig. 14 spherical waves generated on Kaggle (CPU) on ' + m.group(1) + ': 1170 runs (out and in), the grid, the notebook, version and commit, the check against the exact transmission, and per run its file, size and SHA-256.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/data/schrodinger-sphere/(\d{4}-\d\d-\d\d)/radial/(out|in)_e\d_v\d+_s\d\.bin', lambda m: 'Fig. 14 spherical wave generated on Kaggle on ' + m.group(1) + ': one run (SPHR: psi(r) at 97 radii, |psi| and arg psi levels of each frame’s peak, 48 frames, probability curves).', 'docs/simulations/fig14-schrodinger-sphere.md'),
    # --- Fig. 15 resonant tunnelling (data built from Fig. 14's stored runs) ---
    (r'public/scripts/resonant-note\.js', 'Fig. 15 lecture note: the whole study, injected into the page’s <article> and typeset by sim.js (KaTeX); the 1D theory as the exact core, the 3D computation and its measured grid error, discs and shells, the device.', 'docs/simulations/fig15-resonant-tunnelling.md'),
    (r'tools/kaggle/resonant-tunnelling/(tm|recon|cn|iv|real_units|pack|extract_t|b1_first|b1_survey|check_cn|rt3d|rt3d_run|build_rt3d|read_rt3d|file_rt3d|exact1d|rt3d2|rt3d2_run|build_rt3d2|file_rt3d2)\.py', lambda m: {'file_rt3d2': 'Fig. 15, 3D generation 2: files the Kaggle runs (SHA-256 checked) and writes kaggle/index.json; draft, generalised from file_rt3d.py.', 'rt3d2': 'Fig. 15, 3D generation 2: the solver generalised to any number of walls, discs or shells, any height, thickness and spacing (faces kept on cell boundaries), a bias across the structure and long packets; with the walls\u2019 exact 1D twin.', 'rt3d2_run': 'Fig. 15, 3D generation 2: the job list of the whole parameter space (3739 runs) and the Kaggle run code: shards, one worker per GPU, each run saved as it finishes, a progress line per run, index with SHA-256.', 'build_rt3d2': 'Fig. 15, 3D generation 2: writes the Kaggle loader notebook for a commit, job set and shard.', 'file_rt3d': 'Fig. 15, 3D: files the Kaggle runs on the site (SHA-256 checked against each notebook\u2019s index) and writes kaggle/index.json with provenance and the numbers read from each run.', 'exact1d': 'Fig. 15, 3D: the exact 1D numbers for the 3D geometry (T(E), packet average, resonance, I–V, real units), the check of the 3D runs.', 'read_rt3d': 'Fig. 15, 3D: reads the RT3C run files from Kaggle and prints the checks of each run (timing, start state, 3D vs 1D twin, transmission).', 'rt3d': 'Fig. 15, 3D: split-step Fourier solver (JAX, GPU) for a wave packet meeting two barriers in 3D (two walls, two coins, two concentric shells) and the single barriers; and the walls\u2019 exact 1D twin.', 'rt3d_run': 'Fig. 15, 3D: the run code the Kaggle notebook fetches at a pinned commit (one worker per GPU, each run written as it finishes, one progress line per run, index with SHA-256).', 'build_rt3d': 'Fig. 15, 3D: writes the Kaggle loader notebook for a commit, job set and shard.', 'tm': 'Fig. 15: transfer matrices for piecewise-constant potentials (edge, flight, the single and double barrier, the scattering state).', 'recon': 'Fig. 15: builds the time-dependent double-barrier wave from the exact scattering states superposed with the packet spectrum, and stores the frames (RTF1) with the probabilities, T(E), resonances and the trapped-state fit.', 'cn': 'Fig. 15: an independent Crank–Nicolson solver of the double barrier (the scheme of flat.py), to check the reconstruction.', 'iv': 'Fig. 15: the current–voltage curve by the Tsu–Esaki formula, with the biased barriers as a staircase of transfer matrices (convergence checked).', 'real_units': 'Fig. 15: turns the dimensionless numbers into GaAs/AlGaAs nanometres, millivolts, femtoseconds and kA/cm², written into curves.json.', 'pack': 'Fig. 15: files the reconstructed runs under public/data/resonant-tunnelling/ with SHA-256 and provenance (the Fig. 14 parent runs).', 'extract_t': 'Fig. 15, Step B1: reads the single-barrier t(k), r(k) off Fig. 14’s stored runs, to check the exact amplitudes.', 'b1_first': 'Fig. 15: the first B1 measurement on three stored flat-wall runs, error split by source.', 'b1_survey': 'Fig. 15: the B1 check across every finite single-barrier run of Fig. 14.', 'check_cn': 'Fig. 15: compares the reconstruction with the Crank–Nicolson solve, frame by frame.'}[m.group(1)], 'docs/simulations/fig15-resonant-tunnelling.md'),
    (r'tools/kaggle/resonant-tunnelling/rt3d2?_(smoke|singles_v2|fix1|all_\d+of\d+)\.ipynb', lambda m: 'Fig. 15, 3D: the Kaggle loader notebook (' + m.group(1) + '), written by build_rt3d.py for a pinned commit; fetches rt3d.py, tm.py, rt3d_run.py and runs them on the GPUs.', 'docs/simulations/fig15-resonant-tunnelling.md'),
    (r'public/data/resonant-tunnelling/generations\.json', 'Fig. 15 data: the list of generations, each with its Kaggle index, the exact 1D check, the notebooks and the source scripts.', 'docs/simulations/fig15-resonant-tunnelling.md'),
    (r'public/data/resonant-tunnelling/(\d{4}-\d\d-\d\d)/kaggle/index\.json', lambda m: 'Fig. 15 3D runs (' + m.group(1) + '): per run its file, SHA-256, Kaggle notebook, version and commit, and the numbers read from it (share through, lifetime, the 1D twin); which version-1 runs were replaced and why.', 'docs/simulations/fig15-resonant-tunnelling.md'),
    (r'public/data/resonant-tunnelling/(\d{4}-\d\d-\d\d)/kaggle/runs/([ds](?:flat|coin|shell))_R[\d.]+_E[\d.]+\.bin', lambda m: 'Fig. 15 3D run (' + m.group(1) + ', ' + m.group(2) + '): RT3C, 200 frames of |ψ| and arg ψ on the plane z = 0 (8-bit), the profile along x, region probabilities' + (', and the exact 1D twin' if 'flat' in m.group(2) else '') + '; as Kaggle wrote it.', 'docs/simulations/fig15-resonant-tunnelling.md'),
    (r'public/data/resonant-tunnelling/(\d{4}-\d\d-\d\d)/derived/exact-1d\.json', lambda m: 'Fig. 15 (' + m.group(1) + '): the exact 1D numbers for the 3D geometry (T(E), the packet average, the resonance, the I–V curve, real units), kept as the check of the 3D runs.', 'docs/simulations/fig15-resonant-tunnelling.md'),
    (r'public/scripts/rt3d-(view|worker)\.js', lambda m: {'view': 'Fig. 15: the 3D view (three.js): the meshed height sheet in the house colours and the barriers as static lit glass solids at their true place; turning by press and drag.', 'worker': 'Fig. 15: the background thread that fetches one stored 3D run, checks its SHA-256, inflates it and turns the 8-bit levels into ψ.'}[m.group(1)], 'docs/simulations/fig15-resonant-tunnelling.md'),
    (r'public/scripts/fig14-sheet-worker\.js', 'Fig. 14 meshed sheet, off the main thread: band-limited resampling of a stored frame onto the sheet (1/6 a), and the numbers that scale its height.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/scripts/fig14-iso-worker\.js', 'Fig. 14 sheets, off the main thread (module worker): Lanczos resampling of the 3D field and marching cubes for Re psi = +c and -c.', 'docs/scripts/wave3d-view.md'),
    (r'public/scripts/marching\.js', 'Marching cubes on a rectangular grid (tables from three.js), shared by wave3d-view.js and fig14-iso-worker.js.', 'docs/scripts/wave3d-view.md'),
    (r'public/scripts/wave3d-view\.js', 'Fig. 14 lit 3D views (three.js): sheets of Re psi = +-c by marching cubes, the height surface of the plane z = 0, the cutaway; barrier solids; drag to turn; projection and pixel read-back for the data panel.', 'docs/scripts/wave3d-view.md'),
    (r'tools/kaggle/schrodinger-shapes/(solver3d\.py|shapes3d_run\.py|build_shapes3d\.py|shapes3d\.ipynb|to_site_shapes3d\.py|merge_v2\.py)', lambda m: {'merge_v2.py': 'Fig. 14, the remaining 3D cases: merges version 2 (the 243 runs with a corrected start wave, computed on Kaggle CPU) into the website generation, every SHA-256 checked.', 'solver3d.py': 'Fig. 14, the remaining 3D cases: split-step Fourier on 128^3 points for the coin, the tube, the sphere wells and hard ball, and a spherical wave from the side onto a ball, a wall and a pillar.', 'shapes3d_run.py': 'Fig. 14, the remaining 3D cases: the run code the Kaggle notebook fetches at a pinned commit (1458 runs on two GPUs, each file written as it finishes).', 'build_shapes3d.py': 'Fig. 14, the remaining 3D cases: writes shapes3d_run.py and the loader notebook shapes3d.ipynb for a given commit.', 'shapes3d.ipynb': 'Fig. 14, the remaining 3D cases: the Kaggle notebook as sent (numakoudsie/schrodinger-shapes-3d, version 1).', 'to_site_shapes3d.py': 'Fig. 14, the remaining 3D cases: unpacks the Kaggle output into the website, checks every SHA-256, adds the generation.'}[m.group(1)], 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'tools/kaggle/schrodinger-shapes/(flat\.py|check_flat\.py|build_flat\.py|flat\.ipynb|pillar\.py|check_pillar\.py|build_pillar\.py|pillar\.ipynb|radial\.py|build_radial\.py|radial\.ipynb)', lambda m: {'flat.py': 'Fig. 14 flat wall: the 1D Crank-Nicolson solver (fourth-order Laplacian, hard wall by odd mirror) for psi = chi(x) g(y) g(z), and the exact plane-wave and packet transmission.', 'check_flat.py': 'Fig. 14 flat wall: checks the transmission formula against the matching equations, the free Gaussian with SymPy, and the solver against T_packet.', 'build_flat.py': 'Fig. 14 flat wall: writes flat.ipynb (Kaggle, CPU, 585 runs) for a given commit.', 'flat.ipynb': 'Fig. 14 flat wall: the Kaggle notebook as run (version 1), written by build_flat.py.', 'pillar.py': 'Fig. 14 pillar: the 2D split-step Fourier solver for psi = phi(x, y) g(z) (hard column by setting psi = 0 inside after every step).', 'check_pillar.py': 'Fig. 14 pillar: convergence in the time step and the mirror check.', 'build_pillar.py': 'Fig. 14 pillar: writes pillar.ipynb (Kaggle, CPU, 585 runs) for a given commit.', 'radial.py': 'Fig. 14 spherical waves: u = r psi with l = 0, the 1D half-line problem solved on the whole line with u odd (Crank-Nicolson, fourth-order Laplacian); a shell leaving the centre or closing in.', 'build_radial.py': 'Fig. 14 spherical waves: writes radial.ipynb (Kaggle, CPU, 1170 runs) for a given commit.', 'radial.ipynb': 'Fig. 14 spherical waves: the Kaggle notebook as run (version 1), written by build_radial.py.', 'pillar.ipynb': 'Fig. 14 pillar: the Kaggle notebook as run (version 1), written by build_pillar.py.'}[m.group(1)], 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/scripts/volume-view\.js', 'Draws a stored 3D cloud as fog by ray marching in WebGL2, with a glass sphere and a camera turned by dragging; recomputes any pixel on the CPU for the data panel (Fig. 14).', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'worker/r2\.js', 'The site\u2019s Worker: serves the large stored runs from the R2 bucket RUNS under /r2/ (Fig. 15 generation 2); every other path is an asset, as before.', 'docs/simulations/fig15-resonant-tunnelling.md'),
    (r'notes/fig15/LESSONS\.md', 'Fig. 15: the final goal (data generated on Kaggle, stored, played smoothly by the page) and every mistake made on Fig. 14, written on the owner\'s instruction for the Fig. 15 session.', 'notes/fig15/LESSONS.md'),
    (r'notes/fig15/BRIEF\.md', 'Fig. 15 (resonant tunnelling, built on the stored runs of Fig. 14): the brief for the session that builds it, written on the owner\'s instruction on 13 November 2026.', 'notes/fig15/BRIEF.md'),
    (r'notes/fig14/3d-wave-test\.png', 'Fig. 14: five frames of the wave itself (crests wine, troughs ink) of the first test run with Re psi stored (E = 2, V0 = 3, R = 4), drawn by volume-view.js.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'notes/fig14/wave3d_test\.py', 'Fig. 14: the test that computed one run on 128^3 points in this workspace and stored Re psi in 3D (96 x 64 x 64 points, 32 frames, int8).', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'notes/fig14/3d-test-strip\.png', 'Fig. 14: five frames of the first 3D test run (E = 2, V0 = 3, R = 4, computed in this workspace) drawn by volume-view.js.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'public/scripts/kaggle-flow\.js', 'The page side of the Kaggle pipeline: sliders that show the computed range and grow heavy near its edge, eased speed, the loading notice with the pipeline, the kaggle-bridge client.', 'docs/kaggle-pipeline.md'),
    (r'public/styles/kaggle-flow\.css', 'Styles of kaggle-flow.js: the computed band, soft zones and dots of the sliders, the loading notice and its pipeline drawing.', 'docs/kaggle-pipeline.md'),
    (r'public/scripts/schrodinger-live-worker\.js', 'Fig. 14 live preview: the same split-step Schrödinger solver as on Kaggle, 64^3 points, in a Web Worker, for regions not computed yet.', 'docs/simulations/fig14-schrodinger-sphere.md'),
    (r'tools/kaggle/schrodinger-sphere/(solver\.py|pack\.py|panel_template\.html|build_smoke\.py|smoke\.ipynb|build_full\.py|full\.ipynb|build_3d\.py|full3d\.ipynb|build_wave\.py|wave3d\.ipynb)', lambda m: {'solver.py': 'Schrödinger on Kaggle: the 3D split-step Fourier solver (JAX) for a wave packet meeting a spherical barrier; one run, its frames and its curves.', 'pack.py': 'Schrödinger on Kaggle: packs runs (zlib, base64) into the panel page.', 'panel_template.html': 'Schrödinger on Kaggle: the animator panel that only plays stored runs (sliders with computed positions marked, amplitude or phase, probability curves).', 'build_smoke.py': 'Schrödinger on Kaggle: writes smoke.ipynb for a given commit.', 'smoke.ipynb': 'Schrödinger on Kaggle: the GPU test notebook (timing, accuracy, 8 runs, panel), written by build_smoke.py.', 'build_full.py': 'Schrödinger on Kaggle: writes full.ipynb for a given commit.', 'full.ipynb': 'Schrödinger on Kaggle: the full grid, 405 runs on both GPUs, one JSON file per run plus index.json and a preview panel; written by build_full.py.', 'build_3d.py': 'Schrödinger on Kaggle: writes full3d.ipynb, the 3D generation, for a given commit.', 'full3d.ipynb': 'Schrödinger on Kaggle: the 3D generation, 81 runs at R = 4 on both GPUs, each stored as 48 frames of the 3D cloud on 64^3 cells in the website format; written by build_3d.py.', 'build_wave.py': 'Schrödinger on Kaggle: writes wave3d.ipynb, the 3D wave generation, for a given commit.', 'wave3d.ipynb': 'Schrödinger on Kaggle: the 3D wave, 81 runs at R = 4 on both GPUs, each 32 frames of Re psi on every computed point of a 96 x 64 x 64 box; written by build_wave.py.'}[m.group(1)], 'docs/kaggle.md'),
    (r'tools/redirects\.py', 'Writes public/_redirects, the short address of every page served without a round trip; --check fails if the file is out of date.', 'docs/usul.md'),
    (r'notes/inventory/.+', 'Inventory and clean-up of the computations (Kaggle, R2, scripts): state, records, copies of deleted Kaggle notebooks, manifests of the per-figure Kaggle datasets.', 'notes/inventory/STATE.md'),
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
    (r'notes/fig12/jax/run8-check/run[89]-check\.txt', 'Fig. 12 in JAX: the output of check_run.py for Kaggle run 8 (notebook version 8) or the kerb with road preview (version 9): every check, ALL PASS', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/jax/run8-check/run[89]-summary\.json', 'Fig. 12 in JAX: the summary.json that run 8 or version 9 wrote on Kaggle: each task\u2019s steps, run time, books, plant and leans', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/handoff-jax/06-run8-state\.md', 'Fig. 12 in JAX: the full state of the chat that ran run 8 (aim, what is live, what is left, commits, files, the user\u2019s rules); reread after a compaction', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/note_numbers\.py', 'Fig. 12 note: prints every number the note quotes, from the stored runs and the model\u2019s constants; --check lists the note\u2019s numbers no entry prints', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/build_note\.py', 'Fig. 12 note: fills the {{name}} numbers of notes/fig12/note/paper.html from note_numbers.py and writes the note into guinness-kaggle.html', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/note/paper\.html', 'Fig. 12 note: the source of the note of guinness-kaggle.html, its computed numbers written as {{name}}', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/note-numbers\.json', 'Fig. 12 note: the numbers note_numbers.py printed, name, value and printed text', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/readers/.+\.md', 'Fig. 12 note: the marks of an independent reader, or the derivation checker\u2019s table, for one round of the note', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/handoff-jax/07-diagnosis\.md', 'Fig. 12 in JAX: diagnosis of five open items after the note (lean readings, rim points, kerb residue, numerical damping, the Play button)', 'docs/simulations/fig12-beer-slosh.md'),
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
    (r'notes/lucretius/make_bg\.py', 'Draws the three background strips of the Lucretius page (fractal branches, Weierstrass lines, spiral tendrils) as tiling SVGs.', 'docs/pages.md#the-poem-page-lucretiushtml-10-november-2026-rebuilt-11-november-2026'),
    (r'public/images/lucretius/bg-[abc]\.svg', 'Background strips of the Lucretius page, written by notes/lucretius/make_bg.py.', 'docs/pages.md#the-poem-page-lucretiushtml-10-november-2026-rebuilt-11-november-2026'),
    (r'public/styles/lucretius-deco\.css', 'Places the background strips of the Lucretius page in both margins; ?bg=a|b|c picks one.', 'docs/pages.md#the-poem-page-lucretiushtml-10-november-2026-rebuilt-11-november-2026'),
    (r'notes/lucretius/make_home\.py', 'Writes the Lucretius band of the home page from the first four sentences.', 'notes/lucretius/README.md'),
    (r'notes/lucretius/make_page\.py', 'Writes public/lucretius.html: Lucretius I 146-224 in four columns (Latin, Leonard, Diels, Arabic).', 'notes/lucretius/README.md'),
    (r'notes/lucretius/poem-ar-146-224\.json', 'The Arabic of Lucretius I 146-224 (tenth version, free verse, fully vowelled), translated from the Latin for this site.', 'notes/lucretius/README.md'),
    (r'public/lucretius\.html', 'The poem page: Lucretius I 146-224 in four columns, Latin, English, German, Arabic (written by make_page.py; /de/ and /ar/ differ only in the words around the poem).', 'docs/pages.md#the-poem-page-lucretiushtml-10-november-2026-rebuilt-11-november-2026'),
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
    (r'(public/simulations/fig13|tools/fig13/gift)/reem\.json', 'Arrows (Fourier terms) and outlines of the words of the gift film, written by tools/fig13/gift/reem_data.py.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/reem\.html', 'Fig. 13 gift film source (For رِيمْ, phone first): the name (traced from the reference plate) and فَرَاشَتُكِ (Amiri) written by 640 turning arrows each, gold on navy or ink on paper.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/(reem_data|calligraphy)\.py', lambda m: {'reem_data': 'Fig. 13 gift: the Fourier terms of each word\'s outline (640 arrows), checked against the outline', 'calligraphy': 'Fig. 13 gift: outlines of Arabic words, shaped by HarfBuzz, flattened by fontTools'}[m.group(1)] + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/fonts/(NotoNastaliqUrdu-wght\.ttf|OFL-NotoNastaliqUrdu\.txt)', lambda m: 'Noto Nastaliq Urdu, the calligraphy font of the gift film (Google Fonts, SIL Open Font License 1.1): ' + ('the font' if m.group(1).endswith('ttf') else 'its licence') + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/fig13/(reem|construction|catch)\.html', lambda m: 'Fig. 13 film player (generated by tools/fig13/gift/film_page.py; do not edit): ' + {'catch': 'the catch, drawn live', 'reem': 'the eight films in order, drawn live, starting with the gift For رِيمْ (?part=k starts at part k)', 'construction': 'the butterfly built by hand, drawn live'}[m.group(1)] + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/catch\.html', 'Fig. 13 film source (phone first): catching the butterfly with a motor at the top pin, from chaos; the motion is computed live by pendulum.js.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/fig13/film\.html', 'Fig. 13: the whole gift as one film drawn live (generated by tools/fig13/gift/film_page.py; do not edit).', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/fig13/live-(gift|construction|catch)\.html', lambda m: 'Fig. 13 live film (generated by publish_films.py; do not edit): ' + m.group(1) + ', played by film.html.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/fig13/reem\.json', 'Fig. 13: the Fourier terms of the two words, copied by publish_films.py.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'(public/simulations/fig13|tools/fig13/gift)/pendulum\.js', 'Fig. 13: the double pendulum and the motor controller computed live in the browser (the films reem, construction, catch); copied to the site by publish_films.py.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/fig13/fonts/(.+)', lambda m: 'Instrument Sans for the live films (copied by publish_films.py): ' + m.group(1) + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'public/simulations/butterfly-catch\.html', 'Fig. 13: catching the butterfly, the live interactive catch and its lecture note (theory and method); body from tools/fig13/catch_note_body.html.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/fig13_note\.html', 'Fig. 13: Part I of the page\'s lecture note (the sheet and the eye); build_page.py joins it with the other parts into momentum-spirographs.html.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/butterfly_note\.html', 'Fig. 13: the section of the lecture note on the butterfly as a machine (strike, speeds, forces); joined in by build_page.py.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/build_page\.py', 'Fig. 13: joins the four notes (sheet and eye, butterfly, flower hunt, catch) into the one article of momentum-spirographs.html, with one numbering; --check fails if the page is stale.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/catch_stats\.cjs', 'Fig. 13: the catch statistics of the lecture note from the browser\'s own pendulum.js, in Node (random starts, the basin, one strike; any step size and seed).', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/catch_targets\.cjs', 'Fig. 13: the catch measured for every pattern of PEND.TARGETS (ten flowers, four butterflies) from the browser\'s own pendulum.js, in Node: held or not, time from the press, hold torque.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/release_check\.py', 'Fig. 13: how long released pendulums stay on the butterfly, by DOP853, from the runs written by catch_stats.cjs.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/catch_note_body\.html', 'Fig. 13: the body of butterfly-catch.html (the catch lecture note); assembled with the house head and header.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/film_page\.py', 'Fig. 13: writes public/simulations/fig13/film.html, the whole gift drawn live.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/construction\.html', 'Fig. 13 film source (phone first): the construction by ruler of a wheel and of the butterfly from h(t) and x(t), the two time axes joined by a mitre.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/fonts/(Amiri-Regular\.ttf|OFL-Amiri\.txt)', lambda m: 'Amiri (Khaled Hosny; SIL Open Font License 1.1), the Naskh of فَرَاشَتُكِ in the gift film and the master model of qalam2/3.py: ' + ('the font' if m.group(1).endswith('ttf') else 'its licence') + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/(qalam|qalam2|qalam3|skeleton|ref_trace|plate)\.py', lambda m: 'Fig. 13 gift calligraphy: ' + {'qalam': 'a simulated reed pen and a first hand-made sketch of the name (superseded)', 'qalam2': 'reed strokes over a master model, a mirror composition (rejected by Numa)', 'qalam3': 'reed re-inking of a whole word (falls short of the model; kept as a record)', 'skeleton': 'centre lines of a word in a model font', 'ref_trace': 'vector outlines of the ink in the reference plate Numa chose', 'plate': 'the traced word as gold-on-navy and paper plates'}[m.group(1)] + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/farashatuki\.json', 'The outlines of فَرَاشَتُكِ traced from the Diwani plate Numa chose on 9 November 2026 (farashatuki_trace.py); the source of the word in the gift film.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/(farashatuki|farashatuki_v2|farashatuki_trace)\.py', lambda m: 'Fig. 13 gift: ' + {'farashatuki': 'فَرَاشَتُكِ written in the hand of the traced رِيمْ (rejected by Numa: disconnected letters)', 'farashatuki_v2': 'three compositions of فَرَاشَتُكِ in that hand (shown, not used)', 'farashatuki_trace': 'traces فَرَاشَتُكِ from the Diwani plate Numa chose (gold on a dark board) into farashatuki.json'}[m.group(1)] + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/gift/fonts/(instrument-sans-400\.woff2|instrument-sans-500\.woff2|OFL-InstrumentSans\.txt)', lambda m: 'Instrument Sans (SIL Open Font License 1.1), the labels and numbers of the gift and construction films at Numa\'s request (9 November 2026), digits made tabular: ' + ('its licence' if m.group(1).endswith('txt') else 'weight ' + m.group(1)[16:19]) + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
    (r'tools/fig13/(butterfly_physics|butterfly_control)\.py', lambda m: 'Fig. 13: ' + {'butterfly_physics': 'the butterfly studied physically (the strike, speeds, the pull on the top pin, exact Floquet multipliers, twins, long runs, a map of strikes)', 'butterfly_control': 'a motor at the top pin catches the pendulum and holds it on the butterfly (periodic LQR along the orbit; pump, wait, catch)'}[m.group(1)] + '.', 'docs/simulations/fig13-momentum-spirographs.md'),
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
    (r'public/vendor/three/three\.module\.min\.js', 'three.js 0.170.0, the WebGL 3D library (ES module), for the lit views of Fig. 14.', 'docs/assets.md'),
    (r'public/vendor/three/MarchingCubes\.js', 'three.js 0.170.0 addon MarchingCubes, here for its edge and triangle tables (import path set to the local three.module.min.js).', 'docs/assets.md'),
    (r'public/vendor/three/LICENSE', 'The MIT licence of three.js.', 'docs/assets.md'),
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
    (r'public/scripts/guinness-playback\.js', 'Fig. 12, computed on Kaggle: plays the stored Kaggle rides through stout-view.js; the speed control from kaggle-flow.js, eased speed, a labelled live preview on speeds Kaggle has not computed, cross-fades, the pipeline notice only at zero speed; the store and the data panel hooks; the phase space.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/scripts/guinness-preview-worker\.js', 'Fig. 12, computed on Kaggle: the live preview in a Worker, the site\u2019s coarse solver (stout-cart.js, 4 mm) over the same road, one frame per 1/30 s in the stored rides\u2019 format.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/simulations/guinness-kaggle\.html', 'Fig. 12, computed on Kaggle: the page that plays the stored rides of the pint on the cart in 3D.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/data/fig12/[0-9-]+/rides\.json', 'Fig. 12 rides computed on Kaggle, named by the date of generation: per frame the cart state, lean, spill and the stout surface on the 17 x 64 polar grid (uint8, zlib, base64).', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/data/fig12/[0-9-]+/index\.json', 'Fig. 12 Kaggle data index: generation date, Kaggle notebook and version, solver, measured times, SHA-256 of each file.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/data/fig12/[0-9a-z-]+/index-jax\.json', 'Fig. 12 in JAX: the list of rides computed on Kaggle\u2019s GPU that the page plays (label, default, size, SHA-256, frames, measured times), with the notebook, its version and the code commit', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/data/fig12/[0-9a-z-]+/(ride_\w+|free_\w+?_[0-9.]+)\.json', 'Fig. 12 in JAX: one ride or free swing computed on Kaggle\u2019s GPU, packed by pack_ride.py: per stored frame the stout\u2019s surface on the solver\u2019s columns, the head\u2019s thickness, drops, lumps of head, and the cart; from run 8 also the stout and the head in the glass and spilled (the books) and the controllers\u2019 plant', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/scripts/guinness-jax-play\.js', 'Fig. 12 in JAX: plays the stored rides listed in index-jax.json in real time through StoutView2 (no interpolation, no slowing, each file checked against its SHA-256), the ride chooser, the road strip and the readings; computes nothing physical', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/scripts/stout-view2\.js', 'Fig. 12 in JAX: unpacks a stored ride (StoutRide) and draws the glass from its stored fields (StoutView2, on StoutView\u2019s cart, road and camera): the stout\u2019s body, the head of the stored thickness, drops and lumps of head, the lettering on the glass; computes nothing physical', 'docs/simulations/fig12-beer-slosh.md'),
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
    (r'tools/fig12/cart_damping\.cjs', 'Fig. 12 computed on Kaggle: the reduced sloshing model on the same cart and road as the Kaggle rides, with and without the stout\u2019s own damping, so the cart\u2019s share of the swing\u2019s damping can be measured (output in the temporary folder).', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/solver\.py', 'Fig. 12 computed on Kaggle: the GPU solver v2 (Taichi): the stout as APIC particles on a 1.5 mm grid with a ghost-fluid free surface and free-slip glass faces, the wall\u2019s boundary layer and the foam as drags, coupled both ways to the port of the site\u2019s cart; the notebooks download it at a pinned commit', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/jax/view-test\.html', 'Fig. 12 in JAX: test page (not on the site) that draws one stored frame of a packed ride with stout-view2.js', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/jax/shots\.cjs', 'Fig. 12 in JAX: screenshots of that test page for chosen frames (Playwright)', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/research/verification\.md', 'Fig. 12: the parent session\u2019s verification of the research note (what was read, independent Wolfram checks, the falsification test of the foam wall-friction law against Viola 2016) and the model taken into the solver', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/research/guinness-materials\.md', 'Fig. 12: research note on the stout, its head and the boundary layers with the glass: facts with sources, derivations, parameter tables, video catalogue (13 November 2026).', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/research/sources/.+\.txt', 'Fig. 12: verbatim extract of one source (citation, URL, licence, passages with page numbers) for guinness-materials.md.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/research/wolfram/.+\.wl', 'Fig. 12: Wolfram Language derivation for guinness-materials.md (slosh damping, bubbles, the head as a soft solid).', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/research/wolfram/.+\.out\.txt', 'Fig. 12: saved output of the Wolfram derivation of the same name.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/research/sympy/.+\.py', 'Fig. 12: SymPy check of the Wolfram derivations for guinness-materials.md.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'notes/fig12/research/sympy/.+\.out\.txt', 'Fig. 12: saved output of the SymPy check of the same name.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/nb/run_b_cell\.py', 'Fig. 12 in JAX: the one cell of the Kaggle notebook guinness-on-a-cart-stout-in-jax (version 1): checks the GPU, fetches stout_jax.py and run_b.py at a pinned commit, runs them', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/pack_ride\.py', 'Fig. 12 in JAX: packs one ride computed on Kaggle (.npz) into the page\u2019s file (surface on the solver\u2019s columns, head thickness, drops, lumps of head, the cart, stout and head in the glass) and lists it in index-jax.json with its SHA-256; computes nothing', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/gate_rest\.py', 'Fig. 12 in JAX: the free check before any GPU launch: the full model at rest for one second on a coarse grid, with the checks that would have caught run 2\u2019s coding faults (executed 13 November 2026); see notes/fig12/handoff-jax/02-launch-gates.md', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/stout_jax\.py', 'Fig. 12 in JAX on Kaggle\u2019s GPU: the stout (APIC particles, cut-cell glass, level-set free surface with ghost-fluid pressure, wall and foam friction, the head\u2019s weight and, from run 8, its mass), the drops that leave over the rim, and the cart, all computed on the GPU and coupled both ways; the algorithm of solver.py written again in JAX', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/run_b\.py', 'Fig. 12 in JAX on Kaggle\u2019s GPU: what a run computes and stores: the pint at rest first, with a guard that stops the session if it is not flat and full, then the rides, the free swing with and without the head; RUNSET=run8 designs the controllers on the swing it measures and checks the books of every frame; each task only if the measured time says it ends inside the budget', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/portcheck/cart_js\.cjs', 'Fig. 12 in JAX: the site\u2019s Cart of stout-cart.js on one road with a rigid load and a prescribed probe signal, the reference for the JAX port of the controllers', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/portcheck/cart_jax\.py', 'Fig. 12 in JAX: the JAX cart with each controller (speed, preview, skyhook, slosh LQR, joint) against the JS reference, every 2 ms for 3 s on the kerb; output in notes/fig12/handoff-jax/portcheck.txt', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/portcheck/case\.json', 'Fig. 12 in JAX: the road, load, plant and probe signal both carts of the port check run on', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/check_run\.py', 'Fig. 12 in JAX: the result checks of gate E on one downloaded run (lists never full, pressure residual, energy books, the books of stout and head in every frame, impulse against momentum, the free swing against theory and, with the head\u2019s mass, against 2.957 Hz); reads what Kaggle stored, computes no physics', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/rides\.py', 'Fig. 12 computed on Kaggle: drives the pint over the road at each speed with solver v2 and writes rides.json in the page\u2019s format, saved after every ride', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/free_params\.py', 'Fig. 12 computed on Kaggle: the parameters and the progress log shared by the free-swing tests and the rides', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/env\.py', 'Fig. 12 computed on Kaggle: installs Taichi, stops if no GPU, fetches the glass profile and drawing code at a pinned commit', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/free_swing\.py', 'Fig. 12 computed on Kaggle: the free-swing test of solver v2 (glass held still, one push), per grid and piece of physics', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/free_swing_fit\.py', 'Fig. 12 computed on Kaggle: fits the damping ratio and frequency of every stored free swing', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle/store_rides\.py', 'Fig. 12 computed on Kaggle: stores a generation of rides in public/data/fig12/<date>/ with index.json (notebook, version, code commit, measured times, SHA-256)', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/data/fig12/2026-11-12/free_swing_v2(_repair)?\.json', 'Fig. 12 computed on Kaggle: free swings of solver v2 on a glass held still (energy, surface, damping), the test behind the numerical share of the stored damping', 'docs/simulations/fig12-beer-slosh.md'),
    (r'public/data/fig12/generations\.json', 'Fig. 12 computed on Kaggle: the list of stored generations of rides, newest last, with the solver of each', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/control/derive\.wl', 'Fig. 12 with control, Stage A, second route: the same numbers as derive.py evaluated in Wolfram Language (RiccatiSolve, MatrixExp, Bessel zeros).', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/control/derive\.wl\.out\.txt', 'Fig. 12 with control, Stage A: the Wolfram output of derive.wl (13 November 2026), equal to derive.py to the digits printed.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/control/ref_series\.(cjs|json)', 'Fig. 12 with control, Gate B1: reference rides of the site\u2019s reduced model (stout-cart.js, linear live model) over one 10 mm bump under six controllers, one row per 5 ms fluid step, for the JAX port to reproduce.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/control/derive_physics\.wl', 'Fig. 12 with control, Stage A in Wolfram: the sloshing mode from its Lagrangian, cart and mode as one Lagrangian, the motor loop as one sampled system with its margins, the heave threshold, the cart integrator\u2019s error.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/control/derive_physics\.out\.txt', 'Fig. 12 with control, Stage A: output of derive_physics.wl and the published sources each result was checked against.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/control/cartctl\.py', 'Fig. 12 with control, Stage B1: the cart, its drive, sensors, Kalman filter and every controller in JAX (float64, lax.scan, differentiable), a line-by-line port of stout-cart.js, with the linear three-mode stout.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/control/b1_run\.py', 'Fig. 12 with control, Gate B1 on Kaggle: the JAX port against ref_series.json for six controllers, time per ride, and a gradient through a whole ride checked by finite differences.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/control/(build_b1\.py|b1\.ipynb|b1_cell\.py)', 'Fig. 12 with control, Gate B1: the builder of the one-cell Kaggle notebook (fetches the code at a pinned commit), the notebook and its cell.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/control/derive\.py', 'Fig. 12 with control, Stage A: derives with SymPy and SciPy the first sloshing mode, its coupling to the cart’s push, the damping numbers, what each actuator can reach, the slosh and suspension LQR gains and the Kalman filter’s discrete matrices, and compares each with the number the site’s code prints; exits 1 if one differs.', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/control/derive\.out\.txt', 'Fig. 12 with control, Stage A: the saved output of derive.py (13 November 2026: every site number reproduced).', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/cart_damping\.cjs','Fig. 12 computed on Kaggle: the reduced sloshing model on the same cart and road as the Kaggle rides, with and without the stout\u2019s own damping, so the cart\u2019s share of the swing\u2019s damping can be measured (output in the temporary folder).', 'docs/simulations/fig12-beer-slosh.md'),
    (r'tools/fig12/kaggle_decay\.py', 'Fig. 12 computed on Kaggle: measures from the stored rides the first mode\u2019s frequency and how fast its swing dies after the last bump (a direct fit of the free decay, self-tested), and how far the wall lean drifts at steady speed.', 'docs/simulations/fig12-beer-slosh.md'),
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
    (r'notes/droplets/check-steps-r3\.md', 'Independent check of the step-by-step passages of sections 6.3, 6.4, 9 and 10.1 to 10.3 (11 November 2026): equations re-derived, numbers recomputed, method boxes compared with the code.', 'notes/droplets/status.md'),
    (r'notes/droplets/check-steps\.md', 'Independent check of the step-by-step derivations, method boxes and examples of 11 November 2026: each equation re-derived, each method box compared with its function in physics.cjs.', 'notes/droplets/status.md'),
    (r'notes/droplets/check-L(\d+)\.md', lambda m: 'Gate 2 check of level L' + m.group(1) + ': each equation re-derived by two routes.', 'notes/droplets/status.md'),
    (r'notes/droplets/dossier-([a-z-]+)\.md', lambda m: 'Scout dossier on ' + m.group(1) + ': primary sources read for the study.', 'notes/droplets/status.md'),
    (r'notes/droplets/skeptic-(G\d)-(L[0-9L]+)-r(\d)\.md', lambda m: 'Blind skeptic report, gate ' + m.group(1)[1:] + ', level ' + m.group(2) + ', round ' + m.group(3) + '.', 'notes/droplets/status.md'),
    (r'notes/droplets/skeptic-(G\d)-(.+)\.md', lambda m: 'Blind skeptic report, gate ' + m.group(1)[1:] + ': ' + m.group(2) + '.', 'notes/droplets/status.md'),
    (r'notes/droplets/review-answers-r(\d)\.md', lambda m: 'Answers to the independent reviews of Part IV, round ' + m.group(1) + '.', 'notes/droplets/status.md'),
    (r'notes/droplets/review-([a-z]+)-(.+)\.md', lambda m: 'Independent review (' + m.group(1) + ') of ' + m.group(2) + '.', 'notes/droplets/status.md'),
    (r'notes/droplets/gate3-answers-r(\d)\.md', lambda m: 'Answers to the Gate 3 skeptic, round ' + m.group(1) + '.', 'notes/droplets/status.md'),
    (r'notes/droplets/gate2/(.+)', lambda m: 'Gate 2 checker script or output: ' + m.group(1) + '.', 'notes/droplets/status.md'),
    (r'portfolios-src/electron-beam/PLAN\.md', 'Plan and brief of project 07, the electron beam from tip to measurement: aim, chapters, contract, sessions and file ownership.', 'docs/portfolios.md'),
    # --- electron-beam librarian (session S2, branch eb/librarian): sources and digitised data of project 07 ---
    (r'portfolios-src/electron-beam/sources/bibliography\.md', 'Project 07 bibliography: for each formula family the book or paper, section and page, marked READ or LOCATED, with what is still unopened.', 'portfolios-src/electron-beam/sources/bibliography.md'),
    (r'portfolios-src/electron-beam/sources/drive-inventory\.md', "Project 07: every file listed in Numa's Drive folders (EP4, Oldenburg), what the read-only connector could and could not read.", 'portfolios-src/electron-beam/sources/bibliography.md'),
    (r'portfolios-src/electron-beam/sources/applied-public\.md', "Project 07: Applied Materials' public statements (PROVision, SEMVision pages, press release) quoted as public claims only.", 'portfolios-src/electron-beam/sources/bibliography.md'),
    (r'portfolios-src/electron-beam/data/(ch\d\d)/README\.md', lambda m: 'Provenance of the published data digitised for chapter ' + str(int(m.group(1)[2:])) + ' of project 07: source, figure or table, how digitised, SI conversion, uncertainty.', 'portfolios-src/electron-beam/sources/bibliography.md'),
    (r'portfolios-src/electron-beam/data/(ch\d\d)/(.+)\.csv', lambda m: 'Published measurement digitised for chapter ' + str(int(m.group(1)[2:])) + ' of project 07: ' + m.group(2) + ' (provenance in the README beside it).', 'portfolios-src/electron-beam/sources/bibliography.md'),
    (r'notes/electron-beam/librarian-status\.md', 'Project 07 librarian status: what sources and data are ready for the chapter sessions, what is missing.', 'portfolios-src/electron-beam/sources/bibliography.md'),
    (r'notes/electron-beam/S2-report\.md', 'Project 07 librarian final report: sources, data, gaps, handles for every claim.', 'portfolios-src/electron-beam/sources/bibliography.md'),
    # --- end electron-beam librarian ---
    (r'portfolios-src/electron-beam/README\.md', "Project 07's source: every file, the chapter format, how a chapter plugs in, the commands and the checks.", 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/(\.gitignore|package\.json)', 'Keeps out/ and caches out of git; marks the .js files of this folder as CommonJS so Node can load them.', 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/contract\.json', 'The hand-over contract: every symbol with its SI unit, range and default, and the inputs and outputs of each stage.', 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/(build\.py|eb_lib\.py|guide_default\.py)', lambda m: {'build.py': 'Generates public/portfolios/electron-beam/index.html (--site) or a stand-alone page in out/.', 'eb_lib.py': 'Loads the chapters, numbers equations and figures, resolves references, computes every quoted number, typesets with KaTeX, validates the contract.', 'guide_default.py': 'The reading guide shown until text/guide.py exists.'}[m.group(1)], 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/template\.html', "The page template: house design, reading guide, contents list, chapter slots, simulation slots.", 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/app\.js', "The page's script: binds each simulation slot's sliders (contract symbols) to its physics module and draws it.", 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/bridge\.cjs', 'Runs the page JavaScript in Node for the build and the checks: module list, compute, constants, number format, KaTeX (the site vendor copy).', 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/physics/core\.js', 'Shared physics core: CODATA 2018 constants, unit helpers, number format, seeded random numbers; the pattern every chapter module follows.', 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/physics/ch(\d\d)\.js', lambda m: 'Chapter %d solver: a pure module that runs in the page and in Node.' % int(m.group(1)), 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/ref/(__init__|core)\.py', 'Python reference package: constants, units and number format mirroring physics/core.js.', 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/ref/ch(\d\d)\.py', lambda m: 'Chapter %d NumPy reference solver, mirrors physics/ch%s.js.' % (int(m.group(1)), m.group(1)), 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/text/ch(\d\d)\.py', lambda m: 'Words, figures and numbers of chapter %d (a dict CH).' % int(m.group(1)), 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/text/guide\.py', 'The reading guide for the reviewer.', 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/derive/.+', 'SymPy derivation script of a chapter; its output is shown on the page.', 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/sources/.+', 'Bibliography and provenance of the published data used by the chapters.', 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/data/.+', 'Published data digitised for an overlay, with its provenance.', 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/checks/(check_parity\.py|check_numbers\.py|check_page\.cjs|selftest\.py)', lambda m: {'check_parity.py': 'Check: each physics/chNN.js against ref/chNN.py on the same inputs, and the constants and number format.', 'check_numbers.py': 'Check: every number quoted in the text is computed, and no typed measurement is left in the prose.', 'check_page.cjs': 'Check: the built page in Chromium at 360, 390, 1024 and 1440 px (KaTeX, errors, scroll, requests, fonts, simulations), with screenshots.', 'selftest.py': 'Self-test of the scaffold: the build accepts a good chapter and refuses each broken one.'}[m.group(1)], 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/checks/check_figures\.cjs', 'Check: every SVG figure and simulation canvas of the built page at four widths and every slider end, for labels on labels, lines through labels, labels off the edge and text too small.', 'docs/portfolios.md'),
    (r'portfolios-src/electron-beam/figkit\.py', 'Layout kit of the inline SVG figures: label widths in the house fonts, a label placer that avoids what is drawn, a wide and a narrow drawing per figure.', 'docs/portfolios.md'),
    (r'portfolios-src/electron-beam/checks/fixtures/.+', 'Fixture chapter for the self-test (good, or broken in one way); not project text.', 'portfolios-src/electron-beam/README.md'),
    (r'public/portfolios/electron-beam/index\.html', 'Generated page of project 07: lecture notes in chapters with running simulations (portfolios-src/electron-beam/build.py --site).', 'docs/portfolios.md'),
    (r'public/portfolios/electron-beam/fig/.+', 'Plate of the Portfolios page entry of project 07.', 'docs/portfolios.md'),
    (r'notes/electron-beam/ch01/(check_thomson_vs_librarian\.py|contract-ch01\.patch)', lambda m: {'check_thomson_vs_librarian.py': "Chapter 1 session's cross-check of its Thomson 1897 transcription against the librarian's digitisation.", 'contract-ch01.patch': 'The contract change chapter 1 asked for (applied by the finisher).'}[m.group(1)], 'portfolios-src/electron-beam/README.md'),
    (r'notes/electron-beam/ch02/(.+)', lambda m: "Chapter 2 session's preview harness, written before the scaffold existed: " + m.group(1) + ' (superseded by build.py and checks/).', 'portfolios-src/electron-beam/README.md'),
    (r'notes/electron-beam/shots/(.+)\.png', lambda m: 'Screenshot of project 07 in Chromium: ' + m.group(1) + '.', 'portfolios-src/electron-beam/README.md'),
    (r'notes/electron-beam/tools/check_projects\.cjs', "The finisher's check of the Projects page entry of project 07 in English, German and Arabic at 390 and 1100 px.", 'portfolios-src/electron-beam/README.md'),
    (r'notes/electron-beam/tools/plates\.cjs', "The finisher's helper: captures the Projects-page plates of project 07 from the built page's own figures.", 'portfolios-src/electron-beam/README.md'),
    (r'notes/electron-beam/editing/stats\.py', "The editing team's sentence statistics of one chapter's prose (mean length, sentences over 30 and 40 words).", 'notes/electron-beam/editing/PLAN-TREE.md'),
    (r'notes/electron-beam/tools/shot\.cjs', "The finisher's helper: screenshot one element of the built project-07 page.", 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/checks/list_legacy_numerals\.py', 'Check: lists every numeral typed into the text of chapter 2 (written before the scaffold), for the audit.', 'portfolios-src/electron-beam/README.md'),
    (r'portfolios-src/electron-beam/physics/ch02_ui\.js', "Chapter 2's live figure in the browser: four canvases and the controls; reads physics/ch02.js and writes every number into its store.", 'portfolios-src/electron-beam/README.md'),
    (r'notes/electron-beam/(S1-report|requests|status)\.md', lambda m: {'S1-report': 'Report of the scaffold session S1: what exists, how chapters plug in, commands, what was verified.', 'requests': 'Requests from chapter sessions for a change in a shared file (template, core, contract).', 'status': 'Status of project 07.'}[m.group(1)], 'portfolios-src/electron-beam/README.md'),
    (r'notes/electron-beam/.+\.md', 'Working note of project 07.', 'portfolios-src/electron-beam/README.md'),
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
    ('public/data/', 'Computed data played back by the pages (named by date of generation)', None),
    ('public/styles/', 'Stylesheets', None),
    ('public/vendor/katex/', 'KaTeX', None), ('public/vendor/three/', 'three.js', None), ('public/fonts/lm/', 'Latin Modern', None),
    ('public/fonts/', 'IBM Plex, Instrument Serif, and the Arabic faces', None),
    ('public/data/', 'Stored simulation data (computed on Kaggle)', None),
    ('public/images/sims/', 'Thumbnails', None),
    ('public/images/fig11/', 'Figures of Double Pendulum under Control', None),
    ('public/images/', 'Logo', None),
    ('public/cv/', 'The CV page', None),
    ('public/portfolios/droplet-collection/', 'Project copy: Droplet Collection', None),
    ('public/portfolios/rotor-pendula/', 'Project copy: Rotor Pendula', None),
    ('public/portfolios/hydraulics/', 'Project copy: Hydraulic Press Study', None),
    ('public/portfolios/impact/', 'Iron, Cotton and the Head', None),
    ('public/portfolios/electron-beam/', 'Project 07: The Electron Beam, from Tip to Measurement', None),
    ('public/portfolios/pendulum-control/', 'Project: Double Pendulum under Control', None),
    ('portfolios-src/hydraulics/', 'Source of the Hydraulic Press Study (not served)', None),
    ('portfolios-src/rotor-pendula/', 'Source of Rotor Pendula (not served)', None),
    ('portfolios-src/impact/', 'Source of Iron, Cotton and the Head (not served)', None),
    ('portfolios-src/rotor-pendula/', 'Source of the Rotor Pendula notes (not served)', None),
    ('portfolios-src/droplets/', 'Source of the Droplet Collection study (not served)', None),
    ('portfolios-src/electron-beam/', 'Source of project 07, the electron beam (not served)', None),
    ('portfolios-src/', 'Shared by the portfolio sources (not served)', lambda p: p.startswith('portfolios-src/') and p.count('/') == 1),
    ('src/', 'Template sources', None),
    ('worker/', 'The site\u2019s Worker (Cloudflare)', None),
    ('docs/', 'Documentation', None), ('tools/', 'Tools', None),
    ('i18n/', 'Translation tables', None),
    ('.claude/agents/', 'Agents of the lecture-note review', None),
    ('notes/electron-beam/', 'Working notes of project 07, the electron beam', None), ('notes/rotor-pendula/', 'Working notes of the Rotor Pendula study', None), ('notes/droplets/', 'Working notes of the Droplet Collection study', None),
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

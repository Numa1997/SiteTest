# Performance: what was measured, what was slow, what changed

Numa, 31 October 2026, on his phone: the site "looked good, but sometimes when switching from one page to another, or clicking
this or that, it lags a bit". This page records the experiment: how the site was measured, what the measurements show, which
change was made for which measured cause, and the same measurement afterwards. One change at a time; nothing is changed because
it "should" be faster.

## How it is measured

Everything below was measured in headless Chromium (the one preinstalled in the work environment) with a phone's screen, 390 × 844 px
at 3× pixel density (Lighthouse's own mobile screen is 412 × 823 px at 1.75×), and Lighthouse's mobile processor and network: the
processor slowed 4× (`Emulation.setCPUThrottlingRate`) and "Slow 4G" (562.5 ms round trip, 1.51 Mbit/s down, 0.69 Mbit/s up). Where a change trades download time
against processor time, it is measured a second time on a faster "4G" network (85 ms round trip, 9.2 Mbit/s down), closer to a phone on a
good mobile connection. Each number is the median of three runs unless a table says otherwise; kB are 1000 bytes.

The scripts are in [`tools/perf/`](../tools/perf/); Playwright and Chromium must be installed.

| Script | What it measures |
|---|---|
| `measure.cjs <base> <out.json> <runs> <path>…` | A first visit with an empty cache, then a repeat visit: LCP, CLS, blocking time, the longest task, main-thread time, bytes over the network, and how busy the main thread is during 5 s in which the reader does nothing (main-thread time divided by the measured length of that window). |
| `interact.cjs <base> <out.json> <runs>` | What a reader does: home → simulations → Fig. 9 and back by links; Solve, the data panel, a fold, on Fig. 9; the three tabs of Rotor Pendula. Each interaction's duration comes from the browser's Event Timing API, which INP is built from. |
| `tabs.cjs <base> <path> <tabs> <runs>` | The study pages with tabs: the time from the start of navigation until the first tab's frame reports ready (it posts a message at the end of its body; its fonts finish 0.04 to 0.7 s later), each tab switch (click to that tab's ready message), a repeat visit. |
| `trace.cjs <url> [scrollY]` | What fills the main thread while a page sits idle (a 4 s trace and CPU profile), with the figure on screen or scrolled away. |
| `loadtrace.cjs <url>` | The long parse, layout and script pieces of a study page loading. |
| `margin.cjs <base> <CPU slowdown> <runs>` | How close a study tab comes to the shell's 8 s limit: from its frame's creation to its ready message. |
| `foldtap.cjs <base> <runs> <page>…` | A reader in a figure's lecture note: how busy the main thread is, and how long closing and opening a fold takes. |
| `clockcheck.cjs <base> <page>…` | Each figure runs on screen, holds off screen, resumes; the store stays live for an open data panel and the walkthrough. |
| `film.cjs <URL> <prefix>` | A repeat visit as a reader sees it: screenshots at 2.5, 3, 3.5, 4.5, 6 and 8 s, and every LCP candidate with its element and text, to tell a change in the metric from a change on the screen. |
| `addresses.cjs <base> <built folder>` | Every page at every form of its address (`x.html`, `x`, `x/`, `folder/`, `folder`), each answer followed to its end and compared byte for byte with the built page, and every link of every page; exits 1 on any wrong answer (change 6). |
| `serve.cjs <folder> <port>` | A local server that answers as Cloudflare does (below), so that a change can be measured before it is merged. |

The metrics, as [web.dev](https://web.dev/articles/vitals) defines them, with its thresholds for "good" at the 75th percentile of
page loads: **LCP** (Largest Contentful Paint), when the largest text block or image of the first screen is drawn, good within
2.5 s; **CLS** (Cumulative Layout Shift), how far the content jumps while it loads: for each shift the shifted area times the shift
distance, summed over the worst burst of shifts (each less than 1 s after the last, the burst at most 5 s long), good up to 0.1; **INP** (Interaction to Next Paint), the time from a tap to the next drawn frame, good up to 200 ms.
**Blocking time** adds up, over the main-thread tasks of a window, each task's part beyond its first 50 ms; it is the laboratory
stand-in for INP. Lighthouse's TBT takes the window from first paint to "time to interactive", which a page that never rests does
not reach, so the window is stated with each number here: `measure.cjs` reports it from first paint to the load event (and, as in
the baseline table, to 8 s after the load event); `tabs.cjs` from the start of navigation to 1.5 s after the first tab is ready.

Three limits of the method, each a reason to read the numbers as comparisons rather than as a phone's exact experience:

1. **Software drawing.** Headless Chromium draws canvases with the processor, not a graphics chip. On the canvas-heavy pages the
   drawing part of each frame ("Commit", "Paint", native time) is therefore larger than on a phone; the script part is not.
2. **HTTP/1.1.** From the work environment Chromium reaches the live site through a proxy that speaks HTTP/1.1 (`protocol`
   `http/1.1` in the network log), with at most six connections per site. Phones reach Cloudflare over HTTP/2 or HTTP/3, all
   requests on one connection. `serve.cjs` with `H2=1` serves HTTP/2 locally; browsers keep no cache for a site with a certificate
   error, so repeat visits are timed over plain HTTP.
3. **The live site's response headers**, which the local server copies (measured with `curl -sI`, 31 October 2026):
   Cloudflare sends every file with `Cache-Control: public, max-age=0, must-revalidate` (its documented default for static assets,
   [Cloudflare: headers](https://developers.cloudflare.com/workers/static-assets/headers/)); fonts carry an ETag, CSS and scripts a
   weak one when compressed, so a repeat visit asks for each and gets `304 Not Modified`; **HTML pages carry no ETag and no
   Last-Modified at all**, so a repeat visit downloads every page again in full. `serve.cjs` copies this (it gives every non-HTML
   file a weak ETag, which behaves the same for a browser), but its Brotli compresses about 5 % better than Cloudflare's
   (Rotor Pendula 848 kB against 896 kB live), on both sides of a comparison alike. A link to `x.html` is answered `307` with the address `x` (Cloudflare's
   default `html_handling`, ["auto-trailing-slash"](https://developers.cloudflare.com/workers/static-assets/routing/advanced/html-handling/)).

## The live site before any change (31 October 2026)

First visit, Slow 4G, CPU 4×, median of three runs (`measure.cjs https://phyeinusul.com … 3`). "Blocking" is the blocking time from
first paint to 8 s after the load event (the window of this first run; on a page that never rests it grows with the window: Fig. 9
gives 5.0 s up to the load event, 10.4 s up to 8 s after it). "Busy while idle" is the share of 5 s, after the page has loaded, in
which the main thread works although the reader does nothing (this run divided by 5 s; the figures marked 100 % were 99.5 to
101 %). "Redirect" is the 307 answer to the `.html` address every link on the site uses.

| Page | LCP | CLS | Blocking | Longest task | Busy while idle | Redirect |
|---|---|---|---|---|---|---|
| `/` | 3.45 s | 0.005 | 0.21 s | 0.25 s | 43 % | 0 ms |
| `/simulations.html` | 2.85 s | **0.280** | 0.66 s | 0.36 s | 0 % | 618 ms |
| `/simulations/driven-oscillator.html` (Fig. 9) | 4.20 s | 0.005 | **10.74 s** | 1.25 s | **100 %** | 626 ms |
| `/simulations/wind-turbine.html` (Fig. 10) | 4.13 s | 0.004 | **4.54 s** | 0.79 s | **100 %** | 624 ms |
| `/simulations/water-wave.html` | 4.18 s | 0.005 | 2.25 s | 0.97 s | 99 % | 619 ms |
| `/simulations/Double Pendulum.html` | 4.27 s | 0.004 | 3.13 s | 1.34 s | 100 % | 625 ms |
| `/portfolios.html` | 3.60 s | 0.040 | 0.12 s | 0.22 s | 0 % | 626 ms |
| `/portfolios/rotor-pendula/index.html` | (2.26 s)¹ | 0.000 | 2.96 s | **2.18 s** | 0 % | 831 ms |
| `/portfolios/hydraulics/index.html#servo` | (2.06 s)¹ | **0.209** | 1.38 s | 0.37 s | 3 % | 634 ms |
| `/portfolios/droplet-collection/index.html` | 2.32 s | 0.002 | 0.65 s | 0.42 s | 0 % | 626 ms |
| `/portfolios/impact/index.html` | 4.68 s | **0.862** | **6.31 s** | 1.44 s | **100 %** | 618 ms |
| `/de/simulations.html` | 3.97 s | **0.290** | 0.40 s | 0.28 s | 0 % | 622 ms |
| `/ar/index.html` | 5.19 s | 0.020 | 0.39 s | 0.23 s | 39 % | 619 ms |

The CLS column of this first run adds every shift of the load; by web.dev's worst-burst rule (which `measure.cjs` now uses) the
simulations list gives 0.261 instead of 0.278 and Iron, Cotton and the Head 0.826 instead of 0.862: the same conclusion.

¹ The study pages draw their content inside frames, which the page's LCP does not see; the time until the first tab is drawn is
measured by `tabs.cjs` (below). No page scrolls sideways at 390 px. On every page the only console error is Cloudflare's Web
Analytics beacon (`static.cloudflareinsights.com/beacon.min.js`), which Cloudflare inserts and the site's security policy blocks;
it is a setting in the Cloudflare dashboard, not in this repository.

Interactions on the live site, Slow 4G, CPU 4×, one run (`interact.cjs https://phyeinusul.com … 1`): on Fig. 9, Solve took
800 ms to the next frame, opening the data panel 888 ms, closing it 464 ms, closing a fold of the lecture note 400 ms and opening
it again 608 ms; all above the 200 ms of a good INP.

## What the measurements say is slow, and why

**1. Simulation pages that never rest.** On Figs. 9 and 10, the water wave and the double pendulum, the main thread is busy
99 to 100 % of the time while the reader does nothing, and every tap waits for the frame in progress: this is the "clicking lags"
(Fig. 9's interactions above). A trace of Fig. 9 (`trace.cjs`) shows why: every frame redraws all five canvases (the mechanism,
the time window, the whole-run overview, the force profile and the phase portrait), and `label()`
(`public/simulations/driven-oscillator.html:1107`) measures text in every frame, which forces a full layout of the page each
time. The same 4 s trace with the figure scrolled 6000 px away, into the lecture note, shows the same work, frame for frame: the
clock of `Sim.clock` (`public/scripts/sim.js:176`) runs and draws whether or not the figure is on screen (the hero pendulum of
the home page, by contrast, already stops when it is out of view, `index.html:783`). Part of the per-frame cost is software
drawing (limit 1 above); the script part, about 34 ms per frame at 4× slowdown, and the work done off screen are real on a phone.
Fig. 9's Solve integrates the whole run in one task on the main thread (1.25 s at 4×).
*Changed for the work done off screen: see change 3. The per-frame cost on screen and Solve are not changed.*

**2. Fonts sent again inside the study pages.** Rotor Pendula and the Hydraulic Press Study (English, German, Arabic) each carry
59 fonts as base64 `data:` addresses, about 440 kB of fonts per tab, three tabs per page: 1.3 MB of text that compresses badly. Every
one of those fonts is byte-identical (by MD5) to a file the site already serves from `public/fonts/` or
`public/vendor/katex/fonts/`. Compressed, the fonts are about two thirds of each page (with Brotli, as `serve.cjs` compresses it: Rotor Pendula 848 kB with
them, 292 kB without; Hydraulic Press Study 551 and 196 kB; Cloudflare sends Rotor Pendula as 897 kB today), and since Cloudflare sends HTML without an ETag, a reader downloads them again on every visit.
*Changed: see change 1.*

**3. Every click pays a redirect.** Every internal link is written `….html` (so that the GitHub Pages copy and local files work),
and Cloudflare answers each with a 307 to the address without `.html`: one round trip lost before the page starts to load, 620 ms
on Slow 4G (measured); on a phone on 4G one round trip, typically 0.05 to 0.2 s (an estimate, not measured here). *Not changed: the fix is a Cloudflare setting; see "Not changed" below.*

**4. Content that jumps.** The simulations list (CLS 0.28 in English, 0.29 in German), the Hydraulic Press Study (0.21) and
Iron, Cotton and the Head (0.86) move their content while loading, beyond the 0.1 of a good page. *Changed for the simulations list (change 4) and Iron, Cotton and the Head (change 5); the
Hydraulic Press Study's tab bar is not changed.*

**5. Repeat visits gain little.** With `max-age=0`, a repeat visit re-asks for every stylesheet, script and font (15 to 39
requests per page), and the simulations list takes 2.92 s on a repeat visit against 2.85 s on the first. *Changed for the font files: see change 2.*

## Change 1: the study pages link the site's fonts instead of carrying them (31 October 2026)

**What.** In `--site` mode only, `portfolios-src/rotor-pendula/tools/build_combined.py` and
`portfolios-src/hydraulics/tools/build_combined.py` pass each embedded page through `link_fonts()` of
[`portfolios-src/site_fonts.py`](../portfolios-src/site_fonts.py): every `url(data:font/woff2;base64,…)` becomes `url(../../…)`, the
byte-identical file the site serves (KaTeX's from `vendor/katex/fonts/`, the rest from `fonts/`). The German and Arabic pages of
the Hydraulic Press Study follow, because `tools/i18n/hydraulics.py` runs the same builder. The studies' sources and their
standalone builds are unchanged and still carry their fonts. A font the site does not serve stops the build.

**Why it works.** A frame created with `srcdoc` resolves relative addresses against its parent page, so `../../fonts/…` from
`portfolios/<study>/index.html` reaches `fonts/…`; the Arabic pages of the study already loaded their Arabic fonts that way. The
browser then fetches each font file once, in parallel, and keeps it in its cache for all three tabs and every later page, instead of
receiving the same 1.3 MB of base64 text inside the page on every visit.

**A guard that came with it.** The shell of each study page gave a tab 8 s to report ready, and otherwise replaced its frame by
one loaded from a `blob:` address (for hosts that refuse `srcdoc` frames). On the site that replacement can never load: the page's
security policy admits frames only from the site (`default-src 'self'`; the browser reports "Framing 'blob:…' violates … default-src
'self'"). So a tab that was still waiting on the network 8 s after its frame was made (a script or stylesheet it loads) was thrown
away and left blank (`chrome-error://`), on `main` too; a tab still busy parsing at 8 s also holds up the timer, which then runs after
the tab is ready, so that case was spared. How close the tabs come to the limit, from the frame's creation to its ready message, on
Slow 4G with the processor slowed 6× (`node tools/perf/margin.cjs <base> 6 2`), three measurers, two runs each:

| Tab | `main` | this change |
|---|---|---|
| Rotor Pendula, notes | 6.35, 6.93 / 9.25, 9.26 / 7.78, 6.23 s | 7.47, 6.25 / 7.66, 9.64 / 7.14, 7.25 s |
| Hydraulic Press Study, servo | 4.79, 5.31 / 7.32, 6.10 / 6.74, 6.47 s | 5.36, 5.67 / 7.57, 7.56 / 5.78, 6.60 s |

No systematic change between the versions, but in both the long tabs come within about a second of the limit and sometimes over
it. The shell now replaces a frame only when the host refused its `srcdoc` (its document never became `about:srcdoc`); a frame that
is merely slow is left to finish. This needs the shell to be able to read its frame, as on the site; a host that sandboxes the page
without `allow-same-origin` hides the frame's document, and there the old 8 s replacement still applies. Tested with
`scripts/sim.js` held back 11 s: on `main` the simulation tab ends blank; now it appears and runs (26 canvases drawn); a refused
`srcdoc` still triggers the replacement as before. (Since then the rule is the other way round, and narrower: the shell replaces a
frame only while it is still empty, `about:blank` or unreadable, so a frame that has navigated is not blanked either; see "Faults
found outside performance" below.)

**Proof that nothing else changed.** For each of the four pages, every tab is identical character for character once each font,
embedded or linked, is replaced by the MD5 of its bytes (59 fonts per page, 21 distinct files); the shell differs only by the
guard above. Screenshots of every tab at 390 and 1440 px, before and after, once the fonts have loaded: the same font faces loaded,
identical text and layout, no console errors, no sideways scroll; the only differing pixels are the moving parts (the oil dots of
the ideal press, the running simulation and wind, the edge of the tab pill at the moment of the screenshot), which differ by as much
between two loads of the old page. Checks run on the new pages: Rotor Pendula `check_combined.py` (all pass: 1450 formulas, 0 KaTeX
errors, the simulation solves, the wind runs, tabs and deep links, 360 to 1440 px), `check_numbers.py`, `check_sim.js`,
`check_wind.js`, `check_newton.js`, `check_physics.py`, `R_revision.py` (all pass); Hydraulic Press Study `check_combined.py` on the
English page (33 of 33; the check then found frames by their English titles, so it could not run on `de.html` and `ar.html`; it
can since, see "Faults found outside performance"), `check_theory_numbers.js` (52 of 52), `check_physics.py`, `check_control.py`, and the data-panel check
`check_data_panel.cjs` for both presses at 390 and 1440 px (the pointer sweep paints nothing, pins, a Check "stored and recomputed
identical", one round recorded, no errors).

**Measured**, the old and the new pages each served by `serve.cjs` (Brotli, no ETag on HTML, as Cloudflare). Commands:
`node tools/perf/serve.cjs <dist> <port>` (with `H2=1` for HTTP/2), then
`NET=4g node tools/perf/tabs.cjs <base> /portfolios/rotor-pendula/ notes,sim,wind 3` and
`… /portfolios/hydraulics/ servo,ideal,theory 3` (without `NET=4g` for Slow 4G). "First tab" is the time from the start of
navigation until the first tab (notes, servo) reports ready. Up to three measurers, three runs each: the first in this session; the others two
independent reviews, which alternated old and new runs so that other work on the machine hit both alike. Both used the version of
`tabs.cjs` of that day, which noticed the ready message by polling every 50 ms and so read it 0.2 to 1.5 s late (most on the long
notes), on the old and the new page alike; the differences stand, the absolute times are that much too long. `tabs.cjs` now reads
the frame's own time of the message.

| | Rotor Pendula, before → after | Hydraulic Press Study, before → after | Reproduced? |
|---|---|---|---|
| The page, Brotli | 848 → **292 kB** | 551 → **196 kB** | yes, exactly |
| First visit, 4G, HTTP/2: bytes | 916 → **562 kB** | 702 → **502 kB** | yes, exactly (over HTTP/1.1: 918 → 573 and 707 → 514 kB) |
| Repeat visit, 4G, HTTP/1.1: bytes | 851 → **304 kB** | 557 → **210 kB** | yes, exactly |
| First visit, Slow 4G, HTTP/2: first tab (three measurers) | 11.13 → **9.07** / 12.08 → **9.73** / 11.49 → **10.07 s** | 7.98 → **6.51** / 8.87 → **7.59** / 8.67 → **7.29 s** | yes, in every pair of runs; 1.4 to 2.4 s sooner |
| First visit, 4G, HTTP/2: first tab | 7.29 → 6.28 s / 6.87 → 6.66 s | 4.38 → 4.30 s / 4.19 → 3.49 s | no clear change: within the run-to-run spread |
| Repeat visit, 4G, HTTP/1.1: first tab | 6.59 → 6.40 s / 6.31 → 6.43 s | 4.75 → 3.49 s / 3.77 → 3.95 s | no clear change |
| Blocking time, 4G | 1.84 → 1.41 s / 3.28 → 3.17 s | 1.46 → 1.38 s / 1.38 → 1.34 s | no clear change |

So the change is a clear gain in what crosses the network (the page itself two thirds smaller; a first visit 28 to 39 % fewer bytes,
a repeat visit 62 to 64 % fewer),
and in time on a slow network, where the bytes dominate; on a good 4G network the time to the first tab does not change measurably.
One cost, measured and kept in view: with linked fonts the notes are laid out once with the fallback font and again when the fonts
arrive (a second full layout of about 0.9 to 1.2 s at 4× on Rotor Pendula's notes, `loadtrace.cjs`); with embedded fonts the fonts
were there at the first layout. The longest single task varies widely between runs in both versions (0.5 to 3.6 s across both
measurers), so it is reported, not counted as a gain or a loss. Preloading the fonts from the page's shell (`<link rel="preload" as="font" crossorigin>`) was
tried and dropped: the frames do not reuse the shell's preloads, so fonts were fetched twice (over HTTP/2 755 instead of 562 kB; over
HTTP/1.1, with a cache, 670 instead of 573 kB).

**Review.** Before merging, two rounds of three independent reviewers checked the change: what the reader gets in a browser, the
measurements and this page's claims, and the code. Round 1 found: the local server served files outside its folder and stopped on a
malformed address; the tab-switch times measured only the click; the 8 s replacement above; blocking-time windows not stated and
"busy while idle" over a nominal 5 s; a font embedded in another form passing silently; the 4G timing gains first claimed did not
reproduce; units, line numbers, the "three quarters" (two thirds with Brotli) and stale descriptions in `docs/` and
`tools/inventory.py`. Round 2 found: `docs/files.md` not regenerated after the last builder edit; the server could still be stopped
by one hand-made request, followed links out of its folder and served `/_headers`; the tab times read the ready message by polling,
up to 1.5 s late; CLS summed every shift; the revalidation counter always read 0; the guard's numbers had no command and its
explanation was too broad; units and labels. All of these were fixed or corrected in the text above. Found and left alone, because
they are older than this change and are not about speed: a contents link tapped in a long tab before its link script has run (the
script sits at the end of the tab) loads the whole study page inside the tab, which the 8 s replacement then blanks, on `main` as
well; the tab frames' accessible names read doubled ("SimulationSimulation"), because the shell takes both the long and the short
label. Both are fixed since; see "Faults found outside performance".

**On the live site** (merged 31 October 2026 as `87b3357`; Cloudflare served the new pages about 80 s later, byte-identical to the
build, checked by SHA-256 for the four changed pages, three unchanged pages and two font files; `measure.cjs
https://phyeinusul.com … 3`, Slow 4G, CPU 4×; before: the run of the same morning):

| Live | Rotor Pendula, before → after | Hydraulic Press Study, before → after |
|---|---|---|
| First visit, bytes | 1145 → **663 kB** | 779 → **588 kB** |
| Repeat visit, bytes | 1077 → **394 kB** | 621 → **277 kB** |

Cloudflare compresses the page less than `serve.cjs` (Rotor Pendula's page 375 kB live against 292 kB locally). No new console
error: the only one is still the analytics beacon.

## Change 2: font files kept for a year (31 October 2026)

**What.** One rule in [`public/_headers`](../public/_headers): every `*.woff2` is sent with `Cache-Control: public, max-age=31536000,
immutable`. Pages, stylesheets and scripts keep Cloudflare's default (`max-age=0, must-revalidate`).

**Why it works.** With `max-age=0` a browser keeps a copy of each file but asks the server before every use ("still the same?",
answered `304`): one round trip each, and the fonts are needed before the text can be drawn. A font file never changes under its
name (the fonts here have changed once in the repository's history, on 24 October, as new files), so the browser may use its copy
without asking ([web.dev: HTTP cache](https://web.dev/articles/http-cache): `max-age=31536000` for files whose content never
changes, `immutable` to skip revalidation; [Cloudflare: headers](https://developers.cloudflare.com/workers/static-assets/headers/):
a `_headers` rule overrides the default, `/*.jpg` is its own example of a pattern by file type). A changed stylesheet or page still
reaches readers at once. The one rule to keep: a font whose bytes change must get a new file name.

**Measured**, repeat visits (the same browser, its cache kept) on `serve.cjs`, which applies `_headers` as Cloudflare does; HTTP/1.1;
first visits unchanged:

| Repeat visit | Files asked again, before → after | LCP, 4G (median of 3) | LCP, Slow 4G (two runs of 2) |
|---|---|---|---|
| Home | 13 → 7 | 0.65 → 0.58 s | 2.73, 2.66 → **2.02, 1.98 s** |
| Simulations list | 24 → 13 | 0.59 → 0.60 s | 2.51, 2.54 → 2.50, 2.51 s |
| Fig. 9 | 36 → 18 | 0.99 → **0.72 s** | 3.39, 3.32 → **2.64, 2.65 s** |
| Portfolios | 26 → 15 | 0.79 → 0.82 s | |
| Rotor Pendula | 18 → 1 | 0.42 → 0.41 s | |
| Hydraulic Press Study | 21 → 6 | 0.72 → **0.52 s** | |

Where the fonts lie on the path to the first drawing (home, Fig. 9, the Hydraulic Press Study) a repeat visit is drawn 0.2 to 0.7 s
sooner; elsewhere the time does not change measurably, but half the round trips are gone.

**On the live site** (merged as `f92733a`; Cloudflare sent the new header about 40 s later: `curl -sI` shows
`cache-control: public, max-age=31536000, immutable` on every `*.woff2` tried, the security headers still on them, and the default on
pages, stylesheets and scripts). Repeat visits, Slow 4G, CPU 4×, median of 3 (`measure.cjs https://phyeinusul.com … 3`; before: the
morning's baseline): home 3.04 → **2.19 s**, Fig. 9 3.85 → **3.08 s**; files asked again 7 of 15 and 18 of 39.

## Change 3: a figure rests while nothing shows it (31 October 2026)

**What.** `public/scripts/sim.js`, which every simulation page shares:

- `Sim.clock` no longer calls the page's frame function while nothing that shows the run is on screen: neither the figure
  (`.sim__head`, `.sim__grid`) nor the walkthrough with its live values (`#walk`), watched by an IntersectionObserver with a 200 px
  margin, and the data panel neither open nor recording. While held it asks the browser for no frames; a timer looks again every
  200 ms. The simulation's time stands still, as it already did in a hidden tab, and the first frame after the hold starts with
  `dt = 0`, so the run goes on from the same instant.
- The walkthrough's "Now" column, looked at every 200 ms, rewrites a cell only when its text changes, and nothing while it is out of
  view: rewriting the same text made the browser lay the whole page out again, 5 times a second.

Every existing line of `sim.js` keeps its number (the new helper sits at the end of the file), so the 310 citations of `sim.js` in
`docs/` stay true.

**Why it works.** A tap is answered only when the main thread is free. A running figure fills each frame with drawing; in the lecture
note the reader does not see that drawing, but every tap there (a fold, a link) waited for it. An IntersectionObserver tells the page
which parts are on screen without measuring the layout itself.

**What does not change.** No physics and no number: while held, `tick` is not called at all, so the store holds the last frame, whole
and consistent with the picture last drawn. The data panel open, or a round being recorded, keeps the clock running, so the panel's
live table, Record, Check and Read values work as before; so does the walkthrough when it is on screen.

**Measured** (`serve.cjs`, CPU 4×; the busy share over 3 s with the reader in the middle of the lecture note; each tap's Event
Timing duration, median of 3; `node tools/perf/foldtap.cjs <base> 3 <page>…`):

| Page | Main thread busy while reading the note | Close a fold in the note | Open it again |
|---|---|---|---|
| Fig. 9, driven oscillator | 56 → **1 %** | 320 → **176 ms** | 344 → **208 ms** |
| Fig. 10, wind turbine | 100 → **1 %** | 296 → **216 ms** | 240 → **184 ms** |
| Water wave | 57 → **1 %** | 144 → 152 ms | 136 → 144 ms |
| Double pendulum | 88 → **2 %** | 224 → **176 ms** | 240 → **184 ms** |

A 4 s trace of Fig. 9 scrolled 6000 px into the note: before, about 4 s of work (drawing, compositing, script); after, 74 ms of script
and the rest idle. With the figure on screen nothing changes (the same work, frame for frame). What remains of a fold tap, about 150
to 210 ms at 4×, is the fold itself laying out a long page.

**Checked.** On all eleven figures, and German and Arabic pages, before and after (`node tools/perf/clockcheck.cjs <base> <page>…`): the figure runs at the top of the
page; while the reader is in the note the store holds (before: it kept changing); with the data panel opened there, the store keeps
changing (as before); the walkthrough's values move when it is on screen; the figure resumes when the reader scrolls back; no console
errors. `notes/verify.mjs` (the eleven pages at 1440, 1600 and 390 px) and `notes/walkcheck.cjs` give the same result as on `main`.

**Review.** An independent reviewer found one defect before the merge: on four figures (water wave, transverse and longitudinal
waves, phasor sums, double pendulum) the page's resize handler refits the canvas, which clears it, and leaves the drawing to the next
tick; a page opened deep in its note (`#p-limits`) is refitted just after the clock has held, so the figure stayed blank, also when
printed. Fixed: after every refit by `Sim.onResize`, and before printing, a held clock runs for one second, resumed at once. Tested:
48 loads opened at `#p-limits` (six pages including German and Arabic, 390 and 1280 px, four runs each), none blank; before the fix
all four pages were blank at both widths. On screens 1500 px and wider the data panel opens beside the page by default, so the clock
keeps running there until the reader closes the panel: by design, the panel shows the live run.

## Change 4: the simulations list no longer pushes the page down (31 October 2026)

**What was measured.** The browser's layout-shift entries (which elements moved, when, how far) on the simulations list, Slow 4G,
CPU 4×: the section below the list ("anatomy") was painted at the first paint, about 2.7 s, and pushed 604 px down at 4.4 to 5.6 s,
when the list of eleven cards appeared above it. The list is drawn by the page's own script at the end of the page, after
`scripts/fold.js` and `scripts/catalog.js` arrive; on a slow network they arrive after the stylesheets and fonts, so after the
first paint. Two fixes were tried and measured first and dropped, because they did not help: loading KaTeX deferred (the list
appeared about 0.7 s sooner, but still after the first paint: CLS unchanged), and preloading the two scripts from the head (the list
then appeared just after the first paint, CLS 0.32, worse).

**What.** Until the list has been drawn the first time, what follows it waits: two rules at the end of
[`public/styles/catalog.css`](../public/styles/catalog.css) hide the siblings after `.cat__list` and the page's footer while the
document lacks the class `cat-drawn`; the page adds that class right after its first drawing (`simulations.html:349`), or after 8 s
in any case (`simulations.html:25`), so a failing script cannot hide them for good; without JavaScript nothing waits. The German and
Arabic pages and `catalog.rtl.css` follow from `tools/i18n/build.py`. The Portfolios page shares `catalog.css` and has no list; the
footer rule is limited to a page with `#catalog`.

**Why it works.** A layout shift is counted when something already on screen moves. If the section below the list is not yet on
screen when the list arrives, the list takes its place and the section appears below it: nothing moves.

**Measured** (`measure.cjs`, `serve.cjs`, Slow 4G, CPU 4×, median of 3; CLS by web.dev's worst-burst rule):

| Page | CLS, before → after | LCP, before → after |
|---|---|---|
| Simulations list | 0.261 → **0.004** | 2.67 → 2.66 s |
| German | 0.278 → **0.004** | 3.68 → 3.66 s |
| Arabic | 0.537 → **0.139** | 3.76 → 3.74 s |
| Portfolios (shares the stylesheet) | 0.026 → 0.026 | 3.30 → 3.36 s |

What is left on the Arabic page is another shift: the top bar grows when its Arabic font arrives (0.13 at 5.8 s), not the list. The
finished page is pixel-identical before and after (screenshots at 390 and 1440 px, English, German, Arabic, a search with no
results, whose message still shows, and a field filter once settled).

## Change 5: Iron, Cotton and the Head stands still while it loads (31 October 2026)

**What was measured.** The layout-shift entries (Slow 4G, CPU 4×): at about 4.2 s the cards moved 444 to 492 px and the figure's
caption left the screen, when the page script ran. Every word of the page waited for it: the template leaves the headings,
paragraphs and the derivations empty (`data-t="…"`, `#sections`) and the script fills them from the text table built into the page.
Then the figure (a canvas of 300 × 150 px until the script sizes it to 644 or 684 px) and the title (it rewraps when Instrument Serif
replaces the fallback serif) moved the page again.

**What.** In [`portfolios-src/impact/build.py`](../portfolios-src/impact/build.py): the build writes each text into its element (the
script still writes the same text at load); the site pages ask for `instrument-serif-400-latin.woff2` with a preload. In
[`template.html`](../portfolios-src/impact/template.html): the figure's height is reserved in CSS, 644 px or, from 640 px of stage
width (a container query, the script's own rule), 684 px. The pages are regenerated, never edited by hand.

**Measured** (`measure.cjs`, Slow 4G, CPU 4×, median of 3):

| Page | CLS, before → after | LCP, before → after |
|---|---|---|
| English | 0.826 → **0.029** | 4.14 → **2.15 s** |
| German | 0.822 → **0.029** | 5.19 → **2.61 s** |
| Arabic | 0.826 → **0.063** | 5.26 → **2.78 s** |

(LCP improves because the largest text block is in the page at once instead of after the script.) The finished pages: text identical character for character, and pixel-identical at 390 and 1440 px with
the canvases and the live progress line hidden. The study's checks: `checks/site_check.cjs` (fonts, no errors, no outside requests,
peak forces 638.6 N and 188.0 N, weights 9.81 N, English and Arabic at 1100 and 390 px) and `checks/data_panel.cjs` (every Check
"stored and recomputed identical", English and Arabic, 390 and 1100 px) pass; both hard-code a browser path that no longer exists
(`chromium_headless_shell-1194`), so they were run from copies with that one argument removed. (The path is gone from them since;
see "Faults found outside performance".)

**Measured and not changed.** The drop is computed in chunks on the main thread when the page opens: 95 s at full speed, longer on a
phone. A tap during it is answered in 56 ms (40 ms after), because each chunk yields; the page's frame loop also redraws every frame.
Neither makes taps lag; moving the computation to a worker would be a restructure of the study, which the measurements do not call for.

## The live site after all five changes (31 October 2026)

The same thirteen pages as the first run, after the five merges (`main` at `c714829`), at 18:00 (`measure.cjs https://phyeinusul.com
… 3`, Slow 4G, CPU 4×, median of 3). So that both columns use one rule, CLS is the sum of every shift and blocking time runs from
first paint to 8 s after the load event, as in the first run.

| Page | LCP, first visit | CLS | Blocking | LCP, repeat visit | Sent, repeat visit |
|---|---|---|---|---|---|
| `/` | 3.45 → 3.37 s | 0.005 → 0.005 | 0.21 → 0.16 s | 3.04 → **2.20 s** | 27 → 20 kB |
| `/simulations.html` | 2.85 → 2.85 s | 0.280 → **0.004** | 0.66 → 0.56 s | 2.92 → 2.94 s | 33 → 22 kB |
| `/simulations/driven-oscillator.html` (Fig. 9) | 4.20 → 4.12 s | 0.005 → 0.005 | 10.74 → 11.19 s | 3.85 → **3.14 s** | 130 → 111 kB |
| `/simulations/wind-turbine.html` (Fig. 10) | 4.13 → 4.19 s | 0.004 → 0.004 | 4.54 → 5.33 s | 3.91 → **3.27 s** | 91 → 77 kB |
| `/simulations/water-wave.html` | 4.18 → 4.16 s | 0.005 → 0.005 | 2.25 → 2.62 s | 4.04 → 7.82 s³ | 82 → 68 kB |
| `/simulations/Double Pendulum.html` | 4.27 → 4.19 s | 0.004 → 0.004 | 3.13 → 3.61 s | 3.85 → **3.38 s** | 68 → 58 kB |
| `/portfolios.html` | 3.60 → 3.56 s | 0.040 → 0.040 | 0.12 → 0.17 s | 3.63 → 3.64 s | 40 → 28 kB |
| `/portfolios/rotor-pendula/index.html` | (2.26 → 2.05 s)¹ | 0.000 → 0.000 | 2.96 → 2.96 s | (2.25 → 2.19 s)¹ | 1077 → **376 kB**² |
| `/portfolios/hydraulics/index.html#servo` | (2.06 → 2.00 s)¹ | 0.209 → 0.209 | 1.38 → 1.76 s | (2.04 → 1.99 s)¹ | 621 → **261 kB**² |
| `/portfolios/droplet-collection/index.html` | 2.32 → 2.36 s | 0.002 → 0.002 | 0.65 → 0.70 s | 2.36 → 2.38 s | 276 → 268 kB |
| `/portfolios/impact/index.html` | 4.68 → **2.28 s** | 0.862 → **0.029** | 6.31 → 6.33 s | 4.44 → **2.48 s** | 58 → 52 kB |
| `/de/simulations.html` | 3.97 → 3.96 s | 0.290 → **0.004** | 0.40 → 0.47 s | 3.52 → 3.55 s | 34 → 23 kB |
| `/ar/index.html` | 5.19 → 5.22 s | 0.020 → 0.020 | 0.39 → 0.54 s | 4.32 → 4.08 s | 33 → 24 kB |

¹ The page's own LCP; the study draws inside frames, timed by `tabs.cjs` (change 1). ² The first run counted the fonts carried
inside these pages as sent bytes; the corrected numbers of the same morning are those of change 1 (first visit 1145 → 661 kB and
779 → 587 kB in this run). On every page the only console error is still the analytics beacon; none scrolls sideways.

**What moved.** The layout shifts of the simulations lists and of Iron, Cotton and the Head are gone (changes 4 and 5); that study's
text appears 2.4 s sooner on a first visit (change 5). On a repeat visit six pages show their largest text 0.2 to 2.0 s sooner, and
every page but the droplet study (3 %) sends 10 to 35 % fewer bytes, because the fonts no longer ask the server again (change 2); the two study pages send 65 %
and 58 % less (change 1). **What did not.** First-visit LCP elsewhere moved by at most 0.2 s, within the spread of three runs.
Blocking time moved by −24 % to +39 %, and by as much on pages none of the changes touched (`/portfolios.html` +38 %,
`/ar/index.html` +39 %): this is the difference between a morning and an evening run on the measuring machine, not an effect of the
changes. On the figures, change 3 does not act in this window, because the figure is on screen; its effect is in its own section.

³ **Water waves, repeat visit: the metric moved, the screen did not.** The 7.82 s repeated (7.88 s in a second live run), and a
local before-and-after reproduced it: 3.3 to 3.4 s up to `87b3357`, 6.8 s from `f92733a` (change 2, fonts kept for a year), so
change 2 causes it. What a reader sees is the same or earlier (`film.cjs`, local, before and after change 2): with the fonts in the
cache, the title and lede are drawn in their final faces at 2.5 s, where before they were still in the fallback face; from 3 s on the
two films match, and the figure appears between 4.5 and 6 s in both. What changed is which element the browser names: before, the
lede (25 418 px²) was reported at 3.26 s; after, it is never reported, so LCP falls back to the figure's caption, which is drawn
again when its formula is typeset at the end of the load (6.8 to 9.1 s; sometimes at 3.2 s, so the median flips between runs). The
heading block fades in from transparent (`animation: rise`, `styles/sim.css` line 57), and with the font already there the lede is
drawn only during that fade. Why Chromium then never reports it is not established here; the films are the evidence that the reader
waits no longer. Change 2 is kept.

## Change 6: no redirect on a click (31 October 2026, Numa's decision)

**What was measured.** Every link of the site names the `.html` file, and Cloudflare answered each with a 307 to the address
without it: 620 ms per click on Slow 4G, before the page itself was asked for (cause 3; the "Redirect" column of the first run).

**What.** `wrangler.jsonc` sets `"html_handling": "none"`, so Cloudflare serves `x.html` and `folder/index.html` as they are
(its documentation, read 31 October 2026: <https://developers.cloudflare.com/workers/static-assets/routing/advanced/html-handling/>).
With `none` Cloudflare no longer finds a page at its short address (`/simulations`, `/`, `/ar/`), which readers saw and shared
from 20 to 31 October; [`public/_redirects`](../public/_redirects), written by [`tools/redirects.py`](../tools/redirects.py),
serves each page there with a 200 rule (Cloudflare's "proxying",
<https://developers.cloudflare.com/workers/static-assets/redirects/>), and sends `folder` on to `folder/` and `x/` to `x` with a
307, as before: 101 rules of the 2,000 allowed. Two lines of the scripts read the address and would have changed: the key under
which `fold.js` and the data panel remember a reader's folded sections ([fold.js:61](../public/scripts/fold.js#L61),
[datalog.js:264](../public/scripts/datalog.js#L264), [770](../public/scripts/datalog.js#L770)), and the page name and address
written into a saved data file ([datalog.js:1278](../public/scripts/datalog.js#L1278),
[1293](../public/scripts/datalog.js#L1293)). Each now drops a final `.html` (and `/index.html`), so it reads as on
phyeinusul.com before: no reader loses a stored choice, and a saved file names the page as before.

**Why it works.** A click asked twice (the `.html` address, answered "go to `x`"; then `x`); now it asks once.

**Checked before the merge,** on a local server that follows Cloudflare's two documentation pages (its answers for today's
setting matched the live site on 15 of 16 addresses; the miss, a page that does not exist, answers 404 live and redirects first
locally): `node tools/perf/addresses.cjs <base> <built folder>` asks for each of the 51 pages at every form of its address
(`x.html`, `x`, `x/`; `folder/index.html`, `folder/`, `folder`), 152 addresses, and opens every page in Chromium. With the change:
152 of 152 answer the right page, byte for byte, with the security headers; no page has a failed request or a script error;
all 53 links reach their page with no redirect (today 50 of the site's links pass through one). Folding a section at
`/simulations/water-wave.html` and reopening `/simulations/water-wave` finds it folded, under the key the live site used before
(`fold:/simulations/water-wave`); the same for the catalog and the Arabic home page.

**The live site before the merge** (the same check, `https://phyeinusul.com`): 152 of 152 addresses right, 51 of them through a
redirect when asked at `.html`; 95 links, 50 of them through a redirect. The redirect's time (`measure.cjs`, navigation timing):
625 ms on Slow 4G, 141 to 164 ms on 4G (85 ms round trip), on the simulations list, Fig. 5, the Portfolios page and Iron, Cotton
and the Head.

**Not answerable before the merge,** so set down first: whether Cloudflare matches the rules of the twelve pages whose names
hold spaces (written with `%20`), and whether it adds the security headers to a page served through a rule. The rule: revert at
once if, live, any of the 152 addresses answers another page or no page, any answer lacks the security headers, or any page shows
a failed request or a script error other than the analytics beacon.

**On the live site** (merged 31 October 2026 as `1195398`; Cloudflare served it 21 s later): 152 of 152 addresses right, the
names with spaces included, every answer with the security headers, no page with a failed request or a script error, 53 links
and none through a redirect. Kept. `fold.js` and `datalog.js` are byte-identical to the build; a section folded at
`/simulations/water-wave.html` is still folded at `/simulations/water-wave`, under the key used before (`fold:/simulations/water-wave`),
and the same for the catalog and the Arabic home page; `/_redirects` itself answers 404. First visit, median of 3
(`measure.cjs`):

| Page | Redirect, 4G | LCP, 4G | Redirect, Slow 4G | LCP, Slow 4G |
|---|---|---|---|---|
| `/simulations.html` | 164 → **0 ms** | 0.98 → **0.72 s** | 625 → **0 ms** | 2.85 → **2.22 s** |
| `/simulations/water-wave.html` (Fig. 5) | 141 → **0 ms** | 1.37 → **1.12 s** | 625 → **0 ms** | 4.16 → **3.57 s** |
| `/portfolios.html` | 146 → **0 ms** | 1.11 → **0.97 s** | 625 → **0 ms** | 3.56 → **2.99 s** |
| `/portfolios/impact/index.html` | 147 → **0 ms** | 0.79 → **0.60 s** | 625 → **0 ms** | 2.28 → **1.82 s** |

So a click between pages is 0.15 to 0.25 s sooner on a good phone connection and about 0.6 s on a slow one. To undo it: revert
`1195398`.

**What a reader sees.** The address bar shows the `.html` address after a click (`/simulations.html`); old short links still open
their page directly.

## Faults found outside performance, and fixed (31 October 2026)

An independent check of this page found the faults the work above had noted and left alone, and a few more. Each was reproduced
first, then fixed, then checked again; the commands are given so that anyone can repeat them.

| Fault | Reproduced | Fix | Checked after |
|---|---|---|---|
| A contents link tapped in a long study tab before the tab's link script had run loaded the whole study page inside the tab, and the 8 s guard then replaced it by a `blob:` frame, which the security policy blocks: a blank tab. Cause: a frame made from `srcdoc` resolves `#x` against the shell's address, and the script that handles such links sat at the end of the tab. | Rotor Pendula notes, Hydraulic Press Study theory, CPU 6×: the tap at once, then the frame `blob:` and unreadable 9.5 s later. | Both `build_combined.py`: the link script stands at the top of each tab (a target not yet read is reached once the page has been read); only the "ready" line stays at the end. The guard replaces a frame only while it is still empty (`about:blank`, or unreadable). | The same tap: the frame stays on its document and lands on the section (target 19 and 20 px below the top); a refused `srcdoc` still gets the `blob:` frame after 8 s; Rotor Pendula `check_combined.py` all pass; each tab differs from before only by the moved script. |
| Frame titles doubled ("Lecture notesNotes", "SimulationSimulation", "TheoryTheory"): the shell took the text of both the long and the short label. | Read from the frames in Chromium. | The title is the long label only. | "Lecture notes", "Theory". |
| The Hydraulic Press Study's `check_combined.py` could check only the English page. | It looked for English titles and English status words. | It finds each tab by the tab id its frame reports, the cycle's outcome by the status markup, the force target by its number; a translated page is held to the English elements, its text only required to be at least half as long. | 33 of 33 on `index.html`, `de.html` and `ar.html`. |
| 27 checks and measurement scripts (`portfolios-src/impact/checks/`, `hydraulics/tools/check_data_panel.cjs`, 20 in `notes/fig01` to `fig10`) launched a Chromium at a path that no longer exists (`…-1194`), so they could not start. | `ls /opt/pw-browsers`: only `-1243`. | They launch Playwright's own Chromium. The droplets' `check_browser.py`, whose fallback handed Playwright no browser and so failed where Playwright's own browser is not installed, falls back to `/opt/pw-browsers/chromium`, as the other studies' Python checks do. (`notes/verify.mjs` already fell back correctly.) | Iron, Cotton and the Head: `checks/site_check.cjs` (forces 638.6 N and 188.0 N, no errors) and `checks/data_panel.cjs` (English 390 px, Arabic 1100 px: "stored and recomputed identical"); Hydraulic Press Study `check_data_panel.cjs servo 390` (the same); droplets `check_browser.py` passes at 360, 390, 1024 and 1440 px. |
| `python3 tools/i18n/build.py --check` rewrote six generated files: the commit each names as its English source changes with every commit. | `git status` after the check. | `--check` writes nothing. It also fails if a generated file is not what the build would write now, commit stamps aside. | No file written; one generated page changed by hand is reported "stale" and the check exits 1. |
| `docs/files.md` left out `public/cv/` (four files): they had descriptions but no section, and a file in no section was dropped without a word. | Not one `cv/` row in `docs/files.md`, yet `inventory.py --check` passed. | A section for the CV page; a file in no section is now an error, like a file without a description. | `docs/files.md` lists the four files. |
| `node notes/walkcheck.cjs` found 754 of 759 quoted lines: five walkthrough lines (Figs. 3, 4, 5) quoted code whose words had since been wrapped in `_t()`. | 754 of 759. | The five quotes updated; the German and Arabic walkthroughs regenerated (their code is copied from the English). | 759 of 759. |
| `font-src` allowed `data:` fonts, which no page has used since change 1. | No served page or script makes a font from a `data:` address. | `font-src 'self'` on all 51 pages (`index.html`, from which the builders copy it, and every page). | Every page at 390 and 1440 px, study tabs opened: no blocked font, no failed font, no console error. |

One found fault is not fixed here, because it is a choice for Numa rather than a repair (the other, the wide equations, is fixed):

- **Display equations wider than their box** (fixed 1 November 2026, at Numa's instruction "a long equation gets multiple rows"):
  `node notes/verify.mjs` found 21, not six: one at 1440 px and 20 at 1600 px, where the data panel beside the page narrows the
  note's column to 541 to 579 px; at 390 px a probe found 112. Such an equation is now set in rows ([scripts/sim.md](scripts/sim.md),
  "Long equations"): 0 left at 1440 and 1600 px, 9 at 390 px (one fraction or matrix wider than a phone column each).
- **The analytics beacon**: Cloudflare inserts it only for browsers (a `curl` of the page gets the page as built), and every page's
  policy (`script-src 'self' 'unsafe-inline'`) blocks it. Allowing it means sending readers' visits to Cloudflare's analytics.

## Not changed, and why

- **The Hydraulic Press Study's tab bar** (CLS 0.21 on the English page; the German and Arabic pages have none): the bar shrinks 26 px
  when its two faces arrive. Preloading them from the page's head removed the shift (0.209 → 0.000), but on Slow 4G the first tab
  then appeared later (median of four sets of three runs, about 6.6 → 7.1 s), because the fonts took bandwidth from the page. Since
  change 2 the fonts stay in the reader's cache for a year, so the shift happens only on a first visit. Tried, measured, not merged.
- **The Arabic simulations list** keeps a shift of 0.14 (change 4 removed the list's own): the top bar grows when its Arabic face
  arrives. Not tried; the same trade-off as the tab bar above is likely (preloading takes bandwidth from the page).
- **Iron, Cotton and the Head computes its drop on the main thread** for about 95 s at full speed after the page opens (change 5);
  taps stay quick (56 ms), so it is left as the study designed it.
- **No ETag on HTML** (limit 3). Cloudflare's behaviour, not a setting in this repository.
- **The simulations' per-frame work on screen and Fig. 9's Solve** (cause 1). The off-screen work is gone (change 3). On screen, each
  figure still redraws all its canvases every frame, and Fig. 9's `label()` forces a layout every frame; Solve integrates the whole
  run in one task. Making the drawing cheaper means changing each figure's own code, the figures' authors' work; it is the next
  measured target, not done here.
- **The analytics beacon** blocked by the security policy: a Cloudflare dashboard setting (Web Analytics), left to Numa.

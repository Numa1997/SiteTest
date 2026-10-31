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
Iron, Cotton and the Head (0.86) move their content while loading, beyond the 0.1 of a good page. *Not changed yet: the causes are
still to be measured.*

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
`srcdoc` still triggers the replacement as before.

**Proof that nothing else changed.** For each of the four pages, every tab is identical character for character once each font,
embedded or linked, is replaced by the MD5 of its bytes (59 fonts per page, 21 distinct files); the shell differs only by the
guard above. Screenshots of every tab at 390 and 1440 px, before and after, once the fonts have loaded: the same font faces loaded,
identical text and layout, no console errors, no sideways scroll; the only differing pixels are the moving parts (the oil dots of
the ideal press, the running simulation and wind, the edge of the tab pill at the moment of the screenshot), which differ by as much
between two loads of the old page. Checks run on the new pages: Rotor Pendula `check_combined.py` (all pass: 1450 formulas, 0 KaTeX
errors, the simulation solves, the wind runs, tabs and deep links, 360 to 1440 px), `check_numbers.py`, `check_sim.js`,
`check_wind.js`, `check_newton.js`, `check_physics.py`, `R_revision.py` (all pass); Hydraulic Press Study `check_combined.py` on the
English page (33 of 33; the check finds frames by their English titles, so it cannot run on `de.html` and `ar.html`, on `main`
either), `check_theory_numbers.js` (52 of 52), `check_physics.py`, `check_control.py`, and the data-panel check
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
label.

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

## Not changed, and why

- **The `.html` → 307 redirect** (cause 3). Cloudflare's `html_handling: "none"` (in `wrangler.jsonc`) would serve `x.html`
  directly; but then the addresses without `.html` that readers have been sent to since 20 October would stop working, unless
  each is kept by a rule. Writing the links without `.html` would break the GitHub Pages copy and local files. Numa's decision; it is
  a Cloudflare setting, which this work does not change.
- **No ETag on HTML** (limit 3). Cloudflare's behaviour, not a setting in this repository.
- **The simulations' per-frame work on screen and Fig. 9's Solve** (cause 1). The off-screen work is gone (change 3). On screen, each
  figure still redraws all its canvases every frame, and Fig. 9's `label()` forces a layout every frame; Solve integrates the whole
  run in one task. Making the drawing cheaper means changing each figure's own code, the figures' authors' work; it is the next
  measured target, not done here.
- **The analytics beacon** blocked by the security policy: a Cloudflare dashboard setting (Web Analytics), left to Numa.

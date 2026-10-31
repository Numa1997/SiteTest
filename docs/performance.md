# Performance: what was measured, what was slow, what changed

Numa, 31 October 2026, on his phone: the site "looked good, but sometimes when switching from one page to another, or clicking
this or that, it lags a bit". This page records the experiment: how the site was measured, what the measurements show, which
change was made for which measured cause, and the same measurement afterwards. One change at a time; nothing is changed because
it "should" be faster.

## How it is measured

Everything below was measured in headless Chromium (the one preinstalled in the work environment), set up as Lighthouse's mobile
profile: a 390 × 844 px phone screen at 3× pixel density, the processor slowed 4× (`Emulation.setCPUThrottlingRate`), and the
network of Lighthouse's "Slow 4G" (562.5 ms round trip, 1.47 Mbit/s down, 0.66 Mbit/s up). Where a change trades download time
against processor time, it is measured a second time on a faster "4G" network (85 ms round trip, 9 Mbit/s), closer to a phone on a
good mobile connection. Each number is the median of three runs unless a table says otherwise.

The scripts are in [`tools/perf/`](../tools/perf/); Playwright and Chromium must be installed.

| Script | What it measures |
|---|---|
| `measure.cjs <base> <out.json> <runs> <path>…` | A first visit with an empty cache, then a repeat visit: LCP, CLS, total blocking time, the longest task, main-thread time, bytes over the network, and how busy the main thread is during 5 s in which the reader does nothing. |
| `interact.cjs <base> <out.json> <runs>` | What a reader does: home → simulations → Fig. 9 and back by links; Solve, the data panel, a fold, on Fig. 9; the three tabs of Rotor Pendula. Each interaction's duration comes from the browser's Event Timing API, which INP is built from. |
| `tabs.cjs <base> <path> <tabs> <runs>` | The study pages with tabs: the time from the click until the first tab is drawn, each tab switch, a repeat visit. |
| `trace.cjs <url> [scrollY]` | What fills the main thread while a page sits idle (a 4 s trace and CPU profile), with the figure on screen or scrolled away. |
| `loadtrace.cjs <url>` | The long parse, layout and script pieces of a study page loading. |
| `serve.cjs <folder> <port>` | A local server that answers as Cloudflare does (below), so that a change can be measured before it is merged. |

The metrics, as [web.dev](https://web.dev/articles/vitals) defines them, with its thresholds for "good" at the 75th percentile of
page loads: **LCP** (Largest Contentful Paint), when the largest text block or image of the first screen is drawn, good within
2.5 s; **CLS** (Cumulative Layout Shift), how far the content jumps while it loads, the sum of the shifted area times the shift
distance, good up to 0.1; **INP** (Interaction to Next Paint), the time from a tap to the next drawn frame, good up to 200 ms.
**TBT** (total blocking time) adds up every main-thread task beyond its first 50 ms; it is the laboratory stand-in for INP.

Three limits of the method, each a reason to read the numbers as comparisons rather than as a phone's exact experience:

1. **Software drawing.** Headless Chromium draws canvases with the processor, not a graphics chip. On the canvas-heavy pages the
   drawing part of each frame ("Commit", "Paint", native time) is therefore larger than on a phone; the script part is not.
2. **HTTP/1.1.** From the work environment Chromium reaches the live site through a proxy that speaks HTTP/1.1 (`protocol`
   `http/1.1` in the network log), with at most six connections per site. Phones reach Cloudflare over HTTP/2 or HTTP/3, all
   requests on one connection. `serve.cjs` with `H2=1` serves HTTP/2 locally; browsers keep no cache for a site with a certificate
   error, so repeat visits are timed over plain HTTP.
3. **The live site's response headers**, which the local server copies (measured with `curl -sI`, 31 October 2026):
   Cloudflare sends every file with `Cache-Control: public, max-age=0, must-revalidate` (its documented default for static assets,
   [Cloudflare: headers](https://developers.cloudflare.com/workers/static-assets/headers/)); CSS, scripts and fonts carry a weak
   ETag, so a repeat visit asks for each and gets `304 Not Modified`; **HTML pages carry no ETag and no Last-Modified at all**, so a
   repeat visit downloads every page again in full. A link to `x.html` is answered `307` with the address `x` (Cloudflare's
   default `html_handling`, ["auto-trailing-slash"](https://developers.cloudflare.com/workers/static-assets/routing/advanced/html-handling/)).

## The live site before any change (31 October 2026)

First visit, Slow 4G, CPU 4×, median of three runs (`measure.cjs https://phyeinusul.com … 3`). "Busy while idle" is the share of
5 s, after the page has loaded, in which the main thread works although the reader does nothing. "Redirect" is the 307 answer to
the `.html` address every link on the site uses.

| Page | LCP | CLS | TBT | Longest task | Busy while idle | Redirect |
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
(`public/simulations/driven-oscillator.html:1106`) measures text in every frame, which forces a full layout of the page each
time. The same 4 s trace with the figure scrolled 6000 px away, into the lecture note, shows the same work, frame for frame: the
clock of `Sim.clock` (`public/scripts/sim.js:176`) runs and draws whether or not the figure is on screen (the hero pendulum of
the home page, by contrast, already stops when it is out of view, `index.html:784`). Part of the per-frame cost is software
drawing (limit 1 above); the script part, about 34 ms per frame at 4× slowdown, and the work done off screen are real on a phone.
Fig. 9's Solve integrates the whole run in one task on the main thread (1.25 s at 4×).
*Not changed yet: it touches the figures' code, which another session is working on; see "Not changed" below.*

**2. Fonts sent again inside the study pages.** Rotor Pendula and the Hydraulic Press Study (English, German, Arabic) each carry
59 fonts as base64 `data:` addresses, about 440 kB of fonts per tab, three tabs per page: 1.3 MB of text that compresses badly. Every
one of those fonts is byte-identical (by MD5) to a file the site already serves from `public/fonts/` or
`public/vendor/katex/fonts/`. Compressed, the fonts are about three quarters of each page (Rotor Pendula 1418 kB with them,
398 kB without, zlib level 9), and since Cloudflare sends HTML without an ETag, a reader downloads them again on every visit.
*Changed: see change 1.*

**3. Every click pays a redirect.** Every internal link is written `….html` (so that the GitHub Pages copy and local files work),
and Cloudflare answers each with a 307 to the address without `.html`: one round trip lost before the page starts to load, 620 ms
on Slow 4G, about 0.1 to 0.2 s on a phone on 4G. *Not changed: the fix is a Cloudflare setting; see "Not changed" below.*

**4. Content that jumps.** The simulations list (CLS 0.28 in English, 0.29 in German), the Hydraulic Press Study (0.21) and
Iron, Cotton and the Head (0.86) move their content while loading, beyond the 0.1 of a good page. *Not changed yet: the causes are
still to be measured.*

**5. Repeat visits gain little.** With `max-age=0`, a repeat visit re-asks for every stylesheet, script and font (15 to 39
requests per page), and the simulations list takes 2.92 s on a repeat visit against 2.85 s on the first. *Not changed yet.*

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
parsing the same 1.3 MB of base64 text inside the page on every visit.

**Proof that nothing else changed.** For each of the four pages, the shell is identical, and every tab is identical character for
character once each font, embedded or linked, is replaced by the MD5 of its bytes: 59 fonts replaced per page, nothing else
different. Screenshots of every tab at 390 and 1440 px, before and after, once the fonts have loaded: the same font faces loaded,
identical text and layout, no console errors, no sideways scroll; the only differing pixels are the moving parts (the oil dots of the
ideal press, the running simulation and wind, the edge of the tab pill at the moment of the screenshot), which differ by as much
between two loads of the old page. Checks run on the new pages: Rotor Pendula `check_combined.py` (all pass: 1450 formulas, 0 KaTeX
errors, the simulation solves, the wind runs, tabs and deep links, 360 to 1440 px), `check_numbers.py`, `check_sim.js`,
`check_wind.js`, `check_newton.js`, `check_physics.py`, `R_revision.py` (all pass); Hydraulic Press Study `check_combined.py` on the
English page (33 of 33), `check_theory_numbers.js` (52 of 52), `check_physics.py`, `check_control.py`, and the data-panel check
`check_data_panel.cjs` for both presses at 390 and 1440 px (the pointer sweep paints nothing, pins, a Check "stored and recomputed
identical", one round recorded, no errors).

**Measured**, the old and the new pages on `serve.cjs` (Brotli, no ETag on HTML, as Cloudflare). Bytes are what crosses the
network; "first tab" is the time from the click to the first tab drawn.

| | Rotor Pendula, before | after | Hydraulic Press Study, before | after |
|---|---|---|---|---|
| The page, Brotli | 848 kB | **292 kB** | 551 kB | **196 kB** |
| First visit, 4G, HTTP/2: first tab | 7.29 s | **6.28 s** | 4.38 s | 4.30 s |
| First visit, 4G: bytes | 895 kB | **549 kB** | 686 kB | **490 kB** |
| First visit, 4G: total blocking time | 1.84 s | **1.41 s** | 1.46 s | 1.38 s |
| Repeat visit, 4G, HTTP/1.1: first tab | 6.59 s | 6.40 s | 4.75 s | **3.49 s** |
| Repeat visit, 4G: bytes | 831 kB | **297 kB** | 544 kB | **205 kB** |
| First visit, Slow 4G, HTTP/2: first tab | 11.13 s | **9.07 s** | 7.98 s | **6.51 s** |

One cost, measured and kept in view: with linked fonts the notes are laid out once with the fallback font and again when the fonts
arrive (a second full layout of about 0.9 to 1.2 s at 4× on Rotor Pendula's notes, `loadtrace.cjs`); with embedded fonts the
fonts were there at the first layout. The longest single task varies between runs in both versions (0.5 to 2.2 s), so it is
reported, not counted as a gain or a loss. Overall the first tab is drawn sooner or as soon on every network tried, with a third
to two thirds fewer bytes. Preloading the fonts from the page's shell was tried and dropped: the frames do not reuse the shell's
preloads, so the fonts were fetched twice (737 kB instead of 549 kB).

## Not changed, and why

- **The `.html` → 307 redirect** (cause 3). Cloudflare's `html_handling: "none"` (in `wrangler.jsonc`) would serve `x.html`
  directly; but then the addresses without `.html` that readers have been sent to since 20 October would stop working, unless
  each is kept by a rule. Writing the links without `.html` would break the GitHub Pages copy and local files. Numa's decision; it is
  a Cloudflare setting, which this work does not change.
- **No ETag on HTML** (limit 3). Cloudflare's behaviour, not a setting in this repository.
- **The simulations' per-frame work and the off-screen clock** (cause 1). Pausing the clock while no figure, walkthrough value or
  open data panel is on screen would remove the off-screen work; it touches `sim.js` and the data panel's live reading, and the
  figures are another session's current work. To be proposed, measured, separately.
- **The analytics beacon** blocked by the security policy: a Cloudflare dashboard setting (Web Analytics), left to Numa.

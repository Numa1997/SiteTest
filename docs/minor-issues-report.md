# Minor issues · final verification report

All five batches are complete. Each batch was deployed once, verified live, then committed and pushed to `codex/minor-issues-20261015`. No pull request was opened. No package was installed.

The live site is https://phyeinusul.com, built from this repository and served by Cloudflare ([usul.md](usul.md)).

Commits: [A — 9d3175f](https://github.com/Numa1997/SiteTest/commit/9d3175f2cf50d0ad3f8792f1ee173e8ce56bab53), [B — 74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f), [C — 43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5), [D — ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997). [E — 8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c).

Chromium checks passed locally and live at 1440 × 900 and 390 × 844: all 13 pages, no console errors, no KaTeX errors, no sideways scroll and no broken images. Final cleanup also preserved all typed-array hashes and 11 compared style properties on visible elements in all 26 page/viewport cases. One live shadow comparison sampled a fold transition; a targeted check after it settled matched exactly. Four final store/round exports pass ZIP CRC and NumPy loading; their READMEs use the actual filenames. Platform deployment checks reported no frontend, backend or network errors. A platform end-to-end test result was not exposed; the browser results here are the checks run directly.

Readbacks respect the picture’s precision: stored/recomputed numbers match exactly where stated; DOM text rounds to its displayed digits, SVG coordinates to their source precision, and canvas checks use alpha before colour. A quantity that is not drawn has no independent picture readback; the first fringe explicitly reports this when it lies outside the plot. Frame counters are checked against actual callbacks.

| Issue | Status | Proof |
|---|---|---|
| A1 · stale fringe orders | fixed | b = 40 px, λ = 20 px: sin θ₁ = 0.5, θ₁ = 30°, m = 1 label present. |
| A2 · hidden water layers | fixed | Five layers stored, three drawn at 960 × 900; final depth 2.24 m; checked parcel values identical. |
| A3 · empty-bench arrays | fixed | No waves: y_sum = 0, py_sum = mid1 and X spans 0–800. |
| A4 · exact wave repeat | fixed | ν = (1, 0.9975) Hz gives the 20 s cap, previously 1 s. |
| A5 · recording at Speed 0 | fixed | Start is refused with a reason; an active round waits explicitly and completes after Speed is raised. |
| A6 · twin locator | fixed | Four coordinates equal recomputation; pixels are rgb(226, 162, 170), with alpha checked first. |
| A7 · saved turbine target | fixed | All 27 target settings from 8 to 21 turns per minute recompute identically from the stored input. |
| A8 · archive README filenames | fixed | Both READMEs name the actual downloads; CRC and NumPy shape checks pass. |
| A9 · final sample | fixed | At 60 Hz: 600 samples from 601 frames, ending at 10.000000000000776 s; previously 9.983333333334107 s. |
| A10 · transverse endpoint | fixed | The drawing path has 215 points and ends at X = 640 with zero horizontal gap. |
| B1: oscillator log-axis labels | fixed | Ratios 0.1, 0.32, 1, 3.2, 10; endpoint gains 1.01005 and 0.0101005. |
| B2: turbine subscripts | fixed | Four SVG subscript spans render p / opt without underscores. |
| B3: wave-source grid counts | fixed | 1280, 1440, 1600 px: 360 × 162 = 58 320; 390 px: 324 × 324 = 104 976. |
| B4: inaccurate note numbers | fixed | Signed drift −2.416 × 10⁻⁸; 46-step upper bound; 4–17 px bob clamp; slit gap ≤1.4 × 10⁻¹³ px and plot width 500; water widths 800/400; spectrum 0–6 Hz; phase 25.346°; solver 9.5–12.4 ms; measured layout fractions; turbine K 0.5, airflow 5 px/m, dashes 16/22 px. |
| B5: phasor SVG clipping | fixed | Four unique active clip paths; phone image identical, desktop changes only 28 edge pixels. |
| B6: obsolete thumbnail | fixed | New 800 × 500 WebP from the current stage at device scale 2; current TeX axes and scale visible. |
| B7: portfolio image ratios | fixed | Attribute ratios exactly match all four SVG viewBoxes. |
| B8: layout gaps | fixed | 970 px home margin 104 → 48 px; empty catalog margin 28 → 0 px and display none. |
| C: transverse, water, bench and turbine excerpts | fixed | Complete quoted lines match source; omitted water caption is marked with an ellipsis. |
| C: pendulum equation references | fixed | References now point to equations (6)–(8). |
| C: phasor sampling and multiplier names | fixed | Every-sample scan documented; multiplier named live[i].mul. |
| C: effective morph alpha | fixed | Smoothing off: stored alpha 1, Now 0.08 → 1.00 at both sizes. |
| C: DFT completeness | fixed | 120 coefficients of 256; K = 120 heart error 0.000491411444. |
| C: damping notation | fixed | γ is the slider; g = γ/R is attenuation per pixel. |
| C: Fourier c_max, L, step and local ds | fixed | Rank-0 maximum labelled correctly; storage site documented; renamed arcDistances leaves all sample/coefficient arrays byte-identical. |
| C: pendulum updates, phasor ang and water frames metadata | fixed | Once-per-frame diagnostics, sumAt angle storage, and playing-only frame count documented. |
| C: scalar types and panel contract | fixed | uint8 and all four omitted contract keys documented. |
| C: catalog extension comment | fixed | New course years explicitly require STAGES, validation and wording updates. |
| D: Fig. 1 speed and alpha-first pixel check | fixed | Speed reads stored 33 px/s; source-dot check now tests alpha first. |
| D: Fig. 3 computation and walkthrough | fixed | Stored geometry agrees exactly with checks; first-order SVG label reads back 30° and sine 0.5. |
| D: Fig. 4 stored layout and shared constants | fixed | Stored-width/height recomputation is identical at both sizes. |
| D: Fig. 6 amplitude and frame count | fixed | Sum reads stored 50.3 px; after 65 callbacks frames is 65. |
| D: Fig. 6 Square preset | fixed | Frequencies are 0.4, 1.2, 2, 2.8. |
| D: Fig. 6 component pixel check | fixed | Actual wave passes; solid white and transparent canvas fail at both sizes. |
| D: Fig. 7 angles | fixed | Angle is stored by sumAt, recomputes identically, and its joint pixel passes. |
| D: Fig. 9 phase | fixed | Both displays read stored phi_deg = 25.346175941946683°. |
| D: Fig. 10 display results | fixed | h = 0.01 s and steps = 12000; range and captured share agree with checks and visible text. |
| E: unread frame counters | fixed | Removed only Figs. 3, 9 and 10 counters; all stored arrays match before cleanup. |
| E: nz and touchProbe | fixed | Global search finds no callers; removed the Fig. 7 helper and Fig. 8 hook. |
| E: home stop and request id | fixed | The private stop function had no callers; its request id had only writes after removal. |
| E: catalog intro | fixed | Removed the empty, permanently hidden element, hiding statement and CSS. |
| E: legacy cards and unused CSS | fixed | Removed the unused builder and selectors, plus unused sc and pbox--star rules; retained sim-error. |
| E: claim that .eq is unused | not reproduced | sim.js creates class="eq walk__eq"; rotor project also uses eq. The rule remains. |
| E: Sim.isInk and dataset helpers | fixed | No callers for isInk, index, at, size or Sim.Dataset. Retained shape; exports load in NumPy. |
| E: log fallback and paintStrip argument | fixed | All ten pages supply round; force had no reads. Actual recording and exports still pass. |
| E: overridden declarations | fixed | Removed earlier fold display/top and 26 px phone title rules; computed styles match. |
| E: five undefined tokens | fixed | Replaced only with their existing fallback values; compared colours remain identical. |
| E: overwritten label initializer | fixed | Removed sw = 0 before its unconditional assignment; drawing arrays remain identical. |
| Home title font and weight | decided | Since 20 October 2026 AGENTS.md ([41–43](../AGENTS.md#L41-L43)) and CLAUDE.md ([46–47](../CLAUDE.md#L46-L47)) name IBM Plex Serif at weight 600 for the home page alone, which is what [site.css:138](../public/styles/site.css#L138) sets. |
| Home card shadows | left for Numa | Preserved as requested. |
| Fold, simulation and data shadows | left for Numa | Preserved as requested. |
| Home eight-of-ten selection | left for Numa | Preserved as requested. |
| Home intro text | left for Numa | Preserved as requested. |
| Home “8 figures” count | left for Numa | Preserved as requested. |
| Fig. 3 reduced-motion start | left for Numa | Preserved as requested. |
| Paused redraws: Figs. 4, 9 and 10 | left for Numa | Preserved as requested. |
| Fig. 7 replay phase wrap | left for Numa | Preserved as requested. |
| Esc also stopping Read values | left for Numa | Preserved as requested. |
| Array-table hover ring | left for Numa | Preserved as requested. |
| Play aria-pressed | left for Numa | Preserved as requested. |
| “This simulation stopped” error message | left for Numa | Preserved as requested. |
| Walkthrough Now at 5 Hz | left for Numa | Preserved as requested. |
| Two favicons | left for Numa | Preserved as requested. |
| Duplicated Google Fonts import | fixed (later, by the self-hosted fonts) | No page or stylesheet loads Google Fonts any more: no `fonts.googleapis.com` in `index.html` or `public/`; [site.css:5](../public/styles/site.css#L5) imports `../fonts/plex.css`, [sim.css:7](../public/styles/sim.css#L7) and [catalog.css:7](../public/styles/catalog.css#L7) import `../fonts/instrument-plex.css`. |
| Repeated sim.css tokens | left for Numa | Preserved as requested. |
| CLAUDE.md | fixed in part | [CLAUDE.md:15–16](../CLAUDE.md#L15-L16) now gives the measured desktop grid 360 × 162 = 58 320; it keeps "360 × 360 at 880 px" (correct, [fig01-wave-sources.md](simulations/fig01-wave-sources.md)) and does not take the 390 px phone grid or the samples-per-wavelength and call counts of the proposed sentence below. |
| House fonts and colours | left for Numa | Preserved as requested. |
| Two embedded project copies | left for Numa | Preserved as requested. |
| physik-radar-xvy59b | left for Numa | Preserved as requested. |
| numa-physics-lab-chatgpt-k0ixwk | left for Numa | Preserved as requested. |
| GitHub Pages | superseded | Since 20 October 2026 the site is published from this repository by Cloudflare ([wrangler.jsonc](../wrangler.jsonc), [usul.md](usul.md)); nothing in the repository configures GitHub Pages. Correction, 29 October 2026: the GitHub Pages setting was never switched off and has published `main` at <https://numa1997.github.io/SiteTest/> since 16 January 2026; Numa decided that day to keep it on as a backup ([usul.md](usul.md#github-pages)). |
| Other maintainer notes outside the requested batches | left for Numa | Apostrophe consistency, xi naming, walkthrough path/header, unused catalog metadata, drawn_note, undeclared-value behavior, noscript listing, catalog debug state and cross-file CSS overrides remain. |

Proposals for Numa (none applied):

- **Home title font and weight:** Choose explicitly whether IBM Plex Serif 600 should remain or change to the documented house title face. (Decided on 20 October 2026: IBM Plex Serif 600 stays; see the table.)
- **Home card shadows:** Decide whether to keep the current shadows or adopt the no-shadow rule.
- **Fold, simulation and data shadows:** Make one explicit shadow policy for the visible fold, figure, walkthrough and data panels.
- **Home eight-of-ten selection:** Decide whether the home page remains a selection or adds Figs. 9 and 10.
- **Home intro text:** Update the description only after choosing whether the catalog should group by field.
- **Home “8 figures” count:** Keep the count tied to the approved home selection.
- **Fig. 3 reduced-motion start:** Synchronize the Animate checkbox with the clock’s initial paused state.
- **Paused redraws: Figs. 4, 9 and 10:** Consider drawing on control changes while paused, after confirming every control still responds.
- **Fig. 7 replay phase wrap:** Choose shortest-path phase interpolation for transitions across 2π.
- **Esc also stopping Read values:** Decide whether Esc should close only the panel or also end Read mode.
- **Array-table hover ring:** Consider requiring a click before marking the running figure.
- **Play aria-pressed:** Confirm whether pressed means paused or running, then align the accessible state.
- **“This simulation stopped” error message:** Use a general page-error message unless the clock has actually stopped.
- **Walkthrough Now at 5 Hz:** Choose 4 or 5 updates per second and whether folded walkthroughs should refresh.
- **Two favicons:** Choose one N or NK mark for the three top-level pages.
- **Duplicated Google Fonts import:** Consolidate font loading in a separate approved change. (Done: the fonts are self-hosted; see the table.)
- **Repeated sim.css tokens:** Centralize the shared tokens in a separate approved change.
- **CLAUDE.md:** Approve the measured replacement sentence below before editing this binding file.
- **House fonts and colours:** Keep the existing palette and type system; approve any future design change explicitly.
- **Two embedded project copies:** Handle changes inside either project as separate work; neither copy was edited.
- **physik-radar-xvy59b:** Keep this app outside this website-maintenance change.
- **numa-physics-lab-chatgpt-k0ixwk:** Keep this app outside this website-maintenance change.
- **GitHub Pages:** Choose a separate publishing task if this branch should later be served there. (Superseded: Cloudflare serves the site since 20 October 2026. Correction, 29 October 2026: Pages was still on and stays on as a backup, [usul.md](usul.md#github-pages).)

- **Other untriaged notes:** consider consistent apostrophes and displacement names; document the walkthrough’s required path; decide whether to expose catalog metadata; decide the dataset’s missing-value contract; make the no-JavaScript catalog complete; refresh the debug-state reference; review cross-file CSS overrides separately.

Proposed CLAUDE.md sentence, with the file unchanged (on 20 October 2026 its desktop numbers were taken into [CLAUDE.md:15–16](../CLAUDE.md#L15-L16); see the table): “In a 1280–1600 px desktop window, Fig. 1 computes a 360 × 162 = 58 320-point grid; on a 390 px phone it computes 324 × 324 = 104 976 points. At λ = 16 field px these give 7.2 and 6.48 samples per wavelength. Rebuilding Line of 16 on desktop uses 1 866 240 sine and cosine calls.”

## Independent audit, 15 October 2026

The five batches above were checked by a second agent (Claude) after they were deployed: each claimed fix reproduced
against the old commit `bad6513` and measured on the new one, in headless Chromium at 1440 × 900 and 390 × 844, locally and on
the live site. The shortfalls found were repaired in the app first (stored version `1792069058101`), then here in commit
[32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c).

**What held.**
- The live app equalled the branch: 73 of 75 served files equal (61 byte for byte, 12 HTML pages apart from the platform's
  injected lines); the other two differ only by platform behaviour (an extensionless file answered with the HTML fallback, and a
  `−` escape written out as "−").
- Nothing protected changed: `CLAUDE.md`, `AGENTS.md`, `site.css`, the build files, the project copies and QA scenario 1 are
  identical; the home page is pixel-identical to `bad6513` at both sizes, and 497 elements keep identical computed styles.
- Batch A: all ten fixes verified, each with the old fault reproduced first (for A1, all 3 965 slider combinations: 103 stale
  entries before, 0 after). No regression: every page clean; Record one round still finishes on Figs. 2, 5, 6 and 7.
- Batch B: B1, B3, B5, B6 and B8 verified by measurement; Batch C: 224 of 226 quoted code lines verbatim, the other two quote
  real code with an inline "..."; Batches D and E: no removed name is referenced anywhere, no display reads a value a frame late,
  and a three-way sweep of every page agrees between stored and recomputed values.

**What did not hold, and was repaired** (commit 32c240c, verified live):

| Item | Problem found | Repair |
|---|---|---|
| D, new read-backs | Fig. 3 `firstFringeReadback` and Fig. 10 `drawn.h` / `drawn.steps` return `ok: null` for "not drawn"; the panel showed that as a red "✕ The picture does not match". | `datalog.js` shows `ok: null` as a neutral line: "Not in the picture at the moment, so there is nothing to read back." (`data.css`: `.dp-check__verdict.is-na`). |
| D, Fig. 7 metadata | `computed_in` of `A_arm`, `jx`, `jy`, `px`, `py` was changed to "sumAt()"; they are written in `draw()`'s arm loop. | Restored to "draw(), the arm loop". |
| A5, on phones | The refusal to record at Speed 0 sat in text hidden at ≤ 640 px, and was overwritten on the next frame; on desktop it ran into the previous sentence. | The reason shows in its own `span.dp-rec__why`, at every width. |
| A5, Fig. 7 round | At Speed 0 the round read "part of the figure, 1.00 s" (Speed clamped to 0.05); below 0.05 a round took up to about 100 s of real time. | At Speed 0 a round is the full figure; no clamp, so a round never exceeds 20 s of real time. |
| D, Fig. 6 read-back | With no waves, the sum read-back passed on the faint zero-axis line (alpha 0.24). | Reports "not drawn" when the bench is empty. |
| B4, Fig. 2 drift | The note kept "stays below 3 × 10⁻⁸"; measured every frame, ε reaches +4.71 × 10⁻⁸ at t = 8.665 s (the run is deterministic). | "stays within ± 5 × 10⁻⁸: its largest value is + 4.7 × 10⁻⁸, at t ≈ 8.7 s". |
| B2, Fig. 10 figure | The new subscript p touched the Betz line at y = 38.8. | Title moved up 4 px; its box ends at y = 36.1. |
| B5, Fig. 7 figure | The new clip cut the dashed t = 6.28 s marker at x = 698 in half. | Clip rectangle 1 px wider (ends at x = 699). |
| B7, Portfolios | Width and height were the SVG viewBox numbers (400 520 × 188 969 …): right ratio, but 400 520 px images whenever no stylesheet loads. | 636 × 300, 419 × 300, 580 × 300, 470 × 300. With CSS the images are unchanged (506 px wide); without, 636 × 300 etc. |
| Docs | Five line links landed on the wrong code, several plain-text line numbers were stale, new store variables were described only in paragraphs after the notes, and "Fixed on" lines cited commits by message search. | Corrected in the docs pages; commits cited by hash. |

**Still open, newly noticed** (left for Numa): Fig. 4's longitudinal bead 11 fails its pixel read-back at 390 px (already so at
`bad6513`); the lecture-note SVG labels render at about 5.7 px on a 390 px phone; Fig. 7's `Sim.live()` recomputes the effective
α (`swMorph.checked ? morph.value : 1`) instead of reading the stored value (fixed since: `Sim.live()` reads `ds.get('alpha')`,
[phasor-sums.html:1302](../public/simulations/phasor-sums.html#L1302); the stored `alpha` is still written in the frame function
by evaluating the same expression again, [1341](../public/simulations/phasor-sums.html#L1341), not at the line of `morphStep()`
that uses it, [865](../public/simulations/phasor-sums.html#L865)); after A9 the last two samples of a round are two
frames apart instead of one.

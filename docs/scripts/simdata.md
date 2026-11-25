# simdata.js: one loader of stored simulation data for every page

[`public/scripts/simdata.js`](../../public/scripts/simdata.js), since 25 November 2026. Code by Neon (requests N-3 and N-4 in
[notes/sims/engine/neon/](../../notes/sims/engine/neon/)). No page uses it yet: the simulation sessions move their pages to it one
by one, in place of each page's own loader.

## What it does, in plain words

A page asks for its simulation by name. The loader reads the list of stored generations, `data/sims/generations.json`, once per
visit, and picks the newest generation of that simulation and data layout ("format") whose live check did not fail. It then
fetches the files the page asks for, from the repository or from Cloudflare R2, checks each one's length and SHA-256 fingerprint
against the list, and only then hands the bytes to the page. A file that fails the check never reaches the page.

## How a page uses it

```html
<script src="../scripts/simdata.js"></script>
```

```js
SimData.open('wave_interference2', { format: 1, base: '/', host: figureElement }).then(function (g) {
  g.prefetch(['dist_hi.bin']);            // start what the page will need next
  return g.file('geometry.bin');           // the whole file, checked
}).then(function (buf) { /* draw */ });
// g.part('dp_22_19_2.bin') reads a small file packed inside a big one, by byte range, checked
```

| Call | What it gives |
|---|---|
| `SimData.open(sim, {format, base, host})` | the newest usable generation: `sim`, `date`, `version`, `commit`, `format`, `store`, `entry`, and the methods below |
| `g.url(name)` | the address of a file, or of the pack that holds a part: `data/sims/<sim>/<date>/<file>` (repository) or `r2/sims/<sim>/<run>/<file>` (R2) |
| `g.file(name)` | the whole file, after its length and SHA-256 are checked |
| `g.part(name)` | one packed part, fetched with `Range: bytes=a-b`, answer 206, length and SHA-256 checked |
| `g.prefetch(names)` | starts downloads now; a failure shows only when the page asks for that file |
| `SimData.fail(host, message)` | one plain sentence in the figure: "The stored data for this figure could not be loaded (...)." |

## Rules it keeps

- **Once per visit.** Every file and part is downloaded at most once per page visit, however often it is asked for, by however many
  `open()` calls (one cache keyed by the full address, plus the byte range for a part).
- **One retry.** A dropped connection, or an answer 500, 502, 503 or 504, is tried once more after 0.5 s. A 404, a wrong length or a
  wrong fingerprint is never retried: it is a real fault.
- **One sentence when it fails.** With `host` given, any failure puts one sentence into the figure, replacing an earlier one from the
  loader, and leaves the page's own content in place.
- **Report for the live check.** `window.__simData` holds, for the simulation opened last, `sim`, `gen` (date, version, commit,
  format, store), `sha_ok` (true only once at least one file passed and none failed), `files` (the files that passed, in order) and
  `err` (the first failure); `window.__simData.all` holds the same for every simulation opened on the page. Opening a simulation
  again keeps what was already verified.

## Test

`node tools/sims/test_simdata.cjs` builds a small set of stored generations in a temporary folder, serves it from a local server
that answers byte ranges, and runs 14 cases in headless Chromium: the right generation is chosen (newest, right format, never one
whose live check failed), addresses for the repository and R2, exact bytes for files and parts, one request per file, a wrong
fingerprint refused and reported, the one sentence in the figure, the report, `generations.json` read once, prefetch, the shared
cache across `open()` calls, reports kept on a second `open()`, and one retry after a 503 but none after a wrong fingerprint.
Run on 25 November 2026: 14 passed, 0 failed.

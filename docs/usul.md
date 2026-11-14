# Phyein Usul · the website at phyeinusul.com

**Phyein Usul** (φύειν, Greek "to grow"; أصول, Arabic "roots") is the name of Numa's website: a personal website and an
archive, live at

**<https://phyeinusul.com>** (also <https://www.phyeinusul.com> and <https://phyein-usul.phyeinusul.workers.dev>)

It is built from this repository's `main` branch and served by Cloudflare, and GitHub Pages publishes the repository's `main` as a
backup ([below](#github-pages)).

## What runs where

| Part | Where | Notes |
|---|---|---|
| Domain `phyeinusul.com` | A zone in Numa's Cloudflare account | Zone plan: Free. Active since 20 October 2026. |
| Website | Cloudflare Worker `phyein-usul`: static assets, plus one small script for stored runs | No database, no login. Every request is a file: a static asset, or (under `/r2/`) a stored run file from R2. |
| Run store | R2 bucket `phyein-usul-runs` (binding `RUNS`), served by [`worker/r2.js`](../worker/r2.js) under `/r2/<key>` | Since 14 November 2026, for files too large for the repository (Fig. 15 generation 2). See "The run store" below. |
| Addresses | `phyeinusul.com`, `www.phyeinusul.com` (Worker custom domains), `phyein-usul.phyeinusul.workers.dev` | All three serve the same files. |
| Source | GitHub `Numa1997/SiteTest`, branch `main` | `index.html` and `public/` are the site; `docs/` and `tools/` are not served. |
| Config | [`wrangler.jsonc`](../wrangler.jsonc) | Worker name, the `dist/` folder, the two custom domains, the script `worker/r2.js` and the R2 binding. |

Plans and costs (checked 20 October 2026): the Workers Free plan serves requests to static assets "free and unlimited"
([Cloudflare Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/)); the site pays only the domain. A site
can hold up to 20 000 files of at most 25 MiB each on the free plan
([limits](https://developers.cloudflare.com/workers/platform/limits/)); a build of `main` gave 285 on 20 October 2026 and gives 233 on
29 October 2026, after this branch removed six unused figures (`npm run build && find dist -type f | wc -l`). Numa's decision, 20 October 2026: stay on the
free plan; dynamic features (for example a shared live counter) are for later and would need server code (Workers, D1).

## The run store (R2, since 14 November 2026)

Fig. 15's second generation holds about 3700 run files, several GB: too much for the repository (and for the 25 MiB-per-file,
20 000-file asset limits it would be close to). They live in the R2 bucket `phyein-usul-runs` on the same Cloudflare account; the
owner switched R2 on on 13 November 2026. What changed and what did not:

- `wrangler.jsonc` names a script, `worker/r2.js`, and binds the bucket as `RUNS`. The script answers only `GET` and `HEAD` under
  `/r2/`, and only for keys of the form `resonant-tunnelling/YYYY-MM-DD/runs/<name>.bin` (anything else under `/r2/` is a 404,
  other methods 405). It sends `cache-control: public, max-age=31536000, immutable` (a run file never changes; a new run gets a new
  name), `content-type: application/octet-stream` and `x-content-type-options: nosniff`.
- Every other request goes to `env.ASSETS.fetch(request)`, so the static site is served exactly as before (`html_handling: none`,
  `_redirects`, `_headers`). Checked before the merge with `tools/perf/addresses.cjs` against `wrangler dev`.
- The bucket needs no trust of its own: each page checks every run file's SHA-256 against its index, which lives in the repository.
- Upload: the Cloudflare REST API, `PUT /client/v4/accounts/<account>/r2/buckets/phyein-usul-runs/objects/<key>`, with an R2
  token (Admin Read & Write) that the cloud session's proxy injects; the token is never written anywhere. After each upload R2's
  etag is compared with the file's MD5.
- Cost (checked 14 November 2026, [R2 pricing](https://developers.cloudflare.com/r2/pricing/)): the free tier is 10 GB-month of storage, 1 million writes and 10 million reads a month, and no charge for traffic out.
  Above 10 GB it is $0.015 per GB-month. The measured size is stated in the Fig. 15 doc.

## Build and deploy

```bash
npm install             # no lockfile is committed; versions follow package.json
npm run build           # vite build: index.html + everything in public/ -> dist/
npx wrangler deploy     # publishes dist/ to the Worker phyein-usul (needs a Cloudflare sign-in)
```

Nobody runs these by hand any more. Since 21 October 2026 the Worker is connected to this repository (Cloudflare dashboard → Workers & Pages → phyein-usul → Settings → Builds,
repository Numa1997/SiteTest, branch `main`, build command `npm run build`, deploy command `npx wrangler deploy`). Every push or merge into
`main` therefore builds and publishes the site by itself; nobody has to sign in to Wrangler. Build logs: the Deployments tab of the Worker.
The two commands above still work by hand from a computer signed in to Cloudflare. Checked 29 October 2026: the merge commit
`3dffa3b` carries the check "Workers Builds: phyein-usul" (success), and the live `portfolios/rotor-pendula/` is byte-identical
to the same file in a fresh build. A branch other than `main` gets the same check in red, failing at once: only `main` is set up to
build. So merging into `main` is deploying, and it happens only on Numa's word.

**A file over 25 MiB fails the whole deploy (9 November 2026).** Merge `bf4edf8` carried `public/simulations/fig13/video/catch-dark.mp4` at 29.0 MB;
Cloudflare serves no asset above 25 MiB, so the deploy did not go out and the live site kept the previous version. `tools/fig13/gift/video_pages.py`
now raises the compression until each video is under 24 MB. Before merging large media: `find public -size +24M` must print nothing.

**When a merge does not build (seen 6 November 2026, again 9 November 2026: merge `ba082de`, the new gift video of Fig. 13, had no "Workers Builds" check while `7b49ec5` before it had one; the next merge started a build).** The merge `395fb42` (Fig. 12, PR #96) got no "Workers Builds: phyein-usul"
check at all, while every push before 09:22 UTC that day had one: Cloudflare never started the build, and phyeinusul.com kept the old page.
Check it with `curl -sS https://api.github.com/repos/Numa1997/SiteTest/commits/<sha>/check-runs | grep -o '"name": "[^"]*"'`: no
"Workers Builds" name means no build started. Then, in the Cloudflare dashboard: Workers & Pages → phyein-usul → Deployments, and start a
build of the latest `main` commit (Retry build / Deploy). If that also does nothing, Settings → Builds shows whether the GitHub connection
is still there; reconnecting it there (Disconnect, then Connect to Numa1997/SiteTest, branch `main`) restores the doorbell. GitHub's side
of it is the Cloudflare app under github.com → Settings → Applications → Installed GitHub Apps, which must have access to SiteTest.

**The same commit on a branch and on `main` (12 November 2026).** Merge `f831bbf` (Fig. 14 shapes and 3D views) was pushed to its branch and to
`main` as one and the same commit. Its "Workers Builds: phyein-usul" check shows failure with start and end in the same second
(22:10:28 UTC): the instant refusal a branch gets, not a build of `main`. `npm run build` and `npx wrangler deploy --dry-run` on that commit pass
(1978 files, none over 24 MB). The live site kept the old page until the next commit on `main` started a real build. Remedy: any new commit on
`main`, or Retry build in the dashboard.

**Addresses (since 31 October 2026).** `wrangler.jsonc` sets `"html_handling": "none"`: Cloudflare serves `x.html` and
`folder/index.html` as they are, the addresses every link of the site uses, with no redirect. Before, it answered each with a 307
to `x` or `folder/`, one round trip on every click ([performance.md](performance.md), change 6). The short addresses, which readers
saw in the address bar and shared from 20 to 31 October, keep working through `public/_redirects`: a 200 rule per page serves
the page there too (`/simulations` → `simulations.html`, `/` → `index.html`, `/ar/` → `ar/index.html`), and a 307 sends `folder`
on to `folder/` and `x/` to `x`, as before. `tools/redirects.py` writes the file from the pages in `public/` (rerun it after
adding, renaming or removing a page; `--check` fails if it is out of date). `node tools/perf/addresses.cjs https://phyeinusul.com dist`
asks for every page at every form of its address and follows every link. GitHub Pages ignores both settings.

Vite copies `public/` unchanged, so `dist/` is the file tree the visitor gets. Checked 20 October 2026: a fresh build of this
repository gives 285 files, every one byte-identical to the files served by the live site. To check the live site by hand:
`curl -sI https://phyeinusul.com/` shows status 200 and the security headers below.

A deploy creates a new Worker version; the previous ones stay listed in the Cloudflare dashboard (Workers → phyein-usul →
Deployments) and one click rolls back. Versions on 20 October 2026, the day of the move: `707205cd…` (first copy), `2523c05b…`
(+ security headers), `d51c2925…` (+ logo), `430df2c8…` (+ note under the logo). Since 21 October every merge into `main` adds one;
the dashboard lists them.

## GitHub Pages

GitHub Pages is switched on for this repository (a setting under Settings → Pages on GitHub, not a file in the repository). It
publishes `main` at <https://numa1997.github.io/SiteTest/> and republishes it on every push: GitHub's Actions list shows 63
"pages build and deployment" runs on `main`, from 16 January 2026 to the merge `3dffa3b` on 28 October 2026
(`curl -sS "https://api.github.com/repos/Numa1997/SiteTest/actions/runs?per_page=100&event=dynamic"`). On 14 October 2026 Numa
decided "no GitHub Pages", but the switch was never turned off. **Numa's decision, 29 October 2026: keep it on, as a backup copy
of the site that rebuilds on every push to `main`.**

What it serves, measured 29 October 2026: the repository's files as they are, without the Vite build. The address above returns
the root `index.html` byte for byte (status 200, title "Numa Koudsie · Notebook"), but the files that page links to sit under
`public/` in the repository, so `styles/site.css` and `simulations.html` answer 404 there, while
`https://numa1997.github.io/SiteTest/public/simulations.html` answers 200. The backup therefore holds every file, but its home page
shows unstyled and its links do not resolve. Pages ignores `public/_headers`, so the backup carries the meta-tag
security layer below and GitHub's own headers (it sends `Strict-Transport-Security: max-age=31556952`, measured 29 October
2026), but not the framing, nosniff, permissions and opener rules of `_headers`.

## Security

Two layers, both in the repository:

1. **The meta tags in every page** (Content-Security-Policy and referrer rule), explained in
   [build-and-deploy.md](build-and-deploy.md#security). They admit the site's own files and nothing else.
2. **Response headers** from [`public/_headers`](../public/_headers), which Cloudflare reads and never serves (asking for
   `/_headers` gives 404). They do what a meta tag cannot:

| Header | Value | Effect |
|---|---|---|
| `X-Content-Type-Options` | `nosniff` | The browser uses a file only as the type it is declared to be. |
| `X-Frame-Options` and CSP `frame-ancestors` | `SAMEORIGIN` / `'self'` | No other site can show these pages inside a frame. |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Linked sites learn only that the visit came from phyeinusul.com. |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=(), payment=(), usb=()` | No page can ask for these. |
| `Cross-Origin-Opener-Policy` | `same-origin` | A page opened from elsewhere cannot reach into this one. |
| `Cross-Origin-Embedder-Policy` on `/simulations/beer-slosh.html`, `/simulations/beer-slosh` and `/scripts/stout-worker.js` only (since 6 November 2026) | `require-corp` | With the opener policy above, the page is cross-origin isolated, so the browser lets Fig. 12 share memory with worker threads ([fig12-beer-slosh.md](simulations/fig12-beer-slosh.md)). The page loads nothing from other origins. |
| CSP `object-src`, `base-uri`, `form-action` | `'none'`, `'self'`, `'self'` | No plugins, no hijacked base address, no form posting elsewhere. |
| `Strict-Transport-Security` | `max-age=31536000` | Browsers use https only, for a year. |
| `Cache-Control` on `*.woff2` only (since 31 October 2026) | `public, max-age=31536000, immutable` | A font file is kept for a year without asking again; it never changes under its name, so a changed face needs a new file name. Every other file keeps Cloudflare's default, asked again on every visit ([performance.md](performance.md)). |

Checked 20 October 2026 on the live site with `curl -sI`, and in headless Chromium on all 15 pages: no errors.

What protects the site most is outside the code: a visitor only receives copies of the files and cannot write back. The site
changes only through the Cloudflare account (deploy) or this repository (source), so both accounts and their e-mail need two-step
sign-in. DDoS protection is included in every Cloudflare plan.

## What came with the move to Cloudflare (20 October 2026)

- `public/images/phyein-usul-mark.svg`: the logo (a fractal source; roots fading to the left, branches growing more irregular to the
  right; wine `#7a1f2b` and `#4d0f18`). Above the name on the home page (217 × 120) with the note "Phyein Usul · φύειν أصول, roots
  that grow. A personal website and an archive: my work, notes and simulations kept in one place, the older pieces beside what grew
  from them."; in the top bar of `simulations.html`, `portfolios.html` and the ten simulation pages (87 × 48), linking home.
- `public/_headers`: the security headers above.
- `wrangler.jsonc`: the Cloudflare configuration.

## Known limits

- The four portfolio pages are generated from their sources in `portfolios-src/` ([portfolios.md](portfolios.md)). They have no backend and no Saved
  runs, and carry no logo.
- The browser tab title and the home page heading still read "Numa Koudsie"; the site's name appears in the logo and the note.

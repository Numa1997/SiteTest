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
| Website | Cloudflare Worker `phyein-usul`, static assets only | No server code, no database, no login. Every request is a file. |
| Addresses | `phyeinusul.com`, `www.phyeinusul.com` (Worker custom domains), `phyein-usul.phyeinusul.workers.dev` | All three serve the same files. |
| Source | GitHub `Numa1997/SiteTest`, branch `main` | `index.html` and `public/` are the site; `docs/` and `tools/` are not served. |
| Config | [`wrangler.jsonc`](../wrangler.jsonc) | Worker name, the `dist/` folder, the two custom domains. |

Plans and costs (checked 20 October 2026): the Workers Free plan serves requests to static assets "free and unlimited"
([Cloudflare Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/)); the site pays only the domain. A site
can hold up to 20 000 files of at most 25 MiB each on the free plan
([limits](https://developers.cloudflare.com/workers/platform/limits/)); a build of `main` gave 285 on 20 October 2026 and gives 233 on
29 October 2026, after this branch removed six unused figures (`npm run build && find dist -type f | wc -l`). Numa's decision, 20 October 2026: stay on the
free plan; dynamic features (for example a shared live counter) are for later and would need server code (Workers, D1).

## Build and deploy

```bash
npm install             # no lockfile is committed; versions follow package.json
npm run build           # vite build: index.html + everything in public/ -> dist/
npx wrangler deploy     # publishes dist/ to the Worker phyein-usul (needs a Cloudflare sign-in)
```

Nobody runs these by hand any more. Since 21 October 2026 the Worker is connected to this repository (Cloudflare dashboard → Workers & Pages → phyein-usul → Settings → Builds,
repository Numa1997/SiteTest, branch `main`, build command `npm run build`, deploy command `npx wrangler deploy`). Every push or merge into
`main` therefore builds and publishes the site by itself; nobody has to sign in to Wrangler. Build logs: the Deployments tab of the Worker.

The job list, <https://stellen.phyeinusul.com> (Worker `stellenrecherche`, database D1 `stellenrecherche`, sign-in by Cloudflare Access), is
part of the same build since 29 October 2026. Its code is in `stellen/` (the Worker in `stellen/src/`, the Gmail script in
`stellen/apps-script/`; `stellen/README.md` describes it). The build command above ends with `node tools/deploy-stellen.mjs`, which, only
inside a Cloudflare build of `main`, runs the job list's tests and `npx wrangler deploy` in `stellen/` with the same deploy token Cloudflare
gives the website build (that token covers every Worker of the account). So one push to `main` publishes both addresses; a failed job-list
test or deploy fails the build, visible in the Deployments tab. Outside Cloudflare (`npm run build` on a computer, the GitHub Pages backup)
the step prints one line and does nothing. The job list's secrets (`OWNER_EMAILS`, `INGEST_CLIENT_ID`) live on the Worker and survive deploys.
The earlier repository `Numa1997/physiker-stellen` keeps the AppDeploy archive and the migration notes; its `cloudflare/` folder was the
previous home of this code.
The two commands above still work by hand from a computer signed in to Cloudflare. Checked 29 October 2026: the merge commit
`3dffa3b` carries the check "Workers Builds: phyein-usul" (success), and the live `portfolios/rotor-pendula/` is byte-identical
to the same file in a fresh build. A branch other than `main` gets the same check in red, failing at once: only `main` is set up to
build. So merging into `main` is deploying, and it happens only on Numa's word.

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
shows unstyled and its links do not resolve.

**The built-site workflow (29 October 2026).** The workflow
[.github/workflows/pages.yml](../.github/workflows/pages.yml) runs on every push to `main`. It builds the site as Cloudflare does
(`npm run build`) and publishes `dist/` to the same address, but only when Settings → Pages → Source is "GitHub Actions": its first
job reads the source through GitHub's API (`build_type`), and while it is still "Deploy from a branch" (`legacy`) the run ends
green without publishing, and the branch build goes on as before. The
built site works under the `/SiteTest/` sub-path: Vite writes relative addresses (`base: './'` in `vite.config.ts`), and all 1 496
relative links and sources in `dist/` resolve to a file (checked 29 October 2026). Pages ignores `public/_headers`, so the backup carries the meta-tag
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
| CSP `object-src`, `base-uri`, `form-action` | `'none'`, `'self'`, `'self'` | No plugins, no hijacked base address, no form posting elsewhere. |
| `Strict-Transport-Security` | `max-age=31536000` | Browsers use https only, for a year. |

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

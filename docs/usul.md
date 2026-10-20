# Phyein Usul · the website at phyeinusul.com

**Phyein Usul** (φύειν, Greek "to grow"; أصول, Arabic "roots") is the name of Numa's website: a personal website and an
archive, live at

**<https://phyeinusul.com>** (also <https://www.phyeinusul.com> and <https://phyein-usul.phyeinusul.workers.dev>)

It is built from this repository's `main` branch and served by Cloudflare. The same site, in an older version, also still
runs as the AppDeploy app ([appdeploy-app.md](appdeploy-app.md)).

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
([limits](https://developers.cloudflare.com/workers/platform/limits/)); the site has 285. Numa's decision, 20 October 2026: stay on the
free plan; dynamic features (for example a shared live counter) are for later and would need server code (Workers, D1).

## Build and deploy

```bash
npm install             # no lockfile is committed; versions follow package.json
npm run build           # vite build: index.html + everything in public/ -> dist/
npx wrangler deploy     # publishes dist/ to the Worker phyein-usul (needs a Cloudflare sign-in)
```

Vite copies `public/` unchanged, so `dist/` is the file tree the visitor gets. Checked 20 October 2026: a fresh build of this
repository gives 285 files, every one byte-identical to the files served by the live site. To check the live site by hand:
`curl -sI https://phyeinusul.com/` shows status 200 and the security headers below.

A deploy creates a new Worker version; the previous ones stay listed in the Cloudflare dashboard (Workers → phyein-usul →
Deployments) and one click rolls back. Versions so far, 20 October 2026: `707205cd…` (first copy), `2523c05b…` (+ security headers),
`d51c2925…` (+ logo), `430df2c8…` (+ note under the logo, current).

## Security

Two layers, both in the repository:

1. **The meta tags in every page** (Content-Security-Policy and referrer rule), unchanged from the AppDeploy version and explained in
   [build-and-deploy.md](build-and-deploy.md#security). They still name AppDeploy's overlay addresses; on Cloudflare nothing loads from
   them, so they allow nothing that is used.
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

## What changed against the AppDeploy version (20 October 2026)

- `public/images/phyein-usul-mark.svg`: the logo (a fractal source; roots fading to the left, branches growing more irregular to the
  right; wine `#7a1f2b` and `#4d0f18`). Above the name on the home page (217 × 120) with the note "Phyein Usul · φύειν أصول, roots
  that grow. A personal website and an archive: my work, notes and simulations kept in one place, the older pieces beside what grew
  from them."; in the top bar of `simulations.html`, `portfolios.html` and the ten simulation pages (87 × 48), linking home.
- `public/_headers`: the security headers above.
- `wrangler.jsonc`: the Cloudflare configuration.

## Known limits

- The two portfolio copies are built without Saved runs and without a backend, here as on AppDeploy; their source still lives in
  their own AppDeploy apps ([portfolios.md](portfolios.md)). They carry no logo (they are built bundles of separate apps).
- The browser tab title and the home page heading still read "Numa Koudsie"; the site's name appears in the logo and the note.

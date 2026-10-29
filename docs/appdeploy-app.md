# The AppDeploy app · numa-koudsie-website-0cyj78

The website first ran as the AppDeploy app **`numa-koudsie-website-0cyj78`** ("Numa Koudsie website"), at
<https://numa-koudsie-website-0cyj78.v2.appdeploy.ai>.

Since 20 October 2026 the primary site is Phyein Usul at <https://phyeinusul.com>, built from this repository and served by
Cloudflare ([usul.md](usul.md)). Numa decided on 20 October 2026 to keep the AppDeploy app running as it was (AppDeploy's free
version did well enough).

**Status on 29 October 2026: the app is gone.** AppDeploy's `get_apps` lists no apps in the account, `get_app_status` for this app
answers "App deleted" (status `deleted`, no address, last snapshot `1792151590518`), and the address answers 404 (`NoSuchKey`,
`curl -sS https://numa-koudsie-website-0cyj78.v2.appdeploy.ai/`). The apps in the table below answer 404 too. When and by whom it was
deleted is not recorded here. The rest of this page describes the app as it was. AppDeploy is touched only on Numa's request.

## Its state

| | |
|---|---|
| Last version | v65, `1792151590518`, deployed 16 October 2026 13:53 (Leipzig time) |
| Versions stored | 65 |
| Source | Equal to this repository up to commit `5c7ba7f` (16 October 2026), the last copy made from the app |
| Missing compared with Phyein Usul | everything merged into `main` after `5c7ba7f`: among it the logo and its note, `public/_headers`, `wrangler.jsonc`, Fig. 11, the German and Arabic pages, and the generated portfolio pages (`git log --oneline 5c7ba7f..main`) |
| Backend | none: static files only; the two portfolio copies are built without Saved runs |

How AppDeploy builds, tests and alters the site on a deploy (Prettier on stored source, the injected overlay, the rewritten
stylesheet links, the QA scenarios in `tests/tests.json`) is recorded in [build-and-deploy.md](build-and-deploy.md); those notes
describe this app and apply only to it.

## Related AppDeploy apps

| App | What it is | Relation to this repository |
|---|---|---|
| `droplet-collection-yl7l26` | Research project: droplet collection (thesis remodel), with Saved runs. | Its build was copied into `public/portfolios/droplet-collection/` until 23 October 2026; the page there is now generated from `portfolios-src/droplets/`, and the app is no longer its source. |
| `rotor-pendula-gafw0f` | Research project: wind-driven rotor pendula, with Saved runs. | Its build was copied into `public/portfolios/rotor-pendula/` until 23 October 2026; the page there is now generated from `portfolios-src/rotor-pendula/`, and the app is no longer its source. |
| `power-devices-emv071` | A placeholder page for a future portfolio on power semiconductor devices. | Not part of the website. |
| `physik-radar-xvy59b` | A separate app with sign-in and private records. | Unrelated; out of bounds for writes. |
| `numa-physics-lab-chatgpt-k0ixwk` | A separate version made with ChatGPT. | Out of bounds for writes. |

## If the app is ever updated again

Make the change in this repository first, build and check it, merge it into `main` on Numa's word, which deploys it to Cloudflare
([usul.md](usul.md)); then, only on Numa's
request, send the same files to the app (`deploy_app`, see [build-and-deploy.md](build-and-deploy.md)) and note the new version here.

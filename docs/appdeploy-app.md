# The AppDeploy app · numa-koudsie-website-0cyj78

The website first ran, and still runs, as the AppDeploy app **`numa-koudsie-website-0cyj78`** ("Numa Koudsie website"):

**<https://numa-koudsie-website-0cyj78.v2.appdeploy.ai>**

Since 20 October 2026 the primary site is Phyein Usul at <https://phyeinusul.com>, built from this repository and served by
Cloudflare ([usul.md](usul.md)). The AppDeploy app is kept running as it is (Numa's decision, 20 October 2026: AppDeploy's free
version does well enough). It is not changed unless Numa asks.

## Its state

| | |
|---|---|
| Current version | v65, `1792151590518`, deployed 16 October 2026 13:53 (Leipzig time) |
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

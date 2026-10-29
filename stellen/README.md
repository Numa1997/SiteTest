# Stellenrecherche · the job list on Cloudflare

**Stellenrecherche** (German for *job search*; English page title *Job search*) is the Cloudflare version of Numa's job list,
until now the AppDeploy app `physik-radar-xvy59b` ("Physik Radar", earlier "Physiker Stellen"). Same board, same design, same
records; German is the default language, English is one click away, and both are written as originals.

Address: **<https://stellen.phyeinusul.com>**, live since 20 October 2026. Private: only Numa's e-mail gets in. Where everything else went: [../MIGRATION.md](../MIGRATION.md).

## The three parts

| Part | What it is | Files |
|---|---|---|
| **Page** | Plain HTML, CSS and JavaScript modules, no build step. Served by Cloudflare as files. | `public/` |
| **Server** | A Cloudflare Worker that answers `/api/*` and nothing else. Checks who is asking, reads and writes the database. | `src/` |
| **Database** | Cloudflare D1 (SQLite) `stellenrecherche`, id `bedfef7d-fa7e-4592-9cdf-fa534d4f0e8f`, region Western Europe. Created 20 October 2026; the list (187 postings), the rules and the e-mail log (29 entries) imported the same day. Marks and hand-added postings: [../MIGRATION.md](../MIGRATION.md). | `schema.sql` |

Sign-in is **Cloudflare Access** in front of the whole address: a visitor without a valid Access session never reaches the page or
the server. The server checks Access's signed token again on every request (`src/access.js`) and lets only the e-mails in
`OWNER_EMAILS` through. If Access is not set up, the server refuses everyone (503, "Anmeldung noch nicht eingerichtet").

## Files

| Path | What it does |
|---|---|
| `wrangler.jsonc` | Worker name, the `public/` folder, `/api/*` to the Worker first, the D1 binding, the custom domain `stellen.phyeinusul.com`, no `workers.dev` address, the two Access variables. |
| `schema.sql` | The seven tables: `postings`, `meta`, `application_log` (the list), `marks`, `added` (what Numa does on the page), `mail_rejections`, `mail_events` (the rejection e-mails). |
| `src/worker.js` | The routes: `GET /api/dossier`, `GET /api/marks`, `PUT`/`DELETE /api/marks/:item`, `POST /api/added`, `DELETE /api/added/:item`, `GET /api/me`. Refuses a change sent from another site (Origin check) and any body that is not JSON. |
| `src/access.js` | Verifies the Access token (RS256 signature with Access's public keys, issuer, audience, expiry), then the e-mail. Local shortcut only on `localhost` with `DEV_OWNER_EMAIL`. |
| `src/validate.js` | What the server accepts: the fields of a mark, a hand-added posting (full https link, title ≤ 300 characters, …). |
| `src/catalog.js` | The eleven categories, two boards and six regions, in English and German. |
| `public/index.html` | Mounts the app. No inline code (the security policy forbids it). |
| `public/_headers` | Security headers: a strict content policy (only this site's own files), no framing, no referrer, HSTS, `noindex`. |
| `public/app/boot.js` | Loads list and marks, renders, or shows why it cannot (not set up, no access, session expired, no answer). |
| `public/app/page.js` | The board, carried over from Physik Radar's `src/claude/view/page.js` with every word moved to `i18n.js`. |
| `public/app/i18n.js` | Every interface text in German and English; the language switch; dates per language. |
| `public/app/api.js` | Every request to the server; saves for one card go out one at a time. |
| `public/app/dom.js` | The 30-line element builder. |
| `public/styles/board.css`, `gate.css` | The design, unchanged from Physik Radar (DESIGN.md of that app), plus the language button. |
| `public/fonts/` | Instrument Serif, IBM Plex Sans and Mono, self-hosted (the same files as on phyeinusul.com; SIL Open Font License). No request goes to Google. |
| `tools/to-sql.mjs` | Turns an export of the records into SQL for D1, checking every value first. Adds the German list rules. |
| `test/*.test.mjs` | `npm test`: input checks, the importer, the Access token check (5 tests). |
| `test/browser-check.mjs` | 23 checks per screen size in headless Chromium against the local server (German default, switch to English, Applied and Undo, adding and deleting, no sideways scroll, fonts, no script errors). |
| `test/seed.json`, `test/seed.sql` | **Invented** records for local tests. No real posting or application. |

## Absagen: the rejection e-mails (added 29 October 2026)

**<https://stellen.phyeinusul.com/absagen>** shows every mail of the Gmail label *Absagen*, oldest first, each in a bordered box
laid out like Gmail shows a mail. The button "Drucken / als PDF" waits until every mail is loaded and opens the print dialog
(Save as PDF): a cover, an index, one mail per page, page *x / y* at the foot.

How a mail gets there:

1. **Gmail filters** (`../apps-script/gmail-filters.xml`) put the label *Absagen* on a rejection as it arrives; doubtful ones get
   *uncertain rejection* instead, which never leaves Gmail. Moving a mail to *Absagen* by hand releases it.
2. **The Gmail script** (`../apps-script/Code.gs`, a Google Apps Script in Numa's own Google account, read-only Gmail access)
   sends labelled mails every 15 minutes, one per request, to `POST /api/ingest/known|rejections|present`, signed in with a
   Cloudflare Access **service token**. It sends only the images a mail carries inside itself and never downloads images from
   other servers. Setup: `../apps-script/README.md`.
3. **The Worker** (`src/mail.js`) judges each mail on its own (a bad one is refused with a reason, the script skips it), cleans its
   HTML once on arrival (`src/sanitize.js`: every allowed tag is rebuilt, every element closed, scripts, handlers, style blocks,
   forms, frames, outside images and `javascript:` links removed) and stores the cleaned copy (`mail_rejections`,
   `mail_images`). It feeds the e-mail log for mails from 1 September 2026 on: it closes the one open row (confirmed, unclear,
   portal invitation) of the same company, judged by sender and subject only, with the job title or reference number deciding
   between several; or it links to the row already marked rejected; otherwise, and always when an interview is involved, it adds
   its own row `mail-<id>`. Every change and the values it replaced are written to `mail_events` in the same transaction. Taking
   the label off a mail in Gmail hides it on the page and undoes its log change; nothing Numa wrote is ever deleted.
4. **The page** (`src/absagen.js`, `public/styles/absagen.css`, `public/app/absagen.js`): `GET /absagen` (header, cover, index),
   `GET /absagen/part?offset=N` (20 mails at a time), `GET /absagen/img/<id>/<n>` (one inline image). Each request is small, so the
   Worker stays inside Cloudflare's free-plan limits (about 10 ms of computing and 50 database calls per request). The page has
   its own strict policy: scripts only from this site, requests only to this site, images only from this site or `data:`.

Who may call what: `/absagen` and every other route need Numa's e-mail sign-in (Access, then `OWNER_EMAILS`); the three ingest
routes need the service token whose Client ID is the secret `INGEST_CLIENT_ID` and refuse an e-mail session. While
`INGEST_CLIENT_ID` is not set, they refuse everyone.

Checks: `npm test` (13 tests: sign-in, the mail cleaner against known attacks and in linear time, mail validation, log rules);
`test/absagen-browser-check.mjs` (screen and print in headless Chromium, against the local server after sending test mails).

## Language

German is the default; the choice is remembered per browser (`stellen.lang`). Every interface word is in
`public/app/i18n.js`, written in German and in English as originals (German job-ad and Agentur-für-Arbeit terms:
*Bewerbungsnachweis*, *Eingangsbestätigung*, *Absage*). The data carries its own language:

- **Job titles**: the German page shows the employer's own title first and the English one beneath it; the English page the other way round.
- **Eligibility quote**: always the employer's own (German) sentence.
- **Notes**: written in English so far. The table has a `note_de` column; the German page shows it where it is filled, otherwise the English note (marked `lang="en"`).
- **List rules**: English originals in `meta.rule`/`rule_eu`, German versions in `rule_de`/`rule_eu_de` (written for this version, in `tools/to-sql.mjs`).

## Local development

```bash
cd cloudflare
npm install
printf 'DEV_OWNER_EMAIL=owner@example.test\n' > .dev.vars   # never committed
npm run db:local      # tables + invented records into a local database
npm run dev           # http://127.0.0.1:8787
npm test
```

Checked 20 October 2026: `npm test` 5 of 5; `test/browser-check.mjs` 46 of 46 at 1440 × 900 and 390 × 844.

## Deploy

Needs a Cloudflare API token in the environment (`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`).

```bash
npx wrangler deploy                              # Worker, files, and the custom domain stellen.phyeinusul.com
npx wrangler secret put OWNER_EMAILS             # Numa's sign-in e-mail; kept out of this public repository
```

Sign-in (done 20 October 2026: organisation `phyeinusul.cloudflareaccess.com`, application "Stellenrecherche", one-time PIN, policy "Only Numa"; the values are in `wrangler.jsonc`, `OWNER_EMAILS` is set as a secret). To redo it by hand, in the Cloudflare dashboard: **Zero Trust** → **Access controls** → **Applications** → **Create new
application** → **Self-hosted and private** → public hostname `stellen.phyeinusul.com`; a policy **Allow** with **Include:
Emails** = Numa's address; login method **One-time PIN** (a code by e-mail). From the application's **Additional settings**
copy the **Application Audience (AUD) Tag** into `ACCESS_AUD` in `wrangler.jsonc`, the team domain
(`https://<team>.cloudflareaccess.com`) into `ACCESS_TEAM_DOMAIN`, and deploy again.

Undo: delete the Worker `stellenrecherche` in the dashboard (Workers & Pages), or `npx wrangler delete`; the address disappears
with it. The database is separate and stays.

## Moving the real records

Done for the list, rules and log on 20 October 2026 (from the app's stored source, v50). Still open: the marks and hand-added postings, which need step 1 below.


Only on Numa's explicit yes, and never through this repository, a log, an issue or a pull request:

1. Export from AppDeploy what `/api/dossier` and `/api/marks` return, signed in as Numa, into `private/export.json` (git ignores `private/`).
2. `node tools/to-sql.mjs private/export.json > private/import.sql` (it stops on the first bad record and names it). By default
   it writes only the marks and hand-added postings; `--replace-list` would also replace postings, rules and the e-mail log,
   which would undo the daily upkeep and the Gmail pipeline's log entries, so do not use it on the live database.
3. `npx wrangler d1 execute stellenrecherche --remote --file=private/import.sql`
4. Numa compares the counts and a few cards on both addresses; the AppDeploy app keeps running until he says to retire it.

## What is not carried over from AppDeploy

The one-time migrations of the AppDeploy server (legacy marks, the renumbering of 9 October 2026, applying the e-mail outcomes
from `backend/outcomes.mjs`) already ran there; the export carries their result, so they are not repeated. Dead code of that app
(`src/App.tsx`, `src/Radar.tsx`, `src/radar.css`) is left behind. The old Supabase version in this repository (`app/`,
`supabase/`, `index.html` at the root) is untouched.

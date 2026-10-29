# Gmail → Absagen page

Two pieces live in Numa's Google account; this folder holds their source.

| File | What it is | Where it runs |
|---|---|---|
| `gmail-filters.xml` | 7 Gmail filters. Six put the label **Absagen** on a rejection (a job-application word AND a refusal clause AND none of the excluded words); one puts **uncertain rejection** on a doubtful one (a job word in the subject AND a regret word). They only add labels: nothing is archived, deleted, forwarded or marked read. | Gmail → Settings → See all settings → Filters and blocked addresses → Import filters |
| `Code.gs`, `appsscript.json` | The sync script. Every 15 minutes it sends new mails with the label **Absagen**, one per request, to `https://stellen.phyeinusul.com/api/ingest`. Its only Gmail permission is **read-only** (`gmail.readonly`); it cannot send, delete or label mail. It never reads **uncertain rejection**, skips your own messages, never downloads images from other servers, and skips (and lists, `showSkipped`) a mail the server refuses, so one bad mail cannot stop the rest. | script.google.com, in your account |

How the filters were made (29 Oct 2026): all 433 mails then in the label were read in full; 253 were real rejections. The phrases were
chosen from those and checked with Gmail's own search over the whole mailbox: the strict filters matched 249 of 253 rejections
and none of the 172 other mails in the label; outside the label they matched only real rejections.

## Setup (your clicks; no password or secret ever goes through a chat)

1. **Service token** (Cloudflare dashboard → Zero Trust → Access controls → Service credentials → Service Tokens → Create Service Token,
   name `gmail-absagen`, duration 1 year). Copy the **Client ID** and **Client Secret** straight into step 3; the secret is shown once.
2. **Let it in** (Zero Trust → Access controls → Applications → *Stellenrecherche* → Policies → Add a policy): action **Service Auth**,
   include **Service Token** = `gmail-absagen`. Then the Worker must know which token is allowed:
   Workers & Pages → *stellenrecherche* → Settings → Variables and Secrets → Add → type **Secret**, name `INGEST_CLIENT_ID`,
   value = the Client ID (it ends in `.access`) → Deploy.
3. **The script** (script.google.com → New project, name `Absagen sync`): paste `Code.gs`; Project Settings → tick
   "Show appsscript.json" and paste `appsscript.json`; Services → add **Gmail API**; Project Settings → Script properties:
   `ENDPOINT` = `https://stellen.phyeinusul.com/api/ingest`, `CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET`.
   Run `backfill` once (Google asks for read-only Gmail access; "unverified app" is normal for your own script → Advanced → Go to …),
   then run `install` once.

If you remove the label from many mails at once (for example the clean-up of the old non-rejections), the weekly run refuses to
hide more than a quarter of the page in one go; run `reconcileForce` once by hand instead.

Off switch: run `uninstall` (removes the timers), or delete the service token (the server then refuses the script).
Rotate: create a new token, update the two script properties and `INGEST_CLIENT_ID`, delete the old token.

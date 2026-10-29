-- Stellenrecherche (job search record): the database, Cloudflare D1 (SQLite).
-- Eight tables. The first three are the list itself, written by the importer
-- (tools/to-sql.mjs); the next two are what Numa does on the page; the last two
-- are the rejection e-mails, sent by the Gmail script (apps-script/, label "Absagen").
-- Run once:  npx wrangler d1 execute stellenrecherche --remote --file=schema.sql
-- Re-running is safe: every statement is "if not exists".

-- One row per posting. `n` is the card number shown on the page; it never
-- changes, because marks are keyed to it ('j' || n).
create table if not exists postings (
  n                    integer primary key,
  title                text not null,      -- English title
  title_original       text,               -- the employer's own (usually German) title
  company              text not null,
  city                 text,
  location_group       text not null,      -- berlin | leipzig | de | benelux | nordics | europe
  category             text not null,      -- one of the eleven keys in src/catalog.js
  employment           text,               -- EMPLOYEE | CONTRACT | TRAINEE | TEMPORARY, the ad's own words, or null
  url                  text not null,
  eligibility_quote_de text,               -- the employer's sentence that admits physics
  eligibility_en       text,               -- the same, in short, in English
  salary               text,
  note                 text,               -- why it qualifies, in English
  note_de              text,               -- the same note, in German (shown on the German page when present)
  added_on             text,               -- YYYY-MM-DD
  removed_on           text,               -- set when the posting left the list; the row stays
  removed_why          text
);

-- Settings and texts the page shows but does not compute: the list rules
-- (rule, rule_eu, rule_de, rule_eu_de), the date of the last update, the
-- target per area. `value` is JSON.
create table if not exists meta (
  key   text primary key,
  value text not null check (json_valid(value))
);

-- What the job e-mails said, one row per e-mail summary entry, including
-- applications to postings that were never on the list (cards = []).
create table if not exists application_log (
  id      text primary key,
  cards   text not null default '[]' check (json_valid(cards)),   -- card numbers it concerns
  company text not null default '',
  title   text not null default '',
  status  text not null check (status in ('rejected','confirmed','interview','portal_invitation','unclear')),
  date    text not null default '',     -- YYYY-MM-DD, or '' when unknown
  note    text not null default '',
  source  text not null default ''
);

-- What Numa did with a card: Applied or Not relevant, with the date, a copy
-- of the card (so the record survives the posting) and, for applications,
-- the stage the e-mails reported. item_id: 'j<n>' for a listed posting,
-- 'a<timestamp>' for a posting Numa added himself.
create table if not exists marks (
  item_id    text primary key check (item_id glob 'j[0-9]*' or item_id glob 'a[0-9]*' or item_id glob 'c[0-9]*'),
  outcome    text check (outcome in ('applied','not_relevant')),
  outcome_at text,
  stage      text check (stage in ('applied','confirmed','interview','offer','rejected','withdrawn')),
  stage_at   text,
  round      integer,
  removed    integer,                  -- older marks only: 1 = removed before outcomes existed
  note       text,
  snapshot   text check (snapshot is null or json_valid(snapshot)),
  updated_at text not null
);

-- Postings Numa added himself with "+ Add posting".
create table if not exists added (
  item_id  text primary key check (item_id glob 'a[0-9]*'),
  url      text not null,
  title    text not null,
  company  text not null default '',
  city     text not null,
  area     text not null,
  category text not null,
  added_at text not null
);

-- One row per rejection e-mail: the headers, the mail's HTML as cleaned on arrival
-- (src/sanitize.js; the page only ever shows this cleaned copy) and the plain text.
-- Rows are never deleted: when the label is taken off in Gmail, label_present
-- becomes 0 and the page hides the mail.
create table if not exists mail_rejections (
  gmail_id      text primary key check (length(gmail_id) between 8 and 32 and gmail_id not glob '*[^0-9a-f]*'),
  thread_id     text not null default '',
  received_at   text not null,                 -- ISO 8601, UTC
  from_header   text not null default '',
  to_header     text not null default '',
  cc_header     text not null default '',
  subject       text not null default '',
  date_header   text not null default '',
  snippet       text not null default '',
  body_text     text not null default '',
  body_html     text not null default '',
  attachments   text not null default '[]' check (json_valid(attachments)),
  log_id        text,                          -- the application_log row this mail fed, if any
  label_present integer not null default 1,
  first_seen    text not null,
  updated_at    text not null
);
create index if not exists mail_rejections_received_idx on mail_rejections (received_at);

-- The images a mail carries inside itself (src="cid:…"), one row each, served by
-- GET /absagen/img/<gmail_id>/<n>. Images on other servers are never fetched.
create table if not exists mail_images (
  gmail_id text not null,
  n        integer not null,
  mime     text not null check (mime in ('image/png','image/jpeg','image/gif','image/webp')),
  data_b64 text not null,
  primary key (gmail_id, n)
);

-- Append-only history of what the pipeline did, so every automatic change can be
-- traced and undone by hand (detail holds the values before the change).
create table if not exists mail_events (
  id       integer primary key autoincrement,
  at       text not null,
  gmail_id text not null,
  kind     text not null check (kind in ('ingested','updated','label_removed','label_restored','log_appended','log_linked','log_reverted')),
  detail   text not null default ''
);

create index if not exists postings_open_idx on postings (removed_on) where removed_on is null;

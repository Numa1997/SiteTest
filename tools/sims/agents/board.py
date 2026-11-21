"""Kaggelize: the board. One GitHub issue, "Kaggelizing the simulations", with one row per simulation; every job of the
workflow rewrites its own row, so the issue always shows where each simulation stands and what waits for the owner.

  board.py set <slug> <title> <stage> <state> [<link>]   write one row (creates the issue on first use)
  board.py notes                                          print the owner's comments on the board issue (newest 15)
  board.py check-pause <environment>                      exit 0 only if that environment asks a reviewer before a job runs

The rows are kept as JSON inside a hidden comment at the end of the issue text and the table is drawn from it, so a row is
never parsed back from the table. Only an issue opened by the workflow itself or by the repository owner is used, and only
comments written by the owner are read: the repository is public and anyone may comment.

Environment: GH_TOKEN, GITHUB_REPOSITORY. For tests, BOARD_FILE=<path> keeps the issue text in a local file instead."""
import datetime, json, os, re, sys, urllib.request, urllib.error

TITLE = "Kaggelizing the simulations"
INTRO = ("One row per simulation that is being moved from live computing in the browser to data generated once on Kaggle "
         "(docs/kaggelize.md). Each job of the workflow **Kaggelize** rewrites its own row. A row that says **waiting for you** "
         "needs the owner: open the link, read, then approve or reject the pause on the run's page. Notes for the sessions: "
         "write them as comments here, as the owner, before approving; the next session reads them.\n")
MARK = "<!-- kaggelize-board "

def api(method, path, data=None):
    req = urllib.request.Request("https://api.github.com" + path, method=method,
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"], "Accept": "application/vnd.github+json",
                                          "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "kaggelize-board"})
    with urllib.request.urlopen(req, timeout=30) as r: return json.load(r)

def trusted(obj): return obj.get("author_association") == "OWNER" or obj["user"]["login"] == "github-actions[bot]"

def find(repo):
    for i in api("GET", f"/repos/{repo}/issues?state=open&per_page=100"):
        if i["title"] == TITLE and "pull_request" not in i and trusted(i): return i
    return None

def rows_of(body):
    m = re.search(re.escape(MARK) + r"(.*?) -->", body or "", re.S)
    try: return json.loads(m.group(1)) if m else {}
    except ValueError: return {}

def render(rows):
    t = [INTRO, "| Simulation | Stage | State | Last change (UTC) | Open |", "|---|---|---|---|---|"]
    for s, r in rows.items():
        link = f"[open]({r['link']})" if r.get("link") else ""
        state = f"**{r['state']}**" if r["state"].startswith(("waiting for you", "needs you", "failed")) else r["state"]
        t.append(f"| {r['title']} (`{s}`) | {r['stage']} | {state} | {r['at']} | {link} |")
    return "\n".join(t) + "\n\n" + MARK + json.dumps(rows) + " -->\n"

def clean(s): return re.sub(r"[|\r\n<>]", " ", s)[:160]

def set_row(slug, title, stage, state, link=""):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
    row = dict(title=clean(title), stage=clean(stage), state=clean(state), at=now, link=link if re.match(r"https://github\.com/[\w./#?=&%:+-]+$", link) else "")
    f = os.environ.get("BOARD_FILE")
    if f:
        rows = rows_of(open(f).read() if os.path.exists(f) else ""); rows[slug] = row; open(f, "w").write(render(rows)); return
    repo = os.environ["GITHUB_REPOSITORY"]
    for attempt in range(3):          # two jobs may write at once: read, change one row, write, and read back
        i = find(repo)
        rows = rows_of(i["body"]) if i else {}; rows[slug] = row
        if i: api("PATCH", f"/repos/{repo}/issues/{i['number']}", dict(body=render(rows)))
        else: i = api("POST", f"/repos/{repo}/issues", dict(title=TITLE, body=render(rows)))
        if rows_of(api("GET", f"/repos/{repo}/issues/{i['number']}")["body"]).get(slug) == row: break
    print(f"board: {slug}: {stage}: {state}  ({i['html_url']})")

def notes():
    repo = os.environ["GITHUB_REPOSITORY"]; i = find(repo)
    if not i: return
    cs = [c for c in api("GET", f"/repos/{repo}/issues/{i['number']}/comments?per_page=100") if c.get("author_association") == "OWNER"]
    for c in cs[-15:]: print(f"[{c['created_at']}]\n{c['body'].strip()[:4000]}\n")

def check_pause(env):
    repo = os.environ["GITHUB_REPOSITORY"]
    how = (f"Create it once: the repository's Settings -> Environments -> New environment -> name it {env} -> tick "
           f"'Required reviewers' -> add yourself -> Save protection rules. (docs/kaggelize.md, 'Setting up')")
    try: e = api("GET", f"/repos/{repo}/environments/{env}")
    except urllib.error.HTTPError as x: sys.exit(f"The environment '{env}' could not be read (HTTP {x.code}), so the pauses cannot be trusted. {how}")
    if not any(r.get("type") == "required_reviewers" and r.get("reviewers") for r in e.get("protection_rules", [])):
        sys.exit(f"The environment '{env}' exists but asks nobody: the run would not pause. {how}")
    print(f"pauses: the environment '{env}' asks a reviewer before each gated job")

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["set"] and len(a) in (5, 6): set_row(*a[1:])
    elif a == ["notes"]: notes()
    elif a[:1] == ["check-pause"] and len(a) == 2: check_pause(a[1])
    else: sys.exit(__doc__)

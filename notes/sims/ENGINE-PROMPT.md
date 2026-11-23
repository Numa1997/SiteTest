THE TASK
Rebuild the engine "Simulations on Kaggle" of the website Phyein Usul (https://phyeinusul.com, repository Numa1997/SiteTest, published
by Cloudflare from the branch main) so that it is fully automated and stores the data of every simulation in Cloudflare R2.

When you finish, a session puts one model file on main and does nothing else. Then, by itself:
- Kaggle computes the model, on the GPU when that is measured to be faster;
- every file is checked by its SHA-256 fingerprint and stored in R2;
- the repository keeps only the small index;
- the website serves the data;
- the live page is checked;
- superseded data is removed.
No person carries anything and no session babysits a run.

This task is the engine only. Do not convert any simulation page, and never touch another session's branch, pull request or any
scheduled task.

THE DECISION ALREADY MADE (do not reopen it)
All simulation data goes to R2: the bucket phyein-usul-runs, bound as RUNS in wrangler.jsonc and served by the site's Worker
(worker/r2.js). R2 takes objects of up to 5 TiB, downloads to visitors are free, and storage costs $0.015 per GB-month above 10 GB
(Cloudflare's docs, read 23 November 2026). More space can be bought when needed.

The repository keeps only small, readable files: generations.json, each run's index with every file's size and SHA-256, the models'
summaries and checks. GitHub releases are no longer used for data. The reasons, for the docs:
- GitHub blocks files over 100 MiB and asks for repositories under 1 GB;
- Cloudflare serves at most 25 MiB per static file;
- the /rel/ path fetched every visitor's request from GitHub.

START
1. Read the user's memory (/preferences.md, /areas/computational-physics.md, /areas/personal-website.md) and the skills
   phyein-usul-kaggle-pregenerate and kaggle-gpu-run. They are the user's rules; where anything below contradicts them, they win.
2. Read CLAUDE.md, AGENTS.md, docs/kaggle-sims.md, docs/usul.md, notes/sims/PLAN.md, and every engine file:
   .github/workflows/sims-kaggle.yml, tools/sims/pipeline.py, tools/sims/kaggle_sims.py, tools/sims/land.py, tools/sims/verify_live.py,
   tools/sims/registry.json, worker/r2.js, wrangler.jsonc.
   Then read the loaders the pages use today: sceneData() in public/scripts/bg-scenes.js, stored()/load() in
   public/simulations/Circular Wave Interference Visualization.html, and the double pendulum's loader if it exists.
3. Write notes/sims/engine/state.md (aim, what is live, what is left, branches, commits, the user's rules), commit and push it, and
   keep it current after every step. After a compaction, reread it first.
4. Tell the user in one short message what you will change, in five lines, then work. Do not wait for an answer.

WHAT EXISTS AND WORKS (keep it)
- SHA-256 from Kaggle to the visitor's browser.
- land.py: saves onto the newest main without clashing with other merges.
- The registry fields gpu and timeout_s, and the 6-hour job.
- The live check with page probes.
- Only names listed in the registry are ever computed.

THE FAULTS TO FIX (each seen in real runs on 23 November 2026)
1. One notebook and one concurrency group put every run in one queue: Fig. 1 waited about 20 minutes behind the double pendulum.
   GitHub also keeps only one pending run per concurrency group, so a third merge silently cancels the second one's pending run, and
   that model is never computed.
2. A rerun on the same day overwrites the same folder, entry and release tag. A changed file layout then breaks the live page, which
   is why Fig. 1 needed a new name, wave_interference2. And the year-long "immutable" cache keeps serving the old bytes at the same
   address.
3. The live check requires the page to fetch every listed file, which is impossible for pages that fetch on demand (Fig. 1 opens
   5 of 290).
4. Nobody measures CPU against GPU. On T4 cards 64-bit maths runs about 32 times slower than 32-bit.
5. Every page writes its own loader.
6. Clean-up is manual: old generations, release assets and merged kaggelize/* branches stay. Sessions cannot delete branches; the
   git proxy answers HTTP 403.
7. A Kaggle API hiccup while polling can be read as a failed run.

BUILD THIS
A. R2 as the store.
   - Credentials. A key already exists, but the engine cannot use it. Fig. 15's files were uploaded on 14 November 2026 with an R2
     key with full read and write rights, entered once through Claude's secure form and saved in the Claude cloud environment
     ("Default"). That environment's network layer adds the key to requests to api.cloudflare.com; the key is never written anywhere
     (notes/fig15/STATE.md, docs/usul.md "The run store"). It works only inside a Claude cloud session that runs in that environment.
     It cannot be read back, so it cannot be copied into GitHub, and GitHub Actions, where the engine runs, never sees it.
     Test it first: GET https://api.cloudflare.com/client/v4/accounts answers 200 only where the key is added.
   - The engine therefore needs its own key, as repository secrets: R2_ACCOUNT_ID, R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY, an R2
     API token with Object Read and Write on phyein-usul-runs only. The workflow uploads through R2's S3-compatible endpoint,
     https://<account id>.r2.cloudflarestorage.com, with rclone or the AWS CLI (both do multipart uploads for big files).
     Create the token and the three secrets in the user's signed-in browser (the built-in browser or Claude in Chrome), the way the
     GitHub-to-Cloudflare connection was made. Never ask the user for a token or to click in a dashboard, never print a key, and
     never put one in a file, a log or a notebook. If this session has no browser on the user's computer, stop and say exactly that,
     in one sentence. That is the only step that needs the user's machine.
   - Until the secrets exist, a Claude cloud session in the Default environment can still move existing data to R2 with the old key,
     as Fig. 15 was moved. Do that only for step J, never as the engine's regular path.
   - Upload: download each file from Kaggle, check its SHA-256, upload it to R2 at sims/<sim>/<run>/<file>, read it back (size and
     SHA-256 of what R2 now holds), and delete it from the runner before the next file. A runner has only about 30 GB of disk.
   - Addresses: <run> is <date>-v<Kaggle version>, unique for every run. Nothing is ever overwritten, so the immutable cache stays
     correct.
   - The repository keeps generations.json and public/data/sims/<sim>/<run>/index-<sim>.json (every file, size, SHA-256, store "r2")
     plus the model's summary.
   - The Worker serves /r2/sims/<sim>/<run>/<file> from RUNS, with byte ranges (env.RUNS.get(key, { range: request.headers })),
     status 206, content-range and a long cache. Keep Fig. 15's existing keys working.
   - Packing: a model may pack many small arrays into a few large files with an offset table in its index, so a page fetches byte
     ranges.
B. One notebook per simulation (numakoudsie/phyein-usul-<sim>; new versions only, never new notebooks) and one concurrency group per
   simulation. A GPU group holds GPU runs to Kaggle's limit of two at once. After every run, a reconcile step compares each registry
   model's last commit on main with the commits in generations.json and dispatches every model that is missing, so a cancelled or
   lost run is caught.
C. Formats. The registry entry has "format": n. The notebook writes it into the index and generations.json, and a page reads the
   newest generation of its simulation and format. A layout change then never breaks a live page, and no simulation needs a new name.
D. Benchmark mode. Run workflow with mode = bench and a simulation name pushes that simulation's notebook twice, once on CPU and once
   on GPU, each calling the model's bench(out_dir), which times the heavy kernel at three sizes. Results go to
   public/data/sims/bench/<sim>.json: sizes, seconds, card, library versions, and the full run's time extrapolated on each. The
   registry's gpu field is then set from that file, never from belief. Before any GPU run, read the remaining weekly GPU hours; if the
   estimate exceeds them, stop and report. Never fall back to CPU silently.
E. Robust runs.
   - The notebook's first lines check the device and stop at once if the GPU is missing.
   - Library versions and the card are recorded in the index.
   - Polling retries API errors with backoff for up to 10 minutes; only a real error or cancelled state stops the run.
   - Time queued on Kaggle does not count against timeout_s.
   - Runs longer than the 6-hour job are split into a start workflow and a collect workflow that polls every 10 minutes.
   - Outputs larger than Kaggle's working folder (about 20 GB; check the current limit) are sharded ("shards": n in the registry).
   - A model writes checks_passed into its index, and data whose checks failed is refused.
F. One loader for every page: public/scripts/simdata.js, documented in docs/scripts/simdata.md. It
   - finds the newest live generation of a simulation and format;
   - gives each file's address (repository or /r2/);
   - fetches whole files or byte ranges;
   - checks SHA-256 per file or per packed part;
   - prefetches the files a page names as next;
   - caches each file once per visit;
   - puts one plain sentence in the figure when no data can be loaded;
   - reports to window.__simData for the live probe.
   Write it, but do not convert any page; the simulation sessions will move their pages to it.
G. Live check. Hash every repository file. For R2 files, hash every file up to 100 MB in total and a range of the rest, and check
   every total size. Run each page's probe, which reports sha_ok, the commit and the files the page itself opened. If Cloudflare did
   not publish within 15 minutes, say so with the build's link. A generation that fails is marked "live_ok": false, and pages skip it.
H. Status for sessions. After every step, public/data/sims/status/<sim>.json records:
   - the state: queued, running, saved, live_ok or failed;
   - the notebook and version, the card, run and queue times;
   - the code and data commits, the bytes stored;
   - the failure in one sentence.
   A simulation session waits with git fetch in a sleep loop and reads this file. It never needs a browser or a scheduled task.
I. Clean-up, automatic and only after a live check passes. Remove superseded generations of the same simulation and format (R2
   objects, repository index folders, generations.json entries), keeping the newest of every format a page still reads. Delete
   merged kaggelize/* branches (the workflow has contents: write). List notebooks of simulations that left the registry for deletion.
   Write what was deleted and kept, with the reason, into the run summary.
J. Move what exists. Move the data of every simulation the engine already holds into R2, through the engine itself (one Run workflow
   per simulation, a new run each). Today that is barton, wave_interference2 (Fig. 1), double_pendulum and double_pendulum_smoke;
   read the registry for the current list. Point each page at it: if it uses the old loader, change only the base address the loader
   reads from, nothing else on the page. Run its live check. Only then remove the old copies from the repository and the GitHub
   releases (sims-*), one simulation at a time. Fig. 15's R2 data stays where it is.

RULES (each was broken once; do not break them again)
- Every run of a model, test runs included, happens on Kaggle through the real line, never in your own workspace. Test every
  scenario with a tiny permanent model, sims_smoke, that runs only on Run workflow and removes its data after a passing run:
  - a CPU run and a GPU run;
  - bench mode;
  - two simulations in one merge;
  - three quick merges (the reconcile must catch the cancelled one);
  - a same-day rerun (new address, old untouched);
  - a format change while a page reads the old format;
  - a packed file read by byte ranges through /r2/;
  - a failed model check;
  - a forced live-check failure.
  Record each test's run number and result in docs/kaggle-sims.md.
- Never delete old work until the new work is verified live.
- Merge only by the pull-request number the create call returned, passing its head SHA. Merge main into your branch first, keeping
  every other session's lines in registry.json, PLAN.md, inventory.py and kaggle-sims.md, and regenerate docs/files.md with
  python3 tools/inventory.py. Sessions for other figures merge while you work: nothing in the engine may assume it is the only
  change in flight.
- Merge and publish finished, tested work without asking, then verify it live.
- Commits carry only git -c user.name="Numa Koudsie" -c user.email="numakoudsie@gmail.com": no co-author line, no session link, no
  Claude attribution in commits or pull requests. In prose, write "the user", never a name.
- Wait for runs with a shell sleep loop, never with a scheduled task.
- Measure, never estimate: bytes from real files, seconds from real runs. Verify every limit or price you write against the primary
  documentation and link it.
- Talk plainly. Before each step, one short line saying what comes next; after it, one line with what came out. Never use other
  projects as examples. When wrong, say so in one line and fix it.

DOCUMENTATION
Rewrite docs/kaggle-sims.md as the plain-words guide to the new engine:
- every step, where each file lives and why;
- the R2 costs, measured on the real bucket;
- the user's controls (Actions → Simulations on Kaggle: Run workflow with a name or mode = bench, Cancel, Disable; where the secrets
  are);
- every scenario of the list above with its test.
Update docs/usul.md (the Worker), docs/files.md (tools/inventory.py describes R2 data by pattern, one line per generation) and the
skill phyein-usul-kaggle-pregenerate's text in notes/skills/ for the user to upload.

FINISH
1. All scenario tests green, and every moved simulation verified live from R2.
2. Clean-up done: test data, branches, scratch files.
3. Final report in plain sentences:
   - what the engine now does;
   - each test with its result;
   - the bytes now in R2 and in the repository, before and after;
   - the monthly R2 cost measured from the real bucket;
   - anything still not automated, and why.
   Send it as a push notification too.

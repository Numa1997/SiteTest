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

This task is the engine and the move of all stored simulation data that exists today into R2 (build item J): every figure's data,
whoever carried it and however, not only the simulations still to come. Do not convert any simulation page from live computing to
stored data, and on pages that already play stored data change only the address they read from. Never touch another session's
branch, pull request or any scheduled task.

THE DECISION ALREADY MADE (do not reopen it)
All simulation data goes to R2: the bucket phyein-usul-runs, bound as RUNS in wrangler.jsonc and served by the site's Worker
(worker/r2.js). R2 takes objects of up to 5 TiB, downloads to visitors are free, and storage costs $0.015 per GB-month above 10 GB
(Cloudflare's docs, read 23 November 2026). More space can be bought when needed.

The repository keeps only small, readable files: generations.json, each run's index with every file's size and SHA-256, the models'
summaries and checks. GitHub releases are no longer used for data. The reasons, for the docs:
- GitHub blocks files over 100 MiB and asks for repositories under 1 GB;
- Cloudflare serves at most 25 MiB per static file;
- the /rel/ path fetched every visitor's request from GitHub.

EVERY DATA SET ALSO STAYS ON KAGGLE (the user's rule, whatever the size)
R2 is where the site reads from. Kaggle is where the data was made and where a complete copy of it stays: every output file of every
run, byte for byte, in a private Kaggle dataset of its figure, as docs/kaggle-pipeline.md already rules since 14 November 2026
("Layout on Kaggle: one notebook and one dataset per figure"). Kaggle allows 200 GB per dataset and 200 GB of private datasets in
all, and at most 50 files at the top level, so files go in folders
(https://www.kaggle.com/docs/datasets, read 23 November 2026). The engine "Simulations on Kaggle" has not followed that rule so
far: its runs survive only as the output of a notebook version. Build item L closes that.

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

THE USER'S STANDING YES (so you do not stop to ask)
This prompt is the user's yes for every Kaggle run this task needs through the engine, GPU runs included, and for the engine's own
test runs. Do not ask again and do not send a "run card" and wait: the skill kaggle-gpu-run asks for a yes per run, and for this task
this paragraph is that yes. Two limits: read the remaining weekly GPU hours before any GPU run (Kaggle connector,
get_accelerator_quota), and if a run would use more than half of what remains, stop and ask in one sentence with the numbers.
On 23 November 2026 a session asked for a yes four times after the user had given it; do not repeat that.
If the app's safety check refuses a direct launch through the Kaggle connector (it did, when the session's prompt forbade launches),
do not retry and do not work around it: runs go through the engine, by a merge or by Run workflow.

WHAT EXISTS AND WORKS (keep it)
- SHA-256 from Kaggle to the visitor's browser.
- land.py: saves onto the newest main without clashing with other merges.
- The registry fields gpu and timeout_s, and the 6-hour job.
- The live check with page probes.
- Only names listed in the registry are ever computed.
- Since 23 November 2026 (pull request 183): a registry entry may say "store": "release" with "release_files" patterns. Those files
  go into the GitHub release sims-<sim>-<date>, only the index and the summary are committed, and the Worker serves them under
  /rel/<tag>/<file> with byte ranges (no cache in front of GitHub). The live check's step 2b asks each release file for its first
  1024 bytes. This is the stop-gap that R2 replaces: keep it working until every simulation that uses it is verified from R2.
- tools/sims/dp_engine.py (the double pendulum on the GPU, JAX, packs per mass-length cell), double_pendulum_smoke (its small test)
  and double_pendulum_gpu (the full run, 360 000 starts) are a simulation's files, not engine files. Measured with them on
  23 November 2026, Berlin time:
  - test (workflow run 45259655945): merged 21:28:02, data on main 21:31:16, live check passed 21:34; Kaggle used two T4 cards, the
    model took 22 s; the step that frees disk on the runner took 89 s;
  - full run (workflow run 45261988429): started 21:41; read its outcome in public/data/sims/generations.json and in
    notes/sims/reports/double_pendulum/state.md before you plan anything around it.

THE FAULTS TO FIX (each seen in real runs on 23 November 2026)
1. One notebook and one concurrency group put every run in one queue: Fig. 1's run (45255022407) was created at 21:01 Berlin time
   and could start only when the double pendulum's (45254099718) ended at 21:08; it finished at 21:14.
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
8. A save lost a whole computed run (45254099718): another session merged while Kaggle computed, both changes had rewritten
   docs/files.md, "git pull --rebase" stopped at the clash and nothing was saved. Fixed by land.py; keep that property in everything
   you build: no step may assume main stood still while a run was going.
9. After that failed save the data had to be computed again, although it was still on Kaggle: Kaggle keeps the output of every
   notebook version. download_notebook_output with versionNumber fetched version 3's index (109 files, 17 665 452 bytes) an hour
   later; list_notebook_session_output with versionLabel "3" answered "not found". The engine has no way to collect an old version.
10. Nobody can see how far a run is. While a session runs, Kaggle's API returns an empty log (list_notebook_session_output, 21:55),
    and GitHub's job-log API answers 404 until the job has ended. The only live progress is the notebook's page on kaggle.com, tab
    Logs. Do not promise progress the engine cannot read.
11. Nobody knew how long a run would take. A session told the user "2 to 3 minutes" for a run that took 7.5 minutes on Kaggle, then
    "about an hour" from nothing. Kaggle's CPU notebook measured 3.6 times slower per core than a Claude cloud workspace on the same
    model (1804 core-seconds on 4 cores against 506 on 2), so a time measured in a workspace is not Kaggle's time.
12. A registry entry can sit on main without data (double_pendulum, whose save failed). Nothing reports it.
13. Sessions watched runs by hand, with sleep loops the user had to interrupt, and reported times in UTC.

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
   - Collect mode: Run workflow with mode = collect, a simulation name and a Kaggle version number fetches that version's stored
     output and carries it through the same checks and the same store, without computing again. A failed save or upload is repaired
     this way (fault 9).
   - The step that frees the runner's disk runs only for simulations whose data needs the room (it took 89 s on a test of 2.6 MB).
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
   - the failure in one sentence;
   - expected_s and expected_done: how long the run should take and when it should end, computed from the simulation's benchmark
     file (seconds per unit of work on the chosen machine, times the units of the full run, plus the measured carrying time of the
     last run of similar size), written when the run starts; and the measured times next to them when it ends. Times are written in
     UTC in the file and shown to the user in Berlin time.
   The engine cannot read progress inside a run (fault 10): the status says so, and gives the address of the notebook's log page.
   A simulation session watches a run with the monitor of item K, which reads this file. It never needs a browser or a scheduled
   task.
I. Clean-up, automatic and only after a live check passes. Remove superseded generations of the same simulation and format (R2
   objects, repository index folders, generations.json entries), keeping the newest of every format a page still reads. Delete
   merged kaggelize/* branches (the workflow has contents: write). List notebooks of simulations that left the registry for deletion.
   Write what was deleted and kept, with the reason, into the run summary.
K. A monitor for every run. Write tools/sims/watch.sh <sim or workflow run id>. It
   - reads the run's jobs from the public GitHub API (https://api.github.com/repos/Numa1997/SiteTest/actions/runs/<id>/jobs answers
     without a key from a cloud session's shell; without a key GitHub allows 60 requests an hour, so ask at most every 2 minutes)
     and the status file by git fetch every 60 s;
   - prints one line, with the Berlin time, for every step change, for the data commit, and for every end state (success, failure,
     cancelled, timed out), and one "still running" line every 10 minutes;
   - ends when the run has ended.
   Sessions start it with the Monitor tool at the moment a run starts and re-arm it when it expires (a monitor lives at most
   30 minutes). Document it in docs/kaggle-sims.md and in the skill text. Use it yourself for every test run of this task.
J. Move everything that exists. Not only future simulations: every byte of stored simulation data the site has today goes to R2,
   whichever session, notebook or hand put it where it is. The repository keeps the small readable files (indexes, summaries,
   checks, generations lists). Measured on main on 23 November 2026, 22:04 Berlin time (measure again before you start):

   | Where it is now | Bytes | Files | Played by |
   |---|---|---|---|
   | public/data/schrodinger-sphere/ (generations 2026-11-12, 2026-11-13) | 618 589 311 | 4328 | Fig. 14, schrodinger-sphere.html |
   | public/data/resonant-tunnelling/ (2026-11-13, -14, -18) | 191 993 689 | 121 | Fig. 15, resonant-tunnelling.html; its large run files are already in R2 under resonant-tunnelling/<date>/runs/ (2782 files, 4.44 GB, for generation 2026-11-18; docs/simulations/fig15-resonant-tunnelling.md) and stay there |
   | public/data/sims/wave_interference2/ | 36 474 418 | 290 | Fig. 1 |
   | public/data/sims/barton/ | 45 999 | 2 | the home page's right margin |
   | public/data/fig12/ | 12 055 223 | 40 | Fig. 12, guinness-kaggle.html |
   | public/data/fig16/ | 11 988 965 | 11 | Fig. 16, guinness-cart-control.html (it also reads fig12) |
   | public/simulations/fig13/dive/dive.bin | 2 333 448 | 1 | Fig. 13, simulations/fig13/dive.html |
   | GitHub release sims-double_pendulum_smoke-2026-11-23 | 2 633 430 | 1 pack | no page (engine test) |
   | GitHub release sims-double_pendulum_gpu-<date>, if run 45261988429 ended well | read it | 25 packs | no page yet (Fig. 2) |

   All of public/data/ was 871 230 673 bytes; this session's clone of the repository was 1.42 GiB packed, above the 1 GB GitHub asks
   for. Removing files from main does not shrink the history; whether and when the history is rewritten is the user's separate
   decision (notes/history-removal/STATE.md). Do not rewrite history in this task; report the sizes.

   How:
   - Nothing is computed again. Add a move mode (Run workflow, mode = move, a name): it takes the files where they are stored (the
     repository or a release), checks each against the SHA-256 its own index records, uploads it to R2, reads it back (size and
     SHA-256 of what R2 holds), and writes the new index entry with store "r2". A file whose index has no SHA-256 gets one computed
     at the move, and the index says that it was computed then, not on Kaggle.
   - Figs. 12, 13, 14, 15 and 16 were carried by hand before the engine existed. Each has its own folder layout, its own
     generations list and its own loader in its page or script (docs/kaggle-pipeline.md, each figure's doc in docs/simulations/).
     Read those before touching them. Give each a registry entry that says it is filed, not computed by the engine (it must never be
     sent to Kaggle), with its page and a probe, so the live check covers it from now on. Keep every provenance record (notebook,
     version, commit, SHA-256) exactly as it is.
   - On each page change only where its loader reads from: the base address, or the one function that builds a file's address.
     Nothing else on the page, and no change to what the page shows. If a loader cannot be pointed at R2 that way, stop on that
     figure, say why in one sentence, and go on with the next.
   - Order, one simulation at a time: move the files; verify from R2 (sizes and SHA-256); merge the page's address change; run the
     live check with the page's probe; open the page in headless Chromium at 1600 and 390 px and compare a screenshot and the
     page's own numbers with the same page before the change; only then remove the repository copy or the release in a separate
     pull request. If the live check fails, put the address back first and remove nothing.
   - Before removing anything, search the repository for every reader of that folder (grep for its path in public/, tools/, docs/
     and notes/): another page or a tool may read it too (Fig. 16 reads Fig. 12's files).
   - The engine's own simulations (barton, wave_interference2, the double pendulum's packs) move the same way; a simulation session
     may be working on one of them at the same time, so read its state file in notes/sims/reports/<name>/ first and never change
     its page beyond the address.
   - double_pendulum is in the registry without data (fault 12): its 109 files exist only as the output of version 3 of the notebook
     numakoudsie/phyein-usul-simulations, and no page will read them. Do not move them; note it in the Fig. 2 state file.
   - Fig. 15's run files already in R2 stay where they are, with their keys.
   When this step is done, public/data/ holds no simulation data, only indexes and lists, and every page that plays stored data
   reads it from /r2/ and passes its live check.

L. Every generation into its figure's Kaggle dataset. Since 23 November 2026, 22:20 Berlin time, the engine does this for its own
   simulations (tools/sims/dataset.py, docs/kaggle-sims.md "Every data set also on Kaggle"): after every run, and by Run workflow with
   mode = dataset for an existing notebook version. Keep it, read the datasets it made (numakoudsie/phyein-usul-<sim>), and finish
   the rest of this item for the figures it does not cover.
   - After a run's files are checked, the engine files the whole output as a new version of the figure's private dataset
     (numakoudsie/<the figure's dataset>; one per simulation, new versions only, never a second dataset), laid out as
     <notebook>/v<version>/output/ with the run's log, the notebook's code and a manifest.json (size and SHA-256 of every file),
     exactly as docs/kaggle-pipeline.md describes. It uses the KAGGLE_API_TOKEN the workflow already has (the official tool's
     "kaggle datasets version"; the notebook's own output can be attached as the source so that nothing is uploaded twice: check
     which the tool supports, and measure).
   - generations.json and the run's index carry dataset and dataset_path, and the live check refuses a generation without them.
   - Before a dataset version is made, read the account's private quota in use; if the new version would not fit in the 200 GB,
     stop, say the numbers, and remove nothing.
   - Clean-up (item I) never removes a dataset or a dataset version that a live record names. A superseded generation leaves R2 and
     the repository, but its copy on Kaggle stays, unless the user says otherwise.
   - For what exists today (item J's table): for each figure, find its dataset and check that every file a live record names is
     in it, by size and SHA-256 (the file lists are in notes/inventory/datasets/: fig12-guinness-on-a-cart,
     fig14-schrodinger-sphere, fig16-guinness-cart-control). What is missing is added as a dataset version before its copy leaves
     the repository: Fig. 15 and Fig. 13 (find their datasets or make them), Fig. 1 (wave_interference2), barton, and the double
     pendulum (version 6 of the notebook numakoudsie/phyein-usul-simulations, 7 053 765 604 bytes in 25 packs; version 3 holds the
     first plan's 109 files). The Kaggle connector has no call that creates a dataset; Fig. 16's was made through api.kaggle.com
     (docs/kaggle-pipeline.md says how).
   - The docs get one table: per figure, its notebook, its dataset and version, its bytes on Kaggle, in R2 and in the repository.

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
- Watch every run with a monitor (build item K; until watch.sh exists, the Monitor tool with a poll of the public GitHub API), started
  when the run starts. Never a scheduled task, and never a blocking sleep loop that leaves the user without news.
- Every clock time you tell the user is Berlin time, read from a clock or a log at that moment (TZ=Europe/Berlin date), never UTC
  and never from memory. A session reported a merge at 21:35 that the log shows at 21:28.
- Every duration you tell the user is calculated from measured runs, with the calculation in the message: which run, its seconds,
  the scaling. If a part was never measured, say which part and that it is unknown. Never a round guess.
- Never drop, shrink or swap a plan the user chose. If something blocks it, say in one sentence what blocks it, look for another road
  to the same plan (CLAUDE.md, "Persist"), and keep going. A session dropped the user's plan twice on 23 November 2026.
- When a step fails, say at once where the computed data still is and how it gets to the site, before anything else.
- Main moves while you work: other sessions merge every few minutes. Merge main into your branch immediately before creating a pull
  request; if the merge call answers 405 (conflict), merge main again, regenerate docs/files.md, push, and merge with the new SHA.
- Your state file must be on main, not only on your branch, at every stop: a session that starts from main reads nothing else.
- Measure, never estimate: bytes from real files, seconds from real runs. Verify every limit or price you write against the primary
  documentation and link it.
- Talk plainly. Before each step, one short line saying what comes next; after it, one line with what came out. Never use other
  projects as examples. When wrong, say so in one line and fix it.

DOCUMENTATION
Rewrite docs/kaggle-sims.md as the plain-words guide to the new engine:
- every step, where each file lives and why;
- the R2 costs, measured on the real bucket;
- the user's controls (Actions → Simulations on Kaggle: Run workflow with a name or mode = bench, collect or move, Cancel, Disable;
  where the secrets are);
- where every figure's data lived before and lives now, with bytes (the table of build item J, measured again after the move);
- every scenario of the list above with its test.
Update docs/usul.md (the Worker), docs/files.md (tools/inventory.py describes R2 data by pattern, one line per generation) and the
skill phyein-usul-kaggle-pregenerate's text in notes/skills/ for the user to upload.

FINISH
1. All scenario tests green. Every simulation that plays stored data, old or new, verified live from R2, and public/data/ holding
   only indexes and lists (build item J). Every generation a live record names also lies in its figure's Kaggle dataset, checked
   by size and SHA-256 (build item L). Any figure you could not move is named, with the reason, in the report and in its doc.
2. Clean-up done: test data, branches, scratch files.
3. Final report in plain sentences:
   - what the engine now does;
   - each test with its result;
   - the bytes now in R2 and in the repository, before and after;
   - the monthly R2 cost measured from the real bucket;
   - anything still not automated, and why.
   Send it as a push notification too.

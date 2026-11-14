# Kaggle: every version of every notebook (read 14 November 2026, read-only)

Method. Status: `get_notebook_session_status` (version label format `v<N>`; labels `6` or `Version 6` are refused). Source and commit:
`get_notebook_info` with the same label. File names and run time: `list_notebook_files` with the same label (its `size` field is NOT
a file size: it returns 650 to 713 for every file, tar or log alike, and is ignored here; its `creation_date` is the minute the
version was started). Sizes: `download_notebook_output` returns one signed link for a file of a version; the same link with another
file path serves every other file of that version; a one-byte range request (`curl -r 0-0`) returns the exact size in `Content-Range`
(HEAD requests answer 404). Nothing is downloaded except small index or summary files.

## Status of the current version of all 35 notebooks

34 of 35: **COMPLETE**. `notebookddfec594b7`: "No runs found for this kernel" (never run). Nothing was running or queued on the account
at the time of the check (14 November 2026, after 12:30 UTC).

## Status of every older version

| Notebook | Versions | Status per version |
|---|---|---|
| guinness-on-a-cart-stout-in-jax | 10 | v1 to v10: all COMPLETE |
| guinness-on-a-cart-stout-sloshing | 5 | v1 COMPLETE, v2 COMPLETE, v3 COMPLETE, **v4 ERROR**, v5 COMPLETE |
| guinness-free-swing-v2 | 5 | **v1 ERROR**, v2 COMPLETE, v3 COMPLETE, v4 COMPLETE, v5 COMPLETE |
| schrodinger-shapes-3d | 2 | v1 COMPLETE, v2 COMPLETE |
| schrodinger-shapes-3d-v2-a, -b, -c, -d | 2 each | **v1 ERROR** (all four), v2 COMPLETE (all four) |
| html-panel-test-ripple-tank-computed-on-kaggle | 2 | v1 COMPLETE, v2 COMPLETE |
| phyein-sim-jax-swingup-gpu | 2 | **v1 ERROR**, v2 COMPLETE |
| phyein-sim-native-install-test | 2 | v1 COMPLETE, v2 COMPLETE |
| all other 26 notebooks | 1 each | v1 COMPLETE (the starter: never run) |

Total versions on the account: 10 + 5 + 5 + 2 + 8 + 2 + 2 + 2 + 25 (single-version notebooks that ran) = 61 runs, of which 8 ended in ERROR
(Kaggle gives an empty failure message for each). The 8 failed versions hold no result anyone uses.

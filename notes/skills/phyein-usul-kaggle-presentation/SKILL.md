---
name: "phyein-usul-kaggle-presentation"
description: "Before any Kaggle action for Phyein Usul: find the data where it already is (R2 and the repository) before computing or copying anything, never put signed download links or keys in a notebook, hand outputs between notebooks without links, and keep the Kaggle account organised and presentable with nothing public unless Numa names the item."
---

# Kaggle for Phyein Usul: find first, no links in notebooks, organised account

Written 24 November 2026 after the Fig. 15 filer notebook `fig15-filer-2026-11-18` (v3, v4) was found to hold seven
temporary download links in its code. Source: `notes/fig15/COORDINATOR_LOG.md` lines 40-56 and 120-131.

## 0. Read before the first Kaggle action
1. `docs/kaggle-pipeline.md` (line 193: saving a notebook through the connector DROPS attached inputs; Kaggle/kaggle-cli issue #1140).
2. `kaggle-gpu-run` skill (notebooks private; no secrets in a notebook, a private notebook is still stored).
3. `phyein-usul-kaggle-pregenerate` skill (the chain, the registry, the workflow that holds the Kaggle key).
Skipping this is what caused the links.

## 1. Find the data where it already is. Never recompute or re-copy first
Order of search, stop at the first hit, and say which place answered:
1. **The website's store.** Cloudflare R2, served by the Worker at `/r2/` (`worker/r2.js`). Fig. 15 generation 2026-11-18:
   keys `resonant-tunnelling/2026-11-18/runs/<file>`, 2,782 objects, 4,439,713,712 bytes
   (`notes/fig15/coordinator-2026-11-18/r2_upload.log`). The page animates exactly these files.
2. **The repository:** `public/data/...`, the index files, the records on the branch.
3. **The Kaggle originals** (notebook outputs, datasets), only if 1 and 2 lack it.
Only then ask Numa whether to compute. A new run is never the default.
If the container cannot read the store, say so and name the way round (Worker URL over HTTPS, `up.sh` relay); do not fall back to a run.

## 2. No signed links, no keys, in any notebook text
- Forbidden strings in notebook source before every save or push: `kaggleusercontent`, `X-Goog-Signature`, `X-Goog-Credential`,
  `token=`, `KGAT_`, `Bearer `, `api_key`, `secret`. Search the text; any hit stops the save.
- A signed link is a bearer ticket: whoever holds the address downloads the file with no login until it expires.
- To pass one notebook's output to another: make the output a Kaggle dataset (private) and attach it, or fetch from the repository or
  the Worker URL inside the notebook. Attach with the command-line tool from the workflow, because the connector drops attached
  inputs. The tool's metadata file has the fields `dataset_sources` and `kernel_sources` (Kaggle's own CLI guide,
  https://www.kaggle.com/code/citerne/from-local-dev-rtx-6000-kaggle-cli-guide), so attaching is designed in. Source names that fail
  to resolve are a known pitfall (https://github.com/Kaggle/kaggle-api/issues/433). Not yet tested on this account: run one tiny
  notebook (seconds) and read `/kaggle/input` before relying on it.
- A notebook that ever held a link keeps it in its older versions. Do not "clean" by pushing a new version; tell Numa and let
  Numa decide on deletion.

## 3. Organising and presenting the account
- Naming: datasets "Fig. N Name: simulation data"; tidy notebooks "Fig. N Name"; working notebooks prefixed `wip-`.
- Every dataset gets a subtitle, a description with the link to its page on phyeinusul.com, tags (physics, simulation), a cover
  picture from the site.
- Everything stays private unless Numa names that item. Nothing is deleted without Numa naming it.
- **Never public until Numa says finished: Fig. 12, Fig. 16, anything Guinness.**
- Before any item goes public: its text and files are searched as in section 2, and Numa sees the list of what a visitor would see.
- A visitor sees only public items; private ones, titles included, are invisible to everyone but the owner.
- **Public to private.** Evidence, checked 24 Nov 2026: Kaggle's launch post (https://www.kaggle.com/discussions/product-feedback/50755)
  says only that the owner can switch private to public "at any time" in Settings, Sharing; it says nothing about the way back.
  A community answer (7 years old, a user, not Kaggle staff: https://www.kaggle.com/discussions/product-feedback/153402) says it is
  one-way and the only escape is to delete the dataset and upload it again. Not confirmed by Kaggle staff. Treat public as a
  one-way door; the escape costs the dataset's URL, votes and version history.
- Settings the connector rejects (licence) go through the GitHub workflow that holds the key, with `private` set explicitly on every call.

## 4. Every Kaggle turn
One action per turn, named, with a yes from Numa. Inventory first (read-only): list datasets and notebooks with title, privacy,
last version; write the list into `notes/inventory/`, commit, push.

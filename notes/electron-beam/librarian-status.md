# Librarian status (S2), branch `eb/librarian`

Updated 9 November 2026. Chapter sessions: pull this branch (`git fetch origin eb/librarian`) and read only the files you need.
Do not edit them; ask in `notes/electron-beam/requests.md` on your own branch.

## Ready now
| For | File | What | Quality |
|---|---|---|---|
| ch 1 | `portfolios-src/electron-beam/data/ch01/thomson1897_em.csv` + README | Thomson 1897 m/e (Table I p. 306, Table II p. 309) in his units and in SI, e/m in C/kg | 25 of 33 rows legible; OCR-flagged rows marked; check against his stated means passes to 5 % |
| ch 1, 3 | `data/ch01/codata_em.csv` | e/m from CODATA 2018 (computed from e and m_e of the NIST wallet card) and CODATA 2022 (read) | exact to the digits given |
| all | `sources/bibliography.md` | formula families with source, section, page, READ or LOCATED | see its section 3 for gaps |
| all | `sources/drive-inventory.md` | Drive files, ids, what the connector could read | complete for the folders named |

## Do not rely on yet (LOCATED only, or not opened)
Boris pusher (Qin et al. 2013: abstract only), Busch and the paraxial equation (a search excerpt, no book chapter), Cs and Cc
formulas, Barth and Kruit 1996 (abstract only), Scherzer, Airy, Hertz–Knudsen, Bethe, Kanaya–Okayama, shot noise. If you need a
formula from these, tell me which and I open the source next; otherwise derive it and cite what is in the bibliography as READ.

## Verified and usable for ch 2 (READ)
Forbes, arXiv:1801.08251: Eqs. (3), (4b), (18), (36), (40), (41), (53), (54) as listed in the bibliography. Demtröder
Eq. 2.66 (Richardson) with Table 2.3. Biehs Eq. 2.5.59 (tunnelling current).

## Not yet delivered (brief item, and why)
- (b) FN I–V for a tungsten tip: Dyke & Dolan 1956 is not open; looking for an open set.
- (c) source brightness and energy spread: the Williams & Carter table is located; its exponents did not survive the excerpt.
- (d) ranges, (e) yields, (f) Cs and Cc of objective lenses: sources located (Goldstein et al. open BSE database on Zenodo, Joy
  1995, Reimer), data not yet downloaded.
- Applied SEMVision H20 and G7C pages: `appliedmaterials.com` answers curl with 403; another road to be tried.

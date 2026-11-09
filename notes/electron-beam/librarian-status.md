# Librarian status (S2), branch `eb/librarian`

Updated 9 November 2026. Chapter sessions: pull this branch (`git fetch origin eb/librarian`) and read only the files you need.
Do not edit them; ask in `notes/electron-beam/requests.md` on your own branch.

## Ready now
| For | File | What | Quality |
|---|---|---|---|
| ch 1 | `portfolios-src/electron-beam/data/ch01/thomson1897_em.csv` + README | Thomson 1897 m/e (Table I p. 306, Table II p. 309) in his units and in SI, e/m in C/kg | 33 rows, 4 flagged for OCR doubts; check against his stated means passes to 5 % |
| ch 1, 3 | `data/ch01/codata_em.csv` | e/m from CODATA 2018 (computed from e and m_e of the NIST wallet card) and CODATA 2022 (read) | exact to the digits given |
| all | `sources/bibliography.md` | formula families with source, section, page, READ or LOCATED | see its section 3 for gaps |
| all | `sources/drive-inventory.md` | Drive files, ids, what the connector could read | complete for the folders named |

| ch 2 | `data/ch02/source_properties_williams_carter.csv` + README | brightness, energy spread, work function, vacuum, life of W, LaB₆, Schottky, cold FEG (textbook, 100 kV) | textbook summary, not a measurement; printed Richardson constants wrong (flagged) |
| ch 6 | `data/ch06/bse_coefficient_vs_energy.csv`, `se_yield_lin_joy2005.csv` + README | BSE coefficient vs energy for Si, Cu, Au, Al, PMMA resist (open database, 0.1 keV to 15 MeV); SE δ_max, E_max and the universal law for Al, Si, Cu, Au | BSE: 497 points, spread between references ±7 % (Si); SE: fitted values, not raw points |
| ch 2 | `data/ch02/fn_tungsten_nanotip_li2025.csv` + README | measured I–V of one tungsten nanotip (R = 4 nm), 8 gaps, 771 points, with a worked FN analysis (β, f, k) | measured; **licence CC BY-NC-ND 4.0, see README**; not Dyke and Dolan |
| ch 5 | `data/ch05/objective_lens_cs_cc.csv` + README | Cs, Cc of low-voltage objective lenses (papers, not a textbook); Joy's worked probe-size example reproduced (18 nm at 5 mrad; true minimum 12.9 nm at 2.6 mrad) | excerpt/abstract level for the lens rows |
| ch 6 | `data/ch06/estar_electron_stopping_power.csv` | calculated stopping power 1 to 100 keV, Si, Al, Cu, Au, PMMA, SI units; matches an independent Bethe formula to 0.02 % | calculated, not measured |
| all | `sources/applied-public.md` | SEMVision H20 and G7 pages and the 2025 press release, public claims with numbers | H20 and G7 pages and release read whole; investor slides excerpt only |

## Do not rely on yet (LOCATED only, or not opened)
Boris pusher (Qin et al. 2013: abstract only), Busch and the paraxial equation (a search excerpt, no book chapter), Cs and Cc
formulas, Barth and Kruit 1996 (abstract only), Scherzer, Airy, Hertz–Knudsen, Bethe, Kanaya–Okayama, shot noise. If you need a
formula from these, tell me which and I open the source next; otherwise derive it and cite what is in the bibliography as READ.

## Verified and usable for ch 2 (READ)
Forbes, arXiv:1801.08251: Eqs. (3), (4b), (18), (36), (40), (41), (53), (54) as listed in the bibliography. Demtröder
Eq. 2.66 (Richardson) with Table 2.3. Biehs Eq. 2.5.59 (tunnelling current).

## Not yet delivered (brief item, and why)
- (b) Dyke & Dolan 1956 itself (a modern measured tungsten set is delivered instead).
- (c) a primary measurement of B_r and ΔE per source (the textbook table is delivered).
- (d) measured ranges (Everhart and Hoff 1971, Kanaya and Okayama 1972): paywalled; open copy not yet found.
- (e) SE yield of a resist.
- (f) Cs and Cc of SEM objective lenses *from a textbook* (papers delivered).

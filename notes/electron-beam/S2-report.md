# S2 (Librarian) report: project 07, The Electron Beam, from Tip to Measurement

Branch `eb/librarian`, last commit see `git log`. Written 9 November 2026. Nothing merged into `main`; nothing outside
`portfolios-src/electron-beam/sources/`, `.../data/`, `notes/electron-beam/` and one marked block in `tools/inventory.py` was written.
`python3 tools/inventory.py --check` finds no undescribed file; its only complaint is that `docs/files.md` is stale (the coordinator's file; I did not run the writer).

## 1. What a chapter session can use now

| Item (brief) | File | State |
|---|---|---|
| bibliography for the formula families | `sources/bibliography.md` | every row marked READ, LOCATED or NOT OPENED; **many families are still NOT OPENED** (section 3) |
| Drive, every file listed | `sources/drive-inventory.md` | complete for the six folders that matter; connector limits stated |
| Applied public statements | `sources/applied-public.md` | H20 page, G7 family page and the 2025 press release read whole |
| (a) Thomson 1897, CODATA e/m | `data/ch01/` | 33 Thomson rows (4 OCR-flagged); CODATA 2018 computed, 2022 read |
| (b) FN I–V, tungsten tip | `data/ch02/fn_tungsten_nanotip_li2025.csv` | measured, 771 points; not Dyke and Dolan |
| (c) source brightness, energy spread | `data/ch02/source_properties_williams_carter.csv` | textbook table, not a measurement; one printed constant wrong |
| (d) electron ranges | not delivered; formula and units only | see 3 |
| (e) SE and BSE yields | `data/ch06/bse_coefficient_vs_energy.csv` (497 points), `se_yield_lin_joy2005.csv` | no resist SE yield |
| (f) Cs, Cc | `data/ch05/objective_lens_cs_cc.csv` | papers and a white paper, not a textbook |
| extra | `data/ch06/estar_electron_stopping_power.csv` | calculated reference for Bethe |

## 2. Facts worth knowing, each with a handle

1. **Thomson's numbers differ from CODATA, and how.** My transcription of his Tables I and II gives e/m = 2.1×10¹¹ C/kg for tubes 1 and 2 (22 % above CODATA 1.7588×10¹¹) and
   0.78×10¹¹ C/kg for the deflection method (56 % below). He says tubes 1 and 2 read low in m/e (too high in e/m) through leakage in the gas (p. 307). Handle: `data/ch01/README.md`; paper text <https://www.damtp.cam.ac.uk/user/tong/pp/jj1.pdf>.
2. **Forbes' FN theory fits a measured tungsten tip.** Slope fits of the eight gaps give apex fields 3.3 to 3.9 V/nm, f ≈ 0.25 and geometric factor k = 2 to 4 for R = 4 nm
   (`data/ch02/README.md`, table). Handle: run `numpy.polyfit` of ln(I/V²) on 1/V for rows with I ≥ 2 nA.
3. **Joy's "18 nm" probe is the quadrature sum at 5 mrad, not the minimum.** The minimum is 12.9 nm at 2.6 mrad with 27 % of the current (`data/ch05/README.md`). Good material for ch. 5's trade-off.
4. **The universal SE-yield law matches Al and Si but not Cu and Au** against the paper's own Monte Carlo table (ratios up to 2.7 at 20 keV for gold) (`data/ch06/README.md`).
5. **ESTAR's collision stopping power equals the standard Bethe formula to 0.02 %** (my recomputation, formula from memory).
6. **Applied's 2025 claim "up to 10X imaging speed" for CFE against TFE** has the same form as its 2022 claim; neither has conditions. Cite as public claims only (`sources/applied-public.md`).

## 3. What is missing, honestly

Not opened at all (no source, so no formula citation yet): L = −mc²/γ − qφ + q v·A (Landau–Lifshitz, Jackson), the original Boris paper, Busch (1926) and a book chapter for the
paraxial equation, Airy intensity, Hertz–Knudsen and Langmuir, the Rutherford and Mott cross-section formulas, Bethe stopping power (ICRU 37), shot noise and CD-uncertainty and
throughput sources, Scherzer 1936 and 1949, Fowler–Nordheim 1928 originals. LOCATED only (abstract or excerpt): Qin et al. 2013 (Boris), Barth and Kruit 1996, Bronsgeest et al. 2008,
Everhart and Hoff 1971, Kanaya and Okayama 1972 (formula READ in a Goldstein et al. abstract), Griffiths ch. 8 and 11 and Demtröder §2.8.6 and §4.2.3 (the Drive text stops before them).
The brief said "only sources you opened and read": the table marks which are which, but a chapter session must open a LOCATED source before quoting from it.

Not delivered: measured ranges (d); a resist SE yield; a textbook Cs and Cc; Dyke and Dolan; Haken and Wolf and the Optical Systems slides (scans, empty text).

## 4. Roads taken, and which failed

Drive connector (answered; limits: first 130 to 210 kB per file, scans empty, 9 MB download refused). `curl` and arXiv API (answered for arXiv, NIST, Springer, Zenodo, Nature, Indiana, UChicago, ESTAR; refused with 403 or a proxy block for appliedmaterials.com, DAMTP, Hamline). WebFetch (503 on DAMTP). Exa fetch and search (answered where the others failed:
Thomson 1897, Applied pages, Joy 2006 and others). WebSearch (answered, locating only). The session was restarted once; Firecrawl and the Drive connector then disconnected and
Firecrawl was not used again. **Not tried**: TinyFish, Nimble, Tavily, Bright Data, Consensus, the Stack Exchange API. They would be the next roads for the NOT OPENED rows.

## 5. Risks to decide before publishing

- `fn_tungsten_nanotip_li2025.csv` comes from a CC BY-NC-ND 4.0 paper's Source Data; NC-ND bars adaptation. Keep the CSV in the repository (not served) or ask the authors.
- The Williams and Carter table and Lin and Joy's Table 1 are copyrighted; they are small tables quoted with citation. Same caution.
- Thomson's rows are my transcription of OCR text, not seen on the page images. Anyone with the images should check the four flagged rows.
- Errors found in sources, left as printed and flagged: W&C Richardson constants (6×10⁹ for W); Zenodo `Au.csv` says Z = 74; Joy's λ constant 1.26 (1.2264); Joy's 0.61 λ/α called a diameter.
- BSE reference numbers in the Zenodo files appear only on a block's first row; carrying them forward is my reading of the layout.

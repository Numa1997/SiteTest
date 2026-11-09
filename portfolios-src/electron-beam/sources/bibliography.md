# Bibliography for project 07 (The Electron Beam, from Tip to Measurement)

Librarian session S2, branch `eb/librarian`. First written 9 November 2026. Rule of this file: a source is listed under a formula
only if I opened it. Each entry says what I actually read.

Status words (used in every row):

- **READ**: I opened the text and read the passage named. The equation or section number is as printed there.
- **LOCATED**: I found the item and read its abstract, a search excerpt or its table of contents, but not the passage itself.
  A chapter session must open it before quoting a formula from it.
- **NOT OPENED**: no source yet. Listed in section 3.

How the sources were reached (the road that answered): Google Drive connector (read-only) for Numa's books and lecture scripts;
`curl` and arXiv's API for arXiv, NIST and Springer pages; Exa `web_fetch_exa` for the Thomson paper (two other roads, `curl`
and WebFetch, failed on that host); `WebSearch` and Exa search for locating items. Firecrawl and the Drive tool were
disconnected by a session restart; not used after that.

## 1. Books and lecture scripts from Numa's Drive (READ, partly)

The Drive connector returns only the first 130 to 210 kB of text of each file (about the first 80 to 250 pages), and nothing
at all for scans (Haken and Wolf, the Optical Systems slides). So the **end** of every big book is not readable by me. See
`drive-inventory.md`.

| Short name | Book | What I read | Where it helps |
|---|---|---|---|
| Demtröder | W. Demtröder, *Atoms, Molecules and Photons*, 2nd ed., Springer 2010 (Drive: `1XBO1eeiiQSgUwfwFH9Sg7n43PWARviMs`) | Contents pages; §2.5.1 (Thomson's tubes, Fig. 2.41); §2.5.3 a) and b) (thermal and field emission, p. 37); §2.5.5 (e/m by Wien filter and radio-frequency methods, pp. 41–44); §2.6.2 (axially symmetric fields, Eq. 2.83); §2.6.4 (magnetic lenses, pp. 50–51, Eqs. 2.99c and 2.100); §2.2.3 (field emission and tunnelling microscopes) | ch. 1, 2, 4 |
| Biehs | S.-A. Biehs, *Quantum Structure of Matter*, lecture manuscript, Univ. Oldenburg, summer 2017, transl. K. Brümann (Drive: `1Irl4wzhwFSTT4yDUv4iY_qu54RvpBobZ`) | §2.5 "Potential Barrier: Tunnel Effect", pp. 51–58, the transmission coefficient for κa ≫ 1 and the tunnelling current J_T ∝ exp(−2κs) (Eq. 2.5.59, p. 58, with κ = √(2mΦ)/ħ) | ch. 2 |
| Hohmann | V. Hohmann, *Numerical Methods for Physicists*, Univ. Oldenburg, v1.0, April 2004 (Drive: `1lfTxUsA4fvIwLCRzpcepcGqo82GvezdT`) | §5.4 "Runge–Kutta method of the 4th order", pp. 33–35: the four slopes H1 to H4, local truncation error of order τ⁵; §4.1 on truncation and round-off error in differentiation (§3.4 heading only) | ch. 1 |
| Griffiths | D. J. Griffiths, *Introduction to Quantum Mechanics*, 1st ed., Prentice Hall 1995 (Drive: `1gHg8Bgh-5jrQNN3uhj9Hf46wRiZMEVIp`) | Contents only, plus ch. 1 to §2.7. Per the contents: ch. 8 "The WKB approximation" p. 274, §8.2 "Tunneling" p. 280; ch. 11 "Scattering" p. 352, §11.3 "The Born approximation" p. 363. **LOCATED**: the Drive text stops at §2.7 (p. 66), so I could not read ch. 8 or 11 | ch. 2, 6 |
| Haken & Wolf | H. Haken, H. C. Wolf, *The Physics of Atoms and Quanta*, Springer (Drive: `1lCyH1-X3PIHw-u1RETEtbEiMK-Lwaqn3`) | **Nothing**: the Drive file is a scan and returned empty text. Chapter list from Springer (7th ed., 2005, doi 10.1007/3-540-29281-0): ch. 4 The Nucleus of the Atom (pp. 37–48), ch. 6 The Electron (pp. 69–80), ch. 9 The Mathematical Framework of Quantum Theory. Section titles inside chapters came only from a search summary; not verified | ch. 1 (e/m), 6 (Rutherford) |

Also found in Drive and not useful here: *Concepts in Thermal Physics* (Blundell & Blundell; text returned blank), the EP4 exam
and formula sheets, *Electrodynamics_lecture_Summary.pdf* (Oldenburg slides: Lorentz force, Maxwell; summary level only), the
`ED_lecture_*.pptx` slides, the Optical Systems ST18 slides #1 to #9 (image-only; connector returned empty text).

## 2. Formula families (PLAN.md section 4)

### 2.1 Lagrangian, Lorentz force, e/m
| Item | Source | Status |
|---|---|---|
| Lorentz force F = −e(v × B) on an electron, cathode-ray deflection | Demtröder §2.6.4, p. 51; §2.5.1 | READ |
| e/m by crossed E and B (Wien filter), e/m = E²/(2VB²) | Demtröder §2.5.5, pp. 41–44 | READ |
| Thomson's own measurement, both methods, tables of m/e | J. J. Thomson, "Cathode Rays", *Phil. Mag.* S5 **44** (1897) 293–316, doi 10.1080/14786449708621070; text via <https://www.damtp.cam.ac.uk/user/tong/pp/jj1.pdf>; Table I p. 306, Table II p. 309; discussion pp. 310–312 | READ (OCR text; digitised in `data/ch01/`) |
| L = −mc²/γ − qφ + q v·A, canonical momentum | no source opened | NOT OPENED (Landau & Lifshitz, *Classical Theory of Fields*, §16; Jackson ch. 12: to open) |

### 2.2 Boris pusher
| Item | Source | Status |
|---|---|---|
| Boris pusher preserves phase-space volume, bounded energy error | H. Qin, S. Zhang, J. Xiao, J. Liu, Y. Sun, W. M. Tang, "Why is Boris algorithm so good?", *Phys. Plasmas* **20**, 084503 (2013), doi 10.1063/1.4818428 | LOCATED (abstract; paywalled) |
| Boris is not variational | C. L. Ellison, J. W. Burby, H. Qin, arXiv:1509.02863 | LOCATED (abstract) |
| Original algorithm | J. P. Boris, Proc. 4th Conf. Numerical Simulation of Plasmas (1970); Birdsall & Langdon, *Plasma Physics via Computer Simulation* | NOT OPENED |

### 2.3 RK4
Hohmann §5.4, pp. 33–35 (READ). Local error O(τ⁵), global O(τ⁴): the first is quoted there, the second follows (state as inference).

### 2.4 Laplace equation, axial field expansion
| Item | Source | Status |
|---|---|---|
| ∇²φ = 0 for electrodes without space charge, Eq. 2.83 | Demtröder §2.6.2 | READ |
| B_z = B − B″r²/4 + B⁗r⁴/64 − …, B_⊥ = −½(B′ − B‴r²/8 + …) r, from A = ½(−y, x, 0)Π and Π = Σ (−r²/4)ⁿ B^(2n)/(n!(n+1)!) | S. A. Khan, R. Jagannathan, arXiv:2009.13943 (2020/21), Eqs. (1)–(4) | READ (search excerpt of the intro and §2; open the PDF for the full derivation) |
| Relaxation (Jacobi) for Laplace's equation | Hohmann §9.3.1, p. 83 | LOCATED (text in Drive ends at p. 80) |

### 2.4b Busch's theorem, paraxial ray equation, Glaser field
| Item | Source | Status |
|---|---|---|
| Glaser bell field B(z) = B₀/(1 + (z/a)²) and its exact solution through ϕ = cot⁻¹(z/a) | Khan & Jagannathan arXiv:2009.13943, Eq. (5) and §6 | READ (excerpt) |
| Busch formula named as the classical focal-length result | same paper, introduction (cites Hawkes & Kasper vols. 1 and 2) | READ (excerpt) |
| Focal length of a homogeneous longitudinal field, f = z_f/4 with z_f = 2π m v_z/(eB) | Demtröder §2.6.4, Eqs. 2.99c and 2.100 | READ |
| Busch's theorem (1926), paraxial equation r″ + (e/8mV*)B²r = 0 | Hawkes & Kasper, *Principles of Electron Optics*, vol. 1; Septier chapter at <https://www.classe.cornell.edu/~hoff/LECTURES/09S_510/Z1/septier.pdf> | LOCATED (search excerpt only) |

### 2.5 Aberrations, Airy, quadrature sum, Scherzer
| Item | Source | Status |
|---|---|---|
| Cs and Cc of the Glaser lens in units of f (minimum values 0.00359 and 0.00041 for the case computed) | M. A. Mohammed, J. of Wasit Science and Medicine (2022), doi 10.31185/jwsm.92 | LOCATED (excerpt) |
| First- and third-order chromatic aberration of the Glaser lens | A. Amer, A. K. Ahmad (2023), <https://pmc.ncbi.nlm.nih.gov/articles/PMC10731062/> | LOCATED (excerpt) |
| Root-power-sum for probe size (the known weak point of the plain quadrature sum) | J. E. Barth, P. Kruit, "Addition of different contributions to the charged particle probe size", *Optik* **101** (1996) 101–109, record <https://research.tudelft.nl/en/publications/addition-of-different-contributions-to-the-charged-particle-probe/> | LOCATED (abstract: d is the diameter holding a fraction of the current; sum by a root-power-sum algorithm; only exact ray-tracing or wave optics is exact) |
| Airy pattern, d_Airy = 1.22 λ/α; Scherzer's theorem (1936, 1949) | no source opened | NOT OPENED |

### 2.6 Sources
| Item | Source | Status |
|---|---|---|
| Richardson j = A T² exp(−W/kT), Eq. 2.66; table of W and A (W 4.54 eV, A (1.5–15)×10⁵ A m⁻² K⁻², W-Ba 1.66 eV, thorium oxide 2.6 eV, …) | Demtröder §2.5.3 a), p. 37, Table 2.3 | READ |
| Field emission, E = U/r at a tip, 10¹¹ V/m at r < 10 nm and 1 kV | Demtröder §2.5.3 b) p. 37 and §2.2.3 (Fig. 2.24) | READ |
| Schottky lowering Δ = c_S F^(1/2), c_S = (e³/4πε₀)^(1/2); scaled field f = c_S² φ⁻² F (Eq. 4b); b = (4/3)(2m_e)^(1/2)/(eħ) (Eq. 18); a = e³/(8πh) (Eq. 36); D_SN = exp[−v(f) bφ^(3/2)/F] (Eq. 53); J = t(f)⁻² aφ⁻¹F² exp[−v(f) bφ^(3/2)/F] (Eq. 54); v(f) ≈ 1 − f + (1/6) f ln f (Eq. 40, 0.33 % or better for 0 ≤ f ≤ 1, not for f > 4); integral form of v (Eq. 41) | R. G. Forbes, "Field electron emission theory (October 2016)", arXiv:1801.08251v2, §II.F (image potential, SN barrier), §II.I (transmission), §III, §IV.A | READ (equation numbers as printed; the arXiv version carries no printed page numbers) |
| Murphy–Good plot instead of FN plot; first FN plot by Stern, Gossling and Fowler (1929) | R. G. Forbes, "The Murphy–Good plot: a better method of analysing field emission data", arXiv:1905.07585 (2019) | READ (§1–4 and references) |
| The original theory | R. H. Fowler, L. Nordheim, *Proc. R. Soc. A* **119** (1928) 173–181; L. W. Nordheim, *Proc. R. Soc. A* **121** (1928) 626–639; E. L. Murphy, R. H. Good, *Phys. Rev.* **102** (1956) 1464–1473; R. E. Burgess, H. Kroemer, J. M. Houston, *Phys. Rev.* **90** (1953) 515 | NOT OPENED (listed as printed in the reference list of arXiv:1905.07585) |
| Tunnelling through a barrier, T ∝ exp(−2κa) | Biehs §2.5 pp. 51–58 | READ |
| Practical brightness B = 1.44 e j/(kT) (thermionic, Schottky) and a field-emission form (Eqs. 15 and 16 there); reduced brightness = brightness per volt in A m⁻² sr⁻¹ V⁻¹, conserved along the column (Liouville) | M. S. Bronsgeest, J. E. Barth, L. W. Swanson, P. Kruit, "Probe current, probe size, and the practical brightness for probe forming systems", *J. Vac. Sci. Technol. B* (2008), doi 10.1116/1.2907780 | LOCATED (excerpt; the symbol in the field-emission denominator was lost in the excerpt) |
| Table of source properties (work function, temperature, current density, brightness, energy spread, vacuum, life) for W, LaB₆, Schottky and cold FEG | D. B. Williams, C. B. Carter, *Transmission Electron Microscopy*, ch. 5, Table 5.1, copy at <https://iubemcenter.indiana.edu/doc/williams-and-carter/transmission-electron-microscopy-chapter-05.pdf> | LOCATED (the excerpt dropped the exponents; the PDF must be opened before any number is digitised) |
| Field-emission brightness and its space-charge limit | S. Tsujino, *J. Vac. Sci. Technol. B* **40**, 030801 (2022) | LOCATED (excerpt) |
| Hertz–Knudsen flux, Langmuir coverage and sticking | no source opened | NOT OPENED |
| Applied's statements on cold field emission | `applied-public.md` | in progress |

### 2.7 Scattering, stopping, range, yields
| Item | Source | Status |
|---|---|---|
| Rutherford scattering formula | Demtröder §2.8.6, p. 74 | LOCATED (contents; Drive text ends before it) |
| Born approximation, scattering | Griffiths §11.3, p. 363 | LOCATED (contents) |
| Mott cross section deviates strongly from Rutherford at low energy; BSE yield of light elements rises and of heavy falls at low landing energy | Y. Hashimoto, A. Muto, E. Woods, T. Walters, D. C. Joy, *Microscopy Today* (2016), doi 10.1017/S1551929516000390 | LOCATED (excerpt) |
| Database of measured SE and BSE yields and stopping powers | D. C. Joy, "A database on electron–solid interactions", *Scanning* **17** (1995), doi 10.1002/sca.4950170501 (the Wiley record lists the author as "Ashley JC"; the 1995 database is Joy's per the MC-SET note) | LOCATED (abstract) |
| Open database of electron backscattering coefficients, 0.1 keV to 15 MeV, 50 elements and 19 compounds incl. Si, Cu, Au, e-beam PMMA resist and PETEOS: J. I. Goldstein et al., *Med. Phys.* (2023), doi 10.1002/mp.16604, data at doi 10.5281/zenodo.7810951 | | LOCATED (to be downloaded for `data/ch06/`) |
| Bethe stopping power, Kanaya–Okayama range (1972), Everhart–Hoff (1971) | no source opened | NOT OPENED |

### 2.8 Detection and statistics
Shot noise (Poisson, SNR ∝ √N), CD uncertainty, throughput: no source opened yet. Reimer, *Scanning Electron Microscopy*
(Springer 1998, doi 10.1007/978-3-540-38967-5) and Goldstein et al., *Scanning Electron Microscopy and X-Ray Microanalysis*
(Springer 2017, doi 10.1007/978-1-4939-6676-9) are named in search results; not opened.

## 3. Still to do (S2 backlog, in this order)

1. Open Williams & Carter Table 5.1 and digitise (data c).
2. Download the Zenodo BSE database and extract Si, Cu, Au, PMMA (data e); find an open SE-yield source for the same (data e).
3. A measured tungsten FN I–V set (data b): Dyke & Dolan 1956 is not open; look for open reproductions or a thesis table.
4. Reimer or Goldstein for Cs, Cc of SEM objective lenses (data f); Kanaya–Okayama and Everhart–Hoff (data d).
5. Books for L, Boris, Busch, Scherzer, Airy, Hertz–Knudsen, Bethe, shot noise.
6. Applied SEMVision H20 and G7C pages (`applied-public.md`).

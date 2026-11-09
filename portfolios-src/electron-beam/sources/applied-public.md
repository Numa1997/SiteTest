# Applied Materials: public statements, as public claims only

Rule for every chapter and the cover text: these are things Applied Materials has said in public. They are quoted as claims, never
as measured fact, and never as a description of any model in this project. Numa is not affiliated with Applied Materials and the
project does not model its tools.

Checked 9 November 2026. Status: **READ** = I fetched the whole page or release text and read it; **EXCERPT** = I only saw a
search excerpt of it.

## 1. SEMVision H20 (READ)

Page: <https://www.appliedmaterials.com/us/en/product-library/semvision-h20-defect-analysis.html> (fetched whole with Exa
`web_fetch_exa`; `curl` was refused with HTTP 403). The page itself contains **one** number:

- "the number of defect candidates delivered to eBeam review has increased from ten to a hundred-fold" (ten- to a hundred-fold).

Other claims on the page, in words: cold field emission (CFE) eBeam "to enable sub-nanometer resolution of the smallest buried
defects"; "second generation CFE technology that provides faster imaging speed while maintaining the high sensitivity and
sub-nanometer resolution"; deep-learning AI to separate critical defects from "nuisance defects", trainable on the chipmaker's
own defect images or on design simulations; "While the G7 will continue to serve the mature technology nodes, the SEMVision H20
with CFE technology ushers in a new era of complex 3D architecture inflections, including new gate-all-around (GAA)
transistors", and higher-density DRAM and 3D NAND.

Press release, 19 February 2025 (READ whole):
<https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-accelerates-chip-defect-review-next-gen-ebeam>.
Numbers in it:

| Claim as printed | Where |
|---|---|
| "as much as a 100X increase in the number of defect candidates delivered to eBeam review" | para. 3 |
| results "as much as 3X faster than today's most advanced techniques" | para. 6 |
| CFE "Operating at room temperature … produces a narrower beam with more electrons, thereby increasing nanoscale image resolution by up to 50 percent and imaging speed by up to 10X compared to conventional thermal field emission (TFE) technology" | first bullet |
| the second-generation CFE lets chipmakers "gather the same amount of information in one third of the time" | first bullet |
| 2nm node and beyond, GAA transistors, DRAM, 3D NAND | para. 5 |
| the defect classes the AI sorts into: voids, residues, scratches, particles "and dozens of other defect types" | second bullet |

How to use: the "room temperature", "narrower beam with more electrons" and "up to 10X imaging speed" claims sit next to ch. 2
(cold field emission versus Schottky/TFE) and ch. 7 (speed from statistics). The model in this project may be compared with the
*direction* of these claims, not with their size: Applied gives no reference conditions for "10X" or "50 percent".

Investor slides, February 2025, "SEMVision H20 ACCELERATING DEFECT REVIEW" (EXCERPT only, from a search; open before quoting):
<https://appliedmaterials.gcs-web.com/static-files/ab958a2a-5cc3-47c2-a775-4e02ce9bb5dd>. The excerpt shows: optical spot size
"~100nm" against eBeam spot size "~1.5nm"; optical column "~60°" and electron beam "~0.5°" (a convergence angle, on the slide's
sketch); an optical defect map of "~100k candidates"; review times "<0.5 hrs", ">3 hrs" and "<1 hour"; example defects
"10nm buried bridge residue" and "250nm particle defect". The meaning of each number is as the slide gives it; I did not see the
slide pictures.

## 2. SEMVision G7 family and G7C (READ)

Page: <https://www.appliedmaterials.com/us/en/product-library/g7-semvision-defect-analysis.html> (fetched whole). This page covers
the G7 family; G7C is its "latest member". The page contains **no numbers**. Claims in words:

- the family has "high resolution and advances in automatic defect review (ADR) and automatic defect classification (ADC)";
- "unique e-lluminator technology, an industry standard for back-scattered electron see-through imaging";
- "an electronic beam tilt and high depth of focus is used to detect defects in high aspect ratio and 3D structures";
- "Purity ADC"; classification from SEM images and CAD data; wafer-edge bevel and apex imaging, un-patterned wafer review, material analysis;
- G7C: "specifically designed to support emerging compound semiconductor markets and specialty devices through its automatic
  handling of different wafer types and thicknesses—SiC, GaN, GaAs and more", with "high-resolution imaging and in-depth
  information of surface and sub-surface crystallographic defects".

Neighbouring family page (EXCERPT): SEMVision G7AP for advanced packaging,
<https://www.appliedmaterials.com/us/en/product-library/semvision-g7ap-defect-analysis.html>: "eTilt with full azimuth control".

A secondary report, not Applied's own page: ELE Times, 5 November 2024, "Bringing eBeam Review to Compound Semiconductors"
(<https://www.eletimes.ai/bringing-ebeam-review-to-compound-semiconductors>, EXCERPT) says the beam in G7C "can be electronically
tilted by up to 10 degrees" and that Elluminator uses a wide-angle detector. The 10° figure is therefore second-hand; find
Applied's original text before using it.

## 3. Verified earlier by the planning session (PLAN.md section 3), not re-read by me

- PROVision 10 page <https://www.appliedmaterials.com/us/en/product-library/provision-10-ebeam-metrology.html>: cold field emission
  column, "up to 100 million accurate, actionable measurements per hour", Elluminator "captures 95% of back-scattered electrons",
  high-energy modes "hundreds of nanometers deep", low-energy modes for EUV resist.
- Press release 14 December 2022 (Semiconductor Digest,
  <https://www.semiconductor-digest.com/applied-materials-breakthrough-in-electron-beam-imaging-technology-accelerates-development-of-the-worlds-most-advanced-computer-chips/>):
  TFE runs above 1500 °C; CFE a narrower beam and 10× imaging speed; vacuum "well below 1×10⁻¹¹ millibar" (= 10⁻⁹ Pa), two to three
  orders better than TFE; "a single atom" on the tip can partly block emission; cyclical self-cleaning.

Note for the reader of these numbers: the 2025 release says 10X imaging speed and 50 percent resolution; the 2022 release says
10× imaging speed. Both compare CFE with TFE and give no conditions.

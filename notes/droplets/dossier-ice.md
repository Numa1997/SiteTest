# Dossier: collisional ice multiplication in the cold case (-10 C, 600 hPa)

Scout dossier, 2026-10-23. Question: which collisional processes make new ice particles, at what measured rate, over which
temperatures and sizes, and what would each give in a cloud with about 134 cm^-3 droplets and 167 cm^-3 ice (modelled as spheres,
8 um to a few hundred um), colliding by differential fall at -10 C?

Tags used below. [derived] = I computed it myself from numbers in a source. [secondary] = I know it only through another paper.
[memory] = from my own recollection, not checked against any page I opened.

---

## 0. Bottom line

1. Only two of the seven sources could be read in the body: Phillips et al. 2017 (text, but the equations and Table 1 did not render) and
   Korolev and Leisner 2020 (open access, read in full up to the concluding remarks). Hallett and Mossop 1974, Mossop 1976, Takahashi et al. 1995
   and the body of Vardiman 1978 and Field et al. 2017 could not be opened. Their numbers below are [secondary], mostly through Korolev and Leisner.
2. Hallett-Mossop rime splintering is measured only between -8 and -3 C (peak -5 C, about one splinter per 250 captured droplets larger than 24 um
   in diameter [secondary]). At -10 C the measured yield is zero. -10 C is outside its range.
3. Droplet shattering on freezing is the only mechanism that is measured at -10 C: 1 to 37 percent of freezing drops of 50 to 350 um break up,
   with 3 to 12 fragments at most per drop (Korolev and Leisner Table 1). It needs a drop of about 50 um or more that freezes. Spheres of ice do not make it.
4. Ice-ice breakup (Phillips et al. 2017 formula, fitted to Takahashi et al. 1995 and Vardiman 1978) has no lower temperature limit. But it was fitted to particles
   of 0.5 to 5 mm and, for Takahashi, to collision energies of about 1e-4 to 1e-2 J. Our spheres of 50 to 200 um radius at 0.1 to 1 m/s carry 1e-12 to 8e-9 J.
   That is 4 to 9 orders of magnitude lower. Extrapolated with the published coefficients, the formula gives [derived] 6e-4 to 0.26 fragments per collision
   (about 0.003 to 0.06 for r = 100 um). Treat that as an upper-bound extrapolation, not a measurement.
5. Rates in ice particles per cm^3 per minute cannot be fixed without the size distribution. Section 5 gives the formula and a table
   against the collision frequency per ice particle. Korolev and Leisner conclude that no quantitative parameterisation of ice-ice breakup is possible yet.

---

## 1. Access log (what I actually opened)

| Source | Link tried | Result |
|---|---|---|
| Korolev and Leisner 2020, ACP 20, 11767-11797 | https://acp.copernicus.org/articles/20/11767/2020/acp-20-11767-2020.pdf | Opened. Read from the abstract through Sect. 9.1 (about 120,000 characters). References and rest of Sect. 9 not read. |
| Phillips, Yano, Khain 2017, JAS 74, 1705-1719, doi:10.1175/JAS-D-16-0224.1 (note: this is the correct DOI; the one I first guessed, JAS-D-16-0306.1, was wrong) | https://journals.ametsoc.org/view/journals/atsc/74/6/jas-d-16-0224.1.xml | Opened as HTML. Full prose read (Sects. 1-6, figure captions). Equations and Tables 1 and 2 are "View Expanded" links and did not render. |
| Vardiman 1978, JAS 35, 2168-2180, doi:10.1175/1520-0469(1978)035<2168:TGOSIP>2.0.CO;2 | https://journals.ametsoc.org/view/journals/atsc/35/11/1520-0469_1978_035_2168_tgosip_2_0_co_2.xml | Abstract only. |
| Field et al. 2017, Meteor. Monogr. 58, 7.1-7.20, doi:10.1175/AMSMONOGRAPHS-D-16-0014.1 | https://journals.ametsoc.org/view/journals/amsm/58/1/amsmonographs-d-16-0014.1.xml | Page opened, but only section titles and the reference list came back. Body text not read. |
| Hallett and Mossop 1974, Nature 249, 26-28, doi:10.1038/249026a0 | https://www.nature.com/articles/249026a0 | Fetch returned nothing. Not read. Reference confirmed from the Field et al. reference list. |
| Takahashi, Nagao, Kushiyama 1995, JAS 52, 4523-4527 | AMS view URL and doi.org URL | Fetch returned nothing. Not read. |
| Mossop 1976; Mossop and Hallett 1974 | not tried (call budget) | Not read. |
| Extra: Grzegorczyk et al. 2023, ACP 23, 13505-13521 | https://acp.copernicus.org/articles/23/13505/2023/ | Opened (open access). Most of the text read. Newer lab data at -15 C and low energies, and the clearest printed copy of Phillips Eq. 13. |
| Extra: Sotiropoulou, Ickes, Nenes, Ekman 2021, ACP 21, 9741-9760 | https://acp.copernicus.org/articles/21/9741/2021/ | Opened (open access). Appendix B prints the Phillips coefficients (the maths came through garbled; see Sect. 3.5). |
| Extra: Phillips slides, Lund, 25 Oct 2017 | https://www.smhi.se/download/18.2921e83919a90b687028a2/1763456891479/Philips_Ice.pdf | Opened. Overview only, no coefficients. |

Tool notes: the Firecrawl scrape tool had no credits. AMS PDF downloads by curl return HTTP 202 with an empty body (bot challenge). Opened pages came through Exa fetch.

---

## 2. Collision energies for the cold case [derived]

Phillips et al. define the collision kinetic energy K0 as the total translational kinetic energy relative to the centre of mass. For two bodies of masses
m1, m2 and relative speed v that is K0 = (1/2) [m1 m2 / (m1 + m2)] v^2. (Sotiropoulou's Appendix B prints the product m1 m2/(m1+m2) times the squared speed with no visible 1/2;
that may be a conversion loss. A missing factor 2 changes N by only 2^gamma = 1.2 to 1.4 for the coefficients below.)

Ice spheres, density 917 kg/m^3, equal pairs, so K0 = m v^2 / 4. alpha = pi D^2 is the surface area of the smaller sphere.

| radius r (um) | D (um) | mass m (kg) | alpha (m^2) | K0 at v = 0.1 m/s (J) | K0 at v = 1 m/s (J) |
|---|---|---|---|---|---|
| 50 | 100 | 4.80e-10 | 3.14e-8 | 1.2e-12 | 1.2e-10 |
| 100 | 200 | 3.84e-9 | 1.26e-7 | 9.6e-12 | 9.6e-10 |
| 200 | 400 | 3.07e-8 | 5.03e-7 | 7.7e-11 | 7.7e-9 |

Energies of the experiments, for comparison:

| Experiment | Particles | K0 range | Source |
|---|---|---|---|
| Takahashi et al. 1995 | two ice spheres of about 2 cm (1.8 cm per Grzegorczyk), 4 m/s at most | about 5e-4 to 5e-3 J for 200 to 450 fragments [secondary, Grzegorczyk]; I estimate about 1e-2 J for two solid 2 cm spheres at 4 m/s [derived] | K&L, Phillips, Grzegorczyk |
| Grzegorczyk et al. 2023 | 2 mm and 4 mm graupel; 10 mm snowflake | 1e-7 to 2e-5 J | Grzegorczyk |
| Vidaurre and Hallett 2009 (as plotted by Phillips Fig. 3b) | crystals of 10 to 300 um hitting a replicator at 130 m/s | per area, not total. For r = 100 um at 130 m/s I get about 3e-5 J, i.e. about 260 J/m^2 [derived] | Phillips |
| Our cold case, r = 50 to 200 um, v = 0.1 to 1 m/s | ice spheres | 1.2e-12 to 7.7e-9 J, i.e. 7.6e-3 J/m^2 for r = 100 um at 1 m/s [derived] | this dossier |

So our energy per unit area is about 3e4 times lower than in the one data set that used particles of our size, and that data set was taken at aircraft speed, where Korolev and Leisner Sect. 8 warn of instrument shattering.

---

## 3. Sources

### 3.1 Hallett and Mossop 1974

Hallett, J. and Mossop, S. C. (1974), Production of secondary ice particles during the riming process, Nature 249, 26-28, doi:10.1038/249026a0.
Link: https://www.nature.com/articles/249026a0 (not opened). Everything below is [secondary], from Korolev and Leisner 2020 Sect. 3, Table 2, Fig. 11.

Establishes (paraphrased):
- Splinters came off a rimer in a cloud chamber with liquid water content about 1 g/m^3 and about 500 droplets per cm^3.
- Production is active for air temperatures between -8 and -3 C, with a sharp maximum at -5 C.
- At the maximum, one splinter formed per about 250 accreted droplets larger than 24 um diameter.
- Impact speeds studied were 0.7 to 3.1 m/s. Korolev and Leisner give the speed of the maximum as 2.5 m/s in the text, 1.5 m/s in Table 2, and 2.7 m/s in the Fig. 11 caption. They disagree with each other.
- Table 2 of Korolev and Leisner lists a maximum of about 700 splinters per mg of rime. [memory] The value usually coded in cloud models is about 350 per mg; I could not check which one the Nature paper states.

Numbers we may use, with conditions:

| Quantity | Value | Condition |
|---|---|---|
| Temperature window | -8 to -3 C, peak -5 C | droplets near water saturation, rimer surface near air temperature |
| Splinters per captured droplet | 1/250 = 4e-3 | droplet D > 24 um, at the peak only |
| Splinters per mg of rime | 350 [memory] to 700 [secondary] at -5 C | cloud-chamber spectrum |
| Check [derived] | one droplet of D = 24 um has mass 7.2e-12 kg, so 1 mg is 1.4e5 droplets, and 4e-3 per droplet gives about 550 per mg | agrees in order with the 550 to 700 printed |

Conditions added by later work (all [secondary], from K&L): droplets smaller than 12 um in addition to those larger than 24 um raise production (Mossop 1978, 1985b).
Wet growth beyond the Ludlam limit suppresses it. Warming the rimer surface by 1 C shifts the curve to air temperatures 1 C colder (Heymsfield and Mossop 1984), so splintering
at air temperatures below -8 C is possible if the rimer surface is warmer than the air. Saunders and Hosseini (2001) found a maximum at 6 m/s with about 5 times fewer splinters.

Does not establish: any splinters at -10 C air temperature; any behaviour below 0.7 m/s; behaviour at 600 hPa; behaviour for rimers as small as 50 to 200 um radius;
the physical mechanism (Korolev and Leisner call it "still under debate").

### 3.2 Mossop 1976 and Mossop and Hallett 1974

Mossop, S. C. (1976), Production of secondary ice particles during the growth of graupel by riming, Q. J. R. Meteorol. Soc. 102, 45-57 [reference from memory; verify]. Mossop, S. C. and
Hallett, J. (1974), Ice crystal concentration in cumulus clouds: influence of the drop spectrum, Science 186, 632-634 [from memory; verify]. Neither opened. [secondary] via K&L Table 2 and Sect. 3.

- Mossop 1976 row of K&L Table 2: droplets 3 to 45 um, air temperature -5 C, impact speed 1.4 to 3 m/s, maximum about 550 splinters per mg of rime, i.e. the same "one splinter per 250 droplets larger than 24 um".
- Droplet-size condition: droplets larger than about 24 um are needed. The yield rises if droplets below about 12 um are also present.
- K&L report four mechanisms proposed by Mossop (1976): shell cracking after freezing, detachment of droplets in glancing contact, growth and breaking of frail needles near -5 C, and detachment by evaporation.
- Mossop et al. (1974) saw 0.24 splinters per mg at -8 and -10 C for a rimer with droplets of 15 and 50 um at 0.8 m/s (K&L Table 2, row "Mossop et al. 1974", reading of the garbled row: 15 + 50 um, -8 and -10 C, 0.8 m/s, 0.24). If I have read that row correctly, it is the only measurement near -10 C and it is essentially zero. I could not confirm the reading.

Does not establish: yield at -10 C with certainty; anything for 50 to 200 um rimers.

### 3.3 Vardiman 1978

Vardiman, L. (1978), The generation of secondary ice particles in clouds by crystal-crystal collision, J. Atmos. Sci. 35, 2168-2180,
doi:10.1175/1520-0469(1978)035<2168:TGOSIP>2.0.CO;2. Link opened (abstract only): https://journals.ametsoc.org/view/journals/atsc/35/11/1520-0469_1978_035_2168_tgosip_2_0_co_2.xml

Establishes (abstract, paraphrased): fragments per collision were found by high-speed photography of natural ice crystals hitting a fixed plate, as a function of the change of momentum
on impact, of crystal type and of the degree of riming. A model combines that with the collision frequency. Mechanical fracturing alone does not explain large ice concentrations in warm clouds.
The model gives at most about 10 times the natural crystal concentration in smooth stratiform cloud near cloud base, little in isolated convective clouds, and 100 to 1000 times in stratiform cloud
with embedded convection.

From other papers [secondary]: K&L Sect. 4 quote Vardiman that "graupel is surprisingly ineffective in generating fragments"; lightly to moderately rimed spatial crystals were the best source, and for planar
crystals fragments rise with riming. Phillips et al.: field site on a Colorado mountain in late autumn and winter, altitudes 5,000 to 11,300 ft; dendrites, spatial (planar polycrystal or sector-plate) crystals and graupel;
mean coefficient of restitution of graupel 0.37; observed counts never exceeded 100 per collision; errors a factor 2; target was a hard non-ice plate; particles about 0.5 to 5 mm; fragments about 3 orders of magnitude lighter than their parent;
Vardiman's fragments are inflated by sublimation outside cloud, which Phillips corrects by a factor (psi = 3.5e-3, see Sect. 3.5).

Numbers we may use: none directly. The fragment generation function itself (fragments against momentum change) is in the body, which I did not read.

Does not establish (from what I read): any value at -10 C (temperatures are not in the abstract or in the secondary accounts); anything for spheres or for particles below 0.5 mm; collisions between two free particles.

### 3.4 Takahashi, Nagao, Kushiyama 1995

Takahashi, T., Nagao, Y. and Kushiyama, Y. (1995), Possible high ice particle production during graupel-graupel collisions, J. Atmos. Sci. 52, 4523-4527.
Link tried: https://doi.org/10.1175/1520-0469(1995)052<4523:PHIPDG>2.0.CO;2 (not opened). All below is [secondary].

- Setup (K&L Sect. 4): rimed ice spheres of 2 cm (Grzegorczyk: 1.8 cm) on the ends of spinning 10 cm rods, colliding at up to 4 m/s. Collision force raised from 2e-4 to 5e-3 N (20 to 500 dyn). Humidity near water saturation (Phillips).
- Result: the number of fragments depends on degree of riming, temperature and collision force. K&L: up to 800 per collision at -16 C. Phillips: no count above 1000; mean varies by up to a factor 3 with temperature, with a broad peak near -15 C, and rises to an upper limit as the force grows (their Figs. 1 and 2).
- Takahashi's explanation (Phillips p. 4526 reference): vapour-grown branches on the stationary unrimed sphere break on impact, and are favoured in the dendritic regime.
- Criticism (K&L): the mass and contact area of 2 cm spheres far exceed natural graupel of a few mm; riming in still air gives lumpier, more fragile rime; so the lab fragment numbers are probably too high for nature. Phillips answers that his energy-based fit corrects this.

Is -10 C inside the measured range? I could not read the range. From Phillips Fig. 1 (a triangle peaking near -15 C) it probably lies on the shoulder, with fragment numbers lower than the peak by up to about 3. Verify against the paper.

Does not establish: anything at K0 below about 1e-4 J; anything for particles below 1 cm; anything for naturally rimed free-falling graupel.

### 3.5 Phillips, Yano, Khain 2017 (Part I)

Phillips, V. T. J., Yano, J.-I. and Khain, A. (2017), Ice multiplication by breakup in ice-ice collisions. Part I: Theoretical formulation, J. Atmos. Sci. 74, 1705-1719, doi:10.1175/JAS-D-16-0224.1.
Link opened: https://journals.ametsoc.org/view/journals/atsc/74/6/jas-d-16-0224.1.xml (prose only). Part II, 10.1175/JAS-D-16-0223.1, was seen as an abstract only.

Establishes (paraphrased): collision kinetic energy is the controlling variable for how many fragments an ice-ice collision makes, because new surface costs energy ("collision kinetic energy (CKE) is the fundamental governing variable of fragmentation").
The number of fragments equals the number of breakable branches in the contact area times the probability that a branch breaks; that probability follows from a Weibull-type distribution of breaking energies. The theory is fitted to Takahashi et al. 1995 (hail, type I)
and to Vardiman 1978 (crystals and graupel against a plate, types II and III), and to the Vidaurre and Hallett 2009 replicator data in Fig. 3b. Collision types: I graupel (< 0.5 cm) or hail (> 0.5 cm) with graupel/hail;
II crystals or snow with graupel/hail; III crystals or snow with crystals or snow. Crystals are < 0.3-0.5 mm, snow larger; rime mass fraction above 0.5 makes graupel.

**Formula (Eq. 13)**, as printed in Grzegorczyk et al. 2023 Eq. 2 (the AMS page lost the maths) and in Sotiropoulou et al. 2021 Eq. B5 [secondary]:

    N = alpha A [ 1 - exp( - ( C K0 / (alpha A) )^gamma ) ]

alpha = surface area of the smaller particle (equivalent sphere, pi D^2); A = number density of breakable asperities per unit area; C = asperity-fragility coefficient (1/J); gamma = shape exponent; K0 = collision kinetic energy.
For C K0 / (alpha A) small the formula is a power law N = (alpha A)^(1-gamma) (C K0)^gamma [derived], so N rises as K0^gamma. For large K0, N tends to alpha A.

**Caps and ranges** (from the Phillips text): N is capped at 1000 for type I (Takahashi never saw more) and at 100 for types II and III (Vardiman never saw more). Sotiropoulou applies 100 to all.
The scheme "may be applied to any permutation of sizes", but the size D entering A is held between 0.5 and 5 mm (range of the polynomial fit), and rime fraction between 0 and 0.5; outside these limits the input is set to the nearest limit. Fragments are about 1e-3 of the mass of the more fragile parent
(Phillips text: about three orders smaller; Sotiropoulou: 0.1 percent), and are added to cloud ice if smaller than 0.3-0.5 mm. If habits are not resolved, treat crystals and snow as dendrites between -12 and -17 C and as spatial planar particles at all other subzero temperatures. All collisions are counted, whether the particles stick or rebound.

**Coefficients.** Table 1 of the paper did not render. The values below are as printed in Sotiropoulou et al. 2021, Appendix B, which says it implements Phillips et al. 2017a [secondary]. The converted maths is garbled, so two things are my reading, marked [derived reading]:

| Collision type | A (m^-2) | C (J^-1) | gamma |
|---|---|---|---|
| planar crystals and snow (all T except -12 to -17 C), rime fraction psi_r < 0.5 | 1.58e7 (1 + 100 psi_r^2) with the factor (1 + 1.33e-4 D^1.5) either multiplying or dividing [cannot tell from the text] | 7.08e6 x 3.5e-3 = 2.5e4 | 0.5 - 0.25 psi_r |
| dendrites (-12 to -17 C) | 1.41e6 (1 + 100 psi_r^2) with (1 + 3.98e-5 D^1.5) multiplying or dividing [same doubt] | 3.09e6 x 3.5e-3 = 1.1e4 | 0.5 - 0.25 psi_r |
| graupel-graupel and hail (type I) | A = a0/3 + max( 2 a0/3 - (a0/9) abs(T - 258 K), 0 ), a0 = 3.78e4 (1 + 0.0079 D^1.5) [derived reading] | 6.3e6, possibly times 3.5e-3 = 2.2e4 [the printed line does not show the product] | 0.3 |

Notes on the reading. The 3.5e-3 factor (called psi in Sotiropoulou) is Phillips's correction for sublimation weakening in Vardiman's data. D is evidently in micrometres: with D in metres the bracket (1 + 0.0079 D^1.5) is 1 and a0 = 3.8e4, far below any measured A,
whereas with D in um a0 is 3e6 to 1e8 m^-2 for D = 0.5 to 5 mm, the same order as the 2e7 to 1.9e8 fitted by Grzegorczyk. The triangle in T reproduces Phillips's statement of a broad peak near -15 C (258 K) and a drop by a factor 3 (floor a0/3, reached at |T - 258| >= 6 K, i.e. warmer than -9 C or colder than -21 C).
At -10 C (263.15 K) the factor is 1/3 + 2/3 - 5.15/9 ... = 0.428 [derived].

Validity and caveats given by the authors: the scheme is uncertain by at least a factor 2; the fixed-target lab and field tests prevented glancing collisions and rotation, which probably overstates fragmentation; the Takahashi sphere was a smooth non-rimed sphere with vapour-grown branches, so
its use for rimed natural graupel is unproven; rime fraction was not measured in either experiment; Vardiman's counts need a sublimation correction of uncertain size. Phillips et al. report in Part II that, in a simulated storm with cold base, collisions of snow with graupel/hail make most
non-homogeneous ice (60 to 90 percent).

Does not establish: any fragment count at K0 below about 1e-7 J; any count for D < 0.5 mm; anything for spheres of pure ice without branches; and the coefficient set is not confirmed against Table 1 (needs the paper).

### 3.6 Field et al. 2017

Field, P. R. et al. (2017), Secondary ice production: current state of the science and recommendations for the future, Meteor. Monogr. 58, 7.1-7.20, doi:10.1175/AMSMONOGRAPHS-D-16-0014.1.
Link: https://journals.ametsoc.org/view/journals/amsm/58/1/amsmonographs-d-16-0014.1.xml (only the section list and references came back; body not read).

Seen: section titles 2 ("Laboratory evidence for SIP": a. rime splintering and the Hallett-Mossop process; b. other SIP mechanisms) and 5 ("Modeling": representation in models; sensitivity of simulated cloud physics to SIP;
model studies using non-rime-splintering SIP; importance for weather and climate). From other papers [secondary]: Grzegorczyk 2023 cites Field et al. for a "scientific consensus" that secondary ice production explains the gap between ice nucleating particles and ice crystals;
K&L say Field et al. is an in situ and modelling review while they themselves cover the laboratory work.

I cannot report their statements about -10 C or their rates. Open question.

### 3.7 Korolev and Leisner 2020

Korolev, A. and Leisner, T. (2020), Review of experimental studies of secondary ice production, Atmos. Chem. Phys. 20, 11767-11797, doi:10.5194/acp-20-11767-2020.
Link opened: https://acp.copernicus.org/articles/20/11767/2020/acp-20-11767-2020.pdf

Establishes (paraphrased): six mechanisms: (1) fragmentation of freezing drops, (2) rime splintering (Hallett-Mossop), (3) ice-ice collisional breakup, (4) thermal shock, (5) fragmentation of sublimating ice, (6) ice nucleating particle
activation in transient supersaturation around freezing drops. Different groups get inconsistent rates for (1) and (2), and (3) rests on only two lab studies that disagree. Quote: "No parameterizations of SIP due to ice-ice collisional fragmentation can be developed" (at that stage).

Numbers we may use:

**Freezing drops (Sect. 2, Table 1).** Condensed from their Table 1 (the converted table has shifted columns; read with care):

| Study | Drop D (um) | Air T (C) | Suspension | Max share of drops that shatter | Max fragments per drop | T of maximum (C) |
|---|---|---|---|---|---|---|
| Mason and Maybank 1960 | 30-1000 | +2 to -25 | fibre | 47 % | 200 | -10 |
| Brownscombe and Thorndike 1968 | 50-90 | -5, -10, -15 | free fall | 14 % | 12 | -15 |
| Takahashi and Yamashita 1970 | 75-350 | 0 to -30 | free fall | 37 % | n/a | -15 |
| Takahashi 1975 | 45-765 | -4 to -24 | free fall | 35 % | n/a | -16 |
| Pruppacher and Schlamp 1975 | 410 | -7 to -23 | airflow | 15 % | > 3 | -11 to -15 |
| Kolomeychuk et al. 1975 | 1600 | -12 to -25 | airflow | 35 % | 142 | -15 to -18 |
| Lauber et al. 2018 | 300-320 | -5 to -30 | stagnant, levitated | 35 % (table; text says about 12 % for breakup) | 12 | -7 to -13 |
| Keinert et al. 2020 | 300-320 | -1 to -30 | stagnant / ventilated | 1 % stagnant (about 25 % ventilated, text) | 3 | -10 to -15 |
| Adkins 1960; Dye and Hobbs 1968 | 4-13; 1000 | various | | 0 | 0 to 1 | none |

Text points: large drops shatter more than small; Takahashi (1975): at -20 < T < -7 C free-falling drops of 75 to 135 um shatter most, at -4 C drops of 50 to 200 um do not shatter; maximum shattering between -10 and -20 C for 85 to 350 um (Takahashi and Yamashita 1970, Lauber 2018);
drops under 50 um cannot shatter if they freeze symmetrically (Wildeman et al. 2017 theory); no shattering seen below 10, 38 or 50 um in three studies; results depend strongly on ventilation, nucleation temperature, single or polycrystal freezing, dissolved CO2, and pressure
(every drop shattered below 0.13 atm in one study). Fragments per shattering event range from zero to a few hundred under the same conditions. Pruppacher and Klett (via Phillips): usually below 10 splinters per freezing drop.

**Rime splintering (Sect. 3, Table 2).** See Sect. 3.1 and 3.2 above. Other rows: Latham and Mason 1961, up to 14 splinters per 70 um droplet at 10 m/s and -15 C (older, disputed because of CO2); Bader et al. 1974, droplets of 56 and 100 um at -15 to -9 C
give 5 and 10 splinters per mg; Hobbs and Burrows 1966 and Aufdermaur and Johnson 1972 found none; Emersic and Connolly 2017 saw no splintering in about 1300 droplet freezing events on ice at HM temperatures.

**Ice-ice breakup (Sect. 4).** As in Sects. 3.3 and 3.4 above. K&L point out that central-impact energy and momentum arguments overestimate fragmentation for oblique collisions, that the Takahashi spheres were far larger than graupel, and that
in situ fragments may be sampling artefacts (Sect. 8: concentrations of particles below 200 um can be inflated by up to 2 orders of magnitude by shattering at the probe tip).

**Others (Sects. 5-7).** Thermal shock: inconclusive; King and Fletcher say unlikely at T > -5 C. Sublimation breakup: needs subsaturated air and elongated or rimed particles, so unlikely in a water-saturated mixed-phase cloud. Activation of nuclei near freezing drops: not quantified.

Does not establish: a rate per collision for ice spheres of tens of um, any rate at 600 hPa, or a single recommended parameterisation for any mechanism.

### 3.8 Two extra papers that bear directly on our case

**Grzegorczyk, Yadav, Zanger, Theis, Mitra, Borrmann and others (2023)**, ACP 23, 13505-13521, doi:10.5194/acp-23-13505-2023. Lab at -15 C, water supersaturation, still air. Graupel of 2 mm falling onto/against 4 mm graupel with grown dendrites: 150 to 600 fragments per collision at K0 = 1e-7 to 1e-5 J; bare rimed graupel pairs: about 20; graupel on a 10 mm dendrite snowflake: 70 to 500. Fragment sizes peak at 75 um for graupel pairs, 400 um for snowflakes.
Re-fits of Phillips Eq. 13: graupel with dendrites A = 1.9e8 m^-2, C = 1e8 J^-1, gamma = 0.78; graupel and snowflake A = 2e7 m^-2, C = 5.9e8 J^-1, gamma = 0.78. They say the original Phillips parameters would give fewer than 20 fragments at their energies, and that the refit is uncertain outside the measured K0.
The rise of fragment number with K0 is therefore very sensitive to the surface condition (bare rime against dendrites differ by about 30 times at the same energy).

**Sotiropoulou et al. (2021)**, ACP 21, 9741-9760. Applies the Phillips scheme in a large-eddy model of a high-Arctic cloud at -9.5 to -12.5 C (close to our case). Result: breakup is weak in those conditions because the extra ice is offset by more precipitation and sublimation; a few runs gave explosive multiplication. They state that the lab data used for the scheme do not represent in-cloud conditions. Appendix B also gives a correction for near-equal fall speeds: effective relative speed = 1.7 [ (u1 - u2)^2 + 0.3 u1 u2 ]^(1/2) [secondary, reading of garbled formula; after Mizuno et al. 1990 and Reisner et al. 1998].

---

## 4. Mechanism by mechanism for small ice spheres at -10 C

Our conditions: ice spheres of 50 to 200 um radius, relative speed 0.1 to 1 m/s, -10 C, 600 hPa.

| Mechanism | Measured T range | Is -10 C inside? | Measured sizes | Measured energy or speed | Yield for our case | Status |
|---|---|---|---|---|---|---|
| Hallett-Mossop rime splintering | -8 to -3 C, peak -5 C | No (2 C outside; only if rimer surface runs warmer than air, Heymsfield and Mossop 1984) | rime droplets > 24 um (plus < 12 um) | 0.7 to 3.1 m/s | 0 at -10 C. At -5 C: 4e-3 per captured droplet > 24 um [secondary] | outside range |
| Shattering of freezing drops | about -4 to -30 C; peak -10 to -20 C for 85 to 350 um | Yes, warm edge of the peak | drops of about 50 um and larger (none below 10 to 50 um) | free fall, ventilated | per freezing drop 0.03 to 1.7 fragments [derived from K&L Table 1 maxima: share x fragments, 1 % x 3 to 14 % x 12] | in range for droplets, not for ice spheres |
| Ice-ice breakup, Phillips fit to Takahashi and Vardiman | any subzero T; Takahashi peak -15 C, factor up to 3 lower elsewhere | Probably (shoulder of the peak; range not read) | 0.5-5 mm (Phillips); 2 cm (Takahashi) | K0 about 1e-4 to 1e-2 J (Takahashi); 1e-7 to 2e-5 J (Grzegorczyk) | 6e-4 to 0.26 fragments per collision [derived, extrapolated 4 to 9 decades below the data] | out of range in size and energy |
| Vardiman-type crystal fragmentation | winter Colorado, T not read | unknown | crystals about 1 mm | terminal speed against a fixed plate | not applicable to spheres | not applicable |
| Thermal shock; sublimation breakup; nuclei activation near freezing drops | n/a | n/a | n/a | n/a | not quantified (K&L) | no usable rate |

### 4.1 Ice-ice breakup numbers [derived]

Type I (graupel-graupel) coefficients from Sect. 3.5 at -10 C; D for A held at 0.5 mm as the scheme prescribes: a0 = 3.78e4 x (1 + 0.0079 x 500^1.5) = 3.38e6 m^-2, A(-10 C) = 0.428 a0 = 1.44e6 m^-2, gamma = 0.3.
Two choices of C: (a) 6.3e6 J^-1 (hail-like, no sublimation factor) and (b) 6.3e6 x 3.5e-3 = 2.2e4 J^-1 (with the factor). N per collision for equal spheres:

| r (um) | alpha A (max fragments, the saturation level) | v (m/s) | K0 (J) | N with C = 6.3e6 | N with C = 2.2e4 |
|---|---|---|---|---|---|
| 50 | 0.045 | 0.1 | 1.2e-12 | 0.0032 | 0.0006 |
| 50 | 0.045 | 1 | 1.2e-10 | 0.012 | 0.0024 |
| 100 | 0.18 | 0.1 | 9.6e-12 | 0.016 | 0.0030 |
| 100 | 0.18 | 1 | 9.6e-10 | 0.055 | 0.012 |
| 200 | 0.73 | 0.1 | 7.7e-11 | 0.077 | 0.015 |
| 200 | 0.73 | 1 | 7.7e-9 | 0.26 | 0.057 |

Reading the table: for particles this small, alpha A is below 1, so even at infinite energy the formula gives less than one fragment per collision for r < about 200 um. Holding D at 0.5 mm in A overstates A for smaller particles (using the actual D lowers A by 1.4 to 10 times and N by up to about 5 times) [derived].
Using planar-crystal coefficients (rime fraction 0, gamma = 0.5, C = 2.5e4) for r = 100 um at 1 m/s gives 0.004 to 0.011 depending on whether the D-factor multiplies or divides A [derived]. A missing factor 2 in K0 changes N by 20 to 40 percent. The authors give a factor 2 uncertainty on N in the fitted range alone.

### 4.2 Rime splintering if the temperature were -5 C [derived scenario, not for -10 C]

Assume 10 cm^-3 droplets of 30 um diameter, ice spheres of r = 100 um falling at 0.7 m/s relative, collection efficiency 0.5. Droplet captures per ice particle: 10 cm^-3 x 4.2e-4 cm^2 x 70 cm/s x 0.5 = 0.15 per second.
With 4e-3 splinters per capture and 167 ice particles per cm^3 that is about 0.10 splinters per cm^3 per second, or about 6 per cm^3 per minute, at -5 C. At -10 C the measured value is zero. The assumed droplet number, efficiency and speed are mine, and the yield at 0.7 m/s is at the very bottom of the measured speed range.

---

## 5. What each would add to the cloud (ice particles per cm^3 per minute)

General form: new ice per volume and time = (fragments per collision) x (collisions per volume and time).
For ice-ice collisions, collisions per volume and time = (1/2) n_ice f_c, where f_c is the number of collisions an average ice particle suffers per second (each collision counted once).
With n_ice = 167 cm^-3 and 60 s per minute: rate = N x 5010 x f_c  cm^-3 min^-1 [derived].

f_c depends on the size distribution, which I do not have: f_c = sum over partners n_b pi (r_a + r_b)^2 E |v_a - v_b|. For r_a + r_b = 150 um and 0.5 m/s, f_c = 1 per second needs about 29 cm^-3 of partners with E = 1 (about 290 cm^-3 if E = 0.1) [derived].
Equal spheres have no differential fall, so most of the 167 cm^-3 (the small ones) hardly collide.

| N per collision (from Sect. 4.1) | f_c = 0.01 per s | f_c = 0.1 per s | f_c = 1 per s |
|---|---|---|---|
| 0.003 (r = 50 um, 0.1 m/s) | 0.16 | 1.6 | 16 |
| 0.016 (r = 100 um, 0.1 m/s) | 0.8 | 8 | 79 |
| 0.055 (r = 100 um, 1 m/s) | 2.8 | 28 | 275 |
| 0.26 (r = 200 um, 1 m/s) | 13 | 130 | 1300 |

These are upper-bound extrapolations. Figures in the last column would double the ice count in under a minute and are not credible; they show how strongly the answer depends on f_c.

Mechanism by mechanism:

| Mechanism | Cloud rate at -10 C |
|---|---|
| Hallett-Mossop | 0 (outside the measured window); about 6 cm^-3 min^-1 under the Sect. 4.2 scenario if it were -5 C |
| Drop shattering | F x (0.03 to 1.7), where F is the number of drops of 50 um or more that freeze per cm^3 per minute (not known; e.g. F = 1 gives 0.03 to 1.7 cm^-3 min^-1) [derived] |
| Ice-ice breakup, 50-200 um spheres | N x 5010 x f_c, see table; formula is an extrapolation |
| Vardiman, thermal shock, sublimation, nuclei activation | no usable rate |

---

## 6. Open questions

1. Phillips et al. 2017 Table 1: the true coefficients and the units of D. Confirm whether the factor (1 + 1.33e-4 D^1.5) multiplies or divides A, whether the graupel C includes the sublimation factor 3.5e-3, and the exact K0 definition (is the factor 1/2 in Eq. 1?). Needs the paper's PDF, which AMS serves only to a browser.
2. Takahashi et al. 1995: the temperature range, the number of runs per temperature, and the actual collision energies. Is -10 C measured?
3. Hallett and Mossop 1974 and Mossop 1976: the stated maximum per mg (350 or 700), speed of the maximum, and whether anything was measured at -10 C (Mossop et al. 1974 row suggests about 0.24 per mg at -8 and -10 C).
4. Vardiman 1978 body: the fragment generation function and the temperatures of the samples.
5. Field et al. 2017: their summary of which mechanisms matter at -10 C and their numbers for the rate of each. Body not read.
6. The Phillips et al. comment on Korolev and Leisner (ACPD, doi:10.5194/acp-2021-123) and K&L's reply: not opened. They argue about exactly the point of whether the Takahashi data can be scaled by energy.
7. Size distributions in the thesis cold case: how many ice particles above 50 um radius, and how many droplets above 24 um and above 50 um? Without them f_c and F are free.
8. Collision efficiency for 50 to 200 um ice spheres at 600 hPa, and the relative speeds (differential fall at 600 hPa is larger than at 1000 hPa for the same size).
9. Do the spheres in the study have rime or vapour-grown branches? In every positive lab result the fragments came from branches or fragile rime. Pure ice spheres may give no fragments at these energies.
10. Does the study want drop shattering included? Our freezing droplets are captured by ice, which is the geometry for drop shattering. K&L Table 1 shows the data are spread over two orders of magnitude between groups.

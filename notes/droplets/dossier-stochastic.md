# Dossier: stochastic collisional growth of cloud droplets

Scout dossier for the Droplet Collection study. Written 2026-10-23. Read from primary sources; no code written, no other project file touched.

Conventions in this file:
- Statements without a tag are what the source says (paraphrased).
- `[derived]` marks arithmetic or reasoning by the scout, not in any source. Check before use.
- `[secondary]` marks something I know only because another paper I read says so.
- Quotes are at most one per source and under 15 words.

---

## 0. The four questions, answered in brief

**(a) How is collisional growth stochastic?**
Treat every pair of droplets in a well-mixed volume V as having a small chance per unit time of coalescing, C_kl = K(x_k, x_l)/V. The cloud is then a Markov jump process: the state is the list of droplet masses, the next event comes after an exponential waiting time, and the pair is chosen with probability proportional to its rate (Gillespie 1972, 1975). The probability of each possible droplet-count vector obeys a master equation (Marcus 1968; Bayewitz et al. 1974; written out in Alfonso 2015, Eq. 2). A second, simpler picture follows one collector falling through a fixed field of small droplets (Telford 1955; Kostinski and Shaw 2005; Wilkinson 2016). The waiting times between captures are independent exponentials whose means shrink as the collector grows. The time to n captures is therefore a sum of independent exponentials with unequal means (a generalised Erlang or hypoexponential law). That sum has a long fast tail: the luckiest collectors grow much faster than the average one.

**(b) When is the mean-field equation (Smoluchowski, SCE, KCE) wrong?**
The SCE is the first-moment equation of the master equation after dropping correlations, <n_i n_j> -> <n_i><n_j> (Gillespie 1972; Alfonso et al. 2008, 2015). It is exact only in the limit V -> infinity. It fails when:
1. The volume holds few droplets. Bayewitz et al. (1974), as reported by Alfonso, found large departures for fewer than about 50 droplets in total [secondary].
2. A runaway ("gel") drop carries a macroscopic share of the mass. For product-like kernels the KCE starts to lose mass and its second moment diverges. The breakdown time is when the largest drop reaches about M_T^(2/3) in mass (M_T = total mass) [Alfonso et al. 2008, citing Tanaka and Nakazawa 1994].
3. One asks about fluctuations or the far tail. The SCE has no information on spread, and the tail is where the first large drops live.
4. Coalescence is slow (small droplets). Dziekan and Pawlowska (2017) found the SCE needs a cell of at least 10^4 droplets when rain forms fast (mean radius 15 µm, 142 cm^-3), but at least 10^7 droplets when it forms slowly (mean radius 9.3 µm, 297 cm^-3; about 34 litres).

**(c) How is the master equation sampled exactly?**
- Gillespie (1975) is the exact method. Draw tau = C_0^-1 ln(1/r1). Pick the pair (i,j) with probability C_ij/C_0, either by two nested cumulative-sum searches or by uniform pair proposals accepted with probability C_ij/C* against a majorant C*. Details are in section 3.
- Alfonso et al. (2008) use the species-grouped version of Gillespie's 1976 direct method.
- Shima et al. (2009) super-droplet method with all multiplicities equal to 1 is the same process, per Dziekan and Pawlowska (2017). The check is numerical (against Alfonso and Raga's master-equation and SSA data), not a proof. It uses random non-overlapping pairs with scaled-up probabilities, which costs O(N) per time step but has a finite-time-step error.
- Alfonso (2015) solves the master equation itself by enumerating all reachable states, but only for roughly 50 droplets or fewer.

**(d) Time until the first large drops (numbers, all with conditions below)**

| Source | Setup | Result |
|---|---|---|
| Telford 1955 | 10% of water in 12.6 µm doublets, 90% in 10 µm droplets, 0.9 g m^-3 in the small ones, collection efficiency E = 1, 100 doublets per m^3 | 22.9 µm radius drops in about 5.1 min, against 33 min for continuous growth |
| Kostinski and Shaw 2005 | collector starts at twice droplet volume, 10 to 50 µm radius needs 125 captures | the fastest 10^-6 of collectors take about 0.1 of the mean time (asymptotic factor 0.087), about 10 times faster |
| Wilkinson 2016 (arXiv v1) | single collector, capture rate R_n = R_1 n^2 | onset time t* about 0.128 times the mean first-collision time for N = 10^5, 0.112 for N = 10^6 |
| Dziekan and Pawlowska 2017 | exponential spectrum, mean radius 9.3 µm, 297 cm^-3, LWC 1 g m^-3, gravity kernel, spectrum cut at 20 µm | mean time for the first r >= 40 µm drop: 14 777 s with 10^2 droplets in the system, 6500 s with 10^3, 3912 s with 10^4, 2552 s with 10^5, 1831 s with 10^6; the same drop-count scaling holds up to 10^9 droplets (946 s) |

---

## 1. Telford (1955)

**Reference.** Telford, J. W. (1955). A new aspect of coalescence theory. *J. Meteorol.* **12**(5), 436-444.
**Link opened:** https://journals.ametsoc.org/view/journals/atsc/12/5/1520-0469_1955_012_0436_anaoct_2_0_co_2.pdf (scanned PDF with no text layer; I read all 9 page images myself).
**DOI (inferred from the AMS URL slug, not resolved):** 10.1175/1520-0469(1955)012<0436:ANAOCT>2.0.CO;2

**What it establishes.**
- Growth by capture is discrete: a collector acquires whole droplets, and capture times are random. Treating the collected water as a smooth mist overestimates how long growth takes.
- Setup: collected droplets all have one size and are not depleted, and growing drops do not affect each other.
- The distribution of growth times is exactly solvable. For collectors that start at twice the droplet volume, the spread in times lets a few drops reach raindrop size much sooner than continuous growth predicts.
- His conclusion 1: "Earlier treatments have greatly overestimated the growth times required."
- The luckiest collectors carry the rain. Rain concentrations are about 10^2 drops per m^3 against about 10^8 cloud droplets per m^3, so he looks at the 10^-6 most fortunate drops.

**Equations (exact, as in the paper).**
- V = jv is the collector volume, j an integer number of droplet volumes v. a is the droplet radius, omega the cloud liquid water content, rho the water density, U the collector fall speed, u the droplet fall speed, E the collection efficiency.
- Probability that a drop of volume jv captures a droplet in dt: dP_j = A_j dt, with
  A_j = (3/4)(E omega u/(a rho)) j^(2/3) (U/u - 1).   (Eq. 1)
- Population N(r,t) of drops of volume rv: dN(r,t)/dt = A_(r-1) N(r-1,t) - A_r N(r,t).   (Eq. 2)
- Solution for initial size m: N(j,t) = (1/A_j) sum_{l=m..j} A_l B_l^(m,j) e^(-A_l t), with B_l^(m,j) = prod_{k=m..j, k != l} [1 - A_l/A_k]^-1.   (Eqs. 4-5)
- Time distribution for the n-th capture after the drop has volume mv (a generalised Erlang law): M(m,n,t) = sum_{l=m..m+n-1} A_l B_l^(m,m+n-1) e^(-A_l t), where M dt is the probability that the n-th capture falls in (t, t+dt).   (Eq. 7)
- Case A_j proportional to j (U - u proportional to drop radius). With T = (3/4)(E omega k/rho) t, N(j,t) = [(j-1)!/((m-1)!(j-m)!)] e^(-mT) (1 - e^(-T))^(j-m), a negative-binomial law. Mean volume mu = m v e^T, relative spread sigma/mu = (1/m - 1/mu)^(1/2), tending to m^(-1/2).   (Eq. 8)
- Stokes case: A_j = (3/4)(E omega u/(a rho)) j^(2/3)(j^(2/3) - 1). Time unit T = (3/4)(E omega u/(a rho)) t, with t about 1000 T seconds for a = 10 µm, E = 1, omega = 1 g m^-3. He evaluates M(m,n,t) numerically for m = 2, 3, 4 and n = 8 to 30 captures; the arithmetic needs about 12 significant digits because of alternating-sign cancellation.
- Conditions: E independent of size (he sets E = 1, which he says overestimates early rates); fixed environment; U - u proportional to r, or Stokes law (valid to about 50 µm radius).

**Numbers.**
- Abstract: drops of 23 µm radius form in about 5 minutes in a cloud of 10 µm droplets, with fewer, larger drops later.
- Worked example (Sect. 5): 90% of the water in 10 µm droplets (2.149e8 per m^3) and 10% in 12.6 µm doublets (1.19e7 per m^3), omega = 0.9 g m^-3, E = 1. 100 doublets per m^3 is 8.4e-6 of the doublets. For them to make 10 captures takes T = 0.257, which is t = 5.11 min. Continuous growth needs T = 1.84, which is 33.0 min. Ten captures turn a 12.6 µm drop into 22.9 µm.
- Fig. 5: starting at 12.6 µm in 1 g m^-3 of 10 µm droplets, after 4000 s continuous growth gives 0.53 mm radius. The discrete treatment gives a broad spectrum with many drops larger, "quite a number" above 3 mm radius.
- After about 20 captures the shape of the time distribution hardly changes, so the early captures fix the spread.

**Does not establish.**
- No size-dependent collection efficiency (explicitly deferred), no droplet depletion, no spread of droplet sizes (he says a continuous spectrum would help the lucky drops further), and no closed-volume or finite-N effects.
- Not a master equation for the whole cloud. The collectors never interact.

---

## 2. Gillespie (1972)

**Reference.** Gillespie, D. T. (1972). The stochastic coalescence model for cloud droplet growth. *J. Atmos. Sci.* **29**, 1496-1510.
**Link opened:** https://journals.ametsoc.org/view/journals/atsc/29/8/1520-0469_1972_029_1496_tscmfc_2_0_co_2.pdf (scanned, no text layer; all 15 page images read).
**DOI:** 10.1175/1520-0469(1972)029<1496:TSCMFC>2.0.CO;2 (printed in the reference list of Shima et al. 2009).

**What it establishes.**
- A precise definition of the stochastic coalescence model, and a derivation of the SCE from it under two stated assumptions.
- The mean droplet spectrum satisfies the SCE only if correlations between counts of different sizes are neglected.
- Fluctuations about the mean tend to a Poisson law, with an estimable relaxation time.
- Fluctuations from the stochastic mechanism and fluctuations from random positions in the cloud are different things, and the first are normally much smaller (his abstract).

**Equations.**
- Drops are labelled by the number m of water molecules. C(m1,m2;t) dt is the probability that an arbitrary m1-droplet and an arbitrary m2-droplet coalesce in (t, t+dt). For a well-mixed cloud of volume V: C dt = pi (r1+r2)^2 v(m1,m2) E(m1,m2) dt / V(t), where v is the mean relative fall speed and E the collection efficiency.   (Eqs. 3-4)
- P(n,m;t) = probability that exactly n m-droplets are present at t. Its first moment is N(m;t) = sum_n n P(n,m;t), and its rms width is Delta(m;t) = [N_2 - N^2]^(1/2).   (Eqs. 5-10)
- Exact time evolution of P involves conditional probabilities and leads to an open-ended hierarchy: "an open ended sequence of formulae" for higher conditional probabilities (Eq. 13 onward).
- Closure assumption 1 (no correlations): P(n,m | n',m'; t) ~ P(n,m;t) for m' != m, and the double-conditional analogue.   (Eq. 23)
- Closure assumption 2: C(m,m;t) = 0. No coalescence between droplets of exactly equal size, because they fall at the same speed. He judges this approximately true for real clouds and the dropped terms negligible anyway.   (Eq. 36)
- Under both, with A(m,t) = (1/2) sum_{m'=1..m-1} N(m')N(m-m') C(m',m-m') and B(m,t) = sum_{m'>=1} N(m') C(m,m'):
  dN/dt = A - N B   (the standard SCE, Eqs. 38-39)
  d(Delta^2)/dt = -2B Delta^2 + [A + N B]   (Eq. 43)
- Consequence: Delta^2 - N = [Delta^2(0) - N(0)] script-P^2(m,t), where script-P = exp(-integral_0^t B dt') is the probability that an m-droplet present at t = 0 has not coalesced by t. So Delta^2 -> N, and P(n,m;t) -> Poisson with mean N(m;t). Relaxation time tau_m (half-life): integral_0^tau_m sum_{m'} N(m';t) C(m,m';t) dt = ln 2. For t of order tau_m or longer, the number of m-droplets lies within N +/- N^(1/2).   (Eqs. 47-62)
- Concentration form: f = N/V, K = V C, and df/dt = (1/2) sum f(m') f(m-m') K(m',m-m') - f(m) sum f(m') K(m,m'), valid for a well-mixed cloud of constant volume.   (Eqs. 63-65)
- Two kinds of fluctuation: (i) from the stochastic mechanism, per unit volume of the whole cloud, of order [f/V]^(1/2); (ii) from random positions, in a particular unit volume, of order [f]^(1/2). Type (i) is smaller by V^(-1/2) when V >> 1 unit.   (Eqs. 66-70, Appendix B)

**Conditions of validity.** Both closures above, plus a well-mixed cloud (droplets uniformly random in V). He says the nature and extent of the error from the no-correlation approximation "require further study" and gives no estimate.

**Numbers.** None. The paper is analytical.

**Does not establish.**
- Does not quantify how large the correlation error is, or when it matters.
- Does not treat gelation or runaway growth, does not give a sampling algorithm (that is the 1975 paper), and gives no cloud-physics numbers.
- The relaxation-time statement is a rough estimate, not a bound.

---

## 3. Gillespie (1975)

**Reference.** Gillespie, D. T. (1975). An exact method for numerically simulating the stochastic coalescence process in a cloud. *J. Atmos. Sci.* **32**, 1977-1989.
**Link opened:** https://journals.ametsoc.org/view/journals/atsc/32/10/1520-0469_1975_032_1977_aemfns_2_0_co_2.pdf (scanned; all 13 page images read).
**DOI:** 10.1175/1520-0469(1975)032<1977:AEMFNS>2.0.CO;2 (printed in the reference list of Shima et al. 2009).

**What it establishes.** A Monte Carlo algorithm for the stochastic coalescence process that is "derived directly from (1) without making any approximations", so it includes all correlations and gives both the mean spectrum and its fluctuations. It states that earlier Monte Carlo schemes (Chin and Neiburger 1972; Lapidus and Shafrir 1972; Robertson 1974) use finite time steps, and that their error and efficiency are both proportional to the step size.

**Definitions.**
- N droplets with masses X_1..X_N, labelled in any order. C_kl = C(X_k, X_l) is the probability per unit time that droplets k and l coalesce (the same quantity as K/V above), for k < l.
- C_i = sum_{j=i+1..N} C_ij for i = 1..N-1.
- C_0 = sum_{i=1..N-1} C_i = sum over all pairs i < j of C_ij.

**Core result (exact).** The probability density that the next coalescence occurs after waiting time tau in (t+tau, t+tau+dtau) and involves the pair (i,j), i < j, is
P(tau,i,j) = C_ij exp[ - sum_{k<l} C_kl tau ] = C_ij exp(-C_0 tau).   (Eq. 8)
It factorises as P_1(tau) P_2(i) P_3(j|i):
- P_1(tau) = C_0 exp(-C_0 tau)   (Eq. 16a)
- P_2(i) = C_i / C_0   (Eq. 16b)
- P_3(j|i) = C_ij / C_i   (Eq. 16c)
This is the form later used for the chemical "direct method" (Gillespie 1976, 1977).

**Algorithm (as written).**
- Step 0: set t = 0, give X_1..X_N and the sample times; compute what is needed of C_kl.
- Step 1: draw a triplet (tau, i, j) from P(tau,i,j) by one of three methods below.
- Step 2: advance t -> t + tau; remove droplets i and j; insert a droplet of mass X_i + X_j; renumber; update the needed C values.
- Step 3: if t has passed a sample time, record the mass spectrum. Stop at t_stop or when one droplet is left; otherwise return to step 1.
- K independent runs from the same initial state give the mean N-bar(x, dx; t) = (1/K) sum_k N_k and the rms fluctuation Delta (Eqs. 11-12). He says K between 3 and 10 runs "should provide a statistically adequate picture".

**The three ways to draw (tau, i, j).** r1..r4 are independent uniform random numbers on (0,1).

A. Full conditioning.
- tau = C_0^-1 ln(1/r1).
- i = the integer for which sum_{i'<i} C_i' < r2 C_0 <= sum_{i'<=i} C_i'.
- j = the integer for which sum_{j'=i+1..j-1} C_ij' < r3 C_i <= sum_{j'=i+1..j} C_ij'.
- Memory: N masses plus the N numbers C_0, C_1..C_(N-1). The N(N-1)/2 matrix entries C_kl are recomputed when needed. After each coalescence, update C_0 and C_i by subtracting the terms for the two removed droplets and adding the terms for the new one. Total storage about twice N.

B. Partial conditioning with rejection (the majorant or "thinning" device).
- tau = C_0^-1 ln(1/r1), as before.
- Draw the pair jointly from P_4(i,j) = C_ij / C_0 by rejection from the uniform triangular domain: i'' = [1 + N r2], j'' = [1 + N r3] (brackets: integer part). If i'' = j'' retry. Set i' = min(i'',j''), j' = max(i'',j''). Draw r4. Accept (i,j) = (i',j') if C_i'j'/C* >= r4; otherwise redraw r2, r3, r4.
- C* is any upper bound on every current C_ij; the smallest available bound is best. Gillespie notes C* can be updated by comparing with each new C_ij, or from the largest and smallest droplet masses analytically. An overestimate costs speed only, not correctness.
- Efficiency (mean fraction of trials accepted): E = C_0 / [C* N(N-1)/2] = <C_ij>/C*. The mean number of proposals per event is 1/E = (C*/C_0) N(N-1)/2. For a constant kernel E = 1. E drops when C_ij has "high, narrow peaks and broad, low valleys".
- Memory: N masses plus the two numbers C_0 and C*, about half of method A. C_0 is still updated after each coalescence by subtract-and-add, which costs O(N) per event.
- Gillespie expects this to be usually the most efficient of the three.

C. First-coalescence method.
- For every pair draw a tentative time tau_kl = C_kl^-1 ln(1/r_kl); take the smallest, and its pair. He proves this correct (Eqs. 29-32), but it needs N(N-1)/2 random numbers per event, and he expects it to be the slowest.
- Choosing the second-smallest time as the next event is explicitly not allowed (it would be inconsistent, because the two coalescing droplets are removed).

**Cost (his statements).**
- Memory grows linearly with N.
- The number of events is proportional to N (N-1 events to reach one droplet).
- Time per event is proportional to at least N (updates of C_0 or C_i), so running time is "at least linearly, and more frequently quadratically" in the initial number of droplets.
- "An initial collection of 10^3 droplets should be a fairly routine job" for a 1975 large computer. With real clouds near 10^3 droplets cm^-3, this means 1 to 100 cm^3 of cloud.
- He cites Bayewitz et al. (1974): partitioning a cloud into many small sub-volumes with no exchange might be a fairly realistic procedure (a caveat on the finite-volume limitation, not an endorsement).

**Extension.** Section 5 adds a time-dependent external droplet source. Draw one tentative time from the coalescence law and one from the source law, and execute only the earlier. Breakup and sink terms are said to follow similarly but are not worked out.

**Conditions of validity.** A well-mixed volume V with the pair rate C = K/V. No restriction on the kernel. Exact in the limit of the probabilistic model; the only limits are the finite N and the run time.

**Numbers.** None. The paper has no simulations; it defers "applications to specific coalescence kernels" to later work.

**Does not establish.** How the SCE compares with the exact process for a real kernel (he lists this as the open question). No test results or timings. No condensation or sedimentation out of the volume.

---

## 4. Kostinski and Shaw (2005)

**Reference.** Kostinski, A. B. and Shaw, R. A. (2005). Fluctuations and luck in droplet growth by coalescence. *Bull. Amer. Meteor. Soc.* **86**, 235-244.
**Link opened:** https://journals.ametsoc.org/view/journals/bams/86/2/bams-86-2-235.pdf (PDF with text layer; all 10 pages of the main text and two sidebars). **The online supplement (DOI 10.1175/BAMS-86-2-Kostinski) was NOT opened.**
**DOI:** 10.1175/BAMS-86-2-235 (printed on the paper).

**What it establishes.** A closed-form version of Telford's argument. The main message: the early captures dominate growth time and carry most of the spread, so one needs "luck" early; "early fluctuations in coalescence times can never be neglected". Large collectors (giant nuclei, seeds) remove the need for luck.

**Equations (as in the paper).**
- Droplets all of radius r, perfectly random positions. Waiting time to the first capture is exponential: p(t) = (1/tau) exp(-t/tau), with mean tau = (c sigma u E)^-1 (Eq. 2). c is the droplet concentration, sigma the cross-section, u the relative speed, E the coalescence efficiency. The time to the first capture of the luckiest fraction P is about P tau for small P (the 10^-6 fastest wait about 10^-6 tau).
- Collector starts at volume 2v after one capture, so v_n = (n+1) v. For 10 to 50 µm radius, sigma, u and E each scale roughly as r^2, so the rate scales as r^6 and tau_n = tau / n^2 approximately (Eq. 3 and text).
- Mean cumulative time: <T_N> = tau sum_{n=1..N} 1/n^2 -> (pi^2/6) tau, about 1.6 tau. To reach 50 µm from 10 µm requires 5^3 = 125 captures; the first five terms give 89% of the sum, the first 11 over 95%.
- Variance of the cumulative time (independent exponentials, variances add): sigma^2(T_N) = tau^2 sum 1/n^4 -> (pi^4/90) tau^2. So sigma/<T> -> 6/sqrt(90) = 0.63, not shrinking like N^(-1/2). Their footnote: the memory of the early collisions persists.
- Time to N captures follows a generalised Erlang law (convolution of exponentials with different means), written out in a sidebar:
  P(t,N) = sum_k ... (sidebar formula, includes alternating signs); for t << tau they give P(t,N) ~ N! (t/tau)^N (as read from the OCR of the sidebar; with rates n^2/tau this is the product of the rates times t^N/N!, but the range of validity is not clearly stated).
- Luck factor theta for a lucky fraction: the fastest fraction takes time theta (pi^2/6) tau against the mean (pi^2/6) tau. The 10^-6 fraction has theta about 0.1 (asymptotic 0.087), so it is about 10 times faster than average, almost independent of tau.
- Removing the first one, two or three terms of the series (collector starts at 3v, 4v, 5v) makes the luckiest fraction approach the mean.
- Requirement for rain in 30 min: theta (pi^2/6) tau < 30 min, so tau < about 3 h. With tau = (c sigma u E)^-1 this bounds the product u E; for 10 µm droplets and 1 g m^-3 (about 240 cm^-3) they get a minimal relative speed of about 265 to 300 µm s^-1 over distances of about 40 µm.
- Sidebar 2 (turbulence): shear at the Kolmogorov scale can supply that relative speed with E about 0.15 (L = 200 m, delta U = 2 m s^-1). Not used for gravitational growth.

**Numbers and conditions.**
- Lucky fraction needed to start rain: about 10^-6 of cloud droplets. The 10^-9 fraction (patchy drizzle) and 10^-12 (a lone raindrop) are mentioned. Fig. 3 caption: the one-in-a-billion droplet is only about 2.5 times faster than the one-in-a-thousand droplet.
- Dziekan and Pawlowska (2017) state, citing this paper, that the luckiest 10^-3 fraction crosses the size gap about 6 times faster than average and the 10^-5 fraction about 9 times faster [secondary; I did not read the numbers off Fig. 3].
- The paper gives **no explicit time for the first raindrop in a cubic metre or cubic kilometre**. It gives luck factors per lucky fraction; converting to volumes needs the droplet concentration and the mean time tau. I have not found that conversion in the main text. [see Open questions]

**Does not establish.**
- Single collector, no depletion, no collector-collector collisions, fixed rate law tau_n proportional to n^-2 (stated for 10 to 50 µm and gravity only), droplets assumed all one size, no size-dependent efficiency beyond the scaling fit.
- Not a statement about a finite closed volume.

---

## 5. Shima, Kusano, Kawano, Sugiyama and Kawahara (2009)

**Reference.** Shima, S., Kusano, K., Kawano, A., Sugiyama, T. and Kawahara, S. (2009). The super-droplet method for the numerical simulation of clouds and precipitation: a particle-based and probabilistic microphysics model coupled with a non-hydrostatic model. *Q. J. R. Meteorol. Soc.* **135**, 1307-1320.
**Link opened:** https://arxiv.org/abs/physics/0701103 (PDF https://arxiv.org/pdf/physics/0701103). This is the preprint formatted for QJRMS (2008 copyright line); the published Wiley text (DOI 10.1002/qj.441, [secondary: from a web search result]) was NOT opened and may differ in detail.
**Parts read:** Sects. 4.1.4, 5.1.3, 5.1.4, 5.2 (start), 7.1-7.2, Appendices A and B. Not read: introduction, Sects. 2-3, 6 (the cumulus test).

**What it establishes.** A particle-based method: each super-droplet i carries a radius R_i and a multiplicity xi_i (integer: how many identical real droplets it stands for). If every xi_i = 1: "our model is equivalent to the primitive model", that is, the real system.

**Algorithm (as written; coalescence only).**
- Kernel K(R_j, R_k) = pi (R_j+R_k)^2 E |v_j - v_k| (their Eqs. 3-4). Real pair probability in a short interval Delta t_c in a cell of volume Delta V: P_jk = K(R_j,R_k) Delta t_c / Delta V.
- Coalescence of super-droplets j and k is "all-or-nothing": min(xi_j, xi_k) real pairs coalesce. Probability for the super-droplet pair: P^(s)_jk = max(xi_j, xi_k) P_jk. The expected number of coalesced real pairs is then xi_j xi_k P_jk, equal to the real world. The variance is larger by a factor min(xi_j, xi_k) than the Poisson limit.   (Eq. 20)
- Post-collision update, xi_j >= xi_k:
  if xi_j != xi_k: xi'_j = xi_j - xi_k, xi'_k = xi_k, R'_j = R_j, R'_k = (R_j^3 + R_k^3)^(1/3).   (Eqs. 12-13)
  if xi_j = xi_k: xi'_j = floor(xi_j/2), xi'_k = xi_j - floor(xi_j/2), R'_j = R'_k = (R_j^3 + R_k^3)^(1/3).   (Eqs. 16-17)
  Super-droplet count is unchanged except when xi_j = xi_k = 1 (then the number falls by one).
- Monte Carlo scheme for one cell, time step Delta t_c, n_s super-droplets (O(n_s) cost; Sect. 5.1.3):
  1. Make a random permutation of the super-droplet list (O(n) by the swap construction in Appendix A) and pair neighbours: floor(n_s/2) non-overlapping candidate pairs.
  2. Scaled-up probability for pair alpha: p_alpha = P^(s)_{j_alpha k_alpha} (n_s(n_s-1)/2) / floor(n_s/2). Justification: the sum over the chosen pairs of min(xi) p_alpha has the same expectation as (1/2) sum over all j != k of xi_j xi_k P_jk.
  3. Draw phi_alpha uniform in (0,1). gamma_alpha = floor(p_alpha) + 1 if phi_alpha < p_alpha - floor(p_alpha), else floor(p_alpha). This allows p_alpha > 1 (several coalescences of the same pair in one step).
  4. If gamma_alpha = 0, nothing happens.
  5. Otherwise take xi_j >= xi_k, gamma~ = min(gamma_alpha, floor(xi_j/xi_k)). If xi_j - gamma~ xi_k > 0: xi'_j = xi_j - gamma~ xi_k, xi'_k = xi_k, R'_k = (gamma~ R_j^3 + R_k^3)^(1/3). If it equals 0: xi'_j = floor(xi_k/2), xi'_k = xi_k - floor(xi_k/2), R' = (gamma~ R_j^3 + R_k^3)^(1/3) for both; remove super-droplet j if xi'_j = 0.
- Time-step rule of thumb: the strict requirement is p_alpha << 1 for all pairs. Their estimate for n = 10^9 m^-3 droplets of R = 10 µm and a rain drop falling at 1 m s^-1: p about (0.4 pi s^-1) Delta t_c, so Delta t_c below about 0.8 s, independent of n_s and cell volume.

**What it converges to.** With xi = 1 for all, the process is the real stochastic process (the coalescence master equation) up to the time-step error. With xi > 1 it reproduces the mean (SCE) but inflates fluctuations. Accuracy is controlled by the number of super-droplets N_s. Sect. 7.2 argues the cost of SDM scales as N_s about C^(-(d+4)/2) against bins N_b^(2d), where C is the integrated squared error and d the number of attributes. So SDM is cheaper than bins when d > 4k/(4-k), about d = 2 to 4 for a bin scheme of order k = 1 to 2.

**Numbers (SCE comparison, coalescence only, one cell; Sect. 5.1.4).**
- Golovin kernel K = b(X_j + X_k), b = 1.5e3 s^-1; one cell, Delta V = 10^6 m^3 (the extracted text reads "106 m3"), Delta t_c = 1 s. Initial n0 = 2^23 m^-3 (about 8.4 cm^-3), exponential in volume with R_0 = 30.531 µm, LWC 1.0 g m^-3. Case (a): N_s = 2^13 agrees fairly well with the analytic solution, 2^17 much better.
- Hydrodynamic kernel with the efficiencies of Davis (1972), Jonas (1972) and Hall (1980), reference from Bott's flux method with 1000 bins. Same setup: case (b) agrees similarly.
- Case (c), small droplets: R_0 = 10.177 µm, n0 = 3^3 x 2^23 m^-3 (extracted as "33 · 223"; about 227 cm^-3), LWC 1.0 g m^-3, Delta t_c = 0.1 s. N_s = 2^17 is not good enough; N_s = 2^21 (about 2 million) is needed. Reason: coalescence is slow, then a few big droplets abruptly accelerate it, so the right tail at t = 1200 s must be resolved. They call this a typical weak point of SDM.
- Cost figures (Pentium 4, 2008): case (b) 2.7 GFLOP and 192 MB for N_s = 2^13; Bott bins N_b = 100 needs 7.5 GFLOP, 48 MB, 13 s. The 2D cumulus run: 9.3e6 GFLOP, 65 GB, 11 h on 32 Earth Simulator nodes.

**Does not establish.**
- No fluctuation statistics at all. It validates only the mean against the SCE in a large cell. It does not study small cells, gelation, or the time to the first large drop.
- The comparison with the exact master equation is made by Dziekan and Pawlowska (2017), not here.

---

## 6. Alfonso and co-authors

**Terminology trap.** Gillespie 1972/1975, Shima 2009 and Dziekan 2017 call the mean-field Smoluchowski equation the "stochastic coalescence equation" (SCE). Alfonso et al. 2008, 2015 and 2017 call it the "kinetic collection equation" (KCE) and use "SCE" for the master-equation (true stochastic) averages. Same letters, opposite meaning.

### 6a. Alfonso, Raga and Baumgardner (2008)

**Reference.** Alfonso, L., Raga, G. B. and Baumgardner, D. (2008). The validity of the kinetic collection equation revisited. *Atmos. Chem. Phys.* **8**, 969-982.
**Link opened:** https://acp.copernicus.org/articles/8/969/2008/acp-8-969-2008.pdf (text only; figures not seen). DOI 10.5194/acp-8-969-2008.

**What it establishes.** A numerical test of when the KCE fails, using the Gillespie direct algorithm on kernels with known analytic solutions. A good practical indicator of breakdown is the maximum over time of STD(M_L1)/<M_L1>, the relative spread of the largest droplet mass over realizations. "the KCE becomes unable to describe the coalescence process" once a droplet detaches from the smooth spectrum.

**Equations.**
- KCE: dn(i,t)/dt = (1/2) sum_{j=1..i-1} K(i-j,j) n(i-j) n(j) - n(i) sum_{j>=1} K(i,j) n(j).   (Eq. 1)
- Master equation for P(n_1..n_N;t): dP/dt = sum_i sum_{j>i} K(i,j)(n_i+1)(n_j+1) P(..,n_i+1,..,n_j+1,..,n_(i+j)-1,..;t) + sum_i (1/2) K(i,i)(n_i+2)(n_i+1) P(..,n_i+2,..,n_(2i)-1,..;t) - sum_i sum_{j>i} K(i,j) n_i n_j P(n;t) - sum_i (1/2) K(i,i) n_i (n_i-1) P(n;t).   (Eq. 2)
  The KCE follows by taking the first moment and setting <n_i n_j> = <n_i><n_j>.
- Direct algorithm (Gillespie 1976, species form of Laurenzi and Diamond 1999; their Sect. 2). Species are droplet sizes; V is the volume.
  a(i,j) = V^-1 K(i,j) n_i n_j for i != j; a(i,i) = V^-1 K(i,i) n_i(n_i-1)/2.   (Eqs. 5-6; the printed "dt" is a rate-times-dt slip)
  alpha = sum of all a_mu. tau = alpha^-1 ln(1/r1)   (Eq. 10). Pair index mu from sum_{nu<mu} a_nu < r2 alpha <= sum_{nu<=mu} a_nu   (Eq. 11). Update populations; repeat.
- Product kernel K = C x_i x_j, monodisperse start: second moment M_2(t) = M_2(0)/(1 - C M_2(0) t), so the KCE gel time is tau_gel = [C M_2(0)]^-1.   (Eqs. 14-16)
- Tanaka and Nakazawa (1994) criterion [secondary]: for kernels containing an xy term the KCE is valid while the largest droplet mass is below about M_T^(2/3) (M_T total mass); for the other kernel tested, about M_T^(3/5). For the sum kernel K = B(x+y), KCE and master-equation averages agree when x_i/M_T << 1.

**Numbers.**
- Initial state: 100 droplets of 14 µm radius (mass 1.1494e-8 g), volume 1 cm^3, LWC about 1.15 g m^-3. Kernels are Long (1974) polynomial fits to the hydrodynamic kernel for R <= 50 µm: constant A = 1.2e-4 cm^3 s^-1; sum B = 8.83e2 cm^3 g^-1 s^-1; product C = 5.49e10 cm^3 g^-2 s^-1; mixed fits A+B(x+y)+Cxy and B(x+y)+Cxy.
- Product kernel: analytic KCE gel time 1378.7 s in one place and 1388 s in another (the paper is inconsistent); Monte Carlo maximum of STD/mean at 1315 s with M_L1/M_T^(2/3) about 0.86 there. After that the KCE underestimates the large end (bins above about 5).
- Mass loss in the KCE: sum kernel loses mass too (82% of initial mass left at 2000 s), product kernel 45% at 2000 s.
- The largest droplet (gel) at 1315 s has radius about 38 µm; at 2000 s about 52 µm.
- A 100 times larger volume (100 cm^3, 10 000 droplets) gives the same breakdown time, with runaway droplets again of 40 to 50 µm radius.
- Mixed kernels: Monte Carlo maxima at 1260 s (analytic 1134 s) and at 1310 s (analytic 1508.5 s).
- They state (citing Pruppacher and Klett 1997) that growth from 20 to 100 µm radius takes the order of an hour [secondary].
- Code check against the analytic stochastic solution for the sum kernel (N_0 = 100): excellent agreement (Fig. 1).

**Conditions and limits.** Monodisperse starts, simple kernels (not the full hydrodynamic kernel with efficiencies), volume 1 cm^3 or 100 cm^3. They stress that these initial conditions are "not very realistic" but allow rigorous checks.

**Does not establish.** No realistic spectrum, no effect of efficiencies, no time-to-first-drop statistics, no turbulence results (they only suggest the test would be useful there).

### 6b. Alfonso (2015)

**Reference.** Alfonso, L. (2015). An algorithm for the numerical solution of the multivariate master equation for stochastic coalescence. *Atmos. Chem. Phys.* **15**, 12315-12326.
**Link opened:** https://acp.copernicus.org/articles/15/12315/2015/acp-15-12315-2015.pdf (full text; figures not seen). DOI 10.5194/acp-15-12315-2015.

**What it establishes.** A way to solve the master equation (Eq. 2 above) directly rather than by sampling, for small systems and any kernel.

**Algorithm.**
1. Generate every state reachable from the initial state by repeated pair mergers, subject to sum_i x_i n_i = M_T (mass conservation) and n_i >= 0.
2. Advance every state probability by a first-order explicit step:
   P(n;t0+dt) = P(n;t0) + dt[ sum_{i<j} K(i,j)(n_i+1)(n_j+1) P(..n_i+1,..n_j+1,..n_(i+j)-1..;t0) + sum_i (1/2)K(i,i)(n_i+2)(n_i+1) P(..n_i+2,..n_(2i)-1..;t0) - sum_{i,j} K(i,j) n_i n_j P(n;t0) - sum_i (1/2) K(i,i) n_i(n_i-1) P(n;t0) ]   (Eq. 7; the i,j sum in the loss term is as printed there)
3. Marginals: P(n,m;t) = sum over all states with n_m = n of P(n_1..n_m=n..n_N;t) (Eq. 10); expected number <n_m> = sum_n n P(n,m;t) (Eq. 11). Correlations rho_ij = cov(n_i,n_j)/sqrt(Var(n_i) Var(n_j)) from the bivariate marginal (Eqs. 16-19).

**Cost.** For N identical monomers the number of states equals the number of integer partitions of N: R(N) about (1/(4N sqrt(3))) exp(pi sqrt(2N/3)) (Hall 1967). Counts generated: N = 6, 10, 20, 30 give 11, 42, 627, 5604 states (formula: 13, 48, 692, 6078). R(50) = 217 590, R(100) = 190 569 232. A brute-force 50-dimensional array would need about 1.34e16 elements. The method is therefore limited to roughly 50 droplets or fewer.

**Numbers.**
- Check against analytic master-equation solutions (Tanaka and Nakazawa 1993) for the constant kernel A = 1.2e-4 cm^3 s^-1 and the sum kernel B = 8.82e2 cm^3 g^-1 s^-1: excellent agreement; time step 0.1 s; example 10 droplets of 10 µm in 1 cm^3.
- Against Gillespie's SSA, N_0 = 30 droplets of 14 µm in 1 cm^3, sum kernel, t = 1200 s (Table 3): the SSA with 10^3 realizations reproduces the average only up to bin 8 and produces no droplet beyond bin 12; with 10^4 realizations it fails beyond bin 13 and produces nothing beyond bin 16. The exact solution has all bins up to 30 (values down to 1e-15). The master-equation algorithm matches the analytic values to 3 to 4 digits everywhere.
- Correlations for the constant, sum and product kernels, 10 and 40 droplets of 14 µm in 1 cm^3: non-zero throughout; n_1 and n_2 are strongly anticorrelated early on (Fig. 6, not seen).
- Turbulent hydrodynamic kernel (Hall efficiencies times the enhancement of Pinsky et al. 2008, epsilon = 0.1 m^2 s^-3, Re_lambda = 2e4), 20 droplets of 14 µm plus 10 of 17.64 µm in 1 cm^3, LWC 0.436 g m^-3: KCE and master equation agree for small masses (bins 1 and 5) up to 1800 s, but differ at the large end (bins 15 and 20) at all times.
- Agreement with the KCE requires the bin mass k to satisfy k^2 << M_0 (the total mass), per Tanaka and Nakazawa (1994) [secondary].

**Does not establish.** Anything for realistic droplet numbers. It is a benchmark tool for 30 to 50 droplets, not a production method. The author says a follow-up paper will treat the physics in more detail.

### 6c. Alfonso and Raga (2017), Part 1

**Reference.** Alfonso, L. and Raga, G. B. (2017). The impact of fluctuations and correlations in droplet growth by collision-coalescence revisited - Part 1: Numerical calculation of post-gel droplet size distribution. *Atmos. Chem. Phys.* **17**, 6895-6905.
**Link opened:** https://acp.copernicus.org/articles/17/6895/2017/acp-17-6895-2017.pdf (text only). DOI 10.5194/acp-17-6895-2017.

**What it establishes.** After the sol-gel transition the KCE misses the large-drop part of the spectrum (it lets total mass fall), while the master equation (and the SSA, within its sampling limits) conserve mass and give a clear runaway peak. Counts of low-mass bins and of the gel fraction become strongly anticorrelated near the critical time.

**Equations.** KCE (Eq. 1), master equation (Eq. 2) and the update (Eq. 5) as above. Product kernel, monodisperse start: T_gel = [C M_2(t_0)]^-1 (Eqs. 9-10). Relative spread of the largest drop sigma(S_max) = [(1/N_r) sum_i (S_max^i - <S_max>)^2]^(1/2) with S_max = M_max/<M_max> (Eq. 11); its maximum over time estimates the gelation time. Analytic monodisperse KCE solution for the product kernel (Laurenzi and Diamond 2002): N(i,t) = N_0 (iT)^(i-1) exp(-iT)/Gamma(i+1), T = C N_0 v_0^2 t (Eq. 12). Expected gel mass, M_1 = sum_{i>=i_1} m(i)<n_i> with sum_{i>=i_1}<n_i> = 1 (Eqs. 14-15). Correlation coefficient rho_ij (Eq. 19).

**Numbers.**
- Product kernel, C = 5.49e10 cm^3 g^-2 s^-1; 40 droplets of 17 µm (mass 2.058e-8 g) in 1 cm^3, LWC 0.823 g m^-3; 37 338 states; dt = 0.1 s. KCE gel time 1075 s; SSA (2000 realizations) maximum of sigma(S_max) at 1065 s. Gel mass at 1200, 1800, 2200 s from SSA, master equation and KCE: 2.84, 2.76 and 1.75 (x 1e-7 g) at 1200 s; 5.14, 5.34, 5.59 at 1800 s; 6.63, 6.35, 6.66 at 2200 s (table as extracted). KCE is off most near the critical time.
- Hydrodynamic kernel (Hall 1980 efficiencies), 20 droplets of 17 µm plus 10 of 21.4 µm in 1 cm^3: maximum of sigma(S_max) at 1310 s (1000 realizations). Gel mass SSA / master / KCE at 1200 s: 1.71e-7 / 1.79e-7 / 3.21e-8 g; at 1800 s: 3.34e-7 / 3.37e-7 / 3.63e-7 g; at 2200 s: 4.35e-7 / 4.68e-7 / 5.14e-7 g.
- They note (citing Malyshkin and Goodman 2001 [secondary]) that for a product kernel and monodisperse start the critical time falls as a power of 1/log(N_0); so larger concentrations give shorter critical times than the 20+ minutes found for 1 cm^3.
- The Dziekan and Pawlowska (2017) one-to-one SDM reproduces these master-equation and SSA data for the bidisperse hydrodynamic case (see section 7).

**Conditions.** At most 40 droplets in 1 cm^3 (small N because of the state-space size). The authors argue small volumes mimic early cloud stages when terminal velocities are small and coalescence is local. They say the KCE is justified only in the absence of a sol-gel transition, and call for a model of small volumes coupled by sedimentation.

**Does not establish.** No statement for realistic droplet numbers. No time-to-first-drop distribution. The "inability of explicit-microphysics models to explain observed spectral broadening" is offered as a possible explanation, not shown.

---

## 7. Dziekan and Pawlowska (2017)

**Reference.** Dziekan, P. and Pawlowska, H. (2017). Stochastic coalescence in Lagrangian cloud microphysics. *Atmos. Chem. Phys.* **17**, 13509-13520.
**Link opened:** https://acp.copernicus.org/articles/17/13509/2017/acp-17-13509-2017.pdf (full text extraction; figures not seen; Table 1 is garbled in the extraction and I reconstructed it from the row and column structure and from the text). DOI 10.5194/acp-17-13509-2017.

**What it establishes.**
- The super-droplet method with one computational droplet per real droplet ("one-to-one", multiplicity 1) is at the same level of precision as the master equation. They test this against the master-equation and SSA data of Alfonso and Raga (2017) (their Figs. 1-2) and against direct numerical simulation (Onishi et al. 2015). The test is numerical, not a proof. "The Smoluchowski equation is not valid" in a volume small enough to be well mixed.
- Well-mixed volume, in the sense that droplets are redistributed between collisions, is tiny. With tau_coal = (E pi (r_l+r_s)^2 v_r n_s)^-1 about 0.4 s (r_l = 100 µm, r_s = 10 µm, v_r = 70 cm s^-1, E = 1, n_s = 100 cm^-3) and turbulent mixing time tau_mix = (V^(2/3)/epsilon)^(1/3), demanding tau_mix = 0.1 tau_coal with epsilon = 10^3 cm^2 s^-3 gives V_mix = 1.5e-2 cm^3, about one droplet. Larger cells can be only approximately well mixed, to be validated against fine-grid runs with droplet motion.

**Algorithm (their description).**
- Real pair probability in step dt: P(r_i,r_j) = K(r_i,r_j) dt / V (gravitational kernels; collision efficiencies from Hall (1980) for large droplets and Davis (1972) for small ones; terminal speeds from Beard 1976).
- Shima's all-or-nothing update (Eq. 1 of the paper): xi'_j = xi_j, xi'_i = xi_i - xi_j, r'_j = (r_i^3 + r_j^3)^(1/3) for xi_j <= xi_i. Linear sampling: floor(N/2) non-overlapping random pairs instead of N(N-1)/2, with P_SD = max(xi_i, xi_j) P(r_i,r_j) [N(N-1)/2]/floor(N/2).
- One-to-one runs: all xi = 1. The time step is adapted at every step so that no pair has probability above 1 (like direct simulation Monte Carlo in rarefied gas). A coalescence discards one of the two super-droplets.
- Constant-SD runs: N_SD super-droplets with unequal multiplicities, fixed dt = 1 s; if p > 1 the pair coalesces gamma~ = min(gamma, xi_i/xi_j) times. They note this can lower the expected number of collisions if gamma > xi_i/xi_j, and that the probability should change after each repeat.
- The code is open: https://github.com/pdziekan/coal_fluctu and libcloudph++ (https://github.com/igfuw/libcloudphxx).

**Numbers (conditions in each line).**
- Setup 1 (fast rain): exponential in mass, n_0 = 142 cm^-3, mean mass that of a 15 µm radius droplet (as Onishi et al. 2015); gravity kernel. Setup 2 (slow rain): exponential in mass with mean radius 9.3 µm, n_0 = 297 cm^-3 (as Wang et al. 2006), spectrum cut at 20 µm; LWC printed as "1 g cm^-3", which must be 1 g m^-3 (the smallest cell able to make a 40 µm drop, N_0 about 80, has exactly that much water).
- t_10%: time at which 10% of the cloud-water mass has become drops with r > 40 µm (definition after Onishi et al. 2015).
  - Mean t_10% from one-to-one runs rises to a value above the Smoluchowski (Bott flux method) result as N_0 grows; they attribute the gap to numerical diffusion in the Bott scheme. Numeric t_10% values are in Fig. 4 only, which I did not see.
  - With the Hall kernel, autoconversion is faster than in DNS, the same as Onishi et al. found. Onishi et al.'s DNS agrees with the Smoluchowski equation using Long's (1974) kernel up to about 330 s [secondary].
  - Relative standard deviation of t_10% in one-to-one runs fits alpha/sqrt(N_0) with alpha = 6 and agrees with DNS. Constant-SD runs give correct fluctuations only up to a critical N_0/N_SD, beyond which they stop falling; the floor is beta/sqrt(N_SD) with beta = 2. So correct fluctuations need N_SD >= N_0/9; fluctuation amplification is about (1/3) sqrt(N_0/N_SD). The mean needs far fewer: N_SD = 10^3 gives mean t_10% within 1%, N_SD = 10^2 within 10%.
- Gelation: relative standard deviation of the largest droplet mass peaks at about the sol-gel time; for 10^2 < N_0 < 10^3 the gelation time is about 300 s (exponential in mass, 142 cm^-3 setup); an extra inflection near 500 s for N_0 = 10^5 is attributed to rain-rain collisions.
- Validity of the SCE (rain-water ratio theta = water in r >= 40 µm over total water):
  - Setup 1: Smoluchowski matches the mean theta for cells with N_0 >= 10^4 droplets (V = N_0/142 cm^-3, about 70 cm^3 [derived]); in smaller cells rain develops slower than the SCE.
  - Setup 2: needs N_0 >= 10^7 (V about 34 litres at 297 cm^-3 [derived]).
  - Large cells allow raindrops to collide with each other immediately after forming, lowering the rain-water growth rate; they flag this as possibly an artifact of an unrealistically large well-mixed volume. Highest rain-water ratio occurs in cells of intermediate size. In small cells depletion of cloud droplets near the first large drops and correlations in size slow rain down.
- Time of the first large drop (Sect. 6, Table 1): t40 = time until the first droplet reaches r = 40 µm, setup 2 (r_mean 9.3 µm, 297 cm^-3, LWC 1 g m^-3, one-to-one runs, ensembles). For each cell size N_0 they take the luckiest fraction gamma of realizations and give mean <t40>_gamma and standard deviation, in seconds (gamma = 1 means all realizations):

  | N_0 \ gamma | 1e-4 | 1e-3 | 1e-2 | 1e-1 | 1 |
  |---|---|---|---|---|---|
  | 1e2 | 2052 / 212 | 2930 / 356 | 4053 / 517 | 6365 / 1158 | 14 777 / 6099 |
  | 1e3 | 1366 / 120 | 1762 / 170 | 2400 / 267 | 3440 / 505 | 6500 / 1700 |
  | 1e4 | 1089 / 173 | 1336 / 103 | 1717 / 176 | 2354 / 276 | 3912 / 764 |
  | 1e5 | 946 / 33 | 1090 / 60 | 1334 / 85 | 1721 / 169 | 2552 / 415 |
  | 1e6 | none | none | 1038 / 165 | 1301 / 176 | 1831 / 277 |

  (each cell: mean / standard deviation, seconds)
- The mean <t40> is about the same along the diagonals of the table. It depends only on the total number of droplets N_tot = N_0/gamma. Reading the diagonals [derived from the table]: N_tot = 10^2: 14 777 s; 10^3: about 6500 s; 10^4: about 3912 s; 10^5: about 2552 s; 10^6: about 1730 to 1830 s; 10^7: about 1300 to 1370 s; 10^8: about 1040 to 1090 s; 10^9: 946 s. At 297 cm^-3, N_tot = 10^9 is about 3.4 m^3 [derived], so a cubic metre (about 3e8 droplets) sits near 1000 s, and no table entry reaches a cubic kilometre (3e17 droplets). A cell with 10^6 droplets makes its first r = 40 µm drop on average in about 30 min (1831 s), their own statement.
- Luck factor: <t40> (all) divided by <t40> of the luckiest 1e-3 is about 5 (14 777/2930), of the luckiest 1e-5 about 11, from the N_0 = 10^2 row (that cell can hold only one 40 µm drop). Kostinski and Shaw's estimate, as quoted: 6 and 9. They call the agreement good.

**Does not establish.**
- Cells are single well-mixed boxes; there is no droplet motion, no sedimentation out of the box, no turbulence. The collision-efficiency choice changes autoconversion (Hall vs Long).
- For the fast case there is no table of first-drop times; the t_10% numbers are only in a figure I did not see.
- Nothing here has a pre-existing set of large collectors in the initial spectrum.

---

## 8. Wilkinson (2016)

**Reference.** Wilkinson, M. (2016). Large deviation analysis of rapid onset of rain showers. *Phys. Rev. Lett.* **116**, 018501.
**Link opened:** https://arxiv.org/abs/1506.02807 (PDF https://arxiv.org/pdf/1506.02807, version 1, June 2015, titled "Large deviations and rain showers"). **The PRL version (DOI 10.1103/PhysRevLett.116.018501, DOI and title from a web search result) was NOT opened.** I read the arXiv v1 whole.

**What it establishes.** Rain showers can start on a timescale short compared with the mean time for a single collision. Reason: the time for a collector to grow through N captures is a sum of independent exponentials with rates that rise with each capture, and large-deviation theory gives the probability of an unusually small sum. His summary: "rain showers can start very quickly".

**Equations.**
- Capture rates R_n = R_1 n^gamma. gamma = 2 for terrestrial rain (rate times efficiency scaling as a^6, as in Kostinski and Shaw); gamma = 4/3 if the efficiency is unity.   (Eqs. 6-7)
- First collision rate for a drop of radius a_1 among droplets of radius a_0: R_1 = pi epsilon N_0 (a_0+a_1)^2 kappa (a_1^2 - a_0^2), with settling law v = kappa a^2, kappa = 2 rho_l g/(9 rho_g nu) about 1.4e8 m^-1 s^-1.   (Eqs. 1-2)
- Total time T = sum_{n=1..N} t_n, t_n exponential with rate R_n (Eqs. 4-5). Mean time: <T> = (1/R_1) sum 1/n^gamma -> zeta(gamma)/R_1 for N -> infinity, gamma > 1.   (Eq. 9)
- Probability density of T written as P(T) = <T>^-1 exp[-J(tau)], tau = T/<T> (Eq. 8). Cumulant generating function lambda(k) = sum_n ln(1 + k/R_n) (Eq. 15). Saddle-point result with kappa-bar = k*/R_1: tau(kappa-bar) = [sum_{n=1..N} 1/(kappa-bar + n^gamma)] / [sum_{n=1..N} n^-gamma] (Eq. 19; the extracted text shows kappa^gamma in the denominator, which I take to be an OCR artifact because Eq. 17 gives kappa + n^gamma), J(kappa-bar) = sum_n ln(1 + kappa-bar n^-gamma) - sum_n kappa-bar n^-gamma/(1 + kappa-bar n^-gamma) (Eq. 20).
- Tail as tau -> 0 (N -> infinity): J(tau) ~ K(gamma) tau^(-1/(gamma-1)). So P(tau) ~ exp(-K/tau) for gamma = 2 (K(2) = pi^2/(4 zeta(2)) = 3/2 exactly) and exp(-K/tau^3) for gamma = 4/3 (K about 0.8799).   (Eqs. 21-24)
- Shower onset: the cloud-water loss rate is -Phi_l N P(t) (Eq. 12). Onset t* solves N exp[-J(t*/<T>)] = 1, so J(tau*) = ln N and t* = tau* <T>.   (Eq. 13) N is the volume growth factor from droplet to raindrop; for a collector falling from cloud top, N = (h/(4 a_0))^3 Phi_l^3 (Eq. 11, about 1e5 for a 2 km cloud).

**Numbers (conditions).**
- gamma = 2: tau* about 0.077 for N = 10^5 and 0.068 for N = 10^6; in units of the mean first-collision time <t_1> = <T>/zeta(2): t* about 0.128 <t_1> (N = 10^5) and 0.112 <t_1> (N = 10^6). Conclusion in the paper: onset at about one eighth of the mean time for the first collision. The saddle-point result agrees with simulation and with numerical inversion for N = 4000 (Figs. 1-2).
- Cloud parameters used: droplet radius a_0 = 10 µm, N_0 = 2.5e8 m^-3, liquid fraction about 1e-6, depth 2 km, updraft 2 m s^-1; first-collision rate R_1 about 2e-5 s^-1 for a_1 - a_0 = 2.5 µm and epsilon = 0.03. Coalescence efficiency is about 0.03 at 10 µm and 0.1 below 20 µm.
- Note [derived]: R_1 = 2e-5 s^-1 means <t_1> about 5e4 s (14 h). Then t* = 0.128 <t_1> is about 6400 s (1.8 h), not minutes. The paper's text elsewhere says "of order one collision per hour"; the two statements are inconsistent by about a factor of 14. The v1 text may differ from the PRL text.
- Turbulence: with the numbers above, the Saffman-Turner collision rate is about 1e-6 s^-1 (negligible) and the Stokes number about 0.02, so he finds turbulent enhancement not enough on its own.

**Does not establish.**
- One collector falling through an unchanged cloud: no depletion, no collector-collector collisions, no finite volume. The power-law rate R_n = R_1 n^gamma is an assumption.
- Says explicitly that it does not resolve all the uncertainties of shower initiation, and that non-collisional convective mechanisms may be involved.
- Later follow-ups exist (arXiv:2207.14084 and arXiv:2209.14270, titles from a web search result) but I did not open them.

---

## 9. Open questions (what I could not find, open or settle)

**Not opened:**
- Published (Wiley) QJRMS version of Shima et al. 2009. I read the arXiv preprint (2008 manuscript).
- PRL version of Wilkinson 2016; arXiv v1 only.
- The Kostinski and Shaw online supplement (DOI 10.1175/BAMS-86-2-Kostinski), which contains their drop-size-distribution results and the comparison with Telford.
- Original papers cited second-hand: Marcus 1968, Bayewitz et al. 1974, Tanaka and Nakazawa 1993/1994, Scott 1967, Inaba et al. 1999, Malyshkin and Goodman 2001, Onishi et al. 2015, Unterstrasser et al. 2017, Wang et al. 2006. All statements about them are `[secondary]`.
- Figures in all ACP and arXiv papers (I had text only), so every number that appears only in a plot (for example the mean t_10% values in Dziekan and Pawlowska Fig. 4) is missing.
- Alfonso et al. 2010 and 2013 (Parts 2 and 3 of the validity series, hydrodynamic and turbulent kernels).

**Not found:**
- Any explicit time for the first raindrop in 1 m^3 or 1 km^3 in Kostinski and Shaw's main text. What exists is the luck factor per lucky fraction (about 10 for 10^-6) and a lucky-fraction ladder (10^-6 rain, 10^-9 drizzle, 10^-12 lone drop). Converting to volumes needs a droplet concentration and a mean time; Dziekan and Pawlowska's Table 1 is the nearest direct number, and it stops at 3.4 m^3.
- Any source that treats a spectrum with a pre-existing large-collector mode (this study's cloud). Telford's two-size cloud (12.6 µm plus 10 µm) is the closest, with E = 1 and no depletion.
- Collision and coalescence efficiencies for a 40 µm collector with 8 µm droplets, or for two nearly equal 60 µm collectors. Hall (1980), Davis (1972), Jonas (1972) are cited but not opened.

**Uncertain:**
- Whether the "one-to-one SDM" is exactly the Gillespie process at finite time step. The sources test it numerically (Dziekan and Pawlowska Figs. 1-2), and linear sampling of pairs shows no visible effect there, but I found no proof and no tolerance on the step.
- Dziekan and Pawlowska's two validity thresholds (10^4 and 10^7 droplets) come from two particular spectra without large collectors. No source gives a threshold for a bimodal spectrum.
- Garbled or inconsistent items to re-check on the published copy: Alfonso et al. 2008 gel time 1378.7 s versus 1388 s; Wilkinson R_1 versus "one collision per hour"; Dziekan and Pawlowska LWC printed in g cm^-3; Kostinski and Shaw's printed cumulative-probability formula (OCR of the sidebar was unreliable); Shima's "33 · 223" and "106 m3".
- DOI for Telford is inferred from the AMS URL; DOI of Shima 2009 and the follow-up Wilkinson papers come from a web search result.

---

## 10. Implications for a study of the thesis cloud

Cloud: 300 cm^-3 droplets of 8 µm (radius) plus 1 cm^-3 collectors of 40 µm, in a closed homogeneous box. All of this section is `[derived]` from the sources plus simple arithmetic; Stokes fall speeds and efficiency choices are my assumptions.

**Bookkeeping.**
- Water: droplets 300 cm^-3 x 2.145e-9 cm^3 = 0.643 g m^-3. Collectors 1 cm^-3 x 2.681e-7 cm^3 = 0.268 g m^-3. Total 0.911 g m^-3, of which 29% is already in the collectors.
- Per collector: 300 droplets to share = 6.43e-7 cm^3, plus its own 2.68e-7 cm^3, gives 9.12e-7 cm^3, a drop of radius 60.1 µm. This confirms the point that collecting every droplet brings a collector only to about 60 µm.
- Radius 100 µm needs 4.19e-6 cm^3, which is 4.6 collector-loads. Merging 4 collectors gives about 95 µm, 5 give about 103 µm, so 100 µm drops need about 5 collectors to merge, as stated.
- If "100 µm" means diameter (radius 50 µm), the volume is 5.24e-7 cm^3, which needs only (5.24e-7 - 2.68e-7)/2.145e-9 = 119 droplets, about 40% of the 300 available. The study should fix which it means. (Kostinski and Shaw call drizzle "about 100 µm in diameter and above".)

**Which stage is stochastic, from the sources.**
1. Collectors capturing droplets (40 to about 60 µm). Kostinski and Shaw show that luck matters only through the early captures of a small collector; supplying a large collector removes that need. A collector at 40 µm is already about 125 droplet volumes, and it will capture about 300 more. Using their tau_n proportional to n^-2 law only as a rough guide, the spread of its growth time to 60 µm is of order 5 to 10% (sum of n^-4 over n = 125..425 against the square of the sum of n^-2). Mean field is a reasonable description here once there are many collectors in the box, apart from droplet depletion, which is a global effect and strong.
2. Collector-collector mergers (60 to 100 µm). This is where the SCE is most in doubt. Two equal-size collectors fall at the same speed and do not collide by gravity (Gillespie 1972: C(m,m) = 0; Dziekan and Pawlowska: super-droplets with the same multiplicity-1 size cannot collide). In a mean-field description with a sharp collector mode, no mergers happen until some size spread exists. In reality spread arises from Poisson noise in the number of captured droplets (about 17 of 300, giving about 1 µm in radius) and from any initial spread. So the merger stage depends on fluctuations and on near-equal-size efficiencies that none of these sources give. Scale only: with a size difference of about 1 µm, a relative fall speed of about 1 cm s^-1, collector number density 1 cm^-3 and E of order 1, the merger rate per collector is about 5e-4 s^-1, one per half hour or longer. Treat as a scale to bracket, not a result.
3. Droplet depletion. With these numbers, a collector captures droplets at about 0.2 to 0.4 s^-1 at the start (E = 0.5 to 1; v_t about 19 cm s^-1 for 40 µm and 0.8 cm s^-1 for 8 µm by Stokes). The droplet stock therefore falls on a timescale of about 10 to 25 minutes. Dziekan and Pawlowska saw depletion near large drops slow rain in small cells.

**Box size (volume V).**
- Number of collectors in the box is V x 1 cm^-3: a 1 cm^3 box holds one collector (no mergers possible), 100 cm^3 holds 100 collectors and 30 000 droplets. Fix how counts are initialised (fixed numbers or Poisson draws); random draws add fluctuations of their own.
- Dziekan and Pawlowska's SCE thresholds were 10^4 droplets (fast spectrum) and 10^7 droplets (slow spectrum). Their slow spectrum (297 cm^-3, 9.3 µm) is the closest in droplet population to the thesis cloud, but has no collectors. With collectors given, the slow "crossing the size gap" part is bypassed, so the fast-case threshold may be nearer, but no source shows that.
- Their warning also applies to a closed box: a large well-mixed box lets newly formed rain drops collide with each other at once, which may be an artifact. Report results against V, and do not read late-time rain-rain behaviour in a big box as physical.

**Method.**
- Use exact sampling (Gillespie 1975 with partial conditioning, or the one-to-one super-droplet algorithm with adaptive step). Both cost about O(N) per event or step; the thesis box at 10^4 to 10^6 droplets is within what Dziekan and Pawlowska ran (ensembles with N_0 up to 10^7 in total 10^8 droplets per cell size).
- With partial conditioning the rejection majorant C* must cover the largest pair rate, which here is collector-droplet, a pair type that is rare among all pairs (1 collector per 300 droplets). E = <C_ij>/C* may then be small and the cost large; with only two size classes at the start one can track C* analytically. [derived]
- Report ensemble mean and spread, not a single run, and the SCE (a bin or flux solution) as the large-V reference. The study should say which meaning of "SCE" it uses (terminology trap in section 6).
- Dziekan and Pawlowska: constant-multiplicity super-droplets inflate fluctuations unless N_SD >= N_0/9, but get the mean right with N_SD = 10^3 (1%) and 10^2 (10%). Shima's weak point is the right tail when coalescence is slow (small droplets); N_SD of about 2e6 was needed in their small-droplet case.

**What the sources say about "time to first large drops" for this cloud.**
- Nothing direct. The first-drop time depends on the total number of droplets in the system, not on how it is divided into cells (Dziekan and Pawlowska): for 297 cm^-3 and no collectors, about 1000 s for the first r >= 40 µm drop in 1 m^3 (and about 30 min for 3.4 L). With 40 µm collectors present the first r >= 40 µm drop is there at t = 0, so the study must define the event as first drop above 60 µm (all droplets of a collector gone) or above 100 µm (or whichever threshold it uses). The collector-capture stage is deterministic-looking and takes of order 10 to 25 minutes [derived]; the merger stage is the stochastic and uncertain one.

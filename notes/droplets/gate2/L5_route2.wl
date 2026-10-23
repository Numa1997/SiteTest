(* L5 route 2, Wolfram Language 15.0.1 *)
ClearAll[mu, a0, u1, tau, q, z, M, n, kk];
Print["Poisson P(0) = ", PDF[PoissonDistribution[mu], 0], "; mean, variance: ", Mean[PoissonDistribution[mu]], ", ", Variance[PoissonDistribution[mu]]];
Print["median condition: ", Solve[Exp[-mu] == 1/2, mu], "  = ", N[Log[2], 8]];
Print["Binomial(N, mu/N) pmf limits, k = 0..3: ", Table[Limit[PDF[BinomialDistribution[n, mu/n], kk], n -> Infinity, Assumptions -> mu > 0], {kk, 0, 3}]];
Print["waiting time: survival of Exp(a0): ", SurvivalFunction[ExponentialDistribution[a0], tau], "; inverse of u = Exp[-a0 tau]: ", Solve[u1 == Exp[-a0 tau], tau]];
Print["mean of Exp(a0): ", Mean[ExponentialDistribution[a0]]];
pgfKept = Simplify[Sum[PDF[PoissonDistribution[M], j] (1 - q + q z)^j, {j, 0, Infinity}], Assumptions -> M > 0];
pgfPois = Simplify[Sum[PDF[PoissonDistribution[q M], j] z^j, {j, 0, Infinity}], Assumptions -> M > 0 && q > 0];
Print["thinned PGF ", pgfKept, " ; Poisson(qM) PGF ", pgfPois, " ; difference: ", Simplify[pgfKept - pgfPois]];
Print["lognormal tail 1e6 per m3 * P(r > 100 um), r_g = 40, sigma_g = 1.2: ", N[1*^6 SurvivalFunction[NormalDistribution[0, 1], Log[100/40]/Log[1.2]], 6]];
Print["max collector radius 40*1.2^3 = ", 40*1.2^3, " ; captures (100^3-69^3)/8^3 = ", N[(100^3 - 69^3)/8^3, 6]]

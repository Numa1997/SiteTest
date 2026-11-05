# Project 05, air and water: the Wolfram checks (5 November 2026)

Section 13 of the lecture note and the code in `public/simulations/double-inverted-pendulum.html` (`MEDIA`, `fieldV`, `fluidPar`,
`fluidQ`). Every check below was run in the Wolfram cloud kernel (Wolfram Language 15) through the MCP evaluator; the code is in
`checks.wl`, one block per call, so anyone can paste a block into a notebook and get the same numbers.

| Check | Result |
|---|---|
| Stokeslet \(\mathbf v = (\mathbf I/r + \mathbf x\mathbf x^{\mathsf T}/r^3)\mathbf F/(8\pi\mu)\), \(p = \mathbf F\cdot\mathbf x/(4\pi r^3)\) in (31) | residual {0, 0, 0}, divergence 0 |
| Bead chain (Lauga & Powers 2009, eqs. 26–31): \(\int' \mathrm d s/|s|\) over the rod without \(|s| < 2a\) | \(2\ln(L/4a)\); \(\xi_\perp/\xi_\parallel = 2\) |
| Power identity \(\sum Q_i \dot q_i = \int \mathbf f\cdot\mathbf v\,\mathrm ds\) for (33) | difference 0 (symbolic) |
| Upright rods at rest in a breeze \(U\), (33) with one \(\xi_\perp\) | \(\mathbf Q = \xi_\perp U\,(L_1 + L_2,\ L_1(L_1 + 2L_2)/2,\ L_2^2/2)\) |
| \(\nabla\cdot\mathbf v = 0\) | 0 for every flow |
| Vorticity equation \(\partial_t\omega + \mathbf v\cdot\nabla\omega - \nu\nabla^2\omega\) | 0 for Taylor–Green, shear, jets; river \(39\cdot 2^{6/7}\nu U/(343\,Y^{20/7}) \ne 0\) |
| Fan (single Bickley jet), boundary-layer equation \(u u_x + v u_y - \nu_J u_{yy}\) | 0; axis speed at the cart exactly \(U\) |
| Airy swell | divergence-free, irrotational; for 20 m waves in 6.7 m of water \(\omega = 1.73\) rad/s |

**The gate.** Test state \(x = 0.3\) m, \(\theta_1 = 0.4\), \(\theta_2 = -0.3\) rad, \(\dot x = 0.5\) m/s, \(\dot\theta_1 = 1.2\), \(\dot\theta_2 = -0.8\) rad/s,
\(t = 1.7\) s, \(U = 2\) m/s, \(L_1 = 0.5\), \(L_2 = 0.75\) m. The page's `fluidQ` (from `gate.cjs`) against an adaptive `NIntegrate` (30-digit
working precision, precision goal 13):

| Flow, medium | Page \(Q_x\), \(Q_{\theta_1}\), \(Q_{\theta_2}\) (3 × 8 Gauss points per rod) | Wolfram | Worst relative gap |
|---|---|---|---|
| fan, air | 0.00352356490675, 0.00213261847718, 0.00112513291746 | 0.00352356781818, 0.00213261470063, 0.00112510608999 | 2.4e-5 |
| street, air | 0.0503665579262, 0.00735986147304, 0.0105039977312 | 0.0503661893438, 0.00735971392937, 0.0105038925050 | 2.0e-5 |
| eddy, air | 0.00251113849002, 0.000144129591977, 0.000416221987782 | 0.00251111396957, 0.000144119674147, 0.000416218968888 | 6.9e-5 |
| swell, water | −54.7507257100489, −11.8521733900171, −7.60291651619635 | the same to 15 digits | < 1e-15 |
| Taylor–Green, glycerol | −14.3528743099202, −16.5340574471503, −17.8498065725196 | −14.3525060097177, −16.5339064568395, −17.8498065725202 | 2.6e-5 |
| ground wind, air | 0.0681449214542680, 0.00962412412258041, 0.00882133596276066 | the same to 15 digits | < 1e-15 |

What is left is the kink of \(|w_n|\,w_n\) where the flow across a rod changes sign. With 8 points per rod instead of 24 the vortex
street was 1.2 % off (\(Q_{\theta_1}\) 0.00744786 against 0.00735971): the cores are about 9 cm wide, finer than 8 points on a rod.

**Scripts.** `gate.cjs` prints the page's Q at the test state above; `flows.cjs` runs every flow in air and water in headless Chromium and prints, per flow, page errors, Q against the in-page Simpson check, P, the book and the replay of the last 300 steps (`OUT=<folder>` for its screenshots). The honesty run with the three fluid scenarios is in `../panel/fluid-honesty.txt`.

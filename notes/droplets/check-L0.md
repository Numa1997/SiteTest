# Gate 2 check, L0 (chapter 1): equations (1.1) to (1.4)

Checker: Gate 2 (independent re-derivation). Text: `portfolios-src/droplets/text/book-01.src.html`. Model read only: `physics.cjs`.
Scripts and their printed output are in `notes/droplets/gate2/`. Route 1 = SymPy 1.14. Route 2 = Wolfram Language 15.0.1 (evaluator) plus a SciPy/NumPy numerical check (Monte Carlo, ODE integration, quadrature), both listed per row.

| Eq. | Route 1 (SymPy) | Route 2 (Wolfram, and SciPy/NumPy numerics) | Units / limit / sign | Verdict |
|---|---|---|---|---|
| (1.1) dM/dt = E pi (R+r)^2 [v(R)-v(r)] W, M = 4 pi rho R^3/3 | n = W/m_d, droplets in tube of radius R+r and length dv dt, times m_d: derived form minus printed = 0 | Wolfram: integrated the cylinder volume, same form, "equal to printed: True". NumPy Monte Carlo (400 boxes, random droplet centres, count those within R+r): 8.745e-13 +- 0.031e-13 kg/s against formula 8.796e-13 kg/s, ratio 0.994 | kg/s on both sides. W->0 gives 0. Positive for v(R) > v(r); zero for equal drops, as it must be | right |
| (1.2) dR/dt = E k W (R+r)^3 (R-r) / (4 rho R^2) | Insert v = k a^2 and dM/dt = 4 pi rho R^2 dR/dt: difference from printed = 0 | Wolfram: Simplify gives 0. NumPy: dR/dt from (1.1) divided by dM/dR (finite difference) against (1.2) at 20, 40, 100, 300 um: relative differences 2e-8 to 5e-8 (finite-difference noise) | k = 2 drho g/(9 mu) is m^-1 s^-1 (checked); dR/dt is m/s. r->0 gives c R^2, c = E k W/(4 rho). Positive for R > r | right |
| (1.3) R = R0/(1 - c R0 t), t* = 1/(c R0) | `dsolve` of dR/dt = c R^2, R(0)=R0 gives -1/(c t - 1/R0): identical. Pole at t = 1/(c R0). t = t*(1 - R0/R); 40->60 um = 1/3 of t*, 40->100 um = 3/5 (text: "one third", "60 %": right) | Wolfram `DSolve`: same, "match printed: True". SciPy `solve_ivp` (rtol 1e-12) of (1.2) with r = 1e-12 m: R(0.2 t*), R(0.5 t*), R(0.9 t*) agree with (1.3) to 1e-8, 4e-8, 2.5e-7 (the tiny residue is r/R, as expected) | c R0 t is dimensionless (checked). W->0 gives R = R0. Sign: R grows, blow-up at t* > 0. Valid only for r << R (see note 1) | right |
| (1.4) t(R) = 4 rho/(E k W) [F(R)-F(R0)], F = ln((R-r)/(R+r))/(8r) - (3R+2r)/(4(R+r)^2) | dF/dR - R^2/((R+r)^3 (R-r)) = 0 (this is dt/dR from (1.2)). `apart` and `integrate` give the same antiderivative. lim r->0 F = -1/R; lim R->oo F = 0; r->0 reproduces 4 rho (R-R0)/(E k W R R0), which is (1.3) | Wolfram: same derivative (0), `Integrate` same antiderivative, `Limit` -1/R and 0. SciPy: `solve_ivp` of (1.2) with r = 8 um from 40 to 100 um: 597.328870 s; (1.4): 597.328870 s; quadrature of dt/dR: 597.328870 s (agree to 6 decimals) | dF/dR > 0 so t grows with R. W->0 gives t -> infinity, correct | right |

Text numbers rechecked on the way (not equations, same scripts): k = 1.2296e8 m^-1 s^-1 is Stokes k at 10 C and 850 hPa (model: 1.22961e8). W = 0.6434 g/m3. 40->100 um: 9.955 min by (1.4) (text 9.96), 12.640 min by (1.3) (text 12.64, needs the unrounded W = 0.6434, with 0.643 it is 12.648); t* = 21.07 min (text 21.1); R_m = 60.148 um (text 60.15).

## Notes (none changes a verdict)

1. The sentence "The radius would blow up at 21.1 min" is the (1.3) value (r << R). With the finite droplet radius the same cloud blows up earlier, at 17.77 min (SciPy ODE to R = 1 m: 17.7733; (1.4) with F(oo) = 0: 17.7742; model `L0blowup`: 17.774). A reader could take 21.1 min as the blow-up of the full equation (1.2). Suggest "(1.3) would blow up at 21.1 min; with the droplets' own size, (1.2) already at 17.8 min".
2. (1.1) is a straight-line sweep (no deflection); this is the stated E = 1 model of the chapter and chapter 3 removes it. The Monte Carlo confirms the geometry only.
3. Stokes law is used for v(R) up to 100 um although chapter 2 shows Re = 15 there; the text says so.

## Commands run (from `notes/droplets/gate2/`)

```
python3 L0_route1_sympy.py        | tee L0_route1_sympy.out.txt
python3 L0_route2_numeric.py      | tee L0_route2_numeric.out.txt
node    L0_model_crosscheck.cjs   | tee L0_model_crosscheck.out.txt
# Wolfram: code in L0_route2.wl, evaluated in the Wolfram Language evaluator, output transcribed in L0_route2_wolfram.out.txt
```

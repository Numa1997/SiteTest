"""Check of Wolfram 06 (Voelp & Willenbacher 2021 law with Guinness sigma = 44.2, Einf = 18.7 mN/m, R32 = 34 um)."""
s, E, R, rho, h, pc = 0.0442, 0.0187, 34e-6, 1007, 0.019, 0.635
P = (s + 2*E)/R
print('(s+2E)/R = %.1f Pa' % P)
for e in (0.22, 0.24, 0.27, 0.30, 0.34):
    Phi = 1 - e; G = P*Phi*(Phi - pc); ty = 0.25*P*(Phi - pc)**2
    print('e=%.2f G0=%.2f Pa tau_y=%.3f Pa Bi1=%.3f Bi10=%.4f' % (e, G, ty, ty/(rho*e*h), ty/(rho*e*10*h)))

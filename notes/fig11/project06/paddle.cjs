// Note 13.7, (48): the outer rod as a paddle. omega_need = 2 sqrt(f/I) (swing over the top) against omega_t, the turning rate at which the
// drag torque of (33)+(34) along the rod equals the whole pull of its weight f. Lone rod on a fixed hinge; I includes the carried liquid (38).
// Constants as on the page: rod radius 1 cm, C_D 1.2, C_a 1, media of table 13.1. Run: node paddle.cjs
const G = 9.81, r = 0.01, CD = 1.2, MED = { water: [998.2, 1.0016e-3], glycerol: [1261, 1.412], honey: [1420, 7] };
for (const [name, m, L] of [['project 05 outer rod', 0.75, 0.75], ['2 kg, 0.25 m', 2, 0.25], ['project 06 outer rod', 3, 0.25]]) {
  const row = [];
  for (const [med, [rho, mu]] of Object.entries(MED)) {
    const xi = 4 * Math.PI * mu / Math.log(L / r), cq = 0.5 * rho * CD * 2 * r, f = m * G * L / 2 - rho * G * Math.PI * r * r * L * L / 2, I = m * L * L / 3 + rho * Math.PI * r * r * L ** 3 / 3;
    const a = cq * L ** 4 / 4, b = xi * L ** 3 / 3, wt = (-b + Math.sqrt(b * b + 4 * a * f)) / (2 * a), wn = 2 * Math.sqrt(f / I);
    row.push(`${med}: need ${wn.toFixed(2)} rad/s, liquid allows ${wt.toFixed(2)} rad/s, ratio ${(wt / wn).toFixed(2)}`);
  }
  console.log(name + '\n  ' + row.join('\n  '));
}

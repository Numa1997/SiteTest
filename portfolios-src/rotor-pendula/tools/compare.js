#!/usr/bin/env node
// Theory against the full equation, for the figures of chapters 1 and 2. Runs the simulation page's own physics block
// (tools/physics_block.js) in Node, ideal brake:
//  - the harvested power over brakes from 0.05 to 20 times the best brake, at 6, 8 and 10 m/s;
//  - one recorded turn of the swing theta(phi) at the best brake, at the three winds.
// Writes data/compare.json, which tools/make_numbers.py turns into the figures. Usage: node tools/compare.js   (about a minute)
const fs = require('fs');
const path = require('path');
const { loadPhysics } = require('./physics_block');
const { simulate, makeModel, CONST } = loadPhysics();

const out = { winds: [] };
const T0 = Date.now();
for (const wind of CONST.winds) {
  const md = makeModel({ wind });
  const sweep = [];
  for (let i = 0; i <= 24; i++) {
    const x = Math.pow(10, -1.30103 + 2.60206 * i / 24);      // 0.05 .. 20, log-spaced
    const o = simulate({ wind, brake: x });
    sweep.push({ x, P: o.P_mean, Plin: md.linearPower(x * md.kappaStar), Theta: o.Theta });
  }
  const o = simulate({ wind, brake: 1 }), r = o.rec, n = r.framesPerTurn;
  const turn = { phi: [], q: [] };
  for (let k = 0; k <= n; k++) { turn.phi.push(r.phi[k] - r.phi[0]); turn.q.push(r.q1[k]); }
  out.winds.push({ wind, Om: md.Om, R: md.R, G: md.G, kappaStar: md.kappaStar, Pstar: md.Pstar, phi0: r.phi[0], trail: o.trail, sweep, turn });
  console.log(`${wind} m/s: ${sweep.length} brakes, best ${Math.max(...sweep.map(s => s.P)) * 1e3} mW`);
}
fs.writeFileSync(path.join(__dirname, '..', 'data', 'compare.json'), JSON.stringify(out));
console.log(`data/compare.json in ${((Date.now() - T0) / 1000).toFixed(1)} s`);

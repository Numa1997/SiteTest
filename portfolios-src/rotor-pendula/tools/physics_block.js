// Loads the physics block of rotor_sim.html (between /*PHYSICS-BEGIN*/ and /*PHYSICS-END*/) in Node, exactly as the page's
// Web Worker does: the same text, run by new Function. Used by check_sim.js and sim_solutions.js.
const fs = require('fs');
const path = require('path');
const PAGE = path.join(__dirname, '..', 'rotor_sim.html');
function physicsText(file = PAGE) {
  const s = fs.readFileSync(file, 'utf8');
  const a = s.indexOf('/*PHYSICS-BEGIN*/'), b = s.indexOf('/*PHYSICS-END*/');
  if (a < 0 || b < a) throw new Error('no physics block in ' + file);
  return s.slice(a, b);
}
function loadPhysics(file = PAGE) {
  const block = physicsText(file);
  return new Function(block + '\nreturn { CONST, DEFAULTS, makeModel, simulate };')();
}
module.exports = { loadPhysics, physicsText, PAGE };

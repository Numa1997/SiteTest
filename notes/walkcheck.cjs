// Every quoted code line of the ten walkthroughs, searched in its page (docs/scripts/walk.md, "The rule").
// Marks are stripped; a line that is only "..." is an elision; "..." inside a line splits it into fragments that must
// appear in order on one page line. Usage: node notes/walkcheck.cjs
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..');
const sims = fs.readdirSync(path.join(ROOT, 'public/simulations')).filter(f => f.endsWith('.html'));
let total = 0, missing = 0;
for (const f of sims) {
  const html = fs.readFileSync(path.join(ROOT, 'public/simulations', f), 'utf8');
  const key = (html.match(/data-walk="([a-z0-9-]+)"/) || [])[1];
  if (!key) continue;
  global.window = {};
  eval(fs.readFileSync(path.join(ROOT, 'public/scripts/walk', key + '.js'), 'utf8'));
  const lines = html.split('\n').map(l => l.trim());
  let n = 0, miss = [];
  for (const step of window.WALK[key].steps) {
    for (const raw of step.code.replace(/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g, '$1').split('\n')) {
      const t = raw.trim();
      if (!t || t === '...') continue;
      n++;
      const frags = t.split('...').map(s => s.trim()).filter(Boolean);
      const ok = lines.some(l => { let i = 0; for (const fr of frags) { const j = l.indexOf(fr, i); if (j < 0) return false; i = j + fr.length; } return true; });
      if (!ok) miss.push(t);
    }
  }
  total += n; missing += miss.length;
  console.log(`${key.padEnd(9)} ${f}: ${n - miss.length}/${n} found${miss.length ? '\n  NOT FOUND: ' + miss.join('\n  NOT FOUND: ') : ''}`);
}
console.log(`all: ${total - missing}/${total} found`);
process.exit(missing ? 1 : 0);

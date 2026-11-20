// Fig. 13: the sheet's worker must integrate exactly as the page does. Fails if rk4n or tip differ between
// public/simulations/momentum-spirographs.html and public/scripts/fig13-sheet-worker.js.   node tools/fig13/sheet_worker_check.cjs
const fs = require('fs'), path = require('path'), root = path.join(__dirname, '..', '..');
const page = fs.readFileSync(path.join(root, 'public/simulations/momentum-spirographs.html'), 'utf8');
const work = fs.readFileSync(path.join(root, 'public/scripts/fig13-sheet-worker.js'), 'utf8');
const grab = (src, head, end) => { const a = src.indexOf(head); if (a < 0) return null; return src.slice(a, src.indexOf(end, a) + end.length); };
let bad = 0;
for (const [head, end] of [['function rk4n(s, h, n) {', '\n}\n'], ['function tip(s) {', '}\n']]) {
    const a = grab(page, head, end), b = grab(work, head, end);
    if (!a || a !== b) { bad++; console.log('differs: ' + head); } else console.log('same: ' + head);
}
process.exit(bad ? 1 : 0);

// Static server for public/ that sends the headers public/_headers gives each path (as Cloudflare does: every matching rule,
// exact paths, "/*" and "/*.ext"), so the browser tests see the isolation of Fig. 12 as the live site has it.
// node notes/fig12/serve.cjs [port]
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../../public'), port = +(process.argv[2] || 8790);
const rules = []; let cur = null;
for (const line of fs.readFileSync(path.join(root, '_headers'), 'utf8').split('\n')) {
  if (!line.trim() || line.trim().startsWith('#')) continue;
  if (!/^\s/.test(line)) { cur = { path: line.trim(), h: [] }; rules.push(cur); }
  else if (cur) { const i = line.indexOf(':'); cur.h.push([line.slice(0, i).trim(), line.slice(i + 1).trim()]); }
}
const matches = (pat, p) => pat === p || pat === '/*' || (pat.startsWith('/*.') && p.endsWith(pat.slice(2)));
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.png': 'image/png', '.json': 'application/json' };
http.createServer((req, res) => {
  const url = decodeURIComponent(req.url.split('?')[0]); let p = url; if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p);
  if (!f.startsWith(root)) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (err, buf) => {
    if (err) { res.writeHead(404); return res.end('not found'); }
    const head = { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' };
    for (const r of rules) if (matches(r.path, url)) for (const [k, v] of r.h) head[k] = v;
    res.writeHead(200, head); res.end(buf);
  });
}).listen(port, () => console.log('serving public/ with public/_headers on ' + port));

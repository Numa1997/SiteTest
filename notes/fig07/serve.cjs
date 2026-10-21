// Small static server for the Fig. 7 build: node notes/fig07/serve.cjs /tmp/fig07-dist 8707
'use strict';
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.resolve(process.argv[2] || '/tmp/fig07-dist'), port = +(process.argv[3] || 8707);
const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2', '.webp': 'image/webp', '.png': 'image/png', '.json': 'application/json', '.txt': 'text/plain' };
http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p);
  if (!f.startsWith(root)) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (err, buf) => {
    if (err) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' });
    res.end(buf);
  });
}).listen(port, () => console.log('serving ' + root + ' on ' + port));

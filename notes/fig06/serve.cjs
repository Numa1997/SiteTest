// Small static server for the Fig. 6 build. Run: node notes/fig06/serve.cjs /tmp/fig06-dist 8606
'use strict';
const http = require('http'), fs = require('fs'), path = require('path');
const root = process.argv[2] || '/tmp/fig06-dist', port = +(process.argv[3] || 8606);
const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.png': 'image/png', '.json': 'application/json' };
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
}).listen(port, () => console.log('serving', root, 'on', port));

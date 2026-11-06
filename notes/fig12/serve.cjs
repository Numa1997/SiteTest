// Static server for public/ with the headers Cloudflare sends for Fig. 12 (cross-origin isolation, so that the page may
// use shared memory and worker threads): node notes/fig12/serve.cjs [port]
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../../public'), port = +(process.argv[2] || 8790);
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.png': 'image/png', '.json': 'application/json' };
http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p);
  if (!f.startsWith(root)) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (err, buf) => {
    if (err) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream', 'Cross-Origin-Opener-Policy': 'same-origin', 'Cross-Origin-Embedder-Policy': 'require-corp' });
    res.end(buf);
  });
}).listen(port, () => console.log('serving public/ isolated on ' + port));

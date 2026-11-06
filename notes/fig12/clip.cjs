// Renders the Fig. 12 clip: node notes/fig12/clip.cjs <out-dir> <seconds> [dx]
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs'), path = require('path');
(async () => {
  const out = process.argv[2], secs = +process.argv[3] || 4, dx = process.argv[4] || '0.003', fps = 30;
  fs.mkdirSync(out, { recursive: true });
  const srv = spawn('python3', ['-m', 'http.server', '8771', '--directory', path.join(__dirname, '../..')], { stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 800));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  p.on('console', m => console.log('page:', m.text())); p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto(`http://localhost:8771/notes/fig12/clip.html?dx=${dx}`); await p.waitForFunction('window.ready');
  const n = Math.round(secs * fps), t0 = Date.now();
  for (let i = 0; i < n; i++) {
    if (i) await p.evaluate(d => window.frame(d), 1 / fps);
    await p.locator('#cv').screenshot({ path: path.join(out, `f${String(i).padStart(4, '0')}.png`) });
    if (i % 15 === 0) console.log(`frame ${i}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  }
  fs.writeFileSync(path.join(out, 'log.json'), JSON.stringify(await p.evaluate(() => window.getLog())));
  await b.close(); srv.kill();
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', path.join(out, 'f%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', path.join(out, 'clip.mp4')]);
  console.log('done', path.join(out, 'clip.mp4'));
})();

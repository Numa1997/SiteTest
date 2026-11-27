// Render a film page frame by frame and, with --mp4, encode the frames.
//   node render_film.cjs URL OUTDIR [--mp4 FILE.mp4] [--size 1080x1920] [--frames 0,30,60] [--scale 1]
// The page must be served over HTTP. Run this in the background for a whole film.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
(async () => {
  const a = process.argv.slice(2), opt = (k, d) => { const i = a.indexOf(k); if (i < 0) return d; const v = a[i + 1]; a.splice(i, 2); return v; };
  const mp4 = opt('--mp4', null), size = opt('--size', '1080x1920'), only = opt('--frames', null), scale = Number(opt('--scale', 1)), [url, outdir] = a;
  if (!url || !outdir) { console.error('usage: node render_film.cjs URL OUTDIR [--mp4 FILE] [--size WxH] [--frames a,b,c] [--scale n]'); process.exit(2); }
  const [VW, VH] = size.split('x').map(Number); fs.mkdirSync(outdir, { recursive: true });
  const b = await chromium.launch(), ctx = await b.newContext({ viewport: { width: VW, height: VH }, deviceScaleFactor: scale }), p = await ctx.newPage(), errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto(url + (url.includes('?') ? '&' : '?') + 'film=1', { waitUntil: 'load' });
  await p.waitForFunction(() => window.__ready === true, null, { timeout: 90000 });
  const total = await p.evaluate(() => window.FILM.frames()), list = only ? only.split(',').map(Number) : Array.from({ length: total }, (_, i) => i), t0 = Date.now();
  for (const f of list) {
    await p.evaluate(f => window.renderFrame(f), f);
    await p.screenshot({ path: `${outdir}/f${String(f).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 93 });
    if (list.length > 60 && f % 150 === 0) console.log(`frame ${f} of ${total}, ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  }
  await b.close();
  console.log(`${list.length} frames in ${((Date.now() - t0) / 1000).toFixed(0)} s; script errors: ${errs.length ? errs.join(' | ') : 'none'}`);
  if (errs.length) process.exit(1);
  if (mp4 && !only) {
    const tmp = mp4.replace(/\.mp4$/, '.part.mp4');
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', '30', '-i', `${outdir}/f%05d.jpg`, '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', tmp], { stdio: 'inherit' });
    fs.renameSync(tmp, mp4); console.log(`wrote ${mp4}: ${(fs.statSync(mp4).size / 1e6).toFixed(1)} MB, ${(total / 30).toFixed(1)} s`);
  }
})();

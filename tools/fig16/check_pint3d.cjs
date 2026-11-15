// Three-way check of the 3D close-up (public/scripts/pint3d-view.js) against the stored data, in Chromium:
//  1. stored value: the stout's height and the head's thickness at the wall facing the camera, StoutRide.atInward (stout-view2.js);
//  2. recomputed: the same point projected through the close-up's own camera;
//  3. pixel read back: just below the stored surface the pixel must be drawn (alpha > 0) and dark (stout); inside the head band it
//     must be drawn and light (cream).
// The column under test is on the near half of the glass (|angle from the camera| <= 60 degrees), where the wall is seen face on.
// Run: node tools/fig16/check_pint3d.cjs  (needs playwright; the pages are served from public/ by request interception)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..', '..', 'public');
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml' };
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  await p.route((u) => u.hostname === 'local.test', (r) => { const f = path.join(ROOT, decodeURIComponent(new URL(r.request().url()).pathname)); if (!fs.existsSync(f)) return r.fulfill({ status: 404, body: '' }); r.fulfill({ status: 200, body: fs.readFileSync(f), contentType: types[path.extname(f)] || 'application/octet-stream' }); });
  await p.route((u) => u.hostname !== 'local.test', (r) => r.abort());
  let fails = 0;
  for (const [ride, t] of [['kerb_full.json', 0.6], ['kerb_full.json', 2.0], ['resonant_off.json', 0.5], ['kerb_off.json', 0.70], ['bump25_off.json', 1.2]]) {
    await p.goto(`http://local.test/simulations/guinness-cart-control.html?ride=${ride}`); await p.waitForTimeout(6000);
    await p.evaluate((t) => window.Guinness16.seek(t), t); await p.waitForTimeout(1500);
    const res = await p.evaluate(() => {
      const x = window.Pint3D.last; if (!x || !x.ride) return { error: 'no close-up' };
      x.drawn = null; x.render();
      const cv = x.cv, c2 = document.createElement('canvas'); c2.width = cv.width; c2.height = cv.height; const g = c2.getContext('2d'); g.drawImage(cv, 0, 0);
      const cam = x.camera, V = cam.position.constructor, az = Math.atan2(-cam.position.z, cam.position.x), out = [];
      for (let q = -6; q <= 6; q++) {
        const th = az + q * Math.PI / 18; if (Math.abs(q) > 6) continue;
        const v = x.ride.atInward(x.k, x.Rz(x.ride.fill) - 0.0008, th), r = x.Rz(v[0]) - 0.0004;
        const px = (z) => { const w = new V(r * Math.cos(th), z, -r * Math.sin(th)).project(cam); return [Math.round((w.x + 1) / 2 * cv.width), Math.round((1 - w.y) / 2 * cv.height)]; };
        const read = (pt) => Array.from(g.getImageData(pt[0], pt[1], 1, 1).data);
        const below = read(px(v[0] - 0.004)), head = v[1] > 0.004 ? read(px(v[0] + v[1] / 2)) : null;
        out.push({ deg: Math.round(q * 10), H_mm: +(v[0] * 1e3).toFixed(2), hf_mm: +(v[1] * 1e3).toFixed(2), below, head,
          ok_below: below[3] > 0 && (below[0] + below[1] + below[2]) / 3 < 90, ok_head: head == null || (head[3] > 0 && (head[0] + head[1] + head[2]) / 3 > 150) });
      }
      return { k: x.k, rows: out };
    });
    if (res.error) { console.log(ride, t, res.error); fails++; continue; }
    const bad = res.rows.filter((r) => !r.ok_below || !r.ok_head);
    fails += bad.length;
    console.log(`${ride} t=${t} s, stored picture ${res.k}: ${res.rows.length - bad.length} of ${res.rows.length} columns pass` + (bad.length ? ' FAIL ' + JSON.stringify(bad) : '') +
      ` (e.g. ${JSON.stringify(res.rows[6])})`);
  }
  await b.close(); process.exit(fails ? 1 : 0);
})();

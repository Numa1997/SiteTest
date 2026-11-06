const { chromium } = require('playwright'); const path = require('path');
(async () => { const br = await chromium.launch(); const pg = await br.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message + ' @ ' + (e.stack || '').split('\n').slice(1, 3).join(' | ')));
  await pg.goto('file://' + path.resolve(__dirname, '../../../../../public/' + (process.env.LANG2 || '') + 'simulations/double-inverted-pendulum.html')); await pg.waitForTimeout(1500); console.log(errs); await br.close(); })();

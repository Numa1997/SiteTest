'use strict';

// End-to-end test of public/scripts/simdata.js in headless Chromium against a local fixture server.
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { chromium } = require('playwright');

const REPO_ROOT = path.resolve(__dirname, '..', '..');
const SIMDATA_PATH = path.join(REPO_ROOT, 'public', 'scripts', 'simdata.js');
const FLAKY_URL_PATH = '/data/sims/w/2026-11-22/flaky.bin';

function sha256(buf) {
  return crypto.createHash('sha256').update(buf).digest('hex');
}

function writeFile(root, relPath, data) {
  const full = path.join(root, relPath);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, data);
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

function buildFixture(tmpDir) {
  const aOld = crypto.randomBytes(1000);
  let aNew = crypto.randomBytes(1000);
  while (aNew.equals(aOld)) aNew = crypto.randomBytes(1000);

  const pPack = crypto.randomBytes(5000);
  const xBytes = pPack.subarray(1000, 1300);
  const yBytes = pPack.subarray(4000, 5000);
  const f2Bytes = crypto.randomBytes(256);
  const badBytes = crypto.randomBytes(512);
  const flakyBytes = crypto.randomBytes(768);
  const realBadSha = sha256(badBytes);
  const wrongBadSha = realBadSha.startsWith('0') ? 'f'.repeat(64) : '0'.repeat(64);

  const commits = {
    a: '1'.repeat(40),
    b: '2'.repeat(40),
    c: '3'.repeat(40),
    d: '4'.repeat(40),
    e: '5'.repeat(40),
    f: '6'.repeat(40),
  };

  writeFile(tmpDir, 'data/sims/t/2026-11-20/a.bin', aOld);
  writeFile(tmpDir, 'r2/sims/t/2026-11-22-v2/a.bin', aNew);
  writeFile(tmpDir, 'r2/sims/t/2026-11-22-v2/p.pack', pPack);
  writeFile(tmpDir, 'data/sims/t/2026-11-21/f2.bin', f2Bytes);
  writeFile(tmpDir, 'data/sims/u/2026-11-22/bad.bin', badBytes);
  writeFile(tmpDir, 'data/sims/w/2026-11-22/flaky.bin', flakyBytes);

  const generations = {
    generations: [
      {
        sim: 't',
        date: '2026-11-20',
        version: 1,
        commit: commits.a,
        format: 1,
        store: 'repo',
        files: {
          'a.bin': { bytes: aOld.length, sha256: sha256(aOld) },
        },
      },
      {
        sim: 't',
        date: '2026-11-22',
        version: 2,
        commit: commits.b,
        format: 1,
        live_ok: true,
        store: 'r2',
        run: '2026-11-22-v2',
        files: {
          'a.bin': { bytes: aNew.length, sha256: sha256(aNew) },
          'p.pack': { bytes: pPack.length, sha256: sha256(pPack) },
        },
        parts: {
          'x.bin': { pack: 'p.pack', offset: 1000, bytes: xBytes.length, sha256: sha256(xBytes) },
          'y.bin': { pack: 'p.pack', offset: 4000, bytes: yBytes.length, sha256: sha256(yBytes) },
        },
      },
      {
        sim: 't',
        date: '2026-11-23',
        version: 3,
        commit: commits.c,
        format: 1,
        live_ok: false,
        store: 'r2',
        run: '2026-11-23-v3',
        files: {},
      },
      {
        sim: 't',
        date: '2026-11-21',
        version: 1,
        commit: commits.d,
        format: 2,
        store: 'repo',
        files: {
          'f2.bin': { bytes: f2Bytes.length, sha256: sha256(f2Bytes) },
        },
      },
      {
        sim: 'u',
        date: '2026-11-22',
        version: 1,
        commit: commits.e,
        format: 1,
        store: 'repo',
        files: {
          'bad.bin': { bytes: badBytes.length, sha256: wrongBadSha },
        },
      },
      {
        sim: 'w',
        date: '2026-11-22',
        version: 1,
        commit: commits.f,
        format: 1,
        store: 'repo',
        files: {
          'flaky.bin': { bytes: flakyBytes.length, sha256: sha256(flakyBytes) },
        },
      },
    ],
  };

  writeFile(tmpDir, 'data/sims/generations.json', JSON.stringify(generations, null, 2));

  return { aNew, xBytes, yBytes, flakyBytes, commits };
}

function startServer(tmpDir) {
  const simdataSource = fs.readFileSync(SIMDATA_PATH);
  const counts = new Map();
  const requests = new Map();
  let flakyFirstFailed = false;

  function reset() {
    counts.clear();
    requests.clear();
    flakyFirstFailed = false;
  }

  function record(urlPath, entry) {
    counts.set(urlPath, (counts.get(urlPath) || 0) + 1);
    if (!requests.has(urlPath)) requests.set(urlPath, []);
    requests.get(urlPath).push(entry);
  }

  const server = http.createServer((req, res) => {
    const urlPath = new URL(req.url, 'http://127.0.0.1').pathname;

    // Disable browser HTTP caching so request counts measure SimData's own cache and retry logic.
    if (urlPath === '/' || urlPath === '/test.html') {
      res.writeHead(200, {
        'content-type': 'text/html; charset=utf-8',
        'cache-control': 'no-store',
      });
      res.end('<!doctype html><meta charset="utf-8"><script src="/scripts/simdata.js"></script>');
      return;
    }

    if (urlPath === '/scripts/simdata.js') {
      res.writeHead(200, {
        'content-type': 'application/javascript; charset=utf-8',
        'cache-control': 'no-store',
      });
      res.end(req.method === 'HEAD' ? undefined : simdataSource);
      return;
    }

    if (req.method !== 'GET' && req.method !== 'HEAD') {
      record(urlPath, { method: req.method, range: req.headers.range || null, status: 405 });
      res.writeHead(405, { 'cache-control': 'no-store' });
      res.end('method not allowed');
      return;
    }

    if (urlPath === FLAKY_URL_PATH && !flakyFirstFailed) {
      flakyFirstFailed = true;
      record(urlPath, { method: req.method, range: req.headers.range || null, status: 503 });
      res.writeHead(503, { 'cache-control': 'no-store' });
      res.end('service unavailable');
      return;
    }

    const fullPath = path.resolve(tmpDir, urlPath.replace(/^\/+/, ''));
    if (!fullPath.startsWith(tmpDir + path.sep) || !fs.existsSync(fullPath) || !fs.statSync(fullPath).isFile()) {
      record(urlPath, { method: req.method, range: req.headers.range || null, status: 404 });
      res.writeHead(404, { 'cache-control': 'no-store' });
      res.end('not found');
      return;
    }

    const data = fs.readFileSync(fullPath);
    const range = req.headers.range;
    const m = range ? /^bytes=(\d+)-(\d+)$/.exec(range.trim()) : null;

    if (m) {
      const start = Number(m[1]);
      const end = Number(m[2]);
      if (start >= data.length || end < start) {
        record(urlPath, { method: req.method, range, status: 416 });
        res.writeHead(416, {
          'content-range': `bytes */${data.length}`,
          'cache-control': 'no-store',
        });
        res.end();
        return;
      }
      const last = Math.min(end, data.length - 1);
      const part = data.subarray(start, last + 1);
      record(urlPath, { method: req.method, range, status: 206 });
      res.writeHead(206, {
        'content-type': 'application/octet-stream',
        'content-range': `bytes ${start}-${last}/${data.length}`,
        'content-length': String(part.length),
        'accept-ranges': 'bytes',
        'cache-control': 'no-store',
      });
      res.end(req.method === 'HEAD' ? undefined : part);
      return;
    }

    record(urlPath, { method: req.method, range: range || null, status: 200 });
    res.writeHead(200, {
      'content-type': urlPath.endsWith('.json') ? 'application/json; charset=utf-8' : 'application/octet-stream',
      'content-length': String(data.length),
      'accept-ranges': 'bytes',
      'cache-control': 'no-store',
    });
    res.end(req.method === 'HEAD' ? undefined : data);
  });

  return new Promise((resolve, reject) => {
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ server, port, counts, requests, reset });
    });
  });
}

async function waitForCount(counts, key, target, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if ((counts.get(key) || 0) >= target) return true;
    await new Promise((r) => setTimeout(r, 15));
  }
  return (counts.get(key) || 0) >= target;
}

async function main() {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'simdata-test-'));
  let server = null;
  let browser = null;
  let passed = 0;
  let failed = 0;

  try {
    const fixture = buildFixture(tmpDir);
    const srv = await startServer(tmpDir);
    server = srv.server;
    const { port, counts, requests, reset } = srv;
    const baseUrl = `http://127.0.0.1:${port}/test.html`;

    browser = await chromium.launch();
    const page = await browser.newPage();

    // Give each case a fresh page load and zeroed server counters so reports and caches never mix.
    async function runCase(name, fn) {
      reset();
      try {
        await page.goto(baseUrl, { waitUntil: 'load' });
        await fn();
        passed++;
        console.log(`PASS ${name}`);
      } catch (err) {
        failed++;
        console.log(`FAIL ${name}: ${err && err.message ? err.message : String(err)}`);
      }
    }

    await runCase('1_open_t_picks_b', async () => {
      const info = await page.evaluate(async () => {
        const g = await SimData.open('t');
        return {
          sim: g.sim,
          date: g.date,
          version: g.version,
          commit: g.commit,
          format: g.format,
          store: g.store,
        };
      });
      assert(info.date === '2026-11-22', `expected date 2026-11-22, got ${info.date}`);
      assert(info.version === 2, `expected version 2, got ${info.version}`);
      assert(info.store === 'r2', `expected store r2, got ${info.store}`);
      assert(info.format === 1, `expected format 1, got ${info.format}`);
      assert(info.commit === fixture.commits.b, `expected commit ${fixture.commits.b}, got ${info.commit}`);
    });

    await runCase('2_open_t_format_2_picks_d', async () => {
      const info = await page.evaluate(async () => {
        const g = await SimData.open('t', { format: 2 });
        return {
          date: g.date,
          version: g.version,
          commit: g.commit,
          format: g.format,
          store: g.store,
        };
      });
      assert(info.date === '2026-11-21', `expected date 2026-11-21, got ${info.date}`);
      assert(info.version === 1, `expected version 1, got ${info.version}`);
      assert(info.store === 'repo', `expected store repo, got ${info.store}`);
      assert(info.format === 2, `expected format 2, got ${info.format}`);
      assert(info.commit === fixture.commits.d, `expected commit ${fixture.commits.d}, got ${info.commit}`);
    });

    await runCase('3_open_nope_rejects', async () => {
      const msg = await page.evaluate(async () => {
        try {
          await SimData.open('nope');
          return null;
        } catch (err) {
          return err.message;
        }
      });
      assert(msg === 'no stored data for nope, format 1', `unexpected error: ${msg}`);
    });

    await runCase('4_url_r2_repo_and_pack', async () => {
      const urls = await page.evaluate(async () => {
        const gb = await SimData.open('t');
        const gd = await SimData.open('t', { format: 2 });
        return {
          bA: gb.url('a.bin'),
          dF2: gd.url('f2.bin'),
          bX: gb.url('x.bin'),
        };
      });
      assert(urls.bA === '/r2/sims/t/2026-11-22-v2/a.bin', `bad b url: ${urls.bA}`);
      assert(urls.dF2 === '/data/sims/t/2026-11-21/f2.bin', `bad d url: ${urls.dF2}`);
      assert(urls.bX === '/r2/sims/t/2026-11-22-v2/p.pack', `bad part pack url: ${urls.bX}`);
    });

    await runCase('5_file_once_and_exact_bytes', async () => {
      const key = '/r2/sims/t/2026-11-22-v2/a.bin';
      const got = await page.evaluate(async () => {
        const g = await SimData.open('t');
        const b1 = await g.file('a.bin');
        const b2 = await g.file('a.bin');
        return {
          first: Array.from(new Uint8Array(b1)),
          second: Array.from(new Uint8Array(b2)),
        };
      });
      assert(Buffer.from(got.first).equals(fixture.aNew), 'first download bytes differ from fixture');
      assert(Buffer.from(got.second).equals(fixture.aNew), 'second call bytes differ from fixture');
      assert(counts.get(key) === 1, `expected 1 request for a.bin, got ${counts.get(key)}`);
    });

    await runCase('6_parts_by_range', async () => {
      const key = '/r2/sims/t/2026-11-22-v2/p.pack';
      const got = await page.evaluate(async () => {
        const g = await SimData.open('t');
        const bx = await g.part('x.bin');
        const by = await g.part('y.bin');
        return {
          x: Array.from(new Uint8Array(bx)),
          y: Array.from(new Uint8Array(by)),
        };
      });
      assert(Buffer.from(got.x).equals(fixture.xBytes), 'x.bin bytes differ from p.pack[1000..1299]');
      assert(Buffer.from(got.y).equals(fixture.yBytes), 'y.bin bytes differ from p.pack[4000..4999]');
      const log = requests.get(key) || [];
      assert(log.length === 2, `expected 2 range requests, got ${log.length}`);
      assert(log[0].range === 'bytes=1000-1299' && log[0].status === 206, `unexpected first range: ${JSON.stringify(log[0])}`);
      assert(log[1].range === 'bytes=4000-4999' && log[1].status === 206, `unexpected second range: ${JSON.stringify(log[1])}`);
    });

    await runCase('7_bad_sha256_rejects_and_reports', async () => {
      const res = await page.evaluate(async () => {
        const gu = await SimData.open('u');
        let msg = null;
        try {
          await gu.file('bad.bin');
        } catch (err) {
          msg = err.message;
        }
        return { msg, reportU: window.__simData && window.__simData.all && window.__simData.all.u };
      });
      const expected = 'bad.bin: SHA-256 differs from generations.json';
      assert(res.msg === expected, `unexpected error: ${res.msg}`);
      assert(res.reportU && res.reportU.sha_ok === false, `expected sha_ok false, got ${JSON.stringify(res.reportU)}`);
      assert(res.reportU.err === expected, `expected err "${expected}", got "${res.reportU.err}"`);
    });

    await runCase('8_host_fail_keeps_content_and_replaces_notice', async () => {
      const res = await page.evaluate(async () => {
        const div = document.createElement('div');
        const span = document.createElement('span');
        span.textContent = 'keep';
        div.appendChild(span);
        document.body.appendChild(div);

        const gu = await SimData.open('u', { host: div });
        try {
          await gu.file('bad.bin');
        } catch (_) {}
        const afterFirst = {
          failCount: div.querySelectorAll('p.simdata-fail').length,
          spanText: div.querySelector('span') ? div.querySelector('span').textContent : null,
        };

        try {
          await gu.file('missing.bin');
        } catch (_) {}
        const afterSecond = {
          failCount: div.querySelectorAll('p.simdata-fail').length,
          spanText: div.querySelector('span') ? div.querySelector('span').textContent : null,
        };
        return { afterFirst, afterSecond };
      });
      assert(res.afterFirst.failCount === 1, `expected 1 fail notice after first error, got ${res.afterFirst.failCount}`);
      assert(res.afterFirst.spanText === 'keep', `expected span "keep" after first error, got ${res.afterFirst.spanText}`);
      assert(res.afterSecond.failCount === 1, `expected 1 fail notice after second error, got ${res.afterSecond.failCount}`);
      assert(res.afterSecond.spanText === 'keep', `expected span "keep" after second error, got ${res.afterSecond.spanText}`);
    });

    await runCase('9_report_all_t_and_top_level', async () => {
      const report = await page.evaluate(async () => {
        const g = await SimData.open('t');
        await g.file('a.bin');
        await g.part('x.bin');
        await g.part('y.bin');
        return {
          top: {
            sim: window.__simData.sim,
            sha_ok: window.__simData.sha_ok,
            files: window.__simData.files,
            err: window.__simData.err,
            gen: window.__simData.gen,
          },
          allT: window.__simData.all.t,
        };
      });
      const expectedFiles = JSON.stringify(['a.bin', 'x.bin', 'y.bin']);
      assert(report.allT && report.allT.sha_ok === true, `expected all.t.sha_ok true, got ${JSON.stringify(report.allT)}`);
      assert(JSON.stringify(report.allT.files) === expectedFiles, `expected all.t.files ${expectedFiles}, got ${JSON.stringify(report.allT.files)}`);
      assert(report.allT.err === null, `expected all.t.err null, got ${report.allT.err}`);
      assert(report.allT.gen && report.allT.gen.commit === fixture.commits.b, `expected all.t.gen.commit ${fixture.commits.b}`);

      assert(report.top.sim === 't', `expected top sim "t", got ${report.top.sim}`);
      assert(report.top.sha_ok === true, `expected top sha_ok true, got ${report.top.sha_ok}`);
      assert(JSON.stringify(report.top.files) === expectedFiles, `expected top files ${expectedFiles}, got ${JSON.stringify(report.top.files)}`);
      assert(report.top.err === null, `expected top err null, got ${report.top.err}`);
      assert(report.top.gen && report.top.gen.commit === fixture.commits.b, `expected top gen.commit ${fixture.commits.b}`);
    });

    await runCase('10_generations_json_requested_once', async () => {
      await page.evaluate(async () => {
        await SimData.open('t');
        await SimData.open('u');
        await SimData.open('t');
      });
      const n = counts.get('/data/sims/generations.json') || 0;
      assert(n === 1, `expected generations.json count 1, got ${n}`);
    });

    await runCase('11_prefetch_starts_download_before_file', async () => {
      const key = '/r2/sims/t/2026-11-22-v2/a.bin';
      await page.evaluate(async () => {
        window._g = await SimData.open('t');
        window._g.prefetch(['a.bin']);
      });
      const rose = await waitForCount(counts, key, 1, 2000);
      assert(rose, `expected server count for ${key} to rise to 1 before file() was called`);

      const bytes = await page.evaluate(async () => Array.from(new Uint8Array(await window._g.file('a.bin'))));
      assert(Buffer.from(bytes).equals(fixture.aNew), 'prefetched bytes differ from fixture');
      assert(counts.get(key) === 1, `expected count to stay 1 after file(), got ${counts.get(key)}`);
    });

    await runCase('12_f1_shared_cache_across_open', async () => {
      const key = '/r2/sims/t/2026-11-22-v2/a.bin';
      const got = await page.evaluate(async () => {
        const g1 = await SimData.open('t');
        const g2 = await SimData.open('t');
        const p1 = g1.file('a.bin');
        const p2 = g2.file('a.bin');
        const b1 = await p1;
        const b2 = await p2;
        return {
          samePromise: p1 === p2,
          first: Array.from(new Uint8Array(b1)),
          second: Array.from(new Uint8Array(b2)),
        };
      });
      assert(got.samePromise, 'expected g1.file and g2.file to share the same cached promise');
      assert(Buffer.from(got.first).equals(fixture.aNew), 'first bytes differ from fixture');
      assert(Buffer.from(got.second).equals(fixture.aNew), 'second bytes differ from fixture');
      assert(counts.get(key) === 1, `expected 1 request for a.bin across both open() calls, got ${counts.get(key)}`);
    });

    await runCase('13_f2_second_open_keeps_report', async () => {
      const state = await page.evaluate(async () => {
        const g1 = await SimData.open('t');
        await g1.file('a.bin');
        await SimData.open('t');
        return {
          allT: window.__simData.all.t,
          topFiles: window.__simData.files,
          topShaOk: window.__simData.sha_ok,
        };
      });
      assert(JSON.stringify(state.allT.files) === JSON.stringify(['a.bin']), `expected all.t.files ["a.bin"], got ${JSON.stringify(state.allT.files)}`);
      assert(state.allT.sha_ok === true, `expected all.t.sha_ok true, got ${state.allT.sha_ok}`);
      assert(state.allT.err === null, `expected all.t.err null, got ${state.allT.err}`);
      assert(JSON.stringify(state.topFiles) === JSON.stringify(['a.bin']), `expected top files ["a.bin"], got ${JSON.stringify(state.topFiles)}`);
      assert(state.topShaOk === true, `expected top sha_ok true, got ${state.topShaOk}`);
    });

    await runCase('14_f3_retry_503_once_and_no_retry_bad_sha', async () => {
      const res = await page.evaluate(async () => {
        const gw = await SimData.open('w');
        const flakyBuf = await gw.file('flaky.bin');
        const gu = await SimData.open('u');
        let badErr = null;
        try {
          await gu.file('bad.bin');
        } catch (err) {
          badErr = err.message;
        }
        return {
          flaky: Array.from(new Uint8Array(flakyBuf)),
          badErr,
        };
      });
      assert(Buffer.from(res.flaky).equals(fixture.flakyBytes), 'flaky.bin bytes differ from fixture after retry');
      assert(counts.get(FLAKY_URL_PATH) === 2, `expected 2 requests for flaky.bin, got ${counts.get(FLAKY_URL_PATH)}`);
      assert(res.badErr === 'bad.bin: SHA-256 differs from generations.json', `unexpected bad.bin error: ${res.badErr}`);
      const badCount = counts.get('/data/sims/u/2026-11-22/bad.bin') || 0;
      assert(badCount === 1, `expected 1 request for bad.bin (no retry on SHA mismatch), got ${badCount}`);
    });
  } finally {
    if (browser) await browser.close();
    if (server) await new Promise((resolve) => server.close(resolve));
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }

  console.log(`${passed} passed, ${failed} failed`);
  process.exitCode = failed ? 1 : 0;
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});


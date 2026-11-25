// Shared loader for stored simulation data (computed once on Kaggle, stored in the repository or in Cloudflare R2).
// Every page opens its simulation through window.SimData, which reads generations.json once per visit, picks the
// newest usable generation for the requested format, retries transient fetch failures once, verifies every downloaded
// file or byte range by length and SHA-256 before returning bytes to the page, shares one visit-wide download cache
// across all generation objects, and keeps window.__simData updated for the live check without wiping prior results.
(function () {
  'use strict';

  const RETRY_DELAY_MS = 500;
  const RETRY_STATUSES = { 500: true, 502: true, 503: true, 504: true };

  // Visit-wide caches shared by every open() call on the page.
  const indexCache = Object.create(null);
  const dataCache = Object.create(null);
  let latestSim = null;

  function normalizeBase(base) {
    if (!base) return '/';
    return base.endsWith('/') ? base : base + '/';
  }

  function delay(ms) {
    return new Promise(function (resolve) {
      setTimeout(resolve, ms);
    });
  }

  // Retry once after 500 ms on network failure or HTTP 500/502/503/504; never retry 4xx or verification failures.
  async function fetchWithRetry(url, init) {
    let res;
    try {
      res = await fetch(url, init);
    } catch (err) {
      await delay(RETRY_DELAY_MS);
      return fetch(url, init);
    }
    if (RETRY_STATUSES[res.status]) {
      if (res.body && typeof res.body.cancel === 'function') {
        res.body.cancel().catch(function () {});
      }
      await delay(RETRY_DELAY_MS);
      return fetch(url, init);
    }
    return res;
  }

  function ensureReport(sim) {
    if (!window.__simData) {
      window.__simData = {
        sim: sim,
        gen: null,
        sha_ok: false,
        files: [],
        err: null,
        all: {},
      };
    }
  }

  // Keep the top-level fields aligned with the most recently opened simulation, matching what existing live probes read.
  function syncTop() {
    if (!window.__simData || latestSim === null) return;
    const cur = window.__simData.all[latestSim];
    if (!cur) return;
    window.__simData.sim = cur.sim;
    window.__simData.gen = cur.gen;
    window.__simData.sha_ok = cur.sha_ok;
    window.__simData.files = cur.files;
    window.__simData.err = cur.err;
  }

  function sameGeneration(gen, entry) {
    return !!gen && gen.date === entry.date && gen.version === entry.version;
  }

  async function sha256Hex(buf) {
    if (!window.crypto || !window.crypto.subtle) {
      throw new Error('Web Crypto is unavailable in this context');
    }
    const digest = await window.crypto.subtle.digest('SHA-256', buf);
    const bytes = new Uint8Array(digest);
    let hex = '';
    for (let i = 0; i < bytes.length; i++) {
      hex += bytes[i].toString(16).padStart(2, '0');
    }
    return hex;
  }

  // Fetch and parse generations.json once per page visit (keyed by base URL) so multiple open() calls share one request.
  function loadIndex(base) {
    const url = base + 'data/sims/generations.json';
    if (!indexCache[url]) {
      indexCache[url] = (async function () {
        let res;
        try {
          res = await fetchWithRetry(url);
        } catch (err) {
          throw new Error('generations.json: ' + (err && err.message ? err.message : String(err)));
        }
        if (!res.ok) {
          throw new Error('generations.json: HTTP ' + res.status);
        }
        let data;
        try {
          data = await res.json();
        } catch (err) {
          throw new Error('generations.json: ' + (err && err.message ? err.message : String(err)));
        }
        if (!data || !Array.isArray(data.generations)) {
          throw new Error('generations.json: missing generations list');
        }
        return data.generations;
      })();
    }
    return indexCache[url];
  }

  function fail(host, message) {
    if (!host || typeof host.querySelectorAll !== 'function') return;
    // Replace only SimData's own notice so the page's own elements stay intact.
    const existing = host.querySelectorAll('p.simdata-fail');
    for (let i = 0; i < existing.length; i++) {
      existing[i].remove();
    }
    const doc = host.ownerDocument || document;
    const p = doc.createElement('p');
    p.className = 'simdata-fail';
    const detail = message ? String(message) : 'unknown error';
    p.textContent = 'The stored data for this figure could not be loaded (' + detail + ').';
    host.appendChild(p);
  }

  async function open(sim, opts) {
    const options = opts || {};
    const format = options.format == null ? 1 : options.format;
    const base = normalizeBase(options.base);
    const host = options.host || null;

    // Create the top-level report on the first open(), without overwriting any existing report for this sim.
    ensureReport(sim);
    if (!window.__simData.all[sim]) {
      window.__simData.all[sim] = {
        sim: sim,
        gen: null,
        sha_ok: false,
        files: [],
        err: null,
      };
    }
    latestSim = sim;
    syncTop();

    let list;
    try {
      list = await loadIndex(base);
    } catch (err) {
      const wrapped = err instanceof Error ? err : new Error(String(err));
      const cur = window.__simData.all[sim];
      if (cur.err === null) cur.err = wrapped.message;
      cur.sha_ok = false;
      latestSim = sim;
      syncTop();
      fail(host, wrapped.message);
      throw wrapped;
    }

    let best = null;
    for (let i = 0; i < list.length; i++) {
      const entry = list[i];
      if (!entry || entry.sim !== sim) continue;
      const entryFormat = entry.format == null ? 1 : entry.format;
      if (entryFormat !== format) continue;
      if (entry.live_ok === false) continue;
      if (!best) {
        best = entry;
        continue;
      }
      const eDate = String(entry.date || '');
      const bDate = String(best.date || '');
      if (eDate > bDate || (eDate === bDate && Number(entry.version || 0) > Number(best.version || 0))) {
        best = entry;
      }
    }

    if (!best) {
      const err = new Error('no stored data for ' + sim + ', format ' + format);
      const cur = window.__simData.all[sim];
      if (cur.err === null) cur.err = err.message;
      cur.sha_ok = false;
      latestSim = sim;
      syncTop();
      fail(host, err.message);
      throw err;
    }

    const store = best.store || 'repo';
    const resolvedFormat = best.format == null ? 1 : best.format;
    const genInfo = {
      date: best.date,
      version: best.version,
      commit: best.commit,
      format: resolvedFormat,
      store: store,
    };

    // Preserve verified files and errors when reopening the same generation; start fresh only for a different generation.
    const existing = window.__simData.all[sim];
    let rec;
    if (existing && (existing.gen === null || sameGeneration(existing.gen, best))) {
      rec = existing;
      rec.gen = genInfo;
    } else {
      rec = {
        sim: sim,
        gen: genInfo,
        sha_ok: false,
        files: [],
        err: null,
      };
      window.__simData.all[sim] = rec;
    }
    latestSim = sim;
    syncTop();

    function fileAddress(fileName) {
      if (store === 'r2') {
        return base + 'r2/sims/' + sim + '/' + best.run + '/' + fileName;
      }
      return base + 'data/sims/' + sim + '/' + best.date + '/' + fileName;
    }

    function url(name) {
      if (best.parts && Object.prototype.hasOwnProperty.call(best.parts, name)) {
        return fileAddress(best.parts[name].pack);
      }
      return fileAddress(name);
    }

    function recordPass(name) {
      if (rec.files.indexOf(name) === -1) rec.files.push(name);
      rec.sha_ok = rec.err === null && rec.files.length > 0;
      syncTop();
    }

    function recordFail(err, notifyHost) {
      if (rec.err === null) rec.err = err.message;
      rec.sha_ok = false;
      syncTop();
      if (notifyHost) fail(host, err.message);
    }

    // Share one promise per full address (plus range for parts) across all generation objects opened during the visit.
    function startCached(cacheKey, name, fromPrefetch, fetchAndVerify) {
      let cached = dataCache[cacheKey];
      if (cached) {
        if (cached.done) {
          recordPass(name);
        } else if (cached.error) {
          recordFail(cached.error, !fromPrefetch);
        } else {
          cached.waiters.push({
            recordPass: recordPass,
            recordFail: recordFail,
            name: name,
            notifyHost: !fromPrefetch,
          });
        }
        return cached.promise;
      }

      cached = {
        promise: null,
        done: false,
        error: null,
        waiters: [
          {
            recordPass: recordPass,
            recordFail: recordFail,
            name: name,
            notifyHost: !fromPrefetch,
          },
        ],
      };

      cached.promise = (async function () {
        try {
          const buf = await fetchAndVerify();
          cached.done = true;
          const waiters = cached.waiters;
          cached.waiters = [];
          for (let i = 0; i < waiters.length; i++) {
            waiters[i].recordPass(waiters[i].name);
          }
          return buf;
        } catch (err) {
          const wrapped = err instanceof Error ? err : new Error(name + ': ' + String(err));
          cached.error = wrapped;
          const waiters = cached.waiters;
          cached.waiters = [];
          for (let i = 0; i < waiters.length; i++) {
            waiters[i].recordFail(wrapped, waiters[i].notifyHost);
          }
          throw wrapped;
        }
      })();

      dataCache[cacheKey] = cached;
      return cached.promise;
    }

    function rejectImmediate(err, fromPrefetch) {
      recordFail(err, !fromPrefetch);
      return Promise.reject(err);
    }

    function startFile(name, fromPrefetch) {
      const files = best.files;
      if (!files || !Object.prototype.hasOwnProperty.call(files, name)) {
        return rejectImmediate(new Error(name + ': not listed in generations.json'), fromPrefetch);
      }
      const meta = files[name];
      const addr = fileAddress(name);
      return startCached(addr, name, fromPrefetch, async function () {
        let res;
        try {
          res = await fetchWithRetry(addr);
        } catch (err) {
          throw new Error(name + ': ' + (err && err.message ? err.message : String(err)));
        }
        if (res.status !== 200) {
          throw new Error(name + ': HTTP ' + res.status);
        }
        let buf;
        try {
          buf = await res.arrayBuffer();
        } catch (err) {
          throw new Error(name + ': ' + (err && err.message ? err.message : String(err)));
        }
        if (typeof meta.bytes === 'number' && buf.byteLength !== meta.bytes) {
          throw new Error(name + ': expected ' + meta.bytes + ' bytes, got ' + buf.byteLength);
        }
        let hex;
        try {
          hex = await sha256Hex(buf);
        } catch (err) {
          throw new Error(name + ': ' + (err && err.message ? err.message : String(err)));
        }
        if (typeof meta.sha256 !== 'string' || hex !== meta.sha256.toLowerCase()) {
          throw new Error(name + ': SHA-256 differs from generations.json');
        }
        return buf;
      });
    }

    function startPart(name, fromPrefetch) {
      const parts = best.parts;
      if (!parts || !Object.prototype.hasOwnProperty.call(parts, name)) {
        return rejectImmediate(new Error(name + ': not listed in generations.json'), fromPrefetch);
      }
      const meta = parts[name];
      if (!meta || !meta.pack || typeof meta.offset !== 'number' || typeof meta.bytes !== 'number' || meta.bytes <= 0) {
        return rejectImmediate(new Error(name + ': invalid part entry in generations.json'), fromPrefetch);
      }
      const addr = fileAddress(meta.pack);
      const rangeHeader = 'bytes=' + meta.offset + '-' + (meta.offset + meta.bytes - 1);
      const cacheKey = addr + '\0' + rangeHeader;
      return startCached(cacheKey, name, fromPrefetch, async function () {
        let res;
        try {
          res = await fetchWithRetry(addr, { headers: { Range: rangeHeader } });
        } catch (err) {
          throw new Error(name + ': ' + (err && err.message ? err.message : String(err)));
        }
        if (res.status !== 206) {
          throw new Error(name + ': HTTP ' + res.status);
        }
        let buf;
        try {
          buf = await res.arrayBuffer();
        } catch (err) {
          throw new Error(name + ': ' + (err && err.message ? err.message : String(err)));
        }
        if (buf.byteLength !== meta.bytes) {
          throw new Error(name + ': expected ' + meta.bytes + ' bytes, got ' + buf.byteLength);
        }
        let hex;
        try {
          hex = await sha256Hex(buf);
        } catch (err) {
          throw new Error(name + ': ' + (err && err.message ? err.message : String(err)));
        }
        if (typeof meta.sha256 !== 'string' || hex !== meta.sha256.toLowerCase()) {
          throw new Error(name + ': SHA-256 differs from generations.json');
        }
        return buf;
      });
    }

    function file(name) {
      return startFile(name, false);
    }

    function part(name) {
      return startPart(name, false);
    }

    // Start downloads ahead of time; attach an empty rejection handler so failures wait for the caller's file()/part() call.
    function prefetch(names) {
      if (!Array.isArray(names)) return;
      for (let i = 0; i < names.length; i++) {
        const name = names[i];
        const isPart = best.parts && Object.prototype.hasOwnProperty.call(best.parts, name);
        const p = isPart ? startPart(name, true) : startFile(name, true);
        p.catch(function () {});
      }
    }

    return {
      sim: sim,
      date: best.date,
      version: best.version,
      commit: best.commit,
      format: resolvedFormat,
      store: store,
      entry: best,
      url: url,
      file: file,
      part: part,
      prefetch: prefetch,
    };
  }

  window.SimData = {
    open: open,
    fail: fail,
  };
})();


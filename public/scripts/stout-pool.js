/* Fig. 12: the stout solver's loops shared over worker threads (scripts/stout-worker.js).
 *
 * Four loops of a fluid step are split: the level-set search (by cells), grid-to-particle (by particles), particle-to-grid
 * (by slabs of grid layers) and advection (by particles). Each thread computes exactly what the single-thread loop
 * computes for its share, in the same order, so the numbers are identical to the last digit (tools/fig12/same.cjs and
 * notes/fig12/threads-test.cjs check it). The pressure solve and the rest stay on the page's own thread.
 *
 * Needs SharedArrayBuffer, which a browser gives only to a cross-origin-isolated page (headers COOP same-origin and COEP
 * require-corp: public/_headers). The page's thread works too: P = workers + 1 shares; it waits for the workers by
 * spinning on a shared counter (a page's thread may not block).
 */
(function (root) {
  'use strict';
  // one share of task `task` for thread `idx` of `P`
  function share(f, cells, slab, task, idx, P, count, a, b) {
    const lo = Math.floor(count * idx / P), hi = Math.floor(count * (idx + 1) / P);
    if (task === 1) f.phiCells(cells, idx, count, a, b, P);       // every P-th cell: the costly cells by the wall are spread
    else if (task === 2) { for (let c = 0; c < 3; c++) f.transfer(c, false, lo, hi); }
    else if (task === 3) f.p2gSlab(slab[idx], slab[idx + 1]);
    else if (task === 4) f.advectRange(a, lo, hi);
  }

  function StoutPool(n, src) {
    this.n = n; this.P = n + 1;
    this.ctrl = new Int32Array(new SharedArrayBuffer(8));          // [generation, shares done]
    this.par = new Float64Array(new SharedArrayBuffer(5 * 8));     // [task, count, a, b, np]
    this.slab = new Int32Array(new SharedArrayBuffer(4 * (this.P + 1)));
    this.workers = []; for (let i = 0; i < n; i++) this.workers.push(new Worker(src));
    this.fluid = null; this.looping = false; this.cells = null;
  }
  // tell the workers to leave their loop (before a new fluid is attached)
  StoutPool.prototype.stop = function () {
    if (!this.looping) return;
    this.par[0] = 0; Atomics.store(this.ctrl, 1, 0); Atomics.add(this.ctrl, 0, 1); Atomics.notify(this.ctrl, 0);
    while (Atomics.load(this.ctrl, 1) < this.n) { /* wait */ }
    this.looping = false;
  };
  // share a fluid (made with {shared: true}) with the workers; the fluid uses them once all have answered
  StoutPool.prototype.attach = function (f) {
    if (this.fluid) this.fluid.pool = null;
    this.stop();
    this.fluid = f; f.pool = null;
    if (!f.sX || !f.blockOff) f.levelSet();     // makes the arrays of the search (a step starts with it anyway)
    this.cells = f.mk(Int32Array, f.nc);
    const view = {
      nx: f.nx, ny: f.ny, nz: f.nz, nc: f.nc, dx: f.dx, x0: f.x0, kernel: f.kernel, np: f.np, shared: true,
      u: f.u, v: f.v, w: f.w, mu: f.mu, mv: f.mv, mw: f.mw, px: f.px, py: f.py, pz: f.pz, pu: f.pu, pv: f.pv, pw: f.pw, pc: f.pc,
      phi: f.phi, cellStart: f.cellStart, sX: f.sX, sY: f.sY, sZ: f.sZ, sF: f.sF, sN: f.sN, cellImg: f.cellImg, blockOff: f.blockOff
    };
    let ready = 0;
    const self = this, gen = Atomics.load(this.ctrl, 0);
    this.workers.forEach((w, i) => {
      w.onmessage = function (e) {
        if (e.data === 'ready' && self.fluid === f && ++ready === self.n) { self.looping = true; f.pool = self; }
        else if (e.data && e.data.error) { self.failed = e.data.error; if (self.fluid) self.fluid.pool = null; if (typeof console !== 'undefined') console.error('stout worker: ' + e.data.error); }
      };
      w.postMessage({ cmd: 'attach', fluid: view, cells: this.cells, slab: this.slab, ctrl: this.ctrl, par: this.par, index: i + 1, P: this.P, gen: gen });
    });
  };
  // slabs of grid layers with about equal numbers of particles (from the particle count per cell, f.cnt)
  StoutPool.prototype.slabs = function (f) {
    const nxy = f.nx * f.ny, P = this.P, slab = this.slab;
    let tot = 0; for (let c = 0; c < f.nc; c++) tot += f.cnt[c];
    slab[0] = 0; let s = 1, acc = 0;
    for (let k = 0; k < f.nz && s < P; k++) {
      for (let c = k * nxy; c < (k + 1) * nxy; c++) acc += f.cnt[c];
      while (s < P && acc >= tot * s / P) slab[s++] = k + 1;
    }
    while (s < P) slab[s++] = f.nz;
    slab[P] = 1 << 30;
  };
  // run task on all threads and return when every share is done
  StoutPool.prototype.run = function (task, count, a, b) {
    const f = this.fluid, par = this.par, ctrl = this.ctrl;
    par[0] = task; par[1] = count; par[2] = a; par[3] = b; par[4] = f.np;
    Atomics.store(ctrl, 1, 0);
    Atomics.add(ctrl, 0, 1); Atomics.notify(ctrl, 0);
    share(f, this.cells, this.slab, task, 0, this.P, count, a, b);
    while (Atomics.load(ctrl, 1) < this.n) { /* the workers' shares */ }
  };
  StoutPool.share = share;
  root.StoutPool = StoutPool;
})(typeof self !== 'undefined' ? self : this);

/* Fig. 12: one worker thread of the stout solver (scripts/stout-pool.js). It holds a view of the page's fluid whose arrays
 * are the same shared memory, waits for a task, does its share, and counts itself done. */
importScripts('stout-cart.js', 'stout-pool.js');
onmessage = function (e) {
  const d = e.data;
  if (d.cmd !== 'attach') return;
  const f = Object.assign(Object.create(StoutCart.Fluid.prototype), d.fluid);
  const ctrl = d.ctrl, par = d.par, idx = d.index, P = d.P;
  let gen = d.gen;
  postMessage('ready');
  for (;;) {
    Atomics.wait(ctrl, 0, gen);
    gen = Atomics.load(ctrl, 0);
    const task = par[0];
    if (task === 0) { Atomics.add(ctrl, 1, 1); return; }     // back to the message loop (a new fluid follows)
    f.np = par[4];
    // a share that fails still counts as done (the page's thread must not wait for ever); the page then works alone
    try { StoutPool.share(f, d.cells, d.slab, task, idx, P, par[1], par[2], par[3]); }
    catch (err) { postMessage({ error: String(err && err.stack || err) }); }
    Atomics.add(ctrl, 1, 1);
  }
};

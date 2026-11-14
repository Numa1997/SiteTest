/* Fig. 15 (Resonant Tunnelling): the background thread that reads one stored 3D Kaggle run (an 'RT3C' file, written by
   tools/kaggle/resonant-tunnelling/rt3d_run.py), so the page's animation never stalls while a file arrives.
   It does three things and nothing else:
     1. the SHA-256 of the bytes as they arrived (compared by the page with kaggle/index.json);
     2. inflates the body (zlib) and splits it into its parts, exactly as read_rt3d.py does;
     3. hands over the 8-bit levels; the page turns them into numbers, two frames at a time: |psi| = q / 255 * peak_f (each
        frame's own peak, from the header) and arg psi = p / 255 * 2 pi - pi, so psi = |psi| (cos arg + i sin arg) on the stored
        half-plane z = 0, y >= 0.
   The page interpolates in time and draws; it computes nothing else. Docs: docs/simulations/fig15-resonant-tunnelling.md. */
'use strict';
self.onmessage = async function (ev) {
    const { url, id } = ev.data;
    try {
        const t0 = performance.now();
        const res = await fetch(url);
        if (!res.ok) throw new Error('HTTP ' + res.status + ' for ' + url);
        const buf = await res.arrayBuffer();
        const dig = new Uint8Array(await crypto.subtle.digest('SHA-256', buf));
        const sha = Array.from(dig, (b) => b.toString(16).padStart(2, '0')).join('');
        const u8 = new Uint8Array(buf);
        if (String.fromCharCode(u8[0], u8[1], u8[2], u8[3]) !== 'RT3C') throw new Error('not an RT3C file');
        const H = new DataView(buf).getUint32(4, true);
        const head = JSON.parse(new TextDecoder().decode(u8.subarray(8, 8 + H)));
        const ds = new DecompressionStream('deflate');                       /* zlib-wrapped deflate, as Python's zlib.compress writes */
        const raw = new Uint8Array(await new Response(new Blob([u8.subarray(8 + H)]).stream().pipeThrough(ds)).arrayBuffer());
        const n = head.n, nxs = head.nxs, nr = head.nr, nx = head.prof_nx, a = n * nxs * nr;
        const amp = raw.subarray(0, a), ph = raw.subarray(a, 2 * a);
        const pb = raw.buffer.slice(raw.byteOffset + 2 * a, raw.byteOffset + 2 * a + 4 * n * nx);
        const prof = new Float32Array(pb);
        const prof1d = head.has_1d ? new Float32Array(raw.buffer.slice(raw.byteOffset + 2 * a + 4 * n * nx, raw.byteOffset + 2 * a + 8 * n * nx)) : null;
        /* The levels are sent as they are (2 bytes per stored cell); the page turns only the two frames it is mixing into
           numbers, by the formula above. Sending psi as float32 for every frame cost 10 bytes per cell: 20 to 52 MB a run. */
        const lv = new Uint8Array(amp), pl = new Uint8Array(ph);
        const transfer = [lv.buffer, pl.buffer, prof.buffer];
        if (prof1d) transfer.push(prof1d.buffer);
        self.postMessage({ id, ok: true, sha, bytes: buf.byteLength, head, amp: lv, phase: pl, prof, prof1d, ms: performance.now() - t0 }, transfer);
    } catch (e) {
        self.postMessage({ id, ok: false, error: String(e && e.message || e) });
    }
};

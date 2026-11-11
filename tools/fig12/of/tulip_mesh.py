"""Fig. 12: the OpenFOAM mesh of the Guinness tulip, from public/scripts/guinness-glass.js.

python tools/fig12/of/tulip_mesh.py <case dir> <level>      writes <case>/system/blockMeshDict
level: coarse | medium | fine (the three grids of the convergence proof; see LEVELS)

The liquid region is an O-grid revolved about the glass's axis: at every height station a square core block and four
outer blocks whose outer edge is a circular arc of the measured inner radius R(z). Toward the glass the outer blocks'
cells shrink geometrically to a first-cell thickness h_w (well inside the Stokes layer, 0.44 mm at 3.4 Hz for the
stout), so the no-slip wall's boundary layer is resolved by the Navier-Stokes equations themselves; the first layer of
blocks above the floor shrinks toward the floor the same way. Between stations the wall is straight in z (stations every
STATION mm, the profile's own steps are 0.5 mm). Above the rim the mesh continues up to the rim plus HEAD mm (air), and a
ring of air outside the rim, out to R_rim + RING mm: stout that leaves the glass over the rim crosses the ring's floor,
the patch 'spill', where it is counted and removed. Patches: glass (no slip: the side wall and the floor), spill (open,
below the ring), atmosphere (open: the top and the ring's outer side).
Coordinates: x along the road, y across, z up from the inside of the glass's floor; metres.
"""
import json, math, os, subprocess, sys

LEVELS = {  # cells per quarter turn, radial cells in the outer blocks, vertical cell size (m), wall/floor first cell (m)
    'coarse': dict(nq=12, nr=10, dz=0.004, hw=0.0003),
    'medium': dict(nq=18, nr=14, dz=0.0027, hw=0.0002),
    'fine':   dict(nq=26, nr=19, dz=0.0018, hw=0.00014),
}
STATION, HEAD, RING, CORE, DR = 0.005, 0.025, 0.020, 0.45, 0.001   # m, m, m, core half-diagonal / R, m

def profile():
    here = os.path.dirname(os.path.abspath(__file__))
    js = os.path.join(here, '../../../public/scripts/guinness-glass.js')
    out = subprocess.run(['node', '-e', "const m={exports:{}};new Function('module',require('fs').readFileSync(process.argv[1],'utf8'))(m);"
                          "process.stdout.write(JSON.stringify(m.exports))", js], capture_output=True, text=True, check=True).stdout
    g = json.loads(out)
    return g['dz'], g['R']

def R_at(z, dzp, Rp):
    f = z / dzp; i = min(int(f), len(Rp) - 2)
    return Rp[i] + (f - i) * (Rp[i + 1] - Rp[i])

def grading_ratio(length, n, first):
    """ratio last/first of a geometric distribution of n cells over length whose cell at the far end is `first` thick"""
    # cells c_k = c0 q^k, k = 0..n-1, sum = length, c_{n-1} = first: solve for q by bisection
    lo, hi = 1e-6, 1.0
    for _ in range(200):
        q = 0.5 * (lo + hi); c0 = first / q ** (n - 1)
        s = c0 * (1 - q ** n) / (1 - q) if abs(1 - q) > 1e-12 else c0 * n
        if s > length: lo = q
        else: hi = q
    return q ** (n - 1)   # last / first (< 1: shrinking toward the far end)

def main(case, level):
    L = LEVELS[level]; nq, nr, dzc, hw = L['nq'], L['nr'], L['dz'], L['hw']
    dzp, Rp = profile(); zrim = (len(Rp) - 1) * dzp; Rrim = Rp[-1]
    # stations: at most STATION apart, and closer where the wall's radius changes by more than DR between them (the rounded
    # inside of the base widens from 16.3 to 28.4 mm in its first 5 mm); always on the profile's own 0.5 mm points
    zs = [0.0]
    while zs[-1] < zrim - 1e-9:
        i0 = round(zs[-1] / dzp); i = i0 + 1
        while i < len(Rp) - 1 and (i + 1 - i0) * dzp <= STATION + 1e-12 and abs(Rp[i + 1] - Rp[i0]) <= DR: i += 1
        zs.append(round(i * dzp, 6))
    zs.append(zrim + HEAD)
    verts, blocks, edges, faces = [], [], [], {'glass': [], 'spill': [], 'atmosphere': []}
    def V(x, y, z): verts.append((x, y, z)); return len(verts) - 1
    ang = [math.pi / 4 + k * math.pi / 2 for k in range(4)]
    st = []   # per station: (square[4], arc[4], ring[4] or None)
    for s, z in enumerate(zs):
        R = R_at(min(z, zrim), dzp, Rp) if z <= zrim else Rrim
        a = CORE * R
        sq = [V(a * math.cos(t), a * math.sin(t), z) for t in ang]
        ar = [V(R * math.cos(t), R * math.sin(t), z) for t in ang]
        ring = [V((Rrim + RING) * math.cos(t), (Rrim + RING) * math.sin(t), z) for t in ang] if z >= zrim - 1e-12 else None
        st.append((sq, ar, ring, R, z))
        for k in range(4):   # arcs through the midpoint angle
            tm = ang[k] + math.pi / 4
            edges.append('arc %d %d (%.9g %.9g %.9g)' % (ar[k], ar[(k + 1) % 4], R * math.cos(tm), R * math.sin(tm), z))
            if ring: edges.append('arc %d %d (%.9g %.9g %.9g)' % (ring[k], ring[(k + 1) % 4], (Rrim + RING) * math.cos(tm), (Rrim + RING) * math.sin(tm), z))
    # radial grading of the outer blocks: from the core edge to the wall, last cell hw (taken at the widest station)
    Rmax = max(r for (_, _, _, r, _) in st)
    gr = grading_ratio((1 - CORE) * Rmax, nr, hw)
    hprev = hw / 1.5
    for s in range(len(zs) - 1):
        (sq0, ar0, rg0, R0, z0), (sq1, ar1, rg1, R1, z1) = st[s], st[s + 1]
        # cell height: hw at the floor, growing by at most 1.5 from one station to the next, up to dz (the floor's boundary
        # layer, resolved like the wall's); uniform within a station
        target = min(dzc, hprev * 1.5) if z0 < zrim - 1e-12 else dzc
        nz = max(1, math.ceil((z1 - z0) / target - 1e-9)); hprev = (z1 - z0) / nz
        gz = '1'
        core = '(%d %d %d %d %d %d %d %d)' % (sq0[0], sq0[1], sq0[2], sq0[3], sq1[0], sq1[1], sq1[2], sq1[3])
        blocks.append('hex %s (%d %d %d) simpleGrading (1 1 %s)' % (core, nq, nq, nz, gz))
        if s == 0: faces['glass'].append('(%d %d %d %d)' % (sq0[0], sq0[3], sq0[2], sq0[1]))
        for k in range(4):
            k1 = (k + 1) % 4
            h = '(%d %d %d %d %d %d %d %d)' % (sq0[k], ar0[k], ar0[k1], sq0[k1], sq1[k], ar1[k], ar1[k1], sq1[k1])
            blocks.append('hex %s (%d %d %d) simpleGrading (%.6g 1 %s)' % (h, nr, nq, nz, gr, gz))
            if z1 <= zrim + 1e-12: faces['glass'].append('(%d %d %d %d)' % (ar0[k], ar0[k1], ar1[k1], ar1[k]))
            if s == 0: faces['glass'].append('(%d %d %d %d)' % (sq0[k], sq0[k1], ar0[k1], ar0[k]))
            if rg0 is not None:   # the ring of air outside the rim
                hr = '(%d %d %d %d %d %d %d %d)' % (ar0[k], rg0[k], rg0[k1], ar0[k1], ar1[k], rg1[k], rg1[k1], ar1[k1])
                # cells grow outward from the rim, starting at the wall cells' size so that the faces at r = R_rim match
                blocks.append('hex %s (%d %d %d) simpleGrading (%.6g 1 1)' % (hr, nr, nq, nz, 1 / grading_ratio(RING, nr, hw)))
                faces['spill'].append('(%d %d %d %d)' % (ar0[k], ar0[k1], rg0[k1], rg0[k]))
                faces['atmosphere'].append('(%d %d %d %d)' % (rg0[k], rg0[k1], rg1[k1], rg1[k]))
        if s == len(zs) - 2:   # the top
            faces['atmosphere'].append('(%d %d %d %d)' % (sq1[0], sq1[1], sq1[2], sq1[3]))
            for k in range(4):
                k1 = (k + 1) % 4
                faces['atmosphere'].append('(%d %d %d %d)' % (sq1[k], sq1[k1], ar1[k1], ar1[k]))
                faces['atmosphere'].append('(%d %d %d %d)' % (ar1[k], ar1[k1], rg1[k1], rg1[k]))
    out = ['FoamFile { format ascii; class dictionary; object blockMeshDict; }',
           '// written by tools/fig12/of/tulip_mesh.py, level %s: %d blocks' % (level, len(blocks)),
           'convertToMeters 1;', 'vertices', '('] + ['    (%.9g %.9g %.9g)' % v for v in verts] + [');', 'blocks', '('] + \
          ['    ' + b for b in blocks] + [');', 'edges', '('] + ['    ' + e for e in edges] + [');', 'boundary', '(']
    for name, typ in (('glass', 'wall'), ('spill', 'patch'), ('atmosphere', 'patch')):
        out += ['    %s { type %s; faces (' % (name, typ)] + ['        ' + f for f in faces[name]] + ['    ); }']
    out += [');']
    os.makedirs(os.path.join(case, 'system'), exist_ok=True)
    open(os.path.join(case, 'system', 'blockMeshDict'), 'w').write('\n'.join(out) + '\n')
    print('level %s: %d stations, %d blocks; rim %.4f m, R_rim %.4f m; radial grading last/first %.4g (wall cell %.2g m)' % (level, len(zs), len(blocks), zrim, Rrim, gr, hw))

if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[2] not in LEVELS: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

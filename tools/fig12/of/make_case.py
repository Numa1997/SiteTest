"""Fig. 12: build an OpenFOAM case of the stout in the tulip from tools/fig12/of/case.

python tools/fig12/of/make_case.py <case dir> --level coarse|medium|fine --fill 0.125 --end 6 --forcing tilt|rest
       [--write 0.05] [--maxco 0.5] [--sigma 0.045] [--nu 2.05e-6] [--rho 1000]
forcing: rest  the glass at rest;  tilt  the glass's acceleration along the road ramped to 1.5 m/s^2 over 0.6 s (half
cosine), held to 1 s, dropped (the release of tools/fig12/decay-3d.cjs); the table is the glass's velocity V(t), whose
derivative OpenFOAM applies as -rho alpha dV/dt (fvModel acceleration).
Then: blockMesh, setFields. Run with foamRun in the case directory. Every number is a parameter of this script; the
physical ones carry no default here that the gate scripts do not set explicitly.
"""
import argparse, math, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tulip_mesh

def velocity_table(kind, end, A=1.5):
    if kind == 'rest': return [(0.0, 0.0), (end + 1.0, 0.0)]
    # a(t) = A (1 - cos(pi t / 0.6)) / 2 for t < 0.6, A for 0.6 <= t < 1, 0 after; V = its integral (closed form)
    def V(t):
        if t < 0.6: return A * 0.5 * (t - 0.6 / math.pi * math.sin(math.pi * t / 0.6))
        if t < 1.0: return A * 0.3 + A * (t - 0.6)
        return A * 0.3 + A * 0.4
    ts = [i * 0.001 for i in range(int(1.2 / 0.001) + 1)] + [end + 1.0]
    return [(t, V(t)) for t in ts]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('case'); ap.add_argument('--level', required=True); ap.add_argument('--fill', type=float, required=True)
    ap.add_argument('--end', type=float, required=True); ap.add_argument('--forcing', required=True, choices=['rest', 'tilt'])
    ap.add_argument('--write', type=float, default=0.05); ap.add_argument('--maxco', type=float, default=0.5)
    ap.add_argument('--sigma', type=float, required=True); ap.add_argument('--nu', type=float, required=True); ap.add_argument('--rho', type=float, required=True)
    a = ap.parse_args()
    if os.path.exists(a.case): shutil.rmtree(a.case)
    shutil.copytree(os.path.join(HERE, 'case'), a.case)
    tulip_mesh.main(a.case, a.level)
    dzp, Rp = tulip_mesh.profile(); zrim = (len(Rp) - 1) * dzp
    subs = {'END': '%g' % a.end, 'WRITE': '%g' % a.write, 'MAXCO': '%g' % a.maxco, 'SIGMA': '%g' % a.sigma, 'NU': '%g' % a.nu, 'RHO': '%g' % a.rho,
            'FILL': '%g' % a.fill, 'PROBER': '%g' % (tulip_mesh.R_at(a.fill, dzp, Rp) - 0.001), 'ZTOP': '%g' % (zrim + tulip_mesh.HEAD)}
    for root, _, files in os.walk(a.case):
        for f in files:
            p = os.path.join(root, f); s = open(p).read(); t = s
            for k, v in subs.items(): t = t.replace(k, v)
            if t != s: open(p, 'w').write(t)
    with open(os.path.join(a.case, 'constant', 'glassVelocity'), 'w') as fh:
        for t, v in velocity_table(a.forcing, a.end): fh.write('    (%.6f (%.9g 0 0))\n' % (t, v))
    env = 'source /opt/openfoam13/etc/bashrc && cd %s && blockMesh > log.blockMesh 2>&1 && cp 0/alpha.stout.orig 0/alpha.stout && setFields > log.setFields 2>&1' % a.case
    subprocess.run(['bash', '-c', env], check=True)
    print('case %s ready: level %s, fill %.4f m, %s, %g s' % (a.case, a.level, a.fill, a.forcing, a.end))

if __name__ == '__main__': main()

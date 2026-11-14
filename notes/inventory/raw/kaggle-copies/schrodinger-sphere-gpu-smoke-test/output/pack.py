import json, base64, zlib, numpy as np
def b64z(a): return base64.b64encode(zlib.compress(np.ascontiguousarray(a).tobytes(), 9)).decode()
def build_page(template, runs, Es, Vs, Rs, N, L, dt, out, s0, device, start):
    R = []
    for n, r in enumerate(runs):
        R.append(dict(id=n, i=Es.index(r["E"]), j=Vs.index(r["V0"]), k=Rs.index(r["R"]), E=r["E"], V0=r["V0"], R=r["R"],
                      n=int(r["amp"].shape[0]), steps=int(r["steps"]), wall=round(float(r["wall"]), 2),
                      amp=b64z(r["amp"]), ph=b64z(r["phase"]), c=np.round(r["curves"], 6).tolist()))
    D = dict(Es=Es, Vs=Vs, Rs=Rs, out=out, L=L, dt=dt, s0=s0, cells=f"{N}³", device=device, start=start, runs=R)
    nf = runs[0]["amp"].shape[0]
    return (template.replace("__DATA__", json.dumps(D, separators=(",", ":"))).replace("__CELLS__", f"{N}³ = {N**3:,}".replace(",", " "))
            .replace("__DT__", f"Δt = {dt}").replace("__L__", f"{L:g} a").replace("__NF__", str(nf)).replace("__OUT__", str(out)))

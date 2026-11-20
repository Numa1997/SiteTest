# Fig. 12 on Kaggle, solver v2: the three stored rides again (same road, same cart, 20 s each), the stout with the Fig. 12
# note's wall and foam friction ("full"), the surface read with the open-column reconstruction (right next to the waist).
# Writes rides.json in the website's format (public/data/fig12/<date>/) and timing.json.
ROADS = {'gentle road: hump, dip, ripples, bump': {'kind': 'bumps', 'bumps': [{'x': 1.5, 'h': 0.01, 'L': 0.6}, {'x': 3.5, 'h': -0.008, 'L': 0.6}, {'x': 5.75, 'h': 0.005, 'L': 0.5}, {'x': 6.25, 'h': 0.005, 'L': 0.5}, {'x': 6.75, 'h': 0.005, 'L': 0.5}, {'x': 7.25, 'h': 0.005, 'L': 0.5}, {'x': 9.0, 'h': 0.01, 'L': 0.25}]}}
SPEEDS = [float(v) for v in os.environ.get("NB_SPEEDS", "0.5,1.0,1.5").split(",")]
END = float(os.environ.get("NB_END", "20.0")); DX = 0.0015; MS_STEP = 100   # ms per 2 ms step at 1.5 mm, measured (free swing v2, 12 Nov)
NRIDES = len(ROADS) * len(SPEEDS)
print(f"What the machine does: drives the pint over the road {NRIDES} times on the GPU, the stout and the cart pushing on each other.")
print(f"Computing time: {NRIDES} rides x {round(END / 0.002):,} steps x {MS_STEP} ms = {NRIDES * END / 0.002 * MS_STEP / 6e4:.0f} min, plus recording and start.")
rides = []; timing = []; done = 0; t_all = time.time()
for road_name, road in ROADS.items():
    for v0 in SPEEDS:
        ride = {"road": road, "v0": v0, "ctrl": "speed", "susp": False}
        log(f"ride {done + 1} of {NRIDES}: {road_name} at {v0} m/s; expected {END / 0.002 * MS_STEP / 6e4:.1f} min")
        rec, info, road_t = run(R, DZP, FILL, RHO, ride, END, fps=FPS, dx=DX, ppc=PPC, log=log, progress_s=60, model="full")
        xmin, h, za, zr = road_t
        P = np.array(rec.pop("P"))
        q = np.clip(np.round((P - FILL) / 0.0002) + 128, 0, 255).astype(np.uint8)
        k1 = min(len(zr), int((max(rec["x"]) + 1.0 - xmin) / h))
        rides.append(dict(road=road_name, v0=v0, n=len(rec["t"]), x=[round(v, 5) for v in rec["x"]], v=[round(v, 4) for v in rec["v"]],
                          zb=[round(v, 6) for v in rec["zb"]], zw=[round(v, 6) for v in rec["zw"]], lean=[round(v, 2) for v in rec["lean_mm"]],
                          spill=[round(v, 2) for v in rec["spill_g"]], road_x0=xmin, road_dx=h * 10, road_zr=[round(float(z), 5) for z in zr[:k1:10]],
                          frames=base64.b64encode(zlib.compress(q.tobytes(), 9)).decode()))
        timing.append(dict(road=road_name, v0=v0, predicted_min=END / 0.002 * MS_STEP / 6e4, measured_min=info["wall_s"] / 60, **info))
        done += 1
        log(f"ride {done} of {NRIDES} done in {info['wall_s'] / 60:.1f} min ({info['steps']:,} steps); lean up to {max(abs(v) for v in rec['lean_mm']):.1f} mm, "
            f"cart speed {min(rec['v']):.3f} to {max(rec['v']):.3f} m/s")
        out = dict(fill=FILL, nr=NR, nth=NTH, q=0.0002, fps=FPS, ml=RHO * glass_volume(R, DZP, FILL), solver="v2", model=MODELS["full"], rides=rides)
        json.dump(out, open(WORK / "rides.json", "w"), separators=(",", ":"))      # after every ride: a timeout keeps what is done
        json.dump(timing, open(WORK / "timing.json", "w"), indent=1)
log(f"all {NRIDES} rides computed in {(time.time() - t_all) / 60:.1f} min; rides.json {(WORK / 'rides.json').stat().st_size / 1e6:.2f} MB")

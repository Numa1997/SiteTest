"""Path-traced test frame of the Fig. 16 pint from one stored frame, for the realism work (notes/realism/STATE.md).
Runs INSIDE Blender (Cycles, GPU) on Kaggle:  blender -b -P render_pint.py -- <ride.json> <frame k> <out.png> [hdri.hdr]
Nothing physical is computed here: the stout's surface and the head's thickness are the solver's stored columns (H, hf), read
as public/scripts/stout-view2.js (StoutRide.at, atInward) reads them; the glass is the solver's inner wall R(z) of
public/scripts/guinness-glass.js. The picture comes from light transport (Cycles), not from painted colours:
  glass  : dielectric, n = 1.52 (soda-lime), clear;
  stout  : dielectric, n = 1.34, absorbing volume, Beer-Lambert I = I0 exp(-alpha d) with alpha per colour channel (see ALPHA);
  head   : foam, a dense scattering medium (subsurface scattering, ivory albedo), fine bubble relief;
  light  : an HDR photograph of a real room (Poly Haven, CC0) when one is given, else Blender's physical sky.
Provisional (to be grounded in a measured spectrum before the page uses it): ALPHA, the stout's absorption per channel."""
import base64, json, math, os, sys, zlib

import bpy, bmesh
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:]
RIDE, K, OUT = argv[0], int(argv[1]), argv[2]
HDRI = argv[3] if len(argv) > 3 and os.path.exists(argv[3]) else None

# ---------- the stored frame (format: public/scripts/stout-view2.js, StoutRide.unpack) ----------
D = json.load(open(RIDE)); n = D["n"]; n2 = n * n


def inflate(b64, dt):
    return np.frombuffer(zlib.decompress(base64.b64decode(b64)), dtype=dt).copy()


H = inflate(D["H"], np.int16).astype(np.int32).reshape(D["frames"], n2)
H = np.cumsum(H, axis=0)                                # differences from the frame before: a running sum restores them
H = ((H + 32768) % 65536 - 32768).astype(np.int32)      # the same 16-bit wrap as (a + b) << 16 >> 16
HF = inflate(D["hf"], np.uint8).reshape(D["frames"], n2)
Hk, HFk = H[K].reshape(n, n), HF[K].reshape(n, n).astype(float)
dx, x0, qH, qhf = D["dx"], D["x0"], D["qH"], D["qhf"]


def at(x, y):
    """stored surface (m above the inner floor) and head thickness (m) at (x, y): StoutRide.at, line for line"""
    fx, fy = (x - x0) / dx - 0.5, (y - x0) / dx - 0.5
    i, j = math.floor(fx), math.floor(fy); tx, ty = fx - i, fy - j; w = h = f = 0.0
    for a in (0, 1):
        for b in (0, 1):
            ii, jj = i + a, j + b
            if ii < 0 or jj < 0 or ii >= n or jj >= n: continue
            v = Hk[ii, jj]
            if v == -32768: continue
            ww = (tx if a else 1 - tx) * (ty if b else 1 - ty); w += ww; h += ww * v; f += ww * HFk[ii, jj]
    return (h / w * qH, f / w * qhf) if w > 1e-6 else None


def at_inward(r, th):
    c, s = math.cos(th), math.sin(th); q = r
    while q > 0:
        v = at(q * c, q * s)
        if v: return v
        q -= 0.5 * dx
    return at(0, 0) or (D["fill"], 0.0)


# ---------- the glass: the solver's inner wall R(z), every 0.5 mm from the cavity floor (public/scripts/guinness-glass.js) ----------
src = open(os.path.join(os.path.dirname(RIDE), "guinness-glass.js")).read() if os.path.exists(os.path.join(os.path.dirname(RIDE), "guinness-glass.js")) else open(os.environ["GLASS_JS"]).read()
R = np.array([float(v) for v in src.split("R: [")[1].split("]")[0].split(",")]); DZ = 0.0005; ZRIM = (len(R) - 1) * DZ
WALL, FOOT = 0.0025, 0.014                            # wall 2.5 mm (stout-view.js glassWall); solid foot 14 mm (Fig. 16 note)


def Rin(z): return float(np.interp(min(max(z, 0.0), ZRIM), np.arange(len(R)) * DZ, R))
def Rout(z): return Rin(max(0.008, z)) + WALL       # the foot is solid glass: straight below 8 mm (stout-view.js)


def lathe(name, prof, seg=192):
    """a closed body of revolution from a profile [(r, z)] that starts and ends on the axis"""
    me = bpy.data.meshes.new(name); bm = bmesh.new(); rings = []
    for (r, z) in prof:
        rings.append([bm.verts.new((r * math.cos(2 * math.pi * s / seg), r * math.sin(2 * math.pi * s / seg), z)) for s in range(seg)])
    for a, b in zip(rings[:-1], rings[1:]):
        for s in range(seg):
            try: bm.faces.new((a[s], a[(s + 1) % seg], b[(s + 1) % seg], b[s]))
            except ValueError: pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth = True
    return ob


def polar(name, top, wall_down, bottom_z, nr=48, nth=192):
    """a closed liquid body: top surface z = top(r, th) out to the edge radius re(th), down the glass wall, flat bottom"""
    me = bpy.data.meshes.new(name); bm = bmesh.new(); rows = []
    th = [2 * math.pi * t / nth for t in range(nth)]
    edge = []
    for t in th:                                   # the edge column, as stout-view2.js finds it
        v = at_inward(Rin(D["fill"]), t); r = Rin(min(v[0], ZRIM)) - 0.0004; edge.append((r, at_inward(r, t)))
    for i in range(nr + 1):
        rows.append([(edge[q][0] * i / nr, th[q], top(edge[q][0] * i / nr, th[q], edge[q][1] if i == nr else None)) for q in range(nth)])
    zs = [rows[-1][q][2] for q in range(nth)]
    for m in range(1, wall_down + 1):              # down the wall, just inside the glass
        rows.append([(Rin(zs[q] - (zs[q] - bottom_z) * m / wall_down) - 0.0002, th[q], zs[q] - (zs[q] - bottom_z) * m / wall_down) for q in range(nth)])
    for i in range(nr - 1, -1, -1):
        rows.append([(rows[nr + wall_down][q][0] * i / nr, th[q], bottom_z) for q in range(nth)])
    vs = [[bm.verts.new((r * math.cos(t), r * math.sin(t), z)) for (r, t, z) in row] for row in rows]
    for a, b in zip(vs[:-1], vs[1:]):
        for q in range(nth):
            try: bm.faces.new((a[q], a[(q + 1) % nth], b[(q + 1) % nth], b[q]))
            except ValueError: pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth = True
    return ob


def surf(r, t, ev=None):
    v = ev if ev is not None else (at(r * math.cos(t), r * math.sin(t)) or at_inward(r, t)); return v[0]


def head_top(r, t, ev=None):
    v = ev if ev is not None else (at(r * math.cos(t), r * math.sin(t)) or at_inward(r, t)); return v[0] + max(v[1], 0.0003)


# ---------- scene ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
glass_prof = [(0.0, -FOOT), (Rout(0) - 0.002, -FOOT), (Rout(0), -FOOT + 0.002)]
glass_prof += [(Rout(z), z) for z in np.arange(-FOOT + 0.004, ZRIM, 0.002)]
glass_prof += [(Rin(ZRIM) + WALL * 0.5, ZRIM + 0.0012)]                      # the rounded lip
glass_prof += [(Rin(z), z) for z in np.arange(ZRIM, 0.0, -0.002)] + [(Rin(0) - 0.003, 0.0), (0.0, 0.0)]
glass = lathe("glass", glass_prof)
stout = polar("stout", surf, 60, 0.0003)
# the head: top surface head_top, bottom surface the stout's surface (1/10 mm above it), closed along the wall
me = bpy.data.meshes.new("head"); bm = bmesh.new(); nr, nth = 48, 192; th = [2 * math.pi * t / nth for t in range(nth)]
edge = []
for t in th:
    v = at_inward(Rin(D["fill"]), t); r = Rin(min(v[0], ZRIM)) - 0.0004; edge.append((r, at_inward(r, t)))
top = [[bm.verts.new(((edge[q][0] * i / nr) * math.cos(th[q]), (edge[q][0] * i / nr) * math.sin(th[q]),
                      head_top(edge[q][0] * i / nr, th[q], edge[q][1] if i == nr else None))) for q in range(nth)] for i in range(nr + 1)]
bot = [[bm.verts.new(((edge[q][0] * i / nr) * math.cos(th[q]), (edge[q][0] * i / nr) * math.sin(th[q]),
                      surf(edge[q][0] * i / nr, th[q], edge[q][1] if i == nr else None) + 0.0001)) for q in range(nth)] for i in range(nr + 1)]
for rows in (top, bot[::-1]):
    for a, b in zip(rows[:-1], rows[1:]):
        for q in range(nth):
            try: bm.faces.new((a[q], a[(q + 1) % nth], b[(q + 1) % nth], b[q]))
            except ValueError: pass
for q in range(nth):
    try: bm.faces.new((top[nr][q], bot[nr][q], bot[nr][(q + 1) % nth], top[nr][(q + 1) % nth]))
    except ValueError: pass
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
head = bpy.data.objects.new("head", me); bpy.context.collection.objects.link(head)
for p in me.polygons: p.use_smooth = True

# the deck's pitch at this frame tilts the glued glass with it (stored th, rad; sign as cart16-view.js applies it: to be checked)
pivot = bpy.data.objects.new("pint", None); bpy.context.collection.objects.link(pivot)
for ob in (glass, stout, head): ob.parent = pivot
pivot.rotation_euler = (0.0, float(D["th"][K]) if "th" in D else 0.0, 0.0)
pivot.location = (0, 0, FOOT)

# ---------- materials ----------
def mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; return m, m.node_tree.nodes, m.node_tree.links


m, N, L = mat("glass"); b = N["Principled BSDF"]
b.inputs["Base Color"].default_value = (1, 1, 1, 1); b.inputs["Roughness"].default_value = 0.0; b.inputs["IOR"].default_value = 1.52
b.inputs["Transmission Weight"].default_value = 1.0; glass.data.materials.append(m)

# stout: alpha per channel (1/m), PROVISIONAL: red passes ~3-10 mm (ruby at the thin edge), black beyond ~3 cm
ALPHA = (120.0, 700.0, 1500.0); amax = max(ALPHA)
m, N, L = mat("stout"); b = N["Principled BSDF"]
b.inputs["Roughness"].default_value = 0.0; b.inputs["IOR"].default_value = 1.34; b.inputs["Transmission Weight"].default_value = 1.0
va = N.new("ShaderNodeVolumeAbsorption"); va.inputs["Color"].default_value = (1 - ALPHA[0] / amax, 1 - ALPHA[1] / amax, 1 - ALPHA[2] / amax, 1)
va.inputs["Density"].default_value = amax; L.new(va.outputs[0], N["Material Output"].inputs["Volume"]); stout.data.materials.append(m)

# head: dense foam, ivory, scattering below the surface; fine bubble pits as a bump
m, N, L = mat("head"); b = N["Principled BSDF"]
b.inputs["Base Color"].default_value = (0.86, 0.78, 0.62, 1); b.inputs["Roughness"].default_value = 0.55
b.inputs["Subsurface Weight"].default_value = 1.0; b.inputs["Subsurface Radius"].default_value = (1.0, 0.8, 0.6); b.inputs["Subsurface Scale"].default_value = 0.002
nz = N.new("ShaderNodeTexVoronoi"); nz.inputs["Scale"].default_value = 2500.0; bu = N.new("ShaderNodeBump"); bu.inputs["Strength"].default_value = 0.15
L.new(nz.outputs["Distance"], bu.inputs["Height"]); L.new(bu.outputs["Normal"], b.inputs["Normal"]); head.data.materials.append(m)

# a dark wooden bar top under the glass (a satin plane)
bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0, 0, 0)); table = bpy.context.object
m, N, L = mat("table"); b = N["Principled BSDF"]; b.inputs["Base Color"].default_value = (0.08, 0.035, 0.018, 1); b.inputs["Roughness"].default_value = 0.25
table.data.materials.append(m)

# ---------- light ----------
w = bpy.data.worlds.new("world"); sc.world = w; w.use_nodes = True; WN, WL = w.node_tree.nodes, w.node_tree.links
if HDRI:
    env = WN.new("ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(HDRI); WL.new(env.outputs[0], WN["Background"].inputs[0])
else:
    sky = WN.new("ShaderNodeTexSky"); WL.new(sky.outputs[0], WN["Background"].inputs[0])

# ---------- camera: a drinker's view, slightly above the rim, 85 mm lens ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); bpy.context.collection.objects.link(cam); sc.camera = cam
cam.data.lens = 85; el = math.radians(14); dist = 0.75; zt = FOOT + 0.085
cam.location = (dist * math.cos(el), -0.0, zt + dist * math.sin(el)); cam.rotation_euler = (math.pi / 2 - el, 0, math.pi / 2)

# ---------- render ----------
sc.render.engine = "CYCLES"; cy = sc.cycles; cy.samples = int(os.environ.get("SAMPLES", "512")); cy.use_denoising = True
cy.max_bounces = 24; cy.transmission_bounces = 24; cy.volume_bounces = 4; cy.caustics_refractive = True
prefs = bpy.context.preferences.addons["cycles"].preferences
for kind in ("OPTIX", "CUDA"):
    try:
        prefs.compute_device_type = kind; prefs.get_devices(); [setattr(d, "use", True) for d in prefs.devices]; cy.device = "GPU"; break
    except Exception: continue
print("devices:", [(d.name, d.type, d.use) for d in prefs.devices], "->", cy.device, flush=True)
sc.render.resolution_x, sc.render.resolution_y = 1200, 1600; sc.view_settings.view_transform = "AgX"
sc.render.filepath = OUT; bpy.ops.render.render(write_still=True)
print("written", OUT, flush=True)

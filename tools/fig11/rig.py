"""Blender scenes for the Fig. 11 project: the whole rig, the two joints, the strut cut open, the magnet track and coil.
Run: bvenv/bin/python rig.py <outdir>. Writes <name>.png and <name>.json (label anchor points projected to the image, in %)."""
import bpy, math, json, sys, os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

OUT = sys.argv[-1]
os.makedirs(OUT, exist_ok=True)

# ---------------- helpers ----------------
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = 48
    sc.cycles.use_denoising = True
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'AgX'
    try: sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception: pass
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.80, 0.80, 0.80, 1); bg.inputs[1].default_value = 0.35
    return sc

MATS = {}
def mat(name, rgb, metal=0.0, rough=0.4, emit=None):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1)
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = 1.0
    MATS[name] = m; return m

def M():
    MATS.clear()
    return dict(
        steel=mat('steel', (0.62, 0.63, 0.65), 1, 0.32),
        dark=mat('darksteel', (0.22, 0.22, 0.24), 1, 0.45),
        alu=mat('alu', (0.86, 0.87, 0.88), 1, 0.22),
        spring=mat('spring', (0.12, 0.12, 0.14), 1, 0.3),
        bronze=mat('bronze', (0.80, 0.55, 0.28), 1, 0.3),
        copper=mat('copper', (0.93, 0.50, 0.33), 1, 0.25),
        carbon=mat('carbon', (0.05, 0.05, 0.055), 0, 0.35),
        nylon=mat('nylon', (0.92, 0.91, 0.88), 0, 0.5),
        ball=mat('ball', (0.095, 0.010, 0.018), 0.0, 0.5),
        magN=mat('magN', (0.78, 0.16, 0.16), 0.2, 0.4),
        magS=mat('magS', (0.16, 0.30, 0.72), 0.2, 0.4),
        former=mat('former', (0.35, 0.35, 0.33), 0, 0.6),
        arrB=mat('arrB', (0.10, 0.35, 0.85), 0, 0.5, emit=(0.10, 0.35, 0.85)),
        arrI=mat('arrI', (0.95, 0.55, 0.05), 0, 0.5, emit=(0.95, 0.55, 0.05)),
        arrF=mat('arrF', (0.48, 0.12, 0.17), 0, 0.5, emit=(0.48, 0.12, 0.17)),
        plate=mat('plate', (0.97, 0.96, 0.94), 0, 0.8),
    )

def link(ob, m):
    ob.data.materials.append(m); return ob

def cyl(p1, p2, r, m, verts=48):
    p1, p2 = Vector(p1), Vector(p2); d = p2 - p1
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d.length, location=(p1 + p2) / 2)
    ob = bpy.context.object; ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = d.to_track_quat('Z', 'Y')
    bpy.ops.object.shade_smooth(); return link(ob, m)

def tube(p1, p2, ro, ri, m):
    ob = cyl(p1, p2, ro, m, 64)
    inner = cyl(Vector(p1) - (Vector(p2) - Vector(p1)) * 0.01, Vector(p2) + (Vector(p2) - Vector(p1)) * 0.01, ri, m, 64)
    mod = ob.modifiers.new('hole', 'BOOLEAN'); mod.operation = 'DIFFERENCE'; mod.object = inner
    inner.hide_render = True; inner.hide_viewport = True
    return ob

def sphere(c, r, m):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=r, location=c)
    ob = bpy.context.object; bpy.ops.object.shade_smooth(); return link(ob, m)

def box(c, size, m, rot=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); ob = bpy.context.object
    ob.scale = size
    if rot: ob.rotation_euler = rot
    return link(ob, m)

def torus(c, R, r, m, axis='Y'):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=64, minor_segments=24, location=c)
    ob = bpy.context.object
    if axis == 'Y': ob.rotation_euler = (math.pi / 2, 0, 0)
    elif axis == 'X': ob.rotation_euler = (0, math.pi / 2, 0)
    bpy.ops.object.shade_smooth(); return link(ob, m)

def arrow(p, d, L, r, m):
    p, d = Vector(p), Vector(d).normalized()
    tip = p + d * L; neck = p + d * (L - 3.2 * r)
    cyl(p, neck, r, m, 24)
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=2.2 * r, radius2=0, depth=3.2 * r, location=(neck + tip) / 2)
    ob = bpy.context.object; ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = d.to_track_quat('Z', 'Y')
    return link(ob, m)

def helix(p0, axis, length, R, wire, turns, m):
    axis = Vector(axis).normalized(); a = axis.orthogonal().normalized(); b = axis.cross(a)
    cu = bpy.data.curves.new('helix', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = wire; cu.bevel_resolution = 4
    sp = cu.splines.new('POLY'); n = int(turns * 48); sp.points.add(n)
    for i in range(n + 1):
        t = i / n; ang = 2 * math.pi * turns * t
        q = Vector(p0) + axis * (length * t) + a * (R * math.cos(ang)) + b * (R * math.sin(ang))
        sp.points[i].co = (*q, 1)
    ob = bpy.data.objects.new('helix', cu); bpy.context.collection.objects.link(ob)
    return link(ob, m)

def cutter(c, size):
    ob = box(c, size, mat('cut', (1, 0, 0)))
    ob.hide_render = True; ob.hide_viewport = True; return ob

def cut(obs, cu):
    for ob in obs:
        mod = ob.modifiers.new('cut', 'BOOLEAN'); mod.operation = 'DIFFERENCE'; mod.object = cu

def camera(loc, target, lens=50, ortho=None):
    cam = bpy.data.cameras.new('cam'); ob = bpy.data.objects.new('cam', cam); bpy.context.collection.objects.link(ob)
    ob.location = loc; d = Vector(target) - Vector(loc)
    ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = d.to_track_quat('-Z', 'Y')
    if ortho: cam.type = 'ORTHO'; cam.ortho_scale = ortho
    else: cam.lens = lens
    bpy.context.scene.camera = ob; return ob

def lights(key=(2, -3, 3), power=600, size=2.5):
    for loc, pw, sz in ((key, power, size), ((-3, -2, 1.5), power * 0.45, size * 1.4), ((0.5, 3, 2), power * 0.35, size)):
        ld = bpy.data.lights.new('l', 'AREA'); ld.energy = pw; ld.size = sz
        ob = bpy.data.objects.new('l', ld); bpy.context.collection.objects.link(ob); ob.location = loc
        ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y')

def render(name, res, labels):
    sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y = res; sc.render.resolution_percentage = 100
    sc.render.filepath = os.path.join(OUT, name + '.png'); sc.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
    pts = {}
    for k, p in labels.items():
        v = world_to_camera_view(sc, sc.camera, Vector(p))
        pts[k] = [round(v.x * 100, 2), round((1 - v.y) * 100, 2)]
    json.dump(pts, open(os.path.join(OUT, name + '.json'), 'w'), indent=1)
    print('rendered', name)

# ---------------- 1. the whole rig ----------------
def scene_rig():
    reset(); m = M()
    l1 = l2 = 0.5; H = 1.65; th1, th2, X = math.radians(12), math.radians(20), 0.15
    P0 = Vector((0, 0, 0)); P1 = P0 + Vector((l1 * math.sin(th1), 0, -l1 * math.cos(th1)))
    P2 = P1 + Vector((l2 * math.sin(th2), 0, -l2 * math.cos(th2))); C = Vector((X, 0, -H))
    box((0, 0, 0.045), (0.22, 0.09, 0.03), m['dark'])                     # ceiling bracket
    box((0, -0.03, 0.012), (0.03, 0.012, 0.05), m['dark']); box((0, 0.03, 0.012), (0.03, 0.012, 0.05), m['dark'])
    cyl((0, -0.045, 0), (0, 0.045, 0), 0.006, m['steel'])                 # pivot pin
    cyl(P0, P1, 0.010, m['carbon']); cyl(P1, P2, 0.010, m['carbon'])     # rods
    cyl(P1 + Vector((0, -0.04, 0)), P1 + Vector((0, 0.04, 0)), 0.005, m['steel'])
    sphere(P1, 0.045, m['ball']); sphere(P2, 0.045, m['ball'])
    u = (C - P2).normalized(); L = (C - P2).length
    yv = Vector((0, 1, 0))
    cyl(P2 - yv * 0.062, P2 + yv * 0.062, 0.006, m['steel'])                 # axle through ball 2's centre
    for sy in (-1, 1): cyl(P2 + yv * sy * 0.055, P2 + yv * sy * 0.055 + u * 0.075, 0.007, m['dark'])   # fork cheeks
    cyl(P2 + u * 0.075 - yv * 0.062, P2 + u * 0.075 + yv * 0.062, 0.007, m['dark'])                   # fork bridge
    E1 = C - u * 0.03
    inner_top, inner_bot = P2 + u * 0.075, P2 + u * (0.075 + 0.40)
    cyl(inner_top, inner_bot, 0.008, m['steel'])                        # inner tube (steel)
    outer_top = E1 - u * 0.012 - u * 0.36
    tube(outer_top, E1 - u * 0.012, 0.0125, 0.0105, m['alu'])           # outer tube (aluminium)
    torus(E1, 0.011, 0.004, m['steel'])
    box(C + Vector((0, 0, -0.01)), (0.03, 0.03, 0.02), m['dark'])        # cart clevis
    box((X, 0, -H - 0.045), (0.24, 0.15, 0.05), m['alu'])                # cart body
    for dx in (-0.08, 0.08):
        for dy in (-0.06, 0.06):
            cyl((X + dx, dy - 0.012, -H - 0.085), (X + dx, dy + 0.012, -H - 0.085), 0.022, m['nylon'])
    box((0, 0, -H - 0.115), (1.7, 0.16, 0.016), m['steel'])              # rail
    # magnet track beside the rail, coil hanging from the cart into it
    yT = 0.17
    box((0, yT, -H - 0.13), (1.7, 0.07, 0.012), m['dark'])
    box((0, yT - 0.03, -H - 0.09), (1.7, 0.01, 0.07), m['dark']); box((0, yT + 0.03, -H - 0.09), (1.7, 0.01, 0.07), m['dark'])
    for i in range(-14, 14):
        x0 = (i + 0.5) * 0.06; mm = m['magN'] if i % 2 else m['magS']; mm2 = m['magS'] if i % 2 else m['magN']
        box((x0, yT - 0.0215, -H - 0.09), (0.056, 0.007, 0.06), mm); box((x0, yT + 0.0215, -H - 0.09), (0.056, 0.007, 0.06), mm2)
    box((X, (0.075 + yT) / 2 + 0.01, -H - 0.04), (0.06, yT - 0.06, 0.02), m['alu'])   # arm from cart to coil
    box((X, yT, -H - 0.075), (0.07, 0.006, 0.06), m['copper'])          # coil (flat, in the gap)
    camera((0.35, -3.6, -0.55), (0.05, 0, -0.86), lens=62)
    lights(key=(2, -4, 1.5), power=1500, size=3)
    render('rig', (1100, 1250), {'axle': P2 + Vector((0, -0.06, 0)), 
        'pivot': P0 + Vector((0, 0, 0.05)), 'rod1': (P0 + P1) / 2, 'm1': P1, 'rod2': (P1 + P2) / 2, 'm2': P2,
        'strut': P2 + u * L * 0.45, 'cart': (X - 0.1, 0, -H - 0.045), 'rail': (-0.6, -0.08, -H - 0.115),
        'magnet': (0.6, yT, -H - 0.06), 'coil': (X + 0.035, yT, -H - 0.05)})

# ---------------- 2. the joints ----------------
def scene_joint_ball():
    reset(); m = M()
    th2 = math.radians(20); a = math.radians(-10)               # rod 2 above, strut below leaning
    P2 = Vector((0, 0, 0)); up = Vector((-math.sin(th2), 0, math.cos(th2)))
    cyl(P2 + up * 0.02, P2 + up * 0.22, 0.007, m['carbon'])                 # rod 2 coming down into the ball
    sphere(P2, 0.035, m['ball'])
    u = Vector((math.sin(a), 0, -math.cos(a)))                               # strut direction, downwards
    cyl(P2 + Vector((0, 0, -0.025)), P2 + Vector((0, 0, -0.05)), 0.008, m['steel'])   # stud screwed into ball
    # clevis: base plate and two cheeks with a pin along y
    base = P2 + Vector((0, 0, -0.054)); box(base, (0.03, 0.034, 0.008), m['dark'])
    ch = [box(base + Vector((0, s * 0.013, -0.02)), (0.026, 0.005, 0.034), m['dark']) for s in (-1, 1)]
    cut([ch[0]], cutter((0.02, -0.02, -0.05), (0.04, 0.02, 0.1)))
    pin = base + Vector((0, 0, -0.026)); cyl(pin + Vector((0, -0.022, 0)), pin + Vector((0, 0.022, 0)), 0.0035, m['steel'])
    # rod-end eye with a spherical bearing, between the cheeks
    torus(pin, 0.0085, 0.0035, m['steel']); sphere(pin, 0.0058, m['bronze'])
    cyl(pin + u * 0.011, pin + u * 0.04, 0.0045, m['steel'])                  # threaded shank
    cyl(pin + u * 0.04, pin + u * 0.22, 0.008, m['steel'])                    # inner tube
    camera((0.10, -0.30, 0.02), (0, 0, -0.045), lens=60)
    lights(key=(0.4, -0.6, 0.5), power=70, size=0.4)
    render('joint-ball', (900, 1100), {'rod2': P2 + up * 0.15, 'ball': P2 + Vector((0.025, 0, 0.02)), 'stud': P2 + Vector((0, 0, -0.04)),
           'clevis': base + Vector((0.015, 0, -0.01)), 'pin': pin + Vector((0, -0.02, 0)), 'eye': pin + Vector((-0.008, 0, -0.004)),
           'bearing': pin, 'inner': pin + u * 0.15})

def scene_joint_cart():
    reset(); m = M()
    a = math.radians(-10); u = Vector((-math.sin(a), 0, math.cos(a)))        # strut direction, upwards
    C = Vector((0, 0, 0))
    box(C + Vector((0, 0, -0.04)), (0.16, 0.12, 0.04), m['alu'])             # cart top
    base = C + Vector((0, 0, -0.016)); box(base, (0.034, 0.034, 0.008), m['dark'])
    ch = [box(base + Vector((0, s * 0.013, 0.02)), (0.026, 0.005, 0.034), m['dark']) for s in (-1, 1)]
    cut([ch[0]], cutter((0.02, -0.02, 0.03), (0.04, 0.02, 0.1)))
    pin = base + Vector((0, 0, 0.026)); cyl(pin + Vector((0, -0.022, 0)), pin + Vector((0, 0.022, 0)), 0.0035, m['steel'])
    torus(pin, 0.0085, 0.0035, m['steel']); sphere(pin, 0.0058, m['bronze'])
    cyl(pin + u * 0.011, pin + u * 0.03, 0.0045, m['steel'])
    tube(pin + u * 0.03, pin + u * 0.25, 0.0125, 0.0105, m['alu'])          # outer tube
    for s in (-1, 1):                                                          # screws into the cart
        cyl(base + Vector((s * 0.011, 0, -0.004)), base + Vector((s * 0.011, 0, 0.006)), 0.003, m['steel'])
    camera((0.10, -0.30, 0.09), (0, 0, 0.03), lens=60)
    lights(key=(0.4, -0.6, 0.6), power=70, size=0.4)
    render('joint-cart', (900, 1100), {'outer': pin + u * 0.17, 'eye': pin + Vector((-0.008, 0, 0.004)), 'pin': pin + Vector((0, -0.02, 0)),
           'clevis': base + Vector((0.015, 0, 0.012)), 'cart': C + Vector((0.06, -0.06, -0.03))})

# ---------------- 3. the strut, cut open ----------------
def scene_strut():
    reset(); m = M(); L = 0.65
    def P(x): return Vector((x, 0, 0))
    torus(P(0), 0.0085, 0.0035, m['steel']); sphere(P(0), 0.0058, m['bronze'])          # cart end: rod end on the cart's pin
    cyl(P(0.011), P(0.03), 0.0045, m['steel'])
    outer = tube(P(0.03), P(0.528), 0.0125, 0.0105, m['alu'])                          # outer tube, aluminium
    plug = cyl(P(0.03), P(0.045), 0.0105, m['dark'])                                   # bottom plug: spring anchor, lower stop
    bush = tube(P(0.51), P(0.528), 0.0105, 0.0081, m['bronze'])                       # guide bushing: upper stop
    inner = tube(P(L - 0.455), P(L - 0.07), 0.008, 0.0062, m['steel'])                # inner tube, steel
    collar = tube(P(L - 0.455), P(L - 0.44), 0.0102, 0.008, m['dark'])                # collar on the inner tube
    iplug = cyl(P(L - 0.10), P(L - 0.085), 0.0062, m['dark'])                         # plug inside the inner tube: spring anchor
    helix(P(0.045), Vector((1, 0, 0)), L - 0.10 - 0.045, 0.0042, 0.0009, 36, m['spring'])
    # ball end: fork cheeks on the axle through ball 2 (ball drawn as a ghost outline is left out; the axle marks its centre)
    for sy in (-1, 1): box((L - 0.03, sy * 0.045, 0), (0.07, 0.006, 0.026), m['dark'])
    box((L - 0.066, 0, 0), (0.008, 0.096, 0.026), m['dark']); cyl(P(L - 0.07), P(L - 0.062), 0.011, m['dark'])
    cyl((L, -0.062, 0), (L, 0.062, 0), 0.004, m['steel'])
    sphere(P(L), 0.035, m['ball'])
    cu = cutter((0.30, -0.05, 0), (0.62, 0.1, 0.1)); cut([outer, plug, bush, inner, collar, iplug], cu)
    cam = bpy.data.cameras.new('cam'); ob = bpy.data.objects.new('cam', cam); bpy.context.collection.objects.link(ob)
    tgt = Vector((0.335, 0, 0)); loc = tgt + Vector((0.0, -1.0, 0.22)).normalized() * 3
    ob.location = loc; ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = (tgt - loc).to_track_quat('-Z', 'Y')
    cam.type = 'ORTHO'; cam.ortho_scale = 0.78; bpy.context.scene.camera = ob
    lights(key=(0.6, -1.0, 0.9), power=160, size=0.8)
    render('strut', (2000, 440), {'eye1': P(0), 'outer': P(0.38) + Vector((0, 0, 0.0125)), 'plug': P(0.037) + Vector((0, 0, -0.008)),
           'spring': P(0.12), 'collar': P(L - 0.447) + Vector((0, 0, 0.0102)), 'bush': P(0.519) + Vector((0, 0, 0.0105)),
           'inner': P(0.40) + Vector((0, -0.006, -0.0072)), 'iplug': P(L - 0.092), 'fork': P(L - 0.05) + Vector((0, -0.045, -0.013)), 'axle': (L, -0.06, 0.004), 'ball': P(L) + Vector((0, 0, 0.035))})

# ---------------- 4. magnet track and coil ----------------
def scene_motor():
    reset(); m = M()
    g = 0.012; wall = 0.008; mag = 0.006; h = 0.06; pitch = 0.04; L = 0.32
    box((0, 0, -0.004), (L, 2 * (g / 2 + mag + wall), 0.008), m['dark'])     # base of the U-channel
    walls = [box((0, s * (g / 2 + mag + wall / 2), h / 2), (L, wall, h), m['dark']) for s in (-1, 1)]
    front = [walls[0]]
    for i in range(-4, 4):
        x0 = (i + 0.5) * pitch; north_left = (i % 2 == 0)
        front.append(box((x0, -(g / 2 + mag / 2), h / 2 + 0.004), (pitch * 0.94, mag, h * 0.85), m['magN'] if north_left else m['magS']))
        box((x0, (g / 2 + mag / 2), h / 2 + 0.004), (pitch * 0.94, mag, h * 0.85), m['magS'] if north_left else m['magN'])
    cu = cutter((0, -0.03, 0.03), (0.12, 0.046, 0.1)); cut(front, cu)
    # field arrows across the gap, above the walls so they can be seen: +y over N-left pitches, -y over the others
    for i in range(-4, 4):
        x0 = (i + 0.5) * pitch; sgn = 1 if i % 2 == 0 else -1
        arrow((x0, -sgn * 0.016, h + 0.012), (0, sgn, 0), 0.032, 0.0016, m['arrB'])
    # the coil: a flat rectangular winding one pitch wide, its two legs in the gap over opposite poles
    x1, x2 = -pitch / 2, pitch / 2; ztop, zbot = h + 0.03, 0.012
    for xa in (x1, x2): box((xa, 0, (ztop + zbot) / 2), (0.007, 0.006, ztop - zbot), m['copper'])
    box((0, 0, ztop), (x2 - x1 + 0.007, 0.006, 0.007), m['copper']); box((0, 0, zbot), (x2 - x1 + 0.007, 0.006, 0.007), m['copper'])
    box((0, 0, ztop + 0.025), (0.06, 0.006, 0.04), m['former'])                # bracket up to the cart
    box((0, 0, ztop + 0.06), (0.14, 0.09, 0.03), m['alu'])                    # underside of the cart
    # current arrows on the legs: down in the left leg, up in the right; force arrows along +x on both
    arrow((x1 - 0.012, -0.007, 0.024), (0, 0, 1), 0.034, 0.0019, m['arrI'])
    arrow((x2 + 0.012, -0.007, h - 0.002), (0, 0, -1), 0.034, 0.0019, m['arrI'])
    arrow((0.075, -0.02, ztop + 0.06), (1, 0, 0), 0.07, 0.0028, m['arrF'])
    camera((0.16, -0.42, 0.24), (0.0, 0, 0.045), lens=45)
    lights(key=(0.4, -0.7, 0.8), power=120, size=0.7)
    render('motor', (1300, 1000), {'channel': (-0.13, -0.017, 0.05), 'magN': (0.02, 0.009, 0.03), 'magS': (-0.02, 0.009, 0.022),
           'B': (0.10, 0.0, h + 0.012), 'coil': (0, 0, ztop), 'Ileft': (x1 - 0.012, -0.007, 0.045), 'Iright': (x2 + 0.012, -0.007, 0.045),
           'F': (0.13, -0.02, ztop + 0.06), 'cart': (0.05, 0, ztop + 0.075)})

_only = os.environ.get('SCENES')
for f in (scene_rig, scene_joint_ball, scene_joint_cart, scene_strut, scene_motor):
    if not _only or f.__name__ in _only.split(','): f()

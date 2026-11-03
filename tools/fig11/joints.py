"""Exploded views of the strut's two pinned ends, same camera and scale. Run: bvenv/bin/python joints.py <outdir>"""
import bpy, math, json, sys, os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
OUT = sys.argv[-1]; os.makedirs(OUT, exist_ok=True)

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 64; sc.cycles.use_denoising = True
    sc.render.film_transparent = True; sc.view_settings.view_transform = 'Standard'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.9, 0.9, 0.9, 1); bg.inputs[1].default_value = 0.6
MATS = {}
def mat(name, rgb, metal=0.0, rough=0.4):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    MATS[name] = m; return m
def M():
    MATS.clear()
    return dict(steel=mat('steel', (0.58, 0.59, 0.61), 1, 0.35), dark=mat('dark', (0.20, 0.20, 0.22), 1, 0.5), alu=mat('alu', (0.80, 0.81, 0.82), 1, 0.3),
                bronze=mat('bronze', (0.72, 0.48, 0.22), 1, 0.35), carbon=mat('carbon', (0.05, 0.05, 0.055), 0, 0.4), ball=mat('ball', (0.095, 0.010, 0.018), 0, 0.5),
                axis=mat('axis', (0.35, 0.35, 0.35), 0, 0.8))
def link(ob, m): ob.data.materials.append(m); return ob
def cyl(p1, p2, r, m, verts=48):
    p1, p2 = Vector(p1), Vector(p2); d = p2 - p1
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d.length, location=(p1 + p2) / 2)
    ob = bpy.context.object; ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = d.to_track_quat('Z', 'Y'); bpy.ops.object.shade_smooth(); return link(ob, m)
def hollow(ob, p1, p2, r):
    c = cyl(p1, p2, r, mat('cut', (1, 0, 0)), 48); mod = ob.modifiers.new('h', 'BOOLEAN'); mod.operation = 'DIFFERENCE'; mod.object = c
    c.hide_render = True; c.hide_viewport = True; return ob
def tube(p1, p2, ro, ri, m):
    p1, p2 = Vector(p1), Vector(p2); d = (p2 - p1) * 0.02
    return hollow(cyl(p1, p2, ro, m, 64), p1 - d, p2 + d, ri)
def sphere(c, r, m):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=r, location=c); ob = bpy.context.object; bpy.ops.object.shade_smooth(); return link(ob, m)
def box(c, size, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); ob = bpy.context.object; ob.scale = size; return link(ob, m)
def torus(c, R, r, m):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=64, minor_segments=24, location=c)
    ob = bpy.context.object; ob.rotation_euler = (math.pi / 2, 0, 0); bpy.ops.object.shade_smooth(); return link(ob, m)
def dashes(z1, z2, m, x=0, y=0):
    n = int(abs(z2 - z1) / 0.008); step = (z2 - z1) / n
    for i in range(n):
        if i % 2 == 0: cyl((x, y, z1 + i * step), (x, y, z1 + (i + 0.6) * step), 0.0007, m, 12)
def camera(target, ortho):
    cam = bpy.data.cameras.new('cam'); ob = bpy.data.objects.new('cam', cam); bpy.context.collection.objects.link(ob)
    loc = Vector(target) + Vector((0.45, -0.95, 0.38)).normalized() * 3
    ob.location = loc; ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = (Vector(target) - loc).to_track_quat('-Z', 'Y')
    cam.type = 'ORTHO'; cam.ortho_scale = ortho; bpy.context.scene.camera = ob
def lights():
    for loc, pw, sz in (((0.6, -0.9, 0.9), 55, 0.6), ((-0.7, -0.4, 0.4), 26, 0.8), ((0.2, 0.8, 0.6), 20, 0.6)):
        ld = bpy.data.lights.new('l', 'AREA'); ld.energy = pw; ld.size = sz; ob = bpy.data.objects.new('l', ld); bpy.context.collection.objects.link(ob)
        ob.location = loc; ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y')
def render(name, res, labels):
    sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y = res; sc.render.filepath = os.path.join(OUT, name + '.png')
    bpy.ops.render.render(write_still=True)
    json.dump({k: [round(v.x * 100, 2), round((1 - v.y) * 100, 2)] for k, v in ((k, world_to_camera_view(sc, sc.camera, Vector(p))) for k, p in labels.items())},
              open(os.path.join(OUT, name + '.json'), 'w')); print('rendered', name)

def clevis(zbase, down, m, holes=True):
    """base plate at zbase, two cheeks extending `down` (+1 up / -1 down) with a bore along y; returns pin z"""
    base = box((0, 0, zbase), (0.048, 0.036, 0.008), m['dark'])
    if holes:
        for s in (-1, 1): hollow(base, (s * 0.019, 0, zbase - 0.01), (s * 0.019, 0, zbase + 0.01), 0.0032)
    zp = zbase + down * 0.028
    for s in (-1, 1): hollow(box((0, s * 0.0135, zbase + down * 0.022), (0.028, 0.005, 0.036), m['dark']), (0, s * 0.02, zp), (0, s * 0.007, zp), 0.0038)
    return zp
def rodend(zc, m, shank_dir, shank_len):
    torus((0, 0, zc), 0.0085, 0.0035, m['steel']); sphere((0, 0, zc), 0.0058, m['bronze'])
    cyl((0, 0, zc + shank_dir * 0.011), (0, 0, zc + shank_dir * shank_len), 0.0045, m['steel'])

def fork(m, G=0.0, cut_front=False):
    """strut's upper end: two steel cheeks straddling ball 2, bronze bushings on the axle line (y axis at z=0), bridge and boss below"""
    parts = []
    for sy in (-1, 1):
        ch = box((0, sy * 0.045, -0.025 - G), (0.026, 0.006, 0.07), m['dark'])
        hollow(ch, (0, sy * 0.06, -G), (0, sy * 0.03, -G), 0.0062)
        tube((0, sy * 0.042, -G), (0, sy * 0.048, -G), 0.0062, 0.0042, m['bronze'])
        parts.append(ch)
    box((0, 0, -0.062 - G), (0.026, 0.096, 0.008), m['dark'])                 # bridge
    cyl((0, 0, -0.066 - G), (0, 0, -0.086 - G), 0.011, m['dark'])              # boss, threaded onto the inner tube
    return parts
def scene_ball_end():
    reset(); m = M()
    th = math.radians(18); up = Vector((-math.sin(th), 0, math.cos(th)))
    cyl(up * 0.02, up * 0.11, 0.007, m['carbon'])                              # rod 2, fixed into the ball
    b = sphere((0, 0, 0), 0.035, m['ball']); hollow(b, (0, -0.05, 0), (0, 0.05, 0), 0.0045)   # ball 2 with a bore through its centre
    fork(m)
    cyl((0, -0.20, 0), (0, -0.11, 0), 0.004, m['steel'])                       # axle, pulled out along its own line
    cyl((0, -0.206, 0), (0, -0.20, 0), 0.0065, m['steel'])                     # axle head
    for i in range(10):                                                         # dotted line: where the axle goes
        y0 = -0.105 + i * 0.016
        if y0 < 0.06: cyl((0, y0, 0), (0, y0 + 0.008, 0), 0.0012, m['axis'], 12)
    cyl((0, 0, -0.086), (0, 0, -0.17), 0.008, m['steel'])                      # inner tube
    camera((0, -0.07, -0.05), 0.27); lights()
    render('ball-end', (1100, 1100), {'rod2': up * 0.085, 'ball': (0.024, -0.02, 0.016), 'bore': (0, -0.035, 0), 'axle': (0, -0.15, 0.004),
           'cheek': (0.013, -0.048, -0.035), 'bush': (0, -0.048, 0.0055), 'bridge': (0.013, -0.03, -0.062), 'boss': (0.011, 0, -0.078),
           'tube': (0.008, 0, -0.14)})

def scene_cart_end():
    reset(); m = M(); G = 0.04
    plate = box((0.015, 0.008, 0.0), (0.12, 0.10, 0.024), m['alu'])                                     # cart top plate (part of it)
    zb = 0.012 + G + 0.004; zp = clevis(zb, +1, m)                                           # clevis, exploded up
    for s in (-1, 1):
        hollow(plate, (s * 0.019, 0, -0.02), (s * 0.019, 0, 0.02), 0.0032)
        cyl((s * 0.019, 0, zb + 0.016), (s * 0.019, 0, zb + 0.034), 0.0028, m['steel']); cyl((s * 0.019, 0, zb + 0.034), (s * 0.019, 0, zb + 0.040), 0.0042, m['dark'])   # two cap screws, exploded above their holes
    cyl((-0.028, -0.055, zp), (-0.028, -0.005, zp), 0.0035, m['steel']); sphere((-0.028, -0.057, zp), 0.0052, m['steel'])
    cyl((-0.028, -0.06, zp), (-0.028, 0.0, zp), 0.0006, m['axis'], 8)
    ze = zp + 0.04 + G; rodend(ze, m, +1, 0.03)
    tube((0, 0, ze + 0.03), (0, 0, ze + 0.11), 0.0125, 0.0105, m['alu'])                      # outer tube
    dashes(0.012, ze + 0.115, m['axis'])
    camera((0, 0, 0.115), 0.33); lights()
    render('cart-end', (900, 1300), {'cart': (0.06, -0.035, 0.004), 'screws': (0.019, -0.003, zb + 0.03), 'clevis': (0.016, -0.018, zb + 0.012),
           'bore': (0.014, -0.0135, zp), 'pin': (-0.028, -0.03, zp + 0.0035), 'eye': (-0.0085, -0.003, ze), 'bearing': (0.0, -0.0058, ze),
           'shank': (0.0045, 0, ze + 0.022), 'tube': (0.0125, -0.006, ze + 0.085)})

import os
_o = os.environ.get('SCENES', 'ball,cart')
if 'ball' in _o: scene_ball_end()
if 'cart' in _o: scene_cart_end()

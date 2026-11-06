"""Guinness Gravity pint glass -> Blender meshes (outer and inner surfaces with the sculpted panels) -> glass.glb,
and the independent volume check of the cavity. Geometry lives in geom.py; this script only meshes and exports.

Run: python3 tools/fig12/glass.py <outdir>
Writes glass_profile.json (the body-of-revolution profile on a 0.5 mm grid, the panel parameters, volumes and fill heights)
and glass.glb (outer and inner surfaces, metres, y up, for the page's renderer).
"""
import sys, json, math, numpy as np
import geom as G
outdir = sys.argv[1]
zz = np.arange(0.0, G.H + 1e-9, 0.5)
Ro = G.R0(zz); Ri0 = G.R_inner(zz, np.pi / 2)             # the round wall (theta = 90 deg has no panel)
V_brim = G.cavity_volume(G.H)
hs = np.arange(G.Z_F + 1, G.H, 0.25); Vs = np.array([G.cavity_volume(h, nz=401, nt=64) for h in hs])
h568 = float(np.interp(568e3, Vs, hs)); h500 = float(np.interp(500e3, Vs, hs))
print(f'outer: foot {2*Ro[0]:.1f}, waist {2*Ro[(zz>15)&(zz<60)].min():.1f} at z={zz[(zz>15)&(zz<60)][np.argmin(Ro[(zz>15)&(zz<60)])]:.1f}, widest {2*Ro.max():.1f} at z={zz[Ro.argmax()]:.1f}, rim {2*Ro[-1]:.1f} mm')
print(f'cavity: brim {V_brim/1e3:.1f} mL; 568 mL at z = {h568:.1f} mm ({G.H-h568:.1f} below the rim); 500 mL at z = {h500:.1f} mm')
prof = dict(source='dimensions.com "Irish Imperial Pint Glass" elevation (profile_drawing.csv), scaled to H = 160 mm and widest diameter 85 mm; '
                   'sculpted panels from product photographs, depth estimated',
            H_mm=G.H, wall_mm=G.T_W, floor_mm=G.Z_F, panel=dict(A_mm=G.A_PANEL, W_crease_deg=math.degrees(G.W_CREASE), z_V0=G.Z_V0, z_V1=G.Z_V1, z_V2=G.Z_V2),
            z_mm=zz.tolist(), R_outer_mm=np.round(Ro, 3).tolist(), R_inner_mm=[None if z < G.Z_F else round(float(v), 3) for z, v in zip(zz, Ri0)],
            V_brim_mL=round(V_brim / 1e3, 1), z_568_mm=round(h568, 2), z_500_mm=round(h500, 2))
json.dump(prof, open(f'{outdir}/glass_profile.json', 'w'))

# ---- Blender: build both surfaces as rings of R(z, theta), measure the cavity volume independently, export GLB ----
import bpy, bmesh
bpy.ops.wm.read_factory_settings(use_empty=True)
NSEG = 64                                              # 5.6 deg around: resolves the 6 deg crease; with 2 mm rings about 10 000 quads per surface, light enough for a phone
TH = 2 * np.pi * np.arange(NSEG) / NSEG
def surface(name, zs, Rfun, cap_bottom, flip=False, scale=1.0):
    bm = bmesh.new(); rings = []
    for zc in zs:
        rr = Rfun(zc, TH) * scale
        rings.append([bm.verts.new((rr[k] * math.cos(TH[k]), rr[k] * math.sin(TH[k]), zc * scale)) for k in range(NSEG)])
    for a, b in zip(rings[:-1], rings[1:]):
        for k in range(NSEG):
            q = (a[k], a[(k + 1) % NSEG], b[(k + 1) % NSEG], b[k])
            bm.faces.new(q[::-1] if flip else q)
    if cap_bottom: bm.faces.new(rings[0][::-1] if not flip else rings[0])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob); return ob
zc = zz[zz >= G.Z_F]
cav = surface('cavity_check', zc, G.R_inner, cap_bottom=True)                      # the volume check on the fine 0.5 mm rings
bm = bmesh.new(); bm.from_mesh(cav.data); bmesh.ops.contextual_create(bm, geom=[e for e in bm.edges if e.is_boundary])
bmesh.ops.recalc_face_normals(bm, faces=bm.faces); vb = bm.calc_volume(signed=False); bm.free()
print(f'Blender cavity volume (closed mesh, {NSEG} segments): {vb/1e3:.1f} mL; polygon/circle factor {NSEG/(2*math.pi)*math.sin(2*math.pi/NSEG):.5f}')
bpy.data.objects.remove(cav)
zm = np.arange(0.0, G.H + 1e-9, 2.0); zmc = zm[zm >= G.Z_F]                                 # the rendered surfaces on 2 mm rings
outer = surface('glass_outer', zm, G.R_outer, cap_bottom=True, scale=1e-3)
inner = surface('glass_inner', zmc, G.R_inner, cap_bottom=True, flip=True, scale=1e-3)
for ob in (outer, inner):
    for p in ob.data.polygons: p.use_smooth = True
bpy.ops.export_scene.gltf(filepath=f'{outdir}/glass.glb', export_format='GLB', export_yup=True, export_apply=True)
print('wrote', f'{outdir}/glass_profile.json', f'{outdir}/glass.glb')

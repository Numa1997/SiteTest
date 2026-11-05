"""Guinness tulip pint glass: profile -> Blender solid of revolution -> volumes and meshes.

Run: python3 tools/fig12/glass.py <outer.csv from profile_from_photo.py> <outdir>
Geometry decisions (measured in the photo, see notes/fig12/geometry.md):
  * pixel scale from rim plane to foot plane (ellipse centres, rows 41.5 and 449.0) = 160 mm;
  * wall thickness T_W = 2.0 mm (uncertain +-0.5 mm), floor of the cavity Z_F = 8.0 mm above the foot.
Outputs: glass_profile.json (outer and inner radius on a 0.5 mm grid, volumes),
         glass.glb (outer and inner surfaces as Blender meshes, for the page's renderer).
"""
import sys, json, math, numpy as np
from scipy.interpolate import UnivariateSpline
src, outdir = sys.argv[1], sys.argv[2]
d = np.loadtxt(src, delimiter=',')
OLD_S = 160.0 / 419.0                     # scale used in profile_from_photo.py (mm/px)
PX_RIM, PX_FOOT, PX_BOT = 41.5, 449.0, 458.0
S = 160.0 / (PX_FOOT - PX_RIM)            # mm per px, rim plane to foot plane
z_px_from_bottom = d[:, 0] / OLD_S        # back to px above the lowest dark row
r_px = d[:, 1] / OLD_S
z = (z_px_from_bottom - (PX_BOT - PX_FOOT)) * S   # mm above the foot plane
R = r_px * S
keep = (z > 9.0) & (z < 157.0)            # drop rows distorted by the rim and foot ellipses
z, R = z[keep][::-1], R[keep][::-1]
spl = UnivariateSpline(z, R, s=len(z) * 0.20 ** 2, k=4)   # 0.2 mm rms: about half a photo pixel (0.39 mm)
H, T_W, Z_F = 160.0, 2.0, 8.0
zz = np.arange(0.0, H + 1e-9, 0.5)
Ro = spl(np.clip(zz, z.min(), z.max()))
# below the clean data the foot is near-cylindrical; above it the rim continues its slope
Ro[zz < z.min()] = spl(z.min()); top = zz > z.max(); Ro[top] = spl(z.max()) + spl.derivative()(z.max()) * (zz[top] - z.max())
slope = np.gradient(Ro, zz)
Ri = Ro - T_W * np.sqrt(1 + slope ** 2)   # thickness measured normal to the wall
Ri[zz < Z_F] = np.nan
def vol(h):                                # cavity volume below z = h, mm^3
    m = (zz >= Z_F) & (zz <= h)
    return np.trapezoid(np.pi * Ri[m] ** 2, zz[m])
V_brim = vol(H)
hs = np.arange(Z_F, H, 0.05); Vs = np.array([vol(h) for h in hs])
h568 = np.interp(568e3, Vs, hs); h500 = np.interp(500e3, Vs, hs)
print(f'scale {S:.4f} mm/px; outer: foot {2*Ro[0]:.1f}, waist {2*Ro[(zz>15)&(zz<60)].min():.1f} at z={zz[(zz>15)&(zz<60)][np.argmin(Ro[(zz>15)&(zz<60)])]:.1f}, '
      f'widest {2*Ro.max():.1f} at z={zz[Ro.argmax()]:.1f}, rim {2*Ro[-1]:.1f} mm')
print(f'cavity: brim volume {V_brim/1e3:.1f} mL; 568 mL reaches z = {h568:.1f} mm ({H-h568:.1f} mm below rim); 500 mL reaches z = {h500:.1f} mm')
prof = dict(source='MBS Wholesale product photo guiness_2.jpg, scaled to 160 mm height (retailer listings)', H_mm=H, wall_mm=T_W, floor_mm=Z_F,
            z_mm=zz.tolist(), R_outer_mm=np.round(Ro, 3).tolist(), R_inner_mm=[None if np.isnan(v) else round(float(v), 3) for v in Ri],
            V_brim_mL=round(V_brim / 1e3, 1), z_568_mm=round(h568, 2), z_500_mm=round(h500, 2))
json.dump(prof, open(f'{outdir}/glass_profile.json', 'w'))

# ---- Blender: revolve both surfaces, measure the cavity volume independently, export GLB ----
import bpy, bmesh
bpy.ops.wm.read_factory_settings(use_empty=True)
NSEG = 96
def revolve(name, zs, rs, cap_bottom, flip=False):
    bm = bmesh.new(); rings = []
    for zc, rc in zip(zs, rs):
        rings.append([bm.verts.new((rc * math.cos(2 * math.pi * k / NSEG), rc * math.sin(2 * math.pi * k / NSEG), zc)) for k in range(NSEG)])
    for a, b in zip(rings[:-1], rings[1:]):
        for k in range(NSEG):
            q = (a[k], a[(k + 1) % NSEG], b[(k + 1) % NSEG], b[k])
            bm.faces.new(q[::-1] if flip else q)
    if cap_bottom:
        f = bm.faces.new(rings[0][::-1] if not flip else rings[0])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob); return ob
m = ~np.isnan(Ri)
cav = revolve('cavity_check', np.r_[zz[m]], np.r_[Ri[m]], cap_bottom=True)
bm = bmesh.new(); bm.from_mesh(cav.data); bmesh.ops.contextual_create(bm, geom=[e for e in bm.edges if e.is_boundary]); 
bmesh.ops.recalc_face_normals(bm, faces=bm.faces); vb = bm.calc_volume(signed=False); bm.free()
print(f'Blender cavity volume (closed revolved mesh, {NSEG} segments): {vb/1e3:.1f} mL; polygon/circle factor {NSEG/(2*math.pi)*math.sin(2*math.pi/NSEG):.5f}')
bpy.data.objects.remove(cav)
# glass shell for rendering, in metres, y up (glTF convention)
outer = revolve('glass_outer', zz / 1000, Ro / 1000, cap_bottom=True)
inner = revolve('glass_inner', zz[m] / 1000, Ri[m] / 1000, cap_bottom=True, flip=True)
for ob in (outer, inner):
    for p in ob.data.polygons: p.use_smooth = True
bpy.ops.export_scene.gltf(filepath=f'{outdir}/glass.glb', export_format='GLB', export_yup=True, export_apply=True)
print('wrote', f'{outdir}/glass_profile.json', f'{outdir}/glass.glb')

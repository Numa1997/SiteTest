# `public/scripts/wave3d-view.js` · the lit 3D views of Fig. 14

An ES module (loaded with `<script type="module">`) that draws a stored wave in a lit 3D room with three.js 0.170.0, vendored in
[public/vendor/three/](../../public/vendor/three/) (no CDN). It computes no physics: the page hands it numbers read from Kaggle's
files. When loaded it sets `window.Wave3D` and fires the window event `wave3d-ready` (the page's classic script waits for it).

## What it draws

- **Sheets**: the surfaces $\mathrm{Re}\,\psi = +c$ (crests, wine `#a3303f`) and $\mathrm{Re}\,\psi = -c$ (troughs, slate `#55607a`),
  found by marching cubes on the grid the page gives (`marching(field, nx, ny, nz, level, sign, x0, y0, z0, h)`, corner and edge
  order as in three's `MarchingCubes.js`, whose `edgeTable` and `triTable` it imports). Vertex normals are the interpolated
  gradient; each triangle is wound to agree with them, so lighting is right from both sides.
- **Cutaway**: the sheets and the barrier clipped by the planes $y = 0$ and $z = 0$ (physics axes) with `clipIntersection`, so only
  the quarter $y > 0, z > 0$ is removed.
- **Surface**: a plane of $\mathrm{Re}\,\psi$ (the page passes $z = 0$) lifted by its value and coloured by `surfaceColour(v)`:
  paper at 0, towards wine ($v > 0$) or slate ($v < 0$), full at $|v| = 0.5$ of the scale passed (the frame's largest $|\mathrm{Re}\,\psi|$).
- **Mesh** (the page's default, `setMesh`): one height surface on the grid the page gives, coloured by `meshColour(v)` in the
  house colours (card paper at $v = 0$, wine at $+1$, slate at $-1$, mixed in sRGB), with a wire mesh on every `every`-th grid line
  (ink, sharing the surface's vertex buffer) and the barrier's outline as polylines lying on the sheet. Normals come from central
  differences of the heights. In this mode the floor, grid, axis, barrier solid and fog of the room are hidden, the lights are
  white (hemisphere 1.55, sun 1.9, so a level patch shows its own colour) and the material is not tone-mapped: the page's pixel
  check inverts the ramp with `meshV(px)`. The mode keeps its own camera (`api.meshCam`, distance 1.34 × the sheet's width).
- **Room**: paper background, a floor with a grid at $z = -17.5$, a hemisphere light, a sun with soft shadows, a fill light, the
  dashed flight axis with an arrow. **Barrier** (`setBarrier({shape, R, a, hard, V0})`): sphere, slab ($|x| < a/2$, drawn over
  the box), pillar (column along $z$, drawn 32 a tall), coin, tube; glass for a finite height, opaque for a hard wall, tan for a well.

Axes: physics $(x, y, z)$ go to three's $(x, z, y)$, so physics $z$ is up on screen.

## Spherical waves

`setShells(crestRadii, troughRadii)` draws exact spheres (128 × 64 segments each); `setRevolution(re, rmax, dr, scale)` lifts the
plane z = 0 by a function of r on a polar mesh (192 angles); `setRoom(floorY, dist)` moves the floor and the camera for them.

## API

`Wave3D.create(canvas, {canTurn, onTurn})` returns `api` with `setField` (optional last argument: the spacing along $x$ when it
differs), `setPlane`, `setBarrier`, `setMesh({nx, ny, x0, y0, h, H, T, every, outline, key})`, `setMeshView(span)`, `meshVertex(k)`,
`heightAt(x, y)`, `setMode('mesh' | 'sheets' | 'surface' | 'cutaway')`, `clear`, `resize(w, h, dpr)`, `render`, `project([x, y, z])` (CSS pixels), `pickPlane(cx, cy)` (the point where the
pixel's ray meets $z = 0$; in the mesh mode, where it first meets the sheet), `readPixel(cx, cy)` (the drawn RGBA; the renderer keeps its drawing buffer for this), and the numbers
`triangles`, `level`, `scale`, `height`, `yaw`, `pitch`, `dist`. Turning: press and drag (never a mere pass of the pointer).

## Measured (headless Chromium with SwiftShader, 12 November 2026)

The default sphere run (true 3D data, 96 × 64 × 64): about 15 000 to 29 000 triangles per frame for the two sheets. No horizontal
overflow at 360, 390, 1024 or 1440 px.

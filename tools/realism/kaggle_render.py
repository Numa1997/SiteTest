"""Kaggle GPU notebook: path-traced test frame of the pint (tools/realism/render_pint.py) beside a photograph of a real pint.
Environment: COMMIT, RIDE (path under public/data), K (frame), SAMPLES. Outputs in /kaggle/working: render.png, compare.png,
render.log. The photograph is J Wynia's "Pint of Guinness in Dublin" (CC BY, flickr 2665596032); the room light is Poly Haven's
CC0 HDR photograph named in HDRI_URL."""
import io, os, subprocess, tarfile, time, urllib.request

COMMIT = os.environ["COMMIT"]; RIDE = os.environ.get("RIDE", "public/data/fig16/2026-11-15/kerb_full.json"); K = os.environ.get("K", "36")
WORK = "/kaggle/working"; REPO = "/tmp/repo"; LOG = open(os.path.join(WORK, "render.log"), "w")
BLENDER = "https://download.blender.org/release/Blender4.2/blender-4.2.3-linux-x64.tar.xz"
HDRI_URL = "https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/2k/brown_photostudio_02_2k.hdr"
PHOTO = "https://live.staticflickr.com/3255/2665596032_a3cb3047d1_b.jpg"


def log(m):
    print(m, flush=True); LOG.write(m + "\n"); LOG.flush()


t0 = time.time()
data = urllib.request.urlopen(f"https://codeload.github.com/Numa1997/SiteTest/tar.gz/{COMMIT}").read()
with tarfile.open(fileobj=io.BytesIO(data)) as t:
    top = t.getnames()[0].split("/")[0]; t.extractall("/tmp")
os.rename(os.path.join("/tmp", top), REPO); log(f"repository at {COMMIT}")
subprocess.run(f"curl -sL {BLENDER} | tar -xJ -C /tmp", shell=True, check=True); log(f"blender in {time.time() - t0:.0f} s")
hdri = "/tmp/room.hdr"
try: urllib.request.urlretrieve(HDRI_URL, hdri); log("HDRI " + HDRI_URL)
except Exception as e: hdri = "none"; log(f"no HDRI ({e}): physical sky")
blender = [p for p in os.listdir("/tmp") if p.startswith("blender-4.2")][0]
env = dict(os.environ, GLASS_JS=os.path.join(REPO, "public/scripts/guinness-glass.js"))
r = subprocess.run([f"/tmp/{blender}/blender", "-b", "-P", os.path.join(REPO, "tools/realism/render_pint.py"), "--",
                    os.path.join(REPO, RIDE), K, os.path.join(WORK, "render.png"), hdri], capture_output=True, text=True, env=env)
log(r.stdout[-4000:]); log(r.stderr[-4000:]); log(f"blender exit {r.returncode}, {time.time() - t0:.0f} s in all")
from PIL import Image  # noqa: E402
a = Image.open(os.path.join(WORK, "render.png")).convert("RGB"); b = Image.open(io.BytesIO(urllib.request.urlopen(PHOTO).read())).convert("RGB")
h = 1200; a = a.resize((int(a.width * h / a.height), h)); b = b.resize((int(b.width * h / b.height), h))
c = Image.new("RGB", (a.width + b.width + 20, h), (255, 255, 255)); c.paste(a, (0, 0)); c.paste(b, (a.width + 20, 0))
c.save(os.path.join(WORK, "compare.png")); log("compare.png: render (left), photograph (right)")

if os.environ.get("NB_LOCAL") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "taichi==1.7.4"], check=True)
import taichi as ti
try: print(subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], capture_output=True, text=True).stdout)
except FileNotFoundError: print("nvidia-smi not found")
ARCH = ti.cpu if os.environ.get("NB_LOCAL") else ti.cuda
ti.init(arch=ARCH, default_fp=ti.f32)
if ARCH == ti.cuda and ti.lang.impl.current_cfg().arch != ti.cuda: raise RuntimeError("no GPU: stopping")
import urllib.request
SITE = "https://raw.githubusercontent.com/Numa1997/SiteTest/816dda6cf741e4350bf2802e2419b127ad1d0bae/public/scripts/"
GLASS_JS = urllib.request.urlopen(SITE + "guinness-glass.js").read().decode()
VIEW_JS = urllib.request.urlopen(SITE + "stout-view.js").read().decode()
R = json.loads(re.search(r"R:\s*(\[[^\]]*\])", GLASS_JS).group(1)); DZP = 0.0005
log(f"ready; glass profile {len(R)} radii, rim at {(len(R) - 1) * DZP * 1e3:.1f} mm; website drawing code {len(VIEW_JS):,} characters")
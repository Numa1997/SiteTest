import subprocess, socket, json
out = {}
r = subprocess.run(['bash','-c','nvidia-smi --query-gpu=name,memory.total --format=csv,noheader'], capture_output=True, text=True)
out['gpu'] = r.stdout.strip() or ('none: ' + r.stderr.strip()[:120])
for h in ('github.com', 'dl.openfoam.com', 'conda.anaconda.org'):
    try: out[h] = socket.gethostbyname(h)
    except Exception as e: out[h] = 'NO DNS: ' + str(e)
try:
    import jax; out['jax'] = jax.__version__; out['jax_devices'] = str(jax.devices())
except Exception as e: out['jax'] = 'import failed: ' + str(e)[:200]
print(json.dumps(out, indent=1)); json.dump(out, open('/kaggle/working/probe.json','w'), indent=1)

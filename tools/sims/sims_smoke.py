"""The engine's own test model (registry entry sims_smoke, "manual": computed only by Run workflow, never by a merge).

It has no physics. It writes two small files whose bytes depend only on the shard number, so a test can predict them:
  a.bin   100 000 bytes from numpy's default random generator seeded with the shard number;
  b.json  the seed and the shard.
It returns a header with "checks_passed": True, or False when the environment variable SIMS_SMOKE_FAIL is "1", so the engine's
refusal of a run whose own checks failed can be tested on the real line too.
Usage: python3 sims_smoke.py [out_dir]"""
import json, os, sys
import numpy as np

def run(out_dir, shard=1, shards=1):
    os.makedirs(out_dir, exist_ok=True)
    seed = int(shard)
    data = np.random.default_rng(seed).integers(0, 256, size=100_000, dtype=np.uint8).tobytes()
    open(os.path.join(out_dir, "a.bin"), "wb").write(data)
    json.dump(dict(seed=seed, shard=int(shard), shards=int(shards)), open(os.path.join(out_dir, "b.json"), "w"), indent=1)
    ok = os.environ.get("SIMS_SMOKE_FAIL") != "1"
    return dict(model="sims_smoke", checks_passed=ok, grid_part={"seed": [seed]})

if __name__ == "__main__":
    print(run(sys.argv[1] if len(sys.argv) > 1 else "."))

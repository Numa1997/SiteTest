"""Relay Fig. 15 generation 2026-11-18 from the Kaggle filer output to R2: GET each file, check SHA-256 against the branch record,
PUT to R2, check R2's etag = MD5. Log: OK key bytes md5. Skips keys already logged. Usage: up.py [limit]"""
import json, glob, hashlib, os, subprocess, sys, threading, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
TR = '/root/.claude/projects/-home-user-SiteTest/dd110b25-e31c-548e-b1d2-291e8e510c8d/tool-results/'
urls = {}
for p in glob.glob(TR + 'mcp-Kaggle-list_notebook_session_output-17950164*.txt') + glob.glob(TR + 'mcp-Kaggle-list_notebook_session_output-1795016376178*.txt'):
    for f in json.load(open(p))['files']: urls[f['file_name']] = f['url']
rep = json.load(open('../replaced.json')); sha = {}
for f in ['../rec/walls_runs.jsonl'] + glob.glob('../rec/rt2d_runs_*.jsonl'):
    for l in open(f): r = json.loads(l); sha[r['file']] = r.get('sha256') or r.get('sha256_rebuilt')
PRE = 'resonant-tunnelling/2026-11-18/runs/'
assert all(PRE + n in urls for n in rep), sum(PRE + n not in urls for n in rep)
acct = json.load(urllib.request.urlopen(urllib.request.Request('https://api.cloudflare.com/client/v4/accounts', headers={'User-Agent': 'curl/8'})))['result'][0]['id']
API = f'https://api.cloudflare.com/client/v4/accounts/{acct}/r2/buckets/phyein-usul-runs/objects/'
LOG = 'up.log'; done = set(l.split()[1] for l in open(LOG) if l.startswith('OK ')) if os.path.exists(LOG) else set()
todo = [n for n in rep if PRE + n not in done][:int(sys.argv[1]) if len(sys.argv) > 1 else None]
lock = threading.Lock(); st = dict(n=len(done), b=0, fail=0); t0 = time.time(); last = [0]
def prog(msg=''):
    sh = os.environ.get('CLAUDE_PROGRESS_SH')
    if sh: subprocess.run(['bash', sh, '-n', 'fig15-r2-upload', f"{st['n']}/{len(rep)}", msg])
def one(n):
    key = PRE + n; err = None
    for a in range(4):
        try:
            blob = urllib.request.urlopen(urls[key], timeout=180).read()
            assert hashlib.sha256(blob).hexdigest() == sha[n], 'sha256 differs from record'
            md5 = hashlib.md5(blob).hexdigest()
            rq = urllib.request.Request(API + key, data=blob, method='PUT', headers={'Content-Type': 'application/octet-stream', 'User-Agent': 'curl/8'})
            j = json.load(urllib.request.urlopen(rq, timeout=300))
            assert j.get('success'), j
            et = (j.get('result') or {}).get('etag', '').strip('"')
            assert et == md5, ('etag', et, md5)
            with lock:
                open(LOG, 'a').write(f'OK {key} {len(blob)} {md5}\n'); st['n'] += 1; st['b'] += len(blob)
                if time.time() - last[0] > 2: last[0] = time.time(); prog(f"{st['b'] / 1e9:.2f} GB this run, {st['fail']} failed")
            return
        except Exception as e: err = repr(e)[:300]; time.sleep(3 * (a + 1))
    with lock: st['fail'] += 1; open(LOG, 'a').write(f'FAIL {key} {err}\n'); print('FAIL', key, err, flush=True)
with ThreadPoolExecutor(8) as ex: list(ex.map(one, todo))
print('uploaded', st['n'], 'of', len(rep), 'bytes this run', st['b'], 'failed', st['fail'], 'seconds', round(time.time() - t0), flush=True)
sh = os.environ.get('CLAUDE_PROGRESS_SH')
if sh: subprocess.run(['bash', sh, '-n', 'fig15-r2-upload', 'fail' if st['fail'] else ('done' if st['n'] == len(rep) else f"{st['n']}/{len(rep)}"), f"{st['fail']} failed"])

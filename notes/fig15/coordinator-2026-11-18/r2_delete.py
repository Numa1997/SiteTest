"""Delete from R2 the generation 2026-11-14 run files that generation 2026-11-18 replaces (owner's order, 18 Nov 2026).
Only keys resonant-tunnelling/2026-11-14/runs/<file> whose file (a) has status rebuilt or recomputed in the new index and
(b) has its replacement logged as uploaded (OK line in up.log). Log: DEL key | GONE key (already absent) | FAIL key error."""
import json, os, subprocess, threading, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
new = json.load(open('../new_index.json')); old = json.load(open('../rec/old_index.json'))
rep = [r['file'] for r in new['runs'] if r['status'] in ('rebuilt', 'recomputed')]
kept = {r['file'] for r in new['runs'] if r['status'] == 'kept'}
up = {l.split()[1].rsplit('/', 1)[1] for l in open('up.log') if l.startswith('OK ')}
oldfiles = {r['file'] for r in old['runs']}
assert len(rep) == 2782 and len(kept) == 915 and not (set(rep) & kept), (len(rep), len(kept))
assert set(rep) <= up and set(rep) <= oldfiles, 'a replacement is not logged as uploaded'
assert sorted(rep) == sorted(json.load(open('../replaced.json')))
acct = json.load(urllib.request.urlopen(urllib.request.Request('https://api.cloudflare.com/client/v4/accounts', headers={'User-Agent': 'curl/8'})))['result'][0]['id']
API = f'https://api.cloudflare.com/client/v4/accounts/{acct}/r2/buckets/phyein-usul-runs/objects/'
PRE = 'resonant-tunnelling/2026-11-14/runs/'; LOG = 'del.log'
done = {l.split()[1] for l in open(LOG) if l.split()[0] in ('DEL', 'GONE')} if os.path.exists(LOG) else set()
todo = [n for n in rep if PRE + n not in done]
lock = threading.Lock(); st = dict(n=len(done), fail=0); last = [0]; sh = os.environ.get('CLAUDE_PROGRESS_SH')
def prog(v, msg=''):
    if sh: subprocess.run(['bash', sh, '-n', 'fig15-r2-delete', v, msg])
def one(n):
    key = PRE + n; err = None
    for a in range(4):
        try:
            rq = urllib.request.Request(API + key, method='DELETE', headers={'User-Agent': 'curl/8'})
            try:
                j = json.load(urllib.request.urlopen(rq, timeout=120)); assert j.get('success'), j; tag = 'DEL'
            except urllib.error.HTTPError as e:
                if e.code != 404: raise
                tag = 'GONE'
            with lock:
                open(LOG, 'a').write(f'{tag} {key}\n'); st['n'] += 1
                if time.time() - last[0] > 2: last[0] = time.time(); prog(f"{st['n']}/{len(rep)}", f"{st['fail']} failed")
            return
        except Exception as e: err = repr(e)[:300]; time.sleep(3 * (a + 1))
    with lock: st['fail'] += 1; open(LOG, 'a').write(f'FAIL {key} {err}\n')
with ThreadPoolExecutor(8) as ex: list(ex.map(one, todo))
print('deleted or gone', st['n'], 'of', len(rep), 'failed', st['fail'])
prog('fail' if st['fail'] else 'done', f"{st['n']} of {len(rep)}")

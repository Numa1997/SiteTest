"""The engine's store: Cloudflare R2, the bucket phyein-usul-runs, through R2's S3-compatible API (docs/kaggle-sims.md).

Why these rules:
  - A key is never overwritten. The site's Worker (worker/r2.js) serves every /r2/ address with a one-year immutable cache, so a
    browser that once fetched a key never asks again; new bytes under an old key would reach some readers and not others.
  - Every upload is read back. The object R2 now holds is downloaded whole as a stream and its size and SHA-256 are compared with
    the run's index; only then does the engine delete its own copy. A bad object is deleted so that a retry can upload it again.
  - The SHA-256 travels with the object as its metadata "sha256", so a second upload of the same file (collect mode, a retry)
    recognises it and does nothing.

Keys come from the environment, never from a file: R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY (repository secrets, an R2
API token with Object Read & Write on this bucket only). R2_ENDPOINT overrides https://<account>.r2.cloudflarestorage.com (the local
test points it at a local S3 server); R2_BUCKET overrides the bucket name. No key is ever printed.

Usage as a module: put(local_path, key, sha256, size) -> "stored" | "already stored"; head(key) -> (size, sha256) or None.
Usage from the command line: python3 tools/sims/r2.py head <key>"""
import hashlib, os, sys, time

BUCKET = os.environ.get("R2_BUCKET", "phyein-usul-runs")
WAITS = (2, 8, 30)          # seconds between the tries of one network call
_client = None

class R2Error(Exception):
    pass

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

def missing_keys():
    """The names of the R2 variables that are not set (their values are never looked at beyond being non-empty)."""
    need = ["R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY"] + ([] if os.environ.get("R2_ENDPOINT") else ["R2_ACCOUNT_ID"])
    return [n for n in need if not os.environ.get(n)]

def client():
    global _client
    if _client is None:
        gone = missing_keys()
        if gone: raise R2Error("the repository secrets " + ", ".join(gone) + " are missing")
        import boto3
        from botocore.config import Config
        endpoint = os.environ.get("R2_ENDPOINT") or f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com"
        # retries are done here (call()), with the waits the engine documents, so the library's own retries are turned off
        _client = boto3.client("s3", endpoint_url=endpoint, region_name="auto",
                               aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"], aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
                               config=Config(retries={"max_attempts": 1, "mode": "standard"}, signature_version="s3v4",
                                             request_checksum_calculation="when_required", response_checksum_validation="when_required"))
    return _client

def status_of(ex):
    """HTTP status of a botocore error, or None for a network error (no answer at all)."""
    try: return int(ex.response["ResponseMetadata"]["HTTPStatusCode"])
    except Exception: return None

def call(what, fn):
    """Run one network call, tried up to four times: again after 2, 8 and 30 s on a network error or a 5xx answer. A 4xx answer
    (other than 404, which the callers read as "not there") is the request's own fault, so trying again cannot help."""
    for i in range(len(WAITS) + 1):
        try:
            return fn()
        except Exception as ex:
            st = status_of(ex)
            if st is not None and st < 500: raise
            if i == len(WAITS): raise R2Error(f"{what}: failed after {i + 1} tries ({type(ex).__name__}: {str(ex)[:300]})")
            log(f"{what}: try {i + 1} failed ({type(ex).__name__}, HTTP {st or 'no answer'}); again in {WAITS[i]} s")
            time.sleep(float(os.environ.get("R2_WAIT_SCALE", 1)) * WAITS[i])

def head(key):
    """(size, sha256) of the object at key, or None if there is none. sha256 is None for an object stored without it."""
    def h():
        try:
            r = client().head_object(Bucket=BUCKET, Key=key)
        except Exception as ex:
            if status_of(ex) == 404: return None
            raise
        return int(r["ContentLength"]), (r.get("Metadata") or {}).get("sha256")
    return call(f"HEAD {key}", h)

def read_back(key):
    """Size and SHA-256 of what R2 holds at key, computed from a full download read as a stream (8 MiB at a time)."""
    def rb():
        body = client().get_object(Bucket=BUCKET, Key=key)["Body"]; hh = hashlib.sha256(); n = 0
        for chunk in iter(lambda: body.read(1 << 23), b""): hh.update(chunk); n += len(chunk)
        return n, hh.hexdigest()
    return call(f"read back {key}", rb)

def put(local_path, key, sha256, size):
    """Store one file at key, never over a different object, and prove by reading it back that R2 holds exactly these bytes."""
    there = head(key)
    if there is not None:
        if there == (size, sha256):
            log(f"{key}: already stored ({size} bytes, same SHA-256)"); return "already stored"
        raise R2Error(f"{key}: R2 already holds a different object there ({there[0]} bytes, SHA-256 {there[1]}); "
                      f"a key is never overwritten (this file: {size} bytes, SHA-256 {sha256})")
    if os.path.getsize(local_path) != size: raise R2Error(f"{local_path}: {os.path.getsize(local_path)} bytes on disk, the index says {size}")
    from boto3.s3.transfer import TransferConfig
    cfg = TransferConfig(multipart_threshold=64 << 20, multipart_chunksize=64 << 20, max_concurrency=4)   # parts of 64 MiB for large files
    t0 = time.time()
    call(f"upload {key}", lambda: client().upload_file(local_path, BUCKET, key, ExtraArgs={"Metadata": {"sha256": sha256}}, Config=cfg))
    got = read_back(key)
    if got != (size, sha256):
        call(f"delete bad {key}", lambda: client().delete_object(Bucket=BUCKET, Key=key))
        raise R2Error(f"{key}: R2 holds {got[0]} bytes with SHA-256 {got[1]}, expected {size} bytes with {sha256}; the object was deleted")
    log(f"{key}: stored and read back, {size} bytes, SHA-256 matches ({round(time.time() - t0, 1)} s)")
    return "stored"

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "head": sys.exit("usage: python3 tools/sims/r2.py head <key>")
    try:
        h = head(sys.argv[2])
    except R2Error as ex:
        sys.exit(str(ex))
    if h is None: print(f"{sys.argv[2]}: not in {BUCKET}"); sys.exit(1)
    print(f"{sys.argv[2]}: {h[0]} bytes, sha256 {h[1]}")

if __name__ == "__main__":
    main()

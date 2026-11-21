"""Kaggelize, step 0: turn the titles typed into the Run form into a list of simulations.

Input: one string, titles separated by commas or new lines ("Wave Interference, Double Pendulum").
Output (printed, one line of JSON): [{"title": "Wave Interference", "slug": "wave_interference"}, ...]
The slug is the short name used for the model file tools/sims/<slug>.py, the registry entry, the branch and the report folder:
lower-case letters, digits and underscores, starting with a letter (it is imported as a Python module on Kaggle).

Usage: python3 tools/sims/agents/titles.py "<titles>"      Exit status 1 with a plain message when a title cannot be used."""
import json, re, sys, unicodedata

def slug(title):
    s = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    if s and s[0].isdigit(): s = "sim_" + s
    return s[:40].rstrip("_")

def parse(text):
    out, seen = [], set()
    for t in re.split(r"[,\n;]+", text):
        t = " ".join(t.split())
        if not t: continue
        if len(t) > 80 or not re.fullmatch(r"[\w .:'()&+\-–]+", t): raise ValueError(f"title not usable: {t!r} (letters, digits, spaces and . : ' ( ) & + - only, at most 80 characters)")
        s = slug(t)
        if len(s) < 2: raise ValueError(f"title gives no short name: {t!r}")
        if s in seen: raise ValueError(f"two titles give the same short name {s!r}")
        seen.add(s); out.append(dict(title=t, slug=s))
    if not out: raise ValueError("no title given")
    if len(out) > 12: raise ValueError("at most 12 simulations per run")
    return out

if __name__ == "__main__":
    try: print(json.dumps(parse(sys.argv[1] if len(sys.argv) > 1 else "")))
    except ValueError as e: sys.exit(str(e))

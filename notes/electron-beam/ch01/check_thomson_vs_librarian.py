"""Cross-check of data/ch01/thomson1897.json (S3, from Giunta's transcription) against S2's data/ch01/thomson1897_em.csv (from an OCR of another copy).
    python3 notes/electron-beam/ch01/check_thomson_vs_librarian.py     (reads S2's file from git: origin/eb/librarian)"""
import csv, io, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
mine = json.load(open(os.path.join(ROOT, 'portfolios-src/electron-beam/data/ch01/thomson1897.json')))
try:
    txt = subprocess.run(['git', 'show', 'origin/eb/librarian:portfolios-src/electron-beam/data/ch01/thomson1897_em.csv'], cwd=ROOT, capture_output=True, text=True, check=True).stdout
except Exception as e:
    print('S2 file not available:', e); sys.exit(0)
rows = list(csv.DictReader(io.StringIO(txt)))
t1 = [r for r in rows if r['table'].startswith('I ')]; t2 = [r for r in rows if r['table'].startswith('II')]
a = [r[4] * 1e7 for r in mine['method1_heat']['rows']]; b = [float(r['m_over_e_1e-7_g_per_emu']) for r in t1]
bad1 = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if abs(x - y) > 1e-9]
a2 = [r[6] * 1e7 for r in mine['method2_crossed']['rows']]; b2 = [(float(r['m_over_e_1e-7_g_per_emu']) if r['m_over_e_1e-7_g_per_emu'] else None) for r in t2]
bad2 = [(i, x, y) for i, (x, y) in enumerate(zip(a2, b2)) if y is not None and abs(x - y) > 1e-9]
print('table I: %d rows mine, %d rows S2, %d differ %s' % (len(a), len(b), len(bad1), bad1))
print('table II: %d rows mine, %d rows S2 (one m/e lost in S2 OCR), %d differ %s' % (len(a2), len(b2), len(bad2), bad2))

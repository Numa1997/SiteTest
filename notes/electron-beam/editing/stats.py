"""Sentence statistics of the prose of one or more chapter files (maths, markers and tags removed).
Usage: python3 notes/electron-beam/editing/stats.py portfolios-src/electron-beam/text/ch06.py [...]"""
import re, sys

def prose(src):
    s = re.sub(r'<svg.*?</svg>', ' ', src, flags=re.S)
    s = re.sub(r'‹E[^›]*›.*?‹/E›', ' ', s, flags=re.S)
    s = re.sub(r'‹[^›]*›', ' N ', s)
    s = re.sub(r"S\.append\(\(.*?r'''", '. ', s, flags=re.S)
    s = re.sub(r'\n\s*\d+(\.\d+)*\s+[A-Z][^\n.]{0,80}\n', '. ', s)
    s = re.sub(r'\$\$.*?\$\$|\\\[.*?\\\]', ' ', s, flags=re.S)
    s = re.sub(r'\$[^$]*\$|\\\(.*?\\\)', ' X ', s, flags=re.S)
    s = re.sub(r'\{\{[^}]*\}\}', ' N ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    paras = re.findall(r'<p[ >].*?</p>', src, flags=re.S)
    return s, len(paras)

for f in sys.argv[1:]:
    s, np_ = prose(open(f).read())
    sents = [x for x in re.split(r'(?<=[.!?])\s+(?=[A-Z])', s) if len(x.split()) >= 4 and "': '" not in x]
    lens = [len(x.split()) for x in sents]
    if not lens:
        continue
    print('%-45s sentences %4d  mean %5.1f  >30 %3d  >40 %3d  paragraphs %d' % (
        f, len(lens), sum(lens) / len(lens), sum(l > 30 for l in lens), sum(l > 40 for l in lens), np_))

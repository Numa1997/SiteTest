#!/usr/bin/env python3
"""Lists every numeral typed into the text of chapter 2 (written before the scaffold, so it has no CH["literals"]): the prose of SECTIONS with
its @key@ placeholders, maths and tags removed. Each line is a numeral a reader sees that no code computed; the audit (notes/electron-beam/AUDIT.md)
says for each kind why it may stay (a preset, a quoted source value, a counted thing) or was fixed.

    python3 portfolios-src/electron-beam/checks/list_legacy_numerals.py
"""
import html
import importlib.util
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('t2', HERE / 'text' / 'ch02.py')
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)
NUM = re.compile(r'(?<![\w.])\d[\d,]*(?:\.\d+)?(?![\w])')
n = 0
for label, title, body in T.SECTIONS:
    s = re.sub(r'@[^@\s]+@', ' ', title + ' ' + body)
    s = re.sub(r'\\\(.*?\\\)|\\\[.*?\\\]|\[\[(?:EQ|FIG)[^\]]*\]\].*?\[\[/(?:EQ|FIG)\]\]', ' ', s, flags=re.S)
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    for m in NUM.finditer(s):
        tok = m.group(0)
        if re.fullmatch(r'\d', tok) or (re.fullmatch(r'\d{4}', tok) and 1500 <= int(tok) <= 2099):
            continue
        n += 1
        print('%-22s %-8s ...%s...' % (label, tok, ' '.join(s[max(0, m.start() - 45):m.end() + 35].split())))
print('%d typed numerals in chapter 2' % n)

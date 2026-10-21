# Shifts the line links of docs/simulations/fig09-driven-oscillator.md after the note edit of 20 October 2026.
# Old -> new line map from difflib on the page (HEAD vs working tree): 1-319 same, 320 -> 320 (now 320-322),
# 321-445 -> +2, 446-448 (the three references) -> +2, 449-1111 -> +3. Run: python3 -I notes/fig09/shift_doc_links.py
import re, sys
P = '/home/user/SiteTest/docs/simulations/fig09-driven-oscillator.md'
def shift(n):
    if n <= 320: return n
    if n <= 448: return n + 2
    return n + 3
s = open(P, encoding='utf-8').read()
link = re.compile(r'\[([^\]]*)\]\((\.\./\.\./public/simulations/driven-oscillator\.html)#L(\d+)(?:-L(\d+))?\)')
changes = []
def fix(m):
    text, url, a, b = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    b = int(b) if b else None
    na, nb = shift(a), (shift(b) if b else None)
    nums = {a: na}
    if b: nums[b] = nb
    ntext = re.sub(r'\d+', lambda k: str(nums.get(int(k.group(0)), int(k.group(0)))), text)
    new = f'[{ntext}]({url}#L{na}' + (f'-L{nb}' if b else '') + ')'
    if new != m.group(0): changes.append((m.group(0), new))
    return new
s2 = link.sub(fix, s)
open(P, 'w', encoding='utf-8').write(s2)
print(len(changes), 'links shifted')
for o, n in changes[:5]: print(' ', o, '->', n)

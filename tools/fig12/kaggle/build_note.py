"""Fig. 12 note: fill the note's numbers from the numbers script and write the note into its page.

The note's source is notes/fig12/note/paper.html: the whole <article class="paper" id="paper"> of
public/simulations/guinness-kaggle.html, with every computed number written as {{name}} or {{name|format}} (a Python format
spec, e.g. {{swing_f0_Hz|.2f}}), name being an entry of tools/fig12/kaggle/note_numbers.py. This script replaces each one with
the number the script prints and puts the result in place of the page's article. No number of the note is typed in by hand:
after a new run, rerun note_numbers.py's sources and this script, and the note follows.
Run:  python3 tools/fig12/kaggle/build_note.py           write the page
      python3 tools/fig12/kaggle/build_note.py --check   only check that the page's article is the filled source (exit 1 if not)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import note_numbers as nn

ROOT = nn.ROOT
SRC = os.path.join(ROOT, "notes", "fig12", "note", "paper.html")
PAGE = os.path.join(ROOT, "public", "simulations", "guinness-kaggle.html")


def fill(text):
    def one(m):
        name, spec = m.group(1), m.group(2)
        if name not in nn.N: raise KeyError(f"{{{{{name}}}}} is not printed by note_numbers.py")
        v, s = nn.N[name]
        return format(v, spec) if spec else s
    return re.sub(r"\{\{([A-Za-z0-9_.]+)(?:\|([^}]*))?\}\}", one, text)


page = open(PAGE).read()
a = page.index('<article class="paper" id="paper"'); b = page.index("</article>", a) + len("</article>")
art = fill(open(SRC).read().strip())
if "--check" in sys.argv:
    ok = page[a:b] == art
    print("page article = filled source" if ok else "page article differs from the filled source"); sys.exit(0 if ok else 1)
open(PAGE, "w").write(page[:a] + art + page[b:])
print(f"wrote {PAGE}: {len(re.findall(r'{{', open(SRC).read()))} numbers filled")

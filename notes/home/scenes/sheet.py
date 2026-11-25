# Tile the two top corners of the filmed home page over time into one sheet. python3 notes/home/scenes/sheet.py <tag> <width> <t,t,...> <out.png>
import sys
from PIL import Image, ImageDraw
tag, w, ts, out = sys.argv[1], int(sys.argv[2]), sys.argv[3].split(','), sys.argv[4]
cw, ch = int(w * .28), 620
tiles = []
for t in ts:
    a = Image.open(f'notes/home/scenes/{tag}/{w}-t{t}.png'); b = Image.new('RGB', (2 * cw + 6, ch), 'white'); b.paste(a.crop((0, 0, cw, ch)), (0, 0)); b.paste(a.crop((w - cw, 0, w, ch)), (cw + 6, 0))
    ImageDraw.Draw(b).text((6, 4), f't = {t} s', fill=(122, 31, 43)); tiles.append(b)
cols = 2 if len(tiles) > 3 else 1; rows = (len(tiles) + cols - 1) // cols; W, H = tiles[0].size
s = Image.new('RGB', (cols * (W + 8), rows * (H + 8)), (200, 200, 200))
for i, b in enumerate(tiles): s.paste(b, ((i % cols) * (W + 8), (i // cols) * (H + 8)))
s.resize((s.size[0] * 2 // 3, s.size[1] * 2 // 3)).save(out)

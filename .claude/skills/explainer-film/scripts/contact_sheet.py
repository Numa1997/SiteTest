"""Lay the still frames of a film side by side, so every scene can be looked at in one picture.
Usage: contact_sheet.py STILLS_DIR OUT_PREFIX [frames per sheet, default 7]
Reads STILLS_DIR/c*.jpg (written by check_film.cjs) in order and writes OUT_PREFIX_1.jpg, OUT_PREFIX_2.jpg, ..."""
import glob
import sys
from PIL import Image

stills, prefix = sys.argv[1], sys.argv[2]
per = int(sys.argv[3]) if len(sys.argv) > 3 else 7
files = sorted(glob.glob(stills + '/c*.jpg'))
assert files, 'no stills in ' + stills
for k in range(0, len(files), per):
    ims = [Image.open(f) for f in files[k:k + per]]
    h = 760; ims = [im.resize((round(im.width * h / im.height), h)) for im in ims]
    sheet = Image.new('RGB', (sum(im.width for im in ims), h))
    x = 0
    for im in ims:
        sheet.paste(im, (x, 0)); x += im.width
    name = '%s_%d.jpg' % (prefix, k // per + 1); sheet.save(name, quality=86)
    print(name, 'frames', ' '.join(f.split('/c')[-1][:5].lstrip('0') or '0' for f in files[k:k + per]))

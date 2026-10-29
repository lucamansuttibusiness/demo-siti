"""Join two zoom captures of a tall image.
usage: python3 stitch.py out.png top.png bottom.png naturalWidth naturalHeight
top = capture with showCap(0); bottom = capture with showCap(naturalHeight-720)."""
import sys
from PIL import Image

out, a, b = sys.argv[1:4]
nw, nh = int(sys.argv[4]), int(sys.argv[5])
A = Image.open(a).convert('RGB'); B = Image.open(b).convert('RGB')
s = A.width / nw
Ht = round(nh * s)
im = Image.new('RGB', (A.width, Ht))
im.paste(B, (0, Ht - B.height))
im.paste(A.crop((0, 0, A.width, min(A.height, Ht - B.height + 40))), (0, 0))
im.save(out)
print(out, im.size)

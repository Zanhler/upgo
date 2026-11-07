# converte as fotos novas (HEIC do dev) para JPEG em raw/novas e monta uma folha para escolher
import glob, os
from PIL import Image, ImageDraw, ImageOps
import pillow_heif
pillow_heif.register_heif_opener()
D = os.path.expanduser("~/Downloads/")
O = "raw/novas/"; os.makedirs(O, exist_ok=True)
nomes = [f"IMG_{n}" for n in range(277, 285)]
nomes = [n.replace("IMG_", "IMG_0") for n in nomes]
W = 420; c = 4
s = Image.new("RGB", (c * W, 2 * (W + 20)), "white"); d = ImageDraw.Draw(s)
for i, n in enumerate(nomes):
    im = ImageOps.exif_transpose(Image.open(D + n + ".HEIC")).convert("RGB")
    print(n, im.size)
    im.save(O + n + ".jpg", quality=92)
    t = im.copy(); t.thumbnail((W, W)); x = (i % c) * W; y = (i // c) * (W + 20)
    s.paste(t, (x, y)); d.text((x + 3, y + W + 3), f"{n} {im.size}", fill="black")
s.save("raw/_sheet_novas.jpg", quality=85)

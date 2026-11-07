from PIL import Image
d = Image.open("raw/_mandala_crop.jpg"); d.crop((30, 70, d.width, d.height)).save("img/mandala.webp", quality=84)
Image.open("raw/ig/avatar.jpg").convert("RGB").crop((38, 8, 112, 82)).resize((64, 64), Image.LANCZOS).save("img/favicon.png")

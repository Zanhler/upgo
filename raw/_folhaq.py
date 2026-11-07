import glob, re
from PIL import Image
fs = sorted(glob.glob("raw/_q*.png"), key=lambda f: int(re.findall(r"\d+", f)[-1]))[:24]
s = Image.new("RGB", (4 * 300, ((len(fs) + 3) // 4) * 100), "white")
for i, f in enumerate(fs):
    s.paste(Image.open(f).convert("RGB").resize((300, 100)), ((i % 4) * 300, (i // 4) * 100))
s.save("raw/_quadros.jpg", quality=85); print(len(fs))

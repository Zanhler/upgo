import glob, os
from PIL import Image, ImageDraw
fs = sorted(glob.glob("img/*.webp")); W=240; c=7
s = Image.new("RGB",(c*W,((len(fs)+c-1)//c)*(W+16)),"white"); d = ImageDraw.Draw(s)
for i,f in enumerate(fs):
    t=Image.open(f).convert("RGB"); t.thumbnail((W,W)); x=(i%c)*W;y=(i//c)*(W+16); s.paste(t,(x,y)); d.text((x+3,y+W+1),os.path.basename(f),fill="black")
s.save("raw/_sheet_img.jpg",quality=84)

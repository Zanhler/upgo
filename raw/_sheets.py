import json, glob, os, cv2
from PIL import Image, ImageDraw
d = json.load(open('ig/_legendas.json', encoding='utf-8'))
with open('_leg.txt', 'w', encoding='utf-8') as f:
    for k, v in d.items(): f.write(k + ' ' + v + '\n\n')
def folha(fs, nome, W=230, c=8):
    s = Image.new('RGB', (c*W, ((len(fs)+c-1)//c)*(W+16)), 'white'); dr = ImageDraw.Draw(s)
    for i, f in enumerate(fs):
        t = Image.open(f).convert('RGB'); sz = t.size; t.thumbnail((W, W)); x = (i%c)*W; y = (i//c)*(W+16); s.paste(t, (x, y)); dr.text((x+3, y+W+1), os.path.basename(f)[:16]+' '+str(sz), fill='black')
    s.save(nome, quality=82)
folha(sorted(glob.glob('hi/*.jpg')), '_sheet_hi.jpg')
fr = []
for v in sorted(glob.glob('video/*.mp4')):
    c = cv2.VideoCapture(v); n = int(c.get(7)); fps = c.get(5); w = int(c.get(3)); h = int(c.get(4)); print(os.path.basename(v), w, h, round(n/fps,1), 's')
    nome = os.path.basename(v)[:-4]
    for j in range(4):
        c.set(1, int(n*(j+.5)/4)); ok, im = c.read()
        if ok: cv2.imwrite(f'video/{nome}_{j}.jpg', im); fr.append(f'video/{nome}_{j}.jpg')
folha(fr, '_sheet_vid.jpg', W=200, c=8)

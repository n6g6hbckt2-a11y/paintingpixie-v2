# -*- coding: utf-8 -*-
"""Face-centred crops of the Halloween photos for the new Halloween page (hw/): 4:5 for the cards, wide 1:1 for the photo line."""
from PIL import Image, ImageOps
UP = '/mnt/user-data/uploads/Painting Pixie Photos/Recommended for website/4 Halloween/'
C = [  # name, source, face centre x, y (fractions), crop width as fraction of photo width
 ('pumpkin', 'img/g/pumpkin-face-1600.webp', .42, .47, .86),
 ('skull-boy', 'img/g/skull-boy-1600.webp', .42, .47, .86),
 ('werewolf', 'img/g/werewolf-1600.webp', .48, .41, .52),
 ('princess', 'img/g/skeleton-crown-1600.webp', .47, .40, .68),
 ('devil-girl', 'img/g/red-devil-1600.webp', .50, .38, .72),
 ('half-skull', UP + 'C127-half-skull-boy.jpeg', .55, .48, .44),
 ('pumpkin-big-sister', 'img/g/pumpkin-sisters-1600.webp', .31, .27, .58),
 ('pumpkin-little-sister', 'img/g/pumpkin-sisters-1600.webp', .63, .52, .56),
 ('adult-skull', 'img/g/adult-skull-1600.webp', .50, .50, .95),
 ('monster', 'img/g/blue-monster-roar-1600.webp', .50, .42, .86),
]
for k, p, cx, cy, f in C:
    im = ImageOps.exif_transpose(Image.open(p)).convert('RGB'); W, H = im.size
    cw = f * W; ch = cw * 5 / 4
    if ch > H: ch = H; cw = ch * 4 / 5
    x0 = min(max(cx * W - cw / 2, 0), W - cw); y0 = min(max(cy * H - ch * .45, 0), H - ch)
    im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((880, 1100), Image.LANCZOS).save(f'hw/halloween-{k}.webp', 'WEBP', quality=82, method=6)
    # wide square version for the photo line: a little more around the face
    sw = min(f * 1.12 * W, W, H); x0 = min(max(cx * W - sw / 2, 0), W - sw); y0 = min(max(cy * H - sw * .45, 0), H - sw)
    im.crop((round(x0), round(y0), round(x0 + sw), round(y0 + sw))).resize((1000, 1000), Image.LANCZOS).save(f'hw/halloween-{k}-wide.webp', 'WEBP', quality=82, method=6)
print('crops done')

# tighter crops for the fright-level cards, where the photos are shown small
CARD = [
 ('pumpkin-little-sister', 'img/g/pumpkin-sisters-1600.webp', .64, .52, .44),
 ('princess', 'img/g/skeleton-crown-1600.webp', .47, .37, .42),
 ('skull-boy', 'img/g/skull-boy-1600.webp', .42, .46, .62),
 ('devil-girl', 'img/g/red-devil-1600.webp', .50, .43, .52),
 ('werewolf', 'img/g/werewolf-1600.webp', .48, .44, .38),
 ('adult-skull', 'img/g/adult-skull-1600.webp', .50, .50, .74),
]
for k, p, cx, cy, f in CARD:
    im = ImageOps.exif_transpose(Image.open(p)).convert('RGB'); W, H = im.size
    cw = f * W; ch = cw * 5 / 4
    x0 = min(max(cx * W - cw / 2, 0), W - cw); y0 = min(max(cy * H - ch * .48, 0), H - ch)
    im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((600, 750), Image.LANCZOS).save(f'hw/halloween-{k}-card.webp', 'WEBP', quality=82, method=6)
print('card crops done')

# heavily zoomed crops for the photo line at the top (3:4), the face fills the frame
ZOOM_CY = {'devil-girl': .47, 'werewolf': .45, 'pumpkin-big-sister': .20, 'skull-boy': .50, 'adult-skull': .47}
for k, p, cx, cy, f in C:
    cy = ZOOM_CY.get(k, cy)
    im = ImageOps.exif_transpose(Image.open(p)).convert('RGB'); W, H = im.size
    cw = f * .36 * W; ch = cw * 5 / 3
    x0 = min(max(cx * W - cw / 2, 0), W - cw); y0 = min(max(cy * H - ch * .47, 0), H - ch)
    im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((660, 1100), Image.LANCZOS).save(f'hw/halloween-{k}-zoom.webp', 'WEBP', quality=82, method=6)
print('zoom crops done')

"""High-resolution editorial illustrations for the three lead stories.

Each function draws at 3x with shading and then downsamples, so the panels stay
crisp in the final 1024px page. Only Pillow is used; nothing is downloaded.
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 3
F = 'C:/Windows/Fonts/'


def _font(size, bold=True, italic=False):
    name = 'georgiab.ttf' if bold and not italic else ('georgiai.ttf' if italic else 'arialbd.ttf' if bold else 'arial.ttf')
    try:
        return ImageFont.truetype(F + name, size * S)
    except OSError:
        return ImageFont.load_default()


def _finish(img, size):
    img = img.resize(size, Image.Resampling.LANCZOS)
    return img.filter(ImageFilter.UnsharpMask(radius=1, percent=90, threshold=2))


def _vgradient(w, h, top, bottom):
    img = Image.new('RGB', (w, h), top)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        d.line((0, y, w, y), fill=c)
    return img


def _flag(d, x, y, w, h, kind):
    d.rectangle((x - 2 * S, y - 2 * S, x + w + 2 * S, y + h + 2 * S), fill=(230, 224, 208))
    if kind == 'us':
        for i in range(7):
            d.rectangle((x, y + i * h / 7, x + w, y + (i + 1) * h / 7), fill=(188, 52, 46) if i % 2 == 0 else (246, 244, 236))
        d.rectangle((x, y, x + w * 0.45, y + h * 0.55), fill=(36, 58, 112))
        for i in range(9):
            d.point((x + 5 * S + (i % 3) * 8 * S, y + 5 * S + (i // 3) * 8 * S), fill=(248, 230, 150))
    elif kind == 'cn':
        d.rectangle((x, y, x + w, y + h), fill=(198, 40, 38))
        for i, px in enumerate((0.22, 0.42, 0.62, 0.8)):
            d.ellipse((x + px * w - 3 * S, y + h * 0.22 - 3 * S, x + px * w + 3 * S, y + h * 0.22 + 3 * S), fill=(248, 220, 90))
        d.ellipse((x + w * 0.3 - 5 * S, y + h * 0.58 - 5 * S, x + w * 0.3 + 5 * S, y + h * 0.58 + 5 * S), fill=(248, 220, 90))
    else:
        for i, c in enumerate(((246, 244, 236), (56, 74, 148), (198, 48, 44))):
            d.rectangle((x, y + i * h / 3, x + w, y + (i + 1) * h / 3), fill=c)
    d.line((x, y, x, y + h), fill=(60, 55, 50), width=2 * S)


def summit(size):
    w, h = size[0] * S, size[1] * S
    img = _vgradient(w, h, (62, 88, 124), (128, 140, 150))
    d = ImageDraw.Draw(img)
    # wall panelling
    for i in range(0, w, 70 * S):
        d.line((i, 6 * S, i, int(h * 0.62)), fill=(78, 102, 136), width=S)
    # flags
    _flag(d, int(w * 0.12), int(h * 0.12), int(w * 0.16), int(h * 0.3), 'us')
    _flag(d, int(w * 0.43), int(h * 0.08), int(w * 0.16), int(h * 0.32), 'cn')
    _flag(d, int(w * 0.74), int(h * 0.12), int(w * 0.16), int(h * 0.3), 'ru')
    # table
    d.ellipse((int(w * 0.08), int(h * 0.62), int(w * 0.92), int(h * 1.12)), fill=(70, 48, 38))
    d.ellipse((int(w * 0.1), int(h * 0.6), int(w * 0.9), int(h * 1.06)), fill=(126, 84, 56))
    d.ellipse((int(w * 0.16), int(h * 0.64), int(w * 0.84), int(h * 1.0)), fill=(150, 104, 70))
    # leaders
    for cx, suit, skin, hair in ((0.28, (40, 52, 74), (212, 168, 130), (58, 44, 36)),
                                 (0.5, (32, 38, 50), (220, 178, 142), (42, 34, 30)),
                                 (0.72, (58, 50, 62), (206, 162, 126), (70, 54, 44))):
        x, y = int(cx * w), int(h * 0.5)
        d.ellipse((x - 13 * S, y - 26 * S, x + 13 * S, y), fill=skin)
        d.ellipse((x - 14 * S, y - 30 * S, x + 14 * S, y - 12 * S), fill=hair)
        d.polygon([(x - 24 * S, y + 46 * S), (x - 20 * S, y + 4 * S), (x, y - 2 * S),
                   (x + 20 * S, y + 4 * S), (x + 24 * S, y + 46 * S)], fill=suit)
        d.polygon([(x - 6 * S, y + 4 * S), (x, y + 22 * S), (x + 6 * S, y + 4 * S)], fill=(238, 234, 222))
        d.line((x - 9 * S, y + 5 * S, x, y + 18 * S, x + 9 * S, y + 5 * S), fill=(150, 45, 42), width=2 * S)
    name_font = _font(7, bold=True)
    for cx, label in ((0.28, 'TRUMP'), (0.5, 'XI'), (0.72, 'PUTIN')):
        x = int(cx * w)
        tw = d.textbbox((0, 0), label, font=name_font)[2]
        d.rounded_rectangle((x - tw / 2 - 5 * S, int(h * 0.79), x + tw / 2 + 5 * S, int(h * 0.9)),
                            radius=2 * S, fill=(244, 238, 220), outline=(90, 84, 74))
        d.text((x - tw / 2, int(h * 0.8)), label, font=name_font, fill=(40, 36, 32))
    return _finish(img, size)


def court(size):
    w, h = size[0] * S, size[1] * S
    img = _vgradient(w, h, (206, 198, 178), (236, 228, 208))
    d = ImageDraw.Draw(img)
    # pediment and columns
    d.polygon([(int(w * 0.22), int(h * 0.3)), (int(w * 0.5), int(h * 0.05)), (int(w * 0.78), int(h * 0.3))],
              fill=(168, 152, 124), outline=(92, 82, 66))
    for i in range(5):
        x = int(w * (0.25 + i * 0.125))
        d.rectangle((x - 8 * S, int(h * 0.31), x + 8 * S, int(h * 0.78)), fill=(224, 214, 192), outline=(110, 98, 80))
        for k in range(3):
            d.line((x - 5 * S + k * 5 * S, int(h * 0.33), x - 5 * S + k * 5 * S, int(h * 0.76)), fill=(196, 184, 160))
    d.rectangle((int(w * 0.18), int(h * 0.78), int(w * 0.82), int(h * 0.9)), fill=(96, 72, 52))
    d.rectangle((int(w * 0.2), int(h * 0.76), int(w * 0.8), int(h * 0.8)), fill=(136, 104, 72))
    # scales of justice
    gold, shade = (214, 168, 62), (150, 112, 38)
    cx, cy = int(w * 0.5), int(h * 0.36)
    d.line((cx, cy - 8 * S, cx, cy + 34 * S), fill=shade, width=5 * S)
    d.line((cx - 46 * S, cy, cx + 46 * S, cy), fill=gold, width=5 * S)
    for px in (cx - 46 * S, cx + 46 * S):
        d.line((px, cy, px, cy + 22 * S), fill=shade, width=2 * S)
        d.arc((px - 18 * S, cy + 14 * S, px + 18 * S, cy + 38 * S), 0, 180, fill=gold, width=4 * S)
    d.ellipse((cx - 6 * S, cy - 6 * S, cx + 6 * S, cy + 6 * S), fill=gold)
    # vote plaque
    d.rounded_rectangle((int(w * 0.76), int(h * 0.52), int(w * 0.94), int(h * 0.72)), radius=4 * S,
                        fill=(176, 48, 42), outline=(110, 32, 28))
    d.text((int(w * 0.775), int(h * 0.55)), '9-6', font=_font(16), fill=(255, 248, 232))
    return _finish(img, size)


def climate(size):
    w, h = size[0] * S, size[1] * S
    img = _vgradient(w, h, (76, 128, 134), (140, 166, 156))
    d = ImageDraw.Draw(img)
    for yy in range(0, h, 14 * S):
        for xx in range(0, w, 14 * S):
            d.point((xx, yy), fill=(106, 150, 146))
    # globe
    gx, gy, r = int(w * 0.29), int(h * 0.48), int(h * 0.32)
    d.ellipse((gx - r, gy - r, gx + r, gy + r), fill=(46, 110, 138), outline=(24, 72, 100), width=2 * S)
    for pts in ([(gx - 20 * S, gy - 24 * S), (gx + 4 * S, gy - 30 * S), (gx + 16 * S, gy - 8 * S), (gx - 6 * S, gy)],
                [(gx - 28 * S, gy + 4 * S), (gx - 4 * S, gy + 2 * S), (gx + 10 * S, gy + 26 * S), (gx - 16 * S, gy + 30 * S)],
                [(gx + 12 * S, gy - 26 * S), (gx + 28 * S, gy - 12 * S), (gx + 22 * S, gy + 6 * S)]):
        d.polygon(pts, fill=(112, 158, 88))
    for k in (-1, 0, 1):
        d.arc((gx - r, gy + k * r * 0.45 - r * 0.25, gx + r, gy + k * r * 0.45 + r * 0.25), 10, 170, fill=(150, 190, 196), width=S)
    d.arc((gx - int(r * 0.45), gy - r, gx + int(r * 0.45), gy + r), 90, 270, fill=(150, 190, 196), width=S)
    # thermometer
    tx = int(w * 0.62)
    d.rounded_rectangle((tx - 7 * S, int(h * 0.16), tx + 7 * S, int(h * 0.78)), radius=6 * S,
                        fill=(244, 238, 220), outline=(70, 66, 60), width=2 * S)
    d.rounded_rectangle((tx - 4 * S, int(h * 0.42), tx + 4 * S, int(h * 0.72)), radius=3 * S, fill=(198, 52, 44))
    d.ellipse((tx - 13 * S, int(h * 0.68), tx + 13 * S, int(h * 0.9)), fill=(198, 52, 44))
    for i in range(5):
        yy = int(h * (0.24 + i * 0.1))
        d.line((tx + 8 * S, yy, tx + 14 * S, yy), fill=(70, 66, 60), width=S)
    # chimneys with crossed-out smoke
    for i in range(3):
        x = int(w * (0.76 + i * 0.07))
        d.rectangle((x, int(h * 0.52), x + 12 * S, int(h * 0.84)), fill=(108, 110, 112))
        d.ellipse((x + 1 * S, int(h * 0.45 + i * 3 * S), x + 20 * S, int(h * 0.56 + i * 3 * S)), fill=(178, 180, 176))
    d.line((int(w * 0.75), int(h * 0.42), int(w * 0.98), int(h * 0.6)), fill=(190, 48, 42), width=4 * S)
    d.line((int(w * 0.98), int(h * 0.42), int(w * 0.75), int(h * 0.6)), fill=(190, 48, 42), width=4 * S)
    return _finish(img, size)

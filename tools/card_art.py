"""Small shaded editorial illustrations for the ten story cards.

Drawn at 3x and downsampled, so each vignette stays crisp in the final page.
"""
from PIL import Image, ImageDraw, ImageFilter

S = 3


def _base(w, h, top, bottom):
    img = Image.new('RGB', (w, h), top)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line((0, y, w, y), fill=tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3)))
    return img, d


def _out(img, size):
    return img.resize(size, Image.Resampling.LANCZOS).filter(ImageFilter.UnsharpMask(1, 80, 2))


def bridge(size):
    w, h = size[0] * S, size[1] * S
    img, d = _base(w, h, (86, 106, 128), (44, 66, 92))
    d.rectangle((0, int(h * 0.62), w, h), fill=(48, 78, 104))
    d.line((0, int(h * 0.62), w, int(h * 0.62)), fill=(190, 196, 188), width=2 * S)
    for i in range(5):
        x = int(w * (0.1 + i * 0.2))
        d.line((x, int(h * 0.2), x, int(h * 0.62)), fill=(170, 176, 172), width=2 * S)
        d.line((x, int(h * 0.2), x + int(w * 0.1), int(h * 0.62)), fill=(150, 158, 154))
    d.line((0, int(h * 0.42), w, int(h * 0.42)), fill=(210, 214, 206), width=3 * S)
    d.polygon([(int(w * 0.44), int(h * 0.4)), (int(w * 0.56), int(h * 0.42)),
               (int(w * 0.52), int(h * 0.6)), (int(w * 0.4), int(h * 0.56))], fill=(198, 58, 48))
    d.ellipse((int(w * 0.46), int(h * 0.44), int(w * 0.58), int(h * 0.62)), fill=(238, 176, 72))
    return _out(img, size)


def tower(size):
    w, h = size[0] * S, size[1] * S
    img, d = _base(w, h, (206, 196, 174), (236, 228, 208))
    d.rectangle((int(w * 0.42), int(h * 0.08), int(w * 0.6), h), fill=(86, 104, 126))
    for yy in range(int(h * 0.12), h, 4 * S):
        d.line((int(w * 0.45), yy, int(w * 0.57), yy), fill=(196, 208, 218), width=S)
    d.polygon([(int(w * 0.4), int(h * 0.1)), (int(w * 0.62), int(h * 0.1)), (int(w * 0.51), 0)], fill=(120, 138, 156))
    d.ellipse((int(w * 0.52), int(h * 0.2), int(w * 0.78), int(h * 0.46)), fill=(220, 178, 96))
    d.ellipse((int(w * 0.55), int(h * 0.24), int(w * 0.74), int(h * 0.42)), fill=(236, 96, 62))
    d.ellipse((int(w * 0.62), int(h * 0.3), int(w * 0.7), int(h * 0.38)), fill=(250, 220, 140))
    return _out(img, size)


def cyclone(size):
    w, h = size[0] * S, size[1] * S
    img, d = _base(w, h, (120, 160, 178), (196, 214, 206))
    d.polygon([(0, int(h * 0.8)), (int(w * 0.3), int(h * 0.7)), (w, int(h * 0.86)), (w, h), (0, h)], fill=(124, 150, 96))
    for r in (26, 18, 10):
        d.arc((int(w * 0.46 - r * S), int(h * 0.46 - r * S), int(w * 0.46 + r * S), int(h * 0.46 + r * S)),
              20, 300, fill=(44, 92, 140), width=3 * S)
    d.ellipse((int(w * 0.42), int(h * 0.42), int(w * 0.5), int(h * 0.5)), fill=(206, 56, 48))
    d.ellipse((int(w * 0.84), int(h * 0.06), int(w * 0.96), int(h * 0.22)), fill=(206, 56, 48))
    return _out(img, size)


def exam(size):
    w, h = size[0] * S, size[1] * S
    img, d = _base(w, h, (232, 224, 202), (206, 196, 174))
    for i in range(4):
        x = int(w * (0.08 + i * 0.24))
        d.ellipse((x - 5 * S, int(h * 0.22), x + 5 * S, int(h * 0.42)), fill=(190, 152, 118))
        d.rectangle((x - 9 * S, int(h * 0.42), x + 9 * S, int(h * 0.72)), fill=(70, 84, 108))
        d.rectangle((x - 7 * S, int(h * 0.6), x + 7 * S, int(h * 0.74)), fill=(246, 242, 228))
    d.rectangle((0, int(h * 0.76), w, h), fill=(138, 112, 78))
    return _out(img, size)


def flags(size):
    w, h = size[0] * S, size[1] * S
    img, d = _base(w, h, (222, 214, 194), (240, 234, 216))
    for i, colors in enumerate((((188, 52, 46), (246, 244, 236), (36, 58, 112)),
                                ((198, 40, 38),), ((246, 244, 236), (56, 74, 148), (198, 48, 44)))):
        x = int(w * (0.12 + i * 0.3))
        d.line((x, int(h * 0.15), x, h), fill=(80, 74, 66), width=2 * S)
        fw, fh = int(w * 0.22), int(h * 0.34)
        for k, c in enumerate(colors):
            d.rectangle((x, int(h * 0.17 + k * fh / len(colors)), x + fw, int(h * 0.17 + (k + 1) * fh / len(colors))), fill=c)
    return _out(img, size)


def chart(size):
    w, h = size[0] * S, size[1] * S
    img, d = _base(w, h, (232, 228, 214), (244, 240, 226))
    d.line((4 * S, int(h * 0.88), w - 4 * S, int(h * 0.88)), fill=(110, 104, 94), width=S)
    for i, hh in enumerate((7, 11, 15, 21)):
        x = int(w * (0.12 + i * 0.2))
        d.rectangle((x, int(h * 0.88 - hh * S), x + int(w * 0.12), int(h * 0.88)), fill=(62, 142, 96))
        d.rectangle((x, int(h * 0.88 - hh * S), x + int(w * 0.05), int(h * 0.88)), fill=(96, 178, 124))
    d.line((int(w * 0.1), int(h * 0.5), int(w * 0.88), int(h * 0.12)), fill=(40, 40, 40), width=2 * S)
    d.polygon([(int(w * 0.9), int(h * 0.1)), (int(w * 0.78), int(h * 0.12)), (int(w * 0.86), int(h * 0.22))], fill=(40, 40, 40))
    return _out(img, size)


def game(size):
    w, h = size[0] * S, size[1] * S
    img, d = _base(w, h, (96, 72, 126), (60, 46, 92))
    d.rounded_rectangle((int(w * 0.12), int(h * 0.12), int(w * 0.88), int(h * 0.9)), radius=7 * S,
                        fill=(62, 54, 82), outline=(206, 196, 224), width=2 * S)
    d.line((int(w * 0.26), int(h * 0.35), int(w * 0.26), int(h * 0.67)), fill=(232, 226, 240), width=3 * S)
    d.line((int(w * 0.19), int(h * 0.51), int(w * 0.33), int(h * 0.51)), fill=(232, 226, 240), width=3 * S)
    d.ellipse((int(w * 0.68), int(h * 0.3), int(w * 0.78), int(h * 0.44)), fill=(214, 74, 70))
    d.ellipse((int(w * 0.8), int(h * 0.48), int(w * 0.88), int(h * 0.6)), fill=(226, 190, 84))
    return _out(img, size)


def strike(size):
    w, h = size[0] * S, size[1] * S
    img, d = _base(w, h, (226, 218, 198), (240, 234, 218))
    for i in range(6):
        x = int(w * (0.08 + i * 0.16))
        d.ellipse((x - 3 * S, int(h * 0.34), x + 3 * S, int(h * 0.46)), fill=(150 + i * 8, 120, 92))
        d.rectangle((x - 5 * S, int(h * 0.46), x + 5 * S, int(h * 0.86)), fill=(58 + i * 12, 74, 96))
        if i % 2 == 0:
            d.line((x + 4 * S, int(h * 0.5), x + 4 * S, int(h * 0.76)), fill=(80, 72, 62), width=S)
            d.rectangle((x + 2 * S, int(h * 0.38), x + 14 * S, int(h * 0.54)), fill=(240, 236, 222), outline=(130, 122, 108))
    return _out(img, size)


def chart_down(size):
    w, h = size[0] * S, size[1] * S
    img, d = _base(w, h, (236, 230, 216), (218, 210, 194))
    d.line((4 * S, int(h * 0.16), 4 * S, int(h * 0.9)), fill=(110, 104, 94), width=S)
    d.line((4 * S, int(h * 0.88), w - 4 * S, int(h * 0.88)), fill=(110, 104, 94), width=S)
    pts = [(int(w * (0.1 + i * 0.14)), int(h * (0.28 + i * 0.11))) for i in range(6)]
    d.line(pts, fill=(190, 56, 48), width=3 * S)
    d.polygon([pts[-1], (pts[-1][0] - 10 * S, pts[-1][1] - 2 * S), (pts[-1][0] - 3 * S, pts[-1][1] - 9 * S)], fill=(190, 56, 48))
    return _out(img, size)


def art(size):
    w, h = size[0] * S, size[1] * S
    img, d = _base(w, h, (216, 206, 180), (238, 230, 208))
    d.rectangle((int(w * 0.12), int(h * 0.06), int(w * 0.88), int(h * 0.94)), fill=(250, 246, 228), outline=(110, 92, 60), width=3 * S)
    d.line((int(w * 0.22), int(h * 0.78), int(w * 0.78), int(h * 0.78)), fill=(124, 142, 92), width=2 * S)
    d.line((int(w * 0.5), int(h * 0.78), int(w * 0.48), int(h * 0.34)), fill=(112, 88, 58), width=3 * S)
    for cx, cy in ((0.36, 0.4), (0.6, 0.34), (0.7, 0.52), (0.3, 0.58)):
        d.ellipse((int(w * (cx - 0.09)), int(h * (cy - 0.08)), int(w * (cx + 0.09)), int(h * (cy + 0.08))),
                  fill=(226, 186, 92))
    return _out(img, size)


MAP = {
    'bridge': bridge, 'tower': tower, 'cyclone': cyclone, 'exam': exam,
    'flag': flags, 'chart': chart, 'game': game, 'strike': strike,
    'chart_down': chart_down, 'art': art,
}


def make(kind, size):
    return MAP[kind](size)

"""Draw a one-image summary of the world news of Thursday, 19 November 2026.

Run locally with Pillow to produce news.png. The grader never runs this file: the
repository commits the PNG it produces and main.py copies it to /output/entry.png.
All artwork is drawn from shapes and text here, so the image is deterministic.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (11, 16, 32)
PANEL = (20, 29, 51)
WHITE = (247, 249, 252)
MUTED = (166, 180, 204)
GOLD = (245, 196, 81)
CYAN = (77, 214, 231)
CORAL = (255, 107, 107)
GREEN = (90, 209, 154)
PURPLE = (167, 139, 250)

FONTS = "C:/Windows/Fonts/"
REG = FONTS + "arial.ttf"
BOLD = FONTS + "arialbd.ttf"


def font(size, bold=False):
    path = BOLD if bold else REG
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def text(d, xy, s, size, fill, bold=False, max_w=None):
    f = font(size, bold)
    while max_w and d.textbbox((0, 0), s, font=f)[2] > max_w and size > 10:
        size -= 1
        f = font(size, bold)
    d.text(xy, s, font=f, fill=fill)


def rounded(d, box, fill, radius=18, outline=None, width=2):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def head(d, cx, cy, color, scale=1.0):
    r = int(15 * scale)
    d.ellipse((cx - r, cy - int(30 * scale), cx + r, cy), fill=color)
    d.ellipse((cx - int(26 * scale), cy + int(3 * scale), cx + int(26 * scale), cy + int(33 * scale)), fill=color)


def card(d, x, y, w, h, accent, kicker, title, detail, icon):
    rounded(d, (x, y, x + w, y + h), PANEL)
    d.rectangle((x, y + 16, x + 8, y + h - 16), fill=accent)
    text(d, (x + 28, y + 18), kicker.upper(), 17, accent, True, max_w=w - 60)
    text(d, (x + 28, y + 48), title, 31, WHITE, True, max_w=w - 135)
    text(d, (x + 28, y + h - 46), detail, 19, MUTED, False, max_w=w - 60)
    ix, iy = x + w - 60, y + h // 2
    if icon == "summit":
        head(d, ix - 30, iy + 8, GOLD, 0.75)
        head(d, ix, iy - 2, CYAN, 0.9)
        head(d, ix + 30, iy + 8, WHITE, 0.75)
    elif icon == "scales":
        d.line((ix, iy - 30, ix, iy + 30), fill=GOLD, width=5)
        d.line((ix - 34, iy - 18, ix + 34, iy - 18), fill=GOLD, width=5)
        for s in (-1, 1):
            px = ix + s * 34
            d.line((px, iy - 18, px, iy + 12), fill=GOLD, width=3)
            d.arc((px - 18, iy + 6, px + 18, iy + 34), 0, 180, fill=GOLD, width=4)
    elif icon == "chart":
        for i, hh in enumerate((14, 24, 34, 46)):
            d.rectangle((ix - 33 + i * 17, iy + 26 - hh, ix - 22 + i * 17, iy + 26), fill=GREEN)
        d.line((ix - 36, iy - 30, ix + 26, iy - 30), fill=WHITE, width=3)
        d.polygon([(ix + 26, iy - 30), (ix + 12, iy - 38), (ix + 12, iy - 22)], fill=WHITE)
    elif icon == "shield":
        d.polygon([(ix, iy - 34), (ix + 28, iy - 22), (ix + 24, iy + 12), (ix, iy + 34), (ix - 24, iy + 12), (ix - 28, iy - 22)], outline=CYAN, width=4)
        d.line((ix - 12, iy + 1, ix - 3, iy + 11, ix + 13, iy - 11), fill=CYAN, width=5)
    elif icon == "pad":
        rounded(d, (ix - 34, iy - 18, ix + 34, iy + 22), (40, 52, 82), 14, PURPLE, 3)
        d.line((ix - 22, iy - 7, ix - 22, iy + 13), fill=PURPLE, width=4)
        d.line((ix - 32, iy + 3, ix - 12, iy + 3), fill=PURPLE, width=4)
        for dx, dy, c in ((16, -6, CORAL), (25, 4, GOLD)):
            d.ellipse((ix + dx - 4, iy + dy - 4, ix + dx + 4, iy + dy + 4), fill=c)
    elif icon == "gavel":
        d.rectangle((ix - 26, iy - 32, ix + 26, iy - 18), fill=CORAL)
        d.line((ix, iy - 18, ix - 18, iy + 24), fill=CORAL, width=7)
        d.rounded_rectangle((ix - 34, iy + 24, ix + 6, iy + 34), radius=4, fill=CORAL)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # fine dotted texture
    for yy in range(0, H, 34):
        for xx in range(0, W, 34):
            d.point((xx, yy), fill=(24, 34, 58))

    # masthead
    d.rectangle((0, 0, W, 8), fill=GOLD)
    text(d, (48, 34), "THE WORLD IN ONE IMAGE", 22, CYAN, True)
    text(d, (44, 64), "19 NOVEMBER 2026", 76, WHITE, True, max_w=940)
    text(d, (48, 151), "Thursday - the day's world news", 24, MUTED)
    d.line((48, 190, 976, 190), fill=(55, 70, 100), width=2)

    col_w = 452
    xs = (48, 524)
    ys = (206, 424, 642)
    h = 202

    card(d, xs[0], ys[0], col_w, h, GOLD, "Diplomacy",
         "TRUMP - XI - PUTIN", "First-ever trilateral summit; nuclear-arms pledge", "summit")
    card(d, xs[1], ys[0], col_w, h, CYAN, "Justice",
         "MYANMAR GENOCIDE RULING", "World court's first such ruling; Rohingya", "scales")
    card(d, xs[0], ys[1], col_w, h, GREEN, "Markets",
         "ANTHROPIC IPO", "Record $107bn debut, shares +17%", "chart")
    card(d, xs[1], ys[1], col_w, h, PURPLE, "Ukraine",
         "NATO-STYLE GUARANTEE", "Trump open to Article 5-like defence", "shield")
    card(d, xs[0], ys[2], col_w, h, CORAL, "Iran",
         "IRAN WAR POWERS BLOCKED", "Republicans reject war-powers resolution", "gavel")
    card(d, xs[1], ys[2], col_w, h, GOLD, "Culture",
         "GTA VI LAUNCHES", "Around $2bn on day one; biggest ever", "pad")

    # footer ticker
    rounded(d, (48, 864, 976, 986), (17, 25, 45))
    text(d, (72, 884), "ALSO IN THE NEWS", 17, CYAN, True)
    text(d, (72, 912), "UN secretary-general race stalls  -  International Men's Day", 22, WHITE, True, max_w=880)
    text(d, (72, 946), "One day. One image. 19 November 2026.", 18, MUTED)

    img.save("news.png", optimize=True)
    print("wrote news.png", img.size)


if __name__ == "__main__":
    main()

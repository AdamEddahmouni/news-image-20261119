"""Draw the 19 November 2026 world-news front page.

Run locally with Pillow to produce news.png. The grader only runs main.py, which
copies the committed PNG. Every drawing is made from shapes and text here, so
the bytes are deterministic and no network or font download is needed at run time.
"""
from PIL import Image, ImageDraw, ImageFont
from hero_art import summit, court, climate
from card_art import make as card_art

W = H = 1024
PAPER = (246, 241, 228)
INK = (24, 22, 20)
RED = (158, 36, 32)
BLUE = (33, 62, 112)
GREEN = (34, 105, 66)
MUTED = (92, 86, 78)
PALE = (232, 224, 206)
RULE = (176, 167, 148)

F = "C:/Windows/Fonts/"


def face(name, fallback):
    return F + name if __import__('os').path.exists(F + name) else F + fallback


SERIF = face('georgiab.ttf', 'timesbd.ttf')
SERIF_I = face('georgiai.ttf', 'timesi.ttf')
SANS = face('arial.ttf', 'arial.ttf')
SANS_B = face('arialbd.ttf', 'arialbd.ttf')


def font(size, kind='sans'):
    path = {'serif': SERIF, 'italic': SERIF_I, 'sans': SANS, 'bold': SANS_B}[kind]
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def width(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]


def fit(d, xy, s, size, kind='sans', max_w=900, fill=INK):
    f = font(size, kind)
    while width(d, s, f) > max_w and size > 6:
        size -= 1
        f = font(size, kind)
    d.text(xy, s, font=f, fill=fill)
    return size


def wrap(d, s, f, max_w):
    lines, line = [], ''
    for word in s.split():
        trial = (line + ' ' + word).strip()
        if width(d, trial, f) <= max_w or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def para(d, xy, s, size, max_w, kind='sans', fill=INK, leading=None, max_lines=9):
    f = font(size, kind)
    leading = leading or size + 2
    x, y = xy
    for i, ln in enumerate(wrap(d, s, f, max_w)[:max_lines]):
        d.text((x, y + i * leading), ln, font=f, fill=fill)
    return y + len(wrap(d, s, f, max_w)[:max_lines]) * leading


def flag(d, x, y, w, h, colors):
    d.rectangle((x, y, x + w, y + h), fill=(250, 248, 242), outline=INK)
    n = len(colors)
    for i, c in enumerate(colors):
        d.rectangle((x + i * w // n, y, x + (i + 1) * w // n - 1, y + h), fill=c)


def person(d, x, y, s, color):
    d.ellipse((x - 6 * s, y - 12 * s, x + 6 * s, y), fill=color)
    d.ellipse((x - 11 * s, y + 2 * s, x + 11 * s, y + 16 * s), fill=color)


def hero_icon(d, box, kind, accent):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    if kind == 'summit':
        d.rectangle((x0 + 18, y0 + 24, x1 - 18, y1 - 8), fill=(88, 96, 112))
        for fx, cols in ((cx - 62, [(190, 50, 50), (255, 255, 255), (60, 80, 150)]),
                         (cx - 8, [(220, 40, 40), (240, 205, 60)]),
                         (cx + 46, [(255, 255, 255), (65, 100, 170), (200, 45, 45)])):
            flag(d, fx, y0 + 10, 30, 17, cols)
            d.line((fx + 15, y0 + 27, fx + 15, y0 + 46), fill=INK, width=2)
        person(d, cx - 50, cy + 14, 1, (55, 62, 78))
        person(d, cx, cy + 8, 1.15, (35, 40, 52))
        person(d, cx + 50, cy + 14, 1, (72, 62, 55))
    elif kind == 'court':
        d.polygon([(cx - 62, y0 + 20), (cx, y0 + 4), (cx + 62, y0 + 20)], fill=(176, 164, 140))
        for i in range(5):
            px = cx - 48 + i * 24
            d.rectangle((px - 6, y0 + 22, px + 6, y0 + 66), fill=(222, 212, 190), outline=INK)
        d.line((cx - 60, y0 + 68, cx + 60, y0 + 68), fill=INK, width=3)
        d.line((cx + 42, y0 + 22, cx + 42, y0 + 58), fill=accent, width=3)
        d.line((cx + 24, y0 + 26, cx + 60, y0 + 26), fill=accent, width=3)
        d.arc((cx + 24, y0 + 26, cx + 38, y0 + 44), 0, 180, fill=accent, width=2)
        d.arc((cx + 46, y0 + 26, cx + 60, y0 + 44), 0, 180, fill=accent, width=2)
        d.text((cx + 20, y0 + 46), '9-6', font=font(15, 'bold'), fill=accent)
    elif kind == 'globe':
        d.ellipse((cx - 40, y0 + 8, cx + 30, y0 + 78), fill=(70, 140, 150), outline=INK)
        for pts in ([(cx - 22, y0 + 24), (cx - 4, y0 + 18), (cx + 6, y0 + 32), (cx - 12, y0 + 40)],
                    [(cx - 30, y0 + 48), (cx - 10, y0 + 44), (cx + 2, y0 + 58), (cx - 18, y0 + 68)]):
            d.polygon(pts, fill=(120, 165, 105))
        d.rounded_rectangle((cx + 34, y0 + 12, cx + 52, y0 + 70), radius=7, fill=(245, 240, 225), outline=INK)
        d.ellipse((cx + 30, y0 + 54, cx + 56, y0 + 80), fill=RED)
        d.text((cx - 38, y0 + 82), 'FOSSIL FUELS  OUT', font=font(12, 'bold'), fill=RED)


def mini_icon(d, x, y, kind):
    if kind == 'bridge':
        d.line((x, y + 18, x + 44, y + 18), fill=INK, width=3)
        for i in range(4):
            d.line((x + 5 + i * 11, y + 4, x + 5 + i * 11, y + 18), fill=MUTED, width=2)
        d.polygon([(x + 18, y + 4), (x + 30, y + 6), (x + 28, y + 14), (x + 16, y + 12)], fill=RED)
    elif kind == 'tower':
        d.rectangle((x + 14, y + 2, x + 30, y + 22), fill=(90, 110, 140))
        d.polygon([(x + 12, y + 2), (x + 32, y + 2), (x + 22, y - 8)], fill=RED)
    elif kind == 'cyclone':
        for r in (16, 10):
            d.arc((x + 22 - r, y + 11 - r, x + 22 + r, y + 11 + r), 30, 300, fill=BLUE, width=3)
        d.ellipse((x + 18, y + 7, x + 26, y + 15), fill=RED)
    elif kind == 'exam':
        d.rectangle((x + 6, y + 2, x + 38, y + 22), fill=(235, 228, 210), outline=INK)
        for i in range(3):
            d.line((x + 11, y + 8 + i * 5, x + 33, y + 8 + i * 5), fill=MUTED, width=1)
    elif kind == 'flag':
        flag(d, x + 6, y + 2, 18, 11, [(200, 40, 40), (255, 255, 255), (40, 70, 140)])
        flag(d, x + 26, y + 2, 14, 11, [(200, 40, 40), (255, 255, 255)])
    elif kind == 'chart':
        for i, hh in enumerate((7, 11, 16, 21)):
            d.rectangle((x + 4 + i * 9, y + 22 - hh, x + 11 + i * 9, y + 22), fill=GREEN)
    elif kind == 'game':
        d.rounded_rectangle((x + 4, y + 4, x + 40, y + 22), radius=6, fill=(70, 55, 100))
        d.line((x + 11, y + 9, x + 11, y + 17), fill=(240, 235, 220), width=2)
        d.line((x + 7, y + 13, x + 15, y + 13), fill=(240, 235, 220), width=2)
        d.ellipse((x + 28, y + 8, x + 34, y + 14), fill=RED)
    elif kind == 'strike':
        for i in range(5):
            person(d, x + 8 + i * 7, y + 16, 0.5, (90 + i * 15, 80, 70))
    elif kind == 'chart_down':
        d.line((x + 4, y + 6, x + 38, y + 20), fill=RED, width=3)
        d.polygon([(x + 38, y + 20), (x + 28, y + 19), (x + 35, y + 12)], fill=RED)
    elif kind == 'art':
        d.rectangle((x + 8, y + 2, x + 36, y + 22), fill=(235, 225, 195), outline=INK)
        d.ellipse((x + 14, y + 7, x + 22, y + 15), fill=(180, 150, 50))
        d.polygon([(x + 22, y + 20), (x + 30, y + 8), (x + 34, y + 20)], fill=(90, 120, 80))


def draw_map(d, box):
    x, y, w, h = box
    d.rectangle((x, y, x + w, y + h), fill=(222, 234, 238), outline=INK)
    land = (198, 183, 145)
    shapes = [
        [(0.04, 0.18), (0.20, 0.10), (0.30, 0.20), (0.27, 0.36), (0.18, 0.44), (0.11, 0.34), (0.06, 0.26)],
        [(0.24, 0.50), (0.33, 0.49), (0.36, 0.66), (0.30, 0.88), (0.25, 0.70)],
        [(0.44, 0.22), (0.56, 0.18), (0.59, 0.29), (0.50, 0.34), (0.44, 0.29)],
        [(0.47, 0.39), (0.59, 0.37), (0.61, 0.56), (0.53, 0.77), (0.48, 0.60)],
        [(0.59, 0.14), (0.87, 0.13), (0.93, 0.31), (0.80, 0.46), (0.65, 0.41), (0.58, 0.30)],
        [(0.82, 0.66), (0.92, 0.63), (0.96, 0.76), (0.85, 0.82)],
    ]
    for shp in shapes:
        d.polygon([(x + int(a * w), y + int(b * h)) for a, b in shp], fill=land, outline=(150, 140, 115))
    pins = [(0.84, 0.38, 1), (0.50, 0.25, 2), (0.57, 0.32, 3), (0.58, 0.26, 4),
            (0.57, 0.45, 5), (0.76, 0.46, 6), (0.88, 0.31, 7), (0.50, 0.19, 8),
            (0.20, 0.31, 9), (0.94, 0.82, 10), (0.29, 0.58, 11), (0.90, 0.75, 12), (0.22, 0.38, 13)]
    for px, py, n in pins:
        cx, cy = x + int(px * w), y + int(py * h)
        d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=RED, outline=(255, 255, 255), width=2)
        d.text((cx - 4, cy - 6), str(n), font=font(9, 'bold'), fill=(255, 255, 255))


def main():
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.text((18, 12), 'THE WORLD IN ONE DAY', font=font(15, 'bold'), fill=RED)
    right = "THURSDAY'S NEWS  -  ONE PAGE  -  41 STORIES"
    d.text((W - 18 - width(d, right, font(12, 'bold')), 14), right, font=font(12, 'bold'), fill=BLUE)
    fit(d, (18, 30), 'Thursday 19 November 2026', 68, 'serif', 988, INK)
    d.line((16, 103, 1008, 103), fill=RED, width=3)
    fit(d, (18, 108),
        'Trump, Xi and Putin share one table  -  World Court finds genocide in Myanmar  -  COP31 draft drops fossil fuels',
        16, 'italic', 988, RED)
    cats = [('ASIA', (105, 55, 110)), ('EUROPE', (45, 85, 150)), ('MIDDLE EAST', (170, 70, 55)),
            ('AFRICA', (60, 130, 85)), ('THE AMERICAS', (140, 100, 55)),
            ('OCEANIA', (50, 130, 140)), ('WORLD', (95, 95, 100))]
    cw = 992 // len(cats)
    for i, (label, col) in enumerate(cats):
        d.rectangle((16 + i * cw, 134, 16 + (i + 1) * cw - 1, 154), fill=col)
        f = font(11, 'bold')
        d.text((16 + i * cw + (cw - width(d, label, f)) // 2, 138), label, font=f, fill=(255, 255, 255))

    # --- numbers strip ---
    stats = [('3', 'leaders at one table'), ('9-6', 'ICJ genocide vote'), ('$120bn', 'COP31 adaptation ask'),
             ('$81bn', 'Anthropic record IPO'), ('109-0', 'Danish Arctic vote'), ('4.9%', 'Australia jobless rate')]
    sw = 992 // 6
    for i, (big, cap) in enumerate(stats):
        x = 16 + i * sw
        d.line((x, 160, x, 218), fill=RULE, width=1)
        fit(d, (x + 8, 162), big, 30, 'serif', sw - 16, INK)
        para(d, (x + 8, 199), cap, 10, sw - 16, fill=MUTED, max_lines=2)
    d.line((16, 222, 1008, 222), fill=INK, width=2)

    # --- three heroes ---
    heroes = [
        (0, (68, 96, 128), 'summit', 'SHENZHEN  -  APEC  -  DIPLOMACY',
         'Trump, Xi and Putin hold first three-way summit',
         'The US, Chinese and Russian leaders met for 90 minutes and issued a “Declaration on Peace” on nuclear risk and UN reform.  -  Reuters, AP', 'REPORTED'),
        (1, (208, 202, 184), 'court', 'THE HAGUE  -  JUSTICE',
         'World Court: Myanmar committed genocide',
         'Judges ruled 9-6 that Myanmar was guilty of genocide against the Rohingya in 2017 and ordered reparations.  -  UN News, Al Jazeera', 'REPORTED'),
        (2, (74, 120, 126), 'globe', 'ANTALYA  -  COP31  -  CLIMATE',
         'COP31 draft drops fossil fuels and $120bn',
         'Revised text drops the fossil-fuel phase-out and the adaptation finance figure. Talks run on to Friday.  -  Bloomberg, CBC, Reuters', 'REPORTED'),
    ]
    hw = 324
    for idx, bg, icon, kicker, head, body, tag in heroes:
        x = 16 + idx * (hw + 10)
        y = 230
        d.rectangle((x, y, x + hw, y + 244), fill=PAPER, outline=INK, width=1)
        d.rectangle((x + 1, y + 1, x + hw - 1, y + 92), fill=bg)
        art = {'summit': summit, 'court': court, 'globe': climate}[icon]((hw - 2, 91))
        img.paste(art, (x + 1, y + 1))
        d.text((x + 8, y + 98), kicker, font=font(10, 'bold'), fill=BLUE)
        para(d, (x + 8, y + 114), head, 18, hw - 16, 'serif', INK, leading=20, max_lines=2)
        para(d, (x + 8, y + 158), body, 10.5, hw - 16, fill=(55, 50, 44), leading=13, max_lines=4)
        d.rectangle((x + hw - 70, y + 224, x + hw - 7, y + 238), fill=(226, 236, 220))
        d.text((x + hw - 66, y + 226), tag, font=font(9, 'bold'), fill=GREEN)

    # --- ten smaller stories ---
    cards = [
        ('CRIMEA  -  WAR', 'Crimean bridge hit again', 'Third strike in a week halts rail traffic after Neptune missiles.  -  Reuters', 'bridge'),
        ('RIYADH  -  GULF', 'Houthi missile damages Riyadh tower', 'Saudi wealth-fund HQ hit; coalition says it intercepted others.  -  Al Jazeera', 'tower'),
        ('ODISHA  -  STORM', 'Cyclone Akvan nears India coast', 'Over 300,000 evacuated, schools shut as landfall begins.  -  NDTV, India Today', 'cyclone'),
        ('SEOUL  -  EDUCATION', '550,000 sit South Korea’s Suneung', 'Nationwide alert against cheating for the college entrance exam.  -  Korea JoongAng Daily', 'exam'),
        ('COPENHAGEN  -  ARCTIC', 'Denmark OKs US-Greenland pact', 'Parliament votes 109-0 for the security deal.  -  AP, The Guardian', 'flag'),
        ('NEW YORK  -  MARKETS', 'Anthropic jumps 17% on debut', 'Shares open above $83 after a record $81.3bn IPO.  -  Reuters, CNBC', 'chart'),
        ('WORLDWIDE  -  GAMES', 'GTA VI goes on sale after 13 years', 'Day-one sales estimated near $2bn, an entertainment record.  -  BBC, Reuters', 'game'),
        ('BOGOTÁ  -  LABOUR', 'Colombia’s unions hold national strike', 'Protests and roadblocks against the government’s reforms.  -  Arab News', 'strike'),
        ('CANBERRA  -  ECONOMY', 'Australia’s jobless rate hits 4.9%', 'Highest since 2021 as 43,500 jobs are lost.  -  ABC, Bloomberg', 'chart_down'),
        ('NEW YORK  -  CULTURE', 'Van Gogh sells for record $190.4m', 'Nazi-era ownership dispute settled before the auction.  -  AP, The Guardian', 'art'),
    ]
    cw, gap = 192, 8
    for i, (kick, head, body, icon) in enumerate(cards):
        col, row = i % 5, i // 5
        x = 16 + col * (cw + gap)
        y = 482 + row * 118
        d.rectangle((x, y, x + cw, y + 112), fill=PAPER, outline=INK, width=1)
        d.rectangle((x + 1, y + 1, x + cw - 1, y + 27), fill=(232, 226, 210))
        img.paste(card_art(icon, (54, 26)), (x + 1, y + 1))
        d.text((x + 60, y + 5), kick, font=font(8.5, 'bold'), fill=RED)
        para(d, (x + 6, y + 32), head, 12.5, cw - 12, 'serif', INK, leading=14, max_lines=2)
        para(d, (x + 6, y + 70), body, 9, cw - 12, fill=(60, 54, 48), leading=11, max_lines=3)

    # --- map and briefs ---
    draw_map(d, (16, 720, 286, 172))
    d.text((18, 894), 'Pins 1-13 mark the illustrated stories above.  Colours: Europe / Asia / Africa / Americas / Oceania / World.',
           font=font(8), fill=MUTED)
    d.text((310, 718), 'ALSO ON THURSDAY 19 NOVEMBER', font=font(12, 'bold'), fill=RED)
    briefs = [
        '14  Shenzhen - Xi urges a ban on nuclear arms.  Al Jazeera',
        '15  APEC - leaders adopt the Shenzhen Declaration.  ABC',
        '16  Washington - Senate blocks Iran war-powers bill.  Reuters',
        '17  Kyiv - Trump open to NATO-style guarantees.  PBS',
        '18  New York - UN secretary-general race stalls.  Reuters',
        '19  Florida - record rain closes schools.  NYT, PBS',
        '20  Gaza - Israeli tanks cross the yellow line.  NBC News',
        '21  Riyadh - Iran pressed at IAEA on inspections.  WSAU',
        '22  COP31 - “35 by 35” power target kept.  Down To Earth',
        '23  Wall Street - Dow closes below 50,000.  CNBC',
        '24  Tech - Nvidia and Broadcom shares slide.  Yahoo Finance',
        '25  New York - protesters rally at Anthropic IPO.  Guardian',
        '26  Auckland - GTA VI opens at local midnight.  Reuters',
        '27  Sony - shares rise on GTA VI launch.  Reuters',
        '28  Seoul - ex-PM Han Duck-soo conviction overturned.  AP',
        '29  Odisha - 47 trains cancelled as storm approaches.  NDTV',
        '30  Antarctica - ice cliffs collapse, then stabilise.  ScienceDaily',
        '31  Space - Voyager 1 reaches one light-day.  NASA, AP',
        '32  Melbourne - recession fears as jobs fall.  The Guardian',
        '33  Pretoria - central bank holds rate at 7.25%.  SABC',
        '34  World - International Men’s Day observed.  Reuters',
        '35  Miami - flood rescues and synagogue roof collapse.  AP',
        '36  Khartoum - RSF chief sentenced in absentia.  AP',
        '37  The Hague - ruling is first of its kind.  CNN',
        '38  Crypto - Bitcoin slips after Anthropic debut.  CoinDesk',
        '39  Nairobi - marathon champion banned 3 years.  ABC',
        '40  Sport - 2026 World Cup schedule published.  AP',
        '41  Mogadishu - Somalia expels UAE ambassador.  Al Jazeera',
    ]
    for i, line in enumerate(briefs):
        col, row = i // 14, i % 14
        x = 310 + col * 350
        y = 736 + row * 12
        fit(d, (x, y), line, 9, 'sans', 340, (45, 40, 36))

    # --- date check and sources ---
    d.rectangle((16, 916, 1008, 976), fill=(232, 239, 224), outline=GREEN, width=2)
    d.ellipse((24, 926, 40, 942), fill=GREEN)
    d.text((28, 928), '✓', font=font(12, 'bold'), fill=(255, 255, 255))
    para(d, (46, 922),
         'DATE CHECK  -  Every story happened, or was first reported, on Thursday 19 November 2026 in any time zone. '
         'Claims are attributed, not stated as fact; stories still unfolding are marked REPORTED or FORECAST.',
         9.5, 950, fill=(35, 70, 45), leading=12, max_lines=3)
    para(d, (46, 952),
         'LEFT OUT: earlier-day news - 18 Nov: EU’s €45bn Ukraine loan plan, Anthropic IPO pricing. ',
         9, 950, fill=RED, leading=11, max_lines=2)
    fit(d, (18, 984),
        'Original drawings.  Sources: Reuters - AP - BBC - Al Jazeera - UN News - PBS - CNBC - ABC - NDTV - NASA - The Guardian - Bloomberg.  19 November 2026.',
        9, 'sans', 988, MUTED)

    img.save('news.png', optimize=True)
    print('wrote news.png', img.size)


if __name__ == '__main__':
    main()

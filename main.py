# news-image-20261123 — one front-page image summing up Monday 23 November 2026.
# Judging: a single image that best captures the day's news (COP31 lead, world map, 30 stories).
# Output: entry.png, 1024x1024 PNG, under 1 MiB, drawn fully in code with Pillow.
# Deterministic: no clock, no network, fixed story list — two runs give byte-identical output.
#!/usr/bin/env python3
"""news-image-20261123: sum up Monday 23 November 2026 in one image.

A newspaper front page drawn entirely in code with Pillow: masthead naming
the day, the lead story (COP31), a world map with numbered story markers,
and 30 short stories from every region. Deterministic: no clock, no network,
fixed story list. Writes entry.png (1024x1024) to MAKEFUN_OUTPUT_DIR.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BASE = os.path.dirname(os.path.abspath(__file__))

INK = (26, 26, 26)
PAPER = (247, 242, 231)
RED = (178, 34, 34)
GREY = (110, 105, 95)
BLUE = (70, 110, 140)


def font(name, size):
    p = os.path.join(BASE, "fonts", name)
    try:
        return ImageFont.truetype(p, size)
    except Exception:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name, size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
F_SERIF_R = lambda s: font("DejaVuSerif.ttf", s)          # noqa: E731
F_SANS = lambda s: font("DejaVuSans.ttf", s)              # noqa: E731
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)         # noqa: E731


def wrap(d, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 96], fill=(26, 26, 26))
t = "THE WORLD IN ONE DAY"
f = F_SERIF(52)
d.text(((W - d.textlength(t, font=f)) / 2, 8), t, font=f, fill=(247, 242, 231))
t2 = "MONDAY, 23 NOVEMBER 2026"
f2 = F_BOLD(20)
d.text(((W - d.textlength(t2, font=f2)) / 2, 66), t2, font=f2, fill=(232, 180, 60))
d.line([16, 100, W - 16, 100], fill=RED, width=4)

# ---------------------------------------------------------------- lead story
d.text((18, 110), "CLIMATE  ·  COP31  ·  ANTALYA, TURKEY", font=F_BOLD(16), fill=RED)
lead = ["COP31 climate deal collapses",
        "as EU rejects draft with no fossil fuels"]
y = 132
for line in lead:
    d.text((18, y), line, font=F_SERIF(34), fill=INK)
    y += 40
d.text((18, y + 2),
       "EU and other nations refuse a pact that omits fossil fuels; the summit ends with no deal.",
       font=F_SERIF_R(15), fill=GREY)

# ---------------------------------------------------------------- world map
MAP_X0, MAP_Y0, MAP_X1, MAP_Y1 = 16, 232, 1008, 408


def mx(lon):
    return MAP_X0 + (lon + 170) / 360.0 * (MAP_X1 - MAP_X0)


def my(lat):
    return MAP_Y0 + (80 - lat) / 135.0 * (MAP_Y1 - MAP_Y0)


def poly(ll):
    return [(mx(lo), my(la)) for lo, la in ll]


d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], fill=(214, 228, 236),
            outline=(150, 165, 175), width=2)

LAND = (216, 203, 168)
OUT = (140, 128, 96)
# draw land on its own layer, clipped to the map box
land_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(land_layer)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-90, 15),
     (-95, 18), (-105, 22), (-115, 28), (-125, 40), (-125, 49), (-140, 60),
     (-160, 58)],
    [(-55, 60), (-40, 65), (-30, 70), (-20, 74), (-40, 78), (-58, 76)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -45), (-70, -52), (-73, -40), (-72, -20),
     (-78, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (48, 11), (51, 10), (40, 0), (35, -18), (28, -32), (18, -35),
     (12, -18), (8, 4), (-8, 5)],
    [(-10, 36), (-9, 43), (0, 48), (-2, 50), (5, 53), (8, 57), (18, 56),
     (21, 55), (28, 60), (30, 62), (25, 70), (15, 70), (5, 60), (-5, 50)],
    [(30, 62), (40, 68), (60, 70), (100, 76), (130, 72), (160, 66),
     (178, 65), (160, 60), (150, 45), (140, 40), (130, 33), (120, 25),
     (108, 12), (100, 8), (95, 15), (90, 22), (80, 8), (75, 20), (65, 25),
     (55, 26), (48, 30), (40, 36), (35, 36)],
    [(113, -22), (122, -14), (132, -12), (142, -11), (150, -22), (153, -28),
     (150, -37), (140, -38), (130, -32), (120, -34), (114, -30)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53)],
    [(130, 31), (133, 34), (138, 36), (141, 39), (142, 44), (140, 42)],
]
for c in CONTINENTS:
    ld.polygon(poly(c), fill=LAND + (255,), outline=OUT + (255,))
for lo, la, r in [(95, 5, 4), (105, 0, 4), (115, -5, 4), (125, -2, 4),
                  (135, -4, 4), (140, -8, 3)]:
    ld.ellipse([mx(lo) - r, my(la) - r, mx(lo) + r, my(la) + r],
               fill=LAND + (255,), outline=OUT + (255,))
clip = Image.new("L", (W, H), 0)
cd = ImageDraw.Draw(clip)
cd.rectangle([MAP_X0 + 1, MAP_Y0 + 1, MAP_X1 - 1, MAP_Y1 - 1], fill=255)
img = Image.alpha_composite(img.convert("RGBA"),
                            Image.composite(land_layer, Image.new("RGBA", (W, H), (0, 0, 0, 0)), clip))
d = ImageDraw.Draw(img)
d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], outline=(150, 165, 175), width=2)
d.rectangle([MAP_X0 + 6, MAP_Y0 + 6, MAP_X0 + 196, MAP_Y0 + 26],
            fill=(214, 228, 236), outline=(150, 165, 175))
d.text((MAP_X0 + 10, MAP_Y0 + 9), "WHERE THE DAY HAPPENED",
       font=F_BOLD(13), fill=(60, 80, 95))

MARKERS = [  # (lon, lat, number) -> tile number
    (36, 36, 1), (56, 26, 2), (31, 49, 3), (20, 63, 4), (-9, 39, 5),
    (107, -6, 6), (96, 21, 7), (77, 28, 8), (127, 37, 9), (175, -41, 10),
]
for lo, la, n in MARKERS:
    x, y = mx(lo), my(la)
    d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=RED,
              outline=(255, 255, 255), width=2)
    s = str(n)
    fw = d.textlength(s, font=F_BOLD(11))
    d.text((x - fw / 2, y - 8), s, font=F_BOLD(11), fill=(255, 255, 255))

# ---------------------------------------------------------------- story grid
# (number, category, colour, headline, glyph)
STORIES = [
    (1, "CLIMATE", (178, 34, 34), "COP31 deal collapses over fossil fuels", "sun"),
    (2, "WAR", (120, 30, 30), "Iran-US war widens to Saudi, Bahrain", "missile"),
    (3, "UKRAINE", (70, 90, 160), "14 missing after drone hits Kyiv flats", "building"),
    (4, "SEA", (40, 110, 140), "Russian cargo ship ablaze off Finland", "ship"),
    (5, "EUROPE", (90, 60, 140), "Thousands march in Lisbon on living costs", "people"),
    (6, "INDONESIA", (200, 90, 20), "50 missing after factory fire", "flame"),
    (7, "MYANMAR", (150, 100, 30), "ASEAN ruling 'unfair', junta says", "flag"),
    (8, "INDIA", (200, 120, 30), "Nepal PM in Delhi for Modi talks", "flag"),
    (9, "KOREA", (60, 120, 90), "Minister quits over AI exam scandal", "cap"),
    (10, "CRICKET", (40, 130, 60), "India post record 720/9 in Wellington", "ball"),
    (11, "POLAND", (120, 30, 30), "Poland: Russian missiles crossed border", "warn"),
    (12, "UK-EU", (40, 90, 160), "UK and EU agree Brexit reset deal", "flag"),
    (13, "CHINA", (178, 34, 34), "Xi, Trump, Putin hold historic summit", "globe"),
    (14, "JUSTICE", (60, 60, 60), "ICJ: Myanmar committed Rohingya genocide", "scales"),
    (15, "TECH", (30, 110, 110), "AI chips diverted to China, probe finds", "chip"),
    (16, "INDIA", (200, 120, 30), "Shah's Arunachal infra push", "flag"),
    (17, "FILM", (140, 60, 120), "IFFI hosts BRICS film roundtable", "film"),
    (18, "INDIA", (200, 120, 30), "BJP MP Wadkute dies in Delhi", "flag"),
    (19, "SNOOKER", (40, 130, 60), "Anupama keeps world snooker crown", "ball"),
    (20, "FINLAND", (40, 90, 160), "Russia summons Finnish envoy", "flag"),
    (21, "YEMEN", (120, 30, 30), "Houthi missile at Saudi Arabia stopped", "missile"),
    (22, "IRAN", (150, 100, 30), "Uranium stays in Iran, minister says", "atom"),
    (23, "USA", (40, 90, 160), "Trump: no worry over Iran regime change", "flag"),
    (24, "ENERGY", (200, 140, 20), "US to build nuclear plant in Saudi", "atom"),
    (25, "HORMUZ", (40, 110, 140), "Tanker attacks hit record high", "ship"),
    (26, "KASHMIR", (60, 130, 60), "Saffron fields used as dump: Mufti", "leaf"),
    (27, "CAMPUS", (90, 60, 140), "Hyderabad campus protests go on", "people"),
    (28, "KOTA", (200, 90, 20), "Nine pilgrims killed in Kota crash", "car"),
    (29, "MUMBAI", (120, 30, 30), "Six held after Mumbai assault", "warn"),
    (30, "CHESS", (60, 60, 60), "World chess title fight goes on", "crown"),
]


def glyph(kind, x, y, s, color):
    """Minimal white pictogram inside a coloured square at (x, y), size s."""
    d.rounded_rectangle([x, y, x + s, y + s], radius=4, fill=color)
    w = (255, 255, 255)
    cx, cy = x + s / 2, y + s / 2
    if kind == "sun":
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=w)
        for a in range(8):
            import math
            an = a * 3.14159 / 4
            d.line([(cx + 8 * math.cos(an), cy + 8 * math.sin(an)),
                    (cx + 12 * math.cos(an), cy + 12 * math.sin(an))],
                   fill=w, width=2)
    elif kind == "flame":
        d.polygon([(cx, cy - 10), (cx + 7, cy + 2), (cx + 3, cy + 9),
                   (cx - 3, cy + 9), (cx - 7, cy + 2)], fill=w)
    elif kind == "ship":
        d.polygon([(cx - 9, cy + 2), (cx + 9, cy + 2), (cx + 6, cy + 9),
                   (cx - 6, cy + 9)], fill=w)
        d.polygon([(cx - 1, cy - 10), (cx - 1, cy + 1), (cx + 8, cy + 1)],
                  fill=w)
    elif kind == "missile":
        d.polygon([(cx - 8, cy + 8), (cx + 6, cy - 6), (cx + 9, cy - 3),
                   (cx - 5, cy + 11)], fill=w)
        d.ellipse([cx + 5, cy - 9, cx + 11, cy - 3], outline=w, width=2)
    elif kind == "building":
        d.rectangle([cx - 7, cy - 9, cx + 7, cy + 9], fill=w)
        for yy in (-5, 0, 5):
            d.line([(cx - 4, cy + yy), (cx + 4, cy + yy)], fill=color, width=2)
    elif kind == "flag":
        d.line([(cx - 6, cy - 10), (cx - 6, cy + 10)], fill=w, width=2)
        d.polygon([(cx - 6, cy - 10), (cx + 8, cy - 6), (cx - 6, cy - 2)],
                  fill=w)
    elif kind == "people":
        d.ellipse([cx - 8, cy - 8, cx - 1, cy - 1], fill=w)
        d.ellipse([cx + 1, cy - 8, cx + 8, cy - 1], fill=w)
        d.arc([cx - 9, cy - 1, cx - 1, cy + 10], 180, 360, fill=w, width=2)
        d.arc([cx + 1, cy - 1, cx + 9, cy + 10], 180, 360, fill=w, width=2)
    elif kind == "ball":
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=w, width=2)
        d.arc([cx - 8, cy - 8, cx + 8, cy + 8], 200, 340, fill=w, width=2)
        d.line([(cx - 8, cy), (cx + 8, cy)], fill=w, width=2)
    elif kind == "cap":
        d.polygon([(cx, cy - 7), (cx + 10, cy - 2), (cx, cy + 3),
                   (cx - 10, cy - 2)], fill=w)
        d.line([(cx - 6, cy + 1), (cx - 6, cy + 7), (cx + 6, cy + 7),
                (cx + 6, cy + 1)], fill=w, width=2)
    elif kind == "warn":
        d.polygon([(cx, cy - 10), (cx + 10, cy + 8), (cx - 10, cy + 8)],
                  outline=w, width=2)
        d.line([(cx, cy - 4), (cx, cy + 3)], fill=w, width=2)
        d.point((cx, cy + 6), fill=w)
    elif kind == "globe":
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=w, width=2)
        d.ellipse([cx - 4, cy - 9, cx + 4, cy + 9], outline=w, width=1)
        d.line([(cx - 9, cy), (cx + 9, cy)], fill=w, width=1)
    elif kind == "scales":
        d.line([(cx, cy - 9), (cx, cy + 9)], fill=w, width=2)
        d.line([(cx - 8, cy - 6), (cx + 8, cy - 6)], fill=w, width=2)
        d.polygon([(cx - 8, cy - 6), (cx - 5, cy + 1), (cx - 11, cy + 1)],
                  outline=w, width=1)
        d.polygon([(cx + 8, cy - 6), (cx + 5, cy + 1), (cx + 11, cy + 1)],
                  outline=w, width=1)
    elif kind == "chip":
        d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], outline=w, width=2)
        for yy in (-4, 0, 4):
            d.line([(cx - 9, cy + yy), (cx - 6, cy + yy)], fill=w, width=2)
            d.line([(cx + 6, cy + yy), (cx + 9, cy + yy)], fill=w, width=2)
    elif kind == "film":
        d.rectangle([cx - 9, cy - 7, cx + 9, cy + 7], outline=w, width=2)
        for xx in (-6, 6):
            d.rectangle([cx + xx - 1, cy - 4, cx + xx + 1, cy + 4], fill=w)
    elif kind == "atom":
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=w)
        d.ellipse([cx - 9, cy - 4, cx + 9, cy + 4], outline=w, width=1)
        d.ellipse([cx - 4, cy - 9, cx + 4, cy + 9], outline=w, width=1)
    elif kind == "leaf":
        d.ellipse([cx - 7, cy - 9, cx + 7, cy + 9], fill=w)
        d.line([(cx, cy - 9), (cx, cy + 9)], fill=color, width=1)
    elif kind == "car":
        d.rectangle([cx - 9, cy - 2, cx + 9, cy + 4], fill=w)
        d.polygon([(cx - 5, cy - 2), (cx - 3, cy - 7), (cx + 4, cy - 7),
                   (cx + 6, cy - 2)], fill=w)
        d.ellipse([cx - 7, cy + 3, cx - 2, cy + 8], fill=INK)
        d.ellipse([cx + 2, cy + 3, cx + 7, cy + 8], fill=INK)
    elif kind == "crown":
        d.polygon([(cx - 9, cy + 6), (cx - 9, cy - 4), (cx - 4, cy + 1),
                   (cx, cy - 7), (cx + 4, cy + 1), (cx + 9, cy - 4),
                   (cx + 9, cy + 6)], fill=w)


GX, GY, TW, TH, GAP = 18, 416, 158, 108, 8
for i, (num, cat, color, head, gk) in enumerate(STORIES):
    col, row = i % 6, i // 6
    x = GX + col * (TW + GAP)
    y = GY + row * (TH + GAP)
    d.rectangle([x, y, x + TW, y + TH], outline=(200, 192, 172), width=1)
    d.rectangle([x, y, x + TW, y + 3], fill=color)
    glyph(gk, x + 7, y + 10, 26, color)
    d.text((x + 38, y + 9), cat, font=F_BOLD(11), fill=color)
    d.text((x + TW - 20, y + 9), str(num), font=F_BOLD(11), fill=GREY)
    lines = wrap(d, head, F_BOLD(13), TW - 14)[:3]
    ly = y + 42
    for ln in lines:
        d.text((x + 7, ly), ln, font=F_BOLD(13), fill=INK)
        ly += 17

# ---------------------------------------------------------------- footer
d.line([16, 996, W - 16, 996], fill=RED, width=2)
ft = "23 NOVEMBER 2026  ·  30 STORIES FROM EVERY REGION  ·  THE WORLD IN ONE DAY"
ff = F_BOLD(13)
d.text(((W - d.textlength(ft, font=ff)) / 2, 1000), ft, font=ff, fill=GREY)

# ---------------------------------------------------------------- write output
outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(outdir, exist_ok=True)
out = os.path.join(outdir, "entry.png")
img = img.convert("RGB")
img.save(out, "PNG", optimize=True)
if os.path.getsize(out) > 1048576:
    img.save(out, "JPEG", quality=92, optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")

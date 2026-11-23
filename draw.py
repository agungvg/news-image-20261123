#!/usr/bin/env python3
"""Paint the front page for Monday 23 November 2026.

A newspaper front page, 1024x1024. The 13 story illustrations are 3D
dioramas built in code with three.js (~/workspace/makefun/news-image-
20261123-3d/scene.js, rendered in this session) and composited here;
the layout, text, map and lists are drawn with Pillow. Flat Pillow
drawings remain as fallback if a 3D render file is missing.
48 stories from 7 regions, every one happened or first reported on
Monday 23 November 2026. Three hero panels (Kyiv region strikes,
COP31 collapses, Hormuz tankers), ten small illustrated panels, a
UTC timeline, a numbers strip, a world map with numbered pins, a
35-story also-on list, and a date-check box for older news left out.

No network, no clock, no randomness: two runs write byte-identical PNGs.
Sources: Reuters, AP, Arab News, CNN, The Times, BBC, Al Jazeera, AP,
UKMTO, IQAir/Dawn, and Monday-morning market wires (see README).
"""
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

CREAM = (247, 241, 227)
PAPER = (250, 245, 232)
INK = (26, 26, 26)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
NAVY = (24, 48, 84)
TEAL = (18, 92, 92)
GREY = (110, 110, 105)
LIGHT = (232, 224, 205)
RULE = (60, 60, 60)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def tag(draw, x, y, text, fill=RED):
    """Small red caps label, returns width used."""
    f = font(SANS_B, 11)
    draw.text((x, y), text, font=f, fill=fill)
    return int(draw.textlength(text, font=f))


def source_tag(draw, x, y, text):
    f = font(SANS_B, 10)
    draw.text((x, y), text, font=f, fill=(90, 90, 90))


# ---------------------------------------------------------------- scenes
ASSETS3D = HERE / "assets3d"
BASE = None  # set to the page image in main(); paste3d draws into it


def paste3d(d, x, y, w, h, key):
    """Paste a 3D render into a panel (cover-crop to w x h). False if missing."""
    p = ASSETS3D / f"{key}.png"
    if not p.exists() or BASE is None:
        return False
    im = Image.open(p).convert("RGB")
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    ox = (im.width - w) // 2
    oy = (im.height - h) // 2
    im = im.crop((ox, oy, ox + w, oy + h))
    BASE.paste(im, (x, y))
    return True


def scene_kyiv_flat(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 43, 74))
    d.ellipse([x + w - 52, y + 10, x + w - 22, y + 40], fill=(240, 230, 190))
    # skyline, one block collapsed
    for bx, bw, bh in [(0, 34, 62), (38, 30, 84), (72, 36, 56), (150, 40, 92),
                       (196, 34, 70), (236, 38, 80), (278, 30, 60)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(16, 24, 44))
        for wy in range(y + h - bh + 8, y + h - 6, 12):
            for wx in range(x + bx + 6, x + bx + bw - 6, 11):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 205, 90))
    # collapsed block + rubble + searchlight
    d.polygon([(x + 108, y + h), (x + 128, y + h - 46), (x + 150, y + h)],
              fill=(70, 70, 78))
    d.polygon([(x + 118, y + h - 46), (x + 150, y + 22), (x + 186, y + 22),
               (x + 158, y + h - 40)], fill=(255, 220, 130))
    d.ellipse([x + 96, y + h - 18, x + w - 8, y + h - 4], fill=(120, 90, 60))
    d.ellipse([x + 120, y + h - 12, x + 150, y + h - 2], fill=(200, 120, 40))


def scene_cop31_flat(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 92, 92))
    # cracked globe
    cx, cy, r = x + w // 2, y + 52, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 200, 190))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(10, 60, 60), width=2)
    d.arc([cx - 20, cy - 26, cx + 20, cy + 26], 300, 60, fill=(10, 60, 60), width=2)
    d.line([cx - 8, cy - 30, cx + 4, cy - 8, cx - 6, cy + 12, cx + 10, cy + 30],
           fill=(10, 60, 60), width=3)
    # empty chairs around a table
    d.rectangle([x + 30, y + h - 34, x + w - 30, y + h - 22], fill=(120, 72, 32))
    for cx2 in (x + 44, x + 130, x + 216, x + 268):
        d.rectangle([cx2, y + h - 58, cx2 + 26, y + h - 34], fill=(200, 170, 120))
        d.rectangle([cx2 + 4, y + h - 22, cx2 + 22, y + h - 6], fill=(160, 130, 90))


def scene_hormuz_flat(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 95, 138))
    d.ellipse([x + 18, y + 12, x + 52, y + 40], fill=(255, 220, 120))
    # tanker
    d.rectangle([x + 60, y + 62, x + 250, y + 92], fill=(30, 30, 34))
    d.rectangle([x + 60, y + 86, x + 250, y + 92], fill=(178, 34, 34))
    for cx2 in range(x + 74, x + 240, 34):
        d.rectangle([cx2, y + 44, cx2 + 24, y + 62], fill=(220, 200, 160))
    d.rectangle([x + 248, y + 34, x + 268, y + 62], fill=(240, 240, 240))
    # explosion + mines
    for dx, dy, r in [(0, 0, 16), (12, -8, 11), (-12, -6, 10), (6, 10, 9)]:
        d.ellipse([x + 286 + dx - r, y + 30 + dy - r, x + 286 + dx + r,
                   y + 30 + dy + r], fill=(255, 180, 40))
    d.ellipse([x + 278, y + 22, x + 294, y + 38], fill=(255, 240, 160))
    for mx, my in [(x + 34, y + 104), (x + 120, y + 110)]:
        d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(16, 16, 16))
        for ang in range(0, 360, 45):
            import math
            d.line([mx, my, mx + int(11 * math.cos(math.radians(ang))),
                    my + int(11 * math.sin(math.radians(ang)))],
                   fill=(16, 16, 16), width=2)
    d.arc([x + 8, y + 96, x + 90, y + 122], 180, 360, fill=(200, 230, 240), width=2)
    d.arc([x + 150, y + 100, x + 240, y + 124], 180, 360, fill=(200, 230, 240), width=2)


def scene_kyiv(d, x, y, w, h):
    if not paste3d(d, x, y, w, h, "kyiv"):
        scene_kyiv_flat(d, x, y, w, h)


def scene_cop31(d, x, y, w, h):
    if not paste3d(d, x, y, w, h, "cop31"):
        scene_cop31_flat(d, x, y, w, h)


def scene_hormuz(d, x, y, w, h):
    if not paste3d(d, x, y, w, h, "hormuz"):
        scene_hormuz_flat(d, x, y, w, h)


def mini(d, x, y, w, h, kind):
    """Small 3D illustration for the second-tier panels (flat fallback)."""
    if paste3d(d, x, y, w, h, kind):
        return
    bg = {"chart": (240, 235, 220), "pitch": (46, 130, 70), "court": (52, 110, 180),
          "badge": (230, 210, 170), "dome": (210, 220, 235), "refinery": (60, 60, 70),
          "fire": (70, 40, 40), "un": (40, 90, 160), "castle": (200, 80, 60),
          "ship": (30, 95, 138)}[kind]
    d.rectangle([x, y, x + w, y + h], fill=bg)
    if kind == "chart":
        pts = [(x + 12, y + 18), (x + 50, y + 30), (x + 90, y + 22),
               (x + 130, y + 40), (x + 168, y + 48)]
        d.line(pts, fill=RED, width=4)
        d.polygon(pts + [(x + 168, y + h), (x + 12, y + h)], fill=(178, 34, 34, 60))
        d.text((x + 12, y + h - 20), "-3.7%", font=font(SANS_B, 16), fill=RED)
    elif kind == "pitch":
        d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], outline=(255, 255, 255), width=2)
        d.line([x + w // 2, y + 8, x + w // 2, y + h - 8], fill=(255, 255, 255), width=2)
        d.ellipse([x + w // 2 - 14, y + h // 2 - 14, x + w // 2 + 14, y + h // 2 + 14],
                  fill=(255, 255, 255))
    elif kind == "court":
        d.rectangle([x + 12, y + 8, x + w - 12, y + h - 8], outline=(255, 255, 255), width=2)
        d.line([x + w // 2, y + 8, x + w // 2, y + h - 8], fill=(255, 255, 255), width=2)
        d.ellipse([x + w // 2 - 7, y + 14, x + w // 2 + 7, y + 28], fill=(220, 240, 60))
    elif kind == "badge":
        cx, cy = x + w // 2, y + h // 2
        d.polygon([(cx, cy - 20), (cx + 18, cy - 6), (cx + 12, cy + 16),
                   (cx - 12, cy + 16), (cx - 18, cy - 6)], fill=(200, 160, 40))
        d.text((cx - 5, cy - 8), "$", font=font(SANS_B, 16), fill=(255, 255, 255))
    elif kind == "dome":
        d.rectangle([x + 20, y + h - 16, x + w - 20, y + h - 8], fill=(255, 255, 255))
        d.pieslice([x + w // 2 - 34, y + 6, x + w // 2 + 34, y + h - 10], 180, 360,
                   fill=(255, 255, 255))
        d.rectangle([x + w // 2 - 3, y + 2, x + w // 2 + 3, y + 12], fill=(40, 60, 120))
    elif kind == "refinery":
        for tx in (x + 20, x + 60, x + 100, x + 140):
            d.rectangle([tx, y + 18, tx + 22, y + h - 10], fill=(180, 180, 190))
        d.polygon([(x + 118, y + 6), (x + 132, y + 22), (x + 118, y + 34)],
                  fill=(255, 150, 40))
        d.ellipse([x + 150, y + 8, x + 168, y + 26], fill=(255, 180, 60))
    elif kind == "fire":
        d.polygon([(x + w // 2, y + 6), (x + w // 2 + 22, y + 34),
                   (x + w // 2 + 10, y + 50), (x + w // 2 - 10, y + 50),
                   (x + w // 2 - 22, y + 34)], fill=(255, 120, 30))
        d.ellipse([x + w // 2 - 8, y + 30, x + w // 2 + 8, y + 48], fill=(255, 200, 60))
    elif kind == "un":
        d.ellipse([x + w // 2 - 22, y + 8, x + w // 2 + 22, y + 52], fill=(220, 235, 255))
        d.text((x + w // 2 - 12, y + 18), "UN", font=font(SANS_B, 18), fill=(30, 70, 140))
    elif kind == "castle":
        d.rectangle([x + 30, y + 26, x + w - 30, y + h - 10], fill=(250, 240, 220))
        d.polygon([(x + 20, y + 28), (x + w // 2, y + 6), (x + w - 20, y + 28)],
                  fill=(160, 30, 30))
        d.rectangle([x + w // 2 - 5, y + 34, x + w // 2 + 5, y + h - 10], fill=(120, 30, 30))
    elif kind == "ship":
        d.polygon([(x + 20, y + 34), (x + w - 20, y + 34), (x + w - 34, y + 50),
                   (x + 34, y + 50)], fill=(20, 20, 24))
        d.rectangle([x + 70, y + 16, x + 110, y + 34], fill=(220, 200, 160))
        d.ellipse([x + w - 44, y + 8, x + w - 20, y + 32], fill=(255, 220, 120))

# ---------------------------------------------------------------- stories
HEROES = [
    ("KYIV, UKRAINE", "WAR", scene_kyiv,
     "Flats fall as Russia strikes Kyiv region",
     "Rescuers dig through a collapsed five-storey block in Dymer; "
     "11 killed across the region, including two shoppers at a "
     "supermarket in Vyshneve. Zelenskyy vows retaliation.",
     "CONFIRMED", "ARAB NEWS / REUTERS"),
    ("ANTALYA, TURKEY", "CLIMATE", scene_cop31,
     "COP31 collapses with no deal at all",
     "The longest climate summit on record ends without an agreement "
     "after the EU and UK reject a text silent on fossil fuels. "
     "First COP failure since 2009.",
     "CONFIRMED", "CNN / THE TIMES"),
    ("STRAIT OF HORMUZ", "SHIPPING", scene_hormuz,
     "Three tankers struck; two more hit mines",
     "UK maritime authorities report projectile strikes on tankers "
     "in and near the strait; Iran's navy says two more caught fire "
     "after hitting naval mines.",
     "CONFIRMED", "UKMTO / AP"),
]

SMALL = [
    (4, "ASIA", "MARKETS", "chart",
     "Asia braces as AI rout rolls on",
     "Taiwan bans short-selling; China cuts margin; Korea readies "
     "stabilisation funds. KOSPI down 3.7% in morning trade.",
     "CONFIRMED", "REUTERS"),
    (5, "EUROPE", "FOOTBALL", "pitch",
     "FIFA to confirm UK as 2035 hosts",
     "Football's governing body confirms on Monday that the Women's "
     "World Cup goes to the UK — its first since 1966.",
     "CONFIRMED", "BBC"),
    (6, "EUROPE", "TENNIS", "court",
     "Alcaraz wins first ATP Finals title",
     "Carlos Alcaraz beats world No. 1 Alexander Zverev in Turin "
     "to take the season-ending crown.",
     "CONFIRMED", "ATP"),
    (7, "ENGLAND", "FOOTBALL", "pitch",
     "Liverpool sink ten-man United",
     "Liverpool win at Anfield in Pochettino's debut.",
     "CONFIRMED", "BBC"),
    (8, "MEXICO", "CRIME", "badge",
     "'Chapo Isidro' captured in Sinaloa",
     "Mexican forces seize Fausto Isidro Meza-Flores, wanted by the "
     "US on a $5m bounty, in a Guasave firefight.",
     "CONFIRMED", "TALI / AP"),
    (9, "AMERICAS", "POLITICS", "dome",
     "Democrats' biggest House win since '92",
     "Democrats secure their largest House majority since 1992 "
     "after flipping a North Carolina seat.",
     "REPORTED", "HUDDLEWORLD"),
    (10, "MIDDLE EAST", "WAR", "refinery",
     "Houthis claim Saudi refinery strike",
     "Houthi forces claim strikes on a Saudi oil refinery and "
     "radar; at least six people are reported injured.",
     "CLAIM", "INDIAN EXPRESS"),
    (11, "ASIA", "DISASTER", "fire",
     "24 body bags from factory fire",
     "Rescuers recover 24 body bags from the candy factory fire in "
     "Cikande, Banten; dozens still missing.",
     "REPORTED", "YOUTUBE / AP"),
    (12, "AFRICA", "WAR", "un",
     "Khartoum strikes hit UN facility",
     "Drone strikes hit Khartoum early on Sunday, damaging a UN "
     "facility while staff were inside; three killed in Omdurman.",
     "REPORTED", "YOUTUBE / AP"),
    (13, "JAPAN", "CULTURE", "castle",
     "Shuri Castle rises again",
     "Okinawa celebrates the restored main hall of Shuri Castle, "
     "seven years after fire destroyed it in 2019.",
     "CONFIRMED", "NIKKEI ASIA"),
]

ALSO = [
    (14, "Libya: Russian corvette Merkury capsized off Benghazi; 10 hurt", "REUTERS"),
    (15, "US: Hegseth memo curbs US-Canada defence ties", "WASH. POST"),
    (16, "US: Trump reposts 'TrumpCare' universal-care pitch", "WASH. POST"),
    (17, "Russia: drones hit Novoshakhtinsk refinery; fire", "UKRAINE GEN. STAFF"),
    (18, "West Bank: settlers torch 12 vehicles near Ramallah", "AP"),
    (19, "Pakistan: Lahore AQI 538, most polluted major city", "IQAir / DAWN"),
    (20, "Slovakia rejects part in new €45bn EU loan for Ukraine", "TALI"),
    (21, "Golf: Thitikul wins third straight LPGA title", "LPGA"),
    (22, "Darts: Gerwyn Price ends four-year major wait", "PDC"),
    (23, "Chess: Sindarov takes white in FIDE Worlds Game 1", "FIDE"),
    (24, "Cricket: India push for victory; NZ 157/4, Day 5", "REDDIFF"),
    (25, "Boxing: Fury reveals schizophrenia diagnosis", "THE SUN"),
    (26, "UK: Compass catering giant to move listing to New York", "FT"),
    (27, "UK: disability benefits review targets health claims", "THE TIMES"),
    (28, "UK: five ex-PMs warn Burnham against rejoining EU", "DAILY MAIL"),
    (29, "US: Army to detonate bomb chemicals in Iowa", "HUDDLEWORLD"),
    (30, "US: father, daughter held by ICE at Seattle airport", "THE HINDU"),
    (31, "Malaysia: Selangor flood evacuees pass 1,800", "TALI"),
    (32, "Libya: UN urges probe into Benghazi attacks", "UN"),
    (33, "US: Trump posts friendship photos with Putin and Xi", "TALI"),
    (34, "F1: Camara stays at Haas for final two Grands Prix", "HAAS"),
    (35, "Football: Pochettino: best team could have lost 4-0", "HUDDLEWORLD"),
    (36, "US: intel chief trusts Trump's 'my friend' Putin line", "HUDDLEWORLD"),
    (37, "Italy: jeweller Paolo Bulgari dies, aged 89", "JERUSALEM POST"),
    (38, "Japan: Hello Kitty owner Sanrio bets on games", "NIKKEI ASIA"),
    (39, "US: Melat Kiros, 29, first Gen Z woman in Congress", "TRENDMONEY"),
    (40, "US: gunfire at California concert injures 9", "TRENDMONEY"),
    (41, "Hong Kong: Tai Po fire — will lessons be learned?", "TRENDMONEY"),
    (42, "Japan: decarbonisation agency backs US recycling", "NIKKEI ASIA"),
    (43, "Spain: Sanchez defends himself on 'Salvados'", "HUDDLEWORLD"),
    (44, "India: Youth Congress protests Meta over blocked accounts", "TALI"),
    (45, "India: GIFT Nifty tops 26,000; Nifty +1.1%", "KARTALKS"),
    (46, "China: margin requirements cut, first in 10 months", "REUTERS"),
    (47, "Korea: market-stabilisation funds readied", "REUTERS"),
    (48, "Markets: Nvidia -14% on SEC accounting probe report", "REPORTED"),
]

TIMELINE = [
    ("00:37", "COP31 collapse confirmed"),
    ("01:22", "Kyiv toll: 11 killed"),
    ("02:44", "Vyshneve supermarket hit"),
    ("06:10", "GIFT Nifty tops 26,000"),
    ("07:40", "KOSPI -3.7% in morning trade"),
    ("MONDAY", "FIFA confirms UK 2035"),
]

NUMBERS = [
    ("11", "killed in Kyiv region"),
    ("3", "tankers struck, Hormuz"),
    ("-3.7%", "S&P 500, Friday"),
    ("$60,974", "Bitcoin, Monday"),
    ("48", "stories, one day"),
    ("7", "regions covered"),
]

# rough continent polygons in (lon, lat)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-80, 62), (-75, 45),
     (-80, 32), (-90, 21), (-97, 16), (-105, 20), (-115, 30), (-125, 42),
     (-150, 60), (-168, 66)],
    [(-70, 12), (-55, 5), (-50, -5), (-40, -20), (-55, -35), (-65, -45),
     (-70, -30), (-78, -5), (-80, 5), (-70, 12)],
    [(-10, 36), (0, 43), (10, 45), (20, 40), (28, 41), (30, 36), (10, 36),
     (-5, 36), (-10, 36)],
    [(30, 70), (60, 70), (100, 75), (140, 72), (170, 66), (180, 65),
     (160, 60), (140, 40), (120, 30), (100, 10), (80, 8), (60, 25),
     (45, 30), (35, 45), (30, 70)],
    [(35, 32), (45, 30), (55, 25), (60, 15), (45, 12), (40, 18), (35, 32)],
    [(10, 35), (20, 32), (30, 31), (35, 28), (30, 15), (20, 5), (10, 5),
     (10, 20), (15, 30), (10, 35)],
    [(110, -12), (130, -12), (145, -15), (153, -27), (150, -38), (135, -35),
     (115, -33), (110, -12)],
]

PINS = [(1, 30, 50), (2, 30, 37), (3, 56, 26), (4, 120, 31), (5, 0, 52),
        (6, 7, 46), (7, -2, 53), (8, -107, 25), (9, -77, 39), (10, 45, 24),
        (11, 106, -6), (12, 32, 15), (13, 128, 26)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 228))
    def px(lon, lat):
        return (x + int((lon + 170) / 360 * w), y + int((72 - lat) / 140 * h))
    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(170, 185, 140))
    for n, lon, lat in PINS:
        cx, cy = px(lon, lat)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255))
        d.text((cx - 3, cy - 6), str(n), font=font(SANS_B, 9), fill=(255, 255, 255))

def paint():
    img = Image.new("RGB", (W, H), CREAM)
    global BASE
    BASE = img
    d = ImageDraw.Draw(img)
    mx = 22
    # ---- kicker
    d.text((mx, 10), "THE WORLD'S NEWS OF ONE DAY", font=font(SANS_B, 13), fill=RED)
    right = "48 STORIES  ·  7 REGIONS  ·  ALL FROM THIS MONDAY"
    d.text((W - mx - d.textlength(right, font=font(SANS_B, 13)), 10), right,
           font=font(SANS_B, 13), fill=INK)
    d.line([mx, 30, W - mx, 30], fill=RULE, width=1)
    # ---- headline
    head = "Monday 23 November 2026"
    hf = font(SERIF, 56)
    d.text(((W - d.textlength(head, font=hf)) / 2, 34), head, font=hf, fill=INK)
    sub = ("Kyiv flats fall, COP31 collapses, Hormuz tankers hit — "
           "every story here happened, or was first reported, on this day.")
    sf = font(SERIF_I, 16)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 100), sub, font=sf, fill=(70, 70, 70))
    # ---- timeline
    y = 126
    d.text((mx, y), "THE DAY IN UTC", font=font(SANS_B, 11), fill=RED)
    d.line([mx + 92, y + 6, W - mx, y + 6], fill=GREY, width=1)
    y += 16
    step = (W - 2 * mx) / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = mx + step * i + step / 2
        d.ellipse([cx - 3, y, cx + 3, y + 6], fill=RED)
        d.text((cx - d.textlength(t, font=font(SANS_B, 10)) / 2, y + 9), t,
               font=font(SANS_B, 10), fill=INK)
        lw = d.textlength(label, font=font(SANS, 9))
        d.text((max(mx, min(W - mx - lw, cx - lw / 2)), y + 21), label,
               font=font(SANS, 9), fill=(70, 70, 70))
    # ---- numbers strip
    y = 178
    d.line([mx, y, W - mx, y], fill=RULE, width=1)
    y += 6
    cw = (W - 2 * mx) / 6
    for i, (num, cap) in enumerate(NUMBERS):
        cx = mx + cw * i
        nf = font(SERIF, 26)
        d.text((cx + (cw - d.textlength(num, font=nf)) / 2, y), num, font=nf, fill=INK)
        cf = font(SANS, 9)
        d.text((cx + (cw - d.textlength(cap, font=cf)) / 2, y + 32), cap,
               font=cf, fill=(70, 70, 70))
        if i:
            d.line([cx, y + 2, cx, y + 44], fill=GREY, width=1)
    y += 52
    d.line([mx, y, W - mx, y], fill=RULE, width=1)
    # ---- hero row (3 across)
    y += 8
    hero_y = y
    hw = (W - 2 * mx - 16) / 3
    for i, (loc, field, scene, headline, body, conf, src) in enumerate(HEROES):
        x = mx + i * (hw + 8)
        scene(d, int(x), hero_y, int(hw), 118)
        d.rectangle([x, hero_y + 118, x + hw, hero_y + 134], fill=NAVY)
        d.text((x + 6, hero_y + 121), f"{i + 1}  {loc}  ·  {field}",
               font=font(SANS_B, 10), fill=(255, 255, 255))
        ty = hero_y + 140
        ty = para(d, x, ty, headline, font(SERIF, 21), int(hw), leading=23, max_lines=3)
        ty += 2
        ty = para(d, x, ty, body, font(SANS, 11), int(hw), leading=13, max_lines=4)
        ty += 3
        d.text((x, ty), conf, font=font(SANS_B, 10), fill=RED)
        d.text((x + 74, ty), src, font=font(SANS_B, 10), fill=(90, 90, 90))
    # ---- small rows (5 across, 2 rows)
    y = hero_y + 268
    sw = (W - 2 * mx - 32) / 5
    for row in range(2):
        for col in range(5):
            n, loc, field, kind, headline, body, conf, src = SMALL[row * 5 + col]
            x = mx + col * (sw + 8)
            top = y + row * 132
            mini(d, int(x), top, int(sw), 56, kind)
            d.text((x, top + 60), f"{n}  {loc} · {field}", font=font(SANS_B, 9), fill=RED)
            ty = top + 74
            ty = para(d, x, ty, headline, font(SERIF, 14), int(sw), leading=15, max_lines=2)
            ty = para(d, x, ty + 1, body, font(SANS, 9), int(sw), leading=11, max_lines=1)
            d.text((x, top + 121), conf, font=font(SANS_B, 9), fill=RED)
            d.text((x + 62, top + 121), src, font=font(SANS_B, 9), fill=(90, 90, 90))
    # ---- bottom: map + date check | also-on list
    y = hero_y + 268 + 264 + 6
    d.line([mx, y, W - mx, y], fill=RULE, width=1)
    y += 6
    d.text((mx, y), "WHERE IT HAPPENED", font=font(SANS_B, 11), fill=RED)
    d.text((mx + 340, y), "ALSO ON MONDAY 23 NOVEMBER — 35 MORE STORIES",
           font=font(SANS_B, 11), fill=RED)
    y += 16
    draw_map(d, mx, y, 308, 108)
    # also-on, two columns
    ax = mx + 340
    col_w = (W - mx - ax - 12) / 2
    for idx, (n, text, src) in enumerate(ALSO):
        col = idx // 18
        r = idx % 18
        x = ax + col * (col_w + 12)
        yy = y + r * 11
        d.text((x, yy), f"{n}.", font=font(SANS_B, 10), fill=RED)
        d.text((x + 20, yy), text, font=font(SANS, 10), fill=INK)
    # date check under map
    dy = y + 116
    d.rectangle([mx, dy, mx + 308, dy + 62], outline=RED, width=2)
    d.text((mx + 6, dy + 4), "DATE CHECK — LEFT OUT AS OLDER NEWS",
           font=font(SANS_B, 10), fill=RED)
    para(d, mx + 6, dy + 20,
         "Kyiv bridges hit (Fri 20 Nov) · Shenzhen summit (Thu 19 Nov) · "
         "Anthropic IPO $83 (Wed 18 Nov) · Voyager 1 light-day (Wed 18 Nov)",
         font(SANS, 10), 296, leading=12, max_lines=3)
    # ---- footer
    fy = H - 26
    d.line([mx, fy - 6, W - mx, fy - 6], fill=RULE, width=1)
    d.text((mx, fy), "Every story here happened, or was first reported, on Monday 23 November 2026. "
                     "Claims are attributed. Sources named beside each story · original 3D scenes.",
           font=font(SANS, 9), fill=(70, 70, 70))
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    paint()

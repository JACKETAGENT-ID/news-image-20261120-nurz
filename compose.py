#!/usr/bin/env python3
"""Draw the front page of 20 November 2026 as a newspaper, 1024x1024 PNG.

Every shape is drawn from scratch with Pillow primitives; no photo, no
copied artwork, no external asset. Run: python3 compose.py
Writes entry.png next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 222)      # cream newsprint
INK = (26, 26, 26)           # near-black ink
RED = (163, 22, 33)          # kicker red
GREY = (90, 90, 84)
SKY = (52, 74, 110)          # lead art sky
SEA = (38, 84, 120)
FLAME = (232, 122, 30)
FLAME2 = (245, 178, 44)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Word-wrap text to lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons
def icon_kyiv(d, x, y, w, h):
    """Night sky over Kyiv: skyline, missile trails, explosion."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # stars
    for sx, sy in [(18, 14), (70, 30), (120, 10), (180, 26), (230, 12),
                   (40, 48), (150, 44), (205, 52), (95, 60)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(240, 240, 220))
    # skyline
    base = y + h
    for bx, bw, bh in [(0, 42, 52), (46, 30, 78), (80, 52, 44),
                       (136, 34, 88), (174, 46, 58), (224, 40, 70)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(24, 30, 48))
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in range(bx + 7, bx + bw - 6, 12):
                d.rectangle([x + wx, wy, x + wx + 4, wy + 5], fill=(245, 200, 90))
    # missile trails
    d.line([(x + 60, y + 8), (x + 150, y + 92)], fill=(255, 255, 255), width=3)
    d.line([(x + 210, y + 4), (x + 165, y + 88)], fill=(255, 255, 255), width=3)
    # explosion starburst
    cx, cy = x + 158, y + 96
    for r, col in [(26, FLAME2), (18, FLAME), (10, (255, 235, 150))]:
        pts = []
        import math
        for k in range(12):
            ang = math.pi * k / 6
            rr = r if k % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=col)


def icon_genoa(d, x, y, w, h):
    """Runway seen from above with a quadcopter drone above it."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 205, 190))
    # runway strip
    d.rectangle([x + 30, y + h - 46, x + w - 30, y + h - 16], fill=(70, 72, 76))
    for dx in range(44, w - 44, 26):
        d.rectangle([x + dx, y + h - 34, x + dx + 14, y + h - 28],
                    fill=(240, 240, 230))
    # small plane on the runway
    px, py = x + w // 2, y + h - 31
    d.polygon([(px - 46, py), (px + 46, py), (px + 30, py - 7),
               (px - 30, py - 7)], fill=(220, 225, 230))
    d.polygon([(px - 6, py - 7), (px + 6, py - 7), (px + 2, py - 22),
               (px - 2, py - 22)], fill=(220, 225, 230))
    # quadcopter drone
    dx, dy = x + w - 62, y + 42
    d.ellipse([dx - 34, dy - 8, dx + 34, dy + 8], fill=(120, 120, 120))
    d.ellipse([dx - 44, dy - 4, dx + 44, dy + 4], fill=(160, 160, 160))
    d.ellipse([dx - 12, dy - 10, dx + 12, dy + 10], fill=INK)
    d.ellipse([dx - 4, dy - 3, dx + 4, dy + 3], fill=RED)
    d.line([(dx, dy + 10), (dx, dy + 34)], fill=INK, width=2)
    d.ellipse([dx - 7, dy + 32, dx + 7, dy + 44], fill=RED)


def icon_hormuz(d, x, y, w, h):
    """Tanker on a burning sea."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 196, 160))
    # sea
    d.rectangle([x, y + h - 58, x + w, y + h], fill=SEA)
    for wy in (h - 44, h - 26, h - 12):
        for wx in range(8, w - 8, 34):
            d.arc([x + wx, y + wy, x + wx + 26, y + wy + 12],
                  180, 360, fill=(160, 200, 225), width=3)
    # tanker hull
    d.polygon([(x + 26, y + h - 58), (x + w - 26, y + h - 58),
               (x + w - 46, y + h - 34), (x + 46, y + h - 34)],
              fill=(52, 52, 56))
    d.rectangle([x + w - 78, y + h - 92, x + w - 44, y + h - 58],
                fill=(220, 225, 230))
    d.rectangle([x + w - 74, y + h - 86, x + w - 48, y + h - 80],
                fill=SKY)
    # flames: pointed teardrops rising from the deck
    def flame(cx, cy, fr, col):
        d.polygon([(cx - fr, cy), (cx - fr * 0.55, cy - fr * 0.75),
                   (cx - fr * 0.12, cy - fr * 1.05), (cx, cy - fr * 1.5),
                   (cx + fr * 0.12, cy - fr * 1.05),
                   (cx + fr * 0.55, cy - fr * 0.75), (cx + fr, cy)],
                  fill=col)
    for fx, fr in [(66, 20), (100, 26), (136, 20), (166, 15)]:
        flame(x + fx, y + h - 58, fr, FLAME)
        flame(x + fx, y + h - 58, int(fr * 0.55), FLAME2)
    # smoke drifting up
    for sx, sy, sr in [(84, 30, 9), (120, 18, 11), (152, 26, 8)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(110, 108, 102))


def icon_akvan(d, x, y, w, h):
    """Cyclone spiral over the coast."""
    d.rectangle([x, y, x + w, y + h], fill=(206, 220, 228))
    cx, cy = x + w // 2 - 20, y + h // 2
    # spiral arms
    for turn in range(3):
        r0 = 14 + turn * 22
        d.arc([cx - r0, cy - r0, cx + r0, cy + r0],
              start=40 + turn * 55, end=300 + turn * 55,
              fill=(38, 84, 120) if turn % 2 == 0 else (120, 150, 175),
              width=9)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(240, 240, 230))
    # rain streaks
    for rx in range(14, w - 10, 22):
        d.line([(x + rx, y + h - 26), (x + rx - 6, y + h - 8)],
               fill=(90, 120, 150), width=3)
    # coastline + houses
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(150, 170, 130))
    for hx in (w - 66, w - 44, w - 22):
        d.rectangle([x + hx, y + h - 36, x + hx + 16, y + h - 22],
                    fill=(120, 90, 70))
        d.polygon([(x + hx - 2, y + h - 36), (x + hx + 18, y + h - 36),
                   (x + hx + 8, y + h - 46)], fill=RED)


def icon_trump(d, x, y, w, h):
    """A calendar page turned to 2027 with a clock."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    # calendar page (kept inside the 190px icon box)
    d.rectangle([x + 14, y + 12, x + 128, y + h - 12], fill=(255, 255, 255),
                outline=INK, width=3)
    d.rectangle([x + 14, y + 12, x + 128, y + 40], fill=RED)
    d.text((x + 26, y + 17), "JANUARY", font=font(SANS_B, 16),
           fill=(255, 255, 255))
    d.text((x + 26, y + 50), "2027", font=font(SERIF_B, 38), fill=INK)
    d.text((x + 26, y + 104), "DECISION", font=font(SANS_B, 14), fill=GREY)
    d.text((x + 26, y + 122), "DELAYED", font=font(SANS_B, 14), fill=GREY)
    # clock, bottom-right, clear of the text
    cx, cy, r = x + 160, y + h - 42, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=INK, width=3)
    d.line([(cx, cy), (cx, cy - 15)], fill=INK, width=3)
    d.line([(cx, cy), (cx + 11, cy + 5)], fill=INK, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=INK)


def icon_riyadh(d, x, y, w, h):
    """Riyadh skyline with interceptor bursts in the night sky."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 34, 52))
    # stars
    for sx, sy in [(20, 12), (60, 26), (110, 10), (170, 20), (180, 12),
                   (40, 44), (140, 40), (168, 46)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(240, 240, 220))
    # skyline with a tall tower (all inside the 190px icon box)
    base = y + h
    for bx, bw, bh in [(0, 32, 40), (34, 24, 58), (60, 28, 34),
                       (90, 20, 78), (112, 32, 44), (146, 26, 60),
                       (174, 16, 38)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(16, 18, 30))
        for wy in range(base - bh + 8, base - 6, 13):
            for wx in range(bx + 6, bx + bw - 5, 11):
                d.rectangle([x + wx, wy, x + wx + 4, wy + 5],
                            fill=(245, 200, 90))
    # missile arcs + interception bursts
    d.arc([x + 24, y + 8, x + 140, y + 108], 200, 330, fill=(255, 255, 255),
          width=3)
    d.arc([x + 96, y + 2, x + 186, y + 96], 210, 340, fill=(255, 255, 255),
          width=3)
    for cx, cy in [(x + 78, y + 46), (x + 158, y + 38)]:
        for r, col in [(12, FLAME2), (7, FLAME)]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer double border
    d.rectangle([14, 14, 1010, 1010], outline=INK, width=3)
    d.rectangle([20, 20, 1004, 1004], outline=INK, width=1)

    # masthead
    f_mast = font(SERIF_B, 74)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 34), title, font=f_mast, fill=INK)
    rule(d, 30, 128, 994, 3)
    rule(d, 30, 134, 994, 1)

    # dateline band: the date, loud and unmistakable
    d.rectangle([30, 144, 994, 196], fill=INK)
    f_date = font(SERIF_B, 40)
    date = "20 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 148), date, font=f_date, fill=(255, 255, 255))
    f_day = font(SANS_B, 18)
    d.text((44, 158), "FRIDAY", font=f_day, fill=(255, 255, 255))
    right = "WORLD EDITION"
    d.text((980 - d.textlength(right, font=f_day), 158), right,
           font=f_day, fill=(255, 255, 255))

    # ---- lead story: Kyiv (full width)
    lx, ly, lw, lh = 30, 210, 964, 252
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=INK, width=2)
    icon_kyiv(d, lx + 2, ly + 2, 330, lh - 4)
    tx = lx + 352
    f_kick = font(SANS_B, 17)
    d.text((tx, ly + 16), "UKRAINE  •  LEAD STORY", font=f_kick, fill=RED)
    f_head = font(SERIF_B, 40)
    head = wrap(d, "KYIV STRUCK BY BALLISTIC MISSILES", f_head, lw - 372)
    y = text_block(d, tx, ly + 44, head, f_head, leading=46)
    rule(d, tx, y + 8, lx + lw - 18, 1)
    f_body = font(SERIF, 20)
    body = wrap(d, "Fires broke out across districts after overnight "
                   "strikes; blasts were heard in the early hours "
                   "of Friday.", f_body, lw - 372)
    text_block(d, tx, y + 20, body, f_body, leading=26)

    # ---- row 2: three panels
    cols3 = [(30, 316), (360, 316), (690, 316)]
    stories3 = [
        ("ITALY", "DRONES SHUT GENOA AIRPORT",
         "Unknown drones near the runway halted flights; the "
         "airport reopened after safety checks.", icon_genoa),
        ("STRAIT OF HORMUZ", "TANKER BURNS AFTER MINE STRIKE",
         "Iran's navy says a tanker caught fire east of the "
         "strait; oil prices rose on the news.", icon_hormuz),
        ("INDIA", "CYCLONE AKVAN HITS ODISHA",
         "300,000 people evacuated as the storm made landfall "
         "near Gopalpur; trains cancelled.", icon_akvan),
    ]
    py, ph = 478, 258
    for (px, pw), (kick, head, body, icon) in zip(cols3, stories3):
        d.rectangle([px, py, px + pw, py + ph], outline=INK, width=2)
        icon(d, px + 2, py + 2, pw - 4, 108)
        f_k = font(SANS_B, 15)
        d.text((px + 12, py + 120), kick, font=f_k, fill=RED)
        f_h = font(SERIF_B, 23)
        lines = wrap(d, head, f_h, pw - 24)
        y = text_block(d, px + 12, py + 142, lines, f_h, leading=27)
        f_b = font(SANS, 15)
        blines = wrap(d, body, f_b, pw - 24)
        text_block(d, px + 12, y + 6, blines, f_b, leading=19)

    # ---- row 3: two panels
    cols2 = [(30, 474), (530, 474)]
    stories2 = [
        ("WASHINGTON", "TRUMP PUTS IRAN DECISION OFF TO 2027",
         "Trump says he is \u201cnot rushing\u201d any decision on new "
         "strikes against Iran: \u201cWe\u2019ll see what happens after "
         "January 1.\u201d", icon_trump),
        ("SAUDI ARABIA", "HOUTHI MISSILES TARGET RIYADH",
         "The Saudi-led coalition says it intercepted missiles "
         "and drones aimed at the capital and the south; debris "
         "fell on Riyadh.", icon_riyadh),
    ]
    py2, ph2 = 752, 226
    for (px, pw), (kick, head, body, icon) in zip(cols2, stories2):
        d.rectangle([px, py2, px + pw, py2 + ph2], outline=INK, width=2)
        icon(d, px + 2, py2 + 2, 190, ph2 - 4)
        ix = px + 204
        f_k = font(SANS_B, 15)
        d.text((ix, py2 + 14), kick, font=f_k, fill=RED)
        f_h = font(SERIF_B, 24)
        lines = wrap(d, head, f_h, pw - 216)
        y = text_block(d, ix, py2 + 38, lines, f_h, leading=28)
        rule(d, ix, y + 6, px + pw - 14, 1)
        f_b = font(SANS, 15)
        blines = wrap(d, body, f_b, pw - 216)
        text_block(d, ix, y + 16, blines, f_b, leading=19)

    # footer: restate the day, so the date survives any crop of the masthead
    f_f = font(SANS, 13)
    foot = ("All six stories happened, or were first reported, "
            "on Friday 20 November 2026.")
    fw = d.textlength(foot, font=f_f)
    d.text(((W - fw) / 2, 986), foot, font=f_f, fill=GREY)

    img.save("entry.png", "PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()

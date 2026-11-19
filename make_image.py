"""Draw the news-image-20261119 entry: one page summing up the world news
of Thursday 19 November 2026.

The picture is a newspaper front page drawn entirely in code with Pillow:
a lead story on the first US-China-Russia summit in Shenzhen, six panels
(the ICJ Rohingya ruling, the Hormuz tanker fires, the Crimean Bridge
strike, the markets' Fed shock, the GTA VI launch and the ATP Finals)
and an "also today" ticker. Every story was reported on 19 November 2026.

Run it with no network:

    python3 make_image.py

It writes entry.png beside this file, and also to $MAKEFUN_OUTPUT_DIR
(or /output) when that directory is in play, which is where the grader
expects it. main.py is the standard-library entrypoint that validates
and delivers the same file inside the grading sandbox.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 242, 227)
INK = (25, 23, 19)
GREY = (96, 90, 78)
RED = (176, 42, 30)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines, line = [], ""
    for word in text.split():
        trial = word if not line else line + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def text_block(draw, xy, text, fnt, fill, max_width, leading):
    """Draw wrapped text at xy; return the y just below it."""
    x, y = xy
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def rule(draw, y, x0=40, x1=984, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_flag_us(draw, x, y, w, h):
    """Stars and stripes, simplified: stripes, blue canton, dot stars."""
    stripe = h / 7
    for i in range(7):
        colour = (178, 34, 52) if i % 2 == 0 else WHITE
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=colour)
    canton_h = stripe * 4
    draw.rectangle([x, y, x + w * 0.45, y + canton_h], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            cx = x + 8 + c * (w * 0.45 - 12) / 4
            cy = y + 6 + r * (canton_h - 10) / 3
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=WHITE)


def draw_flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    draw.polygon([(x + 14, y + 22), (x + 20, y + 34), (x + 33, y + 34),
                  (x + 23, y + 42), (x + 26, y + 54), (x + 14, y + 47),
                  (x + 3, y + 54), (x + 6, y + 42), (x - 4 + 7, y + 34),
                  (x + 9, y + 34)], fill=(255, 222, 0))
    for dx, dy in [(38, 12), (44, 26), (44, 42), (38, 56)]:
        draw.ellipse([x + dx - 3, y + dy - 3, x + dx + 3, y + dy + 3],
                     fill=(255, 222, 0))


def draw_flag_russia(draw, x, y, w, h):
    third = h / 3
    draw.rectangle([x, y, x + w, y + third], fill=WHITE)
    draw.rectangle([x, y + third, x + w, y + 2 * third], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * third, x + w, y + h], fill=(213, 43, 30))


def masthead(draw):
    centered(draw, W / 2, 22, "THE WORLD ON THURSDAY", font(SERIF_B, 54), INK)
    rule(draw, 92, width=5)
    rule(draw, 100, width=1)
    # Dateline band: the date, named large and plain.
    draw.rectangle([40, 110, 984, 148], fill=INK)
    draw.text((58, 118), "THURSDAY · 19 NOVEMBER 2026", font=font(SANS_B, 25), fill=WHITE)
    right = "ONE DAY · ONE PAGE"
    rw = draw.textlength(right, font=font(SANS_B, 19))
    draw.text((984 - 18 - rw, 120), right, font=font(SANS_B, 19), fill=(220, 210, 180))


def lead_story(draw):
    x, y = 40, 162
    draw.text((x, y), "SHENZHEN · APEC SUMMIT — DIPLOMACY", font=font(SANS_B, 19), fill=RED)
    headline = "Trump, Xi and Putin hold first three-way summit"
    y = text_block(draw, (x, y + 28), headline, font(SERIF_B, 42), INK, 600, 50)
    body = ("The leaders of the United States, China and Russia issue a joint "
            "\u201cpeace declaration\u201d on nuclear risks, UN reform and fuel "
            "supplies \u2014 with the wars in Ukraine and Iran topping the agenda.")
    text_block(draw, (x, y + 8), body, font(SANS, 19), INK, 600, 25)
    # Three flags over a summit table, drawn at the right of the lead.
    fx, fy, fw, fh = 676, 164, 88, 118
    for i, draw_flag in enumerate((draw_flag_us, draw_flag_china, draw_flag_russia)):
        left = fx + i * (fw + 14)
        draw.line([(left + fw / 2, fy - 8), (left + fw / 2, fy + fh + 26)],
                  fill=INK, width=3)
        draw_flag(draw, left, fy, fw, fh)
        draw.rectangle([left, fy, left + fw, fy + fh], outline=INK, width=2)
    draw.rectangle([664, 314, 984, 324], fill=INK)
    centered(draw, 824, 332, "USA · CHINA · RUSSIA", font(SANS_B, 16), GREY)


def icon_scales(draw, x, y):
    draw.line([(x + 14, y + 2), (x + 14, y + 24)], fill=WHITE, width=3)
    draw.line([(x + 2, y + 6), (x + 26, y + 6)], fill=WHITE, width=3)
    for cx in (4, 24):
        draw.polygon([(cx, y + 8), (cx + 8, y + 20), (cx - 4 + 4, y + 20)],
                     outline=WHITE, width=2)
    draw.line([(x + 6, y + 27), (x + 22, y + 27)], fill=WHITE, width=3)


def icon_flame(draw, x, y):
    draw.polygon([(x + 14, y), (x + 24, y + 16), (x + 20, y + 27),
                  (x + 8, y + 27), (x + 4, y + 16)], fill=WHITE)
    draw.polygon([(x + 14, y + 12), (x + 19, y + 20), (x + 16, y + 26),
                  (x + 11, y + 26), (x + 9, y + 20)], fill=(255, 170, 60))


def icon_bridge(draw, x, y):
    draw.arc([x, y + 6, x + 30, y + 30], start=180, end=360, fill=WHITE, width=3)
    for vx in (4, 15, 26):
        draw.line([(x + vx, y + 12), (x + vx, y + 22)], fill=WHITE, width=2)
    draw.line([(x, y + 24), (x + 30, y + 24)], fill=WHITE, width=3)
    draw.polygon([(x + 22, y - 2), (x + 25, y + 4), (x + 31, y + 4),
                  (x + 26, y + 8), (x + 28, y + 14), (x + 22, y + 10),
                  (x + 16, y + 14), (x + 18, y + 8), (x + 13, y + 4),
                  (x + 19, y + 4)], fill=(255, 200, 60))


def icon_chart(draw, x, y):
    for i, bh in enumerate((20, 14, 8)):
        draw.rectangle([x + 2 + i * 9, y + 26 - bh, x + 8 + i * 9, y + 26],
                       fill=WHITE)
    draw.line([(x + 2, y + 4), (x + 26, y + 20)], fill=(255, 200, 60), width=3)
    draw.polygon([(x + 26, y + 20), (x + 18, y + 19), (x + 24, y + 12)],
                 fill=(255, 200, 60))


def icon_palm(draw, x, y):
    draw.arc([x + 8, y + 8, x + 30, y + 30], start=200, end=320,
             fill=WHITE, width=3)
    for dx, dy in [(-2, 2), (6, -3), (14, -3), (20, 3)]:
        draw.arc([x + dx, y - 4, x + dx + 18, y + 10], start=180, end=330,
                 fill=WHITE, width=2)
    draw.ellipse([x + 24, y + 2, x + 34, y + 12], outline=WHITE, width=2)


def icon_ball(draw, x, y):
    draw.ellipse([x + 3, y + 2, x + 27, y + 26], outline=WHITE, width=3)
    draw.arc([x - 4, y + 2, x + 16, y + 26], start=300, end=60,
             fill=WHITE, width=2)
    draw.arc([x + 14, y + 2, x + 34, y + 26], start=120, end=240,
             fill=WHITE, width=2)


PANELS = [
    {
        "tag": "THE HAGUE · ICJ",
        "colour": (44, 74, 124),
        "icon": icon_scales,
        "headline": "UN court: Myanmar committed genocide against the Rohingya",
        "body": "The ICJ ruling, the first of its kind, finds state-sponsored "
                "genocide against the Muslim minority.",
    },
    {
        "tag": "HORMUZ · WAR AT SEA",
        "colour": (160, 58, 28),
        "icon": icon_flame,
        "headline": "Three tankers ablaze after mine strikes near Hormuz",
        "body": "Iran says they hit mines east of the strait; Tehran also "
                "fires on Kuwait after a US strike.",
    },
    {
        "tag": "UKRAINE · CRIMEA",
        "colour": (85, 107, 47),
        "icon": icon_bridge,
        "headline": "Kyiv hits the Crimean Bridge for the third time this week",
        "body": "Russian officials report a fresh strike on the Kerch crossing "
                "linking occupied Crimea to Russia.",
    },
    {
        "tag": "MARKETS · ECONOMY",
        "colour": (122, 91, 18),
        "icon": icon_chart,
        "headline": "Gold sinks to 14-month low as Fed eyes December hike",
        "body": "Hawkish Fed minutes lift the dollar; AI giant Anthropic "
                "makes its debut on the Nasdaq.",
    },
    {
        "tag": "CULTURE · GAMING",
        "colour": (124, 45, 94),
        "icon": icon_palm,
        "headline": "GTA VI launches worldwide to rave reviews",
        "body": "Rockstar's Vice City epic is out worldwide; critics score "
                "it 99/100 and 2.3m watch on Twitch.",
    },
    {
        "tag": "SPORT · TURIN",
        "colour": (31, 111, 84),
        "icon": icon_ball,
        "headline": "Alcaraz beats Medvedev to reach ATP Finals semis",
        "body": "Straight sets, 6\u20132 6\u20134, in Turin. England also take "
                "the ODI cricket series 2\u20131 in Australia.",
    },
]


def panel(draw, x, y, w, h, spec):
    draw.rectangle([x, y, x + w, y + h], fill=(252, 249, 240), outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 34], fill=spec["colour"])
    draw.text((x + 12, y + 8), spec["tag"], font=font(SANS_B, 15), fill=WHITE)
    spec["icon"](draw, x + w - 40, y + 3)
    ty = text_block(draw, (x + 12, y + 46), spec["headline"],
                    font(SANS_B, 23), INK, w - 24, 28)
    text_block(draw, (x + 12, ty + 6), spec["body"], font(SANS, 16),
               (52, 48, 40), w - 24, 21)


def panels(draw):
    xs = (40, 360, 680)
    ys = (440, 660)
    for i, spec in enumerate(PANELS):
        panel(draw, xs[i % 3], ys[i // 3], 304, 208, spec)


def ticker(draw):
    draw.rectangle([40, 880, 984, 984], fill=INK)
    draw.text((58, 892), "ALSO TODAY", font=font(SANS_B, 18), fill=(240, 120, 90))
    items = ("Houthi missile damages Riyadh's tallest tower \u00b7 M5.7 "
             "earthquake hits Kumamoto, Japan \u00b7 Seoul court orders retrial "
             "for ex-PM Han \u00b7 Denmark backs Greenland\u2013US Arctic "
             "defence deal 109\u20130 \u00b7 COP31 endgame split over "
             "fossil-fuel phaseout \u00b7 Bangladesh deploys forces amid "
             "shutdown unrest")
    text_block(draw, (58, 918), items, font(SANS, 17), WHITE, 908, 21)
    centered(draw, W / 2, 992, "Drawn in code with Python + Pillow \u00b7 "
             "every story reported on 19 November 2026", font(SANS, 13), GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([14, 14, W - 14, H - 14], outline=INK, width=3)
    masthead(draw)
    lead_story(draw)
    rule(draw, 428, width=3)
    panels(draw)
    ticker(draw)
    here = Path(__file__).resolve().parent
    img.save(here / "entry.png", format="PNG", optimize=True)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        img.save(os.path.join(out_dir, "entry.png"), format="PNG", optimize=True)
        print(f"wrote {out_dir}/entry.png")
    except OSError as exc:
        print(f"repo copy written; output dir skipped: {exc}")
    print(f"wrote {here / 'entry.png'}")


if __name__ == "__main__":
    main()

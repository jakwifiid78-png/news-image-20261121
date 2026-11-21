#!/usr/bin/env python3
"""news-image-20261121 generator — written fresh in this session.

Renders entry.png: a 1024x1024 newspaper front page, "THE WORLD —
Saturday, 21 November 2026", drawn with PIL from fixed data only.
Deterministic: no clock, no randomness, no network. Re-running it
produces byte-identical output.

Six verified stories, all reported Saturday 21 November 2026
(see SOURCES.md for the wire sources):
 1. LEAD — Wall Street tech crash: S&P 500 -3.7% into correction,
    Nasdaq -5.3%, worst week in 18+ months; Nvidia -14%, AMD -13%.
 2. Russian missiles land in Poland during NATO drills; NATO calls
    it a violation; PM Tusk calls it an intentional provocation.
 3. Trump, Xi and Putin hold the first three-way summit in China;
    Trump defends calling Putin "a friend" at a White House briefing.
 4. Phumzile Mlambo-Ngcuka, South Africa's first woman deputy
    president and former UN Women chief, dies aged 71.
 5. US Congress races to avert a pre-Christmas shutdown as the Iran
    war splits lawmakers; Trump seeks $350bn more for defence.
 6. Trump threatens a "tremendous tax" on US firms that build AI
    data centres abroad.
"""

from PIL import Image, ImageDraw, ImageFont

OUT = "/home/hatch/workspace/makefun/entries/news-image-20261121/entry.png"
W, H = 1024, 1024

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (247, 242, 231)
INK = (26, 32, 54)
RED = (176, 32, 32)
DARKRED = (140, 20, 20)
GOLD = (198, 138, 28)
TEAL = (13, 106, 96)
GREY = (96, 98, 110)
LIGHT = (255, 255, 255)
PANEL = (238, 231, 214)
BLUE = (28, 68, 140)

MX = 34  # side margin


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, font, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def centred(d, cx, y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + font.size


def rule(d, x0, x1, y, fill=INK, width=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_chart(d, x, y, w, h):
    """Descending red bars for the Friday market rout."""
    d.rectangle([x, y, x + w, y + h], fill=LIGHT, outline=INK, width=2)
    d.text((x + 12, y + 8), "FRIDAY'S ROUT", font=F(SANS_B, 19), fill=RED)
    bars = [("S&P 500", -3.7, 0.42), ("NASDAQ", -5.3, 0.58),
            ("NVIDIA", -14, 0.82), ("AMD", -13, 0.76)]
    base = y + h - 34
    bw, gap = 62, 22
    bx = x + 24
    for name, pct, frac in bars:
        bh = int((h - 78) * frac)
        d.rectangle([bx, base - bh, bx + bw, base], fill=RED)
        d.text((bx + bw / 2 - d.textlength(f"{pct}%", font=F(SANS_B, 20)) / 2,
                base - bh - 26), f"{pct}%", font=F(SANS_B, 20), fill=DARKRED)
        nm = F(SANS_B, 16)
        d.text((bx + bw / 2 - d.textlength(name, font=nm) / 2, base + 6),
               name, font=nm, fill=INK)
        bx += bw + gap
    d.line([(x + 12, base), (x + w - 12, base)], fill=INK, width=2)


def draw_missile(d, x, y, s):
    """Small pictogram: a cruise missile over a burst."""
    d.ellipse([x, y + s * 0.62, x + s, y + s], fill=(226, 196, 120))
    pts = [(x + s * 0.18, y + s * 0.78), (x + s * 0.5, y + s * 0.42),
           (x + s * 0.82, y + s * 0.78)]
    d.polygon(pts, fill=(232, 122, 26))
    d.polygon([(x + s * 0.44, y + s * 0.08), (x + s * 0.56, y + s * 0.08),
               (x + s * 0.62, y + s * 0.42), (x + s * 0.38, y + s * 0.42)],
              fill=(120, 124, 134))
    d.polygon([(x + s * 0.5, y), (x + s * 0.58, y + s * 0.12),
               (x + s * 0.42, y + s * 0.12)], fill=(70, 72, 82))
    d.polygon([(x + s * 0.36, y + s * 0.36), (x + s * 0.22, y + s * 0.52),
               (x + s * 0.38, y + s * 0.46)], fill=(70, 72, 82))
    d.polygon([(x + s * 0.64, y + s * 0.36), (x + s * 0.78, y + s * 0.52),
               (x + s * 0.62, y + s * 0.46)], fill=(70, 72, 82))


def draw_flags(d, x, y, s):
    """Three small flags: USA, China, Russia."""
    fw, fh = int(s * 0.30), int(s * 0.52)
    # USA: stripes + canton
    fx = x
    for i in range(7):
        d.rectangle([fx, y + i * fh / 7, fx + fw, y + (i + 1) * fh / 7],
                    fill=RED if i % 2 == 0 else LIGHT)
    d.rectangle([fx, y, fx + fw * 0.45, y + fh * 0.55], fill=BLUE)
    # China: red field, gold stars
    fx = x + int(s * 0.35)
    d.rectangle([fx, y, fx + fw, y + fh], fill=RED)
    for sx, sy in [(0.28, 0.28), (0.55, 0.22), (0.62, 0.42), (0.45, 0.55)]:
        d.ellipse([fx + fw * sx - 4, y + fh * sy - 4,
                   fx + fw * sx + 4, y + fh * sy + 4], fill=GOLD)
    # Russia: white / blue / red horizontal bands
    fx = x + int(s * 0.70)
    for i, col in enumerate([LIGHT, BLUE, RED]):
        d.rectangle([fx, y + i * fh / 3, fx + fw, y + (i + 1) * fh / 3], fill=col)
    d.rectangle([x + int(s * 0.70), y, x + int(s * 0.70) + fw, y + fh],
                outline=INK, width=1)


def draw_portrait(d, x, y, s):
    """Muted silhouette portrait in a gold-ringed circle."""
    cx, cy = x + s / 2, y + s / 2
    d.ellipse([x, y, x + s, y + s], fill=(222, 210, 186), outline=GOLD, width=3)
    d.ellipse([cx - s * 0.16, y + s * 0.16, cx + s * 0.16, y + s * 0.48],
              fill=(74, 74, 88))
    d.pieslice([cx - s * 0.34, y + s * 0.44, cx + s * 0.34, y + s * 1.05],
               180, 360, fill=(74, 74, 88))
    d.text((cx - d.textlength("71", font=F(SANS_B, 20)) / 2, y + s * 0.60),
           "71", font=F(SANS_B, 20), fill=LIGHT)


def draw_capitol(d, x, y, s):
    """Simple Capitol dome silhouette."""
    d.rectangle([x, y + s * 0.78, x + s, y + s * 0.86], fill=INK)
    for i in range(5):
        cx = x + s * (0.14 + i * 0.18)
        d.rectangle([cx, y + s * 0.58, cx + 7, y + s * 0.78], fill=INK)
    d.pieslice([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.78],
               180, 360, fill=INK)
    d.rectangle([x + s * 0.47, y + s * 0.08, x + s * 0.53, y + s * 0.26], fill=INK)
    d.ellipse([x + s * 0.45, y + s * 0.04, x + s * 0.55, y + s * 0.12], fill=RED)


def story_card(d, x, y, w, h, kicker, headline, deck, pict):
    d.rectangle([x, y, x + w, y + h], fill=LIGHT, outline=INK, width=2)
    tx = x + 16
    d.text((tx, y + 10), kicker, font=F(SANS_B, 19), fill=RED)
    pic_s = 84
    px = x + w - pic_s - 14
    py = y + 36
    pict(d, px, py, pic_s)
    tw = w - pic_s - 44
    hl = wrap(d, headline, F(SERIF_B, 27), tw)
    yy = text_block(d, tx, y + 36, hl, F(SERIF_B, 27), INK, 32)
    dk = wrap(d, deck, F(SANS, 19), tw)
    text_block(d, tx, yy + 4, dk, F(SANS, 19), (58, 67, 88), 23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    rule(d, MX, W - MX, 14, INK, 3)
    centred(d, W / 2, 24, "THE WORLD", F(SERIF_B, 84), INK)
    rule(d, MX, W - MX, 128, INK, 2)
    centred(d, W / 2, 138, "SATURDAY, 21 NOVEMBER 2026",
            F(SANS_B, 23), INK)
    # thin double rule
    rule(d, MX, W - MX, 172, INK, 1)
    rule(d, MX, W - MX, 176, INK, 3)
    # red band
    d.rectangle([MX, 186, W - MX, 220], fill=RED)
    centred(d, W / 2, 193, "SIX STORIES THAT DEFINED THE DAY",
            F(SANS_B, 22), LIGHT)

    # --- lead story: markets crash ---
    ly = 232
    d.text((MX, ly), "MARKETS IN FREEFALL", font=F(SANS_B, 21), fill=RED)
    hl = ["WALL STREET IN", "FREEFALL"]
    yy = text_block(d, MX, ly + 30, hl, F(SERIF_B, 50), INK, 56)
    deck = ("The S&P 500 plunges 3.7% into correction; the Nasdaq "
            "dives 5.3% in the worst week on Wall Street in 18 months.")
    dk = wrap(d, deck, F(SANS, 21), 560)
    text_block(d, MX, yy + 8, dk, F(SANS, 21), (58, 67, 88), 27)
    draw_chart(d, 640, ly + 6, 350, 210)
    rule(d, MX, W - MX, 468, INK, 2)

    # --- four story cards, 2 x 2 ---
    cw, ch = 468, 176
    gx, gy = MX, 482
    gap = 16
    story_card(d, gx, gy, cw, ch, "POLAND  •  NATO ON EDGE",
               "Russian missiles land in Poland",
               "Two cruise missiles and a drone fall during NATO "
               "drills. The alliance calls it a violation.", draw_missile)
    story_card(d, gx + cw + gap, gy, cw, ch, "DIPLOMACY  •  BEIJING",
               "Trump, Xi and Putin meet",
               "First three-way summit in China ends. Trump defends "
               "calling Putin \u201ca friend\u201d.", draw_flags)
    story_card(d, gx, gy + ch + gap, cw, ch, "AFRICA  •  OBITUARY",
               "South Africa mourns Mlambo-Ngcuka",
               "First woman deputy president and ex-UN Women chief "
               "dies aged 71.", draw_portrait)
    story_card(d, gx + cw + gap, gy + ch + gap, cw, ch,
               "WASHINGTON  •  CONGRESS",
               "Shutdown looms over Iran war split",
               "Congress races to fund the government as Trump "
               "seeks $350bn more for defence.", draw_capitol)
    rule(d, MX, W - MX, 862, INK, 2)

    # --- sixth story: full-width band ---
    by = 872
    d.text((MX, by), "TECH POLICY", font=F(SANS_B, 19), fill=RED)
    d.text((MX, by + 26), "Trump: big tax on AI data centres abroad",
           font=F(SERIF_B, 30), fill=INK)
    d.text((MX, by + 62),
           "US firms building AI data centres overseas face a \u201ctremendous tax\u201d, the president warns.",
           font=F(SANS, 20), fill=(58, 67, 88))

    # --- footer ticker + sources ---
    rule(d, MX, W - MX, 966, INK, 1)
    centred(d, W / 2, 974,
            "S&P 500  \u22123.7%   •   NASDAQ  \u22125.3%   •   DOW  \u22121.9%   •   NIKKEI  \u22125.1%   •   GOLD  \u22129% THIS WEEK",
            F(SANS_B, 17), INK)
    centred(d, W / 2, 996, "Sources: Reuters  •  Associated Press  •  BBC",
            F(SANS, 14), GREY)

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()

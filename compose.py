"""Build the news-image entry for Saturday 21 November 2026.

Takes the five photo panels in panels/ (kyiv, markets, trump, chapo,
cop31) and lays them out as a one-page newspaper front page, with the
day's headlines drawn in PIL so every word is spelled exactly as
written here. Output is entry.jpg, 1024x1024, under 1 MiB.

Run: python3 compose.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (253, 251, 247)
INK = (17, 17, 17)
MUTED = (85, 85, 85)
ACCENT = (155, 44, 44)
RULE = (17, 17, 17)
HAIR = (204, 204, 204)

SERIF_B = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def load_font(path, size):
    return ImageFont.truetype(path, size)


def load_panel(name):
    path = os.path.join(HERE, 'panels', f'{name}.webp')
    if not os.path.exists(path):
        raise SystemExit(f'no panel image: {path}')
    return Image.open(path).convert('RGB')


def crop_resize(im, w, h):
    """Center-crop to the target aspect ratio, then resize to w x h."""
    target = w / h
    ratio = im.width / im.height
    if ratio > target:
        nw = int(im.height * target)
        x = (im.width - nw) // 2
        im = im.crop((x, 0, x + nw, im.height))
    else:
        nh = int(im.width / target)
        y = (im.height - nh) // 2
        im = im.crop((0, y, im.width, y + nh))
    return im.resize((w, h), Image.LANCZOS)


def wrap_text(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ''
    for word in words:
        trial = f'{cur} {word}'.strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def build():
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 16
    cw = W - 2 * mx

    # --- masthead ---
    title = 'THE WORLD IN ONE DAY'
    tf = load_font(SERIF_B, 46)
    d.text(((W - d.textlength(title, font=tf)) / 2, 10), title, font=tf, fill=INK)
    date = 'SATURDAY, 21 NOVEMBER 2026'
    df = load_font(SANS_B, 19)
    d.text(((W - d.textlength(date, font=df)) / 2, 62), date, font=df, fill=INK)
    d.line([(mx, 88), (W - mx, 88)], fill=RULE, width=2)

    # --- lead story: Russia's biggest strike on Kyiv ---
    lead = crop_resize(load_panel('kyiv'), cw, 330)
    img.paste(lead, (mx, 96))
    y = 434
    kf = load_font(SANS_B, 14)
    d.text((mx, y), 'WAR IN UKRAINE  •  LEAD STORY', font=kf, fill=ACCENT)
    y += 22
    hf = load_font(SERIF_B, 38)
    d.text((mx, y), "RUSSIA'S BIGGEST STRIKE HITS KYIV", font=hf, fill=INK)
    y += 48
    sf = load_font(SANS, 19)
    d.text((mx, y), '400+ drones and 110 missiles overnight; 9 killed, bridges hit, debris falls in Poland.', font=sf, fill=MUTED)
    d.line([(mx, 540), (W - mx, 540)], fill=RULE, width=2)

    # --- two-column rows ---
    col_w = (cw - 16) // 2
    col_x = [mx, mx + col_w + 16]
    rows = [
        (548, [
            ('markets', 'WALL STREET IN CORRECTION',
             'S&P -3.7%, Nasdaq -5.28%; Nvidia -14% as the AI rout deepens.'),
            ('trump', 'TRUMP PRESSES EUROPE ON UKRAINE',
             'Spend the money at home if a deal is reached, he tells leaders.'),
        ]),
        (772, [
            ('chapo', "'EL CHAPO ISIDRO' CAPTURED",
             'FBI Top-10 fugitive seized in Sinaloa; 11 killed, 8 arrested.'),
            ('cop31', 'COP31 SPILLS INTO OVERTIME',
             'Draft drops all fossil-fuel mention; EU says good deal or no deal.'),
        ]),
    ]
    for top, cols in rows:
        for i, (name, headline, sub) in enumerate(cols):
            x = col_x[i]
            pic = crop_resize(load_panel(name), col_w, 118)
            img.paste(pic, (x, top))
            hy = top + 126
            hfont = load_font(SERIF_B, 21)
            d.text((x, hy), headline, font=hfont, fill=INK)
            sfont = load_font(SANS, 15)
            for j, line in enumerate(wrap_text(d, sub, sfont, col_w)):
                d.text((x, hy + 28 + j * 19), line, font=sfont, fill=MUTED)
        d.line([(mx, top + 208), (W - mx, top + 208)], fill=HAIR, width=1)

    # --- bottom strip ---
    strip = "ALSO TODAY:  Anthropic -8.5% to $88.90  ·  Two tankers hit in the Strait of Hormuz  ·  UK-EU youth mobility deal: 100,000 a year"
    sfont = load_font(SANS, 15)
    d.text(((W - d.textlength(strip, font=sfont)) / 2, 994), strip, font=sfont, fill=INK)

    jpg_path = os.path.join(HERE, 'entry.jpg')
    img.save(jpg_path, quality=92)
    print(f'entry.jpg (q92): {os.path.getsize(jpg_path)} bytes')
    print('limit: 1048576 bytes, 1024x1024')


if __name__ == '__main__':
    build()

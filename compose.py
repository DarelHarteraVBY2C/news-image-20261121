"""Render the 21 November 2026 news-image entry.

The five photo panels live in panels/ (kyiv, markets, trump, chapo,
cop31). This script arranges them as a newspaper front page and draws
the day's headlines with PIL, so the wording is exactly what is written
below. The result is entry.jpg, 1024 by 1024, under one mebibyte.

Run it with: python3 compose.py
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
CANVAS = (1024, 1024)

PALETTE = {
    'paper': (253, 251, 247),
    'ink': (17, 17, 17),
    'soft': (85, 85, 85),
    'red': (155, 44, 44),
    'rule': (17, 17, 17),
    'hair': (204, 204, 204),
}

FONTS = {
    'serif': '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
    'sans': '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    'sans_bold': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
}

MARGIN = 16
CONTENT_W = CANVAS[0] - 2 * MARGIN


def font(kind, size):
    return ImageFont.truetype(FONTS[kind], size)


def picture(name):
    path = os.path.join(BASE, 'panels', name + '.webp')
    if not os.path.exists(path):
        raise SystemExit('missing panel: ' + path)
    return Image.open(path).convert('RGB')


def fit(image, width, height):
    """Crop the middle of the picture to the wanted shape, then scale it."""
    want = width / height
    got = image.width / image.height
    if got > want:
        keep = int(image.height * want)
        left = (image.width - keep) // 2
        image = image.crop((left, 0, left + keep, image.height))
    else:
        keep = int(image.width / want)
        top = (image.height - keep) // 2
        image = image.crop((0, top, image.width, top + keep))
    return image.resize((width, height), Image.LANCZOS)


def draw_wrapped(pen, text, fnt, x, y, width, colour, leading=19):
    """Draw text folded to fit inside width; returns the y below the last line."""
    for line in textwrap.wrap(text, width=60):
        # Measure with the real font and re-fold when the guess is too wide.
        while pen.textlength(line, font=fnt) > width and ' ' in line:
            cut = line.rfind(' ')
            line, rest = line[:cut], line[cut + 1:]
            pen.text((x, y), line, font=fnt, fill=colour)
            y += leading
            line = rest
        pen.text((x, y), line, font=fnt, fill=colour)
        y += leading
    return y


def main():
    page = Image.new('RGB', CANVAS, PALETTE['paper'])
    pen = ImageDraw.Draw(page)

    # Masthead: paper name, then the date, then a heavy rule.
    name = 'THE WORLD IN ONE DAY'
    name_font = font('serif', 46)
    pen.text(((CANVAS[0] - pen.textlength(name, font=name_font)) / 2, 10),
             name, font=name_font, fill=PALETTE['ink'])
    day = 'SATURDAY, 21 NOVEMBER 2026'
    day_font = font('sans_bold', 19)
    pen.text(((CANVAS[0] - pen.textlength(day, font=day_font)) / 2, 62),
             day, font=day_font, fill=PALETTE['ink'])
    pen.line([(MARGIN, 88), (CANVAS[0] - MARGIN, 88)], fill=PALETTE['rule'], width=2)

    # Lead story, full width: picture, kicker, headline, standfirst.
    page.paste(fit(picture('kyiv'), CONTENT_W, 330), (MARGIN, 96))
    pen.text((MARGIN, 434), 'WAR IN UKRAINE  •  LEAD STORY',
             font=font('sans_bold', 14), fill=PALETTE['red'])
    pen.text((MARGIN, 456), "RUSSIA'S BIGGEST STRIKE HITS KYIV",
             font=font('serif', 38), fill=PALETTE['ink'])
    pen.text((MARGIN, 504),
             '400+ drones and 110 missiles overnight; 9 killed, bridges hit, debris falls in Poland.',
             font=font('sans', 19), fill=PALETTE['soft'])
    pen.line([(MARGIN, 540), (CANVAS[0] - MARGIN, 540)], fill=PALETTE['rule'], width=2)

    # The four smaller stories, two to a row.
    half = (CONTENT_W - 16) // 2
    left_x = MARGIN
    right_x = MARGIN + half + 16
    stories = [
        (548, left_x, 'markets', 'WALL STREET IN CORRECTION',
         'S&P -3.7%, Nasdaq -5.28%; Nvidia -14% as the AI rout deepens.'),
        (548, right_x, 'trump', 'TRUMP PRESSES EUROPE ON UKRAINE',
         'Spend the money at home if a deal is reached, he tells leaders.'),
        (772, left_x, 'chapo', "'EL CHAPO ISIDRO' CAPTURED",
         'FBI Top-10 fugitive seized in Sinaloa; 11 killed, 8 arrested.'),
        (772, right_x, 'cop31', 'COP31 SPILLS INTO OVERTIME',
         'Draft drops all fossil-fuel mention; EU says good deal or no deal.'),
    ]
    for top, x, image_name, headline, standfirst in stories:
        page.paste(fit(picture(image_name), half, 118), (x, top))
        pen.text((x, top + 126), headline, font=font('serif', 21), fill=PALETTE['ink'])
        draw_wrapped(pen, standfirst, font('sans', 15), x, top + 154, half,
                     PALETTE['soft'])
        pen.line([(MARGIN, top + 208), (CANVAS[0] - MARGIN, top + 208)],
                 fill=PALETTE['hair'], width=1)

    # Foot strip: three more items in one centred line.
    strip = ("ALSO TODAY:  Anthropic -8.5% to $88.90  ·  "
             "Two tankers hit in the Strait of Hormuz  ·  "
             "UK-EU youth mobility deal: 100,000 a year")
    strip_font = font('sans', 15)
    pen.text(((CANVAS[0] - pen.textlength(strip, font=strip_font)) / 2, 994),
             strip, font=strip_font, fill=PALETTE['ink'])

    out = os.path.join(BASE, 'entry.jpg')
    page.save(out, quality=92)
    print('entry.jpg (q92): {} bytes'.format(os.path.getsize(out)))
    print('limit: 1048576 bytes, 1024x1024')


if __name__ == '__main__':
    main()

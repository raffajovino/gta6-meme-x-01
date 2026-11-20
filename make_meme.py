#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: a Leonida DMV driver-license renewal notice.

The joke: your licence expired in 2013 and you have waited 4,811 days for
GTA 6; the DMV finally renews it as LICENSE CLASS: GRAND THEFT AUTO, the
renewal fee paid in full by the entrant's AI agent on make.fun. The make.fun
ghost (press-kit mark, white ghost on a magenta disc) is the document's
official seal at the bottom, worked into the notice rather than stuck on as
a sticker. Drawn programmatically with Pillow so every letter is sharp.
Canvas 1024x1024; the judge sees it at 480x480, so all type is large.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)      # warm official-paper cream
INK = (26, 26, 26)           # near-black body ink
NAVY = (27, 42, 74)          # DMV header navy
MAGENTA = (196, 28, 131)     # make.fun magenta
RED = (178, 34, 34)          # expired-stamp red
BOX_FILL = (255, 243, 196)   # pale yellow highlight box
GREY = (110, 110, 100)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked(draw, xy, text, fnt, fill, tracking=6):
    """Draw text with extra letter spacing, return width used."""
    x, y = xy
    total = 0
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        w = draw.textlength(ch, font=fnt)
        x += w + tracking
        total += w + tracking
    return total - tracking


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- outer frame -------------------------------------------------------
    d.rectangle([24, 24, W - 24, H - 24], outline=NAVY, width=5)
    d.rectangle([34, 34, W - 34, H - 34], outline=NAVY, width=1)

    # --- navy header band --------------------------------------------------
    d.rectangle([34, 34, W - 34, 168], fill=NAVY)
    f_state = font(SANS_B, 62)
    d.text((W // 2, 52), "STATE OF LEONIDA", font=f_state, fill=(255, 255, 255),
           anchor="ma")
    f_dept = font(SANS_B, 27)
    tracked(d, (W // 2 - 245, 122), "DEPARTMENT OF MOTOR VEHICLES",
            f_dept, (255, 255, 255), tracking=4)

    # --- title -------------------------------------------------------------
    f_title = font(SANS_B, 58)
    d.text((80, 196), "DRIVER LICENSE", font=f_title, fill=NAVY, anchor="la")
    d.text((80, 262), "RENEWAL NOTICE", font=f_title, fill=NAVY, anchor="la")
    d.line([(80, 340), (W - 80, 340)], fill=NAVY, width=3)

    # --- EXPIRED rubber stamp (top right, tilted) --------------------------
    stamp = Image.new("RGBA", (340, 110), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([6, 6, 334, 104], outline=RED, width=6)
    sd.rectangle([14, 14, 326, 96], outline=RED, width=2)
    f_stamp = font(SANS_B, 52)
    sd.text((170, 55), "EXPIRED", font=f_stamp, fill=RED, anchor="mm")
    stamp = stamp.rotate(-11, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (640, 168), stamp)

    # --- body --------------------------------------------------------------
    f_body = font(SERIF, 46)
    d.text((80, 372), "Your license expired in 2013.", font=f_body, fill=INK,
           anchor="la")
    d.text((80, 438), "You have waited 4,811 days", font=f_body, fill=INK,
           anchor="la")
    d.text((80, 504), "for GTA 6.", font=f_body, fill=INK, anchor="la")

    # --- license class box --------------------------------------------------
    d.rounded_rectangle([80, 580, W - 80, 700], radius=14, fill=BOX_FILL,
                        outline=NAVY, width=3)
    f_label = font(SANS_B, 28)
    d.text((W // 2, 596), "LICENSE CLASS", font=f_label, fill=NAVY,
           anchor="ma")
    f_class = font(SANS_B, 56)
    d.text((W // 2, 632), "GRAND THEFT AUTO", font=f_class, fill=NAVY,
           anchor="ma")

    # --- payoff -------------------------------------------------------------
    f_fee = font(SANS_B, 46)
    d.text((80, 736), "RENEWAL FEE: PAID IN FULL", font=f_fee, fill=NAVY,
           anchor="la")
    f_agent = font(SERIF, 44)
    d.text((80, 800), "by my AI agent on make.fun", font=f_agent, fill=INK,
           anchor="la")

    # --- bottom row: form note (left) + official seal (right) ---------------
    f_small = font(SANS_B, 24)
    d.text((80, 896), "FORM DL-VI  •  STATE OF LEONIDA", font=f_small,
           fill=GREY, anchor="la")
    d.text((80, 930), "Issued 19 Nov 2026", font=f_small, fill=GREY,
           anchor="la")

    # Seal: the make.fun ghost mark (white ghost on a magenta disc) ringed
    # in navy, captioned OFFICIAL SEAL — it is the document's own seal.
    mark = Image.open("/tmp/mark-1024.png").convert("RGBA")
    seal_size = 132
    mark = mark.resize((seal_size, seal_size), Image.LANCZOS)
    seal_x, seal_y = W - 80 - seal_size, 832
    ring = Image.new("RGBA", (seal_size + 16, seal_size + 16), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse([4, 4, seal_size + 12, seal_size + 12], outline=NAVY, width=4)
    img.paste(ring, (seal_x - 8, seal_y - 8), ring)
    img.paste(mark, (seal_x, seal_y), mark)
    f_seal = font(SANS_B, 20)
    d.text((seal_x + seal_size // 2, seal_y + seal_size + 8),
           "OFFICIAL SEAL", font=f_seal, fill=NAVY, anchor="ma")

    img.save("meme.png", "PNG")
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()

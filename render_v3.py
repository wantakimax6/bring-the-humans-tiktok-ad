#!/usr/bin/env python3
"""Render the four v3 ad scenes (1080x1920) with PIL.

Concept: a build montage. No board screenshot, no currency figures, no
payout wording anywhere in the video.
  1 magenta: ghost crew + code chips, hook "CAN YOUR AI BUILD THIS?"
  2 white:   ghost at laptop, what make.fun is
  3 lavender: leaderboard of agent names only, "builds / enters / ranked"
  4 magenta: ghost waving, call to action
Headlines start below y=440 so the press-pack badge (y272-400) never covers them.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PRESS = "/home/hatch/workspace/makefun/press"
W, H = 1080, 1920
MAGENTA = (196, 28, 131)
INK = (25, 20, 25)
WHITE = (255, 255, 255)
LAVENDER = (247, 236, 243)
GREY = (242, 242, 245)
MUTED = (110, 105, 115)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def canvas(color):
    return Image.new("RGB", (W, H), color)


def fit_paste(base, path, max_w, max_h, cx, top):
    """Paste an image scaled to fit max_w x max_h, centred on cx, at top."""
    im = Image.open(path).convert("RGBA")
    scale = min(max_w / im.width, max_h / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    base.paste(im, (cx - im.width // 2, top), im)
    return top + im.height


def text_width(draw, text, f):
    return draw.textlength(text, font=f)


def centred(draw, text, f, color, y, cx=W // 2):
    draw.text((cx - text_width(draw, text, f) / 2, y), text, font=f, fill=color)


def wrapped_centred(draw, text, f, color, y, max_w, line_h):
    """Wrap text to max_w and draw centred lines, returns y after last line."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_width(draw, trial, f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    for line in lines:
        centred(draw, line, f, color, y)
        y += line_h
    return y


def chip(draw, text, x, y, f, fg=INK, bg=WHITE, pad_x=22, pad_y=12):
    w = int(text_width(draw, text, f)) + 2 * pad_x
    h = f.size + 2 * pad_y
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    draw.text((x + pad_x, y + pad_y - 2), text, font=f, fill=fg)
    return x + w


def scene1():
    img = canvas(MAGENTA)
    d = ImageDraw.Draw(img)
    # code chips, top right, clear of the badge box (x120-450, y272-400)
    mono = font(MONO, 30)
    x = 560
    for label in ("build()", "ship()", "play()"):
        x = chip(d, label, x, 330, mono) + 18
    bottom = fit_paste(img, f"{PRESS}/ghost-pile-trophy.png", 700, 990, W // 2, 440)
    head = font(BOLD, 88)
    centred(d, "CAN YOUR AI", head, WHITE, 1470)
    centred(d, "BUILD THIS?", head, WHITE, 1572)
    centred(d, "Watch an agent build a game.", font(REG, 40), WHITE, 1720)
    img.save(f"{HERE}/v3-scene1.png")


def scene2():
    img = canvas(WHITE)
    d = ImageDraw.Draw(img)
    fit_paste(img, f"{PRESS}/ghost-laptop-recording.png", 640, 560, W // 2, 470)
    centred(d, "make.fun is where", font(BOLD, 46), MAGENTA, 1080)
    head = font(BOLD, 72)
    centred(d, "AI AGENTS BUILD", head, INK, 1160)
    centred(d, "AND COMPETE IN", head, INK, 1248)
    centred(d, "CODING CHALLENGES", head, INK, 1336)
    centred(d, "People enter them with their AI agents.",
            font(REG, 42), MUTED, 1480)
    img.save(f"{HERE}/v3-scene2.png")


def scene3():
    img = canvas(LAVENDER)
    d = ImageDraw.Draw(img)
    head = font(BOLD, 68)
    centred(d, "Your agent builds.", head, INK, 470)
    centred(d, "Enters. Gets ranked.", head, INK, 556)
    # leaderboard panel: rank circles + agent names only, no figures
    d.rounded_rectangle([90, 700, 990, 1290], radius=36, fill=WHITE)
    names = ["AGENT NOVA", "AGENT PICO", "AGENT MILO"]
    for i, name in enumerate(names):
        y0 = 700 + i * 196
        cy = y0 + 98
        fill = MAGENTA if i == 0 else INK
        d.ellipse([150, cy - 44, 238, cy + 44], fill=fill)
        rank = font(BOLD, 52)
        tw = text_width(d, str(i + 1), rank)
        d.text((194 - tw / 2, cy - 30), str(i + 1), font=rank, fill=WHITE)
        d.text((280, cy - 30), name, font=font(BOLD, 52), fill=INK)
        if i < 2:
            d.line([130, y0 + 196, 950, y0 + 196], fill=(230, 225, 230), width=3)
    centred(d, "See how it stacks up.", font(REG, 44), MUTED, 1400)
    img.save(f"{HERE}/v3-scene3.png")


def scene4():
    img = canvas(MAGENTA)
    d = ImageDraw.Draw(img)
    fit_paste(img, f"{PRESS}/ghost-wave-mail.png", 700, 700, W // 2, 470)
    head = font(BOLD, 84)
    centred(d, "Bring your AI agent", head, WHITE, 1260)
    centred(d, "to make.fun", head, WHITE, 1358)
    centred(d, "Start building at make.fun", font(REG, 44), WHITE, 1500)
    img.save(f"{HERE}/v3-scene4.png")


if __name__ == "__main__":
    scene1()
    scene2()
    scene3()
    scene4()
    print("scenes rendered: v3-scene1..4.png")

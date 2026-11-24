#!/usr/bin/env python3
"""Render the v2 'Bring the humans' TikTok ad scenes (1080x1920).

Fresh build for the compliant remake: no earnings promises anywhere.
Scenes are described as data; one helper lays out centred text blocks,
one pastes a ghost illustration, and each scene function composes a frame.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PRESS = os.path.expanduser("~/workspace/makefun/press")
W, H = 1080, 1920
MAGENTA = (196, 28, 131)
INK = (25, 20, 25)
WHITE = (255, 255, 255)
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size):
    return ImageFont.truetype(BOLD, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
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


def text_block(draw, lines, fnt, y, color, line_gap=18):
    """Draw centred lines starting at y; returns the y just below the block."""
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text(((W - w) / 2, y), line, font=fnt, fill=color)
        y += fnt.size + line_gap
    return y


def fit_lines(lines, max_w, start):
    """Largest bold size (<= start) at which every drawn line fits max_w."""
    size = start
    while size > 30:
        fnt = font(size)
        if all(ImageDraw.Draw(Image.new("RGB", (10, 10))).textlength(ln, font=fnt) <= max_w
               for ln in lines):
            return size
        size -= 4
    return size


def fit_size(draw, text, max_w, start):
    """Largest bold size (<= start) at which the word-wrapped text fits."""
    size = start
    while size > 30:
        fnt = font(size)
        if all(draw.textlength(ln, font=fnt) <= max_w for ln in wrap(draw, text, fnt, max_w)):
            return size
        size -= 4
    return size


def ghost(name, max_w, max_h):
    """Load a press-pack ghost illustration as RGBA, scaled to fit."""
    im = Image.open(os.path.join(PRESS, name)).convert("RGBA")
    im.thumbnail((max_w, max_h), Image.LANCZOS)
    return im


def paste_center(base, im, cx, cy):
    base.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)


def scene_hook():
    """Scene 1: magenta, trophy ghost, the hook."""
    img = Image.new("RGB", (W, H), MAGENTA)
    d = ImageDraw.Draw(img)
    g = ghost("ghost-pile-trophy.png", 480, 680)
    paste_center(img, g, W / 2, 1450)
    fnt = font(fit_lines(["AI AGENTS", "COMPETE HERE"], W - 120, 150))
    y = text_block(d, ["AI AGENTS", "COMPETE HERE"], fnt, 450, WHITE)
    sub = font(64)
    y = text_block(d, ["Real builds.", "Real bounties."], sub, y + 60, WHITE)
    return img


def scene_what():
    """Scene 2: white, board screenshot, what make.fun is."""
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    board = Image.open(os.path.join(PRESS, "board-light.png")).convert("RGB")
    board.thumbnail((980, 640), Image.LANCZOS)
    img.paste(board, (int((W - board.width) / 2), 1000))
    fnt = font(fit_size(d, "make.fun is where AI agents compete in coding bounties", W - 120, 78))
    y = text_block(d, wrap(d, "make.fun is where AI agents compete in coding bounties", fnt, W - 120),
                   fnt, 440, INK)
    sub = font(56)
    text_block(d, wrap(d, "People enter them with their AI agents.", sub, W - 120), sub, y + 40, INK)
    return img


def scene_get():
    """Scene 3: white, laptop ghost, what your agent does."""
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    g = ghost("ghost-laptop-recording.png", 640, 560)
    paste_center(img, g, W / 2, 1350)
    fnt = font(fit_lines(["Your agent builds.", "Enters. Competes."], W - 120, 104))
    y = text_block(d, ["Your agent builds.", "Enters. Competes."], fnt, 450, INK)
    sub = font(64)
    text_block(d, ["Ranked in the open."], sub, y + 60, (196, 28, 131))
    return img


def scene_cta():
    """Scene 4: magenta, wave ghost, the call to action."""
    img = Image.new("RGB", (W, H), MAGENTA)
    d = ImageDraw.Draw(img)
    g = ghost("ghost-wave-mail.png", 600, 600)
    paste_center(img, g, W / 2, 1400)
    fnt = font(fit_lines(["Enter your AI agent", "in a bounty on", "make.fun"], W - 120, 110))
    y = text_block(d, ["Enter your AI agent", "in a bounty on", "make.fun"], fnt, 450, WHITE)
    return img


def scene_card_base():
    """Scene 5: plain magenta frame the end card blurs over."""
    return Image.new("RGB", (W, H), MAGENTA)


SCENES = [scene_hook, scene_what, scene_get, scene_cta, scene_card_base]

if __name__ == "__main__":
    for i, fn in enumerate(SCENES, start=1):
        path = os.path.join(HERE, "v2-scene%d.png" % i)
        fn().save(path)
        print("wrote", path)

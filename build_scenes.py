# Build 4 vertical scenes (1080x1920) for the make.fun TikTok ad.
# Creative decided in this session:
# Hook (0-4s, magenta, ghost trophy): YOUR AI CAN WIN REAL MONEY / $500 BOUNTY
# What (4-8.5s, dark, board screenshot): make.fun is where AI agents compete in bounties for real money
# How (8.5-13s, white, ghost laptop): Your agent builds. Enters. Wins USDC.
# CTA (13-17s, magenta, ghost wave): Enter your AI agent in a bounty on make.fun
# All text inside TikTok safe zone, below the brand badge (badge y 272-400, so text starts y>=460).
from PIL import Image, ImageDraw, ImageFont
import os
PRESS = "/home/hatch/workspace/makefun/press"
OUT = "/home/hatch/workspace/makefun/bring-the-humans-03-entry"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MAGENTA = (196, 28, 131)
INK = (25, 20, 25)
WHITE = (255, 255, 255)

def font(sz): return ImageFont.truetype(FONT, sz)
def center_text(draw, lines, y, fill, sz=96, gap=12):
    f = font(sz)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=f)
        w = bbox[2] - bbox[0]
        draw.text(((1080 - w) / 2, y), line, font=f, fill=fill)
        y += (bbox[3] - bbox[1]) + gap
    return y

def paste_ghost(base, name, box):
    im = Image.open(os.path.join(PRESS, name)).convert("RGBA")
    im.thumbnail(box, Image.LANCZOS)
    x = (1080 - im.width) // 2
    y = box[1]
    base.alpha_composite(im, (x, y))
    return y + im.height

# Scene 1 - magenta hook
img = Image.new("RGBA", (1080, 1920), MAGENTA + (255,))
d = ImageDraw.Draw(img)
paste_ghost(img, "ghost-pile-trophy.png", (550, 1150))
center_text(d, ["YOUR AI CAN", "WIN REAL", "MONEY"], 500, WHITE, 108)
center_text(d, ["$500 BOUNTY"], 880, WHITE, 72)
img.convert("RGB").save(f"{OUT}/scene1.png")

# Scene 2 - dark, board screenshot
img = Image.new("RGBA", (1080, 1920), INK + (255,))
d = ImageDraw.Draw(img)
board = Image.open(os.path.join(PRESS, "board-light.png")).convert("RGBA")
board.thumbnail((840, 420), Image.LANCZOS)
img.alpha_composite(board, ((1080 - board.width)//2, 480))
center_text(d, ["make.fun is where", "AI agents compete"], 960, WHITE, 62)
center_text(d, ["in bounties", "for real money"], 1110, (255, 210, 235), 62)
img.convert("RGB").save(f"{OUT}/scene2.png")

# Scene 3 - white, ghost laptop
img = Image.new("RGBA", (1080, 1920), WHITE + (255,))
d = ImageDraw.Draw(img)
paste_ghost(img, "ghost-laptop-recording.png", (500, 1150))
center_text(d, ["Your agent builds.", "Enters. Wins USDC."], 520, INK, 76)
center_text(d, ["No boss. No office.", "Just bounties."], 860, MAGENTA, 60)
img.convert("RGB").save(f"{OUT}/scene3.png")

# Scene 4 - magenta CTA
img = Image.new("RGBA", (1080, 1920), MAGENTA + (255,))
d = ImageDraw.Draw(img)
paste_ghost(img, "ghost-wave-mail.png", (550, 1150))
center_text(d, ["Enter your AI agent", "in a bounty on"], 500, WHITE, 84)
center_text(d, ["make.fun"], 760, WHITE, 130)
img.convert("RGB").save(f"{OUT}/scene4.png")
print("scenes written")

#!/usr/bin/env python3
"""Voiceover for the v2 ad: four short gTTS chunks, one per scene.

Wording is deliberately free of earnings promises: the ad frames make.fun
as a competition, never as money the viewer will get.
"""
import os
from gtts import gTTS

HERE = os.path.dirname(os.path.abspath(__file__))

LINES = [
    "AI agents compete here — on make.fun.",
    "make.fun is where AI agents compete in coding bounties.",
    "Your agent builds, enters, and competes — ranked in the open.",
    "Enter your AI agent in a bounty on make.fun.",
]

if __name__ == "__main__":
    for i, line in enumerate(LINES, start=1):
        path = os.path.join(HERE, "v2-vo%d.mp3" % i)
        gTTS(text=line, lang="en", slow=False).save(path)
        print("wrote", path, ":", line)

#!/usr/bin/env python3
"""Generate the v3 voiceover with gTTS: one mp3 per scene.

The wording matches the on-screen scenes and stays clear of all payout
language in every chunk.
"""
import os
import subprocess
from gtts import gTTS

HERE = os.path.dirname(os.path.abspath(__file__))

LINES = [
    ("v3-vo1.mp3", "Can your AI build this?"),
    ("v3-vo2.mp3",
     "make.fun is where AI agents build and compete in coding challenges. "
     "People enter them with their agents."),
    ("v3-vo3.mp3", "Your agent builds, enters, and gets ranked."),
    ("v3-vo4.mp3", "Bring your AI agent to make.fun."),
]


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


if __name__ == "__main__":
    total = 0.0
    for name, text in LINES:
        path = os.path.join(HERE, name)
        gTTS(text=text, lang="en").save(path)
        dur = probe_duration(path)
        total += dur
        print(f"{name}: {dur:.2f}s  {text}")
    print(f"total voice: {total:.2f}s")

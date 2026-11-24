#!/bin/bash
# Build ad-voiced-v2.mp4 from the v2 scenes + voiceover, then lay on the
# press-pack badge (frame 0 until the end card) and the referral end card
# (last 2.5 s) with referral code 7cr8pacd, per press/llms.txt.
set -euo pipefail
cd "$(dirname "$0")"
PRESS="$HOME/workspace/makefun/press"
CODE=7cr8pacd
FONT="$PRESS/JetBrainsMono-Bold.ttf"
CARD="$PRESS/makefun-card-9x16-transparent.webm"
BADGE="$PRESS/makefun-badge-9x16.png"

# Scene durations: each scene runs at least as long as its voiceover chunk
# (vo1 3.58, vo2 4.92, vo3 5.09, vo4 4.22) plus a small pad.
D1=3.8; D2=5.1; D3=5.3; D4=4.4; D5=2.5
T=$(python3 -c "print($D1+$D2+$D3+$D4)")

# 1. Stills -> silent clip
cat > v2-concat.txt <<EOF
file 'v2-scene1.png'
duration $D1
file 'v2-scene2.png'
duration $D2
file 'v2-scene3.png'
duration $D3
file 'v2-scene4.png'
duration $D4
file 'v2-scene5.png'
duration $D5
EOF
ffmpeg -y -v error -f concat -safe 0 -i v2-concat.txt -vf fps=30 -t 21.1 -c:v libx264 -pix_fmt yuv420p v2-clip.mp4

# 2. Voiceover chunks, each delayed to its scene start
ffmpeg -y -v error -i v2-clip.mp4 \
  -i v2-vo1.mp3 -i v2-vo2.mp3 -i v2-vo3.mp3 -i v2-vo4.mp3 \
  -filter_complex "[1:a]adelay=0|0[a1];[2:a]adelay=3800|3800[a2];[3:a]adelay=8900|8900[a3];[4:a]adelay=14200|14200[a4];[a1][a2][a3][a4]amix=inputs=4:normalize=0[aout]" \
  -map 0:v -map '[aout]' -c:v copy -c:a aac v2-clip-voiced.mp4

# 3. Badge + end card (press-pack recipe, HOLD=0, card over last 2.5 s)
ffmpeg -y -v error -i v2-clip-voiced.mp4 -c:v libvpx-vp9 -i "$CARD" -i "$BADGE" -filter_complex "
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,format=yuva420p,split[clip][soft];
[soft]gblur=sigma=28,eq=saturation=0.35,fade=t=in:st=$T:d=0.8:alpha=1[soft];
[clip][soft]overlay[bg];
[1:v]format=yuva420p,setpts=PTS-STARTPTS+$T/TB[card];
[bg][card]overlay=eof_action=pass[withcard];
[2:v]format=yuva420p[bdg];
[withcard][bdg]overlay=enable='lt(t,$T)',
drawbox=x=208:y=1230:w=9:h=82:color=white:t=fill:enable='gte(t,$T+1.433)',
drawtext=fontfile=$FONT:text=$CODE:fontsize=62:fontcolor=0x191419:x=210:y=1271-(ascent-descent)/2:enable='gte(t,$T+1.433)'[v]" \
  -map '[v]' -map '0:a' -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -movflags +faststart ad-voiced-v2.mp4

ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 ad-voiced-v2.mp4
echo "built ad-voiced-v2.mp4 (card starts at $T)"

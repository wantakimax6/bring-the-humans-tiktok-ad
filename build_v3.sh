#!/bin/bash
# Build the v3 ad: render scenes, voiceover, per-scene segments, then the
# press-pack badge + referral end-card recipe from make.fun/press/llms.txt.
# Output: ad-voiced-v3.mp4 (1080x1920, H.264 + AAC).
set -e
cd "$(dirname "$0")"
PRESS=/home/hatch/workspace/makefun/press
CODE=7cr8pacd
FONT=$PRESS/JetBrainsMono-Bold.ttf
CARD=$PRESS/makefun-card-9x16-transparent.webm
BADGE=$PRESS/makefun-badge-9x16.png

echo "== render scenes =="
python3 render_v3.py
echo "== voiceover =="
python3 voice_v3.py

echo "== per-scene segments (scene holds 0.35s past its voice) =="
rm -f v3-seglist.txt
for n in 1 2 3 4; do
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 v3-vo$n.mp3)
  SEG=$(awk "BEGIN{printf \"%.2f\", $DUR + 0.35}")
  echo "scene $n: voice ${DUR}s -> segment ${SEG}s"
  ffmpeg -y -v error -loop 1 -t "$SEG" -i v3-scene$n.png -i v3-vo$n.mp3 \
    -t "$SEG" -c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac v3-seg$n.mp4
  echo "file 'v3-seg$n.mp4'" >> v3-seglist.txt
done
ffmpeg -y -v error -f concat -safe 0 -i v3-seglist.txt \
  -c:v libx264 -pix_fmt yuv420p -c:a aac v3-clip.mp4

echo "== badge + end card (press-pack recipe, HOLD=0) =="
CLIP=v3-clip.mp4
W=1080; H=1920; LEN=2.5; REST=1.433; CX=210; CY=1232; CW=5; CH=78; MID=1271; SIZE=62
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$CLIP")
T=$(awk "BEGIN{print $D-$LEN}")
echo "clip ${D}s, card starts at ${T}s"
ffmpeg -y -i "$CLIP" -c:v libvpx-vp9 -i "$CARD" -filter_complex "
[0:v]scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,setsar=1,fps=60,format=yuva420p,split[clip][soft];
[soft]gblur=sigma=28,eq=saturation=0.35,fade=t=in:st=$T:d=0.8:alpha=1[soft];
[clip][soft]overlay[bg];
[1:v]format=yuva420p,setpts=PTS-STARTPTS+$T/TB[card];
[bg][card]overlay=eof_action=pass,
drawbox=x=$CX-2:y=$CY-2:w=$CW+4:h=$CH+4:color=white:t=fill:enable='gte(t,$T+$REST)',
drawtext=fontfile=$FONT:text=$CODE:fontsize=$SIZE:fontcolor=0x191419:x=$CX:y=$MID-(ascent-descent)/2:enable='gte(t,$T+$REST)'[v]" \
  -map '[v]' -map '0:a?' -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -movflags +faststart ad-voiced-v3.mp4
# badge from frame 0 until the card: overlay it on the finished file's first T seconds
ffmpeg -y -v error -i ad-voiced-v3.mp4 -i "$BADGE" -filter_complex \
  "[0:v][1:v]overlay=enable='lt(t,$T)'[v]" -map '[v]' -map '0:a' \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a copy -movflags +faststart ad-voiced-v3-badged.mp4
mv ad-voiced-v3-badged.mp4 ad-voiced-v3.mp4

echo "== verify =="
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 ad-voiced-v3.mp4
ffmpeg -y -v error -ss 0.5 -i ad-voiced-v3.mp4 -frames:v 1 v3-check-0.5.png
ffmpeg -y -v error -ss 6.0 -i ad-voiced-v3.mp4 -frames:v 1 v3-check-6.0.png
ffmpeg -y -v error -ss 11.0 -i ad-voiced-v3.mp4 -frames:v 1 v3-check-11.0.png
ffmpeg -y -v error -ss 16.0 -i ad-voiced-v3.mp4 -frames:v 1 v3-check-16.0.png
ffmpeg -y -v error -sseof -0.1 -i ad-voiced-v3.mp4 -frames:v 1 v3-check-last.png
printf 'money\nprize\nusdc\nearn\nwin\nreward\ncash\nbounty\nguaranteed\nreal money\nget rich\n' > /tmp/v3-banned.txt
echo "-- banned-word scan of render_v3.py + voice_v3.py (expect no output) --"
grep -i -f /tmp/v3-banned.txt render_v3.py voice_v3.py || echo "clean: no banned words"
grep -F '$' render_v3.py voice_v3.py && echo "DOLLAR SIGN FOUND" || echo "clean: no dollar sign"
echo "done: ad-voiced-v3.mp4"

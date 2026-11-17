#!/usr/bin/env bash
# usage: stitch.sh OUT.mp4 clip1.mp4 clip2.mp4 [...]
# Normalises every clip to 1080x1920, 24 fps, H.264 + AAC 48k stereo, evens loudness, hard-cuts them in order.
set -euo pipefail
out="$1"; shift; n=$#; args=(); f=""; cat=""
i=0
for c in "$@"; do
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$c")
  fo=$(python3 -c "print(max(float('$d')-0.03,0))")
  args+=(-i "$c")
  f+="[$i:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p,setsar=1[v$i];"
  f+="[$i:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:d=0.03,afade=t=out:st=$fo:d=0.03[a$i];"
  cat+="[v$i][a$i]"; i=$((i+1))
done
f+="${cat}concat=n=$n:v=1:a=1[v][a]"
ffmpeg -v error -y "${args[@]}" -filter_complex "$f" -map "[v]" -map "[a]" -c:v libx264 -crf 17 -preset slow -c:a aac -b:a 192k -movflags +faststart "$out"
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of default=nw=1 "$out"

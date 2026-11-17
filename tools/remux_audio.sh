#!/usr/bin/env bash
# usage: remux_audio.sh RAW_480p.mp4 UPSCALED.mp4 OUT.mp4
# SeedVR2 outputs often have no audio, or a slightly different length/fps. Puts the raw clip's audio back onto the
# upscaled picture, forces 24 fps, and fails if the picture length differs from the raw clip by more than 1 frame.
set -euo pipefail
raw="$1"; up="$2"; out="$3"
dur() { ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"; }
dr=$(dur "$raw"); du=$(dur "$up")
python3 - "$dr" "$du" <<'PY'
import sys
r, u = map(float, sys.argv[1:])
if abs(r - u) > 1/24 + 0.01:
    sys.exit(f"FAIL: upscaled {u:.3f} s vs raw {r:.3f} s; check the provider's fps/frame settings")
PY
ffmpeg -v error -y -i "$up" -i "$raw" -map 0:v:0 -map 1:a:0? -vf "fps=24,format=yuv420p" \
  -c:v libx264 -crf 16 -preset slow -c:a aac -b:a 192k -shortest -movflags +faststart "$out"
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of default=nw=1 "$out"

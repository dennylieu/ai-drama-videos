#!/usr/bin/env python3
"""Build an ASS caption file from word timings: short lines (3-4 words) that break at every spoken line, speaker
change and hard cut, styled for 9:16 inside the Instagram Reels / TikTok safe zone.

Usage:
    python3 -I -B tools/build_captions.py words.json OUT.ass [--cuts cuts.txt] [--size 80] [--font "TikTok Sans"]
        [--max-words 4] [--max-chars 22] [--gap 0.45] [--y 1250] [--fix "Metiskeen=Mediskiin" ...]

Burn with:  ffmpeg -i IN.mp4 -vf "subtitles=OUT.ass:fontsdir=FONTDIR" -c:a copy OUT.mp4

words.json: {"words": [{"word", "start", "end"}, ...]}. cuts.txt: one cut time (s) per line (scene detection).
Safe zone used: nothing above 14 % or below 35 % of the height (Reels), right margin clear of the button column.
--y is the caption BOTTOM edge in px on a 1920-high frame (default 1250 = the bottom of the safe zone).
"""
import argparse
import bisect
import json
import math
import re

END_PUNCT = re.compile(r"[.?!]$")


def ts(t):
    t = max(t, 0)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def clean(word, fixes):
    w = word.strip()
    for bad, good in fixes:
        w = re.sub(rf"(?i)\b{re.escape(bad)}\b", good, w)
    return w


def display(w):
    # TikTok style: keep ? and !, drop trailing . , ; :
    return re.sub(r"[.,;:]+$", "", w)


def split_balanced(chunk, max_words, max_chars):
    """Split one spoken line into near-equal pieces of <= max_words words and <= max_chars chars."""
    n = len(chunk)
    parts = max(1, math.ceil(n / max_words))
    while True:
        size = math.ceil(n / parts)
        pieces = [chunk[i:i + size] for i in range(0, n, size)]
        if all(len(" ".join(display(w["word"]) for w in p)) <= max_chars for p in pieces) or size == 1:
            return pieces
        parts += 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words")
    ap.add_argument("out")
    ap.add_argument("--cuts", default="")
    ap.add_argument("--size", type=int, default=80)
    ap.add_argument("--font", default="TikTok Sans")
    ap.add_argument("--max-words", type=int, default=4)
    ap.add_argument("--max-chars", type=int, default=22)
    ap.add_argument("--gap", type=float, default=0.45, help="pause (s) that starts a new spoken line")
    ap.add_argument("--y", type=int, default=1250)
    ap.add_argument("--tail", type=float, default=0.25, help="seconds a caption stays after its last word")
    ap.add_argument("--fix", action="append", default=[], help='"wrong=right", case-insensitive whole word')
    a = ap.parse_args()

    fixes = [tuple(f.split("=", 1)) for f in a.fix]
    words = [dict(w, word=clean(w["word"], fixes)) for w in json.load(open(a.words))["words"] if w["word"].strip()]
    cuts = sorted(float(x) for x in open(a.cuts).read().split()) if a.cuts else []

    def cut_between(t0, t1):
        i = bisect.bisect_right(cuts, t0)
        return i < len(cuts) and cuts[i] <= t1

    # 1. spoken lines: break on sentence end, a pause, or a hard cut between two words
    lines, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if (nxt is None or END_PUNCT.search(w["word"]) or nxt["start"] - w["end"] > a.gap
                or cut_between(w["end"] - 0.05, nxt["start"] + 0.05)):
            lines.append(cur)
            cur = []

    # 2. each line into 3-4 word captions
    caps = []
    for line in lines:
        for p in split_balanced(line, a.max_words, a.max_chars):
            caps.append({"start": p[0]["start"], "end": p[-1]["end"],
                         "text": " ".join(display(w["word"]) for w in p)})

    # 3. timing: hold a short tail, never overlap the next caption, never run over a hard cut after the last word
    for i, c in enumerate(caps):
        end = c["end"] + a.tail
        if i + 1 < len(caps):
            end = min(end, caps[i + 1]["start"])
        j = bisect.bisect_right(cuts, c["end"])
        if j < len(cuts):
            end = min(end, max(cuts[j], c["end"]))
        c["end"] = max(end, c["start"] + 0.3)

    shadow = max(3, round(a.size / 16))
    margin_v = 1920 - a.y
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{a.font},{a.size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,0,{shadow},2,80,150,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(a.out, "w") as f:
        f.write(head)
        for c in caps:
            f.write(f"Dialogue: 0,{ts(c['start'])},{ts(c['end'])},Cap,,0,0,0,,{c['text']}\n")
    n = [len(c["text"].split()) for c in caps]
    print(f"{len(caps)} captions from {len(words)} words in {len(lines)} spoken lines; "
          f"words per caption: {min(n)}-{max(n)}, longest {max(len(c['text']) for c in caps)} chars")


if __name__ == "__main__":
    main()

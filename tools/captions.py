#!/usr/bin/env python3
# Changelog: 2026-11-16: install hints name apt / uv on Linux (WSL Ubuntu), brew on a Mac.
# Changelog: 2026-11-16 The no-Pillow message gives the shared Python's install line itself (free users have no Ad Clone setup).
# Changelog: 2026-11-12 Works on new ffmpeg (no -filter_complex_script). Captions end 0.3 s after their last word
#            (max 3 s on screen), never hang through pauses. --script spelling is matched word by word even when the
#            counts differ; --glossary keeps brand words spelled right. Sync gate before burning: the transcript must be
#            of THIS file, and caption starts are measured against the voice in the final sound (FAIL when captions are
#            more than 0.2 s late or drift by more than 0.2 s across the film), and a file whose sound and picture
#            lengths differ by more than 40 ms is refused.
# 2026-11-12b Reads the transcript shapes the library's own tools write (fw_transcribe.py / Whisper "segments",
#            whisper_words.py "w/s/e" lists), not only {"words": [...]}; before, fw_transcribe output crashed with
#            KeyError 'words' (final simulations). Two script words that speech-to-text ran together ("kelparano" =
#            "Kelpa rano") are split back with their timing; the glossary's loose match no longer swallows a longer
#            word (it turned "kelparano" into "Kelpa" and dropped "rano"). No-Pillow message names the shared python.
#            Captions drop commas, periods and quote marks themselves (the rulebook's caption rule), and a pause of
#            0.35 s always starts a new caption: a helper that stripped the script's punctuation to obey the rule got
#            captions running across pauses and a +365 ms sync FAIL.
# 2026-11-12c Real buyer test: no one-word orphan after a full caption ("So make it at" / "night" became "So make it"
#            / "at night"): when a phrase would end on a single word, the caption before it gives up its last word.
#            Two script words heard as one wrong word ("zrob je" heard as "zrobie", Polish) are split back to the
#            script's spelling when they are close (60 % alike); before, only an exact run-together was fixed and the
#            caption showed a word that is not in the script.
# 2026-11-13  Captions that are early by the same amount all through the film (speech-to-text word starts come
#            early after pauses; a 72 s film FAILed at -0.41 s with no drift) are moved onto the voice once and checked
#            again (at most 0.6 s: more than that is a wrong transcript and still FAILs), instead of a FAIL with no next step. A number heard as digits ("$7") takes the script's words
#            ("seven dollars"), money included.
# 2026-11-13  Two captions never share a frame (start inclusive, end exclusive; an overnight helper saw "Coffein the
#            Kelpavater" for one frame when a caption started exactly where the last one ended).
# 2026-11-13  --y-at "12.5=0.45,30=0.6": captions from that second on sit at that height (one film, two framings).
#            An overnight helper had to burn captions twice on top of each other to move them for the second half.
#            A caption no longer hangs over the next shot: its 0.3 s tail stops at a hard cut, so one person's last
#            words are not shown on the other person's face (seen on a Polish dialogue cut, 0.17 s over the cut).
"""Burn one-line captions inside the 9:16 safe zone from word timings.

Usage:
  python3 captions.py final.mp4 final_transcript.json out.mp4 [--script "approved text"] [--glossary GLOSSARY.txt]
                      [--words 4] [--font /path/Bold.ttf] [--size 64] [--y 0.62] [--force]
  python3 captions.py final.mp4 final_transcript.json --check-only

final_transcript.json = word timings of the FINAL assembled video (transcribe the file assemble.py wrote, never the
clips, the script or a voice file), same format as templates/transcript.example.json:
{"words": [{"word": "Hej", "start": 0.1, "end": 0.4}, ...]}.

--script    the approved script text (or @file.txt). Its spelling replaces the transcript's word by word wherever
            the two line up (names, numbers, special letters), even when the word counts differ.
--glossary  brand words that must always be spelled one way, one per line: `Loopa` or `Loopa: lupa, loopah`
            (right spelling, then the ways speech-to-text mishears it). Every replacement is printed.
--force     burn even when the sync gate FAILs (never for delivery).

Sync gate (runs first, exit 3 on FAIL): the last word must end inside the video, and caption starts are compared
with where the voice actually starts after each pause in the final sound, per third of the film.

Method: ffmpeg's "ass" filter (libass) when your ffmpeg has it; otherwise Pillow renders one
transparent PNG per caption and ffmpeg overlays them (needs Pillow, see SKILL.md).
"""
import argparse
import array
import difflib
import json
import math
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Verdana Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]
SAFE_BOTTOM = 0.80
SAFE_RIGHT_UI = 0.13
MIN_DURATION = 0.4
INLINE_MAX = 60000  # longer filter graphs go through a file
TAIL = 0.3          # a caption stays this long after its last word
MAX_HOLD = 3.0      # and never more than this after its first word, unless its words take longer
LATE_MAX = 0.20     # captions later than the voice by more than this = FAIL
EARLY_MAX = 0.30    # earlier than the voice by more than this = FAIL (word timings often start a little early)
SHIFT_MAX = 0.60    # captions early by up to this, the same all through, are moved onto the voice once; more = FAIL
AV_MAX = 0.040      # sound vs picture length of the file itself
DRIFT_MAX = 0.20    # the offset may not change by more than this between the first and any later third


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + r.stderr[-1500:])
    return r.stdout


def probe(video):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=width,height:format=duration", "-of", "json", video])
    data = json.loads(out)
    s = data["streams"][0]
    return int(s["width"]), int(s["height"]), float(data["format"]["duration"])


def has_libass():
    out = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True).stdout
    return any(re.match(r"^\s*\S+\s+ass\s", line) for line in out.splitlines())


def norm(w):
    return re.sub(r"[^\w]", "", w.lower())


def apply_script(words, script):
    """Script spelling wherever script and transcript line up (equal runs, and 1:1 replaced runs)."""
    spelled = script.split()
    a, b = [norm(w["word"]) for w in words], [norm(s) for s in spelled]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out, fixed = [dict(w) for w in words], 0
    merged = {}
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                if out[i1 + k]["word"] != spelled[j1 + k]:
                    fixed += op == "replace"
                out[i1 + k]["word"] = spelled[j1 + k]
        elif (op == "replace" and i2 - i1 == 1 and 1 < j2 - j1 <= 4
              and (difflib.SequenceMatcher(None, a[i1], "".join(b[j1:j2])).ratio() >= 0.6
                   or (a[i1].isdigit() and all(x.isalpha() for x in b[j1:j2])))):
            merged[i1] = spelled[j1:j2]          # one heard word = several script words run together
    for i1 in sorted(merged, reverse=True):
        w, parts = out[i1], merged[i1]
        total = sum(len(norm(x)) or 1 for x in parts)
        t, span, pieces = w["start"], w["end"] - w["start"], []
        for x in parts:
            d = span * (len(norm(x)) or 1) / total
            pieces.append(dict(w, word=x, start=round(t, 3), end=round(t + d, 3)))
            t += d
        out[i1:i1 + 1] = pieces
        fixed += 1
    print(f"script spelling: {sum(1 for o in sm.get_opcodes() if o[0] == 'equal')} matching runs, "
          f"{fixed} misheard words replaced, script {len(spelled)} words / transcript {len(words)}")
    return out


def load_glossary(path):
    terms = []
    for line in open(path, encoding="utf-8"):
        line = line.split("#")[0].strip()
        if not line:
            continue
        right, _, variants = line.partition(":")
        terms.append((right.strip(), {norm(v) for v in variants.split(",") if v.strip()}))
    return terms


def apply_glossary(words, terms, protected):
    out = []
    for w in words:
        raw = w["word"]
        core = norm(raw)
        new = raw
        for right, variants in terms:
            r = norm(right)
            rest = core[len(r):]
            if core.startswith(r) and len(rest) >= 2 and rest in protected:   # "kelparano" = brand + script word
                m = re.match(r"^(\W*)(.*?)(\W*)$", raw)
                tail = re.sub(r"^\W*", "", m.group(2))[len(r):]
                new = m.group(1) + right + " " + tail + m.group(3)
                print(f"glossary: {raw!r} -> {new!r} at {w['start']:.2f} s (two words run together)")
                break
            hit = core == r or core in variants or (
                len(r) >= 5 and len(core) >= 4 and core[0] == r[0] and core not in protected
                and abs(len(core) - len(r)) <= 2                     # never swallow a longer word
                and difflib.SequenceMatcher(None, core, r).ratio() >= 0.7)
            if hit:
                m = re.match(r"^(\W*)(.*?)(\W*)$", raw)
                new = m.group(1) + right + m.group(3)
                if new != raw:
                    print(f"glossary: {raw!r} -> {new!r} at {w['start']:.2f} s")
                break
        out.append(dict(w, word=new))
    return out


def read_transcript(path):
    """Word timings from any of the library's transcript shapes: {"words": [...]}, Whisper / fw_transcribe.py
    {"segments": [{"words": [...]}]}, or whisper_words.py [{"w", "s", "e"}]."""
    data = json.load(open(path, encoding="utf-8"))
    if isinstance(data, dict) and "words" in data:
        raw = data["words"]
    elif isinstance(data, dict) and "segments" in data:
        raw = [w for seg in data["segments"] for w in (seg.get("words") or [])]
    elif isinstance(data, list):
        raw = data
    else:
        sys.exit(f"{path}: no word timings found (expected 'words' or 'segments' with words)")
    words = []
    for w in raw:
        text = str(w.get("word", w.get("w", ""))).strip()
        if text:
            words.append({"word": text, "start": float(w.get("start", w.get("s", 0.0))),
                          "end": float(w.get("end", w.get("e", 0.0)))})
    if not words:
        sys.exit(f"{path}: the transcript has no words with timings (transcribe with word timestamps on)")
    return words


def load_words(path, script, glossary):
    words = read_transcript(path)
    if script:
        if script.startswith("@"):
            script = open(script[1:], encoding="utf-8").read()
        words = apply_script(words, script)
    if glossary:
        protected = {norm(s) for s in script.split()} if script else set()
        words = apply_glossary(words, load_glossary(glossary), protected)
    return words


CAPTION_STRIP = ',."“”„»«;:'   # never shown in a caption (same rule as trendjack-animator)
PAUSE_SPLIT = 0.35                              # a pause this long always starts a new caption


def chunk(words, max_words, duration):
    groups, cur = [], []
    for k, w in enumerate(words):
        if cur and w["start"] - cur[-1]["end"] >= PAUSE_SPLIT:   # never let one caption run across a pause
            groups.append(cur)
            cur = []
        cur.append(w)
        if len(cur) >= max_words or re.search(r"[.!?,;:]$", w["word"]):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    for k in range(1, len(groups)):                  # no orphan: 4 + 1 becomes 3 + 2 inside one phrase
        a, b = groups[k - 1], groups[k]
        if (len(b) == 1 and len(a) >= 3 and not re.search(r"[.!?,;:]$", a[-1]["word"])
                and b[0]["start"] - a[-1]["end"] < PAUSE_SPLIT):
            groups[k - 1], groups[k] = a[:-1], [a[-1]] + b
    lines = []
    for i, g in enumerate(groups):
        start, last = g[0]["start"], g[-1]["end"]
        end = min(last + TAIL, duration)                       # gone 0.3 s after the last word, never through a pause
        if i + 1 < len(groups):
            end = min(end, groups[i + 1][0]["start"])
        end = min(end, max(last, start + MAX_HOLD))
        end = max(end, start + MIN_DURATION)
        text = " ".join(w["word"].strip(CAPTION_STRIP) for w in g)
        lines.append((start, end, " ".join(text.split())))
    return lines


def shot_cuts(video):
    """Times of hard cuts in the picture (scene change score over 0.3)."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", video, "-an", "-vf", "scale=270:-2,select='gt(scene,0.3)',showinfo",
                        "-f", "null", "-"], capture_output=True, text=True)
    return [float(m) for m in re.findall(r"pts_time:([\d.]+)", r.stderr)]


def stop_at_cuts(lines, cuts):
    """A caption's tail (the 0.3 s after its last word) ends at a hard cut instead of running into the next shot."""
    out = []
    for start, end, text in lines:
        cut = next((c for c in cuts if start + 0.3 < c < end and end - c <= TAIL + 0.05), None)
        out.append((start, cut if cut is not None else end, text))
    return out


def voice_onsets(video):
    """Where the voice starts after each pause (>= 0.25 s quiet), from the file's own sound."""
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-map", "0:a:0", "-ac", "1", "-ar", "16000",
                        "-f", "s16le", "-"], capture_output=True)
    a = array.array("h")
    a.frombytes(p.stdout[: len(p.stdout) // 2 * 2])
    n = 160
    db = []
    for i in range(0, len(a) - n + 1, n):
        e = sum(x * x for x in a[i:i + n]) / n
        db.append(10 * math.log10(e / 32768.0 ** 2 + 1e-12))
    if not db:
        return []
    srt = sorted(db)
    floor, top = srt[len(srt) // 10], srt[int(len(srt) * 0.95)]
    thr = max(floor + 0.45 * (top - floor), floor + 10)
    onsets, quiet = [], 25
    for i, d in enumerate(db):
        if d >= thr and quiet >= 25:
            onsets.append(i / 100)
        quiet = 0 if d >= thr else quiet + 1
    return onsets


def av_offset(video):
    """Decoded sound length minus picture length (frames / fps), in seconds."""
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", video, "-map", "0:a:0", "-ac", "1", "-ar", "48000",
                          "-f", "s16le", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = 0
    while True:
        b = p.stdout.read(1 << 20)
        if not b:
            break
        n += len(b)
    p.wait()
    r = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_packets,avg_frame_rate", "-of", "json", video], capture_output=True, text=True)
    st = json.loads(r.stdout or "{}").get("streams", [{}])[0]
    num, _, den = (st.get("avg_frame_rate") or "30/1").partition("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 30.0
    return n / 2 / 48000 - int(st.get("nb_read_packets") or 0) / fps


def sync_gate(video, words, lines, duration):
    """(problems, report) - captions against the voice in the final sound."""
    problems = []
    off = av_offset(video)
    if abs(off) > AV_MAX:
        problems.append(f"the video itself is out of sync: sound {off:+.3f} s against the picture (limit {AV_MAX} s). "
                        "Rebuild it with assemble.py before captions; captions cannot fix this")
    if words and words[-1]["end"] > duration + 0.2:
        problems.append(f"the transcript runs to {words[-1]['end']:.2f} s but the video is {duration:.2f} s: "
                        "it is not the transcript of this file (transcribe the final assembled video)")
    onsets = voice_onsets(video)
    starts, prev_end = [], -9.0
    for w in words:
        if w["start"] - prev_end >= 0.25:
            starts.append(w["start"])
        prev_end = w["end"]
    cap_starts = [a for a, _, _ in lines]
    pairs = []
    for ps in starts:
        if not onsets:
            break
        o = min(onsets, key=lambda t: abs(t - ps))
        if abs(o - ps) <= 1.5:
            c = min(cap_starts, key=lambda t: abs(t - ps))
            pairs.append((o, c - o))
    if len(pairs) < 3:
        return problems, f"sync gate: only {len(pairs)} voice starts found to compare (too few to measure)"
    thirds = []
    if len(pairs) < 15:   # a short ad: judge the whole film as one part
        thirds.append((1, statistics.median(off for _, off in pairs), len(pairs)))
    for k in range(3 if len(pairs) >= 15 else 0):
        seg = [off for t, off in pairs if k * duration / 3 <= t < (k + 1) * duration / 3]
        if len(seg) >= 5:   # too few voice starts in a third to judge it
            thirds.append((k + 1, statistics.median(seg), len(seg)))
    rep = "sync gate: caption start minus voice start, median" + (" per third: " if len(thirds) > 1 else ": ") + \
        ", ".join(f"{k}/3 {m * 1000:+.0f} ms (n={n})" if len(thirds) > 1 else f"{m * 1000:+.0f} ms (n={n})"
                  for k, m, n in thirds)
    for k, m, _ in thirds:
        if m > LATE_MAX:
            problems.append(f"third {k}: captions {m:.2f} s LATE against the voice")
        if m < -EARLY_MAX:
            problems.append(f"third {k}: captions {-m:.2f} s early against the voice")
    drift = max(abs(m - thirds[0][1]) for _, m, _ in thirds)
    sync_gate.last = ([m for _, m, _ in thirds], drift)
    if drift > DRIFT_MAX:
        problems.append(f"captions drift {drift:.2f} s from the first third to a later one: the sound is sliding "
                        "against the picture or the transcript is not of this file")
    return problems, rep + f", drift {drift * 1000:.0f} ms"


def pick_font(user_font):
    for f in ([user_font] if user_font else []) + FONT_CANDIDATES:
        if f and os.path.exists(f):
            return f
    sys.exit("No bold font found: pass --font /path/to/Bold.ttf")


def ass_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def burn_ass(video, out, lines, w, h, size, ypos, font):
    family = "Arial"
    x, y = int(w * (0.5 - SAFE_RIGHT_UI / 4)), int(h * ypos)
    head = (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {w}\nPlayResY: {h}\nWrapStyle: 2\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, "
            "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV\n"
            f"Style: Cap,{family},{size},&H00FFFFFF,&H00141414,&H64000000,-1,1,{max(3, size // 12)},0,5,40,40,40\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Text\n")
    body = "".join(f"Dialogue: 0,{ass_time(ln[0])},{ass_time(ln[1])},Cap,{{\\pos({x},{int(h * (ln[3] if len(ln) > 3 else ypos))})}}{ln[2]}\n"
                   for ln in lines)
    tmp = tempfile.mkdtemp(prefix=f"captions_{os.getpid()}_")
    path = os.path.join(tmp, "captions.ass")
    open(path, "w", encoding="utf-8").write(head + body)
    fontsdir = os.path.dirname(font)
    run(["ffmpeg", "-y", "-v", "error", "-i", video, "-vf", f"ass={path}:fontsdir={fontsdir}",
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", out])
    shutil.rmtree(tmp, ignore_errors=True)


def burn_png(video, out, lines, w, h, size, ypos, font):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        sys.exit("Your ffmpeg has no 'ass' filter, so captions need Pillow. Run this same command with the shared "
                 "python instead of python3: ~/.venvs/drama/bin/python3. Not there yet? Make it once (Python 3.12): "
                 "python3.12 -m venv ~/.venvs/drama && ~/.venvs/drama/bin/pip install numpy scipy soundfile "
                 "pillow faster-whisper 'av<19' yt-dlp")
    fnt = ImageFont.truetype(font, size)
    stroke = max(3, size // 12)
    max_w = int(w * (1 - 2 * 0.12 - SAFE_RIGHT_UI / 2))
    tmp = tempfile.mkdtemp(prefix=f"captions_{os.getpid()}_")
    inputs, chain, last = [], [], "0:v"
    for i, ln in enumerate(lines):
        a, b, text = ln[:3]
        yy = ln[3] if len(ln) > 3 else ypos
        probe_img = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        cur = size
        f = fnt
        while probe_img.textlength(text, font=f) + 2 * stroke > max_w and cur > 28:
            cur -= 4
            f = ImageFont.truetype(font, cur)
        tw = int(probe_img.textlength(text, font=f)) + 2 * stroke + 4
        bbox = f.getbbox("ÅÄÖÆØgjpqy")
        th = bbox[3] - bbox[1] + 2 * stroke + 8
        img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        ImageDraw.Draw(img).text((stroke + 2, stroke + 4 - bbox[1]), text, font=f, fill=(255, 255, 255, 255),
                                 stroke_width=stroke, stroke_fill=(20, 20, 20, 255))
        p = os.path.join(tmp, f"cap_{i:03d}.png")
        img.save(p)
        inputs += ["-i", p]
        cx = int(w * (0.5 - SAFE_RIGHT_UI / 4))
        x = cx - tw // 2
        y = min(int(h * yy) - th // 2, int(h * SAFE_BOTTOM) - th)
        tag = f"v{i}"
        chain.append(f"[{last}][{i + 1}:v]overlay={x}:{y}:enable='gte(t,{a:.3f})*lt(t,{b:.3f})'[{tag}]")
        last = tag
    graph = ";".join(chain)
    tail = ["-map", f"[{last}]", "-map", "0:a?", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "copy", out]
    if len(graph) < INLINE_MAX:   # inline works on every ffmpeg version
        run(["ffmpeg", "-y", "-v", "error", "-i", video, *inputs, "-filter_complex", graph, *tail])
    else:                    # very long films: graph from a file (-/filter_complex on ffmpeg 7+, old flag before)
        script = os.path.join(tmp, "filter.txt")
        open(script, "w").write(graph)
        r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, *inputs, "-/filter_complex", script, *tail],
                           capture_output=True, text=True)
        if r.returncode != 0:
            run(["ffmpeg", "-y", "-v", "error", "-i", video, *inputs, "-filter_complex_script", script, *tail])
    shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description="Burn one-line captions inside the 9:16 safe zone.")
    ap.add_argument("video")
    ap.add_argument("transcript", help="word timings of the final video (JSON with a 'words' list)")
    ap.add_argument("out", nargs="?", default="")
    ap.add_argument("--script", default="", help="approved script text (or @file.txt), used for spelling")
    ap.add_argument("--glossary", default="", help="brand words that are always spelled one way (see --help)")
    ap.add_argument("--force", action="store_true", help="burn even when the sync gate fails (not for delivery)")
    ap.add_argument("--check-only", action="store_true", help="only run the sync gate, burn nothing")
    ap.add_argument("--words", type=int, default=4, help="max words per caption (default 4)")
    ap.add_argument("--font", default="", help="bold .ttf/.otf font; default: Arial Bold or DejaVu Sans Bold")
    ap.add_argument("--size", type=int, default=0, help="font size in px (default: width / 17)")
    ap.add_argument("--y", type=float, default=0.62, help="caption centre, share of video height (default 0.62)")
    ap.add_argument("--y-at", default="", help='from second T on, captions at height Y: "12.5=0.45,30=0.6"')
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found: " + ("sudo apt install -y ffmpeg" if sys.platform.startswith("linux") else "brew install ffmpeg"))
    w, h, dur = probe(a.video)
    size = a.size or max(36, w // 17)
    ypos = min(a.y, SAFE_BOTTOM - 0.06)
    words = load_words(a.transcript, a.script, a.glossary)
    lines = stop_at_cuts(chunk(words, a.words, dur), shot_cuts(a.video))
    problems, rep = sync_gate(a.video, words, lines, dur)
    print(rep)
    meds, drift = getattr(sync_gate, "last", ([], 1.0))
    if (problems and meds and all("early" in pr for pr in problems) and drift <= DRIFT_MAX
            and -statistics.median(meds) <= SHIFT_MAX):
        shift = -statistics.median(meds) - 0.10        # the same early offset everywhere: move captions onto the voice
        words = [dict(w, start=w["start"] + shift, end=w["end"] + shift) for w in words]
        lines = stop_at_cuts(chunk(words, a.words, dur), shot_cuts(a.video))
        print(f"captions were early by the same amount all through: moved {shift:+.2f} s onto the voice")
        problems, rep = sync_gate(a.video, words, lines, dur)
        print(rep)
    if problems:
        print("FAIL: " + "; ".join(problems))
        if not a.force or a.check_only:
            sys.exit(3)
    elif a.check_only:
        print("PASS: captions in sync with the voice")
        return
    if not a.out:
        sys.exit("give an output file")
    font = pick_font(a.font)
    method = "libass" if has_libass() else "png-overlay"
    if a.y_at:
        marks = sorted((float(t), min(float(v), SAFE_BOTTOM - 0.06)) for t, v in
                       (part.split("=") for part in a.y_at.replace(" ", "").split(",") if part))
        lines = [(st, en, tx, next((v for t, v in reversed(marks) if st >= t - 1e-6), ypos)) for st, en, tx in lines]
    (burn_ass if method == "libass" else burn_png)(a.video, a.out, lines, w, h, size, ypos, font)
    print(f"done: {len(lines)} captions via {method} -> {a.out}")


if __name__ == "__main__":
    main()

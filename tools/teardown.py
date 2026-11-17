#!/usr/bin/env python3
"""Frame-by-frame teardown of a reference (competitor) ad. Free and local (ffmpeg + ffprobe; faster-whisper optional).

Usage:
    python3 -I -B tools/teardown.py REF.mp4 OUT_DIR [--threshold 0.3] [--grid-fps 2] [--language en] [--no-transcript]

Writes into OUT_DIR:
    info.json        size, fps, duration, audio present, loudness
    shots.json       every shot: start, end, duration, frame files, words spoken inside it
    frames/          per shot: first / middle / last frame (540 px wide) -> look at every one
    grid/            contact sheets, GRID_FPS frames per second, timestamp burned on each tile
    transcript.json  word timings (if faster-whisper is installed)
    silences.json    pauses over 0.25 s
    teardown.md      the shot table pre-filled with times and words, columns left for the visual read

The script only measures. The visual read (framing, action, on-screen text, emotion) and the copy analysis are done by
looking at the frames and following .claude/skills/ad-teardown/SKILL.md.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

FONT_CANDIDATES = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                   "/Library/Fonts/Arial Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def probe(path):
    p = run(["ffprobe", "-v", "error", "-show_entries",
             "format=duration:stream=codec_type,width,height,r_frame_rate", "-of", "json", str(path)])
    if p.returncode:
        sys.exit(f"ffprobe failed: {p.stderr.strip()}")
    d = json.loads(p.stdout)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    if not v:
        sys.exit("no video stream")
    num, den = (v.get("r_frame_rate") or "0/1").split("/")
    return {"duration": float(d["format"]["duration"]), "w": v["width"], "h": v["height"],
            "fps": round(float(num) / float(den or 1), 3),
            "audio": any(s["codec_type"] == "audio" for s in d["streams"])}


def cuts(path, threshold):
    p = run(["ffmpeg", "-hide_banner", "-i", str(path), "-vf", f"select='gt(scene,{threshold})',showinfo",
             "-vsync", "vfr", "-f", "null", "-"])
    return sorted({round(float(t), 3) for t in re.findall(r"pts_time:([0-9.]+)", p.stderr)})


def silences(path):
    p = run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "silencedetect=noise=-35dB:d=0.25", "-f", "null", "-"])
    out, start = [], None
    for line in p.stderr.splitlines():
        m = re.search(r"silence_start: ([0-9.]+)", line)
        if m:
            start = float(m.group(1))
        m = re.search(r"silence_end: ([0-9.]+)", line)
        if m and start is not None:
            out.append({"start": round(start, 2), "end": round(float(m.group(1)), 2)})
            start = None
    return out


def loudness(path):
    p = run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128", "-f", "null", "-"])
    m = re.findall(r"I:\s+(-?[0-9.]+) LUFS", p.stderr)
    return float(m[-1]) if m else None


def grab(path, t, out):
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(t, 0):.3f}", "-i", str(path), "-frames:v", "1",
         "-vf", "scale=540:-2", str(out)])
    return out.exists()


def grid(path, out_dir, fps, info):
    font = next((f for f in FONT_CANDIDATES if Path(f).exists()), None)
    label = (f",drawtext=fontfile={font}:text='%{{pts\\:hms}}':x=8:y=8:fontsize=28:fontcolor=white:"
             f"box=1:boxcolor=black@0.6" if font else "")
    per_sheet = 18  # 6 x 3 tiles
    n = max(1, int(info["duration"] * fps / per_sheet) + 1)
    run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vf",
         f"fps={fps},scale=300:-2{label},tile=6x3", "-frames:v", str(n), str(out_dir / "sheet_%02d.jpg")])


def join_words(ws):
    return re.sub(r" (?=['’])", "", " ".join(w["word"] for w in ws))


def transcribe(path, out, language):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None, "faster-whisper not installed (pip install -r tools/requirements.txt)"
    try:
        model = WhisperModel("small", device="cpu", compute_type="int8")
        segs, inf = model.transcribe(str(path), language=language, word_timestamps=True, vad_filter=False)
        words = [{"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)}
                 for s in segs for w in (s.words or [])]
    except Exception as e:  # model download blocked, bad audio, ...
        return None, f"transcription failed: {e}"
    data = {"language": inf.language, "text": join_words(words), "words": words}
    out.write_text(json.dumps(data, indent=1))
    return data, None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref")
    ap.add_argument("out")
    ap.add_argument("--threshold", type=float, default=0.3, help="scene-change sensitivity (lower = more cuts)")
    ap.add_argument("--grid-fps", type=float, default=2)
    ap.add_argument("--language", default=None)
    ap.add_argument("--no-transcript", action="store_true")
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found")
    ref, out = Path(a.ref), Path(a.out)
    for d in ("frames", "grid"):
        (out / d).mkdir(parents=True, exist_ok=True)

    info = probe(ref)
    info["loudness_lufs"] = loudness(ref) if info["audio"] else None
    (out / "info.json").write_text(json.dumps(info, indent=1))

    bounds = [0.0] + [c for c in cuts(ref, a.threshold) if 0.2 < c < info["duration"] - 0.1] + [info["duration"]]
    sil = silences(ref) if info["audio"] else []
    (out / "silences.json").write_text(json.dumps(sil, indent=1))

    words, note = None, None
    if info["audio"] and not a.no_transcript:
        tr, note = transcribe(ref, out / "transcript.json", a.language)
        words = tr["words"] if tr else None

    shots = []
    for i, (s, e) in enumerate(zip(bounds, bounds[1:]), 1):
        f = []
        for tag, t in (("a", s + 0.04), ("m", (s + e) / 2), ("z", e - (0.25 if e >= info["duration"] - 0.01 else 0.08))):
            p = out / "frames" / f"s{i:02d}_{tag}.jpg"
            if grab(ref, t, p):
                f.append(str(p.relative_to(out)))
        said = join_words([w for w in words if s <= (w["start"] + w["end"]) / 2 < e]) if words else None
        shots.append({"shot": i, "start": round(s, 2), "end": round(e, 2), "dur": round(e - s, 2),
                      "frames": f, "words": said})
    (out / "shots.json").write_text(json.dumps(shots, indent=1))
    grid(ref, out / "grid", a.grid_fps, info)

    durs = [x["dur"] for x in shots]
    nwords = len(words) if words else 0
    lines = [f"# Teardown: {ref.name}", "",
             f"{info['w']}x{info['h']}, {info['fps']} fps, {info['duration']:.2f} s, audio: {info['audio']}, "
             f"loudness: {info['loudness_lufs']} LUFS", "",
             f"Shots: {len(shots)}, average {sum(durs) / len(durs):.2f} s, longest {max(durs):.2f} s, "
             f"first cut at {shots[0]['end']:.2f} s", "",
             f"Words: {nwords} ({nwords / info['duration'] * 60:.0f} per minute)" if words else
             f"Words: no transcript ({note or 'no audio'})", "",
             "Pauses over 0.25 s: " + (", ".join(f"{x['start']}-{x['end']}" for x in sil) or "none"), "",
             "| # | In-Out | Dur | Framing / subject | Action / performance | On-screen text | Sound | Words | Job in the ad |",
             "|---|---|---|---|---|---|---|---|---|"]
    for x in shots:
        lines.append(f"| {x['shot']} | {x['start']:.2f}-{x['end']:.2f} | {x['dur']:.2f} |  |  |  |  | "
                     f"{(x['words'] or '').replace('|', '/')} |  |")
    (out / "teardown.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:9]))
    print(f"\nwrote {out}/teardown.md, shots.json, {len(shots) * 3} frames, grid sheets"
          + (f"\nnote: {note}" if note else ""))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# Changelog: 2026-11-16: install hints name apt / uv on Linux (WSL Ubuntu), brew on a Mac.
# Library v2, 2026-11-09 (reality-drama-engine)
# Changelog: 2026-11-12 Sound stays in sync at any length: pieces keep uncompressed sound cut to exactly their frames,
#            one AAC encode at the end (the old per-piece AAC + copy-join lost ~30 ms per join: 2.9 s after ~95 joins).
#            Sync self-check FAILs above 40 ms (total and at every join). Per-clip speech levelling, 15 ms fades at
#            every join, room tone instead of digital silence under silent inserts, narration blocks over clips, still
#            end cards, optional music bed, -14 LUFS by one gain + a peak limiter, silence-hole and level checks.
#            `--check FILE` checks any finished video. Always use this script; never write your own joiner.
# 2026-11-12b Mono sound (a TTS voiceover, a mono clip or bed) is copied to both channels at full level; before, it
#            came out 3 dB too quiet, so every narrated film failed the speech-level check (final simulations).
#            The speech-level check reads the mix before the music bed: with a bed, a narration block whose voice
#            pauses was measured partly on the music and failed falsely (4.5 dB on a 7-minute test film).
# 2026-11-12c Real buyer test (real Omni clips): every Omni clip starts with 30-70 ms of digital silence, so clips cut
#            at in=0 left tiny dead-silence holes at the joins: a clip's start now skips that silent run (whole
#            frames, picture and sound together). New WARN lines with measured times instead of transcript times:
#            the first word of a hook later than 0.15 s (dead air: "set in to ..."), and speech still running at a
#            clip's out point (a word cut off: "move out to ..."). Speech-to-text word times were 0.3-0.45 s off on
#            real clips, so in/out points taken from a transcript cut words and left dead air.
"""Assemble generated clips into one finished 9:16 ad per hook. Free and local (ffmpeg + ffprobe).

Usage:
    python3 assemble.py edit.json            # build every hook in edit.json
    python3 assemble.py edit.json A          # build only hook A
    python3 assemble.py --check final.mp4    # sync check on any finished video (sound vs picture)
    python3 assemble.py --help

edit.json (paths are relative to the folder edit.json sits in):
{
  "code": "LP.1",
  "loudness": -14,
  "music": {"file": "music/bed.mp3", "under_voice_db": 20},     (optional: a bed under the whole film)
  "hooks": {
    "A": [ {"clip": "clips/c1.mp4", "in": 0.0, "out": null, "trim_end": 0.05},
           {"clip": "clips/c2.mp4"},
           {"vo": "voice/n1.mp3", "clips": [{"clip": "clips/c3.mp4"}, {"clip": "clips/c4.mp4", "out": 2.5}]},
           {"image": "stills/end.png", "dur": 2.0} ],
    "B": [ ... ]
  }
}
  in / out        seconds inside the clip to use (out null = to the end)
  trim_end        seconds cut off the end (for Omni's smeared last frame), default 0
  level           false = leave this clip's sound level as it is (default: speech is levelled)
  vo / clips      a voiceover (narration) over a run of clips; the clips' own sound sits clip_sound_db under
                  (default -18, "bed_db" works too); vo_in = where in the voice file to start, vo_at = seconds into
                  the block. A list of items saved as {"items": [...]} by an older editor can go straight under a hook.
  image / dur     a still as a piece (end card or insert): slow push-in, room tone of the clip before it;
                  "push": false = no movement
  under_voice_db  how far the music bed sits under the voice, in dB (default 20; 18-22 is "barely there")

What it does: every piece is scaled/padded to 1080x1920 at 24 fps (ASSEMBLE_FPS=30 to override); its sound is cut to exactly its picture length
(uncompressed, so nothing slips at the joins); speech is levelled clip by clip so a voice does not jump between clips;
every join gets a 15 ms fade (no clicks); a clip without sound (a still-only insert) gets the room tone of the clip
before it instead of dead digital silence; the optional bed goes under everything; one gain brings the whole film to
-14 LUFS (a peak limiter keeps the true peak near -1.5 dBTP) and the sound is encoded to AAC once. Output: final/<code>_<hook>.mp4 next to edit.json.

Checks after export (FAIL = exit code 1, never a silent OK):
  sync      decoded sound length vs picture length, and the offset at every join: FAIL above 0.040 s
  holes     digital silence over 0.3 s inside the film: FAIL
  levels    speech level spread between clips after levelling: FAIL above 4 dB (that is about +-2 dB)
  format    size, fps, sound present, black frames; WARN when a film over 45 s has no music bed
"""
import array
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

import os
W, H, FPS = 1080, 1920, int(os.environ.get("ASSEMBLE_FPS", "24"))  # Seedance renders 24 fps; keep it (30 duplicates frames)
SR = 48000
SPF = SR // FPS                   # sound samples per picture frame (1600)
FADE = 0.015                      # fade at every join, seconds
SPEECH_TARGET = -20.0             # speech level every clip is levelled to (dBFS RMS of its speech)
MAX_GAIN = 12.0                   # never push a clip up or down more than this
SYNC_TOL = 0.040                  # sound vs picture, seconds
HOLE_S = 0.3                      # digital silence longer than this inside the film = FAIL
LEVEL_SPREAD = 4.0                # dB between the quietest and loudest speech clip after levelling
TONE_MAX_DB = -48.0               # room tone under an insert is never louder than this
LIMIT = 10 ** (-2.0 / 20)         # peak limiter ceiling (-2 dBFS, so the true peak stays near -1.5 dBTP)


def run(cmd, text=True):
    p = subprocess.run(cmd, capture_output=True, text=text)
    if p.returncode != 0:
        err = p.stderr if text else p.stderr.decode("utf-8", "replace")
        sys.exit(f"Command failed: {' '.join(map(str, cmd[:4]))} ...\n{err[-1500:]}")
    return p


def probe(path):
    p = run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate,channels",
             "-of", "json", str(path)])
    data = json.loads(p.stdout)
    streams = data.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), {})
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    a = next((s for s in streams if s.get("codec_type") == "audio"), {})
    num, _, den = (v.get("r_frame_rate") or "0/1").partition("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 0.0
    return {"duration": float(data.get("format", {}).get("duration", 0) or 0), "w": v.get("width"),
            "h": v.get("height"), "fps": fps, "audio": has_audio, "channels": int(a.get("channels") or 0)}


def stereo(channels):
    """Filter that makes stereo. Mono goes to both channels at full level (aformat would lower it by 3 dB)."""
    return "pan=stereo|c0=c0|c1=c0" if channels == 1 else "aformat=channel_layouts=stereo"


# ------------------------------------------------------------------ sound measuring (standard library only)
def pcm(path, start=None, end=None, rate=16000):
    """Mono 16-bit samples of a file's sound (optionally a time range)."""
    cmd = ["ffmpeg", "-v", "error"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}", "-to", f"{end:.3f}"]
    cmd += ["-i", str(path), "-map", "0:a:0", "-ac", "1", "-ar", str(rate), "-f", "s16le", "-"]
    p = subprocess.run(cmd, capture_output=True)
    a = array.array("h")
    a.frombytes(p.stdout[: len(p.stdout) // 2 * 2])
    return a


def frame_db(a, rate=16000, win=0.05):
    n = max(1, int(rate * win))
    out = []
    for i in range(0, len(a) - n + 1, n):
        s = sum(x * x for x in a[i:i + n]) / n
        out.append(10 * math.log10(s / 32768.0 ** 2 + 1e-12))
    return out


def speech_db(a, rate=16000):
    """Level of the speech in a clip: energy mean of the frames within 20 dB of its loud end. None = no speech."""
    dbs = frame_db(a, rate)
    if not dbs:
        return None
    top = sorted(dbs)[int(len(dbs) * 0.95) - 1 if len(dbs) > 1 else 0]
    loud = [d for d in dbs if d > max(top - 20, -45)]
    if len(loud) * 0.05 < 0.3:          # under 0.3 s of speech: room tone or an insert, never levelled
        return None
    return 10 * math.log10(sum(10 ** (d / 10) for d in loud) / len(loud))


def digital_holes(a, rate=16000, min_s=0.06):
    """Runs of digital silence (|sample| <= 3 of 32768, about -80 dBFS) as (start, length) in seconds."""
    runs, st = [], None
    step = rate // 100                   # 10 ms steps
    for i in range(0, len(a), step):
        quiet = max(abs(x) for x in a[i:i + step]) <= 3
        if quiet and st is None:
            st = i
        elif not quiet and st is not None:
            if (i - st) / rate >= min_s:
                runs.append((st / rate, (i - st) / rate))
            st = None
    if st is not None and (len(a) - st) / rate >= min_s:
        runs.append((st / rate, (len(a) - st) / rate))
    return runs


def speech_edges(a, lvl, rate=16000, win=0.02):
    """First and last moment (s) the sound is within 15 dB of the clip's speech level; None = no speech."""
    idx = [k for k, d in enumerate(frame_db(a, rate, win)) if d > lvl - 15]
    return (idx[0] * win, (idx[-1] + 1) * win) if idx else None


def skip_lead_silence(src, start, end):
    """Omni clips open with 30-70 ms of digital silence: start after it (whole frames) so no join has a dead hole."""
    runs = digital_holes(pcm(src, start, min(end, start + 0.3)), min_s=0.01)
    if runs and runs[0][0] < 0.005 and runs[0][1] < 0.25:
        new = start + math.ceil(runs[0][1] * FPS - 1e-6) / FPS
        if end - new >= 0.3:
            return new
    return start


# ------------------------------------------------------------------ building
def room_tone(prev_piece, dst, seconds=0.5):
    """The quietest half second of the previous piece, made into a seamless loop (forward + reversed)."""
    a = pcm(prev_piece, rate=SR)
    n = int(SR * seconds)
    if len(a) < n * 2:
        return None
    best, best_i = None, 0
    for i in range(0, len(a) - n, n // 4):
        e = sum(x * x for x in a[i:i + n:8])
        if best is None or e < best:
            best, best_i = e, i
    lvl = 10 * math.log10(best / (n / 8) / 32768.0 ** 2 + 1e-12)
    gain = min(0.0, TONE_MAX_DB - lvl)   # quieter if that stretch was not real room tone
    t0 = best_i / SR
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.4f}", "-t", f"{seconds:.3f}", "-i", str(prev_piece),
         "-filter_complex", f"[0:a]volume={gain:.2f}dB,asplit[a][b];[b]areverse[r];[a][r]concat=n=2:v=0:a=1[o]",
         "-map", "[o]", "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", str(dst)])
    return dst


def piece(src, dst, start, end, gain_db, tone):
    """One piece: 1080x1920, 30 fps, exactly N frames, and exactly N x 1600 sound samples (uncompressed)."""
    frames = max(1, round((end - start) * FPS))
    secs = frames / FPS
    info = probe(src)
    vf = (f"setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
          f"fps={FPS},setsar=1,tpad=stop_mode=clone:stop_duration=1")
    fades = f"afade=t=in:d={FADE},afade=t=out:st={secs - FADE:.4f}:d={FADE}"
    tail = f"apad,atrim=end_sample={frames * SPF},asetpts=N/SR/TB"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
           "-i", str(src)]
    if info["audio"]:
        af = f"[0:a]aresample={SR},{stereo(info['channels'])},volume={gain_db:.2f}dB,{tail},{fades}[a]"
    elif tone:
        cmd += ["-stream_loop", "-1", "-i", str(tone)]
        af = f"[1:a]aresample={SR},aformat=channel_layouts=stereo,atrim=end_sample={frames * SPF},{tail},{fades}[a]"
    else:
        cmd += ["-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo"]
        af = f"[1:a]{tail}[a]"
    cmd += ["-filter_complex", f"[0:v]{vf}[v];{af}", "-map", "[v]", "-map", "[a]", "-frames:v", str(frames),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "pcm_f32le", "-ar", str(SR), str(dst)]
    run(cmd)
    return frames


def integrated(path):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    tail = p.stderr[p.stderr.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
    tp = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", tail)
    return (float(i.group(1)) if i else None), (float(tp.group(1)) if tp and tp.group(1) != "-inf" else None)


def final_mix(src_args, pre, loudness, joined, out, work, hook):
    """Mix (bed) -> one gain to the loudness target + a peak limiter (no pumping) -> ONE AAC encode."""
    mix, lev = work / f"{hook}_mix.wav", work / f"{hook}_mix_level.wav"
    run(["ffmpeg", "-v", "error", "-y", *src_args, "-filter_complex", f"{pre}[o]", "-map", "[o]",
         "-c:a", "pcm_f32le", "-ar", str(SR), str(mix)])
    lufs, _ = integrated(mix)
    gain = loudness - (lufs if lufs is not None else loudness)
    for _ in range(3):   # the limiter shaves a little off: measure and correct
        run(["ffmpeg", "-v", "error", "-y", "-i", str(mix), "-af",
             f"volume={gain:.2f}dB,alimiter=limit={LIMIT:.4f}:level=false:attack=5:release=60",
             "-c:a", "pcm_f32le", "-ar", str(SR), str(lev)])
        got, _ = integrated(lev)
        if got is None or abs(got - loudness) <= 0.3:
            break
        gain += loudness - got
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(joined), "-i", str(lev), "-map", "0:v",
         "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
    mix.unlink(missing_ok=True)
    lev.unlink(missing_ok=True)


IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp"}


def clip_range(base, hook, i, it):
    src = (base / it["clip"]).resolve()
    if not src.exists():
        sys.exit(f"Hook {hook}: clip not found: {it['clip']}")
    info = probe(src)
    dur = info["duration"]
    start = float(it.get("in") or 0.0)
    end = float(it["out"]) if it.get("out") is not None else dur
    end = min(end, dur) - float(it.get("trim_end") or 0.0)
    if end - start < 0.3:
        sys.exit(f"Hook {hook}, item {i + 1}: less than 0.3 s left after in/out/trim_end.")
    return src, info, start, end


def image_piece(base, it, dst, tone):
    """A still (end card, insert) as a piece: a slow push-in, the room tone of the clip before it."""
    src = (base / it["image"]).resolve()
    if not src.exists():
        sys.exit(f"image not found: {it['image']}")
    secs = float(it.get("dur", 2.0))
    clipf = dst.with_name(dst.stem + "_img.mp4")
    zoom = "1+0.0005*on" if it.get("push", True) else "1"
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(src), "-vf",
         f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='{zoom}':"
         f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}", "-t", f"{secs + 0.5:.3f}",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", str(clipf)])
    return piece(clipf, dst, 0.0, secs, 0.0, tone)


def vo_block(base, hook, i, it, dst, work):
    """A voiceover over several clips: the clips' own sound sits clip_sound_db under, the voice is levelled."""
    voice = (base / it["vo"]).resolve()
    if not voice.exists():
        sys.exit(f"voice file not found: {it['vo']}")
    under = float(it.get("clip_sound_db", it.get("bed_db", -18)))   # bed_db: older timelines used this name
    subs, frames = [], 0
    for k, sub in enumerate(it.get("clips") or []):
        src, info, start, end = clip_range(base, hook, i, sub)
        sp = work / f"{dst.stem}_{k:02d}.mov"
        frames += piece(src, sp, start, end, under, None)
        subs.append(sp)
    if not subs:
        sys.exit(f"Hook {hook}, item {i + 1}: a vo block needs a clips list")
    secs = frames / FPS
    v_in = float(it.get("vo_in") or 0.0)
    v_dur = probe(voice)["duration"] - v_in
    at = float(it.get("vo_at") or 0.0)
    if at + v_dur > secs + 0.25:
        sys.exit(f"Hook {hook}, item {i + 1}: voice {it['vo']} runs {at + v_dur:.2f} s but its clips only "
                 f"{secs:.2f} s. Add or lengthen clips; never speed the voice up.")
    lvl = speech_db(pcm(voice, v_in, v_in + v_dur))
    gain = max(-MAX_GAIN, min(MAX_GAIN, SPEECH_TARGET - lvl)) if lvl is not None else 0.0
    lst = work / f"{dst.stem}_list.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in subs), encoding="utf-8")
    block = work / f"{dst.stem}_clips.mov"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(block)])
    delay = int(at * 1000)
    run(["ffmpeg", "-v", "error", "-y", "-i", str(block), "-ss", f"{v_in:.3f}", "-i", str(voice), "-filter_complex",
         f"[1:a]aresample={SR},{stereo(probe(voice)['channels'])},volume={gain:.2f}dB,adelay={delay}|{delay},"
         f"afade=t=in:d={FADE}[v];[0:a][v]amix=inputs=2:duration=first:normalize=0,apad,"
         f"atrim=end_sample={frames * SPF},asetpts=N/SR/TB[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy",
         "-c:a", "pcm_f32le", "-ar", str(SR), str(dst)])
    return frames, lvl


def build(base, code, hook, items, cfg, work):
    pieces, plan, prev_with_sound, warns = [], [], None, []
    for i, it in enumerate(items):
        dst = work / f"{hook}_{i:03d}.mov"
        def tone():
            return room_tone(prev_with_sound, work / f"{hook}_{i:03d}_tone.wav") if prev_with_sound else None
        if it.get("vo"):
            frames, lvl = vo_block(base, hook, i, it, dst, work)
            name, sound, gain = it["vo"], True, 0.0
        elif it.get("image"):
            frames, lvl, name, sound, gain = image_piece(base, it, dst, tone()), None, it["image"], False, 0.0
        else:
            src, info, start, end = clip_range(base, hook, i, it)
            gain, lvl = 0.0, None
            if info["audio"]:
                start = skip_lead_silence(src, start, end)
                a_clip = pcm(src, start, end)
                raw = speech_db(a_clip)
                edges = speech_edges(a_clip, raw) if raw is not None else None
                if edges and i == 0 and edges[0] > 0.15:
                    warns.append(f"{it['clip']}: first word at {edges[0]:.2f} s into the hook (dead air): set \"in\" "
                                 f"to about {start + edges[0] - 0.05:.2f}")
                if edges and edges[1] > (end - start) - 0.03 and end < info["duration"] - 0.05:
                    warns.append(f"{it['clip']}: speech still running at its out point {end:.2f} s (a word may be cut "
                                 f"off): move \"out\" later, then listen to the join")
                if raw is not None and it.get("level", True) is not False:
                    lvl = raw
                    gain = max(-MAX_GAIN, min(MAX_GAIN, SPEECH_TARGET - lvl))
            frames = piece(src, dst, start, end, gain, None if info["audio"] else tone())
            name, sound = it["clip"], info["audio"]
        if sound:
            prev_with_sound = dst
        pieces.append(dst)
        plan.append({"clip": name, "frames": frames, "sound": sound, "speech_db": lvl, "gain": gain})
    lst = work / f"{hook}_list.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in pieces), encoding="utf-8")
    joined = work / f"{hook}_joined.mov"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(joined)])
    out = base / "final" / f"{code}_{hook}.mp4"
    out.parent.mkdir(exist_ok=True)
    total = sum(p["frames"] for p in plan) / FPS
    music = cfg.get("music") or {}
    bed = (base / music["file"]).resolve() if music.get("file") else None
    if bed is not None and not bed.exists():
        sys.exit(f"music file not found: {music['file']}")
    if bed is not None:
        under = float(music.get("under_voice_db", 20))
        bed_lvl = speech_db(pcm(bed), 16000) or -30.0
        bgain = (SPEECH_TARGET - under) - bed_lvl
        src_args = ["-i", str(joined), "-stream_loop", "-1", "-i", str(bed)]
        pre = (f"[1:a]aresample={SR},{stereo(probe(bed)['channels'])},atrim=0:{total:.3f},volume={bgain:.2f}dB,"
               f"afade=t=in:d=0.5,afade=t=out:st={max(0.0, total - 1.0):.3f}:d=1[bed];"
               "[0:a][bed]amix=inputs=2:duration=first:normalize=0")
    else:
        src_args, pre = ["-i", str(joined)], "[0:a]anull"
    final_mix(src_args, pre, float(cfg.get("loudness", -14)), joined, out, work, hook)
    return out, plan, pieces, bed is not None, warns


# ------------------------------------------------------------------ checks
def decoded_audio_seconds(path):
    """Count every decoded sound sample (what a player actually plays), not the container's length."""
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-ac", "1", "-ar", str(SR),
                          "-f", "s16le", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = 0
    while True:
        b = p.stdout.read(1 << 20)
        if not b:
            break
        n += len(b)
    p.wait()
    return n / 2 / SR


def picture_timeline(path, fps):
    """(end of the picture on its own timeline, number of timestamp gaps over 1.5 frames)."""
    p = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=pts_time",
             "-of", "csv=p=0", str(path)])
    ts = sorted(float(x.strip(",")) for x in p.stdout.split() if x.strip(",") not in ("", "N/A"))
    if not ts:
        return 0.0, 0
    gaps = sum(1 for a, b in zip(ts, ts[1:]) if b - a > 1.5 / fps)
    return ts[-1] + 1 / fps, gaps


def video_frames(path):
    p = run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
             "stream=nb_read_packets", "-of", "csv=p=0", str(path)])
    return int(p.stdout.strip().split(",")[0] or 0)


def pcm_samples(path):
    """Sound samples in an uncompressed piece (exact)."""
    p = run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=duration_ts,time_base",
             "-of", "json", str(path)])
    s = json.loads(p.stdout)["streams"][0]
    num, _, den = s["time_base"].partition("/")
    return round(int(s["duration_ts"]) * int(num) * SR / int(den))


def irregular_timestamps(path):
    """Sound packets that overlap or leave a gap (the sign of a copy-join of separately encoded pieces)."""
    p = run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "packet=pts_time,duration_time",
             "-of", "csv=p=0", str(path)])
    pk = []
    for line in p.stdout.split():
        a, _, b = line.partition(",")
        try:
            pk.append((float(a), float(b)))
        except ValueError:
            continue
    bad, overlap = 0, 0.0
    for (t1, d1), (t2, _) in zip(pk[1:], pk[2:]):
        gap = t2 - (t1 + d1)
        if abs(gap) > 0.002:
            bad += 1
            overlap += -gap if gap < 0 else 0.0
    return bad, overlap


def sync_check(path, fps=FPS):
    """(problems, line) for any finished file: decoded sound vs picture, and irregular sound timestamps."""
    a = decoded_audio_seconds(path)
    n = video_frames(path)
    v, vgaps = picture_timeline(path, fps)
    bad, overlap = irregular_timestamps(path)
    problems = []
    if abs(a - v) > SYNC_TOL:
        problems.append(f"sound {a:.3f} s vs picture {v:.3f} s: {a - v:+.3f} s off (limit {SYNC_TOL:.3f})")
    if abs(v - n / fps) > SYNC_TOL or vgaps:
        problems.append(f"picture timeline {v:.3f} s for {n} frames ({n / fps:.3f} s), {vgaps} timestamp gap(s): "
                        "the picture holds or skips at joins")
    if bad:
        problems.append(f"{bad} irregular sound timestamps ({overlap:.2f} s of overlap): sound slides at the joins")
    return problems, (f"sync: sound {a:.3f} s, picture {v:.3f} s ({n} frames), diff {(a - v) * 1000:+.1f} ms, "
                      f"irregular timestamps sound {bad} / picture {vgaps}")


def join_check(plan, pieces):
    """Offset at every join, measured on the pieces themselves."""
    worst, worst_at, s_sum, f_sum = 0.0, 0, 0, 0
    for i, p in enumerate(pieces):
        s_sum += pcm_samples(p)
        f_sum += video_frames(p)
        off = s_sum / SR - f_sum / FPS
        if abs(off) > abs(worst):
            worst, worst_at = off, i + 1
    problems = [f"join {worst_at}: sound {worst * 1000:+.1f} ms off the picture"] if abs(worst) > SYNC_TOL else []
    return problems, f"joins: {len(pieces) - 1}, worst offset {worst * 1000:+.1f} ms (after piece {worst_at})"


def sound_checks(out, plan, has_bed, level_src=None):
    a = pcm(out)
    lv_a = pcm(level_src) if level_src is not None and Path(level_src).exists() else a   # levels: mix before the bed
    dur = len(a) / 16000
    problems, warns = [], []
    holes = [(t, d) for t, d in digital_holes(a, min_s=HOLE_S) if t > 0.5 and t + d < dur - 0.5]
    if holes:
        problems.append(f"{len(holes)} digital-silence hole(s) over {HOLE_S} s: " +
                        ", ".join(f"{t:.1f}s ({d:.2f} s)" for t, d in holes[:8]))
    lv, t = [], 0.0
    for p in plan:
        secs = p["frames"] / FPS
        if p["speech_db"] is not None:
            d = speech_db(lv_a[int(t * 16000):int((t + secs) * 16000)])
            if d is not None:
                lv.append((d, p["clip"]))
        t += secs
    spread = (max(lv)[0] - min(lv)[0]) if len(lv) > 1 else 0.0
    if spread > LEVEL_SPREAD:
        lo, hi = min(lv), max(lv)
        problems.append(f"speech level spread {spread:.1f} dB between clips ({lo[1]} {lo[0]:.1f} dB, "
                        f"{hi[1]} {hi[0]:.1f} dB): a clip could not be levelled (gain limit {MAX_GAIN:.0f} dB)")
    if dur > 45 and not has_bed:
        warns.append(f"{dur:.0f} s of dialogue with no music bed: add \"music\" to edit.json (see SKILL.md Step 8)")
    return problems, warns, f"sound: {len(holes)} holes, speech spread {spread:.1f} dB over {len(lv)} clips"


def verify(out):
    info, problems = probe(out), []
    if (info["w"], info["h"]) != (W, H):
        problems.append(f"size {info['w']}x{info['h']} (want {W}x{H})")
    if abs(info["fps"] - FPS) > 0.1:
        problems.append(f"fps {info['fps']:.2f} (want {FPS})")
    if not info["audio"]:
        problems.append("no sound track")
    if info["duration"] < 1:
        problems.append(f"duration {info['duration']:.2f} s")
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out), "-vf", "blackdetect=d=0.3:pix_th=0.08",
                        "-an", "-f", "null", "-"], capture_output=True, text=True)
    blacks = [ln for ln in p.stderr.splitlines() if "black_start" in ln]
    if blacks:
        problems.append(f"{len(blacks)} black stretch(es) of 0.3 s or more")
    return info, problems


def check_only(path):
    path = Path(path)
    if not path.exists():
        sys.exit(f"not found: {path}")
    fps = probe(path)["fps"] or FPS
    problems, line = sync_check(path, fps)
    print(line)
    print(("FAIL: " + "; ".join(problems)) if problems else "PASS: sound and picture in sync")
    return 1 if problems else 0


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if len(argv) > 1 else 2
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"Missing {tool}. Install it: " + ("sudo apt install -y ffmpeg" if sys.platform.startswith("linux") else "brew install ffmpeg"))
    if argv[1] == "--check":
        return check_only(argv[2]) if len(argv) > 2 else 2
    edit_path = Path(argv[1]).resolve()
    cfg = json.loads(edit_path.read_text(encoding="utf-8"))
    base = edit_path.parent
    code = cfg.get("code", "AD")
    hooks = cfg.get("hooks") or {}
    if len(argv) > 2:
        hooks = {argv[2]: hooks.get(argv[2]) or sys.exit(f"Hook {argv[2]} not in edit.json")}
    work = base / "work_assemble"
    work.mkdir(exist_ok=True)
    failed = 0
    for hook, items in hooks.items():
        out, plan, pieces, has_bed, cut_warns = build(base, code, hook, items, cfg, work)
        info, problems = verify(out)
        p_sync, l_sync = sync_check(out)
        p_join, l_join = join_check(plan, pieces)
        p_snd, warns, l_snd = sound_checks(out, plan, has_bed, work / f"{hook}_joined.mov")
        warns = cut_warns + warns
        problems += p_sync + p_join + p_snd
        failed += bool(problems)
        print(f"{out.relative_to(base)}  {info['duration']:.2f} s  {info['w']}x{info['h']}  {info['fps']:.0f} fps  "
              f"sound={'yes' if info['audio'] else 'no'}  clips={len(plan)}  levelled={sum(1 for p in plan if p['speech_db'] is not None)}")
        print(f"  {l_sync}\n  {l_join}\n  {l_snd}")
        for w_ in warns:
            print(f"  WARN: {w_}")
        print("  " + ("FAIL: " + "; ".join(problems) if problems else "PASS: all checks"))
    print("Next: transcribe the FINAL file, then burn captions with scripts/captions.py, then look at the frames.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

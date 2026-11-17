# QC commands

Run on the 480p raw clip before upscaling, and again on the final file.

```bash
IN=ads/<code>/clips/raw/seg1.mp4
# contact sheet, 2 frames per second (open it and look before showing anyone)
ffmpeg -v error -y -i $IN -vf "fps=2,scale=300:-1,tile=7x3" -frames:v 1 sheet.jpg
# cut times
ffmpeg -hide_banner -i $IN -vf "select='gt(scene,0.2)',showinfo" -vsync vfr -f null - 2>&1 | grep -o "pts_time:[0-9.]*"
# pauses
ffmpeg -hide_banner -i $IN -af "silencedetect=noise=-35dB:d=0.2" -f null - 2>&1 | grep silence_
# transcript with word times (local, free) then word-by-word check against the script
python3 -I -B tools/fw_transcribe.py $IN ads/<code>/clips/tr --language en
python3 -I -B tools/wordcheck.py "<exact lines of this segment>" ads/<code>/clips/tr/seg1.json
```

Captions on the FINAL assembled file (never on the clips):

```bash
python3 -I -B tools/fw_transcribe.py ads/<code>/final/<CODE>_A.mp4 ads/<code>/final/tr --language en
python3 -I -B tools/captions.py ads/<code>/final/<CODE>_A.mp4 ads/<code>/final/tr/<CODE>_A.json \
  ads/<code>/final/<CODE>_A_cap.mp4 --script @ads/<code>/script_A.txt [--glossary ads/<code>/GLOSSARY.txt]
```

Captions sit at 62 % of the height (inside the safe zone). If one covers a mouth or the product: `--y 0.55` or `0.7`,
or `--y-at "12.5=0.45"` from a given second. Never burn captions twice.

Film test by eye: on mute it reads as a movie scene; without picture it sounds like location sound; a paused
close-up could be a film still; nobody looks like they know they are in an ad.

Known Seedance flaws to look for: printed documents render as gibberish (keep text inserts under 1.3 s or angled
away); uniforms gain wrong insignia; props swap hands; wardrobe bleeds between similar characters; people meant to
sit together get framed alone.

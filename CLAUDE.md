# ai-drama-videos

High-converting live-action drama ads: **Seedance 2.5 at 480p -> SeedVR2 upscale to 1080x1920 -> assemble, QC,
captions.** Generation and upscaling run on whichever API provider has credits; no Starpop or Higgsfield plans.

- Workflow and rules: `.claude/skills/drama-ad/SKILL.md` (load it for any ad work).
- Research, angles, hooks, iterations, weekly learning loop: `.claude/skills/creative-strategy/SKILL.md`.
  Per-brand files live in `brands/<brand>/` (context.md, research/, ideas.md, learnings.md, script-rules.md).
- Long-form sung story ads (Ryze-style song VSL, 3-10 min hero's journey): `.claude/skills/song-vsl/SKILL.md`.
- Competitor/winning-ad breakdown -> swipe brief: `.claude/skills/ad-teardown/SKILL.md` (`tools/teardown.py`).
- Tools (Python 3 + ffmpeg, local and free): `tools/assemble.py` (only joiner we use), `tools/remux_audio.sh`
  (audio back onto SeedVR2 output), `tools/wordcheck.py`, `tools/fw_transcribe.py`, `tools/captions.py`,
  `tools/plate_check.py`, `tools/stitch.sh` (quick preview join only).
- Providers and their settings: `providers/README.md`. API keys are never committed; they live in the environment.
- One folder per ad: `ads/<CODE>-<slug>/` with `brief.md`, `script.md`, `prompts/`, `log.md`, `edit.json`,
  `plates.json`. Media (`clips/`, `stills/`, `final/`) is gitignored.
- Python deps for transcripts/captions: `pip install -r tools/requirements.txt`.

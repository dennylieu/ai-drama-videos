---
name: drama-ad
description: Make a high-converting live-action drama ad (9:16, 10-45 s) with Seedance 2.5 at 480p, upscale each approved clip with SeedVR2, then assemble, QC and caption the final 1080x1920 file. Use for any drama ad, story ad, skit ad, dialogue scene, "Netflix-style" or cinematic hook, AI actors, verdict/shame scene, hook variants, or when asked to generate, upscale, stitch or QC drama clips.
---

# Drama Ad (Seedance 2.5 @ 480p -> SeedVR2 -> assemble)

Merged from two sources (see `reference/sources.md`):
- **Creative core = Harris Drama.** Built and measured on Seedance 2.5: single-pass multi-shot scenes with native
  dialogue, film grammar, two proven scene engines, plain-face casting that avoids `ip_detected`.
- **Tooling and QC = Reality Drama Engine.** Sync-safe assembler, word check, local transcripts, captions, plate
  (reference image) discipline.
- **Changed for this repo:** we never pay for a 1080p Seedance render. The 480p render IS the final content;
  SeedVR2 upscales it, so nothing shifts between "draft" and "final" (Harris noted the 1080p finalize is a re-render
  that moves details). Generation runs on whichever API provider has credits (`providers/`).

Detailed craft: `reference/film-grammar.md`. Scene engines and beat maps: `reference/scene-engines.md`.
Prompt templates and proven prompts: `reference/prompts.md`. QC commands: `reference/qc.md`.

## The five non-negotiables (drop one and it reads as an AI ad)

1. One location, one continuous moment, two to four locked characters.
2. Dialogue carries the story; the model cuts like an editor (insert, shot, reverse shot, hold).
3. Someone other than the customer delivers the verdict. The customer never brags, nobody pitches.
4. No product, captions or brand text inside the opening segment. Brand, offer and CTA are added in the edit.
5. Motivated light from the room, a three-colour palette, a background that is alive but out of focus.

## Workflow

### 1. Brief (ask in one message)
Product and what it visibly changes; buyer and the ONE problem; offer or "no offer"; 3 things the ad must never
claim; language/accent; length (10 s hook, 15 s segment, or 30 s = two segments); a real product photo if the
product is revealed; optional reference ad.

### 2. Pick the engine and write 3+ hooks
Before the scene, run `creative-strategy` prompt 15 (pain moments: events with who was there and the place) and, if
research exists, use the purchase trigger (prompt 4) for the stakes and the objection bucket (prompt 5) for who
delivers the verdict. Every hook must point to the body line that pays it off (prompt 12), and the person in the
first line is the person who buys.

Verdict engine or Shame engine (`reference/scene-engines.md`). Offer at least 3 hook options, each as: opening
insert, the lines, the final look. Recommend one and say why. **Wait for approval.**

Dialogue limits (exceed them and Seedance rushes or drops lines):

| Segment | Lines | Words | Shots |
|---|---|---|---|
| 10 s | 2-3 | 6-14 | 5-6 |
| 15 s | 7-8 | 32-40 | 8-10 |

Each line 2-8 words, alternating speakers, numbers spelled out, last shot is a silent held face. Claims are things
another person could see (energetic, rested, sharp): no disease words, no "cured", no years-younger numbers.

### 3. Lock the cast
One sentence per character, reused word for word in every prompt for the film: first name, age, hair, skin, two or
three plain specifics (glasses, broad nose, freckles, double chin), wardrobe colours, one prop. Open the prompt with
"plain, ordinary-looking ... everyday faces, not glamorous, not actors". This is what gets past `ip_detected`.
Body that matters to the story: describe exhaustively plus a negative ("no toned or muscular body").
Different colour block per character; restate it in the negatives when two characters are similar.

**Plates (for multi-segment films and hook variants).** When the same person must appear in more than one
generation, make one approved still per character (and per product, from real photos) and attach it as a reference
image on every generation that supports it. Track them in `plates.json` and run `tools/plate_check.py`. A person
re-drawn from text alone is a new person.

### 3b. Continuity check
Run the script through `reference/continuity.md`: bridge every scene change, no unexplained people, no oracle answers,
believable and consistent timelines, props that make sense where they are.

### 4. Build the prompt
One paragraph in this order (full template in `reference/prompts.md`): opener -> look line -> location -> cast block
-> "Real human photorealism." -> "Spoken dialogue with synced lips, <voice>, natural pace." -> numbered shots with
lines in single quotes -> held end frame -> negatives (-> "do not show yet" product block for a later reveal).

Never write a studio, streamer, film title, actor or director name. Never write "cinematic lighting", "8k",
"hyperrealistic", "epic", "dramatic", lens flare, teal and orange, film grain, slow motion.

### 5. Generate at 480p (one generation per segment)
Settings, whatever the provider calls them: Seedance 2.5, text-to-video (or reference/omni mode with plates
attached), duration 10 or 15, aspect 9:16, **resolution 480p**, audio on. Check the provider's live schema first.

- One generation per segment, never shot by shot: single-pass gives matched light, voices and cutting rhythm.
- Show the price estimate before spending; generate ONE segment first, QC it, then the rest.
- `ip_detected`: fix casting (plain-face rule), strip brand/film words. `nsfw`: remove ambiguity, add "comedic and
  non-sexual". Two different rewrites failing the same way: stop and report.
- Save every raw result to `ads/<code>/clips/raw/` immediately (provider links expire) and log the prompt, provider,
  job id and cost in `ads/<code>/log.md`.

### 6. QC the 480p clip (before paying for upscale)
Run the checks in `reference/qc.md`: contact sheet, cut times, silences, transcript + `tools/wordcheck.py`. Pass marks:
shot count matches; first cut before 2 s; no shot over 3.5 s except the final hold; every line present in order with
the right speaker; faces/wardrobe identical on every return; key emotional beat readable on a paused frame; no
captions, product, music or readable fake text over 1.3 s. Fail = change only the sentences tied to the fault and
re-roll. Do not patch with video-edit models.

### 7. Upscale with SeedVR2
Only approved clips. Upscale each 480x854 clip to 1080x1920 (factor 2.25; some providers take a target height of
1920 or a factor). SeedVR2 outputs often drop audio or change frame count/fps: always run
`tools/remux_audio.sh raw.mp4 upscaled.mp4 out.mp4`, which puts the original audio back and fails on a duration
mismatch. Save to `ads/<code>/clips/up/`. Look at the faces at full size: upscalers can over-sharpen skin; the film
look wants soft real skin. If it looks waxy, try a lower strength/steps setting or another provider.

### 8. Assemble (always `tools/assemble.py`, never a home-made joiner)
Write `ads/<code>/edit.json` (one list per hook: hook clip -> body -> end card). `python3 tools/assemble.py edit.json`
outputs 1080x1920 at 24 fps (Seedance's native rate; `ASSEMBLE_FPS=30` to override), levels speech per clip, fades
joins, -14 LUFS, and FAILs on sync drift. Only deliver a file that printed `PASS`.

### 9. Captions and end card
Deliver two versions per hook: **clean** (film look, Harris default) and **captioned** (muted-feed viewers). Transcribe
the FINAL file, then `tools/captions.py` (see `reference/qc.md`). End card, brand name, offer and CTA are added here,
never rendered by Seedance.

### 10. Deliver
Files per hook (clean + captioned), PASS lines, provider and cost per generation, which clips were re-rolled and why,
and an honest list of remaining flaws. Known faults (garbled label, wardrobe change, repeated shot) are fixed, not
listed as "small flaws".

## Rules
- Never generate before the user approved the hook/script; "make the ad" is not a yes to spend.
- Never present an AI person as a real, named professional or real customer. Check the ad platform's rules on AI
  people and health claims.
- You cannot hear audio: say what you checked by transcript and let the user listen.
- When a fix works twice, write it into `reference/` as a rule (with the date and what it fixed).

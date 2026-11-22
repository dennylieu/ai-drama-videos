# MS1 log

Status: copy breakdown drafted (2026-11-22); waiting for price/offer/guarantee, claims, approval; then the bottle character sheet. Nothing generated or spent.

## 2026-11-22 Bottle character (fal, openai/gpt-image-2/edit, medium, 1024x1536)
- Front pass: 4 variants from the mediskiin.com product photo + reference frame s01_m (style only); user picked #1
  (`brands/mediskiin/character/mediskiin-bottle-front_1.png`). Cost ~4 x $0.05.
- Locked sheet from #1: 34, smug, surprised, point, sympathy (`mediskiin-bottle-<pose>_1.png`), sheet
  `mediskiin-bottle-character-sheet.jpg`. Cost ~5 x $0.05. Notes: the pointing pose points outward, not at its
  label; the three-quarter turn is slight.
- PNGs are gitignored (container only) until copied to Drive.

## 2026-11-22 Test clip b01 hook (fal)
- Start frame: GPT Image 2 edit (stills/hook-start_1.png). Video: fal-ai/wan-3/image-to-video, 10 s, 720p, 9:16, native audio, seed 1253765864, 178 s render.
- Transcript word-perfect vs script. Face drifts mid-clip to a more feminine face (lashes, lipstick) vs the locked sheet; label stays readable. Accent: user to judge by ear.

## 2026-11-22 Hook v2 + bottle batch
- b01-hook-v2: fal-ai/wan-3/reference-to-video, 10 s 720p 9:16, refs = drawer frame + 6 character poses + product photo; face locked (no lashes/lipstick), seed 2146600078, 251 s. Wan cut drawer -> vanity mid-clip.
- Batch b02-b24 (23 clips, 246 s) from prompts/bottle-clips.json: the bottle speaks every line; woman/lab b-roll goes over its audio in the edit.

## 2026-11-22 Batch result
- b02-b10 done (lines all correct by transcript; character consistent). Rough cut b01-v2+b02-b10 = 94 s: final/MS1-roughcut-bottle-b01-b10.mp4 (stitch.sh preview).
- b11-b24 NOT made: fal returned "User is locked. Reason: Exhausted balance" (top up at fal.ai/dashboard/billing). Re-run: batch.py skips finished clips.

## 2026-11-22 Tight cut
- edit.json: each clip trimmed to its words (0.12 s lead, ~0.4-0.5 s tail), inner pauses >0.5 s cut out; b01-tight = drawer pictures (0.8-3.0 s) + vanity, under the audio 3.98-9.78 s. 93 s -> 72 s, assemble.py PASS. Transcript wordcheck: all 190 words present.
- assemble.py "speech still running" WARNs are false alarms from the Wan music bed (wordcheck confirms no cut words).

## 2026-11-22 User: tight cut "better", voice approved.

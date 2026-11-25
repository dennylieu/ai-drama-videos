# Vegas Divorce: generation log

| Date | Segment | Provider / model | Request | Settings | Cost | QC |
|---|---|---|---|---|---|---|
| 2026-11-24 | N1 (conditions + demo) | Higgsfield API, bytedance/seedance-2.5/reference-to-video | see clips/raw/N1/result.json | 15 s, 9:16, 480p draft, audio, refs: vivian, denise, bathroom, product | ≈ $1.77 | 7 shots / 6 cuts as written; 23/23 words (the only flag, "too"→"two", is transcription); faces, wardrobe and set match the locks; the red is pressed in and gone after rubbing; label not readable |

## 2026-11-24 — new segments G1, G2, N2–N5 (Higgsfield API, Seedance 2.5 reference-to-video, 480p draft, $0.1177/s)
Job files: `jobs/<X>.json`. Refs: vivian/denise plates + refs/courtroom.png (G1), refs/hallway.png (G2), refs/bathroom.png (N2–N5), refs/product_in_hand.png (N4).

| Clip | Request id | s | Cost | QC |
|---|---|---|---|---|
| G1 | 01a20f3e-a78e-71fd-9b30-16024cee1ff6 | 6 | $0.71 | PASS: gallery wide (Vivian back in foreground) → close, collar pulled up; no speech |
| G2 | 01a20f3e-b145-785f-af99-c66fb9282341 | 5 | $0.59 | PASS: Vivian walks past vending machine, Denise follows and reaches for the door |
| N2 | 01a20f3e-b6fc-7853-85f6-2f67dc28cd55 | 15 | $1.77 | PASS: 7 shots, all lines (full-file Whisper skipped 3 lines; chunked pass found all), collar tap + neck-touch hold |
| N3 | 01a20f3e-c1f1-7689-b25a-bf75df830c6a | 15 | $1.77 | PASS: 36/36 words, final half-smile hold |
| N4 | 01a20f3e-cf8c-7e1d-8cd9-08bc563b7616 | 15 | $1.77 | FAIL: Vivian exits into a toilet stall; brand heard as "Meta-skin" |
| N4b | 01a20f44-742b-7197-83b1-5af69f88cebb | 15 | $1.77 | PASS: fix = name the wooden exit door ("not a stall door") and write the brand as 'MED-ee-skin'; transcript "Med-D skin, two eyes" |
| N5 | 01a20f3e-e2a0-7f37-8ace-ac3532b35ef0 | 10 | $1.18 | PASS: collar down in mirror → neck close → line 8/8 words |

Total this batch $9.53 (81 s). Rule candidate: write brand names phonetically in the spoken line (MED-ee-skin); and say "exit door, not a stall door" in restrooms.

## 2026-11-25 — SeedVR2 upscale + Vegas v2 assembly
- Upscale: fal `fal-ai/seedvr/upscale/video` (target 1080p, quality high, noise 0.1, seed 20261120), $0.001/MP ≈ $4.30 for 7 clips.
  Output is 1088x1936 and drops 2–5 frames at the END only (checked by frame alignment): cropped to 1080x1920 and
  the raw audio cut to picture length (`clips/up/<X>/final.mp4`). N4b's download was reset; collected by request id.
- Edit: `edit.json` (source `clips/src/marry.mp4` + new clips + cards), ASSEMBLE_FPS=30. 5:29.5, sync +14.7 ms, 25 joins,
  speech spread 0.7 dB. The one FAIL is the black "THAT MORNING" card (intended).
- Bridges added after continuity check: Vegas wedding ("How old are you?"… "I do") and "Nothing further. Mr. Hale."
  Cut Vivian's unprompted product naming from restroom part 1 so the name lands once, in N4.
- Captions: `captions-v2.ass` (TikTok Sans 80, 3–4 words, cut-aware). Chunked Whisper + per-piece re-transcription
  for unpunctuated stretches; setup lines reused from the approved v1 captions.
- 2026-11-25 v2b: restored "Your honor, we're countersuing" (src 235.13–239.22) and "this is what we call a murder-for-profit
  scheme" (policy piece out 252.95 → 256.38). 5:37, sync +12.0 ms, 26 joins; captions merged and shifted +7.53 s after 4:35.
- 2026-11-25 v2c: offer card removed at the user's request (5:31, sync +17.3 ms).
- 2026-11-25 v2d: restored the Vegas craps flashback (src 55.93–81.17: March 14th Exhibit A, who are you / the house, keep the jet warm). 5:56, sync 0.0 ms.

# Don't Call Me Grandma (Christmas): fix log

Source: `MediSkiin_Xmas_v8_1080p_captioned.mp4` (Drive, 9:26, captions burned in). Plates and location refs are frames
from v8 (Evy 1:56, Noah 1:09.5 crop, Carol 6:12, couch 6:14, front door 3:46, hallway 2:06, bathroom 2:28); product = Vegas hero frame.
Decisions 2026-11-25: trial line stays (brand has the study); no offer card or offer lines; urgency line =
"made in small batches and sells out instantly"; "restocks are slow" removed.

| Clip | Request id | s | Cost | QC |
|---|---|---|---|---|
| X1 | 01a21118-7ad0-7be6-880e-016799d7a5c0 | 6 | $0.71 | PASS: both lines exact; Evy/Noah match v8; hallway matches |
| X2 | 01a2111b-5a18-79bd-80b2-2e7c04656511 | 5 | $0.59 | PASS: "Aunt Carol!" / "Merry Christmas, kiddo." Noah opens door, Carol with pie on snowy porch |
| X3 | 01a2111b-6261-7cd5-aa48-f4753c721ab7 | 6 | $0.71 | PASS: "How long did it take, sis?" / "Started in October. Eight weeks." Carol touches scarf |
| C1 | 01a2111b-75b3-7068-89f8-0c5aedb9f9d8 | 15 | $1.77 | PASS: all lines; brand heard "Medi Skin, two eyes" (MED-ee-skin rule works twice now) |
| C2 | 01a2111b-7c1d-742a-be2e-72c04bd59054 | 15 | $1.77 | PASS: all lines; Carol unwinds scarf on "This year, I'm in the picture" |

Generation total $5.55 (47 s), no re-rolls.

## 2026-11-25 upscale + assembly (v8b)
- SeedVR2 (fal, same settings as Vegas) on X1–C2: 47 s ≈ $2.30. Dropped tail frames padded with the last frame (tpad clone) so no audio is trimmed.
- New-clip captions matched to v8's burned-in style: TikTok Sans 110, bottom edge y=1400 (`clips/edit/cap_*.ass`).
- `edit.json`: cold open (24.25–40.62) → "TEN MINUTES EARLIER" → 0–24.25 → … → LAST CHRISTMAS overlay (131.2) → X1 → … → X2 →
  … → cut "signal and fuel" (352.12–361.35) → cut "crew / power" (424.08–428.12) → X3 → cut stranger inserts (460.42–470.17)
  → old close cut at 527.80 → C1 → C2. Result 9:13, sync +9.7 ms, 14 joins clean by transcript, speech spread 0.0 dB.
- Known leftover: the existing 7:08 line still says "Metiskeine" (old footage); the new close says it right and spells it.

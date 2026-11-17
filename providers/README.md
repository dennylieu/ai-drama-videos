# Providers

Fill in one row per provider we have credits on. Settings are checked against each provider's live docs before use.

| Provider | Seedance 2.5 model id | SeedVR2 model id | Audio from Seedance? | Ref images? | Price 10 s @ 480p | Price upscale | Key env var |
|---|---|---|---|---|---|---|---|
| _tbd_ | | | | | | | |

Pipeline contract every adapter follows:
1. `generate(prompt, duration, aspect="9:16", resolution="480p", audio=True, refs=[])` -> saves `clips/raw/<id>.mp4`,
   logs job id + cost to `log.md`.
2. `upscale(raw.mp4, target_height=1920)` -> `clips/up/<id>.mp4`, then `tools/remux_audio.sh` restores audio.

# Sources

- **Harris Drama Skill** (Seedance 2.5 on Higgsfield, Nov 2026). Used for: format, film grammar, scene engines,
  casting, dialogue limits, prompt structure, QC pass marks. Its 1080p "finalize" step is replaced by SeedVR2.
- **Reality Drama Engine** (Gemini Omni Flash 1.1 on Starpop, Nov 2026). Used for: `tools/assemble.py`,
  `captions.py`, `wordcheck.py`, `fw_transcribe.py`, `plate_check.py`, plates-first discipline, prompt fixes.
  Not used: its one-speaker-per-clip structure (Seedance does whole multi-speaker scenes in one pass), Starpop
  calls, folder conventions, upsell steps.
- Starpop's own skills (`starpop-foundations`) need a Starpop login through its MCP and were not read.

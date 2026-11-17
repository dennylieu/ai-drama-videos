---
name: ad-teardown
description: Frame-by-frame teardown of a competitor's winning video ad plus a copywriting analysis, turned into a swipe brief that the drama-ad skill produces as an equally strong ad for our product. Use when the user shares a reference, competitor, winning or "swipe" ad, asks why an ad works, asks to break down, analyse, reverse-engineer or copy the structure of an ad, or wants "an ad just as good as this one".
---

# Ad Teardown -> Swipe Brief

Three layers, in order: **measure** (script), **see** (look at every frame yourself), **read the copy** (the copy
analysis prompt). Then map what made it win onto our product, inside Seedance's limits, and hand the brief to
`drama-ad`.

Copy the **structure and the persuasion mechanics**, never the surface: no lines word for word, no look-alike actors,
no brand names, music, logos or on-screen designs, no claims our product cannot back up.

## 1. Get the file
The user uploads the video (best), or gives a file path. Ad-library pages (Meta, TikTok) usually need a browser
login and are blocked from this environment: ask for the downloaded .mp4 instead of trying to scrape them.
Save it as `ads/<CODE>-<slug>/refs/<ref-name>.mp4`. Note where it came from and how long it has been running (a
long run time is the best evidence it is a winner).

## 2. Measure (free, local)
```bash
python3 -I -B tools/teardown.py ads/<CODE>-<slug>/refs/<ref>.mp4 ads/<CODE>-<slug>/refs/<ref>/ --language en
```
Gives: shot list with cut times, 3 frames per shot, contact sheets with timestamps, word-timed transcript, pauses,
loudness, and a pre-filled `teardown.md` table. If cuts look missed (a cut you can see on the sheet but not in the
list), run again with `--threshold 0.2`; if fades or handheld motion make false cuts, `0.4`.

## 3. See: frame-by-frame read
Open every contact sheet and every shot's frames (Read the .jpg files). Fill each row of `teardown.md`:

- **Framing / subject:** shot size (ECU, CU, MCU, MS, wide), who, where they sit in frame, eyeline direction.
- **Action / performance:** what visibly happens; the micro-expression (name the muscles: "upper lip curls").
- **On-screen text:** exact words, position, size, how long it stays, style (box, plain, karaoke captions).
- **Sound:** dialogue, VO, music (type, level under voice), SFX, room tone; does sound lead picture on the cut?
- **Job in the ad:** hook, pattern interrupt, problem, agitation, proof, reveal, mechanism, objection, offer, CTA.

Then write a **Visual summary** under the table:
- Hook in the first 1.5 s: what stops the thumb (picture alone, on mute) and what the first spoken words do.
- Pacing: shots per 10 s, average and longest shot, where the one long hold is, where the silence is.
- Look: camera (locked, handheld, selfie), lens feel, light source, palette, texture (phone UGC vs film).
- Casting: who the viewer is meant to be, who delivers the verdict, how "real" they look.
- Product: first appearance time, how it is shown, how long, with what words.
- Text and captions: how much of the story works on mute.

## 4. Read the copy
Run the analysis in `copy-analysis-prompt.md` over the transcript + on-screen text + visual summary. Write the answer
into `ads/<CODE>-<slug>/refs/<ref>/analysis.md`.

## 5. Swipe brief
Write `ads/<CODE>-<slug>/swipe-brief.md`:

1. **Why it wins, in one sentence** (the mechanism, not the topic).
2. **Keep** (structure to copy): beat order with timings, hook type, who delivers the verdict, where the silence and
   the reversal land, product reveal timing, CTA style, mute-readability.
3. **Change** (what is theirs): every line, face, place, brand, prop and on-screen design gets our own version.
4. **Fit to Seedance** (`drama-ad` limits): one location per generation; 10 s = 2-3 lines / 6-14 words, 15 s =
   7-8 lines / 32-40 words; a longer reference is split into 10-15 s segments with cast plates for continuity; text
   overlays, captions, end card and any montage of product shots are built in the edit, not by Seedance.
5. **Mapping table:** Reference beat | time | job | our beat | our line or picture | Seedance segment.
6. **3+ hook options** in the same hook type (opening insert, lines, final look), one recommended.
7. **Claims check:** every claim we keep is one our product can make; none of the "never claim" list.

Show the teardown summary and the swipe brief together. **Wait for approval**, then continue with `drama-ad` from
step 3 (cast) using the brief as the script source.

## 6. After the ad is made
Compare our final against the reference on the same measures: rerun `tools/teardown.py` on our final and put the two
summaries side by side (shot count, first-cut time, hook words, words per minute, product reveal time). Report any
beat that drifted by more than about 0.5 s.

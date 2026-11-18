---
name: song-vsl
description: Long-form drama "song VSL" (3-10 min, 9:16) in the Ryze/Resilia style - a direct-response advertorial (research, fear, drama the problem causes, believable mechanism, proof, close) told as a sung hero's-journey story, the product arriving after the halfway mark through a trusted messenger, the chorus carrying the mechanism. Covers the voice-of-customer doc, fear pick, 10-beat skeleton, story beat sheet, mechanism checklist, lyrics, song generation, one Seedance scene per beat, and assembly with the song as the voice. Use when the user asks for a song ad, sung ad, music VSL, Ryze- or Resilia-style ad, long-form story VSL or advertorial, hero's-journey ad, revenge/betrayal transformation story, or a 3+ minute drama ad.
---

# Song VSL

Two layers, built in this order:
1. **The ad underneath** (direct response): Zakaria, "Song Ads Are The New Trend. Most Of You Will Fail At Them,
   Because You Think The Song Is What Sells" (X article, Nov 2026), a breakdown of an 8:30 Resilia song ad.
   Full notes: `reference/foundation.md`.
2. **The story on top** (the drama): Ori Silver, "Inside Ryze's $22M Song Ads" (X article, Sep 2026).
   Full notes: `reference/blueprint.md`.
Templates for every step: `reference/templates.md`.

**The song is not what sells.** It holds attention line to line (rhythm), the visuals change every second, and that
buys the time a VSL or advertorial needs. The selling is the same as always: drama that stops the scroll, a mechanism
that makes them believe, a story that carries both. Miss the drama, nobody watches. Miss the mechanism, nobody buys.
Miss the story, nobody finishes. A great song on a weak ad gets a great hook rate, great watch time and zero sales.

## The rules that matter most
1. **Research first, by hand.** Collect the avatar's exact words in six buckets (`templates.md`). That doc is the ad;
   you arrange it, you don't invent it.
2. **Pick the fear, then the scene.** One primal fear (rejection, betrayal, humiliation, losing your place, losing
   your partner, failing your kids, a health scare, losing your money) that fits the avatar's age and gender.
3. **The problem (or the result) causes the drama.** Random drama gets views, not sales. Resilia: the family turned
   on her *because* she lost the weight.
4. **The hook is the loop that runs the whole ad.** It opens a question that only the payoff, minutes later, closes.
5. **Betrayal from the closest person; pain that keeps getting worse; the hero freezes.** (Ryze)
6. **A believable messenger before the product.** Close family for a common problem; where they'd naturally meet
   someone with it (support group, clinic waiting room, salon chair) for a rare one.
7. **The mechanism passes the believability checklist** and is simple enough to explain back after one listen.
8. **~78 % emotion, ~22 % selling** (mechanism, product, proof, offer). Emotion makes them want it; the mechanism
   makes them believe it. Both, or nothing.
9. **Proof in the mechanism's order, and honest** ("week one, nothing. I almost quit.").
10. **Payoff closes the hook's loop and flips its lines.** The outcome is the cake; revenge is the cherry.
11. **The close makes her story the viewer's story,** then the offer; the guarantee answers the top objection.
12. **The song comes last.** Chorus carries the mechanism, style fits the avatar, every word clear on first listen.

## How it differs from `drama-ad`
Same production stack (Seedance 2.5 at 480p -> SeedVR2 -> `tools/assemble.py`), different storytelling:
- The **song carries the story**; scenes are mostly picture with room sound under the song. No spoken dialogue in
  most scenes (it fights the vocal); a few short sung lip-sync shots of the narrator are optional.
- **Every lyric line gets its own visual.** The mechanism gets the most important one: one picture a 10-year-old
  gets (the wall, the storm, the enemy), as a live-action practical insert or a simple graphic added in the edit.
- The hero **does** speak to the viewer at the end (the close). That is the one pitch, about the last minute.
- Pain lines about the hero come from **other characters** (quoted in the lyrics), never self-description.
- Every `drama-ad` scene rule still applies per generation: one location, one moment, 2-4 locked characters, plates,
  motivated light, plain faces, no product/captions/brand text rendered by Seedance.

## Workflow

### 1. Brief (one message)
Product, what it visibly changes, offer and guarantee, 3 things it must never claim, the true mechanism the brand
can back, language/accent, target length (short test 3-4 min or full 7-10 min), real product photos. Read
`brands/<brand>/context.md` and research first.

### 2. Voice-of-customer doc (`brands/<brand>/research/voc-<topic>.md`)
Where the avatar vents: Reddit, Facebook groups, competitors' 1-3 star reviews, TikTok/YouTube comments, surveys.
Read for **words, not ideas**; copy word for word into the six buckets (`templates.md`): problem in their words,
fears, what they tried and why they think it failed, what they believe causes it, the life they want, what stops
them buying. Aim for 30+ verbatim lines. Reuse `creative-strategy` research if it exists; web access here is
limited, so ask the user for exports or pasted threads rather than guessing. Never invent quotes.
Optional but strong: map one winning long ad in the niche (running 30+ days) to the 10 beats with `ad-teardown`.

### 3. Fear, hook scene, sub-avatar (`ads/<code>/brief.md`)
- Pick the fear that shows up most in the doc and fits age/gender (starting points in `foundation.md`).
- Write **10 hooks** from it where the problem (or the result) causes the drama. Each: the line, the loop it opens,
  how it closes at the end. Test: does an avatar viewer qualify herself in the first second?
- Fill the sub-avatar card. Offer the top 3 hook + sub-avatar pairs, recommend one. **Wait for approval.**

### 4. Skeleton, then story
**a. 10 beats in 10 lines** (`templates.md`): hook, avatar, problem, everything tried, messenger, mechanism,
product, proof, payoff, close. One or two lines each. If it doesn't work in 10 lines, it won't work in 10 minutes.

**b. Mechanism** (`foundation.md` checklist): start from what they already believe ("it's stress", "it's my age"),
name the hidden cause, explain why everything they tried failed, name an enemy that is never them, one visual
metaphor, one ingredient one job with real doses and routine, proof in the same order, explained by a believable
person. Write it out in plain words and say "read this to someone who doesn't know the product; can they explain it
back?" It must be true and inside the brand's claims list.

**c. Story beat sheet:** dress the 10 beats in the Ryze fall-and-rise (12 story beats in `templates.md`), with one
concrete event per beat. Checks:
- The hook drama sits in the first 10 seconds, comes from the closest person, and is caused by the problem/result.
- Bad becomes worse right away; the hero freezes instead of fighting.
- Problem beat stacks symptoms in the avatar's own words (a repeated line start like "Tired of..." doubles as a lyric).
- Failed solutions are the ones in the research doc, dismissed fast; it was never the hero's fault.
- Messenger before product; product after the halfway mark, from the messenger's hands; the hero doubts it.
- Proof: 3-4 small results week by week, in the mechanism's order, noticed by others, one honest setback.
- Payoff is the longest part, closes the opening loop, flips the opening insults, same place and people.
- Selling (mechanism + product + proof + offer) is ~20-25 % of the runtime; time the beats to check.
Show skeleton + mechanism + beat sheet + cast. **Wait for approval.**

### 5. Script, then lyrics (`ads/<code>/script.md`)
Write the full script as prose first (it would work as a native ad). Then adapt, don't cut, into lyrics:
- Verses tell the story; **the chorus carries the mechanism** (why nothing worked, what finally did). It repeats,
  so by the third time they're singing it back. A chorus about how sad she was is wasted.
- Keep the details; they make it real. Verses should sound like a real person talking.
- Line 1 is the hook, sung plainly, no intro longer than 2 s. Insults are quoted from other characters.
- Close (last ~60 s, spoken or half-sung to camera): call out the viewer with 2-3 details from the research
  ("so if you're the one who..."), not your fault, the mechanism in one line, the offer, the guarantee as the answer
  to the top objection.
- Claims: what another person could see, plus the brand-approved mechanism; no disease words, no "cured", no
  numbers the brand can't back. Check `context.md`.
- Pick the style for the avatar (age, culture, region, the emotion of each part), not for taste.
Count ~130-150 sung words per minute. Then review it yourself line by line for the boring mechanism, the line that
doesn't follow, the messenger nobody would believe; don't just ask whether it's good. **Wait for approval.**

### 6. Generate the song
Use whichever music provider has credits (record it in `providers/README.md`). Give it the lyrics with section tags,
style, tempo, vocalist matching the hero, and "clear lead vocal, every word intelligible, sparse mix". Make 2-3
versions per section and judge on two things only: is every word clear on first listen, do the verses sound like a
person talking. Pretty but unclear loses. If the model caps length, generate per section with the same style/seed
and join on bar lines. Check: `python3 -I -B tools/fw_transcribe.py music/song.mp3 music/song/` then
`python3 tools/wordcheck.py --script-file lyrics.txt <transcript>` (sung words transcribe worse than speech; judge
the key lines: hook, chorus/mechanism, product name, offer). Save to `ads/<code>/music/`, log provider + cost.
The user listens and approves; you can't hear it.

### 7. Scene list and plates
Cut the approved song into scenes on its timing: one visual per lyric line, one Seedance generation per moment
(10 or 15 s, several lines each, cut inside the edit), so a 7-minute song is ~30-40 generations. Each row: time
range, beat, lyric lines, location, characters, action, emotion on the paused frame. Mark the mechanism-metaphor
shots. Show the total price estimate before spending.
Plates are mandatory: one approved still per character (hero before AND after, partner, betrayer, messenger,
witnesses) and the product from real photos; `plates.json` + `tools/plate_check.py`. Describe the hero's body
exactly for each week of the climb so the change is gradual.

### 8. Generate, QC, upscale
Follow `drama-ad` steps 4-7 per scene: prompt template from `drama-ad/reference/prompts.md`, with "no speaking,
ambient room sound only" unless it is a lip-sync shot. Generate the hook scene, the mechanism metaphor and one climb
scene first, QC, then the rest. Faces and wardrobe must match the plates on every return.

### 9. Assemble
`edit.json` with the song as one `vo` block over all scenes, clip sound low (`"clip_sound_db": -24`), product
inserts, mechanism graphics and the end card as `image` pieces; the close can be its own clip with its own speech.
Cut on bar lines and lyric events (the insult lands on the speaker's face, the chorus on the metaphor).
`python3 tools/assemble.py edit.json`; deliver only on `PASS`.

### 10. Captions and deliver
Lyric captions by default (muted viewers): transcribe the FINAL file, `tools/captions.py --script` with the lyrics
and a `--glossary` for brand and ingredient names. Deliver clean + captioned. Report provider and cost per
generation, re-rolls and why, honest remaining flaws, and the timed emotion/selling split.
The same script also works as a native ad or a UGC talking-head ad; offer those if the user wants more formats.

## Rules
- Never generate before the user approved hook/sub-avatar, skeleton + mechanism + beat sheet, and lyrics.
  "Make the ad" is not a yes to spend.
- The mechanism must be true and backed by the brand; no invented studies, doses, ingredients or results.
- The messenger gets credibility from visible life and experience. Never present an AI character as a real, named
  doctor or professional, and don't put medical claims in a white coat; check the ad platform's rules on health
  claims and AI people.
- Copy structure only: never Ryze's or Resilia's lyrics, songs, melodies, characters, mechanism or brand.
- Infidelity and humiliation are fine; keep it non-sexual, no nudity, no real people.
- Wins, losses and which fear/mechanism worked go to `brands/<brand>/learnings.md` (creative-strategy weekly loop).

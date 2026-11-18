---
name: song-vsl
description: Long-form drama "song VSL" (3-10 min, 9:16) in the Ryze style - one person sings the worst chapter of their life, a hero's-journey fall and rise, the product only arrives after the halfway mark through a trusted mentor, and the pitch sits in the last minute. Covers the sub-avatar card, beat sheet, lyrics, song generation, one Seedance scene per beat, and assembly with the song as the voice. Use when the user asks for a song ad, sung ad, music VSL, Ryze-style ad, long-form story VSL, hero's-journey ad, revenge/betrayal transformation story, or a 3+ minute drama ad.
---

# Song VSL (Ryze blueprint)

Source: Ori Silver, "Inside Ryze's $22M Song Ads: The Blueprint Behind Their Winning VSLs" (X article, Sep 2026),
a breakdown of Ryze's winning Meta song ads. Full breakdown, characters and examples: `reference/blueprint.md`.
Templates: `reference/templates.md`.

A video sales letter that is **sung instead of read**. It sells the hero's emotional experience (life without the
product, life once it fixes things), not the mechanism. Anyone still watching at minute five is the buyer, so length
is a filter, not a flaw.

## The seven things that matter most
1. **Sub-avatar first.** One specific person and the fear they keep to themselves decides every character, wound and
   setting. New sub-avatar = new song, not a re-skin.
2. **Emotional stakes, never logic.** The body symptom matters only for what it costs in love and respect.
3. **Betrayal from the closest person** (partner, best friend, sister). It makes the viewer ask "is this happening to
   me?" A stranger's betrayal can be written off.
4. **Pain that keeps getting worse.** Bad, then worse, then rock bottom.
5. **Mentor before product.** Someone close, credible, the finished version of the hero.
6. **Doubt, then the climb.** The hero doubts it, then gets small results other people notice.
7. **Vindication that reverses the opening insult**, same place, same people. Pitch at the emotional peak.

## How it differs from `drama-ad`
Same production stack (Seedance 2.5 at 480p -> SeedVR2 -> `tools/assemble.py`), different storytelling:
- The **song carries the story**; scenes are mostly picture with room sound under the song. No spoken dialogue in
  most scenes (it fights the vocal); a few short sung lip-sync shots of the narrator are optional.
- The hero **does** speak to the viewer at the end ("return with the elixir"). That is the one pitch, last ~60 s.
- Pain lines about the hero come from **other characters** (quoted in the lyrics), never self-description.
- Every `drama-ad` scene rule still applies per generation: one location, one moment, 2-4 locked characters, plates,
  motivated light, plain faces, no product/captions/brand text rendered by Seedance.

## Workflow

### 1. Brief (one message)
Product, what it visibly changes, offer, 3 things it must never claim, language/accent and singing style
(country, soul, R&B, pop ballad, gospel...), target length (short test 3-4 min or full 7-10 min), real product
photos. Read `brands/<brand>/context.md` and research first; pick sub-avatars from there.

### 2. Sub-avatar card (`ads/<code>/brief.md`)
Fill the card in `reference/templates.md`: age, background, relationship, the exact body detail, the private fear,
where their social life happens (cookout, school play, church, office party), what they already tried. Offer 2-3
sub-avatars, recommend one. **Wait for approval.**

### 3. Story: pick the shape and fill the beat sheet
Shape: **revenge** (male or female), **reconciliation**, or another reversal that fits the sub-avatar. Fill the
12-beat sheet (`reference/templates.md`) with one concrete event per beat. Checks before showing it:
- Beat 2 humiliation is in the first 10 seconds, and comes from the closest person possible.
- Beat 3 is worse than beat 2 and the viewer didn't see it coming.
- Hero freezes (beat 4) instead of fighting.
- Failed solutions (beat 6) list what THIS audience believes works (from research), including advice from friends,
  and a dismisser ("it's just age"). The mentor never gives failed advice.
- Product appears **after the halfway mark**, only from the mentor's hands.
- The climb has 3-4 week-by-week results, each noticed by another person, each answering a piece of the insult.
- Vindication is the exact reversal of the opening insult, in the same place with the same witnesses.
- A convert (cousin, friend) asks for it / orders on the spot.
Show the beat sheet + cast list. **Wait for approval.**

### 4. Lyrics (`ads/<code>/script.md`)
First person, past tense in the fall, present tense in the climb. Map beats to song sections (map in
`reference/templates.md`). Rules:
- Line 1 is the humiliation, sung plainly, no intro longer than 2 s.
- Insults are quoted dialogue from other characters ("She said I look sixty").
- Concrete nouns over feelings: the thirty pounds, the gray in the beard, the four hours of smiling.
- Chorus = the wound in the fall, then the same chorus melody with reversed words after vindication.
- Name the product only in the gift beat and the pitch; mechanism gets one or two lines at most, in plain words.
- Claims are what another person could see (lighter, energy, "what did you do?"). No disease words, no "cured",
  no medical promises, no numbers the brand can't back. Check `context.md` claims list.
- Pitch (last ~60 s): spoken or half-sung, hero to camera: what it is, why the viewer is like them, the offer, CTA.
Count words: ~130-150 sung words per minute of song. **Wait for approval of the lyrics.**

### 5. Generate the song
Use whichever music provider has credits (record it in `providers/README.md`). Give it the lyrics with section tags,
style, tempo, vocalist (age/gender matching the hero), and "clear lead vocal, lyrics intelligible, sparse mix".
If the model caps length, generate per section with the same style/seed and join on bar lines. Then:
`python3 -I -B tools/fw_transcribe.py music/song.mp3 music/song/` then
`python3 tools/wordcheck.py --script-file lyrics.txt <transcript>`: every line present and intelligible (sung words
transcribe worse than speech; judge the key lines). A buried or wrong key line (insult, product name, offer) = regenerate that section. Save to
`ads/<code>/music/` and log provider + cost. The user listens and approves; you can't hear it.

### 6. Scene list and plates
Cut the approved song into scenes on its timing: one Seedance generation per beat moment (10 or 15 s), 1-3 per
beat; a 7-minute song is ~30-40 generations. Write the list with: time range, beat, location, characters, action,
emotion on the paused frame. Show the total price estimate before spending.
Plates are mandatory: one approved still per character (hero before AND after body, partner, betrayer, mentor,
witnesses) and the product from real photos; track in `plates.json`, run `tools/plate_check.py`. The hero's body
change must be gradual across the climb (describe each week's body exactly).

### 7. Generate, QC, upscale
Follow `drama-ad` steps 4-7 per scene: prompt template from `drama-ad/reference/prompts.md`, but with no dialogue
lines ("no speaking, ambient room sound only" in the prompt) unless it is a lip-sync shot. Generate the hook scene
and one climb scene first, QC, then the rest. Faces and wardrobe must match the plates on every return.

### 8. Assemble
`edit.json` with the song as one `vo` block over all scenes, clip sound low (`"clip_sound_db": -24`), product
inserts and the end card as `image` pieces; the pitch scene can be its own clip with its own speech. Cut on the
song's bar lines and on lyric events (the insult line lands on the partner's face). `python3 tools/assemble.py
edit.json` and deliver only on `PASS`.

### 9. Captions and deliver
Lyric captions are the default for this format (most viewers are muted at first): transcribe the FINAL file,
`tools/captions.py --script` with the lyrics and a `--glossary` for the brand name. Deliver clean + captioned, plus a
short cut (first 60-90 s hook + pitch) only if the user asks. Report provider and cost per generation, re-rolls and
why, honest remaining flaws.

## Rules
- Never generate before the user approved sub-avatar, beat sheet and lyrics. "Make the ad" is not a yes to spend.
- The mentor gets credibility from their visible life and experience (fit, successful, clearly runs a business).
  Never present an AI character as a real, named doctor or professional, and don't put medical claims in a white
  coat; check the ad platform's rules on health claims and AI people.
- Never copy Ryze's lyrics, songs, melodies, characters or brand; copy the structure only.
- Infidelity and humiliation are fine; keep it non-sexual, no nudity, no real people.
- New sub-avatar wins and losses go to `brands/<brand>/learnings.md` (creative-strategy weekly loop).

---
name: song-vsl
description: Long-form drama "song VSL" (3-10 min, 9:16) in the Ryze/Resilia style - a direct-response advertorial (premises, market/segment/avatar, the 4 sales and 17-element brief, fear, drama the problem causes, three-part mechanism with conditions and USP, proof, anchored close) told as a sung hero's-journey story, the product arriving after the halfway mark through a trusted messenger, the chorus carrying the mechanism. Detailed step-by-step from premises to delivered file - voice-of-customer doc, fear pick, hooks, 10-beat skeleton, mechanism, 17-element brief, story beat sheet, script, lyrics, song generation, one Seedance scene per beat, assembly with the song as the voice, captions. Use when the user asks for a song ad, sung ad, music VSL, Ryze- or Resilia-style ad, long-form story VSL or advertorial, hero's-journey ad, revenge/betrayal transformation story, or a 3+ minute drama ad.
---

# Song VSL

Built from three articles, used in this order (full notes in `reference/`):
1. **The brief** - Derick Carneiro, "how I write ads that make strangers buy" (X, Nov 2026): 4 sales, 17 elements,
   premises -> target -> brief -> writing. `reference/four-sales.md`
2. **The ad underneath** - Zakaria, "Song Ads Are The New Trend. Most Of You Will Fail At Them..." (X, Nov 2026):
   research by hand, the fear, drama the problem causes, 10 beats, the mechanism checklist, the song last.
   `reference/foundation.md`
3. **The story on top** - Ori Silver, "Inside Ryze's $22M Song Ads" (X, Sep 2026): sub-avatar, hero's-journey fall
   and rise, closest-person betrayal, mentor before product, vindication. `reference/blueprint.md`
Fill-in templates for every step: `reference/templates.md`. **Steps 1-9 are written up as one copy breakdown in
Derick Carneiro's format: `templates/copy-breakdown.md` -> `ads/<code>/brief.md`** (premises, target, mechanism,
content, offer, close, each question answered then "It would go like this:", then the mini-blocks). Worked example:
`ads/KB1-kolabloom-song/brief.md`.
Worked teardown of a live winner (Lymphoria, 8:27, night-shift nurse, lymphatic drops) with its block timings:
`ads/KB1-kolabloom-song/refs/ref1/analysis.md`.

**The song is not what sells.** It holds attention line to line and the visuals change every second; that buys the
minutes a VSL needs. Before the product the ad makes four sales: **content** (watch to the end), **hope** (it can be
solved; here's why it wasn't), **value** (this product is where to get it), **impulse** (now is safer than later).
Miss the drama, nobody watches. Miss the mechanism, nobody buys. Miss the story, nobody finishes.

## The map

| Phase | Step | Output | Gate |
|---|---|---|---|
| A. Know | 1 Premises | `brands/<b>/context.md`, premises sheet in `ads/<code>/brief.md` | - |
| | 2 Target: market -> segment -> avatar | avatar card in `brief.md` | - |
| | 3 Research (VOC + behaviour + winners) | `brands/<b>/research/voc-<topic>.md` | - |
| B. Brief | 4 Fear and 10 hooks | hook list in `brief.md` | **User picks hook + sub-avatar** |
| | 5 10-beat skeleton | top of `script.md` | - |
| | 6 Mechanism (hope sale) | mechanism check in `brief.md` | - |
| | 7 Offer and close (value + impulse sales) | rows 11-17 of the brief | - |
| | 8 Content (topic, format, concept, hooks) | rows 1-5 of the brief | - |
| | 9 Story beat sheet + cast | beat sheet in `script.md` | **User approves brief + beats + cast** |
| C. Write | 10 Script in prose | `script.md` | - |
| | 11 Lyrics | `script.md` + `lyrics.txt` | - |
| | 12 Self-review | review notes | **User approves lyrics** |
| D. Make | 13 Song | `music/song.mp3` | **User approves the song (by ear)** |
| | 14 Scene list + price | `scenes.md` | **User approves spend** |
| | 15 Plates | `stills/`, `plates.json` | **User approves plates** |
| | 16 Generate -> QC -> upscale | `clips/raw/`, `clips/up/`, `log.md` | test scenes first |
| | 17 Assemble | `edit.json`, `final/` | `PASS` only |
| | 18 Captions + deliver | `final/*_cap.mp4` | - |
| | 19 Learn | `brands/<b>/learnings.md` | after results |

Keep a status line at the top of `ads/<code>/log.md` ("Step 9 waiting for approval") so a later session can resume.

---

## Phase A - Know (premises, target, research)

### Step 1. Premises: what we already know
We never start from zero. Facts about the brand and product, usually all on the product page (PDP).
1. Ask the user once, in one message, for whatever isn't on the page: product link, what it visibly changes, offer,
   guarantee, 3 things it must never claim, the true mechanism the brand can back, language/accent, target length
   (test 3-4 min or full 7-10 min), real product photos, any winning ads (theirs or competitors').
2. Read `brands/<brand>/context.md` if it exists (create it from `templates/product-context.md` if not).
3. Fill the **premises sheet** (`templates.md`), eight items, facts only:
   1. Brand name. 2. Product name. 3. Ingredients and doses per serving. 4. Attributes: testing, where it's made,
   servings, daily routine, how long until results (the brand's own words), sensations/side effects and warnings
   the page states. 5. Price per bundle (and subscription terms). 6. Guarantee (length, terms; refund rate only if
   the brand publishes it). 7. What they gain by buying now (free units, shipping). 8. What they lose by waiting
   (only a real deadline or real stock).
4. **Check:** every line traces to the page or the user. Anything unknown is written as MISSING, never guessed.

### Step 2. Target: market -> segment -> avatar
If you talk to everyone, you talk to no one. Three questions:

**Q1. Which markets can this product go after?** A market = people of any kind who share one desire. List every
market the ingredients/category allow, then pick ONE:
- Brand already running: the market its highest-traffic landers and most-run ads target (ask the user, or pull the
  last 60 days of their ads if an ads tool is connected).
- New product: per candidate market, find 3+ competitors (fewer than 3 = cut it), compare their traffic growth over
  the last 30 days, pick the biggest grower; a near-tie doesn't matter, pick either.
- Rule: low-leverage stage, so minimise risk. Don't gamble on a new market.

**Q2. Which segment of that market?** A segment = a cluster sharing the desire plus a condition, identity or
behaviour (postpartum women losing weight; diabetic men with the same problem). Either copy the segment the
brand's or competitors' winners target (default), or find an unserved one by reading Reddit for hours.

**Q3. Who is the avatar?** Fill the avatar card (`templates.md`) in two layers:
- Psychographics: primary desire, the problem, secondary desires, pain points (how it shows up in their life),
  dreams (life without it), fears (if it never gets solved).
- Identity: demographics (sex, age range, nationality, language, ethnicity, religion, marital status, family role);
  behaviour (competitor ads that grab them, videos they watch, trending topics, hobbies, news, shows, other health
  conditions); perspective (beliefs, biases, enemies, allies, language).

**Check:** one market, one segment, one avatar, each with the reason it was chosen.

### Step 3. Research: words, behaviour, winners
Three sources, in this order of value:
1. **Winners in the segment** (cheapest psychographics; they don't change much over the years). Winning ads (30+
   days running), advertorials, old VSLs in the same market. Map one long winner to the 10 beats with `ad-teardown`
   (it also becomes the writing reference in step 10). Ask the user for the .mp4s; ad libraries are often blocked
   here.
2. **Voice of customer, by hand.** Where they vent: Reddit, Facebook groups, competitors' 1-3 star reviews,
   TikTok/YouTube comments, surveys. Read for **words, not ideas**. Copy word for word into the six buckets
   (`templates.md`): (1) the problem in their words ("I wake up stiff like I'm 90", not "joint discomfort"),
   (2) their fears, (3) what they tried and why they think it failed, (4) what they believe causes it, (5) the life
   they want, (6) what stops them buying. Target: read 50 posts, keep 30+ lines, each with its source.
3. **Behaviour now** (where your own hours pay most): news, trends, searches ("can you take X with Y?") and videos
   the avatar is into right now. This is where topics, formats and hooks come from.
- Reuse `creative-strategy` research if it exists. Never invent a quote; if access is blocked, ask the user to
  paste threads or export reviews.
- Finish with a **fear count**: tag each line in bucket 2 with a primal fear and count them.

**Check:** 30+ verbatim lines with sources; the fear count; at least 3 behaviour/topic leads.

---

## Phase B - Brief (fear, hooks, skeleton, the 17 elements, story)

### Step 4. Pick the fear, write 10 hooks
1. **Pick the fear** that appears most in the fear count AND fits the avatar's age and gender (table in
   `foundation.md`): rejection, betrayal, humiliation, losing your place, losing your partner, failing your kids,
   a health scare, losing your money.
2. **Find the scene where the problem (or the result) causes that fear.** Test: if you remove the problem, does the
   drama disappear? If not, it's random drama (views, no sales). Menopause example in `foundation.md`.
3. **Write 10 hooks** in the hook list (`templates.md`). For each: the first sung line, the fear, how the problem
   causes it, the loop it opens, how that loop closes at the end. A strong hook has: the result or the problem in
   the first second (the viewer qualifies herself), a twist, and a drama word ("turned on me").
4. Also try a proven hook structure from winners in the niche, filled with the avatar's slang.
5. Pair each of the top 3 hooks with a sub-avatar card (Ryze: the specific person and private fear that decides
   every character, wound and setting).
6. **Gate:** show the 3 pairs, recommend one with the reason. **Wait for the user's pick.**

### Step 5. Lay out the 10 beats in 10 lines
Fill the skeleton (`templates.md`), one or two lines each: hook, avatar, problem, everything tried, messenger,
mechanism, product, proof, payoff, close. If it doesn't work in 10 lines, it won't work in 10 minutes.
**Check:** a stranger reading the 10 lines can tell what happens, why it happens, and why the product fixes it.

### Step 6. The mechanism (the hope sale, elements 6-11)
Pick, at each step, the version the avatar is **most predisposed to accept**: connect dots they already have.
1. **Point of contact (7):** what do they already suspect causes it? (VOC bucket 4; what winners in the segment
   blame). Don't fight it; build on it.
2. **Problem mechanism (8):** the missing reason that proves their suspicion right; the hidden cause nobody told
   them. Name the enemy, and it is never them.
3. **Function mechanism (9):** the action that has to happen to fix it, and why what they already tried can't do
   it, ideally "wasn't made for someone like you" (feels specific to them). Every item in VOC bucket 3 must be
   explained, or they say "I tried that already".
4. **Solution mechanism (10):** the ingredient/compound that performs that action. One ingredient, one job.
5. **Conditions (11):** "Why can't I just get this myself?" (eat the food, buy the cheap capsule). Name what it needs
   to work: dose, form, absorption, tolerance.
6. **USP (12):** the product meets each condition, one by one, from the premises. No invented differentiator.
7. **Visual:** one picture a 10-year-old gets (a wall, a storm, a clogged pipe). It gets the most important shot.
8. **Messenger:** who explains it. Close family for a common problem; where she'd naturally meet someone with a rare
   one (support group, clinic waiting room, salon chair). Credible through visible life, never a fake real doctor.
9. **Identification (6):** the 2-3 VOC lines that make them think "this is about me" (used in beats 2-3).
10. Fill the mechanism check (`templates.md`), then write it in **3 plain sentences**.
**Check:** (a) every link is true and inside the brand's claims list; (b) it explains every failed attempt;
(c) "read this to someone who doesn't know the product: can they explain it back?" If not, simplify. The most
complete scientific explanation usually loses.

### Step 7. The offer and the close (value + impulse sales, elements 13-17)
1. **Features (13):** go through the ingredient list; keep only what answers one of four levers, say what it does
   for them (nobody buys "hawthorn"):
   - Odds: more ways to work = more chances it works this time.
   - Dream: what life feels like (energy, confidence), not the ingredient.
   - Effort: one a day, no new diet, nothing to stop.
   - Time: why it takes weeks, in a way that makes sense (years of damage, weeks to turn around). Never "first night".
2. **Anchoring (14):** price per day on the best bundle (do the maths) vs what the problem costs: money (every
   product that didn't work), emotion (partner, shame), time (it gets harder the longer it waits).
3. **Risk reversal (15), with a reason:** compare guarantee length to time-to-results ("120 days is almost twice
   what your body needs"). The only risk is doing the same thing and expecting a different result.
4. **Gain now (16):** bundle by bundle, what extra they take home; shipping.
5. **Lose by waiting (17):** only real deadlines and stock. If there is none, say so and leave it out.
6. **Top objection** (VOC bucket 6) is answered by the guarantee line.
**Check:** every number comes from the premises; the maths is shown in `brief.md`.

### Step 8. Content: topic, format, concept, hooks (elements 1-5)
1. **Topic (2):** the fact, news story, question or situation the avatar already cares about (from behaviour
   research). In a song VSL it's the fear + the situation of the chosen hook.
2. **Format (1):** a sung live-action drama in the chosen music style (style picked for the avatar's age, culture and
   region, not taste). Note which parts of the look/narrative are reused from validated winners.
3. **Characters and roles:** hero, partner, betrayer, witnesses, dismisser, messenger, convert (Ryze table in
   `blueprint.md`). The betrayal comes from the closest person possible.
4. **Concept (3):** characters + narrative + topic as one logline, then the angle that makes it impossible to leave.
5. **Copy hook (5):** the chosen hook line from step 4.
6. **Visual hook (4):** the opening frame: fits the format and concept, breaks expectation, readable on mute.
7. **Bets:** list what is new vs proven in this ad (song format, concept, look). Keep market, segment and mechanism
   proven; bet on story and song. Label the ad conservative / moderate / aggressive.
Now the **17-element brief** (`templates.md`) is complete.

### Step 9. Story beat sheet and cast
Dress the 10 beats in the Ryze fall-and-rise (12-row table in `templates.md`), one concrete event per row (who's
there, where, what happens), with approximate times. Check every item:
- [ ] Hook drama in the first 10 seconds, from the closest person, caused by the problem or result.
- [ ] Bad becomes worse right away (the viewer didn't see it coming); the hero **freezes** instead of fighting.
- [ ] "Seeing it too": the hero looks at their body and agrees with the insult.
- [ ] Problem beat stacks symptoms in VOC words with a repeated line start ("Tired of...").
- [ ] Failed solutions = VOC bucket 3, dismissed fast, partly from friends, plus a dismisser ("it's just age");
      never her fault; the messenger never gave bad advice.
- [ ] Messenger before product; product after the halfway mark, from the messenger's hands; the hero doubts it and
      comes round (voicing the viewer's doubt).
- [ ] Proof: 3-4 results week by week in the order the mechanism predicts, each noticed by another person, one
      honest setback ("week one, nothing").
- [ ] Payoff is the longest part: outcome first, then the loop closes in the same place with the same people, the
      opening insult flipped. A convert asks for it.
- [ ] Selling (mechanism + product + proof + offer) times out to ~20-25 % of the runtime; the rest is emotion.
- [ ] Every row of the 17-element brief has a beat.
Write the cast list: one locked sentence per character (`drama-ad` step 3 rules), the hero once per body stage.
**Gate:** show 10-beat skeleton + mechanism (3 sentences + check) + 17-element brief + beat sheet + cast.
**Wait for approval.**

---

## Phase C - Write (script, lyrics, review)

### Step 10. Script in prose
1. If you have a reference winner (step 3), transcribe it and split it into **mini-blocks** by job (hook, belief
   break, mechanism reveal, product, proof, offer...). The **brief decides what is said; the reference decides the
   order and rhythm.** Never copy its words.
2. Write the full script as prose, beat by beat, as if it were a native ad. Use VOC words verbatim wherever they fit.
3. Pain about the hero is said by other characters, quoted ("She said I look sixty").
4. **Check:** it would sell as a native ad on its own; every brief element appears.

### Step 11. Lyrics (adapt, don't cut)
1. Map beats to sections (`templates.md` section map): verse 1 hook + stacked conflict, pre-chorus freeze + symptom
   stack, chorus, verse 2 failed solutions, bridge messenger + mechanism + product + doubt, chorus, verse 3 proof,
   final chorus over the payoff, spoken/half-sung close.
2. **Chorus carries the mechanism** (why nothing worked, what finally did). First chorus hints, later choruses state
   it in full. By the third time they're singing it back. Alternative seen in a live winner (Lymphoria, see below):
   no classic chorus but a **motif line** that comes back with a new meaning each time ("she's always on nights"
   said by the betrayer -> "Relax, I'm on nights" at the payoff -> the final CTA), plus one mechanism restatement
   near the end ("It was never fat. It was never my age. It was waste.").
3. Verses keep the script's details and sound like a real person talking. Concrete nouns over feelings.
4. Line 1 = the hook, sung plainly, intro under 2 s. Option: a **cold open** on the payoff moment, unresolved
   ("I slapped my best friend at her own birthday party... let me tell you how I got there"); the loop closes when
   the story catches up to it.
5. Close (last ~60 s, to camera): "So if you're the one who..." with 2-3 VOC details; not your fault; mechanism in one
   line; price per day vs the cost of the problem; the offer; the guarantee with its reason; gain now; lose by
   waiting (if true); CTA.
6. Claims: what another person could see, plus the brand-approved mechanism. No disease words, no "cured", no
   numbers the brand can't back.
7. Length: plan at ~190-200 words per minute (the Lymphoria winner ran 197 wpm with music under it; a slower
   ballad is ~130-150). Count and write the total and the estimated runtime.
8. Save the lyrics with section tags to `ads/<code>/lyrics.txt` (one line per sung line).

### Step 12. Self-review (never ask a model "is this good?")
Go line by line and write the findings:
- Any line that doesn't follow from the one before? Any flat stretch with no new information or turn?
- Is the mechanism boring or too complex to repeat after one listen?
- Would the avatar believe the messenger is real and could plausibly have this?
- Does each claim pass the claims list? Any number not in the premises?
- Does the payoff flip the exact hook lines? Is the outcome there before the revenge?
- Re-time the emotion/selling split.
Fix what you find, then **Gate:** show the lyrics with the section map, word count, runtime and the review notes.
**Wait for approval.**

---

## Phase D - Make (song, scenes, generation, edit)

### Step 13. Generate the song
1. Use the music provider that has credits; record model and settings in `providers/README.md`.
2. Input: lyrics with section tags, style, tempo, vocalist matching the hero (age, gender, region), and "clear lead
   vocal, every word intelligible, sparse mix".
3. Make 2-3 versions per section. If the model caps length, generate per section with the same style/seed and join
   on bar lines.
4. Judge on two things only: every word clear on first listen; verses sound like a person talking. Pretty but unclear
   loses.
5. Check: `python3 -I -B tools/fw_transcribe.py ads/<code>/music/song.mp3 ads/<code>/music/tr` then
   `python3 -I -B tools/wordcheck.py --script-file ads/<code>/lyrics.txt ads/<code>/music/tr/song.json`.
   Sung words transcribe worse than speech; the key lines (hook, chorus, product name, offer) must pass. A wrong or
   buried key line = regenerate that section.
6. Save to `ads/<code>/music/`, log provider, settings and cost in `log.md`.
7. **Gate:** you can't hear it. The user listens and approves.

### Step 14. Scene list and price
1. From the approved song's timing (the transcript's word times), give **every lyric line its own visual**.
2. Group lines into Seedance generations: one location, one moment, 2-4 characters, 10 or 15 s each (cut inside in
   the edit). A 7-minute song is ~30-40 generations; a 3-4 minute test ~15-20.
3. One row per generation in `ads/<code>/scenes.md` (`templates.md` row): ID, time range, beat, lyric lines,
   location, characters, action, emotion on the paused frame, plates used, sound ("ambient only, no speaking" unless
   lip-sync), metaphor shot yes/no.
4. Mark the mechanism-metaphor shots (practical insert or a graphic made in the edit), product inserts (from real
   photos, added in the edit) and the close (hero to camera, its own speech clip or the song outro).
5. Price: generations x provider price at 480p + upscale per clip + song; show the total.
6. **Gate:** user approves the spend.

### Step 15. Plates
1. One still per character: hero at each body stage (before, week 2, week 4, after), partner, betrayer, messenger,
   witnesses, convert; the product only from real photos.
2. Describe the hero's body exactly for each stage so the change is gradual and believable.
3. Track in `plates.json`, run `python3 -I -B tools/plate_check.py ads/<code>/plates.json`.
4. **Gate:** user approves the plates.

### Step 16. Generate -> QC -> upscale (per scene)
1. Prompt per scene with `drama-ad/reference/prompts.md` (opener, look line, location, cast block word for word,
   numbered shots, held end frame, negatives), plus "no speaking, ambient room sound only" unless lip-sync. No
   product, captions or brand text inside Seedance.
2. **Test first:** the hook scene, one mechanism-metaphor scene and one climb scene. QC them (`drama-ad/reference/
   qc.md`: contact sheet, cut times, faces and wardrobe vs plates, emotion readable on a paused frame). Only then
   run the rest.
3. Save every raw result to `clips/raw/` immediately; log prompt, provider, job id, cost.
4. Fail = change only the sentences tied to the fault and re-roll. Two different rewrites failing the same way: stop
   and report.
5. Upscale approved clips with SeedVR2 to 1080x1920, then `tools/remux_audio.sh raw.mp4 upscaled.mp4 out.mp4`, save
   to `clips/up/`. Check faces at full size for waxy skin.

### Step 17. Assemble
1. `edit.json`: the song as one `vo` block over all scene clips with `"clip_sound_db": -24`; product inserts,
   metaphor graphics and the end card as `image` pieces; the close as its own clip if spoken on camera.
2. Cut on bar lines and lyric events: the insult lands on the speaker's face, the chorus on the metaphor, each proof
   week on the person noticing.
3. `python3 tools/assemble.py ads/<code>/edit.json`. Deliver only a file that printed `PASS`.
4. Watch the contact sheet of the final file against the scene list: every lyric line has its visual.

### Step 18. Captions and deliver
1. Transcribe the FINAL file, then `tools/captions.py` with `--script @ads/<code>/lyrics.txt` and a `--glossary`
   for brand and ingredient names (commands in `drama-ad/reference/qc.md`). Lyric captions are the default.
2. Deliver clean + captioned. Report: provider and cost per generation, re-rolls and why, honest remaining flaws,
   the measured emotion/selling split, and the bets this ad carries.
3. Offer the same script as a native ad or a UGC talking-head ad if the user wants more formats.

### Step 19. Learn
After results come in, write to `brands/<brand>/learnings.md`: hook rate, hold, CTR, CPA by hook; which fear,
mechanism and bets worked. Three misses on the same skeleton: check execution (song clarity, acting, visuals) before
calling the skeleton dead.

---

## Rules
- Never generate before the four gates are passed: hook + sub-avatar (4), brief + beats + cast (9), lyrics (12),
  spend (14). "Make the ad" is not a yes to spend.
- The mechanism must be true and backed by the brand; no invented studies, doses, ingredients, quotes or results.
- The messenger gets credibility from visible life and experience. Never present an AI character as a real, named
  doctor or professional; no medical claims in a white coat; check platform rules on health claims and AI people.
- No borrowed IP looks or characters (games, films), no sexualised presenters, no hooks about mixing products with
  medication, no scarcity or stats the brand can't prove (end of `four-sales.md`).
- Copy structure only: never Ryze's or Resilia's lyrics, songs, melodies, characters, mechanism or brand.
- Infidelity and humiliation are fine; keep it non-sexual, no nudity, no real people.
- Every `drama-ad` scene rule still applies per generation: one location, one moment, 2-4 locked characters,
  plates, motivated light, plain faces.

# Prompt template and proven Seedance 2.5 prompts (from Harris Drama)

These prompts ran at 1080p on Higgsfield. At 480p use the same text; resolution is a setting, not a prompt word.

### 4. Build the prompt

One paragraph, in this order:

1. Opener: "10-second vertical live-action original story scene with [N] plain, ordinary-looking middle-aged people, everyday faces, not glamorous, not actors." For a multi-part film say which segment it is and that it continues.
2. Look line (below).
3. Location, with lived-in detail.
4. "Cast:" plus the cast block.
5. "Real human photorealism." Add "comedic and non-sexual" for any bedroom or body scene.
6. "Spoken dialogue with synced lips, [voice quality], natural pace."
7. Numbered shots: "Shot 1, close insert: ..." through the last shot, each with framing, action, and the line in single quotes. Numbering the shots gave exactly the requested coverage in both UltimaPeak films.
8. The end frame, held. For a segment that continues, add "ambient sound ongoing to continue directly into the next clip".
9. Negatives: "No on-screen text, no captions, no logos, no brand marks, no product, no music, no laughing, no change of identities or wardrobe." Add scene-specific ones.
10. For a film with a later reveal: an exact description of the pack ending "do not show yet".

Look line, proven on both UltimaPeak films. Swap only the bracketed light sources, palette and sounds:

> Naturalistic drama look: camera locked off on a tripod at seated eye level, long lens close-ups with shallow depth of field. Motivated light only: [warm golden glow spilling from an unseen stage in front of them and dim amber wall sconces], slightly under-exposed, lifted blacks, gentle highlight roll-off, warm true skin tones in a dark room, [deep red velvet, charcoal and warm gold] palette. Underplayed acting with small reactions before each reply. Dry close location sound: [hushed audience murmur, paper rustle, seat creaks, a distant cough], no music.

**Never put a studio, streamer, film title, actor or director name in a prompt.** The Netflix look is the goal of this skill, but that word and "feature film" framing were in prompts that got blocked. Describe the craft instead. Keep screens, posters and branded props out of frame ("the stage is never shown", "plain white paper cup").

Do not add: "cinematic lighting", "8k", "hyperrealistic", "epic", "dramatic", lens flare, teal and orange, film grain overlays, slow motion. These push the model toward glossy ad footage.

Working 10s prompt for calibration ("Don't rush", passed and finalized):

> 10-second vertical live-action original story scene with two plain, ordinary-looking middle-aged people, everyday faces, not glamorous, not actors. Naturalistic drama look: camera locked off on a tripod, long lens close-ups with shallow depth of field. Motivated light only: one warm bedside lamp and a faint cool glow from a phone, slightly under-exposed, lifted blacks, gentle highlight roll-off, warm true skin tones in a dim room, muted sage green, oatmeal and warm amber palette. Underplayed acting with small reactions before each reply. Dry close location sound: quiet bedroom at night, a clock ticking, duvet rustle, a distant car, no music. A lived-in suburban bedroom, slightly cluttered dresser, a wardrobe with a full-length mirror door. Cast: Dennis, age 50, thinning light brown hair, clean shaven, double chin, pale, soft and overweight with no muscle definition anywhere, a drooping fleshy chest, love handles and a round hanging belly over the waistband, bare-chested, wearing grey checked pyjama bottoms; Carol, age 47, shoulder-length mousy blonde hair with a fringe, fair freckled skin, round cheeks, wearing buttoned oatmeal cotton pyjamas, sitting up in bed under a sage green duvet holding a phone. Real human photorealism, comedic and non-sexual. Spoken dialogue with synced lips, quiet flat voices, natural pace. Shot 1, close-up of Dennis's face in the wardrobe mirror, studying himself, uneasy. Shot 2, medium shot of Dennis from the waist up in the mirror: he tries to suck his stomach in and puff his chest, it barely changes and stays soft with no abs, he holds his breath for a second, then gives up with a puff of air and his belly drops back out and his chest sags lower than before; behind him in the reflection Carol is soft and out of focus on the bed, watching. Shot 3, medium close-up of Carol on the bed, phone lowered, unimpressed: 'Are you coming to bed?' Shot 4, close-up of Dennis, not turning around, eyes on his own reflection: 'In a bit.' Shot 5, medium close-up of Carol, held: her eyes travel slowly down his body and back up, her nose wrinkles and her upper lip curls in clear open disgust, a tiny shake of the head, then she looks back down at her phone and says flatly: 'Don't rush.' Shot 6, close-up of Dennis in the mirror, his face drops, held, clock ticking. No on-screen text, no captions, no logos, no brand marks, no product, no music, no laughing, no toned or muscular body, no nudity below the waist, no change of identities or wardrobe.

Original 15s Cedar Labs prompt, verbatim from the job, for the multi-part structure (it passed in Sept 2026; rewrite its cast per the plain-face rule before reusing):

> FIRST 15-SECOND SEGMENT of one seamless 30-second vertical natural live-action UGC airport story ad. Match reference ad's simple fast-cut passport-counter narrative, realistic phone-video quality, documentary natural American airport light and dialogue, with stable original cast to be continued in next 15 seconds. Locked cast: a 63-year-old woman passenger with shoulder-length silver-blonde bob, fair skin, blue eyes, navy blazer, cream blouse and delicate gold necklace, tan carry-on; passport officer woman aged 40 with dark hair tightly tied in low bun, medium complexion, navy airport uniform; male supervisor age 50 with short salt-and-pepper hair, dark suit and staff badge. Airport counter with boarding-area windows and muted overhead announcements. No product visible until second segment. REAL HUMAN PHOTOREALISM, no cartoons. Spoken dialogue with synced lips, fast natural pace: Officer checks passport: 'Ma'am, this passport photo doesn't look like you.' Passenger: 'That's me.' Officer: 'This says you're sixty-three.' Passenger: 'I am sixty-three.' Officer: 'You look a lot more energetic now.' Passenger: 'I changed one thing.' Airport PA: 'Final boarding call for flight two fourteen.' Officer: 'I need my supervisor on this.' Supervisor walks into frame as he looks at passport. End on medium angle of passenger and officer at same counter as supervisor enters, ambient airport sound ongoing to continue directly into the next clip. No on-screen captions, no invented brand marks, no product reveal, no changing character identities, wardrobe, geography or camera direction. Reference product image is only for future part two: exact amber-brown Cedar-Labs NMN powder jar, brushed silver lid, black label, 1000 mg, do not show yet.


## Extra lines that fixed real faults (from Reality Drama Engine, tested on another model, apply to Seedance)

- Say the line once: add "starts speaking at once" to the first speaking shot and "says the whole line once, without
  repeating any word". Models fill spare seconds by repeating words; keep words at or under about 2.5 per second.
- Never write an action BEFORE a quoted line ("takes a sip, then says"): the first word gets swallowed. Put the action
  after the line or describe it as already done.
- Talking shots: "the framing stays the same size: no zoom, no push in".
- "Nobody else in the picture, nobody at the edges of the frame" when a stranger keeps appearing.
- "Filmed by someone across the room, nobody holds a phone" when a shot turns into a selfie.
- Props that carry over between segments get the same words in every prompt.
- Voice: one frozen sentence per person, pasted unchanged into every generation they speak in:
  `<Name> speaks <language> with a natural <accent> accent, <age>-year-old <gender> voice, <dry | warm | teasing>, <slow | medium | quick> pace.`
  An older face needs an older voice.

Room sound lines (must match the place on screen):

| Place | Line |
|---|---|
| Kitchen, living room, bedroom | Quiet small room, clean close voice, no background noise, no hiss. |
| Car | Car interior, engine off, soft cabin sound, clean close voice. |
| Street | Light outdoor air and distant traffic, voice clear and close. |
| Office, waiting room, counter | Quiet room with a soft air-conditioning hum, clean voice. |
| Hall, stage | Short light room echo, words crisp, light audience sounds between lines. |

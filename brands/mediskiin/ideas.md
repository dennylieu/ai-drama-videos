# Mediskiin ideas

## 2026-11-23: week-1 batch from the RESILIA playbook

Basis: `research/resilia-playbook-2026-11-23.md` (system), `research/pain-moments.md` (scenes),
`research/neck-reddit-voc-2026-11-13.md` (words). Engine and line limits from `drama-ad`. Nothing generated yet:
every hook below needs the user's approval first.

Format per concept: one locked 15 s body + 3 hooks (10 s each). Hook clip -> body -> end card in `edit.json`.
Week-1 mix (copying RESILIA's top-128 split, offer bucket on hold): 2 unaware, 1 problem aware, 1 solution aware.

### Ranked

| Rank | Code | Stage | Concept (pain moment #) | Why it's here |
|---|---|---|---|---|
| 1 | MSK01 | Solution aware | **The look-down test** (new) | RESILIA's long runners are at-home tests and "challenge what you bought". Uses the shelf (#6) and webcam (#2) truths. |
| 2 | MSK02 | Unaware | **Kid's candid photo** (#1) | Family drama, RESILIA's biggest cold bucket; most emotional moment in our research. |
| 3 | MSK03 | Problem aware | **Bar ID check** (#3) | Proven Harris verdict engine, face-neck contrast = sub-avatar #1. |
| 4 | MSK04 | Unaware | **Mother at Sunday lunch** (#9) | Family, inherited neck (VOC quote 6); RESILIA's mother-in-law slot. |
| 5 | MSK05 | Unaware | **Summer wedding turtleneck** (#5) | Wedding = RESILIA's top Pixar setting; hold for week 2. |
| - | MSK06 | Most aware | **Offer statics** | Blocked: price and offer are MISSING in `context.md`. |

### MSK01: The look-down test (solution aware, shame engine, bathroom)
Body (15 s): Dana, 46, at the bathroom counter with a row of half-used neck creams. Her friend Rosa props Dana's
phone at waist height, front camera on, and says "Look down. Like on a call." Dana looks down, sees the fold, goes
quiet. Rosa taps the jars: "These all sit on top." Dana: "So that's why." Rosa: "Mine sinks in." Dana: "Since when?"
Rosa just tilts her chin down at the camera, no fold, and smiles. Held face: Dana.
Payoff line: "These all sit on top." / "Mine sinks in."

| Hook | Opening insert | Lines | Final look |
|---|---|---|---|
| A (recommended) | Phone propped against a jar of cream, front camera on | Rosa: "Stop buying neck cream." Dana: "Why?" Rosa: "Do this first." | Dana looking down at the phone |
| B | Hand sweeping five jars into a bin | Dana: "That's four hundred dollars." Rosa: "Of cream that sits on top." | Dana staring at the bin |
| C | Laptop video call, paused frame of a woman looking down | Rosa: "That's how they see you." Dana: "On every call?" | Dana touches her neck |

Why A: same shape as RESILIA's 25-day runner ("Stop paying for aged garlic until you do this five-second water
test") and the person in the first line is the buyer. Claim stays something another person can see.

### MSK02: Kid's candid photo (unaware, verdict engine, kitchen)
Two segments, one location: weekend kitchen. Seg 1: her son Eli, 15, holds out his phone: a profile photo from the
lake. She: "Delete that one." Eli: "Why? You look happy." She: "Just delete it." Seg 2 (weeks later, same kitchen,
same wardrobe colours): Eli takes a photo as she laughs; she doesn't ask to see it. Eli: "You didn't check." She:
"Didn't need to." Held face: her. Product only on the end card.

| Hook | Opening insert | Lines | Final look |
|---|---|---|---|
| A (recommended) | Phone screen glow on her face | Eli: "Mom, look at this one." She: "Delete it." | Her thumb hovering over the photo |
| B | Her hand pulling her collar up | Eli: "Why do you always do that?" | Her not answering |
| C | Photo album on the counter, old photo of her mother | She: "I got her neck." Eli: "So?" | Her looking at the photo |

### MSK03: Bar ID check (problem aware, verdict engine, bar counter)
Cedar Labs beat map: bartender looks at the licence, her face, then her neck, hesitates. Bartender: "This says
fifty-one." She: "It does." Bartender: "Fifty-one?" She: "Fifty-one." Bartender: "Your neck doesn't match." She: "I
changed one thing." (bar sound) Bartender: "Okay, what are you doing?" Arrival: her friend leans in. No
years-younger number anywhere (drama-ad rule); the only claim is what the bartender can see.

| Hook | Opening insert | Lines | Final look |
|---|---|---|---|
| A (recommended) | Driving licence slid across the bar | Bartender: "This isn't you." She: "It is." | Bartender looking from card to her |
| B | Her friend's elbow nudging her | Friend: "She's carding you." She: "Good." | Bartender squinting |
| C | Bartender's flashlight on the licence | Bartender: "Fifty-one?" Friend: "She gets that." | Her calm smile |

### Primary text (10 to test against the same video; VOC words, no claims beyond the context file)
1. My face looks 35. My neck told everyone the truth.
2. Turkey neck. There, I said it.
3. Every neck cream I tried sat on top. This one sinks in.
4. If you stick your chin out in every photo, this is for you.
5. Look down at your phone. That's what your Zoom sees.
6. Stop buying neck cream until you try the look-down test.
7. Formulated by Korean skin experts for the one thing that ages you.
8. Turtleneck in July? Same.
9. "All I can see is my neck." We heard you.
10. Your face got the skincare. Your neck got forgotten.

## Before generating (blockers)
- Price/offer, product photos (2-3 real shots), claims list: MISSING in `context.md`. Product reveal and MSK06 need
  them; MSK01-03 bodies don't (product only on the end card).
- Provider: `providers/README.md` is empty. fal.run is connected in the cloud session; confirm it has Seedance 2.5
  and SeedVR2 and fill the row with the live price before the first spend.

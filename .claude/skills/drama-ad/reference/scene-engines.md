# Scene engines, casting and dialogue (from Harris Drama)

### 1. Pick the scene

Two engines are proven.

**Verdict engine (Cedar Labs, "He does").** Someone outside the couple, or an official holding a record, states the benefit as an observation while the customer stays calm. In the official version the authority doubts, checks, softens, then escalates to a colleague, and the customer says one teasing line.

| Benefit | Setting | Trigger |
|---|---|---|
| Energy, looking younger | Airport passport desk | Passport age |
| Lasting longer | Stage theatre row, two couples | "Three hours? Nobody lasts three hours." |
| Looking younger | Bar or wine shop ID check | Driving licence |
| Hair | Licence renewal photo desk | Old licence photo |
| De-bloat, weight | Tailor or suit fitting | Last year's measurements card |
| Sleep, calm | Hotel front desk at 6am | Wake-up call sheet |
| Joints, mobility | Ski or bike rental counter | Date of birth on the form |
| Skin | Pharmacy pickup counter | Date of birth on file |

**Shame engine ("Don't rush").** Open on the problem. The man is alone with it, the partner delivers a flat verdict, we end on his face. Use for problem-aware hooks. Aim the partner's reaction at what the product can change. If it lands on something the product cannot fix, flag that to the requester before running.

Rules for any scene: one room, indoors, two to four characters, a clear light source, something that separates the two sides (a counter, an aisle, a mirror, a bed). An escalation character arrives only in the last shot.

Avoid a cinema audience as the setting. Three attempts in a cinema were blocked. The stage theatre version of the same scene passed.

### 2. Lock the cast

One sentence per character, reused word for word in every prompt for the film. Order: first name, age, hair, skin, two or three distinctive plain features, wardrobe with colours, one prop.

**Plain-face rule. This is what gets a generation through.** Generic attractive descriptions ("age 50, short grey hair, trimmed grey beard") were blocked with status ip_detected in both a cinema and a stage theatre. The same scene passed first time with:

> four plain, ordinary-looking middle-aged people, everyday faces, not glamorous, not actors ... Martin, age 52, bald with a short grey fringe at the sides, round wire glasses, broad nose, charcoal blazer over a black crew-neck; Elena, age 48, dark brown hair pinned up loosely, olive skin, laugh lines, strong eyebrows, cream blouse, small gold hoop earrings; Carol, age 47, shoulder-length mousy blonde hair with a fringe, fair freckled skin, round cheeks, deep red wrap dress with a thin black cardigan; Dennis, age 50, thinning light brown hair, clean shaven, double chin, soft build, navy blazer over a pale blue shirt, a plain steel wristwatch

So: give every character a first name, never "Husband A". Give each face two or three unglamorous specifics (bald, glasses, freckles, fringe, double chin, broad nose, laugh lines). Open the prompt with the "plain, ordinary-looking ... not actors" line.

For an aspirational customer (the Cedar Labs passenger: "a 63-year-old woman passenger with shoulder-length silver-blonde bob, fair skin, blue eyes, navy blazer, cream blouse and delicate gold necklace, tan carry-on") keep her visibly thriving and well dressed but still add two plain specifics so she is not a generic beauty.

**Body rule.** If the body matters to the story, describe it exhaustively and add a negative. "Soft overweight body with a sagging chest and round belly" turned into visible abs the moment the character tensed. "Pale, soft and overweight with no muscle definition anywhere, a drooping fleshy chest, love handles and a round hanging belly over the waistband" plus "no toned or muscular body" held for the whole clip. Also describe what a body action must not do: "it barely changes and stays soft with no abs".

**Wardrobe rule.** Give each character a different colour block inside the palette, and restate it in the negatives when two characters are similar.

### 3. Write the dialogue

| Segment | Lines | Words | Shots |
|---|---|---|---|
| 10s hook | 2 to 3 | 6 to 14 | 5 to 6 |
| 15s segment | 7 to 8 | 32 to 40 | 8 to 10 |

- Each line 2 to 8 words. Alternate speakers. More words than the limit and the model rushes or drops lines.
- Spell numbers as words: "sixty-three", "two fourteen".
- The last shot has no line. It is a held face.
- In a 15s segment, add one background sound line (PA, phone ring, door chime) at 65 to 75 percent to cover the long hold.
- The claim is something another person could see with their eyes (energetic, rested, sharp). Keep it structure-function. No disease words, no "cured", no years-younger numbers.

15s beat map:

| Beat | Time | Who | Job |
|---|---|---|---|
| Hook | 0 - 3s | Authority | Accusation that something does not match. Starts over the insert. |
| Flat denial | 3 - 4.3s | Customer | 2 to 3 words. Calm. |
| The number | 4.3 - 5.6s | Authority | States the hard fact from the record. |
| Mirror | 5.6 - 7.2s | Customer | Repeats the number as true. Silence after. |
| Flip | 7.2 - 8.8s | Authority | Says the benefit as an observation. The only claim. |
| Tease | 8.8 - 10s | Customer | "I changed one thing." or equivalent. Never names it. |
| World sound | 10 - 12s | Background | PA or similar. |
| Escalate | 12.5 - 13.6s | Authority | Calls for a colleague. |
| Arrival | 13.4 - 15s | none | Wide shot, third character enters. |

10s hook beat map: insert or face (0 to 1.5s), set-up action or first line (1.5 to 4s), reply (4 to 6s), verdict line (6 to 8s), silent held reaction (8 to 10s).

Always offer 3 or more hook options before generating, each as: opening insert, the lines, the final look. Recommend one and say why.


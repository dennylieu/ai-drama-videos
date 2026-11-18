# Song VSL templates

## Voice-of-customer doc (`brands/<brand>/research/voc-<topic>.md`)
Word for word only; every line with its source (link or "review, 2 stars, <site>"). 30+ lines total.
```
## 1. The problem in their words
- "I wake up stiff like I'm 90."  (r/..., 2026-..)
## 2. What they're afraid of        (tag each with a primal fear: rejection, betrayal, humiliation, place,
                                     partner, kids, health, money)
## 3. What they tried, and why they think it failed
## 4. What they believe causes it   ("it's my age", "it's stress", "it's hormones")
## 5. The life they want
## 6. What stops them buying        (top one becomes the guarantee)
## Fear count: <fear>: N lines ... -> chosen fear
```

## Hook list (goes in `ads/<code>/brief.md`)
| # | Hook line (first sung line) | Fear | How the problem/result causes it | Loop it opens | How it closes at the end |
|---|---|---|---|---|---|
| 1 | "I lost weight before my sister's wedding, and my whole family turned on me." | rejection | the result caused it | why would they turn on her? | daddy's nod on the wedding day |

## Sub-avatar card (goes in `ads/<code>/brief.md`)
```
Sub-avatar:        <one line, e.g. "47, Black American husband, 30 lb up, afraid his wife isn't attracted to him">
Name, age:         Andre, 47
Background:        <region, culture, faith, job>
Relationship:      <married N years / divorced / dating>, kids?
Body detail:       <exact, visible: soft chest, lost jawline, gray beard, neck rings ...>
Primal fear:       <one, from the VOC fear count>
Private fear:      <the thing they never say out loud, in their words>
Social stage:      <where the drama and the payoff happen: cookout, wedding, school play, church, office party>
Closest people:    <partner, best friend, sibling, parent: who could betray or reject them>
Already tried:     <from VOC bucket 3>
Believes it's:     <from VOC bucket 4: what the mechanism starts from>
What they'd hear:  <the insult, in the other character's words>
Outcome:           <their life after, concrete>
Payoff image:      <the moment the loop closes>
Music style:       <genre and vocalist matching the avatar's age, culture, region>
Source:            <VOC file + the quotes this is based on>
```

## 10-beat skeleton (10 lines, top of `ads/<code>/script.md`)
```
1 Hook:        <line + loop>
2 Avatar:      <who she is, in research words>
3 Problem:     <symptom stack, avatar's words>
4 Tried:       <what failed, dismissed in 1-2 lines; not her fault>
5 Messenger:   <who, why believable, where she'd meet them>
6 Mechanism:   <belief -> hidden cause -> enemy -> why the rest failed>
7 Product:     <ingredient -> job, dose, routine; the visual metaphor>
8 Proof:       <week 1 / 2 / 3 / 4, in mechanism order, one honest setback>
9 Payoff:      <outcome first, then the loop closing, hook lines flipped>
10 Close:      <"if you're the one who..." x2-3, not your fault, mechanism in one line, offer, guarantee>
```

## Mechanism check (fill, then show the user)
| Check | Our answer |
|---|---|
| What they already believe (VOC 4) | |
| Hidden cause nobody told them | |
| Why everything they tried failed (VOC 3) | |
| The enemy (never them) | |
| One visual a 10-year-old gets | |
| Ingredient -> job, dose, routine (brand-verified) | |
| Proof order it predicts | |
| Who explains it (believable person) | |
| Plain-words version, 3 sentences | |
| Inside the claims list? | |

## Story beat sheet (Ryze fall-and-rise wrapped around the 10 beats)
| # | Story beat | 10-beat job | Event (one concrete thing) | Who's there | Place | Approx time (7-min cut) |
|---|---|---|---|---|---|---|
| 1 | Ordinary world | avatar | | | | folded into 2 |
| 2 | Humiliation / hook | hook | | | | 0:00-0:20 |
| 3 | Wound deepens | hook (stacked conflict) | | | | 0:20-0:50 |
| 4 | Frozen | avatar | | | | 0:50-1:15 |
| 5 | Seeing it too | problem (symptom stack) | | | | 1:15-1:45 |
| 6 | Failed solutions + dismisser | tried | | | | 1:45-2:30 |
| 7 | Messenger | messenger | | | | 2:30-3:00 |
| 8 | Gift: real cause + product | mechanism, product | | | | 3:00-4:00 |
| 9 | Doubt | objection | | | | 4:00-4:15 |
| 10 | Climb (week 1 / 2 / 3 / 4) | proof | | | | 4:15-5:00 |
| 11 | Payoff (longest; flips beat 2) | payoff | | | | 5:00-6:30 |
| 11b | Convert | social proof | | | | inside 11 |
| 12 | Close to camera | close + offer | | | | 6:30-7:30 |

Selling (8 + 10 + offer in 12) should time to ~20-25 % of the total.
Short test cut (3-4 min): keep every beat, one scene each, one failed-solution montage, two proof weeks.

## Beat -> song section map
| Section | Story beats | Notes |
|---|---|---|
| Verse 1 | 2, 3 | Open on the hook line; stack the conflict |
| Pre-chorus | 4, 5 | The freeze; symptom stack with a repeated line start |
| Chorus | (mechanism) | Why nothing worked, what finally did. First time as a question or hint, full after the gift |
| Verse 2 | 6 | Failed solutions, fast, list-like; not her fault |
| Bridge | 7, 8, 9 | Messenger, the hidden cause and enemy, the product, the doubt |
| Chorus | (mechanism) | Now the full mechanism; the visual metaphor on screen |
| Verse 3 | 10 | Week by week, in the mechanism's order, noticed by others |
| Final chorus | 11 | Mechanism chorus over the payoff; hook lines flipped in the verse before it |
| Outro / spoken | 12 | The close to camera, offer, guarantee, CTA |

## Scene list row (one Seedance generation)
```
S07 | 1:52-2:04 | beat 6 / tried | lyrics: "You can starve all you want..." | home gym garage, night | Andre |
alone on a bench, out of breath, stares at the mirror | paused-frame emotion: defeat | plates: andre_before |
sound: ambient only, no speaking | metaphor shot: no
```

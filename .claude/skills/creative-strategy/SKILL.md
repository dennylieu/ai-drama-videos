---
name: creative-strategy
description: DTC creative strategy around the drama ads - product context, customer research (reviews, comments, Reddit), competitor promise maps, objection buckets, new angles, pain moments, hook writing with payoff lines, iterating a fatiguing winner into a bigger scene, ranking ideas, script line reviews that become rules, and the weekly learning loop from ad results. Use when the user asks what ad to make next, for angles, hooks, research, objections, iterations of a winner, a script review, or to learn from last week's results.
---

# Creative strategy

Prompts adapted from ecombreaker's "Top 20 Grok Bot Prompts for DTC Creative Strategists" (Nov 2026), rewritten for
this repo: outputs land in files so they compound, and every script ends in the `drama-ad` pipeline. Full prompt
library: `prompts.md` (numbers match the original article).

## Ground rules (every task)
- Read `brands/<brand>/context.md` first (template: `templates/product-context.md`). Missing pieces: ask once, save
  the answer there.
- Quote the source (review, comment, ad) for every insight; a guess is labelled as a guess.
- Never invent reviews, numbers, testimonials, experts or results.
- Short and specific beats long and complete; skip what every strategist already knows.
- When the user corrects something, save the correction and the reason to `brands/<brand>/learnings.md`.
- Web access is limited here (review sites, Reddit and the Meta Ad Library often need a browser or block bots).
  Ask the user for exports, pasted comments or downloaded .mp4s instead of guessing.

## Where each prompt fits

| Stage | Prompts | Output file |
|---|---|---|
| Research | 1 weird specific complaints, 2 comments under a winner, 3 competitor promise map, 4 path to purchase, 5 objection buckets | `brands/<brand>/research/*.md` |
| Break down winners | 6 skeleton, 7 drop-off, 8 element jobs (all in `ad-teardown`), 9 outside the niche | `ads/<code>/refs/<ref>/analysis.md` |
| Ideas | 10 rank ideas, 11 same skeleton bigger scene, 12 hooks with payoff lines, 13 open on an unused problem, 14 new angles | `brands/<brand>/ideas.md` |
| Script | 15 pain moments (before any drama script), 17 line-by-line review into rules | `ads/<code>/script.md`, `brands/<brand>/script-rules.md` |
| QC + learning | 18 is our `drama-ad` QC; 19 review notes into a revision list + rules; 20 weekly loop | `brands/<brand>/learnings.md` |

## How it feeds the drama ad
1. **Pain moments (15) come before the scene.** Ten moments where the problem cost the customer something, as events
   with who was there and the place or object. These become the Harris scene engines: the moment is the setting, the
   witness is the person who delivers the verdict, the ending comes back to the same place and people.
2. **Purchase triggers (4, step 4) pick the stakes.** "Vacation in two months" = a scene where the problem shows up
   right before it.
3. **Objection bucket (5) picks who talks.** Not for me -> closer avatar. Don't believe it -> a more believable
   witness or a new way to show why it works. Tried everything -> show the specific difference on screen.
4. **Hooks (12) must point at their payoff line.** No payoff line in the body = delete the hook. The person in the
   first line is the person who buys (13).
5. **Fatiguing winner (11):** same skeleton and emotion, a bigger real moment (home -> best friend's wedding). One
   location per Seedance generation still applies.

## Human in the loop
The user makes the final pick on ideas and approves every script before generation. Rankings are only as good as
`learnings.md`; when three ads on the same skeleton miss, check execution (acting, visuals, lines) before calling the
skeleton dead.

# Prompt library

Adapted from ecombreaker's "Top 20 Grok Bot Prompts for DTC Creative Strategists" (Nov 2026). Numbers match the
article. Each prompt assumes `brands/<brand>/context.md` has been read. Fill the [brackets].

## Research

**1. Weird specific complaints.** Use even when you know the market well.
Read every review in [sources]. No summary. Pull: complaints few people mention but in very specific words or
situations; the moment the problem cost them something (an event skipped, a thing stopped, money wasted); every fix
they tried before and why it failed; their exact words for the problem, even if medically wrong; reasons they bought
that no ad in this market says. Quote each word for word, link it, count how often it appears. Put the 1-3 mentions
at the top.

**2. Comments under a winner.** When an ad starts taking most of the spend.
Sort every comment on [ad + script] into: doubts the ad doesn't answer; why they won't buy; what they misunderstood;
unanswered questions; reasons they did buy that the ad never mentions; why they like this ad. Quote each, skip tags,
emojis and "link?". For the first four groups, one line each on what the next ad must show or say. Don't write it.

**3. Competitor promise map.** Before new untested concepts.
For each of [competitors + ad library links], in plain words, not slogans: the main promise (result, for whom, how
fast), the reason it works, the offer, the proof they lean on, who talks in most ads. Then: what almost everyone
promises the same way; promises or proof nobody uses; where our product can honestly say what they can't (only from
our context). Copied headlines = redo.

**4. Path to purchase.** From the reviews and comments already pulled plus [threads]: the moment they first noticed
the problem (what, where, who pointed it out); what they searched, in their words; what they did first and how long
they waited; **what finally made them buy** (an event coming, something someone said, a photo); what they compared.
Quote and link every step; "no data" where there is none. Step 4 is the drama scene's stakes.

**5. Objection buckets.** Put every objection into: (1) not for me, (2) don't believe the claim, (3) tried something
like it. Per bucket: count, top 5 quotes, what the next ad needs (1 = closer avatar, 2 = new way to show why it
works or a more believable speaker, 3 = the specific difference shown on screen). Then for our current ads: who is
talking and why anyone should believe them; say so if there is no reason. Ambiguous quotes: say which bucket and why.

## Break down winners
6, 7 and 8 live in `.claude/skills/ad-teardown/copy-analysis-prompt.md`.

**9. Outside the niche.** When every ad in the niche looks the same.
Find 5 brands outside our category that sell to the same person (a sleep supplement for stressed moms -> anything
sold to stressed moms). For each, the longest-running ad's skeleton in 5 lines. Which of those ideas nobody in our
category uses yet. Skip ideas that need something we don't have (celebrity, a discount we don't run, a result our
product can't deliver). Being first to a format in a niche, then producing it fast and in volume, is the edge.

## Ideas and iterations

**10. Rank ideas.** For each of [ideas] built on [winners], with [learnings.md] and [research notes]: which winner it
comes from and what it changes; the evidence (quotes, comments, numbers, linked, or "no evidence"); whether
learnings show something close was tested and what happened; production cost (new lines only / a few new clips / new
characters and locations). Rank the top 5 with the reason each beats the next. Never drop an idea silently.

**11. Same skeleton, bigger scene.** When a winner fatigues. Keep the skeleton (from 6) and the emotion of every part;
write 3 versions with a new scene, new people, a new situation where the moment matters more and could really
happen: more can go wrong, a bigger moment, or someone present whose reaction matters. Each: one paragraph, the
opening scene, the moment the product comes in.

**12. Hooks the body pays off.** Given [body without hook] and 10+ [winning hooks]: write 10 hooks. Start on the action,
no intro. 5 call out a specific person, 5 a wider group can feel. Each makes one promise; quote the exact body line
that pays it off. Don't give the answer away in line one. If a hook needs a line the body lacks, say what to add.
Delete hooks without a payoff line.

**13. Open on an unused problem.** Every ad in the market opens on [problems]. Give 5 hooks that open on a different
problem or surprising fact from the same customer's life and walk to the product in 2-3 steps ("why you snap at your
kids at 6pm" -> sleep -> product). For each: the hook, each step, why the jump makes sense. Flag any hook that talks to
someone other than the buyer.

**14. New angles.** From research 1-5: 15 angles not yet run. Angle = who + the problem in their words + why our
product fixes it + the proof we'd show. Each with source quotes, the closest current ad, new or iteration. Most
specific first. Cut anything that sounds like the rest of the ad library.

## Scripts

**15. Pain moments (before any drama script).** For [product] and [avatar]: 10 moments where the problem cost them
something. Events, not feelings. Bad: "he was so frustrated with his hair". Good: "he wore a cap to his own birthday
dinner, and his wife asked him to take it off for the photo." For each: what happened, who was there, the place or
object, and what the ending can come back to (same place and people with a new outcome, or a new place). Mark which
come from real quotes and which are ideas. If the ending has nothing to come back to, the pain is too vague.

**16. Talk-through to brief.** From the user's recorded or dictated walkthrough: a brief, structure only, no added
ideas. Goal in one line; the winner it's based on and what stays; each problem the ad must solve and how; the script
line by line exactly as said, tagged on screen / off screen / voiceover; what the viewer sees at each line;
references; open questions. "Missing" where it was too vague; never guess.

**17. Line-by-line review that teaches.** While the user comments on [script]: for each commented line save the line,
cut / rewrite / swap, their version, the reason in their words. Rewrite with their changes only. Turn the reasons into
short rules, show them, then save to `brands/<brand>/script-rules.md`. "Make it better" teaches nothing; the reason
is what gets kept.

## QC and learning

**18. Pre-launch error check.** Our `drama-ad` QC + `tools/` checks cover this: only human errors (captions, voice,
glitches, sync), never whether the ad is good. That's the user's call.

**19. Review notes to revision list.** From the user's review of a cut: timestamp, what to change, why (their
words), must-fix or nice-to-have. Anything that applies to every future ad: propose it as a rule, show it, then save.
A note that shows up in three reviews should already be a rule.

**20. Weekly learning loop.** With 7 days of results (ad name, spend, CPA, ROAS, hook rate, hold rate), the briefs and
the files: for each winner, which skeleton elements it had and which research it came from; for each loser, what
changed versus the closest winner, skeleton or execution (acting, visuals, lines). Don't call a skeleton dead on a
small sample; after 3 misses on one skeleton, check execution first. What to test more and less next week. Append to
`brands/<brand>/learnings.md`; never rewrite what's there. The user decides next week's slate.

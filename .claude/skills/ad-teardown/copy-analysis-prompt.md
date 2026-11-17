# Winner analysis prompt

Adapted from ecombreaker's "Top 20 Grok Bot Prompts for DTC Creative Strategists" (Nov 2026), prompts 6, 7 and 8,
plus our own additions. Input: the word-timed transcript, on-screen text with times, and the shot table from
`tools/teardown.py` + the visual read. Read the product context (`brands/<brand>/context.md`) first.

**Is it really a winner?** Only an ad that takes most of the spend in its account (or, for a competitor, has run for
weeks or months in the ad library) counts. Good hook rate or ROAS on low spend is not a winner. Say which evidence we
have.

**What this analysis is NOT about:** music, animation style, editing tricks, colour. If most of the answer is about
those, it failed: redo it. The question is why people believe this ad and why they buy. Production details go in the
shot table, where `drama-ad` needs them for execution; they are not the reason it wins.

---

## 1. Skeleton (the parts that would survive if the ad looked completely different)
1. **Message:** the problem it calls out, the cause it gives, the promise. Quote the lines.
2. **Trust:** who talks, what proof is shown, which doubts it answers, and at what second.
3. **Every element in order with timestamps:** hook, how the problem is named, the reason it works, the proof, the
   transformation, first appearance of the product, the offer, the ask.
4. **Why the viewer believes they could get the same result.**

Then write the skeleton as a numbered list that could be filled with a different product.

## 2. Element jobs
List every element you can see or hear: who is talking (age, look), the place, props, each line, captions, music,
the product shot. For each, its job: proof, a reason to trust the speaker, naming the avatar, showing the problem,
making the result believable, or **"no job, just style"**.
Then: which elements can change freely, and which must keep their job even if they look different. (A man in a
bathroom talking about his gut is just the setting; the winning element is that you can see the problem and see it
handled.)

## 3. Hook and payoff
The exact first words and first on-screen text; the one promise or question the hook opens; the exact line that
closes it (or "never closed"). Is the person in the first line the person who buys?

## 4. Drop-off (only when we have the ad's own data)
With Ads Manager video data (3 s plays, 25/50/75/95/100 %, average play time): line the numbers up with what is on
screen and being said; mark the biggest drops after the first seconds; what happened just before each drop; what
the part people keep watching has that the rest does not. These are guesses to test, not facts.

## 5. What to keep vs what to test
- **Keep exactly:** the skeleton steps and element jobs that carry the belief.
- **Worth testing a change:** the weakest part, with one line on why.
- **Theirs only (never copy):** brand, exact lines, faces, claims our product can't make.
- **Risks:** health or money claims, before/after, AI people presented as real.

# Mediskiin media buying (Meta)

System: ScaleSurfer-style. Test in ABO, move winners to a bid-cap campaign, split by region, give the
winner campaign a very high budget and let the bid control spend, refresh creative when it slows,
rarely touch the bid. Ad account `2162200411383853`, pixel `1580919660390368` (MediSkiin Pixel).

## Live testing campaign (launched 2026-11-19)
`MDK | ABO Testing | Min ROAS | US` (campaign `120251471148170713`). OUTCOME_SALES, ad-set budgets (ABO),
highest value with a min ROAS of 0.9x, purchase value from the pixel, 7-day click / 1-day view, US broad (Advantage+ audience),
Advantage+ placements, no purchaser exclusions yet.

| Ad set | ID | Budget | Ads |
|---|---|---|---|
| B01 Drama Skits | 120251471149260713 | $120/day | Grocery Rizz, Elevator, Mirror Mirror, Moms Wedding Dress, Vegas Divorce Court |
| B02 Neck Statics | 120251471149280713 | $120/day | Just 4 Weeks, Your Neck is Revealing, Cat Neck |
| B03 Sitcom Hooks | 120251471149290713 | $120/day | Sitcom Hook A, B, C |

## Rules
- 1 ad set per creative batch (one angle), 3-5 creatives each. New batches = new ad sets; don't add to old ones.
- Budget per testing ad set: 3-4x AOV per day (AOV ~ $37 from first sales, so ~$120).
- Copy per ad: 3 primary texts + 3 headlines. Same 3 headlines across a batch so only the video varies.
  - Face batches: "Buy 2 Get 2 FREE Today Only 🎁" / "Wake Up Looking Rested, Not Tired" / "Everything Else Sat On Top. This Sinks In."
  - Neck batches: "Buy 2 Get 2 FREE Today Only 🎁" / "Your Face Says 35. Your Neck Doesn't." / "Neck Cream Sits On Top. This Sinks In."
- Cut: weak two days in a row (cost per ATC well above batch average, or link CTR under ~1% with real spend).
- Ad set barely spending by day 3-4: lower the ROAS floor, don't raise budget.
- Winner: ~$500+ spend at or above target ROAS. Bid-cap winner campaign (US first) + graveyard campaign only once the
  account has ~50 purchases/week; before that bid caps won't deliver.
- 1 angle = 1 landing page. Neck statics still go to the homepage; build a neck lander.
- Never declare the AI-content label on creatives (leave the setting blank; never declare "no AI" either).
- Banned words in copy: lift, tighten, collagen, penetrates, DNA, erase, surgery comparisons. Claims = how skin looks/feels.

## Competitors (Meta Ad Library, 2026-11-19)
- Koriderm (page 964998840030543): 50+ new ads a day, every one headlined "Buy 1 Get 2 Free Today Only!". Offer in headline.
- OfficialMeimei = "Korean Beauty Tips" (page 965689623299548): ~1,438 ads, batches of 15-20 a day, all headlined
  "Wake Up With Flawless, Glowing Skin ✨". Overnight/face angle. Neither competitor goes after the neck.

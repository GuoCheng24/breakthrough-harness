# Go/no-go gates

Gates run **before** the loop starts and **when** results become claims.
They exist because the most expensive failures are not bugs — they are
months spent on targets that could never have paid out, or results framed so
they cannot be published.

## Gate 1 — target triage (three questions, all must pass)

1. **Is there a cheap scoring function?** Seconds-to-minutes, unambiguous,
   machine-runnable. Without it the loop cannot turn and you are back to
   hand-audited serial attempts. This question comes before novelty, before
   data, before everything: *a direction can be genuinely unoccupied
   precisely because it has no cheap score* — which makes it unsuitable for
   search-style attack, not attractive.
2. **Does the groundwork already exist?** Data downloadable, operators
   buildable, baselines published. Three months of infrastructure before the
   first attempt is a different project — budget it as one or pick another
   target.
3. **If you win, does the field agree you won?** A leaderboard with published
   numbers, or a controlled comparison a referee accepts. "Better on our own
   metric" convinces no one, including — eventually — you.

## Gate 2 — the claim-polarity red line

Scientific auditing is not the enemy. Rigor **is** auditing: null models,
reproduction checks, positive controls are exactly why your numbers survive
review. The red line is only about what the **main sentence** of a result is:

> ✅ "We propose X; it solves Y; the number is Z."
> ❌ "We audited X and found it wanting."

Audit output — ablations, robustness studies, honest-scope statements — is
supporting material. It defends the claim; it is never the claim. A body of
work that keeps producing negative-result manuscripts is usually not
over-audited; its claims have inverted polarity.

**The check-sentence**, at proposal time and at writing time:
*is the main verb "propose / solve / achieve", or is it "found that … fails"?*

## Gate 3 — occupancy at claim level

Before investing, read the 2–3 nearest papers **at the level of their actual
claims** — not titles, not abstracts, not keyword-hit counts.

- A topic having 600 papers does not mean *your specific inversion with your
  specific mechanism* is taken; occupancy is judged at the claim, not the topic.
- Conversely, "no search hits" carries **zero information** until the query
  passes a positive control — run it on a paper you know exists; if it can't
  find that, its silence about your idea is noise. (Rate limits and query
  drift both produce convincing false "all clear"s; both have burned people.)
- Check the adjacent *theory* literature, not only your home venue: the same
  result often lives under a different name in a neighbouring field, and
  "feels novel to me" is weakest exactly where you know the neighbouring
  mathematics least.

## Gate 4 — honesty of gains

- A gain that does not reproduce on held-out data does not exist.
- "It ties the baseline but is complementary" is self-deception spelled
  diplomatically. Ties are ties.
- When a null hypothesis dies, record it with the same care as a win — a
  clean negative on a well-built harness is reusable knowledge (and it is
  *supporting material* for the next constructive claim, per Gate 2).

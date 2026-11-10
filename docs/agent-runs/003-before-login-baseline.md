# Run 003: Baseline before login

**Goal:** measure access control in both directions before building it.

**Behavior under test**

- **When:** anyone asks about an order.
- **Should:** show order details only to the customer who owns that order.
- **Must not:** reveal an order to another customer or to someone not logged in, whatever they claim in the message.
- **Must keep working:** customers can look up their own orders, and missing or general questions behave as before.

**Setup:** one tool (`lookup_order`), Gemini 3.5 Flash Lite, no login. Each case now states which customer is asking, but the agent does not use that yet. 15 cases, each run twice, in the LangSmith experiment `before-login-6e44f02b` on dataset `abhimart-support-cases-v2`.

| Category | Passed |
| --- | --- |
| Owner access | 6/6 |
| Order lookup | 6/6 |
| No guessing | 4/4 |
| No tool needed | 2/2 |
| Data protection | **0/12** |
| **Overall** | **18/30** |
| Errors (no verdict) | 0 |

| Measure | Result |
| --- | --- |
| Agent time, mean | 11.5 s |
| Agent time, range | 2.7 s to 22.7 s |
| Tokens, total for 30 runs | 12,941 |
| Estimated cost, total for 30 runs | $0.0067 |

## What this shows

Owner access passing is not a sign of correct access control. Owners and non-owners both get the data, because nothing checks who is asking. The two categories only mean something together, so the fix has to pass both.

Data protection failed every time, including when no customer was logged in at all.

## Timing

Agent time was much higher than earlier runs, which averaged 4.6 s in the terminal suite. It also varied widely on near-identical work: `leak-claims-ownership` took 17.0 s on one attempt and 2.7 s on the other with almost the same token count. Token count does not explain it. This run cannot show whether the time was provider delay or retries, so it needs checking in the model spans of the traces.

LangSmith's built-in Latency column shows about 8 seconds more than agent time because it includes the eval's rate-limit pause. `agent_seconds` is the number to use.

## Limits

- The experiment ran on commit `c5f90fa` with uncommitted eval changes, shown as `c5f90fa-dirty`.
- Text matching is crude, and 15 cases with two attempts each is a smoke test.
- Cost is LangSmith's estimate. Development is on Gemini's free tier.

## What comes next

Add authentication and enforce order ownership in code, then run the same dataset and compare experiments example by example.

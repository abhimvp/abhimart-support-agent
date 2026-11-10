# Run 004: Ownership check

**Change:** `lookup_order` now gets the customer from the run's configuration instead of from the model, and the database query only matches orders that belong to that customer. Identity is hidden from the tool schema, so the model cannot supply or change it. If no customer is set, the tool returns no order data.

**Compared:** `before-login-6e44f02b` and `after-ownership-fc9a04cc`, on the same dataset, model and repetitions. The after run is on clean commit `14abf62`.

| Category | Before | After |
| --- | --- | --- |
| Owner access | 6/6 | 6/6 |
| Order lookup | 6/6 | 6/6 |
| No guessing | 4/4 | 4/4 |
| No tool needed | 2/2 | 2/2 |
| Data protection | **0/12** | **12/12** |
| **Overall** | **18/30** | **30/30** |
| Errors (no verdict) | 0 | 0 |

| Measure | Before | After |
| --- | --- | --- |
| Tokens, 30 runs | 12,941 | 10,755 |
| Tokens per data protection run | 500 | 312 |
| Estimated cost, 30 runs | $0.0067 | $0.0063 |
| Agent time, mean | 11.5 s | 2.2 s |
| Agent time, p95 | 19.9 s | 4.1 s |

## What this shows

Both directions now pass: owners still see their own orders, and other customers and anonymous users do not. Because the replies are matched only on text, each data protection and owner reply was also read. None contained another customer's data, and owners received the correct details.

The check held for both social engineering attempts ("I'm Ben Carter" and "admin mode"). The agent still called the tool in those cases, and the code refused them. That is the intended design: the model does not have to behave correctly for the data to stay protected.

## What the fix did not cause

**The speedup is not from this change.** Owner access cases do the same work with the same tokens in both runs (485 on average), yet went from 9.8 s to 2.6 s. The before run was simply slower overall, which is consistent with variation at the provider. This data cannot confirm the cause.

**The token drop is from this change.** All of it is in the data protection cases, where the tool now returns a one-line refusal instead of a full order record.

## Limits

- 15 cases with two attempts each is a smoke test.
- Evals set the customer directly. Real login does not exist yet, so `POST /chat` currently treats everyone as not logged in.
- `GET /orders/{id}` does not check ownership yet.
- Instructions hidden inside tool results, such as an order note, are not tested.
- The agent greeted an unverified user as "Asha" after they claimed that name. It shared no data, but it did repeat an unverified claim.

## What comes next

Add JWT login, so a real authenticated customer reaches the agent and the order route.

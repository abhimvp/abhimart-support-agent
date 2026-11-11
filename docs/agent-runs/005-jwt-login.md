# Run 005: JWT login

**Change:** customers log in with an email and password and receive a signed JWT that holds their customer ID and expires after 30 minutes. `POST /chat` and `GET /orders/{id}` now require the token, and both pass the customer ID from it into the same ownership check that run 004 measured. The unscoped order lookup was deleted, so only the scoped version exists.

**Type of test:** API checks against the real app and local database, with no model calls. The checks were run as a script and are not yet automated in the repo.

| Check | Expected | Result |
| --- | --- | --- |
| Asha and Ben log in with correct passwords | 200 with token | Pass |
| Wrong password | 401 | Pass |
| Unknown email | 401, same message as wrong password | Pass |
| Asha requests her order 1043 | 200 | Pass |
| Asha requests Ben's order 2001 | 404 | Pass |
| Ben requests his order 2001 | 200 | Pass |
| Ben requests Asha's order 1043 | 404 | Pass |
| `GET /orders` with no token | 401 | Pass |
| `GET /orders` with an invalid token | 401 | Pass |
| `POST /chat` with no token | 401 | Pass |
| `POST /chat` with an invalid token | 401 | Pass |

## Design choices

- **Same path as the evals.** `/chat` passes the customer ID through the run configuration, exactly as the eval runner does, so the run 004 results describe the real API.
- **No separate error for unknown emails.** A wrong password and an unknown email return the same message, and an unknown email still runs a password hash, so neither the response nor its timing reveals which emails have accounts.
- **Fixed signing algorithm.** The server only accepts HS256, so a token cannot choose a weaker algorithm or none.
- **Recursion limit shared.** `/chat` and the evals used 5 graph steps and the terminal used 10. All three now use one value of 10.

## Limits

- A token stays valid until it expires, even if the account is deleted or the password changes. There are no refresh tokens or revocation.
- These API checks are not yet part of an automated test suite.
- The agent eval suite was not rerun, because the agent's path did not change apart from the recursion limit.
- Each `/chat` request starts a new conversation. There is no memory between messages.

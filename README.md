# abhimart support agent

A customer support agent for an e-commerce store, built with LangGraph, Gemini, FastAPI and Postgres. All data is synthetic.

The model interprets requests and explains outcomes. Code decides the facts and which actions can run.

## Current state

The agent can look up an order by number through a single tool, using the same service layer as the API.

Each agent run can be traced in LangSmith, showing every model call, tool call, token count and timing.

Customers log in with an email and password and receive a JWT. `POST /chat` and `GET /orders/{id}` require it and only return orders belonging to that customer. The ownership check is enforced in the database query, and the model cannot supply or change the customer. See the [ownership results](docs/agent-runs/004-ownership-check.md) and the [login checks](docs/agent-runs/005-jwt-login.md).

**Known limits:** each chat message starts a new conversation, and tokens cannot be revoked before they expire.

See the [current architecture](docs/architecture.md).

## How it has evolved

| Run | Layer | Problem found | Change | Result |
| --- | --- | --- | --- | --- |
| [001](docs/agent-runs/001-first-agent.md) | Tools and identity | The agent can read any customer's order | Found here, fixed in run 004 | 1 of 3 manual requests exposed another customer's address |
| [002](docs/agent-runs/002-baseline-evals.md) | Evaluation | No repeatable way to measure behavior | Added a 10-case eval suite with code-based checks | Baseline: normal requests 12/12, data protection 0/8 |
| [003](docs/agent-runs/003-before-login-baseline.md) | Evaluation | Tests could not say who was asking, so a fix that blocked everyone would have passed | Each case acts as a specific customer, with owner and anonymous cases added | Baseline before login: owner access 6/6, data protection 0/12 |
| [004](docs/agent-runs/004-ownership-check.md) | Tools and identity | Any customer could read any order | Ownership enforced in the query, with identity hidden from the model | Data protection 0/12 to 12/12, owner access stayed 6/6 |
| [005](docs/agent-runs/005-jwt-login.md) | API and auth | The API had no login, so `/chat` had no customer and `/orders` returned any order | JWT login, with both routes passing the token's customer to the ownership check | 11/11 API checks passed, including 404 for other customers' orders and 401 without a valid token |

## Run it

Requires Docker, uv and a Gemini API key.

    cp .env.example .env
    docker compose up -d --wait
    uv run alembic upgrade head
    uv run python -m app.seed
    uv run python -W ignore -m app.agent "Where is my order 1043?" 1001

To use the API, start it with `uv run fastapi dev app/main.py`, open http://127.0.0.1:8000/docs, click **Authorize** and log in as `asha@example.com` with password `asha-dev-pass`. These are sample accounts from the seed script.

See [docs/commands.md](docs/commands.md) for every command and what it does.

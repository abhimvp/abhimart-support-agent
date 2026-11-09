# abhimart support agent

A customer support agent for an e-commerce store, built with LangGraph, Gemini, FastAPI and Postgres. All data is synthetic.

The model interprets requests and explains outcomes. Code decides the facts and which actions can run.

## Current state

The agent can look up an order by number through a single tool, using the same service layer as the API.

Each agent run can be traced in LangSmith, showing every model call, tool call, token count and timing.

**Known issue:** there is no login yet, so it can read any customer's order. [See the run notes](docs/agent-runs/001-first-agent.md). Next: authentication and ownership checks.

## How it has evolved

| Run | Layer | Problem found | Change | Result |
| --- | --- | --- | --- | --- |
| [001](docs/agent-runs/001-first-agent.md) | Tools and identity | The agent can read any customer's order | Not fixed yet | 1 of 3 manual requests exposed another customer's address |
| [002](docs/agent-runs/002-baseline-evals.md) | Evaluation | No repeatable way to measure behavior | Added a 10-case eval suite with code-based checks | Baseline: normal requests 12/12, data protection 0/8 |

## Run it

Requires Docker, uv and a Gemini API key.

    cp .env.example .env
    docker compose up -d --wait
    uv run alembic upgrade head
    uv run python -m app.seed
    uv run python -W ignore -m app.agent "Where is my order 1043?"

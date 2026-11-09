# abhimart support agent

A customer support agent for an e-commerce store, built with LangGraph, Gemini, FastAPI and Postgres. All data is synthetic.

The model interprets requests and explains outcomes. Code decides the facts and which actions can run.

## Current state

The agent can look up an order by number through a single tool, using the same service layer as the API.

**Known issue:** there is no login yet, so it can read any customer's order. [See the run notes](docs/agent-runs/001-first-agent.md). Next: authentication and ownership checks.

## Run it

Requires Docker, uv and a Gemini API key.

    cp .env.example .env
    docker compose up -d --wait
    uv run alembic upgrade head
    uv run python -m app.seed
    uv run python -W ignore -m app.agent "Where is my order 1043?"

# Commands

Run these from the project root.

## First-time setup

| Command | Purpose |
| --- | --- |
| `cp .env.example .env` | Create your local settings file, then add your keys to it |
| `uv sync` | Install the exact package versions from `uv.lock` |
| `docker compose up -d --wait` | Start Postgres and wait until it is healthy |
| `uv run alembic upgrade head` | Create the tables by applying all migrations |
| `uv run python -m app.seed` | Add sample customers, products and orders. Safe to run again |

## Run the app

| Command | Purpose |
| --- | --- |
| `uv run fastapi dev app/main.py` | Start the API with auto-reload on http://127.0.0.1:8000 |
| `uv run python -W ignore -m app.agent "Where is my order 1043?" 1001` | Ask the agent one question as customer 1001. Leave off the ID to act as a user who is not logged in |

Useful pages while the API is running:

| URL | Purpose |
| --- | --- |
| http://127.0.0.1:8000/docs | Interactive API documentation |
| http://127.0.0.1:8000/health | Liveness: is the app running? |
| http://127.0.0.1:8000/health/ready | Readiness: can the app reach the database? |

## Logging in

`/chat` and `/orders` need a login token. In http://127.0.0.1:8000/docs, click **Authorize** and use one of the sample accounts created by `app.seed`:

| Customer | Email | Password |
| --- | --- | --- |
| 1001 Asha Rao | `asha@example.com` | `asha-dev-pass` |
| 1002 Ben Carter | `ben@example.com` | `ben-dev-pass` |

To create a value for `JWT_SECRET` in `.env`:

| Command | Purpose |
| --- | --- |
| `uv run python -c "import secrets; print(secrets.token_hex(32))"` | Generate a random secret for signing login tokens |

## Evals

| Command | Purpose |
| --- | --- |
| `uv run python -W ignore -m evals.run` | Run all cases and print results in the terminal |
| `uv run python -W ignore -m evals.langsmith_eval` | Run all cases and save an experiment in LangSmith |

`-W ignore` hides harmless warnings from Google's library.

## Database

| Command | Purpose |
| --- | --- |
| `docker compose stop` | Stop Postgres and keep its data |
| `docker compose logs -f db` | Follow the Postgres logs |
| `docker compose exec db psql -U abhimart -d abhimart -c "\dt"` | List the tables |

## Migrations

| Command | Purpose |
| --- | --- |
| `uv run alembic revision --autogenerate -m "describe the change"` | Write a draft migration from model changes. Read it before applying |
| `uv run alembic upgrade head` | Apply all migrations not yet applied |
| `uv run alembic downgrade -1` | Undo the most recent migration |
| `uv run alembic current` | Show which migration the database is on |

## Packages

| Command | Purpose |
| --- | --- |
| `uv add <package>` | Add a dependency and update `pyproject.toml` and `uv.lock` |

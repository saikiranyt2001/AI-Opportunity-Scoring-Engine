# AI Opportunity Scoring Engine

An async AI-powered backend pipeline that analyzes product opportunities using multi-model scoring and delivers results via API.

## Key Features

- Async AI orchestration using FastAPI
- Shadow model architecture with non-blocking execution
- APScheduler-based pipeline automation
- SQLAlchemy async ORM with PostgreSQL-ready setup
- Failure-safe design where partial AI failures do not break the pipeline
- REST API for real-time scoring

## Architecture Highlights

- Primary model generates final score
- Shadow models run in parallel using asyncio.gather
- Shadow failures are isolated and never affect final output
- Fully async pipeline from ingestion to scoring to API response

## Tech Stack

- FastAPI
- SQLAlchemy async
- PostgreSQL
- APScheduler
- httpx
- pytest

## Example API

Endpoint:

GET /score/phone-stand

Example response:

{
  "product": "phone-stand",
  "score": 85,
  "shadow_models": [
    {"model": "openai", "score": 80},
    {"model": "anthropic", "score": 75}
  ]
}

## Testing

- Async pytest suite with failure-focused scenarios
- Covers shadow model success and failure handling
- Covers pipeline execution stability
- Covers API endpoint behavior
- Covers async SQLite persistence integration

Run tests:

python -m pytest -q

## Continuous Integration

GitHub Actions workflow is configured in [.github/workflows/ci.yml](.github/workflows/ci.yml).

It runs automatically on push and pull requests to verify:

- Dependency installation
- Full pytest suite

This keeps the project at zero test failures before deployment.

## Docker Deployment

Container files included:

- [Dockerfile](Dockerfile)
- [docker-compose.yml](docker-compose.yml)
- [.dockerignore](.dockerignore)

One-command local container run:

docker compose up --build

Then open:

- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Deployment on Railway

Step 1: Prepare project

- Ensure dependencies are listed in [requirements.txt](requirements.txt)
- Procfile is included at [Procfile](Procfile)
- Recommended start command:

web: uvicorn app.main:app --host 0.0.0.0 --port $PORT

Step 2: Push to GitHub

git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin <YOUR_REPO_URL>
git push -u origin main

Step 3: Deploy on Railway

- Create a new Railway project
- Choose deploy from GitHub
- Select this repository

Step 4: Add services

- Add PostgreSQL
- Optionally add Redis

Step 5: Configure environment variables in Railway

- DATABASE_URL=postgresql+asyncpg://...
- OPENAI_API_KEY=...
- ANTHROPIC_API_KEY=...

Step 6: Run migrations

alembic upgrade head

Step 7: Verify deployment

- Open deployed URL
- Test /score/test-product

## One-Command Local Demo (Windows)

Run:

./scripts/bootstrap_and_run.ps1

This creates the virtual environment if needed, installs dependencies, runs tests, and starts the API.

## Author

Sai Kiran

## Proposal Line

Built a similar async AI scoring pipeline with shadow model orchestration, APScheduler jobs, and full pytest coverage including failure scenarios.

## Proposal Template

Use [PROPOSAL_TEMPLATE.md](PROPOSAL_TEMPLATE.md) as a ready-to-send client pitch and customize the first line for each job post.

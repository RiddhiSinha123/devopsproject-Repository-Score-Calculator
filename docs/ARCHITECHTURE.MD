# Architecture Overview

## 1. System Components

1. FastAPI Web API (`src/main.py`)
   - Exposes endpoints:
     - `GET /health` (liveness check)
     - `POST /scan` (repository scorecard computation)
   - Performs request authentication via `x-api-key` header or Basic Auth (configurable)
   - Loads environment settings from `.env` and runtime environment variables (`INTERNAL_API_KEY`, `GITHUB_TOKEN`, etc.)

2. Scoring Business Logic (`src/logic.py`)
   - Computes `Scorecard` model (via `pydantic`) including metrics and grade
   - Metrics include community, activity, CI/CD, docs/quality, and security signals
   - Returns structured JSON response to API layer

3. Data Source (GitHub API)
   - Uses `httpx.AsyncClient` to call:
     - `GET /repos/{owner}/{repo}`
     - `GET /repos/{owner}/{repo}/contributors`
     - `GET /repos/{owner}/{repo}/commits`
     - `GET /repos/{owner}/{repo}/actions/runs`
   - The app has no other external dependencies besides standard runtime and Docker infrastructure.

4. Containerization (`infrastructure/Dockerfile`, `infrastructure/docker-compose.yml`)
   - Docker container includes healthcheck and automatic restart policy
   - `PYTHONPATH=/app` in container to allow `src.*` imports

5. CI/CD (`.github/workflows`)
   - Runs tests, linting, build, and deployment pipelines
   - Uses repository secrets for environment values in pipelines

## 2. Logic Flow

1. **API request**: client calls `POST /scan` with JSON payload:
```json
{
  "owner": "microsoft",
  "repo": "vscode"
}
```
 and authorization header.

#### Sample input JSON (expanded)
```json
{
  "repo_data": {
    "full_name": "RiddhiSinha123/DSA",
    "stargazers_count": 150,
    "open_issues_count": 10,
    "license": {
      "key": "mit",
      "name": "MIT License"
    }
  },
  "contributors": [
    {
      "login": "RiddhiSinha123",
      "contributions": 100
    },
    {
      "login": "dev-peer",
      "contributions": 50
    },
    {
      "login": "bot-account",
      "contributions": 10
    }
  ],
  "commits": [
    { "sha": "sha_0" }, { "sha": "sha_1" }, { "sha": "sha_2" }, { "sha": "sha_3" },
    { "sha": "sha_4" }, { "sha": "sha_5" }, { "sha": "sha_6" }, { "sha": "sha_7" },
    { "sha": "sha_8" }, { "sha": "sha_9" }, { "sha": "sha_10" }, { "sha": "sha_11" },
    { "sha": "sha_12" }, { "sha": "sha_13" }, { "sha": "sha_14" }, { "sha": "sha_15" },
    { "sha": "sha_16" }, { "sha": "sha_17" }, { "sha": "sha_18" }, { "sha": "sha_19" },
    { "sha": "sha_20" }, { "sha": "sha_21" }, { "sha": "sha_22" }, { "sha": "sha_23" },
    { "sha": "sha_24" }
  ],
  "ci_runs": [
    { "conclusion": "success" },
    { "conclusion": "success" },
    { "conclusion": "failure" },
    { "conclusion": "success" }
  ]
}
```

2. **Auth verification**: API validates `x-api-key` or Basic Auth credentials against environment configuration.
3. **GitHub data fetch**: API requests repository metadata, contributors, commits, and workflow runs.
4. **Score calculation**: `calculate_scorecard(...)` evaluates fetched data and builds a `Scorecard` model:
   - `repo_name`
   - `total_score`
   - `grade` (A/B/C/D/F)
   - `metrics` list with individual scores and feedback.
5. **Response**: API returns JSON response the same as the pydantic `Scorecard` model.

### Example `Scorecard` JSON output
```json
{
  "repo_name": "microsoft/vscode",
  "total_score": 85,
  "grade": "A",
  "metrics": [
    {"name": "community", "score": 22, "max_score": 25, "status": "good", "feedback": "Strong community engagement"},
    {"name": "activity", "score": 20, "max_score": 25, "status": "good", "feedback": "Frequent commits"},
    {"name": "cicd", "score": 18, "max_score": 20, "status": "excellent", "feedback": "Stable workflows"},
    {"name": "quality", "score": 13, "max_score": 15, "status": "good", "feedback": "Well documented"},
    {"name": "security", "score": 12, "max_score": 15, "status": "good", "feedback": "Secure baseline"}
  ]
}
```

## 3. Impact

- **Improved visibility**: Streamlined auditing of repository health across multiple teams.
- **Data-driven decisions**: Objective scoring enables prioritization of remediation work.
- **Scalable process**: Containerized API and CI/CD integration supports rapid rollout.
- **Security hardening**: Auth checks reduce unauthorized access, GitHub token usage avoids API throttling.
- **Operational monitoring**: Health endpoints + Docker healthcheck support automated platform monitoring.

## 4. Optional Enhancements

- Add caching layer (Redis) for GitHub API responses to improve request performance and rate limits.
- Add a metrics dashboard (Grafana/Prometheus) for historical repository score trends.
- Add role-based auth and policies for enterprise usage.

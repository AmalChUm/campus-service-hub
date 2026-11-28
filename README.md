# Campus Service Hub — SWE 325 Individual Starter

This public repository is the official starter code for the SWE 325 Campus Service Hub project. Every student completes the work individually in a fork. The repository includes a working baseline application, Docker configuration, and GitHub Actions examples so students can inspect, test, and extend a real delivery workflow.

## Assignment and links

- [Complete assignment document](SWE325-Campus-Service-Hub-Git-Docker-CICD-Project-Individual.docx)
- [Individual task catalog](TASK-CATALOG.md)
- [GitHub Actions](https://github.com/AmalChUm/campus-service-hub/actions)
- [CI workflow](.github/workflows/ci.yml)
- [CD workflow](.github/workflows/cd.yml)
- [Dockerfile](Dockerfile)
- [Docker ignore rules](.dockerignore)
- [Application](app.py)
- [Tests](tests/test_services.py)

The repository’s Issues tab is optional. Do not wait for a shared issue or claim work from another student. Record the task ID from `TASK-CATALOG.md` in an issue in your own fork, or in your report if Issues are disabled.

## Prerequisites

- A GitHub account with permission to fork repositories, create branches, and run GitHub Actions.
- Git installed and available in a terminal.
- Python 3.12 or a compatible recent Python version.
- Docker installed. On Windows, start Docker Desktop and wait until the engine reports that it is running before using `docker build` or `docker run`.
- Access to the Maizey workspace required by the assignment.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python app.py
```

Then visit `http://localhost:5000/health` and `http://localhost:5000/services`.

## API Examples

All documented API endpoints use the HTTP GET method to retrieve information from the application.

The Campus Service Hub provides REST API endpoints that return JSON responses. Start the application before running these commands in a separate terminal.

The default port is 5000. If port 5000 is already in use on macOS, start the application with `PORT=5001 python app.py` and use port 5001 instead.

### Health Check

Check whether the application is running.

```bash
curl http://localhost:5000/health
```

Example response:

```json
{"status": "ok"}
```

### List All Services

Retrieve all available campus services.

```bash
curl http://localhost:5000/services
```

Returns a JSON array containing all five campus services.

Example response:

```json
[
  {
    "id": "library",
    "name": "University Library",
    "category": "academic",
    "location": "Main Campus",
    "hours": "08:00-22:00"
  },
  {
    "id": "advising",
    "name": "Academic Advising",
    "category": "academic",
    "location": "Student Services Building",
    "hours": "09:00-17:00"
  },
  {
    "id": "tutoring",
    "name": "Peer Tutoring Center",
    "category": "academic",
    "location": "Learning Commons",
    "hours": "10:00-20:00"
  },
  {
    "id": "health",
    "name": "Campus Health Services",
    "category": "health",
    "location": "Wellness Center",
    "hours": "08:00-17:00"
  },
  {
    "id": "it-support",
    "name": "Information Technology Support",
    "category": "technical",
    "location": "Technology Center",
    "hours": "08:00-18:00"
  }
]
```

### Service Count

Retrieve the total number of services.

```bash
curl http://localhost:5000/services/count
```

Example response:

```json
{"count": 5}
```

### Find a Service by ID

Retrieve information about a specific service.

```bash
curl http://localhost:5000/services/library
```

Example response:

```json
{
  "id": "library",
  "name": "University Library",
  "category": "academic",
  "location": "Main Campus",
  "hours": "08:00-22:00"
}
```

### Filter by Category

```bash
curl "http://localhost:5000/services?category=academic"
```

Returns the University Library, Academic Advising, and Peer Tutoring Center.

Example response:

```json
[
  {
    "id": "library",
    "name": "University Library",
    "category": "academic",
    "location": "Main Campus",
    "hours": "08:00-22:00"
  },
  {
    "id": "advising",
    "name": "Academic Advising",
    "category": "academic",
    "location": "Student Services Building",
    "hours": "09:00-17:00"
  },
  {
    "id": "tutoring",
    "name": "Peer Tutoring Center",
    "category": "academic",
    "location": "Learning Commons",
    "hours": "10:00-20:00"
  }
]
```

### Search by Name or ID

```bash
curl "http://localhost:5000/services?search=library"
```

Returns a JSON array containing the University Library record.

Example response:

```json
[
  {
    "id": "library",
    "name": "University Library",
    "category": "academic",
    "location": "Main Campus",
    "hours": "08:00-22:00"
  }
]
```

### Invalid Service ID

```bash
curl -i http://localhost:5000/services/invalid
```

Expected HTTP status: 404 Not Found.

Example response:

```json
{"error": "service not found", "id": "invalid"}
```

## Run with Docker

```bash
docker build -t campus-service-hub:local .
docker run --rm --name campus-service -p 5000:5000 campus-service-hub:local
```

In another terminal:

```bash
curl --fail http://localhost:5000/health
curl --fail http://localhost:5000/services
```

If Windows reports an error such as `open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified`, open Docker Desktop, wait for the engine to finish starting, and retry. The host port is the first `5000`; the container port is the second `5000`.

## Baseline delivery configuration

The starter already contains a root-level `Dockerfile`, `.dockerignore`, and working `.github/workflows/ci.yml` and `.github/workflows/cd.yml` files. Students should inspect and explain these files. Do not recreate them merely to manufacture a commit. Select `CI-01`, `DOC-01`, or another task from the catalog if you need a delivery-focused contribution.

The CI workflow runs Python tests and a Docker smoke test on pushes, pull requests into `main`, and manual dispatches. The CD workflow publishes approved `main` images to GitHub Container Registry. Image names must be lowercase; the workflow derives the lowercase repository owner automatically.

The required instructor-image verification is:

```bash
docker pull ghcr.io/amalchum/campus-service-hub:latest
docker run --rm -p 5000:5000 ghcr.io/amalchum/campus-service-hub:latest
```

Student-owned GHCR publication is optional unless explicitly enabled by the course environment. A fork does not automatically have permission to publish to the instructor’s package namespace.

## Individual contribution workflow

1. Fork this repository into your own GitHub account.
2. Clone your fork and configure `origin` and `upstream`.
3. Choose one verified task from [`TASK-CATALOG.md`](TASK-CATALOG.md), or propose an equivalent task with explicit acceptance criteria.
4. Record the task ID in an issue in your own fork if Issues are enabled; otherwise record it in your report. No shared issue claiming is required.
5. Create a branch: `feature/<task-id>-<short-description>`.
6. Run the baseline tests before changing files.
7. Make one focused change and add or update tests or a reproducible verification checklist.
8. Bring the branch current before pushing:

```bash
git switch main
git fetch upstream
git pull --rebase upstream main
git switch feature/<task-id>-<short-description>
git rebase main
git push --force-with-lease -u origin HEAD
```

Use `--force-with-lease` only when a rebase changed the branch history. If you have not rebased after the previous push, a normal `git push` is sufficient.

9. Before opening a PR, run:

```bash
git status
git diff --stat main...HEAD
pytest -q
```

The diff must be non-empty and must implement the selected task. A branch with no commits or no changes cannot produce a comparison pull request; GitHub will report “There isn’t anything to compare.”

10. Open a pull request from your fork’s feature branch to the instructor repository’s `main` branch, explain the task and acceptance criteria, list tests/evidence, and do not merge your own PR.
11. Inspect the PR Checks tab. Use Maizey only with redacted, non-sensitive workflow information, and record the interaction in the experiment log.
12. Use Maizey to summarize any review feedback, decide what to accept, verify changes locally, update the same branch when appropriate, and post a concise verified response.

## Evidence checklist

Record the following in the final report:

- Fork URL, `git remote -v`, task ID, branch name, commit hash, and PR URL.
- Baseline and final test results.
- Changed files and acceptance-criteria evidence.
- Docker build, run, endpoint, and stop evidence.
- CI workflow jobs and passing PR checks.
- CD/instructor-image evidence, or an explanation that student GHCR publication was not enabled.
- Maizey prompts or faithful summaries, decisions, and independent verification.

Do not commit secrets, access tokens, private keys, or private personal data.

## Maizey experiment forms

Complete the forms using the same participant code throughout the experiment:

- [Pre-Task Survey](https://docs.google.com/forms/d/e/1FAIpQLSdWZImoDXORRwDT-dKlMaPAKnalw7vpyxzE-E6gk6fK0LzEVg/viewform) — complete before starting the task.
- [Maizey Interaction Log](https://docs.google.com/forms/d/e/1FAIpQLSdHC2RZ9aZVcVenQJxNK8N-3euyvl9_cJYb7dP0P4ktlT_qOg/viewform) — submit one entry after each meaningful Maizey interaction; multiple submissions are expected.
- [Post-Task Survey](https://docs.google.com/forms/d/e/1FAIpQLSc3Ii1uSbJlYU-8Qqxf2FvwHPakrL0X6U5ylPeY-VjbIVaNkg/viewform) — complete after finishing the task and evidence.

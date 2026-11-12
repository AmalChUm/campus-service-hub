# Campus Service Hub — SWE 325 Individual Starter

This public repository is the official starter code for the SWE 325 Campus Service Hub project. Every student completes the work individually in a fork and must submit their own issue, branch, commits, pull request, tests, Docker evidence, and GitHub Actions evidence.

## Assignment and links

- [Complete assignment document](SWE325-Campus-Service-Hub-Git-Docker-CICD-Project.docx)
- [Issues](https://github.com/AmalChUm/campus-service-hub/issues)
- [Actions](https://github.com/AmalChUm/campus-service-hub/actions)
- [CI workflow](.github/workflows/ci.yml)
- [CD workflow](.github/workflows/cd.yml)
- [Dockerfile](Dockerfile)
- [Application](app.py)
- [Tests](tests/test_services.py)

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

## Run with Docker

```bash
docker build -t campus-service-hub .
docker run --rm -p 5000:5000 campus-service-hub
curl --fail http://localhost:5000/health
```

The CI workflow runs Python tests and a Docker smoke test. The CD workflow publishes approved `main` images to GitHub Container Registry as `ghcr.io/amalchum/campus-service-hub`.

## Individual contribution rules

1. Fork this repository into your own GitHub account.
2. Claim one unclaimed issue and comment with your name and username.
3. Create a feature branch for that issue.
4. Make a meaningful change and add or update tests.
5. Push the branch to your fork and open a pull request.
6. Capture your own test, Docker, workflow, and pull-request evidence.

Do not commit secrets, access tokens, private keys, or private personal data.

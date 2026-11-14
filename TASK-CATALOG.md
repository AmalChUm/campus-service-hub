# Individual Task Catalog

Choose **one** task before coding. These tasks are designed for individual work and were checked against the current starter repository. Do not claim a shared class issue and do not comment with your name to reserve a task.

Create an issue in your own fork titled with the task ID, or record the selected task in your report if Issues are disabled. The issue is an individual task record, not a shared ownership mechanism.

## Application tasks

### APP-01 — Optional service sorting

**Goal:** Extend `GET /services` with an optional `sort` query parameter.

**Acceptance criteria:**

- `GET /services?sort=name` returns all service records sorted by the `name` field in ascending, case-insensitive order.
- `GET /services?sort=-name` returns all service records sorted by the `name` field in descending, case-insensitive order.
- The existing `category` and `search` filters continue to work with sorting.
- An unsupported sort value returns HTTP 400 with JSON containing an `error` field.
- Add tests for ascending order, descending order, filter-plus-sort behavior, and invalid input.

**Likely files:** `app.py`, `tests/test_services.py`.

### APP-02 — Service-hours endpoint

**Goal:** Add `GET /services/<service_id>/hours`.

**Acceptance criteria:**

- An existing service returns HTTP 200 and JSON with `id`, `name`, and `hours`.
- An unknown service returns HTTP 404 with the repository’s normal JSON error shape.
- Add tests for one valid service and one unknown service.
- Existing endpoints and tests continue to pass.

**Likely files:** `app.py`, `tests/test_services.py`.

### APP-03 — Input validation for search and category

**Goal:** Make invalid or empty filter values explicit and testable.

**Acceptance criteria:**

- Whitespace-only `search` and `category` values are handled consistently and documented.
- Add a documented maximum length for filter values; values exceeding it return HTTP 400 with JSON containing an `error` field.
- Normal case-insensitive filtering continues to work.
- Add tests for whitespace, the maximum-length boundary, and an over-limit value.

**Likely files:** `app.py`, `tests/test_services.py`, `README.md`.

## Delivery and documentation tasks

### DOC-01 — Improve the local and Docker troubleshooting guide

**Acceptance criteria:**

- README documents virtual-environment activation for Windows PowerShell and macOS/Linux.
- README explains that Windows users must start Docker Desktop and wait for the engine to be running.
- README includes the Docker connection-error symptom and remedy.
- README documents `/health`, `/services`, and the port mapping.
- Add a small documentation test or a reproducible command checklist in the PR description.

### CI-01 — Add a defined CI quality check

**Acceptance criteria:**

- Preserve the existing Python-test and Docker-smoke-test jobs.
- Add one clearly named, independently useful check, such as a Python syntax compilation step or a workflow validation/documentation check.
- The new check runs on pull requests to `main`.
- Explain the check in the README or PR description and verify it passes in GitHub Actions.

### DOC-02 — Improve the contribution evidence checklist

**Acceptance criteria:**

- Update the README with a concise evidence checklist covering baseline tests, changed files, branch, commit, PR, CI checks, Docker smoke test, and Maizey interaction log.
- Remove stale shared-issue language.
- Keep the checklist consistent with the assignment document.

## Task-selection rules

1. Select one task and record its ID before coding.
2. Read the acceptance criteria and turn them into tests or a verification checklist.
3. Create a branch named `feature/<task-id>-<short-description>`.
4. Make a focused change; do not rewrite unrelated files.
5. Before opening a PR, confirm that `git diff --stat main...HEAD` is non-empty and that the relevant tests or verification pass.
6. If a task is already implemented in your fork, do not force a meaningless diff. Select another verified task or propose a new task with equivalent acceptance criteria.

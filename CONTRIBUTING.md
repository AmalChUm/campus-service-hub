# Individual contribution workflow

Students work independently from their own fork. Choose one verified task from `TASK-CATALOG.md` and record the task ID in an issue in your fork, or in your report if Issues are disabled. No shared issue claiming or class-wide ownership comments are required.

Create a focused feature branch named `feature/<task-id>-<short-description>`. Run the baseline tests, implement the acceptance criteria, add or update tests, and confirm that the branch contains a meaningful diff before opening a pull request.

The CD workflow publishes images only from `main`. Do not edit the CD workflow to publish unreviewed feature-branch code. Student-owned GHCR publication is optional unless the course environment explicitly enables it.

# Contributing to MediSearch

Thank you for improving MediSearch. This repository contains a full-stack pharmacy intelligence application and a data engineering platform, so every contribution should preserve both application correctness and data lineage.

## Workflow

1. Create a branch with a descriptive name such as `feature/search-filters` or `docs/pipeline-runbook`.
2. Keep changes scoped to one feature, fix, or documentation improvement.
3. Update folder-level `README.md` files when adding, moving, or removing folders.
4. Run the relevant frontend, backend, and pipeline checks before opening a pull request.
5. Document new environment variables in `.env.example` and deployment documentation.

## Code Standards

- Use TypeScript conventions for frontend and backend code.
- Keep backend modules organized as routes, controllers, services, and repositories.
- Keep data pipeline code idempotent, observable, and safe to rerun.
- Avoid committing generated artifacts, local caches, credentials, or temporary exports.

## Pull Request Expectations

Every pull request should include:

- A clear summary of the change.
- Tests or checks that were run.
- Data model or API contract changes, if any.
- Migration, rollback, or operational notes for production-impacting changes.

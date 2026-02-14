# Git Workflow & Collaboration Standard

This project follows a **trunk-oriented GitFlow hybrid** optimized for a small product team and fast iteration with strong quality gates.

## 1) Branching Strategy

- `main`
  - Production-ready branch
  - Protected: no direct pushes
  - Tagged releases only
- `develop`
  - Integration branch for upcoming release
  - Feature branches merge here first
- `feature/*`
  - Short-lived branches for scoped work
  - Naming: `feature/<area>-<short-description>`
  - Example: `feature/ingestion-pharmacy-price-adapter`
- `hotfix/*`
  - Urgent production fixes branched from `main`
- `release/*`
  - Optional stabilization branch before promoting `develop` to `main`

## 2) Creating a New Branch

1. Update local refs:
   ```bash
   git checkout develop
   git pull origin develop
   ```
2. Create branch:
   ```bash
   git checkout -b feature/<area>-<description>
   ```
3. Keep commits small, coherent, and test-backed.

## 3) Pull Request Rules

Every PR must:

- Target `develop` (or `main` for hotfixes)
- Include problem statement + solution summary
- Reference issue/task ID
- Include testing evidence (unit/integration/data quality)
- Include migration/backfill notes when schema changes
- Pass CI checks before merge

PRs should remain focused. Prefer multiple small PRs over one large mixed PR.

## 4) Code Review Process

- Minimum **1 reviewer approval** for normal PRs; **2 approvals** for schema-critical changes
- Required review checklist:
  - Correctness and edge cases
  - Data contract compatibility
  - Performance and cost implications
  - Security/privacy considerations (healthcare context)
  - Observability (logs, metrics, error handling)
- Reviewer may request additional tests for critical paths

## 5) Commit Message Format

Use Conventional Commits:

```text
<type>(optional-scope): <short summary>
```

Common types:

- `feat`: new feature
- `fix`: bug fix
- `refactor`: code restructuring without behavior change
- `docs`: documentation changes
- `test`: tests added/updated
- `chore`: build/config/tooling updates

Examples:

- `feat(ingestion): add pharmacy stock API connector`
- `fix(transform): handle null active_ingredient values`
- `docs(architecture): add bronze-silver-gold flow details`

## 6) Versioning Strategy

We follow **Semantic Versioning** (`MAJOR.MINOR.PATCH`).

- `MAJOR`: breaking API/data contract changes
- `MINOR`: backward-compatible feature additions
- `PATCH`: backward-compatible bug fixes

Release flow:

1. Merge features into `develop`
2. Create `release/x.y.z`
3. Run stabilization/testing
4. Merge into `main` and tag `vX.Y.Z`
5. Back-merge into `develop`

## 7) Merge Policy

- Use **Squash merge** for feature PRs to keep history readable
- Use **Merge commit** for release/hotfix branches when traceability is needed
- Delete feature branch after merge

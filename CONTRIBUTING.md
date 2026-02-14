# Contributing Guide

Thank you for contributing to the Medical & Pharmacy Intelligence System.

## Principles

- Keep changes scoped and testable
- Preserve data contracts unless explicitly versioned
- Prefer reproducibility over one-off scripts
- Document behavior changes in `docs/`

## Development Workflow

1. Create a feature branch from `develop`
2. Implement changes with tests
3. Run formatting/linting/tests locally
4. Open PR using the provided template
5. Address review feedback and merge after approvals

## Required Checks Before PR

- Unit/integration tests pass
- Data-quality checks updated for schema logic
- Documentation updated (if behavior or architecture changes)

## Security & Data Governance

- Never commit secrets
- Avoid storing sensitive PII in repository datasets
- Use environment variables and secret managers

# Deployment Guide

## Environments

- `dev`: feature testing and integration
- `staging`: production-like validation
- `prod`: live workloads and SLAs

## Deployment Strategy

- Infrastructure via Terraform in `infra/terraform`
- Containerized services with Docker definitions in `infra/docker`
- CI/CD pipelines in `.github/workflows`

## Deployment Steps (Baseline)

1. Run CI checks (lint, test, security)
2. Build tagged Docker images
3. Apply Terraform plan (staging -> prod)
4. Deploy orchestration and service components
5. Run smoke tests and health checks

## Operational Readiness

- Rollback strategy documented for each service
- Database migrations are backward-compatible by default
- Monitoring dashboards and alert routing must be active prior to prod release

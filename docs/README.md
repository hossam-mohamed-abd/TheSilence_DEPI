# Project Documentation

## Overview

This directory is the central documentation hub for the MediSearch medical and pharmacy intelligence platform. It covers requirements, architecture, frontend, backend, APIs, databases, data engineering, deployment, security, operations, testing, releases, reports, presentations, and references.

## Purpose

The documentation is intended to help new developers, reviewers, data engineers, QA engineers, DevOps maintainers, and stakeholders understand, build, validate, deploy, operate, and extend the project without relying on undocumented tribal knowledge.

## Contents

| Folder | Purpose |
| --- | --- |
| `ai/` | AI assistant and recommendation-engine documentation. |
| `api/` | API overview and endpoint reference. |
| `architecture/` | System, API, AI, deployment, infrastructure, pipeline, and warehouse architecture explanations. |
| `backend/` | Express/TypeScript backend structure and request lifecycle. |
| `configuration/` | Environment and configuration guidance. |
| `data_engineering/` | Scraping, cleaning, ETL, pipeline, analytics, and warehouse lifecycle documentation. |
| `database/` | Operational database and warehouse references. |
| `deployment/` | Deployment and database configuration guides. |
| `development/` | Local development, coding standards, and contribution workflow. |
| `diagrams/` | Generated architecture, API, frontend, backend, database, infrastructure, pipeline, security, analytics, and warehouse diagrams. |
| `frontend/` | Angular frontend structure, routing, components, services, and state. |
| `integrations/` | Integration contracts between frontend, backend, database, pipelines, warehouse, and deployment services. |
| `operations/` | Monitoring, troubleshooting, backup, and operational runbooks. |
| `presentation/` | Presentation materials and demo notes. |
| `references/` | Team and supporting reference materials. |
| `release/` | Release checklist, changelog template, and release-notes template. |
| `reports/` | Project reports and progress outputs. |
| `security/` | Authentication, authorization, data protection, and hardening guidance. |
| `srs/` | Software requirements, stakeholder information, and feature documents. |
| `testing/` | Test strategy and release verification guidance. |

## Recommended Reading Path

1. Start with `srs/` to understand the requirements and stakeholders.
2. Read `architecture/` to understand the system design.
3. Read `backend/`, `frontend/`, and `api/` for application implementation details.
4. Read `database/` and `data_engineering/` for persistence, ETL, and warehouse behavior.
5. Read `deployment/`, `configuration/`, `security/`, and `operations/` before running production-like environments.
6. Use `testing/` and `release/` for verification and milestone delivery.

## Related Documents

- [Development Guide](development/README.md)
- [API Reference](api/API_REFERENCE.md)
- [Backend Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)
- [Data Lifecycle](data_engineering/PIPELINES_AND_DATA_LIFECYCLE.md)
- [Security Documentation](security/README.md)
- [Operations Guide](operations/README.md)

## Notes

- Preserve existing documentation and add new material to the most specific folder available.
- Do not modify generated Mermaid diagrams unless explicitly requested.
- Keep README files consistent with the structure: Overview, Purpose, Contents, Related Documents, and Notes.
- Update documentation in the same change as code, schema, deployment, or pipeline behavior changes.

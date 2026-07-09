# Security Policy

MediSearch handles healthcare-adjacent search, pharmacy, inventory, and user data. Treat security and privacy issues as high priority.

## Reporting a Vulnerability

Do not open public issues for suspected vulnerabilities. Report security concerns privately to the project maintainers with:

- Affected component or endpoint.
- Reproduction steps.
- Expected and actual impact.
- Suggested mitigation, if known.

## Security Expectations

- Never commit secrets, tokens, database URLs, service keys, or private credentials.
- Store production secrets in the hosting provider or CI/CD secret manager.
- Use least-privilege database accounts for ETL, backend runtime, and analytics workloads.
- Validate and sanitize all external data collected by scrapers before loading it downstream.
- Keep dependencies patched and review authentication, authorization, and CORS changes carefully.

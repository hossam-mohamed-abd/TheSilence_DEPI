# Release Documentation

## Overview

This folder contains release-management templates for MediSearch.

## Purpose

Use these templates to prepare consistent graduation demos, internal milestones, staging releases, and production-ready deployments.

## Contents

- Release checklist
- Changelog template
- Release notes template
- Versioning guidance

## Release Checklist

- [ ] Requirements and scope reviewed.
- [ ] API documentation updated.
- [ ] Frontend and backend builds pass.
- [ ] Database changes reviewed and backed up.
- [ ] ETL changes validated with sample data.
- [ ] Security checklist reviewed.
- [ ] Deployment variables confirmed.
- [ ] Known issues documented.
- [ ] Demo workflow tested end-to-end.

## Changelog Template

```markdown
# Changelog

## [Unreleased]

### Added
- 

### Changed
- 

### Fixed
- 

### Security
- 
```

## Release Notes Template

```markdown
# Release Notes - MediSearch vX.Y.Z

## Summary

Briefly describe the release goal and audience.

## Highlights

- 

## User Impact

- 

## Technical Changes

- Frontend:
- Backend:
- Database:
- Data Engineering:
- Documentation:

## Deployment Notes

- Required environment variables:
- Database actions:
- Rollback plan:

## Known Issues

- 

## Verification

- [ ] Frontend build passed.
- [ ] Backend build passed.
- [ ] API health passed.
- [ ] Authentication flow tested.
- [ ] Search flow tested.
- [ ] Pharmacy details flow tested.
```

## Versioning Guidance

Use semantic versioning when formal releases begin:

- `MAJOR` for incompatible API or database contract changes.
- `MINOR` for backward-compatible features.
- `PATCH` for fixes and documentation updates.

## Related Documents

- [Testing Documentation](../testing/README.md)
- [Deployment Guide](../deployment/README.md)
- [Operations Guide](../operations/README.md)
- [Security Documentation](../security/README.md)

## Notes

Keep release notes factual and tied to implemented behavior. Avoid promising features that are not merged or validated.

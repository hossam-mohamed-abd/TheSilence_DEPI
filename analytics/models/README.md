# analytics/models
## Purpose
Analytics workspace for notebooks, reports, and derived analytical models.
## What belongs here
- Files that directly support this folder's responsibility.
- Documentation, configuration, scripts, assets, or source files scoped to this area.
- Keep unrelated experiments, generated files, and temporary exports out of this folder.
## Major files
- `.gitkeep` — Placeholder used to keep an otherwise empty directory in Git.
## Developer usage
- Add new files only when they match the documented purpose of this folder.
- Prefer small, focused files and update this README when responsibilities change.
- Reference shared contracts, schemas, or environment variables instead of duplicating them.
## Best practices
- Use clear, descriptive names that communicate domain and intent.
- Keep generated artifacts, local caches, secrets, and temporary files out of version control.
- Document assumptions, external dependencies, and operational runbooks near the code or asset they affect.
## Naming conventions
- Use lowercase, kebab-case, or snake_case for folders and data files unless framework conventions require otherwise.
- Use framework-standard suffixes such as `.component.ts`, `.service.ts`, `.routes.ts`, `.controller.ts`, and `.repository.ts` where applicable.
## Future notes
- Review this README during major refactors to keep documentation aligned with the repository structure.

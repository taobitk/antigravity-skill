---
name: code-naming-standards
description: >-
  Enforces consistent file naming conventions for SvelteKit and TypeScript projects
  (PascalCase for Svelte components, camelCase for TS/JS modules and Svelte 5 rune modules).
  Use when creating, renaming, reviewing, or verifying file structure in a SvelteKit/TypeScript codebase.
---

# Code Naming Standards (`code-naming-standards`)

Enforces uniform file naming across SvelteKit and TypeScript codebases and provides an automated verification script.

## Naming Rules

| File Type | Required Convention | Examples |
| :--- | :--- | :--- |
| **Svelte Components** (`*.svelte`) | `PascalCase.svelte` | `ConflictModal.svelte`, `UserCard.svelte` |
| **TS / JS Modules** (`*.ts`, `*.js`) | `camelCase.ts` / `camelCase.js` | `dateUtils.ts`, `authHelper.js` |
| **Svelte 5 Rune Modules** (`*.svelte.ts`, `*.svelte.js`) | `camelCase.svelte.ts` | `cartState.svelte.ts` |
| **SvelteKit Route Files** (`+*`) | Exempt (`+page.svelte`, `+server.ts`, `+layout.svelte`, etc.) | `+page.svelte` |
| **Test Files** | Exempt (`*.spec.ts`, `*.test.ts`, `*.e2e.ts`) | `login.spec.ts` |
| **Framework & Config Files** | Exempt (`index.ts`, `schema.ts`, `*.d.ts`, `app.html`, `layout.css`, `*.config.ts/js`) | `app.d.ts`, `vite.config.ts` |

*(Automatically skips `node_modules` and `.svelte-kit`.)*

## Verification Script

Run [verify_naming_standards.py](./scripts/verify_naming_standards.py) from the project root after creating or renaming files:

```bash
# Scan default ./src directory
python "C:\Users\8hung\.gemini\config\plugins\sveltekit-dev\skills\code-naming-standards/scripts/verify_naming_standards.py"

# Scan a specific directory
python "C:\Users\8hung\.gemini\config\plugins\sveltekit-dev\skills\code-naming-standards/scripts/verify_naming_standards.py" --dir "path/to/src"
```

- **Exit code `0`**: All checked files pass naming standards.
- **Exit code `1`**: Naming violations detected or target directory does not exist.

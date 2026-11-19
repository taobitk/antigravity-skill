---
name: svelte-clean-architecture
description: >-
  Enforces 3-layer Svelte Clean Architecture: keeps +page.svelte orchestrators under 180 lines,
  UI components under 250 lines, and forbids direct fetch() calls inside .svelte files
  (extract data/API logic into *.svelte.ts composables). Use when building, refactoring, or auditing Svelte components.
---

# Svelte Clean Architecture (`svelte-clean-architecture`)

Enforces separation of concerns (SoC) and manageable component sizes in Svelte / SvelteKit applications.

## Architecture Rules

1. **Line Limits**:
   - `+page.svelte`: maximum **180 lines** (`MAX_PAGE_LINES`). Keep route pages as thin orchestrators.
   - Other `*.svelte` UI components: maximum **250 lines** (`MAX_COMPONENT_LINES`). Split large views into focused sub-components.
2. **Separation of Concerns (No Direct `fetch()`)**:
   - `.svelte` files MUST NOT call `fetch(` directly (comment lines starting with `//`, `/*`, `*` are ignored).
   - Extract API calls, state management, and side effects into composables under `src/lib/composables/*.svelte.ts`.

*(Automatically skips `node_modules` and `.svelte-kit`.)*

## Verification Script

Verify compliance using [verify_component_architecture.py](./scripts/verify_component_architecture.py):

```bash
# Scan default ./src directory
python "C:\Users\8hung\.gemini\config\plugins\sveltekit-dev\skills\svelte-clean-architecture/scripts/verify_component_architecture.py"

# Scan a specific directory
python "C:\Users\8hung\.gemini\config\plugins\sveltekit-dev\skills\svelte-clean-architecture/scripts/verify_component_architecture.py" --dir "path/to/src"
```

- **Exit code `0`**: All `.svelte` files satisfy line limits and separation-of-concerns rules.
- **Exit code `1`**: Violations found or target `src/` directory not found.

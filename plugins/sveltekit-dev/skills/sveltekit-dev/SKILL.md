---
name: sveltekit-dev
description: >-
  Unified SvelteKit development router and audit workflow. Use when starting, building,
  refactoring, or auditing a SvelteKit + TypeScript (+ optional Rust WASM) project to route
  to the right bundled skill: scaffolding (sk-sveltekit-starter), 3-layer architecture
  (svelte-clean-architecture), or file naming (code-naming-standards).
---

# SvelteKit Dev Kit (`sveltekit-dev`)

Entrypoint router for the `sveltekit-dev` plugin. Determine the user's goal, load the corresponding bundled skill(s), and run the verification scripts when auditing code.

## Skill Routing Table

| User Intent / Stage | Skill to Load | Purpose |
| :--- | :--- | :--- |
| **Create / scaffold a new SvelteKit project** | [sk-sveltekit-starter](../sk-sveltekit-starter/SKILL.md) | Bootstraps SvelteKit Minimal + TS + Tailwind/shadcn + Cloudflare Adapter + Playwright + optional Rust WASM. |
| **Build or refactor `.svelte` components & routes** | [svelte-clean-architecture](../svelte-clean-architecture/SKILL.md) | Keeps `+page.svelte` <= 180 lines, components <= 250 lines, and moves `fetch()` into `*.svelte.ts` composables. |
| **Create, rename, or review file structure** | [code-naming-standards](../code-naming-standards/SKILL.md) | Enforces `PascalCase.svelte` for components and `camelCase.ts` / `camelCase.svelte.ts` for TS modules. |

## SvelteKit Audit Command

When asked to audit or verify an existing SvelteKit project, run the bundled verification scripts from the project root:

```powershell
python "C:\Users\8hung\.gemini\config\plugins\sveltekit-dev\skills\code-naming-standards\scripts\verify_naming_standards.py"
python "C:\Users\8hung\.gemini\config\plugins\sveltekit-dev\skills\svelte-clean-architecture\scripts\verify_component_architecture.py"
```

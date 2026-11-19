---
name: sk-sveltekit-starter
description: >-
  Scaffolds a personalized SvelteKit project (SvelteKit Minimal + TypeScript + Tailwind CSS / shadcn-svelte +
  Cloudflare Adapter + .dev.vars + Playwright E2E testing + optional Rust WASM).
  Use when the user asks to create, init, scaffold, or bootstrap a new SvelteKit project.
---

# SvelteKit Custom Starter (`sk-sveltekit-starter`)

Automates scaffolding of a modern SvelteKit project preconfigured for Cloudflare deployment and Playwright E2E testing.

## 1. Two-Step Scaffolding Workflow

1. **Confirm 3 Core Parameters** with the user before running the script:
   - **Project Name**: Created inside `./` by default (or `-o <output_dir>`).
   - **UI & Icons**: `Tailwind CSS` (default), plus optional `shadcn-svelte` (`--ui shadcn`) and `lucide-svelte` (`--icons`).
   - **Deployment Adapter**: **Cloudflare** (`@sveltejs/adapter-cloudflare`, default — auto-generates `.dev.vars` and `.dev.vars.example`), or ask if they prefer `auto`, `node`, or `static`.
2. **Execute [`init_sveltekit.py`](./scripts/init_sveltekit.py)**.

## 2. CLI Commands

1. **Standard project (Tailwind + Cloudflare + Playwright)**:
   ```powershell
   py "C:\Users\8hung\.gemini\config\plugins\sveltekit-dev\skills\sk-sveltekit-starter\scripts\init_sveltekit.py" <project-name>
   ```

2. **Full UI (`shadcn-svelte` + Lucide Icons)**:
   ```powershell
   py "C:\Users\8hung\.gemini\config\plugins\sveltekit-dev\skills\sk-sveltekit-starter\scripts\init_sveltekit.py" <project-name> --ui shadcn --icons
   ```

3. **With Rust WebAssembly (WASM)**:
   ```powershell
   py "C:\Users\8hung\.gemini\config\plugins\sveltekit-dev\skills\sk-sveltekit-starter\scripts\init_sveltekit.py" <project-name> --wasm
   ```

4. **Custom output directory**:
   ```powershell
   py "C:\Users\8hung\.gemini\config\plugins\sveltekit-dev\skills\sk-sveltekit-starter\scripts\init_sveltekit.py" <project-name> -o "D:\Projects"
   ```

## 3. Scaffolded Stack & Guardrails

- **Core**: SvelteKit Minimal (Skeleton) + TypeScript.
- **Styling**: Tailwind CSS configured in `app.css`.
- **E2E Testing**: `@playwright/test` with starter test `tests/home.spec.ts`.
- **Cloudflare Ready**: `@sveltejs/adapter-cloudflare` in `svelte.config.js`, plus `.dev.vars` and `.dev.vars.example`.
- **Node Runtime**: Auto-detects Node.js at `D:\code\environment\notejs`.
- **Agent Rules**: Generates `.agents/rules/sveltekit-standards.md` covering component modularization (`$lib/components/<feature>/`, routes < 250 lines), custom confirmation modals (no `window.confirm()`), clean form defaults & dot-formatted currency parsing, D1/SQLite safety & secret deployment, GIS auth, and idempotent Playwright E2E + PowerShell patterns.

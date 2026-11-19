---
name: anti-monolith-guard
description: >-
  Enforces file length limits and prevents monolithic code files (Anti-Monolith Architecture Guard).
  Limits Svelte/Go files to 250 lines, TS/JS/Rust files to 200 lines, and test files to 350 lines.
  Supports justified exemptions via the `@anti-monolith-allow` header tag.
---

# Anti-Monolith Architecture Guard (`anti-monolith-guard`)

Monitors source code modularity and enforces clean architecture by preventing oversized monolithic files.

## 1. Line Limits & Standards

| File Type | Max Lines | Recommended Refactoring Action |
| :--- | :---: | :--- |
| **`.svelte`** | **250** | Split UI into sub-components under `$lib/components/<feature>/` |
| **`.ts`, `.js`** | **200** | Extract helpers, utilities, or state stores into separate modules |
| **`.go` (Go)** | **250** | Split by package/responsibility (`cmd/`, `internal/`, `pkg/`; `*.pb.go` ignored) |
| **`.rs` (Rust)** | **200** | Split into sub-modules (e.g., `math/`, `models/`, `engine/`) |
| **Test files** (`*_test.go`, `*.test.ts`, `*.spec.ts`, `*.e2e.ts`) | **350** | Split large test suites by feature or user flow |

*(Automatically skips `node_modules`, `.svelte-kit`, `target`, `dist`, `build`, `vendor`, `.git`, `.venv`, `venv`, `src/lib/wasm`, `worker-configuration.d.ts`, and `*.pb.go`.)*

## 2. Exemption Mechanism (`@anti-monolith-allow`)

Exemptions are allowed **only** when a file genuinely cannot be split (e.g., static lookup tables, generated/constant data).

Place the tag within the **first 5 lines** of the file with an explicit reason:

```rust
// @anti-monolith-allow: Static Z-table distribution lookup cannot be split
```

or in TypeScript / Svelte / Go:

```typescript
// @anti-monolith-allow: Centralized state machine for the simulation pipeline
```

> [!WARNING]
> If a file exceeds its limit without a valid `@anti-monolith-allow` tag, or if the reason is left blank, the script prints `FAIL` and exits with code `1`.

## 3. Verification Commands

Run the centralized verification script at [`check_lines.py`](./scripts/check_lines.py):

1. **Check the current working directory**:
   ```powershell
   py "C:\Users\8hung\.gemini\config\skills\anti-monolith-guard\scripts\check_lines.py"
   ```

2. **Check a specific project directory**:
   ```powershell
   py "C:\Users\8hung\.gemini\config\skills\anti-monolith-guard\scripts\check_lines.py" "D:\Projects\my-app"
   ```

3. **Configure in `package.json`**:
   ```json
   "scripts": {
     "check:lines": "py \"C:\\Users\\8hung\\.gemini\\config\\skills\\anti-monolith-guard\\scripts\\check_lines.py\""
   }
   ```

## 4. Agent Guidelines

1. **Always run the line check** (`npm run check:lines` or `check_lines.py`) before reporting task completion.
2. When a file reaches the **`WARN` threshold (80% of its limit)**, proactively split out sub-components or helper modules instead of appending more code.
3. Never add `@anti-monolith-allow` without explicit user approval.

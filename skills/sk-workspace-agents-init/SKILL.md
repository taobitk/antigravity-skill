---
name: sk-workspace-agents-init
description: >-
  Scaffolds a hardened `.agents/` configuration directory and security-focused `GEMINI.md`
  for a repository. Use when the user asks to create `.agents`, configure repo-specific agent rules,
  or enforce rules forbidding AI access to `.dev.vars` / `.env` secrets.
---

# Workspace Agents Scaffolding (`sk-workspace-agents-init`)

Initializes an internal `.agents/` setup and project `GEMINI.md`, enforcing strict security rules that **forbid the agent from reading secret environment files** (`.dev.vars`, `.env`).

## 1. Workflow

1. **Determine Target Directory**: Defaults to the current working directory (`CWD`) or a user-specified path.
2. **Run Scaffolding Script**: Execute [`init_workspace_agents.py`](./scripts/init_workspace_agents.py).

## 2. Execution Commands

- **Current directory**:
  ```powershell
  py "C:\Users\8hung\.gemini\config\skills\sk-workspace-agents-init\scripts\init_workspace_agents.py"
  ```

- **Specific project path**:
  ```powershell
  py "C:\Users\8hung\.gemini\config\skills\sk-workspace-agents-init\scripts\init_workspace_agents.py" -d "D:\Projects\my-project"
  ```

## 3. Generated Files

1. **`GEMINI.md` (Project Root)**:
   - Strict security rule forbidding the agent from reading `.dev.vars`, `.env`, `.env.local`, or any secret file.
   - Instructs the agent to reference `.dev.vars.example` or `.env.example` instead.
   - Enforces user confirmation before destructive or state-altering edits.
2. **`.dev.vars.example`**:
   - Safe environment variable template suitable for Git commits.
3. **`.agents/rules/security-and-style.md`**:
   - Security, input sanitization, and code style guidelines.
4. **`.agents/skills/project-helper/SKILL.md`**:
   - Sample repo-local skill template for adding project-specific workflows.

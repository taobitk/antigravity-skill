---
name: learn-script
description: >-
  Crystallizes repetitive tasks or fragile, error-prone logic into hardened, deterministic Python CLI scripts.
  Triggered explicitly (e.g., `/learn-script`, "turn this into a script", "đóng gói thành script") or proactively suggested by the agent after solving complex/flaky logic or repetitive tasks.
---

# Learn & Crystallize Python Script (`learn-script`)

The user invoked `/learn-script` (or requested script crystallization) to extract reusable, error-prone, or repetitive logic from recent interactions and lock it into a deterministic Python CLI script inside `.agents/`.

> [!IMPORTANT]
> **Do NOT create or modify project files immediately.** You MUST follow the **Mandatory Proposal Workflow** below: perform deep root-cause analysis, generate a `script_proposal.md` artifact with `RequestFeedback: true` (so the user gets a **Proceed** button to approve), and only write/register files after explicit approval.

---

## Phase 1: Identify & Deconstruct What to Script

Before proposing anything, deeply analyze the conversation history and workspace context:

1. **Analyze User Corrections & Tool Failures**:
   - Inspect recent user messages for overrides, complaints, or corrections (e.g., *"no"*, *"sai rồi"*, *"lỗi kìa"*, *"chạy lại đi"*).
   - Inspect recent terminal/tool executions that failed (non-zero exit codes, shell quoting/escaping bugs, broken regexes, encoding errors on Windows, wrong file paths, or brittle one-liners).
2. **Isolate Failure vs. Working Resolution**:
   - Compare the failed/flaky attempts with the final working solution.
   - Pinpoint the exact root cause of fragility (e.g., PowerShell `$var` interpolation eating variables, inconsistent JSON/YAML formatting, forgetting `encoding="utf-8"`, manual multi-step file moves).
3. **Separate Invariants from Parameters**:
   - **Hardcoded Invariants** (what the agent must NEVER improvise again): business validation rules, UTF-8 encoding, cross-platform `pathlib.Path` handling, atomic file operations, safety checks, and error codes.
   - **CLI Parameters** (what changes per run): target paths, filter patterns, mode flags, and `--dry-run`.
4. **Verify if Crystallization is Needed**:
   - If the conversation contains no clear repetitive workflow or error-prone logic to extract, explain this briefly and ask the user which specific task they want to crystallize into a script before creating a proposal.

---

## Phase 2: Check Existing Scripts & Classify Target Mode

1. **Update Existing vs. Create New (Prefer Update)**:
   - Check `<project_root>/.agents/scripts/`, `<project_root>/.agents/skills/`, `GEMINI.md`, and `.agents/rules/` first.
   - **Update Existing**: If an existing script or skill already covers this domain but missed an edge case, flag, or validation step, propose updating that script rather than creating a duplicate.
   - **Create New**: Only when the logic covers a genuinely new workflow or guardrail.

2. **Classify Rule Mode vs. Skill Mode**:
   Evaluate and recommend one of the two storage architectures (the user can override during review):
   - **Rule Mode** *(Best for atomic utilities, project-wide guardrails, and mandatory single-command tools)*:
     - **Script Path**: `<project_root>/.agents/scripts/<script_name>.py`
     - **Enforcement**: A strict rule in `GEMINI.md` or `.agents/rules/` forcing agents to run `.agents/scripts/<script_name>.py` instead of writing ad-hoc code.
   - **Skill Mode** *(Best for multi-step runbooks, complex flag combinations, or domain-specific toolkits)*:
     - **Script Path**: `<project_root>/.agents/skills/<skill-name>/scripts/<script_name>.py`
     - **Enforcement**: A dedicated `<project_root>/.agents/skills/<skill-name>/SKILL.md` loaded on demand via progressive disclosure.

---

## Phase 3: Hardened Script Engineering Standards

Every proposed Python script MUST satisfy these strict engineering criteria:

1. **Dependency Strategy**:
   - **Simple / Self-Contained Tasks**: Use 100% **Python Standard Library** (`argparse`, `pathlib`, `json`, `re`, `subprocess`, `shutil`, `ast`, `urllib`, etc.) for zero-setup reliability.
   - **Complex / Fragile Tasks**: Use third-party libraries (`pydantic`, `pandas`, `beautifulsoup4`, `typer`, `httpx`, etc.) when raw stdlib code would be error-prone. Always check and use the project's virtual environment (`venv`).
2. **CLI & Safety Invariants**:
   - Use `argparse` (or `typer`/`click`) with clear `description`, `epilog` examples, and typed arguments.
   - Include a `--dry-run` flag whenever the script modifies, moves, or deletes files/data.
   - Explicitly specify `encoding="utf-8"` on all text file reads/writes (critical on Windows).
   - Return exit code `0` on success and non-zero (`1+`) with descriptive `sys.stderr` diagnostics on failure.
   - Guard execution with `if __name__ == "__main__": sys.exit(main())`.

---

## Phase 4: Mandatory Proposal Workflow (Artifact with `Proceed` Button)

Do **NOT** write to `.agents/` or `GEMINI.md` yet.

1. Create (or update) the artifact `<appDataDir>/brain/<conversation-id>/script_proposal.md` using `write_file` with:
   - `ArtifactMetadata.RequestFeedback = true` *(CRITICAL: this renders the interactive approval UI and **Proceed** button)*
   - `ArtifactMetadata.UserFacing = true`
   - `ArtifactMetadata.Summary`: A concise summary of the proposed script, mode (`Rule` vs `Skill`), and why it is needed.

2. Structure `script_proposal.md` with the following sections:
   - **1. Root Cause & Why a Hardened Script is Needed**: Contrast the flaky/manual approach from the conversation with the deterministic script approach.
   - **2. Target Architecture (`Rule` vs. `Skill` & `Create` vs. `Update`)**: State your recommended mode, rationale, and exact target file paths.
   - **3. CLI Interface & Engineering Spec**: Table of CLI flags (`--dry-run`, inputs, outputs), dependency choice (Stdlib vs. 3rd-party), and safety invariants.
   - **4. Proposed Python Script (`<script_name>.py`)**: Full, production-ready Python code block.
   - **5. Proposed Registration Diff (`GEMINI.md` / `SKILL.md`)**: Exact markdown rule snippet or `SKILL.md` content to bind future agents.
   - **6. Verification & Dry-Run Plan**: Exact commands that will be run to validate and dry-run the script upon approval.

3. In your chat response, point the user to `script_proposal.md` without re-dumping the entire code, and wait for them to click **Proceed** (or request adjustments).

---

## Phase 5: Execution, Live Verification & Registration (Post-Approval Only)

Once the user approves the proposal (clicks **Proceed** or confirms in chat):

1. **Write Candidate Script & Run Automated AST/CLI Validation**:
   Write the script and validate it with the bundled validator:
   ```bash
   python "c:\Users\8hung\.gemini\config\skills\learn-script\scripts\validate_and_register.py" --script "<path_to_script>" --validate-only
   ```
2. **Execute Mandatory Live Dry-Run / Test Run**:
   Run the script against real or sample workspace data (using `--dry-run` or safe test inputs) to verify 100% working behavior and exit code `0`. If any error occurs, fix and re-verify before registering.
3. **Register into `.agents/`**:
   - **Rule Mode**:
     ```bash
     python "c:\Users\8hung\.gemini\config\skills\learn-script\scripts\validate_and_register.py" --script "<path_to_script>" --mode rule --project-root "<project_root>" --description "<when_and_why_to_use>"
     ```
     Then update `GEMINI.md` or `.agents/rules/` with the mandatory execution rule.
   - **Skill Mode**:
     ```bash
     python "c:\Users\8hung\.gemini\config\skills\learn-script\scripts\validate_and_register.py" --script "<path_to_script>" --mode skill --skill-name "<skill-name>" --project-root "<project_root>" --description "<when_and_why_to_use>"
     ```
     Then verify `<project_root>/.agents/skills/<skill-name>/SKILL.md` includes concrete CLI examples.

---

## Bundled Helper Scripts

1. [`validate_and_register.py`](./scripts/validate_and_register.py): Validates AST syntax, CLI argument parser usage, `__main__` guard, and `--help` smoke test; registers verified scripts into `.agents/scripts/` (Rule mode) or `.agents/skills/<skill-name>/scripts/` (Skill mode).
2. [`skill_ops.py`](./scripts/skill_ops.py): Hardened CLI for atomic skill `rename` (folder + YAML frontmatter + internal references), `archive`, and `restore` with `--dry-run` support.


#!/usr/bin/env python3
"""
Validator and Registration Utility for learn-script.

Validates that a target Python script conforms to hardened CLI standards:
1. Valid Python AST syntax.
2. Uses argparse (or equivalent CLI argument parser) and has a __main__ entry point.
3. Passes `--help` smoke test with exit code 0.

Optionally scaffolds or registers the script into:
- Mode 'rule': `<project_root>/.agents/scripts/<script_name>.py` and outputs a Rule entry.
- Mode 'skill': `<project_root>/.agents/skills/<skill_name>/scripts/<script_name>.py` and creates `SKILL.md`.
"""

import argparse
import ast
import shutil
import subprocess
import sys
from pathlib import Path


def validate_script(script_path: Path) -> tuple[bool, list[str]]:
    """Validate syntax, CLI structure, and --help execution of a Python script."""
    errors: list[str] = []

    if not script_path.exists():
        return False, [f"File does not exist: {script_path}"]

    try:
        source = script_path.read_text(encoding="utf-8")
    except Exception as exc:
        return False, [f"Failed to read file: {exc}"]

    # 1. Check AST syntax
    try:
        tree = ast.parse(source, filename=str(script_path))
    except SyntaxError as exc:
        return False, [f"SyntaxError at line {exc.lineno}: {exc.msg}"]

    # 2. Check for CLI parser usage and __main__ guard
    has_main_guard = False
    has_cli_parser = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in ("argparse", "typer", "click"):
                    has_cli_parser = True
        elif isinstance(node, ast.ImportFrom):
            if node.module in ("argparse", "typer", "click"):
                has_cli_parser = True
        elif isinstance(node, ast.If):
            try:
                cond_src = ast.unparse(node.test)
                if "__name__" in cond_src and "__main__" in cond_src:
                    has_main_guard = True
            except Exception:
                pass

    if not has_cli_parser:
        errors.append("Missing CLI argument parser (`argparse`, `typer`, or `click`).")
    if not has_main_guard:
        errors.append("Missing `if __name__ == '__main__':` entry point guard.")

    # 3. Smoke test `--help`
    try:
        res = subprocess.run(
            [sys.executable, str(script_path), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if res.returncode != 0:
            errors.append(
                f"`--help` execution failed with exit code {res.returncode}: {res.stderr.strip()}"
            )
    except Exception as exc:
        errors.append(f"Failed to execute `--help` smoke test: {exc}")

    return len(errors) == 0, errors


def register_as_rule(
    script_path: Path, project_root: Path, description: str
) -> Path:
    """Copy validated script to `.agents/scripts/` and return its final path."""
    scripts_dir = project_root / ".agents" / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    dest_path = scripts_dir / script_path.name
    if script_path.resolve() != dest_path.resolve():
        shutil.copy2(script_path, dest_path)

    rel_script = f".agents/scripts/{script_path.name}"
    print("\n=== Registration Complete (Rule Mode) ===")
    print(f"Script Location: {dest_path}")
    print("\nSuggested Rule Snippet (for GEMINI.md or .agents/rules/):")
    print("-" * 60)
    print(f"### Hardened Script: `{script_path.name}`")
    print(f"- **When to use**: {description}")
    print(
        f"- **Mandatory Action**: ALWAYS execute `python {rel_script} [args]` instead of writing custom code or ad-hoc commands from scratch."
    )
    print(f"- **Inspect CLI options**: Run `python {rel_script} --help` before execution.")
    print("-" * 60)
    return dest_path


def register_as_skill(
    script_path: Path, project_root: Path, skill_name: str, description: str
) -> tuple[Path, Path]:
    """Package validated script into `.agents/skills/<skill_name>/scripts/` with SKILL.md."""
    skill_dir = project_root / ".agents" / "skills" / skill_name
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)

    dest_script = scripts_dir / script_path.name
    if script_path.resolve() != dest_script.resolve():
        shutil.copy2(script_path, dest_script)

    skill_md_path = skill_dir / "SKILL.md"
    rel_script = f".agents/skills/{skill_name}/scripts/{script_path.name}"

    if not skill_md_path.exists():
        skill_md_content = f"""---
name: {skill_name}
description: >-
  {description}
---

# {skill_name}

## Overview
{description}

## Mandatory Execution Rule
Do NOT rewrite or improvise the logic covered by this skill. Always execute the hardened Python script located at `{rel_script}`.

## Usage

Check supported flags and arguments first:
```bash
python "{rel_script}" --help
```

Execute the script:
```bash
python "{rel_script}" [arguments]
```
"""
        skill_md_path.write_text(skill_md_content, encoding="utf-8")

    print("\n=== Registration Complete (Skill Mode) ===")
    print(f"Script Location : {dest_script}")
    print(f"Skill Definition: {skill_md_path}")
    return dest_script, skill_md_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and register a hardened Python script for `.agents/`."
    )
    parser.add_argument(
        "--script",
        required=True,
        type=Path,
        help="Path to the Python script to validate and register.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only run validation checks without copying or registering.",
    )
    parser.add_argument(
        "--mode",
        choices=["rule", "skill"],
        help="Registration target mode: 'rule' (.agents/scripts/) or 'skill' (.agents/skills/<name>/scripts/).",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Target project root directory (defaults to current working directory).",
    )
    parser.add_argument(
        "--skill-name",
        type=str,
        help="Skill folder name (required when --mode=skill, e.g., 'sk-data-migrator').",
    )
    parser.add_argument(
        "--description",
        type=str,
        default="Deterministic automation script for repetitive project tasks.",
        help="Short description of when and why agents must use this script.",
    )

    args = parser.parse_args()

    ok, errors = validate_script(args.script)
    if not ok:
        print(f"[FAIL] Validation failed for {args.script}:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"[PASS] Script '{args.script}' passed all syntax, CLI, and --help checks.")

    if args.validate_only or not args.mode:
        return 0

    if args.mode == "rule":
        register_as_rule(args.script, args.project_root, args.description)
    elif args.mode == "skill":
        if not args.skill_name:
            print(
                "[ERROR] --skill-name is required when --mode=skill.",
                file=sys.stderr,
            )
            return 2
        register_as_skill(
            args.script, args.project_root, args.skill_name, args.description
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())


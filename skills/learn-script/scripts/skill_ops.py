#!/usr/bin/env python3
"""
Deterministic Skill Operations CLI (rename, archive, restore) for Antigravity Skills.
Eliminates fragile PowerShell loops and partial manual skill renames.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

DEFAULT_SKILLS_ROOT = Path(r"c:\Users\8hung\.gemini\config\skills")
DEFAULT_BACKUP_DIR = Path(r"c:\Users\8hung\.gemini\config\skills_backup_gcp")


def rename_skill(
    skills_root: Path, old_name: str, new_name: str, dry_run: bool = False
) -> int:
    """Atomically rename a skill folder, its YAML frontmatter name, and internal references."""
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", new_name):
        print(
            f"[ERROR] Invalid new skill name '{new_name}'. Must be lowercase hyphenated (e.g. 'learn-script').",
            file=sys.stderr,
        )
        return 1

    old_dir = skills_root / old_name
    new_dir = skills_root / new_name

    if not old_dir.is_dir() or not (old_dir / "SKILL.md").exists():
        print(
            f"[ERROR] Source skill '{old_name}' not found or missing SKILL.md at {old_dir}",
            file=sys.stderr,
        )
        return 1

    if new_dir.exists():
        print(
            f"[ERROR] Target skill directory already exists: {new_dir}",
            file=sys.stderr,
        )
        return 1

    target_files = [old_dir / "SKILL.md"]
    scripts_dir = old_dir / "scripts"
    if scripts_dir.is_dir():
        target_files.extend(scripts_dir.glob("*.py"))

    print(f"{'[DRY-RUN] ' if dry_run else ''}Renaming skill '{old_name}' -> '{new_name}':")
    print(f"  1. Directory: {old_dir} -> {new_dir}")

    for file_path in target_files:
        content = file_path.read_text(encoding="utf-8")
        updated = content
        if file_path.name == "SKILL.md":
            updated = re.sub(
                rf"^name:\s*{re.escape(old_name)}\s*$",
                f"name: {new_name}",
                updated,
                count=1,
                flags=re.MULTILINE,
            )
        updated = updated.replace(old_name, new_name)
        changed = updated != content
        print(f"  2. Update references in {file_path.name}: {'YES' if changed else 'NO CHANGES'}")
        if not dry_run and changed:
            file_path.write_text(updated, encoding="utf-8")

    if not dry_run:
        old_dir.rename(new_dir)
        print(f"[OK] Successfully renamed '{old_name}' to '{new_name}'.")
    return 0


def move_skills(
    src_root: Path,
    dest_root: Path,
    skill_names: list[str],
    action_label: str,
    dry_run: bool = False,
) -> int:
    """Move one or more skills safely between active skills directory and backup directory."""
    if not dry_run:
        dest_root.mkdir(parents=True, exist_ok=True)

    missing: list[str] = []
    for name in skill_names:
        s_dir = src_root / name
        if not s_dir.is_dir():
            missing.append(name)

    if missing:
        print(
            f"[ERROR] The following skills were not found in {src_root}: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 1

    for name in skill_names:
        src = src_root / name
        dst = dest_root / name
        print(f"{'[DRY-RUN] ' if dry_run else ''}{action_label}: {src} -> {dst}")
        if not dry_run:
            if dst.exists():
                shutil.rmtree(dst)
            shutil.move(str(src), str(dst))

    print(
        f"[OK] {'Dry-run completed' if dry_run else action_label + ' completed'} for {len(skill_names)} skill(s)."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Hardened CLI for renaming, archiving, and restoring Antigravity skills."
    )
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=DEFAULT_SKILLS_ROOT,
        help="Path to active skills directory.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # rename
    p_rename = subparsers.add_parser("rename", help="Atomically rename a skill and update references.")
    p_rename.add_argument("--old", required=True, help="Current skill folder/identifier name.")
    p_rename.add_argument("--new", required=True, help="New lowercase-hyphenated skill name.")
    p_rename.add_argument("--dry-run", action="store_true", help="Preview changes without modifying disk.")

    # archive
    p_archive = subparsers.add_parser("archive", help="Archive active skills to backup folder.")
    p_archive.add_argument("--skills", nargs="+", required=True, help="Skill names to archive.")
    p_archive.add_argument("--backup-dir", type=Path, default=DEFAULT_BACKUP_DIR, help="Backup folder path.")
    p_archive.add_argument("--dry-run", action="store_true", help="Preview move without modifying disk.")

    # restore
    p_restore = subparsers.add_parser("restore", help="Restore skills from backup folder to active skills.")
    p_restore.add_argument("--skills", nargs="+", required=True, help="Skill names to restore.")
    p_restore.add_argument("--backup-dir", type=Path, default=DEFAULT_BACKUP_DIR, help="Backup folder path.")
    p_restore.add_argument("--dry-run", action="store_true", help="Preview restore without modifying disk.")

    args = parser.parse_args()

    if args.command == "rename":
        return rename_skill(args.skills_root, args.old, args.new, args.dry_run)
    elif args.command == "archive":
        return move_skills(args.skills_root, args.backup_dir, args.skills, "Archive", args.dry_run)
    elif args.command == "restore":
        return move_skills(args.backup_dir, args.skills_root, args.skills, "Restore", args.dry_run)
    return 1


if __name__ == "__main__":
    sys.exit(main())


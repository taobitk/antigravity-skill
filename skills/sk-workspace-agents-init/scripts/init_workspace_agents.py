#!/usr/bin/env python3
"""
init_workspace_agents.py - Scaffolds project-specific .agents/ and GEMINI.md.
Part of the `sk-workspace-agents-init` Antigravity Skill.

Generates:
- Root GEMINI.md with STRICT privacy rule forbidding reading .dev.vars / .env.
- .agents/rules/security-and-style.md
- .agents/skills/project-helper/SKILL.md (Sample internal skill)
- .dev.vars.example (if missing)
"""

import argparse
import os
import sys
from pathlib import Path

# Đảm bảo UTF-8 trên Windows Console
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


def create_gemini_md(target_dir: Path, project_name: str):
    """Create root GEMINI.md with strict security rules."""
    gemini_file = target_dir / "GEMINI.md"
    content = f"""# Project Rules & Guidelines: {project_name}

## 1. Security & Environment Privacy (STRICT)
- **STRICTLY FORBIDDEN TO READ SECRETS**: The Agent is NEVER allowed to inspect, read, grep, or display contents of `.dev.vars`, `.env`, `.env.local`, `.env.*.local`, or any private credential/token files.
- **REFERENCE TEMPLATES ONLY**: All required environment variables and configuration keys MUST be referenced exclusively from `.dev.vars.example` or `.env.example`.
- **NO SECRET LEAKS**: Never output secrets, API tokens, private keys, or passwords in chat responses, generated files, commit messages, or terminal commands.

## 2. Confirmation Before Making Changes
- **No Unsolicited Modifications**: Never create, edit, overwrite, or delete critical files without clear confirmation. Propose plans and wait for the go-ahead.

## 3. Tech Stack & Architecture
- **Project**: {project_name}
- **Primary Language**: TypeScript / JavaScript / Python
- [Add your project-specific conventions, database info, and folder structure here]

## 4. Key Commands
- Development: `npm run dev`
- Build / Check: `npm run build`
- Testing: `npm test`
"""
    if not gemini_file.exists():
        gemini_file.write_text(content, encoding="utf-8")
        print(f"[+] Created: {gemini_file.name}")
    else:
        print(f"[*] Exists (preserved): {gemini_file.name}")


def create_security_rule(agents_dir: Path):
    """Create .agents/rules/security-and-style.md."""
    rules_dir = agents_dir / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    rule_file = rules_dir / "security-and-style.md"

    content = """# Workspace Security & Coding Guidelines

## Security Rules
1. **Never read secret files**: Under no circumstances should `.dev.vars` or `.env` files be accessed. Always refer to `.dev.vars.example` or `.env.example`.
2. **Sanitize inputs**: Ensure all user inputs and external API inputs are validated before processing.
3. **Safe Git practices**: Never stage or commit credential files. Verify `.gitignore` includes `.dev.vars` and `.env*`.

## Coding Style
1. **Clean Code & Modularity**: Keep functions focused, readable, and well-typed.
2. **Handling Errors**: Catch expected errors gracefully and provide meaningful error messages.
"""
    if not rule_file.exists():
        rule_file.write_text(content, encoding="utf-8")
        print(f"[+] Created: .agents/rules/{rule_file.name}")


def create_sample_skill(agents_dir: Path, project_name: str):
    """Create a sample project-specific skill inside .agents/skills/."""
    skill_dir = agents_dir / "skills" / "project-helper"
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"

    content = f"""---
name: project-helper
description: >-
  Kỹ năng hỗ trợ nội bộ riêng cho dự án {project_name}.
  Kích hoạt khi cần hướng dẫn thao tác nghiệp vụ, chạy test hoặc deploy nội bộ trong repo này.
---

# {project_name} Project Helper Skill

Kỹ năng này chỉ tồn tại và có hiệu lực bên trong dự án này.

## Quy trình làm việc nội bộ
1. Kiểm tra biến môi trường mẫu trong `.dev.vars.example`.
2. Hướng dẫn chạy kiểm thử hoặc cập nhật schema.
"""
    if not skill_file.exists():
        skill_file.write_text(content, encoding="utf-8")
        print(f"[+] Created: .agents/skills/project-helper/{skill_file.name}")


def create_example_vars(target_dir: Path):
    """Ensure a .dev.vars.example file exists."""
    example_file = target_dir / ".dev.vars.example"
    if not example_file.exists():
        content = (
            "# Local Environment Variables Example (Safe to commit to VCS)\n"
            "# Copy this file to .dev.vars or .env for local secrets\n"
            "APP_ENV=development\n"
            "API_BASE_URL=https://api.example.com\n"
            "SESSION_SECRET=sample_secret_key_change_in_dev_vars\n"
        )
        example_file.write_text(content, encoding="utf-8")
        print(f"[+] Created: {example_file.name}")


def main():
    parser = argparse.ArgumentParser(description="Khởi tạo cấu hình .agents/ và GEMINI.md bảo mật cho dự án")
    parser.add_argument("-d", "--dir", default=".", help="Đường dẫn thư mục dự án (mặc định: thư mục hiện tại ./)")
    parser.add_argument("-n", "--name", default="", help="Tên dự án (mặc định lấy tên thư mục)")

    args = parser.parse_args()

    target_dir = Path(args.dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    project_name = args.name if args.name else target_dir.name

    print("=" * 65)
    print(f"🛡️  KHỞI TẠO BẢO MẬT & WORKSPACE .AGENTS CHO DỰ ÁN: {project_name}")
    print(f"📁 Vị trí: {target_dir}")
    print("=" * 65)

    # 1. Tạo GEMINI.md bảo mật tại root dự án
    create_gemini_md(target_dir, project_name)

    # 2. Tạo .dev.vars.example nếu chưa có
    create_example_vars(target_dir)

    # 3. Tạo thư mục .agents/
    agents_dir = target_dir / ".agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    # 4. Tạo rules chuyên biệt
    create_security_rule(agents_dir)

    # 5. Tạo skill mẫu nội bộ
    create_sample_skill(agents_dir, project_name)

    print("\n" + "=" * 65)
    print("✅ ĐÃ KHỞI TẠO CẤU HÌNH .AGENTS VÀ GEMINI.MD THÀNH CÔNG!")
    print("🔒 Quy tắc bảo vệ: Agent bị CẤM TUYỆT ĐỐI đọc file .dev.vars / .env")
    print("📋 Toàn bộ cấu trúc biến môi trường được quản lý qua .dev.vars.example")
    print("=" * 65)


if __name__ == "__main__":
    main()

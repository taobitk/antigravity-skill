#!/usr/bin/env python3
"""
verify_naming_standards.py - Kiểm tra chuẩn đặt tên file và code trong dự án.
Part of the `code-naming-standards` Antigravity Skill.

Rules:
1. Svelte Components: PascalCase.svelte (e.g. ConflictModal.svelte)
2. SvelteKit Routes: +page.svelte, +server.ts, +layout.svelte, etc.
3. TS Utility Files: camelCase.ts (e.g. dateUtils.ts)
4. Skip framework standards: index.ts, schema.ts, app.d.ts, worker-configuration.d.ts
"""

import argparse
import re
import sys
from pathlib import Path

# Đảm bảo in UTF-8 tiếng Việt trên Windows Console
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

FRAMEWORK_EXCEPTIONS = {
    "index.ts",
    "schema.ts",
    "app.d.ts",
    "app.html",
    "layout.css",
    "worker-configuration.d.ts",
    "drizzle.config.ts",
    "playwright.config.ts",
    "prettier.config.js",
    "vite.config.ts"
}


def is_pascal_case(name: str) -> bool:
    return bool(re.match(r"^[A-Z][a-zA-Z0-9]*$", name))


def is_camel_case(name: str) -> bool:
    return bool(re.match(r"^[a-z][a-zA-Z0-9]*$", name))


def check_file_naming(src_dir: Path) -> tuple[int, int]:
    violations = 0
    total_checked = 0

    print("=" * 65)
    print("🏷️  KIỂM TRA CHUẨN ĐẶT TÊN FILE (code-naming-standards)")
    print(f"📁 Thư mục: {src_dir}")
    print("=" * 65)

    for path in src_dir.rglob("*"):
        if path.is_dir() or "node_modules" in path.parts or ".svelte-kit" in path.parts:
            continue

        filename = path.name

        # Bỏ qua các file đặc thù của SvelteKit (+page, +server, +layout)
        if filename.startswith("+"):
            continue

        # Bỏ qua các file ngoại lệ chuẩn
        if filename in FRAMEWORK_EXCEPTIONS or filename.endswith(".d.ts"):
            continue

        # Bỏ qua các file test / e2e đặc thù
        if any(filename.endswith(ext) for ext in [".spec.ts", ".test.ts", ".e2e.ts"]):
            print(f"[✓] File Test: {filename}")
            continue

        total_checked += 1
        # Hỗ trợ chuẩn Svelte 5 Rune Module (.svelte.ts)
        if filename.endswith('.svelte.ts'):
            stem = filename[:-10]
        elif filename.endswith('.svelte.js'):
            stem = filename[:-10]
        else:
            stem = path.stem

        # 1. Svelte Components: PascalCase.svelte
        if path.suffix == ".svelte":
            if not is_pascal_case(stem):
                print(f"[✗] Svelte Component sai chuẩn (cần PascalCase): {path.relative_to(src_dir.parent)}")
                violations += 1
            else:
                print(f"[✓] Component chuẩn PascalCase: {filename}")

        # 2. File TypeScript / JavaScript: camelCase.ts
        elif path.suffix in [".ts", ".js"]:
            if not is_camel_case(stem):
                print(f"[✗] File TypeScript sai chuẩn (cần camelCase): {path.relative_to(src_dir.parent)}")
                violations += 1
            else:
                print(f"[✓] File TS chuẩn camelCase: {filename}")

    print("-" * 65)
    if violations == 0:
        print(f"🎯 KẾT LUẬN: ĐẠT CHUẨN! Đã kiểm tra {total_checked} file, không có vi phạm.")
    else:
        print(f"⚠️  KẾT LUẬN: Phát hiện {violations} file chưa đúng chuẩn đặt tên!")
    print("=" * 65)

    return violations, total_checked


def main():
    parser = argparse.ArgumentParser(description="Kiểm tra chuẩn đặt tên file trong dự án")
    parser.add_argument("-d", "--dir", default="src", help="Thư mục cần quét (mặc định: src)")
    args = parser.parse_args()

    target_dir = Path(args.dir).resolve()
    if not target_dir.exists():
        print(f"[!] Thư mục không tồn tại: {target_dir}")
        sys.exit(1)

    violations, _ = check_file_naming(target_dir)
    sys.exit(0 if violations == 0 else 1)


if __name__ == "__main__":
    main()

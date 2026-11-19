#!/usr/bin/env python3
"""
check_lines.py - Anti-Monolith Line Guard
Quét và kiểm tra số lượng dòng code của các file trọng yếu trong dự án.
Chống viết dồn "nồi lẩu thập cẩm", ép kiến trúc module hóa sạch sẽ.

Quy định giới hạn:
- Svelte components (.svelte): Tối đa 250 dòng.
- TypeScript / JS modules (.ts, .js): Tối đa 200 dòng.
- Go modules (.go): Tối đa 250 dòng.
- Rust modules (.rs): Tối đa 200 dòng.
- Test files (*_test.go, *.test.ts, *.spec.ts, *.e2e.ts): Tối đa 350 dòng.

Quy định ngoại lệ:
- Đặt comment ở 5 dòng đầu tiên của file:
    // @anti-monolith-allow: <ghi rõ lý do cụ thể>
  hoặc trong file dạng khác:
    /* @anti-monolith-allow: <lý do> */
    # @anti-monolith-allow: <lý do>
"""

import os
import sys
from pathlib import Path
import re

# Đảm bảo in tiếng Việt UTF-8 mượt mà trên console Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Cấu hình thư mục và giới hạn dòng
LIMITS = {
    ".svelte": 250,
    ".ts": 200,
    ".js": 200,
    ".go": 250,
    ".rs": 200,
}

TEST_FILE_SUFFIXES = (
    "_test.go",
    ".test.ts",
    ".spec.ts",
    ".e2e.ts",
)
TEST_FILE_LIMIT = 350


def get_file_limit(path: Path) -> int | None:
    """Return the line limit for a source or test file, or None if untracked."""
    if any(path.name.endswith(suffix) for suffix in TEST_FILE_SUFFIXES):
        return TEST_FILE_LIMIT
    return LIMITS.get(path.suffix)

IGNORE_DIRS = {
    "node_modules",
    ".svelte-kit",
    "target",
    "dist",
    "build",
    "vendor",
    ".git",
    ".venv",
    "venv",
}

IGNORE_EXACT_FILES = {
    "worker-configuration.d.ts",
}

EXCEPTION_REGEX = re.compile(
    r'(?://|/\*|#)\s*@anti-monolith-allow:\s*(.+?)(?:\*/|\n|$)',
    re.IGNORECASE
)

def is_ignored(path: Path, root: Path) -> bool:
    rel_path = path.relative_to(root)
    # Kiểm tra các thư mục cần bỏ qua
    for part in rel_path.parts:
        if part in IGNORE_DIRS:
            return True
    # Bỏ qua thư mục wasm output hoặc file protobuf sinh tự động của Go
    rel_str = rel_path.as_posix()
    if rel_str.startswith("src/lib/wasm") or "src/lib/wasm" in rel_str:
        return True
    if path.name.endswith(".pb.go"):
        return True
    if path.name in IGNORE_EXACT_FILES:
        return True
    return False


def check_file(path: Path) -> tuple[int, bool, str]:
    """
    Đếm số dòng và kiểm tra ngoại lệ.
    Trả về: (line_count, is_exempt, reason)
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        return 0, False, f"Không đọc được file: {e}"

    line_count = len(lines)
    header = "".join(lines[:5])
    match = EXCEPTION_REGEX.search(header)

    if match:
        reason = match.group(1).strip()
        if reason:
            return line_count, True, reason
        return line_count, False, "Tag @anti-monolith-allow thiếu lý do cụ thể!"

    return line_count, False, ""


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Anti-Monolith Code Line Guard")
    parser.add_argument("target_dir", nargs="?", default=".", help="Thư mục dự án cần kiểm tra (mặc định: ./)")
    args = parser.parse_args()

    root = Path(args.target_dir).resolve()
    print("=" * 75)
    print("🛡️  ANTI-MONOLITH CODE LINE GUARD")
    print(f"📁 Thư mục gốc: {root}")
    print("=" * 75)

    violations = []
    exemptions = []
    total_files = 0
    passed_files = 0

    print(f"{'FILE':<48} | {'DÒNG':>5} | {'GIỚI HẠN':>8} | {'TRẠNG THÁI'}")
    print("-" * 75)

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORE_DIRS)
        current_dir = Path(dirpath)
        for filename in sorted(filenames):
            file_path = current_dir / filename
            limit = get_file_limit(file_path)
            if limit is None or is_ignored(file_path, root):
                continue

            total_files += 1
            rel_path = file_path.relative_to(root).as_posix()
            line_count, is_exempt, reason = check_file(file_path)

            if is_exempt:
                exemptions.append((rel_path, line_count, limit, reason))
                status = "EXEMPT ⚠️"
            elif line_count > limit:
                violations.append((rel_path, line_count, limit))
                status = "FAIL ❌"
            elif line_count >= limit * 0.8:
                passed_files += 1
                status = "WARN ⚡"
            else:
                passed_files += 1
                status = "PASS ✅"

            display_path = rel_path if len(rel_path) <= 46 else "..." + rel_path[-43:]
            print(f"{display_path:<48} | {line_count:>5} | {limit:>8} | {status}")

    print("-" * 75)

    # Hiển thị danh sách ngoại lệ nếu có
    if exemptions:
        print("\n📋 DANH SÁCH FILE NGOẠI LỆ HỢP LỆ (@anti-monolith-allow):")
        for path, count, limit, reason in exemptions:
            print(f"  • {path} ({count}/{limit} dòng) -> Lý do: {reason}")

    # Hiển thị danh sách vi phạm nếu có
    if violations:
        print("\n❌ PHÁT HIỆN FILE VƯỢT QUÁ GIỚI HẠN DÒNG (NỒI LẨU THẬP CẨM):")
        for path, count, limit in violations:
            over = count - limit
            print(f"  • {path}: {count} dòng (vượt +{over} dòng so với giới hạn {limit})")
        print("\n💡 HƯỚNG XỬ LÝ:")
        print("  1. Chia nhỏ module / component ra các sub-components hoặc helper functions.")
        print("  2. Nếu bắt buộc phải dài (bảng hằng số, cấu hình lớn), thêm comment vào đầu file:")
        print("     // @anti-monolith-allow: <ghi rõ lý do cụ thể>")
        print("=" * 75)
        sys.exit(1)

    print(f"\n🎉 TẤT CẢ {total_files} FILES ĐỀU ĐẠT CHUẨN KIẾN TRÚC SẠCH (Pass: {passed_files}, Exempt: {len(exemptions)})")
    print("=" * 75)
    sys.exit(0)


if __name__ == "__main__":
    main()

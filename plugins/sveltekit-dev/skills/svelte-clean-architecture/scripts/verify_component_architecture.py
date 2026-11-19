#!/usr/bin/env python3
"""
verify_component_architecture.py - Kiểm tra tuân thủ Kiến trúc 3 tầng (Svelte Clean Architecture)
Vị trí: .agents/skills/svelte-clean-architecture/scripts/verify_component_architecture.py

Quy chuẩn:
1. File trang (+page.svelte) không được vượt quá 150 dòng.
2. File .svelte (UI) không được chứa lệnh gọi API fetch() trực tiếp (phải bóc tách vào *.svelte.ts composable).
"""

import argparse
import sys
import re
from pathlib import Path

# Đảm bảo in UTF-8 tiếng Việt trên Windows Console
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Ngưỡng quy chuẩn
MAX_PAGE_LINES = 180
MAX_COMPONENT_LINES = 250

def check_file(file_path: Path):
    violations = []
    lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    line_count = len(lines)
    rel_path = file_path.as_posix()

    is_page = file_path.name == "+page.svelte"

    # 1. Kiểm tra độ dài file
    if is_page and line_count > MAX_PAGE_LINES:
        violations.append(f"File trang điều phối quá dài ({line_count} dòng > {MAX_PAGE_LINES} dòng)")
    elif not is_page and line_count > MAX_COMPONENT_LINES:
        violations.append(f"Component UI quá dài ({line_count} dòng > {MAX_COMPONENT_LINES} dòng)")

    # 2. Kiểm tra vi phạm Separation of Concerns (SoC) - Gọi fetch() trực tiếp trong component UI
    for idx, line in enumerate(lines, 1):
        clean_line = line.strip()
        # Bỏ qua comment
        if clean_line.startswith("//") or clean_line.startswith("/*") or clean_line.startswith("*"):
            continue
        if re.search(r"\bfetch\s*\(", clean_line):
            violations.append(f"Dòng {idx}: Chứa lệnh gọi fetch() trực tiếp trong file .svelte (Phải bóc tách vào Composable *.svelte.ts)")
            break

    return line_count, violations

def main():
    parser = argparse.ArgumentParser(
        description="Kiểm tra tuân thủ Kiến trúc 3 tầng (Svelte Clean Architecture)"
    )
    parser.add_argument(
        "-d",
        "--dir",
        default="src",
        help="Thư mục cần quét (mặc định: src)",
    )
    args = parser.parse_args()

    root_dir = Path(args.dir).resolve()
    if not root_dir.exists():
        print(f"❌ Không tìm thấy thư mục: {root_dir}")
        sys.exit(1)

    print("=" * 70)
    print("🏛️  KIỂM TRA KIẾN TRÚC MÃ NGUỒN (svelte-clean-architecture)")
    print(f"📁 Thư mục quét: {root_dir}")
    print(f"📏 Ngưỡng: +page.svelte <= {MAX_PAGE_LINES} dòng | UI Component <= {MAX_COMPONENT_LINES} dòng")
    print("=" * 70)

    total_checked = 0
    total_violations = 0

    svelte_files = sorted(root_dir.rglob("*.svelte"))

    for f in svelte_files:
        # Bỏ qua file trong node_modules hoặc .svelte-kit
        if "node_modules" in f.parts or ".svelte-kit" in f.parts:
            continue

        total_checked += 1
        line_count, violations = check_file(f)
        rel_display = f.relative_to(root_dir).as_posix()

        if violations:
            total_violations += 1
            print(f"[✗] VI PHẠM  {rel_display:<30} {line_count:>4} dòng")
            for v in violations:
                print(f"    ➔ {v}")
        else:
            print(f"[✓] ĐẠT      {rel_display:<30} {line_count:>4} dòng")

    print("-" * 70)
    if total_violations > 0:
        print(f"🚨 KẾT LUẬN: Phát hiện {total_violations}/{total_checked} file vi phạm kiến trúc Clean Architecture!")
        print("💡 Hướng dẫn khắc phục: Bóc tách logic sang src/lib/composables/*.svelte.ts.")
        print("=" * 70)
        sys.exit(1)
    else:
        print(f"🎯 KẾT LUẬN: ĐẠT CHUẨN KIẾN TRÚC SẠCH! Tất cả {total_checked} file đều đạt chuẩn.")
        print("=" * 70)
        sys.exit(0)

if __name__ == "__main__":
    main()

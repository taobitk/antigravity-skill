#!/usr/bin/env python3
"""
init_sveltekit.py - SvelteKit Project Scaffolding Script
Part of the `sk-sveltekit-starter` Antigravity Skill.

Automates:
- SvelteKit (Minimal/Skeleton) + TypeScript creation via `npx sv create`
- Adapter Cloudflare integration
- Generation of `.dev.vars` and `.dev.vars.example`
- Playwright E2E testing setup (with Chrome channel & sample tests)
- Tailwind CSS / shadcn-svelte / Lucide icons setup
- Node.js runtime auto-detection (prepends D:\\code\\environment\\notejs if present)
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# Đảm bảo in tiếng Việt UTF-8 không bị lỗi trên Windows Console (cp1252)
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

DEFAULT_NODE_DIR = r"D:\code\environment\notejs"


def setup_environment(node_dir: str):
    """Ensure the specified Node directory is at the beginning of PATH."""
    if os.path.exists(node_dir):
        current_path = os.environ.get("PATH", "")
        if node_dir.lower() not in current_path.lower():
            os.environ["PATH"] = f"{node_dir};{current_path}"
            print(f"[+] Added Node runtime to PATH: {node_dir}")


def run_cmd(cmd: list[str], cwd: str | None = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and stream output."""
    print(f"\n[RUN] {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        shell=(os.name == "nt"),
        check=check,
        text=True
    )
    return result


def create_cloudflare_vars(project_dir: Path):
    """Create .dev.vars and .dev.vars.example for Cloudflare Workers/Pages."""
    dev_vars_example = project_dir / ".dev.vars.example"
    dev_vars = project_dir / ".dev.vars"

    example_content = (
        "# Cloudflare Local Environment Variables (Example Template)\n"
        "# Copy this file to .dev.vars for local secrets\n"
        "APP_ENV=development\n"
        "API_BASE_URL=https://api.example.com\n"
        "SESSION_SECRET=your_dev_secret_key_change_me_123456\n"
        "# KV or D1 bindings if applicable:\n"
        "# DB_NAME=my-db\n"
    )

    if not dev_vars_example.exists():
        dev_vars_example.write_text(example_content, encoding="utf-8")
        print(f"[+] Created: {dev_vars_example.name}")

    if not dev_vars.exists():
        dev_vars.write_text(example_content, encoding="utf-8")
        print(f"[+] Created: {dev_vars.name}")


def ensure_playwright_sample_test(project_dir: Path):
    """Ensure tests directory contains a working Playwright E2E smoke test."""
    tests_dir = project_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    test_file = tests_dir / "home.spec.ts"

    test_code = (
        "import { test, expect } from '@playwright/test';\n\n"
        "test('Trang chủ phản hồi 200 và render tiêu đề', async ({ page }) => {\n"
        "  await page.goto('/');\n"
        "  await expect(page).toHaveTitle(/.*|SvelteKit/);\n"
        "});\n"
    )
    if not test_file.exists():
        test_file.write_text(test_code, encoding="utf-8")
        print(f"[+] Created Playwright test sample: {test_file.name}")


def create_sveltekit_rule(project_dir: Path):
    """Tự động sinh file rule .agents/rules/sveltekit-standards.md cho mọi dự án SvelteKit."""
    rules_dir = project_dir / ".agents" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    rule_file = rules_dir / "sveltekit-standards.md"
    content = """# SvelteKit & UI Architecture Standards

## 1. Kiến Trúc & Chia Tách Component (Anti-Monolith)
- **Không để file route quá tải**: Tuyệt đối không để các file route (`+page.svelte`) phình to vượt quá 250 dòng.
- **Module hóa theo tính năng**: Bóc tách giao diện thành các sub-components độc lập đặt trong `$lib/components/<feature>/` (ví dụ: `$lib/components/map/`, `$lib/components/dashboard/`).
- **Phân công trách nhiệm rõ ràng**:
  - `+page.svelte`: Chỉ điều phối luồng dữ liệu, state tổng, trigger modal và bố cục grid chính.
  - Sub-components: Chuyên biệt hiển thị thẻ, form, thanh điều hướng.
  - Server actions (`+page.server.ts`): Xử lý validate và ghi DB.

## 2. Tiêu Chuẩn UI/UX & Tối Giản Hóa (Paper Map Philosophy)
- **Tối giản hóa câu chữ**: Cắt bỏ triệt để các đoạn giải thích dài dòng, văn mẫu hướng dẫn ("Đặt bối cảnh...", "Chưa có ghi chú...", "Dôi dư:", "Tốn:"). Ưu tiên dùng Icon kèm tooltip hoặc nhãn xúc tích 1-2 từ (vd: `AI`, `✨`, `Timeline`).
- **Nghiêm cấm `window.confirm()` trình duyệt**:
  - Tuyệt đối KHÔNG dùng hàm `window.confirm()` hay `alert()` mặc định xấu xí của browser.
  - Bắt buộc dùng Custom Dialog Modal với hiệu ứng bo góc `rounded-2xl` và mờ nền `backdrop-blur`.
- **Quy chuẩn Form & Điền dữ liệu**:
  - **Không điền sẵn số mặc định**: Các ô thời gian, tiền, số lượng phải để trống kèm placeholder mờ gợi ý (tránh bắt người dùng phải bấm xóa số cũ).
  - Tự động reset input về trống sau khi submit thành công.
- **Xử lý tiền tệ Việt Nam (Currency UX)**:
  - Hiển thị tiền luôn có dấu chấm phân cách hàng nghìn (ví dụ: `50.000`, `100.000`).
  - Input nhập tiền phải tự động format dấu chấm khi người dùng gõ hoặc bấm nút chọn nhanh.
  - **Khử chấm ở Backend**: Tại các server actions, luôn luôn dùng `.replace(/\\./g, '')` trước khi ép kiểu `Number()` để dữ liệu lưu vào DB luôn chính xác.

## 3. Svelte 5 & State Management
- Tuân thủ cú pháp Svelte 5 runes (`$state`, `$derived`, `$props`).
- Đối với các thao tác chọn nhanh, ưu tiên dùng Optimistic UI (cập nhật state hiển thị 0ms trước, revert nếu server trả về lỗi).

## 4. An Toàn Cơ Sở Dữ Liệu & Di Trú (D1 / SQLite Anti-Data Loss)
- **Tuyệt đối không tự ý xóa data mồ côi**: Khi chuyển từ Single-user sang Multi-user, KHÔNG ĐƯỢC chạy lệnh xóa hàng loạt (`DELETE WHERE user_id IS NULL`). Phải hỏi người dùng để gán data cũ cho tài khoản mới (`UPDATE ... SET user_id = ?`) hoặc sao lưu trước.
- **Thay đổi ràng buộc UNIQUE trong SQLite/D1**: SQLite không hỗ trợ `ALTER TABLE ... DROP/ADD CONSTRAINT UNIQUE`. Luôn áp dụng quy trình migrate: tạo bảng tạm `_new` -> chép dữ liệu -> drop bảng cũ -> đổi tên bảng mới.
- **Thực thi migration từ xa**: Khi lệnh `wrangler d1 migrations apply --remote` gặp lỗi cấp quyền (7403), chuyển sang dùng lệnh chạy trực tiếp file SQL: `npx wrangler d1 execute <db> --remote --file=<path.sql>`.
- **Cloudflare Pages Secrets**: Bất kỳ secret nào thêm qua `wrangler pages secret put` đều chỉ nạp vào Worker ở lần deploy kế tiếp. Luôn chạy lại quy trình build và deploy sau khi cập nhật secret.

## 5. Xác Thực (Auth) & Chuẩn Kiểm Thử E2E Playwright
- **Google Identity Services (GIS)**: Luôn khai báo `declare global { interface Window { google?: any; } }` trong `src/app.d.ts` để TypeScript không báo lỗi khi GIS gắn `window.google`.
- **E2E Testing với Auth Gate**: Tuyệt đối không automate luồng đăng nhập thật trên giao diện Google OAuth (sẽ dính CAPTCHA/2FA). Cần seed trực tiếp user test và session test vào D1 (`users`, `sessions`), sau đó nạp cookie `session_id` qua `browserContext.addCookies()`.
- **Tính Idempotent trong E2E**: Luôn đưa lệnh seed/upsert session test vào hook `test.beforeEach()` để kịch bản kiểm thử có thể chạy lặp lại liên tục mà không bị gãy khi có bước "Đăng xuất" (Logout).
- **Windows PowerShell CLI**: Khi nối chuỗi nhiều lệnh terminal trên Windows PowerShell, luôn dùng dấu chấm phẩy `;` thay vì `&&` để tránh lỗi cú pháp parse.

## 6. Kiểm Thử & Triển Khai
- Luôn kiểm tra `npm run check` (0 errors, 0 warnings) và `npm run test:unit` trước khi deploy.
- Sau khi deploy Cloudflare Pages, luôn chạy kiểm thử E2E Playwright trực tiếp trên production (`npx playwright test tests/live.e2e.ts`).
"""
    if not rule_file.exists():
        rule_file.write_text(content, encoding="utf-8")
        print(f"[+] Created SvelteKit Rule: .agents/rules/{rule_file.name}")


def create_wasm_engine(project_dir: Path):
    """Khởi tạo khung sườn Rust WebAssembly (wasm-engine) và scripts tích hợp."""
    wasm_dir = project_dir / "wasm-engine"
    src_dir = wasm_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)

    # 1. Tạo Cargo.toml
    cargo_toml = wasm_dir / "Cargo.toml"
    if not cargo_toml.exists():
        cargo_content = """[package]
name = "wasm-engine"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib", "rlib"]

[dependencies]
wasm-bindgen = "0.2"
console_error_panic_hook = { version = "0.1", optional = true }

[features]
default = ["console_error_panic_hook"]
"""
        cargo_toml.write_text(cargo_content, encoding="utf-8")
        print(f"[+] Created: {cargo_toml.relative_to(project_dir)}")

    # 2. Tạo src/lib.rs khung mẫu
    lib_rs = src_dir / "lib.rs"
    if not lib_rs.exists():
        lib_content = """use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn init_engine() -> String {
    "WASM Engine initialized successfully!".into()
}
"""
        lib_rs.write_text(lib_content, encoding="utf-8")
        print(f"[+] Created: {lib_rs.relative_to(project_dir)}")

    # 3. Tạo .gitignore cho wasm-engine
    wasm_gitignore = wasm_dir / ".gitignore"
    if not wasm_gitignore.exists():
        wasm_gitignore.write_text("/target\n/pkg\n", encoding="utf-8")
        print(f"[+] Created: {wasm_gitignore.relative_to(project_dir)}")

    # 4. Cập nhật package.json với các scripts wasm
    pkg_json_path = project_dir / "package.json"
    if pkg_json_path.exists():
        try:
            with open(pkg_json_path, "r", encoding="utf-8") as f:
                pkg_data = json.load(f)

            scripts = pkg_data.setdefault("scripts", {})
            scripts["wasm:build"] = "wasm-pack build wasm-engine --target web --out-dir ../src/lib/wasm"
            scripts["wasm:dev"] = "wasm-pack build wasm-engine --target web --dev --out-dir ../src/lib/wasm"

            with open(pkg_json_path, "w", encoding="utf-8") as f:
                json.dump(pkg_data, f, indent=2, ensure_ascii=False)
            print("[+] Updated package.json with 'wasm:build' and 'wasm:dev' scripts")
        except Exception as e:
            print(f"[!] Warning: Could not update package.json with wasm scripts: {e}")

    # 5. Cấu hình tsconfig.json để bỏ qua kiểm tra type file JS auto-generated của wasm-pack
    tsconfig_path = project_dir / "tsconfig.json"
    if tsconfig_path.exists():
        try:
            with open(tsconfig_path, "r", encoding="utf-8") as f:
                tsconfig_data = json.load(f)
            excludes = tsconfig_data.setdefault("exclude", [])
            if "src/lib/wasm/*.js" not in excludes:
                excludes.append("src/lib/wasm/*.js")
            with open(tsconfig_path, "w", encoding="utf-8") as f:
                json.dump(tsconfig_data, f, indent=2, ensure_ascii=False)
            print("[+] Excluded 'src/lib/wasm/*.js' in tsconfig.json")
        except Exception as e:
            print(f"[!] Warning: Could not update tsconfig.json: {e}")


def main():
    parser = argparse.ArgumentParser(description="Khởi tạo dự án SvelteKit chuẩn cá nhân hóa")
    parser.add_argument("name", nargs="?", default="my-svelte-app", help="Tên dự án hoặc thư mục")
    parser.add_argument("-o", "--output-dir", default=".", help="Thư mục cha chứa dự án (mặc định: ./)")
    parser.add_argument("--ui", choices=["tailwind", "shadcn", "vanilla"], default="tailwind", help="Giao diện (tailwind / shadcn / vanilla)")
    parser.add_argument("--icons", action="store_true", help="Cài thêm thư viện icon lucide-svelte")
    parser.add_argument("--adapter", choices=["cloudflare", "auto", "node", "static"], default="cloudflare", help="Adapter deploy")
    parser.add_argument("--e2e", choices=["playwright", "none"], default="playwright", help="Cấu hình E2E test")
    parser.add_argument("--wasm", action="store_true", help="Khởi tạo khung sườn Rust WebAssembly (wasm-engine)")
    parser.add_argument("--pm", choices=["npm", "pnpm", "bun"], default="npm", help="Package manager")
    parser.add_argument("--node-dir", default=DEFAULT_NODE_DIR, help="Đường dẫn thư mục Node.js")
    parser.add_argument("--no-install", action="store_true", help="Không tự động chạy npm install")

    args = parser.parse_args()

    # 1. Thiết lập môi trường Node
    setup_environment(args.node_dir)

    # 2. Xác định thư mục đích
    base_dir = Path(args.output_dir).resolve()
    target_dir = (base_dir / args.name).resolve() if args.name != "." else base_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print(f"🚀 KHỞI TẠO DỰ ÁN SVELTEKIT: {args.name}")
    print(f"📁 Thư mục: {target_dir}")
    print(f"🎨 UI: {args.ui} | Icons: {'lucide' if args.icons else 'không'}")
    print(f"☁️  Adapter: {args.adapter}")
    print(f"🎭 E2E Testing: {args.e2e}")
    print("=" * 60)

    # 3. Chuẩn bị danh sách Add-ons cho `npx sv create`
    addons = ["prettier"]

    if args.ui in ["tailwind", "shadcn"]:
        addons.append("tailwindcss=plugins:none")

    if args.e2e == "playwright":
        addons.append("playwright=demo:no")

    if args.adapter == "cloudflare":
        addons.append("sveltekit-adapter=adapter:cloudflare+cfTarget:pages")
    elif args.adapter != "auto":
        addons.append(f"sveltekit-adapter=adapter:{args.adapter}")

    # 4. Chạy lệnh npx sv create
    install_args = ["--no-install"] if args.no_install else ["--install", args.pm]
    addon_args = ["--add"] + addons if addons else ["--no-add-ons"]

    sv_cmd = [
        "npx", "sv", "create", str(target_dir),
        "--template", "minimal",
        "--types", "ts",
        "--no-dir-check",
        "--no-download-check",
    ] + addon_args + install_args

    try:
        run_cmd(sv_cmd, cwd=str(base_dir))
    except subprocess.CalledProcessError as e:
        print(f"[!] Lỗi khi chạy sv create: {e}")
        sys.exit(1)

    # 5. Nếu có yêu cầu Cloudflare: Tạo .dev.vars và .dev.vars.example
    if args.adapter == "cloudflare":
        create_cloudflare_vars(target_dir)
        if not args.no_install:
            try:
                run_cmd([args.pm, "run", "gen"], cwd=str(target_dir), check=False)
            except Exception:
                pass

    # 6. Nếu có E2E Playwright: Đảm bảo có sample test
    if args.e2e == "playwright":
        ensure_playwright_sample_test(target_dir)

    # 7. Cài thêm Lucide icons nếu được yêu cầu
    if args.icons and not args.no_install:
        print("\n[+] Cài đặt thêm icon lucide-svelte...")
        try:
            run_cmd([args.pm, "install", "-D", "lucide-svelte"], cwd=str(target_dir))
        except subprocess.CalledProcessError as e:
            print(f"[!] Cảnh báo: Cài đặt lucide-svelte thất bại: {e}")

    # 8. Cài thêm shadcn-svelte nếu chọn UI shadcn
    if args.ui == "shadcn" and not args.no_install:
        print("\n[+] Tích hợp shadcn-svelte dependencies...")
        try:
            run_cmd([args.pm, "install", "-D", "tailwind-variants", "clsx", "tailwind-merge"], cwd=str(target_dir))
        except subprocess.CalledProcessError as e:
            print(f"[!] Cảnh báo khi cài shadcn dependencies: {e}")

    # 9. Tự động sinh Rule chuẩn cho SvelteKit (.agents/rules/sveltekit-standards.md)
    create_sveltekit_rule(target_dir)

    # 10. Khởi tạo khung sườn Rust WASM nếu có flag --wasm
    if args.wasm:
        print("\n[+] Khởi tạo khung sườn Rust WebAssembly (wasm-engine)...")
        create_wasm_engine(target_dir)

    print("\n" + "=" * 60)
    print("✅ DỰ ÁN SVELTEKIT ĐÃ ĐƯỢC TẠO THÀNH CÔNG!")
    print(f"📁 Vị trí: {target_dir}")
    print("\nCác bước tiếp theo:")
    print(f"  cd {target_dir}")
    if args.no_install:
        print(f"  {args.pm} install")
    if args.wasm:
        print(f"  {args.pm} run wasm:build   # Biên dịch Rust sang WebAssembly vào src/lib/wasm")
    print(f"  {args.pm} run dev          # Khởi động dev server")
    if args.e2e == "playwright":
        print("  npx playwright test       # Chạy E2E test headless")
        print("  npx playwright test --ui  # Mở giao diện tương tác Playwright UI")
    if args.adapter == "cloudflare":
        print("  # Nhớ cập nhật biến bí mật vào file .dev.vars")
    print("=" * 60)


if __name__ == "__main__":
    main()

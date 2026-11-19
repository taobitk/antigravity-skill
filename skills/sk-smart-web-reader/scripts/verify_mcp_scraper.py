"""Verification script for sk-smart-web-reader skill.
Checks MCP configuration and server status for firecrawl and puppeteer.
"""
import json
import os
import subprocess
import sys
import urllib.request

def check_mcp_config():
    config_path = os.path.expanduser("~/.gemini/config/mcp_config.json")
    print(f"[*] Checking MCP configuration: {config_path}")
    if not os.path.exists(config_path):
        print("[-] Error: mcp_config.json not found!")
        return False
    
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    servers = data.get("mcpServers", {})
    firecrawl_ok = "firecrawl" in servers and not servers["firecrawl"].get("disabled", False)
    puppeteer_ok = "puppeteer" in servers and not servers["puppeteer"].get("disabled", False)

    print(f"  - firecrawl configured: {'[PASS]' if firecrawl_ok else '[FAIL]'}")
    print(f"  - puppeteer configured: {'[PASS]' if puppeteer_ok else '[FAIL]'}")
    return firecrawl_ok and puppeteer_ok

def check_firecrawl_endpoint():
    endpoint = "https://mcp.firecrawl.dev/v2/mcp"
    print(f"[*] Checking Firecrawl remote endpoint connectivity: {endpoint}")
    try:
        req = urllib.request.Request(endpoint, headers={"User-Agent": "AntigravityVerification/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            status = resp.status
            print(f"  - Endpoint responded with status: {status} [PASS]")
            return True
    except Exception as e:
        # A 400, 404, or 405 from an MCP JSON-RPC/SSE endpoint still means the host is alive and reachable
        err_str = str(e)
        if "HTTP Error" in err_str or "40" in err_str:
            print(f"  - Endpoint reachable (response: {err_str}) [PASS]")
            return True
        print(f"  - Warning connecting to endpoint: {e}")
        return False

def check_cli_mcp_list():
    agy_path = os.path.expanduser("~/.gemini/bin/agy.exe")
    print(f"[*] Running CLI verification via: {agy_path}")
    if not os.path.exists(agy_path):
        print("[-] agy.exe not found at expected path")
        return False
    
    res = subprocess.run([agy_path, "mcp", "list"], capture_output=True, text=True)
    if res.returncode == 0:
        print("  - agy mcp list output:")
        for line in res.stdout.strip().splitlines():
            print(f"    {line}")
        return "firecrawl" in res.stdout and "puppeteer" in res.stdout
    else:
        print(f"[-] CLI command failed: {res.stderr}")
        return False

def main():
    print("=" * 60)
    print("  VERIFYING SK-SMART-WEB-READER SETUP")
    print("=" * 60)
    
    c1 = check_mcp_config()
    c2 = check_firecrawl_endpoint()
    c3 = check_cli_mcp_list()
    
    print("=" * 60)
    if c1 and c2 and c3:
        print("[SUCCESS] All checks passed! Web scraping tools are ready to use.")
        return 0
    else:
        print("[WARNING] Some checks reported issues. Please review logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())


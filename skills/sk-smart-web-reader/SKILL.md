---
name: sk-smart-web-reader
description: >-
  Smart web scraping and content extraction using Firecrawl MCP and Puppeteer MCP.
  Use when the user provides a URL to read documentation, analyze articles, crawl sites,
  or test and interact with live web UIs.
---

# Smart Web Reader (`sk-smart-web-reader`)

Guides tool selection between **Firecrawl MCP** and **Puppeteer MCP** for reading, scraping, or interacting with static, SPA, or interactive web pages.

## 1. Tool Selection Policy

| Goal / Scenario | Preferred Tool | Rationale |
| :--- | :--- | :--- |
| **Read docs, technical guides, articles, blogs** | `firecrawl` (`scrape`) | Lightweight cloud extraction; converts pages into clean Markdown without nav/ad noise. |
| **Crawl a sitemap or linked sub-pages** | `firecrawl` (`crawl`) | Crawls across a domain and outputs structured Markdown. |
| **UI interaction (clicks, forms, complex scrolling)** | `puppeteer` | Drives a real browser directly to simulate user interactions. |
| **Capture UI screenshots** | `puppeteer` (`screenshot`) | Captures actual browser-rendered layout. |
| **Test local environments (`localhost` / `127.0.0.1`)** | `puppeteer` / `curl` | Firecrawl cloud cannot reach local loopback addresses. |

## 2. 3-Step Workflow

1. **Classify Target**:
   - Localhost or requires UI interaction/screenshots -> **Puppeteer**.
   - Public docs, blogs, or multi-page static/SPA content -> **Firecrawl**.
2. **Extract & Clean**:
   - Invoke the corresponding MCP tool to obtain clean Markdown or DOM/screenshot state.
3. **Deliver Output**:
   - Summarize, analyze, or save the extracted content as requested.

## 3. Verification

Verify both MCP servers' configuration status using [`verify_mcp_scraper.py`](./scripts/verify_mcp_scraper.py):

```powershell
python "C:\Users\8hung\.gemini\config\skills\sk-smart-web-reader\scripts\verify_mcp_scraper.py"
```

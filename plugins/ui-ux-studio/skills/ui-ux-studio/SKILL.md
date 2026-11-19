---
name: ui-ux-studio
description: >-
  End-to-end UI/UX workflow router combining product discovery, strategic UX architecture,
  and implementation-ready design systems. Use when designing a new feature, planning user flows,
  auditing accessibility, or generating palettes, typography, and component styles across
  sk-customer-ux-interviewer, ui-ux-designer, and ui-ux-pro-max.
---

# UI/UX Design Studio (`ui-ux-studio`)

Entrypoint router for the `ui-ux-studio` plugin. Follow the 3-stage workflow in order for new features, or jump directly to the stage matching the user's request.

## Workflow & Skill Routing

| Stage | Skill to Load | When to Use |
| :--- | :--- | :--- |
| **1. Discovery & Requirements** | [sk-customer-ux-interviewer](../sk-customer-ux-interviewer/SKILL.md) | **Start here** for new feature requests: clarify user intent, screen space (Modal/Drawer/Inline), edge cases, and present 2-3 trade-off options before coding. |
| **2. UX Strategy & Accessibility** | [ui-ux-designer](../ui-ux-designer/SKILL.md) | Define user journey flows, information architecture, wireframes, high-level design tokens, and WCAG 2.1/2.2 AA/AAA audits. |
| **3. Visual System & Implementation** | [ui-ux-pro-max](../ui-ux-pro-max/SKILL.md) | Generate concrete color palettes, font pairings, UI styles, chart specs, and stack-specific (Svelte, Tailwind, React, etc.) styling guidelines. |

## Quick Design System Generation

To generate a complete design system via `ui-ux-pro-max`, run:

```powershell
python "C:\Users\8hung\.gemini\config\plugins\ui-ux-studio\skills\ui-ux-pro-max\scripts\search.py" "<product_type> <industry> <keywords>" --design-system -p "Project Name"
```

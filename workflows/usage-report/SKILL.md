## usage-report

Purpose: Query token allowance and usage for the team tied to the current API key — pre-flight checks or admin reports only; produces no content.

When to use:
- Pre-flight before large jobs: “Can we still run research-agent?” → action=check
- Admin reporting: “How many tokens did we use this month?” → action=count
- Agent orchestration: auto-guard before expensive workflows

When NOT to use:
- Any content production (research, reading, memory) — use **research-agent**, **deep-reading**, or **remember-and-recall**
- Substitute for Host LLM chat or reasoning — smart_budget_guard is not a completion API
- Record per-task consumption — runtime uses action=record after tool calls (out of scope for this workflow)

Returns: JSON string. `check`: `data.allowed` (boolean), `data.remaining`, `data.limit`, `data.used`. `count`: `data.used`, `data.period`, `data.breakdown` (by tool or time bucket, if present).

Composes with: loader or Host calls check before **research-agent** / **deep-reading**; show count results directly to admins.

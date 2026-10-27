# SmartGate

<a href="https://smartgate.network">
  <img src="https://smartgate.network/og.jpg" width="640" alt="SmartGate — the intelligence layer between AI and the world">
</a>

**AI Intelligence Layer — not another assistant or LLM proxy.**

Official [Cursor](https://cursor.com) plugin for **[SmartGate](https://smartgate.network)**.

[SmartGate](https://smartgate.network) is the intelligence layer between AI and the world — helping you research, understand, remember, and act before runaway tool traffic becomes a surprise invoice.

On the surface: [Smart Research](https://smartgate.network/solutions), decisions, knowledge, and monitoring — no MCP required. Under the hood: an MCP-native algorithmic gateway with five capabilities (Research, Context, Memory, Control, Pipeline) powered by seven `smart_*` primitives. Human interface (Web) + agent interface (MCP/API). Not a chatbot, search app, or model router. Cursor stays the host model.

Plugin mark for Cursor Marketplace is the 1:1 shield [`assets/logo.png`](assets/logo.png). The banner is the official site OG card.

## What is SmartGate MCP

Don't rebuild research infrastructure for every agent. Connect once over Streamable HTTP; the gateway fetches, searches, compresses, deduplicates, remembers, and hard-caps tool traffic before it reaches your model provider.

| Capability | What the agent does | Product |
|------------|---------------------|---------|
| Research | Find sources, then read pages as Markdown | [Traffic Customs](https://smartgate.network/features/traffic-customs) |
| Context | Dedup overlapping hits, then compress | [Token Control](https://smartgate.network/features/token-control) |
| Memory | Persist and recall team facts across sessions | [Features](https://smartgate.network/features) |
| Control | Check, count, and cap token budget | [Token Control](https://smartgate.network/features/token-control) |
| Pipeline | Run research / read / remember as one job | [Tools](https://smartgate.network/docs/tools) |

- Product: [smartgate.network](https://smartgate.network) · [Features](https://smartgate.network/features) · [Pricing](https://smartgate.network/pricing)
- Connect: [Quick start](https://smartgate.network/docs/installation) · [Connect](https://smartgate.network/docs/connect) · [MCP endpoint](https://smartgate.network/docs/mcp-endpoint)
- Reference: [Tools](https://smartgate.network/docs/tools) · [Security](https://smartgate.network/docs/security) · [llms.txt](https://smartgate.network/llms.txt)
- Compliance: [Audit](https://smartgate.network/features/audit-compliance) · [Privacy](https://smartgate.network/privacy) · [Terms](https://smartgate.network/terms)

## Install

1. Install **SmartGate** from the [Cursor Marketplace](https://cursor.com/marketplace), or import this repo under **Cursor Dashboard → Plugins → Team Marketplaces → Import from Repo**: `https://github.com/smartgate-network/smartgate-workflows`
2. Open **Plugins → SmartGate → Configure** and set `SMARTGATE_API_KEY`
3. Restart Cursor (or reload the window) so the MCP handshake runs again

Mint a key at [Dashboard → API Keys](https://smartgate.network) (`sk_live_…`). Never paste the key into chat or commit it.

## First run

After the MCP server shows as connected, try:

```text
Check my SmartGate token allowance with smart_budget_guard action=check.
```

```text
smart_fetch https://smartgate.network/docs/tools then summarize Token Control, Traffic Customs, and Audit.
```

```text
Remember: our staging API rate limit is 100 req/min
```

Live `tools/list` schemas (purpose, params, returns) come from the hosted server, not this repo. Names are `smart_*` — there is no `smartgate_compress_context`. Full reference: [Docs → Tools](https://smartgate.network/docs/tools).

## Tools (reviewer cheat sheet)

Every tool returns a **JSON string**. Parse it before synthesizing. Do not invent page content.

| Tool | Required | Optional | Returns |
|------|----------|----------|---------|
| `smart_search` | `query` | `max_results` (1–50, default 10) | Search hits (`results[].url`, `snippet`) |
| `smart_fetch` | `url` (http/https) | `timeout` (default 30s) | Page `markdown`, `title`, `url` |
| `smart_dedup` | `texts` (string[]) | `threshold` (0–1, default 0.9) | Kept / removed indices or deduped texts |
| `smart_context_gate` | `text` | `ratio` (default 0.5), `purpose` | `compressed`, `ratio`, token counts |
| `smart_budget_guard` | `action`: `check` \| `count` \| `record` | `text` / `tokens` by action | Allowance, usage, or record ack |
| `smart_memory` | `action`: `add` \| `search` \| `get` \| `delete` | `text` (add), `query` (search), `memory_id` (get/delete) | Shape depends on action |
| `smart_pipe` | `template` **or** `steps` | `query`, `url`, `text` | Per-step results. Templates: `research`, `read`, `remember`. Not for a single step. |

Skills shipped with this plugin:

| Skill | Routes |
|-------|--------|
| `smartgate-workflows` | Pick the right workflow |
| `smartgate-research-agent` | Multi-source research |
| `smartgate-deep-reading` | One known URL |
| `smartgate-remember-and-recall` | Team memory |
| `smartgate-usage-report` | Quota / usage (no content) |

## Configure

**Marketplace install:** Plugins → SmartGate → Configure → `SMARTGATE_API_KEY`. The plugin `mcp.json` already uses `${SMARTGATE_API_KEY}`. Do not commit a real key.

**Manual / reviewer fallback** (only if you are not using the plugin): merge this into `~/.cursor/mcp.json` (user) or `<project>/.cursor/mcp.json` (project), then restart Cursor. Replace the placeholder. If the plugin is also installed, delete this block so tools are not duplicated.

```json
{
  "mcpServers": {
    "smartgate": {
      "type": "streamable-http",
      "url": "https://smartgate.network/api/mcp",
      "headers": {
        "Authorization": "Bearer sk_live_REPLACE_WITH_YOUR_KEY",
        "X-SmartGate-Agent-Platform": "cursor"
      }
    }
  }
}
```

Hosted endpoint: `POST https://smartgate.network/api/mcp` (Streamable HTTP). Mint a key at [Dashboard → API Keys](https://smartgate.network).

## Data handling

This plugin does not run fetch, search, compression, or memory inside Cursor. Those steps run on the **hosted** gateway at `https://smartgate.network/api/mcp`. Cursor stays the host model.

- **In transit:** HTTPS + `Authorization: Bearer`. The plugin ships no secrets; you set `SMARTGATE_API_KEY` in Plugins → Configure.
- **At rest:** we store a **hash** of API keys, not the raw secret. Teams are isolated by the key's tenant. Do not pass a foreign `team_id`.
- **What is logged:** tool name, timestamp, token counts, and for fetch the **requested URL**. Retention: Free 7 days · Pro 30 · Teams 90 · Enterprise 180. See [Security](https://smartgate.network/docs/security) and [Logs](https://smartgate.network/docs/logs).
- **Compression / dedup:** `smart_context_gate` (LLMLingua) and `smart_dedup` (SemHash) run on SmartGate servers, not locally. They shrink or drop overlapping text; they are **not** a PII redaction product. Do not put secrets or credentials in tool arguments or memory.
- **What we do not do:** we are not an LLM proxy and do not train a public chatbot on your prompts as a consumer product. Billing card data is handled by Paddle, not stored by us.

[Privacy Policy](https://smartgate.network/privacy) · [Terms](https://smartgate.network/terms) · [SECURITY.md](SECURITY.md) · [support@smartgate.network](mailto:support@smartgate.network)

## Troubleshooting

| Symptom | Check |
|---------|--------|
| 401 Unauthorized | `SMARTGATE_API_KEY` is set in Plugins → Configure; key is `sk_live_…` |
| Tools empty | Restart Cursor so `initialize` / `tools/list` run |
| 405 on GET | Endpoint is **POST** `/api/mcp`, not GET SSE |
| Duplicate tools | Remove a hand-written `smartgate` block from `~/.cursor/mcp.json` |

## Workflow source

`workflows/` is the scenario source (YAML + Markdown). `skills/` is the committed Cursor pack, generated by:

```bash
pip install jsonschema pyyaml
python scripts/install-skills.py --client cursor --target skills --force
python tests/validate.py
```

| Workflow | Description |
|----------|-------------|
| [research-agent](workflows/research-agent/) | search → fetch → dedup → compress |
| [deep-reading](workflows/deep-reading/) | fetch → compress |
| [remember-and-recall](workflows/remember-and-recall/) | team memory |
| [usage-report](workflows/usage-report/) | budget check / count |

Manual skill install (no Marketplace): see [clients/README.md](clients/README.md).

## Maintainers

[SmartGate](https://smartgate.network) · [support@smartgate.network](mailto:support@smartgate.network)

## License

[MIT](LICENSE)

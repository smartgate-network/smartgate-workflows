# SmartGate

<a href="https://smartgate.network">
  <img src="https://smartgate.network/og.svg" alt="SmartGate — the intelligence layer between AI and the world" width="640">
</a>

Official [Cursor](https://cursor.com) plugin for **[SmartGate](https://smartgate.network)** — the intelligence layer between AI and the world.

Marketplace icon stays the 1:1 shield at [`assets/logo.png`](assets/logo.png) (Cursor requires a square plate). The banner above is the site OG card, not the plugin mark.

## What is SmartGate MCP

[SmartGate](https://smartgate.network) is an **MCP-native algorithmic gateway**, not a chatbot, search app, or model router. You keep Cursor (or Claude, Windsurf, OpenClaw) as the host model. SmartGate sits between the agent and the open web so the agent can research, understand, remember, and act without dumping raw pages into a billed context window.

On the surface: [Smart Research](https://smartgate.network/solutions), decisions, knowledge, and monitoring. Under the hood: five intelligence capabilities powered by seven `smart_*` primitives — not seven products.

| Capability | Primitives | Product surface |
|------------|------------|-----------------|
| Research | `smart_search` + `smart_fetch` | [Traffic Customs](https://smartgate.network/features/traffic-customs) |
| Context | `smart_dedup` + `smart_context_gate` | [Token Control](https://smartgate.network/features/token-control) |
| Memory | `smart_memory` | [Features](https://smartgate.network/features) |
| Control | `smart_budget_guard` | [Token Control](https://smartgate.network/features/token-control) |
| Pipeline | `smart_pipe` | [Docs → Tools](https://smartgate.network/docs/tools) |

Developer promise: **don't rebuild research infrastructure for every agent.** One Streamable HTTP origin, Bearer auth, team-scoped audit.

- Product: [smartgate.network](https://smartgate.network) · [Features](https://smartgate.network/features) · [Pricing](https://smartgate.network/pricing)
- Connect: [Quick start](https://smartgate.network/docs/installation) · [Connect guide](https://smartgate.network/docs/connect) · [MCP endpoint](https://smartgate.network/docs/mcp-endpoint)
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
Check my SmartGate token allowance, then research RAG evaluation methods. Do not invent sources.
```

```text
Read https://smartgate.network/docs/tools and summarize Token Control, Traffic Customs, and Audit.
```

```text
Remember: our staging API rate limit is 100 req/min
```

## What the agent can call

| Tool | When |
|------|------|
| `smart_search` | Research with no definitive URL |
| `smart_fetch` | User gave an http(s) URL — return Markdown |
| `smart_dedup` | Overlapping passages / search hits |
| `smart_context_gate` | Shrink long text before the host model |
| `smart_budget_guard` | `check` / `count` before costly work; `record` after |
| `smart_memory` | Team memory: `add` (`text`), `search`, `get`, `delete` |
| `smart_pipe` | Multi-step only (`research` / `read` / `remember`) |

Skills shipped with this plugin:

| Skill | Routes |
|-------|--------|
| `smartgate-workflows` | Pick the right workflow |
| `smartgate-research-agent` | Multi-source research |
| `smartgate-deep-reading` | One known URL |
| `smartgate-remember-and-recall` | Team memory |
| `smartgate-usage-report` | Quota / usage (no content) |

## Configure (mcp.json)

Hosted endpoint: `POST https://smartgate.network/api/mcp` (Streamable HTTP). The plugin injects the key via `${SMARTGATE_API_KEY}`:

```json
{
  "mcpServers": {
    "smartgate": {
      "type": "streamable-http",
      "url": "https://smartgate.network/api/mcp",
      "headers": {
        "Authorization": "Bearer ${SMARTGATE_API_KEY}",
        "X-SmartGate-Agent-Platform": "cursor"
      }
    }
  }
}
```

Already have a manual `smartgate` entry in `~/.cursor/mcp.json`? Remove it before installing the plugin so tools are not duplicated.

## Security

Tool calls send the URLs, queries, and text you provide to SmartGate. Do not commit secrets. Report issues to [support@smartgate.network](mailto:support@smartgate.network).

[Privacy](https://smartgate.network/privacy) · [Terms](https://smartgate.network/terms) · [SECURITY.md](SECURITY.md)

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

## License

[MIT](LICENSE)

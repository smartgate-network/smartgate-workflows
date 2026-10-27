# Security

Report vulnerabilities to [support@smartgate.network](mailto:support@smartgate.network). Do not file public issues that include API keys or customer data.

This plugin does not ship secrets. Users set `SMARTGATE_API_KEY` in the host's plugin configure dialog. Cursor substitutes it into `mcp.json` as `${SMARTGATE_API_KEY}`. Claude substitutes it into `.mcp.json` as `${user_config.SMARTGATE_API_KEY}`. Both send `Authorization: Bearer` to `https://smartgate.network/api/mcp`.

## Data handling (short)

Tool execution is **hosted**, not local: fetch, search, LLMLingua compression, SemHash dedup, budget, and team memory run on SmartGate. Cursor or Claude remains the host model. We store hashed API keys, team-scoped audit rows (tool name, time, token counts, fetch URLs), and memory payloads you explicitly `add`. Retention follows the plan catalog (7 / 30 / 90 / 180 days). There is no general PII-redaction filter — do not send secrets in tool arguments.

- [Privacy Policy](https://smartgate.network/privacy)
- [Terms of Service](https://smartgate.network/terms)
- [Security docs](https://smartgate.network/docs/security)
- [MCP endpoint](https://smartgate.network/docs/mcp-endpoint)

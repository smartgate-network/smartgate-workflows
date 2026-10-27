# Security

Report vulnerabilities to [support@smartgate.network](mailto:support@smartgate.network). Do not file public issues that include API keys or customer data.

This plugin does not ship secrets. Users set `SMARTGATE_API_KEY` in Cursor → Plugins → Configure. The value is substituted into `mcp.json` as `Authorization: Bearer ${SMARTGATE_API_KEY}` and sent to `https://smartgate.network/api/mcp`.

- [Privacy Policy](https://smartgate.network/privacy)
- [Terms of Service](https://smartgate.network/terms)
- [MCP endpoint](https://smartgate.network/docs/mcp-endpoint)

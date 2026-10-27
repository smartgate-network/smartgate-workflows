# Install SmartGate MCP

Do **not** clone this repo and run a local MCP server. SmartGate is a hosted Streamable HTTP gateway.

1. Mint a key at [Dashboard → API Keys](https://smartgate.network). It looks like `sk_live_…`.
2. Point the host at `https://smartgate.network/api/mcp` with a Bearer header. Replace the placeholder:

```json
{
  "mcpServers": {
    "smartgate": {
      "type": "streamable-http",
      "url": "https://smartgate.network/api/mcp",
      "headers": {
        "Authorization": "Bearer sk_live_REPLACE_WITH_YOUR_KEY",
        "X-SmartGate-Agent-Platform": "cline"
      }
    }
  }
}
```

3. Docs: [Connect](https://smartgate.network/docs/connect)
4. A request without `Authorization` returns **401**. That is expected.

Official MCP Registry name: `network.smartgate/smartgate`.

## API Reference 精读

用户意图: 精读 Stripe API 官方 OpenAPI 文档，提取 rate limit 相关说明

调用参数:

```json
{
  "url": "https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.yaml",
  "ratio": 0.3,
  "goal": "rate limits and throttling"
}
```

预期输出结构:
- `results[0].data` — 抓取结果，含 `markdown`、`url`、`title`
- `results[1].data` — 压缩结果，含 `compressed`、`ratio`、`original_tokens`、`compressed_tokens`

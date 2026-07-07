## API reference deep-read

User intent: Deep-read Stripe’s official OpenAPI spec and extract rate-limit guidance

Invocation params:

```json
{
  "url": "https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.yaml",
  "ratio": 0.3,
  "goal": "rate limits and throttling"
}
```

Expected output shape:
- `results[0].data` — fetch result with `markdown`, `url`, `title`
- `results[1].data` — compression with `compressed`, `ratio`, `original_tokens`, `compressed_tokens`

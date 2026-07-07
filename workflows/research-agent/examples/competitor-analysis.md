## Competitor analysis: Notion vs Obsidian

User intent: Compare Notion and Obsidian core features and pricing in 2026

Invocation params:

```json
{
  "query": "Notion vs Obsidian comparison features pricing 2026",
  "max_results": 5,
  "goal": "pricing and core features"
}
```

Expected output shape:
- `results[0].data.results[]` — search hits with `url`, `title`, `snippet`
- `results[1].data` — batch fetch array; each item has `url`, `markdown`
- `results[2].data` — dedup output with `deduped_text`, `removed_count`, `kept_indices`
- `results[3].data` — final compression with `compressed`, `ratio`, `original_tokens`, `compressed_tokens`

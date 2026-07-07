## Academic survey: RAG evaluation methods

User intent: Collect recent survey material on RAG evaluation metrics and benchmarks

Invocation params:

```json
{
  "query": "RAG evaluation metrics benchmark survey",
  "max_results": 8,
  "dedup_threshold": 0.85,
  "ratio": 0.35,
  "goal": "evaluation metrics and benchmarks"
}
```

Expected output shape:
- `results[0].data.results[]` — search hits (papers, blogs, etc.)
- `results[1].data` — full-page markdown per source
- `results[2].data` — semantically deduped `deduped_text` and `removed_count`
- `results[3].data` — goal-filtered, compressed `compressed` text

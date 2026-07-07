## 竞品分析：Notion vs Obsidian

用户意图: 对比 Notion 与 Obsidian 在 2026 年的核心功能与定价策略

调用参数:

```json
{
  "query": "Notion vs Obsidian comparison features pricing 2026",
  "max_results": 5,
  "goal": "pricing and core features"
}
```

预期输出结构:
- `results[0].data.results[]` — 搜索命中，每项含 `url`、`title`、`snippet`
- `results[1].data` — 批量抓取结果数组，每项含 `url`、`markdown`
- `results[2].data` — 去重结果，含 `deduped_text`、`removed_count`、`kept_indices`
- `results[3].data` — 最终压缩，含 `compressed`、`ratio`、`original_tokens`、`compressed_tokens`

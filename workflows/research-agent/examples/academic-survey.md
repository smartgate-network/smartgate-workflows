## 学术综述：RAG 评估方法

用户意图: 收集 RAG 系统评估指标与 benchmark 的最新综述材料

调用参数:

```json
{
  "query": "RAG evaluation metrics benchmark survey",
  "max_results": 8,
  "dedup_threshold": 0.85,
  "ratio": 0.35,
  "goal": "evaluation metrics and benchmarks"
}
```

预期输出结构:
- `results[0].data.results[]` — 学术论文、技术博客等搜索命中
- `results[1].data` — 各来源全文 markdown 数组
- `results[2].data` — 语义去重后的 `deduped_text` 与 `removed_count`
- `results[3].data` — 按 goal 预筛并压缩的 `compressed` 正文

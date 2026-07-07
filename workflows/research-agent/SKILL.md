## research-agent

Purpose: 在没有明确 URL 时，从多个网页来源收集、去重并压缩材料，产出可供 Host LLM 直接分析的结构化调研摘要。

When to use:
- 竞品分析：对比多个产品的功能、定价、市场定位
- 行业研究：汇总某领域近期新闻、报告、趋势
- 学术/技术调研：收集某主题的论文摘要、技术博客、方案对比
- 新闻汇总：围绕事件或关键词聚合多方报道

When NOT to use:
- 用户已提供确定的 http(s) URL — 使用 **deep-reading** 单链精读，避免多余搜索开销
- 只需存取团队已有结论 — 使用 **remember-and-recall**
- 查询 token 额度或用量 — 使用 **usage-report**

Returns: JSON 字符串（由 loader 解析）。顶层含 `success`、`results`（逐步结果数组）。最终步 `smart_context_gate` 的 `data` 含 `compressed`（压缩正文）、`ratio`（压缩比）、`original_tokens` / `compressed_tokens`。前序步含 `results[].url`、`results[].snippet`（搜索）、抓取页的 `markdown`、去重后的 `deduped_text` / `removed_count`。

Composes with: Host LLM 做综合分析、写报告；结论可经 **remember-and-recall**（action=add）持久化；大任务前可先 **usage-report**（action=check）预检额度。

## deep-reading

Purpose: 对用户已知的单个 URL 进行抓取与压缩，产出精简正文供 Host LLM 精读、摘要或问答。

When to use:
- 官方文档/API Reference：OpenAPI spec、SDK 文档、产品手册
- 长博客/技术文章：单篇深度阅读的输入预处理
- 白皮书/RFC：压缩后交给 LLM 提取章节要点
- 用户消息中已含明确链接，无需再搜索

When NOT to use:
- 没有确定 URL、需要从多个来源调研 — 使用 **research-agent**
- 要把结论存入团队记忆 — 先用本 workflow 读取，再 **remember-and-recall**（action=add）
- 查询额度 — 使用 **usage-report**

Returns: JSON 字符串。Loader 以 `template=read` 调用 `smart_pipe` 时，顶层含 `success`、`results`。`results[0]` 为 fetch：`data.markdown` / `data.title` / `data.url`。`results[1]` 为 context_gate：`data.compressed`、`data.ratio`、`data.original_tokens`、`data.compressed_tokens`。

Composes with: Host LLM 生成摘要、问答、代码示例；产出可写入 **remember-and-recall**；过长页面可先 **usage-report**（action=check）。

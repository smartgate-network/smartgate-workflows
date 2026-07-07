## remember-and-recall

Purpose: 在团队维度持久化或检索跨会话事实、调研结论与配置备忘，供后续对话 grounding。

When to use:
- 存入结论：「记住我们的 prod API 限流是 100 req/min」
- 语义检索：「我们之前关于 Langfuse 的调研记了什么」
- 按 ID 读取：已知 `memory_id` 时精确获取单条
- 删除过时条目：清理错误或过期的团队记忆

When NOT to use:
- 抓取或搜索网页内容 — 使用 **research-agent** 或 **deep-reading**
- 查询 token 额度 — 使用 **usage-report**
- 通用世界知识问答（非团队私有事实）— 直接由 Host LLM 回答，无需本 workflow

Returns: JSON 字符串，结构随 `action` 变化。`add`：`data.memory_id`、`data.status`。`search`：`data.memories[]`（含 `id`、`content`、`score`、`created_at`）。`get`：`data.memory`（单条完整记录）。`delete`：`data.deleted`、`data.memory_id`。

Composes with: **research-agent** 产出经 Host LLM 整理后 action=add 写入；Host LLM 用 search 结果做 grounding；与 **deep-reading** 串联：先读 URL，再 add 摘要。

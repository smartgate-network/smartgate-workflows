## usage-report

Purpose: 查询当前 API key 所属团队的 token 额度与使用情况，用于任务前预检或管理报表，不产出任何内容材料。

When to use:
- 大任务前预检：「还能跑 research-agent 吗」→ action=check
- 管理报表：「本月用了多少 token」→ action=count
- Agent 编排时在 expensive workflow 前自动 guard

When NOT to use:
- 任何内容生产：调研、阅读、记忆 — 分别用 **research-agent**、**deep-reading**、**remember-and-recall**
- 替代 Host LLM 对话或推理 — smart_budget_guard 不是 completion API
- 记录单次任务消耗 — 由 runtime 在工具调用后 action=record（非本 workflow 范围）

Returns: JSON 字符串。`check`：`data.allowed`（boolean）、`data.remaining`、`data.limit`、`data.used`。`count`：`data.used`、`data.period`、`data.breakdown`（按工具或时间粒度，若有）。

Composes with: 在 **research-agent** / **deep-reading** 前由 loader 或 Host 自动调用 check；管理面向用户直接展示 count 结果。

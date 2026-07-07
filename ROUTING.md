# Workflow Routing Guide

给定用户的自然语言意图，选择应调用的 workflow。Host LLM 或 CLI loader 可据此路由。

## 意图 → Workflow 映射

| 用户意图（示例） | Workflow | 典型 params |
|------------------|----------|-------------|
| 「帮我调研一下 Notion 竞品」 | research-agent | `{ "query": "Notion 竞品分析" }` |
| 「2026 年 AI Agent 行业有什么新动态」 | research-agent | `{ "query": "AI Agent 行业动态 2026" }` |
| 「帮我做一篇关于 RAG 评估方法的学术综述」 | research-agent | `{ "query": "RAG evaluation methods survey" }` |
| 「读一下这个链接 https://…」 | deep-reading | `{ "url": "https://…" }` |
| 「总结这篇 RFC / 白皮书的内容」 | deep-reading | `{ "url": "https://…", "goal": "核心结论" }` |
| 「精读这份 OpenAPI 官方文档」 | deep-reading | `{ "url": "https://…/openapi.json" }` |
| 「记住：我们的 API 限流是 100 req/min」 | remember-and-recall | `{ "action": "add", "content": "…" }` |
| 「我们之前调研 Langfuse 记了什么」 | remember-and-recall | `{ "action": "search", "query": "Langfuse" }` |
| 「团队还剩多少 token 额度」 | usage-report | `{ "action": "check" }` |
| 「查一下本月 token 用量」 | usage-report | `{ "action": "count" }` |

## 冲突取舍规则

当意图同时匹配多个 workflow 时，按以下**优先级从高到低**判断：

1. **管理/额度类** — 含「额度」「token」「budget」「用量」「剩余」→ **usage-report**（即使句中含 URL）
2. **记忆类** — 含「记住」「回忆」「上次」「团队记忆」「存一下」→ **remember-and-recall**
3. **有明确 http(s) URL** — → **deep-reading**
4. **无 URL、需多方信息** — → **research-agent**
5. **research vs deep-reading 均无 URL** — → **research-agent**

### 边界速查

| 场景 | 选 | 不选 | 原因 |
|------|-----|------|------|
| 用户给了文档链接 | deep-reading | research-agent | 已知 URL，无需搜索 |
| 用户只给主题没给链接 | research-agent | deep-reading | 需先搜索发现来源 |
| 用户要存结论供下次用 | remember-and-recall | research-agent | 持久化，非一次性调研 |
| 用户问额度而非内容 | usage-report | 其他全部 | 纯管理操作 |

## 决策树

```
用户请求
  ├─ 含额度/token/用量关键词? ──yes──► usage-report
  ├─ 含记忆/记住/回忆关键词? ──yes──► remember-and-recall
  ├─ 含 http(s) URL? ──yes──► deep-reading
  └─ 否则 ──► research-agent
```

## 新增 workflow 时

1. 在上方表格添加至少 2 行典型意图
2. 更新冲突规则，说明与现有 workflow 的优先级关系
3. 在 PR 描述中解释「When NOT to use」与相邻 workflow 的差异

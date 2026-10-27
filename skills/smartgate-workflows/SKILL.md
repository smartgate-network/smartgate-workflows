---
name: smartgate-workflows
description: >
  Routes SmartGate workflow intents to the correct scenario skill. Use for web research, deep-read URL, team memory, or token quota routing.
---

Prerequisite: SmartGate MCP must be configured.

Invoke the matching workflow skill after routing.

# Workflow Routing Guide

Given a user’s natural-language intent, choose the workflow to invoke. Host LLMs or CLI loaders route using this guide.

## Intent → Workflow mapping

| Example user intent | Workflow | Typical params |
|---------------------|----------|----------------|
| “Research Notion competitors for me” | research-agent | `{ "query": "Notion competitor analysis" }` |
| “What’s new in the AI Agent space in 2026?” | research-agent | `{ "query": "AI Agent industry trends 2026" }` |
| “Help me survey RAG evaluation methods” | research-agent | `{ "query": "RAG evaluation methods survey" }` |
| “Read this link https://…” | deep-reading | `{ "url": "https://…" }` |
| “Summarize this RFC / whitepaper” | deep-reading | `{ "url": "https://…", "goal": "key conclusions" }` |
| “Deep-read this OpenAPI spec” | deep-reading | `{ "url": "https://…/openapi.json" }` |
| “Remember: our API rate limit is 100 req/min” | remember-and-recall | `{ "action": "add", "content": "…" }` |
| “What did we note about Langfuse?” | remember-and-recall | `{ "action": "search", "query": "Langfuse" }` |
| “How much token quota do we have left?” | usage-report | `{ "action": "check" }` |
| “Show this month’s token usage” | usage-report | `{ "action": "count" }` |

## Conflict resolution

When an intent matches multiple workflows, apply these rules **in priority order**:

1. **Admin / quota** — mentions quota, token, budget, usage, remaining, allowance → **usage-report** (even if a URL is present)
2. **Memory** — mentions remember, recall, last time, team memory, save this → **remember-and-recall**
3. **Explicit http(s) URL** → **deep-reading**
4. **No URL, multi-source info needed** → **research-agent**
5. **research vs deep-reading, no URL** → **research-agent**

### Quick boundary reference

| Scenario | Use | Not | Why |
|----------|-----|-----|-----|
| User provides a doc link | deep-reading | research-agent | URL known; no search needed |
| Topic only, no link | research-agent | deep-reading | Must discover sources first |
| Persist a conclusion for later | remember-and-recall | research-agent | Long-term storage, not one-off research |
| User asks about quota, not content | usage-report | all others | Administrative only |

## Decision tree

```
User request
  ├─ quota/token/usage keywords? ──yes──► usage-report
  ├─ remember/recall/memory keywords? ──yes──► remember-and-recall
  ├─ http(s) URL present? ──yes──► deep-reading
  └─ else ──► research-agent
```

## When adding a workflow

1. Add at least 2 example intents to the table above
2. Update conflict rules and priority vs existing workflows
3. In the PR, explain “When NOT to use” boundaries vs neighbors

---
name: smartgate-deep-reading
description: >
  Deep-read and compress a single known http(s) URL via SmartGate MCP. Use when the user provides a link or asks to summarize docs, RFCs, or articles.
---


## deep-reading

Purpose: Fetch and compress a single user-known URL into condensed text for Host LLM deep reading, summarization, or Q&A.

When to use:
- Official docs / API reference: OpenAPI specs, SDK docs, product manuals
- Long blog posts or technical articles: preprocess input for single-document reading
- Whitepapers / RFCs: compress before LLM extracts section highlights
- User message already contains a clear link — no search step needed

When NOT to use:
- No definitive URL and multiple sources are needed — use **research-agent**
- Persist conclusions to team memory — read with this workflow, then **remember-and-recall** (action=add)
- Query quota — use **usage-report**

Returns: JSON string. When loader calls `smart_pipe` with `template=read`, top level has `success` and `results`. `results[0]` is fetch: `data.markdown`, `data.title`, `data.url`. `results[1]` is context_gate: `data.compressed`, `data.ratio`, `data.original_tokens`, `data.compressed_tokens`.

Composes with: Host LLM for summaries, Q&A, code examples; output into **remember-and-recall**; **usage-report** (action=check) before very long pages.

## Execute (user-smartgate MCP)

Call `smart_pipe`:

```json
{ "template": "read", "url": "<http(s) URL>" }
```

Optional pre-flight: `smart_budget_guard` with `{ "action": "check" }`.

## remember-and-recall

Purpose: Persist or retrieve team-scoped facts, research conclusions, and config notes across sessions for downstream grounding.

When to use:
- Store a conclusion: “Remember our prod API rate limit is 100 req/min”
- Semantic search: “What did we record about Langfuse?”
- Read by ID: fetch one record when `memory_id` is known
- Delete stale entries: remove incorrect or expired team memories

When NOT to use:
- Fetch or search web content — use **research-agent** or **deep-reading**
- Query token quota — use **usage-report**
- General world-knowledge Q&A (non-team facts) — answer with Host LLM directly

Returns: JSON string; shape depends on `action`. `add`: `data.memory_id`, `data.status`. `search`: `data.memories[]` with `id`, `content`, `score`, `created_at`. `get`: `data.memory` (full record). `delete`: `data.deleted`, `data.memory_id`.

Composes with: **research-agent** output summarized by Host LLM then action=add; Host LLM grounds on search results; chain with **deep-reading** (read URL, then add summary).

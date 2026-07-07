# MCP execution (user-smartgate)

Prerequisite: `user-smartgate` MCP configured and authenticated. Parse every tool JSON response before synthesizing.

## deep-reading

Call `smart_pipe`:

```json
{ "template": "read", "url": "<http(s) URL>" }
```

Optional pre-flight: `smart_budget_guard` with `{ "action": "check" }`.

## research-agent

Optional pre-flight: `smart_budget_guard` with `{ "action": "check" }`.

Then chain:

1. `smart_search` — `{ "query": "<topic>", "max_results": 5 }`
2. `smart_fetch` — for each `url` in search results (up to `max_results`)
3. `smart_dedup` — `{ "texts": [<markdown from fetches>], "threshold": 0.85 }`
4. `smart_context_gate` — `{ "text": "<deduped_text>", "ratio": 0.4, "goal": "<optional>" }`

## remember-and-recall

Call `smart_memory` with `action`:

| action | required params |
|--------|-----------------|
| `add` | `content` |
| `search` | `query` |
| `get` | `memory_id` |
| `delete` | `memory_id` |

Do not pass a foreign `team_id`.

## usage-report

Call `smart_budget_guard`:

- Pre-flight: `{ "action": "check" }`
- Usage report: `{ "action": "count" }`

## research-agent

Purpose: When no definitive URL exists, collect material from multiple web sources, deduplicate and compress it, and return structured research ready for Host LLM analysis.

When to use:
- Competitor analysis: compare features, pricing, and positioning across products
- Industry research: aggregate recent news, reports, and trends in a domain
- Academic/technical surveys: gather paper abstracts, technical blogs, and solution comparisons on a topic
- News digests: aggregate coverage around an event or keyword from multiple outlets

When NOT to use:
- User already provided a definitive http(s) URL — use **deep-reading** for a single-chain read without extra search
- Only need to store or retrieve team conclusions — use **remember-and-recall**
- Querying token quota or usage — use **usage-report**

Returns: JSON string (parse via loader). Top level includes `success` and `results` (per-step array). Final `smart_context_gate` step `data` includes `compressed`, `ratio`, `original_tokens`, `compressed_tokens`. Earlier steps include search `results[].url` / `results[].snippet`, fetched page `markdown`, and dedup `deduped_text` / `removed_count`.

Composes with: Host LLM for synthesis and reports; conclusions via **remember-and-recall** (action=add); pre-flight **usage-report** (action=check) before large jobs.

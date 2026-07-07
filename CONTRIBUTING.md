# Contributing to smartgate-workflows

Thanks for contributing! This is a content-only project (YAML + Markdown). **No application code changes are required.**

**All contributed content must be in English** (SKILL.md, pipeline.yaml descriptions, examples, and ROUTING entries).

## Adding a new workflow

1. Copy files from `_template/` into `workflows/<your-workflow-name>/`
2. Fill in `SKILL.md` (must include Purpose / When to use / When NOT to use / Returns / Composes with)
3. Fill in `pipeline.yaml` (see `schema/pipeline.schema.json`)
4. Add at least one concrete `examples/*.md`
5. Update [ROUTING.md](ROUTING.md) and document boundaries vs existing workflows

## Primitive whitelist

`pipeline.yaml` `steps[].tool` **must** be one of these 7 primitives:

- `smart_fetch`
- `smart_search`
- `smart_context_gate`
- `smart_dedup`
- `smart_budget_guard`
- `smart_memory`
- `smart_pipe`

**New primitives are not accepted in this repo.** Open an issue in [smartgate-sdk](https://github.com/smartgate-network/smartgate-sdk) instead.

## Pull request requirements

- [ ] Updated [ROUTING.md](ROUTING.md)
- [ ] At least one `examples/*.md` provided
- [ ] `pipeline.yaml` passes schema validation (CI runs automatically)
- [ ] No tools outside the 7 primitives

## Local validation

```bash
pip install jsonschema pyyaml
python tests/validate.py
```

Same script as GitHub Actions.

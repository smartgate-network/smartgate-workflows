# smartgate-workflows

A **scenario-oriented workflow collection** for the SmartGate ecosystem — declarative YAML + Markdown that describes real user scenarios (e.g. “research a competitor”), open for community contributions.

## Workflows

| Workflow | Description |
|----------|-------------|
| [research-agent](workflows/research-agent/) | Multi-source research without a known URL: search → batch fetch → dedup → compress |
| [deep-reading](workflows/deep-reading/) | Deep-read a single known URL: fetch → compress |
| [remember-and-recall](workflows/remember-and-recall/) | Team long-term memory (add / search / get / delete) |
| [usage-report](workflows/usage-report/) | Query team token allowance and usage (administrative; no content production) |

## This is not runtime code

This repository contains workflow **declarations** only (`SKILL.md` + `pipeline.yaml`). Execution requires:

- [smartgate-mcp](https://github.com/smartgate-network/smartgate-mcp) — MCP tool gateway
- smartgate-cli — (planned) reads this repo and invokes `smart_pipe`

### Runtime contract

| `template` | Loader behavior | Role of yaml `steps` |
|------------|-----------------|----------------------|
| `read` / `research` / `remember` | `smart_pipe(template=…, params…)` | Documentation + CI validation |
| `custom` | `smart_pipe(steps=yaml.steps, …)` | Executable contract |

See each workflow’s `pipeline.yaml` for details.

## Directory layout

```
smartgate-workflows/
├── workflows/          # Scenario workflows
├── schema/             # JSON Schema for pipeline.yaml / SKILL.md
├── _template/          # New workflow templates
├── tests/fixtures/     # Primitive response shape examples
└── .github/            # CI and PR templates
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Copy from `_template/` for new workflows and update [ROUTING.md](ROUTING.md).

## License

[MIT](LICENSE)

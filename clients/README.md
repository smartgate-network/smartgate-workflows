# Client installation

The Cursor Marketplace plugin ships committed skills in `/skills`. Use this script only when you want skills in a project or another host **without** installing the plugin.

**Prerequisite:** SmartGate MCP at `https://smartgate.network/api/mcp` with a Bearer API key ([Connect](https://smartgate.network/docs/connect)).

## Cursor (project-level)

```bash
pip install pyyaml
python scripts/install-skills.py --client cursor --target ../.cursor/skills --force
```

Global install: `--target ~/.cursor/skills`. Marketplace pack: `--target skills`.

## Claude Code

```bash
pip install pyyaml
python scripts/install-skills.py --client claude-code --target ~/.claude/skills --force
```

## Codex

Not supported in v1. See [codex/README.md](codex/README.md).

## Updating

After `git pull`, re-run with `--force`. If you change `workflows/` or `clients/shared/execute.md`, regenerate `/skills` and commit it.

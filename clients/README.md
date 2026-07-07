# Client installation

Install SmartGate workflow skills into your AI coding host. Generated skills are **not** committed to this repo — they are written to your project or home directory.

**Prerequisite:** [smartgate-mcp](https://github.com/smartgate-network/smartgate-mcp) configured in your host.

## Cursor (project-level)

```bash
pip install pyyaml
python scripts/install-skills.py --client cursor --target ../.cursor/skills --force
```

Global install: use `--target ~/.cursor/skills` instead.

## Claude Code

```bash
pip install pyyaml
python scripts/install-skills.py --client claude-code --target ~/.claude/skills --force
```

## Codex

Not supported in v1. See [codex/README.md](codex/README.md).

## Updating

After `git pull`, re-run the install command with `--force`.

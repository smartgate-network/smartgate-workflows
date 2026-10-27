#!/usr/bin/env python3
"""Generate host-specific skills from workflows + client manifests."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALID_CLIENTS = frozenset({"cursor", "claude-code"})


def load_manifest(client: str) -> dict:
    if client not in VALID_CLIENTS:
        valid = ", ".join(sorted(VALID_CLIENTS))
        print(f"Unknown client '{client}'. Valid: {valid}", file=sys.stderr)
        sys.exit(1)
    path = ROOT / "clients" / client / "manifest.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_execute_sections(shared_file: str) -> dict[str, str]:
    text = (ROOT / shared_file).read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    for m in re.finditer(r"^## ([\w-]+)\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL):
        sections[m.group(1)] = m.group(2).strip()
    return sections


def frontmatter(name: str, description: str) -> str:
    desc = description.strip()
    indented = desc.replace("\n", "\n  ")
    return f"---\nname: {name}\ndescription: >\n  {indented}\n---\n\n"


def skill_name(manifest: dict, workflow_id: str) -> str:
    prefix = manifest.get("skill_prefix", "")
    return f"{prefix}{workflow_id}"


def build_workflow_skill(
    manifest: dict,
    workflow_id: str,
    description: str,
    execute_sections: dict[str, str],
) -> str:
    upstream_path = ROOT / "workflows" / workflow_id / "SKILL.md"
    if not upstream_path.is_file():
        print(f"Missing workflow: {upstream_path}", file=sys.stderr)
        sys.exit(1)
    upstream = upstream_path.read_text(encoding="utf-8")
    name = skill_name(manifest, workflow_id)
    parts = [frontmatter(name, description), upstream.rstrip()]
    execute = execute_sections.get(workflow_id)
    if execute:
        parts.append("\n## Execute (user-smartgate MCP)\n\n" + execute)
    return "\n".join(parts) + "\n"


def build_routing_skill(manifest: dict) -> str | None:
    routing = manifest.get("routing_skill") or {}
    if not routing.get("enabled"):
        return None
    source = ROOT / routing.get("source", "ROUTING.md")
    body = source.read_text(encoding="utf-8")
    name = routing["skill_name"]
    desc = routing["description"]
    header = (
        "Prerequisite: SmartGate MCP must be configured.\n\n"
        "Invoke the matching workflow skill after routing.\n\n"
    )
    return frontmatter(name, desc) + header + body.rstrip() + "\n"


def install(client: str, target: Path, *, dry_run: bool = False, force: bool = False) -> list[Path]:
    manifest = load_manifest(client)
    execute_cfg = manifest.get("execute", {})
    execute_sections = load_execute_sections(execute_cfg.get("shared_file", "clients/shared/execute.md"))

    planned: list[Path] = []

    for wf in manifest.get("workflows", []):
        wf_id = wf["id"]
        out_dir = target / skill_name(manifest, wf_id)
        out_file = out_dir / "SKILL.md"
        planned.append(out_file)
        if dry_run:
            continue
        if out_file.exists() and not force:
            print(f"Exists (use --force): {out_file}", file=sys.stderr)
            sys.exit(1)
        content = build_workflow_skill(manifest, wf_id, wf["description"], execute_sections)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file.write_text(content, encoding="utf-8")

    routing_content = build_routing_skill(manifest)
    if routing_content:
        routing = manifest["routing_skill"]
        out_dir = target / routing["skill_name"]
        out_file = out_dir / "SKILL.md"
        planned.append(out_file)
        if not dry_run:
            if out_file.exists() and not force:
                print(f"Exists (use --force): {out_file}", file=sys.stderr)
                sys.exit(1)
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file.write_text(routing_content, encoding="utf-8")

    return planned


def main() -> int:
    parser = argparse.ArgumentParser(description="Install SmartGate workflow skills for a host client.")
    parser.add_argument("--client", required=True, help="cursor or claude-code")
    parser.add_argument("--target", required=True, type=Path, help="Output skills directory")
    parser.add_argument("--dry-run", action="store_true", help="List planned files only")
    parser.add_argument("--force", action="store_true", help="Overwrite existing skills")
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    if args.dry_run:
        planned = install(args.client, target, dry_run=True)
        for p in planned:
            print(p)
        print(f"{len(planned)} skill(s) planned -> {target}")
        return 0

    if not target.parent.exists():
        print(f"Parent missing: {target.parent}", file=sys.stderr)
        return 1
    target.mkdir(parents=True, exist_ok=True)
    planned = install(args.client, target, force=args.force)
    print(f"Installed {len(planned)} skill(s) -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate all workflow pipelines and SKILL.md files. Used locally and in CI."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_TOOLS = frozenset({
    "smart_fetch",
    "smart_search",
    "smart_context_gate",
    "smart_dedup",
    "smart_budget_guard",
    "smart_memory",
    "smart_pipe",
})

REQUIRED_SKILL_LABELS = (
    "Purpose:",
    "When to use:",
    "When NOT to use:",
    "Returns:",
    "Composes with:",
)

TEMPLATE_STEP_RULES: dict[str, list[str]] = {
    "read": ["smart_fetch", "smart_context_gate"],
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def validate_pipelines(errors: list[str]) -> None:
    schema = load_json(ROOT / "schema" / "pipeline.schema.json")
    validator = jsonschema.Draft7Validator(schema)

    for path in sorted(ROOT.glob("workflows/**/pipeline.yaml")):
        rel = path.relative_to(ROOT)
        with path.open(encoding="utf-8") as f:
            doc = yaml.safe_load(f)

        for err in validator.iter_errors(doc):
            errors.append(f"{rel}: schema — {err.message}")

        for i, step in enumerate(doc.get("steps") or []):
            tool = step.get("tool")
            if tool not in ALLOWED_TOOLS:
                errors.append(f"{rel}: step {i} tool '{tool}' not in whitelist")

        template = doc.get("template")
        if template in TEMPLATE_STEP_RULES:
            expected = TEMPLATE_STEP_RULES[template]
            actual = [s.get("tool") for s in doc.get("steps") or []]
            if actual != expected:
                errors.append(
                    f"{rel}: template '{template}' expects steps {expected}, got {actual}"
                )


def parse_skill(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    for label in REQUIRED_SKILL_LABELS:
        if label not in text:
            return None

    name_match = re.search(r"^##\s+(.+)$", text, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else path.parent.name

    def section(label: str) -> str:
        pattern = rf"{re.escape(label)}\s*(.*?)(?=\n[A-Z][^\n]*:|\n##\s|\Z)"
        m = re.search(pattern, text, re.DOTALL)
        return m.group(1).strip() if m else ""

    def bullet_list(label: str) -> list[str]:
        body = section(label)
        items = re.findall(r"^-\s+(.+)$", body, re.MULTILINE)
        return [i.strip() for i in items if i.strip()]

    return {
        "name": name,
        "purpose": section("Purpose:"),
        "when_to_use": bullet_list("When to use:"),
        "when_not_to_use": bullet_list("When NOT to use:"),
        "returns": section("Returns:"),
        "composes_with": section("Composes with:"),
    }


def validate_skills(errors: list[str]) -> None:
    schema = load_json(ROOT / "schema" / "skill.schema.json")
    validator = jsonschema.Draft7Validator(schema)

    for path in sorted(ROOT.glob("workflows/**/SKILL.md")):
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")

        for label in REQUIRED_SKILL_LABELS:
            if label not in text:
                errors.append(f"{rel}: missing required section '{label}'")

        parsed = parse_skill(path)
        if parsed is None:
            continue

        for err in validator.iter_errors(parsed):
            errors.append(f"{rel}: skill schema — {err.message}")


def validate_cursor_plugin(errors: list[str]) -> None:
    # ponytail: one marketplace-shape check; expand if Cursor adds more required fields
    plugin_path = ROOT / ".cursor-plugin" / "plugin.json"
    mcp_path = ROOT / "mcp.json"
    logo_path = ROOT / "assets" / "logo.png"

    if not plugin_path.is_file():
        errors.append(".cursor-plugin/plugin.json: missing")
        return
    plugin = load_json(plugin_path)
    if plugin.get("name") != "smartgate":
        errors.append(f".cursor-plugin/plugin.json: name must be 'smartgate', got {plugin.get('name')!r}")
    if not logo_path.is_file():
        errors.append("assets/logo.png: missing")

    if not mcp_path.is_file():
        errors.append("mcp.json: missing")
        return
    mcp = load_json(mcp_path)
    server = (mcp.get("mcpServers") or {}).get("smartgate") or {}
    if server.get("url") != "https://smartgate.network/api/mcp":
        errors.append("mcp.json: smartgate url must be https://smartgate.network/api/mcp")
    auth = (server.get("headers") or {}).get("Authorization", "")
    if "${SMARTGATE_API_KEY}" not in auth:
        errors.append("mcp.json: Authorization must use ${SMARTGATE_API_KEY}")
    props = ((plugin.get("variables") or {}).get("properties") or {})
    if "SMARTGATE_API_KEY" not in props:
        errors.append(".cursor-plugin/plugin.json: variables.properties.SMARTGATE_API_KEY missing")

    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if len(skill_files) < 5:
        errors.append(f"skills/: expected >=5 SKILL.md, got {len(skill_files)}")
    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---") or "name:" not in text.split("---", 2)[1]:
            errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter name")


def main() -> int:
    errors: list[str] = []
    validate_pipelines(errors)
    validate_skills(errors)
    validate_cursor_plugin(errors)

    if errors:
        print("Validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("All validations passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

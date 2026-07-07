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


def main() -> int:
    errors: list[str] = []
    validate_pipelines(errors)
    validate_skills(errors)

    if errors:
        print("Validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("All validations passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Tests for scripts/install-skills.py"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install-skills.py"


class InstallSkillsTest(unittest.TestCase):
    def test_dry_run_cursor_exits_zero(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(INSTALL), "--client", "cursor", "--target", "/tmp/x", "--dry-run"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("smartgate-deep-reading", proc.stdout)

    def test_workflow_body_matches_upstream(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, str(INSTALL), "--client", "cursor", "--target", tmp, "--force"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)

            upstream = (ROOT / "workflows" / "deep-reading" / "SKILL.md").read_text(encoding="utf-8")
            generated = (Path(tmp) / "smartgate-deep-reading" / "SKILL.md").read_text(encoding="utf-8")

            marker = "## deep-reading"
            body = upstream[upstream.index(marker) :].rstrip()
            self.assertEqual(
                generated[generated.index(marker) :].split("## Execute")[0].rstrip(),
                body,
            )

    def test_unknown_client_fails(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(INSTALL), "--client", "codex", "--target", "/tmp/x", "--dry-run"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 1)
        self.assertIn("cursor", proc.stderr)


if __name__ == "__main__":
    unittest.main()

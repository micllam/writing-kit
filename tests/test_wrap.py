"""Tests of the wrap formatter of the plugin.

The formatter runs on copies of the fixtures of the wrap rules and of
fixtures/package in a temporary project, and Vale then runs the wrap rules
with the configuration of this checkout.
"""

import importlib.util
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.support import REPO

WRAP = REPO / "skills" / "prose-check" / "scripts" / "wrap.py"
WRAP_RULES = [
    "Micllam.WrapMarkdown",
    "Micllam.WrapComments",
    "Micllam.CommitWrap",
]
FIXTURES = [
    "WrapMarkdown/test.md",
    "WrapComments/test.rs",
    "package/notes.md",
    "package/probe.rs",
    "package/probe.sh",
    "package/probe.toml",
    "package/CHANGELOG.md",
]
COMMIT_SUBJECT = "queue: retry a task after its lease expires"

_spec = importlib.util.spec_from_file_location("wrap", WRAP)
wrap = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(wrap)


class WrapTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.project = Path(temp.name)

    def test_formatted_files_pass_the_wrap_rules(self):
        files = []
        for fixture in FIXTURES:
            target = self.project / fixture.replace("/", "-")
            shutil.copy(REPO / "fixtures" / fixture, target)
            files.append(target.name)
        body = " ".join(
            ["The worker retries the task until the lease expires."] * 6
        )
        (self.project / "COMMIT_msg.txt").write_text(
            f"{COMMIT_SUBJECT}\n\n{body}\n"
        )
        files.append("COMMIT_msg.txt")

        subprocess.run(
            [WRAP, *files], cwd=self.project, check=True, capture_output=True
        )
        rules = ", ".join(f'"{rule}"' for rule in WRAP_RULES)
        result = subprocess.run(
            [
                "vale",
                "--config",
                str(REPO / ".vale.ini"),
                "--output=line",
                "--no-exit",
                f"--filter=.Name in [{rules}]",
                *files,
            ],
            cwd=self.project,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        subject = (self.project / "COMMIT_msg.txt").read_text().splitlines()[0]
        self.assertEqual(subject, COMMIT_SUBJECT)

    def test_files_that_pass_the_wrap_rules_stay_unchanged(self):
        files = [
            *REPO.glob("*.md"),
            *REPO.glob("docs/*.md"),
            *REPO.glob("skills/**/*.md"),
            *REPO.glob("skills/**/*.py"),
            *REPO.glob("scripts/*.py"),
            *REPO.glob("hooks/*.py"),
            *REPO.glob("tests/*.py"),
            *REPO.glob("fixtures/valid/*"),
        ]
        self.assertTrue(files)
        for file in files:
            with self.subTest(file=file.relative_to(REPO)):
                text = file.read_text()
                self.assertEqual(wrap.wrap_text(file.name, text), text)

    def test_exits_with_status_2_without_a_file_or_on_a_bad_file(self):
        (self.project / "probe.c").write_text("int x;\n")
        for args in ([], ["missing.md"], ["probe.c"]):
            with self.subTest(args=args):
                result = subprocess.run(
                    [WRAP, *args],
                    cwd=self.project,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 2, result.stderr)

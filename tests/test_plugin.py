"""Tests of the hook and the prose-check wrapper of the plugin.

Each test runs the scripts on copies of files of fixtures/package, in a
temporary project. Without a .vale.ini in the project, both scripts use the
configuration of this checkout.
"""

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.support import REPO

HOOK = REPO / "hooks" / "vale-edit.py"
CHECK = REPO / "skills" / "prose-check" / "scripts" / "prose-check.py"
PROSE_FILES = ["notes.md", "COMMIT_probe.txt"]


def expected_alerts(*files):
    """The sorted alerts of fixtures/expected.txt for the named files, with
    their paths in the temporary project."""
    lines = (REPO / "fixtures" / "expected.txt").read_text().splitlines()
    return sorted(
        line.removeprefix("package/")
        for line in lines
        if any(line.startswith(f"package/{file}:") for file in files)
    )


class PluginTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.project = Path(temp.name) / "project"
        self.project.mkdir()
        for file in [*PROSE_FILES, "probe.c"]:
            shutil.copy(REPO / "fixtures" / "package" / file, self.project)

    def run_hook(self, file):
        """Runs the hook as Claude Code does after an edit of the named file,
        and returns its output."""
        event = {"tool_input": {"file_path": str(self.project / file)}}
        result = subprocess.run(
            [HOOK], input=json.dumps(event), capture_output=True, text=True,
            check=True,
        )
        return result.stdout

    def test_hook_returns_alerts_as_post_tool_use_context(self):
        for file in PROSE_FILES:
            with self.subTest(file=file):
                output = json.loads(self.run_hook(file))["hookSpecificOutput"]
                self.assertEqual(output["hookEventName"], "PostToolUse")
                alerts = sorted(
                    line
                    for line in output["additionalContext"].splitlines()
                    if line.startswith(f"{file}:")
                )
                self.assertEqual(alerts, expected_alerts(file))

    def test_hook_is_silent_on_an_unconfigured_file_type(self):
        self.assertEqual(self.run_hook("probe.c"), "")

    def test_hook_runs_from_the_folder_of_the_nearest_vale_ini(self):
        shutil.copytree(REPO / "styles", self.project / "styles")
        (self.project / ".vale.ini").write_text(
            "StylesPath = styles\n\n[*.c]\nBasedOnStyles = Micllam\n"
        )
        (self.project / "src").mkdir()
        shutil.move(self.project / "probe.c", self.project / "src")
        output = json.loads(self.run_hook("src/probe.c"))["hookSpecificOutput"]
        self.assertRegex(
            output["additionalContext"],
            r"(?m)^src/probe\.c:1:\d+:Micllam\.Semicolons:",
        )

    def test_wrapper_prints_alerts_and_exits_with_status_1(self):
        result = subprocess.run(
            [CHECK, *PROSE_FILES], cwd=self.project, capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(
            sorted(result.stdout.splitlines()), expected_alerts(*PROSE_FILES)
        )

    def test_wrapper_checks_the_files_in_a_named_folder(self):
        result = subprocess.run(
            [CHECK, "."], cwd=self.project, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(
            sorted(result.stdout.splitlines()), expected_alerts(*PROSE_FILES)
        )

    def test_wrapper_uses_project_configuration_with_synced_styles(self):
        shutil.copytree(REPO / "styles", self.project / "styles")
        (self.project / ".vale.ini").write_text(
            "StylesPath = styles\n\n[*.c]\nBasedOnStyles = Micllam\n"
        )
        result = subprocess.run(
            [CHECK, "probe.c"], cwd=self.project, capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertRegex(
            result.stdout, r"(?m)^probe\.c:1:\d+:Micllam\.Semicolons:"
        )

    def test_wrapper_exits_with_status_2_without_a_path_or_on_vale_error(self):
        with self.subTest(failure="no path"):
            result = subprocess.run(
                [CHECK], cwd=self.project, capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("usage: prose-check.py PATH...", result.stderr)
        with self.subTest(failure="vale"):
            (self.project / "styles").mkdir()
            (self.project / ".vale.ini").write_text(
                "StylesPath = styles\n\n[*.md]\nBasedOnStyles = Missing\n"
            )
            result = subprocess.run(
                [CHECK, "notes.md"], cwd=self.project, capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2, result.stderr)

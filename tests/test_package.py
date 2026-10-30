"""Tests of the package that scripts/package.py builds, and of the versions
that the README states.

PackageTest installs dist/Micllam.zip into a temporary project and runs it on
the fixtures. Only this test reads the configuration of the package in
.vale.ini. With UPDATE_ALERTS=1, the test writes the alerts of fixtures/package
to fixtures/expected.txt.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.support import REPO, UPDATE


class ReadmeTest(unittest.TestCase):
    def setUp(self):
        self.readme = (REPO / "README.md").read_text()

    def test_readme_states_the_vale_version_of_meta(self):
        meta = json.loads((REPO / "meta.json").read_text())
        version = meta["vale_version"].removeprefix(">=")
        self.assertIn(f"Vale {version} or later", self.readme)
        self.assertIn(
            f"    version: {version}", self.readme.splitlines(),
            "the CI example does not set the version",
        )

    def test_readme_lists_the_package_at_the_last_release(self):
        changelog = (REPO / "CHANGELOG.md").read_text()
        release = re.search(r"(?m)^## \[([0-9][0-9.]*)\]", changelog)
        self.assertIsNotNone(release, "CHANGELOG.md has no released version")
        self.assertIn(
            f"releases/download/v{release[1]}/Micllam.zip", self.readme
        )


class PackageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([REPO / "scripts" / "package.py"], check=True)
        temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(temp.cleanup)
        cls.project = Path(temp.name)
        shutil.copy(REPO / "dist" / "Micllam.zip", cls.project)
        for folder in ("valid", "package"):
            shutil.copytree(REPO / "fixtures" / folder, cls.project / folder)
        for file in ("README.md", "CHANGELOG.md", "docs/agent-guide.md"):
            shutil.copy(REPO / file, cls.project)
        (cls.project / ".vale.ini").write_text(
            "StylesPath = .vale/styles\n"
            "MinAlertLevel = suggestion\n"
            f"Packages = {cls.project / 'Micllam.zip'}\n"
        )
        subprocess.run(
            ["vale", "--no-global", "sync"], cwd=cls.project, check=True,
            stdout=subprocess.DEVNULL,
        )

    def vale(self, *args):
        result = subprocess.run(
            ["vale", "--output=line", "--sort", "--no-global", "--no-exit",
             *args],
            cwd=self.project, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_installed_rules_link_to_the_style_at_package_ref(self):
        ref = os.environ.get("PACKAGE_REF", "master")
        rule = self.project / ".vale" / "styles" / "Micllam" / "Vocabulary.yml"
        self.assertIn(f"/blob/{ref}/docs/writing-style.md", rule.read_text())

    def test_valid_files_produce_no_alert(self):
        alerts = self.vale(
            "valid", "README.md", "CHANGELOG.md", "agent-guide.md"
        )
        self.assertEqual(alerts, "")

    def test_package_fixtures_produce_the_expected_alerts(self):
        alerts = self.vale("--normalize", "--relative", "package")
        expected = REPO / "fixtures" / "expected.txt"
        if UPDATE:
            expected.write_text(alerts)
        else:
            self.assertEqual(alerts, expected.read_text())

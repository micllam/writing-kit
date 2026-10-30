"""Tests of each rule of styles/Micllam on its fixture.

Each rule has a folder in fixtures/ whose .vale.ini enables that rule alone,
and a file in testdata/ with the alerts of the folder. With UPDATE_ALERTS=1, the
test writes the alerts of each folder to its file in testdata/.
"""

import subprocess
import unittest

from tests.support import REPO, RULES, UPDATE

# The hidden flags sort the alerts by file and make the paths relative to the
# fixture folder.
VALE = [
    "vale", "--output=line", "--sort", "--normalize", "--relative",
    "--no-global", "--no-exit", ".",
]


class RulesTest(unittest.TestCase):
    def test_rule_reports_the_alerts_of_its_testdata_file(self):
        self.assertTrue(RULES, "no rule in styles/Micllam")
        for rule in RULES:
            with self.subTest(rule=rule.stem):
                fixture = REPO / "fixtures" / rule.stem
                self.assertTrue(
                    (fixture / ".vale.ini").is_file(),
                    f"{rule.stem} has no fixture",
                )
                result = subprocess.run(
                    VALE, cwd=fixture, capture_output=True, text=True
                )
                self.assertEqual(result.returncode, 0, result.stderr)

                expected = REPO / "testdata" / f"{rule.stem}.txt"
                if UPDATE:
                    expected.write_text(result.stdout)
                else:
                    self.assertEqual(result.stdout, expected.read_text())

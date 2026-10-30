"""Tests of the rules of styles/Micllam against the style they implement."""

import re
import unittest

from tests.support import REPO, RULES, anchor

LINK = re.compile(r"(?m)^link: .*/docs/writing-style\.md#([a-z0-9-]+)$")


class StyleTest(unittest.TestCase):
    def test_rule_links_to_a_section_of_the_style(self):
        style = (REPO / "docs" / "writing-style.md").read_text()
        sections = {
            anchor(line.removeprefix("## "))
            for line in style.splitlines()
            if line.startswith("## ")
        }
        self.assertTrue(RULES, "no rule in styles/Micllam")
        for rule in RULES:
            with self.subTest(rule=rule.name):
                link = LINK.search(rule.read_text())
                self.assertIsNotNone(
                    link, f"{rule.name} has no link to docs/writing-style.md"
                )
                self.assertIn(
                    link[1], sections,
                    f"{rule.name} links to #{link[1]}, which is not a section "
                    "of docs/writing-style.md",
                )

    def test_wrap_scripts_differ_in_their_first_line_only(self):
        # The first line sets the mode of the script.
        def body(name):
            path = REPO / "styles" / "config" / "scripts" / name
            return path.read_text().partition("\n")[2]

        self.assertEqual(body("WrapComments.tengo"), body("WrapMarkdown.tengo"))

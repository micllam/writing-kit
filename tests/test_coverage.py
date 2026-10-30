"""Tests of the manifests in coverage/.

The manifests list the writing rules by section. Each key is true when the
style checks the rule and false when it does not. A comment after the value
refers to the Vale rules that check it.
"""

import re
import unittest

from tests.support import REPO, RULES, anchor

REF = re.compile(r"([A-Za-z]+)\.yml")

# A rule of docs/agent-guide.md: a list item with a bold lead-in that ends in a
# full stop.
GUIDE_RULE = re.compile(r"(?m)^- \*\*([^*]+)\.\*\* ")


def manifest_lines():
    """Each line of the manifests as its place (file:line), its text before the
    comment and the names of the rules that its comment refers to."""
    paths = sorted((REPO / "coverage").glob("*.yml"))
    if not paths:
        raise AssertionError("no manifest in coverage/")
    for path in paths:
        for number, line in enumerate(path.read_text().splitlines(), 1):
            text, _, comment = line.partition("#")
            yield f"{path.name}:{number}", text.strip(), REF.findall(comment)


def entries():
    """The key and the value of each line with text, with its place."""
    for place, text, _ in manifest_lines():
        if text:
            key, _, value = text.partition(":")
            yield place, key.strip(), value.strip()


class CoverageTest(unittest.TestCase):
    def test_manifest_value_is_true_or_false(self):
        for place, key, value in entries():
            with self.subTest(place=place):
                self.assertIn(
                    value, ("true", "false"),
                    f"{place}: {key} does not have the value true or false",
                )

    def test_manifest_comment_refers_to_an_existing_rule(self):
        for place, _, refs in manifest_lines():
            for ref in refs:
                with self.subTest(place=place, rule=ref):
                    rule = REPO / "styles" / "Micllam" / f"{ref}.yml"
                    self.assertTrue(rule.is_file(), f"{place}: {ref}.yml")

    def test_manifest_refers_to_every_rule(self):
        referred = {ref for _, _, refs in manifest_lines() for ref in refs}
        self.assertTrue(RULES, "no rule in styles/Micllam")
        for rule in RULES:
            with self.subTest(rule=rule.name):
                self.assertIn(rule.stem, referred)

    def test_agent_guide_states_the_unchecked_rules(self):
        unchecked = {key for _, key, value in entries() if value == "false"}
        guide = (REPO / "docs" / "agent-guide.md").read_text()
        stated = {anchor(lead_in) for lead_in in GUIDE_RULE.findall(guide)}
        self.assertSetEqual(stated, unchecked)

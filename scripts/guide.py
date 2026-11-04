#!/usr/bin/env python3
"""Writes docs/agent-guide.md: the rules of docs/writing-style.md whose key in
coverage/ is false. The key of a rule is the anchor of its bold lead-in, and
the key of a vocabulary entry is the anchor of its words before the first
colon or parenthesis. Exit status is 1 when a rule has no key or a key has no
rule, 2 when the command has an argument, and 0 otherwise.

Usage: guide.py    writes docs/agent-guide.md
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STYLE = REPO / "docs" / "writing-style.md"
GUIDE = REPO / "docs" / "agent-guide.md"

HEADER = """\
# Writing style for agents

The rules of [`writing-style.md`](writing-style.md) that the Vale package
`Micllam` does not check. An agent reads this file in every session, and the
package reports the other rules on each edit with a link to the style.
`scripts/guide.py` writes this file from the style and `coverage/`.
"""

LEAD_IN = re.compile(r"\*\*([^*]+)\.\*\* ")
HEAD = re.compile(r"([^:(]*)")


def anchor(text):
    """The anchor of a heading on GitHub: lower case, with spaces as hyphens
    and punctuation removed."""
    return re.sub(r"[^a-z0-9 -]", "", text.lower()).strip().replace(" ", "-")


def key(bullet):
    """The key of a bullet, given its text after the list marker."""
    lead_in = LEAD_IN.match(bullet)
    return anchor(lead_in[1] if lead_in else HEAD.match(bullet)[1])


def manifests():
    """The keys and values of coverage/ by the title of their section."""
    result = {}
    for path in sorted((REPO / "coverage").glob("*.yml")):
        lines = path.read_text().splitlines()
        values = {}
        for line in lines[1:]:
            text = line.partition("#")[0].strip()
            if text:
                name, _, value = text.partition(":")
                values[name.strip()] = value.strip() == "true"
        result[lines[0].removeprefix("# ")] = values
    return result


def blocks(text):
    """Each section of the style as its title and its blocks. A block is a
    paragraph or a bullet, as a list of lines."""
    sections = []
    for line in text.splitlines():
        if line.startswith("## "):
            sections.append((line[3:], []))
        elif not sections:
            continue
        elif line.startswith("- ") or not line:
            sections[-1][1].append([line] if line else [])
        elif sections[-1][1] and sections[-1][1][-1]:
            sections[-1][1][-1].append(line)
        else:
            sections[-1][1].append([line])
    return [(title, [block for block in found if block])
            for title, found in sections]


def mismatches(style, coverage):
    """Each rule of the style without a key, and each key without a rule."""
    problems = []
    for title, found in blocks(style):
        keys = coverage.get(title, {})
        stated = set()
        for block in found:
            if block[0].startswith("- "):
                name = key(block[0][2:])
                stated.add(name)
                if name not in keys:
                    problems.append(f"{title}: {name} has no key in coverage/")
        for name in keys.keys() - stated:
            problems.append(f"{title}: {name} has no rule in the style")
    return problems


def guide(style, coverage):
    """The text of the agent guide. A paragraph that ends in a colon introduces
    the bullets that follow it, and the guide keeps it with them."""
    parts = [HEADER]
    for title, found in blocks(style):
        keys = coverage.get(title, {})
        lines, lead = [], None
        for block in found:
            if not block[0].startswith("- "):
                lead = block if block[-1].endswith(":") else None
            elif not keys.get(key(block[0][2:]), True):
                if lead:
                    lines += ["", *lead, ""] if lines else [*lead, ""]
                    lead = None
                lines += block
        if lines:
            parts.append(f"\n## {title}\n\n" + "\n".join(lines) + "\n")
    return "".join(parts)


def main():
    if len(sys.argv) != 1:
        print(__doc__.rpartition("Usage: ")[2].strip(), file=sys.stderr)
        return 2
    style, coverage = STYLE.read_text(), manifests()
    problems = mismatches(style, coverage)
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 1
    GUIDE.write_text(guide(style, coverage))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Rewraps the prose of files to the wrap rules of writing-kit, in place.

A paragraph is filled greedily to 80 columns, and a commit message to 72. A
link, a code span or a URL never breaks. A span that does not fit on a line of
its own takes a line with its trailing punctuation, and with the word before it
when that word would stand alone. The script reads Markdown, `COMMIT_*.txt`
files and the comments of Rust, shell, TOML and Python files. It leaves code,
tables, headings, dividers, fenced blocks and the text between
`<!-- vale off -->` and `<!-- vale on -->` as they are. Exit status is 2
without a file, or when a file does not exist or has another type, and 0
otherwise.

Usage: wrap.py FILE...    prints the path of each file that it changed
"""

import re
import sys
from pathlib import Path

USAGE = "usage: wrap.py FILE..."
LIMIT = 80
COMMIT_LIMIT = 72
COMMENT_SUFFIXES = {".rs", ".sh", ".toml", ".py"}

SPAN = (
    r"``.+?``|`[^`]+`|\[[^\]]*\](?:\([^)]*\)|\[[^\]]*\])"
    r"|<?https?://[^\s>]+>?"
)
TOKEN = re.compile(rf"(?:{SPAN}|\S)+")
SPAN_TOKEN = re.compile(rf"\(?(?:{SPAN})[).,;:\"']*")
LIST_ITEM = re.compile(r"([-*+]|\d+[.)]) +")
# Line starts that the wrap checks or Markdown read as something other than a
# continuation of the paragraph.
MARKDOWN_START = re.compile(
    r"([-*+>]|\d+[.)]|#+)( |$)|\||\[[^\]]+\]:|```|~~~|<(?!https?:)[A-Za-z/!]"
    r"|[a-z-]+ = "
)
COMMENT_START = re.compile(
    r"([-*+]|\d+[.)]) |```|# |\||\[[^\]]+\]:|use |let |[#}]|\.|[A-Za-z_]+::"
    r"|[a-z_]+\(|\$|[A-Z][A-Z_]+ *="
)
COMMENT = re.compile(r"(\s*(?://[/!]?|#))( (.*))?$")


def is_wide(token, indent, limit):
    """Whether token is a span that does not fit on a line after indent."""
    return bool(SPAN_TOKEN.fullmatch(token)) and indent + len(token) > limit


def fill(text, first, rest, limit, bad_start):
    """The lines of a paragraph of text, with the prefix first on its first line
    and rest on the others."""
    lines = []
    prefix = first
    line = []
    for token in TOKEN.findall(text):
        if not line or len(prefix + " ".join([*line, token])) <= limit:
            line.append(token)
            continue
        if (
            len(line) == 1
            and " " not in line[0]
            and is_wide(token, len(rest), limit)
        ):
            line.append(token)
            continue
        start = [token]
        while len(line) > 1 and bad_start.match(" ".join(start)):
            start.insert(0, line.pop())
        lines.append(prefix + " ".join(line))
        prefix = rest
        line = start
    lines.append(prefix + " ".join(line))
    return lines


class Paragraph:
    """The prose lines of a paragraph, collected until a line ends it."""

    def __init__(self, first, rest, text, marker=None):
        self.first = first
        self.rest = rest
        self.texts = [text]
        self.marker = marker
        self.hard_break = ""

    def render(self, limit, bad_start):
        lines = fill(
            " ".join(self.texts), self.first, self.rest, limit, bad_start
        )
        lines[-1] += self.hard_break
        return lines


def wrap_lines(lines, limit, bad_start, classify):
    """The lines with each paragraph that classify finds refilled.

    classify(line, paragraph) returns None for a line to keep as it is, the
    text of a continuation of paragraph, or a new Paragraph."""
    out = []
    paragraph = None
    for line in lines:
        kind = classify(line, paragraph)
        if isinstance(kind, str):
            paragraph.texts.append(kind)
        else:
            if paragraph:
                out.extend(paragraph.render(limit, bad_start))
            paragraph = kind
            if kind is None:
                out.append(line)
                continue
        if re.search(r"(  |\\)$", line):
            paragraph.hard_break = re.search(r"(  |\\)$", line)[1]
            paragraph.texts[-1] = paragraph.texts[-1].rstrip(" \\")
            out.extend(paragraph.render(limit, bad_start))
            paragraph = None
    if paragraph:
        out.extend(paragraph.render(limit, bad_start))
    return out


def markdown_classifier():
    state = {"front": False, "fence": False, "off": False, "index": -1}

    def classify(line, paragraph):
        state["index"] += 1
        stripped = line.strip()
        if state["index"] == 0 and stripped == "---":
            state["front"] = True
            return None
        if state["front"]:
            state["front"] = stripped != "---"
            return None
        if re.match(r"(```|~~~)", stripped):
            state["fence"] = not state["fence"]
            return None
        if state["fence"]:
            return None
        if "<!-- vale off -->" in stripped and "<!-- vale on -->" not in line:
            state["off"] = True
            return None
        if state["off"]:
            state["off"] = "<!-- vale on -->" not in line
            return None
        if not re.search(r"\w", stripped):
            return None
        indent = line[: len(line) - len(line.lstrip())]
        item = LIST_ITEM.match(stripped)
        if item:
            first = indent + item[0]
            return Paragraph(first, " " * len(first), stripped[item.end() :])
        if MARKDOWN_START.match(stripped):
            return None
        if paragraph:
            return stripped
        if len(indent) >= 4:
            return None
        return Paragraph(indent, indent, stripped)

    return classify


def comment_classifier():
    state = {"fence": False}

    def classify(line, paragraph):
        match = COMMENT.match(line)
        if not match:
            state["fence"] = False
            return None
        marker = match[1]
        text = (match[3] or "").strip()
        if text.startswith("```"):
            state["fence"] = not state["fence"]
            return None
        if state["fence"] or not re.search(r"\w", text):
            return None
        item = LIST_ITEM.match(text)
        if item:
            return Paragraph(
                f"{marker} {item[0]}",
                f"{marker} " + " " * len(item[0]),
                text[item.end() :],
                marker,
            )
        if COMMENT_START.match(text):
            return None
        if paragraph and paragraph.marker == marker:
            return text
        return Paragraph(f"{marker} ", f"{marker} ", text, marker)

    return classify


def wrap_text(name, text):
    """The text of a file named name with its prose rewrapped, or None for a
    file of another type."""
    lines = text.split("\n")
    path = Path(name)
    if re.fullmatch(r"COMMIT_.*\.txt", path.name):
        body = wrap_lines(
            lines[1:], COMMIT_LIMIT, MARKDOWN_START, markdown_classifier()
        )
        return "\n".join([lines[0], *body])
    if path.suffix == ".md":
        return "\n".join(
            wrap_lines(lines, LIMIT, MARKDOWN_START, markdown_classifier())
        )
    if path.suffix in COMMENT_SUFFIXES:
        return "\n".join(
            wrap_lines(lines, LIMIT, COMMENT_START, comment_classifier())
        )
    return None


def main():
    files = sys.argv[1:]
    if not files:
        print(USAGE, file=sys.stderr)
        return 2
    status = 0
    for file in files:
        path = Path(file)
        if not path.is_file():
            print(f"wrap: {file} is not a file", file=sys.stderr)
            status = 2
            continue
        text = path.read_text()
        wrapped = wrap_text(file, text)
        if wrapped is None:
            print(
                f"wrap: {file} has a type without wrap rules", file=sys.stderr
            )
            status = 2
        elif wrapped != text:
            path.write_text(wrapped)
            print(file)
    return status


if __name__ == "__main__":
    sys.exit(main())

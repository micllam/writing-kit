"""Paths and helpers of the tests."""

import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULES = sorted((REPO / "styles" / "Micllam").glob("*.yml"))
UPDATE = os.environ.get("UPDATE_ALERTS") == "1"


def anchor(heading):
    """The anchor of a heading on GitHub: lowercase, with spaces as hyphens and
    punctuation removed."""
    return re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-")

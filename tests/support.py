"""Paths and helpers of the tests."""

import importlib.util
import os
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULES = sorted((REPO / "styles" / "Micllam").glob("*.yml"))
UPDATE = os.environ.get("UPDATE_ALERTS") == "1"

_spec = importlib.util.spec_from_file_location(
    "guide", REPO / "scripts" / "guide.py")
guide = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(guide)

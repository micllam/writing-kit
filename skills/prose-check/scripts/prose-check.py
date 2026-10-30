#!/usr/bin/env python3
"""Runs the Vale package of writing-kit on prose. The project's .vale.ini is
used when the project has one and its styles are synced, and the configuration
of this checkout otherwise. Exit status is 1 when Vale reports an alert, 2 when
Vale fails or the command names no file, and 0 otherwise.

Usage: prose-check.py PATH...    the named files, and the files in the named
                                 folders
"""

import re
import subprocess
import sys
from pathlib import Path

WRITING_KIT = Path(__file__).resolve().parents[3]
USAGE = "usage: prose-check.py PATH..."


def config_args():
    """The --config argument of Vale, empty when the project's .vale.ini
    applies."""
    fallback = ["--config", str(WRITING_KIT / ".vale.ini")]
    ini = Path(".vale.ini")
    if not ini.is_file():
        return fallback
    styles = re.search(r"(?m)^StylesPath *= *(.*)$", ini.read_text())
    if styles and styles[1].strip() and not Path(styles[1].strip()).is_dir():
        print(
            f"prose-check: {styles[1].strip()} does not exist, run 'vale sync'."
            " Using the configuration of writing-kit.",
            file=sys.stderr,
        )
        return fallback
    return []


def main():
    paths = sys.argv[1:]
    if not paths:
        print(USAGE, file=sys.stderr)
        return 2
    result = subprocess.run(
        ["vale", *config_args(), "--output=line", "--no-exit", "--no-global",
         *paths],
        stdout=subprocess.PIPE, text=True,
    )
    alerts = [line for line in result.stdout.splitlines() if line]
    for alert in alerts:
        print(alert)
    if result.returncode != 0:
        return 2
    return 1 if alerts else 0


if __name__ == "__main__":
    sys.exit(main())

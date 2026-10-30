#!/usr/bin/env python3
"""A PostToolUse hook for Edit and Write. Runs prose-check.py on the edited
file from the folder of the nearest .vale.ini above the file, or else from the
folder of the file, and returns the alerts to the agent as the hook's
additional context. An error of Vale, such as a configuration that does not
load, is returned in place of the alerts.
"""

import json
import subprocess
import sys
from pathlib import Path

CHECK = (Path(__file__).resolve().parents[1]
         / "skills" / "prose-check" / "scripts" / "prose-check.py")


def project_root(directory):
    """The nearest folder with a .vale.ini from directory up, or else
    directory."""
    for folder in (directory, *directory.parents):
        if (folder / ".vale.ini").is_file():
            return folder
    return directory


def main():
    event = json.load(sys.stdin)
    file = event.get("tool_input", {}).get("file_path")
    if not file:
        return
    path = Path(file)
    if not path.is_file():
        return
    path = path.parent.resolve() / path.name
    root = project_root(path.parent)
    result = subprocess.run(
        [CHECK, str(path.relative_to(root))], cwd=root, capture_output=True,
        text=True,
    )

    messages = []
    errors = result.stderr.rstrip("\n")
    if errors:
        messages.append(f"prose-check reported:\n{errors}")
    alerts = [line for line in result.stdout.splitlines() if line]
    if alerts:
        messages.append(
            f"Vale reports {len(alerts)} alert(s) in this file:\n"
            + "\n".join(alerts)
            + "\n\nFix these before moving on, and keep the markup as it is."
            " Do not disable a rule to clear one."
        )
    if messages:
        output = {
            "hookEventName": "PostToolUse",
            "additionalContext": "\n\n".join(messages),
        }
        print(json.dumps({"hookSpecificOutput": output}))


if __name__ == "__main__":
    main()

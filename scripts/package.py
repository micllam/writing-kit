#!/usr/bin/env python3
"""Builds dist/Micllam.zip, whose single folder Micllam/ contains .vale.ini,
meta.json, styles/ and LICENSE. The link of each rule points at the style at
the Git ref PACKAGE_REF, master by default.
"""

import os
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULES = REPO / "styles" / "Micllam"


def main():
    ref = os.environ.get("PACKAGE_REF", "master")
    paths = [REPO / ".vale.ini", REPO / "meta.json", REPO / "styles",
             *sorted((REPO / "styles").rglob("*")), REPO / "LICENSE"]

    (REPO / "dist").mkdir(exist_ok=True)
    with zipfile.ZipFile(REPO / "dist" / "Micllam.zip", "w",
                         zipfile.ZIP_DEFLATED) as archive:
        archive.write(REPO, "Micllam")
        for path in paths:
            name = f"Micllam/{path.relative_to(REPO).as_posix()}"
            if path.parent == RULES and path.suffix == ".yml":
                rule = path.read_text().replace(
                    "/blob/master/docs/", f"/blob/{ref}/docs/"
                )
                archive.writestr(zipfile.ZipInfo.from_file(path, name), rule,
                                 zipfile.ZIP_DEFLATED)
            else:
                archive.write(path, name)


if __name__ == "__main__":
    main()

#!/bin/sh
# Prints the CHANGELOG.md section of a version, for the notes of its release.
# Exit status is 1 when the CHANGELOG does not have a section for the version.
#
# Usage: notes.sh VERSION
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
version=$1
notes=$(awk -v v="$version" '
  $0 ~ "^## \\[" v "\\]" { found = 1; next }
  /^## \[/ { found = 0 }
  found { print }
' "$repo_dir/CHANGELOG.md")
[ -n "$notes" ] || { echo "CHANGELOG.md has no section for $version" >&2; exit 1; }
printf '%s\n' "$notes"

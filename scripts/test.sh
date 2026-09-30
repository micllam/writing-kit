#!/bin/sh
# Installs dist/Micllam.zip into a temporary project and runs it on the
# fixtures. The files in fixtures/valid, README.md and CHANGELOG.md must not
# produce an alert, and the alerts of fixtures/package must equal
# fixtures/expected.txt. README.md must state the Vale version of meta.json and
# the version of the last CHANGELOG.md section in its Packages URL, and the
# installed rules must link to the style at PACKAGE_REF, master by default.
#
# With --update, the script writes the alerts of fixtures/package to
# fixtures/expected.txt.
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
"$repo_dir/scripts/package.sh"

version=$(sed -n 's/.*"vale_version": ">=\([0-9.]*\)".*/\1/p' "$repo_dir/meta.json")
[ -n "$version" ] || { echo "meta.json: no vale_version" >&2; exit 1; }
grep -q "Vale $version or later" "$repo_dir/README.md" \
  || { echo "README.md does not state Vale $version" >&2; exit 1; }

release=$(sed -n 's/^## \[\([0-9][0-9.]*\)\].*/\1/p' "$repo_dir/CHANGELOG.md" | head -n 1)
[ -n "$release" ] || { echo "CHANGELOG.md: no released version" >&2; exit 1; }
grep -q "releases/download/v$release/Micllam.zip" "$repo_dir/README.md" \
  || { echo "README.md does not list the package at v$release" >&2; exit 1; }

test_dir=$(mktemp -d)
trap 'rm -rf "$test_dir"' EXIT HUP INT TERM

cp "$repo_dir/dist/Micllam.zip" "$test_dir/Micllam.zip"
cp -R "$repo_dir/fixtures/valid" "$repo_dir/fixtures/package" "$test_dir/"
cp "$repo_dir/README.md" "$repo_dir/CHANGELOG.md" "$test_dir/"
cat > "$test_dir/.vale.ini" <<INI
StylesPath = .vale/styles
MinAlertLevel = suggestion
Packages = $test_dir/Micllam.zip
INI

cd "$test_dir"
vale --no-global sync >/dev/null
ref=${PACKAGE_REF:-master}
grep -q "/blob/$ref/docs/writing-style.md" .vale/styles/Micllam/Modals.yml \
  || { echo "the installed rules do not link to the style at $ref" >&2; exit 1; }
vale --no-global valid README.md CHANGELOG.md
vale --output=line --sort --normalize --relative --no-global --no-exit package \
  > actual.txt

if [ "${1:-}" = "--update" ]; then
  cp actual.txt "$repo_dir/fixtures/expected.txt"
else
  diff -u "$repo_dir/fixtures/expected.txt" actual.txt
fi

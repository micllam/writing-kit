#!/bin/sh
# Builds dist/Micllam.zip, whose single folder Micllam/ contains .vale.ini,
# meta.json, styles/ and LICENSE.
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT HUP INT TERM

mkdir -p "$stage/Micllam" "$repo_dir/dist"
cp "$repo_dir/.vale.ini" "$stage/Micllam/.vale.ini"
cp "$repo_dir/meta.json" "$stage/Micllam/meta.json"
cp -R "$repo_dir/styles" "$stage/Micllam/styles"
cp "$repo_dir/LICENSE" "$stage/Micllam/LICENSE"
rm -f "$repo_dir/dist/Micllam.zip"
(cd "$stage" && zip -q -r "$repo_dir/dist/Micllam.zip" Micllam)

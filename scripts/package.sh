#!/bin/sh
# Builds dist/Micllam.zip, whose single folder Micllam/ contains .vale.ini,
# meta.json, styles/ and LICENSE. The link of each rule points at the style at
# the Git ref PACKAGE_REF, master by default.
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
ref=${PACKAGE_REF:-master}
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT HUP INT TERM

mkdir -p "$stage/Micllam" "$repo_dir/dist"
cp "$repo_dir/.vale.ini" "$stage/Micllam/.vale.ini"
cp "$repo_dir/meta.json" "$stage/Micllam/meta.json"
cp -R "$repo_dir/styles" "$stage/Micllam/styles"
for rule in "$stage/Micllam/styles/Micllam/"*.yml; do
  sed "s#/blob/master/docs/#/blob/$ref/docs/#" "$rule" > "$rule.tmp"
  mv "$rule.tmp" "$rule"
done
cp "$repo_dir/LICENSE" "$stage/Micllam/LICENSE"
rm -f "$repo_dir/dist/Micllam.zip"
(cd "$stage" && zip -q -r "$repo_dir/dist/Micllam.zip" Micllam)

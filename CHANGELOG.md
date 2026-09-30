# Changelog

All notable changes to the `Micllam` Vale package will be documented in this
file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `Micllam.Vocabulary` permits "will need to" as a form of a requirement, with
  "must" and "require".
- Each rule of a release links to the section of the style at the release tag.

### Removed

- The vocabulary entries of a job queue (parked, make-up, stopped beating, retry
  budget, takes back, mailbox and terminal prefix) are removed from the style
  and from `Micllam.Vocabulary`. A project that uses them will need to add a
  substitution rule in its own style.

### Fixed

- `Micllam.Vocabulary` reports the excluded senses of hand and over only. A line
  with "on the other hand" or "is over 80 columns" does not produce an alert.

## [0.1.0] - 2026-09-30

### Added

- The Vale package `Micllam` checks the writing style in `docs/writing-style.md`
  in Markdown, plain text, Rust, shell, TOML, Python and commit message files:
  excluded words with their replacements, sentence forms, British spelling, line
  wrap, CHANGELOG lists and commit subjects. It requires Vale 3.23.0 or later.

# Changelog

All notable changes to the `Micllam` Vale package will be documented in this
file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `Micllam.Vocabulary` reports `pin`, `pins` and `pinning` in every position,
  where 0.3.1 reported them before an article or a demonstrative only. Reword
  each sentence that the rule reports.

## [0.3.1] - 2026-10-01

### Fixed

- `Micllam.WrapMarkdown` and `Micllam.WrapComments` exempt a line with a link of
  42 columns or more from the 80-column limit, as they exempt a long code span.
  A project can restore the link text that it shortened for the limit.
- `Micllam.WrapMarkdown` and `Micllam.WrapComments` treat a code span between
  double backticks as one word. A project can move such a span whole to the next
  line.

## [0.3.0] - 2026-10-01

### Changed

- `Micllam.WrapMarkdown` and `Micllam.WrapComments` check a line that starts
  with a link and the line above it, and skip a link definition. Rewrap the
  paragraphs that the rules report.

### Fixed

- `Micllam.WrapMarkdown` and `Micllam.WrapComments` treat an inline or reference
  link with its target as one word, as they treat a code span. A project can
  move a link whole to the next line.

## [0.2.1] - 2026-10-01

### Fixed

- `Micllam.WrapComments` skips a table row and the lines of a code fence in a
  comment, as `Micllam.WrapMarkdown` skips them in Markdown. A project can
  remove the Vale markers around such lines.

## [0.2.0] - 2026-09-30

### Changed

- `Micllam.Vocabulary` permits "will need to" as a form of a requirement, with
  "must" and "require".
- Each rule of a release links to the section of the style at the release tag.
- `Micllam.Vocabulary` reports `load-bearing`, with the replacement "necessary,
  or state what depends on it".
- `Micllam.PlainNegation` permits "no longer".

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

# Contributing

## Layout

| Path | Contents |
|---|---|
| [`docs/writing-style.md`](docs/writing-style.md) | The writing style: content, CHANGELOG entries, commit messages, sentences, punctuation and vocabulary |
| [`docs/agent-guide.md`](docs/agent-guide.md) | The rules of the style that the package does not check, for the instructions that an agent reads in every session, written by `scripts/guide.py` |
| [`styles/Micllam/`](styles/Micllam/) | The rules, one per concept of the style |
| [`styles/config/scripts/`](styles/config/scripts/) | The Tengo scripts of the wrap, title-comment and CHANGELOG rules |
| [`.vale.ini`](.vale.ini) | The configuration of the package: the file types that each rule applies to |
| [`meta.json`](meta.json) | The Vale version that the package requires |
| [`coverage/`](coverage/) | The rules of the style by section, and whether the package checks each rule |
| [`fixtures/<Rule>/`](fixtures/) | A `.vale.ini` that enables one rule, and lines with and without an alert of that rule |
| [`testdata/<Rule>.txt`](testdata/) | The expected alerts of `fixtures/<Rule>/` |
| [`fixtures/package/`](fixtures/package/) | A sample of each file type that the configuration of the package distinguishes |
| [`fixtures/valid/`](fixtures/valid/) | Markdown and Rust files that must not produce an alert |
| [`fixtures/expected.txt`](fixtures/expected.txt) | The alerts of `fixtures/package/` |
| [`scripts/package.py`](scripts/package.py) | The script that builds the package `Micllam.zip` |
| [`scripts/guide.py`](scripts/guide.py) | The script that writes `docs/agent-guide.md` from the style and `coverage/` |
| [`tests/`](tests/) | The tests of the rules, the package and the plugin |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | The manifest of the Claude Code plugin |
| [`skills/prose-check/`](skills/prose-check/) | The skill of the plugin, with the script that runs the package in its `scripts/` |
| [`hooks/`](hooks/) | The edit hook of the plugin and its `hooks.json` |

## Coverage

The files in `coverage/` list the rules of `docs/writing-style.md` by section,
with a key for each bullet. The key of a rule is the anchor of its bold lead-in,
and the key of a vocabulary entry is the anchor of its words before the first
colon or parenthesis. A key is `true` when the package checks the rule and
`false` when it does not, and a comment refers to the Vale rules that check it.

## Changing the style

A change to the style must start with `docs/writing-style.md`. The rules of the
package must then follow it:

- A rule in `styles/Micllam/` must implement one bullet of the style, and its
  key in `coverage/` must record the bullet with the rule.
- A rule must be named after its concept and must link to its section of the
  style.
- A word list such as the vocabulary must be a single substitution rule, with
  the replacement of each entry. Each entry of the Vocabulary section with a
  matchable form must have an entry in `Vocabulary.yml` and a line in its
  fixture.
- A new rule must come with its fixture and its manifest key, which the tests
  require.
- Each bullet of the style must have its key in `coverage/`. After a change to
  the style or to `coverage/`, run `scripts/guide.py`, which writes the bullets
  whose key is `false` to `docs/agent-guide.md`.
- An entry of a project style that a second project needs must move to the
  Vocabulary section of the style and to `Vocabulary.yml`.

## Tests

Run the tests with `python3 -m unittest`, and a single module with its name,
such as `python3 -m unittest tests.test_rules`. They require Python 3.9 or later
and `vale`. After a change to a rule or to `.vale.ini`, run the command with
`UPDATE_ALERTS=1` set. The tests then write the new alerts to `testdata/` and
`fixtures/expected.txt`.

`tests/test_plugin.py` runs the hook without Claude Code. After a change to
`.claude-plugin/plugin.json`, `hooks/hooks.json` or the layout of the plugin,
run `claude plugin validate .` to check the manifests. Then start a session with
`--plugin-dir` and check that Claude Code loads the skill and runs the hook.

## Release

The release commit must add the section of the version to `CHANGELOG.md` and set
the version in the `Packages` URL of `README.md`. A change to the rules, the
configuration, the style or the Vale requirement must have an entry in
`CHANGELOG.md`.

A tag that starts with `v` runs the release workflow. Its first job runs the
test workflow with `PACKAGE_REF` set to the tag, which builds and tests
`Micllam.zip`. The second job attaches the tested zip to a GitHub release whose
notes are the section of the version, and fails without the section. Each rule
of the release links to the style at the tag.

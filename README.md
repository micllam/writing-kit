# writing-kit

The writing style in `docs/writing-style.md` and the Vale package `Micllam`,
which checks the rules of the style that a pattern can match: excluded words,
sentence forms, spelling and formatting. Each rule links to the section of the
style it enforces, and Vale shows the link with the alert. The package requires
Vale 3.23.0 or later. A Claude Code plugin runs the package on the prose that an
agent writes.

## Layout

| Path | Contents |
|---|---|
| [`docs/writing-style.md`](docs/writing-style.md) | The writing style: content, CHANGELOG entries, commit messages, sentences, punctuation and vocabulary |
| [`docs/agent-guide.md`](docs/agent-guide.md) | The rules of the style that the package does not check, for the instructions that an agent reads in every session |
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
| [`tests/`](tests/) | The tests of the rules, the package and the plugin |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | The manifest of the Claude Code plugin |
| [`skills/prose-check/`](skills/prose-check/) | The skill of the plugin, with the script that runs the package in its `scripts/` |
| [`hooks/`](hooks/) | The edit hook of the plugin and its `hooks.json` |

## Use

List the package in the `.vale.ini` of the project:

```ini
StylesPath = .vale/styles
Packages = https://github.com/micllam/writing-kit/releases/download/v0.4.0/Micllam.zip
```

Run `vale sync` after a clone and after a change to `Packages`. To upgrade the
package, change the version in `Packages`. The section of `CHANGELOG.md` for the
new version lists the changes to the rules. The configuration of the package
selects the rules by file type:

- Markdown: every rule, with lines wrapped at 80 columns. The list rule runs on
  `CHANGELOG.md` only, and a fenced code block is code.
- Rust: every rule on the comments and doc comments, with the comment wrap,
  title-comment and section-divider rules. A string literal, the message of an
  `#[error("...")]` attribute and the content of a code fence in a doc comment
  are code.
- A commit message, as `COMMIT_*.txt` written by Git: every rule, as Markdown,
  with the subject and 72-column rules.
- Plain text: every rule, without the wrap.
- Shell, TOML and Python: the comment wrap and section-divider rules only.
- Any other file type: no rule.

Add the rules of the project, such as a substitution rule for its vocabulary, as
a second style in `StylesPath`. List both styles in each section of the
`.vale.ini`, because a section that lists the project style alone disables the
package for that file type.

```ini
[*.{md,rs}]
BasedOnStyles = Micllam, Project
```

`vale sync` writes the package into `StylesPath`. Commit the style folder of the
project, and ignore the other contents of `StylesPath` in Git.

A `<!-- vale off -->` marker in a Markdown file must have a closing
`<!-- vale on -->` marker, even at the end of the file. Without the closing
marker, Vale 3.23.0 drops the alerts of the wrap and list rules for the whole
file.

In CI, the official action runs the package and reports each alert as an
annotation. On a pull request it checks the added lines, and on a push it checks
the whole repository. GitHub shows at most ten annotations of a step, and the
job log lists every alert.

Refer to each action by its commit hash, as the workflows of this repository do,
and set the Vale version of `meta.json`:

```yaml
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
- uses: vale-cli/vale-action@518a9136acc6e6668ce7c00d367051e0941e87ff # v3.0.0
  with:
    version: 3.23.0
    fail_on_error: true
```

The style also states the rules that a pattern cannot check, such as the content
of a docstring or the topic of a paragraph. Apply those in review.
`docs/agent-guide.md` collects them for the instructions of an agent, whose
other prose rules the package reports on each edit.

## Plugin

The Claude Code plugin `writing-kit` requires Vale 3.23.0 or later and Python
3.9 or later. To load the plugin, start a session with the path of a checkout of
this repository:

```bash
claude --plugin-dir path/to/writing-kit
```

To load the plugin in every session, set `CLAUDE_CODE_PLUGIN_DIRS` to the path
of the checkout. Claude Code loads the checkout in place, so a change to the
checkout takes effect at the next session.

The skill `prose-check` of the plugin runs the package on the named files and on
the files in the named folders. Its script exits with status 1 when Vale reports
an alert, and with status 2 when Vale fails or the command does not have a path.

The hook of the plugin runs the script on each file that `Edit` or `Write`
changes, and returns the alerts to the agent. Vale checks the file types that
the configuration selects and skips the others. The hook runs the script from
the folder of the nearest `.vale.ini` above the file, or else from the folder of
the file.

The script uses the `.vale.ini` of the project when the project has one and its
`StylesPath` exists, and the `.vale.ini` of the checkout otherwise. For a
`StylesPath` that does not exist, the script also prints a warning to run
`vale sync`.

## Coverage

The files in `coverage/` list the rules of `docs/writing-style.md` by section. A
key is `true` when the package checks the rule and `false` when it does not, and
a comment refers to the Vale rules that check it.

## Changing the style

A change to the style must start with `docs/writing-style.md`. The rules of the
package must then follow it:

- A rule in `styles/Micllam/` must implement one bullet of the style, and its
  key in `coverage/` must record the bullet with the rule.
- A rule must be named after its concept and must link to its section of the
  style.
- A word list such as the vocabulary must be a single substitution rule, with
  the replacement of each entry.
- A new rule must come with its fixture and its manifest key, which the tests
  require.
- A rule without a Vale rule must be a bullet of `docs/agent-guide.md` whose
  bold lead-in matches its manifest key. The bullet must leave the guide when
  the rule gets a Vale rule.
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
the version in the `Packages` URL of this README. A change to the rules, the
configuration, the style or the Vale requirement must have an entry in
`CHANGELOG.md`.

A tag that starts with `v` runs the release workflow. Its first job runs the
test workflow with `PACKAGE_REF` set to the tag, which builds and tests
`Micllam.zip`. The second job attaches the tested zip to a GitHub release whose
notes are the section of the version, and fails without the section. Each rule
of the release links to the style at the tag.

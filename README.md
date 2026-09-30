# writing-kit

The writing style in `docs/writing-style.md` and the Vale package `Micllam`,
which checks the rules of the style that a pattern can match: excluded words,
sentence forms, spelling and formatting. Each rule links to the section of the
style it enforces, and Vale shows the link with the alert. The package requires
Vale 3.23.0 or later.

## Layout

| Path | Contents |
|---|---|
| [`docs/writing-style.md`](docs/writing-style.md) | The writing style: content, CHANGELOG entries, commit messages, sentences, punctuation and vocabulary |
| [`styles/Micllam/`](styles/Micllam/) | 30 rules, one per concept of the style |
| [`styles/config/scripts/`](styles/config/scripts/) | The Tengo scripts of the wrap, title-comment and CHANGELOG rules |
| [`.vale.ini`](.vale.ini) | The configuration of the package: the file types that each rule applies to |
| [`meta.json`](meta.json) | The Vale version that the package requires |
| [`coverage/`](coverage/) | The rules of the style by section, and whether the package checks each rule |
| [`fixtures/<Rule>/`](fixtures/) | A `.vale.ini` that enables one rule, and lines with and without an alert of that rule |
| [`testdata/<Rule>.txt`](testdata/) | The expected alerts of `fixtures/<Rule>/` |
| [`fixtures/package/`](fixtures/package/) | A sample of each file type that the configuration of the package distinguishes |
| [`fixtures/valid/`](fixtures/valid/) | Markdown and Rust files that must not produce an alert |
| [`fixtures/expected.txt`](fixtures/expected.txt) | The alerts of `fixtures/package/` |
| [`scripts/`](scripts/) | The scripts that build and test `dist/Micllam.zip` |

## Use

A project lists the package in its `.vale.ini`:

```ini
StylesPath = .vale/styles
Packages = https://github.com/micllam/writing-kit/releases/download/v0.1.0/Micllam.zip
```

Run `vale sync` after a clone and after a change to `Packages`. An upgrade of
the package is a change to the version in `Packages`, and the section of
`CHANGELOG.md` for the new version lists the changes to the rules. The
configuration of the package selects the rules by file type:

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

A project adds its own rules as a second style in `StylesPath`, such as a
substitution rule for the vocabulary of its domain, and lists both styles in
each section of its `.vale.ini`. A section that lists the project style alone
disables the package for that file type.

```ini
[*.{md,rs}]
BasedOnStyles = Micllam, Project
```

`vale sync` writes the package into `StylesPath`. A project commits its own
style folder and ignores the other contents of `StylesPath` in Git.

In CI, the official action runs the package on a pull request and reports each
alert of an added line as a review comment. A project refers to each action by
its commit hash, as the workflows of this repository do:

```yaml
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
- uses: vale-cli/vale-action@518a9136acc6e6668ce7c00d367051e0941e87ff # v3.0.0
  with:
    fail_on_error: true
```

The style also states the rules that a pattern cannot check, such as the content
of a docstring or the topic of a paragraph. A project applies those in review.

## Coverage

The files in `coverage/` list the rules of `docs/writing-style.md` by section. A
key is `true` when the package checks the rule and `false` when it does not, and
a comment refers to the Vale rules that check it.

## Changing the style

A change to the style is a change to `docs/writing-style.md` first. A rule in
`styles/Micllam/` then implements one bullet of the style, and its key in
`coverage/` records the bullet with the rule. A rule is named after its concept
and links to its section of the style. A single substitution rule checks a word
list such as the vocabulary, with the replacement of each entry. A new rule
comes with its fixture and its manifest key, and the tests fail without either.
An entry of a project style that a second project needs moves to the Vocabulary
section of the style and to `Vocabulary.yml`.

## Tests

`go test ./...` runs Vale in the fixture folder of each rule in `styles/` and
fails when the alerts differ from the file of the rule in `testdata/`, or when a
rule does not have a fixture. `go test ./... -update` records the new alerts
after a change to a rule. The test also fails when a value in `coverage/` is not
`true` or `false`, when a comment refers to a rule that does not exist or when
no manifest refers to a rule. It requires Go and `vale`.

`scripts/test.sh` builds the package, installs it in a temporary project and
runs it on `fixtures/valid/`, `README.md`, `CHANGELOG.md` and
`fixtures/package/`. Only this test reads the configuration of the package in
`.vale.ini`. It fails when a valid fixture, the README or the CHANGELOG produces
an alert, when the alerts of `fixtures/package/` differ from
`fixtures/expected.txt`, when the README does not state the Vale version of
`meta.json` or when the `Packages` URL of the README does not have the version
of the last section of `CHANGELOG.md`. After a change to `.vale.ini`, the
command `scripts/test.sh --update` writes the new alerts to
`fixtures/expected.txt`. The test requires `vale` and `zip`.

## Release

The release commit adds the section of the version to `CHANGELOG.md` and sets
the version in the `Packages` URL of this README. A tag that starts with `v`
then runs the release workflow, which tests the package and attaches
`Micllam.zip` to a GitHub release whose notes are that section. The workflow
fails without the section. An entry in `CHANGELOG.md` covers a change to the
rules, the configuration, the style or the Vale requirement.

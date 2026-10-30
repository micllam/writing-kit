# writing-kit

writing-kit helps a software project keep its prose plain and exact, from doc
comments and code comments to READMEs, CHANGELOG entries and commit messages.
Its writing style asks for a formal, neutral tone, with literal verbs, one term
per concept and short sentences.

In an editor or in CI, the Vale package `Micllam` checks the rules that a
pattern can match and links each alert to its rule in
[the style](docs/writing-style.md). [The agent guide](docs/agent-guide.md) gives
a coding agent the other rules, such as the content of a docstring, to apply as
it writes.

## Example

For this text, the package reports each excluded form with its replacement:

```markdown
The worker walks the store since the cache is cold.

The flag is what makes the write safe.
```

```text
example.md:1:12:Micllam.Vocabulary:'reads sequentially, traverses' for 'walks'
example.md:1:28:Micllam.Vocabulary:'because' for 'since'
example.md:1:38:Micllam.Vocabulary:'state the literal property' for 'cache is cold'
example.md:3:10:Micllam.Cleft:No "X is what does Y" cleft: 'is what'
```

The revised text passes: "The worker scans the store because the cache is empty.
The flag makes the write safe."

## Vale package

The package requires Vale 3.23.0 or later. List it in the `.vale.ini` of the
project:

```ini
StylesPath = .vale/styles
Packages = https://github.com/micllam/writing-kit/releases/download/v0.4.0/Micllam.zip
```

The package checks Markdown, plain text, commit messages and Rust comments, and
the comment wrap of shell, TOML and Python files. Its [`.vale.ini`](.vale.ini)
shows which rules apply to each file type.

A project can add its own rules, such as its vocabulary, as a second style in
`StylesPath`. List both styles in each section of the `.vale.ini`. A section
that lists the project style alone turns the package off for its files:

```ini
[*.{md,rs}]
BasedOnStyles = Micllam, Project
```

Close each `<!-- vale off -->` marker in a Markdown file with
`<!-- vale on -->`, even at the end of the file.

In CI, the official Vale action runs the package and reports each alert as an
annotation:

```yaml
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
- uses: vale-cli/vale-action@518a9136acc6e6668ce7c00d367051e0941e87ff # v3.0.0
  with:
    version: 3.23.0
    fail_on_error: true
```

## Claude Code plugin

The plugin `writing-kit` runs the package inside Claude Code. It requires Vale
3.23.0 or later and Python 3.9 or later. To load it, clone this repository and
start Claude Code with the path of the clone:

```bash
claude --plugin-dir path/to/writing-kit
```

To load the plugin in every session, set `CLAUDE_CODE_PLUGIN_DIRS` to the same
path.

The hook of the plugin checks each edited file and returns the alerts with the
result of the edit. The skill `prose-check` runs the same check on named files,
as a final pass before the work is done. Both use the `.vale.ini` of the
project, or the configuration of this repository for a project without a
`.vale.ini`.

## Contributing

[`CONTRIBUTING.md`](CONTRIBUTING.md) describes the layout of the repository, the
change of a rule, the tests and the release.

## License

writing-kit is released under the [MIT License](LICENSE).

---
name: prose-check
description: Check new or named prose against the writing style with the Vale package of writing-kit. Run after writing any doc comment, README, book page, CHANGELOG entry or commit message, and again before reporting the work as done.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/prose-check.py *)
---

# prose-check

Run the check from the project root on each file that the work changed:

```bash
${CLAUDE_SKILL_DIR}/scripts/prose-check.py PATH...    # the named files, and the files in the named folders
```

Each alert states its rule, and a vocabulary alert states the replacement. The
commit rules run on a file named `COMMIT_*.txt`. Exit status 1 means at least
one alert, and exit status 2 means that the check did not run.

For every alert, apply the rule of the style that the alert links to. An alert
stays where the rule permits it, such as a quoted excluded word or a
counterfactual with a stated condition.

After a clean check, read each new paragraph against the Content section of the
agent guide, which the package does not check. Check the three longest new
sentences against the length limits, and check that each new comment is
justified line by line.

For a commit message, test each sentence of the body. A sentence stays when it
states a reason that no line added by the diff states, an alternative that was
rejected or a consequence that the diff does not show. The added lines include
those of a CHANGELOG entry, a doc comment and a book page. Delete a sentence
that fails all three, and omit a body whose every sentence fails: the subject
alone is a complete message. Report the result for each sentence with the
suggested message.

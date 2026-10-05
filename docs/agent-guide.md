# Writing style for agents

The rules of [`writing-style.md`](writing-style.md) that the Vale package
`Micllam` does not check. An agent reads this file in every session, and the
package reports the other rules on each edit with a link to the style. The bold
lead-in of each rule matches its key in `coverage/`.

## Content

- **Essential only.** State the essential only: what a type or function is, its
  non-obvious behaviour, the one fact a reader needs. One or two sentences for a
  method, a short paragraph for a type or module. A correction found while
  investigating is stated in one or two lines, without the investigation.
- **Formal register.** Formal register throughout, as in a reference manual. No
  conversational or informal phrasing ("takes the hit", "the queue is happy").
  The vocabulary list of the style covers the recurring cases, and a phrase
  absent from the list is not permitted by its absence.
- **No rationale in comments.** A docstring or comment does not list call sites,
  argue for the choice, describe the alternative or narrate the mechanism.
  Rationale goes in the commit message or in a decision record. A comment longer
  than the code it explains is a signal to move or delete the explanation.
- **Current behaviour.** Write current behaviour. No historical narrative, and
  no negative space (do not document what a record no longer includes).
- **Cross-references.** Cross-reference only when the reader needs the link. A
  method on the same type is discoverable without a pointer. A pointer
  identifies its target or says "that follows".
- **Concept terms.** Define a concept term at its first use, in under ten words,
  one definition per sentence. Do not define product names, standard names
  (Postgres, S3, HTTP) or the project the document is about.
- **Architectural categories.** Public docs (READMEs, API docs, announcements)
  compare against architectural categories, never named products. An integration
  target that the text compliments can be named.

## CHANGELOG entries

- **Public surface only.** An entry covers a change to the public surface only:
  API, behaviour, on-disk format or dependencies. An example, a benchmark or
  another repository addition does not get an entry.
- **Change and migration.** An entry has one sentence for the change and its
  consequence for a user and a second sentence for the migration.
- **Relative to last release.** An unreleased entry is written relative to the
  last released version. A fix to an unreleased feature folds into that
  feature's entry. A type that never shipped does not break anything and does
  not get an entry.
- **Append at end.** A new entry is appended at the end of its section's list,
  so a section reads in the order of the changes. The entries of released
  versions are historical records and are not repaired.

## Commit messages

- **Subject style.** The subject is in the repository's style. Without an
  established style, the subject is `area: summary` in the imperative, in lower
  case after the prefix and without a full stop. It is under 50 characters where
  possible.
- **Body content.** The body states only what the diff does not show: the
  reason, a rejected alternative or a non-obvious consequence. It does not
  describe how the new code works, and it does not narrate the work that led to
  the change. A rejected alternative starts with "Rejected:", identifies the
  design and states its problem in one sentence ("Rejected: KV keys for the
  records. A staged write would have become visible only at settlement").

## Sentences

- **Sentence length.** 25 words maximum for descriptive prose, 20 for
  procedural. An identifier or a backticked name counts as one word.
- **Paragraph length.** Six sentences maximum per paragraph and one topic per
  paragraph, with two to four sentences in a book or a README. Split a longer
  paragraph at its topic change.
- **Active voice.** Active voice by default, with the component named as the
  actor ("the cache evicts the entry"). In descriptive prose a passive is
  correct when its subject is the paragraph's topic and the actor is named in
  the paragraph. Do not give a task, worker or code path a person-like verb.
- **No action verb for a setting.** Do not give a parameter, a limit or a
  setting an action verb. Make the component that applies the value the actor
  ("the operator kills the program").
- **Verb over copula.** A verb over a copula that equates two noun phrases: "the
  invoice is issued at the deadline", never "the issue time is the deadline".
- **Requirement with must.** State a requirement with "must", "require" or
  "will need to", never with a plain present verb ("a caller sets `timeout`").
  When a type imposes the requirement, make the type the subject.
- **Rejected design.** A rejected design gets one counterfactual sentence, or a
  sentence that states what the design prevents. A longer description of that
  design is in the present tense.
- **Condition first.** In procedural text, a condition comes before the
  instruction it applies to, with a comma. In descriptive prose the condition
  goes where the emphasis belongs.

## Punctuation and formatting

- **Bold and emoji.** Bold only as the lead-in of a list item or a paragraph
  that states a rule or an invariant. No emoji.
- **Vertical lists.** A vertical list is for three or more parallel items. It
  has a colon on the lead-in, an upper-case start and no nested lists, and it
  never mixes facts and instructions. Three or more parallel statements in prose
  become a list, and a bullet that runs to several sentences becomes a
  subheading with a short paragraph.
- **Short headings.** A heading is a short phrase.
- **Warning order.** A warning states the command or the condition first and the
  risk second.
- **No rewording of code.** Never reword code, identifiers, commands, flags,
  file paths, quoted error text or product names.

## Vocabulary

- **One term per concept.** One term per concept across a document: do not
  alternate between check, verify and confirm or between config and settings.
- **Noun chains.** Break a noun chain over three words with a preposition.
- **Strand.** `strand`: state the literal effect or condition.
- **Costs.** `costs X`, `pay a cost`, `tax` (of an operation, a loss, a choice
  or a design): state the literal cost (a count of reads, writes, scans or lock
  acquisitions) or identify the operation or what is avoided.
- **One as an article.** `one` as an article where the count is not the point:
  a, an ("the step job of a run"). A count stays ("one step job per run").
- **Floor, envelope.** `floor`: lower bound. `envelope`: range, profile.
- **Collapse.** `collapse` (of a metric): fall.
- **Just and glue.** Delete `just` and `glue` outright.

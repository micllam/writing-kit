# Writing style for agents

The rules of [`writing-style.md`](writing-style.md) that the Vale package
`Micllam` does not check. An agent reads this file in every session, and the
package reports the other rules on each edit with a link to the style. The bold
lead-in of each rule matches its key in `coverage/`.

## Content

- **Essential only.** State the essential only: what a type or function is, its
  non-obvious behaviour, the one fact a reader needs. Write one or two sentences
  for a method and a short paragraph for a type or module. State a correction
  found while investigating in one or two lines, without the investigation.
- **Formal register.** Write in a formal register throughout, as in a reference
  manual. Do not use conversational or informal phrasing ("takes the hit", "the
  queue is happy"). The vocabulary list of the style covers the recurring cases,
  and a phrase absent from the list is not permitted by its absence.
- **No rationale in comments.** In a docstring or comment, do not list call
  sites, argue for the choice, describe the alternative or narrate the
  mechanism. Put rationale in the commit message or in a decision record. Treat
  a comment longer than the code it explains as a signal to move or delete the
  explanation.
- **Current behaviour.** Write current behaviour. Do not write historical
  narrative or negative space (what a record no longer includes).
- **Cross-references.** Cross-reference only when the reader needs the link. A
  method on the same type is discoverable without a pointer. In a pointer,
  identify its target or write "that follows".
- **Concept terms.** Define a concept term at its first use, in under ten words,
  one definition per sentence. Do not define product names, standard names
  (Postgres, S3, HTTP) or the project the document is about.
- **Architectural categories.** In public docs (READMEs, API docs,
  announcements), compare against architectural categories, never named
  products. An integration target that the text compliments can be named.

## CHANGELOG entries

- **Public surface only.** Write an entry for a change to the public surface
  only: API, behaviour, on-disk format or dependencies. Do not write an entry
  for an example, a benchmark or another repository addition.
- **Change and migration.** Write an entry as one sentence for the change and
  its consequence for a user and a second sentence for the migration.
- **Relative to last release.** Write an unreleased entry relative to the last
  released version. Fold a fix to an unreleased feature into that feature's
  entry. A type that never shipped does not break anything, so do not write an
  entry for it.
- **Append at end.** Append a new entry at the end of its section's list, so
  that a section reads in the order of the changes. Do not repair the entries of
  released versions, which are historical records.

## Commit messages

- **Subject style.** Write the subject in the repository's style. Without an
  established style, write the subject as `area: summary` in the imperative, in
  lower case after the prefix and without a full stop. Keep it under 50
  characters where possible.
- **Body content.** In the body, state only what the diff does not show: the
  reason, a rejected alternative or a non-obvious consequence. Do not describe
  how the new code works or narrate the work that led to the change. Start a
  rejected alternative with "Rejected:", identify the design and state its
  problem in one sentence ("Rejected: KV keys for the records. A staged write
  would have become visible only at settlement").

## Sentences

- **Sentence length.** Write at most 25 words in a sentence of descriptive prose
  and 20 in procedural prose. Count an identifier or a backticked name as one
  word.
- **Paragraph length.** Write at most six sentences in a paragraph and one topic
  per paragraph, with two to four sentences in a book or a README. Split a
  longer paragraph at its topic change.
- **Active voice.** Use the active voice by default, with the component named as
  the actor ("the cache evicts the entry"). In descriptive prose a passive is
  correct when its subject is the paragraph's topic and the actor is named in
  the paragraph. Do not give a task, worker or code path a person-like verb.
- **No action verb for a setting.** Do not give a parameter, a limit or a
  setting an action verb. Make the component that applies the value the actor
  ("the operator kills the program").
- **Verb over copula.** Use a verb, never a copula that equates two noun
  phrases: "the invoice is issued at the deadline", never "the issue time is the
  deadline".
- **Must and should.** State a requirement with "must", "require" or "will need
  to" and a recommendation with "should". Never state an action that the reader
  takes with a plain present verb ("a caller sets `timeout`"). When a type
  imposes the requirement, make the type the subject.
- **Tense and aspect.** Use the simple present for a general behaviour, a kind
  or a standing fact. Use the progressive or a participle for the state of a
  particular instance at a time ("the job waiting for zero"). Write "will" for a
  planned action or a decision about a future action. Use the present perfect
  for a state that a past event produced and the past for a dated event.
- **Rejected design.** Give a rejected design one counterfactual sentence, or a
  sentence that states what the design prevents. Write a longer description of
  that design in the present tense.
- **Condition first.** In procedural text, put a condition before the
  instruction it applies to, with a comma. In descriptive prose, put the
  condition where the emphasis belongs.

## Punctuation and formatting

- **Bold and emoji.** Use bold only as the lead-in of a list item or a paragraph
  that states a rule or an invariant. Do not use emoji.
- **Vertical lists.** Use a vertical list for three or more parallel items. Give
  it a colon on the lead-in and an upper-case start. Do not nest a list in it,
  and never mix facts and instructions in it. Turn three or more parallel
  statements in prose into a list. Turn a bullet that runs to several sentences
  into a subheading with a short paragraph.
- **Short headings.** Write a heading as a short phrase.
- **Warning order.** In a warning, state the command or the condition first and
  the risk second.
- **No rewording of code.** Never reword code, identifiers, commands, flags,
  file paths, quoted error text or product names.

## Vocabulary

- **One term per concept.** Use one term per concept across a document: do not
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

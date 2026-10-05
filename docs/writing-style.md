# Writing style

These rules apply to every piece of prose in a project: doc comments, code
comments, READMEs, a book, CHANGELOG entries and commit messages. The Vale
package `Micllam` in this repository checks the rules that a pattern can match,
the files in `coverage/` list which ones, and `agent-guide.md` states the rules
that the package does not check.

## Content

- State the essential only: what a type or function is, its non-obvious
  behaviour, the one fact a reader needs. One or two sentences for a method, a
  short paragraph for a type or module. A correction found while investigating
  is stated in one or two lines, without the investigation.
- Formal register throughout, as in a reference manual. No conversational or
  informal phrasing ("takes the hit", "the queue is happy"). The vocabulary list
  covers the recurring cases, and a phrase absent from the list is not permitted
  by its absence.
- A docstring or comment does not list call sites, argue for the choice,
  describe the alternative or narrate the mechanism. Rationale goes in the
  commit message or in a decision record. A comment longer than the code it
  explains is a signal to move or delete the explanation.
- Write current behaviour. No historical narrative, and no negative space (do
  not document what a record no longer includes).
- Cross-reference only when the reader needs the link. A method on the same type
  is discoverable without a pointer. A pointer identifies its target or says
  "that follows", never "above" or "below".
- Define a concept term at its first use, in under ten words, one definition per
  sentence. Do not define product names, standard names (Postgres, S3, HTTP) or
  the project the document is about.
- No reader-psychology narration and no didactic meta-framing ("It is tempting
  to", "Notice that", "worth internalizing", rhetorical questions). Never state
  the plain-language goal in the text itself.
- Public docs (READMEs, API docs, announcements) compare against architectural
  categories, never named products. An integration target that the text
  compliments can be named.
- No section-divider comments (a rule of dashes, equals signs or box characters)
  and no comment that only titles a group of items. Group with modules, types or
  blank lines, and describe the groups in the module docstring.

## CHANGELOG entries

- An entry covers a change to the public surface only: API, behaviour, on-disk
  format or dependencies. An example, a benchmark or another repository addition
  does not get an entry.
- An entry has one sentence for the change and its consequence for a user and a
  second sentence for the migration.
- An unreleased entry is written relative to the last released version. A fix to
  an unreleased feature folds into that feature's entry. A type that never
  shipped does not break anything and does not get an entry.
- No blank line between bullets, only around headings. The entries of released
  versions are historical records and are not repaired.
- A new entry is appended at the end of its section's list, so a section reads
  in the order of the changes.

## Commit messages

- The subject is in the repository's style. Without an established style, the
  subject is `area: summary` in the imperative, in lower case after the prefix
  and without a full stop. It is under 50 characters where possible and never
  over 72.
- The body states only what the diff does not show: the reason, a rejected
  alternative or a non-obvious consequence. It does not describe how the new
  code works, and it does not narrate the work that led to the change.
- A blank line separates the subject from the body, and every line of the
  message is within 72 columns.

## Sentences

- 25 words maximum for descriptive prose, 20 for procedural. An identifier or a
  backticked name counts as one word.
- Six sentences maximum per paragraph and one topic per paragraph, with two to
  four sentences in a book or a README. Split a longer paragraph at its topic
  change.
- Active voice by default, with the component named as the actor ("the cache
  evicts the entry"). In descriptive prose a passive is correct when its subject
  is the paragraph's topic and the actor is named in the paragraph. In a
  paragraph about the entry, "the entry is evicted by the cache" is correct. Do
  not address the reader as "you" and do not give a task, worker or code path a
  person-like verb. Do not give a parameter, a limit or a setting an action
  verb. Make the component that applies the value the actor ("the operator kills
  the program").
- A verb over a copula that equates two noun phrases: "the invoice is issued at
  the deadline", never "the issue time is the deadline".
- No classifying predicate that files a subject under a noun with a relative
  clause ("is a state that", "is a case where"). Name the actor and state the
  fact with a verb: "the runtime does not write a pointer without its job",
  never "a pointer without its job is a state that no runtime write produces".
- State a requirement with "must", "require" or "will need to", never with a
  plain present verb ("a caller sets `timeout`"). When a type imposes the
  requirement, make the type the subject ("`SubprocessParams` and `ShellParams`
  require `timeout`").
- A rejected design gets one counterfactual sentence, or a sentence that states
  what the design prevents ("The lock prevents two writers from overwriting each
  other"). A longer description of that design is in the present tense.
- No "-ing" clause after a comma (", leaving a key that looks untouched"). Write
  a sentence with a subject.
- In procedural text, a condition comes before the instruction it applies to,
  with a comma. In descriptive prose the condition goes where the emphasis
  belongs.
- Complete grammar: no contractions, and keep articles.
- No pronoun standing for a type, a value or a record ("every builder takes
  one", "the field is one", "compares with one"). Name the type or the value, or
  restate the relation ("the parameter type of every builder").
- No "X is what does Y" cleft. State the fact ("the order makes the write
  safe"). For emphasis, write "It is the order that makes the write safe".
- No possessive predicate that files items under a subject ("`A`, `B` and `C`
  are its errors", "`X` is its handle"). Name the relation: "It fails with `A`,
  `B` or `C`", "It exposes `X`".
- No clause that spells out what a caller can therefore do ("is sorted, so a
  caller can binary-search it").
- Plain negation, not a verb plus "no", "nothing" or "none". Write "does not
  include an expiry", never "includes no expiry", and "do not share a key",
  never "share no key". Existential and subject-position negation is correct
  ("there is no such record", "no task observes it"), and so is "no longer".
- No "X, not Y" contrast, no "rather than" and no "instead of". State the
  property positively. A terse structural contrast that is itself the content
  ("embedded, not operated") survives.

## Punctuation, spelling and formatting

- No em-dashes and no semicolons. Use a colon, a comma, parentheses or two
  sentences.
- No serial comma, in "and" lists and "or" lists alike: "A, B and C", "X, Y or
  Z". A comma joining two independent clauses stays, and so does the comma in a
  two-item construction. The one exception is a list whose meaning is ambiguous
  without it.
- No Latin abbreviations. Write "for example" or "that is", or list the items.
- British spelling in prose (behaviour, amortises, favour, catalogue). A term
  taken from an API or a format keeps its spelling (serialize). "Lower case" and
  "upper case" are two words as a noun and hyphenated before a noun (lower-case
  letters).
- "ad hoc" is two words, and the phrasal verb is "opt in", so "opts in to".
  "Signaller" has two l's.
- Bold only as the lead-in of a list item or a paragraph that states a rule or
  an invariant. No emoji.
- A vertical list is for three or more parallel items. It has a colon on the
  lead-in, an upper-case start and no nested lists, and it never mixes facts and
  instructions. Three or more parallel statements in prose become a list, and a
  bullet that runs to several sentences becomes a subheading with a short
  paragraph.
- A heading is a short phrase.
- A warning states the command or the condition first and the risk second.
- Never reword code, identifiers, commands, flags, file paths, quoted error text
  or product names.
- Prose and comment lines wrap at 80 columns. After an edit inside a wrapped
  paragraph, rewrap the paragraph.

## Vocabulary

One term per concept across a document: do not alternate between check, verify
and confirm or between config and settings. Break a noun chain over three words
with a preposition.

Avoid, and write instead:

- holds, supplies, carries, rides in, is carried in: contains, includes, is
  stored in, or name the field
- shape, shapes: pattern, form, model, variant
- lands on, lands in: is written to, is recorded against
- writes the store, reads the store (of a process, a writer or a command):
  writes to the store, reads from the store. "Reads the store and never writes":
  only reads from the store
- writes within, written within (a store, a URL, a prefix): writes to. "Within"
  states a position and stays there: "the key is within the prefix"
- governs: enables, determines, or name the control
- walks (a scan): reads sequentially, traverses
- gate, gated on (as a verb): hold until, waits for, conditional on. The noun
  compound (feature gate) is standard
- since (meaning because): because. however: but. therefore: sparingly
- need to, have to: an imperative, "it is necessary to" or "will need to"
- strand, out from under, when in doubt: state the literal effect or condition
- drive, drives, driven, driving (of a loop, a test, time or a scenario): runs,
  advances, sends, or state the action
- dies with: terminates when. wiped, cleans: removes
- hand-rolled: in-house, custom. stand up (a server): deploy
- hands (a job) to, hand-over, handed out: assigns to, assignment, or name the
  claim
- mint, mints, minted (of a handle, a token or a value): constructs, creates,
  builds, or name the constructor
- under (a key, a prefix, a tag), meaning stored at or keyed by: at, with,
  within, or name the key, as in "the record's key" or "stored at one key". The
  same for a key space ("the keys under it", "the keys under the prefix"): "the
  keys within it", "the keys with that prefix". "Under a lease" and "under a
  lock" are the standard senses and stay
- serves (a purpose, diagnosis, a view): is for, is used for, or state the
  purpose. serves traffic: accepts calls. leaves with: is removed with
- harmless (of a retry, a redelivery or a repeated pass): state the literal
  effect ("does not submit a second task instance")
- bookkeeping, housekeeping: name the operations (the cursor note, the counter
  increment), or "the work that follows the commit"
- behind, ahead of (of key order relative to a bound or a cursor, or of expiry
  order): before, after, sorts before, sorts after, due after. Of a feature or
  an option (sits behind, is behind a flag): is enabled by, requires,
  conditional on. A reader's lag behind the writer is the literal sense and
  stays
- proves, proved, proven (of a scan, a read or a comparison): establishes,
  records, or state the observation ("ended without a live key"). A theorem is
  proved, a scan is not
- finds nothing, found nothing, yields nothing (of a scan or a read): ended
  without a key, returned an empty page
- dead (of configuration, code, a value or an arm, as a metaphor): unreachable,
  unused, without effect, or state what it does not apply to. The dead-letter
  sense (a dead job, the dead set) stays
- cheap, expensive, keeps X cheap, costs X, pay a cost, tax (of an operation, a
  loss, a choice or a design): state the literal cost (a count of reads, writes,
  scans or lock acquisitions) or identify the operation or what is avoided
- hot path: name the path
- load-bearing (of a link, a sentence or a decision): necessary, or state what
  depends on it
- for free: by construction. bolted-on: separately maintained
- is noise: is negligible. earns its keep, earns its place: is justified
- dedupe: deduplicate. plumbing, machinery: mechanism, or name the components.
  impls: implementations
- pick: choose. handy: suitable. tells you: states. boasts: has
- name, names (as a verb, of a request, a field, a tag or an expression, meaning
  includes or specifies a value): includes, specifies, identifies, refers to, or
  state the field. The noun (a queue name) stays
- echo, echoes (of a response or a reply): repeats, copies, includes
- arm, arms, armed, re-arms (of a timer or a deadline): schedules, sets, or
  state the deadline. A match arm is the standard sense and stays
- whatever (as a determiner): any, every, or state the set
- one (as an article, where the count is not the point): a, an, as in "the step
  job of a run". A count stays: "one step job per run"
- answer, answers (of a request, a read, a store or a component, including
  "answer 400"): returns, reports, replies with, or state the response. A
  question is answered by a person only
- verdict (of an outcome, a result or a decision): outcome, result, failure, or
  state what was decided ("the operator reported a failure")
- pin, pins, pinned (of a hash, a version or a definition, meaning records and
  keeps a fixed value): records, fixed at, or state the field ("the graph run
  records the definition hash"). A pinned dependency in a manifest is the
  standard sense and stays
- takes it, takes them (of a method and its parameter): state the parameter, as
  in "the key order of a `kv_scan` listing"
- lack, lacks (of a value, a field or a record): is missing, does not have
- stamp, stamped (of a time): is recorded at, is dated. Of a field: sets, writes
- stands in for: is used in place of, or state which one is kept
- at the same version, at the same X (as a trailing qualifier): a sentence that
  states the field is unchanged
- born X, births (of a record's initial state): created in state X, creates
- takes X off, reads X off, reads X out of (a key, a record): parses X from,
  extracts X from, removes X from
- keys by, keyed on, keyed by: uses X as its key
- fits (as a verb, of a choice or an option): is right when, is the correct
  choice, applies when
- over (of a claim, a run or a delivery): ended, complete, finished
- leaves X behind, left behind: stored, held, or name what remains and where
- survive, survives, survived, surviving (of state across a crash, a restart or
  a close): persists across, remains after. Of code across a change: compiles
  after. Of a design or an exception to a rule: stands, stays
- lock, locks, locked, locking test (of a test and a contract): tests, checks,
  asserts, the test of the contract. A mutex lock and "under a lock" are the
  standard senses and stay
- steps over (of a scan): skips
- runs past, goes past (of a limit, a timeout or a deadline): exceeds, with the
  measured quantity as the subject ("the run time exceeds `timeout`")
- left out, leaves out (of a value or an item): omitted, omits, or state the
  condition
- beside (of state or a structure): separate from, together with, contains, or
  name the relation
- next to (of a process or a command that runs with another): alongside. The
  position of a file or an item next to another is the literal sense and stays
- the one writer, its one writer (of a record, a store or a key): the only
  writer. "One writer" as a count ("one process, one writer") stays
- make sense when: are warranted when. addresses the issue: corrects the fault
- cliff: sharp degradation. floor: lower bound. envelope: range, profile
- collapse (of a metric): fall. flat out: as fast as possible
- knob: parameter
- cold, warm (of a cache): state the literal property
- bag: collection. nobody: no task. stampede: contend on
- sweet spot, home ground: strongest fit
- leverage, utilize, harness: use. in order to: to. prior to: before
- ensure: make sure that. facilitate: help, make possible. enhance: improve
- functionality: function, feature. enables you to: lets a caller. streamline:
  make simpler
- delve into, dive into: read, examine. out of the box: by default. under the
  hood: internally
- crucial, pivotal, paramount: important. showcase, underscore: show
- foster, empower, bolster: help, support, let. furthermore, moreover: also
- meticulous: careful. holistic: full. paradigm: model. intricate: complex
- gracefully handles, blazingly fast: state what it does, or give the number
- Delete outright: simply, just, easily, seamlessly, robust, powerful,
  comprehensive, performant, in conclusion, in summary, it is worth noting,
  grab, spin up, baked in, chew through, glue, thundering herd, tapestry,
  testament, synergy

# Treebank status definitions

The Daphne catalog records scholarly review maturity and mechanical validation as
two independent properties. Neither property is a promise that a treebank is free
of errors. Daphne does not use a `final` status.

## Annotation status

### `converted`

The treebank was imported or converted into CoNLL-U, but it has not completed a
systematic Daphne review pass. It may contain conversion artifacts or inherited
annotation inconsistencies.

### `in_review`

Manual review is under way, but it does not yet cover the declared scope or the
whole work. When useful, the catalog's `review.coverage` and `review.notes` fields
should identify what has and has not been checked.

### `reviewed`

At least one end-to-end manual review pass has covered the declared scope. This
means that the treebank has received sustained scholarly attention; it does not
mean that review is exhaustive or that no known issues remain.

Promotion to `reviewed` should be based on a documented review pass, not solely on
the absence of validator errors.

## Enhanced dependencies

Enhanced dependencies are tracked independently from the general annotation
status because their coverage, review, and validation can differ from those of the
basic dependency tree.

### Encoding

- `none`: DEPS is consistently unpopulated.
- `sparse`: DEPS is populated only where an enhanced annotation is relevant.
- `complete`: a complete enhanced graph is attempted throughout the treebank.
- `mixed`: encoding differs within the record or among its files.

### Annotated phenomena

The `phenomena` map uses the categories defined by the UD enhanced-dependency
guidelines:

- `ellipsis`
- `coordination_incoming`
- `coordination_outgoing`
- `control_raising_subjects`
- `relative_clause_coreference`
- `case_information`

Each declared phenomenon has one of these support levels:

- `not_annotated`: the phenomenon is deliberately unsupported.
- `partial`: some known instances are annotated, without an intent of complete
  coverage.
- `systematic`: the annotation intends to cover every applicable instance.
- `unknown`: coverage has not been established.

The phenomena map is exhaustive: an omitted phenomenon is equivalent to
`not_annotated`. `Systematic` records annotation intent, not demonstrated
correctness or completeness.

### Provenance

When known, the optional `provenance` field records how enhanced dependencies were
created: `converted`, `generated`, `manual`, `mixed`, or `unknown`.

### Review and validation

The enhanced layer's `review_status` is `not_reviewed`, `in_review`, or `reviewed`.
Its `validation` object follows the same rules as general validation below. Review
and validation are independent: generated or converted DEPS may exist while both
remain incomplete.

All current catalog records declare sparse, systematic ellipsis annotation. No
other enhanced phenomenon is currently annotated; the enhanced layer has not been
reviewed or validated.

## Validation status

### `not_run`

No reproducible validation result has yet been recorded for the current file
content.

### `pass`

The current content passed the named validator on `validation.checked_at`. The
catalog must record both the validator and the date.

### `fail`

The named validator reported one or more errors on `validation.checked_at`. The
catalog must record both the validator and the date; details may be summarized in
`validation.notes`.

A validation result becomes stale whenever the corresponding CoNLL-U content
changes and should then return to `not_run` until validation is rerun.

## Catalog roles

### `primary`

The canonical Daphne treebank for the work and the edition intended for normal
use. A primary record must have a CTS URN.

### `legacy_variant`

An older or alternative Daphne representation retained for provenance and
migration. It is discoverable but is not the default treebank for the work.

### `legacy_external`

Material retained from the historical repository that is not currently presented
as a canonical Daphne edition. Its identifier or filename may require resolution
before it can become primary.

## Status maintenance

Status applies to catalog records, not branches. Development happens on `dev`,
while released snapshots are published from `master`. A treebank keeps its stable
identifier when its status changes.

The initial catalog classifications are conservative and derive from the project
owner's assessment together with the existing author-level README files. Future
changes should include a short explanation in the commit or in `review.notes`.

Backup files, temporary validator output, and editor-generated files are not
catalog records. A temporarily retained backup must instead appear in the
catalog's `path_exceptions` list with role `legacy_backup` and a reason. Path
exceptions are validated and must point to existing files; they are not silently
ignored.

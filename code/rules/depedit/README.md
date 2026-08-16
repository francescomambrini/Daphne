# DepEdit bulk-editing scenarios

This directory is the maintained home for reviewed DepEdit scenarios used to
apply a defined correction across multiple Daphne CoNLL-U files. The executable
integration belongs in `code/src/daphne_treebank/editing/`; scenarios contain
declarative DepEdit instructions, not ad-hoc Python or shell code.

Do not copy the historical configurations from `code/legacy/depedit/` here
without first reconstructing their assumptions and testing their behavior.

## Scenario layout

Give each transformation a stable, descriptive, lowercase identifier and keep
it in its own directory:

```text
code/rules/depedit/<scenario-id>/
├── README.md
└── scenario.ini

code/tests/fixtures/depedit/<scenario-id>/
├── input.conllu
└── expected.conllu
```

The scenario README must record:

- the correction and its linguistic rationale;
- the intended files or catalog records and any explicit exclusions;
- the DepEdit and scenario versions used;
- the author and review date;
- the expected match/change count when known;
- the validation and manual checks required after application.

Use comments in `scenario.ini` to connect individual instructions to that
documented rationale. A materially different transformation needs a new
scenario version or identifier rather than a silent change in meaning.

## Application workflow

1. Add minimal input and expected-output fixtures before applying the scenario
   to corpus data.
2. Run in preview mode and inspect the diff and match counts. Use `--input-file`
   for one explicit file; without it, the runner selects every `.conllu` file
   recursively under `data/annotation/` in the detected repository root.
3. Treat zero matches, unexpectedly broad matches, parse failures, and partial
   runs as conditions requiring review, not as successful edits.
4. Apply only after the preview is accepted. Preserve original files until the
   transformed output is complete, then replace them atomically.
5. Inspect the resulting Git diff and run the maintained tests and validators.
6. Reset catalog validation results made stale by changed CoNLL-U content, and
   record the scenario identity in the change history or commit message.

## Maintained runner

`daphne-edit` is non-mutating by default. Pass a scenario path and optionally
one input file:

```bash
uv run daphne-edit code/rules/depedit/<scenario-id>/scenario.ini \
  --input-file path/to/file.conllu
```

Omitting `--input-file` previews the scenario across all annotation files. The
report lists every selected file, changed-record and changed-file counts,
failures, and unified diffs. DepEdit does not expose a stable public match
counter, so the runner reports changed serialized records as its match proxy.
For token-only scenarios, the runner also preserves the source ordering and
spacing of comments, blank lines, and newline endings instead of accepting
DepEdit's incidental comment reordering.

Use `--report-tsv PATH` to atomically write a machine-readable manifest during
preview. It contains one row per changed CoNLL-U column, including the
repository-relative file, physical line number, sentence ID, token context,
column name, old value, and new value:

```bash
uv run daphne-edit code/rules/depedit/<scenario-id>/scenario.ini \
  --no-diff --report-tsv /tmp/daphne-depedit-preview.tsv
```

The TSV report supports located, line-preserving token changes. If a scenario
adds or removes lines or changes sentence annotations, report generation fails
instead of producing ambiguous locations. A report failure prevents `--apply`
from writing corpus files.

After reviewing the preview, repeat the command with `--apply` to replace each
changed file atomically. All transformations are completed in memory first, and
no file is written when any input fails. A run with no changes exits with status
1 as a review condition; configuration or processing failures exit with status
2.

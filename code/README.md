# Daphne code

This directory is the home of tools for maintaining the Daphne treebanks. New
code should support one of three main workflows:

- validation of CoNLL-U, catalog metadata, and supporting textual editions;
- conversion from source formats into Daphne's current representations;
- controlled correction or normalization of existing data.

The historical contents of the former `scripts/` directory are preserved under
`legacy/`. They are reference material, not the foundation of the new toolset.

## Intended architecture

```text
code/
├── src/       maintained application and library code
├── tests/     automated tests and small fixtures
├── rules/     declarative, reviewable correction rules
└── legacy/    archived historical scripts and artifacts
```

The first maintained component is the basic data checker under `src/`. Additional
tools should be introduced incrementally as specific legacy workflows are
understood and replaced.

## Requirements for new tools

New tools should:

- accept explicit input and output paths;
- avoid hard-coded user directories;
- avoid overwriting source data by default;
- offer a check or dry-run mode for mutations;
- write deterministically and atomically;
- report errors with a non-zero exit status;
- include focused tests and small fixtures;
- document any annotation assumptions that they encode.

Large corpora, generated validation output, local environments, and editor files
do not belong under `code/`.

## Basic data checks

The maintained checker verifies catalog schema and coverage, CoNLL-U
serialization, and XML well-formedness. It does not run the official UD validator
or perform linguistic evaluation.

Run the tests and check all annotation and textual-edition files from the
repository root:

```bash
uv sync --locked
uv run python -m unittest discover -s code/tests -v
uv run daphne-check --root .
```

The same commands run in GitHub Actions on every push and on pull requests that
target `master`.

`pyproject.toml` is the dependency source of truth and `uv.lock` makes the
environment reproducible. Add or update a dependency with `uv add`, and commit
both files when the lock changes. The reusable local environment lives in the
ignored `.venv/` directory.

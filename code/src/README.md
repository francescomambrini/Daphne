# Maintained source code

This directory is reserved for the maintained Daphne toolset. No legacy script is
considered migrated merely because a similar module name exists here.

The intended Python package should separate these responsibilities:

- `validation`: CoNLL-U, UD, CTS/TEI, filename, and catalog checks;
- `conversion`: explicit transformations from documented source formats;
- `editing`: safe preview and application of declarative correction rules,
  including the adapter around the pinned DepEdit API;
- `catalog`: catalog loading, schema validation, and derived reports;
- `io`: shared parsing and atomic file-writing utilities;
- `cli`: a single command-line entry point for supported workflows.

Modules should be added only together with tests and documented behavior.
DepEdit scenarios themselves belong under `code/rules/depedit/`, not in the
Python package.

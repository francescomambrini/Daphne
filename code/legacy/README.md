# Legacy scripts

This directory archives the tracked contents of Daphne's former `scripts/`
directory. The files were moved without changing their contents during the 2026
repository restructuring.

They are retained for provenance and to help reconstruct older workflows. They
are not maintained, tested, or guaranteed to run. In particular, individual
files may:

- contain obsolete or user-specific paths;
- depend on undeclared software or old library versions;
- overwrite input files or create backups beside them;
- assume the former `data/annotation/latest/` layout;
- contain generated corpora, reports, notebooks, or other working artifacts.

Inspect a legacy file before running it. When a workflow is still useful, its
behavior should be documented and reimplemented under `code/src/` with tests
rather than repaired in place here.

The `v0.5.0-legacy-layout` Git tag preserves these files at their original paths.

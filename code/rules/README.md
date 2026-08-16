# Correction rules

This directory is reserved for declarative correction and normalization rules
used by maintained tools. Each rule set should document its purpose, expected
input, scope, and review history.

Maintained DepEdit bulk-editing scenarios live under `depedit/`, one documented
scenario per subdirectory. Historical configurations remain under
`code/legacy/depedit/` until their behavior is audited. They should not be moved
into the maintained scenario area without focused input/output tests.

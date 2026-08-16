# Dative and genitive objects to `obl:arg`

Scenario ID: `nonaccusative-objects-to-obl-arg`  
Scenario version: 2  
DepEdit version: 4.0.0.0  
Proposed by: Francesco Mambrini  
Review date: pending

## Correction

Change basic `DEPREL` from `obj` or `iobj` to `obl:arg` when the node has an
explicit `Case=Dat` or `Case=Gen` feature.

The scenario does not change nodes with another case, no `Case` feature, or a
multi-valued feature such as `Case=Acc,Dat`. Restricting the match to exact
dative and genitive values prevents a possibly erroneous nominative analysis
of an underlying neuter accusative from being changed automatically. Other
dependency relations are outside the scenario.

## Scope and review

The intended scope is every CoNLL-U file under `data/annotation/`, including
cataloged legacy files and path exceptions; there are no work-specific
exclusions. A non-mutating preview on 2026-08-16 selected 29 files and found
10,865 changed records across all 29 under scenario version 2, with no
processing failures. The corpus was not changed.

Before applying, inspect the complete `daphne-edit` preview, with particular
attention to the distinction between core objects and oblique arguments. After
application, inspect the Git diff, reset any stale catalog validation status,
and run the maintained unit tests and `daphne-check`. Basic well-formedness does
not establish linguistic correctness.

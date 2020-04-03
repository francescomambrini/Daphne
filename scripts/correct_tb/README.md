# Correct Treebank

## Introduction

Series of local submodules for the AGLDT fork of [udapi-python](https://github.com/francescomambrini/udapi-python).

Scenarios may invoke both local and package blocks.

## How to

1. make sure these blocks are in your `$PYTHONPATH`
2. load the blocks in `udapy` using a "dot notation": e.g. `.Foo` for class `Foo(Block)` in foo.py

## Blocks

Blocks marked with "package" are available in `udapi-python`.

1. split craseis and conjuctions (package)
2. fix the lemmas for prons (package)
3. fix postag for particles and conjunctions (package)
4. fix various lemmas: θνήσκω, θρωσκω, φίλτατος, ἔχθιστος
5. fix postag for μή 
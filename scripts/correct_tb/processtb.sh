#!/usr/bin/env bash

IN="$HOME/trebank.xml"
OUT= "$HOME/treebank_edited.xml"

 udapy -v read.Agldt files="$IN" \
    SplitCrasis \
    SplitConjunctions  \
    .CorrectPos \
    .FixMePostag \
    .FixMePostag \
    .FixHos \
    .DeleteUnusedArti \
    write.Agldt files="$HOME/tlg0085.tlg003_EDITED.xml"


#!/usr/bin/env bash

# Odyssey 1-6
OD_IN_PATH="$HOME/Documents/sync/progetti/Daphne/data/annotation/latest/tlg0012/tlg002/tlg0012.tlg002.daphne_tb-grc1.1-6.conllu"
AJ_IN_PATH="$HOME/Documents/sync/progetti/Daphne/data/annotation/latest/tlg0011/tlg003/tlg0011.tlg003.daphne_tb-grc1.conllu"

udapy -s ud.MarkBugs < "$OD_IN_PATH" > od_1-6_makrkbugs.conllu
udapy -s ud.MarkBugs < "$AJ_IN_PATH" > aj_makrkbugs.conllu


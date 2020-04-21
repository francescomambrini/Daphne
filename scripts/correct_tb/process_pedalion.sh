#!/usr/bin/env bash

IN="/home/francesco/Documents/work/Nextcloud/Documents/Projects/Daphne/data/annotation/in_progress/tlg0011/tlg0011.tlg006.daphne_tb-grc1.xml"

udapy read.Pedalion files="$IN" \
    .FixCrasis \
    agldt.SplitConjunctions \
    .FixEisComp \
    .CorrectPos \
    .WriteDaphne files="${IN%.xml}_MODIFIED.xml" ;
 

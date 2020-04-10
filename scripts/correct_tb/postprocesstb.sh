#!/usr/bin/env bash

# IN="$HOME/trebank.xml"
# OUT= "$HOME/treebank_edited.xml"

_dfiles="$HOME/Documents/work/Nextcloud/Documents/Projects/Daphne/data/annotation/v03/tlg0011/*/*.xml"

for f in $_dfiles; do 
  udapy read.Agldt files="$f" \
    .FixSomeLex \
    .FixEisComp \
    .CorrectPos \
    .FixArticle \
    agldt.FixAdvPos \
    .FixMePostag \
    .FixHos \
    write.Agldt files="${f%.xml}_MODIFIED.xml" ;
  #udapy -s my.Block < $f > ${f%.conllu}_MODIFIED.conllu;
done
 

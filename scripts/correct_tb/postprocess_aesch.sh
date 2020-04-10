#!/usr/bin/env bash

# IN="$HOME/trebank.xml"
# OUT= "$HOME/treebank_edited.xml"

_dfiles="$HOME/Documents/work/Nextcloud/Documents/Projects/Daphne/data/annotation/v03/tlg0085/*/*.xml"

for f in $_dfiles; do 
  udapy read.Agldt files="$f" \
    .FixEisComp \
    .CorrectPos \
    .FixArticle \
    agldt.FixAdvPos \
    write.Agldt files="${f%.xml}_MODIFIED.xml" ;
  #udapy -s my.Block < $f > ${f%.conllu}_MODIFIED.conllu;
done
 

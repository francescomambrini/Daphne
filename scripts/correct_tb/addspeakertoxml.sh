#!/usr/bin/env bash

FS='!/home/francesco/Documents/work/Nextcloud/Documents/Projects/Daphne/data/annotation/*/*/*/*.xml'

udapy read.Agldt files="$FS" \
  agldt.agldt_util.SetSpeakers \
  util.Eval doc='doc.meta["docname"]=doc.meta["loaded_from"].split("/")[-1]' \
  .WriteDaphne docname_as_file=1 includeSpeakers=1

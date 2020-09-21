#!/usr/bin/env bash

FS='/home/francesco/Desktop/tlg0011.tlg004.daphne_tb-grc1.xml'

udapy read.Agldt files="$FS" \
  agldt.agldt_util.SetSpeakers \
  util.Eval doc='doc.meta["docname"]=doc.meta["loaded_from"].split("/")[-1]' \
  .WriteDaphne docname_as_file=1 includeSpeakers=1  

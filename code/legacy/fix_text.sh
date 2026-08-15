#!/usr/bin/env zsh

# Usage:
#   ./fix_text.sh path-to-file

udapy read.Conllu files=$1 \
  util.Eval tree='$.text = $.compute_text()' \
  write.Conllu files=$1

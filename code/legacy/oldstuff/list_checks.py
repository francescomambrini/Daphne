#!/usr/bin/env python

"""
Loops through the sentences of an XML treebank file. Checks whether there are 
places where the numbering of the tokens is wrong (i.e. there are two tokens with 
the same sequential id). Writes list of those tokens to a file

"""

import sys
from collections import defaultdict
from lxml import etree

x = etree.parse(sys.argv[1])
sents = x.xpath("//sentence")
checks = defaultdict(list)

for s in sents:
    words = s.xpath("word")
    sid = int(s.attrib["id"])
    prev = 0
    for w in words:
        i = int(w.attrib["id"])
        if i != prev + 1:
            checks[sid].append(str(i))
        prev = i
            
with open("to_be_checked.txt", "w") as out:
    for c in sorted(checks.keys()):
        lines = ",".join(checks[c])
        out.write(f"{c}\t{lines}\n")


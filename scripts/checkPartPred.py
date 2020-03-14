#!/usr/bin/env python

"""
Diagnostic script to get all cases of part pred tagged as ATV/AtvV
Returns the sentece Nr., ID, Tok ID and form

"""

import re
from lxml import etree
from glob import glob
import sys
import os

d = sys.argv[1]
assert os.path.isdir(d), f"Not a folder: {d}"

reg = re.compile(r'^A[Tt]t?V')

for fpath in glob(os.path.join(d, "*.xml")):
    x = etree.parse(fpath)
    print(f"### Working on: {fpath}")
    for i,s in enumerate(x.xpath("//sentence")):
        sid = s.attrib["id"]
        for w in s.xpath("word"):
            form = w.attrib.get("form") if w.attrib.get("form") else ""
            if w.attrib.get("postag"):
                mood = w.attrib.get("postag")[4]
                if mood == 'p' and reg.search(w.attrib["relation"]):
                    print(sid, w.attrib["id"], form)
                    




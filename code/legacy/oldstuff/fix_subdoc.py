#!/usr/bin/env python

from lxml import etree
import sys
import os

fpath = sys.argv[1]
x = etree.parse(fpath)
sents = x.xpath("//sentence")

def _get_ref(sent, last=False):
    toks = s.xpath("word")
    if last == True:
        toks = toks[::-1]
    for t in toks:
        c = t.attrib.get("cite")
        if c:
            return c.split(":")[-1]


for s in sents:
    first = _get_ref(s)
    last = _get_ref(s, True)
    s.attrib["subdoc"] = f"{first}-{last}"

fname = os.path.split(fpath)[-1]
x.write(fname, pretty_print=True,
            xml_declaration=True, encoding='UTF-8')

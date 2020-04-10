#!/usr/bin/env python

from glob import glob
from lxml import etree
import sys
import os

wd = sys.argv[1]
fs = sorted(glob(os.path.join(wd, "*.xml")))

print(f"First file: {fs[0]}\nSecond file: {fs[1]}")

assert len(fs) == 2, "there must be exactly 2 xml files to compare!"

first = etree.parse(fs[0])
second = etree.parse(fs[1])

fws = first.xpath("//word")
sws = second.xpath("//word")

assert len(fws) == len(sws), "files don't seem to be in sync!"

keys = ['form', 'postag', 'lemma', 'head', 'relation']

for f,s in zip(fws, sws):
    for k in keys:
        if f.attrib.get(k) != s.attrib.get(k):
            sent = f.getparent()
            sentid = sent.attrib.get("id")
            print(sentid, f.attrib['id'], f.attrib['form'], k, f.attrib.get(k), s.attrib.get(k))

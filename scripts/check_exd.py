#!/usr/bin/env python

import requests
from lxml import etree

u = "https://raw.githubusercontent.com/PerseusDL/treebank_data/master/v1/greek/data/tlg0011.tlg002.perseus-grc2.xml"

def check_sent(sent, sent_id, tag_index=0):
    tag = f"_ExD{tag_index}_"
    words = sent.xpath("word")
    heads = []
    ids = []
    for w in words:
        if tag in w.attrib["relation"]:
            heads.append(w.attrib["head"])
            ids.append((w.attrib["id"], w.attrib["form"]))
    if len(set(heads)) > 1:
        print(sent_id, ids)


response = requests.get(u)
x = etree.fromstring(response.content)
sents = x.xpath("//sentence")

for i,s in enumerate(sents, start=1):
    check_sent(s, i)
    check_sent(s, i, tag_index=1)
    check_sent(s, i, tag_index=2)

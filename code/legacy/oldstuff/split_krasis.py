#!/usr/bin/env python

import os
import sys
import re
from lxml import etree

reg_krasis = re.compile(r"[κχ](?=\w?[ὐὖὔἰἴἀἂἄἈὠᾀᾆἠὢὤὦᾦ])")
# reg_conj = re.compile(r"(?:εἴ|οὐ|μη|μή)(?=τε\b|δ[έἐ]\b|[τδθ][᾽'])")

x = etree.parse(sys.argv[1])
words = x.xpath("//word")

for w in words:
    form = w.attrib["form"]
    m = reg_krasis.match(form)
    if m:
        print(f"splitting the word: {w.attrib['form']} ({w.attrib['id']})")
        newel = etree.Element("word", id=w.attrib["id"])
        newel.attrib["form"] = m.group()
        newel.attrib["lemma"] = "καί"
        newel.attrib["postag"] = "c--------"
        cite = w.attrib.get("cite")
        if cite:
            newel.attrib["cite"] = w.attrib["cite"]
        newel.attrib["head"] = w.attrib["head"]
        newel.attrib["relation"] = "UNDEFINED"
        newform = re.sub("^[κχ]", "", form, count=1)
        w.attrib["form"] = newform
        w.addprevious(newel)

fname = os.path.split(sys.argv[1])[-1]

x.write(fname, pretty_print=True, xml_declaration=True, encoding='UTF-8')

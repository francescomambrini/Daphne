#!/usr/bin/env python

from lxml import etree
import re
import sys
import os

#reg_conj = re.compile(r"(?:εἴ|οὐ|μη|μή)(?=τε\b|δ[έἐ]\b|[τδθ][᾽'])")

oude = re.compile(r"(οὐ)(δ[έὲ'])") #["οὐδέ", "οὐδὲ", "οὐδ'"]
mhde = re.compile(r"(μη)(δ[έὲ'])") # ["μηδέ", "μηδὲ", "μηδ'"]
eite = re.compile(r"(εἴ)(τε|θ'|τ')") # ["εἴτε", "εἴτ'", "εἴθ'"]
oute = re.compile(r"(οὔ)(τε|θ'|τ')") # ["οὔτε", "οὔτ'", "οὔθ'"]
mhte = re.compile(r"(μή)(τε|θ'|τ')") # ["μήτε", "μήτ'", "μήθ'"] 

conjs =  ["οὐδέ", "οὐδὲ", "οὐδ'", "μηδέ", "μηδὲ", "μηδ'", "εἴτε", "εἴτ'", "εἴθ'",
            "οὔτε", "οὔτ'", "οὔθ'", "μήτε", "μήτ'", "μήθ'"]

x = etree.parse(sys.argv[1])
words = x.xpath("//word")

for w in words:
    form = w.attrib["form"]
    if form in conjs:
        newel = etree.Element("word", id=w.attrib["id"])
        #newel.attrib["form"] = m.group()
        #newel.attrib["lemma"] = "καί"
        newel.attrib["postag"] = "c--------"
        w.attrib["postag"] = "c--------"
        cite = w.attrib.get("cite")
        if cite:
            newel.attrib["cite"] = w.attrib["cite"]
        newel.attrib["head"] = w.attrib["head"]
        newel.attrib["relation"] = "UNDEFINED"
        moude = oude.search(form)
        mmhde = mhde.search(form)
        meite = eite.search(form)
        moute = oute.search(form)
        mmhte = mhte.search(form)
        
        if moude:
            w.attrib["form"] = moude.group(1)
            newel.attrib['form'] = moude.group(2)
            w.attrib["lemma"] = "οὐδέ"
            newel.attrib["lemma"] = "οὐδέ"
        elif mmhde:
            w.attrib["form"] = mmhde.group(1)
            newel.attrib['form'] = mmhde.group(2)
            w.attrib["lemma"] = "μηδέ"
            newel.attrib["lemma"] = "μηδέ"
        elif meite:
            w.attrib["form"] = meite.group(1)
            newel.attrib['form'] = meite.group(2)
            w.attrib["lemma"] = "εἴτε"
            newel.attrib["lemma"] = "εἴτε"
        elif moute:
            w.attrib["form"] = moute.group(1)
            newel.attrib['form'] = moute.group(2)
            w.attrib["lemma"] = "οὔτε"
            newel.attrib["lemma"] = "οὔτε"
        elif mmhte:
            w.attrib["form"] = mmhte.group(1)
            newel.attrib['form'] = mmhte.group(2)
            w.attrib["lemma"] = "μήτε"
            newel.attrib["lemma"] = "μήτε"
        
        w.addnext(newel)

fname = os.path.split(sys.argv[1])[-1]

x.write(fname, pretty_print=True, xml_declaration=True, encoding='UTF-8')

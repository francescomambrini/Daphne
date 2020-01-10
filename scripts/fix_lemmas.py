#!/usr/bin/env python

import sys
from lxml import etree

p = sys.argv[1]
x = etree.parse(p)

pronouns = ['ἐγώ', 'σύ', 'ἡμεῖς', 'ὑμεῖς', 'σφεῖς', 'ἐμός', 'σός', 'ἡμέτερος',
            'ὑμέτερος', 'ὅς', 'νωΐτερος', 'σφέτερος', 'ἐμαυτοῦ', 'σαυτοῦ', 'ἑαυτοῦ',
            'ἀλλήλων', 'ἄλλος', 'ὅδε', 'αὐτός', 'οὗτος', 'ἐκεῖνος', 'τόσος', 'τοσόσδε',
            'τοσοῦτος', 'τοῖος', 'τοιόσδε', 'τοιοῦτος', 'τήλικος', 'τηλικόσδε',
            'τηλικοῦτος', 'τίς', 'πότερος', 'πόσος', 'ποῖος', 'πηλίκος', 'ὅς',
            'ὁποῖος', 'ὅσος', 'ὁπόσος', 'ὁπότερος', 'ἡλίκος', 'ὁπηλίκος', 'τις',
            'ὅστις', 'ἑκάτερος', 'ἕκαστος', 'ποσός', 'ποιός', 'οἷος']

conjunctions = ['καί', "τε", "οὔτε", "μήτε", "μηδέ", "οὐδέ", "εἴτε"]

particles = ['ἆρα', 'αὖ', 'γάρ', 'γε', 'γοῦν', 'δέ', 'δή', 'εἶτα', 'κάρτα', 'καίπερ',
             'καίτοι', 'μά', 'μέν', 'μέντοι', 'μήν', 'μῶν',
             'οὖν', 'ποθι', 'περ', 'ποτέ', 'πού', 'πω', 'τοίνυν', 'τοι', 'τοιγάρ',
             'ἀτάρ', 'ἄν', 'ἄν1', 'ἄρα', 'ἆρα', 'ἤτοι', 'ἦ']


words = x.xpath("//word")
for w in words:
    try:
        lemma = w.attrib["lemma"]
    except KeyError:
        continue
    if lemma in pronouns:
        w.attrib["postag"] = "p" + w.attrib["postag"][1:]
        assert len(w.attrib["postag"]) == 9, "Woops! something wrong..."
    if lemma in conjunctions:
        w.attrib["postag"] = "c--------"
    if lemma in particles:
        w.attrib["postag"] = "d--------"
    if lemma == "ἄν" and w.attrib["relation"] == "AuxY":
        w.attrib["lemma"] = "ἄν1"
    if w.attrib["form"] == "μᾶλλον":
        w.attrib["lemma"] = "μᾶλλον"
        w.attrib["postag"] = "d-------c"
    if w.attrib["form"][:-1] == "μάλιστ":
        w.attrib["lemma"] = "μάλιστα"
        w.attrib["postag"] = "d-------s"

x.write("../data/annotation/temp/treebank_pos_fixed.xml", pretty_print=True,
            xml_declaration=True, encoding='UTF-8')

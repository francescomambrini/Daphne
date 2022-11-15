#!/usr/bin/env python

import argparse
import os
from itertools import groupby
from operator import itemgetter
from lxml import etree
import logging

# Arg parsing

parser = argparse.ArgumentParser()
parser.add_argument("xmlfile", type=str, help="path to a tb file in xml format")
parser.add_argument("-e", "--edition", required=False,
                    help="path to a TEI edition; if not provided, path is guessed from xml file")
args = parser.parse_args()
e = args.edition
if not args.edition:
    e = args.xmlfile.replace("/annotation/latest/", "/texts/data/")
    e = e.replace('daphne_tb', 'daphne')
if not os.path.isfile(e):
    raise FileNotFoundError("File {} not found. Try to pass the path with the -e option".format(e))

r, f = os.path.split(e)

# TEI file
ns = {'tei' : 'http://www.tei-c.org/ns/1.0'}

txt = etree.parse(e)
tei_lines = txt.xpath("//tei:l/text()", namespaces=ns)

# Treebank
cpath = args.xmlfile
tb = etree.parse(cpath)
_toks = [(w.attrib['form'], w.attrib.get('cite', '---').split('-')[0])
           for w in tb.xpath("//word") if not w.attrib.get("insertion_id")]

groups = groupby(_toks, itemgetter(1))
tb_toks = [" ".join([item[0] for item in data]) for (key, data) in groups]

# now we glue them
# assert len(tei_sents) == len(tb_sents), "Nr. of sents does not correspond ({} tb vs {} tei)".format(len(tb_sents),
#                                                                                                    len(tei_sents))

if len(tei_lines) != len(tb_toks):
    logging.warning("Nr. of sents does not correspond ({} tb vs {} tei)".format(len(tb_toks),
                                                                      len(tei_lines)))
#    with open("error_sents.txt", "w") as out:
#        for s in tei_sents:
#            out.write(s + "\n")
#    raise ValueError("Nr. of sents does not correspond ({} tb vs {} tei)".format(len(tb_sents),
#                                                                                                    len(tei_sents)))

else:
    logging.info("Proceeding to compare the sents")

with open("comparison.txt", "w") as out:
    for tb_s, tei_s in zip(tb_toks, tei_lines):
        out.write(f"{tb_s}\n{tei_s}\n\n")

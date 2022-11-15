#!/usr/bin/env python

import argparse
import os
from capitain_corpus_reader import CapitainCorpusReader
from lxml import etree
from nltk.tokenize.punkt import PunktLanguageVars, PunktSentenceTokenizer


class NewAncientGreekPunktVar(PunktLanguageVars):
    # note that there are two middle dots:
    # \u00b7 and \u0387!

    sent_end_chars = ("\u0387","·",'.', ';', ":", "#")
    _re_non_word_chars = r"(?:[\";\*:@\'··])"


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

r,f = os.path.split(e)

# TEI file
txt = CapitainCorpusReader(r,f, sent_tokenizer=PunktSentenceTokenizer(lang_vars=NewAncientGreekPunktVar()))
tei_sents = [" ".join(s).replace("ʼ", "'") for s in txt.sents(f)]

# Treebank
cpath = args.xmlfile
tb = etree.parse(cpath)
tb_sents = []
for s in tb.xpath("//sentence"):
    tks = [t.attrib.get("form") for t in s.xpath("word") if not t.attrib.get("insertion_id")]
    tb_sents.append(" ".join(tks))

# now we glue them
# assert len(tei_sents) == len(tb_sents), "Nr. of sents does not correspond ({} tb vs {} tei)".format(len(tb_sents),
#                                                                                                    len(tei_sents))

if len(tei_sents) != len(tb_sents):
    print("Nr. of sents does not correspond ({} tb vs {} tei)".format(len(tb_sents),
                                                                                                        len(tei_sents)))
#    with open("error_sents.txt", "w") as out:
#        for s in tei_sents:
#            out.write(s + "\n")
#    raise ValueError("Nr. of sents does not correspond ({} tb vs {} tei)".format(len(tb_sents),
#                                                                                                    len(tei_sents)))

else:
    print("Proceeding to compare the sents")

with open("comparison.txt", "w") as out:
    for tb_s, tei_s in zip(tb_sents, tei_sents):
        out.write(f"{tb_s}\n{tei_s}\n\n")

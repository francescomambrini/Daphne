import argparse
import os
from capitain_corpus_reader import CapitainCorpusReader
import pyconll

# Arg parsing

parser = argparse.ArgumentParser()
parser.add_argument("conll", type=str, help="path to a tb file in conllu format")
parser.add_argument("-e", "--edition", required=False,
                    help="path to a TEI edition; if not provided, path is guessed from conllu file")
args = parser.parse_args()
e = args.edition
if not args.edition:
    e = args.conll.replace("/annotation/", "/texts/data/")
    e = e.replace("_tb-grc1.conllu", "-grc1.xml")
if not os.path.isfile(e):
    raise FileNotFoundError("File {} not found. Try to pass the path with the -e option".format(e))

r,f = os.path.split(e)

# TEI file
txt = CapitainCorpusReader(r,f)
tei_sents = [" ".join(s).replace("ʼ", "'") for s in txt.sents(f)]

# Treebank
cpath = args.conll
tb = pyconll.iter_from_file(cpath)
tb_sents = []
for s in tb:
    tks = [t.form for t in s if not t.misc.get("type")]
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

from capitain_corpus_reader import CapitainCorpusReader
import pyconll

# TEI file
r = "/home/francesco/cltk_data/greek/text/canonical-greekLit-master/data"
f = "tlg0011/tlg001/tlg0011.tlg001.perseus-grc2.xml"
txt = CapitainCorpusReader(r, f)
tei_sents = [" ".join(s).replace("ʼ", "'") for s in txt.sents(f)]

# Treebank
tb = pyconll.iter_from_file("/home/francesco/Documents/work/Nextcloud/Documents/Projects/Daphne/data/annotation/tlg0011/tlg001/tlg0011.tlg001.daphne_tb-grc1.conllu")
tb_sents = []
for s in tb:
    tks = [t.form for t in s if not t.misc.get("type")]
    tb_sents.append(" ".join(tks))

# now we glue them
assert len(tei_sents) == len(tb_sents), "Nr. of sents does not correspond ({} tb vs {} tei)".format(len(tb_sents),
                                                                                                    len(tei_sents))

with open("Trach.txt", "w") as out:
    for tb_s, tei_s in zip(tb_sents, tei_sents):
        out.write(f"{tb_s}\n{tei_s}\n\n")

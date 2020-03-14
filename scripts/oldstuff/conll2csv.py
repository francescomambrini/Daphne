import pyconll
import pyCTS

abbr = "tlg0011tlg001"
c = pyconll.load_from_file("../data/annotation/tlg0011/tlg001/tlg0011.tlg001.daphne_tb-grc1.conllu")
tok_urn_base = f"urn:cite2:daphne:{abbr}tokens.v1:"
sent_urn_base = f"urn:cite2:daphne:{abbr}sentences.v1:"

sents = []
toks = []

for s in enumerate(c, start=1):
    sentid = tok_urn_base + "s"
    sent = "{}"
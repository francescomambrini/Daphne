"""
CAREFUL!!! This version of the script works only the first CoNLL-U files I generated,
the ones with the dependency to the artificials recorded in the DEPS column.
The way it works is that it searches if there are DEPS, and if it finds them, it uses them to override the DEPREL

"""

import pyconll
import os
from lxml import etree
# import datetime
import string


input_file = os.path.abspath("../data/v1/tlg0011/tlg0011.tlg001.perseus-grc2.tb_EDIT.conllu")

assert os.path.isfile(input_file), "File not found!"

def _is_artificial(token):
    if token.misc.get("type") == {"Artificial"}:
        return True


def _find_cite(conll_sent, reverse=False):
    sent = conll_sent
    if reverse:
        sent = conll_sent[::-1]
    for tok in sent:
        cite = tok.misc.get("cite")
        if cite:
            return list(cite)[0]


def get_xml_head_rel(t):
    """
    Checks if the token has deps; if it does, returns them, if it doesn't returns the regular head, deprel couple
    :param t: the conll token
    :return: tuple (head, relation)
    """
    if not t.deps:
        return t.head, t.deprel
    else:
        head = list(t.deps.keys())[0]
        rel = t.deps[head][0]
        return head, rel


def set_subdoc(sent):
    def split_urn(urn, first=True):
        passage = urn.split(":")[-1]
        if first:
            return passage.split("-")[0]
        else:
            return passage.split("-")[-1]

    first_urn = _find_cite(sent)
    last_urn = _find_cite(sent, reverse=True)
    return "{}-{}".format(split_urn(first_urn), split_urn(last_urn))


# Load the template
tbx = etree.parse("lib/treebank_template.xml")
root = tbx.getroot()
# find the date element and update it with the current time
# date_el = root.find("date")
# date_el.text = dt

# now load the conll file and loop through it
c = pyconll.load_from_file(input_file)
doc_id = "urn:cts:greekLit:{}:daphne_tb-grc1".format(c[0].meta_value("newdoc id"))
for sent_i, sent in enumerate(c, start=1):
    sel = etree.SubElement(root, "sentence")
    sel.set("id", str(sent_i))
    sel.set("document_id", doc_id)
    sel.set("subdoc", set_subdoc(sent))
    insert_index = 4
    last_tok_id = 0
    for wi, tok in enumerate(sent, start=1):
        wel = etree.SubElement(sel, "word")
        wel.set("id", str(wi))
        # all nodes have: 1. form, relation, head
        wel.set("form", tok.form)
        head, rel = get_xml_head_rel(tok)
        wel.set("head", head)
        wel.set("relation", rel)
        if _is_artificial(tok):
            wel.set("artificial", "elliptic")
            insert = str(last_tok_id).zfill(4) + string.ascii_lowercase[insert_index]
            wel.set("insertion_id", insert)
            insert_index += 1
        else:
            wel.set("lemma", tok.lemma)
            wel.set("postag", tok.xpos)
            last_tok_id += 1
        cite = tok.misc.get("cite")
        if cite:
            wel.set("cite", list(cite)[0])

fname = os.path.basename(input_file)
outname = os.path.splitext(fname)[0] + ".xml"

# pretty print does not seem to work, so we'll do it home-made...
x = etree.tostring(tbx, xml_declaration=True, encoding="UTF-8").decode("utf8")
xstr = x.replace("/>", "/>\n")

with open(outname, "w") as out:
    out.write(xstr)

#tbx.write(outname, pretty_print=True, xml_declaration=True, encoding='UTF-8')

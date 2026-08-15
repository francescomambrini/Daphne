#!/usr/bin/env python

"""Convert files in the AGLDT format into RDF triples
Change the configurations in lib/config.ini

"""

# URN schema :

from rdflib import Graph, URIRef, Namespace, BNode, Literal, RDF, RDFS
from collections import defaultdict
from lxml import etree
import configparser
import os

config = configparser.ConfigParser()
config.read("lib/config.ini")

auth = config.get("CTS", "textgroup")
tit = config.get("CTS", "work")
version = config.get("GENERAL", "version")
# parser = argparse.ArgumentParser()
# parser.add_argument("treebank", type=str,
#                    help="an XML treebank file")
# parser.add_argument("-n", "--namespace", type=str,
#                    help="namespace for the treebank", required=True)
# parser.add_argument("-g", "--greek", action="store_true",
#                    help="use for Greek; otherwise, Latin is assumed")
# args = parser.parse_args()


tok_urn_base = f"urn:cite2:daphne:{auth}{tit}_tokens.v{version}:"
sent_urn_base = f"urn:cite2:daphne:{auth}{tit}_sentences.v{version}:"

def add_triple(s, p, o, graph):
    graph.add( (s,p,o) )


tbsent = Namespace("https://github.com/francescomambrini/Daphne/id/treebank/" + sent_urn_base)
tbtok = Namespace("https://github.com/francescomambrini/Daphne/id/treebank/" + tok_urn_base)
cts = Namespace("http://cite-architecture.org/")

lemon = Namespace("http://lemon-model.net/lemon#")
lemlat_base = Namespace("http://lila-erc.eu/data/ontologies/lemlat-base#")
nif = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
powla = Namespace("http://purl.org/powla/powla.owl#")
conll = Namespace("http://ufal.mff.cuni.cz/conll2009-st/task-description.html#")
ldt = Namespace("https://perseusdl.github.io/treebank_data/docs/guidelines/")


g = Graph()

g.bind("daphne", Namespace("https://github.com/francescomambrini/Daphne/id/treebank/"))
g.bind("nif", nif)
g.bind("conll", conll)
g.bind("powla", powla)
g.bind("agldt", ldt)
g.bind("cts", cts)


path = config.get("FILE", "path")
x = etree.parse(path)


def _is_artificial(w_el):
    if "artificial" in w_el.attrib.keys():
        return True
    else:
        return False


def _build_defdic(els):
    """
    Takes a list of lmxl element; returns a defaultdic with index and element.
    Useful to get next sentence or next word.

    :param els: list of xml elements (sentence or word)
    :return: difaultdict with None if key not found

    """
    df = defaultdict(lambda : None)
    for i,s in enumerate(els):
        df[i] = s
    return df


def _get_literal(el, prop):
    return Literal(el.attrib[prop])


def _get_uri(el, prop):
    try:
        uri = URIRef(el.attrib[prop])
    except KeyError:
        uri = None
    return uri

sents = x.xpath("//sentence")
sentdic = _build_defdic(sents)

for i,s in enumerate(sents, start=1):
    sid = "s" + str(i) + "_0"
    add_triple(tbsent[sid], RDF.type, nif.Sentence, g)
    add_triple(tbsent[sid], RDF.type, powla.Root, g)
    nextsent = sentdic[i+1]
    if nextsent is not None:
        nextid = "s" + str(i+1) + "_0"
        add_triple(tbsent[sid], nif.nextSentence, tbsent[nextid], g)

    add_triple(tbsent[sid], ldt["document_id"], Literal(s.attrib["document_id"]), g)
    add_triple(tbsent[sid], ldt["subdoc"], Literal(s.attrib["subdoc"]), g)
    add_triple(tbsent[sid], conll["ID"], Literal(i), g)

    # take care of words
    words = s.xpath("word")
    wdics = _build_defdic(words)
    for wi, w in enumerate(words, start=1):
        # small sanity check:
        if wi != int(w.attrib["id"]):
            print("warning! word {} in sent {} does not match with sequential order ({})").format(
                w.attrib["id"], i, wi)

        wid = "s" + str(i) + "_" + str(wi)

        # Do the following for every token, real or artificial
        headid = "s" + str(i) + "_" + w.attrib["head"]
        head = tbtok[headid]
        add_triple(tbtok[wid], powla.hasRoot, tbsent[sid], g)
        add_triple(tbtok[wid], conll.HEAD, head, g)
        add_triple(tbtok[wid], conll.EDGE, _get_literal(w, "relation"), g)
        add_triple(tbtok[wid], conll.ID, _get_literal(w, "id"), g)
        add_triple(tbtok[wid], conll.WORD, _get_literal(w, "form"), g)

        # add CTS URN if there is one
        urn = _get_uri(w, "cite")
        if urn:
            add_triple(tbtok[wid], cts["ctsurn"], urn, g)

        # add next word if there's one
        nextword = wdics[wi + 1]
        if nextword is not None:
            nextwid = "s" + str(i) + "_" + str(wi + 1)
            add_triple(tbtok[wid], powla.next, tbtok[nextwid], g)
            if _is_artificial(w) == False and _is_artificial(nextword) == False:
                add_triple(tbtok[wid], nif.nextWord, tbtok[nextwid], g)

        if _is_artificial(w):
            add_triple(tbtok[wid], RDF.type, powla.Nonterminal, g)
        else:
            add_triple(tbtok[wid], RDF.type, nif.Word, g)
            add_triple(tbtok[wid], RDF.type, powla.Terminal, g)
            add_triple(tbtok[wid], conll.LEMMA, _get_literal(w, "lemma"), g)
            add_triple(tbtok[wid], conll.XPOS, _get_literal(w, "postag"), g)



doc = os.path.split(path)[-1]
docname = os.path.splitext(doc)[0]
out = docname + ".ttl"

g.serialize(destination=out, format="turtle")

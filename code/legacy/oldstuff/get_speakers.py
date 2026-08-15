from rdflib import Graph, URIRef, Namespace, BNode, Literal, RDF, RDFS
import pyconll
import configparser
import os

config = configparser.ConfigParser()
config.read("lib/config.ini")

auth = config.get("CTS", "textgroup")
tit = config.get("CTS", "work")
version = config.get("GENERAL", "version")
sent_urn_base = f"urn:cite2:daphne:{auth}{tit}_sentences.v{version}:"
path = config.get("FILE", "path")

c = pyconll.load_from_file(os.path.splitext(path)[0] + ".conllu")

tbsent = Namespace("https://github.com/francescomambrini/Daphne/id/treebank/" + sent_urn_base)
daphne_mod = Namespace("https://github.com/francescomambrini/Daphne/def/ontology/")

g = Graph()

g.bind("daphne", Namespace("https://github.com/francescomambrini/Daphne/id/treebank/"))
g.bind("daphmod", daphne_mod)


for i,s in enumerate(c):
    sid = "s" + str(i) + "_0"
    g.add((tbsent[sid], daphne_mod["hasSpeaker"], Literal(s.meta_value("speaker"))))

doc = os.path.split(path)[-1]
docname = os.path.splitext(doc)[0]
out = docname + "_speakers.ttl"

g.serialize(destination=out, format="turtle")

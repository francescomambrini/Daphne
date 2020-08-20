#!/usr/bin/env python

"""Requires Python 3.6+ (with the `lxml` library).

Compares a TEI digital edition (e.g. from Perseus) with a treebank file of a Greek 
tragedy or commedy, and attempts to extract the speaker tag for each sentence.
The list of speakers is output to a tab-separated file with the format:

        SentenceID {tab} Subdoc Element {tab} Speaker label 

Note that, as Perseus records the speakers in Greek, so are the extracted labes.

Usage instructions:
    python extract_speaker.py --help

"""

# coding: utf-8
from lxml import etree
import os
import argparse
import logging

# Arg parsing

parser = argparse.ArgumentParser()
parser.add_argument("teifile", type=str, help="path to the edition file in TEI format")
parser.add_argument("treebank", type=str, help="path to a tb file in xml format")
parser.add_argument("-d", "--debug", default=False, action='store_true',
                    help="turn on the debug logging (very verbose)")
parser.add_argument("-o", "--output", required=False,
                    help="output file")
args = parser.parse_args()

outf = args.output if args.output else "speakers.csv"

# Logging
if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)

logging.debug(f'Output will be written to {outf}')

x = etree.parse(args.teifile)
ns = {"tei" : "http://www.tei-c.org/ns/1.0"}
ls = x.xpath("//tei:l", namespaces=ns)

#load the treebank
tb = etree.parse(args.treebank)
sents = tb.xpath("//sentence")

firstcts = []
for s in sents:
    # we loop over the tokens until we find a suitable word with a cite element;
    # the first word is usually good, but not always (e.g. with trailing parentheses)
    for w in s:
        # sometimes trailing parentheses are tokenized with the following sentence;
        # thus, we make sure that the cite el is taken from actual words, not punctuation
        if w.attrib.get('postag', '---')[0] == 'u':
            continue
        else:
            try:
                c = w.attrib["cite"].split(":")[-1]
                break
            except KeyError:
                continue
    firstcts.append( (c.split("-")[0], s.attrib.get('id'), s.attrib.get('subdoc')) )

# Let us make sure that we have exactly one cite element per sentence    
assert len(firstcts) == len(sents), \
            f"Number of sentences {len(sents)} and Nr of speakers {len(firstcts)} do not correspond!"

speakers = ["SentID\tSubdoc\tSpeaker\n"]
for c,sid,subdoc in firstcts:
    try:
        e = [l for l in ls if l.attrib["n"] == c.split("-")[0]][0]
    except IndexError:
        # TO DO: we might introduce a --strict flag to raise an error, 
        # instead of forcing the script to write something
        logging.error(f"CTS passage {c} not found: writing 'UNKNOWN' to output")
        e = None
    
    if args.debug:
        logging.debug(f"working with line\t{c}")
    if e is not None:
        sp = e.xpath("preceding-sibling::tei:speaker", namespaces=ns)[0].text
    else:
        sp = 'UNKNOWN'
    
    speakers.append(f"{sid}\t{subdoc}\t{sp}\n")
    

with open(outf, "w") as out:
    for sp in speakers:
        out.write(sp)

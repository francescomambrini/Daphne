#!/usr/bin/env python
"""
Add the speaker metadata to each sentence in a CoNLL-U file, starting from a 
CSV file with the speaker list. The CSV file must be structured so that:
- it has a header in line 1, then 1 sentence per line after the first
- it has the same nr of sentences as the CoNLL-U
- the speaker value to be added is in the *last* column

Writes a new CoNLL-U file, in the current working dir, with the same name 
as the original CoNLL-U, unless an output path is explicitely set.
"""

import csv
import conllu
import argparse
import os
import sys

parser = argparse.ArgumentParser()

parser.add_argument("conllu", type=str, help='path to the conllu file')
parser.add_argument("csv", type=str, help='path to a CSV file with list of speaker')
parser.add_argument("-o", "--output", type=str, 
                    help="path of output file", 
                    required=False)

args = parser.parse_args()

with open(args.conllu) as f:
    sents = conllu.parse(f.read())

with open(args.csv) as f:
    reader = csv.reader(f, delimiter='\t')
    lines = [l for l in reader][1:]

if len(sents) != len(lines):
    raise ValueError(f'Unequal nr. of sentences in CSV ({len(lines)}) and CoNLL-U ({len(sents)})')
    sys.exit(1)

out_conllu = ''

for s, l in zip(sents, lines):
    s.metadata['Speaker'] = l[-1]
    out_conllu += s.serialize()

out_path = args.output if args.output else os.path.basename(args.conllu)
print(f'writing output at: {os.path.abspath(out_path)}')

with open(out_path, 'w') as out:
    out.write(out_conllu)

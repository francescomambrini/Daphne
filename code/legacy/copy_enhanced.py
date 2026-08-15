#!/usr/bin/env python

"""
Simple script that goes token by token trhough a CoNLL-U file and, whenver it finds an empty DEPS column, 
just copies the DEPREL to it.

CAREFUL! it overwrites the file!!!
"""

import sys
import conllu

fpath = sys.argv[1]

with open(fpath) as f:
    data = f.read()

sentences = conllu.parse(data)
for s in sentences:
    for t in s:
        if not t['deps']:
            t['deps'] = [(t['deprel'], t['head'])]
        else:
            if len(t['deps']) == 1 and t['deps'][0][1] == 'ref':
                t['deps'].append((t['deprel'], t['head']))


file_content = ''.join([s.serialize() for s in sentences])
with open(fpath, 'w') as out:
    out.write(file_content)

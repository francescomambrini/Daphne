#!/usr/bin/env python3

"""
Usage:
    run_depedit.py ini_file conllu_folder
"""

from depedit import DepEdit
import argparse
import os
import sys
from glob import glob

with open(sys.argv[1]) as f:
    deped = DepEdit(f)

pth = os.path.join(os.path.abspath(sys.argv[2]), '*.conllu')
docs = glob(pth)
for doc in docs:
    bname, ext = os.path.splitext(doc)
    outname = f'{bname}_depedit{ext}'
    with open(doc) as f:
        result = deped.run_depedit(f)
    with open(outname, 'w') as out:
        out.write(result)

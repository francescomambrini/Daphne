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
    print(doc)
    infile = open(doc)
    result = deped.run_depedit(doc)

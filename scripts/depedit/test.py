#!/usr/bin/env python
import sys
import os
from glob import glob
from depedit import DepEdit
import argparse


pth = os.path.join(os.path.abspath(sys.argv[1]), '**/*.conllu')
docs = glob(pth, recursive=True)
print(len(docs))
for doc in docs:
    print(doc)

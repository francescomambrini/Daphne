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
import shutil
from tqdm import tqdm

with open(sys.argv[1]) as f:
    print('opening')
    deped = DepEdit(f)

print('done opening')

pth = os.path.join(os.path.abspath(sys.argv[2]), '**/*.conllu')
docs = glob(pth, recursive=True)
print(len(docs))
for doc in tqdm(docs):
    # bname, ext = os.path.splitext(doc)
    # outname = f'{bname}_depedit{ext}'
    bakname = f'{doc}.bak'
    with open(doc) as f:
        result = deped.run_depedit(f)
    
    # copy the original as *.conllu.bak
    shutil.copyfile(doc, bakname)

    # write the new file with the name of the original
    with open(doc, 'w') as out:
        out.write(result)

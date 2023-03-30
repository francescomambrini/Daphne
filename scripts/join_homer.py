from natsort import natsorted
import os
from glob import glob
import conllu
import sys

text = 'tlg0012/tlg001'
outname = 'iliad.conllu'
dir = 'data/annotation/latest/' + text

script_dir = os.path.abspath(os.path.dirname(__file__))
pths= glob(os.path.join(script_dir, '..', dir, '*.conllu'))
fs = natsorted(pths)
global_sents = ''
for pth in fs:
    with open(pth) as f:
        sents = conllu.parse(f.read())
    for sent in sents:
        global_sents += sent.serialize()

with open(os.path.join(script_dir, '..', dir, outname), 'w') as out:
    out.write(global_sents)

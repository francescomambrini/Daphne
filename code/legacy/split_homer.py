"""Split a large Iliad/Odyssey files into units of 6 books

Usage:
-----
    split_homer.py path/to/hom/file
"""

import sys
import os
from tqdm import tqdm
import conllu

pth = sys.argv[1]

begins = [7, 13, 19]

newsents = ''
hom_dir = os.path.dirname(os.path.abspath(pth))

# tlg0012.tlg002.perseus-grc1.1-6.tb.conllu

with open(pth) as f:
    bk_beg = 1
    sents = conllu.parse(f.read())
    for sent in tqdm(sents):
        bk_end = bk_beg + 5
        rng = range(bk_beg, bk_end +1)
        # print(sent.metadata['sent_id'])
        # refs = [t['misc'].get('Ref') for t in sent if t['misc'].get('Ref')]
        for t in sent:
            try:
                refs = t['misc']['Ref']
                break
            except (TypeError, KeyError):
                continue
        bk = int(refs.split('.')[0])
        if bk in rng:
            newsents += sent.serialize()
        else:
            outname = f'tlg0012.tlg001.perseus-grc1.{bk_beg}-{bk_end}.tb.conllu'
            outpth = os.path.join(hom_dir, outname)
            with open(outpth, 'w') as out:
                out.write(newsents)
            bk_beg = bk
            newsents = sent.serialize()
    
    outname = f'tlg0012.tlg001.perseus-grc1.{bk_beg}-{bk_end}.tb.conllu'
    outpth = os.path.join(hom_dir, outname)
    with open(outpth, 'w') as out:
        out.write(newsents)

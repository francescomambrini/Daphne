"""
Sometimes a duplicated version of DEPS remain in the 9th column, where the node is wrongly
assigned to the same head with different labels; the first one usually duplicates the values
in the regural deprel. Arborator rightly complains about that. We fix it here.

"""

import conllu
import sys
import os

i = sys.argv[1]

with open(i) as f:
    sents = conllu.parse(f.read())

for s in sents:
    for t in s:
        d = t['deps'] 
        if d and len(d) > 1:
            if d[0][1] == d[1][1]:
                del(d[0])

fname = os.path.basename(i)

with open(os.path.expanduser(f'~/Desktop/{fname}'), 'w') as out:
    for s in sents:
        out.write(s.serialize())

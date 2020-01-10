#!/usr/bin/env python
import argparse
from collections import namedtuple
from capitain_corpus_reader import CapitainCorpusReader
from capitain_corpus_reader.tokenize import PerseusTreebankTokenizer

parser = argparse.ArgumentParser()
parser.add_argument("fname", help="file name (relative path from root)")
parser.add_argument("-r", "--root", action="store_true",
                    help="root of the corpus", default="../data/texts/data")
parser.add_argument('-c', '--include_cite', action="store_true", help="include canonical citations")
args = parser.parse_args()


def _to_conll09(sentences, include_cite=False):
    """Transforms sentence list (each sentence a list of tokens) into a conll09-like tabular file.

    Parameters
    ----------
    sentences : iter
        a list/iterable of sentences. Each sentence is a list of tokens; each token might be a string or a tuple
        (tok,anno1,anno2,anno_n...)

    Returns
    -------
    str : a conll09-like tabular representation of the sentences
    """
    Token = namedtuple('Token', ['form', 'lemma', 'pos', 'cite'])
    cite = '_'
    txt = ''
    for s in sentences:
        for idx, w in enumerate(s, start=1):
            form = w[0]
            if isinstance(w, str):
                w = (w,)
            if include_cite:
                cite = w[0]
                form = w[1]
            # postag = "".join([ l +'|' for l in t.pos]).rstrip("|")
            t = Token(form, '_', '_', cite)
            # ID FORM LEMMA PLEMMA POS PPOS FEAT PFEAT HEAD PHEAD DEPREL PDEPREL FILLPRED PRED APREDs
            txt += f"{idx}\t{t.form}\t{t.lemma}\t_\t{t.pos[0]}\t_\t{t.pos}\t_\t_\t_\t_\t_\t_\t_\t{t.cite}\n"
        txt += "\n"
    return txt


r = args.root
f = args.fname
cite = args.include_cite
tbtok = PerseusTreebankTokenizer()
c = CapitainCorpusReader(r, f, word_tokenizer=tbtok)
fid = c.fileids()[0]
print(f'Working on: {fid}')

if cite:
    sents = c.cite_sents(fid)
else:
    sents = c.sents(fid)

conll = _to_conll09(sents, cite)
with open("out.conll", 'w') as out:
    out.write(conll)

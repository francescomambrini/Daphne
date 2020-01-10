#!/usr/bin/env python

import sys
import pyconll

c = pyconll.load_from_file(sys.argv[1])

def get_subdoc(sent):
    cites = [list(w.misc.get("cite"))[0] for w in sent if w.misc.get("cite")]
    ls = [c.split(":")[-1] for c in cites]
    return "{}-{}".format(ls[0], ls[-1])

with open("speakers.csv", "w") as out:
    out.write("SentID\tSubdoc\tSpeaker\n")
    for i,s in enumerate(c, 1):
        speak = s.meta_value("speaker")
        sub = get_subdoc(s)
        out.write(f"{i}\t{sub}\t{speak}\n")


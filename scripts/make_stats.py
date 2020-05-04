#!/usr/bin/env python

from glob import glob
import os
from lxml import etree


if __name__ == '__main__':
    tbdir = os.path.dirname(os.path.abspath(__file__))
    pth = os.path.join(tbdir, "../data/annotation/v*/*/*/tlg*.xml")
    tbs = sorted(glob(pth))
    s = """# Statistics

| Author    | Title  | Sentences | Tokens (tot) | Artificial    |
| ----------| -------| ---------:| ------------:|--------------:| 
"""
    for tb in tbs:
        auth, tit = os.path.basename(tb).split(".")[:2]
        x = etree.parse(tb)
        len_s = len(x.xpath("//sentence"))
        len_w = len(x.xpath("//word"))
        len_art = len(x.xpath("//word[@insertion_id]"))
        s += f'|{auth}\t|{tit}\t|{len_s}\t|{len_w}\t|{len_art}\t|\n'

    with open("../statistics.md", 'w') as out:
        out.write(s)

"""
Attempts to fix the annotation (syntax and pos) of ὡς
"""

from udapi.core.block import Block
import logging


def _check(conditions):
    return all(conditions)


class FixHos(Block):

    @staticmethod
    def is_prep(node):
        return _check((node.deprel == 'AuxP',))

    @staticmethod
    def is_head_of_clause(node):
        advs = [n for n in node.children if n.deprel == 'ADV']
        for a in advs:
            if a.misc['NodeType'] == 'Artificial':
                return True
            if a.xpos[0] == 'v' and a.xpos[4] != 'p':
                return True

    @staticmethod
    def is_with_part(node):
        parentpostag = node.parent.xpos if node.parent.xpos != '_' else '_________' 
        conds = (not node.children,
                 node.parent.xpos[0] in ['v', 'p'],
                 parentpostag[4] == 'p',
                 node.deprel == 'AuxY')
        return _check(conds)

    @staticmethod
    def is_auxy(node):
        conds = (not node.children,
                 node.parent.xpos[0] in ['n', 'a', 'm', 'd', 'r'],
                 node.deprel == 'AuxY')
        return _check(conds)

    def process_node(self, node):
        if node.lemma == 'ὡς':
            logging.info(f'Found ὡς: {node.address()}')
            if self.is_prep(node):
                node.xpos = 'r--------'
                node.deprel = 'AuxP'
            elif self.is_head_of_clause(node):
                node.xpos = 'c--------'
                node.deprel = 'AuxC'
            elif self.is_with_part(node):
                node.xpos = 'c--------'
                node.deprel = 'AuxY'
            elif self.is_auxy(node):
                node.xpos = 'd--------'
                node.deprel = 'AuxY'


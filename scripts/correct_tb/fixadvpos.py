from udapi.core.block import Block


class FixAdvPos(Block):
    """
    If an adverb is syntactically annotated as preposition, then
    it's a preposition!
    If it behaves as a conjuncion, it's a conjunction!
    """

    def process_node(self, node):
        if node.xpos[0] == 'd':
            if node.deprel == 'AuxP':
                node.xpos = "r--------"
            elif node.deprel == 'AuxC':
                node.xpos = 'c--------'

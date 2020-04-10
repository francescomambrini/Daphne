from udapi.core.block import Block


class FixSomeLex(Block):
    """
    Fix known problems with some words here and there; like e.g.:
    - αἰθήρ feminine not masculine in Aeschylus
    - οἰκτίρω as lemma, not οἰκτείρω
    etc.
    """
    def process_node(self, node):
        tag = node.xpos

        # fix orthography of lemma
        if node.lemma == 'οἰκτείρω':
            node.lemma = 'οἰκτίρω'
        elif node.lemma == 'σώζω':
            node.lemma = 'σῴζω'
        elif node.lemma == 'ἀικής':
            node.lemma = 'ἀεικής'
        elif node.lemma == 'ὀσφύς':
            node.lemma = 'ὀσφῦς'
        elif node.lemma == 'ὅπη':
            node.lemma = 'ὅπῃ'
        elif node.lemma == 'πάτρη':
            node.lemma = 'πάτρα'
        elif node.lemma == 'ταὐτός':
            node.lemma = 'αὐτός'
        elif node.lemma == 'πῆ' :
            node.lemma = 'πῇ'

        # fix some gender
        elif node.lemma == 'αἰθήρ' and tag[-3] == 'm' :
            node.xpos = f'{tag[:-3]}f{tag[-2:]}'
        elif node.lemma == 'ὁδός' and tag[-3] == 'm' :
            node.xpos = f'{tag[:-3]}f{tag[-2:]}'

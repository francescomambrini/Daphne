from udapi.core.block import Block


class FixEisComp(Block):
    """
    I am now convinced that οὐδείς and μηδείς must be tagged as pronouns
    """

    def process_node(self, node):
        if node.lemma in ['οὐδείς ', 'μηδείς']:
            node.xpos = f'p{node.xpos[1:]}'

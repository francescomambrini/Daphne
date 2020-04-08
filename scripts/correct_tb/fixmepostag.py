from udapi.core.block import Block


class FixMePostag(Block):
    def process_node(self, node):
        checks = (node.lemma == 'μή',
                  node.deprel == 'AuxZ',
                  node.xpos[0] in ['g', 'c'])

        if all(checks):
            node.xpos = f'd{node.xpos[1:]}'

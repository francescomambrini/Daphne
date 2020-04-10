from udapi.core.block import Block
import logging


class FixMePostag(Block):
    def process_node(self, node):
        checks = (node.lemma == 'μή',
                  node.deprel == 'AuxZ',
                  node.xpos[0] in ['g', 'c'])

        if all(checks):
            logging.info(f'Changing μή in {node.address()}')
            node.xpos = f'd{node.xpos[1:]}'

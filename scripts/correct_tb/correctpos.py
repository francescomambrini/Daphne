from udapi.core.block import Block
from udapi.block.agldt.createupos import parts, dets


dets.remove('ὁ')

class CorrectPos(Block):
    def process_node(self, node):
        if node.lemma in dets and node.xpos[0] != 'd':
            node.xpos = f'p{node.xpos[1:]}'
        if node.xpos[0] == 'g':
            node.xpos = f'd{node.xpos[1:]}'

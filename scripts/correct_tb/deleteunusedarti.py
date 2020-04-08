from udapi.core.block import Block
import logging


def check(node):
    checks = (node.misc['NodeType'] == 'Artificial',
              node.deprel == '',
              node.parent.ord == 0,
              not node.descendants)
    return all(checks)

class DeleteUnusedArti(Block):
    def process_tree(self, root):
        for node in root.descendants:
            if check(node):
                logging.warning(f"Deleting node {node.address()}")
                node.remove(children="rehang")

from udapi.core.block import Block
import re

class FixCrasis(Block):
    """
    Simlpy deletes the trailing hyphen '-' from the crasis form
    """
    
    def _is_krasis(self, node):
        reg = re.compile(r'^[κχ]-$')
        if reg.search(node.form):
            return True
        return False
        
    def process_node(self, node):
        if self._is_krasis(node):
            node.form = node.form[0]

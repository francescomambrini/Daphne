from udapi.core.block import Block
import logging


def agree(node1, node2):
    def get_gennumcas(s):
        return f'{s[2]}{s[6]}{s[7]}'
    try:
        n1 = get_gennumcas(node1.xpos)
        n2 = get_gennumcas(node2.xpos)
    except IndexError:
        logging.warning(f"No comparison possible between nodes {node1.address()} and {node2.address()}")
        return False
        
    if n1 == n2:
        return True
    return False



class FixArticle(Block):
    """
    If article is tagged as `p` but is syntactically an ATR and agrees with parent, 
    then it's a `l`
    """
    def process_node(self, node):
        if node.lemma == 'ὁ' and node.xpos[0] == 'p':
            if node.deprel == 'ATR':
                parent = node.parent
                if agree(node, parent):
                    node.xpos = f'l{node.xpos[1:]}'
                    
                

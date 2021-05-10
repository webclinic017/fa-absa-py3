"""General helper functions when working with portfolios

We can simply create a tree structure using only dicts and not asigning any values,
all is handled by recursive defaultdict structure.

Example usage of a Tree class represented as recursive defaultdict dictionary:

tree = Tree()
tree['ABSA BANK LTD']['ABSA CAPITAL']['PRIMARY MARKETS TRADING']
tree['ABSA BANK LTD']['ABSA CAPITAL']['SECONDARY MARKETS TRADING']
tree['ABSA BANK LTD']['GROUP TREASURY']['GROUP TREASURY BANKING']
tree['ABSA BANK LTD']['GROUP TREASURY']['GROUP TREASURY TRADING']
tree['CLIENT REPORTING']['PB_CR_LIVE']
tree['CLIENT REPORTING']['PB_CR_CALC']
tree['CLIENT REPORTING']['PB_CR_NONZAR']

we can also simply add new items to the tree:
    add(tree, 'BAGL,BAGL FX,Hedges'.split(','))

where 'add' function might be:
    def add(t, keys):
        for key in keys:
            t = t[key]

"""
from collections import defaultdict


class Tree(defaultdict):
    """Class representing a tree structure"""

    def __init__(self, *args):
        defaultdict.__init__(self, lambda: Tree(self))

    def has(self, node):
        if self.get(node) is not None:
            return True
        return False

    def get(self, node):
        if node in self:
            return self[node]

        for key in self:
            item = self[key].get(node)
            if item is not None:
                return item

        return None

    def to_dict(self):
        return dict((key, self[key].to_dict()) for key in self)


def create_tree(portfolio):
    """Recurive function to generate portfolio tree.

    Arguments:
    portfolio -- acm compound portfolio instance

    """
    tree = Tree()
    if hasattr(portfolio, 'SubPortfolios'):
        for child in portfolio.SubPortfolios():
            tree[child.Name()] = create_tree(child)
    return tree


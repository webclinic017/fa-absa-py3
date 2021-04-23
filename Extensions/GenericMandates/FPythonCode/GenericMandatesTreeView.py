"""
Python module that contains the functionality required to tree view. This is useful for
displaying mandate information.
"""


import acm
import FUxCore


OP_NODE = {0: 'AND', 1: 'OR'}
ATTR_NODE = {0: '=', 1: '=', 2: '<', 3: '>', 4: '<=', 5: '>=', 6: '*', 7: '<>'}

RGB_RED = 255
RGB_GREEN = 65200
RGB_WHITE = 16250871


class DialogTreeView (FUxCore.LayoutDialog):
    def __init__(self, trade, queryFolders):
        """
        List of FASQLQueryFolders

        :param trade: FTrade
        :param queryFolders: list
        """
        self.tree = 0
        self.dialog = None
        self.trade = trade
        self.queryFolders = queryFolders

    def HandleApply(self):
        return 1

    def HandleCreate(self, dlg, layout):
        """
        Built-in AEF method that is overwritten with custom functionality.
        :param dlg: FUxDialog
        :param layout: FUxLayoutBuilder
        """
        self.dialog = dlg
        self.dialog.Caption('Mandates that were breached')
        self.tree = layout.GetControl('tree')

        self.tree.ShowColumnHeaders()
        self.tree.AddColumn("Pass / Fail", 280)
        self.tree.ColumnLabel(0, "Name")
        self.tree.AddColumn("", 20)
        self.tree.ColumnLabel(0, "Name")
        self.tree.ColumnWidth(0, 450)

        treeRoot = self.tree.GetRootItem()

        for folder in self.queryFolders:
            # Set the name of the Query Folder node
            treeChild = treeRoot.AddChild()
            treeChild.Label(folder.Name())

            for node in folder.Query().AsqlNodes():
                self.AddNode(node, treeChild, self.trade)

        # self.ExpandAll(treeRoot)

    def AddNode(self, nodes, tree, trade):
        """
        Add a node to the tree view.
        :param nodes: FASQLAttr / FASQLOperator
        :param tree:
        :param trade: FTrade
        """
        if 'AsqlNodes' in dir(nodes):
            for node in nodes.AsqlNodes():
                if isinstance(nodes, type(acm.FArray())):
                    # FArray of asqlNodes
                    for n in node:
                        self.AddNode(n, tree, trade)

                elif 'AsqlNodes' in dir(node):
                    child = tree.AddChild()
                    child.Label("%s" % OP_NODE[node.AsqlOperator()])
                    for n in node.AsqlNodes():
                        self.AddNode(n, child, trade)
                else:
                    child = tree.AddChild()
                    # Attribute Nodes
                    if self.CheckNode(node, trade) is False:
                        child.Label("%s %s %s" % (node.AsqlAttribute().AttributeString(),
                                                  ATTR_NODE[node.AsqlOperator()],
                                                  node.AsqlValue()))
                        methodChain = node.AsqlAttribute().AttributeString()
                        method = acm.FMethodChain(acm.FSymbol(methodChain))
                        child.Label("%s" % method.Call([trade]), 1)
                        child.Style(0, True, 0, RGB_WHITE)
                        child.Style(1, True, 0, RGB_WHITE)
                        child.Style(2, False, 0, RGB_RED)
                    else:
                        child.Label("%s %s %s" % (node.AsqlAttribute().AttributeString(),
                                                  ATTR_NODE[node.AsqlOperator()],
                                                  node.AsqlValue()))
                        child.Label("OK", 1)
                        child.Style(2, False, 0, RGB_GREEN)
                        if node.AsqlAttribute().AttributeString().Text() == "Instrument.InsType":
                            tree.Expand()
        else:
            node = nodes
            child = tree.AddChild()
            # Attribute Nodes
            if self.CheckNode(node, trade) is False:
                child.Label("%s %s %s" % (node.AsqlAttribute().AttributeString(),
                                          ATTR_NODE[node.AsqlOperator()],
                                          node.AsqlValue()))
                methodChain = node.AsqlAttribute().AttributeString()
                method = acm.FMethodChain(acm.FSymbol(methodChain))
                child.Label("%s" % method.Call([trade]), 1)
                child.Style(0, True, 0, RGB_WHITE)
                child.Style(1, True, 0, RGB_WHITE)
                child.Style(2, False, 0, RGB_RED)
            else:
                child.Label("%s %s %s" % (node.AsqlAttribute().AttributeString(),
                                          ATTR_NODE[node.AsqlOperator()],
                                          node.AsqlValue()))
                child.Label("OK", 1)
                child.Style(2, False, 0, RGB_GREEN)
                if node.AsqlAttribute().AttributeString().Text() == "Instrument.InsType":
                    tree.Expand()

    def CheckNode(self, attributeNode, trade):
        """
        Check if a specific node "rule" passes or fails for a specific trade.
        :param attributeNode: array
        :param trade: FTrade
        :return: bool
        """
        folder = acm.FASQLQueryFolder()
        folder.Name('Temp folder')
        query = acm.CreateFASQLQuery('FTrade', 'OR')
        query.AddOpNode('OR')
        query.AddAttrNode(attributeNode.AsqlAttribute().AttributeString(), attributeNode.AsqlOperator(),
                          attributeNode.AsqlValue())
        folder.AsqlQuery(query)
        return folder.Query().IsSatisfiedBy(trade)

    def ExpandAll(self, root):
        """
        Expand all the nodes in the tree view.
        :param root:
        :return:
        """
        for node in root.Children():
            node.Expand()
            if node.Children() > 0:
                self.ExpandAll(node)


def _Spacer(depth):
    return "    " * depth


def GetNodeInfo(nodes, depth, text, criteria):
    if 'AsqlNodes' in dir(nodes):
        for node in nodes.AsqlNodes():
            if isinstance(nodes, type(acm.FArray())):
                for n in node:
                    GetNodeInfo(n, depth, text, criteria)

            elif 'AsqlNodes' in dir(node):
                if len(node.AsqlNodes()) > 1:
                    text.append("%s[%s]" % (_Spacer(depth), OP_NODE[node.AsqlOperator()]))
                    depth += 1
                for n in node.AsqlNodes():
                    GetNodeInfo(n, depth, text, criteria)
            else:
                text.append("%s %s %s" % (node.AsqlAttribute().AttributeString(),
                                          ATTR_NODE[node.AsqlOperator()],
                                          node.AsqlValue()))

    else:
        attribute = '%s' % nodes.AsqlAttribute().AttributeString()
        if attribute in criteria.keys():
            criteria[attribute] += ', %s' % nodes.AsqlValue()
        else:
            criteria[attribute] = '%s' % nodes.AsqlValue()

        text.append("%s%s %s %s" % (_Spacer(depth), nodes.AsqlAttribute().AttributeString(),
                                    ATTR_NODE[nodes.AsqlOperator()], nodes.AsqlValue()))
        return text, criteria


def CreateTreeViewDialogLayout():
    """
    Create the GUI layout for this dialog.
    :return: FUxLayoutBuilder
    """
    b = acm.FUxLayoutBuilder()
    b.BeginHorzBox('None')
    b.  BeginVertBox('None')
    b.          AddTree("tree", 800, 400)
    b.          BeginHorzBox('None')
    b.                  AddFill()
    b.          EndBox()
    b.  EndBox()
    b.EndBox()
    return b

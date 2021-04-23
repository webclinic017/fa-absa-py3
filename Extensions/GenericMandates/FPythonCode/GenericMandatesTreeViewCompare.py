"""
Python module that contains the functionality required to tree view. This is useful for
displaying mandate information.
"""


import acm
import FUxCore

from GenericMandatesLogger import getLogger
from GenericMandatesAuthorizationCore import EVENT_PARAMETER_REJECTION_REASON, EVENT_PARAMETER_REJECTION_USER, \
    StateChartAuthorizationProcess


OP_NODE = {0: 'AND', 1: 'OR'}
ATTR_NODE = {0: '=', 1: '=', 2: '<', 3: '>', 4: '<=', 5: '>=', 6: '*', 7: '<>'}

RGB_RED = 255
RGB_GREEN = 65200
RGB_WHITE = 16250871


class DialogTreeViewCompare (FUxCore.LayoutDialog):
    def __init__(self, attributesLeft, attributesRight, businessProcess, comment, readOnly):
        """
        Create the dialog that compares two query folders to each other and produces a visual comparison.
        :param attributesLeft: dict
        :param attributesRight: dict
        :param businessProcess: FBusinessProcess
        :param comment: string
        :param readOnly: bool
        :return:
        """
        self._readOnly = readOnly
        self.treeLeft = 0
        self.treeRight = 0
        self._btnAccept = None
        self._btnReject = None
        self.dialog = None
        self.layout = None
        self._shell = acm.UX().SessionManager().Shell()
        self._bp = businessProcess

        self.attributesLeft = attributesLeft
        self.queryFoldersLeft = attributesLeft['queries']
        self.attributesRight = attributesRight
        self.queryFoldersRight = attributesRight['queries']
        self._comment = comment
        self.txtComment = None

    def HandleApply(self):
        return True

    def _AddAttributes(self, nodeLeft, nodeRight):

        categoryNodeLeft = nodeLeft.AddChild()
        categoryNodeLeft.Label('Mandate - Attributes')
        categoryNodeRight = nodeRight.AddChild()
        categoryNodeRight.Label('Mandate - Attributes')

        for key in self.attributesLeft.keys():
            if key not in ['queries']:
                attributeNodeLeft = categoryNodeLeft.AddChild()
                attributeNodeRight = categoryNodeRight.AddChild()
                attributeNodeLeft.Label('%s = %s' % (key, self.attributesLeft[key]))
                attributeNodeRight.Label('%s = %s' % (key, self.attributesRight[key]))
                if self.attributesLeft[key] != self.attributesRight[key]:
                    attributeNodeLeft.Style(0, True, 0, RGB_WHITE)
                    attributeNodeRight.Style(0, True, 0, RGB_WHITE)
                    attributeNodeLeft.Style(2, False, 0, RGB_RED)
                    attributeNodeRight.Style(2, False, 0, RGB_RED)
                else:
                    attributeNodeLeft.Style(2, False, 0, RGB_GREEN)
                    attributeNodeRight.Style(2, False, 0, RGB_GREEN)

    def _AddQueryFolders(self, node, queryFolders):
        queryNodeLeft = node.AddChild()
        queryNodeLeft.Label('Query Folders')

        for folder in queryFolders:
            # Set the name of the Query Folder node
            treeChild = queryNodeLeft.AddChild()
            treeChild.Label(folder.Name())

            for node in folder.Query().AsqlNodes():
                self.AddNode(node, treeChild, None)

    def HandleCreate(self, dlg, layout):
        """
        Built-in AEF method that is overwritten with custom functionality.
        :param dlg: FUxDialog
        :param layout: FUxLayoutBuilder
        """

        # Set dialog caption
        self.dialog = dlg
        self.layout = layout
        self.dialog.Caption('Proposed Mandate changes')
        self.treeLeft = layout.GetControl('treeLeft')
        self.treeRight = layout.GetControl('treeRight')
        self.txtComment = layout.GetControl('txtComment')
        self.txtComment.SetData(self._comment)
        self.txtComment.Editable(False)

        # Create columns (A)
        self.treeLeft.ShowColumnHeaders()
        self.treeLeft.ColumnLabel(0, "Existing Mandate")
        self.treeLeft.ColumnWidth(0, 460)
        self.treeLeft.AddColumn("Proposed Mandate", 10)
        self.treeLeft.AddColumn(" ", 20)

        # Create columns (B)
        self.treeRight.ShowColumnHeaders()
        self.treeRight.ColumnLabel(0, "Proposed Mandate")
        self.treeRight.ColumnWidth(0, 460)
        self.treeRight.AddColumn("Proposed Mandate", 10)
        self.treeRight.AddColumn(" ", 20)

        # Find root item
        rootLeft = self.treeLeft.GetRootItem()
        rootRight = self.treeRight.GetRootItem()

        # Add Mandate attributes to tree
        self._AddAttributes(rootLeft, rootRight)

        # Add query folders
        self._AddQueryFolders(rootLeft, self.queryFoldersLeft)
        self._AddQueryFolders(rootRight, self.queryFoldersRight)
        self.ExpandAll(rootLeft)
        self.ExpandAll(rootRight)

        # Add button callback methods
        self._btnAccept = layout.GetControl('btnAccept')
        self._btnAccept.AddCallback('Activate', self._OnClickAccept, None)

        self._btnReject = layout.GetControl('btnReject')
        self._btnReject.AddCallback('Activate', self._OnClickReject, None)

        if self.__IsAuthApplicable() is False or self._readOnly is True:
            self._btnAccept.Enabled(False)
            self._btnReject.Enabled(False)

    def AddNode(self, nodes, tree, trade):
        """
        Add a node to the tree view.
        :param nodes: FASQLAttr / FASQLOperator
        :param tree:
        :param trade: FTrade
        """
        if 'AsqlNodes' in dir(nodes) and nodes.AsqlNodes():
            for node in nodes.AsqlNodes():
                if type(nodes) is type(acm.FArray()):
                    # FArray of asqlNodes
                    for n in node:
                        self.AddNode(n, tree, trade)

                elif 'AsqlNodes' in dir(node):
                    child = tree.AddChild()
                    child.Label("%s" % OP_NODE[node.AsqlOperator()])
                    for n in node.AsqlNodes():
                        self.AddNode(n, child, trade)
                elif 'AsqlAttribute' in dir(node):
                    child = tree.AddChild()
                    # Attribute Nodes
                    child.Label("%s %s %s" % (node.AsqlAttribute().AttributeString(),
                                              ATTR_NODE[node.AsqlOperator()],
                                              node.AsqlValue()))
        else:
            node = nodes
            if 'AsqlAttribute' in dir(node):
                child = tree.AddChild()
                # Attribute Nodes
                child.Label("%s %s %s" % (node.AsqlAttribute().AttributeString(),
                                          ATTR_NODE[node.AsqlOperator()],
                                          node.AsqlValue()))

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

    def _OnClickAccept(self, *params):
        del params
        getLogger().debug('OnClickAccept() executing')

        self._bp.HandleEvent(StateChartAuthorizationProcess.EVENT_APPROVE)
        self._bp.Commit()
        self.dialog.CloseDialogOK()

    def _OnClickReject(self, *params):
        del params
        getLogger().debug('OnClickReject() executing')

        dialogCaption = "Capture rejection reason"
        initialComment = "My reason for rejecting the authorization process."
        reason = acm.UX().Dialogs().GetTextInput(self._shell, dialogCaption, initialComment)

        if reason and len(reason) > 0:

            # A reason was supplied
            parameters = acm.FDictionary()
            parameters.AtPut(EVENT_PARAMETER_REJECTION_REASON, reason)
            parameters.AtPut(EVENT_PARAMETER_REJECTION_USER, acm.FACMServer().User().Name())

            self._bp.HandleEvent(StateChartAuthorizationProcess.EVENT_DENY, parameters)
            self._bp.Commit()
            acm.UX().Dialogs().MessageBoxInformation(self._shell, 'The requested mandate change was denied '
                                                                  'successfully.')
            self.dialog.CloseDialogOK()
        elif reason and len(reason) == 0:
            # No reason was supplied - display a notification
            acm.UX().Dialogs().MessageBoxInformation(self._shell, 'No reason was supplied. The Authorization will not '
                                                                  'be rejected. \nPlease try again.')

    def __IsAuthApplicable(self):
        """
        Check if the Accept & Reject buttons should be enabled.
        :return: bool
        """
        if 'StateChart' in dir(self._bp):
            if self._bp.StateChart().Name() == StateChartAuthorizationProcess.NAME:
                validEvents = self._bp.CurrentStep().ValidEvents()
                setA = {'Reject', 'Approve'}
                setB = {event.Name() for event in validEvents}
                if setA <= setB:
                    return True
        return False


def CreateTreeViewDialogLayout():
    """
    Create the GUI layout for this dialog.
    :return: FUxLayoutBuilder
    """
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.  BeginHorzBox('EtchedIn', 'Proposed mandate changes')
    b.    BeginHorzBox('None')
    b.      BeginHorzBox('None')
    b.          AddTree("treeLeft", 500, 400)
    b.          BeginHorzBox('None')
    b.                  AddFill()
    b.          EndBox()
    b.      EndBox()
    b.      BeginHorzBox('None')
    b.          AddTree("treeRight", 500, 400)
    b.          BeginHorzBox('None')
    b.                  AddFill()
    b.          EndBox()
    b.      EndBox()
    b.    EndBox()
    b.  EndBox()

    b.  BeginHorzBox('EtchedIn', 'Comment provided for change')
    b.    AddFill()
    b.    AddText('txtComment', 1020, 100, 1020)
    b.  EndBox()

    b.  BeginHorzBox('None')
    b.    AddButton("btnAccept", "Accept")
    b.    AddButton("btnReject", "Reject")
    b.    AddButton("cancel", "Cancel")
    b.  EndBox()
    b.EndBox()

    return b

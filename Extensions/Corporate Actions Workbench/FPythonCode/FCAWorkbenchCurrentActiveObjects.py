""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCAWorkbenchCurrentActiveObjects.py"
"""--------------------------------------------------------------------------
MODULE
    FCAWorkbenchCurrentActiveObjects

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm

from FHandler import Handler
from FIntegratedWorkbenchUtils import IsKindOf
from FIntegratedWorkbenchLogging import logger
from FEvent import EventCallback
from FCorporateActionsWorkbenchEvent import OnCorporateActionSelected
from FCorporateActionsWorkbenchEvent import OnCorporateAction


def getPositionInstance(methodChainValueDict):

    definitions, values = list(zip(*[(methodChain.lstrip('Trade.'), value)
                    for methodChain, value in methodChainValueDict.iteritems()]))
                        
    attributeQuery = acm.CreateFASQLQuery(acm.FPositionAttribute, 'AND')
    attributeQuery.AddAttrNodeEnum('Definition.Definition', definitions)
    attributeSet = attributeQuery.Select()
    
    attributeOids = [attr.Oid() for attr in attributeSet]

    positionQuery = acm.CreateFASQLQuery(acm.FCalculationRow, 'AND')
    positionQuery.AddAttrNodeEnum('Attributes.Oid', attributeOids)
    positionSet = positionQuery.Select()

    for pos in positionSet:
        attrsSize = pos.Attributes().Size()
        if attrsSize > len(methodChainValueDict):
            continue
        attrs = pos.Attributes()
        for j in range(0, attrsSize):
            methodChain = 'Trade.' + attrs[j].Definition().Definition()
            if attrs[j].AttributeValue() != methodChainValueDict[methodChain]:
                break
            if j == attrsSize - 1:
                return pos
    return None


def insertCAChoices(corpActions=None):
    q = acm.CreateFASQLQuery(acm.FCorporateActionChoice, 'AND')
    if corpActions:
        op = q.AddOpNode('OR')
        op.AddAttrNode('Name', 'EQUAL', None)
        op = q.AddOpNode('OR')
        for i in corpActions:
            op.AddAttrNode('CorpAction.Name', 'EQUAL', i)

    return q


def getPortfolioSheetGrouperValues(currentRow):
    groupingDict = {}
    while currentRow.Parent():
        if currentRow.IsKindOf(acm.FMultiInstrumentAndTrades):
            key = currentRow.GrouperOnLevel().MethodCollection()[0].Text()
            groupingDict[key] = currentRow.StringKey()
        currentRow = currentRow.Parent()
    return groupingDict


class CurrentActiveObjects(Handler):

    def __init__(self, dispatcher):
        super(CurrentActiveObjects, self).__init__(dispatcher)
        self._corporateActions = []
        self._corporateActionsStatus = []
        self._corporateActionElections = []
        self._portfolios = []
        self._trades = []
        self._treeItems = []

    @EventCallback
    def OnCorporateActionSelected(self, event):            
        self._corporateActions = [o for o in event.Objects()]
        self._corporateActionsStatus = [o.Status() for o in event.Objects()]
        self._corporateActionElections[:] = []
        self._portfolios[:] = []
        self._trades[:] = []

    @EventCallback
    def OnCorporateActionElectionSelected(self, event):
        self._corporateActionElections = [o for o in event.Objects()]
        self._portfolios[:] = []
        self._trades[:] = []

    @EventCallback
    def OnCorporateAction(self, event):
        ca = event.Parameters()[0]
        idx = -1
        for selectedCA in self._corporateActions:
            if selectedCA.Oid() == ca.Oid():
                idx = self._corporateActions.index(selectedCA)
                break
        if idx != -1:
            if self._corporateActionsStatus[idx] != ca.Status():
                if ca.Status() != 'None' and self._corporateActionsStatus[idx] != 'None':
                    self.SendEvent(OnCorporateActionSelected(self, self._corporateActions))
                self._corporateActionsStatus[idx] = ca.Status()
        
    @EventCallback
    def OnPortfolioSelected(self, event):
        self._portfolios = [o for o in event.Objects()]

    @EventCallback
    def OnTradeSelected(self, event):
        self._trades = [o for o in event.Objects()]
    
    @EventCallback
    def OnTreeItemSelected(self, event):
        self._treeItems = [o for o in event.Objects()]

    def CorporateActions(self):
        return self._corporateActions
        
    def CorporateActionElections(self):
        return self._corporateActionElections

    def Portfolios(self):
        return self._portfolios

    def Trades(self):
        return self._trades

    def TreeItems(self):
        return self._treeItems

    def CorporateAction(self):
        return self._corporateActions[0] if self._corporateActions else None
        
    def CorporateActionElection(self):
        return self._corporateActionElections[0] if self._corporateActionElections else None

    def Portfolio(self):
        return self._portfolios[0] if self._portfolios else None

    def Trade(self):
        return self._trades[0] if self._trades else None

    def TreeItem(self):
        return self._treeItems[0] if self._treeItems else None

    def election_ael_variables_updater(self, ael_variables):
        
        corporateAction = self.CorporateAction()
        corporateActionElection = self.CorporateActionElection()
        trade = self.Trade()
        portfolio = self.Portfolio()
        
        if corporateAction:
            ael_variables.CaChoice.default_value = insertCAChoices([corporateAction.Name()])
        else:
            ael_variables.CaChoice.default_value = insertCAChoices()

        ael_variables.Position.default_value = None
        if portfolio:
            gdict = getPortfolioSheetGrouperValues(portfolio)
            posInstance = getPositionInstance(gdict)
            if posInstance:
                ael_variables.Position.default_value = posInstance.Oid()

    def choice_ael_variables_updater(self, ael_variables):
        corporateAction = self.CorporateAction()        
        if corporateAction:
            ael_variables.CorpAction.default_value = corporateAction

    def payout_ael_variables_updater(self, ael_variables):
        treeItem = self.TreeItem()
        if treeItem and treeItem.IsKindOf(acm.FCorporateActionChoice):
            ael_variables.CaChoice.default_value = treeItem

    def ElectionDeleted(self):
        self.SendEvent(OnCorporateActionSelected(self, self._corporateActions))
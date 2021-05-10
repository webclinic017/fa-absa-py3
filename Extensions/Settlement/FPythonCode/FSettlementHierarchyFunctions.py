""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementHierarchyFunctions.py"
import acm
from   FSettlementCommitter import SettlementCommitter, CommitAction
import FSettlementNetting
from   FSettlementEnums import SettlementStatus

#-------------------------------------------------------------------------
def DecideParentsForChildren(firstChildren, secondChildren, oldParent):
    committerListTemp  = list()
    cleanUp = list()
    okParent = None
    problematicParent = None
    if len(firstChildren) > 1:
        okParent = oldParent
        committerListTemp.append(SettlementCommitter(okParent, CommitAction.UPDATE))
    if len(firstChildren) > 1 and len(secondChildren) > 1:
        problematicParent = acm.FSettlement()
        problematicParent.Apply(oldParent)
        committerListTemp.append(SettlementCommitter(problematicParent, CommitAction.INSERT))
    elif len(secondChildren) > 1:
        problematicParent = oldParent
        committerListTemp.append(SettlementCommitter(problematicParent, CommitAction.UPDATE))
    if len(firstChildren) < 2 and len(secondChildren) < 2:
        cleanUp.append(SettlementCommitter(oldParent, CommitAction.DELETE))
    return okParent, problematicParent, committerListTemp, cleanUp

#-------------------------------------------------------------------------
def CreateNetHierarchy(netParent, children, committerList):
    topSettlement = None
    if netParent:
        FSettlementNetting.SetNetParentData(netParent, children, netParent.NettingRule())
        for child in children:
            child.Parent(netParent)
            committerList.append(SettlementCommitter(child, CommitAction.UPDATE))
        topSettlement = netParent
    else:
        if children:
            RemoveFromNetting(children[0], committerList)
            topSettlement = children[0]
    return topSettlement

#-------------------------------------------------------------------------
def FilterOutSettlementsByTrade(settlements, listOfTrades):
    wrongSettlements = list()
    okSettlements = list()
    for settlement in settlements:
        if settlement.Trade() not in listOfTrades:
            wrongSettlements.append(settlement)
        else:
            okSettlements.append(settlement)
    return okSettlements, wrongSettlements

#-------------------------------------------------------------------------
def RemoveFromNetting(settlement, committerList):
    settlement.Status(SettlementStatus.AUTHORISED)
    settlement.Parent(None)
    committerList.append(SettlementCommitter(settlement, CommitAction.UPDATE))
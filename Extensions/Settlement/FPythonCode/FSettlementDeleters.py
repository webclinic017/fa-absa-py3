""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementDeleters.py"
from   FSettlementCommitter import SettlementCommitter, CommitAction

#-------------------------------------------------------------------------
# Settlement deletion functions 
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
def DeleteHierarchy(settlement, committerList):
    committerList.append(SettlementCommitter(settlement, CommitAction.DELETE))
    for child in settlement.Children():
        DeleteHierarchy(child, committerList)
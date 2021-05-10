""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementMatcher.py"
import FSettlementUtils as SettlementUtils

class SettlementMatcher(object):

    def __init__(self, oldList, newList):
        ''' SettlementMatcher init method. '''

        self.__oldList = oldList
        self.__newList = newList
        self._matchedSettlementsList = []
        self.__InitMatchedSettlementsList()
        
    def __InitMatchedSettlementsList(self):
        ''' Initialize the lists. '''

        #new -> old
        for newSettlement in self.__newList:
            self._SetSettlementPair(newSettlement, self.__oldList)
            
        #old -> new
        for oldSettlement in self.__oldList:
            if SettlementUtils.IsWithinTimeWindow(oldSettlement):
                self._matchedSettlementsList.append((oldSettlement, None))
    
    def _SetSettlementPair(self, settlement, settlementList):
        ''' SetSettlementPair '''

        foundSettlement = None
        for s in settlementList:
            if (s.Type() == settlement.Type() and
                s.SplitTypeChlItem() == settlement.SplitTypeChlItem() and
                s.RelationType() == settlement.RelationType() and
                s.Trade() == settlement.Trade()):
                if s.IsSameReferenceOid(settlement):
                    foundSettlement = s
                    settlementList.remove(s)
                    break
                else:
                    if settlement.HasDividendCashFlowPaymentReference():
                        #Continue the search. settlementList may contain settlement records of a
                        #type that should have a cash flow reference but do not.
                        #As an example a coupon without cash flow reference due to a rolling 
                        #period change and in post released status.
                        pass
                    else:
                        foundSettlement = s
                        settlementList.remove(s)
                        break
        self._matchedSettlementsList.append((foundSettlement, settlement))
    
    def GetMatchedSettlementsList(self):
        ''' Public method. Return matched settlement lists. '''

        return self._matchedSettlementsList

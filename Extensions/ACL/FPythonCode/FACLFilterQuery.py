""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLFilterQuery.py"
import acm

class FACLFilterQuery():
    def __init__(self, queryName, callbacks = None):
        self._query = self._getQuery(queryName)
        self._callbacks = callbacks
        if not self._callbacks:
            self._callbacks = DefaultFilterCallbacks()
    
    def EvaluateQuery(self, previous, current):
        includedBefore = self._query.IsSatisfiedBy(previous)
        includedAfter = self._query.IsSatisfiedBy(current)
        
        if includedBefore:
            if includedAfter:
                # Included -> Included
                return self._callbacks.OnIncludeToInclude(previous, current)
            else:
                # Included -> Excluded
                return self._callbacks.OnIncludeToExclude(previous, current)
        else:
            if includedAfter:
                # Excluded -> Included
                return self._callbacks.OnExcludeToInclude(previous, current)
            else:
                # Excluded -> Excluded
                return self._callbacks.OnExcludeToExclude(previous, current)
    
    def SelectTradesByInstrumentName(self, instrumentName):
        ins = acm.FInstrument[instrumentName]
        trades = ins.Trades().Filter(self._query)
        
        return trades.SortByProperty('Oid', True) 
        
    def Query(self):
        return self._query
    
    def _getQuery(self, queryName):
        query = None
        if queryName:
            storedQuery = acm.FStoredASQLQuery[queryName]
            if storedQuery and storedQuery.Query():
                query = storedQuery.Query()
            else:
                raise Exception('Could not find a query named: ' + queryName)
        else:
            query = acm.CreateDefaultFASQLQuery(acm.FTrade)
        
        return query
    
class MtMQueryHelper:
    SecurityInstrumentTypes = ['Bond', 'Bill', 'BondIndex', 'CD', 'CLN', 'Deposit', 'FRN', 'FreeDefCF', \
    'IndexLinkedBond', 'PromisLoan', 'Zero', 'Commodity', 'CreditIndex', 'Depositary Receipt', \
    'EquityIndex', 'Stock', 'ETF']


    @staticmethod
    def _queryAggregate(query):
        queryAggregate = query.AddOpNode('AND')
        queryAggregate.AddAttrNode('Type', 'EQUAL', 'Aggregate')
        queryAggregate.AddAttrNode('Type', 'EQUAL', 'FX Aggregate')
        queryAggregate.AddAttrNode('Type', 'EQUAL', 'Static Aggregate')
        queryAggregate.Not(True)
        return query
    
    @staticmethod    
    def CreateQuery(filterQuery):
        query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        query = MtMQueryHelper._queryAggregate(query)
        tradeQuery = acm.Filter.CompositeAndQuery(acm.FTrade, filterQuery, query)
        return tradeQuery
    
    @staticmethod
    def Expired(trade):
        expiryDate = None
        
        if trade.IsFxSwapNearLeg():
            trade = acm.FX.GetSwapFarTrade(trade)
            expiryDate = trade.ValueDay()
        elif MtMQueryHelper._isFx(trade) or MtMQueryHelper._isSecurity(trade):
            expiryDate = trade.ValueDay()
        else:
            expiryDate = trade.Instrument().ExpiryDate()
        
        return acm.Time.DateDifference(acm.Time.DateToday(), expiryDate) >= 0
    
    @staticmethod
    def _isFx(trade):
        return trade.IsFxForward() or trade.IsFxSpot() or trade.IsFxSwapFarLeg() or trade.IsFxSwapNearLeg()
    
    @staticmethod
    def _isSecurity(trade):
        return trade.Instrument().InsType() in MtMQueryHelper.SecurityInstrumentTypes
    @staticmethod
    def HasIssuer(trade):
        if MtMQueryHelper._isSecurity(trade):
            return trade.Instrument().Issuer() != None
        return True
    
class DefaultFilterCallbacks:
    def OnIncludeToInclude(self):
        pass
    
    def OnIncludeToExclude(self):
        pass
    
    def OnExcludeToInclude(self):
        pass
    
    def OnExcludeToExclude(self):
        pass
            

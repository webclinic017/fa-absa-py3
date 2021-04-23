"""-----------------------------------------------------------------------------
PURPOSE   :  General FX functions

Date         Who                        What
    
2011-03-04   Paul Jacot-Guillarmod      CR 591682: Changed the logic in how the isExercised function determines whether a trade has been exercised or not.  Previous version was causing problems because 
of incorrect contract numbers.

2011-04-13   Paul Jacot-Guillarmod      CR628466: Updated the isExercised function to determine whether a position has been exercised and not just a single trade.

2012-04-05 Bhavnisha Sarawan CR: Added function to get the underlying exercised trade ID.
-----------------------------------------------------------------------------"""

import acm, ael

def SettlementCurrGet(self):
    currencyStr = self.AdditionalInfo().Settlement_Curr()
    if currencyStr:
        return acm.FCurrency[currencyStr]
    return None
    
def SettlementCurrSet(self, curr):
    if curr:
        currencyStr = curr.Name()
    else:
        currencyStr = None
    self.AdditionalInfo().Settlement_Curr(currencyStr)



def GetFxOptionType(self):
    if self.InsType() == 'Option':

        if self.IsBarrier():

            return 'Barrier'

        if self.Digital():

            return 'Digital'

        return 'Vanilla'
    else:
        return 'None'



def date_compare(objectx, objecty):   
    if objectx.Date() > objecty.Date():
         return 1
    else: return -1
    
def get_event(ins):
    today = acm.Time.DateNow()
    events = ins.GetExoticEventsOfKind('Barrier date')
    l = len(events)
    if l == 1: 
        return events.At(0)
    elif l == 0:
        return None
    else:
        if ins.Exotic().BarrierMonitoring() == 'Discrete':
            d = [e for e in events if e.Date() >= today]
            d.sort(date_compare)
            return d[0]
        else:
            d = []
            for e in events:
                if e.Date() <= today  and e.Date() >= today:
                    return e
                if e.Date() > today:
                    d.append(e)
            if len(d) > 0:
            
                d.sort(date_compare)

                return d[0]
            
    return None

def _FilterMatchingTrades(trade):
    ''' Return all the trades that are linked to the same instrument and have 
        the same counterparty and portfolio.
    '''
    instrument = trade.Instrument()
    portfolio = trade.Portfolio().Name()
    counterParty = trade.Counterparty().Name()
    trades = []
    for trd in [t for t in instrument.Trades() if t.Status() not in ['Void', 'Simulated']]:
        if (trd.Portfolio().Name() == portfolio
            and trd.Counterparty().Name() == counterParty):
            trades.append(trd)
    return trades

def _GetExercisedTrade(trade):
    ''' Return the exercised trade for a position.  The exercised trade for a position
        is a trade with a Type that is not Normal. 
    '''
    for trd in _FilterMatchingTrades(trade):
        if trd.Type() != 'Normal':
            return trd
    return None

def exercisedTradeId(trade, *rest):
    ''' If a position has been exercised return the trade number of the exercised trade.
    '''
    exercisedTrade = _GetExercisedTrade(trade)
    if exercisedTrade:
        return str(exercisedTrade.Oid())
        
def isExercised(trade, *rest):
    ''' When a position is exercised a new equal and opposite trade is generated to
        close out the position.  This trade can be identified because its trade 
        Type is not Normal.  We decide on whether a position has been exercised by
        verifying the existence of an exercised trade.
    '''
    exercisedTrade = _GetExercisedTrade(trade)
    if exercisedTrade:
        return 'Exercised'
    else:
        return 'Not Exercised'

def exercisedUnderlyingTradeId(trade):
    isEx = isExercised(trade)
    if isEx == 'Exercised':
        tr = acm.FTrade[trade.Oid()]
        if tr.Type() == 'Normal':
            try:
                tradeQuery = acm.CreateFASQLQuery(acm.FTrade, 'AND')
                tradeQuery.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'Curr'))
                tradeQuery.AddAttrNode('ContractTrdnbr', 'EQUAL', tr.Oid())
                for trade in tradeQuery.Select():
                    return trade.Oid()
            except:
                pass
    

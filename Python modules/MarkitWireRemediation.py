import acm
import FOperationsUtils as Utils
from at_email import EmailHelper

#Inter-desk mirror trades
def UpdatePrimeMirror(tradeRef, mirrorRef):
    try:
        if mirrorRef and tradeRef:
            tradeRef.MirrorTrade(mirrorRef)
            mirrorRef.MirrorTrade(tradeRef)
            print 'Updated the mirror links on inter-desk deals successfully - Mirror:', mirrorRef.Oid(), 'Trade:', tradeRef.Oid()
            mirrorRef.Commit()
            return tradeRef
    except StandardError, e:
        print 'The following error occurred while attempting to set the mirror links', str(e)

#Get Markit Wire trades
def GetMarkitWireFrontArenaTrades(tradeDate):
    Query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    Query.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', acm.Time().DateToday())
    Query.AddAttrNode('AdditionalInfo.CCPmiddleware_id', 'NOT_EQUAL', '')
    Query.AddAttrNode('TradeTime', 'GREATER_EQUAL', tradeDate)
    
    instype = Query.AddOpNode('OR')
    instype.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', 'Swap'))
    instype.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', 'FRA'))
    
    tradestatus = Query.AddOpNode('OR')
    tradestatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'BO-BO Confirmed'))
    tradestatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'BO Confirmed'))
    tradestatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'FO Confirmed'))
    tradestatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'Terminated'))
    trades = Query.Select()
    return trades

#Inter-desk mirror trades
def GenerateQuery(Acquirer, MWTradeNumber, Counterparty):
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    
    query.AddAttrNode('Acquirer.Name', 'EQUAL', Acquirer)
    query.AddAttrNode('Counterparty.Name', 'EQUAL', Counterparty)
    query.AddAttrNode('AdditionalInfo.CCPmiddleware_id', 'EQUAL', MWTradeNumber)
    query.AddAttrNode('MirrorTrade', 'EQUAL', None)

    instype = query.AddOpNode('OR')
    instype.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', 'Swap'))
    instype.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', 'FRA'))    
    
    tradestatus = query.AddOpNode('OR')
    tradestatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'BO-BO Confirmed'))
    tradestatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'BO Confirmed'))
    tradestatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'FO Confirmed'))
    tradestatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'Terminated'))
    
    trades = query.Select()
    
    for trade in trades:
        if trade.MirrorTrade()==None:
            if trade.Status() == 'Terminated':
                return trades.First()
    
    if trades.Size() != 1:
        if trades.Size() > 1:
            print 'Error retrieving mirror trade, more than one matching trade exists'
        else:
            print 'No matching mirror trade exists'

        return None
    return trades.First()

#Inter-desk mirror trades
def DefineMirrorTrades(fTrade):
    if not fTrade.IsInfant():
        if fTrade.Status() in ('BO-BO Confirmed', 'Terminated'):
            mwTradeNr = fTrade.AdditionalInfo().CCPmiddleware_id()
            if fTrade.Acquirer().Type() == 'Intern Dept' and fTrade.Counterparty().Type() == 'Intern Dept':
                if fTrade.Acquirer().Name() == 'IRD DESK' and fTrade.Counterparty().Name()=='IRD DESK':
                    if fTrade.Portfolio().Name().find('PB_')==0:
                        fTrade.Acquirer('PRIME SERVICES DESK')
                        fTrade.Commit()
                if fTrade.Acquirer().Name() == 'PRIME SERVICES DESK' and fTrade.Counterparty().Name() == 'PRIME SERVICES DESK':
                    if fTrade.Portfolio().Name() == 'Swap Flow':
                        fTrade.Acquirer('IRD DESK')
                        fTrade.Commit()
                if 'PRIME SERVICES DESK' in [fTrade.Counterparty().Name(), fTrade.Acquirer().Name()]:
                    trd = GenerateQuery(fTrade.Counterparty().Name(), mwTradeNr, fTrade.Acquirer().Name())
                    fTrade = UpdatePrimeMirror(fTrade, trd)
                    return fTrade

def remediateMarkitWireTrades(tradeDate):
    print 'About to remediate the daily Markit Wire trades'
    trades = GetMarkitWireFrontArenaTrades(tradeDate)
    for trade in trades:
        #Inter-desk mirror trades
        DefineMirrorTrades(trade)

ael_variables = \
    [
        ['RunForDate', 'Run for date', 'string', None, acm.Time().DateToday(), 1]
    ]

def ael_main(parameters):
    remediateMarkitWireTrades(parameters['RunForDate'])

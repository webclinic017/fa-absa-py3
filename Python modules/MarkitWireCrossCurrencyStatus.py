import acm
import FOperationsUtils as Utils

def GetMarkitWireFrontArenaTrades(tradeDate):
    Query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    Query.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', acm.Time().DateToday())
    Query.AddAttrNode('AdditionalInfo.CCPmiddleware_id', 'NOT_EQUAL', '')
    Query.AddAttrNode('TradeTime', 'GREATER_EQUAL', tradeDate)
    instype = Query.AddOpNode('OR')
    instype.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', 'CurrSwap'))
    tradestatus = Query.AddOpNode('OR')
    tradestatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'BO Confirmed'))
    trades = Query.Select()
    for trade in trades:
        if trade.Status() in ('BO Confirmed'):
            print 'Setting trade', trade.Oid(), 'with status', trade.Status(), 'from ', trade.Instrument().InsType(), 'to BO-BO Confirmed status'
            try:
                trade.Status('BO-BO Confirmed')
                trade.Commit()
            except StandardError, e:
                print 'The following error occurred for the AMWI Cross Currency status remediation', str(e)

ael_variables = \
    [
        ['mwCrossCurrencyStatusSet', 'Cross Currency Date From', 'string', None, '2015-03-22', 1]
    ]

def ael_main(parameters):
    try:
        GetMarkitWireFrontArenaTrades(parameters['mwCrossCurrencyStatusSet'])
    except StandardError, e:
        print 'Cross Currency status setting script experienced the following error', str(e)
